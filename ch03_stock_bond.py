"""ch03_stock_bond.py — Chapter 3 Hands-On: do bonds still hedge stocks?

90-day correlation of daily returns between a stock ETF and a long Treasury ETF,
read with the chapter's regimes: < 0 hedge | 0 to 0.2 neutral | > 0.2 move together.

Run from the repo root:
    python ch03_stock_bond.py                 # SPY vs TLT
    python ch03_stock_bond.py VGK IBGL.L      # any stock / bond pair
    python ch03_stock_bond.py --demo
"""
import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from common import pd, cli, closes


def regime(c: float) -> str:
    return "hedge" if c < 0 else "neutral" if c <= 0.2 else "together"


def stock_bond(px: pd.DataFrame) -> pd.DataFrame:
    r = px.pct_change().dropna()
    s, b = r.iloc[:, 0], r.iloc[:, 1]
    out = pd.DataFrame({f"corr_{w}d": s.rolling(w).corr(b) for w in (30, 90)})
    out["regime"] = out["corr_90d"].map(regime)
    return out.dropna()


if __name__ == "__main__":
    pair, demo = cli(["SPY", "TLT"])
    t = stock_bond(closes(pair[:2], demo))
    print(t.tail(5).round(2).to_string())
    days = int((t["regime"][::-1] == t["regime"].iloc[-1]).cumprod().sum())
    print(f"\nRegime now: {t['regime'].iloc[-1]} (for {days} trading days)")
