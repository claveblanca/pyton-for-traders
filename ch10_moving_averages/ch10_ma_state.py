"""ch10_ma_state.py -- the moving-average state of a market, on the last bar.

Ref: §10.3 (slope confirms the single-MA signal), §10.4.1 (golden/death
cross), §10.5.2-10.5.3 (Bollinger %B, bandwidth, squeeze), §10.9.3
(Tables 10.3 and 10.4 trigger conditions).

Reports: EMA stack order, slope of each average, distance from SMA-200 in %
and in ATR units, bars since the last 50/200 cross, Bollinger %B, bandwidth
percentile (126 bars), squeeze flag, band-walk count, and the Table 10.3 /
10.4 rows that are true now (ADX from common.indicators gates them).

Usage:
    python ch10_ma_state.py --selftest
    python ch10_ma_state.py BTC-USD
"""

from __future__ import annotations

import argparse
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common.data import get_ohlcv, synthetic_ohlcv  # noqa: E402
from common.indicators import adx, atr, bollinger, crosses, ema, sma  # noqa: E402


def state(df: pd.DataFrame) -> dict:
    c = df["close"]
    e = {n: ema(c, n) for n in (9, 21, 50)}
    s50, s200 = sma(c, 50), sma(c, 200)
    bb = bollinger(c)
    a = adx(df)
    x = crosses(s50, s200)
    last_x = x[x != 0]
    width_pct = bb["bb_width"].rolling(126).rank(pct=True).iloc[-1] * 100
    walk = (bb["bb_pct_b"] > 0.8)[::-1].cumprod().sum()
    stack = [
        k
        for k, _ in sorted(
            {
                "price": c.iloc[-1],
                **{f"ema{n}": v.iloc[-1] for n, v in e.items()},
            }.items(),
            key=lambda kv: -kv[1],
        )
    ]
    out = {
        "date": str(df.index[-1].date()),
        "close": round(float(c.iloc[-1]), 2),
        "stack": " > ".join(stack),
        "bullish_stack": stack == ["price", "ema9", "ema21", "ema50"],
        "slope_ema21_5bar_pct": round(float(e[21].pct_change(5).iloc[-1] * 100), 2),
        "dist_sma200_pct": round(float((c.iloc[-1] / s200.iloc[-1] - 1) * 100), 2),
        "dist_sma200_atr": round(
            float((c.iloc[-1] - s200.iloc[-1]) / atr(df).iloc[-1]), 2
        ),
        "last_50_200_cross": (
            ("golden" if last_x.iloc[-1] > 0 else "death") if len(last_x) else None
        ),
        "bars_since_cross": (
            int(len(c) - 1 - c.index.get_loc(last_x.index[-1])) if len(last_x) else None
        ),
        "pct_b": round(float(bb["bb_pct_b"].iloc[-1]), 3),
        "bandwidth_pctile": round(float(width_pct), 1),
        "squeeze": bool(width_pct <= 10),
        "upper_band_walk_bars": int(walk),
        "adx": round(float(a["adx"].iloc[-1]), 1),
    }
    fast_x = crosses(e[9], e[21]).iloc[-1]
    trend, rng = out["adx"] > 25, out["adx"] < 20
    out["table_10_4"] = (
        "BUY"
        if fast_x > 0 and trend
        else (
            "SELL"
            if fast_x < 0 and trend
            else "STAND ASIDE (braided, ADX < 20)" if rng else "no trigger"
        )
    )
    out["table_10_5"] = (
        "BUY breakout"
        if out["squeeze"] and out["pct_b"] > 1
        else (
            "SELL breakout"
            if out["squeeze"] and out["pct_b"] < 0
            else (
                "HOLD band walk"
                if 0.5 < out["pct_b"] <= 1 and trend
                else "MEAN REVERSION zone" if rng else "no trigger"
            )
        )
    )
    return out


def selftest() -> None:
    s = state(synthetic_ohlcv(800))
    assert (
        s["last_50_200_cross"] in {"golden", "death"}
        and 0 <= s["bandwidth_pctile"] <= 100
    )
    up = synthetic_ohlcv(400, regimes=False, drift=0.004, vol=0.005)
    su = state(up)
    assert su["bullish_stack"] and su["dist_sma200_pct"] > 0
    for k, v in s.items():
        print(f"{k:24s} {v}")
    print("selftest OK")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("symbol", nargs="?")
    p.add_argument("--interval", default="1d")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest or not a.symbol:
        selftest()
    else:
        for k, v in state(get_ohlcv(a.symbol, a.interval)).items():
            print(f"{k:24s} {v}")
