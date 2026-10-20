-- ============================================================================
-- ch06_cot.sql  (PostgreSQL)
-- Ref: PROOF §6.4.6 (Table 6.10 managed-money score), §6.2.8-6.2.9
--      (crypto ETN premium and coin flows, Listing 6.2)
-- ============================================================================

CREATE TABLE IF NOT EXISTS cot_disaggregated (
    report_date   DATE         NOT NULL,          -- Tuesday positions, published Friday
    market_code   VARCHAR(16)  NOT NULL,          -- CFTC contract market code
    commodity     VARCHAR(96)  NOT NULL,
    sector        VARCHAR(24),                    -- energy | precious_metals | industrial_metals | agriculture
    mm_long       BIGINT, mm_short    BIGINT,     -- managed money
    prod_long     BIGINT, prod_short  BIGINT,     -- producer/merchant
    swap_long     BIGINT, swap_short  BIGINT,     -- swap dealers
    open_interest BIGINT,
    PRIMARY KEY (report_date, market_code)
);

-- Percentile of the latest managed-money net position over 156 weeks
CREATE OR REPLACE VIEW v_mm_score AS
WITH net AS (
    SELECT report_date, market_code, commodity, sector, mm_long - mm_short AS mm_net,
           ROW_NUMBER() OVER (PARTITION BY market_code ORDER BY report_date DESC) AS age
    FROM cot_disaggregated
), hist AS (
    SELECT * FROM net WHERE age <= 156
), last_row AS (
    SELECT * FROM hist WHERE age = 1
)
SELECT l.market_code, l.commodity, l.sector, l.report_date, l.mm_net,
       ROUND(100.0 * AVG((h.mm_net < l.mm_net)::int), 0)          AS score,
       ROUND((l.mm_net - AVG(h.mm_net)) / NULLIF(STDDEV_SAMP(h.mm_net), 0), 2) AS z,
       CASE WHEN 100.0 * AVG((h.mm_net < l.mm_net)::int) >= 90 THEN 'crowded long'
            WHEN 100.0 * AVG((h.mm_net < l.mm_net)::int) <= 10 THEN 'crowded short'
            ELSE 'no positioning objection' END                   AS reading
FROM last_row l JOIN hist h USING (market_code)
GROUP BY l.market_code, l.commodity, l.sector, l.report_date, l.mm_net;

CREATE TABLE IF NOT EXISTS etn_daily (
    isin           CHAR(12)    NOT NULL,
    d              DATE        NOT NULL,
    close_ts       TIMESTAMPTZ NOT NULL,          -- the listing's close, not midnight UTC
    close          NUMERIC     NOT NULL,
    coin_per_note  NUMERIC     NOT NULL,          -- issuer's daily entitlement
    units          NUMERIC     NOT NULL,          -- notes outstanding
    spot_eur       NUMERIC     NOT NULL,          -- spot at close_ts
    PRIMARY KEY (isin, d)
);

CREATE OR REPLACE VIEW v_etn_premium_flow AS
SELECT isin, d,
       close / NULLIF(coin_per_note * spot_eur, 0) - 1                          AS premium,
       units * coin_per_note                                                    AS coins_held,
       units * coin_per_note - LAG(units * coin_per_note) OVER (PARTITION BY isin ORDER BY d)
                                                                                AS flow_coins
FROM etn_daily;
