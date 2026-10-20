"""One way of printing results, so every Hands-On output looks the same."""


def show(result: dict, note: str | None = None) -> None:
    width = max(len(k) for k in result)
    for k, v in result.items():
        print(f"{k:>{width}}: {v}")
    if note:
        print(note)
