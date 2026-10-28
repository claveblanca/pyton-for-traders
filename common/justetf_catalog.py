"""ETF catalogs from the justETF screener (all funds, one venue, or one provider)."""
from __future__ import annotations

import re
from typing import Any, Literal

import pandas as pd

HedgeFilter = Literal["any", "hedged", "unhedged"]

from common.justetf_listings import listing_target
from common.justetf_screener import _MIC_COUNTRY, screener_rows

_STRATEGIES = ("epg-longOnly", "epg-activeEtfs")
_AMUNDI = "Amundi ETF"


def parse_fund_currency(raw: str | None) -> tuple[str | None, bool]:
    """justETF fundCurrency → (base currency label, currency-hedged share class)."""
    if not raw or raw in ("-", ""):
        return None, False
    s = str(raw).replace("<br />", " ").strip()
    hedged = bool(re.search(r"\bhedged\b", s, re.I))
    currency = re.sub(r"\s+Hedged\s*$", "", s, flags=re.I).strip() or None
    return currency, hedged


def filter_by_hedge(df: pd.DataFrame, hedge: HedgeFilter) -> pd.DataFrame:
    if hedge == "any" or df.empty or "hedged" not in df.columns:
        return df
    mask = df["hedged"] if hedge == "hedged" else ~df["hedged"]
    return df.loc[mask].reset_index(drop=True)


def parse_ter(raw: str | None) -> float | None:
    if not raw or raw in ("-", ""):
        return None
    s = str(raw).strip().removesuffix("%").replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def _merge_screener_rows(
    *,
    mic: str,
    country: str,
    provider: str | None,
    include_active: bool,
) -> dict[str, dict[str, Any]]:
    strategies = list(_STRATEGIES if include_active else _STRATEGIES[:1])
    by_isin: dict[str, dict[str, Any]] = {}
    for strategy in strategies:
        params = f"search=ETF&productGroup={strategy}&ls={mic}&instrumentType=ETF"
        if provider:
            params += f"&ic={provider}"
        for row in screener_rows(params, country=country):
            by_isin.setdefault(row["isin"], row)
    return by_isin


def _rows_to_frame(by_isin: dict[str, dict[str, Any]], suffix: str) -> pd.DataFrame:
    rows = []
    for isin, row in sorted(by_isin.items()):
        ticker = (row.get("ticker") or "").strip()
        if not ticker:
            continue
        t = ticker.upper()
        yahoo = t if "." in t else f"{t}{suffix}"
        currency, hedged = parse_fund_currency(row.get("fundCurrency"))
        rows.append(
            {
                "yahoo": yahoo,
                "isin": isin,
                "screener": ticker,
                "ter": parse_ter(row.get("ter")),
                "currency": currency,
                "hedged": hedged,
                "name": (row.get("name") or "").replace("<br />", " ").strip(),
                "note": "",
            }
        )
    return pd.DataFrame(rows)


def etfs_on_listing(
    listing: str,
    *,
    provider: str | None = None,
    include_active: bool = True,
    hedge: HedgeFilter = "any",
) -> pd.DataFrame:
    """All ETFs (optionally one provider) tradable on a venue — one screener query per strategy."""
    mic, suffix = listing_target(listing)
    if not mic:
        raise ValueError(
            f"Listing {listing!r} has no exchange code for bulk fetch; use PA, DE, MI, L, AS, …"
        )
    country = _MIC_COUNTRY.get(mic, "DE")
    by_isin = _merge_screener_rows(
        mic=mic, country=country, provider=provider, include_active=include_active
    )
    frame = filter_by_hedge(_rows_to_frame(by_isin, suffix), hedge)
    if not frame.empty and "ter" in frame.columns:
        frame = frame.sort_values("ter", ascending=True, na_position="last").reset_index(drop=True)
    return frame


def all_etfs(*, include_active: bool = True) -> pd.DataFrame:
    """All long-only (+ optional active) ETFs on justETF (German screener tickers)."""
    by_isin: dict[str, dict[str, Any]] = {}
    for strategy in _STRATEGIES if include_active else _STRATEGIES[:1]:
        params = f"search=ETF&productGroup={strategy}&ls=any&instrumentType=ETF"
        for row in screener_rows(params, country="DE"):
            by_isin.setdefault(row["isin"], row)
    rows = []
    for isin, row in sorted(by_isin.items()):
        ticker = (row.get("ticker") or "").strip()
        if not ticker:
            continue
        rows.append(
            {
                "isin": isin,
                "name": (row.get("name") or "").replace("<br />", " ").strip(),
                "ticker": ticker,
                "ter": parse_ter(row.get("ter")),
            }
        )
    return pd.DataFrame(rows)


def amundi_etfs(*, include_active: bool = True, hedge: HedgeFilter = "any") -> pd.DataFrame:
    """All Amundi ETFs on justETF (DE screener tickers, any exchange filter)."""
    by_isin: dict[str, dict[str, Any]] = {}
    for strategy in _STRATEGIES if include_active else _STRATEGIES[:1]:
        params = f"search=ETF&productGroup={strategy}&ls=any&instrumentType=ETF&ic={_AMUNDI}"
        for row in screener_rows(params, country="DE"):
            by_isin.setdefault(row["isin"], row)
    rows = []
    for isin, row in sorted(by_isin.items()):
        ticker = (row.get("ticker") or "").strip()
        if not ticker:
            continue
        currency, hedged = parse_fund_currency(row.get("fundCurrency"))
        rows.append(
            {
                "isin": isin,
                "name": (row.get("name") or "").replace("<br />", " ").strip(),
                "ticker": ticker,
                "ter": parse_ter(row.get("ter")),
                "currency": currency,
                "hedged": hedged,
            }
        )
    return filter_by_hedge(pd.DataFrame(rows), hedge)


def demo_list_by_listing(listing: str, *, hedge: HedgeFilter = "any") -> pd.DataFrame:
    """Offline sample for --list-by-listing --demo."""
    from common.justetf_listings import yahoo_symbol_for_listing

    catalog = demo_amundi_etfs()
    out = []
    for _, row in catalog.iterrows():
        yahoo, note = yahoo_symbol_for_listing(
            str(row["isin"]), str(row["ticker"]), listing, demo=True
        )
        if not yahoo:
            continue
        out.append(
            {
                "yahoo": yahoo,
                "isin": row["isin"],
                "screener": row["ticker"],
                "ter": row["ter"],
                "currency": row.get("currency"),
                "hedged": bool(row.get("hedged")),
                "name": row["name"],
                "note": note,
            }
        )
    return filter_by_hedge(pd.DataFrame(out), hedge)


def demo_amundi_etfs() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "isin": "IE00B5BMR087",
                "name": "Amundi S&P 500 UCITS ETF Acc",
                "ticker": "CSPX",
                "ter": 0.07,
                "currency": "EUR",
                "hedged": False,
            },
            {
                "isin": "LU1681043599",
                "name": "Amundi MSCI World UCITS ETF Acc",
                "ticker": "AMEW",
                "ter": 0.38,
                "currency": "EUR",
                "hedged": False,
            },
        ]
    )
