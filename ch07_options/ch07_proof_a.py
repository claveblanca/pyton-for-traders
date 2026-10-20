"""ch07_proof_a.py -- PROOF §7.13 part A: one trade taken through seven gates.

Ref: PROOF §7.13 part A; Table 7.4 (§7.7.5); §7.6.6 (IV rank); §7.7.1
(expected move); §7.8 (2% sizing); §7.4 (permission); §7.9 (exit plan).

The book prints an ILLUSTRATIVE snapshot (inputs below, labelled as such in
the text). Re-run with today's inputs before using any of it:
    python ch07_proof_a.py --spot 600 --adx 17 --iv 0.21 --ivr 62 --dte 38

Usage:
    python ch07_proof_a.py --selftest
"""

from __future__ import annotations

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch07_payoff_and_greeks import analyse, bs  # noqa: E402
from ch07_screen import pick_structure, screen_option_trade  # noqa: E402


def condor_legs(spot, iv, dte, r, wing=5.0, step=5.0):
    move = spot * iv * math.sqrt(dte / 365)  # 1-sd expected move to expiry
    kp = math.floor((spot - move) / step) * step  # short put at or below -1 sd
    kc = math.ceil((spot + move) / step) * step  # short call at or above +1 sd
    spec = [("put", kp - wing, +1), ("put", kp, -1), ("call", kc, -1), ("call", kc + wing, +1)]
    legs = [dict(type=t, strike=k, qty=q, iv=iv, dte=dte,
                 premium=bs(spot, k, dte, r, iv, t)["price"]) for t, k, q in spec]
    return move, legs


def run(equity=20_000, level=3, spot=600.0, adx=17.0, iv=0.21, ivr=62.0, dte=38,
        r=0.04, event=False):
    fit = pick_structure(adx, ivr)
    move, legs = condor_legs(spot, iv, dte, r)
    a = analyse(legs, spot, r)
    credit = -sum(L["qty"] * L["premium"] for L in legs) * 100
    exit_plan = {"profit_target": 0.5, "time_stop": 21, "loss_stop": 2.0}
    sc = screen_option_trade("iron_condor", level, equity, a["max_loss"], dte,
                             iv_rank=ivr, adx=adx, event_before_expiry=event,
                             exit_plan=exit_plan)
    n = sc["rule13_max_contracts_allowed"]
    return {
        "gate1_regime": "range" if adx < 20 else "trend" if adx > 25 else "between",
        "gate2_iv_rank": ivr, "gate2_expected_move": round(move, 2),
        "gate2_expected_move_pct": round(move / spot * 100, 2),
        "gate3_structure": fit,
        "strikes": [L["strike"] for L in legs],
        "gate4_credit": round(credit, 2), "gate4_max_loss": round(a["max_loss"], 2),
        "gate4_breakevens": a["breakevens"], "gate4_prob_profit": round(a["prob_profit"], 3),
        "gate4_net_delta": round(a["net_delta"], 2), "gate4_net_vega": round(a["net_vega"], 2),
        "gate4_net_theta": round(a["net_theta"], 2),
        "gate5_contracts": n, "gate5_risk_used": round(n * a["max_loss"], 2),
        "gate6_level_ok": sc["rule4_8_level_ok"],
        "gate7_close_at_profit": round(credit * 0.5, 2),
        "gate7_close_at_loss": round(credit * 2.0, 2),
        "gate7_time_stop_days_held": dte - 21,
        "tradeable": sc["tradeable"],
    }


def selftest() -> None:
    r = run()
    assert r["gate3_structure"] == "iron_condor" and r["strikes"] == [550, 555, 645, 650]
    assert r["gate5_contracts"] == 1 and r["gate4_max_loss"] <= 400 and r["tradeable"]
    assert run(level=2)["gate6_level_ok"] is False
    for k, v in r.items():
        print(f"{k:28} {v}")
    print("selftest OK")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    for k, d in dict(equity=20_000, level=3, spot=600.0, adx=17.0, iv=0.21, ivr=62.0,
                     dte=38).items():
        ap.add_argument(f"--{k}", type=type(d), default=d)
    a = ap.parse_args()
    if a.selftest:
        selftest()
    else:
        for k, v in run(a.equity, a.level, a.spot, a.adx, a.iv, a.ivr, a.dte).items():
            print(f"{k:28} {v}")
