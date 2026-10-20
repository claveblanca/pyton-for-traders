"""ch03_bond_metrics.py -- price, yield and rate risk of one fixed-rate bond.

Ref: §3.2.2 (clean vs dirty price), §3.2.4 (effective yield, Figure 3.2),
PROOF §3.13.4 (Table 3.13: +1% parallel shock).

    accrued(coupon, last_coupon, settle, freq)   accrued coupon, ACT/ACT
    ytm(price, coupon, years, freq)              effective yield (root-finder)
    durations(ytm, coupon, years, freq)          Macaulay, modified, convexity
    shock_pnl(notional, mod_dur, convexity, dy)  price change for a rate move

Usage:
    python ch03_bond_metrics.py --selftest
    python ch03_bond_metrics.py --price 95 --coupon 5 --years 10
"""

from __future__ import annotations

import argparse
from datetime import date

import numpy as np
from scipy.optimize import brentq


def cashflows(coupon: float, years: float, freq: int = 1, face: float = 100.0):
    n = int(round(years * freq))
    t = np.arange(1, n + 1) / freq
    cf = np.full(n, coupon / freq)
    cf[-1] += face
    return t, cf


def price_from_yield(y: float, coupon: float, years: float, freq: int = 1) -> float:
    t, cf = cashflows(coupon, years, freq)
    return float(np.sum(cf / (1 + y / freq) ** (t * freq)))


def ytm(price: float, coupon: float, years: float, freq: int = 1) -> float:
    """Effective yield: the rate at which inflows repay the price paid (§3.2.4)."""
    return brentq(lambda y: price_from_yield(y, coupon, years, freq) - price, -0.5, 1.0)


def durations(y: float, coupon: float, years: float, freq: int = 1) -> dict:
    t, cf = cashflows(coupon, years, freq)
    disc = cf / (1 + y / freq) ** (t * freq)
    p = disc.sum()
    mac = float(np.sum(t * disc) / p)
    conv = float(np.sum(cf * t * (t + 1 / freq) / (1 + y / freq) ** (t * freq + 2)) / p)
    return {"macaulay": mac, "modified": mac / (1 + y / freq), "convexity": conv}


def accrued(
    coupon: float, last_coupon: date, next_coupon: date, settle: date, freq: int = 1
) -> float:
    """Accrued coupon per 100, ACT/ACT: dirty = clean + accrued (§3.2.2)."""
    return (
        coupon / freq * (settle - last_coupon).days / (next_coupon - last_coupon).days
    )


def shock_pnl(
    notional: float, mod_dur: float, convexity: float = 0.0, dy: float = 0.01
) -> float:
    """dP ≈ (-D_mod·dy + ½·C·dy²) · notional  (Table 3.13 uses the first term)."""
    return notional * (-mod_dur * dy + 0.5 * convexity * dy**2)


def selftest() -> None:
    assert abs(ytm(95, 5, 10) - 0.0567) < 5e-4  # Figure 3.2
    assert abs(ytm(100, 5, 10) - 0.05) < 1e-9
    assert abs(ytm(105, 5, 10) - 0.0437) < 5e-4
    d = durations(0.036, 3.6, 10)
    assert 8.0 < d["modified"] < 8.6  # "about 8.3"
    assert abs(shock_pnl(2000, 8.3) + 166) < 1e-9  # Table 3.13 long slice
    acc = accrued(5, date(2026, 3, 1), date(2027, 3, 1), date(2026, 9, 1))
    assert abs(acc - 5 * 184 / 365) < 1e-9
    print({k: round(v, 3) for k, v in d.items()}, "accrued:", round(acc, 3))
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--price", type=float)
    p.add_argument("--coupon", type=float)
    p.add_argument("--years", type=float)
    p.add_argument("--freq", type=int, default=1)
    p.add_argument("--notional", type=float, default=10_000)
    a = p.parse_args()
    if a.selftest or a.price is None:
        selftest()
    else:
        y = ytm(a.price, a.coupon, a.years, a.freq)
        d = durations(y, a.coupon, a.years, a.freq)
        print(
            f"effective yield {y:.4%}  Macaulay {d['macaulay']:.2f}  modified {d['modified']:.2f}"
            f"  convexity {d['convexity']:.1f}"
        )
        print(
            f"+1% shock on {a.notional:,.0f}: {shock_pnl(a.notional, d['modified'], d['convexity']):,.2f}"
        )
