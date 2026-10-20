"""ch03_bond_endpoints.py -- the free public series behind Chapter 3.

Ref: §3.12.1 (cites `bond_data_endpoints.py` -- this is that file),
PROOF §3.13.1 (the reading: €STR, 6M Euribor + fixing date, US 10Y).

    estr()            ECB €STR, daily (%)
    euribor(tenor)    ECB monthly Euribor, '3M' | '6M' (%), with fixing date
    hicp()            euro-area HICP index (2015=100) and annual rate (%)
    fred_csv(id)      any FRED series without an API key (DGS10, DGS2, ...)
    reading()         one dated snapshot dict -- the §3.13.1 reading

Sources (no key needed): ECB Data Portal SDMX API (data-api.ecb.europa.eu)
and FRED's public CSV endpoint (fred.stlouisfed.org/graph/fredgraph.csv).
Euribor in the ECB series is a monthly average -- check the date before
computing a coupon (Ch 3 WARNING "Using a stale Euribor").

Usage:
    python ch03_bond_endpoints.py --selftest
    python ch03_bond_endpoints.py            # live snapshot
"""

from __future__ import annotations

import argparse
import io

import pandas as pd

ECB = "https://data-api.ecb.europa.eu/service/data/{flow}/{key}?format=csvdata"
SERIES = {
    "estr": ("EST", "B.EU000A2X2A25.WT"),
    "euribor_3m": ("FM", "M.U2.EUR.RT.MM.EURIBOR3MD_.HSTA"),
    "euribor_6m": ("FM", "M.U2.EUR.RT.MM.EURIBOR6MD_.HSTA"),
    "hicp_index": ("ICP", "M.U2.N.000000.4.INX"),
    "hicp_yoy": ("ICP", "M.U2.N.000000.4.ANR"),
}
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"


def parse_ecb_csv(text: str) -> pd.Series:
    df = pd.read_csv(io.StringIO(text))
    s = pd.Series(
        pd.to_numeric(df["OBS_VALUE"], errors="coerce").values,
        index=pd.to_datetime(df["TIME_PERIOD"]),
    )
    return s.dropna().sort_index()


def parse_fred_csv(text: str) -> pd.Series:
    df = pd.read_csv(io.StringIO(text))
    s = pd.Series(
        pd.to_numeric(df.iloc[:, 1], errors="coerce").values,
        index=pd.to_datetime(df.iloc[:, 0]),
    )
    return s.dropna().sort_index()


def _get(url: str) -> str:
    import requests  # lazy

    r = requests.get(url, timeout=30, headers={"Accept": "text/csv"})
    r.raise_for_status()
    return r.text


def ecb(name: str) -> pd.Series:
    flow, key = SERIES[name]
    return parse_ecb_csv(_get(ECB.format(flow=flow, key=key)))


def estr() -> pd.Series:
    return ecb("estr")


def euribor(tenor: str = "6M") -> pd.Series:
    return ecb(f"euribor_{tenor.lower()}")


def hicp() -> pd.DataFrame:
    return pd.DataFrame({"index": ecb("hicp_index"), "yoy": ecb("hicp_yoy")})


def fred_csv(series_id: str) -> pd.Series:
    return parse_fred_csv(_get(FRED.format(sid=series_id)))


def snapshot(series: dict[str, pd.Series]) -> dict:
    """Latest value + its date for each series: the §3.13.1 reading."""
    return {
        k: {
            "value": round(float(s.iloc[-1]), 4),
            "date": s.index[-1].date().isoformat(),
        }
        for k, s in series.items()
        if len(s)
    }


def reading() -> dict:
    return snapshot(
        {
            "estr": estr(),
            "euribor_6m": euribor("6M"),
            "hicp_yoy": ecb("hicp_yoy"),
            "us10y": fred_csv("DGS10"),
            "us2y": fred_csv("DGS2"),
        }
    )


def selftest() -> None:
    ecb_txt = (
        "KEY,FREQ,TIME_PERIOD,OBS_VALUE\n"
        "EST.B.EU000A2X2A25.WT,B,2026-09-22,2.441\nEST.B.EU000A2X2A25.WT,B,2026-09-23,2.44\n"
    )
    fred_txt = (
        "observation_date,DGS10\n2026-09-22,5.10\n2026-09-23,5.11\n2026-09-24,.\n"
    )
    snap = snapshot({"estr": parse_ecb_csv(ecb_txt), "us10y": parse_fred_csv(fred_txt)})
    assert snap["estr"] == {"value": 2.44, "date": "2026-09-23"}
    assert snap["us10y"] == {
        "value": 5.11,
        "date": "2026-09-23",
    }  # '.' (missing) dropped
    print(snap)
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()
    selftest() if args.selftest else print(reading())
