"""Amundi ETF list from the justETF screener (provider filter)."""
from __future__ import annotations

import pandas as pd

from common.justetf_catalog import HedgeFilter, amundi_etfs as _amundi_etfs
from common.justetf_catalog import demo_amundi_etfs as demo_amundi_etfs


def amundi_etfs(*, include_active: bool = True, hedge: HedgeFilter = "any") -> pd.DataFrame:
    return _amundi_etfs(include_active=include_active, hedge=hedge)
