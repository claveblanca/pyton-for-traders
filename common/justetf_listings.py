"""Exchange listings for an ETF ISIN — Yahoo ticker mapping via justETF screener."""
from __future__ import annotations

from dataclasses import dataclass

from common.justetf_screener import isin_ticker_at_mic

# Primary venues for --list-by-listing (justETF ls=MIC) and --list-exchanges
@dataclass(frozen=True)
class Exchange:
    mic: str
    name: str
    yahoo_suffix: str
    screener_country: str
    listing_aliases: tuple[str, ...]


_EXCHANGES: tuple[Exchange, ...] = (
    Exchange("XPAR", "Euronext Paris", ".PA", "FR", ("PA", ".PA", "PAR", "Paris")),
    Exchange("XETR", "Xetra", ".DE", "DE", ("DE", ".DE", "Xetra")),
    Exchange("MUND", "gettex", ".DE", "DE", ("gettex",)),
    Exchange("XLON", "London Stock Exchange", ".L", "GB", ("L", ".L", "LSE", "Lon")),
    Exchange("XAMS", "Euronext Amsterdam", ".AS", "NL", ("AS", ".AS", "Ams")),
    Exchange("XMIL", "Borsa Italiana", ".MI", "IT", ("MI", ".MI")),
    Exchange("XSWX", "SIX Swiss Exchange", ".SW", "CH", ("SW", ".SW")),
    Exchange("XMAD", "Bolsa de Madrid", ".MC", "ES", ("MC", ".MC")),
    Exchange("XBRU", "Euronext Brussels", ".BR", "BE", (".BR",)),
    Exchange("XWBO", "Wiener Börse", ".VI", "AT", (".VI",)),
)


def available_exchanges() -> tuple[Exchange, ...]:
    """Venues supported for --listing and --list-by-listing."""
    return _EXCHANGES

# MIC (justETF row id) -> Yahoo Finance suffix
_MIC_YAHOO: dict[str, str] = {
    "XPAR": ".PA",
    "XETR": ".DE",
    "XETRA": ".DE",
    "MUND": ".DE",
    "XSTU": ".DE",
    "XLON": ".L",
    "XAMS": ".AS",
    "XMIL": ".MI",
    "XSWX": ".SW",
    "XBRU": ".BR",
    "XMAD": ".MC",
    "XWBO": ".VI",
    "XETB": ".DE",
}

# CLI --listing values -> MIC
_LISTING_MIC: dict[str, str] = {
    "pa": "XPAR",
    ".pa": "XPAR",
    "par": "XPAR",
    "paris": "XPAR",
    "xpar": "XPAR",
    "de": "XETR",
    ".de": "XETR",
    "xetra": "XETR",
    "gettex": "MUND",
    "l": "XLON",
    ".l": "XLON",
    "lon": "XLON",
    "lse": "XLON",
    "as": "XAMS",
    ".as": "XAMS",
    "ams": "XAMS",
    "mi": "XMIL",
    ".mi": "XMIL",
    "sw": "XSWX",
    ".sw": "XSWX",
}

# Offline demo: ISIN -> Yahoo symbol per MIC
_DEMO_YAHOO: dict[str, dict[str, str]] = {
    "IE00B5BMR087": {"XETR": "CSPX.DE", "XLON": "CSPX.L", "XPAR": "CSPX.PA"},
    "LU1681043599": {"XETR": "AMEW.DE", "XPAR": "CW8.PA"},
}


@dataclass(frozen=True)
class Listing:
    mic: str
    exchange: str
    ticker: str | None
    currency: str | None = None


def listing_target(listing: str) -> tuple[str, str]:
    """Map --listing to (MIC, Yahoo suffix). Unknown listings pass through as suffix-only."""
    key = listing.strip().lower()
    if key in _LISTING_MIC:
        mic = _LISTING_MIC[key]
        return mic, _MIC_YAHOO[mic]
    suffix = listing if listing.startswith(".") else f".{listing}"
    mic = next((m for m, s in _MIC_YAHOO.items() if s.lower() == suffix.lower()), "")
    return mic, suffix


def yahoo_symbol_for_listing(
    isin: str,
    screener_ticker: str,
    listing: str,
    *,
    demo: bool = False,
) -> tuple[str, str]:
    """Return (Yahoo symbol, note) using justETF venue tickers from the screener."""
    mic, suffix = listing_target(listing)
    if demo:
        sym = _DEMO_YAHOO.get(isin, {}).get(mic or "")
        if sym:
            return sym, ""
        t = screener_ticker.strip().upper()
        if "." in t:
            return t, ""
        return f"{t}{suffix}", ""

    t = screener_ticker.strip().upper()
    if "." in t:
        return t, ""

    if mic:
        venue_ticker = isin_ticker_at_mic(isin, mic)
        if venue_ticker:
            return f"{venue_ticker.upper()}{suffix}", ""
        venue = {"XPAR": "Paris", "XETR": "Xetra", "XLON": "London"}.get(mic, mic)
        if mic == "XPAR":
            return "", f"no {venue} listing"
        return f"{t}{suffix}", f"screener ticker (no {venue} row)"

    return f"{t}{suffix}", ""
