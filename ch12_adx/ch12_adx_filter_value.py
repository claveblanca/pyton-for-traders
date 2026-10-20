"""ch12_adx_filter_value.py -- does the ADX gate actually improve a trend system?

Ref: PROOF §12.11 (stratify by ADX quintile, recalibrate thresholds, account
for lag; Listing 12.6), §12.8.1 (ADX lags by 3-5 bars).

1. Quintile table: forward 5-bar returns of a trend-following position
   (EMA 9/21, long/short), bucketed by the ADX quintile in force, sampled
   NON-overlapping (every 5th bar) so the annualised Sharpe is not inflated
   (the caveat on Listing 12.6).
2. Gate comparison: the same EMA system ungated, gated on fixed ADX > 25,
   gated on the percentile regime, and gated on ADX > 25 OR the 3-bar
   rate-of-change early warning (Listing 12.5), all after costs.

Usage:
    python ch12_adx_filter_value.py --selftest
    python ch12_adx_filter_value.py SPY
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import backtest  # noqa: E402
from common.data import get_ohlcv, synthetic_ohlcv  # noqa: E402
from common.indicators import adx, ema  # noqa: E402
from common.stats import forward_returns  # noqa: E402


def trend_position(close: pd.Series) -> pd.Series:
    return np.sign(ema(close, 9) - ema(close, 21)).fillna(0)


def quintile_table(df: pd.DataFrame, h: int = 5) -> pd.DataFrame:
    a = adx(df)["adx"]
    pos = trend_position(df["close"])
    fwd = forward_returns(df["close"], h) * pos
    d = pd.DataFrame({"adx": a, "r": fwd}).dropna().iloc[::h]  # non-overlapping
    d["q"] = pd.qcut(d["adx"], 5, labels=False, duplicates="drop")
    t = d.groupby("q")["r"].agg(["count", "mean", "std"])
    t["sharpe_ann"] = t["mean"] / t["std"] * np.sqrt(252 / h)
    t["adx_range"] = d.groupby("q")["adx"].agg(lambda x: f"{x.min():.0f}-{x.max():.0f}")
    t["preliminary_n<30"] = t["count"] < 30
    return t


def gate_comparison(df: pd.DataFrame, cost_bps: float = 5.0) -> pd.DataFrame:
    a = adx(df)
    pos = trend_position(df["close"])
    p40, p60 = a.adx.rolling(126).quantile(0.4), a.adx.rolling(126).quantile(0.6)
    gates = {
        "ungated": pd.Series(True, df.index),
        "adx > 25": a.adx > 25,
        "percentile (> p60)": a.adx > p60,
        "adx > 25 or roc3 > 2": (a.adx > 25) | ((a.adx < 25) & (a.adx.diff(3) > 2)),
    }
    rows = []
    for name, g in gates.items():
        r = backtest.run(df["close"], pos.where(g, 0), cost_bps)
        rows.append({"gate": name, **{k: v for k, v in r.items() if k != "equity"}})
    return pd.DataFrame(rows).set_index("gate")


def selftest() -> None:
    df = synthetic_ohlcv(2000, seed=8)
    q = quintile_table(df)
    assert len(q) == 5 and q["count"].sum() > 300
    g = gate_comparison(df)
    assert g.loc["ungated", "trades"] > g.loc["adx > 25", "trades"]  # the gate filters
    print(q.round(4).to_string())
    print(g.round(3).to_string())
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("symbol", nargs="?")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.symbol:
        selftest()
    else:
        df = get_ohlcv(a.symbol)
        print(quintile_table(df).round(4).to_string())
        print(gate_comparison(df).round(3).to_string())
