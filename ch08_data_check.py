"""ch08_data_check.py — Chapter 8 Hands-On: your first live bars, checked, and the trend they show.

Downloads daily bars (Kraken for crypto, yfinance for everything else), runs the
data-quality checks every later chapter relies on, then reads the trend the classic
way: compare the last 20 days' high and low with the 20 days before.

Run from the repo root:
    python ch08_data_check.py XBTUSD --kraken
    python ch08_data_check.py SPY
    python ch08_data_check.py --demo
"""
import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from common import cli, daily, check_ohlcv, show


def trend(df, n=20) -> str:
    now, before = df.tail(n), df.iloc[-2 * n:-n]
    hh, hl = now.high.max() > before.high.max(), now.low.min() > before.low.min()
    lh, ll = now.high.max() < before.high.max(), now.low.min() < before.low.min()
    return ("uptrend (higher high, higher low)" if hh and hl else
            "downtrend (lower high, lower low)" if lh and ll else "no clear trend (range)")


if __name__ == "__main__":
    (sym, *_), demo = cli(["XBTUSD"])
    df = daily(sym, demo, kraken="--kraken" in sys.argv)
    q = check_ohlcv(df)
    problems = [k for k in ("duplicate_ts", "nan_cells", "ohlc_violations", "missing_bar_gaps") if q.get(k)]
    show({**q, "data": "OK" if not problems else f"fix before use: {problems}",
          "last_close": f"{df.close.iloc[-1]:,.2f} on {df.index[-1].date()}", "trend": trend(df)})
