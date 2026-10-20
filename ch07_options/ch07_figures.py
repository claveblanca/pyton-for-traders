"""ch07_figures.py -- Figures 7.1-7.3 of Chapter 7 (black and white).

Ref: §7.3.1 (Figure 7.1 time cost: roll yield vs Theta), §7.5 (Figure 7.2
payoffs at expiry), §7.7.5 (Figure 7.3 strategy picker, Table 7.4).
Inputs: Ch 5 §5.2.3 cocoa roll (-2.13% per roll); the illustrative snapshot of
PROOF §7.13 part A (spot 600, IV 21%, 38 days, r 4%).

Usage:
    python ch07_figures.py OUT_DIR
"""

from __future__ import annotations

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ch07_payoff_and_greeks import bs, payoff_at_expiry  # noqa: E402
from ch07_proof_a import condor_legs  # noqa: E402

plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans", "axes.linewidth": 0.6})
SPOT, IV, DTE, R = 600.0, 0.21, 38, 0.04


def fig_time_cost(path):
    fig, (a, b) = plt.subplots(1, 2, figsize=(7, 2.6))
    rolls = np.arange(5)
    a.plot(rolls * 3, 100 * (1 - 0.0213) ** rolls, "o-", color="black", lw=1.2, ms=4)
    a.set_xticks([0, 3, 6, 9, 12])
    a.set_xlabel("Months held (one roll every 3 months)")
    a.set_ylabel("Value of 100, price unchanged")
    a.set_title("Futures: roll yield in contango\n(cocoa, -2.13% per roll, Ch 5)", fontsize=8)
    a.set_ylim(90, 101)
    days = np.arange(45, 0, -1)
    v = [bs(SPOT, SPOT, d, R, IV, "call")["price"] for d in days]
    held = 45 - days
    b.plot(held, v, color="black", lw=1.2)
    b.axvspan(45 - 21, 45, color="0.85", lw=0)
    b.text(45 - 10.5, max(v) * 0.92, "last 21 days", ha="center", fontsize=7)
    b.set_xlabel("Days held (45-day option)")
    b.set_ylabel("Option value, price unchanged ($)")
    b.set_title("Options: Theta\n(at-the-money call, IV 21%)", fontsize=8)
    b.set_ylim(0, max(v) * 1.05)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def _leg(t, k, q, dte=DTE):
    return dict(type=t, strike=k, qty=q, iv=IV, dte=dte, premium=bs(SPOT, k, dte, R, IV, t)["price"])


def fig_payoffs(path):
    s = np.linspace(SPOT * 0.82, SPOT * 1.18, 600)
    _, condor = condor_legs(SPOT, IV, DTE, R)
    panels = [
        ("Long call (600)", [_leg("call", 600, 1)], None),
        ("Bull call spread (600/620)", [_leg("call", 600, 1), _leg("call", 620, -1)], None),
        ("Iron condor (550/555 - 645/650)", condor, None),
        ("Collar: stock + put 570 - call 630", [_leg("put", 570, 1), _leg("call", 630, -1)], 1),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(7, 4.2), sharex=True)
    for ax, (title, legs, stock) in zip(axes.flat, panels):
        pl = payoff_at_expiry(legs, s) * 100
        if stock:
            pl += (s - SPOT) * 100
        ax.plot(s, pl, color="black", lw=1.2)
        ax.axhline(0, color="0.5", lw=0.6)
        ax.axvline(SPOT, color="0.5", lw=0.6, ls=":")
        ax.set_title(title, fontsize=8)
        ax.set_ylabel("P/L per contract ($)")
    for ax in axes[1]:
        ax.set_xlabel("Underlying at expiry ($); dotted line = 600 today")
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def fig_picker(path):
    fig, ax = plt.subplots(figsize=(7, 3.0))
    ax.set_xlim(0, 3)
    ax.set_ylim(-0.3, 2.6)
    ax.axis("off")
    cells = {
        (1, 1): "CREDIT VERTICAL\nwith the trend\n(sell premium)",
        (2, 1): "DEBIT VERTICAL or\nlong call/put\nwith the trend",
        (1, 0): "IRON CONDOR\naround the range",
        (2, 0): "STAND ASIDE\n(or a calendar spread\nbefore a known event)",
    }
    for (cx, cy), txt in cells.items():
        shade = "0.88" if cx == 1 else "1.0"
        ax.add_patch(plt.Rectangle((cx - 0.02, cy + 0.02), 0.96, 0.96, fc=shade, ec="black", lw=0.8))
        ax.text(cx + 0.46, cy + 0.5, txt, ha="center", va="center", fontsize=8)
    ax.text(1.46, 2.25, "IV rank >= 50\noptions expensive", ha="center", fontsize=8, weight="bold")
    ax.text(2.46, 2.25, "IV rank <= 30\noptions cheap", ha="center", fontsize=8, weight="bold")
    ax.text(0.5, 1.5, "TREND\nADX > 25", ha="center", va="center", fontsize=8, weight="bold")
    ax.text(0.5, 0.5, "RANGE\nADX < 20", ha="center", va="center", fontsize=8, weight="bold")
    ax.text(1.96, -0.2, "ADX 20-25 or IV rank 30-50: no edge from the grid - smaller size, or wait",
            ha="center", fontsize=7, style="italic")
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    fig_time_cost(os.path.join(out, "Ch7_Options_1_time_cost.png"))
    fig_payoffs(os.path.join(out, "Ch7_Options_2_payoffs.png"))
    fig_picker(os.path.join(out, "Ch7_Options_3_strategy_picker.png"))
    print("saved 3 figures to", out)
