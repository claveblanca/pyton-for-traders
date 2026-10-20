"""
pft_bw.py — Black & White print style for *The Data-Driven Trader* figures.

Rule: in B&W print, colour = nothing. Series must differ by at least TWO of:
    (1) gray level  (≥ 25 % luminance apart)
    (2) line style  (solid / dashed / dotted / dash-dot)
    (3) marker or line width
and every series is labelled directly at its line end (no colour-only legend).

Usage
-----
    import pft_bw as bw
    bw.apply()                                  # once, before plotting
    for i, (name, y) in enumerate(series.items()):
        ax.plot(x, y, **bw.series(i))
        bw.end_label(ax, x, y, name, i)
    bw.candles(ax, df)                          # hollow-up / filled-down
    bw.save(fig, "Ch12_ADX_bw.png")             # 300 dpi + gray-distinctness check
"""
from __future__ import annotations
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# ── Gray ramp (print-safe: avoid < 8 % and > 92 % except paper/ink) ─────────
INK      = "#1A1A1A"   # primary series, text
G_DARK   = "#4D4D4D"   # secondary series
G_MID    = "#808080"   # tertiary series, reference lines
G_LIGHT  = "#B3B3B3"   # quaternary, area fills (with hatch)
G_PALE   = "#E0E0E0"   # gridlines, shaded regimes
G_PANEL  = "#F2F2F2"   # panel / badge background
PAPER    = "#FFFFFF"

# ── Series ladder: index → (gray, linestyle, width, marker) ─────────────────
# Ordered so neighbours always differ on ≥ 2 channels.
_LADDER = [
    dict(color=INK,     ls="-",            lw=1.6, marker=None),  # 0 main
    dict(color=G_DARK,  ls=(0, (5, 2)),    lw=1.2, marker=None),  # 1 dashed
    dict(color=G_MID,   ls=(0, (1, 1.5)),  lw=1.4, marker=None),  # 2 dotted
    dict(color=INK,     ls=(0, (6, 2, 1, 2)), lw=0.9, marker=None),  # 3 dash-dot
    dict(color=G_DARK,  ls="-",            lw=0.9, marker="o"),   # 4 markers
    dict(color=G_MID,   ls="-",            lw=0.9, marker="s"),   # 5 markers
]
HATCHES = ["", "////", "....", "xxxx", "\\\\\\\\", "++"]  # area / bar fills
BAR_FILLS = [INK, G_LIGHT, PAPER, G_MID]                   # with black edge

# Semantic roles used across the book (replace red/green everywhere)
ROLE = {
    "up":      dict(face=PAPER, edge=INK),            # hollow candle / gain
    "down":    dict(face=INK,   edge=INK),            # filled candle / loss
    "buy":     dict(marker="^", color=INK, ms=7),
    "sell":    dict(marker="v", color=INK, ms=7, mfc=PAPER),
    "threshold": dict(color=G_MID, ls=(0, (3, 3)), lw=0.7),
    "price_now": dict(color=G_DARK, ls=(0, (1, 2)), lw=0.7),
}


def apply(font_size: float = 8.0) -> None:
    """Set rcParams for B&W print (Arial-compatible sans, light grid)."""
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"],
        "font.size": font_size,
        "axes.titlesize": font_size + 1.5, "axes.titleweight": "bold",
        "axes.labelsize": font_size, "axes.labelcolor": INK,
        "axes.edgecolor": G_MID, "axes.linewidth": 0.6,
        "axes.facecolor": PAPER, "figure.facecolor": PAPER,
        "axes.grid": True, "grid.color": G_PALE, "grid.linewidth": 0.5,
        "axes.spines.top": False, "axes.spines.right": False,
        "xtick.color": G_DARK, "ytick.color": G_DARK,
        "xtick.labelsize": font_size - 0.5, "ytick.labelsize": font_size - 0.5,
        "legend.frameon": False, "legend.fontsize": font_size - 0.5,
        "axes.prop_cycle": mpl.cycler(color=[d["color"] for d in _LADDER[:4]],
                                      linestyle=[d["ls"] for d in _LADDER[:4]]),
        "hatch.color": INK, "hatch.linewidth": 0.5,
        "savefig.dpi": 360, "savefig.bbox": "tight", "savefig.facecolor": PAPER,
    })


def series(i: int) -> dict:
    """plot() kwargs for the i-th series."""
    d = _LADDER[i % len(_LADDER)]
    kw = dict(color=d["color"], linestyle=d["ls"], linewidth=d["lw"])
    if d["marker"]:
        kw.update(marker=d["marker"], markersize=3, markevery=0.08,
                  markerfacecolor=PAPER, markeredgecolor=d["color"])
    return kw


def bar_style(i: int) -> dict:
    """bar()/fill_between() kwargs for the i-th category: fill + hatch + black edge."""
    return dict(facecolor=BAR_FILLS[i % len(BAR_FILLS)], hatch=HATCHES[i % len(HATCHES)],
                edgecolor=INK, linewidth=0.6)


def end_label(ax, x, y, text: str, i: int = 0, value_fmt: str = "{:.2f}") -> None:
    """Direct label at the right end of a line: 'NAME 12.34' in a boxed tag.
    Replaces colour-coded legends and TradingView price tags."""
    xv, yv = x[-1], float(np.asarray(y)[-1])
    d = _LADDER[i % len(_LADDER)]
    dark = d["color"] in (INK, G_DARK)
    ax.annotate(f"{text} {value_fmt.format(yv)}", (xv, yv), xytext=(4, 0),
                textcoords="offset points", va="center", fontsize=7, fontweight="bold",
                color=PAPER if dark else INK,
                bbox=dict(boxstyle="square,pad=0.25", fc=d["color"] if dark else PAPER,
                          ec=d["color"], lw=0.8))


def candles(ax, o, h, l, c, x=None, width=0.6, tone: str = "ink") -> None:
    """Hollow (up) / filled (down) candlesticks — readable without colour.
    tone="ink"  : black candles (price is the main subject)
    tone="light": mid-gray candles, so overlay lines (EMAs, bands) stay on top visually."""
    o, h, l, c = map(np.asarray, (o, h, l, c))
    x = np.arange(len(c)) if x is None else np.asarray(x)
    edge = INK if tone == "ink" else G_MID
    fill_dn = INK if tone == "ink" else G_LIGHT
    for xi, oi, hi, li, ci in zip(x, o, h, l, c):
        up = ci >= oi
        ax.vlines(xi, li, hi, color=edge, lw=0.6, zorder=2)
        ax.add_patch(plt.Rectangle((xi - width / 2, min(oi, ci)), width,
                                   max(abs(ci - oi), 1e-9), facecolor=PAPER if up else fill_dn,
                                   edgecolor=edge, lw=0.6, zorder=3))
    ax.autoscale_view()


def header(fig, text: str, y: float = 0.90) -> None:
    """Dashboard header strip (replaces coloured dashboard headers)."""
    fig.text(0.125, y, text, fontsize=7.5, fontweight="bold", color=INK,
             bbox=dict(boxstyle="square,pad=0.4", fc=G_PANEL, ec=G_MID, lw=0.6))


def date_axis(ax, x_dates, fmt: str = "%d %b", weekly: bool = True, hourly: bool = False) -> None:
    import matplotlib.dates as mdates
    if hourly:
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    elif weekly:
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
        ax.xaxis.set_major_formatter(mdates.DateFormatter(fmt))
    else:
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))


def regime_band(ax, x0, x1, label: str | None = None, dense: bool = False) -> None:
    """Shaded regime (e.g. ADX > 25, positive correlation): pale fill, optional hatch."""
    ax.axvspan(x0, x1, facecolor="#EDEDED" if not dense else G_PALE,
               hatch="////" if dense else None, edgecolor=G_MID, lw=0, zorder=0)
    if label:
        ax.text((x0 + x1) / 2, 0.97, label, transform=ax.get_xaxis_transform(),
                ha="center", va="top", fontsize=6.5, color=G_DARK)


def gray_check(fig, min_delta: float = 0.20) -> list[str]:
    """Warn when two line series in the same axes are within `min_delta` luminance
    AND share the same linestyle — i.e. would merge in B&W print."""
    from matplotlib.colors import to_rgb
    issues = []
    for ax in fig.axes:
        lines = [ln for ln in ax.get_lines() if ln.get_label() and not ln.get_label().startswith("_")
                 or len(ln.get_xdata()) > 2]
        for a in range(len(lines)):
            for b in range(a + 1, len(lines)):
                la = np.dot(to_rgb(lines[a].get_color()), [.299, .587, .114])
                lb = np.dot(to_rgb(lines[b].get_color()), [.299, .587, .114])
                same_ls = str(lines[a].get_linestyle()) == str(lines[b].get_linestyle())
                if abs(la - lb) < min_delta and same_ls:
                    issues.append(f"{ax.get_title() or 'axes'}: line {a} vs {b} "
                                  f"ΔL={abs(la-lb):.2f}, same style → indistinguishable in print")
    return issues


def save(fig, path: str, check: bool = True) -> None:
    if check:
        for msg in gray_check(fig):
            print("[BW-CHECK]", msg)
    fig.savefig(path)


def to_print_gray(src: str, dst: str) -> None:
    """Preview how ANY image (e.g. a TradingView screenshot) will print: luminance only."""
    from PIL import Image
    Image.open(src).convert("L").save(dst)
