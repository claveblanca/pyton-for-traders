"""Command-line symbols and daily bars for the Hands-On scripts."""
import argparse
import sys

import pandas as pd

from common.ohlcv import get_ohlcv, synthetic_ohlcv

START = "2025-01-01"          # enough history for every 200-day indicator


def cli(default: list[str]) -> tuple[list[str], bool]:
    """Symbols typed after the script name (or `default`) and whether --demo was given."""
    symbols = [a for a in sys.argv[1:] if not a.startswith("--")] or default
    return symbols, "--demo" in sys.argv


def daily(symbol: str, demo: bool = False, start: str = START, kraken: bool = False,
          seed: int = 7) -> pd.DataFrame:
    """Daily OHLCV. Live: yfinance (or Kraken), today's still-forming bar dropped.
    Demo: the repository's offline sample bars."""
    if demo:
        return synthetic_ohlcv(seed=seed)
    return get_ohlcv(symbol, start=start, source="kraken" if kraken else "yfinance").iloc[:-1]


def closes(symbols: list[str], demo: bool = False, start: str = START) -> pd.DataFrame:
    """Closing prices of several symbols on the days they all traded (one column each)."""
    df = pd.DataFrame({s: daily(s, demo, start, seed=i)["close"] for i, s in enumerate(symbols)})
    df.index = df.index.normalize()
    return df.groupby(level=0).last().dropna()


def options(symbols: list[str] | None = None, **defaults):
    """Symbols plus --name value options, typed from their defaults, and --demo.
    options(["GC=F"], equity=10000.0)  ->  args.symbols, args.equity, args.demo"""
    p = argparse.ArgumentParser()
    p.add_argument("symbols", nargs="*", default=symbols or [])
    for name, value in defaults.items():
        p.add_argument("--" + name.replace("_", "-"), default=value,
                       type=float if isinstance(value, (int, float)) else str)
    p.add_argument("--demo", action="store_true")
    return p.parse_args()
