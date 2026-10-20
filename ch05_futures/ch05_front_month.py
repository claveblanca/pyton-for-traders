"""ch05_front_month.py -- which contract month is live, and when volume rolls.

Ref: §5.1.5 (front month, month codes), §5.6.5 (Listing 5.3 liquidity
gate: volume and open interest migrate before expiry).

Input: daily settlements, one row per (trade_date, contract): columns
    trade_date, contract, expiry, volume, open_interest
Output per trade_date: front (nearest expiry), active (highest open interest),
whether the roll has happened (active != front), and the projected roll date
= first day the next contract's open interest exceeds the front's.

Usage:
    python ch05_front_month.py --selftest
    python ch05_front_month.py settlements.csv
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd

MONTH_CODES = dict(zip("FGHJKMNQUVXZ", range(1, 13)))


def parse_symbol(sym: str, decade: int = 2020) -> tuple[str, int, int]:
    """'CLZ6' -> ('CL', 2026, 12); 'MGCZ26' -> ('MGC', 2026, 12)  (§5.1.5)."""
    i = max(i for i, c in enumerate(sym) if c in MONTH_CODES and sym[i + 1 :].isdigit())
    yr = sym[i + 1 :]
    year = 2000 + int(yr) if len(yr) == 2 else decade + int(yr)
    return sym[:i], year, MONTH_CODES[sym[i]]


def active_months(s: pd.DataFrame) -> pd.DataFrame:
    s = s.copy()
    s["expiry"] = pd.to_datetime(s["expiry"])
    s["trade_date"] = pd.to_datetime(s["trade_date"])
    live = s[s["expiry"] >= s["trade_date"]]
    front = live.sort_values("expiry").groupby("trade_date").first()["contract"]
    active = live.sort_values("open_interest").groupby("trade_date").last()["contract"]
    out = pd.DataFrame({"front": front, "active": active})
    out["rolled"] = out["front"] != out["active"]
    return out


def roll_dates(a: pd.DataFrame) -> pd.Series:
    """First date each contract becomes the active (highest-OI) month."""
    return a.reset_index().groupby("active")["trade_date"].min().sort_values()


def selftest() -> None:
    assert parse_symbol("CLZ6") == ("CL", 2026, 12)
    assert parse_symbol("MGCZ26") == ("MGC", 2026, 12)
    days = pd.bdate_range("2026-11-01", "2026-11-30")
    rows = []
    for i, d in enumerate(days):
        w = i / len(days)
        rows += [
            {
                "trade_date": d,
                "contract": "CLZ6",
                "expiry": "2026-11-20",
                "volume": 300_000 * (1 - w),
                "open_interest": 400_000 * (1 - w),
            },
            {
                "trade_date": d,
                "contract": "CLF7",
                "expiry": "2026-12-18",
                "volume": 300_000 * w,
                "open_interest": 380_000 * w + 50_000,
            },
        ]
    a = active_months(pd.DataFrame(rows))
    rd = roll_dates(a)
    assert rd.index[-1] == "CLF7" and rd.iloc[-1] < pd.Timestamp("2026-11-20")
    assert a.loc[pd.Timestamp("2026-11-24"), "front"] == "CLF7"  # Z6 expired
    print(a.iloc[::4].to_string())
    print(rd)
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("csv", nargs="?")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.csv:
        selftest()
    else:
        am = active_months(pd.read_csv(a.csv))
        print(am.tail(20).to_string())
        print(roll_dates(am))
