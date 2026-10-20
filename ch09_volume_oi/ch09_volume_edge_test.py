"""ch09_volume_edge_test.py -- do volume-confirmed breakouts actually do better?

Ref: §9.3.2 (breakouts on light volume are a false-breakout warning),
the WARNING after §9.3.2, PROOF §9.11 (check 1). Uses the Mann-Whitney
edge test from code_snippets/ch06/ch06_proof.py (common/stats.py).

Every close above the prior 20-day high is a breakout; it is "confirmed"
when volume >= 1.5x its 20-day average. Forward 5- and 20-bar returns of the
two groups are compared, non-overlapping events only (one per 5 bars).

Usage:
    python ch09_volume_edge_test.py --selftest
    python ch09_volume_edge_test.py SPY QQQ
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common.data import get_ohlcv, synthetic_ohlcv  # noqa: E402
from common.stats import forward_returns, mann_whitney_edge  # noqa: E402


def breakout_events(
    df: pd.DataFrame, n: int = 20, vol_x: float = 1.5, gap: int = 5
) -> pd.DataFrame:
    brk = df["close"] > df["close"].shift(1).rolling(n).max()
    conf = df["volume"] >= vol_x * df["volume"].rolling(n).mean()
    ev = pd.DataFrame({"confirmed": conf[brk]})
    keep, last = [], None
    for t in ev.index:  # thin to non-overlapping events
        if last is None or df.index.get_loc(t) - df.index.get_loc(last) >= gap:
            keep.append(t)
            last = t
    ev = ev.loc[keep]
    for h in (5, 20):
        ev[f"fwd_{h}"] = forward_returns(df["close"], h).reindex(ev.index)
    return ev


def edge(df: pd.DataFrame) -> pd.DataFrame:
    ev = breakout_events(df)
    rows = []
    for h in (5, 20):
        r = mann_whitney_edge(
            ev.loc[ev.confirmed, f"fwd_{h}"], ev.loc[~ev.confirmed, f"fwd_{h}"]
        )
        rows.append({"horizon": h, **r, "preliminary": min(r["n_a"], r["n_b"]) < 30})
    return pd.DataFrame(rows).set_index("horizon")


def selftest() -> None:
    df = synthetic_ohlcv(2000, seed=3)
    ev = breakout_events(df)
    rng = np.random.default_rng(0)
    conf_idx = ev.index[ev.confirmed]
    for t in conf_idx:  # plant follow-through after confirmed ones
        i = df.index.get_loc(t)
        df.iloc[i + 1 : i + 21, df.columns.get_loc("close")] *= 1.03
    e = edge(df)
    assert e.loc[20, "edge"] > 0
    print(e.round(4).to_string())
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("symbols", nargs="*")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.symbols:
        selftest()
    else:
        for s in a.symbols:
            print(s)
            print(edge(get_ohlcv(s)).round(4).to_string())
