"""ch09_obv_volume.py — Chapter 9 Hands-On: does volume confirm the price?

On-Balance Volume (OBV) and its 20-day divergence from price, plus the last day's
volume against its 20-day average. A big-volume down day (>= 1.5 x average) is the
first sign of a possible selling climax.

Run from the repo root:
    python ch09_obv_volume.py BTC-USD
    python ch09_obv_volume.py SPY
    python ch09_obv_volume.py --demo
"""
import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from common import cli, daily, obv, show


def volume_reading(df, n=20) -> dict:
    o = obv(df)
    px, ov = df.close.tail(n), o.tail(n)
    rel_vol = df.volume.iloc[-1] / df.volume.iloc[-n - 1:-1].mean()
    down_day = df.close.iloc[-1] < df.close.iloc[-2]
    return {
        "date": str(df.index[-1].date()),
        "obv_trend_20d": "up" if ov.iloc[-1] > ov.iloc[0] else "down",
        "bearish_divergence": bool(px.iloc[-1] >= px.max() and ov.iloc[-1] < ov.max()),
        "bullish_divergence": bool(px.iloc[-1] <= px.min() and ov.iloc[-1] > ov.min()),
        "volume_vs_20d": round(rel_vol, 2),
        "possible_selling_climax": bool(rel_vol >= 1.5 and down_day),
    }


if __name__ == "__main__":
    (sym, *_), demo = cli(["BTC-USD"])
    show(volume_reading(daily(sym, demo)))
