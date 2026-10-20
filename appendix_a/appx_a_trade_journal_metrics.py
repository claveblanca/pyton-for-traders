"""appx_a_trade_journal_metrics.py -- performance and behaviour from a trade journal.

Ref: §A.3.3 (size after losing and winning streaks), §A.9.2 (the written
trade journal), §A.10.1 (loss aversion), §A.10.4 (zero-based test),
PROOF §A.13 checks 5-8.

Journal columns (CSV or the sim_trades table of code_snippets/ch14):
    trade_id, symbol, side ('long'|'short'), entry_ts, exit_ts, entry_px, exit_px,
    stop_px, target_px, size, point_value, rationale

Performance: win rate, payoff ratio, expectancy (R), profit factor, max
drawdown, longest losing streak, R-multiple distribution.
Behaviour (bias metrics):
    disposition_ratio      avg holding time of losers / winners (> 1 = loss aversion)
    stop_overrides         losses that exited beyond the planned stop (> 1.1 R)
    size_after_losses      avg risk after 2+ losses / overall avg risk (> 1 = revenge sizing)
    size_after_wins        avg risk after 2+ wins / overall avg risk (> 1 = euphoria)
    no_rationale_share     share of trades with an empty rationale
    target_cut_short       winners closed before 50% of the target distance

Usage:
    python appx_a_trade_journal_metrics.py --selftest
    python appx_a_trade_journal_metrics.py journal.csv
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd


def enrich(j: pd.DataFrame) -> pd.DataFrame:
    j = j.copy().sort_values("entry_ts").reset_index(drop=True)
    j["point_value"] = j.get("point_value", 1.0)
    sgn = np.where(j["side"] == "long", 1, -1)
    j["pnl"] = sgn * (j["exit_px"] - j["entry_px"]) * j["size"] * j["point_value"]
    j["risk"] = (j["entry_px"] - j["stop_px"]).abs() * j["size"] * j["point_value"]
    j["r"] = j["pnl"] / j["risk"]
    j["hold_h"] = (
        pd.to_datetime(j["exit_ts"]) - pd.to_datetime(j["entry_ts"])
    ).dt.total_seconds() / 3600
    j["target_progress"] = (
        sgn * (j["exit_px"] - j["entry_px"]) / (sgn * (j["target_px"] - j["entry_px"]))
    )
    win = j["pnl"] > 0
    streak = win.ne(win.shift()).cumsum()
    j["streak_len"] = win.groupby(streak).cumcount() + 1
    j["prev_streak"] = j["streak_len"].shift(1)
    j["prev_win"] = win.shift(1)
    return j


def performance(j: pd.DataFrame) -> dict:
    w, l = j[j.pnl > 0], j[j.pnl <= 0]
    eq = j["pnl"].cumsum()
    loss_runs = (j.pnl <= 0).groupby((j.pnl > 0).cumsum()).sum()
    return {
        "trades": len(j),
        "win_rate": len(w) / len(j),
        "payoff_ratio": w.pnl.mean() / -l.pnl.mean() if len(l) and len(w) else np.nan,
        "expectancy_r": j["r"].mean(),
        "profit_factor": w.pnl.sum() / -l.pnl.sum() if len(l) else np.inf,
        "max_drawdown": float((eq - eq.cummax()).min()),
        "longest_losing_streak": int(loss_runs.max()),
        "r_p10_p50_p90": tuple(np.round(j["r"].quantile([0.1, 0.5, 0.9]).values, 2)),
    }


def behaviour(j: pd.DataFrame) -> dict:
    w, l = j[j.pnl > 0], j[j.pnl <= 0]
    avg_risk = j["risk"].mean()
    after_l = j[(j.prev_win == False) & (j.prev_streak >= 2)]  # noqa: E712
    after_w = j[(j.prev_win == True) & (j.prev_streak >= 2)]  # noqa: E712
    out = {
        "disposition_ratio": (
            l.hold_h.mean() / w.hold_h.mean() if len(w) and len(l) else np.nan
        ),
        "stop_overrides": int((l["r"] < -1.1).sum()),
        "size_after_losses": (
            after_l["risk"].mean() / avg_risk if len(after_l) else np.nan
        ),
        "size_after_wins": (
            after_w["risk"].mean() / avg_risk if len(after_w) else np.nan
        ),
        "no_rationale_share": float(
            j["rationale"].fillna("").str.strip().eq("").mean()
        ),
        "target_cut_short": int((w["target_progress"] < 0.5).sum()),
    }
    out["flags"] = [
        k
        for k, bad in [
            ("loss aversion (A.10.1)", out["disposition_ratio"] > 1.3),
            ("stop overridden (A.12 check 3)", out["stop_overrides"] > 0),
            ("revenge sizing after losses (A.3.3)", out["size_after_losses"] > 1.1),
            ("euphoria sizing after wins (A.8.1)", out["size_after_wins"] > 1.1),
            ("missing written rationale (A.9.2)", out["no_rationale_share"] > 0.1),
            ("winners cut short (A.10.1)", out["target_cut_short"] > len(w) * 0.3),
        ]
        if bad
    ]
    return out


def _fmt(d: dict) -> dict:
    return {
        k: (
            round(float(v), 3)
            if isinstance(v, (float, np.floating))
            else tuple(float(x) for x in v) if isinstance(v, tuple) else v
        )
        for k, v in d.items()
    }


def selftest() -> None:
    rng = np.random.default_rng(2)
    n = 60
    entry = pd.Timestamp("2026-01-05") + pd.to_timedelta(np.arange(n) * 24, unit="h")
    win = rng.random(n) < 0.45
    r = np.where(win, rng.uniform(0.3, 3.0, n), rng.uniform(-1.6, -0.8, n))
    hold = np.where(win, 6, 30)  # losers held 5x longer
    j = pd.DataFrame(
        {
            "trade_id": range(n),
            "symbol": "MGC",
            "side": "long",
            "entry_ts": entry,
            "exit_ts": entry + pd.to_timedelta(hold, unit="h"),
            "entry_px": 100.0,
            "stop_px": 99.0,
            "target_px": 103.0,
            "size": 1,
            "point_value": 100,
            "rationale": np.where(rng.random(n) < 0.2, "", "breakout + ADX>25"),
        }
    )
    j["exit_px"] = 100 + r
    e = enrich(j)
    p, b = performance(e), behaviour(e)
    assert b["disposition_ratio"] == 5 and b["stop_overrides"] > 0
    assert "loss aversion (A.10.1)" in b["flags"]
    print(_fmt({**p, **b}))
    print("selftest OK")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("journal", nargs="?")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest or not a.journal:
        selftest()
    else:
        e = enrich(pd.read_csv(a.journal))
        print(_fmt(performance(e)))
        print(_fmt(behaviour(e)))
