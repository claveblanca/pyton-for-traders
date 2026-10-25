"""ch02_stock_screen.py — Chapter 2 Hands-On: SEC fundamentals, ratios, and market multiples.

Self-contained SEC XBRL (companyfacts) plus optional yfinance for current valuation multiples.

Requires:
    export SEC_USER_AGENT="Your Name you@email.com"
    pip install pandas requests
    pip install yfinance   # for P/E, P/B, EV/Sales, etc. (skip with --no-yfinance)

Run from the repo root:
    python ch02_stock_screen.py              # default AAPL
    python ch02_stock_screen.py NVDA MSFT
    python ch02_stock_screen.py AAPL --years 10
    python ch02_stock_screen.py AAPL --no-yfinance
"""
from __future__ import annotations

import argparse
import os
import sys
from functools import lru_cache

import pandas as pd
import requests

YEARS = 7

SEC_FIELDS = [
    "total_assets",
    "total_liabilities",
    "equity",
    "goodwill",
    "other_intangibles",
    "cash",
    "long_term_debt",
    "debt_current",
    "revenue",
    "cogs",
    "ebit",
    "interest_expense",
    "net_income",
    "cfo",
    "capex_ppe",
]

# field -> XBRL tags (first tag with data for a year wins via combine_first)
EDGAR_TAGS: dict[str, list[str]] = {
    "total_assets": ["us-gaap:Assets", "ifrs-full:Assets"],
    "total_liabilities": ["us-gaap:Liabilities", "ifrs-full:Liabilities"],
    "equity": [
        "us-gaap:StockholdersEquity",
        "us-gaap:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
        "ifrs-full:EquityAttributableToOwnersOfParent",
    ],
    "goodwill": ["us-gaap:Goodwill", "ifrs-full:Goodwill"],
    "other_intangibles": [
        "us-gaap:IntangibleAssetsNetExcludingGoodwill",
        "ifrs-full:IntangibleAssetsOtherThanGoodwill",
    ],
    "cash": [
        "us-gaap:CashAndCashEquivalentsAtCarryingValue",
        "ifrs-full:CashAndCashEquivalents",
    ],
    "long_term_debt": [
        "us-gaap:LongTermDebtNoncurrent",
        "us-gaap:LongTermDebt",
        "us-gaap:LongTermDebtAndCapitalLeaseObligations",
    ],
    "debt_current": [
        "us-gaap:DebtCurrent",
        "us-gaap:ShortTermBorrowings",
        "us-gaap:CommercialPaper",
    ],
    "revenue": [
        "us-gaap:Revenues",
        "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax",
        "us-gaap:SalesRevenueNet",
        "ifrs-full:Revenue",
    ],
    "cogs": [
        "us-gaap:CostOfRevenue",
        "us-gaap:CostOfGoodsAndServicesSold",
        "ifrs-full:CostOfSales",
    ],
    "ebit": [
        "us-gaap:OperatingIncomeLoss",
        "ifrs-full:ProfitLossFromOperatingActivities",
    ],
    "interest_expense": [
        "us-gaap:InterestExpense",
        "us-gaap:InterestExpenseNonoperating",
        "us-gaap:InterestExpenseDebt",
        "ifrs-full:InterestExpense",
        "ifrs-full:FinanceCosts",
    ],
    "net_income": [
        "us-gaap:NetIncomeLoss",
        "ifrs-full:ProfitLossAttributableToOwnersOfParent",
    ],
    "cfo": [
        "us-gaap:NetCashProvidedByUsedInOperatingActivities",
        "ifrs-full:CashFlowsFromUsedInOperatingActivities",
    ],
    "capex_ppe": [
        "us-gaap:PaymentsToAcquirePropertyPlantAndEquipment",
        "ifrs-full:PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities",
    ],
    # Not in SEC_FIELDS: used only for historical market cap (unit is shares, not USD).
    "shares_diluted": [
        "us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding",
        "us-gaap:WeightedAverageNumberOfShareOutstandingBasicAndDiluted",
        "us-gaap:WeightedAverageNumberOfSharesOutstandingBasic",
    ],
}

RATIO_COLS = [
    "gross_margin",
    "operating_margin",
    "net_margin",
    "roa",
    "roe",
    "fcf",
]

# Short column titles for printed tables (internal keys unchanged).
SEC_LABELS: dict[str, str] = {
    "total_assets": "Total assets",
    "total_liabilities": "Total liabilities",
    "equity": "Stockholders' equity",
    "goodwill": "Goodwill",
    "other_intangibles": "Other intangibles",
    "cash": "Cash & equivalents",
    "long_term_debt": "Long-term debt",
    "debt_current": "Current debt",
    "revenue": "Revenue",
    "cogs": "Cost of revenue (COGS)",
    "ebit": "Operating income (EBIT)",
    "interest_expense": "Interest expense",
    "net_income": "Net income",
    "cfo": "Operating cash flow (CFO)",
    "capex_ppe": "CapEx (PP&E)",
}

# (display name, one-line definition)
RATIO_HELP: dict[str, tuple[str, str]] = {
    "gross_margin": (
        "Gross margin (%)",
        "Revenue minus COGS, divided by revenue — profit after direct product costs.",
    ),
    "operating_margin": (
        "Operating margin (%)",
        "Operating income (EBIT) divided by revenue — profit from core operations.",
    ),
    "net_margin": (
        "Net profit margin (%)",
        "Net income divided by revenue — bottom-line profit as a share of sales.",
    ),
    "roa": (
        "Return on assets — ROA (%)",
        "Net income divided by average total assets — how efficiently assets earn profit.",
    ),
    "roe": (
        "Return on equity — ROE (%)",
        "Net income divided by book equity — return to shareholders on accounting equity.",
    ),
    "fcf": (
        "Free cash flow — FCF (USD)",
        "Operating cash flow minus capital expenditure — cash left after maintaining the business.",
    ),
    "total_debt": (
        "Total debt (USD)",
        "Long-term debt plus current debt tags from the 10-K (may omit some lease/other obligations).",
    ),
}

VALUATION_HELP: dict[str, tuple[str, str]] = {
    "price": (
        "Share price (USD)",
        "Last market price from Yahoo Finance (today).",
    ),
    "market_cap": (
        "Market capitalization (USD)",
        "Share price × shares outstanding — total equity market value.",
    ),
    "pe": (
        "P/E — Price-to-Earnings",
        "Market cap divided by last fiscal year net income — dollars paid per $1 of annual earnings.",
    ),
    "pb": (
        "P/B — Price-to-Book",
        "Market cap divided by last fiscal year book equity — market value vs accounting net worth.",
    ),
    "p_cf": (
        "P/CF — Price-to-Cash-Flow",
        "Market cap divided by last fiscal year operating cash flow — valuation vs cash from operations.",
    ),
    "p_fcf": (
        "P/FCF — Price-to-Free-Cash-Flow",
        "Market cap divided by last fiscal year free cash flow — valuation vs cash after CapEx.",
    ),
    "ev": (
        "EV — Enterprise value (USD)",
        "Market cap + total debt − cash — approximate value of the whole firm to all capital providers.",
    ),
    "ev_to_sales": (
        "EV/Sales — Enterprise value to revenue",
        "Enterprise value divided by last fiscal year revenue — how many dollars of EV per $1 of sales.",
    ),
}

HISTORY_LABELS: dict[str, str] = {
    "fy_end": "FY end",
    "price": "Price",
    "market_cap": "Market cap",
    "pe": "P/E",
    "pb": "P/B",
    "p_cf": "P/CF",
    "p_fcf": "P/FCF",
    "ev": "EV",
    "ev_to_sales": "EV/Sales",
}


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("symbols", nargs="*", default=["AAPL"], help="tickers (default AAPL)")
    p.add_argument("--years", type=int, default=YEARS, help=f"fiscal years to show (default {YEARS})")
    p.add_argument(
        "--no-yfinance",
        action="store_true",
        help="skip market multiples (P/E, EV/Sales, …)",
    )
    return p.parse_args(argv)


def _sec_get(url: str) -> dict:
    ua = os.getenv("SEC_USER_AGENT")
    if not ua:
        raise SystemExit(
            "SEC EDGAR requires SEC_USER_AGENT, e.g.\n"
            '  export SEC_USER_AGENT="Your Name you@email.com"'
        )
    r = requests.get(url, headers={"User-Agent": ua}, timeout=30)
    r.raise_for_status()
    return r.json()


@lru_cache(maxsize=1)
def _ticker_cik_map() -> dict[str, int]:
    data = _sec_get("https://www.sec.gov/files/company_tickers.json")
    return {row["ticker"].upper(): int(row["cik_str"]) for row in data.values()}


@lru_cache(maxsize=32)
def _company_facts(cik: int) -> dict:
    return _sec_get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json")


def _tag_frame(facts: dict, qtag: str) -> pd.DataFrame:
    """Annual facts for one tag: columns end, filed, val (latest filing per period end)."""
    empty = pd.DataFrame(columns=["end", "filed", "val"])
    tax, tag = qtag.split(":")
    node = facts.get("facts", {}).get(tax, {}).get(tag)
    if not node:
        return empty
    units = node["units"]
    unit = "USD" if "USD" in units else next((u for u in units if "/" not in u), None)
    if unit is None:
        return empty
    rows = []
    for f in units[unit]:
        if not str(f.get("form", "")).startswith(("10-K", "20-F", "40-F")):
            continue
        end = pd.Timestamp(f["end"])
        if "start" in f:
            days = (end - pd.Timestamp(f["start"])).days
            if not 350 <= days <= 380:
                continue
        rows.append((end, f.get("filed", ""), float(f["val"])))
    if not rows:
        return empty
    return (
        pd.DataFrame(rows, columns=["end", "filed", "val"])
        .sort_values("filed")
        .drop_duplicates("end", keep="last")
    )


def _tag_series(facts: dict, qtag: str) -> pd.Series:
    df = _tag_frame(facts, qtag)
    if df.empty:
        return pd.Series(dtype=float)
    s = df.set_index(df["end"].dt.year)["val"]
    return s.groupby(level=0).last()


def _fy_end_dates(facts: dict) -> pd.Series:
    """Fiscal year label -> balance-sheet date, from the total assets tag."""
    for qtag in EDGAR_TAGS["total_assets"]:
        df = _tag_frame(facts, qtag)
        if not df.empty:
            return df.groupby(df["end"].dt.year)["end"].max()
    return pd.Series(dtype="datetime64[ns]")


def _shares_frame(facts: dict) -> pd.DataFrame:
    """Diluted share count per fiscal year plus the filing date it comes from."""
    frames = []
    for qtag in EDGAR_TAGS["shares_diluted"]:
        df = _tag_frame(facts, qtag)
        if df.empty:
            continue
        df = df.assign(filed=pd.to_datetime(df["filed"])).groupby(df["end"].dt.year).last()
        frames.append(df.rename(columns={"val": "shares_diluted", "filed": "shares_filed"})[
            ["shares_diluted", "shares_filed"]
        ])
    if not frames:
        return pd.DataFrame(columns=["shares_diluted", "shares_filed"])
    return pd.concat(frames).groupby(level=0).first()


def _field_series(facts: dict, field: str) -> pd.Series:
    out = pd.Series(dtype=float)
    for qtag in EDGAR_TAGS[field]:
        out = out.combine_first(_tag_series(facts, qtag))
    if field == "interest_expense":
        out = out.abs()
    if field == "capex_ppe":
        out = out.abs()
    return out


def fetch_annual(ticker: str, years: int = YEARS) -> pd.DataFrame:
    """SEC_FIELDS per fiscal year, plus fy_end, shares_diluted, shares_filed."""
    cik = _ticker_cik_map().get(ticker.upper())
    if cik is None:
        raise SystemExit(f"{ticker!r} is not in SEC company_tickers (US filer only).")
    facts = _company_facts(cik)
    cols = {f: _field_series(facts, f) for f in SEC_FIELDS}
    df = pd.DataFrame(cols).sort_index().dropna(how="all")
    if df.empty:
        raise SystemExit(f"No SEC annual data returned for {ticker!r}.")
    df = df.join(_shares_frame(facts))
    df["fy_end"] = _fy_end_dates(facts)
    return df.tail(years)


def screen(ticker: str, years: int = YEARS) -> pd.DataFrame:
    """Fundamentals + ratios for the last `years` fiscal years.

    Fetches one extra year so ROA (average assets) is defined for the oldest row shown.
    """
    return add_ratios(fetch_annual(ticker, years + 1)).tail(years)


def add_ratios(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    rev = out["revenue"]
    book_equity = out["equity"].combine_first(out["total_assets"] - out["total_liabilities"])
    avg_assets = (out["total_assets"] + out["total_assets"].shift(1)) / 2

    out["gross_margin"] = (rev - out["cogs"]) / rev
    out["operating_margin"] = out["ebit"] / rev
    out["net_margin"] = out["net_income"] / rev
    out["roa"] = out["net_income"] / avg_assets
    out["roe"] = out["net_income"] / book_equity
    out["fcf"] = out["cfo"] - out["capex_ppe"]
    out["total_debt"] = out["long_term_debt"].fillna(0) + out["debt_current"].fillna(0)
    return out


def _ratio(num: float, den: float) -> float | None:
    if den is None or pd.isna(den) or den == 0:
        return None
    return num / den


def _multiples(mcap: float, fy: pd.Series) -> dict:
    """Valuation multiples from a market cap and one fiscal year of fundamentals."""
    equity = fy.get("equity")
    if equity is None or pd.isna(equity):
        equity = fy["total_assets"] - fy["total_liabilities"]
    cash = fy["cash"] if pd.notna(fy.get("cash")) else 0.0
    debt = fy["total_debt"] if pd.notna(fy.get("total_debt")) else 0.0
    ev = mcap + debt - cash
    return {
        "market_cap": mcap,
        "pe": _ratio(mcap, fy["net_income"]),
        "pb": _ratio(mcap, equity),
        "p_cf": _ratio(mcap, fy["cfo"]),
        "p_fcf": _ratio(mcap, fy["fcf"]),
        "ev": ev,
        "ev_to_sales": _ratio(ev, fy["revenue"]),
    }


def market_multiples(ticker: str, last: pd.Series) -> pd.DataFrame:
    """Today's market cap against the latest fiscal year."""
    import yfinance as yf

    info = yf.Ticker(ticker).info or {}
    mcap = info.get("marketCap")
    if not mcap:
        raise RuntimeError("yfinance returned no marketCap")
    price = info.get("currentPrice") or info.get("regularMarketPrice")
    row = {"price": price, "fy_label": int(last.name), **_multiples(float(mcap), last)}
    return pd.DataFrame([row])


def _tz_naive(s: pd.Series) -> pd.Series:
    if isinstance(s.index, pd.DatetimeIndex) and s.index.tz is not None:
        s = s.copy()
        s.index = s.index.tz_localize(None)
    return s


def historical_multiples(ticker: str, df: pd.DataFrame) -> pd.DataFrame:
    """Per fiscal year: close on the fiscal year-end date × SEC diluted shares.

    yfinance prices are split-adjusted to today's share basis; SEC share counts are on the
    basis of their filing date, so each count is scaled by the splits that happened after it
    was filed.
    """
    import yfinance as yf

    ends = df["fy_end"].dropna()
    if ends.empty:
        raise RuntimeError("SEC returned no fiscal year-end dates")
    t = yf.Ticker(ticker)
    hist = t.history(start=ends.min() - pd.Timedelta(days=10), auto_adjust=False)
    if hist.empty:
        raise RuntimeError("yfinance returned no price history")
    close = _tz_naive(hist["Close"])
    splits = _tz_naive(t.splits)

    rows = {}
    for fy, r in df.iterrows():
        end, shares, filed = r.get("fy_end"), r.get("shares_diluted"), r.get("shares_filed")
        if pd.isna(end) or pd.isna(shares):
            continue
        px = close.loc[:end]
        if px.empty:
            continue
        factor = 1.0
        if len(splits) and pd.notna(filed):
            factor = float(splits[splits.index > filed].prod())
        price = float(px.iloc[-1])
        rows[fy] = {"fy_end": end.date(), "price": price, **_multiples(price * shares * factor, r)}
    if not rows:
        raise RuntimeError("no fiscal year had both a share count and a price")
    out = pd.DataFrame.from_dict(rows, orient="index")
    out.index.name = df.index.name
    return out


def _fmt_pct_table(df: pd.DataFrame) -> pd.DataFrame:
    show = df.copy()
    for c in ("gross_margin", "operating_margin", "net_margin", "roa", "roe"):
        if c in show.columns:
            show[c] = (show[c] * 100).round(2)
    return show


def _print_metric_guide(help_map: dict[str, tuple[str, str]], keys: list[str]) -> None:
    print("  What each metric means:")
    for key in keys:
        if key not in help_map:
            continue
        title, blurb = help_map[key]
        print(f"    • {title} — {blurb}")
    print()


def _format_metric_value(key: str, value) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "n/a"
    if key in ("gross_margin", "operating_margin", "net_margin", "roa", "roe"):
        return f"{value * 100:.2f}%"
    if key in ("price",):
        return f"${value:,.2f}"
    if key in ("pe", "pb", "p_cf", "p_fcf", "ev_to_sales"):
        return f"{value:,.2f}×"
    if key in ("market_cap", "ev", "fcf", "total_debt") or key in SEC_FIELDS:
        return f"${value:,.0f}"
    return f"{value:,.2f}"


def _print_history_table(hist: pd.DataFrame) -> None:
    print("  Price = split-adjusted close on the fiscal year-end date; market cap = price × SEC")
    print("  diluted shares; denominators from that same fiscal year.\n")
    view = hist.copy()
    for col in view.columns:
        if col == "price":
            view[col] = view[col].map(lambda v: f"${v:,.2f}")
        elif col in ("market_cap", "ev"):
            view[col] = view[col].map(lambda v: f"${v / 1e9:,.0f}B" if pd.notna(v) else "n/a")
        elif col != "fy_end":
            view[col] = view[col].map(lambda v: f"{v:,.1f}×" if v is not None and pd.notna(v) else "n/a")
    print(view.rename(columns=HISTORY_LABELS).to_string())


def _print_valuation_block(row: pd.Series, fy: int) -> None:
    order = [
        "price",
        "market_cap",
        "pe",
        "pb",
        "p_cf",
        "p_fcf",
        "ev",
        "ev_to_sales",
    ]
    print(f"  Based on market data today and SEC fiscal year {fy} fundamentals.\n")
    for key in order:
        title, blurb = VALUATION_HELP[key]
        val = row.get(key)
        print(f"  {title}")
        print(f"    {blurb}")
        print(f"    Value: {_format_metric_value(key, val)}\n")


def main() -> None:
    args = parse_args(sys.argv[1:])
    for ticker in [s.upper() for s in args.symbols]:
        df = screen(ticker, args.years)
        last = df.iloc[-1]

        print(f"\n=== {ticker} — last {len(df)} fiscal years — SEC EDGAR ===")
        print("  Raw line items from annual 10-K XBRL (USD).\n")
        sec_view = df[SEC_FIELDS].round(2).rename(columns=SEC_LABELS)
        print(sec_view.to_string())

        ratio_keys = RATIO_COLS + ["total_debt"]
        print(f"\n=== {ticker} — profitability & cash flow (per fiscal year) ===")
        _print_metric_guide(RATIO_HELP, ratio_keys)
        ratio_view = _fmt_pct_table(df[ratio_keys])
        ratio_view = ratio_view.rename(
            columns={k: RATIO_HELP[k][0] for k in ratio_keys if k in RATIO_HELP}
        )
        for col in ratio_view.columns:
            if "FCF" in col or "debt" in col.lower():
                ratio_view[col] = ratio_view[col].map(
                    lambda x: f"${x:,.0f}" if pd.notna(x) else "n/a"
                )
            elif "%" in col:
                ratio_view[col] = ratio_view[col].map(
                    lambda x: f"{x:.2f}" if pd.notna(x) else "n/a"
                )
        print(ratio_view.to_string())

        if args.no_yfinance:
            print("\n(market multiples skipped: --no-yfinance)")
            continue

        try:
            hist = historical_multiples(ticker, df)
            print(f"\n=== {ticker} — valuation multiples per fiscal year ===")
            _print_history_table(hist)
        except Exception as exc:
            print(f"\n[yfinance] could not compute historical multiples: {exc}")

        try:
            m = market_multiples(ticker, last)
            row = m.iloc[0]
            print(f"\n=== {ticker} — valuation multiples today ===")
            _print_valuation_block(row, int(last.name))
        except Exception as exc:
            print(f"\n[yfinance] could not compute multiples: {exc}")


if __name__ == "__main__":
    main()
