"""justETF screener AJAX (search.html) — avoids etf-profile.html (often 403)."""
from __future__ import annotations

import re
import warnings
from functools import lru_cache
from typing import Any

import requests

_SEARCH_URL = "https://www.justetf.com/en/search.html"
_WICKET = re.compile(
    r"(\d)-1.0-container-tabsContentContainer-tabsContentRepeater-1-container-content-etfsTablePanel&search=ETFS&_wicket=1"
)
_BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

# justETF screener `country` field → venue-specific ticker in results
_MIC_COUNTRY: dict[str, str] = {
    "XPAR": "FR",
    "XETR": "DE",
    "MUND": "DE",
    "XSTU": "DE",
    "XETB": "DE",
    "XLON": "GB",
    "XAMS": "NL",
    "XMIL": "IT",
    "XSWX": "CH",
    "XMAD": "ES",
    "XBRU": "BE",
    "XWBO": "AT",
}

_session: requests.Session | None = None
_counter: int | None = None


def reset_screener_session() -> None:
    global _session, _counter
    _session = _counter = None


def _ensure_session() -> tuple[requests.Session, int]:
    global _session, _counter
    if _session is None or _counter is None:
        _session = requests.Session()
        _session.headers.update(
            {
                "User-Agent": _BROWSER_UA,
                "Accept-Language": "en-GB,en;q=0.9",
            }
        )
        html = _session.get(f"{_SEARCH_URL}?search=ETFS", timeout=60)
        html.raise_for_status()
        match = _WICKET.search(html.text)
        if not match:
            warnings.warn("justETF screener layout changed; counter assumed 0.", stacklevel=2)
            _counter = 0
        else:
            _counter = int(match.group(1))
    return _session, _counter


def _screener_post_url(counter: int) -> str:
    return (
        f"{_SEARCH_URL}?{counter}-1.0-container-tabsContentContainer-tabsContentRepeater-"
        "1-container-content-etfsTablePanel=&search=ETFS&_wicket=1"
    )


def screener_rows(
    etfs_params: str,
    *,
    country: str = "DE",
    length: int = -1,
) -> list[dict[str, Any]]:
    """POST the justETF screener and return raw `data` rows."""
    session, counter = _ensure_session()
    r = session.post(
        _screener_post_url(counter),
        {
            "draw": 1,
            "start": 0,
            "length": length,
            "lang": "en",
            "country": country,
            "universeType": "private",
            "defaultCurrency": "EUR",
            "etfsParams": etfs_params,
        },
        timeout=60,
    )
    if r.status_code >= 400:
        reset_screener_session()
        r.raise_for_status()
    payload = r.json()
    return payload.get("data") or []


@lru_cache(maxsize=2048)
def isin_ticker_at_mic(isin: str, mic: str) -> str | None:
    """Ticker for an ISIN at a venue (from screener country, not profile HTML)."""
    country = _MIC_COUNTRY.get(mic, "DE")
    params = f"search=ETF&productGroup=epg-longOnly&ls=any&query={isin}"
    for row in screener_rows(params, country=country, length=10):
        if row.get("isin") == isin:
            ticker = (row.get("ticker") or "").strip()
            return ticker or None
    return None
