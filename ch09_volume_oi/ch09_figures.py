"""
ch09_figures.py — Figure 9.1, Volume and OBV dashboard (BTC/USD daily), B&W print version.

Data : common/data/BTCUSD_kraken_daily_*.csv (common.book_data) — Kraken XBT/USD
Maths: common.indicators.obv (= Listing 9.1), 20-day volume average
Style: common.pft_bw (style.md §0)

    python ch09_figures.py [--out PATH] | --selftest
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
from common.indicators import obv           # noqa: E402
from common import pft_bw as bw             # noqa: E402

START, END = "2026-03-25", "2026-09-17"


def load() -> pd.DataFrame:
    d = btc_daily()
    d["vavg"] = d.volume.rolling(20).mean()
    d["vx"] = d.volume / d.vavg
    w = d.loc[START:END].copy()
    w["obv"] = obv(w)                # OBV starts at 0 on the first bar of the window
    return w


def summary(w: pd.DataFrame) -> dict:
    dn = w[w.close < w.open]
    aug = w.loc["2026-08-17":"2026-08-25"]
    peak_may = w.obv.loc[:"2026-05-31"].max()
    aug_lo = w.obv.loc["2026-08-10":"2026-08-18"].min()
    aug_hi = w.obv.loc["2026-08-18":"2026-09-05"].max()
    return dict(
        obv_may_peak=(round(peak_may), str(w.obv.loc[:"2026-05-31"].idxmax().date())),
        obv_jun_jul_low=round(w.obv.loc["2026-06-01":"2026-07-31"].min()),
        biggest_down_vol=[(str(i.date()), round(v, 2)) for i, v in dn.nlargest(3, "volume").vx.items()],
        aug_up_days_vx=[(str(i.date()), round(v, 2)) for i, v in aug[aug.close > aug.open].vx.items() if v > 1.5],
        obv_aug_high=(round(aug_hi), str(w.obv.loc["2026-08-18":"2026-09-05"].idxmax().date())),
        obv_aug_high_vs_may=round(aug_hi - peak_may),
        obv_highest_since=str(w.obv.loc[:"2026-08-17"][w.obv.loc[:"2026-08-17"] >= aug_hi].index.max().date()),
        aug_gain=round(aug_hi - aug_lo),
        given_back_pct=round(100 * (aug_hi - w.obv.iloc[-1]) / (aug_hi - aug_lo)),
        price_high_aug=w.high.loc["2026-08-18":"2026-08-31"].max(),
        price_high_early_sep=w.high.loc["2026-09-01":"2026-09-10"].max(),
    )


def draw(w: pd.DataFrame, out: str) -> None:
    bw.apply(8)
    x = mdates.date2num(w.index.to_pydatetime())
    fig, (a, v, o) = plt.subplots(3, 1, figsize=(7, 4.2), height_ratios=[1.1, 1, 1.1],
                                  sharex=True, gridspec_kw=dict(hspace=0.08))
    bw.header(fig, f"BTC/USD · Daily    Volume and OBV    {w.index[0]:%d %b} – {w.index[-1]:%d %b %Y}", y=0.915)
    a.plot(x, w.close, **bw.series(0)); a.set_ylabel("Close")
    a.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda val, _: f"{val/1000:.0f}k"))
    up = (w.close >= w.open).values
    v.bar(x[up], w.volume[up] / 1000, width=0.75, facecolor=bw.PAPER, edgecolor=bw.INK, lw=0.4)
    v.bar(x[~up], w.volume[~up] / 1000, width=0.75, facecolor=bw.INK, edgecolor=bw.INK, lw=0.4)
    v.plot(x, w.vavg / 1000, **bw.ROLE["threshold"])
    v.set_ylabel("Vol (k BTC)")
    v.set_ylim(0, w.volume.max() / 1000 * 1.38)
    v.text(0.99, 0.95, "□ up-day volume   ■ down-day volume   - - 20-day average", transform=v.transAxes,
           fontsize=6.5, color=bw.G_DARK, va="top", ha="right")
    o.plot(x, w.obv / 1000, **bw.series(0))
    o.axhline(0, color=bw.G_MID, lw=0.5)
    bw.end_label(o, x, (w.obv / 1000).values, "OBV", 0, "{:.1f}k")
    o.set_ylabel("OBV (k BTC)")
    o.set_xlim(x[0] - 2, x[-1] + 22)
    o.xaxis.set_major_locator(mdates.MonthLocator()); o.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    bw.save(fig, out); plt.close(fig)


def selftest() -> None:
    w = load(); s = summary(w)
    assert len(w) > 170 and w.obv.iloc[0] == 0
    assert s["obv_aug_high_vs_may"] < 0          # August OBV high stays below May
    with tempfile.TemporaryDirectory() as td:
        draw(w, os.path.join(td, "f.png"))
    print("selftest OK", s)


if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--out", default="Ch09_OBV_dashboard_BTC_bw.png")
    p.add_argument("--selftest", action="store_true"); a = p.parse_args()
    if a.selftest: selftest()
    else:
        w = load(); print(summary(w)); draw(w, a.out); print("wrote", a.out)
