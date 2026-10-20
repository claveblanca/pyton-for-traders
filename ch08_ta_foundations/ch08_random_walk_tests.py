"""ch08_random_walk_tests.py -- §8.4.2 "markets trend" tested, not asserted.

Ref: §8.4.2 (random walk theory and the technical answer), §8.1.2 (prices
move in trends), WARNING after §8.4.2 ("disproving randomness is not the
same as any pattern you see is real").

    variance_ratio(close, q)   Lo-MacKinlay VR(q) and its heteroskedasticity-
                               robust z-statistic. VR > 1 = trending
                               (positive autocorrelation), < 1 = mean-reverting
    autocorr(close, lags)      return autocorrelations + Ljung-Box p-value
    hurst(close)               Hurst exponent from aggregated-variance scaling:
                               0.5 = random walk, > 0.5 persistent, < 0.5 anti
    report(close)              one table per instrument

Usage:
    python ch08_random_walk_tests.py --selftest
    python ch08_random_walk_tests.py SPY GLD BTC-USD
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common.data import get_ohlcv  # noqa: E402


def variance_ratio(close: pd.Series, q: int) -> dict:
    x = np.log(close.dropna().values)
    r = np.diff(x)
    n = len(r)
    mu = r.mean()
    var1 = np.sum((r - mu) ** 2) / (n - 1)
    rq = x[q:] - x[:-q]
    m = q * (n - q + 1) * (1 - q / n)
    varq = np.sum((rq - q * mu) ** 2) / m
    vr = varq / var1
    # heteroskedasticity-robust asymptotic variance (Lo & MacKinlay 1988)
    e2 = (r - mu) ** 2
    theta = sum(
        ((2 * (q - j) / q) ** 2) * np.sum(e2[j:] * e2[:-j]) / np.sum(e2) ** 2
        for j in range(1, q)
    )
    z = (vr - 1) / np.sqrt(theta) if theta > 0 else np.nan
    return {
        "q": q,
        "vr": float(vr),
        "z": float(z),
        "p": float(2 * (1 - stats.norm.cdf(abs(z)))),
    }


def autocorr(close: pd.Series, lags: int = 10) -> dict:
    r = np.log(close).diff().dropna()
    ac = [r.autocorr(k) for k in range(1, lags + 1)]
    n = len(r)
    lb = n * (n + 2) * sum(a**2 / (n - k) for k, a in enumerate(ac, 1))
    return {
        "ac1": float(ac[0]),
        "ljung_box_q": float(lb),
        "lb_p": float(1 - stats.chi2.cdf(lb, lags)),
    }


def hurst(close: pd.Series, scales=(1, 2, 4, 8, 16, 32)) -> float:
    r = np.log(close).diff().dropna().values
    v = []
    for s in scales:
        k = len(r) // s
        agg = r[: k * s].reshape(k, s).sum(axis=1)
        v.append(agg.var())
    slope = np.polyfit(np.log(scales), np.log(v), 1)[0]
    return float(slope / 2)


def report(close: pd.Series) -> dict:
    out = {f"vr_{q}": round(variance_ratio(close, q)["vr"], 3) for q in (2, 5, 10)}
    out.update(
        {f"vr_{q}_p": round(variance_ratio(close, q)["p"], 4) for q in (2, 5, 10)}
    )
    out.update({k: round(v, 4) for k, v in autocorr(close).items()})
    h = hurst(close)
    out["hurst"] = round(h, 3)
    out["reading"] = (
        "trending"
        if out["vr_10"] > 1 and out["vr_10_p"] < 0.05
        else (
            "mean-reverting"
            if out["vr_10"] < 1 and out["vr_10_p"] < 0.05
            else "not distinguishable from a random walk"
        )
    )
    return out


def selftest() -> None:
    rng = np.random.default_rng(11)
    n = 3000
    rw = pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.01, n))))
    e = rng.normal(0, 0.01, n)
    ar = np.zeros(n)
    for t in range(1, n):
        ar[t] = 0.3 * ar[t - 1] + e[t]  # persistent returns
    tr = pd.Series(100 * np.exp(np.cumsum(ar)))
    a, b = report(rw), report(tr)
    assert a["reading"] == "not distinguishable from a random walk", a
    assert b["reading"] == "trending" and b["vr_10"] > 1.3 and b["hurst"] > 0.55
    print(pd.DataFrame([a, b], index=["random walk", "AR(0.3) returns"]).T.to_string())
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("symbols", nargs="*")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.symbols:
        selftest()
    else:
        print(
            pd.DataFrame(
                {s: report(get_ohlcv(s)["close"]) for s in a.symbols}
            ).to_string()
        )
