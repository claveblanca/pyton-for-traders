"""Smoke-test Hands-On scripts with --demo (offline sample bars).

    python run_selftests.py
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
scripts = sorted(ROOT.glob("ch*.py"))
failed: list[pathlib.Path] = []
for p in scripts:
    r = subprocess.run(
        [sys.executable, str(p), "--demo"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    ok = r.returncode == 0
    print(f"{'OK  ' if ok else 'FAIL'} {p.name}")
    if not ok:
        failed.append(p)
        print((r.stderr or r.stdout)[-600:])
print(f"\n{len(scripts) - len(failed)}/{len(scripts)} passed")
sys.exit(1 if failed else 0)
