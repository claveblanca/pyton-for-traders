"""Google Trends via pytrends (unofficial; rate-limit requests)."""
from __future__ import annotations

import time
from typing import Literal

import pandas as pd

Category = Literal["economy", "trading", "crypto", "geopolitics", "commodities"]

CATEGORY_KEYWORDS: dict[Category, list[str]] = {
    "economy": ["inflation", "recession", "interest rates"],
    "trading": ["stock market", "S&P 500"],
    "crypto": ["bitcoin", "cryptocurrency"],
    "geopolitics": ["war", "sanctions", "election"],
    "commodities": ["oil price", "gold price", "natural gas"],
}

_MIN_INTERVAL_S = 5.0
_last_request_at = 0.0
_MAX_RETRIES = 4
_RETRY_BACKOFF_S = 15.0


def _throttle() -> None:
    global _last_request_at
    elapsed = time.monotonic() - _last_request_at
    if elapsed < _MIN_INTERVAL_S:
        time.sleep(_MIN_INTERVAL_S - elapsed)
    _last_request_at = time.monotonic()


def _with_retries(fn):
    from pytrends import exceptions as pex

    last: Exception | None = None
    for attempt in range(_MAX_RETRIES):
        try:
            _throttle()
            return fn()
        except pex.TooManyRequestsError as e:
            last = e
            time.sleep(_RETRY_BACKOFF_S * (attempt + 1))
    if last:
        raise last
    raise RuntimeError("retry loop failed")


def _trend_req(hl: str = "en-US", tz: int = 0):
    from pytrends.request import TrendReq

    return TrendReq(hl=hl, tz=tz)


def interest_over_time(
    keywords: list[str],
    *,
    timeframe: str = "today 3-m",
    geo: str = "",
    hl: str = "en-US",
) -> pd.DataFrame:
    """Relative search interest 0–100 per keyword (Google Trends index)."""
    if not keywords:
        return pd.DataFrame()
    pytrends = _trend_req(hl=hl)

    def _fetch():
        pytrends.build_payload(keywords[:5], timeframe=timeframe, geo=geo)
        return pytrends.interest_over_time()

    df = _with_retries(_fetch)
    if df is None or df.empty:
        return pd.DataFrame()
    if "isPartial" in df.columns:
        df = df.drop(columns=["isPartial"])
    return df


def interest_by_category(
    category: Category,
    *,
    timeframe: str = "today 3-m",
    geo: str = "",
) -> pd.DataFrame:
    return interest_over_time(CATEGORY_KEYWORDS[category], timeframe=timeframe, geo=geo)


def trending_searches(*, geo: str = "united_states") -> pd.DataFrame:
    """Daily trending searches for a country (`united_states`, `italy`, …)."""
    pytrends = _trend_req()
    return _with_retries(lambda: pytrends.trending_searches(pn=geo))


def related_queries(keyword: str, *, timeframe: str = "today 3-m", geo: str = "") -> dict:
    pytrends = _trend_req()

    def _fetch():
        pytrends.build_payload([keyword], timeframe=timeframe, geo=geo)
        return pytrends.related_queries()

    return _with_retries(_fetch)


def latest_vs_recent_mean(series: pd.Series, window: int = 7) -> dict[str, float | None]:
    """Compare last observation to recent mean (simple spike hint)."""
    s = series.dropna()
    if len(s) < 2:
        return {"latest": float(s.iloc[-1]) if len(s) else None, "mean": None, "ratio": None}
    tail = s.iloc[-window:] if len(s) >= window else s
    latest = float(s.iloc[-1])
    mean = float(tail.mean())
    ratio = latest / mean if mean else None
    return {"latest": latest, "mean": mean, "ratio": ratio}


def demo_interest(keywords: list[str]) -> pd.DataFrame:
    """Offline sample interest series."""
    idx = pd.date_range("2025-01-01", periods=12, freq="W")
    data = {kw: [40 + i * 2 + (hash(kw) % 10) for i in range(12)] for kw in keywords[:5]}
    return pd.DataFrame(data, index=idx)
