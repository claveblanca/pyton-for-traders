"""ch04_ics.py -- Synthetic Cost Index, horizon cost, break-even and hurdle.

Ref: §4.4.1-4.4.8 (Tables 4.3, 4.5), PROOF §4.8.2-4.8.8 (Tables 4.8, 4.9).

All rates in percent, as the book prints them (TER 0.15 = 0.15%).
    ics(ter, spread)                     TER + 2 x spread       (§4.4)
    cost_pct(ter, spread, years)         TER x years + 2 x spread (§4.4.4)
    cost_eur(...)                        same, in euros, + optional commission
    break_even_years(a, b)               holding period where two costs meet (§4.4.7)
    spread_horizon(ter, spread)          2 x spread / TER       (§4.8.3)
    hurdle(spread, k=5)                  minimum target gain    (§4.4.6, §4.8.4)
    switch_payback_years(...)            years to repay a switch (§4.4.8, §4.8.8)

Usage:
    python ch04_ics.py --selftest
    python ch04_ics.py --amount 20000 --etf 500.PA:0.15:0.03 --etf X:0.07:0.08
"""

from __future__ import annotations

import argparse
import itertools

import pandas as pd


def ics(ter: float, spread: float) -> float:
    return ter + 2 * spread


def cost_pct(ter: float, spread: float, years: float) -> float:
    return ter * years + 2 * spread


def cost_eur(
    amount: float,
    ter: float,
    spread: float,
    years: float,
    commission_per_order: float = 0.0,
) -> float:
    return amount * cost_pct(ter, spread, years) / 100 + 2 * commission_per_order


def break_even_years(a: tuple[float, float], b: tuple[float, float]) -> float | None:
    """(ter, spread) pairs; None when one product is cheaper at every horizon."""
    (ta, sa), (tb, sb) = a, b
    if ta == tb:
        return None
    t = 2 * (sb - sa) / (ta - tb)
    return t if t > 0 else None


def spread_horizon(ter: float, spread: float) -> float:
    return 2 * spread / ter


def hurdle(spread: float, k: float = 5) -> float:
    return k * 2 * spread


def switch_payback_years(
    amount: float, ter_saving: float, spread: float, commission_per_order: float = 0.0
) -> float:
    cost = amount * 2 * spread / 100 + 2 * commission_per_order
    return cost / (amount * ter_saving / 100)


def table(
    amount: float,
    etfs: dict[str, tuple[float, float]],
    horizons=(1 / 12, 1, 10),
    commission: float = 0.0,
) -> pd.DataFrame:
    rows = []
    for name, (ter, spr) in etfs.items():
        r = {
            "etf": name,
            "ter": ter,
            "spread": spr,
            "ics": ics(ter, spr),
            "spread_horizon_m": spread_horizon(ter, spr) * 12,
            "hurdle_pct": hurdle(spr),
        }
        for h in horizons:
            label = f"eur_{round(h * 12)}m" if h < 1 else f"eur_{h:g}y"
            r[label] = cost_eur(amount, ter, spr, h, commission)
        rows.append(r)
    return pd.DataFrame(rows)


def break_evens(etfs: dict[str, tuple[float, float]]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"a": a, "b": b, "break_even_months": (be * 12 if be else None)}
            for a, b in itertools.combinations(etfs, 2)
            for be in [break_even_years(etfs[a], etfs[b])]
        ]
    )


def selftest() -> None:
    # Table 4.3
    assert round(cost_eur(10_000, 0.10, 0.10, 2 / 12), 2) == 21.67
    assert round(cost_eur(10_000, 0.30, 0.02, 10), 2) == 304
    assert (
        abs(break_even_years((0.10, 0.10), (0.30, 0.02)) * 12 - 9.6) < 1e-9
    )  # "about ten months"
    # Table 4.5 and §4.4.7 break-evens
    etfs = {"500.PA": (0.15, 0.03), "X": (0.07, 0.08), "Y": (0.20, 0.02)}
    t = table(20_000, etfs)
    assert [round(v, 2) for v in t["eur_1m"]] == [14.5, 33.17, 11.33]
    assert [round(v, 2) for v in t["eur_10y"]] == [312, 172, 408]
    assert abs(break_even_years(etfs["Y"], etfs["500.PA"]) - 0.4) < 1e-9
    assert abs(break_even_years(etfs["500.PA"], etfs["X"]) - 1.25) < 1e-9
    # Tables 4.8 / 4.9 and §4.8.8
    assert round(cost_eur(20_000, 0.38, 0.06, 1 / 12), 2) == 30.33
    assert round(spread_horizon(0.59, 0.34) * 12, 1) == 13.8  # "about 14 months"
    assert abs(hurdle(0.34) - 3.4) < 1e-12
    assert (
        round(switch_payback_years(20_000, 0.10, 0.34), 1) == 6.8
    )  # "about seven years"
    print(t.round(2).to_string(index=False))
    print(break_evens(etfs).round(1).to_string(index=False))
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--amount", type=float, default=20_000)
    p.add_argument("--etf", action="append", help="NAME:TER:SPREAD in percent")
    p.add_argument("--commission", type=float, default=0.0)
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.etf:
        selftest()
    else:
        etfs = {n: (float(t), float(s)) for n, t, s in (e.split(":") for e in a.etf)}
        print(
            table(a.amount, etfs, commission=a.commission)
            .round(2)
            .to_string(index=False)
        )
        print(break_evens(etfs).round(1).to_string(index=False))
