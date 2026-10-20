"""
ch12_figures.py — Figure 12.1, ADX dashboard (BTC/USD daily), B&W print version.

Data : common/data/BTCUSD_kraken_daily_2026-03-01_2026-10-19.csv (common.book_data)
Maths: common.indicators.adx  (= Listing 12.1)
Style: common.pft_bw          (B&W print rules, style.md §Charts)

    python ch12_figures.py                 # writes Ch12_ADX_dashboard_BTC_bw.png
    python ch12_figures.py --out PATH
    python ch12_figures.py --selftest
"""
import argparse, os, sys
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common.indicators import adx          # noqa: E402
from common import pft_bw as bw            # noqa: E402

from common.book_data import btc_daily  # noqa: E402
START, END = "2026-07-27", "2026-09-17"


def load() -> pd.DataFrame:
    d = btc_daily()
    return d.join(adx(d[["open", "high", "low", "close"]]))


def regime_label(row) -> str:
    lvl = "STRONG TREND" if row.adx > 40 else "TREND" if row.adx > 25 else \
          "WEAK" if row.adx > 20 else "NO TREND"
    side = "Bull" if row.plus_di > row.minus_di else "Bear"
    return f"{lvl} · {side}"


def draw(d: pd.DataFrame, out: str) -> None:
    w = d.loc[START:END]
    x = mdates.date2num(w.index.to_pydatetime())
    bw.apply(8)
    fig, (a, b) = plt.subplots(2, 1, figsize=(7, 4.2), height_ratios=[1.8, 1],
                               sharex=True, gridspec_kw=dict(hspace=0.06))
    last = w.iloc[-1]
    # header strip (replaces the coloured dashboard header)
    fig.text(0.125, 0.895,
             f"BTC/USD · Daily    ADX {last.adx:.1f}    {regime_label(last)}    "
             f"+DI {last.plus_di:.1f}    −DI {last.minus_di:.1f}",
             fontsize=7.5, fontweight="bold", color=bw.INK,
             bbox=dict(boxstyle="square,pad=0.4", fc=bw.G_PANEL, ec=bw.G_MID, lw=0.6))
    # price pane
    bw.candles(a, w.open, w.high, w.low, w.close, x, width=0.62)
    a.axhline(last.close, **bw.ROLE["price_now"])
    a.annotate(f"{last.close:,.0f}", (x[-1], last.close), xytext=(8, 0),
               textcoords="offset points", va="center", fontsize=7, fontweight="bold",
               color=bw.PAPER, bbox=dict(boxstyle="square,pad=0.25", fc=bw.G_DARK, ec=bw.G_DARK))
    a.set_ylabel("USD")
    a.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v/1000:.0f}k"))
    a.text(0.01, 0.96, "□ hollow = up day     ■ filled = down day", transform=a.transAxes,
           fontsize=6.5, color=bw.G_DARK, va="top")
    # indicator pane
    above = w.adx > 25
    if above.any():
        bw.regime_band(b, x[np.argmax(above.values)] - 0.5, x[-1] + 0.5, "ADX > 25 — trend regime")
    for i, (name, col) in enumerate([("ADX", "adx"), ("+DI", "plus_di"), ("−DI", "minus_di")]):
        b.plot(x, w[col], **bw.series(i))
        bw.end_label(b, x, w[col].values, name, i, "{:.1f}")
    b.axhline(25, **bw.ROLE["threshold"])
    b.text(x[1], 26, "25", fontsize=6.5, color=bw.G_DARK, va="bottom")
    b.set_ylabel("ADX / DI")
    b.set_ylim(0, max(60, w[["adx", "plus_di", "minus_di"]].max().max() + 5))
    b.set_xlim(x[0] - 1, x[-1] + 9)
    b.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    b.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    bw.save(fig, out)
    plt.close(fig)


def summary(d: pd.DataFrame) -> dict:
    w = d.loc[START:END]
    rng = w.loc[:"2026-08-17"]
    return dict(range_adx=(round(rng.adx.min(), 1), round(rng.adx.max(), 1)),
                pdi_peak=round(w.plus_di.max(), 1), pdi_peak_day=str(w.plus_di.idxmax().date()),
                adx_peak=round(w.adx.max(), 1), adx_peak_day=str(w.adx.idxmax().date()),
                adx_cross25=str(w.index[(w.adx > 25).values.argmax()].date()),
                last=w.iloc[-1][["close", "adx", "plus_di", "minus_di"]].round(1).to_dict())


def selftest() -> None:
    d = load()
    assert len(d) >= 190 and d.index.is_monotonic_increasing
    s = summary(d)
    assert 40 < s["last"]["adx"] < 45, s          # dashboard snapshot read 42.3
    assert s["adx_peak"] > 45
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        draw(d, os.path.join(td, "fig.png"))
    print("selftest OK", s)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="Ch12_ADX_dashboard_BTC_bw.png")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        selftest()
    else:
        d = load(); print(summary(d)); draw(d, a.out); print("wrote", a.out)
