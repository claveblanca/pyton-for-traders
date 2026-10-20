"""appx_a_portfolio_limits.py -- the Appendix A ceilings as a live pre-trade check.

Ref: §A.2 (Table A.1), §A.2.2 (2% working rule, 5% ceiling, Ch 5's 3-5%
open-risk cap vs the 10-15% margin cap), §A.3.1 (3:1 floor),
PROOF §A.13 checks 1-4.  Inspired by code_snippets/ch14/risk_engine.py
(check_exposure, compute_rrr) without its database layer.

Positions: list of dicts {symbol, market, sector, margin, entry, stop, target,
size, point_value}. Risk per position = |entry - stop| x size x point_value.

Usage:
    python appx_a_portfolio_limits.py --selftest
    python appx_a_portfolio_limits.py positions.csv --equity 25000 --new new_trade.json
"""

from __future__ import annotations

import argparse
import json

import pandas as pd

LIMITS = {
    "total_committed": 0.50,
    "market_margin": 0.15,
    "market_open_risk": 0.05,
    "trade_risk_working": 0.02,
    "trade_risk_ceiling": 0.05,
    "sector": 0.25,
    "rr_min": 3.0,
}


def enrich(pos: pd.DataFrame) -> pd.DataFrame:
    p = pos.copy()
    p["point_value"] = p.get("point_value", 1.0)
    p["risk"] = (p["entry"] - p["stop"]).abs() * p["size"] * p["point_value"]
    p["reward"] = (p["target"] - p["entry"]).abs() * p["size"] * p["point_value"]
    p["rr"] = p["reward"] / p["risk"]
    return p


def check(positions: pd.DataFrame, new: dict, equity: float) -> pd.DataFrame:
    """Eight-line verdict for adding `new` to `positions` (first four A.12 checks)."""
    p = enrich(pd.concat([positions, pd.DataFrame([new])], ignore_index=True))
    n = p.iloc[-1]
    mkt, sec = p[p.market == n.market], p[p.sector == n.sector]
    rows = [
        (
            "total committed / equity",
            p["margin"].sum() / equity,
            LIMITS["total_committed"],
        ),
        (
            "margin in this market / equity",
            mkt["margin"].sum() / equity,
            LIMITS["market_margin"],
        ),
        (
            "open risk in this market / equity",
            mkt["risk"].sum() / equity,
            LIMITS["market_open_risk"],
        ),
        ("sector exposure / equity", sec["margin"].sum() / equity, LIMITS["sector"]),
        (
            "trade risk / equity (working 2%)",
            n.risk / equity,
            LIMITS["trade_risk_working"],
        ),
        (
            "trade risk / equity (ceiling 5%)",
            n.risk / equity,
            LIMITS["trade_risk_ceiling"],
        ),
    ]
    out = pd.DataFrame(rows, columns=["check", "value", "limit"])
    out["pass"] = out["value"] <= out["limit"]
    rr = pd.DataFrame(
        [
            (
                "reward / risk (floor 3:1)",
                n.rr,
                LIMITS["rr_min"],
                n.rr >= LIMITS["rr_min"],
            )
        ],
        columns=out.columns,
    )
    out = pd.concat([out, rr], ignore_index=True)
    max_size = int(
        LIMITS["trade_risk_working"]
        * equity
        // ((abs(n.entry - n.stop)) * n.point_value)
    )
    verdict = (
        "NOT ALLOWED (> 5%)"
        if not out.loc[5, "pass"]
        else (
            "EXCEPTION: justify in writing (2-5%)"
            if not out.loc[4, "pass"]
            else "OK" if out["pass"].all() else "RESIZE / SKIP"
        )
    )
    out.attrs.update(verdict=verdict, max_size_at_2pct=max_size)
    return out


def selftest() -> None:
    eq = 25_000
    pos = pd.DataFrame(
        [
            dict(
                symbol="MGCZ6",
                market="gold",
                sector="metals",
                margin=1650,
                entry=3000,
                stop=2980,
                target=3060,
                size=1,
                point_value=10,
            ),
            dict(
                symbol="SIZ6",
                market="silver",
                sector="metals",
                margin=2000,
                entry=40,
                stop=39,
                target=43,
                size=1,
                point_value=500,
            ),
        ]
    )
    ok = check(
        pos,
        dict(
            symbol="MCLZ6",
            market="crude",
            sector="energy",
            margin=1000,
            entry=70,
            stop=68,
            target=76,
            size=2,
            point_value=100,
        ),
        eq,
    )
    assert ok.attrs["verdict"] == "OK", ok
    big = check(
        pos,
        dict(
            symbol="MGCZ6b",
            market="gold",
            sector="metals",
            margin=1650,
            entry=3000,
            stop=2900,
            target=3300,
            size=1,
            point_value=10,
        ),
        eq,
    )
    assert (
        big.attrs["verdict"].startswith("EXCEPTION")
        and big.attrs["max_size_at_2pct"] == 0
    )
    print(big.round(3).to_string(index=False))
    print(big.attrs)
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("positions", nargs="?")
    p.add_argument("--equity", type=float)
    p.add_argument("--new", help="JSON file with the proposed trade")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.positions:
        selftest()
    else:
        r = check(pd.read_csv(a.positions), json.load(open(a.new)), a.equity)
        print(r.round(4).to_string(index=False))
        print(r.attrs)
