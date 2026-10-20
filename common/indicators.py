"""common/indicators.py -- indicator maths shared by Ch 8-12 and Appendix A.

All functions take pandas Series/DataFrames and return Series/DataFrames
aligned to the input index. Wilder smoothing = EMA with alpha = 1/period,
adjust=False (Ch 11 §11.4 WARNING, Ch 12 §12.4.1).
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def wilder(s: pd.Series, period: int) -> pd.Series:
    return s.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()


def ema(s: pd.Series, span: int) -> pd.Series:
    return s.ewm(span=span, adjust=False).mean()


def sma(s: pd.Series, window: int) -> pd.Series:
    return s.rolling(window).mean()


def true_range(df: pd.DataFrame) -> pd.Series:
    pc = df["close"].shift(1)
    return pd.concat(
        [df["high"] - df["low"], (df["high"] - pc).abs(), (df["low"] - pc).abs()],
        axis=1,
    ).max(axis=1)


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    return wilder(true_range(df), period)


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    d = close.diff()
    g, l = wilder(d.clip(lower=0), period), wilder(-d.clip(upper=0), period)
    return 100 - 100 / (1 + g / l)


def macd(close: pd.Series, fast=12, slow=26, signal=9) -> pd.DataFrame:
    line = ema(close, fast) - ema(close, slow)
    sig = ema(line, signal)
    return pd.DataFrame({"macd": line, "signal": sig, "hist": line - sig})


def adx(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """+DI, -DI, DX, ADX exactly as Ch 12 Listing 12.1."""
    up = df["high"].diff()
    dn = -df["low"].diff()
    pdm = up.where((up > dn) & (up > 0), 0.0)
    mdm = dn.where((dn > up) & (dn > 0), 0.0)
    a = wilder(true_range(df), period)
    pdi = 100 * wilder(pdm, period) / a
    mdi = 100 * wilder(mdm, period) / a
    dx = 100 * (pdi - mdi).abs() / (pdi + mdi).replace(0, np.nan)
    return pd.DataFrame(
        {"plus_di": pdi, "minus_di": mdi, "dx": dx, "adx": wilder(dx, period)}
    )


def bollinger(close: pd.Series, window=20, k=2.0) -> pd.DataFrame:
    mid = close.rolling(window).mean()
    sd = close.rolling(window).std(ddof=0)
    up, lo = mid + k * sd, mid - k * sd
    return pd.DataFrame(
        {
            "bb_mid": mid,
            "bb_upper": up,
            "bb_lower": lo,
            "bb_pct_b": (close - lo) / (up - lo),
            "bb_width": (up - lo) / mid,
        }
    )


def stochastic(df: pd.DataFrame, k=14, d=3) -> pd.DataFrame:
    hh, ll = df["high"].rolling(k).max(), df["low"].rolling(k).min()
    pk = 100 * (df["close"] - ll) / (hh - ll)
    return pd.DataFrame(
        {
            "stoch_k": pk,
            "stoch_d": pk.rolling(d).mean(),
            "williams_r": -100 * (hh - df["close"]) / (hh - ll),
        }
    )


def cci(df: pd.DataFrame, window=20) -> pd.Series:
    tp = (df["high"] + df["low"] + df["close"]) / 3
    ma = tp.rolling(window).mean()
    md = tp.rolling(window).apply(lambda x: np.mean(np.abs(x - x.mean())), raw=True)
    return (tp - ma) / (0.015 * md)


def obv(df: pd.DataFrame) -> pd.Series:
    return (np.sign(df["close"].diff().fillna(0)) * df["volume"]).cumsum()


def crosses(fast: pd.Series, slow: pd.Series) -> pd.Series:
    """+1 on a cross above, -1 on a cross below, 0 otherwise."""
    above = fast > slow
    prev = above.shift(1, fill_value=False)
    return (above & ~prev).astype(int) - (
        ~above & prev & fast.notna() & slow.notna()
    ).astype(int)
