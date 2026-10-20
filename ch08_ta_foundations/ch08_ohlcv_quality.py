"""ch08_ohlcv_quality.py -- data-quality score for an OHLCV series.

Ref: §8.10 [CODE] HANDS-ON (Listings 8.1-8.3), Ch 9 prereq line ("the OHLCV data layer this chapter's code
assumes"), §8.5.2 (closing prices carry the information).

Checks: duplicates, NaNs, OHLC consistency, zero-volume share, |z| > 6
return outliers, missing-bar gaps, and the close difference against a second
source. Score = 100 minus weighted penalties; below 90 = do not compute
indicators on it yet.

Usage:
    python ch08_ohlcv_quality.py --selftest
    python ch08_ohlcv_quality.py BTC-USD --second XBTUSD     # yfinance vs Kraken
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common.data import check_ohlcv, get_ohlcv, synthetic_ohlcv  # noqa: E402

PENALTY = {
    "duplicate_ts": 5,
    "nan_cells": 2,
    "ohlc_violations": 3,
    "outlier_returns": 2,
    "missing_bar_gaps": 1,
}


def cross_source_diff(a: pd.Series, b: pd.Series) -> dict:
    """Median and max |close_a / close_b - 1| on common daily timestamps, in %."""
    a, b = a[~a.index.duplicated()], b[~b.index.duplicated()]
    j = pd.concat([a.rename("a"), b.rename("b")], axis=1, sort=True).dropna()
    d = (j["a"] / j["b"] - 1).abs() * 100
    return {
        "common_bars": len(j),
        "median_diff_pct": float(d.median()) if len(d) else np.nan,
        "max_diff_pct": float(d.max()) if len(d) else np.nan,
    }


def quality_score(df: pd.DataFrame, second: pd.Series | None = None) -> dict:
    f = check_ohlcv(df)
    pen = sum(PENALTY[k] * min(f.get(k) or 0, 10) for k in PENALTY)
    pen += 20 * max(0.0, f["zero_volume_share"] - 0.05)
    out = {**f}
    if second is not None:
        x = cross_source_diff(df["close"], second)
        pen += 10 * (x["median_diff_pct"] > 0.5)
        out.update(x)
    out["score"] = max(0.0, 100 - pen)
    out["usable"] = out["score"] >= 90
    return out


def selftest() -> None:
    clean = synthetic_ohlcv(300)
    assert quality_score(clean)["score"] == 100
    dirty = clean.copy()
    dirty.iloc[10, dirty.columns.get_loc("high")] = (
        dirty["low"].iloc[10] * 0.9
    )  # high < low
    dirty = pd.concat([dirty, dirty.iloc[[50]]]).sort_index()  # duplicate
    dirty = dirty.drop(dirty.index[100:105])  # gap
    q = quality_score(dirty, second=clean["close"] * 1.01)
    assert (
        q["duplicate_ts"] == 1
        and q["ohlc_violations"] >= 1
        and q["missing_bar_gaps"] >= 1
    )
    assert not q["usable"]
    print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in q.items()})
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("symbol", nargs="?")
    p.add_argument("--interval", default="1d")
    p.add_argument("--second", help="Kraken pair for the cross-source check")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.symbol:
        selftest()
    else:
        df = get_ohlcv(a.symbol, a.interval)
        sec = (
            get_ohlcv(a.second, a.interval, source="kraken")["close"]
            if a.second
            else None
        )
        if sec is not None:
            df.index, sec.index = df.index.normalize(), sec.index.normalize()
        print(quality_score(df, sec))
