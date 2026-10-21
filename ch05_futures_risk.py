"""ch05_futures_risk.py — Chapter 5 Hands-On: how many contracts the 2% rule allows today.

Fetches the front-month future, sets the stop at 2 x ATR(14) from the last close,
and sizes the position so that a stop-out costs at most 2% of the account.

Run from the repo root:
    python ch05_futures_risk.py                         # Micro Gold, 10 000 account
    python ch05_futures_risk.py CL=F --point-value 100  # Micro Crude (100 barrels)
    python ch05_futures_risk.py --demo
Point value = money per 1.00 move of the price for ONE contract (Micro Gold: 10).
"""
import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from common import options, daily, atr, show


def size(df, equity, point_value, risk=0.02, k_atr=2.0, margin=None) -> dict:
    close, a = df["close"].iloc[-1], atr(df).iloc[-1]
    risk_per_contract = k_atr * a * point_value
    n = int(risk * equity // risk_per_contract)
    notional = n * close * point_value
    out = {"close": round(close, 2), "atr14": round(a, 2),
           "stop": round(close - k_atr * a, 2),
           "risk_per_contract": round(risk_per_contract, 2), "max_contracts": n,
           "notional": round(notional), "leverage": round(notional / equity, 2)}
    if margin:
        out["margin_used_pct"] = round(100 * n * margin / equity, 1)
    return out


if __name__ == "__main__":
    a = options(["GC=F"], equity=10000.0, point_value=10.0, margin=0.0)   # margin: broker page
    show(size(daily(a.symbols[0], a.demo), a.equity, a.point_value, margin=a.margin),
         "max_contracts = 0: even one contract risks more than 2% - use a smaller contract.")
