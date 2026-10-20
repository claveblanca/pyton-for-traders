"""ch09_volume_signal_board.py -- the Table 9.4 volume/OBV triggers, bar by bar.

Ref: §9.3.1 (volume expands with the trend), §9.4.2 (OBV divergence),
§9.7.2 (selling climax, Listing 9.3), §9.9.3 (Table 9.4 trigger table),
PROOF §9.11 (check 1). Concepts ported from code_snippets/volume_oi_rules.py.

Signals per bar:
    BUY         close > prior 20-day high AND volume >= 1.5x avg AND OBV > its prior 20-day high
    SELL        close < prior 20-day low  AND volume >= 1.5x avg AND OBV < its prior 20-day low
    EXIT/WARN   OBV divergence or a climax bar after an extended move
    STAND ASIDE volume below average AND OBV flat (|20-bar OBV slope| small)

Usage:
    python ch09_volume_signal_board.py --selftest
    python ch09_volume_signal_board.py BTC-USD
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common.data import get_ohlcv, synthetic_ohlcv  # noqa: E402
from common.indicators import obv  # noqa: E402


def board(df: pd.DataFrame, n: int = 20, vol_x: float = 1.5) -> pd.DataFrame:
    b = pd.DataFrame(index=df.index)
    b["obv"] = obv(df)
    b["vol_ratio"] = df["volume"] / df["volume"].rolling(n).mean()
    hi, lo = (
        df["close"].shift(1).rolling(n).max(),
        df["close"].shift(1).rolling(n).min(),
    )
    ohi, olo = b["obv"].shift(1).rolling(n).max(), b["obv"].shift(1).rolling(n).min()
    b["buy"] = (df["close"] > hi) & (b["vol_ratio"] >= vol_x) & (b["obv"] > ohi)
    b["sell"] = (df["close"] < lo) & (b["vol_ratio"] >= vol_x) & (b["obv"] < olo)
    new_hi = df["close"] >= df["close"].rolling(n).max()
    new_lo = df["close"] <= df["close"].rolling(n).min()
    b["bear_div"] = new_hi & (b["obv"] < b["obv"].rolling(n).max())
    b["bull_div"] = new_lo & (b["obv"] > b["obv"].rolling(n).min())
    vz = (df["volume"] - df["volume"].rolling(60).mean()) / df["volume"].rolling(
        60
    ).std()
    extended = (df["close"] / df["close"].rolling(50).mean() - 1).abs() > 0.10
    b["climax"] = (vz >= 2) & extended
    slope = b["obv"].diff(n) / (df["volume"].rolling(n).mean() * n)
    b["stand_aside"] = (b["vol_ratio"] < 1) & (slope.abs() < 0.1)
    b["signal"] = np.select(
        [b.buy, b.sell, b.bear_div | b.bull_div | b.climax, b.stand_aside],
        ["BUY", "SELL", "EXIT/WARN", "STAND ASIDE"],
        "",
    )
    return b


def selftest() -> None:
    df = synthetic_ohlcv(600)
    i = 400  # inject a confirmed breakout
    df.iloc[i : i + 3, df.columns.get_loc("close")] *= np.array([1.08, 1.10, 1.12])
    df.iloc[i : i + 3, df.columns.get_loc("high")] = df["close"].iloc[i : i + 3] * 1.005
    df.iloc[i : i + 3, df.columns.get_loc("volume")] *= 4
    b = board(df)
    assert b["buy"].iloc[i : i + 3].any()
    assert set(b["signal"].unique()) <= {"", "BUY", "SELL", "EXIT/WARN", "STAND ASIDE"}
    print(b["signal"].value_counts().to_string())
    print(b.loc[b.signal != ""].tail(5)[["vol_ratio", "signal"]].round(2).to_string())
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("symbol", nargs="?")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.symbol:
        selftest()
    else:
        b = board(get_ohlcv(a.symbol))
        print(
            b.loc[b.signal != ""]
            .tail(15)[["vol_ratio", "obv", "signal"]]
            .round(2)
            .to_string()
        )
