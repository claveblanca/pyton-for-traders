"""ch02_stock_screen.py — Chapter 2 Hands-On: SEC fundamentals, ratios, and market multiples.

Self-contained SEC XBRL (companyfacts) plus optional yfinance for current valuation multiples.

Requires:
    export SEC_USER_AGENT="Your Name you@email.com"
    pip install pandas requests
    pip install yfinance   # for P/E, P/B, EV/Sales, etc. (skip with --no-yfinance)

Run from the repo root:
    python ch02_stock_screen.py              # default AAPL
    python ch02_stock_screen.py NVDA MSFT
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


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("symbols", nargs="*", default=["AAPL"], help="tickers (default AAPL)")
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


def _tag_series(facts: dict, qtag: str) -> pd.Series:
    tax, tag = qtag.split(":")
    node = facts.get("facts", {}).get(tax, {}).get(tag)
    if not node:
        return pd.Series(dtype=float)
    units = node["units"]
    unit = "USD" if "USD" in units else next((u for u in units if "/" not in u), None)
    if unit is None:
        return pd.Series(dtype=float)
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
        return pd.Series(dtype=float)
    df = (
        pd.DataFrame(rows, columns=["end", "filed", "val"])
        .sort_values("filed")
        .drop_duplicates("end", keep="last")
    )
    s = df.set_index(df["end"].dt.year)["val"]
    return s.groupby(level=0).last()


def _field_series(facts: dict, field: str) -> pd.Series:
    out = pd.Series(dtype=float)
    for qtag in EDGAR_TAGS[field]:
        out = out.combine_first(_tag_series(facts, qtag))
    if field == "interest_expense":
        out = out.abs()
    if field == "capex_ppe":
        out = out.abs()
    return out


def fetch_annual(ticker: str) -> pd.DataFrame:
    cik = _ticker_cik_map().get(ticker.upper())
    if cik is None:
        raise SystemExit(f"{ticker!r} is not in SEC company_tickers (US filer only).")
    facts = _company_facts(cik)
    cols = {f: _field_series(facts, f) for f in SEC_FIELDS}
    df = pd.DataFrame(cols).sort_index().dropna(how="all")
    if df.empty:
        raise SystemExit(f"No SEC annual data returned for {ticker!r}.")
    return df.tail(YEARS)


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


def market_multiples(ticker: str, last: pd.Series) -> pd.DataFrame:
    import yfinance as yf

    info = yf.Ticker(ticker).info or {}
    mcap = info.get("marketCap")
    if not mcap:
        raise RuntimeError("yfinance returned no marketCap")
    price = info.get("currentPrice") or info.get("regularMarketPrice")

    equity = last.get("equity") or (last["total_assets"] - last["total_liabilities"])
    ni, cfo, fcf, rev = last["net_income"], last["cfo"], last["fcf"], last["revenue"]
    cash = last["cash"] if pd.notna(last.get("cash")) else 0.0
    debt = last["total_debt"] if pd.notna(last.get("total_debt")) else 0.0
    ev = mcap + debt - cash

    def ratio(num: float, den: float) -> float | None:
        if den is None or pd.isna(den) or den == 0:
            return None
        return num / den

    row = {
        "price": price,
        "market_cap": mcap,
        "fy_label": int(last.name),
        "pe": ratio(mcap, ni),
        "pb": ratio(mcap, equity),
        "p_cf": ratio(mcap, cfo),
        "p_fcf": ratio(mcap, fcf),
        "ev": ev,
        "ev_to_sales": ratio(ev, rev),
    }
    return pd.DataFrame([row])


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
        df = add_ratios(fetch_annual(ticker))
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
            m = market_multiples(ticker, last)
            row = m.iloc[0]
            print(f"\n=== {ticker} — valuation multiples ===")
            _print_valuation_block(row, int(last.name))
        except Exception as exc:
            print(f"\n[yfinance] could not compute multiples: {exc}")


if __name__ == "__main__":
    main()
