"""ch08_trend_structure.py -- Chapter 8's chart vocabulary turned into numbers.

Ref: §8.7.1 (trend = sequence of peaks and troughs), §8.7.3-8.7.4 (support,
resistance, role reversal), §8.8.4 (Table 8.3 retracement bands), §8.9.1
(reversal and outside days), §8.9.2 (Table 8.4 gap types),
PROOF §8.10 (checks 1, 3, 4).

    swings(df, n)          pivot highs/lows: bar is the extreme of +/- n bars
    trend_label(sw)        'up' | 'down' | 'sideways' from the last 2 peaks + 2 troughs
    retracement(df, sw)    % of the last swing retraced, and its Table 8.3 band
    reversal_days(df)      key reversal + outside-day flags (volume-confirmed)
    gaps(df, trend)        gap rows with a Table 8.4 *candidate* type
    report(df)             one dict: the PROOF §8.10 reading of the last bar

Gap types are candidates: the book's definitions depend on context the code
only approximates (pattern completion = break of a 20-bar range; "near the
end of a move" = price > 2 ATR from its 50-bar mean).

Usage:
    python ch08_trend_structure.py --selftest
    python ch08_trend_structure.py SPY
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common.data import get_ohlcv, synthetic_ohlcv  # noqa: E402
from common.indicators import atr  # noqa: E402

BANDS = [
    (0.0, 0.33, "shallow (< 33%)"),
    (0.33, 0.62, "normal (33-62%, median 50%)"),
    (0.62, 0.66, "deep (62-66%)"),
    (0.66, 9.9, "beyond 66%: treat as reversal"),
]


def swings(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Confirmed pivots only: a pivot at t is known at t + n (no look-ahead in use)."""
    w = 2 * n + 1
    hi = df["high"] == df["high"].rolling(w, center=True).max()
    lo = df["low"] == df["low"].rolling(w, center=True).min()
    out = pd.concat(
        [
            pd.DataFrame({"kind": "peak", "price": df["high"][hi]}),
            pd.DataFrame({"kind": "trough", "price": df["low"][lo]}),
        ]
    ).sort_index()
    return out


def trend_label(sw: pd.DataFrame) -> str:
    p = sw[sw.kind == "peak"]["price"].tail(2)
    t = sw[sw.kind == "trough"]["price"].tail(2)
    if len(p) < 2 or len(t) < 2:
        return "unknown"
    if p.iloc[1] > p.iloc[0] and t.iloc[1] > t.iloc[0]:
        return "up"
    if p.iloc[1] < p.iloc[0] and t.iloc[1] < t.iloc[0]:
        return "down"
    return "sideways"


def retracement(df: pd.DataFrame, sw: pd.DataFrame) -> dict:
    last2 = sw.tail(2)
    if len(last2) < 2 or last2.kind.iloc[0] == last2.kind.iloc[1]:
        return {"retracement": np.nan, "band": "n/a"}
    a, b = last2.price.iloc[0], last2.price.iloc[1]
    move = b - a
    r = (b - df["close"].iloc[-1]) / move if move else np.nan
    band = (
        next((lbl for lo, hi, lbl in BANDS if lo <= abs(r) < hi), "n/a")
        if pd.notna(r)
        else "n/a"
    )
    return {
        "swing_from": float(a),
        "swing_to": float(b),
        "retracement": round(float(r), 3),
        "band": band,
    }


def reversal_days(df: pd.DataFrame, lookback: int = 20) -> pd.DataFrame:
    vol_ok = df["volume"] > df["volume"].rolling(20).mean()
    new_hi = df["high"] >= df["high"].rolling(lookback).max()
    new_lo = df["low"] <= df["low"].rolling(lookback).min()
    pc = df["close"].shift(1)
    outside = (df["high"] > df["high"].shift(1)) & (df["low"] < df["low"].shift(1))
    return pd.DataFrame(
        {
            "top_reversal": new_hi & (df["close"] < pc) & vol_ok,
            "bottom_reversal": new_lo & (df["close"] > pc) & vol_ok,
            "outside_day": outside,
        }
    )


def gaps(df: pd.DataFrame, island_window: int = 10) -> pd.DataFrame:
    up = df["low"] > df["high"].shift(1)
    dn = df["high"] < df["low"].shift(1)
    a = atr(df, 14)
    ext = (df["close"] - df["close"].rolling(50).mean()) / a
    vol_x = df["volume"] / df["volume"].rolling(20).mean()
    brk_up = df["close"] > df["high"].shift(1).rolling(20).max()
    brk_dn = df["close"] < df["low"].shift(1).rolling(20).min()
    rows = []
    for t in df.index[up | dn]:
        d = 1 if up[t] else -1
        if (d == 1 and brk_up[t]) or (d == -1 and brk_dn[t]):
            kind = "breakaway" if vol_x[t] >= 1.5 else "breakaway (light volume)"
        elif abs(ext[t]) > 2 and np.sign(ext[t]) == d:
            kind = "exhaustion"
        else:
            kind = "runaway"
        rows.append(
            {
                "ts": t,
                "direction": "up" if d == 1 else "down",
                "type": kind,
                "volume_x": round(float(vol_x[t]), 2),
            }
        )
    g = (
        pd.DataFrame(rows).set_index("ts")
        if rows
        else pd.DataFrame(columns=["direction", "type", "volume_x"])
    )
    # island: an exhaustion gap followed within N bars by an opposite gap
    for i, (t, r) in enumerate(g.iterrows()):
        nxt = g.iloc[i + 1 :]
        nxt = nxt[
            (nxt.direction != r.direction)
            & (nxt.index <= t + (df.index[1] - df.index[0]) * island_window)
        ]
        if r.type == "exhaustion" and len(nxt):
            g.loc[nxt.index[0], "type"] = "island reversal"
    return g


def report(df: pd.DataFrame, n: int = 5) -> dict:
    sw = swings(df, n)
    rd = reversal_days(df).iloc[-1]
    g = gaps(df)
    return {
        "date": str(df.index[-1].date()),
        "trend": trend_label(sw),
        **retracement(df, sw),
        **{k: bool(v) for k, v in rd.items()},
        "last_gap": (
            (g.iloc[-1].to_dict() | {"ts": str(g.index[-1].date())}) if len(g) else None
        ),
        "gaps_last_60": int((g.index >= df.index[-60]).sum()) if len(g) else 0,
    }


def selftest() -> None:
    idx = pd.date_range("2025-01-01", periods=9, freq="D", tz="UTC")
    zz = pd.DataFrame({"high": [10, 12, 11, 14, 13, 16, 15, 18, 17]}, index=idx)
    zz["low"] = zz["high"] - 1
    sw = swings(zz, 1)
    assert trend_label(sw) == "up"  # higher highs, higher lows
    df = synthetic_ohlcv(600)
    r = report(df)
    assert r["trend"] in {"up", "down", "sideways"}
    g = gaps(df)
    assert set(g["type"]) <= {
        "breakaway",
        "breakaway (light volume)",
        "runaway",
        "exhaustion",
        "island reversal",
    }
    print(r)
    print(g.tail(5).to_string())
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("symbol", nargs="?")
    p.add_argument("--n", type=int, default=5)
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.symbol:
        selftest()
    else:
        print(report(get_ohlcv(a.symbol), a.n))
