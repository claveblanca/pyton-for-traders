"""ch07_payoff_and_greeks.py -- metrics of a multi-leg option position at entry.

Ref: §7.4.1-7.4.2 (Table 7.2 defined risk), §7.5 (Delta, Theta, Gamma --
Vega added here), §7.6 (2% sizing on the worst-case loss),
PROOF §7.9 (scorecard: size, defined risk, permission).

A leg: {type: 'call'|'put', strike, qty (+long/-short), premium, iv, dte}.
    bs(...)                  Black-Scholes price + Delta/Gamma/Theta(per day)/Vega(per 1 vol pt)
    payoff_at_expiry(legs,S) P/L per share at expiry
    analyse(legs, spot, r)   max profit, max loss, break-evens, net Greeks,
                             probability of profit (lognormal), defined-risk flag
    contracts_2pct(equity, max_loss_per_contract)
    plot(legs, spot, path)   payoff diagram (matplotlib, optional)

Usage:
    python ch07_payoff_and_greeks.py --selftest
"""

from __future__ import annotations

import argparse
import math

import numpy as np
from scipy.stats import norm

MULT = 100


def bs(spot: float, strike: float, dte: float, r: float, iv: float, kind: str) -> dict:
    t = max(dte, 1e-6) / 365
    d1 = (math.log(spot / strike) + (r + iv**2 / 2) * t) / (iv * math.sqrt(t))
    d2 = d1 - iv * math.sqrt(t)
    if kind == "call":
        price = spot * norm.cdf(d1) - strike * math.exp(-r * t) * norm.cdf(d2)
        delta = norm.cdf(d1)
        theta = (
            -spot * norm.pdf(d1) * iv / (2 * math.sqrt(t))
            - r * strike * math.exp(-r * t) * norm.cdf(d2)
        ) / 365
    else:
        price = strike * math.exp(-r * t) * norm.cdf(-d2) - spot * norm.cdf(-d1)
        delta = norm.cdf(d1) - 1
        theta = (
            -spot * norm.pdf(d1) * iv / (2 * math.sqrt(t))
            + r * strike * math.exp(-r * t) * norm.cdf(-d2)
        ) / 365
    return {
        "price": price,
        "delta": delta,
        "gamma": norm.pdf(d1) / (spot * iv * math.sqrt(t)),
        "theta": theta,
        "vega": spot * norm.pdf(d1) * math.sqrt(t) / 100,
    }


def payoff_at_expiry(legs: list[dict], s: np.ndarray) -> np.ndarray:
    pl = np.zeros_like(s, dtype=float)
    for L in legs:
        intrinsic = (
            np.maximum(s - L["strike"], 0)
            if L["type"] == "call"
            else np.maximum(L["strike"] - s, 0)
        )
        pl += L["qty"] * (intrinsic - L["premium"])
    return pl


def analyse(legs: list[dict], spot: float, r: float = 0.045) -> dict:
    grid = np.unique(
        np.r_[np.linspace(0.01, spot * 4, 40_001), [L["strike"] for L in legs]]
    )
    pl = payoff_at_expiry(legs, grid)
    slope_up = pl[-1] - pl[-2]  # >0: unlimited upside, <0: unlimited loss
    max_loss = -pl.min() if slope_up >= -1e-12 else np.inf
    max_profit = pl.max() if slope_up <= 1e-12 else np.inf
    be = grid[np.where(np.diff(np.sign(pl)) != 0)[0]]
    g = {
        k: sum(
            L["qty"] * bs(spot, L["strike"], L["dte"], r, L["iv"], L["type"])[k]
            for L in legs
        )
        for k in ("delta", "gamma", "theta", "vega")
    }
    dte, iv = min(L["dte"] for L in legs), np.mean([L["iv"] for L in legs])
    t = dte / 365
    dist = norm(loc=math.log(spot) + (r - iv**2 / 2) * t, scale=iv * math.sqrt(t))
    p_profit = float(np.sum((pl > 0)[1:] * np.diff(dist.cdf(np.log(grid)))))
    return {
        "max_profit": max_profit * MULT,
        "max_loss": max_loss * MULT,
        "breakevens": [round(float(x), 2) for x in be],
        "defined_risk": bool(np.isfinite(max_loss)),
        "prob_profit": p_profit,
        **{f"net_{k}": v * MULT for k, v in g.items()},
        "theta_decay_zone": dte <= 21,
    }


def contracts_2pct(
    equity: float, max_loss_per_contract: float, risk: float = 0.02
) -> int:
    return (
        int(equity * risk // max_loss_per_contract)
        if np.isfinite(max_loss_per_contract)
        else 0
    )


def plot(legs: list[dict], spot: float, path: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    s = np.linspace(spot * 0.7, spot * 1.3, 400)
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(s, payoff_at_expiry(legs, s) * MULT, color="black")
    ax.axhline(0, color="grey", lw=0.8)
    ax.set_xlabel("Underlying at expiry")
    ax.set_ylabel("P/L per contract ($)")
    fig.tight_layout()
    fig.savefig(path, dpi=200)


def selftest() -> None:
    # PROOF §7.9: vertical spread, $350 max loss per contract, 18 DTE, $20,000 account
    spread = [
        {
            "type": "call",
            "strike": 225,
            "qty": 1,
            "premium": 5.00,
            "iv": 0.28,
            "dte": 18,
        },
        {
            "type": "call",
            "strike": 232,
            "qty": -1,
            "premium": 1.50,
            "iv": 0.28,
            "dte": 18,
        },
    ]
    a = analyse(spread, 225)
    assert (
        abs(a["max_loss"] - 350) < 1
        and abs(a["max_profit"] - 350) < 1
        and a["defined_risk"]
    )
    assert contracts_2pct(20_000, a["max_loss"]) == 1 and a["theta_decay_zone"]
    straddle = [
        {"type": "call", "strike": 230, "qty": 1, "premium": 6, "iv": 0.28, "dte": 30},
        {"type": "put", "strike": 230, "qty": 1, "premium": 6, "iv": 0.28, "dte": 30},
    ]
    s = analyse(straddle, 230)
    assert s["breakevens"] == [218.0, 242.0] or all(
        abs(x - y) < 0.05 for x, y in zip(s["breakevens"], [218, 242])
    )
    assert s["net_vega"] > 0 and s["net_theta"] < 0 and not np.isfinite(s["max_profit"])
    naked = analyse(
        [
            {
                "type": "call",
                "strike": 240,
                "qty": -1,
                "premium": 2,
                "iv": 0.28,
                "dte": 30,
            }
        ],
        230,
    )
    assert not naked["defined_risk"]  # Table 7.2: undefined
    g = bs(225, 230, 18, 0.045, 0.28, "call")
    print("BS call 225/230 18d:", {k: round(float(v), 4) for k, v in g.items()})
    print(
        "long straddle:",
        {
            k: (round(float(v), 3) if isinstance(v, (float, np.floating)) else v)
            for k, v in s.items()
        },
    )
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--selftest", action="store_true")
    p.parse_args()
    selftest()
