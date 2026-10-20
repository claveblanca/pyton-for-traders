"""Search metric / indicator definitions from Markdown under mcp/docs/."""

from __future__ import annotations

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MCP_DOCS_DIR = Path(__file__).resolve().parent / "docs"

# Glob patterns relative to MCP_DOCS_DIR
DOC_GLOBS: dict[str, list[str]] = {
    "investing": [
        "partI-investing/**/*.md",
    ],
    "crypto": [
        "partII-technical-analysis/**/*.md",
    ],
}


def _paths_for_domain(domain: str) -> list[Path]:
    if domain == "any":
        keys = ("investing", "crypto")
    elif domain in DOC_GLOBS:
        keys = (domain,)
    else:
        keys = ("investing", "crypto")
    seen: set[Path] = set()
    out: list[Path] = []
    for key in keys:
        for pattern in DOC_GLOBS[key]:
            for p in sorted(MCP_DOCS_DIR.glob(pattern)):
                if p.is_file() and p.suffix.lower() == ".md" and p not in seen:
                    seen.add(p)
                    out.append(p)
    return out


def search_docs(query: str, domain: str = "any", max_hits: int = 12) -> str:
    q = query.strip()
    if not q:
        return "Provide a non-empty query (metric name, § section, or indicator)."

    tokens = [t for t in re.split(r"\W+", q.lower()) if len(t) >= 2]
    if not tokens:
        tokens = [q.lower()]

    hits: list[tuple[int, str, int, str]] = []

    for path in _paths_for_domain(domain):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lines = text.splitlines()
        for i, line in enumerate(lines):
            lower = line.lower()
            score = sum(1 for t in tokens if t in lower)
            if score == 0:
                continue
            start = max(0, i - 2)
            end = min(len(lines), i + 4)
            snippet = "\n".join(lines[start:end])
            rel = path.relative_to(PROJECT_ROOT)
            hits.append((score, str(rel), i + 1, snippet))

    hits.sort(key=lambda h: (-h[0], h[1], h[2]))
    if not hits:
        domains = domain if domain != "any" else "investing or crypto"
        return f"No matches for {q!r} under mcp/docs ({domains})."

    parts: list[str] = []
    for score, rel, line_no, snippet in hits[:max_hits]:
        parts.append(f"--- {rel}:{line_no} (score {score}) ---\n{snippet}\n")
    return "\n".join(parts)


def list_doc_sources(domain: str = "any") -> str:
    lines = [f"Docs root: {MCP_DOCS_DIR}", ""]
    for path in _paths_for_domain(domain):
        lines.append(f"- {path.relative_to(PROJECT_ROOT)}")
    if len(lines) == 2:
        lines.append("(no .md files matched DOC_GLOBS for this domain)")
    return "\n".join(lines)
