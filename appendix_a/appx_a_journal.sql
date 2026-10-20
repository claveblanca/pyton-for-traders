-- ============================================================================
-- appx_a_journal.sql  (PostgreSQL)
-- Ref: §A.9.2 (written trade journal), §A.2 (Table A.1 ceilings),
--      §A.10.1 (loss aversion), PROOF §A.13
-- Trade journal + R-multiples, disposition effect, sizing after streaks and
-- open exposure against the Appendix A ceilings. Can be pointed at
-- code_snippets/ch14's sim_trades instead (same columns, renamed in a view).
-- ============================================================================

CREATE TABLE IF NOT EXISTS trade_journal (
    trade_id      BIGSERIAL    PRIMARY KEY,
    symbol        VARCHAR(24)  NOT NULL,
    market        VARCHAR(32)  NOT NULL,          -- e.g. 'gold'
    market_group  VARCHAR(32)  NOT NULL,          -- e.g. 'metals' (sector ceiling)
    side          VARCHAR(5)   NOT NULL CHECK (side IN ('long', 'short')),
    entry_ts      TIMESTAMPTZ  NOT NULL,
    entry_px      NUMERIC      NOT NULL,
    stop_px       NUMERIC      NOT NULL,
    target_px     NUMERIC      NOT NULL,
    size          NUMERIC      NOT NULL,
    point_value   NUMERIC      NOT NULL DEFAULT 1,
    margin        NUMERIC,
    exit_ts       TIMESTAMPTZ,                    -- NULL while open
    exit_px       NUMERIC,
    rationale     TEXT,                           -- written AT entry (A.9.2)
    setup_tag     VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS account_equity (
    as_of   DATE    PRIMARY KEY,
    equity  NUMERIC NOT NULL
);

-- R-multiple and holding time per closed trade
CREATE OR REPLACE VIEW v_trade_r AS
SELECT trade_id, symbol, market, market_group, side, entry_ts, exit_ts,
       ABS(entry_px - stop_px) * size * point_value                                    AS risk,
       CASE side WHEN 'long' THEN exit_px - entry_px ELSE entry_px - exit_px END
           * size * point_value                                                        AS pnl,
       (CASE side WHEN 'long' THEN exit_px - entry_px ELSE entry_px - exit_px END)
           / NULLIF(ABS(entry_px - stop_px), 0)                                        AS r_multiple,
       EXTRACT(EPOCH FROM exit_ts - entry_ts) / 3600                                   AS hold_hours,
       COALESCE(TRIM(rationale), '') = ''                                              AS no_rationale
FROM trade_journal
WHERE exit_ts IS NOT NULL;

-- Disposition effect: losers held longer than winners = loss aversion (A.10.1)
CREATE OR REPLACE VIEW v_disposition AS
SELECT AVG(hold_hours) FILTER (WHERE pnl <= 0) / NULLIF(AVG(hold_hours) FILTER (WHERE pnl > 0), 0)
                                                        AS disposition_ratio,
       COUNT(*) FILTER (WHERE r_multiple < -1.1)        AS stop_overrides,
       AVG(no_rationale::int)                           AS no_rationale_share,
       AVG(r_multiple)                                  AS expectancy_r,
       AVG((pnl > 0)::int)                              AS win_rate
FROM v_trade_r;

-- Sizing after streaks of 2+ (A.3.3: shrink after losses, stay strict after wins)
CREATE OR REPLACE VIEW v_size_after_streak AS
WITH t AS (
    SELECT trade_id, entry_ts, risk, pnl > 0 AS win,
           LAG(pnl > 0, 1) OVER (ORDER BY entry_ts) AS w1,
           LAG(pnl > 0, 2) OVER (ORDER BY entry_ts) AS w2
    FROM v_trade_r
)
SELECT CASE WHEN w1 AND w2 THEN 'after_2_wins'
            WHEN NOT w1 AND NOT w2 THEN 'after_2_losses'
            ELSE 'mixed' END                    AS context,
       COUNT(*)                                 AS trades,
       AVG(risk) / (SELECT AVG(risk) FROM v_trade_r) AS risk_vs_average
FROM t
WHERE w2 IS NOT NULL
GROUP BY 1;

-- Open exposure against the ceilings (A.2, A.2.2)
CREATE OR REPLACE VIEW v_exposure_now AS
WITH eq AS (SELECT equity FROM account_equity ORDER BY as_of DESC LIMIT 1),
open_pos AS (
    SELECT market, market_group, margin,
           ABS(entry_px - stop_px) * size * point_value AS risk
    FROM trade_journal WHERE exit_ts IS NULL
)
SELECT 'total committed' AS scope, NULL::text AS name,
       SUM(margin) / (SELECT equity FROM eq) AS share, 0.50 AS ceiling
FROM open_pos
UNION ALL
SELECT 'market margin', market, SUM(margin) / (SELECT equity FROM eq), 0.15
FROM open_pos GROUP BY market
UNION ALL
SELECT 'market open risk', market, SUM(risk) / (SELECT equity FROM eq), 0.05
FROM open_pos GROUP BY market
UNION ALL
SELECT 'sector', market_group, SUM(margin) / (SELECT equity FROM eq), 0.25
FROM open_pos GROUP BY market_group;
