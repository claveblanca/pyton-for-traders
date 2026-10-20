"""ch07_ib_chain.py -- an option chain with Greeks through Interactive Brokers.

Ref: §7.11 (data by the risk it reduces: IB returns model Greeks with each
quote), Listing 5.5 / Ch 5 §5.8.5 (same ib_async connection, delayed data),
PROOF §7.13 part A (gate 2: ATM implied volatility).

Requires TWS or IB Gateway running (paper port 7497) and `pip install ib_async`.
Delayed data (reqMarketDataType(3)) is free; ticks may arrive empty outside
US market hours.

Usage:
    python ch07_ib_chain.py --selftest
    python ch07_ib_chain.py SPY
"""

from __future__ import annotations

import argparse
import datetime as dt


def pick_expiry(expiries, today, lo=30, hi=45):
    """First listed expiry 30-45 days out (the §7.9 opening window)."""
    for e in sorted(expiries):
        d = (dt.datetime.strptime(e, "%Y%m%d").date() - today).days
        if lo <= d <= hi:
            return e
    return None


def pick_strikes(strikes, spot, n=4):
    return sorted(sorted(strikes, key=lambda k: abs(k - spot))[: 2 * n])


def chain_with_greeks(sym: str, port: int = 7497):
    from ib_async import IB, Option, Stock

    ib = IB()
    ib.connect("127.0.0.1", port, clientId=7)
    ib.reqMarketDataType(3)  # delayed, free
    stk = Stock(sym, "SMART", "USD")
    ib.qualifyContracts(stk)
    [t] = ib.reqTickers(stk)
    spot = t.marketPrice()
    p = ib.reqSecDefOptParams(stk.symbol, "", stk.secType, stk.conId)[0]
    exp = pick_expiry(p.expirations, dt.date.today())
    opts = [Option(sym, exp, k, r, "SMART") for k in pick_strikes(p.strikes, spot)
            for r in ("C", "P")]
    opts = ib.qualifyContracts(*opts)
    rows = []
    for tk in ib.reqTickers(*opts):
        g = tk.modelGreeks
        if g:
            rows.append((tk.contract.right, tk.contract.strike, tk.bid, tk.ask,
                         g.impliedVol, g.delta, g.gamma, g.vega, g.theta))
    ib.disconnect()
    return spot, exp, rows


def selftest() -> None:
    today = dt.date(2026, 10, 8)
    ex = ["20261016", "20261113", "20261120", "20261218"]
    assert pick_expiry(ex, today) == "20261113"  # 36 days
    assert pick_strikes([590, 595, 600, 605, 610, 615], 601, n=2) == [595, 600, 605, 610]
    print("selftest OK (offline; live mode needs TWS/IB Gateway)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("symbol", nargs="?")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.symbol and not a.selftest:
        spot, exp, rows = chain_with_greeks(a.symbol)
        print(f"{a.symbol} {spot:.2f} expiry {exp}")
        for r in rows:
            print(r)
    else:
        selftest()
