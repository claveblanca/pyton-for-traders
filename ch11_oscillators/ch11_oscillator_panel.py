"""ch11_oscillator_panel.py -- every Chapter 11 oscillator, one row per bar.

Ref: §11.1.1 (Table 11.1 three rules), §11.2-11.6 (Table 11.2 scales),
§11.10.1-11.10.4 (Listings 11.1-11.4), §11.9.3 (Table 11.3 triggers).

Columns: RSI(14, Wilder), RSI range-shift band (40-80 uptrend / 20-60
downtrend), MACD line/signal/hist + histogram turning points, Stochastic
%K/%D, Williams %R (zones: -20..0 overbought, -80..-100 oversold), CCI(20),
ROC(10), momentum(10), RSI divergence flags, and the Table 11.3 signal.

Usage:
    python ch11_oscillator_panel.py --selftest
    python ch11_oscillator_panel.py BTC-USD
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common.data import get_ohlcv, synthetic_ohlcv  # noqa: E402
from common.indicators import adx, cci, macd, rsi, stochastic  # noqa: E402


def williams_zone(wr: float) -> str:
    return "overbought" if wr >= -20 else "oversold" if wr <= -80 else "neutral"


def panel(df: pd.DataFrame) -> pd.DataFrame:
    c = df["close"]
    p = pd.DataFrame(index=df.index)
    p["rsi14"] = rsi(c, 14)
    p = p.join(macd(c)).join(stochastic(df))
    p["cci20"] = cci(df)
    p["roc10"] = 100 * c / c.shift(10)
    p["mom10"] = c - c.shift(10)
    p["wr_zone"] = p["williams_r"].map(williams_zone)
    p["hist_peak"] = (p["hist"] < p["hist"].shift(1)) & (
        p["hist"].shift(1) >= p["hist"].shift(2)
    )
    p["hist_trough"] = (p["hist"] > p["hist"].shift(1)) & (
        p["hist"].shift(1) <= p["hist"].shift(2)
    )
    lo40 = p["rsi14"].rolling(60).min()
    hi60 = p["rsi14"].rolling(60).max()
    p["range_shift"] = np.select(
        [lo40 >= 38, hi60 <= 62], ["uptrend band 40-80", "downtrend band 20-60"], ""
    )
    n = 14
    p["bear_div"] = (c == c.rolling(n).max()) & (
        p["rsi14"] < p["rsi14"].rolling(n).max()
    )
    p["bull_div"] = (c == c.rolling(n).min()) & (
        p["rsi14"] > p["rsi14"].rolling(n).min()
    )
    a = adx(df)
    p["adx"] = a["adx"]
    up_trend, dn_trend = a["plus_di"] > a["minus_di"], a["minus_di"] > a["plus_di"]
    exit_os = (p["rsi14"] > 30) & (p["rsi14"].shift(1) <= 30)
    exit_ob = (p["rsi14"] < 70) & (p["rsi14"].shift(1) >= 70)
    turn_up = p["rsi14"] > p["rsi14"].shift(1)
    p["signal"] = np.select(
        [
            (p.adx < 20) & exit_os,
            (p.adx < 20) & exit_ob,
            (p.adx > 25) & up_trend & p.rsi14.between(40, 50) & turn_up,
            (p.adx > 25) & dn_trend & p.rsi14.between(50, 60) & ~turn_up,
            p.rsi14.between(45, 55) & ~p.bear_div & ~p.bull_div,
        ],
        [
            "BUY (range)",
            "SELL (range)",
            "BUY (trend pullback)",
            "SELL (trend rally)",
            "STAND ASIDE",
        ],
        "",
    )
    return p


def selftest() -> None:
    assert [williams_zone(x) for x in (-5, -50, -90)] == [
        "overbought",
        "neutral",
        "oversold",
    ]
    p = panel(synthetic_ohlcv(800))
    assert p["rsi14"].dropna().between(0, 100).all()
    assert p["williams_r"].dropna().between(-100, 0).all()
    assert p["stoch_k"].dropna().between(0, 100).all()
    print(p["signal"].value_counts().to_string())
    print(
        p.iloc[-1][
            [
                "rsi14",
                "macd",
                "hist",
                "stoch_k",
                "williams_r",
                "wr_zone",
                "cci20",
                "adx",
                "signal",
            ]
        ].to_string()
    )
    print("selftest OK")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("symbol", nargs="?")
    ap.add_argument("--interval", default="1d")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest or not a.symbol:
        selftest()
    else:
        print(panel(get_ohlcv(a.symbol, a.interval)).tail(10).round(2).to_string())
