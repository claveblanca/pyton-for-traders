"""ch06_etc_vs_futures_gap.py -- the roll cost made visible: ETC vs spot.

Ref: §6.1.3 (EUR/USD effect), §6.1.5 (Table 6.3, dashboard A "ETC vs spot
gap"), PROOF §6.4.7 (costs next to the carry).

An ETC earns the futures return, roll included, in its trading currency.
This script compares, over 1/3/12 months:
    etc_return          the EUR-listed ETC
    spot_return_usd     the front-month/spot commodity price (USD)
    spot_return_eur     the same converted to EUR
and decomposes the gap: fx = spot_eur - spot_usd; fee = TER x t;
roll_and_other = etc - spot_eur + fee  (what the curve took).

Usage:
    python ch06_etc_vs_futures_gap.py --selftest
    python ch06_etc_vs_futures_gap.py --etc BRNT.MI --spot BZ=F --fx EURUSD=X --ter 0.49
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def decompose(
    etc: pd.Series,
    spot_usd: pd.Series,
    eurusd: pd.Series,
    ter_pct: float,
    horizons_m=(1, 3, 12),
) -> pd.DataFrame:
    d = (
        pd.concat({"etc": etc, "spot": spot_usd, "fx": eurusd}, axis=1, sort=True)
        .ffill()
        .dropna()
    )
    d["spot_eur"] = d["spot"] / d["fx"]  # EURUSD = USD per EUR
    end = d.index[-1]
    rows = []
    for m in horizons_m:
        start = d.index[
            d.index.get_indexer([end - pd.DateOffset(months=m)], method="nearest")[0]
        ]
        r = d.loc[end] / d.loc[start] - 1
        fee = ter_pct / 100 * m / 12
        rows.append(
            {
                "months": m,
                "etc_return": r["etc"],
                "spot_return_usd": r["spot"],
                "spot_return_eur": r["spot_eur"],
                "fx_effect": r["spot_eur"] - r["spot"],
                "fee": -fee,
                "roll_and_other": r["etc"] - r["spot_eur"] + fee,
                "gap_total": r["etc"] - r["spot_eur"],
            }
        )
    return pd.DataFrame(rows).set_index("months")


def selftest() -> None:
    idx = pd.bdate_range("2025-01-01", periods=300)
    spot = pd.Series(100.0, idx)  # flat spot price
    contango_daily = (1 - 0.085) ** (1 / 252) - 1  # -8.5%/yr roll (Ch 6 §6.4.2 cocoa)
    ter_daily = 0.0049 / 252
    etc = pd.Series(10 * np.cumprod(np.full(300, 1 + contango_daily - ter_daily)), idx)
    fx = pd.Series(1.10, idx)
    g = decompose(etc, spot, fx, 0.49)
    assert abs(g.loc[12, "roll_and_other"] + 0.085) < 0.01  # roll recovered
    assert abs(g.loc[12, "fx_effect"]) < 1e-12
    fx_up = pd.Series(np.linspace(1.10, 1.21, 300), idx)  # euro +10%
    etc_eur = etc * 1.10 / fx_up  # unhedged EUR listing
    g2 = decompose(etc_eur, spot, fx_up, 0.49)
    assert g2.loc[12, "fx_effect"] < -0.05  # §6.1.3: EUR up, ETC down
    assert abs(g2.loc[12, "roll_and_other"] + 0.085) < 0.015  # roll still isolated
    print(g2.round(4).to_string())
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--etc")
    p.add_argument("--spot")
    p.add_argument("--fx", default="EURUSD=X")
    p.add_argument("--ter", type=float, default=0.49)
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.etc:
        selftest()
    else:
        from common.data import get_ohlcv

        print(
            decompose(
                get_ohlcv(a.etc)["close"],
                get_ohlcv(a.spot)["close"],
                get_ohlcv(a.fx)["close"],
                a.ter,
            )
            .round(4)
            .to_string()
        )
