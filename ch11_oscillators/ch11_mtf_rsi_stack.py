"""ch11_mtf_rsi_stack.py -- the three-layer RSI stack the §11.7 DATA box promises.

Ref: §11.7.2 (weekly/daily filter) and the DATA box after it: "daily RSI sets
the regime bias (bull above 50, bear below), 4H RSI defines a pullback setup
zone (40-55 for a long), and 1H RSI supplies the entry trigger (exit from
oversold) -- shifted forward before joining so no timeframe leaks future
information into another." Inspired by code_snippets/ch13/
strategy_multi_timeframe_v2.md and the ch13/mock JSON fixtures.

Input: one 1H OHLCV frame; 4H and daily bars are resampled from it, each
higher-timeframe value is shifted one bar (only the CLOSED bar is known),
then forward-filled onto the 1H index.

Usage:
    python ch11_mtf_rsi_stack.py --selftest
    python ch11_mtf_rsi_stack.py XBTUSD          # Kraken 1H
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common.data import get_ohlcv, synthetic_ohlcv  # noqa: E402
from common.indicators import rsi  # noqa: E402

AGG = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}


def higher_tf_rsi(h1: pd.DataFrame, rule: str, period: int = 14) -> pd.Series:
    # 1H stamps are bar OPEN times: [00:00, 04:00) closes at 04:00 and is stamped 04:00
    bars = h1.resample(rule, label="right", closed="left").agg(AGG).dropna()
    r = rsi(bars["close"], period)  # labelled at bar CLOSE time
    return r.reindex(h1.index, method="ffill")  # known only after the close


def stack(h1: pd.DataFrame) -> pd.DataFrame:
    s = pd.DataFrame(index=h1.index)
    s["rsi_1d"] = higher_tf_rsi(h1, "1D")
    s["rsi_4h"] = higher_tf_rsi(h1, "4h")
    s["rsi_1h"] = rsi(h1["close"], 14)
    s["regime"] = np.where(s.rsi_1d > 50, "bull", np.where(s.rsi_1d < 50, "bear", ""))
    s["setup_long"] = (s.regime == "bull") & s.rsi_4h.between(40, 55)
    s["setup_short"] = (s.regime == "bear") & s.rsi_4h.between(45, 60)
    s["trigger_long"] = (s.rsi_1h > 30) & (s.rsi_1h.shift(1) <= 30)
    s["trigger_short"] = (s.rsi_1h < 70) & (s.rsi_1h.shift(1) >= 70)
    s["entry"] = np.select(
        [s.setup_long & s.trigger_long, s.setup_short & s.trigger_short],
        ["LONG", "SHORT"],
        "",
    )
    return s


def no_lookahead(h1: pd.DataFrame) -> bool:
    """Truncating the future must not change any past value."""
    full = stack(h1)
    cut = stack(h1.iloc[: len(h1) // 2])
    common = cut.index
    return np.allclose(
        full.loc[common, "rsi_4h"].fillna(-1), cut["rsi_4h"].fillna(-1)
    ) and np.allclose(full.loc[common, "rsi_1d"].fillna(-1), cut["rsi_1d"].fillna(-1))


def selftest() -> None:
    h1 = synthetic_ohlcv(24 * 120, freq="h", vol=0.006)
    s = stack(h1)
    assert no_lookahead(h1)
    assert set(s["entry"].unique()) <= {"", "LONG", "SHORT"}
    print(s["entry"].value_counts().to_string())
    print(
        s[s.entry != ""]
        .tail(5)[["rsi_1d", "rsi_4h", "rsi_1h", "entry"]]
        .round(1)
        .to_string()
    )
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("pair", nargs="?")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.pair:
        selftest()
    else:
        s = stack(get_ohlcv(a.pair, "1h", source="kraken"))
        print(s.tail(10).round(1).to_string())
