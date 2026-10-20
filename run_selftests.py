"""Run every chapter script's offline --selftest and report pass/fail.

    python run_selftests.py
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
scripts = sorted(p for p in ROOT.glob("*/*.py") if p.parent.name != "common")
failed = []
for p in scripts:
    r = subprocess.run([sys.executable, str(p), "--selftest"], capture_output=True, text=True)
    ok = r.returncode == 0 and r.stdout.strip().endswith("selftest OK")
    print(f"{'OK  ' if ok else 'FAIL'} {p.relative_to(ROOT)}")
    if not ok:
        failed.append(p)
        print((r.stderr or r.stdout)[-800:])
print(f"\n{len(scripts) - len(failed)}/{len(scripts)} passed")
sys.exit(1 if failed else 0)
