-- ============================================================================
-- ch02_fundamentals.sql  (PostgreSQL)
-- Ref: §2.3.1-2.3.3, §2.4.1, Table 2.2, PROOF §2.9.4 (CFI trend since 2013)
-- Annual fundamentals + the negative-filter and CAPE-style P/E views, so the
-- Ch 2 screen re-runs without re-downloading and trends are a query.
-- Sign convention as ch02_data.py: capex and dividends NEGATIVE, interest
-- expense POSITIVE.
-- ============================================================================

CREATE TABLE IF NOT EXISTS fundamentals_annual (
    symbol               VARCHAR(16)  NOT NULL,
    fiscal_year          SMALLINT     NOT NULL,
    revenue              NUMERIC,
    ebit                 NUMERIC,
    net_income           NUMERIC,
    cfo                  NUMERIC,
    capex                NUMERIC,      -- negative
    d_and_a              NUMERIC,
    interest_expense     NUMERIC,      -- positive
    total_liabilities    NUMERIC,
    total_assets         NUMERIC,
    intangibles          NUMERIC,      -- goodwill + other intangibles
    current_assets       NUMERIC,
    current_liabilities  NUMERIC,
    receivables          NUMERIC,
    inventory            NUMERIC,
    dividends_paid       NUMERIC,      -- negative
    diluted_shares       NUMERIC,
    source               VARCHAR(16)  DEFAULT 'edgar',
    loaded_at            TIMESTAMPTZ  NOT NULL DEFAULT now(),
    PRIMARY KEY (symbol, fiscal_year)
);

-- Daily prices: same table Ch 9 Listing 9.2 reads.
CREATE TABLE IF NOT EXISTS stock_daily_prices (
    symbol      VARCHAR(16) NOT NULL,
    price_date  DATE        NOT NULL,
    open        NUMERIC, high NUMERIC, low NUMERIC, close NUMERIC,
    volume      BIGINT,
    PRIMARY KEY (symbol, price_date)
);

-- Stage 1 negative filters, 7-year pooled (§2.3.1-2.3.3)
CREATE OR REPLACE VIEW v_negative_filters AS
SELECT
    symbol,
    fiscal_year,
    total_liabilities / NULLIF(total_assets - COALESCE(intangibles, 0), 0)        AS debt_ratio,
    SUM(ebit)       OVER w7 / NULLIF(SUM(interest_expense) OVER w7, 0)            AS coverage_7y,
    SUM(cfo)        OVER w7 / NULLIF(SUM(net_income) OVER w7, 0)                  AS cfi_7y,
    cfo / NULLIF(net_income, 0)                                                   AS cfi_year,
    current_assets / NULLIF(current_liabilities, 0)                               AS current_ratio,
    cfo + capex                                                                   AS fcf,
    capex * -1 / NULLIF(d_and_a, 0)                                               AS capex_to_da,
    COUNT(*)        OVER w7                                                       AS years_in_window
FROM fundamentals_annual
WINDOW w7 AS (PARTITION BY symbol ORDER BY fiscal_year ROWS BETWEEN 6 PRECEDING AND CURRENT ROW);

-- Stage 3 valuation: latest close against 7-year average EPS (§2.4.1-2.4.2)
CREATE OR REPLACE VIEW v_cape_pe AS
WITH last_px AS (
    SELECT DISTINCT ON (symbol) symbol, price_date, close
    FROM stock_daily_prices ORDER BY symbol, price_date DESC
), cyc AS (
    SELECT symbol, fiscal_year, diluted_shares,
           AVG(net_income) OVER (PARTITION BY symbol ORDER BY fiscal_year
                                 ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS avg_ni_7y,
           ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY fiscal_year DESC) AS rn
    FROM fundamentals_annual
)
SELECT c.symbol, c.fiscal_year, p.price_date, p.close,
       p.close * c.diluted_shares / NULLIF(c.avg_ni_7y, 0)          AS cape_pe,
       16 * c.avg_ni_7y / NULLIF(c.diluted_shares, 0)               AS fair_price_16x,
       (16 * c.avg_ni_7y / NULLIF(c.diluted_shares, 0) - p.close) / p.close AS margin_of_safety
FROM cyc c JOIN last_px p USING (symbol)
WHERE c.rn = 1;

-- One row per symbol: the §2.9 screening stage
CREATE OR REPLACE VIEW v_screen_stage AS
SELECT n.symbol, n.fiscal_year, n.debt_ratio, n.coverage_7y, n.cfi_7y, v.cape_pe,
       v.fair_price_16x, v.margin_of_safety,
       CASE WHEN n.debt_ratio > 0.60 OR n.coverage_7y < 3 OR n.cfi_7y < 1 THEN 'rejected_stage_1'
            WHEN v.cape_pe > 16 THEN 'fails_valuation'
            ELSE 'candidate' END AS stage
FROM v_negative_filters n
JOIN v_cape_pe v ON v.symbol = n.symbol AND v.fiscal_year = n.fiscal_year;
