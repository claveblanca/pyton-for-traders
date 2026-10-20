"""ch04_spread_sampler.py -- a measured spread instead of one live quote.

Ref: §4.4.5 (Table 4.4: "a single live quote is unreliable in both
directions"), PROOF §4.8.2 (label the spread with its source); Ch 6 §6.4.7.

Samples bid/ask N times across the trading day and reports the median and
90th-percentile relative spread, plus how far a single snapshot sits from
the median (flag above 50%). The median is what goes into the ICS when no
exchange monthly figure exists.

    relative_spread(bid, ask)      (ask - bid) / mid, in percent
    summarise(samples)             median, p90, n, snapshot deviation flag
    sample_live(ticker, n, every)  yfinance fast_info bid/ask, every N seconds

Usage:
    python ch04_spread_sampler.py --selftest
    python ch04_spread_sampler.py AMEW.DE --n 12 --every 1800
"""

from __future__ import annotations

import argparse
import time

import numpy as np
import pandas as pd


def relative_spread(bid: float, ask: float) -> float:
    mid = (bid + ask) / 2
    return float((ask - bid) / mid * 100) if bid > 0 and ask > bid else np.nan


def summarise(samples: pd.DataFrame, snapshot_pct: float | None = None) -> dict:
    s = samples.apply(lambda r: relative_spread(r["bid"], r["ask"]), axis=1).dropna()
    out = {
        "n": int(len(s)),
        "median_pct": float(s.median()),
        "p90_pct": float(s.quantile(0.9)),
        "min_pct": float(s.min()),
        "max_pct": float(s.max()),
    }
    snap = snapshot_pct if snapshot_pct is not None else float(s.iloc[-1])
    dev = (snap - out["median_pct"]) / out["median_pct"]
    out.update(
        snapshot_pct=snap, snapshot_deviation=dev, snapshot_unreliable=abs(dev) > 0.5
    )
    return out


def sample_live(ticker: str, n: int = 12, every: int = 1800) -> pd.DataFrame:
    import yfinance as yf  # lazy

    rows = []
    for i in range(n):
        q = yf.Ticker(ticker).info
        rows.append(
            {"ts": pd.Timestamp.now(tz="UTC"), "bid": q.get("bid"), "ask": q.get("ask")}
        )
        if i < n - 1:
            time.sleep(every)
    return pd.DataFrame(rows).set_index("ts")


def selftest() -> None:
    rng = np.random.default_rng(3)
    mid = 100 + rng.normal(0, 0.2, 40)
    spr = (
        np.r_[np.full(30, 0.06), np.full(10, 0.025)] / 100 * mid
    )  # quiet hour at the end
    df = pd.DataFrame({"bid": mid - spr / 2, "ask": mid + spr / 2})
    s = summarise(df)
    assert (
        abs(s["median_pct"] - 0.06) < 1e-3 and s["snapshot_unreliable"]
    )  # quote understates
    thin = summarise(df, snapshot_pct=0.20)
    assert thin["snapshot_deviation"] > 1  # quote overstates
    print({k: round(v, 4) if isinstance(v, float) else v for k, v in s.items()})
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("ticker", nargs="?")
    p.add_argument("--n", type=int, default=12)
    p.add_argument("--every", type=int, default=1800)
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.ticker:
        selftest()
    else:
        print(summarise(sample_live(a.ticker, a.n, a.every)))
