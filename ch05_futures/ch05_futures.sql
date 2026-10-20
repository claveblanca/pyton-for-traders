-- ============================================================================
-- ch05_futures.sql  (PostgreSQL)
-- Ref: §5.1.5 (front month), §5.2.3 (the curve, M1..M6), §5.6.5 (volume and
--      open interest decide the active month); feeds Ch 6 PROOF §6.4 and
--      Ch 9 §9.5 (price/OI matrix)
-- ============================================================================

CREATE TABLE IF NOT EXISTS futures_settlements (
    root            VARCHAR(8)   NOT NULL,     -- 'CL', 'CC', 'MGC'
    contract        VARCHAR(12)  NOT NULL,     -- 'CLZ6'
    expiry          DATE         NOT NULL,
    trade_date      DATE         NOT NULL,
    settle          NUMERIC      NOT NULL,
    volume          BIGINT,
    open_interest   BIGINT,
    exchange        VARCHAR(16),               -- IB code: NYMEX, NYBOT, IPE, ...
    PRIMARY KEY (contract, trade_date)
);

-- The curve on the latest date, months ranked by expiry (M1, M2, ...)
CREATE OR REPLACE VIEW v_curve_today AS
WITH last_day AS (
    SELECT root, MAX(trade_date) AS d FROM futures_settlements GROUP BY root
)
SELECT s.root, s.trade_date, s.contract, s.expiry, s.settle,
       'M' || ROW_NUMBER() OVER (PARTITION BY s.root ORDER BY s.expiry)            AS m,
       LAG(s.settle) OVER (PARTITION BY s.root ORDER BY s.expiry) / s.settle - 1  AS roll_from_prev,
       CASE WHEN LAG(s.settle) OVER (PARTITION BY s.root ORDER BY s.expiry) IS NULL THEN NULL
            WHEN s.settle > LAG(s.settle) OVER (PARTITION BY s.root ORDER BY s.expiry)
            THEN 'contango' ELSE 'backwardation' END                               AS step_shape
FROM futures_settlements s
JOIN last_day l ON l.root = s.root AND l.d = s.trade_date
WHERE s.expiry >= s.trade_date;

-- Active month per root and day = highest open interest (§5.6.5)
CREATE OR REPLACE VIEW v_front_month AS
SELECT root, trade_date, contract AS active_contract, open_interest, volume
FROM (
    SELECT s.*, ROW_NUMBER() OVER (PARTITION BY root, trade_date
                                   ORDER BY open_interest DESC NULLS LAST) AS rn
    FROM futures_settlements s
    WHERE expiry >= trade_date
) x
WHERE rn = 1;
