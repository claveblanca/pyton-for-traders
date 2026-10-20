"""ch03_bond_score.py -- the §3.4 weighted, partial-credit bond score (0-100).

Ref: §3.3 (Table 3.2, seven checks), §3.4.1-3.4.3 (Table 3.3 weights,
partial credit, missing-data penalty); PROOF §3.13.4 ("each still has to
pass the Section 3.3 checks").

Input: one dict per bond (or a CSV with these columns):
    isin, rating, oas_bp, mod_duration, horizon_years, ytm,
    has_call, has_cap, has_tarn, regulated_market, adv_eur,
    structure ('fixed'|'floating'|'zero'|'inflation_linked'|'step'),
    laddered, seniority ('government'|'senior'|'tier2'|'tier1'|...)
inflation_regime: 'high' | 'normal' (from Ch 3 §3.9 / §3.10 reading)

Usage:
    python ch03_bond_score.py --selftest
    python ch03_bond_score.py candidates.csv --regime high
"""

from __future__ import annotations

import argparse
import math

import pandas as pd

WEIGHTS = {
    "credit": 20,
    "duration": 15,
    "clauses": 15,
    "liquidity": 15,
    "inflation": 15,
    "reinvestment": 10,
    "subordination": 10,
}  # Table 3.3
RATING_CREDIT = {
    "AAA": 1,
    "AA": 1,
    "A": 1,
    "BBB": 0.7,
    "BB": 0.3,
    "B": 0.0,
    "BAA": 0.7,
    "BA": 0.3,
}  # S&P/Fitch + Moody's
MIN_ADV_EUR = 50_000
MISSING_PENALTY = 0.15


def _missing(x) -> bool:
    return x is None or (isinstance(x, float) and math.isnan(x))


def credit(b: dict) -> float | None:
    if not _missing(b.get("rating")):
        r = str(b["rating"]).upper().rstrip("+-123 ")  # 'Aa2'/'BBB+' -> 'AA'/'BBB'
        return RATING_CREDIT.get(r, 0.0)
    if not _missing(b.get("oas_bp")):  # spread proxy (Table 3.2 #1)
        return 1.0 if b["oas_bp"] < 150 else 0.6 if b["oas_bp"] < 300 else 0.2
    return None


def duration_fit(b: dict) -> float | None:
    """Partial credit (§3.4.2): 6.2y vs a 6y horizon keeps most, 15y keeps none."""
    if _missing(b.get("mod_duration")):
        return None
    over = max(0.0, b["mod_duration"] - b["horizon_years"])
    return max(0.0, 1 - over / b["horizon_years"])


def liquidity(b: dict) -> float:
    if not b.get("regulated_market"):
        return 0.0
    return min(1.0, (b.get("adv_eur") or 0) / MIN_ADV_EUR)


def inflation_fit(b: dict, regime: str) -> float:
    if regime != "high":
        return 1.0
    return {
        "inflation_linked": 1.0,
        "floating": 0.7,
        "zero": 0.0,
        "fixed": 0.2,
        "step": 0.3,
    }.get(b.get("structure"), 0.2)


def score(b: dict, regime: str = "normal") -> dict:
    parts = {
        "credit": credit(b),
        "duration": duration_fit(b),
        "clauses": (
            0.0 if any(b.get(k) for k in ("has_call", "has_cap", "has_tarn")) else 1.0
        ),
        "liquidity": liquidity(b),
        "inflation": inflation_fit(b, regime),
        "reinvestment": (
            1.0 if b.get("laddered") or b.get("structure") == "zero" else 0.0
        ),
        "subordination": 1.0 if b.get("seniority") in ("government", "senior") else 0.0,
    }
    raw = sum(WEIGHTS[k] * (v or 0.0) for k, v in parts.items())
    n_missing = sum(
        _missing(x) for x in (parts["credit"], parts["duration"], b.get("ytm"))
    )
    final = raw * (1 - MISSING_PENALTY) ** n_missing  # §3.4.3
    return {
        "isin": b.get("isin"),
        "raw": round(raw, 1),
        "missing_fields": n_missing,
        "score": round(final, 1),
        **{f"s_{k}": v for k, v in parts.items()},
    }


def selftest() -> None:
    base = dict(
        isin="IT0000000001",
        rating="AA",
        mod_duration=6.2,
        horizon_years=6,
        ytm=0.034,
        has_call=False,
        regulated_market=True,
        adv_eur=80_000,
        structure="fixed",
        laddered=True,
        seniority="government",
    )
    s1 = score(base)
    assert s1["s_duration"] > 0.95 and s1["score"] > 95
    assert score({**base, "mod_duration": 15})["s_duration"] == 0.0  # §3.4.2
    assert score({**base, "has_call": True})["score"] == s1["score"] - 15
    miss = score({**base, "rating": None, "ytm": None})
    assert (
        miss["missing_fields"] == 2
        and abs(miss["score"] - (miss["raw"] * 0.85**2)) < 0.11
    )
    assert score(base, "high")["s_inflation"] == 0.2
    print(
        pd.DataFrame(
            [s1, miss, score({**base, "structure": "inflation_linked"}, "high")]
        ).to_string(index=False)
    )
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("csv", nargs="?")
    p.add_argument("--regime", default="normal", choices=["normal", "high"])
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.csv:
        selftest()
    else:
        rows = pd.read_csv(a.csv).to_dict("records")
        print(
            pd.DataFrame([score(r, a.regime) for r in rows])
            .sort_values("score", ascending=False)
            .to_string(index=False)
        )
