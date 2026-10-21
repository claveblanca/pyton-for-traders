# handson — one script per chapter of *The Data-Driven Trader*

Each script fetches free market data, computes the indicator of its chapter and prints a short verdict.
The book's [CODE] Hands-On section of every chapter explains the script and shows its main function as Listing N.1.

## Install once (Chapter 1, Section 1.6)

```bash
git clone https://github.com/claveblanca/pyton-for-traders.git
cd pyton-for-traders/handson
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run_selftests.py            # every script on offline sample data -> 12/12 passed
```

## Run

Every script works the same way, from this folder:

```bash
python ch10_ma_bands.py --demo     # offline sample data
python ch10_ma_bands.py BTC-USD    # live data (Yahoo Finance; add --kraken in ch08 for Kraken)
```

| Ch | Script | What it prints | Live example | Needs |
|---|---|---|---|---|
| 1 | `ch01_asset_classes.py` | return, volatility, drawdown, correlation to stocks per asset class | `python ch01_asset_classes.py` | — |
| 2 | `ch02_stock_screen.py` | debt ratio, coverage, cash conversion ratio, cycle P/E, fair price, stage | `python ch02_stock_screen.py NVDA KO` | `SEC_USER_AGENT` for 7 years |
| 3 | `ch03_stock_bond.py` | 30/90-day stock/bond correlation, regime | `python ch03_stock_bond.py SPY TLT` | — |
| 4 | `ch04_etf_cost.py` | spread, RTC, cost over N years, trade hurdle | `python ch04_etf_cost.py CSPX.L --ter 0.07` | TER from the factsheet; market hours |
| 5 | `ch05_futures_risk.py` | ATR stop, contracts allowed by the 2% rule, leverage | `python ch05_futures_risk.py GC=F --point-value 10` | contract point value |
| 6 | `ch06_etc_gap.py` | yearly gap between an ETC and its future | `python ch06_etc_gap.py --etc BRNT.MI --future BZ=F` | — |
| 7 | `ch07_options_iv.py` | straddle, expected move, IV vs HV20 | `python ch07_options_iv.py SPY` | market hours |
| 8 | `ch08_data_check.py` | data-quality checks, 20-day trend structure | `python ch08_data_check.py XBTUSD --kraken` | — |
| 9 | `ch09_obv_volume.py` | OBV trend, divergence, selling-climax test | `python ch09_obv_volume.py BTC-USD` | — |
| 10 | `ch10_ma_bands.py` | EMA trend and last cross, %B, squeeze | `python ch10_ma_bands.py SPY` | — |
| 11 | `ch11_rsi_macd.py` | RSI zone, MACD histogram turn | `python ch11_rsi_macd.py BTC-USD` | — |
| 12 | `ch12_adx_gate.py` | ADX regime and which tools may trade | `python ch12_adx_gate.py XLE XLK GLD` | — |

## Shared code — `common/`

Everything the scripts share is imported from `common` (`from common import cli, daily, show, rsi, ...`):
command-line helpers, daily bars with the still-forming bar dropped, offline sample data for `--demo`,
the indicators and one way of printing the result.

Live prices are free and delayed: they are for study, not for placing orders.
