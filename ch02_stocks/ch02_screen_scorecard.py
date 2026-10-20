"""ch02_screen_scorecard.py -- Chapter 2 PROOF (§2.9) as a multi-ticker screen.

Ref: §2.3.1-2.3.3 (negative filters), §2.4.1-2.4.3 (CAPE-style P/E, 16x
ceiling, value trap), PROOF §2.9 Steps 2-9 and the checklist §2.9.10.

Per ticker: debt ratio on tangible assets, 7-year pooled interest coverage,
7-year pooled Cash Flow Index, CAPE-style P/E, fair price at 16x, margin of
safety, value-trap flags, and the stage where the screen stops:
    rejected_stage_1 | fails_valuation | watch | candidate

Usage:
    python ch02_screen_scorecard.py --selftest
    python ch02_screen_scorecard.py NVDA MSFT KO        # live (ch02_data via common.stocks_data)
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))

LIMITS = {"debt_ratio": 0.60, "coverage": 3.0, "cfi": 1.0, "pe_max": 16.0}
FIELDS = [
    "total_assets",
    "total_liabilities",
    "goodwill",
    "other_intangibles",
    "revenue",
    "ebit",
    "interest_expense",
    "net_income",
    "cfo",
]


def negative_filters(a: pd.DataFrame, years: int = 7) -> dict:
    """Stage 1 (§2.3): a is annual data, index = fiscal year, oldest first."""
    w = a.tail(years)
    last = a.iloc[-1]
    tangible = (
        last["total_assets"]
        - last.get("goodwill", 0)
        - last.get("other_intangibles", 0)
    )
    out = {
        "debt_ratio": last["total_liabilities"] / tangible,
        "coverage_7y": w["ebit"].sum() / w["interest_expense"].sum(),
        "cfi_7y": w["cfo"].sum() / w["net_income"].sum(),
    }
    out["pass_debt"] = out["debt_ratio"] <= LIMITS["debt_ratio"]
    out["pass_coverage"] = out["coverage_7y"] >= LIMITS["coverage"]
    out["pass_cfi"] = out["cfi_7y"] >= LIMITS["cfi"]
    return out


def valuation(a: pd.DataFrame, price: float, shares: float, years: int = 7) -> dict:
    """Stage 3 (§2.4.1-2.4.2): price against cycle-average earnings."""
    avg_ni = a["net_income"].tail(years).mean()
    mcap = price * shares
    fair = LIMITS["pe_max"] * avg_ni / shares
    return {
        "avg_net_income": avg_ni,
        "pe_last": mcap / a["net_income"].iloc[-1],
        "cape_pe": mcap / avg_ni,
        "fair_price_16x": fair,
        "margin_of_safety": (fair - price) / price,
        "pass_valuation": mcap / avg_ni <= LIMITS["pe_max"],
    }


def value_trap(a: pd.DataFrame) -> dict:
    """Stage 2 (§2.4.3, Step 8): structural decline or cyclicality."""
    rev = a["revenue"].dropna()
    g = rev.pct_change().dropna()
    yrs = len(rev) - 1
    return {
        "revenue_cagr": (
            (rev.iloc[-1] / rev.iloc[0]) ** (1 / yrs) - 1 if yrs else np.nan
        ),
        "down_years": int((g < 0).sum()),
        "last_growth": float(g.iloc[-1]),
        "declining": bool(g.tail(3).mean() < 0),
    }


def screen(ticker: str, a: pd.DataFrame, price: float, shares: float) -> dict:
    nf, vt, val = negative_filters(a), value_trap(a), valuation(a, price, shares)
    if not (nf["pass_debt"] and nf["pass_coverage"] and nf["pass_cfi"]):
        stage = "rejected_stage_1"
    elif vt["declining"]:
        stage = "watch"
    elif not val["pass_valuation"]:
        stage = "fails_valuation"
    else:
        stage = "candidate"
    return {"ticker": ticker, "stage": stage, **nf, **vt, **val}


def run(rows: list[dict]) -> pd.DataFrame:
    order = {"candidate": 0, "watch": 1, "fails_valuation": 2, "rejected_stage_1": 3}
    df = pd.DataFrame(rows)
    return (
        df.assign(_o=df["stage"].map(order))
        .sort_values(["_o", "margin_of_safety"], ascending=[True, False])
        .drop(columns="_o")
    )


# ----------------------------------------------------------------- data
def mock_nvda() -> tuple[pd.DataFrame, float, float]:
    """NVIDIA fiscal 2020-2026 net income as printed in §2.9.6 ($ billions)."""
    ni = [2.8, 4.3, 9.8, 4.4, 29.8, 72.9, 120.1]
    a = pd.DataFrame(
        {
            "net_income": ni,
            "revenue": [10.9, 16.7, 26.9, 27.0, 60.9, 130.5, 215.9],
            "ebit": [2.8, 4.5, 10.0, 4.2, 33.0, 81.5, 130.4],
            "interest_expense": [0.05, 0.18, 0.24, 0.26, 0.26, 0.25, 0.26],
            "cfo": [4.8, 5.8, 9.1, 5.6, 28.1, 64.1, 102.7],
            "total_assets": [17.3, 28.8, 44.2, 41.2, 65.7, 111.6, 206.0],
            "total_liabilities": [5.1, 11.9, 17.6, 19.1, 22.8, 32.3, 49.3],
            "goodwill": [0.6, 4.2, 4.3, 4.4, 4.4, 5.2, 6.0],
            "other_intangibles": [0.0, 0.5, 2.3, 1.7, 1.1, 0.8, 18.1],
        },
        index=range(2020, 2027),
    )
    return a, 239.0, 24.5


def live(ticker: str) -> tuple[pd.DataFrame, float, float]:
    from common.stocks_data import annual, price_and_shares

    a = annual(ticker, FIELDS).sort_index().dropna(subset=["net_income"])
    price, shares = price_and_shares(ticker)
    return a, price, shares


def selftest() -> None:
    a, px, sh = mock_nvda()
    r = screen("NVDA", a, px, sh)
    assert abs(r["avg_net_income"] - 34.87) < 0.01  # §2.9.6
    assert abs(r["cape_pe"] - 168) < 1 and abs(r["pe_last"] - 48.8) < 0.1  # §2.9.7
    assert abs(r["fair_price_16x"] - 22.8) < 0.1  # "about $23"
    assert r["cfi_7y"] < 1 and r["stage"] == "rejected_stage_1"  # Step 5 verdict
    healthy = a.assign(cfo=a["net_income"] * 1.2, net_income=a["net_income"])
    assert screen("X", healthy, 20.0, sh)["stage"] in {"candidate", "fails_valuation"}
    print(
        run([r, screen("NVDA_cfo_ok", healthy, px, sh)])[
            [
                "ticker",
                "stage",
                "debt_ratio",
                "coverage_7y",
                "cfi_7y",
                "cape_pe",
                "fair_price_16x",
                "margin_of_safety",
            ]
        ]
        .round(2)
        .to_string(index=False)
    )
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("tickers", nargs="*")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()
    if args.selftest or not args.tickers:
        selftest()
    else:
        rows = [screen(t, *live(t)) for t in args.tickers]
        print(run(rows).round(3).to_string(index=False))
