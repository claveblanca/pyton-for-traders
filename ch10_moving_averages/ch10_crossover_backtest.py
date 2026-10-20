"""ch10_crossover_backtest.py -- crossover systems vs buy-and-hold, after costs.

Ref: §10.2 (lag vs whipsaw trade-off), §10.4 (dual and 4-9-18 triple
crossover), §10.8.1 (optimization trap), PROOF §10.11 (checks 1-2,
Listing 10.5: count events, report n). Inspired by code_snippets/ch06/
ch06_proof.py (ema_sensitivity_grid) and ch13/backtest.

Systems (long/flat by default, --short for long/short):
    dual  f/s     fast SMA above slow SMA
    triple 4-9-18 4 > 9 > 18 fully stacked (R.C. Allen)
Metrics: CAGR, max drawdown, Sharpe, trades (n), hit rate, average hold,
whipsaw rate (trades closed within 5 bars), after cost_bps per side.

Usage:
    python ch10_crossover_backtest.py --selftest
    python ch10_crossover_backtest.py SPY --cost-bps 5
"""

from __future__ import annotations

import argparse
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import backtest  # noqa: E402
from common.data import get_ohlcv, synthetic_ohlcv  # noqa: E402
from common.indicators import sma  # noqa: E402

PAIRS = [(5, 20), (10, 50), (20, 50), (50, 200)]


def dual(close: pd.Series, f: int, s: int, short: bool = False) -> pd.Series:
    up = sma(close, f) > sma(close, s)
    return up.astype(int) - ((~up) & short).astype(int)


def triple(close: pd.Series, short: bool = False) -> pd.Series:
    a, b, c = sma(close, 4), sma(close, 9), sma(close, 18)
    long_ = (a > b) & (b > c)
    shrt = (a < b) & (b < c)
    return long_.astype(int) - (shrt & short).astype(int)


def grid(close: pd.Series, cost_bps: float = 5.0, short: bool = False) -> pd.DataFrame:
    rows = []
    bh = backtest.run(close, pd.Series(1, close.index), 0)
    rows.append(
        {"system": "buy & hold", **{k: v for k, v in bh.items() if k != "equity"}}
    )
    for f, s in PAIRS:
        r = backtest.run(close, dual(close, f, s, short), cost_bps)
        rows.append(
            {"system": f"dual {f}/{s}", **{k: v for k, v in r.items() if k != "equity"}}
        )
    r = backtest.run(close, triple(close, short), cost_bps)
    rows.append(
        {"system": "triple 4-9-18", **{k: v for k, v in r.items() if k != "equity"}}
    )
    t = pd.DataFrame(rows).set_index("system")
    t["preliminary_n<30"] = t["trades"] < 30
    return t


def selftest() -> None:
    df = synthetic_ohlcv(1500, seed=21)
    g = grid(df["close"])
    assert (
        g.loc["dual 5/20", "trades"] > g.loc["dual 50/200", "trades"]
    )  # §10.2 trade-off
    assert g.loc["dual 5/20", "whipsaw_rate"] >= g.loc["dual 50/200", "whipsaw_rate"]
    assert g.loc["buy & hold", "trades"] == 1
    print(g.round(3).to_string())
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("symbol", nargs="?")
    p.add_argument("--cost-bps", type=float, default=5.0)
    p.add_argument("--short", action="store_true")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.symbol:
        selftest()
    else:
        print(
            grid(get_ohlcv(a.symbol)["close"], a.cost_bps, a.short).round(3).to_string()
        )
