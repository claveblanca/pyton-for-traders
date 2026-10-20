-- ============================================================================
-- ch03_macro_series.sql  (PostgreSQL)
-- Ref: §3.12.2 (FRED series), §3.10.1-3.10.2 (rolling correlation, Table 3.9),
--      PROOF §3.13.1 (the dated reading)
-- One long table for every macro series (€STR, Euribor, HICP, DGS10, ...),
-- loaded by ch03_bond_endpoints.py; daily closes for the stock/bond legs
-- come from stock_daily_prices (ch02_fundamentals.sql).
-- ============================================================================

CREATE TABLE IF NOT EXISTS macro_series (
    series_id  VARCHAR(32) NOT NULL,        -- 'estr', 'euribor_6m', 'hicp_yoy', 'DGS10'
    obs_date   DATE        NOT NULL,
    value      NUMERIC     NOT NULL,
    source     VARCHAR(16) NOT NULL,        -- 'ecb' | 'fred' | 'eurostat'
    loaded_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (series_id, obs_date)
);

-- §3.13.1: latest value and its date per series (check Euribor's fixing date!)
CREATE OR REPLACE VIEW v_bond_reading AS
SELECT DISTINCT ON (series_id) series_id, obs_date, value, source
FROM macro_series
ORDER BY series_id, obs_date DESC;

-- §3.10: rolling 30/60/90-day correlation of daily returns, SPY vs TLT
CREATE OR REPLACE VIEW v_stock_bond_corr AS
WITH px AS (
    SELECT s.price_date AS d, s.close AS spy, b.close AS tlt
    FROM stock_daily_prices s
    JOIN stock_daily_prices b ON b.price_date = s.price_date AND b.symbol = 'TLT'
    WHERE s.symbol = 'SPY'
), r AS (
    SELECT d,
           spy / LAG(spy) OVER (ORDER BY d) - 1 AS r_spy,
           tlt / LAG(tlt) OVER (ORDER BY d) - 1 AS r_tlt
    FROM px
)
SELECT d,
       CORR(r_spy, r_tlt) OVER (ORDER BY d ROWS 29 PRECEDING) AS corr_30,
       CORR(r_spy, r_tlt) OVER (ORDER BY d ROWS 59 PRECEDING) AS corr_60,
       CORR(r_spy, r_tlt) OVER (ORDER BY d ROWS 89 PRECEDING) AS corr_90
FROM r
WHERE r_spy IS NOT NULL;

-- Table 3.9 regime on the 90-day line
CREATE OR REPLACE VIEW v_stock_bond_regime AS
SELECT d, corr_90,
       CASE WHEN corr_90 < 0 THEN 'hedge'
            WHEN corr_90 <= 0.2 THEN 'neutral'
            ELSE 'together' END AS regime
FROM v_stock_bond_corr;
