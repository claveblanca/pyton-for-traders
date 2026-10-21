"""ch07_options_iv.py — Chapter 7 Hands-On: is volatility expensive today?

From the option chain (first expiry at least 14 days away): the at-the-money straddle,
the move it prices in, and implied volatility (IV) against the volatility the stock
actually showed over the last 20 days (HV20). IV well above HV: options are rich,
favour selling defined-risk structures; IV below HV: favour buying.

Run from the repo root:
    python ch07_options_iv.py SPY
    python ch07_options_iv.py --demo
Data: free yfinance chain, delayed about 15 minutes.
"""
import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from common import pd, cli, daily, show


def atm_reading(calls, puts, spot: float, days: int, hv20: float) -> dict:
    k = calls.loc[(calls.strike - spot).abs().idxmin(), "strike"]
    c, p = calls[calls.strike == k].iloc[0], puts[puts.strike == k].iloc[0]
    straddle = (c.bid + c.ask) / 2 + (p.bid + p.ask) / 2
    iv = (c.impliedVolatility + p.impliedVolatility) / 2
    return {"strike": k, "days": days, "straddle": round(straddle, 2),
            "expected_move_pct": round(100 * straddle / spot, 1),
            "iv_atm": round(iv, 3), "hv20": round(hv20, 3),
            "iv_minus_hv": round(iv - hv20, 3),
            "reading": "rich: sell defined risk" if iv > 1.2 * hv20 else
                       "cheap: buy" if iv < hv20 else "fair"}


def chain(symbol: str, demo: bool):
    if demo:
        calls = pd.DataFrame({"strike": [95, 100, 105], "bid": [6.1, 3.0, 1.0], "ask": [6.3, 3.2, 1.1],
                              "impliedVolatility": [0.24, 0.22, 0.21]})
        return calls, calls.assign(bid=[1.0, 2.9, 6.0], ask=[1.1, 3.1, 6.2]), 30
    import yfinance as yf
    t = yf.Ticker(symbol)
    expiry = next(e for e in t.options if (pd.Timestamp(e) - pd.Timestamp.today()).days >= 14)
    ch = t.option_chain(expiry)
    return ch.calls, ch.puts, (pd.Timestamp(expiry) - pd.Timestamp.today()).days


if __name__ == "__main__":
    (sym, *_), demo = cli(["SPY"])
    close = daily(sym, demo)["close"]
    if demo:
        close = close / close.iloc[-1] * 100                # demo spot = 100
    hv20 = close.pct_change().tail(20).std() * 252 ** 0.5
    calls, puts, days = chain(sym, demo)
    show(atm_reading(calls, puts, close.iloc[-1], days, hv20))
