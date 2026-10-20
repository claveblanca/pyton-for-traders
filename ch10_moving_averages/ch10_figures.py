"""
ch10_figures.py — Figures 10.1 (EMA 9/12/26 dashboard, daily) and 10.2 (Bollinger Bands, hourly),
B&W print versions.

Data : common.book_data — Kraken XBT/USD daily; Coinbase BTC-USD hourly (Kraken serves only
       the latest 720 hourly bars, see book_data.py)
Maths: common.indicators.ema / macd (Listings 10.2) and bollinger (Listing 10.4)
Style: common.pft_bw (style.md §0)

    python ch10_figures.py [--outdir DIR] | --selftest
"""
import argparse, os, sys, tempfile
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common.book_data import btc_daily, btc_hourly   # noqa: E402
from common.indicators import ema, macd, bollinger   # noqa: E402
from common import pft_bw as bw                      # noqa: E402

MA_START, MA_END = "2026-07-01", "2026-09-17"
BB_START, BB_END = "2026-09-19 00:00", "2026-09-24 09:00"   # last bar = the dashboard snapshot


def load_ma() -> pd.DataFrame:
    d = btc_daily()
    for n in (9, 12, 26):
        d[f"ema{n}"] = ema(d.close, n)
    return d.join(macd(d.close)).loc[MA_START:MA_END]


def load_bb() -> pd.DataFrame:
    h = btc_hourly()
    return h.join(bollinger(h.close)).loc[BB_START:BB_END]


def summary_ma(w) -> dict:
    cross = np.sign(w.ema9 - w.ema12).diff().fillna(0)
    c26 = np.sign(w.ema12 - w.ema26).diff().fillna(0)
    x = w.loc[:"2026-08-15", ["ema9", "ema12", "ema26"]]
    return dict(
        braid_range=(round(x.min().min()), round(x.max().max())),
        ema9_12_crosses_sep=[(str(i.date()), int(v)) for i, v in cross.loc["2026-09-01":].items() if v],
        ema12_26_cross_up=[str(i.date()) for i, v in c26.items() if v > 0],
        closes_below_ema26_sep=[str(i.date()) for i in w.loc["2026-09-01":].index if w.close[i] < w.ema26[i]],
        macd_aug_peak=round(w.macd.loc["2026-08-01":"2026-08-31"].max()),
        macd_last=round(w.macd.iloc[-1]),
    )


def summary_bb(h) -> dict:
    sq = h.bb_width
    return dict(
        width_min_19_21=round(sq.loc[:"2026-09-21 06:00"].min(), 4),
        range_19_21=(round(h.low.loc[:"2026-09-21 06:00"].min()), round(h.high.loc[:"2026-09-21 06:00"].max())),
        high_21=round(h.high.loc["2026-09-21"].max()),
        high_23=round(h.high.loc["2026-09-23"].max()),
        low_23=round(h.low.loc["2026-09-23"].min()),
        last=h.iloc[-1][["close", "bb_lower", "bb_mid"]].round(0).to_dict(),
        last_below_lower=bool(h.close.iloc[-1] < h.bb_lower.iloc[-1]),
    )


def draw_ma(w, out) -> None:
    bw.apply(8)
    x = mdates.date2num(w.index.to_pydatetime())
    fig, (a, m) = plt.subplots(2, 1, figsize=(7, 4.2), height_ratios=[2.4, 1], sharex=True,
                               gridspec_kw=dict(hspace=0.07))
    last = w.iloc[-1]
    bw.header(fig, f"BTC/USD · Daily    EMA 9 {last.ema9:,.0f}    EMA 12 {last.ema12:,.0f}    "
                   f"EMA 26 {last.ema26:,.0f}    MACD {last.macd:+,.0f}", y=0.915)
    bw.candles(a, w.open, w.high, w.low, w.close, x, width=0.62, tone="light")
    # EMA 26 = slow, most important → black solid; EMA 12 dashed; EMA 9 dotted
    for i, (name, col) in enumerate([("EMA 26", "ema26"), ("EMA 12", "ema12"), ("EMA 9", "ema9")]):
        a.plot(x, w[col], **bw.series(i))
    # end tags, nudged apart so they do not overlap
    # end tags stacked in value order, 13 pt apart, so they never overlap
    ys = sorted([(w[c].iloc[-1], n, i) for i, (n, c) in enumerate([("EMA 26", "ema26"), ("EMA 12", "ema12"), ("EMA 9", "ema9")])])
    for k, (yv, n, i) in enumerate(ys):
        dark = i in (0, 1)
        a.annotate(f"{n} {yv:,.0f}", (x[-1], yv), xytext=(8, (k - 1) * 13), textcoords="offset points",
                   va="center", fontsize=6.5, fontweight="bold", color=bw.PAPER if dark else bw.INK,
                   bbox=dict(boxstyle="square,pad=0.22", fc=(bw.INK, bw.G_DARK, bw.PAPER)[i], ec=(bw.INK, bw.G_DARK, bw.G_MID)[i], lw=0.7))
    a.set_ylabel("USD")
    a.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v/1000:.0f}k"))
    a.text(0.01, 0.95, "□ up day  ■ down day   — EMA 26   - - EMA 12   ··· EMA 9", transform=a.transAxes,
           fontsize=6.5, color=bw.G_DARK, va="top")
    m.plot(x, w.macd, **bw.series(0)); m.axhline(0, **bw.ROLE["threshold"])
    bw.end_label(m, x, w.macd.values, "MACD", 0, "{:+,.0f}")
    m.set_ylabel("MACD\n(12−26)")
    m.set_xlim(x[0] - 1, x[-1] + 15)
    bw.date_axis(m, x)
    bw.save(fig, out); plt.close(fig)


def draw_bb(h, out) -> None:
    bw.apply(8)
    x = mdates.date2num(h.index.to_pydatetime())
    fig, a = plt.subplots(figsize=(7, 3.6))
    last = h.iloc[-1]
    bw.header(fig, f"BTC/USD · 1 hour    Bollinger Bands (20, 2)    Upper {last.bb_upper:,.0f}    "
                   f"Mid {last.bb_mid:,.0f}    Lower {last.bb_lower:,.0f}", y=0.935)
    a.fill_between(x, h.bb_lower, h.bb_upper, color="#EDEDED", lw=0, zorder=0)
    w_c = (x[1] - x[0]) * 0.62
    bw.candles(a, h.open, h.high, h.low, h.close, x, width=w_c, tone="ink")
    a.plot(x, h.bb_upper, color=bw.G_DARK, lw=1.0, ls="-", zorder=4)
    a.plot(x, h.bb_lower, color=bw.G_DARK, lw=1.0, ls="-", zorder=4)
    a.plot(x, h.bb_mid, **{**bw.series(1), "zorder": 4})
    for name, col, i in (("Upper", "bb_upper", 1), ("Mid", "bb_mid", 1), ("Lower", "bb_lower", 1)):
        pass
    span = h[["bb_upper", "bb_lower"]].max().max() - h[["bb_upper", "bb_lower"]].min().min()
    for k, (name, col) in enumerate((("Lower", "bb_lower"), ("Mid", "bb_mid"), ("Upper", "bb_upper"))):
        a.annotate(f"{name} {last[col]:,.0f}", (x[-1], last[col]), xytext=(6, (k - 1) * 11), textcoords="offset points",
                   va="center", fontsize=6.5, fontweight="bold", color=bw.INK,
                   bbox=dict(boxstyle="square,pad=0.2", fc=bw.PAPER, ec=bw.G_DARK, lw=0.6))
    a.text(0.99, 0.03, "shaded = band (±2σ)   - - middle band (20-h SMA)   □ up hour  ■ down hour",
           transform=a.transAxes, fontsize=6.5, color=bw.G_DARK, va="bottom", ha="right",
           bbox=dict(boxstyle="square,pad=0.3", fc=bw.PAPER, ec="none"))
    a.set_ylabel("USD")
    a.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v/1000:.1f}k"))
    a.set_xlim(x[0] - 0.05, x[-1] + 0.55)
    bw.date_axis(a, x, hourly=True)
    bw.save(fig, out); plt.close(fig)


def selftest() -> None:
    w, h = load_ma(), load_bb()
    sm, sb = summary_ma(w), summary_bb(h)
    assert sb["last_below_lower"], sb
    assert sm["macd_last"] > 0 and sm["macd_last"] < sm["macd_aug_peak"]
    with tempfile.TemporaryDirectory() as td:
        draw_ma(w, os.path.join(td, "a.png")); draw_bb(h, os.path.join(td, "b.png"))
    print("selftest OK", sm, sb)


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--outdir", default=".")
    p.add_argument("--selftest", action="store_true"); a = p.parse_args()
    if a.selftest: selftest()
    else:
        w, h = load_ma(), load_bb(); print(summary_ma(w)); print(summary_bb(h))
        draw_ma(w, os.path.join(a.outdir, "Ch10_MA_dashboard_BTC_bw.png"))
        draw_bb(h, os.path.join(a.outdir, "Ch10_BB_dashboard_BTC_bw.png")); print("wrote 2 figures")
