"""Annual fundamentals + quote info via ch02_stocks/ch02_data (yfinance / SEC EDGAR).

Chapter scripts import from here instead of manipulating sys.path to ch03_stocks.

Requires for full 5–7 year history:
    export SEC_USER_AGENT="Your Name your@email.com"
"""

from __future__ import annotations

import importlib
import os
import sys
from functools import lru_cache
from typing import Any

import pandas as pd

from common.data import V1_ROOT

_CH02_STOCKS = os.path.join(V1_ROOT, "ch02_stocks")


@lru_cache(maxsize=1)
def _ch02_data():
    mod_path = os.path.join(_CH02_STOCKS, "ch02_data.py")
    if not os.path.isfile(mod_path):
        raise FileNotFoundError(f"Missing data layer: {mod_path}")
    if _CH02_STOCKS not in sys.path:
        sys.path.insert(0, _CH02_STOCKS)
    return importlib.import_module("ch02_data")


def annual(ticker: str, fields: list[str], source: str = "auto") -> pd.DataFrame:
    return _ch02_data().annual(ticker, fields, source=source)


def info(ticker: str) -> dict[str, Any]:
    return _ch02_data().info(ticker)


def price_and_shares(ticker: str) -> tuple[float, float]:
    inf = info(ticker)
    price = float(inf["price"])
    shares = float(inf["marketCap"]) / price
    return price, shares
