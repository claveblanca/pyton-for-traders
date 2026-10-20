"""ch09_price_oi_matrix.py -- futures price and open interest read together.

Ref: §9.2 (Table 9.1 how OI changes), §9.5 (Table 9.2 price x OI matrix),
§9.6.1 (OI as a fuel gauge), §9.6.2 (OI build-up in a consolidation),
PROOF §9.11 (checks 2-3).

Input: daily front/active-month (or total) series with close and
open_interest (e.g. from ch05_front_month / futures_settlements).
    quadrant      Table 9.2 reading per day
    fuel_gauge    OI levelling off or falling while price trends (warning)
    buildup       OI rising while price range is narrow (stored energy)

Usage:
    python ch09_price_oi_matrix.py --selftest
    python ch09_price_oi_matrix.py series.csv     # columns: date, close, open_interest
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd

READING = {
    (1, 1): ("new money entering - aggressive buying", "bullish"),
    (1, -1): ("short covering, not new buying", "bearish"),
    (-1, 1): ("new money entering - aggressive short selling", "bearish"),
    (-1, -1): ("long liquidation, not new selling", "bullish / stabilizing"),
}


def matrix(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    m = pd.DataFrame(index=df.index)
    dp = np.sign(df["close"].diff(n))
    doi = np.sign(df["open_interest"].diff(n))
    m["quadrant"] = [READING.get((p, o), ("flat", ""))[0] for p, o in zip(dp, doi)]
    m["bias"] = [READING.get((p, o), ("", "neutral"))[1] for p, o in zip(dp, doi)]
    trend = df["close"].diff(20) / df["close"].shift(20)
    oi_slope = df["open_interest"].diff(20) / df["open_interest"].shift(20)
    m["fuel_gauge_warning"] = (trend.abs() > 0.03) & (oi_slope <= 0.0)
    rng = df["close"].rolling(20).max() / df["close"].rolling(20).min() - 1
    m["consolidation_buildup"] = (rng < 0.04) & (oi_slope > 0.05)
    return m


def selftest() -> None:
    idx = pd.bdate_range("2026-01-01", periods=120)
    close = np.r_[
        np.linspace(100, 120, 60),
        np.linspace(120, 128, 30),
        np.full(30, 128) + np.sin(np.arange(30)),
    ]
    oi = np.r_[
        np.linspace(50_000, 80_000, 60),
        np.linspace(80_000, 70_000, 30),
        np.linspace(70_000, 95_000, 30),
    ]
    m = matrix(pd.DataFrame({"close": close, "open_interest": oi}, index=idx))
    assert m["bias"].iloc[30] == "bullish"  # price up, OI up
    assert (
        m["quadrant"].iloc[80] == "short covering, not new buying"
    )  # trap case §9.5.1
    assert m["fuel_gauge_warning"].iloc[85]
    assert m["consolidation_buildup"].iloc[-1]
    print(m.iloc[::15].to_string())
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("csv", nargs="?")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.csv:
        selftest()
    else:
        df = pd.read_csv(a.csv, index_col=0, parse_dates=True)
        print(matrix(df).tail(20).to_string())
