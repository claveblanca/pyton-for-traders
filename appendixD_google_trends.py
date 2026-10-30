"""appendixD_google_trends.py — search-interest trends (Google Trends / pytrends).

Unofficial API: keep request volume low.

    python appendixD_google_trends.py --demo
    python appendixD_google_trends.py --category economy
    python appendixD_google_trends.py --keyword inflation --timeframe "today 1-m"
    python appendixD_google_trends.py --trending --geo italy
    python appendixD_google_trends.py --all-categories --geo US
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from common import show
from common.google_trends import (
    CATEGORY_KEYWORDS,
    demo_interest,
    interest_by_category,
    interest_over_time,
    latest_vs_recent_mean,
    trending_searches,
)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Google Trends search interest.")
    p.add_argument("--demo", action="store_true")
    p.add_argument(
        "--category",
        choices=list(CATEGORY_KEYWORDS),
        help="use default keywords for economy/trading/crypto/geopolitics/commodities",
    )
    p.add_argument("--keyword", action="append", default=[], help="one or more search terms")
    p.add_argument("--all-categories", action="store_true", help="summarize all five categories")
    p.add_argument("--timeframe", default="today 3-m", help='e.g. "today 1-m", "today 5-y"')
    p.add_argument("--geo", default="", help='region code, e.g. US, GB, IT (empty = worldwide)')
    p.add_argument(
        "--trending",
        action="store_true",
        help="show daily trending searches (uses --geo as country name if set)",
    )
    p.add_argument(
        "--trending-geo",
        default="united_states",
        help="pytrends country name for trending_searches (default united_states)",
    )
    return p.parse_args()


def _summarize_df(df, label: str) -> None:
    if df.empty:
        print(f"{label}: no data\n")
        return
    print(f"--- {label} (last 5 rows) ---")
    print(df.tail().to_string(), "\n")
    for col in df.columns:
        stats = latest_vs_recent_mean(df[col])
        if stats["latest"] is not None:
            show(
                {
                    "series": col,
                    "latest": round(stats["latest"], 1),
                    "recent_mean": round(stats["mean"], 1) if stats["mean"] else None,
                    "latest_over_mean": round(stats["ratio"], 2) if stats["ratio"] else None,
                }
            )


if __name__ == "__main__":
    a = _parse_args()

    if a.trending:
        if a.demo:
            print("0  inflation\n1  bitcoin\n2  stock market\n(demo)")
            sys.exit(0)
        geo = a.trending_geo
        if a.geo and not a.trending_geo:
            geo = a.geo.lower().replace(" ", "_")
        df = trending_searches(geo=geo)
        print(df.head(20).to_string(index=False))
        sys.exit(0)

    if a.all_categories:
        for cat in CATEGORY_KEYWORDS:
            kws = CATEGORY_KEYWORDS[cat]
            if a.demo:
                df = demo_interest(kws)
            else:
                df = interest_by_category(cat, timeframe=a.timeframe, geo=a.geo)
            print(f"=== {cat} ===")
            _summarize_df(df, cat)
        sys.exit(0)

    if a.category:
        kws = CATEGORY_KEYWORDS[a.category]
    elif a.keyword:
        kws = a.keyword
    else:
        kws = CATEGORY_KEYWORDS["economy"]

    if a.demo:
        df = demo_interest(kws)
    elif a.category:
        df = interest_by_category(a.category, timeframe=a.timeframe, geo=a.geo)
    else:
        df = interest_over_time(kws, timeframe=a.timeframe, geo=a.geo)

    _summarize_df(df, a.category or ", ".join(kws))
