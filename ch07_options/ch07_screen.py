"""ch07_screen.py -- the Chapter 7 rules as one pre-trade scorecard.

Ref: §7.4 (Table 7.1 broker levels, Rules 4-8), §7.5 (Rule 9 defined risk),
§7.6 (Rules 10-12 Greeks, Rule 15 IV rank), §7.7.5 (Rule 16, Table 7.4 strategy
picker), §7.7.4 (Rule 17 events), §7.8 (Rule 13 2% sizing), §7.9 (Rule 19 exit
plan), PROOF §7.13 part A (gates 3, 5, 6, 7).
Ported from code_snippets/options_trading/options_rules_screener.py (Tradier
version); this one has no broker dependency.

    broker_level_required(strategy)      Table 7.1 -> {"min_level", "is_defined_risk"}
    position_size_by_risk(eq, max_loss)  Rule 13: contracts within 2% of equity
    pick_structure(adx, iv_rank, trend)  Rule 16: Table 7.4
    screen_option_trade(...)             one pass/fail dict per proposed trade

Usage:
    python ch07_screen.py --selftest
"""

from __future__ import annotations

import argparse
import math

LEVELS = {  # Table 7.1: strategy -> (minimum broker level, defined risk?)
    "covered_call": (1, True),
    "cash_secured_put": (1, True),
    "long_call": (2, True),
    "long_put": (2, True),
    "collar": (2, True),
    "vertical_spread": (3, True),
    "credit_spread": (3, True),
    "debit_spread": (3, True),
    "long_straddle": (3, True),
    "iron_condor": (3, True),
    "calendar_spread": (3, True),
    "naked_call": (4, False),
    "naked_put": (4, False),
}
THETA_ZONE_DAYS = 21


def broker_level_required(strategy: str) -> dict:
    lvl, defined = LEVELS[strategy]
    return {"min_level": lvl, "is_defined_risk": defined}


def position_size_by_risk(
    equity: float, max_loss_per_contract: float, risk: float = 0.02
) -> int:
    if not math.isfinite(max_loss_per_contract) or max_loss_per_contract <= 0:
        return 0
    return int(equity * risk // max_loss_per_contract)


def pick_structure(adx: float, iv_rank: float, trend: str = "up") -> str:
    """Table 7.4: trend strength (Ch 12 ADX) x price of volatility (IV rank)."""
    if 20 <= adx <= 25 or 30 < iv_rank < 50:
        return "no_edge"  # between the bands: smaller size, or wait
    trending, rich = adx > 25, iv_rank >= 50
    if trending and rich:
        return "credit_spread"  # sold with the trend (bull put spread if up)
    if trending:
        return "debit_spread"  # bought with the trend
    return "iron_condor" if rich else "stand_aside"


def screen_option_trade(
    strategy: str,
    account_level: int,
    account_equity: float,
    max_loss_per_contract: float,
    days_to_expiration: int,
    iv_rank: float | None = None,
    adx: float | None = None,
    event_before_expiry: bool | None = None,
    exit_plan: dict | None = None,
) -> dict:
    need = broker_level_required(strategy)
    out = {
        "strategy": strategy,
        "rule4_8_level_ok": account_level >= need["min_level"],
        "rule4_8_min_level_required": need["min_level"],
        "rule9_defined_risk": need["is_defined_risk"],
        "rule11_in_theta_decay_zone": days_to_expiration <= THETA_ZONE_DAYS,
        "rule13_max_contracts_allowed": position_size_by_risk(
            account_equity, max_loss_per_contract
        ),
        "rule13_max_dollar_risk": round(account_equity * 0.02, 2),
    }
    if iv_rank is not None and adx is not None:
        fit = pick_structure(adx, iv_rank)
        out["rule16_suggested"] = fit
        out["rule16_structure_fits"] = fit == strategy or (
            fit == "credit_spread" and strategy == "vertical_spread"
        )
    if event_before_expiry is not None:
        out["rule17_event_clear"] = not event_before_expiry
    if exit_plan is not None:
        out["rule19_exit_set"] = all(
            k in exit_plan for k in ("profit_target", "time_stop", "loss_stop")
        )
    gates = [k for k, v in out.items() if k.endswith(("_ok", "_fits", "_clear", "_set"))]
    out["tradeable"] = (
        all(out[k] for k in gates)
        and out["rule9_defined_risk"]
        and out["rule13_max_contracts_allowed"] >= 1
    )
    return out


def selftest() -> None:
    # PROOF §7.13 part A gate 6 (the original §7.9 case): Level 2 blocks a spread
    s = screen_option_trade("vertical_spread", 2, 20_000, 350, 18)
    assert s["rule4_8_level_ok"] is False and s["rule4_8_min_level_required"] == 3
    assert s["rule13_max_contracts_allowed"] == 1 and s["rule11_in_theta_decay_zone"]
    assert s["tradeable"] is False
    # Table 7.4
    assert pick_structure(17, 62) == "iron_condor"
    assert pick_structure(31, 70) == "credit_spread"
    assert pick_structure(31, 20) == "debit_spread"
    assert pick_structure(15, 10) == "stand_aside"
    assert pick_structure(22, 70) == "no_edge" and pick_structure(30, 40) == "no_edge"
    ok = screen_option_trade(
        "iron_condor", 3, 20_000, 390, 38, iv_rank=62, adx=17,
        event_before_expiry=False,
        exit_plan={"profit_target": 0.5, "time_stop": 21, "loss_stop": 2.0},
    )
    assert ok["tradeable"], ok
    assert position_size_by_risk(20_000, float("inf")) == 0  # Rule 9: naked
    print({k: v for k, v in ok.items()})
    print("selftest OK")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    selftest()
