#!/usr/bin/env python3
"""
MCP server for python_for_traders datacollect APIs (investing + crypto).

Run (stdio, for Cursor):
  pip install -r mcp/requirements.txt
  INVESTING_API_BASE=http://127.0.0.1:5001 CRYPTO_API_BASE=http://127.0.0.1:5000 \\
    python mcp/server.py

See mcp/cursor-mcp.example.json for Cursor configuration.
"""

from __future__ import annotations

from _sdk import load_mcpserver
from api_client import backend_health, crypto_get, investing_get
from doc_search import list_doc_sources, search_docs

MCPServer = load_mcpserver()
mcp = MCPServer(
    "trading-datacollect",
    instructions=(
        "Tools call the local datacollect Flask backends: investing on port 5001 "
        "(stocks, Ch03 financials, macro) and crypto on port 5000 (Kraken OHLC, "
        "indicators, signals). Use investing_* for equities and crypto_* for pairs "
        "like XXBTZUSD. Use explain_metric for definitions from mcp/docs Markdown."
    ),
)


def _symbols_param(symbols: str | None) -> str | None:
    if symbols is None or not str(symbols).strip():
        return None
    return str(symbols).strip()


# ─── Combined health ─────────────────────────────────────────────────────────


@mcp.tool()
def datacollect_health() -> dict:
    """Check /health on both investing (5001) and crypto (5000) backends."""
    return backend_health()


# ─── Investing (port 5001, no /api prefix) ───────────────────────────────────


@mcp.tool()
def investing_health() -> dict:
    """Investing backend health (Chapter 3, prices, macro, universe)."""
    return investing_get("/health")


@mcp.tool()
def investing_list_symbols(sector_group: str | None = None) -> dict:
    """
    List tradable symbols from sector_symbols.
    Optional sector_group filters via /symbols/<sector_group>; omit for all /symbols.
    """
    if sector_group and sector_group.strip():
        return investing_get(f"/symbols/{sector_group.strip()}")
    return investing_get("/symbols")


@mcp.tool()
def investing_list_sectors() -> dict:
    """Sector groups for the investing universe."""
    return investing_get("/sectors")


@mcp.tool()
def investing_ch03_universe(
    symbols: str | None = None,
    data_source: str = "mixed",
    fiscal_year: int | None = None,
) -> dict:
    """
    Merged Ch03 universe table (§3.2 statements + §3.3–3.5 filters).
    symbols: comma-separated tickers, e.g. AAPL,MSFT
    """
    return investing_get(
        "/financial-ch03/universe",
        symbols=_symbols_param(symbols),
        data_source=data_source or None,
        fiscal_year=fiscal_year,
    )


@mcp.tool()
def investing_ch03_screen(
    symbols: str | None = None,
    data_source: str | None = None,
    limit: int = 500,
) -> dict:
    """Latest Ch03 §3.3–3.5 screen snapshot rows."""
    return investing_get(
        "/financial-ch03/screen",
        symbols=_symbols_param(symbols),
        data_source=data_source,
        limit=limit,
    )


@mcp.tool()
def investing_ch03_filter_annual(
    symbols: str | None = None,
    data_source: str | None = None,
    fiscal_year_min: int | None = None,
    limit: int = 500,
) -> dict:
    """Annual Ch03 filter metrics (debt, interest coverage, CFI, etc.)."""
    return investing_get(
        "/financial-ch03/filter-annual",
        symbols=_symbols_param(symbols),
        data_source=data_source,
        fiscal_year_min=fiscal_year_min,
        limit=limit,
    )


@mcp.tool()
def investing_balance_sheet(
    symbols: str | None = None,
    data_source: str | None = None,
    fiscal_year_min: int | None = None,
    limit: int = 200,
) -> dict:
    """Annual balance sheet rows (Ch03 §3.2)."""
    return investing_get(
        "/financial-statements/balance-sheet",
        symbols=_symbols_param(symbols),
        data_source=data_source,
        fiscal_year_min=fiscal_year_min,
        limit=limit,
    )


@mcp.tool()
def investing_income_statement(
    symbols: str | None = None,
    data_source: str | None = None,
    fiscal_year_min: int | None = None,
    limit: int = 200,
) -> dict:
    """Annual income statement rows (Ch03 §3.2)."""
    return investing_get(
        "/financial-statements/income",
        symbols=_symbols_param(symbols),
        data_source=data_source,
        fiscal_year_min=fiscal_year_min,
        limit=limit,
    )


@mcp.tool()
def investing_cash_flow(
    symbols: str | None = None,
    data_source: str | None = None,
    fiscal_year_min: int | None = None,
    limit: int = 200,
) -> dict:
    """Annual cash flow rows (Ch03 §3.2)."""
    return investing_get(
        "/financial-statements/cash-flow",
        symbols=_symbols_param(symbols),
        data_source=data_source,
        fiscal_year_min=fiscal_year_min,
        limit=limit,
    )


@mcp.tool()
def investing_stock_prices(symbol: str, days: int = 90) -> dict:
    """Daily OHLCV for a stock symbol from yfinance-backed prices table."""
    return investing_get(f"/prices/{symbol.strip()}", days=days)


@mcp.tool()
def investing_macro(series_id: str | None = None) -> dict:
    """FRED macro series list or one series by id (/macro or /macro/<series_id>)."""
    if series_id and series_id.strip():
        return investing_get(f"/macro/{series_id.strip()}")
    return investing_get("/macro")


# ─── Crypto (port 5000, /api/* routes) ─────────────────────────────────────────


@mcp.tool()
def crypto_health() -> dict:
    """Crypto / Kraken datacollect backend health."""
    return crypto_get("/health")


@mcp.tool()
def crypto_list_pairs() -> dict:
    """Available Kraken pairs from /api/config/pairs."""
    return crypto_get("/api/config/pairs")


@mcp.tool()
def crypto_ticker(pair: str, limit: int = 50) -> dict:
    """Recent ticker snapshots for a pair (default Kraken pair if omitted in API)."""
    return crypto_get("/api/ticker", pair=pair.upper(), limit=limit)


@mcp.tool()
def crypto_ohlc(pair: str, limit: int = 50) -> dict:
    """Intraday OHLC bars from DB (/api/ohlc)."""
    return crypto_get("/api/ohlc", pair=pair.upper(), limit=limit)


@mcp.tool()
def crypto_ohlc_daily(pair: str, days: int = 90) -> dict:
    """Daily OHLC bars (/api/ohlc-daily). days=0 returns all stored history."""
    return crypto_get("/api/ohlc-daily", pair=pair.upper(), days=days)


@mcp.tool()
def crypto_rsi(
    pair: str,
    timeframe: str = "daily",
    days: int = 90,
    warmup: bool = False,
) -> dict:
    """
    Enriched RSI + ADX regime (/api/indicators/rsi).
    timeframe: daily | 4h | 1h
    """
    return crypto_get(
        "/api/indicators/rsi",
        pair=pair.upper(),
        timeframe=timeframe,
        days=days,
        warmup=str(warmup).lower(),
    )


@mcp.tool()
def crypto_macd(pair: str, timeframe: str = "daily", days: int = 90) -> dict:
    """MACD indicator (/api/indicators/macd). timeframe: daily | 4h | 1h"""
    return crypto_get(
        "/api/indicators/macd",
        pair=pair.upper(),
        timeframe=timeframe,
        days=days,
    )


@mcp.tool()
def crypto_obv(pair: str, days: int = 90) -> dict:
    """On-Balance Volume daily series (/api/indicators/obv)."""
    return crypto_get("/api/indicators/obv", pair=pair.upper(), days=days)


@mcp.tool()
def crypto_volume_stats(pair: str, days: int = 90) -> dict:
    """ADTV and volume z-score (/api/indicators/volume)."""
    return crypto_get("/api/indicators/volume", pair=pair.upper(), days=days)


@mcp.tool()
def crypto_volume_screener(days: int = 30) -> dict:
    """Cross-pair volume screener (/api/indicators/volume-screener)."""
    return crypto_get("/api/indicators/volume-screener", days=days)


@mcp.tool()
def crypto_signals(pair: str = "all", days: int = 90) -> dict:
    """
    Strategy signals from DB indicators (/api/signals).
    pair: Kraken pair or 'all' for every configured pair.
    """
    return crypto_get("/api/signals", pair=pair.upper(), days=days)


# ─── Documentation ───────────────────────────────────────────────────────────


@mcp.tool()
def explain_metric(query: str, domain: str = "any") -> str:
    """
    Search mcp/docs Markdown for metric definitions (partI-investing, partII-technical-analysis).
    domain: investing | crypto | any
    Examples: debt ratio, interest coverage, RSI, OBV, CAPE.
    """
    return search_docs(query, domain=domain)


@mcp.tool()
def list_metric_doc_paths(domain: str = "any") -> str:
    """List Markdown files searched by explain_metric."""
    return list_doc_sources(domain=domain)


if __name__ == "__main__":
    mcp.run()
