"""ch04_tracking_difference.py -- what the ICS does not see: tracking.

Ref: §4.4.6 (tracking difference sits outside the ICS),
PROOF §4.8.6 (Step 6: tracking difference over as many years as possible).

    tracking_difference(etf, index)   yearly ETF total return - index total return
    tracking_error(etf, index)        annualised std of daily return differences
    compare_to_ter(td, ter)           is the gap explained by the TER?

Both series must be total-return (dividends reinvested): use an accumulating
share class against the net-total-return index, or adjusted closes.

Usage:
    python ch04_tracking_difference.py --selftest
    python ch04_tracking_difference.py --etf CSPX.L --index ^SP500TR --ter 0.07
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def tracking_difference(etf: pd.Series, index: pd.Series) -> pd.DataFrame:
    y = pd.DataFrame({"etf": etf, "index": index}).dropna().resample("YE").last()
    r = y.pct_change().dropna()
    r["td_pct"] = (r["etf"] - r["index"]) * 100
    return r


def tracking_error(etf: pd.Series, index: pd.Series) -> float:
    d = pd.DataFrame({"e": etf.pct_change(), "i": index.pct_change()}).dropna()
    return float((d["e"] - d["i"]).std() * np.sqrt(252) * 100)


def compare_to_ter(td: pd.DataFrame, ter: float) -> dict:
    avg = float(td["td_pct"].mean())
    return {
        "years": len(td),
        "avg_td_pct": avg,
        "ter_pct": ter,
        "td_vs_ter": avg + ter,  # > 0: tracks better than its fee
        "replication_problem": avg < -2 * ter,
    }  # §4.4.8 trigger: TD well beyond TER


def selftest() -> None:
    rng = np.random.default_rng(5)
    idx = pd.bdate_range("2020-01-01", "2025-12-31")
    r = rng.normal(0.0004, 0.01, len(idx))
    index = pd.Series(100 * np.cumprod(1 + r), idx)
    fee_daily = 0.0015 / 252
    etf = pd.Series(
        100 * np.cumprod(1 + r - fee_daily + rng.normal(0, 0.0002, len(idx))), idx
    )
    td = tracking_difference(etf, index)
    c = compare_to_ter(td, 0.15)
    assert -0.4 < c["avg_td_pct"] < 0.1 and not c["replication_problem"]
    te = tracking_error(etf, index)
    assert 0.1 < te < 0.6
    print(td.round(3).to_string())
    print(c, "TE %:", round(te, 3))
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--etf")
    p.add_argument("--index")
    p.add_argument("--ter", type=float)
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.etf:
        selftest()
    else:
        from common.data import get_ohlcv

        e, i = get_ohlcv(a.etf)["close"], get_ohlcv(a.index)["close"]
        td = tracking_difference(e, i)
        print(td.round(3).to_string())
        print(compare_to_ter(td, a.ter), "TE %:", tracking_error(e, i))
