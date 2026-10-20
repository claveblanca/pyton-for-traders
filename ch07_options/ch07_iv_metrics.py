"""ch07_iv_metrics.py -- the volatility context behind an options trade.

Ref: §7.4.2 (straddles and condors are "a bet that volatility will exceed
what the market has priced in"), PROOF §7.9.1 (a broker/BS mismatch "usually
means a stale quote or a difference in the volatility input").

    implied_vol(price, S, K, dte, r, kind)  IV by root-finding Black-Scholes
    atm_iv(chain, spot)                     IV of the nearest-to-money strike
    iv_rank / iv_percentile(history)        where today's IV sits in 252 days
    realised_vol(close, 20)                 annualised close-to-close vol
    expected_move(straddle, spot)           market-implied move to expiry
    skew_25d(chain)                         25-delta put IV - 25-delta call IV

Chain columns: strike, type ('call'|'put'), mid, dte, (optional) iv.

Usage:
    python ch07_iv_metrics.py --selftest
    python ch07_iv_metrics.py AAPL          # yfinance option chain, nearest expiry > 14 days
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np
import pandas as pd
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch07_payoff_and_greeks import bs  # noqa: E402


def implied_vol(
    price: float, s: float, k: float, dte: float, r: float, kind: str
) -> float:
    f = lambda v: bs(s, k, dte, r, v, kind)["price"] - price  # noqa: E731
    try:
        return brentq(f, 1e-4, 5.0)
    except ValueError:
        return np.nan


def with_iv(chain: pd.DataFrame, spot: float, r: float = 0.045) -> pd.DataFrame:
    c = chain.copy()
    if "iv" not in c or c["iv"].isna().any():
        c["iv"] = [
            implied_vol(m, spot, k, d, r, t)
            for m, k, d, t in zip(c.mid, c.strike, c.dte, c.type)
        ]
    c["delta"] = [
        bs(spot, k, d, r, v, t)["delta"] if v == v else np.nan
        for k, d, v, t in zip(c.strike, c.dte, c.iv, c.type)
    ]
    return c


def atm_iv(chain: pd.DataFrame, spot: float) -> float:
    k = chain.loc[(chain.strike - spot).abs().idxmin(), "strike"]
    return float(chain[chain.strike == k]["iv"].mean())


def iv_rank(hist: pd.Series) -> float:
    h = hist.tail(252)
    return float((h.iloc[-1] - h.min()) / (h.max() - h.min()) * 100)


def iv_percentile(hist: pd.Series) -> float:
    h = hist.tail(252)
    return float((h < h.iloc[-1]).mean() * 100)


def realised_vol(close: pd.Series, window: int = 20) -> float:
    return float(np.log(close).diff().tail(window).std() * np.sqrt(252))


def expected_move(chain: pd.DataFrame, spot: float) -> dict:
    k = chain.loc[(chain.strike - spot).abs().idxmin(), "strike"]
    straddle = chain[chain.strike == k]["mid"].sum()
    return {"strike": k, "straddle": straddle, "move_pct": straddle / spot}


def skew_25d(chain: pd.DataFrame) -> float:
    p = chain[chain.type == "put"].iloc[
        (chain[chain.type == "put"]["delta"] + 0.25).abs().argsort()[:1]
    ]
    c = chain[chain.type == "call"].iloc[
        (chain[chain.type == "call"]["delta"] - 0.25).abs().argsort()[:1]
    ]
    return float(p["iv"].iloc[0] - c["iv"].iloc[0])


def selftest() -> None:
    spot, dte, r = 225.0, 30, 0.045
    strikes = np.arange(190, 261, 5)
    rows = []
    for k in strikes:
        smile = 0.25 + 0.0015 * (225 - k)  # put skew
        for t in ("call", "put"):
            rows.append(
                {
                    "strike": k,
                    "type": t,
                    "dte": dte,
                    "mid": bs(spot, k, dte, r, smile, t)["price"],
                }
            )
    ch = with_iv(pd.DataFrame(rows), spot, r)
    assert abs(atm_iv(ch, spot) - 0.25) < 1e-4  # IV recovered from price
    assert skew_25d(ch) > 0  # puts dearer
    em = expected_move(ch, spot)
    assert 0.05 < em["move_pct"] < 0.07
    hist = pd.Series(np.r_[np.linspace(0.18, 0.40, 200), np.full(52, 0.25)])
    assert 30 < iv_rank(hist) < 35
    rv = realised_vol(
        pd.Series(
            100 * np.exp(np.cumsum(np.random.default_rng(1).normal(0, 0.012, 60)))
        )
    )
    print(
        {
            "atm_iv": round(atm_iv(ch, spot), 4),
            "skew_25d": round(skew_25d(ch), 4),
            "expected_move_pct": round(em["move_pct"] * 100, 2),
            "iv_rank": round(iv_rank(hist), 1),
            "iv_percentile": round(iv_percentile(hist), 1),
            "rv20": round(rv, 3),
        }
    )
    print("selftest OK")


def live(ticker: str) -> dict:
    import yfinance as yf  # lazy

    tk = yf.Ticker(ticker)
    spot = float(tk.history(period="5d")["Close"].iloc[-1])
    exp = next(
        e for e in tk.options if (pd.Timestamp(e) - pd.Timestamp.now()).days > 14
    )
    oc = tk.option_chain(exp)
    dte = (pd.Timestamp(exp) - pd.Timestamp.now()).days
    ch = pd.concat([oc.calls.assign(type="call"), oc.puts.assign(type="put")])
    ch = ch.assign(mid=(ch.bid + ch.ask) / 2, dte=dte, iv=ch.impliedVolatility)[
        ["strike", "type", "mid", "dte", "iv"]
    ]
    ch = with_iv(ch[ch.mid > 0].reset_index(drop=True), spot)
    close = tk.history(period="3mo")["Close"]
    return {
        "expiry": exp,
        "spot": spot,
        "atm_iv": atm_iv(ch, spot),
        "rv20": realised_vol(close),
        "iv_minus_rv": atm_iv(ch, spot) - realised_vol(close),
        **expected_move(ch, spot),
        "skew_25d": skew_25d(ch),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("ticker", nargs="?")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    selftest() if a.selftest or not a.ticker else print(live(a.ticker))
