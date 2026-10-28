"""ch04_etf_cost.py — Chapter 4 Hands-On: the Round-Trip Cost (RTC) of an ETF from a live quote.

RTC = TER + 2 x spread (one year, % of the amount). Hurdle = the gain a trade must
target to be worth its round trip (5 x the round-trip spread).
One quote is a snapshot: sample several, at different hours, before you decide.

Run from the repo root:
    python ch04_etf_cost.py CSPX.L --ter 0.07
    python ch04_etf_cost.py AMEW.DE --ter 0.38 --amount 20000 --years 5
    python ch04_etf_cost.py --demo
    python ch04_etf_cost.py --amundi --demo
    python ch04_etf_cost.py --amundi --listing .DE --limit 20
    python ch04_etf_cost.py --amundi --listing PA --limit 20
    python ch04_etf_cost.py --amundi --list-by-listing --listing PA
    python ch04_etf_cost.py --list-by-listing --listing PA
    python ch04_etf_cost.py --list-by-listing --listing MI --limit 50
    python ch04_etf_cost.py --list-exchanges
    python ch04_etf_cost.py --list-by-listing --listing DE --hedge unhedged
    python ch04_etf_cost.py --list-by-listing --listing DE --amundi --hedge hedged
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pandas as pd

from common import show
from common.amundi_etfs import demo_amundi_etfs
from common.justetf_catalog import (
    HedgeFilter,
    demo_list_by_listing,
    etfs_on_listing,
    filter_by_hedge,
)
from common.justetf_listings import available_exchanges, yahoo_symbol_for_listing


def rtc(ter_pct: float, spread_pct: float) -> float:
    """Round-trip cost: TER + 2× one-way spread (% per year)."""
    return ter_pct + 2 * spread_pct


def cost_eur(amount: float, ter_pct: float, spread_pct: float, years: float) -> float:
    """Euros paid over `years`: the fee every year, the spread once (buy + sell)."""
    return amount * (ter_pct * years + 2 * spread_pct) / 100


def hurdle(spread_pct: float) -> float:
    """Minimum gain target: 5× round-trip spread (%)."""
    return 5 * (2 * spread_pct)


def _valid_bid_ask(bid: float | None, ask: float | None) -> bool:
    if bid is None or ask is None:
        return False
    try:
        bid_f, ask_f = float(bid), float(ask)
    except (TypeError, ValueError):
        return False
    return bid_f > 0 and ask_f > 0 and ask_f >= bid_f


def yahoo_symbol_available(ticker: str, info: dict | None = None) -> bool:
    """True if Yahoo returns a tradable quote for this symbol."""
    import yfinance as yf

    q = info if info is not None else yf.Ticker(ticker).info
    if not q:
        return False
    if q.get("regularMarketPrice") or q.get("previousClose"):
        return True
    return q.get("quoteType") in {"EQUITY", "ETF", "MUTUALFUND", "INDEX"}


def quote_spread(
    ticker: str,
    *,
    strict: bool = True,
    estimate: bool = False,
    info: dict | None = None,
) -> tuple[float | None, str]:
    """Spread from Yahoo bid/ask, or day-range estimate when bid/ask are missing."""
    import yfinance as yf

    q = info if info is not None else yf.Ticker(ticker).info
    bid, ask = q.get("bid"), q.get("ask")
    if _valid_bid_ask(bid, ask):
        mid = (float(ask) + float(bid)) / 2
        return (float(ask) - float(bid)) / mid * 100, ""

    if estimate:
        high, low = q.get("regularMarketDayHigh"), q.get("regularMarketDayLow")
        last = q.get("regularMarketPrice") or q.get("previousClose")
        if high and low and last:
            high_f, low_f, last_f = float(high), float(low), float(last)
            if high_f > low_f > 0 and last_f > 0:
                # Crude one-way spread proxy from the session range (not a true quote).
                one_way = (high_f - low_f) / (2 * last_f) * 100
                return one_way, "spread est. (day range)"

    if strict:
        raise SystemExit(
            f"{ticker}: no bid/ask now (market closed?) - try during trading hours or --estimate-spread"
        )
    return None, ""


def spread_pct(ticker: str, *, strict: bool = True, estimate: bool = False) -> float | None:
    spread, _ = quote_spread(ticker, strict=strict, estimate=estimate)
    return spread


def sort_by_ter(df: pd.DataFrame) -> pd.DataFrame:
    """Lowest TER first (missing TER last)."""
    if df.empty or "ter" not in df.columns:
        return df
    return df.sort_values("ter", ascending=True, na_position="last").reset_index(drop=True)


def list_amundi_etfs(
    *,
    demo: bool = False,
    include_active: bool = True,
    hedge: HedgeFilter = "any",
) -> pd.DataFrame:
    """Retrieve Amundi ETF symbols and TER from justETF (or offline demo rows)."""
    from common.amundi_etfs import amundi_etfs

    if demo:
        return filter_by_hedge(demo_amundi_etfs(), hedge)
    return amundi_etfs(include_active=include_active, hedge=hedge)


def list_catalog_by_listing(
    catalog: pd.DataFrame,
    listing: str,
    *,
    demo: bool = False,
    limit: int = 0,
    include_unlisted: bool = False,
) -> tuple[pd.DataFrame, int]:
    """Map catalog rows to Yahoo symbols for a venue (no live spread quotes)."""
    df = catalog.head(limit) if limit and limit > 0 else catalog
    out: list[dict] = []
    skipped = 0
    for _, row in df.iterrows():
        yahoo, note = yahoo_symbol_for_listing(
            str(row["isin"]),
            str(row["ticker"]),
            listing,
            demo=demo,
        )
        if not yahoo and not include_unlisted:
            skipped += 1
            continue
        out.append(
            {
                "yahoo": yahoo,
                "isin": row["isin"],
                "screener": row["ticker"],
                "ter": row["ter"],
                "name": row["name"],
                "note": note,
            }
        )
    return pd.DataFrame(out), skipped


def etf_cost_table(
    catalog: pd.DataFrame,
    *,
    amount: float,
    years: float,
    listing: str = ".DE",
    demo: bool = False,
    limit: int = 0,
    default_ter: float | None = None,
    estimate_spread: bool = False,
) -> tuple[pd.DataFrame, int]:
    """Build spread / RTC / cost / hurdle for each row in `catalog`.

    Returns (table, skipped) where skipped counts rows with no Yahoo symbol or no quote.
    """
    df = sort_by_ter(catalog)
    out: list[dict] = []
    skipped = 0
    demo_spread = 0.06
    cost_col = f"cost_eur_{years:g}y"
    for _, row in df.iterrows():
        yahoo, map_note = yahoo_symbol_for_listing(
            str(row["isin"]),
            str(row["ticker"]),
            listing,
            demo=demo,
        )
        ter = row["ter"] if pd.notna(row.get("ter")) else default_ter
        if not yahoo:
            skipped += 1
            continue
        if ter is None:
            skipped += 1
            continue
        if demo:
            s, spread_note = demo_spread, ""
        else:
            import yfinance as yf

            info = yf.Ticker(yahoo).info
            if not yahoo_symbol_available(yahoo, info):
                skipped += 1
                continue
            s, spread_note = quote_spread(
                yahoo, strict=False, estimate=estimate_spread, info=info
            )
        if s is None:
            skipped += 1
            continue
        note = ", ".join(x for x in (map_note, spread_note) if x)
        out.append(
            {
                "yahoo": yahoo,
                "isin": row["isin"],
                "name": row["name"],
                "ter": ter,
                "spread_pct": round(s, 3),
                "rtc_pct_1y": round(rtc(ter, s), 2),
                cost_col: round(cost_eur(amount, ter, s, years)),
                "trade_hurdle_pct": round(hurdle(s), 1),
                "note": note,
            }
        )
    table = sort_by_ter(pd.DataFrame(out))
    if limit and limit > 0:
        table = table.head(limit)
    return table, skipped


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="ETF round-trip cost from live quotes.")
    p.add_argument("symbols", nargs="*", default=["DEMO"])
    p.add_argument("--ter", type=float, default=0.38, help="yearly TER %% (single-ticker mode)")
    p.add_argument("--amount", type=float, default=20000.0)
    p.add_argument("--years", type=float, default=5.0)
    p.add_argument("--demo", action="store_true")
    p.add_argument(
        "--amundi",
        action="store_true",
        help="load Amundi ETFs from justETF and print a cost table",
    )
    p.add_argument(
        "--listing",
        default=".DE",
        help="venue: .DE, .PA, PA/PAR (Paris), .L, … — Paris uses justETF Euronext tickers",
    )
    p.add_argument("--limit", type=int, default=0, help="max ETFs to quote (0 = all)")
    p.add_argument(
        "--no-active",
        action="store_true",
        help="exclude Amundi active ETFs from the justETF list",
    )
    p.add_argument(
        "--estimate-spread",
        action="store_true",
        help="if bid/ask missing, estimate one-way spread from the session high/low",
    )
    p.add_argument(
        "--no-estimate-spread",
        action="store_true",
        help="disable day-range spread fallback (enabled by default for Paris listings)",
    )
    p.add_argument(
        "--list-by-listing",
        action="store_true",
        help="print ETFs on --listing with Yahoo symbols (all funds; use --amundi to filter)",
    )
    p.add_argument(
        "--include-unlisted",
        action="store_true",
        help="with --list-by-listing: include rows with no symbol on that venue",
    )
    p.add_argument(
        "--list-exchanges",
        action="store_true",
        help="print venues supported by --listing and --list-by-listing",
    )
    p.add_argument(
        "--hedge",
        choices=("any", "hedged", "unhedged"),
        default="any",
        help="currency-hedged share class filter for --list-by-listing and --amundi",
    )
    return p.parse_args()


def _print_exchanges() -> None:
    rows = [
        {
            "mic": ex.mic,
            "exchange": ex.name,
            "yahoo": ex.yahoo_suffix,
            "country": ex.screener_country,
            "use_listing": ex.listing_aliases[0],
        }
        for ex in available_exchanges()
    ]
    df = pd.DataFrame(rows)
    print(df.to_string(index=False))
    print(
        "\nPass any alias to --listing (e.g. --list-by-listing --listing PA). "
        "Bulk lists use justETF screener ls=MIC."
    )


def _estimate_spread_default(listing: str, no_estimate: bool, force_estimate: bool) -> bool:
    if no_estimate:
        return False
    if force_estimate:
        return True
    key = listing.strip().lower()
    return key in {"pa", ".pa", "par", "paris", "xpar"}


if __name__ == "__main__":
    a = _parse_args()
    if a.list_exchanges:
        _print_exchanges()
        sys.exit(0)

    estimate = _estimate_spread_default(a.listing, a.no_estimate_spread, a.estimate_spread)

    if a.list_by_listing:
        if a.demo:
            table = demo_list_by_listing(a.listing, hedge=a.hedge)
            skipped = 0
        else:
            try:
                provider = "Amundi ETF" if a.amundi else None
                table = etfs_on_listing(
                    a.listing,
                    provider=provider,
                    include_active=not a.no_active,
                    hedge=a.hedge,
                )
            except ValueError as e:
                raise SystemExit(str(e)) from e
            skipped = 0
        table = sort_by_ter(table)
        if a.limit and a.limit > 0:
            table = table.head(a.limit)
        cols = ["yahoo", "isin", "screener", "ter", "hedged", "currency", "name", "note"]
        cols = [c for c in cols if c in table.columns]
        if len(table):
            print(table[cols].to_string(index=False))
        else:
            print("(no rows — empty catalog or unknown listing)")
        scope = "Amundi " if a.amundi else ""
        hedge_note = "" if a.hedge == "any" else f", hedge={a.hedge}"
        tail = f"\n{len(table)} {scope}ETFs on listing {a.listing!r}{hedge_note}"
        if skipped:
            tail += f"; {skipped} skipped (no symbol on venue)"
        print(tail)
        sys.exit(0)

    if a.amundi:
        catalog = list_amundi_etfs(
            demo=a.demo, include_active=not a.no_active, hedge=a.hedge
        )
        table, skipped = etf_cost_table(
            catalog,
            amount=a.amount,
            years=a.years,
            listing=a.listing,
            demo=a.demo,
            limit=a.limit,
            default_ter=a.ter,
            estimate_spread=estimate,
        )
        cost_col = f"cost_eur_{a.years:g}y"
        cols = ["yahoo", "ter", "spread_pct", "rtc_pct_1y", cost_col, "trade_hurdle_pct", "note"]
        if len(table):
            print(table[cols].to_string(index=False))
        else:
            print("(no rows — all skipped or empty catalog)")
        est = (table["note"].str.contains("spread est", na=False)).sum() if len(table) else 0
        tail = f"\n{len(table)} rows"
        if skipped:
            tail += f"; {skipped} skipped (no symbol or quote)"
        if est:
            tail += f" ({est} estimated from day range)"
        if a.demo:
            tail += " (demo spreads)"
        print(tail)
        sys.exit(0)

    symbol = a.symbols[0]
    if a.demo:
        s = 0.06
    else:
        s = spread_pct(symbol, estimate=estimate)
    show(
        {
            "spread_pct": round(s, 3),
            "rtc_pct_1y": round(rtc(a.ter, s), 2),
            f"cost_eur_{a.years:g}y": round(cost_eur(a.amount, a.ter, s, a.years)),
            "trade_hurdle_pct": round(hurdle(s), 1),
        }
    )
