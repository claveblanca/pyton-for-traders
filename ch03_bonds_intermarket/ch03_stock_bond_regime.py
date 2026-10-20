"""ch03_stock_bond_regime.py -- Rule A of Chapter 3: do bonds hedge stocks now?

Ref: §3.10.2 (Table 3.9 regimes), §3.11 Rule A (Table 3.11),
PROOF §3.13.5 (Table 3.14 rebalance triggers).

Rolling 30/60/90-day correlation of daily returns (stocks vs long Treasuries),
regime from the 90-day line (< 0 hedge | 0..0.2 neutral | > 0.2 together),
days in the current regime, and the Table 3.14 trigger.

Usage:
    python ch03_stock_bond_regime.py --selftest
    python ch03_stock_bond_regime.py --stock SPY --bond TLT
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def rolling_corr(
    stock: pd.Series, bond: pd.Series, windows=(30, 60, 90)
) -> pd.DataFrame:
    r = pd.DataFrame({"s": stock.pct_change(), "b": bond.pct_change()}).dropna()
    return pd.DataFrame({f"corr_{w}": r["s"].rolling(w).corr(r["b"]) for w in windows})


def regime(c90: float) -> str:
    return "hedge" if c90 < 0 else "neutral" if c90 <= 0.2 else "together"  # Table 3.9


def reading(corr: pd.DataFrame) -> dict:
    c = corr.dropna()
    labels = c["corr_90"].map(regime)
    run = int((labels[::-1] == labels.iloc[-1]).cumprod().sum())
    below0_month = bool((c["corr_90"].tail(21) < 0).all())
    trigger = (
        "move part of floaters into 7-10y fixed"
        if below0_month
        else (
            "hold: diversify but no hedge"
            if labels.iloc[-1] == "neutral"
            else (
                "keep long duration small; favour floaters/short/linkers"
                if labels.iloc[-1] == "together"
                else "long duration works as a hedge"
            )
        )
    )
    return {
        "date": str(c.index[-1].date()),
        **c.iloc[-1].round(3).to_dict(),
        "regime": labels.iloc[-1],
        "days_in_regime": run,
        "action": trigger,
    }


def selftest() -> None:
    rng = np.random.default_rng(1)
    n = 400
    z = rng.normal(0, 0.01, n)
    sign = np.r_[np.full(200, -0.8), np.full(200, 0.7)]  # hedge, then together
    b = sign * z + np.sqrt(1 - sign**2) * rng.normal(0, 0.01, n)
    idx = pd.bdate_range("2025-01-01", periods=n)
    stock, bond = pd.Series(100 * np.cumprod(1 + z), idx), pd.Series(
        100 * np.cumprod(1 + b), idx
    )
    c = rolling_corr(stock, bond)
    assert regime(c["corr_90"].iloc[150]) == "hedge"
    r = reading(c)
    assert r["regime"] == "together" and r["days_in_regime"] > 50
    print(r)
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--stock", default="SPY")
    p.add_argument("--bond", default="TLT")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        selftest()
    else:
        from common.data import get_ohlcv

        s, b = get_ohlcv(a.stock)["close"], get_ohlcv(a.bond)["close"]
        print(reading(rolling_corr(s, b)))
