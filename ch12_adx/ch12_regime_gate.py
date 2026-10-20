"""ch12_regime_gate.py -- the ADX regime router as a metric.

Ref: §12.4.2-12.4.3 (Tables 12.2-12.3: static bands and line direction),
§12.7.1-12.7.2 (regime filter, percentile threshold), §12.10.3 (Listing
12.3), §12.9.3 (Table 12.6 trigger table).

Per bar: ADX, +DI, -DI, 3-bar ADX slope, fixed regime (Table 12.2),
percentile regime (p40/p60 over 126 bars), bars in regime, the active
toolkit (Chapter 10 trend tools | Chapter 11 oscillators | none) and the
Table 12.6 signal.

Usage:
    python ch12_regime_gate.py --selftest
    python ch12_regime_gate.py BTC-USD
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common.data import get_ohlcv, synthetic_ohlcv  # noqa: E402
from common.indicators import adx  # noqa: E402


def gate(df: pd.DataFrame, period: int = 14, lookback: int = 126) -> pd.DataFrame:
    g = adx(df, period)
    g["adx_slope3"] = g["adx"].diff(3)
    g["regime_fixed"] = pd.cut(
        g["adx"],
        [0, 20, 40, 50, 100],
        labels=["ranging", "developing_trend", "strong_trend", "exhausted"],
    )
    p40 = g["adx"].rolling(lookback).quantile(0.40)
    p60 = g["adx"].rolling(lookback).quantile(0.60)
    g["regime_pctile"] = np.select(
        [g.adx > p60, g.adx < p40], ["trending", "ranging"], "neutral"
    )
    run_id = (g["regime_pctile"] != g["regime_pctile"].shift()).cumsum()
    g["bars_in_regime"] = g.groupby(run_id).cumcount() + 1
    g["toolkit"] = np.select(
        [(g.adx > 25) & (g.adx_slope3 > 0), g.adx < 20],
        ["Ch 10 trend tools", "Ch 11 oscillators"],
        "none (transition)",
    )
    up, dn = g.plus_di > g.minus_di, g.minus_di > g.plus_di
    rising = g.adx_slope3 > 0
    x_up = up & ~up.shift(1, fill_value=False)
    x_dn = dn & ~dn.shift(1, fill_value=False)
    thr_x = (g.adx > 25) & (g.adx.shift(1) <= 25)
    turned_down_40 = (g.adx.shift(1) > 40) & (g.adx < g.adx.shift(1))
    g["signal"] = np.select(
        [
            up & rising & (thr_x | (x_up & (g.adx > 25))),
            dn & rising & (thr_x | (x_dn & (g.adx > 25))),
            turned_down_40,
            g.adx < 20,
        ],
        ["BUY", "SELL", "EXIT (ADX turning down from > 40)", "STAND ASIDE -> Ch 11"],
        "",
    )
    return g


def selftest() -> None:
    df = synthetic_ohlcv(900, seed=2)
    g = gate(df)
    assert g["adx"].dropna().between(0, 100).all()
    assert {"BUY", "SELL"} & set(g["signal"])
    last = g.iloc[-1]
    print(g["signal"].value_counts().to_string())
    print(
        last[
            [
                "adx",
                "plus_di",
                "minus_di",
                "adx_slope3",
                "regime_fixed",
                "regime_pctile",
                "bars_in_regime",
                "toolkit",
            ]
        ].to_string()
    )
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("symbol", nargs="?")
    p.add_argument("--interval", default="1d")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.symbol:
        selftest()
    else:
        print(gate(get_ohlcv(a.symbol, a.interval)).tail(10).round(2).to_string())
