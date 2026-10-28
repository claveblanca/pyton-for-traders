"""One way of printing results, so every Hands-On output looks the same."""


def _format_value(key: str, value: object) -> str:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if key.startswith("cost_eur") or key.endswith("_eur") or key == "amount_eur":
            return f"€{float(value):,.0f}"
        if key in ("bid", "ask"):
            return f"{float(value):,.4f}".rstrip("0").rstrip(".")
        if key.endswith("_pct") or "pct" in key:
            s = f"{value:g}" if float(value) == int(value) else str(value)
            return f"{s} %"
    if key == "ter_pct" and isinstance(value, (int, float)):
        return f"{value:g} %"
    return str(value)


def show(
    result: dict,
    note: str | None = None,
    *,
    title: str | None = None,
    labels: dict[str, str] | None = None,
) -> None:
    labels = labels or {}
    display_keys = [labels.get(k, k) for k in result]
    width = max(len(k) for k in display_keys) if display_keys else 0
    if title:
        print(title)
        print("─" * max(len(title), width + 12))
        for k, v in result.items():
            label = labels.get(k, k)
            print(f"  {label:<{width}}  {_format_value(k, v)}")
        print("─" * max(len(title), width + 12))
    else:
        for k, v in result.items():
            label = labels.get(k, k)
            print(f"{label:>{width}}: {_format_value(k, v)}")
    if note:
        print(note)

