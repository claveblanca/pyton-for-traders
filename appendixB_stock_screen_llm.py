"""appendixB_stock_screen_llm.py — Appendix B: profitability & valuation JSON → OpenRouter LLM.

Feeds a stock-screen JSON payload (from ch02 or a saved file) to DeepSeek on OpenRouter and
returns structured commentary for short-, medium-, and long-term horizons.

Requires:
    export OPENROUTER_API_KEY="..."
    pip install openai

When building live data from a ticker (not --input):
    export SEC_USER_AGENT="Your Name you@email.com"
    pip install pandas requests yfinance

Run from this folder:
    python appendixB_stock_screen_llm.py              # data/sample.json (default)
    python appendixB_stock_screen_llm.py --input other.json
    python appendixB_stock_screen_llm.py AAPL --save-screen   # overwrite data/sample.json
    python appendixB_stock_screen_llm.py AAPL --save-screen out.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

MODEL = "deepseek/deepseek-v4.1-flash-1017"
DEFAULT_SCREEN_PATH = _ROOT / "data" / "sample.json"

SYSTEM_PROMPT = """\
You are an equity research assistant for education only. Use ONLY numbers and facts in the
user's JSON: profitability by fiscal year, current valuation multiples, and (when present)
valuation_history with per-fiscal-year multiples—use it to judge whether today's multiples
are high or low versus the company's own history. Do not invent figures,
filings, or news. If data is missing or inconsistent, say so in data_quality_notes.

This is not investment advice. Do not say buy, sell, or hold. Frame ideas as hypotheses,
risks, and items to verify—not trading instructions.

Return a single JSON object with these keys:
- symbol (string, from input)
- disclaimer (string, one sentence: educational, not advice)
- data_quality_notes (array of strings)
- short_term (object): horizon (e.g. weeks to ~3 months), narrative (string, max 120 words),
  themes (array of strings), risks (array), research_ideas (array)
- medium_term (object): horizon (~3–18 months), same subfields as short_term
- long_term (object): horizon (~18 months to several years), same subfields as short_term
- summary (string, max 80 words tying the three horizons together)
"""


def _json_safe(value: Any) -> Any:
    if value is None:
        return None
    try:
        import math

        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return None
    except ImportError:
        pass
    if hasattr(value, "item"):
        return _json_safe(value.item())
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    return value


def build_screen_json(ticker: str, *, years: int = 7, include_valuation: bool = True) -> dict[str, Any]:
    """Build ch02-aligned screen payload from live SEC + yfinance."""
    import ch02_stock_screen as ch02

    sym = ticker.upper()
    df = ch02.screen(sym, years)
    ratio_keys = ch02.RATIO_COLS + ["total_debt"]
    profitability = []
    for fy, row in df.iterrows():
        entry: dict[str, Any] = {"fiscal_year": int(fy)}
        for key in ratio_keys:
            entry[key] = _json_safe(row.get(key))
        profitability.append(entry)

    payload: dict[str, Any] = {
        "symbol": sym,
        "source": "ch02_stock_screen (SEC EDGAR + yfinance)",
        "screened_at": datetime.now(timezone.utc).isoformat(),
        "profitability": profitability,
    }

    if include_valuation:
        last = df.iloc[-1]
        m = ch02.market_multiples(sym, last)
        payload["valuation"] = _json_safe(m.iloc[0].to_dict())
        hist = ch02.historical_multiples(sym, df)
        payload["valuation_history"] = [
            _json_safe({"fiscal_year": int(fy), **row, "fy_end": row["fy_end"].isoformat()})
            for fy, row in hist.to_dict(orient="index").items()
        ]

    return payload


def load_screen_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: expected a JSON object at the top level")
    if "profitability" not in data:
        raise SystemExit(f"{path}: missing 'profitability' array")
    return data


def ask_openrouter(screen: dict[str, Any], *, model: str, api_key: str) -> dict[str, Any]:
    from openai import OpenAI

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    user_content = (
        "Analyze the following stock screen JSON. Comment on profitability trends and "
        "valuation context, then give short-, medium-, and long-term research angles.\n\n"
        + json.dumps(screen, indent=2)
    )
    response = client.chat.completions.create(
        model=model,
        temperature=0.25,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
    )
    raw = response.choices[0].message.content or "{}"
    return json.loads(raw)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument(
        "symbol",
        nargs="?",
        help="US ticker: fetch SEC/yfinance screen JSON (default input: data/sample.json)",
    )
    p.add_argument(
        "--demo",
        action="store_true",
        help=f"read {DEFAULT_SCREEN_PATH.relative_to(_ROOT)} (same as running with no args)",
    )
    p.add_argument(
        "--input",
        "-i",
        type=Path,
        help=f"read screen JSON from file (default: {DEFAULT_SCREEN_PATH.relative_to(_ROOT)})",
    )
    p.add_argument(
        "--save-screen",
        nargs="?",
        const=DEFAULT_SCREEN_PATH,
        default=None,
        type=Path,
        metavar="PATH",
        help=(
            "write screen JSON after fetch; PATH defaults to data/sample.json "
            "(overwrites the default sample when PATH is omitted)"
        ),
    )
    p.add_argument(
        "--save-analysis",
        type=Path,
        metavar="PATH",
        help="write the LLM JSON response",
    )
    p.add_argument("--years", type=int, default=7, help="fiscal years to fetch for a live ticker (default 7)")
    p.add_argument("--no-valuation", action="store_true", help="omit yfinance multiples when fetching ticker")
    p.add_argument("--model", default=MODEL, help=f"OpenRouter model slug (default {MODEL})")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="print screen JSON only; do not call OpenRouter",
    )
    return p.parse_args()


def _default_screen_path() -> Path:
    if not DEFAULT_SCREEN_PATH.is_file():
        raise SystemExit(
            f"Missing default screen file: {DEFAULT_SCREEN_PATH}\n"
            "Add data/sample.json or pass --input PATH or a SYMBOL to fetch live data."
        )
    return DEFAULT_SCREEN_PATH


def main() -> None:
    args = parse_args()

    if args.symbol:
        screen = build_screen_json(
            args.symbol, years=args.years, include_valuation=not args.no_valuation
        )
    elif args.input:
        screen = load_screen_json(args.input)
    else:
        screen = load_screen_json(_default_screen_path())

    save_path = args.save_screen
    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_text(json.dumps(screen, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote screen JSON → {save_path}")

    if args.dry_run:
        print(json.dumps(screen, indent=2))
        return

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit(
            "Set OPENROUTER_API_KEY to call OpenRouter, or use --dry-run to inspect JSON only."
        )

    analysis = ask_openrouter(screen, model=args.model, api_key=api_key)
    print(json.dumps(analysis, indent=2))

    if args.save_analysis:
        args.save_analysis.write_text(json.dumps(analysis, indent=2) + "\n", encoding="utf-8")
        print(f"\nWrote analysis JSON → {args.save_analysis}")


if __name__ == "__main__":
    main()
