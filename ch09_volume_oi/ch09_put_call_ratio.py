"""ch09_put_call_ratio.py -- put/call ratio as a contrary sentiment indicator.

Ref: §9.8.1-9.8.3 (high ratio = excessive bearishness, oversold; low ratio =
excessive bullishness, overbought; strongest alongside the price/volume/OI
read), PROOF §9.11 (check 4). Feeds Ch 11 §11.8 (ch11_sentiment_extremes.py).

    pcr_from_chain(chain)     volume- and OI-based ratio from one chain snapshot
    extremes(history)         z-score and percentile over 252 observations,
                              'excessive bearishness' / 'excessive bullishness'

Usage:
    python ch09_put_call_ratio.py --selftest
    python ch09_put_call_ratio.py SPY          # today's ratio from yfinance chains
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd


def pcr_from_chain(chain: pd.DataFrame) -> dict:
    """chain: type ('call'|'put'), volume, open_interest."""
    g = chain.groupby("type")[["volume", "open_interest"]].sum()
    return {
        "pcr_volume": float(g.loc["put", "volume"] / g.loc["call", "volume"]),
        "pcr_oi": float(g.loc["put", "open_interest"] / g.loc["call", "open_interest"]),
    }


def extremes(hist: pd.Series, window: int = 252, z_lim: float = 2.0) -> pd.DataFrame:
    h = hist.rolling(window, min_periods=60)
    out = pd.DataFrame(
        {
            "pcr": hist,
            "z": (hist - h.mean()) / h.std(),
            "pctile": hist.rolling(window, min_periods=60).rank(pct=True) * 100,
        }
    )
    out["reading"] = np.select(
        [out.z >= z_lim, out.z <= -z_lim],
        [
            "excessive bearishness (contrarian bullish)",
            "excessive bullishness (contrarian bearish)",
        ],
        "no extreme",
    )
    return out


def live(ticker: str, n_expiries: int = 4) -> dict:
    import yfinance as yf  # lazy

    tk = yf.Ticker(ticker)
    frames = []
    for e in tk.options[:n_expiries]:
        oc = tk.option_chain(e)
        frames += [oc.calls.assign(type="call"), oc.puts.assign(type="put")]
    ch = pd.concat(frames).rename(columns={"openInterest": "open_interest"}).fillna(0)
    return pcr_from_chain(ch)


def selftest() -> None:
    ch = pd.DataFrame(
        {
            "type": ["call", "call", "put", "put"],
            "volume": [100, 300, 250, 350],
            "open_interest": [1000, 1000, 900, 1100],
        }
    )
    r = pcr_from_chain(ch)
    assert r == {"pcr_volume": 1.5, "pcr_oi": 1.0}
    rng = np.random.default_rng(9)
    hist = pd.Series(
        0.9 + rng.normal(0, 0.08, 400), pd.bdate_range("2025-01-01", periods=400)
    )
    hist.iloc[-1] = 1.4  # panic day
    e = extremes(hist)
    assert e["reading"].iloc[-1].startswith("excessive bearishness")
    print(e.tail(3).round(3).to_string())
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("ticker", nargs="?")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    selftest() if a.selftest or not a.ticker else print(live(a.ticker))
