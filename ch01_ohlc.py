"""ch01_ohlc.py — Chapter 1 Hands-On: fetch daily OHLC(V) from yfinance.

Run from the repo root:
    python ch01_ohlc.py
    python ch01_ohlc.py MSFT
    python ch01_ohlc.py AAPL --start 2024-01-01 --tail 20
    python ch01_ohlc.py --demo
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import check_ohlcv, get_ohlcv, show, synthetic_ohlcv


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("symbol", nargs="?", default="AAPL")
    p.add_argument("--demo", action="store_true", help="offline sample bars (no network)")
    p.add_argument("--start", default="2025-01-01", help="first date (YYYY-MM-DD)")
    p.add_argument("--tail", type=int, default=15, help="recent rows to print")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.demo:
        df = synthetic_ohlcv()
    else:
        df = get_ohlcv(args.symbol, interval="1d", start=args.start, source="yfinance")
        if len(df):
            df = df.iloc[:-1]  # drop today's incomplete bar (same as common.daily)

    print(df.tail(args.tail).to_string())
    print(
        f"\n{args.symbol} · yfinance · 1d · "
        f"{len(df)} bars · {df.index[0].date()} … {df.index[-1].date()}"
    )
    show(check_ohlcv(df, expected_freq="D"))
