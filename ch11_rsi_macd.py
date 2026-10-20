"""ch11_rsi_macd.py — Chapter 11 Hands-On: is the market stretched, and is momentum turning?

RSI(14) with Wilder smoothing (70 overbought, 30 oversold) and MACD (12, 26, 9):
the histogram's sign gives the momentum side, a change of direction is the earliest turn.

Run from the repo root:
    python ch11_rsi_macd.py BTC-USD
    python ch11_rsi_macd.py SPY
    python ch11_rsi_macd.py --demo
"""
import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from common import cli, daily, rsi, macd, show


def oscillators(df) -> dict:
    r = rsi(df.close).iloc[-1]
    h = macd(df.close)["macd_hist"].tail(3)
    return {
        "date": str(df.index[-1].date()),
        "rsi14": round(r, 1),
        "rsi_zone": "overbought" if r >= 70 else "oversold" if r <= 30 else "neutral",
        "macd_hist": round(h.iloc[-1], 2),
        "momentum": "bullish" if h.iloc[-1] > 0 else "bearish",
        "histogram": ("turning up" if h.iloc[-1] > h.iloc[-2] < h.iloc[-3] else
                      "turning down" if h.iloc[-1] < h.iloc[-2] > h.iloc[-3] else "no turn"),
    }


if __name__ == "__main__":
    (sym, *_), demo = cli(["BTC-USD"])
    show(oscillators(daily(sym, demo)))
