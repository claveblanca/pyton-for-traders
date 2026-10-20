"""
ch11_figures.py — Figure 11.1, RSI dashboard (BTC/USD daily), B&W print version.

Data : common.book_data — Kraken XBT/USD daily (RSI warm-up from 1 March)
Maths: common.indicators.rsi (Wilder, = Listing 11.1)
Style: common.pft_bw (style.md §0)

    python ch11_figures.py [--out PATH] | --selftest
"""
import argparse, os, sys, tempfile
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common.book_data import btc_daily      # noqa: E402
from common.indicators import rsi           # noqa: E402
from common import pft_bw as bw             # noqa: E402

START, END = "2026-08-26", "2026-09-17"
DIV = ("2026-08-27", "2026-09-03")          # bearish divergence: higher close, lower RSI


def load() -> pd.DataFrame:
    d = btc_daily(); d["rsi"] = rsi(d.close)
    return d.loc[START:END]


def summary(w) -> dict:
    a, b = DIV
    return dict(
        rsi_26_27=(round(w.rsi[a.replace("27", "26")], 1), round(w.rsi[a], 1)),
        div_close=(w.close[a], w.close[b]), div_rsi=(round(w.rsi[a], 1), round(w.rsi[b], 1)),
        rsi_sep4_10=(round(w.rsi.loc["2026-09-04":"2026-09-10"].max(), 1), round(w.rsi.loc["2026-09-04":"2026-09-10"].min(), 1)),
        rsi_sep15=round(w.rsi["2026-09-15"], 1), close_sep15=w.close["2026-09-15"],
        rsi_last=round(w.rsi.iloc[-1], 1),
    )


def draw(w, out) -> None:
    bw.apply(8)
    x = mdates.date2num(w.index.to_pydatetime())
    fig, (a, r) = plt.subplots(2, 1, figsize=(7, 4.0), height_ratios=[1.5, 1], sharex=True,
                               gridspec_kw=dict(hspace=0.07))
    last = w.iloc[-1]
    bw.header(fig, f"BTC/USD · Daily    RSI(14) {last.rsi:.1f}    Close {last.close:,.0f}", y=0.915)
    bw.candles(a, w.open, w.high, w.low, w.close, x, width=0.6)
    a.set_ylabel("USD")
    a.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v/1000:.0f}k"))
    r.plot(x, w.rsi, **bw.series(0))
    for lvl, ls in ((70, (0, (3, 3))), (50, (0, (1, 2))), (30, (0, (3, 3)))):
        r.axhline(lvl, color=bw.G_MID, lw=0.7, ls=ls)

    r.axhspan(45, 55, color="#EDEDED", lw=0, zorder=0)
    r.text(x[len(x) // 2], 46, "45–55 neutral", fontsize=6, color=bw.G_DARK, ha="center", va="bottom")
    # divergence: connect the two closes and the two RSI highs
    xa, xb = mdates.date2num(pd.Timestamp(DIV[0])), mdates.date2num(pd.Timestamp(DIV[1]))
    a.plot([xa, xb], [w.close[DIV[0]], w.close[DIV[1]]], color=bw.INK, lw=1.0, ls=(0, (4, 2)), marker="o",
           ms=3.5, mfc=bw.PAPER, zorder=5)
    r.plot([xa, xb], [w.rsi[DIV[0]], w.rsi[DIV[1]]], color=bw.INK, lw=1.0, ls=(0, (4, 2)), marker="o",
           ms=3.5, mfc=bw.PAPER, zorder=5)
    a.annotate("higher high", ((xa + xb) / 2, max(w.close[DIV[0]], w.close[DIV[1]])), xytext=(0, 10),
               textcoords="offset points", ha="center", fontsize=6.5, color=bw.INK)
    r.annotate("lower high → bearish divergence", ((xa + xb) / 2, (w.rsi[DIV[0]] + w.rsi[DIV[1]]) / 2),
               xytext=(18, 8), textcoords="offset points", ha="left", fontsize=6.5, color=bw.INK)
    bw.end_label(r, x, w.rsi.values, "RSI", 0, "{:.1f}")
    r.set_ylim(25, 90); r.set_yticks([30, 50, 70]); r.set_ylabel("RSI(14)")
    r.set_xlim(x[0] - 1, x[-1] + 3.2)
    r.xaxis.set_major_locator(mdates.DayLocator(interval=3)); r.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    bw.save(fig, out); plt.close(fig)


def selftest() -> None:
    w = load(); s = summary(w)
    assert s["div_close"][1] > s["div_close"][0] and s["div_rsi"][1] < s["div_rsi"][0]
    with tempfile.TemporaryDirectory() as td:
        draw(w, os.path.join(td, "f.png"))
    print("selftest OK", s)


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--out", default="Ch11_RSI_dashboard_BTC_bw.png")
    p.add_argument("--selftest", action="store_true"); a = p.parse_args()
    if a.selftest: selftest()
    else:
        w = load(); print(summary(w)); draw(w, a.out); print("wrote", a.out)
