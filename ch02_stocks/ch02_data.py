# -*- coding: utf-8 -*-
"""
ch02_data.py
============
Shared fundamentals data layer for Chapter 2 stock screens (and Ch. 3-style fields).

Two sources, one interface:

  * yfinance      -- free, no key, ~4 fiscal years of annual statements.
                     Good for the current snapshot, sector, price, dividends.
  * SEC EDGAR     -- free XBRL "companyfacts" API, history back to ~2009.
                     Needed for every 5-7 year average (SS3.3.2, SS3.4.1).
                     Requires a User-Agent: export SEC_USER_AGENT="Name email".

    annual(ticker, fields, source="auto")  -> DataFrame, index = fiscal year
    info(ticker)                           -> dict (sector, industry, country,
                                              marketCap, price, currency)

source="auto" uses EDGAR when SEC_USER_AGENT is set and the ticker is an SEC
filer, then fills any gaps from yfinance. Ticker "MOCK" returns an offline
fixture so every script can run `--selftest` with no network.

Sign convention (matches the book's FCF = CFO + CAPEX):
  outflows (capex_*, dividends_paid) are always NEGATIVE;
  interest_expense is always POSITIVE.

NOTE: yfinance row labels below come from Yahoo's current schema and can
change without notice -- print `yf.Ticker(t).balance_sheet.index` to check.
EDGAR tags are listed in priority order; companies switch tags over time
(e.g. InterestExpense -> InterestExpenseNonoperating), so the first tag that
has a value for a given year wins.
"""
from __future__ import annotations

import os
from functools import lru_cache

import pandas as pd

# --------------------------------------------------------------------------
# Field map: name -> (statement, yfinance labels, EDGAR tags)
# --------------------------------------------------------------------------
FIELDS: dict[str, tuple[str, list[str], list[str]]] = {
    # ---- Balance sheet (SS3.2.1) ----------------------------------------
    "total_assets": ("bs", ["Total Assets"],
                     ["us-gaap:Assets", "ifrs-full:Assets"]),
    "total_liabilities": ("bs", ["Total Liabilities Net Minority Interest"],
                          ["us-gaap:Liabilities", "ifrs-full:Liabilities"]),
    "equity": ("bs", ["Stockholders Equity", "Common Stock Equity"],
               ["us-gaap:StockholdersEquity",
                "ifrs-full:EquityAttributableToOwnersOfParent"]),
    "total_equity": ("bs", ["Total Equity Gross Minority Interest"],
                     ["us-gaap:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
                      "ifrs-full:Equity"]),
    "goodwill": ("bs", ["Goodwill"],
                 ["us-gaap:Goodwill", "ifrs-full:Goodwill"]),
    "other_intangibles": ("bs", ["Other Intangible Assets"],
                          ["us-gaap:IntangibleAssetsNetExcludingGoodwill",
                           "ifrs-full:IntangibleAssetsOtherThanGoodwill"]),
    "current_assets": ("bs", ["Current Assets"],
                       ["us-gaap:AssetsCurrent", "ifrs-full:CurrentAssets"]),
    "current_liabilities": ("bs", ["Current Liabilities"],
                            ["us-gaap:LiabilitiesCurrent",
                             "ifrs-full:CurrentLiabilities"]),
    "cash": ("bs", ["Cash And Cash Equivalents"],
             ["us-gaap:CashAndCashEquivalentsAtCarryingValue",
              "ifrs-full:CashAndCashEquivalents"]),
    "receivables": ("bs", ["Accounts Receivable", "Receivables"],
                    ["us-gaap:AccountsReceivableNetCurrent",
                     "ifrs-full:TradeAndOtherCurrentReceivables"]),
    "inventory": ("bs", ["Inventory"],
                  ["us-gaap:InventoryNet", "ifrs-full:Inventories"]),
    "payables": ("bs", ["Accounts Payable"],
                 ["us-gaap:AccountsPayableCurrent",
                  "ifrs-full:TradeAndOtherCurrentPayables"]),
    "trading_assets": ("bs", ["Trading Securities"],
                       ["us-gaap:TradingSecurities"]),
    # ---- Income statement (SS3.2.2) -------------------------------------
    "revenue": ("is", ["Total Revenue"],
                ["us-gaap:Revenues",
                 "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax",
                 "us-gaap:SalesRevenueNet", "ifrs-full:Revenue"]),
    "cogs": ("is", ["Cost Of Revenue"],
             ["us-gaap:CostOfRevenue", "us-gaap:CostOfGoodsAndServicesSold",
              "ifrs-full:CostOfSales"]),
    "operating_income": ("is", ["Operating Income"],
                         ["us-gaap:OperatingIncomeLoss",
                          "ifrs-full:ProfitLossFromOperatingActivities"]),
    # EDGAR has no single "EBIT" tag; operating income is the usual proxy.
    "ebit": ("is", ["EBIT"],
             ["us-gaap:OperatingIncomeLoss",
              "ifrs-full:ProfitLossFromOperatingActivities"]),
    "d_and_a": ("is", ["Reconciled Depreciation", "Depreciation And Amortization"],
                ["us-gaap:DepreciationDepletionAndAmortization",
                 "us-gaap:DepreciationAndAmortization",
                 "ifrs-full:DepreciationAndAmortisationExpense"]),
    "interest_expense": ("is", ["Interest Expense", "Interest Expense Non Operating"],
                         ["us-gaap:InterestExpense",
                          "us-gaap:InterestExpenseNonoperating",
                          "us-gaap:InterestExpenseDebt",
                          "ifrs-full:InterestExpense", "ifrs-full:FinanceCosts"]),
    "interest_income": ("is", ["Interest Income", "Interest Income Non Operating"],
                        ["us-gaap:InvestmentIncomeInterest",
                         "ifrs-full:FinanceIncome"]),
    "interest_capitalized": ("is", [], ["us-gaap:InterestCostsCapitalized"]),
    "net_income": ("is", ["Net Income", "Net Income Common Stockholders"],
                   ["us-gaap:NetIncomeLoss",
                    "ifrs-full:ProfitLossAttributableToOwnersOfParent"]),
    "unusual_items": ("is", ["Total Unusual Items"], []),
    "normalized_income": ("is", ["Normalized Income"], []),
    # ---- Cash flow statement (SS3.2.3) ----------------------------------
    "cfo": ("cf", ["Operating Cash Flow"],
            ["us-gaap:NetCashProvidedByUsedInOperatingActivities",
             "ifrs-full:CashFlowsFromUsedInOperatingActivities"]),
    "cfi": ("cf", ["Investing Cash Flow"],
            ["us-gaap:NetCashProvidedByUsedInInvestingActivities",
             "ifrs-full:CashFlowsFromUsedInInvestingActivities"]),
    "cff": ("cf", ["Financing Cash Flow"],
            ["us-gaap:NetCashProvidedByUsedInFinancingActivities",
             "ifrs-full:CashFlowsFromUsedInFinancingActivities"]),
    "capex_ppe": ("cf", ["Capital Expenditure", "Purchase Of PPE"],
                  ["us-gaap:PaymentsToAcquirePropertyPlantAndEquipment",
                   "ifrs-full:PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities"]),
    "capex_intangibles": ("cf", ["Purchase Of Intangibles"],
                          ["us-gaap:PaymentsToAcquireIntangibleAssets",
                           "ifrs-full:PurchaseOfIntangibleAssetsClassifiedAsInvestingActivities"]),
    "dividends_paid": ("cf", ["Cash Dividends Paid", "Common Stock Dividend Paid"],
                       ["us-gaap:PaymentsOfDividends",
                        "us-gaap:PaymentsOfDividendsCommonStock",
                        "ifrs-full:DividendsPaidClassifiedAsFinancingActivities"]),
    # ---- Bank regulatory ratios (SS3.5.1) -- tagged by SOME US banks only.
    # Tag names: verify against the filer's XBRL before relying on them.
    "cet1_ratio": ("bs", [],
                   ["us-gaap:CommonEquityTierOneCapitalRatio",
                    "us-gaap:CommonEquityTierOneCapitalToRiskWeightedAssets"]),
    "tier1_ratio": ("bs", [],
                    ["us-gaap:TierOneRiskBasedCapitalToRiskWeightedAssets"]),
}

OUTFLOWS = {"capex_ppe", "capex_intangibles", "dividends_paid"}
POSITIVE = {"interest_expense", "interest_capitalized", "d_and_a"}


# --------------------------------------------------------------------------
# Offline fixture -- ticker "MOCK" (8 fiscal years, a sound mid-cap)
# --------------------------------------------------------------------------
def _mock_annual() -> pd.DataFrame:
    years = list(range(2018, 2026))
    g = [1.00, 1.04, 0.97, 1.06, 1.10, 1.13, 1.17, 1.20]   # growth path
    df = pd.DataFrame(index=years, dtype=float)
    df["revenue"] = [10_000 * x for x in g]
    df["cogs"] = df["revenue"] * 0.60
    df["operating_income"] = df["revenue"] * 0.15
    df["ebit"] = df["operating_income"]
    df["d_and_a"] = df["revenue"] * 0.04
    df["interest_expense"] = [300, 300, 320, 310, 300, 290, 280, 270]
    df["interest_income"] = 20.0
    df["interest_capitalized"] = 15.0
    df["net_income"] = (df["ebit"] - df["interest_expense"]) * 0.75
    df["unusual_items"] = [0, -50, -120, 0, 0, -30, 0, 0]
    df["normalized_income"] = df["net_income"] - df["unusual_items"] * 0.75
    df["cfo"] = df["net_income"] * 1.25
    df["capex_ppe"] = -df["revenue"] * 0.045
    df["capex_intangibles"] = -df["revenue"] * 0.005
    df["cfi"] = df["capex_ppe"] + df["capex_intangibles"] - 50
    df["dividends_paid"] = -df["net_income"] * 0.45
    df["cff"] = df["dividends_paid"] - 200
    df["total_assets"] = df["revenue"] * 1.5
    df["goodwill"] = df["revenue"] * 0.20
    df["other_intangibles"] = df["revenue"] * 0.05
    df["total_liabilities"] = (df["total_assets"]
                               - df["goodwill"] - df["other_intangibles"]) * 0.50
    df["total_equity"] = df["total_assets"] - df["total_liabilities"]
    df["equity"] = df["total_equity"] - 50
    df["current_assets"] = df["revenue"] * 0.45
    df["current_liabilities"] = df["revenue"] * 0.28
    df["cash"] = df["revenue"] * 0.10
    df["receivables"] = df["revenue"] * 0.15
    df["inventory"] = df["revenue"] * 0.12
    df["payables"] = df["revenue"] * 0.10
    df["trading_assets"] = float("nan")
    df["cet1_ratio"] = float("nan")
    df["tier1_ratio"] = float("nan")
    return df


MOCK_INFO = {"sector": "Consumer Defensive", "industry": "Beverages",
             "country": "United States", "marketCap": 14_000.0,
             "price": 70.0, "currency": "USD", "longName": "Mock Corp"}


# --------------------------------------------------------------------------
# yfinance
# --------------------------------------------------------------------------
@lru_cache(maxsize=32)
def _yf_statements(ticker: str) -> dict[str, pd.DataFrame]:
    import yfinance as yf
    t = yf.Ticker(ticker)
    return {"bs": t.balance_sheet, "is": t.income_stmt, "cf": t.cashflow}


def _yf_series(ticker: str, field: str) -> pd.Series:
    stmt, labels, _ = FIELDS[field]
    df = _yf_statements(ticker).get(stmt)
    if df is None or df.empty:
        return pd.Series(dtype=float)
    for lab in labels:
        if lab in df.index:
            s = df.loc[lab].dropna().astype(float)
            s.index = pd.to_datetime(s.index).year
            return s.groupby(level=0).last()
    return pd.Series(dtype=float)


# --------------------------------------------------------------------------
# SEC EDGAR (XBRL companyfacts)
# --------------------------------------------------------------------------
def _sec_get(url: str) -> dict:
    ua = os.getenv("SEC_USER_AGENT")
    if not ua:
        raise RuntimeError('SEC requires a User-Agent: '
                           'export SEC_USER_AGENT="Your Name your@email"')
    import requests
    r = requests.get(url, headers={"User-Agent": ua}, timeout=30)
    r.raise_for_status()
    return r.json()


@lru_cache(maxsize=1)
def _sec_ticker_map() -> dict[str, int]:
    data = _sec_get("https://www.sec.gov/files/company_tickers.json")
    return {row["ticker"].upper(): int(row["cik_str"]) for row in data.values()}


def cik_for(ticker: str) -> int | None:
    return _sec_ticker_map().get(ticker.upper())


@lru_cache(maxsize=32)
def company_facts(cik: int) -> dict:
    return _sec_get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json")


def _edgar_tag(facts: dict, qtag: str) -> pd.Series:
    """One XBRL tag -> Series indexed by fiscal-year-end year (annual filings)."""
    tax, tag = qtag.split(":")
    node = facts.get("facts", {}).get(tax, {}).get(tag)
    if not node:
        return pd.Series(dtype=float)
    units = node["units"]
    unit = "USD" if "USD" in units else next(
        (u for u in units if "/" not in u), None)          # EUR, pure, ...
    if unit is None:
        return pd.Series(dtype=float)
    rows = []
    for f in units[unit]:
        if not str(f.get("form", "")).startswith(("10-K", "20-F", "40-F")):
            continue
        end = pd.Timestamp(f["end"])
        if "start" in f:                                   # duration fact
            days = (end - pd.Timestamp(f["start"])).days
            if not 350 <= days <= 380:                     # keep full years only
                continue
        rows.append((end, f.get("filed", ""), float(f["val"])))
    if not rows:
        return pd.Series(dtype=float)
    df = (pd.DataFrame(rows, columns=["end", "filed", "val"])
          .sort_values("filed")
          .drop_duplicates("end", keep="last"))            # latest restatement wins
    s = df.set_index(df["end"].dt.year)["val"]
    return s.groupby(level=0).last()


def _edgar_series(ticker: str, field: str) -> pd.Series:
    cik = cik_for(ticker)
    if cik is None:
        return pd.Series(dtype=float)
    facts = company_facts(cik)
    out = pd.Series(dtype=float)
    for qtag in FIELDS[field][2]:                          # priority order
        out = out.combine_first(_edgar_tag(facts, qtag))
    return out


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------
def _normalise(field: str, s: pd.Series) -> pd.Series:
    if field in OUTFLOWS:
        return -s.abs()
    if field in POSITIVE:
        return s.abs()
    return s


def annual(ticker: str, fields: list[str], source: str = "auto") -> pd.DataFrame:
    """Annual values for `fields`, index = fiscal-year-end year (ascending)."""
    if ticker.upper() == "MOCK":
        return _mock_annual()[fields].copy()
    use_edgar = source in ("edgar", "auto") and bool(os.getenv("SEC_USER_AGENT"))
    if source == "edgar" and not use_edgar:
        raise RuntimeError("source='edgar' needs SEC_USER_AGENT to be set")
    cols = {}
    for f in fields:
        s = pd.Series(dtype=float)
        if use_edgar:
            try:
                s = _edgar_series(ticker, f)
            except Exception as exc:                       # network / not a filer
                print(f"[edgar] {f}: {exc}")
        if source in ("yf", "auto"):
            try:
                s = s.combine_first(_yf_series(ticker, f))
            except Exception as exc:
                print(f"[yfinance] {f}: {exc}")
        cols[f] = _normalise(f, s)
    return pd.DataFrame(cols).sort_index()


def info(ticker: str) -> dict:
    if ticker.upper() == "MOCK":
        return dict(MOCK_INFO)
    import yfinance as yf
    i = yf.Ticker(ticker).info or {}
    return {"sector": i.get("sector"), "industry": i.get("industry"),
            "country": i.get("country"), "marketCap": i.get("marketCap"),
            "price": i.get("currentPrice") or i.get("regularMarketPrice"),
            "currency": i.get("financialCurrency") or i.get("currency"),
            "longName": i.get("longName")}


def window(df: pd.DataFrame, years: int) -> pd.DataFrame:
    """Last `years` fiscal years that have no missing values."""
    return df.dropna().tail(years)


# --------------------------------------------------------------------------
# Small CLI / print helpers shared by the scripts
# --------------------------------------------------------------------------
def cli(description: str):
    import argparse
    p = argparse.ArgumentParser(description=description)
    p.add_argument("ticker", nargs="?", default="MOCK",
                   help="e.g. KO, AAPL, MC.PA (default: offline MOCK)")
    p.add_argument("--source", choices=["auto", "yf", "edgar"], default="auto")
    p.add_argument("--selftest", action="store_true",
                   help="run offline checks on the MOCK fixture and exit")
    return p


def fmt(x, pct: bool = False, mult: bool = False) -> str:
    if x is None or pd.isna(x):
        return "n/a"
    if pct:
        return f"{x:.1%}"
    if mult:
        return f"{x:.2f}x"
    return f"{x:,.0f}"


def verdict(ok: bool | None) -> str:
    return {True: "PASS", False: "FAIL", None: "N/A"}[ok]


def warn_depth(df: pd.DataFrame, need: int) -> None:
    n = len(df.dropna())
    if n < need:
        print(f"! only {n} complete fiscal years (need {need}). yfinance gives ~4; "
              "set SEC_USER_AGENT for EDGAR history (US/SEC filers), or "
              "collect older annual reports by hand.")
