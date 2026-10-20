"""ch02_stock_screen.py — Chapter 2 Hands-On: the stock screen on any ticker.

Fetches up to 7 years of annual statements and applies the chapter's filters:
debt ratio <= 60% of tangible assets, interest coverage >= 3, Cash Flow Index >= 1,
cycle-average P/E <= 16 (fair price = 16 x average net income per share).

Run from the repo root:
    python ch02_stock_screen.py NVDA KO MSFT
    python ch02_stock_screen.py --demo          # NVIDIA, the chapter's PROOF numbers
Needs: for 7 years of history a free SEC identity ->  export SEC_USER_AGENT="Name you@mail.com"
       (without it, yfinance gives about 4 years)
"""
import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from common import pd, cli
from common.stocks_data import live, mock_nvda, screen

COLUMNS = ["ticker", "stage", "debt_ratio", "coverage_7y", "cfi_7y", "cape_pe", "fair_price_16x"]

if __name__ == "__main__":
    tickers, demo = cli(["NVDA"])
    rows = [screen("NVDA", *mock_nvda())] if demo else [screen(t, *live(t)) for t in tickers]
    print(pd.DataFrame(rows)[COLUMNS].round(2).to_string(index=False))
    print("stage: candidate > watch > fails_valuation > rejected_stage_1 (failed a safety filter)")
