"""ch12_adx_gate.py — Chapter 12 Hands-On: which tools may trade today?

ADX(14) with +DI and -DI on the last closed bar. ADX > 25: a trend, use the moving
averages of Chapter 10 in the direction of the stronger DI. ADX < 20: no trend,
use the oscillators of Chapter 11. In between: a transition, stand aside or reduce size.

Run from the repo root:
    python ch12_adx_gate.py BTC-USD
    python ch12_adx_gate.py XLE XLK GLD          # several markets, strongest trend first
    python ch12_adx_gate.py --demo
"""
import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from common import pd, cli, daily, adx


def gate(df) -> dict:
    d = adx(df).iloc[-1]
    a, side = d.adx, "long" if d.plus_di > d.minus_di else "short"
    return {"date": str(df.index[-1].date()), "adx": round(a, 1),
            "plus_di": round(d.plus_di, 1), "minus_di": round(d.minus_di, 1),
            "regime": "trend" if a > 25 else "range" if a < 20 else "transition",
            "use": (f"trend tools (Ch 10), {side} side" if a > 25 else
                    "oscillators (Ch 11)" if a < 20 else "stand aside / reduce size")}


if __name__ == "__main__":
    symbols, demo = cli(["BTC-USD"])
    rows = {s: gate(daily(s, demo, seed=i)) for i, s in enumerate(symbols)}
    print(pd.DataFrame(rows).T.sort_values("adx", ascending=False).to_string())
