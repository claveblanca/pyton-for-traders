-- ============================================================================
-- ch08_ohlcv.sql  (PostgreSQL)
-- Ref: §8.10 [CODE] HANDS-ON (OHLCV schema), §8.9.2 (price gaps,
--      Table 8.4), PROOF §8.10
-- The base OHLCV table every Part II chapter reads, plus data-gap and
-- price-gap views. stock_daily_prices (ch02_fundamentals.sql) stays as the
-- daily equity table used by Ch 9 Listing 9.2; this one holds any interval.
-- ============================================================================

CREATE TABLE IF NOT EXISTS ohlcv (
    symbol    VARCHAR(24)  NOT NULL,
    interval  VARCHAR(4)   NOT NULL,        -- '1h' | '4h' | '1d' | '1wk'
    ts        TIMESTAMPTZ  NOT NULL,
    open      NUMERIC      NOT NULL,
    high      NUMERIC      NOT NULL,
    low       NUMERIC      NOT NULL,
    close     NUMERIC      NOT NULL,
    volume    NUMERIC,
    source    VARCHAR(16)  NOT NULL,        -- 'kraken' | 'yfinance' | 'ib'
    PRIMARY KEY (symbol, interval, ts),
    CONSTRAINT ohlc_consistent CHECK (high >= GREATEST(open, close, low)
                                  AND low  <= LEAST(open, close, high))
);

-- Missing bars: consecutive timestamps further apart than 1.5 intervals
CREATE OR REPLACE VIEW v_data_gaps AS
WITH s AS (
    SELECT symbol, interval, ts,
           LEAD(ts) OVER (PARTITION BY symbol, interval ORDER BY ts) AS next_ts
    FROM ohlcv
)
SELECT symbol, interval, ts, next_ts, next_ts - ts AS gap
FROM s
WHERE next_ts - ts > 1.5 * CASE interval WHEN '1h' THEN INTERVAL '1 hour'
                                         WHEN '4h' THEN INTERVAL '4 hours'
                                         WHEN '1d' THEN INTERVAL '1 day'
                                         ELSE INTERVAL '7 days' END
  -- daily equities: weekends and holidays are not gaps
  AND NOT (interval = '1d' AND next_ts - ts <= INTERVAL '4 days');

-- Price gaps (§8.9.2): today's low above yesterday's high, or the mirror
CREATE OR REPLACE VIEW v_price_gaps AS
WITH s AS (
    SELECT symbol, interval, ts, high, low, close, volume,
           LAG(high) OVER w AS prev_high,
           LAG(low)  OVER w AS prev_low,
           AVG(volume) OVER (PARTITION BY symbol, interval ORDER BY ts
                             ROWS BETWEEN 20 PRECEDING AND 1 PRECEDING) AS avg_vol_20
    FROM ohlcv
    WINDOW w AS (PARTITION BY symbol, interval ORDER BY ts)
)
SELECT symbol, interval, ts,
       CASE WHEN low > prev_high THEN 'up' ELSE 'down' END                  AS direction,
       CASE WHEN low > prev_high THEN (low - prev_high) / prev_high
            ELSE (prev_low - high) / prev_low END * 100                      AS gap_pct,
       volume / NULLIF(avg_vol_20, 0)                                         AS volume_x
FROM s
WHERE low > prev_high OR high < prev_low;
