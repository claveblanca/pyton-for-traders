"""ch01_asset_classes.py — Chapter 1 Hands-On: one year of five asset classes side by side.

Return, volatility, worst drawdown and correlation to stocks for one ETF per class.
A class that moves with stocks (correlation near 1) does not diversify them.

Run from the repo root:
    python ch01_asset_classes.py                    # SPY IEF GLD DBC BTC-USD
    python ch01_asset_classes.py SPY TLT GLD        # your own list, stocks first
    python ch01_asset_classes.py --demo             # offline sample data
"""
import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
from common import pd, cli, closes


def class_table(px: pd.DataFrame) -> pd.DataFrame:
    r = px.pct_change().dropna()
    return pd.DataFrame({
        "return_1y": px.iloc[-1] / px.iloc[0] - 1,
        "volatility": r.std() * 252 ** 0.5,                 # annualised
        "max_drawdown": (px / px.cummax() - 1).min(),
        "corr_to_stocks": r.corr()[px.columns[0]],          # first symbol = stocks
    }).round(3)


if __name__ == "__main__":
    symbols, demo = cli(["SPY", "IEF", "GLD", "DBC", "BTC-USD"])
    print(class_table(closes(symbols, demo).tail(252)).to_string())
