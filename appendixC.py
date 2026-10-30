"""appendixC.py — GDELT DOC API timelines and optional GKG v2 file download.

    python appendixC.py
    python appendixC.py --download
    python appendixC.py --download --data-dir data/gdelt
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

import pandas as pd
import requests

DOC_API = "https://api.gdeltproject.org/api/v2/doc/doc"
LASTUPDATE_URL = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"
_MIN_DOC_INTERVAL_S = 5.0
_last_doc_request_at = 0.0


def gdelt(query, mode="timelinetone", timespan="3m", *, retries: int = 5, **kw):
    """Query GDELT DOC API; spaces requests and retries on HTTP 429."""
    global _last_doc_request_at
    p = {"query": query, "mode": mode, "timespan": timespan, "format": "json", **kw}
    last_response: requests.Response | None = None
    for attempt in range(retries):
        elapsed = time.monotonic() - _last_doc_request_at
        if elapsed < _MIN_DOC_INTERVAL_S:
            time.sleep(_MIN_DOC_INTERVAL_S - elapsed)
        last_response = requests.get(DOC_API, params=p, timeout=30)
        _last_doc_request_at = time.monotonic()
        if last_response.status_code == 429:
            wait = int(last_response.headers.get("Retry-After", 30 + attempt * 15))
            time.sleep(wait)
            continue
        last_response.raise_for_status()
        return last_response.json()
    if last_response is not None:
        last_response.raise_for_status()
    raise requests.HTTPError("GDELT DOC API failed after retries")


def timeline(js):
    s = js["timeline"][0]["data"]
    return pd.Series({pd.to_datetime(d["date"]): d["value"] for d in s})


def parse_gdelt_lastupdate(text: str) -> list[tuple[int, str, str]]:
    """Parse lastupdate.txt lines: size md5 url."""
    rows: list[tuple[int, str, str]] = []
    for line in text.strip().splitlines():
        parts = line.split()
        if len(parts) >= 3:
            rows.append((int(parts[0]), parts[1], parts[2]))
    return rows


def download_gdelt_v2_lastupdate(
    data_dir: str | Path = "data/gdelt",
    *,
    timeout: int = 300,
) -> list[Path]:
    """Fetch lastupdate.txt and download each listed zip into ``data_dir``."""
    dest = Path(data_dir)
    dest.mkdir(parents=True, exist_ok=True)
    meta = requests.get(LASTUPDATE_URL, timeout=30)
    meta.raise_for_status()
    saved: list[Path] = []
    for _size, _md5, url in parse_gdelt_lastupdate(meta.text):
        name = url.rsplit("/", 1)[-1]
        path = dest / name
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        path.write_bytes(r.content)
        saved.append(path)
    return saved


def _main_doc_demo() -> None:
    tone = timeline(gdelt('(inflation OR "interest rates") sourcelang:english'))
    vol = timeline(gdelt("recession sourcelang:english", mode="timelinevol"))
    arts = pd.DataFrame(
        gdelt(
            '"bond market" sourcelang:english',
            mode="artlist",
            maxrecords=50,
            timespan="1w",
        )["articles"]
    )
    print("tone (last):", tone.iloc[-1] if len(tone) else None)
    print("vol (last):", vol.iloc[-1] if len(vol) else None)
    print(arts[["seendate", "domain", "title"]].head())


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="GDELT appendix: DOC API or v2 file download.")
    p.add_argument(
        "--download",
        action="store_true",
        help="download files listed in gdeltv2/lastupdate.txt",
    )
    p.add_argument(
        "--data-dir",
        default="data/gdelt",
        help="folder for downloaded zips (default: data/gdelt)",
    )
    args = p.parse_args()
    if args.download:
        paths = download_gdelt_v2_lastupdate(args.data_dir)
        for path in paths:
            print(path)
        print(f"\n{len(paths)} file(s) in {args.data_dir}")
    else:
        _main_doc_demo()
