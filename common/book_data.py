"""
book_data.py — saved market data used by the book's figures (offline, reproducible).

Files in common/data/:
  BTCUSD_kraken_daily_2026-03-01_2026-10-19.csv   Kraken public OHLC, XBTUSD, interval 1440 (UTC days;
      last row = 19 Oct, still open when fetched — drop it for any 'close' statistic)
  BTCUSD_coinbase_1h_2026-09-18_2026-09-25.csv    Coinbase Exchange candles, BTC-USD, 3600 s (UTC hours)
      (hourly: Kraken's public OHLC endpoint only serves the latest 720 bars, so mid-September
       hourly history came from Coinbase; daily highs/lows agree with Kraken within ~0.1 %)
"""
import os
import pandas as pd

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
BTC_DAILY = os.path.join(DATA, "BTCUSD_kraken_daily_2026-03-01_2026-10-19.csv")
BTC_HOURLY = os.path.join(DATA, "BTCUSD_coinbase_1h_2026-09-18_2026-09-25.csv")


def btc_daily() -> pd.DataFrame:
    d = pd.read_csv(BTC_DAILY)
    d.index = pd.to_datetime(d["time"], unit="s")
    return d[["open", "high", "low", "close", "volume"]].sort_index()


def btc_hourly() -> pd.DataFrame:
    d = pd.read_csv(BTC_HOURLY)
    d.index = pd.to_datetime(d["time"], unit="s")
    return d[["open", "high", "low", "close", "volume"]].sort_index()


def check(df: pd.DataFrame, freq: str) -> None:
    """No gaps, no duplicates, high >= max(open, close), low <= min(open, close)."""
    assert df.index.is_unique and df.index.is_monotonic_increasing
    full = pd.date_range(df.index[0], df.index[-1], freq=freq)
    assert len(full) == len(df), f"gaps: {len(full) - len(df)}"
    assert (df.high >= df[["open", "close"]].max(axis=1) - 1e-9).all()
    assert (df.low <= df[["open", "close"]].min(axis=1) + 1e-9).all()


if __name__ == "__main__":
    for name, f, fq in (("daily", btc_daily, "D"), ("hourly", btc_hourly, "h")):
        df = f(); check(df, fq); print(name, len(df), df.index[0], "→", df.index[-1], "OK")
