-- ============================================================================
-- ch07_option_chain.sql  (PostgreSQL)
-- Ref: §7.5 (Greeks), §7.8 (Table 7.3: live Tradier chain), PROOF §7.9.1
--      (broker Greeks vs from-scratch Black-Scholes)
-- Daily option-chain snapshots -> ATM IV history and IV rank.
-- (Put/call ratios live in ch09_volume_oi.sql -- Ch 9 §9.8.)
-- ============================================================================

CREATE TABLE IF NOT EXISTS option_quotes (
    underlying     VARCHAR(16)  NOT NULL,
    quote_ts       TIMESTAMPTZ  NOT NULL,
    expiry         DATE         NOT NULL,
    strike         NUMERIC      NOT NULL,
    opt_type       CHAR(1)      NOT NULL CHECK (opt_type IN ('C', 'P')),
    spot           NUMERIC      NOT NULL,
    bid            NUMERIC, ask NUMERIC,
    iv             NUMERIC,                   -- broker IV
    delta NUMERIC, gamma NUMERIC, theta NUMERIC, vega NUMERIC,
    volume         BIGINT,
    open_interest  BIGINT,
    PRIMARY KEY (underlying, quote_ts, expiry, strike, opt_type)
);

-- ATM IV per day: nearest strike, first expiry with more than 14 days left
CREATE OR REPLACE VIEW v_atm_iv_daily AS
WITH c AS (
    SELECT underlying, quote_ts::date AS d, expiry, strike, iv, spot,
           ROW_NUMBER() OVER (PARTITION BY underlying, quote_ts::date
                              ORDER BY expiry, ABS(strike - spot)) AS rn
    FROM option_quotes
    WHERE expiry - quote_ts::date > 14 AND iv IS NOT NULL
)
SELECT underlying, d, expiry, strike, iv AS atm_iv
FROM c WHERE rn <= 2;                         -- call + put at the ATM strike

-- IV rank over the last 252 observations: (IV - min) / (max - min)
CREATE OR REPLACE VIEW v_iv_rank AS
WITH a AS (
    SELECT underlying, d, AVG(atm_iv) AS atm_iv FROM v_atm_iv_daily GROUP BY underlying, d
)
SELECT underlying, d, atm_iv,
       100 * (atm_iv - MIN(atm_iv) OVER w) / NULLIF(MAX(atm_iv) OVER w - MIN(atm_iv) OVER w, 0) AS iv_rank
FROM a
WINDOW w AS (PARTITION BY underlying ORDER BY d ROWS BETWEEN 251 PRECEDING AND CURRENT ROW);
