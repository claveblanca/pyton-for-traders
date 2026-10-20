"""Wilder-style indicators for Hands-On scripts."""

from __future__ import annotations

import numpy as np
import pandas as pd


def sma(series: pd.Series, period: int) -> pd.Series:
    return series.rolling(period, min_periods=period).mean()


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False, min_periods=period).mean()


def _wilder_smooth(x: pd.Series, period: int) -> pd.Series:
    return x.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()


def true_range(df: pd.DataFrame) -> pd.Series:
    prev = df["close"].shift(1)
    tr = pd.concat(
        [
            df["high"] - df["low"],
            (df["high"] - prev).abs(),
            (df["low"] - prev).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return tr


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    return _wilder_smooth(true_range(df), period)


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = (-delta).clip(lower=0)
    avg_gain = _wilder_smooth(gain, period)
    avg_loss = _wilder_smooth(loss, period)
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - 100 / (1 + rs)


def macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    line = ema(close, fast) - ema(close, slow)
    sig = ema(line, signal)
    return pd.DataFrame({"macd_line": line, "macd_signal": sig, "macd_hist": line - sig})


def adx(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    up = df["high"].diff()
    down = -df["low"].diff()
    plus_dm = np.where((up > down) & (up > 0), up, 0.0)
    minus_dm = np.where((down > up) & (down > 0), down, 0.0)
    tr = true_range(df)
    atr_w = _wilder_smooth(tr, period)
    plus_di = 100 * _wilder_smooth(pd.Series(plus_dm, index=df.index), period) / atr_w
    minus_di = 100 * _wilder_smooth(pd.Series(minus_dm, index=df.index), period) / atr_w
    dx = (100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)).fillna(0)
    adx_line = _wilder_smooth(dx, period)
    return pd.DataFrame(
        {"adx": adx_line, "plus_di": plus_di, "minus_di": minus_di},
        index=df.index,
    )


def bollinger(close: pd.Series, period: int = 20, k: float = 2.0) -> pd.DataFrame:
    mid = sma(close, period)
    std = close.rolling(period, min_periods=period).std()
    upper = mid + k * std
    lower = mid - k * std
    width = (upper - lower) / mid.replace(0, np.nan)
    pct_b = (close - lower) / (upper - lower).replace(0, np.nan)
    return pd.DataFrame(
        {
            "bb_mid": mid,
            "bb_upper": upper,
            "bb_lower": lower,
            "bb_width": width,
            "bb_pct_b": pct_b,
        }
    )


def crosses(fast: pd.Series, slow: pd.Series) -> pd.Series:
    """+1 golden cross, -1 death cross, 0 otherwise."""
    diff = fast - slow
    prev = diff.shift(1)
    out = pd.Series(0, index=fast.index, dtype=int)
    out[(prev <= 0) & (diff > 0)] = 1
    out[(prev >= 0) & (diff < 0)] = -1
    return out


def obv(df: pd.DataFrame) -> pd.Series:
    direction = np.sign(df["close"].diff().fillna(0))
    return (direction * df["volume"]).cumsum()
