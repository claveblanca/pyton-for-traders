|                                                             |
| ----------------------------------------------------------- |
| **PYTHON FOR TRADERS: INVESTING, DERIVATIVES, AND TECHNICAL ANALYSIS APPLIED** |

|           |       |
| --------- | ----- |
| Chapter 9 | **9** |

**Volume and Open Interest: The Secondary Indicators Price Alone Cannot Give You**

*Why volume must confirm a trend, how open interest reveals whether new money is entering or leaving, and what the COT report and put/call ratios add on top*

Part II — Technical Analysis · Prereqs: Chapter 8 (Technical Analysis Foundations, including §8.10 Python Quickstart for the OHLCV data layer this chapter's code assumes)

<table>
<thead>
<tr class="header">
<th><strong>THIS CHAPTER COVERS</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>9.1 Volume and Open Interest as Secondary Indicators</p>
<p>9.2 Open Interest Mechanics — How the Count Actually Changes</p>
<p>9.3 Interpreting Volume Across All Markets</p>
<p>9.4 On-Balance Volume and Its Limitations in Futures</p>
<p>9.5 Interpreting Open Interest in Futures</p>
<p>9.6 Open Interest at Trend Extremes and Consolidations</p>
<p>9.7 Blowoffs, Selling Climaxes, and the Commitments of Traders Report</p>
<p>9.8 Open Interest and Sentiment in Options</p>
<p>9.9 Reading the Volume/OBV Dashboard — Signals in Practice</p>
<p>9.10 [CODE] Hands-On — OBV and Selling Climaxes in Python and SQL</p>
<p>9.11 [PROOF] Reading Price, Volume, and Open Interest as One System</p></td>
</tr>
</tbody>
</table>

|                                                         |
| --------------------------------------------------------- |
| **9.1 VOLUME AND OPEN INTEREST AS SECONDARY INDICATORS** |

Price action is the primary source of technical data — everything in Chapter 8 is built on it directly. Volume and open interest are secondary indicators: they do not generate an independent forecast the way a trend or a moving average does, but they measure the intensity, liquidity, and underlying pressure behind whatever price is currently doing, and they can confirm or quietly undermine a price-based signal before that signal fails outright.

**9.1.1 Volume, defined.** The total number of shares or contracts traded during a specified time period. It measures the intensity or urgency of buyers and sellers — the same price move on high volume and on low volume is not the same event.

**9.1.2 Open interest, defined.** Used exclusively in futures and options, open interest represents the total number of outstanding, unliquidated contracts at the end of the trading day. Unlike volume, which resets to zero at the start of every new session, open interest is a running count that persists until a position is closed, offset, or expires.

**9.1.3 The reporting-lag caveat.** Official volume and open interest figures in futures markets are reported with a one-day lag — only an estimated volume is available for the current session. Any system reading these fields needs to account for this lag explicitly rather than treating the number as live.

| **◆ EDGE — Secondary does not mean optional**                                                                                                                                                                                                                                                            |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Secondary indicator" describes the order of analysis, not the order of importance. A trend signal that price alone appears to confirm can still be a weak or false signal if volume and open interest are pointing the other way — Sections 9.3 through 9.6 below are what turn a price-only read into a three-variable one. |

|                                                                    |
| ---------------------------------------------------------------------- |
| **9.2 OPEN INTEREST MECHANICS — HOW THE COUNT ACTUALLY CHANGES** |

Open interest changes — or doesn't — depending on whether each side of a given trade is opening a new position or closing an existing one. There are exactly four combinations, and only two of them move the count.

*Table 9.1 — The four open interest outcomes*

| **Buyer side**            | **Seller side**             | **Effect on open interest** |
| ----------------------------- | -------------------------------- | -------------------------------- |
| New buyer (opening)               | New seller (opening)                 | Increases (+1)                       |
| New buyer (opening)               | Old seller (liquidating/closing)       | Unchanged (0)                        |
| Old buyer (covering/closing)        | New seller (opening)                 | Unchanged (0)                        |
| Old buyer (covering/closing)        | Old seller (liquidating/closing)       | Decreases (-1)                       |

**9.2.1 Why this table is the foundation for everything that follows.** Every interpretation rule in Sections 9.5 and 9.6 — whether rising open interest means new money is entering or existing positions are simply being transferred — reduces to this table. Open interest only tells a directional story about capital flow when combined with the direction price is actually moving; on its own, a rising or falling count says only that positions in aggregate are opening or closing, not who is opening them or why.

|                                                         |
| ----------------------------------------------------------- |
| **9.3 INTERPRETING VOLUME ACROSS ALL MARKETS** |

**9.3.1 The general rule.** Volume should expand in the direction of the prevailing price trend. In an uptrend, volume should be heavier on advance days and lighter on corrective pullbacks. In a downtrend, volume should be heavier on decline days and lighter on technical bounces. A trend where volume behaves the opposite way — heavier on the corrective moves than on the trend moves — is a trend losing conviction, whether or not price has broken any visible level yet.

**9.3.2 Volume as pattern confirmation.** Breakouts from chart patterns — triangles, head and shoulders, rectangles — require heavy volume to be trusted as valid. A breakout on light volume is a warning sign of a potential false breakout, sometimes called a bull trap or bear trap: the pattern completed on the chart, but the participation behind it was not there to sustain the move.

| **⚠ WARNING — A clean pattern on light volume is not a clean signal**                                                                                                                                                                                                                                   |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| It is tempting to treat a textbook-looking breakout as sufficient on its own, especially once the pattern-recognition work is automated. Volume confirmation is not a redundant check — a mechanically perfect breakout on volume well below average is exactly the setup most likely to fail and reverse, precisely because the participation needed to sustain the move never showed up. |

|                                                                |
| ------------------------------------------------------------------ |
| **9.4 ON-BALANCE VOLUME AND ITS LIMITATIONS IN FUTURES** |

**9.4.1 What OBV is.** Developed by Joseph Granville, On-Balance Volume (OBV) is a running cumulative volume total: daily volume is added on up-close days and subtracted on down-close days. The result is a single line that should trend in the same direction as price if volume genuinely confirms the move.

**9.4.2 Divergence as the actionable signal.** A divergence between the OBV line and price — price making a new high while OBV fails to — is read as an early warning of an impending trend reversal. OBV's value is almost entirely in these divergences; when OBV simply tracks price with no divergence, it is confirming what price already showed rather than adding new information. Section 9.10.1 states the rule in code (Listings 9.1 and 9.2).

**9.4.3 The futures-specific limitation.** Locked limit days — sessions where price hits an exchange-imposed limit and trading effectively halts — produce artificially light volume purely because there is no counterparty available to trade against, not because genuine market interest is low. This can temporarily distort an OBV calculation despite the underlying move being one of extreme market strength or weakness. A locked-limit day should be flagged and treated differently from an ordinary low-volume session, not fed into OBV as if it were routine.

|                                                       |
| ----------------------------------------------------- |
| **9.5 INTERPRETING OPEN INTEREST IN FUTURES** |

Open interest indicates whether new capital is entering or leaving a market — and, combined with the direction price is moving, it distinguishes genuine trend conviction from a trend that is running on fumes.

*Table 9.2 — Price and open interest, combined*

| **Price**   | **Open interest** | **Reading**                                                   | **Bias**   |
| --------------- | ---------------------- | ------------------------------------------------------------------- | -------------- |
| Rising            | Rising                     | New money entering — aggressive new buying                            | Bullish            |
| Rising            | Falling                    | Money leaving — short covering by losing traders, not new buying       | Bearish             |
| Falling           | Rising                     | New money entering — aggressive new short selling                     | Bearish             |
| Falling           | Falling                    | Money leaving — long liquidation, not new selling pressure              | Bullish / stabilizing |

**9.5.1 Why "rising price, falling open interest" is the trap case.** This is the combination most likely to be mistaken for trend strength when it is actually the opposite: price is rising only because shorts are being forced to cover, not because new buyers believe in the move. Once the short-covering is exhausted, there is no fresh buying left to sustain the trend — which is exactly the mechanism behind the blowoff tops described in Section 9.7.

|                                                                     |
| ------------------------------------------------------------------- |
| **9.6 OPEN INTEREST AT TREND EXTREMES AND CONSOLIDATIONS** |

**9.6.1 Open interest as an early-warning fuel gauge.** A leveling-off or decline in open interest after a prolonged price trend is an early warning that the trend is running out of the capital needed to sustain it — even while price itself may still be making new highs or lows. This reading is available before the price trend visibly stalls, which is the entire point of tracking it as a leading rather than a coincident signal.

**9.6.2 Open interest during a consolidation.** High open interest built up during a sideways trading range indicates a large accumulation of positions on both sides of the market — a buildup of potential energy that fuels an explosive move once the range finally breaks. A quiet, narrow-range market with rising open interest underneath it is not a market to ignore; it is often a market storing up the fuel for its next real move.

|                                                                            |
| ----------------------------------------------------------------------------- |
| **9.7 BLOWOFFS, SELLING CLIMAXES, AND THE COMMITMENTS OF TRADERS REPORT** |

**9.7.1 Blowoff tops.** A blowoff top occurs at market highs when price suddenly surges on massive volume while open interest drops sharply — the Table 9.2 "rising price, falling open interest" case taken to its extreme, reflecting long profit-taking and short-side exhaustion happening simultaneously rather than genuine new demand.

**9.7.2 Selling climaxes.** A selling climax occurs at market lows on panic volume, typically followed by a rapid V-shaped recovery — the mirror image of a blowoff top, where capitulation selling exhausts itself abruptly rather than the decline continuing to grind lower. Section 9.10.2 states the test in code (Listings 9.3 and 9.4).

**9.7.3 The Commitments of Traders (COT) report.** Released by the CFTC, the COT report breaks down total open interest into three distinct groups of participants, each with a different informational value.

*Table 9.3 — COT report participant groups*

| **Group**                | **Who they are**                                          | **Interpretive value**                                  |
| ---------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- |
| Commercials (hedgers)             | The "smart money" operating in the physical commodity itself      | Treated as the most informed group — watched most closely        |
| Large speculators                   | Commodity funds and trend-following institutions                     | Typically positioned with the trend, often late in extremes         |
| Small speculators                    | Retail public traders                                                  | Typically the most extreme at market turning points, contrarian signal |

**9.7.4 The core COT rule — watch the commercials.** When commercials are heavily net long — an extreme bullish position for that group — while speculators are heavily net short, a major bullish buying opportunity is signaled. The reverse configuration — commercials heavily net short while speculators are heavily net long — warns of a major top. The logic depends on treating commercials, not speculators, as the informed side of the trade.

|                                                        |
| ------------------------------------------------------ |
| **9.8 OPEN INTEREST AND SENTIMENT IN OPTIONS** |

**9.8.1 Put/call ratios as contrary sentiment indicators.** The ratio of put volume (or put open interest) to call volume/open interest measures the balance of bearish to bullish options activity — and, read as a contrarian indicator, an extreme in either direction says more about crowd positioning than about where price is actually headed next.

**9.8.2 Reading the extremes.** A high put/call ratio reflects excessive public bearishness — read as a sign of an oversold market and a setup for a bullish turn, on the logic that once nearly everyone who wants to be bearish already is, there is limited fresh selling left to push price lower. A low put/call ratio reflects excessive public bullishness — read as an overbought market vulnerable to a decline, on the same contrarian logic in reverse.

**9.8.3 Combining option sentiment with the rest of the chapter.** A put/call extreme is strongest as a confirming signal alongside the price/volume/open-interest reads from Sections 9.3 through 9.6, not as a standalone trigger — an extreme put/call ratio arriving at the same time as a Section 9.6 open-interest fuel buildup is a materially stronger combined read than either indicator taken in isolation.

|                                                                     |
| -------------------------------------------------------------------- |
| **9.9 READING THE VOLUME/OBV DASHBOARD — SIGNALS IN PRACTICE** |

Sections 9.3 and 9.4 explained what volume and On-Balance Volume measure, and Section 9.10 builds the OBV line in code (Listing 9.1). This section puts both on a live chart, reads six months of one market through them, and turns the rules into explicit trigger conditions.

**9.9.1 The dashboard.** Figure 9.1 shows daily volume bars, shaded by up and down days, with their 20-day average, and underneath them the OBV line computed exactly as in Listing 9.1.

![Volume and OBV dashboard — BTC/USD daily, March to September 2026](../images/OBV_dashboard_BTC_2026-09_light.png)

*Figure 9.1 — Volume and OBV dashboard, BTC/USD daily, late March – mid-September 2026. Top: daily volume with its 20-day average (dashed). Bottom: OBV.*

Read the OBV line for its shape only. Its value depends entirely on where the calculation starts: the same market started one month earlier prints a completely different number. Direction, slope and divergences are the only information the line carries.

**9.9.2 Reading the chart.**

1. **Late March – mid-May: accumulation.** OBV climbs steadily on ordinary volume. More volume trades on up days than on down days, so buyers are in control (Section 9.3.1's general rule).
2. **Late May – early June: distribution.** OBV rolls over, then collapses. The early-June bars carry the largest down-day volume of the period, over four times the average: heavy, decisive selling.
3. **Late June – mid-August: stabilisation, then a flat line.** OBV bottoms, recovers slightly, and then goes flat for six weeks. No accumulation, no distribution: the volume picture of a trading range.
4. **Mid-August: a volume-confirmed breakout.** Up-day bars of roughly three times the average volume accompany the price breakout from about $64k to $78k, and OBV jumps to a new high for the window. Price, volume and OBV all agree.
5. **Late August – September: fading participation.** OBV peaks and then makes a series of lower highs, giving back about half of the August gain, while price holds a sideways range and even prints a marginal new high in early September. That is Section 9.4.2's bearish divergence in miniature.

The dashboard's own header still read "Volume confirms uptrend" at the end of the window. That label described August, not September: a static label is no substitute for reading the line's direction.

**9.9.3 The signal table.** Volume rarely initiates a trade on its own; it decides whether a price signal from Chapters 10–12 deserves to be trusted. Table 9.4 writes that decision as conditions that are either true on a bar or not.

*Table 9.4 — Volume and OBV trigger conditions*

| **Signal** | **Conditions (all must be true)** | **Action** |
| --- | --- | --- |
| **BUY (confirmed breakout)** | Close above the prior 20-day high **and** volume ≥ 1.5× its 20-day average **and** OBV above its own prior 20-day high | Take the long breakout |
| **SELL (confirmed breakdown)** | Close below the prior 20-day low **and** volume ≥ 1.5× average **and** OBV below its own prior 20-day low | Take the short, or exit longs |
| **EXIT / WARNING** | `obv_divergence` (Listing 9.1) flags a divergence against the open position, **or** a climax bar (Listing 9.3, Section 9.7) prints after an extended move | Tighten the stop, stop adding, or close |
| **STAND ASIDE** | Volume below its average and OBV flat | Treat breakouts as suspect; wait for a retest |

| **▲ WARNING — Four ways to misread a volume dashboard** |
| --- |
| Reading the OBV number: only its shape matters. Treating every volume spike as a climax: spikes at the *start* of a move (mid-August in Figure 9.1) confirm it; only spikes at the end of an extended move hint at exhaustion. Mixing volume sources: in crypto especially, a single exchange's volume is only part of the market, so use one consistent feed. Forgetting OBV's bluntness: a day that closes one dollar higher adds its whole volume, exactly like a day that closes three thousand dollars higher. |


|                                                                      |
| ---------------------------------------------------------------------- |
| **9.10 [CODE] HANDS-ON — OBV AND SELLING CLIMAXES IN PYTHON AND SQL** |

Two of this chapter's rules are mechanical enough to state as code: the OBV line with its divergence check, and the selling-climax test. Each comes twice, as a pandas function for backtesting and as a PostgreSQL view for a live database, and the two versions compute the same quantity.

**9.10.1 OBV and its divergence check (Sections 9.4.1–9.4.2).** The rule in Sections 9.4.1–9.4.2 reduces directly to a running signed-volume sum and a rolling high/low comparison — the listings below are a translation of that prose into a backtestable function and a live database view, not an approximation of it.

**💻 PYTHON · Listing 9.1 — `obv` and `obv_divergence`: the cumulative line and its one actionable signal**

```python
import numpy as np
import pandas as pd

def obv(df: pd.DataFrame) -> pd.Series:
    """On-Balance Volume: cumulative volume, added on up-close days,
    subtracted on down-close days, unchanged on flat-close days (9.4.1)."""
    direction = np.sign(df["close"].diff().fillna(0))
    signed_volume = direction * df["volume"]
    return signed_volume.cumsum().rename("obv")


def obv_divergence(df: pd.DataFrame, obv_series: pd.Series, lookback: int = 20) -> dict:
    """Divergence is OBV's actionable signal (9.4.2): price makes a new
    high/low over `lookback` bars while OBV fails to confirm it."""
    price_window = df["close"].tail(lookback)
    obv_window = obv_series.tail(lookback)

    price_new_high = price_window.iloc[-1] >= price_window.max()
    obv_confirms_high = obv_window.iloc[-1] >= obv_window.max()

    price_new_low = price_window.iloc[-1] <= price_window.min()
    obv_confirms_low = obv_window.iloc[-1] <= obv_window.min()

    return {
        "bearish_divergence": bool(price_new_high and not obv_confirms_high),
        "bullish_divergence": bool(price_new_low and not obv_confirms_low),
    }
```

**💻 SQL · Listing 9.2 — `stock_obv_daily`: the same formula as a running PostgreSQL view**

```sql
CREATE OR REPLACE VIEW stock_obv_daily AS
WITH signed AS (
    SELECT
        symbol,
        price_date,
        close,
        volume,
        CASE
            WHEN LAG(close) OVER w IS NULL THEN 0::bigint
            WHEN close > LAG(close) OVER w THEN volume
            WHEN close < LAG(close) OVER w THEN -volume
            ELSE 0::bigint
        END AS signed_volume
    FROM stock_daily_prices
    WHERE volume IS NOT NULL
    WINDOW w AS (PARTITION BY symbol ORDER BY price_date)
)
SELECT
    symbol, price_date, close, volume, signed_volume,
    SUM(signed_volume) OVER (
        PARTITION BY symbol ORDER BY price_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS obv
FROM signed;
```

| **▣ DATA — One formula, two engines**                                                                                                                                                                                                                                                                    |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Listing 9.1 and Listing 9.2 compute the identical quantity — a signed, cumulative volume sum keyed off the sign of each day's close-to-close change — once as a pandas function for backtesting, once as a live PostgreSQL view queried by the production system. Keeping the two in sync, rather than letting the SQL drift into an informal reimplementation, is what makes a backtested OBV divergence rule and a live OBV divergence alert the same rule rather than two rules that happen to share a name. |

**9.10.2 Selling climaxes (Section 9.7.2).** A climax is a volume spike — relative to the symbol's own trailing volume distribution — landing on a down day. No open-interest condition is attached here, unlike the blowoff-top case in 9.7.1: panic volume on a down day is the climax's defining, checkable feature, and the V-shaped recovery is only confirmed in hindsight, on the bars that follow.

**💻 PYTHON · Listing 9.3 — `detect_selling_climax`: a volume z-score spike on a down day**

```python
def detect_selling_climax(df: pd.DataFrame, volume_zscore_window: int = 60,
                           volume_zscore_threshold: float = 2.0) -> pd.Series:
    vol_mean = df["volume"].rolling(volume_zscore_window).mean()
    vol_std = df["volume"].rolling(volume_zscore_window).std()
    vol_z = (df["volume"] - vol_mean) / vol_std

    price_down = df["close"].diff() < 0

    flag = (vol_z >= volume_zscore_threshold) & price_down
    return flag.rename("selling_climax")
```

**💻 SQL · Listing 9.4 — `stock_selling_climax_daily`: the same z-score-and-down-day test as a view**

```sql
CREATE OR REPLACE VIEW stock_selling_climax_daily AS
SELECT
    symbol, price_date, close, volume,
    (volume::numeric - vol_mean60) / NULLIF(vol_std60, 0) AS volume_zscore,
    (
        vol_window_count >= 60
        AND vol_std60 > 0
        AND (volume::numeric - vol_mean60) / vol_std60 >= 2.0
        AND chg < 0
    ) AS selling_climax
FROM stock_volume_daily;
```

`stock_volume_daily` (Listing 9.4's source view) rolls `vol_mean60`/`vol_std60` over the trailing 60 bars the same way Listing 9.3's `.rolling(volume_zscore_window)` does — the z-score threshold of 2.0 is the same default in both.

The PROOF that follows treats these flags as inputs, not as signals in their own right: volume decides whether a price signal deserves trust.

|                                                                        |
| ------------------------------------------------------------------------ |
| **9.11 [PROOF] READING PRICE, VOLUME, AND OPEN INTEREST AS ONE SYSTEM** |

<table>
<thead>
<tr class="header">
<th><strong>▶ PROOF — Four checks before trusting a price-only signal</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>Check whether volume is expanding in the direction of the move, per Section 9.3.1. A trend or breakout with volume weaker on the trend days than on the counter-trend days is not confirmed, regardless of how clean the price pattern looks.</p>
<p>Run the Section 9.5 price/open-interest matrix before reading a price move as trend strength. "Rising price, falling open interest" specifically should be downgraded from bullish continuation to short-covering until proven otherwise -- it is the single most commonly misread combination in this chapter.</p>
<p>Check open interest for the Section 9.6 fuel-gauge pattern before assuming a trend still has room to run, and check it for the consolidation buildup pattern before assuming a quiet range will stay quiet.</p>
<p>Where futures COT data or options put/call data is available, check it against the price/volume/open-interest read rather than in isolation -- Section 9.7's "watch the commercials" rule and Section 9.8's put/call extremes are corroborating evidence, not a replacement for the price-based read.</p>
<p>A signal confirmed by volume, open interest, and (where available) COT or put/call positioning is being read as one integrated system -- not as four separate, potentially conflicting indicators picked one at a time.</p></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td><p><strong>◈ KEY INSIGHT<br />
</strong></p>
<p><em>"Price tells you what happened. Volume and open interest tell you who was behind it, and whether they're still there. A price move nobody is actually behind is the one most likely to stop -- which is exactly why blowoffs and selling climaxes exist as named patterns in the first place."</em></p></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><strong>CHAPTER SUMMARY</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>Volume and open interest are secondary indicators -- they don't generate an independent forecast, but they measure the intensity and capital flow behind whatever price is already doing, and can confirm or undermine a price-based signal.</p>
<p>Open interest only increases or decreases when a new position is opened or an old one is closed on both sides of a trade -- two of the four buyer/seller combinations leave it unchanged.</p>
<p>Volume should expand in the direction of the prevailing trend; pattern breakouts on light volume are a false-breakout warning, not a confirmed signal.</p>
<p>On-Balance Volume's divergences from price are an early warning of trend reversal, but futures locked-limit days can distort it with artificially light volume unrelated to genuine market conviction.</p>
<p>Combining price direction with open-interest direction distinguishes real trend conviction (rising price, rising open interest) from a trend running on fumes (rising price, falling open interest is short covering, not new buying).</p>
<p>A leveling-off of open interest after a long trend warns the trend is running out of fuel before price confirms it; high open interest built during a consolidation fuels the eventual breakout.</p>
<p>Blowoff tops and selling climaxes are the extreme cases of the price/open-interest matrix; the COT report's "watch the commercials" rule and options put/call ratios add corroborating, contrarian-sentiment evidence on top.</p>
<p>Section 9.9 turns the volume rules into triggers: a breakout counts only on at least 1.5× average volume with OBV at a new high, divergence and climax bars are exit warnings, and flat OBV on thin volume means stand aside — Figure 9.1 shows the full accumulation–distribution–breakout–fade cycle on BTC/USD.</p></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><strong>KEY TERMS</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p><strong>Volume</strong> Total shares or contracts traded during a specified period; measures the intensity of buying/selling.</p>
<p><strong>Open interest</strong> Total outstanding, unliquidated futures or options contracts at the end of a session; a running count, not a per-session total.</p>
<p><strong>On-Balance Volume (OBV)</strong> A running cumulative volume total, added on up-close days and subtracted on down-close days.</p>
<p><strong>Divergence</strong> Price and an indicator (e.g. OBV) moving in opposite directions -- an early warning of a potential reversal.</p>
<p><strong>Locked limit day</strong> A futures session where price hits an exchange-imposed limit and trading effectively halts, artificially suppressing volume.</p>
<p><strong>Blowoff top</strong> A market-high surge on massive volume with sharply falling open interest -- profit-taking and short exhaustion, not new demand.</p>
<p><strong>Selling climax</strong> A market-low panic-volume decline typically followed by a rapid V-shaped recovery.</p>
<p><strong>Commitments of Traders (COT) report</strong> A CFTC report breaking down open interest into commercials, large speculators, and small speculators.</p>
<p><strong>Commercials</strong> Hedgers operating in the physical commodity; treated as the most informed COT group.</p>
<p><strong>Put/call ratio</strong> Put volume or open interest divided by call volume or open interest; used as a contrarian sentiment indicator.</p>
<p><strong>Short covering</strong> Buying to close an existing short position -- can push price up without reflecting new bullish conviction.</p>
<p><strong>Long liquidation</strong> Selling to close an existing long position -- can push price down without reflecting new bearish conviction.</p>
<p><strong>Volume-confirmed breakout</strong> A price breakout accompanied by volume of at least 1.5–2× its average and a new high (or low) in OBV; breakouts on thin volume are treated as suspect.</p></td>
</tr>
</tbody>
</table>

| **WHAT'S NEXT**                                                                                                                                                                                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Chapter 10 — Moving Averages. This chapter added the volume, open-interest, and sentiment layers that confirm or undermine a price-based read; the next chapter turns to how moving averages construct that price-based signal in the first place, now with a volume/open-interest lens already in hand to judge it critically from the start. |


---

*Source: Restructured from `writing_plans/chapter_7_summary.md`, condensing source material on volume and open interest into this project's house style (opening block, THIS CHAPTER COVERS, numbered N.x sections and sub-sections, data tables, EDGE/WARNING/PROOF callouts, KEY INSIGHT, Chapter Summary, Key Terms, What's Next). Code listings 12.1-12.2 (originally 3.1-3.2, added in a later pass -- see the dated note below) are simplified extracts from this project's own rules module and the production PostgreSQL views `stock_obv_daily` and `stock_selling_climax_daily` in the user's separate `datacollect` repository.*

**Updated 2026-09-20** (original numbering) — added the four code listings (originally 3.1-3.4, now 12.1-12.4) to the On-Balance Volume and selling-climax sections, departing from this chapter's original prose-only decision. Coverage is deliberately limited to the two Tier-1, OHLCV-only rules (OBV/divergence and selling climax) the real data pipeline supports; blowoff tops, the open-interest fuel-gauge/consolidation checks, the COT report rule, and put/call sentiment remain prose only, since their data pipelines are not yet built.

**Updated 2026-09-22** — this chapter was renamed and renumbered from its original standalone draft slot ("Chapter 3") to Chapter 12 in this project's book, per user request ("shift right this chapters (chapter 3 should become chapter12)"), alongside three companion chapters shifting the same +9: Moving Averages (4 -> 13), Oscillators and Contrary Opinion (5 -> 14), and ADX and Directional Movement (6 -> 15). All internal section, table, and listing references were renumbered from 3.x to 12.x throughout. This chapter now sits in Part IV — Technical Analysis, immediately after Chapter 11 (Technical Analysis Foundations); its Prereqs were updated to "Ch 11 (Technical Analysis Foundations)" since that chapter's content is this project's integration of the same draft's own "Chapter 1." The draft's other stated prereq, "Chapter 2 (Markets, Instruments & Data)," has no corresponding chapter in this project yet -- flagged rather than guessed at, since inventing a chapter number for content that doesn't exist here would be worse than leaving the gap explicit. WHAT'S NEXT was updated to point to Chapter 13 (Moving Averages), the next chapter in this same renumbering batch.

**Updated 2026-09-22 (2)** -- the Prereqs line was updated to point at Chapter 11's new §11.11 (Python Quickstart), which now supplies the OHLCV data-fetch code (Kraken/yfinance) this chapter's Listing 12.1-12.4 functions assume as their input, resolving the previously-flagged "Markets, Instruments & Data prereq not yet integrated" gap noted in the note above.

**Updated 2026-09-24** — added Section 12.9 (dashboard reading and trigger table, adapted from `writing_plans/*_Trading_Guide.md`), with Figure 12.1 and Table 12.4; the PROOF section was renumbered 12.9 → 12.10 (THIS CHAPTER COVERS, cross-references, Chapter Summary and Key Terms updated). Images live in `content_md/images/` (light-gray conversions of the BTC/USD dashboard screenshots; flagged for replacement by print-ready grayscale charts at 300 dpi).

**Updated 2026-10-03** -- Dividend Investing (formerly Chapter 6) was removed from the manuscript; Chapters 7-15 shifted down by one to 6-14. All internal section, table, listing and figure numbers and cross-chapter references in the body were decremented accordingly. Historical dated notes above are left as written.

**Updated 2026-10-06** — Renumbered from Chapter 11 to Chapter 12 after Chapter 2 (Exchange Traded Products) was split into Chapter 2 (ETFs) and Chapter 3 (ETCs and ETNs). Section, subsection, table, figure and listing numbers, the header digit box, Prereqs and cross-chapter references updated; dated notes above keep the numbering of their time.

**Updated 2026-10-06 (c)** — Part label aligned with `.claude/CLAUDE.md` §3.3: Part I — Investing and Stock Market (Ch 1–9), Part II — Technical Analysis (Ch 10–15); "opens/closes Part …" sentences adjusted.

**Updated 2026-10-06 (e)** — Cross-references updated after Futures Trading moved to Chapter 3 and ETCs/ETNs to Chapter 4 (old Ch 3–6 → 4–7).

**Updated 2026-10-07** — Renumbered (−1) after Bonds and Intermarket Analysis were merged into Chapter 6 (Bonds and the Intermarket Chain); section, table, figure and listing numbers and cross-references updated.

**Updated 2026-10-07 (c)** — Prereqs line normalised to "Chapter N (…)".
