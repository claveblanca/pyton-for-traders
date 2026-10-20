"""ch06_carry_trend_screen.py -- the §6.1.6 carry-plus-trend rule as a monthly screen.

Ref: §6.1.4 (Table 6.2, strategy 4), §6.1.6 (the rule), PROOF §6.4.4-6.4.5
and §6.4.8 (Table 6.11 decision). Builds on code_snippets/ch02/
ch02_etc_carry_cot.py (roll_yield, cot_score, etc_signal).

Rule (§6.1.6):
    1. universe: one ETC per commodity group
    2. filter: price > 200-day average AND annualised roll > -5%
    3. rank by 6-month EUR return, hold the top 3 equally weighted
    4. empty slots go to a euro money-market ETF (cash)
    5. rebalance monthly
Optional positioning overlay (§6.4.6): crowded (score >= 90) -> reduced size.

Usage:
    python ch06_carry_trend_screen.py --selftest
    python ch06_carry_trend_screen.py universe.csv   # ticker, group, roll_annual, cot_pct
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

MIN_CARRY, TOP_N, CROWDED = -0.05, 3, 90


def etc_signal(
    roll_annual: float, above_200d: bool, cot_pct: float | None = None
) -> str:
    """Ch 6 Listing 6.3."""
    if roll_annual < MIN_CARRY:
        return "AVOID - contango cost"
    if not above_200d:
        return "STAND ASIDE - no uptrend"
    return "LONG, REDUCED SIZE - crowded" if (cot_pct or 0) >= CROWDED else "LONG"


def screen(universe: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
    """universe: ticker, group, roll_annual, cot_pct; prices: EUR closes, one column per ticker."""
    rows = []
    for _, u in universe.iterrows():
        px = prices[u.ticker].dropna()
        above = bool(px.iloc[-1] > px.rolling(200).mean().iloc[-1])
        mom6 = px.iloc[-1] / px.iloc[-min(len(px), 126)] - 1
        rows.append(
            {
                **u.to_dict(),
                "above_200d": above,
                "mom_6m": mom6,
                "signal": etc_signal(u.roll_annual, above, u.get("cot_pct")),
            }
        )
    t = pd.DataFrame(rows)
    ok = (
        t[t.signal.str.startswith("LONG")]
        .sort_values("mom_6m", ascending=False)
        .head(TOP_N)
    )
    t["weight"] = 0.0
    t.loc[ok.index, "weight"] = 1 / TOP_N
    t.loc[ok.index[ok.signal.str.contains("REDUCED")], "weight"] = 1 / TOP_N / 2
    cash = 1 - t["weight"].sum()
    t = pd.concat(
        [t, pd.DataFrame([{"ticker": "CASH (EUR money market)", "weight": cash}])],
        ignore_index=True,
    )
    return t.sort_values("weight", ascending=False)


def selftest() -> None:
    rng = np.random.default_rng(4)
    idx = pd.bdate_range("2025-01-01", periods=300)

    def path(drift):
        return pd.Series(100 * np.exp(np.cumsum(drift + rng.normal(0, 0.01, 300))), idx)

    prices = pd.DataFrame(
        {
            "BRNT": path(0.002),
            "COPA": path(0.001),
            "GOLD": path(0.0015),
            "COCO": path(0.002),
            "AGRI": path(-0.004),
        }
    )
    uni = pd.DataFrame(
        {
            "ticker": prices.columns,
            "group": ["energy", "ind.metals", "gold", "agri", "broad"],
            "roll_annual": [1.268, -0.02, -0.005, -0.085, -0.03],
            "cot_pct": [40, 96, 74, 95, 60],
        }
    )
    t = screen(uni, prices)
    assert (
        t.set_index("ticker").loc["COCO", "signal"] == "AVOID - contango cost"
    )  # §6.4.4
    assert t.set_index("ticker").loc["AGRI", "signal"].startswith("STAND ASIDE")
    assert abs(t["weight"].sum() - 1) < 1e-12
    print(
        t[
            [
                "ticker",
                "roll_annual",
                "above_200d",
                "mom_6m",
                "cot_pct",
                "signal",
                "weight",
            ]
        ]
        .round(3)
        .to_string(index=False)
    )
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("csv", nargs="?")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.csv:
        selftest()
    else:
        from common.data import get_ohlcv

        uni = pd.read_csv(a.csv)
        prices = pd.DataFrame({t: get_ohlcv(t)["close"] for t in uni.ticker})
        print(screen(uni, prices).round(3).to_string(index=False))
