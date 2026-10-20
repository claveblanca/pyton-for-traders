"""appx_a_risk_of_ruin.py -- why 2% is the rule and 5% the ceiling, by simulation.

Ref: §A.2.2 (2% working rule, 5% absolute ceiling), §A.3.3 (streaks);
Ch 5 §5.5.2 (ten losses at 2% = -18%, at 10% = -65%).

Bootstraps R-multiples (from a journal or a win-rate/payoff assumption),
compounds them at a fixed fraction of equity per trade, and reports the
probability of a 20% / 50% drawdown and the median trades to recover.

Usage:
    python appx_a_risk_of_ruin.py --selftest
    python appx_a_risk_of_ruin.py --win-rate 0.45 --payoff 2.0 --risks 0.01 0.02 0.05
    python appx_a_risk_of_ruin.py --journal journal.csv          # uses its R column logic
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd


def streak_loss(risk: float, n: int) -> float:
    """Drawdown after n consecutive full losses (Ch 5 §5.5.2)."""
    return 1 - (1 - risk) ** n


def simulate(
    r_multiples: np.ndarray,
    risk: float,
    trades: int = 200,
    paths: int = 5000,
    seed: int = 0,
) -> dict:
    rng = np.random.default_rng(seed)
    draws = rng.choice(r_multiples, size=(paths, trades), replace=True)
    equity = np.cumprod(1 + risk * draws, axis=1)
    peak = np.maximum.accumulate(np.c_[np.ones(paths), equity], axis=1)[:, 1:]
    dd = (equity / peak - 1).min(axis=1)
    rec = []
    for e, pk in zip(equity, peak):
        under = e < pk
        if under.any():
            runs = np.diff(np.r_[0, under.astype(int), 0])
            starts, ends = np.where(runs == 1)[0], np.where(runs == -1)[0]
            rec.append((ends - starts).max())
    return {
        "risk": risk,
        "p_dd_20": float((dd <= -0.20).mean()),
        "p_dd_50": float((dd <= -0.50).mean()),
        "median_max_dd": float(np.median(dd)),
        "median_terminal": float(np.median(equity[:, -1])),
        "median_longest_underwater_trades": float(np.median(rec)) if rec else 0.0,
    }


def r_from_assumption(win_rate: float, payoff: float, n: int = 1000) -> np.ndarray:
    k = int(round(win_rate * n))
    return np.r_[np.full(k, payoff), np.full(n - k, -1.0)]


def table(r: np.ndarray, risks=(0.01, 0.02, 0.05), **kw) -> pd.DataFrame:
    return pd.DataFrame([simulate(r, x, **kw) for x in risks]).set_index("risk")


def selftest() -> None:
    assert (
        round(streak_loss(0.02, 10), 3) == 0.183
        and round(streak_loss(0.10, 10), 2) == 0.65
    )
    t = table(r_from_assumption(0.40, 2.0), paths=2000)
    assert t.loc[0.01, "p_dd_20"] < t.loc[0.02, "p_dd_20"] < t.loc[0.05, "p_dd_20"]
    assert t.loc[0.05, "p_dd_50"] > t.loc[0.02, "p_dd_50"]
    print(t.round(3).to_string())
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--win-rate", type=float, default=0.45)
    p.add_argument("--payoff", type=float, default=2.0)
    p.add_argument("--risks", type=float, nargs="*", default=[0.01, 0.02, 0.05])
    p.add_argument("--journal")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        selftest()
    else:
        if a.journal:
            from appx_a_trade_journal_metrics import enrich

            r = enrich(pd.read_csv(a.journal))["r"].dropna().values
        else:
            r = r_from_assumption(a.win_rate, a.payoff)
        print(table(r, a.risks).round(3).to_string())
