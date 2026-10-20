"""common/backtest.py -- a minimal vectorised backtest shared by Ch 10 and Ch 12.

position: Series in {-1, 0, 1} decided at the close of bar t and held over
bar t+1 (shifted inside, so no look-ahead). Costs are charged per unit of
position change, in basis points of notional (spread + fees).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from common.stats import cagr, max_drawdown, sharpe


def run(
    close: pd.Series,
    position: pd.Series,
    cost_bps: float = 5.0,
    periods_per_year: float = 252,
) -> dict:
    pos = position.reindex(close.index).fillna(0).shift(1).fillna(0)
    ret = close.pct_change().fillna(0)
    turnover = pos.diff().abs().fillna(pos.abs())
    strat = pos * ret - turnover * cost_bps / 1e4
    equity = (1 + strat).cumprod()
    changes = pos.ne(pos.shift()) & pos.ne(0)
    trade_id = changes.cumsum().where(pos != 0)
    per_trade = (
        strat.groupby(trade_id).sum()
        if trade_id.notna().any()
        else pd.Series(dtype=float)
    )
    hold = (
        pos.ne(0).groupby(trade_id).sum()
        if trade_id.notna().any()
        else pd.Series(dtype=float)
    )
    return {
        "cagr": cagr(equity, periods_per_year),
        "sharpe": sharpe(strat, periods_per_year),
        "max_dd": max_drawdown(equity),
        "trades": int(len(per_trade)),
        "hit_rate": float((per_trade > 0).mean()) if len(per_trade) else np.nan,
        "avg_hold_bars": float(hold.mean()) if len(hold) else np.nan,
        "whipsaw_rate": float((hold <= 5).mean()) if len(hold) else np.nan,
        "equity": equity,
    }
