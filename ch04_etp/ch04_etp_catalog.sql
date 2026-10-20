-- ============================================================================
-- ch04_etp_catalog.sql  (PostgreSQL)
-- Ref: §4.1.2 (instrument sheet), §4.4.5 (spread sources), §4.4.8 (monthly
--      monitoring), Ch 6 §6.2.7 DATA box (the `collateral` field)
-- Product catalog + spread observations -> monthly ICS and ranking within
-- the same underlying index (the ICS only compares like with like, §4.4.3).
-- ============================================================================

CREATE TABLE IF NOT EXISTS etp_products (
    isin             CHAR(12)     PRIMARY KEY,
    ticker           VARCHAR(16)  NOT NULL,
    exchange         VARCHAR(16)  NOT NULL,
    family           VARCHAR(3)   NOT NULL CHECK (family IN ('ETF', 'ETC', 'ETN')),
    underlying_index VARCHAR(64)  NOT NULL,
    replication      VARCHAR(24)  NOT NULL,   -- full_physical | sampled | synthetic_unfunded | synthetic_funded | physical
    collateral       VARCHAR(24),             -- physical | swap_collateralized | unsecured (Ch 6 Table 6.6)
    ter_pct          NUMERIC(6,3) NOT NULL,   -- from the KID (ongoing charges)
    currency         CHAR(3),
    hedged           BOOLEAN      DEFAULT FALSE,
    distribution     VARCHAR(4)   CHECK (distribution IN ('acc', 'dist')),
    aum_eur          NUMERIC,
    inception        DATE
);

CREATE TABLE IF NOT EXISTS etp_spread_obs (
    isin        CHAR(12)    NOT NULL REFERENCES etp_products(isin),
    obs_ts      TIMESTAMPTZ NOT NULL,
    bid         NUMERIC     NOT NULL,
    ask         NUMERIC     NOT NULL,
    source      VARCHAR(24) NOT NULL,      -- 'xlm' | 'borsa_monthly' | 'euronext' | 'live'
    PRIMARY KEY (isin, obs_ts, source)
);

-- Monthly average relative spread and ICS (TER + 2 x spread), §4.4
CREATE OR REPLACE VIEW v_ics_monthly AS
SELECT p.isin, p.ticker, p.underlying_index,
       date_trunc('month', o.obs_ts)::date                                   AS month,
       COUNT(*)                                                               AS n_obs,
       AVG((o.ask - o.bid) / ((o.ask + o.bid) / 2) * 100)                     AS spread_pct,
       p.ter_pct + 2 * AVG((o.ask - o.bid) / ((o.ask + o.bid) / 2) * 100)     AS ics_pct
FROM etp_products p
JOIN etp_spread_obs o USING (isin)
GROUP BY p.isin, p.ticker, p.underlying_index, date_trunc('month', o.obs_ts), p.ter_pct;

-- Rank within the same underlying, latest month; flag the §4.4.8 triggers
CREATE OR REPLACE VIEW v_ics_rank AS
WITH m AS (
    SELECT v.*,
           LAG(spread_pct) OVER (PARTITION BY isin ORDER BY month) AS prev_spread_pct,
           ROW_NUMBER()    OVER (PARTITION BY isin ORDER BY month DESC) AS rn
    FROM v_ics_monthly v
)
SELECT m.underlying_index, m.isin, m.ticker, m.month, m.spread_pct, m.ics_pct,
       RANK() OVER (PARTITION BY m.underlying_index ORDER BY m.ics_pct)        AS ics_rank,
       m.spread_pct > 1.5 * m.prev_spread_pct                                  AS spread_widened_50pct,
       p.aum_eur < 50000000                                                    AS small_fund_delisting_risk
FROM m JOIN etp_products p USING (isin)
WHERE m.rn = 1;
