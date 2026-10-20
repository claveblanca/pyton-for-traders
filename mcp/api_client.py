"""HTTP helpers for datacollect investing (5001) and crypto (5000) backends."""

from __future__ import annotations

import os
from typing import Any

import httpx

DEFAULT_INVESTING_BASE = "http://127.0.0.1:5001"
DEFAULT_CRYPTO_BASE = "http://127.0.0.1:5000"
TIMEOUT = httpx.Timeout(60.0, connect=10.0)


def investing_base() -> str:
    return os.environ.get("INVESTING_API_BASE", DEFAULT_INVESTING_BASE).rstrip("/")


def crypto_base() -> str:
    return os.environ.get("CRYPTO_API_BASE", DEFAULT_CRYPTO_BASE).rstrip("/")


def _get(base: str, path: str, params: dict[str, Any] | None = None) -> Any:
    url = f"{base}{path}"
    with httpx.Client(timeout=TIMEOUT) as client:
        resp = client.get(url, params=params or {})
        resp.raise_for_status()
        return resp.json()


def investing_get(path: str, **params: Any) -> Any:
    clean = {k: v for k, v in params.items() if v is not None}
    return _get(investing_base(), path, clean)


def crypto_get(path: str, **params: Any) -> Any:
    clean = {k: v for k, v in params.items() if v is not None}
    return _get(crypto_base(), path, clean)


def backend_health() -> dict[str, Any]:
    out: dict[str, Any] = {
        "investing_base": investing_base(),
        "crypto_base": crypto_base(),
    }
    for key, base, path in (
        ("investing", investing_base(), "/health"),
        ("crypto", crypto_base(), "/health"),
    ):
        try:
            out[key] = {"ok": True, "data": _get(base, path)}
        except Exception as exc:  # noqa: BLE001 — surface connection errors to MCP client
            out[key] = {"ok": False, "error": str(exc)}
    return out
