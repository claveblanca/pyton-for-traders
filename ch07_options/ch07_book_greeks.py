"""ch07_book_greeks.py -- net Delta, Vega and Theta of every option position held.

Ref: §7.8.2 (Rule 18: cap the whole book, not just each trade), §7.6.4-7.6.5
(Vega, implied volatility), §7.11 (free data: yfinance chains carry IV but no
Greeks), Appendix A §A.2 (portfolio ceilings).

Free inputs (yfinance, delayed): option_chain(expiry) -> impliedVolatility per
strike; history() -> spot; ^IRX -> 13-week T-bill as the risk-free rate.
Greeks come from bs() in ch07_payoff_and_greeks.py.

    book_greeks(positions, chain_fn, spot_fn, r)   one row per underlying
    book_limits(totals, equity)                     Rule 18 stress caps

Rule 18 stress caps (starting points to test, like every threshold in the book):
    a 3% move against the book      <= 2% of equity  (one trade's risk budget)
    a 10-point jump in volatility   <= 5% of equity  (Appendix A ceiling)

Usage:
    python ch07_book_greeks.py --selftest
    python ch07_book_greeks.py --live positions.json --equity 20000
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch07_payoff_and_greeks import bs  # noqa: E402


def yf_chain(sym: str, expiry: str) -> pd.DataFrame:
    import yfinance as yf

    ch = yf.Ticker(sym).option_chain(expiry)
    return pd.concat([ch.calls.assign(kind="call"), ch.puts.assign(kind="put")])


def yf_spot(sym: str) -> float:
    import yfinance as yf

    return float(yf.Ticker(sym).history(period="5d")["Close"].iloc[-1])


def yf_rate() -> float:
    import yfinance as yf

    return float(yf.Ticker("^IRX").history(period="5d")["Close"].iloc[-1]) / 100


def book_greeks(positions, chain_fn=yf_chain, spot_fn=yf_spot, r=None, today=None):
    """positions: [{sym, expiry, strike, kind 'call'|'put', qty (+long/-short)}]"""
    r = yf_rate() if r is None else r
    today = pd.Timestamp(today or pd.Timestamp.today().normalize())
    rows = []
    for p in positions:
        spot, ch = spot_fn(p["sym"]), chain_fn(p["sym"], p["expiry"])
        q = ch[(ch.kind == p["kind"]) & (ch.strike == p["strike"])].iloc[0]
        dte = (pd.Timestamp(p["expiry"]) - today).days
        g = bs(spot, p["strike"], dte, r, q["impliedVolatility"], p["kind"])
        k = p["qty"] * 100
        rows.append({"sym": p["sym"],
                     "delta_usd_1pct": g["delta"] * k * spot / 100,  # per 1% move
                     "vega_usd": g["vega"] * k,                      # per vol point
                     "theta_usd": g["theta"] * k})                   # per day
    return pd.DataFrame(rows).groupby("sym").sum()


def book_limits(totals: pd.DataFrame, equity: float) -> dict:
    d, v = totals["delta_usd_1pct"].sum(), totals["vega_usd"].sum()
    move3, vol10 = abs(d) * 3, abs(v) * 10
    return {
        "loss_3pct_move": round(move3, 2),
        "loss_10pt_vol": round(vol10, 2),
        "delta_ok": move3 <= 0.02 * equity,
        "vega_ok": vol10 <= 0.05 * equity,
    }


def selftest() -> None:
    spot = {"SPY": 600.0}
    iv = 0.21

    def chain(sym, expiry):
        ks = range(540, 665, 5)
        return pd.DataFrame(
            [{"strike": float(k), "kind": t, "impliedVolatility": iv}
             for k in ks for t in ("call", "put")]
        )

    condor = [  # PROOF §7.13 part A: short 555/645, long 550/650, 38 days
        dict(sym="SPY", expiry="2026-11-15", strike=550.0, kind="put", qty=1),
        dict(sym="SPY", expiry="2026-11-15", strike=555.0, kind="put", qty=-1),
        dict(sym="SPY", expiry="2026-11-15", strike=645.0, kind="call", qty=-1),
        dict(sym="SPY", expiry="2026-11-15", strike=650.0, kind="call", qty=1),
    ]
    t = book_greeks(condor, chain, spot.get, r=0.04, today="2026-10-08")
    row = t.loc["SPY"]
    assert row.vega_usd < 0 and row.theta_usd > 0  # short premium: short Vega, long Theta
    assert abs(row.delta_usd_1pct) < 5  # roughly delta-neutral at entry
    lim = book_limits(t, 20_000)
    assert lim["delta_ok"] and lim["vega_ok"]
    five = pd.concat([t] * 5)  # five such condors on one index = one bigger bet
    assert abs(five.vega_usd.sum()) == abs(row.vega_usd) * 5
    print(t.round(2).to_string())
    print(lim, book_limits(five, 20_000))
    print("selftest OK")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--live", help="JSON file with the positions list")
    ap.add_argument("--equity", type=float, default=20_000)
    a = ap.parse_args()
    if a.live:
        tot = book_greeks(json.load(open(a.live)))
        print(tot.round(2).to_string())
        print(book_limits(tot, a.equity))
    else:
        selftest()
