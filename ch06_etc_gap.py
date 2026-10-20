"""ch06_etc_gap.py — Chapter 6 Hands-On: what an ETC really cost you over a year.

Compares a euro-listed commodity ETC with the front-month future it tracks, both in
US dollars. The yearly gap is the price of holding the commodity through a product:
roll yield (contango or backwardation) plus fees.

Run from the repo root:
    python ch06_etc_gap.py                                        # Brent: BRNT.MI vs BZ=F
    python ch06_etc_gap.py --etc CRUD.L --future CL=F --fx none   # USD-listed ETC
    python ch06_etc_gap.py --demo
"""
import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from common import pd, options, closes, show


def yearly_gap(px: pd.DataFrame) -> dict:
    d = px.tail(252)
    etc_usd = d["etc"] * d["fx"]                            # EUR price x USD per EUR
    r_etc, r_fut = etc_usd.iloc[-1] / etc_usd.iloc[0] - 1, d["fut"].iloc[-1] / d["fut"].iloc[0] - 1
    return {"from": str(d.index[0].date()), "to": str(d.index[-1].date()),
            "etc_return_usd": round(r_etc, 3), "future_return": round(r_fut, 3),
            "gap_per_year": round(r_etc - r_fut, 3)}


if __name__ == "__main__":
    a = options(etc="BRNT.MI", future="BZ=F", fx="EURUSD=X")       # fx none: ETC quoted in USD
    if a.demo:
        fut = closes(["fut"], demo=True)["fut"]
        drag = pd.Series(0.9996 ** pd.RangeIndex(len(fut)).to_numpy(), fut.index)   # ~10%/yr
        px = pd.DataFrame({"etc": fut * drag / 1.1, "fut": fut, "fx": 1.1})
    else:
        px = closes([a.etc, a.future] + ([] if a.fx == "none" else [a.fx]), start="2024-06-01")
        px.columns = ["etc", "fut", "fx"][:px.shape[1]]
        if "fx" not in px:
            px["fx"] = 1.0
    show(yearly_gap(px), "gap < 0: the product lagged the future (contango + fees); "
                         "gap > 0: backwardation helped.")
