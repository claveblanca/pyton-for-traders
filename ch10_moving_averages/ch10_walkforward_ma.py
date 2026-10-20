"""ch10_walkforward_ma.py -- the curve-fitting warning, measured.

Ref: §10.8.1 (the optimization trap), PROOF §10.11 (check 3: "hold out data
the parameter search never saw").

Rolling walk-forward: in each window, pick the dual-SMA pair with the best
in-sample Sharpe (train = 2 years), then trade it out of sample for the next
6 months. Report per fold the chosen pair, IS Sharpe and OOS Sharpe, plus
the overall degradation ratio OOS / IS. A ratio well below 1 is the
signature of a fit to noise.

Usage:
    python ch10_walkforward_ma.py --selftest
    python ch10_walkforward_ma.py SPY
"""

from __future__ import annotations

import argparse
import itertools
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import backtest  # noqa: E402
from common.data import get_ohlcv, synthetic_ohlcv  # noqa: E402
from ch10_crossover_backtest import dual  # noqa: E402

FASTS, SLOWS = (5, 10, 20, 30), (50, 100, 150, 200)


def walk_forward(
    close: pd.Series, train: int = 504, test: int = 126, cost_bps: float = 5.0
) -> pd.DataFrame:
    rows = []
    start = 0
    while start + train + test <= len(close):
        tr = close.iloc[start : start + train]
        te_full = close.iloc[
            start : start + train + test
        ]  # warm-up from the train window
        best = max(
            ((f, s) for f, s in itertools.product(FASTS, SLOWS) if f < s),
            key=lambda p: backtest.run(tr, dual(tr, *p), cost_bps)["sharpe"],
        )
        pos = dual(te_full, *best)
        is_r = backtest.run(tr, dual(tr, *best), cost_bps)
        oos = backtest.run(te_full.iloc[train:], pos.iloc[train:], cost_bps)
        rows.append(
            {
                "test_start": te_full.index[train].date(),
                "pair": f"{best[0]}/{best[1]}",
                "is_sharpe": is_r["sharpe"],
                "oos_sharpe": oos["sharpe"],
                "oos_trades": oos["trades"],
            }
        )
        start += test
    return pd.DataFrame(rows)


def summary(wf: pd.DataFrame) -> dict:
    is_m, oos_m = float(wf["is_sharpe"].mean()), float(wf["oos_sharpe"].mean())
    return {
        "folds": len(wf),
        "mean_is_sharpe": round(is_m, 3),
        "mean_oos_sharpe": round(oos_m, 3),
        "degradation_oos_over_is": round(oos_m / is_m, 3) if is_m else None,
        "pair_changes": int((wf["pair"] != wf["pair"].shift()).sum() - 1),
    }


def selftest() -> None:
    df = synthetic_ohlcv(
        1600, seed=5, regimes=False, drift=0.0
    )  # pure noise: nothing to find
    wf = walk_forward(df["close"])
    s = summary(wf)
    assert (
        s["folds"] >= 8 and s["mean_is_sharpe"] > s["mean_oos_sharpe"]
    )  # fit to noise degrades
    print(wf.round(2).to_string(index=False))
    print(s)
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("symbol", nargs="?")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.symbol:
        selftest()
    else:
        wf = walk_forward(get_ohlcv(a.symbol)["close"])
        print(wf.round(2).to_string(index=False))
        print(summary(wf))
