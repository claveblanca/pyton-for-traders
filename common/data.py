"""common/data.py -- shared data layer for code_snippets/v1.

Every chapter script imports from here instead of fetching data itself.

    get_ohlcv(symbol, interval="1d", start=None, source="yfinance")
        -> DataFrame[open, high, low, close, volume], UTC DatetimeIndex
    check_ohlcv(df)          -> dict of data-quality findings (Ch 8 §8.10)
    synthetic_ohlcv(n, ...)  -> deterministic fake OHLCV for --selftest
    get_fred(series_id)      -> pd.Series (needs FRED_API_KEY, fredapi)

Network libraries (yfinance, requests, fredapi) are imported lazily, so
every --selftest runs offline. Ported from code_snippets/ch01/
(ch01_yfinance.py, ch01_kraken_ohlcv.py, ch01_sanity_checks.py) and
ch02/ch02_cast_index.py.
"""

from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

OHLCV = ["open", "high", "low", "close", "volume"]
V1_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNIPPETS_ROOT = os.path.dirname(V1_ROOT)  # code_snippets/


# ----------------------------------------------------------------- fetchers
def _from_yfinance(symbol: str, interval: str, start: str | None) -> pd.DataFrame:
    import yfinance as yf  # lazy

    df = yf.download(
        symbol,
        interval=interval,
        start=start,
        period=None if start else "5y",
        auto_adjust=True,
        progress=False,
    )
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.rename(columns=str.lower)[OHLCV]
    df.index = pd.to_datetime(df.index, utc=True)
    return df.astype(float)


def _from_kraken(pair: str, interval: str, start: str | None) -> pd.DataFrame:
    import requests  # lazy

    minutes = {"1m": 1, "5m": 5, "15m": 15, "30m": 30, "1h": 60, "4h": 240, "1d": 1440}[
        interval
    ]
    params = {"pair": pair, "interval": minutes}
    if start:
        params["since"] = int(pd.Timestamp(start, tz="UTC").timestamp())
    r = requests.get("https://api.kraken.com/0/public/OHLC", params=params, timeout=30)
    r.raise_for_status()
    res = r.json()["result"]
    key = next(k for k in res if k != "last")
    df = pd.DataFrame(
        res[key], columns=["ts", "open", "high", "low", "close", "vwap", "volume", "n"]
    )
    df.index = pd.to_datetime(df["ts"].astype(int), unit="s", utc=True)
    return df[OHLCV].astype(float)


def get_ohlcv(
    symbol: str,
    interval: str = "1d",
    start: str | None = None,
    source: str = "yfinance",
) -> pd.DataFrame:
    """One call for every chapter. source: 'yfinance' | 'kraken' | 'csv:<path>'."""
    if symbol.upper() == "SYNTH":
        return synthetic_ohlcv()
    if source.startswith("csv:"):
        df = pd.read_csv(source[4:], index_col=0, parse_dates=True)
        df.index = pd.to_datetime(df.index, utc=True)
        return df.rename(columns=str.lower)[OHLCV].astype(float)
    if source == "kraken":
        return _from_kraken(symbol, interval, start)
    return _from_yfinance(symbol, interval, start)


def get_fred(series_id: str) -> pd.Series:
    """FRED series (free key: fred.stlouisfed.org) -- as in Ch 3 Listing 3.1."""
    from fredapi import Fred  # lazy

    return Fred(api_key=os.environ["FRED_API_KEY"]).get_series(series_id).dropna()


# ----------------------------------------------------------------- checks
def check_ohlcv(df: pd.DataFrame, expected_freq: str | None = None) -> dict:
    """Data-quality findings used by Ch 8 (§8.10) and before every indicator."""
    out = {"rows": len(df)}
    out["duplicate_ts"] = int(df.index.duplicated().sum())
    out["nan_cells"] = int(df[OHLCV].isna().sum().sum())
    bad_hl = (df["high"] < df[["open", "close", "low"]].max(axis=1)) | (
        df["low"] > df[["open", "close", "high"]].min(axis=1)
    )
    out["ohlc_violations"] = int(bad_hl.sum())
    out["zero_volume_share"] = float((df["volume"] <= 0).mean()) if len(df) else 0.0
    r = np.log(df["close"]).diff()
    z = (r - r.mean()) / r.std()
    out["outlier_returns"] = int((z.abs() > 6).sum())
    freq = expected_freq or (pd.infer_freq(df.index[:50]) if len(df) > 3 else None)
    if freq:
        step = pd.to_timedelta(pd.tseries.frequencies.to_offset(freq).nanos, unit="ns")
        gaps = df.index.to_series().diff() > step * 1.5
        out["missing_bar_gaps"] = int(gaps.sum())
    else:
        out["missing_bar_gaps"] = None
    return out


# ----------------------------------------------------------------- synthetic
def synthetic_ohlcv(
    n: int = 600,
    seed: int = 7,
    start: str = "2024-01-01",
    freq: str = "D",
    drift: float = 0.0004,
    vol: float = 0.018,
    regimes: bool = True,
) -> pd.DataFrame:
    """Deterministic OHLCV with alternating trend/range regimes for selftests."""
    rng = np.random.default_rng(seed)
    mu = np.full(n, drift)
    if regimes:
        block = n // 6
        for i in range(6):
            mu[i * block : (i + 1) * block] = [0.003, 0.0, -0.0025, 0.0, 0.002, 0.0][i]
    ret = mu + rng.normal(0, vol, n)
    close = 100 * np.exp(np.cumsum(ret))
    open_ = np.r_[close[0], close[:-1]] * (1 + rng.normal(0, vol / 4, n))
    hi = np.maximum(open_, close) * (1 + np.abs(rng.normal(0, vol / 2, n)))
    lo = np.minimum(open_, close) * (1 - np.abs(rng.normal(0, vol / 2, n)))
    volume = rng.lognormal(12, 0.4, n) * (1 + 3 * (np.abs(ret) > 2 * vol))
    idx = pd.date_range(start, periods=n, freq=freq, tz="UTC")
    return pd.DataFrame(
        {"open": open_, "high": hi, "low": lo, "close": close, "volume": volume},
        index=idx,
    )


def add_v1_to_path() -> None:
    """Call from a chapter script so `import common...` works from any cwd."""
    if V1_ROOT not in sys.path:
        sys.path.insert(0, V1_ROOT)
