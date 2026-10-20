"""common/stats.py -- validation helpers shared by the PROOF scripts.

forward_returns, sharpe, max_drawdown, mann_whitney_edge, hit_rate.
Non-overlapping sampling is the default wherever a horizon > 1 is used,
so annualised figures are not inflated (audit note on Ch 12 Listing 12.6).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def forward_returns(close: pd.Series, h: int) -> pd.Series:
    return close.shift(-h) / close - 1


def non_overlapping(s: pd.Series, h: int) -> pd.Series:
    return s.iloc[::h]


def sharpe(r: pd.Series, periods_per_year: float = 252) -> float:
    r = r.dropna()
    return (
        float(r.mean() / r.std() * np.sqrt(periods_per_year)) if r.std() > 0 else np.nan
    )


def cagr(equity: pd.Series, periods_per_year: float = 252) -> float:
    e = equity.dropna()
    yrs = len(e) / periods_per_year
    return float((e.iloc[-1] / e.iloc[0]) ** (1 / yrs) - 1) if yrs > 0 else np.nan


def max_drawdown(equity: pd.Series) -> float:
    return float((equity / equity.cummax() - 1).min())


def mann_whitney_edge(a: pd.Series, b: pd.Series) -> dict:
    a, b = a.dropna(), b.dropna()
    if len(a) < 5 or len(b) < 5:
        return {"n_a": len(a), "n_b": len(b), "p_value": np.nan, "edge": np.nan}
    u, p = stats.mannwhitneyu(a, b, alternative="two-sided")
    return {
        "n_a": len(a),
        "n_b": len(b),
        "mean_a": a.mean(),
        "mean_b": b.mean(),
        "edge": a.mean() - b.mean(),
        "p_value": float(p),
    }


def hit_rate(signal: pd.Series, fwd: pd.Series) -> dict:
    m = (signal != 0) & fwd.notna()
    n = int(m.sum())
    hits = (np.sign(signal[m]) == np.sign(fwd[m])).mean() if n else np.nan
    return {"n": n, "hit_rate": float(hits), "preliminary": n < 30}
