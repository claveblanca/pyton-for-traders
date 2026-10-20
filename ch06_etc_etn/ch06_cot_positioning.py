"""ch06_cot_positioning.py -- CFTC managed-money positioning score by sector.

Ref: PROOF §6.4.6 (Table 6.10: score 0-100 and z-score per sector; >= 90
crowded long, <= 10 crowded short); also Ch 9 §9.7.3-9.7.4 (COT groups --
see LEGACY_MAP for how the Disaggregated categories map to them, audit X8).

Data: CFTC Disaggregated Futures-Only report, via the `cot_reports` package
(pip install cot_reports) -- columns used:
    'Market_and_Exchange_Names', 'Report_Date_as_YYYY-MM-DD',
    'M_Money_Positions_Long_All', 'M_Money_Positions_Short_All'
The report reflects Tuesday's positions and is published on Friday.

Usage:
    python ch06_cot_positioning.py --selftest
    python ch06_cot_positioning.py --year 2026
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd

WINDOW = 156  # 3 years of weekly reports
SECTORS = {
    "energy": ["CRUDE OIL", "BRENT", "NATURAL GAS", "GASOLINE", "HEATING OIL"],
    "precious_metals": ["GOLD", "SILVER", "PLATINUM", "PALLADIUM"],
    "industrial_metals": ["COPPER", "ALUMINUM", "ZINC", "NICKEL"],
    "agriculture": [
        "CORN",
        "WHEAT",
        "SOYBEAN",
        "COCOA",
        "COFFEE",
        "SUGAR",
        "COTTON",
        "LIVE CATTLE",
        "LEAN HOGS",
    ],
}
LEGACY_MAP = {
    "managed money": "large speculators (non-commercial)",
    "producer/merchant + swap dealers": "commercials (hedgers)",
    "non-reportable": "small speculators",
}


def score(net: pd.Series, window: int = WINDOW) -> tuple[int, float]:
    """Percentile (0-100) and z-score of the last net position (Ch 6 Listing 6.3)."""
    h, last = net.tail(window), net.iloc[-1]
    return round(float((h < last).mean() * 100)), round(
        float((last - h.mean()) / h.std()), 2
    )


def label(pct: float, z: float) -> str:
    if pct >= 90 or z > 1.5:
        return "Crowded long (contrarian caution)"
    if pct <= 10 or z < -1.5:
        return "Crowded short (contrarian caution)"
    return "Elevated spec long" if pct >= 70 else "Neutral positioning"


def sector_of(market: str) -> str | None:
    m = market.upper()
    return next((s for s, keys in SECTORS.items() if any(k in m for k in keys)), None)


def board(cot: pd.DataFrame) -> pd.DataFrame:
    c = cot.rename(
        columns={
            "Market_and_Exchange_Names": "market",
            "Report_Date_as_YYYY-MM-DD": "date",
            "M_Money_Positions_Long_All": "mm_long",
            "M_Money_Positions_Short_All": "mm_short",
        }
    )
    c["date"] = pd.to_datetime(c["date"])
    c["net"] = c["mm_long"] - c["mm_short"]
    c["sector"] = c["market"].map(sector_of)
    c = c.dropna(subset=["sector"])
    sec = c.groupby(["sector", "date"])["net"].sum().reset_index()
    rows = []
    for s, g in sec.groupby("sector"):
        pct, z = score(g.sort_values("date")["net"])
        rows.append(
            {
                "sector": s,
                "date": g["date"].max().date(),
                "score": pct,
                "z": z,
                "reading": label(pct, z),
            }
        )
    return pd.DataFrame(rows)


def fetch(year: int) -> pd.DataFrame:
    import cot_reports as cot  # lazy

    frames = [
        cot.cot_year(y, cot_report_type="disaggregated_fut")
        for y in range(year - 3, year + 1)
    ]
    return pd.concat(frames, ignore_index=True)


def selftest() -> None:
    rng = np.random.default_rng(6)
    dates = pd.date_range("2023-01-03", periods=200, freq="W-TUE")
    rows = []
    for mkt, trend in [
        ("GOLD - COMMODITY EXCHANGE INC.", 0),
        ("COCOA - ICE FUTURES U.S.", 1),
        ("CRUDE OIL, LIGHT SWEET - NEW YORK MERCANTILE EXCHANGE", 0),
    ]:
        base = rng.normal(0, 10_000, len(dates)).cumsum() * 0.1
        if trend:
            base[-10:] += 40_000  # recent crowding in agriculture
        for d, b in zip(dates, base):
            rows.append(
                {
                    "Market_and_Exchange_Names": mkt,
                    "Report_Date_as_YYYY-MM-DD": d.date(),
                    "M_Money_Positions_Long_All": 100_000 + b,
                    "M_Money_Positions_Short_All": 60_000,
                }
            )
    b = board(pd.DataFrame(rows)).set_index("sector")
    assert b.loc["agriculture", "score"] >= 90 and b.loc[
        "agriculture", "reading"
    ].startswith("Crowded long")
    assert label(40, -0.11) == "Neutral positioning"  # Table 6.10 energy row
    print(b.to_string())
    print(LEGACY_MAP)
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--year", type=int)
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.year:
        selftest()
    else:
        print(board(fetch(a.year)).to_string(index=False))
