-- ============================================================================
-- ch12_regime.sql  (PostgreSQL)
-- Ref: §12.4.2 (Table 12.2 regimes), §12.7.3 (cross-market ranking),
--      §12.9.4 (Table 12.7 one market, five dashboards)
-- regime_daily is written by ch12_regime_gate.py (ADX needs Wilder smoothing,
-- computed in Python); SQL does run lengths and cross-market ranks.
-- ============================================================================

CREATE TABLE IF NOT EXISTS regime_daily (
    symbol     VARCHAR(24) NOT NULL,
    d          DATE        NOT NULL,
    adx        NUMERIC     NOT NULL,
    plus_di    NUMERIC     NOT NULL,
    minus_di   NUMERIC     NOT NULL,
    regime     VARCHAR(16) NOT NULL,     -- ranging | developing_trend | strong_trend | exhausted
    PRIMARY KEY (symbol, d)
);

-- Run length of each regime (gaps-and-islands)
CREATE OR REPLACE VIEW v_regime_runs AS
WITH g AS (
    SELECT symbol, d, regime,
           ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY d)
         - ROW_NUMBER() OVER (PARTITION BY symbol, regime ORDER BY d) AS grp
    FROM regime_daily
)
SELECT symbol, regime, MIN(d) AS run_start, MAX(d) AS run_end, COUNT(*) AS bars
FROM g
GROUP BY symbol, regime, grp;

-- §12.7.3: rank all markets by ADX each day, with direction and slope
CREATE OR REPLACE VIEW v_market_adx_rank AS
SELECT symbol, d, adx, plus_di - minus_di AS di_spread,
       CASE WHEN plus_di > minus_di THEN 'up' ELSE 'down' END            AS direction,
       adx - LAG(adx, 3) OVER (PARTITION BY symbol ORDER BY d)          AS adx_slope3,
       RANK() OVER (PARTITION BY d ORDER BY adx DESC)                    AS adx_rank
FROM regime_daily;
