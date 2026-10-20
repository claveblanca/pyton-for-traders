"""ch11_sentiment_extremes.py -- contrary opinion as numbers.

Ref: §11.8.1-11.8.3 (Contrary Opinion; Market Vane equilibrium ~55%,
extremes > 90% / < 20%; Investors Intelligence > 55% bullish / < 35%).
NOTE: the free sources below (AAII, crypto Fear & Greed) are not named in
§11.8 yet -- one sentence there would cover them (see the code proposals).

    survey_reading(bull_pct, scheme)   extreme flag on the book's thresholds
    percentile_extremes(series)        z-score / percentile for any sentiment series
    fear_greed_crypto()                alternative.me API (free, no key)
    aaii(csv)                          AAII weekly survey export (bullish, bearish %)
Put/call extremes come from ../ch09_volume_oi/ch09_put_call_ratio.py.

Usage:
    python ch11_sentiment_extremes.py --selftest
    python ch11_sentiment_extremes.py --crypto
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd

SCHEMES = {
    "market_vane": (90, 20),  # §11.8.2
    "investors_intelligence": (55, 35),
}  # §11.8.3


def survey_reading(bull_pct: float, scheme: str) -> str:
    hi, lo = SCHEMES[scheme]
    return (
        "excessive optimism (contrarian bearish)"
        if bull_pct > hi
        else (
            "excessive pessimism (contrarian bullish)"
            if bull_pct < lo
            else "no extreme"
        )
    )


def percentile_extremes(
    s: pd.Series, window: int = 260, z_lim: float = 2.0
) -> pd.DataFrame:
    r = s.rolling(window, min_periods=52)
    out = pd.DataFrame(
        {
            "value": s,
            "z": (s - r.mean()) / r.std(),
            "pctile": s.rolling(window, min_periods=52).rank(pct=True) * 100,
        }
    )
    out["reading"] = np.select(
        [out.z >= z_lim, out.z <= -z_lim],
        ["crowd euphoric (contrarian bearish)", "crowd fearful (contrarian bullish)"],
        "no extreme",
    )
    return out


def fear_greed_crypto(limit: int = 400) -> pd.Series:
    import requests  # lazy

    d = requests.get(
        f"https://api.alternative.me/fng/?limit={limit}", timeout=30
    ).json()["data"]
    return pd.Series(
        {pd.to_datetime(int(x["timestamp"]), unit="s"): float(x["value"]) for x in d}
    ).sort_index()


def aaii(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, parse_dates=[0], index_col=0)
    df["bull_bear_spread"] = df["bullish"] - df["bearish"]
    return percentile_extremes(df["bull_bear_spread"])


def selftest() -> None:
    assert survey_reading(92, "market_vane").startswith("excessive optimism")
    assert survey_reading(30, "investors_intelligence").startswith(
        "excessive pessimism"
    )
    assert survey_reading(50, "investors_intelligence") == "no extreme"
    rng = np.random.default_rng(12)
    s = pd.Series(
        50 + rng.normal(0, 8, 300), pd.date_range("2021-01-01", periods=300, freq="W")
    )
    s.iloc[-1] = 12  # extreme fear
    e = percentile_extremes(s)
    assert e["reading"].iloc[-1].startswith("crowd fearful")
    print(e.tail(3).round(2).to_string())
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--crypto", action="store_true")
    p.add_argument("--aaii")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.crypto:
        print(percentile_extremes(fear_greed_crypto()).tail(5).round(2).to_string())
    elif a.aaii:
        print(aaii(a.aaii).tail(5).round(2).to_string())
    else:
        selftest()
