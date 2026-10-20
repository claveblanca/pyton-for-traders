-- ============================================================================
-- ch11_oscillators.sql  (PostgreSQL)
-- Ref: §11.10.5 (Listing 11.5: RSI regime buckets + forward returns),
--      PROOF §11.11 (validate before trusting)
-- Indicator values are computed in Python (Wilder smoothing is recursive)
-- and stored here; SQL does the bucketing and the forward-return join, so
-- Listing 11.5's Kruskal-Wallis input is one query.
-- ============================================================================

CREATE TABLE IF NOT EXISTS indicators (
    symbol     VARCHAR(24)  NOT NULL,
    interval   VARCHAR(4)   NOT NULL,
    ts         TIMESTAMPTZ  NOT NULL,
    close      NUMERIC      NOT NULL,
    rsi14      NUMERIC,
    macd       NUMERIC, macd_signal NUMERIC, macd_hist NUMERIC,
    stoch_k    NUMERIC, stoch_d NUMERIC,
    williams_r NUMERIC,            -- -20..0 overbought, -80..-100 oversold
    cci20      NUMERIC,
    adx        NUMERIC, plus_di NUMERIC, minus_di NUMERIC,
    PRIMARY KEY (symbol, interval, ts)
);

CREATE OR REPLACE VIEW v_rsi_regime_buckets AS
SELECT symbol, interval, ts, rsi14,
       CASE WHEN rsi14 < 30 THEN 'oversold'
            WHEN rsi14 < 50 THEN 'bearish'
            WHEN rsi14 < 70 THEN 'bullish'
            ELSE 'overbought' END                                                    AS rsi_regime,
       LEAD(close, 5) OVER (PARTITION BY symbol, interval ORDER BY ts) / close - 1   AS fwd_return_5
FROM indicators
WHERE rsi14 IS NOT NULL;

-- Summary per bucket (the describe() of Listing 11.5)
CREATE OR REPLACE VIEW v_rsi_regime_summary AS
SELECT symbol, interval, rsi_regime, COUNT(*) AS n,
       AVG(fwd_return_5) AS mean_fwd_5, STDDEV_SAMP(fwd_return_5) AS sd_fwd_5,
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fwd_return_5) AS median_fwd_5
FROM v_rsi_regime_buckets
WHERE fwd_return_5 IS NOT NULL
GROUP BY symbol, interval, rsi_regime;
