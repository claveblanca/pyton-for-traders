"""ch05_margin_monitor.py -- effective leverage and distance to a margin call.

Ref: §5.3.2 (notional and leverage), §5.3.5 (effective leverage = notional /
whole account, Figure 5.6), §5.5.1 (Listing 5.1, the 2% rule),
PROOF §5.9.2 (Table 5.8). Builds on code_snippets/futures_trading/
ch06_margin_proof.py and ch06_risk.py.

Per position or proposed trade:
    notional, effective leverage, margin leverage, points and % to the
    maintenance-margin call, contracts allowed by the 2% rule vs by margin,
    and whether the stop sits inside the margin-call distance.

Usage:
    python ch05_margin_monitor.py --selftest
    python ch05_margin_monitor.py --equity 10000 --price 3000 --point-value 10 \
        --initial 1650 --maint 1500 --stop-points 20 --contracts 1
"""

from __future__ import annotations

import argparse


def max_contracts_2pct(
    equity: float, stop_points: float, point_value: float, risk_pct: float = 0.02
) -> int:
    return int(equity * risk_pct // (stop_points * point_value))


def max_contracts_margin(equity: float, initial: float) -> int:
    return int(equity // initial)


def monitor(
    equity: float,
    price: float,
    point_value: float,
    initial: float,
    maint: float,
    contracts: int,
    stop_points: float | None = None,
) -> dict:
    notional = price * point_value * contracts
    pts_to_call = (equity - contracts * maint) / (contracts * point_value)
    out = {
        "notional": notional,
        "effective_leverage": notional / equity,
        "margin_leverage": price * point_value / initial,
        "points_to_margin_call": pts_to_call,
        "pct_to_margin_call": pts_to_call / price,
        "contracts_2pct_rule": (
            max_contracts_2pct(equity, stop_points, point_value)
            if stop_points
            else None
        ),
        "contracts_margin_max": max_contracts_margin(equity, initial),
    }
    if stop_points:
        out["stop_inside_call_distance"] = stop_points < pts_to_call
        out["loss_at_stop_pct"] = stop_points * point_value * contracts / equity
    return out


def selftest() -> None:
    eq, px, pv, ini, mnt = 10_000, 3000, 10, 1650, 1500
    assert (
        max_contracts_2pct(eq, 4, pv) == 5 and max_contracts_margin(eq, ini) == 6
    )  # §5.9
    m6 = monitor(eq, px, pv, ini, mnt, 6, 20)  # Table 5.8 row 2
    assert (
        round(m6["effective_leverage"], 1) == 18.0
        and round(m6["points_to_margin_call"], 1) == 16.7
    )
    assert not m6["stop_inside_call_distance"]
    m5 = monitor(eq, px, pv, ini, mnt, 5, 4)  # row 3
    assert m5["points_to_margin_call"] == 50 and m5["stop_inside_call_distance"]
    m1 = monitor(eq, px, pv, ini, mnt, 1, 20)  # row 4
    assert (
        m1["points_to_margin_call"] == 850
        and abs(m1["loss_at_stop_pct"] - 0.02) < 1e-12
    )
    assert (
        round(monitor(30_000, px, pv, ini, mnt, 1)["effective_leverage"], 1) == 1.0
    )  # Figure 5.6
    for n, r in [(6, m6), (5, m5), (1, m1)]:
        print(
            n, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()}
        )
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    for k in ("equity", "price", "point-value", "initial", "maint", "stop-points"):
        p.add_argument(f"--{k}", type=float)
    p.add_argument("--contracts", type=int, default=1)
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or a.equity is None:
        selftest()
    else:
        print(
            monitor(
                a.equity,
                a.price,
                a.point_value,
                a.initial,
                a.maint,
                a.contracts,
                a.stop_points,
            )
        )
