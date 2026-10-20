"""ch10_ma_bands.py — Chapter 10 Hands-On: trend from moving averages, quiet from the bands.

EMA 12 vs EMA 26 gives the trend and the date of the last cross; Bollinger Bands
(20, 2) give %B (where the close sits inside the bands) and the squeeze: bandwidth
in the lowest 10% of the last 120 days means a big move is likely, direction unknown.

Run from the repo root:
    python ch10_ma_bands.py BTC-USD
    python ch10_ma_bands.py SPY
    python ch10_ma_bands.py --demo
"""
import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from common import cli, daily, ema, bollinger, crosses, show


def ma_bands(df) -> dict:
    c = df.close
    fast, slow = ema(c, 12), ema(c, 26)
    x = crosses(fast, slow)
    last_x = x[x != 0]
    bb = bollinger(c).dropna()
    width_rank = (bb.bb_width.tail(120) < bb.bb_width.iloc[-1]).mean()
    return {
        "date": str(df.index[-1].date()), "close": round(c.iloc[-1], 2),
        "trend": "up (EMA12 > EMA26)" if fast.iloc[-1] > slow.iloc[-1] else "down (EMA12 < EMA26)",
        "last_cross": (f"{'golden' if last_x.iloc[-1] > 0 else 'death'} on {last_x.index[-1].date()}"
                       if len(last_x) else "none"),
        "pct_b": round(bb.bb_pct_b.iloc[-1], 2),            # >1 above upper band, <0 below lower
        "squeeze": bool(width_rank <= 0.10),
    }


if __name__ == "__main__":
    (sym, *_), demo = cli(["BTC-USD"])
    show(ma_bands(daily(sym, demo)))
