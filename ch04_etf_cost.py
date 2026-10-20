"""ch04_etf_cost.py — Chapter 4 Hands-On: the Index of Cost (ICS) of an ETF from a live quote.

ICS = TER + 2 x spread (one year, % of the amount). Hurdle = the gain a trade must
target to be worth its round trip (5 x the round-trip spread).
One quote is a snapshot: sample several, at different hours, before you decide.

Run from the repo root:
    python ch04_etf_cost.py CSPX.L --ter 0.07
    python ch04_etf_cost.py AMEW.DE --ter 0.38 --amount 20000 --years 5
    python ch04_etf_cost.py --demo
"""
import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from common import options, show


def ics(ter_pct: float, spread_pct: float) -> float:
    """Synthetic cost index: TER + 2× one-way spread (% per year)."""
    return ter_pct + 2 * spread_pct


def cost_eur(amount: float, ter_pct: float, spread_pct: float, years: float) -> float:
    return amount * (ics(ter_pct, spread_pct) / 100) * years


def hurdle(spread_pct: float) -> float:
    """Minimum gain target: 5× round-trip spread (%)."""
    return 5 * (2 * spread_pct)


def spread_pct(ticker: str) -> float:
    import yfinance as yf
    q = yf.Ticker(ticker).info
    bid, ask = q.get("bid"), q.get("ask")
    if not bid or not ask:
        raise SystemExit(f"{ticker}: no bid/ask now (market closed?) - try during trading hours")
    return (ask - bid) / ((ask + bid) / 2) * 100           # % of the mid price


if __name__ == "__main__":
    a = options(["DEMO"], ter=0.38, amount=20000.0, years=5.0)     # ter = yearly fee, %
    s = 0.06 if a.demo else spread_pct(a.symbols[0])
    show({"spread_pct": round(s, 3), "ics_pct_1y": round(ics(a.ter, s), 2),
          f"cost_eur_{a.years:g}y": round(cost_eur(a.amount, a.ter, s, a.years)),
          "trade_hurdle_pct": round(hurdle(s), 1)})
