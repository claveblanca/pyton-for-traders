-- ============================================================================
-- ch10_ma.sql  (PostgreSQL)
-- Ref: §10.4.1 (golden/death cross), §10.10.1-10.10.3 (Listings 10.1-10.3),
--      PROOF §10.11 (count the cross events before trusting a hit rate)
-- SMAs, cross events and the SMA-200 regime with run length. EMA is
-- recursive and stays in Python (ch10_ma_state.py).
-- Reads stock_daily_prices (ch02_fundamentals.sql).
-- ============================================================================

CREATE OR REPLACE VIEW v_sma AS
SELECT symbol, price_date, close,
       AVG(close) OVER (PARTITION BY symbol ORDER BY price_date ROWS 19  PRECEDING) AS sma20,
       AVG(close) OVER (PARTITION BY symbol ORDER BY price_date ROWS 49  PRECEDING) AS sma50,
       AVG(close) OVER (PARTITION BY symbol ORDER BY price_date ROWS 199 PRECEDING) AS sma200,
       COUNT(*)   OVER (PARTITION BY symbol ORDER BY price_date ROWS 199 PRECEDING) AS n200
FROM stock_daily_prices;

-- Cross events: sign change of (fast - slow); warm-up rows excluded (never forward-fill)
CREATE OR REPLACE VIEW v_ma_cross_events AS
WITH s AS (
    SELECT symbol, price_date, close, sma20, sma50, sma200, n200,
           SIGN(sma50 - sma200)                                                         AS s_50_200,
           LAG(SIGN(sma50 - sma200)) OVER (PARTITION BY symbol ORDER BY price_date)     AS p_50_200,
           SIGN(sma20 - sma50)                                                          AS s_20_50,
           LAG(SIGN(sma20 - sma50))  OVER (PARTITION BY symbol ORDER BY price_date)     AS p_20_50
    FROM v_sma
)
SELECT symbol, price_date, close, '50/200' AS pair,
       CASE WHEN s_50_200 > p_50_200 THEN 'golden' ELSE 'death' END AS event
FROM s WHERE n200 = 200 AND s_50_200 <> p_50_200 AND p_50_200 <> 0
UNION ALL
SELECT symbol, price_date, close, '20/50',
       CASE WHEN s_20_50 > p_20_50 THEN 'golden' ELSE 'death' END
FROM s WHERE n200 >= 50 AND s_20_50 <> p_20_50 AND p_20_50 <> 0;

-- SMA-200 regime with run length (gaps-and-islands)
CREATE OR REPLACE VIEW v_regime_200 AS
WITH r AS (
    SELECT symbol, price_date, close, sma200,
           close > sma200 AS above
    FROM v_sma WHERE n200 = 200
), g AS (
    SELECT r.*,
           ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY price_date)
         - ROW_NUMBER() OVER (PARTITION BY symbol, above ORDER BY price_date) AS grp
    FROM r
)
SELECT symbol, price_date, close, sma200,
       CASE WHEN above THEN 'bull' ELSE 'bear' END                                  AS regime,
       ROW_NUMBER() OVER (PARTITION BY symbol, above, grp ORDER BY price_date)       AS bars_in_regime
FROM g;
