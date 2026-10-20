"""ch06_crypto_etn_premium.py -- crypto ETN premium/discount and coin flows.

Ref: §6.2.8 (coin entitlement, WARNING on timestamps), §6.2.9 (Table 6.9
data sources, Listings 6.1-6.2). Promoted from code_snippets/ch02/
ch02_crypto_etn.py.

    isin_to_tickers(isins)   OpenFIGI mapping (Listing 6.1)
    signals(df)              premium, premium z-score, coin flows (Listing 6.2)
    align_spot(etn, spot)    spot sampled at the ETN's own close timestamp
                             (17:30 CET for Xetra), never a midnight-UTC print

Usage:
    python ch06_crypto_etn_premium.py --selftest
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd


def isin_to_tickers(isins: list[str], api_key: str | None = None) -> pd.DataFrame:
    import requests  # lazy

    headers = {"X-OPENFIGI-APIKEY": api_key} if api_key else {}
    jobs = [{"idType": "ID_ISIN", "idValue": i} for i in isins[:100]]
    r = requests.post(
        "https://api.openfigi.com/v3/mapping", json=jobs, headers=headers, timeout=30
    )
    r.raise_for_status()
    return pd.DataFrame(
        [
            {"isin": i, "ticker": d.get("ticker"), "exch_code": d.get("exchCode")}
            for i, res in zip(isins, r.json())
            for d in res.get("data", [])
        ]
    )


def align_spot(etn_close: pd.Series, spot_intraday: pd.Series) -> pd.Series:
    """Spot as of each ETN close timestamp (last spot print at or before it)."""
    s = spot_intraday.sort_index()
    return pd.Series(s.reindex(etn_close.index, method="ffill").values, etn_close.index)


def signals(df: pd.DataFrame, window: int = 20, z_entry: float = 2.0) -> pd.DataFrame:
    """df per day: close, spot (EUR, same timestamp), coin_per_note, units."""
    out = pd.DataFrame(index=df.index)
    out["premium"] = df["close"] / (df["coin_per_note"] * df["spot"]) - 1
    out["coins_held"] = df["units"] * df["coin_per_note"]
    out["flow_coins"] = out["coins_held"].diff()
    st = out["premium"].rolling(window)
    out["premium_z"] = (out["premium"] - st.mean()) / st.std()
    out["retail_demand"] = out["premium_z"] > z_entry
    return out


def selftest() -> None:
    idx = pd.bdate_range("2026-06-01", periods=60, tz="Europe/Berlin") + pd.Timedelta(
        hours=17, minutes=30
    )
    rng = np.random.default_rng(8)
    spot = pd.Series(60_000 * np.exp(np.cumsum(rng.normal(0, 0.02, 60))), idx)
    fee_daily = 0.0095 / 365
    ent = 0.001 * (1 - fee_daily) ** np.arange(60)  # entitlement shrinks daily
    prem = np.r_[np.zeros(55), np.full(5, 0.03)]  # a 3% premium appears
    df = pd.DataFrame(
        {
            "close": ent * spot * (1 + prem),
            "spot": spot,
            "coin_per_note": ent,
            "units": np.r_[np.full(30, 1e6), np.full(30, 1.2e6)],
        },
        index=idx,
    )
    s = signals(df)
    assert abs(s["premium"].iloc[-1] - 0.03) < 1e-9 and s["retail_demand"].iloc[-5]
    assert s["flow_coins"].iloc[30] > 190  # 0.2M notes x ~0.001 coin
    intraday = pd.Series(spot.values, idx - pd.Timedelta(minutes=1))
    assert np.allclose(align_spot(df["close"], intraday).values, spot.values)
    print(s.tail(6).round(4).to_string())
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--isin", nargs="*")
    a = p.parse_args()
    if a.isin:
        print(isin_to_tickers(a.isin).to_string(index=False))
    else:
        selftest()
