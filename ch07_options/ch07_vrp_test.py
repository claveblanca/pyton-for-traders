"""ch07_vrp_test.py -- does implied volatility overstate the volatility that follows?

Ref: PROOF §7.13 part B (the edge behind Rule 15), §7.7.1-7.7.2 (implied vs
realised; sell premium when IV rank is high), §7.7.3 (the VIX).

Free data: daily ^VIX and SPY closes from yfinance (about 10 years).
Method: non-overlapping 21-trading-day blocks. At each block start read the
VIX (30-day implied volatility of the S&P 500, in vol points) and its 1-year
rank; over the next 21 days measure SPY's realised volatility (close-to-close,
annualised, in vol points). Gap = VIX - realised. Bucket by VIX rank:
low (<= 30), mid, high (>= 50) -- the IV-rank bands of Table 7.4.

Report per bucket: blocks, mean gap, share of positive gaps, worst gap.

Usage:
    python ch07_vrp_test.py --selftest
    python ch07_vrp_test.py --live --years 10
"""

from __future__ import annotations

import argparse

import numpy as np
import pandas as pd


def blocks(vix: pd.Series, close: pd.Series, h: int = 21) -> pd.DataFrame:
    df = pd.concat({"vix": vix, "close": close}, axis=1).dropna()
    rank = df.vix.rolling(252).apply(lambda w: (w[-1] - w.min()) / (w.max() - w.min()) * 100,
                                     raw=True)
    lr = np.log(df.close).diff()
    rows = []
    for i in range(252, len(df) - h, h):  # non-overlapping, after a 1-year warm-up
        rv = lr.iloc[i + 1:i + 1 + h].std() * np.sqrt(252) * 100
        rows.append({"date": df.index[i], "vix": df.vix.iloc[i], "rank": rank.iloc[i],
                     "realised": rv, "gap": df.vix.iloc[i] - rv})
    return pd.DataFrame(rows).set_index("date")


def summary(b: pd.DataFrame) -> pd.DataFrame:
    b = b.assign(bucket=pd.cut(b["rank"], [-1, 30, 50, 101],
                               labels=["low (<=30)", "mid", "high (>=50)"], right=False))
    g = b.groupby("bucket", observed=False)["gap"]
    out = pd.DataFrame({"blocks": g.size(), "mean_gap": g.mean(),
                        "share_positive": g.apply(lambda x: (x > 0).mean()),
                        "worst_gap": g.min()})
    out.loc["all"] = [len(b), b.gap.mean(), (b.gap > 0).mean(), b.gap.min()]
    return out.round(2)


def live(years: int = 10) -> pd.DataFrame:
    import yfinance as yf

    px = yf.download(["^VIX", "SPY"], period=f"{years + 1}y", auto_adjust=True,
                     progress=False)["Close"]
    return summary(blocks(px["^VIX"], px["SPY"]))


def selftest() -> None:
    rng = np.random.default_rng(7)
    n = 252 * 8
    vol = np.clip(16 + np.cumsum(rng.normal(0, 0.6, n)) * 0.3, 9, 60)  # realised regime
    ret = rng.normal(0, vol / 100 / np.sqrt(252))
    idx = pd.bdate_range("2017-01-02", periods=n)
    close = pd.Series(100 * np.exp(np.cumsum(ret)), idx)
    vix = pd.Series(vol * 1.15 + rng.normal(0, 1.0, n), idx)  # IV priced ~15% rich
    b = blocks(vix, close)
    s = summary(b)
    assert len(b) == (n - 252 - 21 - 1) // 21 + 1
    assert s.loc["all", "mean_gap"] > 0 and s.loc["all", "share_positive"] > 0.5
    print(s.to_string())
    print("selftest OK")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--years", type=int, default=10)
    a = ap.parse_args()
    print(live(a.years).to_string() if a.live else "") if a.live else selftest()
