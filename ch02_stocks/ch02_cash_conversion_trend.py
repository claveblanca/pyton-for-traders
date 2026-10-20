"""ch02_cash_conversion_trend.py -- can a Cash Flow Index breach be cleared?

Ref: §2.3.3 (Cash Flow Index), PROOF §2.9.4-2.9.5 (the three clearing
checks: working capital, direction, consistency -- described, not coded).

Per fiscal year: CFO / net income, revenue growth, growth of receivables +
inventory, FCF vs net income gap. Verdict:
    ok                         CFI >= 1 on the pooled window
    working_capital_explained  breach, but receivables+inventory growth
                               outpaces revenue growth and the yearly CFI
                               is recovering
    deteriorating              breach not explained, or still drifting down

Usage:
    python ch02_cash_conversion_trend.py --selftest
    python ch02_cash_conversion_trend.py NVDA
"""

from __future__ import annotations

import argparse
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
FIELDS = ["revenue", "net_income", "cfo", "capex_ppe", "receivables", "inventory"]


def yearly_table(a: pd.DataFrame) -> pd.DataFrame:
    t = pd.DataFrame(index=a.index)
    t["cfi"] = a["cfo"] / a["net_income"]
    t["revenue_growth"] = a["revenue"].pct_change()
    wc = a[["receivables", "inventory"]].sum(axis=1)
    t["wc_growth"] = wc.pct_change()
    t["fcf"] = a["cfo"] + a["capex_ppe"]  # capex negative (book sign)
    t["fcf_minus_ni"] = t["fcf"] - a["net_income"]
    return t


def verdict(a: pd.DataFrame, years: int = 7) -> dict:
    t = yearly_table(a)
    w = a.tail(years)
    pooled = w["cfo"].sum() / w["net_income"].sum()
    if pooled >= 1:
        return {"cfi_pooled": pooled, "verdict": "ok"}
    recent = t.tail(3)
    wc_explains = bool((recent["wc_growth"] > recent["revenue_growth"]).mean() >= 2 / 3)
    recovering = bool(t["cfi"].iloc[-1] > t["cfi"].iloc[-3])  # direction check
    gap_widening = bool(
        recent["fcf_minus_ni"].is_monotonic_decreasing
    )  # consistency check
    v = (
        "working_capital_explained"
        if wc_explains and recovering and not gap_widening
        else "deteriorating"
    )
    return {
        "cfi_pooled": pooled,
        "wc_explains": wc_explains,
        "recovering": recovering,
        "gap_widening": gap_widening,
        "verdict": v,
    }


def selftest() -> None:
    base = pd.DataFrame(
        {
            "revenue": [100, 120, 150, 200, 260, 320, 380],
            "net_income": [10, 12, 16, 22, 30, 38, 45],
            "capex_ppe": [-3, -3, -4, -5, -6, -7, -8],
        },
        index=range(2020, 2027),
    )
    good = base.assign(cfo=base["net_income"] * 1.15, receivables=20, inventory=10)
    assert verdict(good)["verdict"] == "ok"
    wc = base.assign(
        cfo=[9, 10, 12, 16, 22, 33, 42],
        receivables=[20, 26, 36, 52, 75, 95, 115],
        inventory=[10, 13, 18, 26, 37, 46, 55],
    )
    assert verdict(wc)["verdict"] == "working_capital_explained", verdict(wc)
    bad = base.assign(cfo=[9, 10, 12, 15, 18, 20, 21], receivables=20, inventory=10)
    assert verdict(bad)["verdict"] == "deteriorating"
    print(yearly_table(wc).round(2).to_string())
    print(verdict(wc))
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("ticker", nargs="?")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()
    if args.selftest or not args.ticker:
        selftest()
    else:
        from common.stocks_data import annual

        a = (
            annual(args.ticker, FIELDS)
            .sort_index()
            .dropna(subset=["net_income", "cfo"])
        )
        print(yearly_table(a).round(3).to_string())
        print(verdict(a))
