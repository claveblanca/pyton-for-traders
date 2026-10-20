-- ============================================================================
-- ch09_volume_oi.sql  (PostgreSQL) -- extends Listings 9.2 and 9.4
-- Ref: §9.10.1 (Listing 9.2 stock_obv_daily), §9.7.2 (Listing 9.4 climax),
--      §9.9.3 (Table 9.4), §9.5 (Table 9.2), §9.8 (put/call ratio)
-- Needs: stock_daily_prices (ch02_fundamentals.sql), futures_settlements
-- (ch05_futures.sql), option_quotes (ch07_option_chain.sql).
-- ============================================================================

-- Listing 9.2, repeated here so this file is self-contained
CREATE OR REPLACE VIEW stock_obv_daily AS
WITH signed AS (
    SELECT symbol, price_date, close, volume,
           CASE WHEN LAG(close) OVER w IS NULL THEN 0::bigint
                WHEN close > LAG(close) OVER w THEN volume
                WHEN close < LAG(close) OVER w THEN -volume
                ELSE 0::bigint END AS signed_volume
    FROM stock_daily_prices
    WHERE volume IS NOT NULL
    WINDOW w AS (PARTITION BY symbol ORDER BY price_date)
)
SELECT symbol, price_date, close, volume, signed_volume,
       SUM(signed_volume) OVER (PARTITION BY symbol ORDER BY price_date
                                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS obv
FROM signed;

-- Table 9.4 BUY row: close > prior 20-day high, volume >= 1.5x, OBV at a new 20-day high
CREATE OR REPLACE VIEW v_volume_confirmed_breakout AS
WITH s AS (
    SELECT symbol, price_date, close, volume, obv,
           MAX(close)  OVER (PARTITION BY symbol ORDER BY price_date ROWS BETWEEN 20 PRECEDING AND 1 PRECEDING) AS hi20,
           MIN(close)  OVER (PARTITION BY symbol ORDER BY price_date ROWS BETWEEN 20 PRECEDING AND 1 PRECEDING) AS lo20,
           AVG(volume) OVER (PARTITION BY symbol ORDER BY price_date ROWS BETWEEN 20 PRECEDING AND 1 PRECEDING) AS avg_vol20,
           MAX(obv)    OVER (PARTITION BY symbol ORDER BY price_date ROWS BETWEEN 20 PRECEDING AND 1 PRECEDING) AS obv_hi20,
           MIN(obv)    OVER (PARTITION BY symbol ORDER BY price_date ROWS BETWEEN 20 PRECEDING AND 1 PRECEDING) AS obv_lo20
    FROM stock_obv_daily
)
SELECT symbol, price_date, close, volume / NULLIF(avg_vol20, 0) AS vol_ratio,
       CASE WHEN close > hi20 AND volume >= 1.5 * avg_vol20 AND obv > obv_hi20 THEN 'BUY'
            WHEN close < lo20 AND volume >= 1.5 * avg_vol20 AND obv < obv_lo20 THEN 'SELL'
       END AS signal
FROM s
WHERE (close > hi20 AND volume >= 1.5 * avg_vol20 AND obv > obv_hi20)
   OR (close < lo20 AND volume >= 1.5 * avg_vol20 AND obv < obv_lo20);

-- Table 9.2 on the active futures month
CREATE OR REPLACE VIEW v_price_oi_quadrant AS
WITH f AS (
    SELECT s.root, s.trade_date, s.settle, s.open_interest,
           s.settle - LAG(s.settle, 5) OVER w               AS d_price,
           s.open_interest - LAG(s.open_interest, 5) OVER w AS d_oi
    FROM v_front_month m
    JOIN futures_settlements s
      ON s.root = m.root AND s.trade_date = m.trade_date AND s.contract = m.active_contract
    WINDOW w AS (PARTITION BY s.root ORDER BY s.trade_date)
)
SELECT root, trade_date, settle, open_interest,
       CASE WHEN d_price > 0 AND d_oi > 0 THEN 'new buying (bullish)'
            WHEN d_price > 0 AND d_oi < 0 THEN 'short covering (bearish)'
            WHEN d_price < 0 AND d_oi > 0 THEN 'new short selling (bearish)'
            WHEN d_price < 0 AND d_oi < 0 THEN 'long liquidation (stabilizing)'
            ELSE 'flat' END AS reading
FROM f;

-- §9.8 put/call ratio per underlying and day (volume and open interest)
CREATE OR REPLACE VIEW v_pcr_daily AS
SELECT underlying, quote_ts::date AS d,
       SUM(volume) FILTER (WHERE opt_type = 'P')::numeric
           / NULLIF(SUM(volume) FILTER (WHERE opt_type = 'C'), 0)        AS pcr_volume,
       SUM(open_interest) FILTER (WHERE opt_type = 'P')::numeric
           / NULLIF(SUM(open_interest) FILTER (WHERE opt_type = 'C'), 0) AS pcr_oi
FROM option_quotes
GROUP BY underlying, quote_ts::date;
