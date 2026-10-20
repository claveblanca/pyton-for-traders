"""ch05_curve_roll.py -- forward-curve state and roll yield, annualised correctly.

Ref: §5.2.2 (Table 5.3), §5.2.3 (cocoa curve, Figures 5.1-5.2);
shared with Ch 6 PROOF §6.4.1-6.4.3.

    curve_table(quotes)           price per contract month, M1..Mn, slope labels
    roll_yield(front, nxt, gap_m) per-roll and annualised by the REAL gap
    annualise_variants(...)       the three numbers of Figure 5.2: per roll,
                                  per year at the real gap, per year over the
                                  days left before the roll (dashboard style)

Settles audit item X6: Ch 5 and Ch 6 both quote a dashboard figure; this
script prints every convention side by side so the one in use is explicit.

Usage:
    python ch05_curve_roll.py --selftest
    python ch05_curve_roll.py curve.csv            # columns: contract, expiry, price
"""

from __future__ import annotations

import argparse

import pandas as pd


def roll_yield(front: float, nxt: float, gap_months: float) -> tuple[float, float]:
    """Per-roll yield for a long holder (+ backwardation, - contango) and annualised."""
    per = front / nxt - 1
    return per, (1 + per) ** (12 / gap_months) - 1


def annualise_variants(
    front: float, nxt: float, gap_months: float, days_to_roll: int
) -> dict:
    per, yr = roll_yield(front, nxt, gap_months)
    return {
        "per_roll": per,
        "annual_real_gap": yr,
        "annual_days_to_roll": (1 + per) ** (365 / days_to_roll) - 1,
        "annual_monthly_assumption": (1 + per) ** 12 - 1,
    }


def curve_table(quotes: pd.DataFrame) -> pd.DataFrame:
    q = quotes.sort_values("expiry").reset_index(drop=True)
    q["m"] = [f"M{i + 1}" for i in range(len(q))]
    q["step"] = q["price"].diff()
    q["shape"] = q["step"].map(
        lambda s: "" if pd.isna(s) else "contango" if s > 0 else "backwardation"
    )
    gap = (pd.to_datetime(q["expiry"]).diff().dt.days / 30.44).round()
    q["roll_from_prev_pct"] = (q["price"].shift(1) / q["price"] - 1) * 100
    q["annualised_pct"] = ((1 + q["roll_from_prev_pct"] / 100) ** (12 / gap) - 1) * 100
    return q


def state(q: pd.DataFrame) -> str:
    s = set(q["shape"].iloc[1:])
    return (
        s.pop()
        if len(s) == 1
        else "mixed ("
        + ", ".join(
            f"{a}->{b}: {c}"
            for a, b, c in zip(q.m.shift(1).iloc[1:], q.m.iloc[1:], q["shape"].iloc[1:])
        )
        + ")"
    )


def selftest() -> None:
    v = annualise_variants(5796, 5922, 3, 61)  # Ch 5 §5.2.3
    assert round(v["per_roll"] * 100, 2) == -2.13
    # book: "about -8.3%" (compounded from the rounded -2.13%); exact value is -8.24%
    assert abs(v["annual_real_gap"] * 100 + 8.24) < 0.01
    # book quotes the dashboard's -12.11%; 61 days to roll reproduces -12.07%
    assert abs(v["annual_days_to_roll"] * 100 + 12.1) < 0.05
    w = annualise_variants(5619, 5745, 3, 61)  # Ch 6 §6.4.2
    assert (
        round(w["per_roll"] * 100, 2) == -2.19
        and round(w["annual_real_gap"] * 100, 1) == -8.5
    )
    assert (
        abs(((1 + w["per_roll"]) ** 6 - 1) * 100 + 12.46) < 0.01
    )  # Ch 6 dashboard -12.46%
    b = roll_yield(104.32, 97.44, 1)  # Brent, monthly
    assert round(b[0] * 100, 2) == 7.06 and round(b[1] * 100, 1) == 126.8
    quotes = pd.DataFrame(
        {
            "contract": ["CCZ26", "CCH27", "CCK27", "CCN27", "CCU27", "CCZ27"],
            "expiry": [
                "2026-12-15",
                "2027-03-15",
                "2027-05-14",
                "2027-07-16",
                "2027-09-15",
                "2027-12-15",
            ],
            "price": [5796, 5922, 5990, 6020, 6035, 5962],
        }
    )
    q = curve_table(quotes)
    assert state(q).startswith("mixed")
    print(q.round(2).to_string(index=False))
    print(state(q))
    print({k: round(x * 100, 2) for k, x in v.items()})
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("csv", nargs="?")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.csv:
        selftest()
    else:
        q = curve_table(pd.read_csv(a.csv))
        print(q.round(3).to_string(index=False))
        print(state(q))
