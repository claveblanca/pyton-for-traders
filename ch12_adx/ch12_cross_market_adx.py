"""ch12_cross_market_adx.py -- rank a basket of markets by trend strength.

Ref: §12.7.3 (cross-market screening: concentrate trend-following capital in
the highest-ADX markets). Default basket = SPDR sector ETFs; pass any list,
or reuse code_snippets/sector_symbols/sector_symbol_map.py for constituents.

Per market: ADX, DI spread (+DI - -DI), direction, ADX slope, rank.
Top-N with ADX > 25 and rising ADX are the trend candidates.

Usage:
    python ch12_cross_market_adx.py --selftest
    python ch12_cross_market_adx.py XLE XLK XLU GLD USO BTC-USD --top 3
"""

from __future__ import annotations

import argparse
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common.data import get_ohlcv, synthetic_ohlcv  # noqa: E402
from common.indicators import adx  # noqa: E402

SECTOR_ETFS = [
    "XLB",
    "XLC",
    "XLE",
    "XLF",
    "XLI",
    "XLK",
    "XLP",
    "XLRE",
    "XLU",
    "XLV",
    "XLY",
]


def snapshot(frames: dict[str, pd.DataFrame], top: int = 3) -> pd.DataFrame:
    rows = []
    for name, df in frames.items():
        a = adx(df).dropna()
        last = a.iloc[-1]
        rows.append(
            {
                "market": name,
                "adx": last.adx,
                "di_spread": last.plus_di - last.minus_di,
                "direction": "up" if last.plus_di > last.minus_di else "down",
                "adx_slope3": a["adx"].diff(3).iloc[-1],
            }
        )
    t = pd.DataFrame(rows).sort_values("adx", ascending=False).reset_index(drop=True)
    t["rank"] = t.index + 1
    elig = (t.adx > 25) & (t.adx_slope3 > 0)
    t["candidate"] = elig & (elig.cumsum() <= top)
    return t


def selftest() -> None:
    frames = {
        f"M{i}": synthetic_ohlcv(400, seed=i, regimes=False, drift=d, vol=0.01)
        for i, d in enumerate([0.004, 0.0, -0.003, 0.0005, 0.0])
    }
    t = snapshot(frames)
    assert t.iloc[0]["market"] in {"M0", "M2"}  # strong drifts trend hardest
    assert t["candidate"].sum() <= 3
    print(t.round(2).to_string(index=False))
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("symbols", nargs="*")
    p.add_argument("--top", type=int, default=3)
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        selftest()
    else:
        syms = a.symbols or SECTOR_ETFS
        print(
            snapshot({s: get_ohlcv(s) for s in syms}, a.top)
            .round(2)
            .to_string(index=False)
        )
