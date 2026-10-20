|                                                             |
| ----------------------------------------------------------- |
| **PYTHON FOR TRADERS: INVESTING, DERIVATIVES, AND TECHNICAL ANALYSIS APPLIED** |

|           |       |
| --------- | ----- |
| Chapter 8 | **8** |

**Technical Analysis Foundations: Philosophy, Dow Theory, Charts, and Trend**

*Why price action is treated as sufficient evidence, and the vocabulary — Dow Theory, chart construction, trend, support/resistance — every later chapter assumes you already have*

Part II — Technical Analysis · Prereqs: Chapter 1 (Investment Classes and Instruments)

<table>
<thead>
<tr class="header">
<th><strong>THIS CHAPTER COVERS</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>8.1 The Philosophy of Technical Analysis — Three Premises</p>
<p>8.2 Technical vs. Fundamental Analysis, and the Problem of Timing</p>
<p>8.3 Flexibility Across Markets and Timeframes</p>
<p>8.4 Answering the Critics — Self-Fulfilling Prophecy and Random Walk</p>
<p>8.5 Dow Theory — The Six Basic Tenets</p>
<p>8.6 Chart Construction — Types, Scales, Volume, and Open Interest</p>
<p>8.7 Basic Concepts of Trend — Direction, Classification, Support and Resistance</p>
<p>8.8 Trendlines, Channels, and Percentage Retracements</p>
<p>8.9 Reversal Days and Price Gaps</p>
<p>8.10 [CODE] Hands-On — Pulling Your First Live Market Data</p>
<p>8.11 [PROOF] Reading a Chart Without Skipping a Premise</p></td>
</tr>
</tbody>
</table>

|                                                     |
| ------------------------------------------------------- |
| **8.1 THE PHILOSOPHY OF TECHNICAL ANALYSIS — THREE PREMISES** |

Technical analysis is the study of market action — primarily through charts — for the purpose of forecasting future price trends. Everything downstream of this chapter, including every Python signal built later in this book, rests on three premises treated as foundational rather than optional.

**8.1.1 Market action discounts everything.** Any factor capable of affecting price — economic, political, psychological, or fundamental — is automatically reflected in the price itself. The chartist's position is that price action reflects the net result of shifting supply and demand, whatever is driving that shift.

**8.1.2 Prices move in trends.** Price action moves in directional trends that tend to persist over time — a trend in motion is more likely to continue than to reverse. This premise alone is what justifies trend-following as a category of strategy at all; without it, chasing a moving average crossover would be no better than chasing noise.

**8.1.3 History repeats itself.** Human psychology drives market dynamics, and because psychological patterns remain consistent over time, recognizable chart patterns recur and reveal market sentiment. A pattern is not treated as predictive because of its shape — it is treated as predictive because the crowd behavior that produces the shape tends to recur.

| **◆ EDGE — The three premises are a chain, not three separate claims**                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| If price already discounts everything (8.1.1), then price action is a sufficient object of study on its own. If prices then move in trends rather than randomly (8.1.2), a trend once identified has some persistence to trade. If history repeats (8.1.3), the trader has a way to recognize that a trend or pattern is forming before it completes. Each premise depends on the one before it — reject any single one and the case for chart-based trading weakens accordingly. |

|                                                              |
| ------------------------------------------------------------ |
| **8.2 TECHNICAL VS. FUNDAMENTAL ANALYSIS, AND THE PROBLEM OF TIMING** |

**8.2.1 Two different questions.** Fundamental analysis examines economic factors — earnings, interest rates, supply/demand data — to determine intrinsic value: what *should* an asset be worth? Technical analysis focuses directly on price action and market reaction: what *is* the market actually doing right now, regardless of what it should be doing?

**8.2.2 Price as a leading indicator.** Price action often moves ahead of the fundamentals that will eventually justify it, reacting to unknown or unannounced developments before they appear in official data. A chartist does not need to know *why* informed money is buying to notice *that* it is buying.

**8.2.3 Timing is a problem fundamentals cannot solve.** Being fundamentally right about a company or a market says nothing about when to enter or exit — and in a leveraged instrument, entering a correct thesis at the wrong moment can still produce a loss large enough to be forced out before the thesis plays out. Technical analysis exists specifically to answer the timing question that fundamental analysis leaves open.

|                                                     |
| ------------------------------------------------------- |
| **8.3 FLEXIBILITY ACROSS MARKETS AND TIMEFRAMES** |

**8.3.1 Universal principles, not market-specific rules.** Technical principles apply across every financial medium — stocks, futures, currencies, commodities — and across every timeframe, from tick data to intraday to daily, weekly, and monthly charts. The same trend, support/resistance, and pattern concepts developed in this chapter are used unchanged whether the underlying is a single equity or a currency pair.

**8.3.2 Capital rotation as a consequence of flexibility.** Because the same toolkit applies everywhere, a chartist can rotate attention and capital toward whichever markets are currently trending — "hot" markets — while ignoring markets that are lateral and non-trending, rather than being tied to one instrument regardless of whether it is currently offering anything tradeable.

**8.3.3 Commodities as a macro leading indicator.** Commodity price trends themselves serve as leading indicators for macroeconomic factors such as inflation and interest rates — a theme this book's later chapters on intermarket relationships build on directly.

|                                                                     |
| ------------------------------------------------------------------- |
| **8.4 ANSWERING THE CRITICS — SELF-FULFILLING PROPHECY AND RANDOM WALK** |

**8.4.1 The self-fulfilling prophecy objection.** Critics argue that widespread chart usage causes technical patterns to form simply because enough traders are watching for them and acting in concert — the pattern "works" only because everyone expects it to. The counter-argument is that technical patterns are objective reflections of underlying supply/demand dynamics, and that traders act independently, across different timeframes and different strategies, which undercuts the idea of a single coordinated crowd producing the pattern artificially.

**8.4.2 Random walk theory.** Proponents of random walk theory claim that price changes are statistically independent from one period to the next — that there is no exploitable memory in price series at all. Technical analysis's answer is empirical: markets demonstrably trend and persist over extended periods, which is inconsistent with pure statistical randomness. This is also the claim later chapters in this book test directly with hypothesis testing, rather than simply asserting.

| **⚠ WARNING — "Disproving randomness" is not the same as "any pattern you see is real"**                                                                                                                                                                                                              |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The counter to random walk theory establishes that markets trend on average, not that every pattern a chartist believes they see is a genuine, tradeable edge. The distinction matters throughout the rest of this book: the [PROOF] discipline in later chapters exists precisely because "markets aren't purely random" is a much weaker claim than "this specific pattern predicts returns." |

|                                                |
| ---------------------------------------------- |
| **8.5 DOW THEORY — THE SIX BASIC TENETS** |

Formulated by Charles Dow and refined by William Peter Hamilton and Robert Rhea, Dow Theory is treated as the cornerstone of modern technical analysis — most of the vocabulary in the rest of this chapter descends directly from it.

*Table 8.1 — The six tenets of Dow Theory*

| **#** | **Tenet**                          | **Core claim**                                                               |
| ------- | -------------------------------------- | ----------------------------------------------------------------------------------- |
| 1         | The averages discount everything          | All market knowledge, expectations, and fundamentals are reflected in the averages       |
| 2         | The market has three trends               | Primary (over 1 year), Secondary (3 weeks–3 months), Minor (under 3 weeks)               |
| 3         | Major trends have three phases            | Accumulation (informed buying), Public Participation (trend-following), Distribution (early buyers sell to the public) |
| 4         | The averages must confirm each other      | A trend is not confirmed unless multiple averages (e.g. industrials and transports) reach new highs/lows together |
| 5         | Volume must confirm the trend             | Volume expands in the direction of the primary trend                                     |
| 6         | A trend is assumed in effect until reversed | Price action is presumed to continue until a clear, definitive signal proves otherwise   |

**8.5.1 Why the three-phase structure (Tenet 3) matters practically.** The accumulation phase is invisible to most participants — it happens while news is still bad and sentiment is still poor, which is exactly why it is available only to traders willing to act against the prevailing mood. By the distribution phase, the news is good, volume is high, and participation is widest — which is also when the earliest, best-informed buyers are selling into that demand. Recognizing which phase a trend is in is a recurring practical question, not just historical color.

**8.5.2 Closing prices, not intraday extremes.** Dow Theory focuses primarily on closing prices, treating intraday highs and lows as minor noise relative to where the market actually settled for the session. This is a deliberate simplification, and it is the same reasoning OHLCV-based analysis throughout this book inherits: the close is the single most information-dense, least noisy field in a candle.

**8.5.3 Line formations.** A sideways consolidation range — a "line" in Dow's terminology — represents an accumulation or distribution phase in progress, not a market doing nothing. The absence of directional movement is itself informative.

**8.5.4 Applicability to futures.** Despite the shorter contract lifespans and different mechanics of futures relative to the industrial-average context Dow originally worked in, the core Dow Theory concepts remain valid for tracking underlying trend direction.

|                                                                         |
| ------------------------------------------------------------------------ |
| **8.6 CHART CONSTRUCTION — TYPES, SCALES, VOLUME, AND OPEN INTEREST** |

**8.6.1 The four chart types.** Each chart type trades off information density against readability, and each remains in use for a different reason.

*Table 8.2 — Chart types and what each one shows*

| **Chart type**       | **What it plots**                                                     |
| ------------------------ | ----------------------------------------------------------------------------- |
| Line chart                  | Connects single price points (usually closes) over time — simplest, least information-dense |
| Bar chart                     | Plots High, Low, Open (left tick), and Close (right tick) for each period          |
| Point & figure chart           | Alternating columns of X's (rising) and O's (falling), filtering out time entirely to focus purely on price moves |
| Candlestick chart               | A "real body" between Open and Close, with upper/lower shadows showing the High and Low |

**8.6.2 Arithmetic vs. logarithmic scale.** On an arithmetic scale, vertical distance represents equal dollar increments — a move from $10 to $15 occupies the same visual distance as $100 to $105, even though the second move is proportionally far smaller. On a logarithmic (ratio) scale, equal vertical distances represent equal *percentage* changes instead — a move from $10 to $20 (a 100% gain) occupies the same distance as $50 to $100. Logarithmic scaling is essential for any long-term trend analysis, precisely because it prevents large absolute-dollar moves late in a trend from visually dwarfing proportionally identical moves earlier in it.

**8.6.3 Volume.** The total number of shares or contracts traded during a specific period, conventionally plotted as vertical bars beneath the price chart. Volume is the confirming variable behind Dow's Tenet 5 — a price move on rising volume carries more weight than the same move on falling volume.

**8.6.4 Open interest.** Used exclusively in futures and options, open interest measures the total number of outstanding, unliquidated contracts. Total open interest across all contract months is what gets plotted and analyzed — not any single contract month in isolation — specifically to avoid the distortions that contract expiration and rollover would otherwise introduce into the series.

**8.6.5 Weekly and monthly bar charts.** Compressing multiple years of daily data into weekly or monthly bars strips away short-term noise and reveals major long-term trends and multi-decade support/resistance structures that are simply invisible at daily resolution — the same "choose the timeframe that matches the question" logic this book applies later when selecting bar sizes for a given strategy.

|                                                                                    |
| ------------------------------------------------------------------------------------- |
| **8.7 BASIC CONCEPTS OF TREND — DIRECTION, CLASSIFICATION, SUPPORT AND RESISTANCE** |

**8.7.1 Trend has three directions.** A trend is defined mechanically as a series of ascending or descending peaks and troughs — not by slope alone, but by the sequence of highs and lows. An uptrend shows ascending peaks and troughs; a downtrend shows descending peaks and troughs; a sideways (trendless) market shows roughly horizontal peaks and troughs. Trend-following systems are specifically weak during sideways phases — a fact worth remembering before applying a trend-following signal indiscriminately.

**8.7.2 Trend has three classifications.** The same Major (over 1 year), Secondary (3 weeks to 3 months), and Near-term (under 3 weeks) buckets introduced under Dow Theory in Section 8.5 apply generally to trend classification, independent of which specific averages or instruments are being analyzed.

**8.7.3 Support and resistance.** Support is a trough — a buying floor below the current market — where buying pressure has historically overcome selling pressure and halted a decline. Resistance is a peak — a selling ceiling above the current market — where selling pressure has historically overcome buying pressure and halted an advance.

**8.7.4 Role reversal.** Once a support level is decisively broken, it reverses roles and becomes resistance on subsequent rallies; a penetrated resistance level likewise becomes support. This role-reversal behavior is one of the most consistently observed patterns in price structure, and it is the mechanism behind the common "re-test of the breakout level" setup.

| **▣ DATA — Degree of penetration matters, not just direction**                                                                                                                                                                                                                                          |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A support or resistance level is not "broken" by any close on the wrong side of it by any margin. How decisively a level is penetrated — by how much, on what volume, and whether the penetration holds on a closing basis rather than an intraday poke — determines whether the role-reversal behavior in Section 8.7.4 should actually be expected to hold. |

|                                                                     |
| ------------------------------------------------------------------- |
| **8.8 TRENDLINES, CHANNELS, AND PERCENTAGE RETRACEMENTS** |

**8.8.1 Drawing trendlines.** An up trendline is drawn beneath a series of reaction lows; a down trendline is drawn above a series of rally peaks. Two points establish only a tentative line; a third touch that respects the line is what confirms it as valid rather than coincidental.

**8.8.2 The fan principle.** Following the violation of an initial trendline, subsequent rallies or declines commonly produce a second, and then a third, trendline at a different angle. The penetration of this third trendline is treated as the confirming signal of a genuine trend reversal — not the first violation, which is more often a normal pullback within the still-intact trend.

**8.8.3 Channel lines.** A channel line is plotted parallel to the main trendline, connecting the opposing series of peaks (in an uptrend) or troughs (in a downtrend). The main trendline is used for entries and for defining where the trend is still intact; the channel line on the opposite side sets a short-term profit-taking target.

**8.8.4 Percentage retracements.** Countertrend corrections tend to retrace a predictable percentage band of the prior move rather than any arbitrary fraction: a minimum around 33% (or 38% on a Fibonacci basis), a median around 50% — the most commonly cited benchmark — and a maximum around 66% (or 62% Fibonacci). Retracing beyond roughly 66% is read as a signal that the correction has become a full trend reversal rather than a pullback within the prior trend.

*Table 8.3 — Percentage retracement bands*

| **Band**            | **Approximate level** | **Reading**                                                    |
| ------------------------ | -------------------------- | ---------------------------------------------------------------------- |
| Minimum                    | 33% (or 38% Fibonacci)         | Shallow pullback; the prior trend is still clearly intact                   |
| Median                      | 50%                             | The most commonly observed and cited retracement level                      |
| Maximum                     | 66% (or 62% Fibonacci)          | Deep pullback; beyond this, treat it as a reversal rather than a correction |

|                                                    |
| ---------------------------------------------------- |
| **8.9 REVERSAL DAYS AND PRICE GAPS** |

**8.9.1 Reversal days.** A reversal day occurs when a market sets a new high (or low) for the move, but then closes in the opposite direction on heavy volume — a same-session round trip that signals a potential change in control between buyers and sellers. An outside day, where the entire daily range exceeds the prior day's range, adds further weight to the significance of the reversal.

**8.9.2 Price gaps — four types, four different meanings.** A gap is not one signal; which type of gap it is changes what it implies about where the market is in a trend.

*Table 8.4 — Price gap types and what each signals*

| **Gap type**             | **Typically occurs**                          | **What it signals**                                          |
| --------------------------- | -------------------------------------------------- | ------------------------------------------------------------------- |
| Breakaway gap                  | Upon completing a price pattern or breaking key support/resistance, on high volume | The start of a new move                                                  |
| Runaway (measuring) gap          | Near the midpoint of a trend                          | A projection tool — the remaining move can be estimated by doubling the distance already travelled |
| Exhaustion gap                    | Near the end of a move                                | A final surge before the trend terminates                               |
| Island reversal                     | An exhaustion gap immediately followed by a breakaway gap in the opposite direction | Price action left isolated like an island — a strong reversal signal          |

|                                                                      |
| ---------------------------------------------------------------------- |
| **8.10 [CODE] HANDS-ON — PULLING YOUR FIRST LIVE MARKET DATA** |

Every indicator in Chapters 9 through 12 — On-Balance Volume, moving averages, oscillators, ADX — is written against a df with five columns: open, high, low, close, volume, indexed by a UTC timestamp. This section is the missing step between the chart vocabulary above and that DataFrame: how to pull it live, from a real exchange, in three short scripts.

**8.10.1 OHLCV — the five-field schema every later chapter reads.** Open is the first trade in the period; High and Low are the period's extremes; Close is the last trade — the cleanest field of the five, since it represents one agreed price at one moment rather than a range; Volume is total units traded. High and Low compress the whole intra-period path into two numbers and discard the path itself: two candles with identical OHLCV can hide completely different journeys. This is exactly why Section 8.9's reversal-day and gap logic reads Close as authoritative and treats intraday extremes as secondary — the same convention this book's code inherits.

**8.10.2 Two data sources, one for each asset class this book uses.** Crypto data (Chapters 9-12's primary examples) comes from Kraken's public REST API — no authentication, no account, effectively no rate limit below one request per second. Equity data comes from yfinance, an unofficial but free wrapper around Yahoo Finance. Both return the same five-field shape once normalized to lowercase columns.

*Table 8.5 — The two data sources used in this book's code*

| **Source** | **Covers** | **Auth?** | **Install** | **Caveat** |
| --- | --- | --- | --- | --- |
| Kraken REST | Crypto spot & perps | No | pip install requests | Max 720 bars/request; paginate with `since` |
| yfinance | US equities, ETFs | No | pip install yfinance | Unofficial scraper — fine for backtesting, not production |

**💻 PYTHON · Listing 8.1 — fetch_kraken_ohlcv(): the crypto data source Chapters 9-12 build on**

```python
import requests, pandas as pd, time

def fetch_kraken_ohlcv(pair: str = "XBTUSD", interval: int = 60,
                        lookback_days: int = 4) -> pd.DataFrame:
    """Fetch OHLCV from Kraken public REST API -- no auth required.
    pair: Kraken pair code (Kraken uses XBT for Bitcoin, not BTC).
    interval: candle width in minutes -- 1,5,15,30,60,240,1440.
    lookback_days: history depth (max 720 bars per request).
    Returns a DataFrame with a UTC DatetimeIndex and OHLCV columns.
    """
    url = "https://api.kraken.com/0/public/OHLC"
    since = int(time.time()) - (lookback_days * 24 * 3600)
    resp = requests.get(url, params={"pair": pair,
                                      "interval": interval, "since": since})
    resp.raise_for_status()
    data = resp.json()
    pair_key = next(k for k in data["result"] if k != "last")
    bars = data["result"][pair_key]
    cols = ["timestamp","open","high","low","close","vwap","volume","count"]
    df = pd.DataFrame(bars, columns=cols)
    df = df[["timestamp","open","high","low","close","volume"]].astype(float)
    df["timestamp"] = pd.to_datetime(
        df["timestamp"].astype(int), unit="s", utc=True)
    df.set_index("timestamp", inplace=True)
    return df
```

**💻 PYTHON · Listing 8.2 — equity OHLCV via yfinance, adjusted for splits and dividends**

```python
import yfinance as yf

df = yf.download("SPY", period="2y", interval="1d", auto_adjust=True)
df.columns = df.columns.str.lower()  # normalize to lowercase columns
```

auto_adjust=True is not optional. An unadjusted 2-for-1 stock split halves the price overnight with no change in value — read by a moving-average crossover (Chapter 10) as a 50% crash, firing a spurious signal on an event that was not a price move at all. Crypto has no splits or dividends, so Listing 8.1 needs no equivalent flag.

**8.10.3 Validate before computing anything.** A corrupted candle — a duplicate timestamp, a zero-volume bar, a high below close — propagates silently into every indicator downstream, including On-Balance Volume's divergence check (Section 9.4) and every moving average in Chapter 10. Run the check below immediately after every load, before computing a single indicator.

**💻 PYTHON · Listing 8.3 — check_ohlcv(): run this before every indicator in Chapters 9-12**

```python
def check_ohlcv(df):
    assert df["high"].ge(df["low"]).all(),   "HIGH < LOW -- corrupt"
    assert df["high"].ge(df["open"]).all(),  "HIGH < OPEN -- corrupt"
    assert df["high"].ge(df["close"]).all(), "HIGH < CLOSE -- corrupt"
    assert df["low"].le(df["open"]).all(),   "LOW > OPEN -- corrupt"
    assert df["low"].le(df["close"]).all(),  "LOW > CLOSE -- corrupt"
    print("Duplicate timestamps:", df.index.duplicated().sum())
    print("Zero-volume bars:", (df["volume"] == 0).sum())
    print("All quality checks passed.")
```

| **▣ DATA — Run this before every backtest, not just the first one** |
| --- |
| Zero-volume bars divide by zero inside On-Balance Volume (Section 9.4) and any other volume-weighted calculation. Duplicate timestamps break the rolling and shift-based windows every moving average and oscillator in this book depends on. These are the single most common cause of "works in backtest, breaks live" — and they are fully preventable in under a second per run. |


|                                                                       |
| ------------------------------------------------------------------------ |
| **8.11 [PROOF] READING A CHART WITHOUT SKIPPING A PREMISE** |

<table>
<thead>
<tr class="header">
<th><strong>▶ PROOF — Four checks before treating a chart pattern as a signal</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>Confirm which trend classification (major, secondary, near-term) the pattern is forming within. A pattern that looks decisive on a near-term chart can be noise against the major trend -- Section 8.7.2's three classifications exist precisely so this question has a concrete answer, not a hand-wave.</p>
<p>Check whether volume confirms the move, per Dow's Tenet 5. A breakout or reversal day on light volume is a materially weaker signal than the identical price action on heavy volume -- Section 8.9.1's reversal-day definition explicitly requires the volume condition, not just the price condition.</p>
<p>Verify a trendline break against the fan principle before treating it as a reversal. Section 8.8.2's third-trendline rule exists because a first trendline violation is frequently just a pullback -- a single break is not yet the confirming signal.</p>
<p>Identify which type of gap is present before drawing a conclusion from it. Section 8.9.2's four gap types imply four different things about where price sits in a trend -- treating a runaway gap as an exhaustion gap, or vice versa, produces the opposite trading conclusion from the correct one.</p>
<p>A pattern that passes all four checks is being read with the full Dow-Theory-derived toolkit this chapter built, not just a visual impression of the chart.</p></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td><p><strong>◈ KEY INSIGHT<br />
</strong></p>
<p><em>"Technical analysis is not 'the chart told me' -- it is three explicit premises (price discounts everything, trends persist, history repeats), a defined vocabulary (Dow Theory's six tenets, trend classification, support/resistance), and a discipline for reading a chart against that vocabulary rather than against a feeling."</em></p></td>
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
<td><p>Technical analysis rests on three premises: market action discounts everything, prices move in trends, and history repeats itself via recurring crowd psychology -- each depends on the one before it.</p>
<p>Technical analysis answers the timing question fundamental analysis cannot, and price action often leads fundamentals rather than following them.</p>
<p>The same technical toolkit applies across every market and every timeframe, which is what allows capital and attention to rotate toward whichever markets are currently trending.</p>
<p>Dow Theory's six tenets -- averages discount everything, three trends, three phases, mutual confirmation, volume confirmation, and trend-in-effect-until-reversed -- underpin most of the vocabulary used throughout the rest of this book.</p>
<p>Chart type (line, bar, point & figure, candlestick) and scale (arithmetic vs. logarithmic) are deliberate choices with real tradeoffs, not stylistic preferences.</p>
<p>A trend is a sequence of peaks and troughs, not a slope; support and resistance reverse roles once decisively broken; trendlines require a third touch to move from tentative to valid, and the fan principle's third-trendline break is the actual reversal confirmation.</p>
<p>Percentage retracements cluster around 33-38%, 50%, and 62-66% bands, and the four gap types (breakaway, runaway, exhaustion, island reversal) each imply a different position within a trend's life cycle.</p></td>
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
<td><p><strong>Technical analysis</strong> The study of market action, primarily via charts, to forecast future price trends.</p>
<p><strong>Dow Theory</strong> The foundational six-tenet framework (Charles Dow, refined by Hamilton and Rhea) underlying modern technical analysis.</p>
<p><strong>Primary trend</strong> The major market tide, lasting over a year.</p>
<p><strong>Secondary trend</strong> A corrective wave lasting three weeks to three months, retracing 1/3 to 2/3 of the primary move.</p>
<p><strong>Minor trend</strong> Near-term fluctuations lasting less than three weeks.</p>
<p><strong>Accumulation phase</strong> Informed buying while sentiment is still poor and bad news is being fully digested.</p>
<p><strong>Distribution phase</strong> Early buyers selling into high-volume, widely bullish public participation.</p>
<p><strong>Support / resistance</strong> A price floor/ceiling where buying/selling pressure has historically reversed a move; each can flip roles once decisively broken.</p>
<p><strong>Fan principle</strong> Successive trendlines drawn after each violation; the third trendline's break confirms a genuine reversal.</p>
<p><strong>Percentage retracement</strong> A countertrend correction's typical size, clustering around 33-38%, 50%, and 62-66% of the prior move.</p>
<p><strong>Reversal day</strong> A new high/low for the move followed by a close in the opposite direction on heavy volume.</p>
<p><strong>Breakaway / runaway / exhaustion gap</strong> Price gaps signaling, respectively, the start of a move, its midpoint, and its final surge.</p>
<p><strong>Island reversal</strong> An exhaustion gap immediately followed by an opposite-direction breakaway gap.</p>
<p><strong>Random walk theory</strong> The claim that price changes are statistically independent; the premise technical analysis's trend-persistence claim directly contradicts.</p></td>
</tr>
</tbody>
</table>

| **WHAT'S NEXT**                                                                                                                                                                                                                                                                                                                                     |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| This chapter lays the chart-reading foundation of Part II — Technical Analysis, establishing the philosophy and vocabulary (Dow Theory, chart construction, trend, support/resistance) that later technical-analysis chapters in this Part will build on. Carry the Section 8.11 PROOF checklist forward as the standard discipline for reading a chart before treating a pattern as a signal, not as a one-time read. |

---

*Source: Restructured from `writing_plans/technical_analysis_summary.md` and `writing_plans/chapters_1_4_summary.md`, condensing four source chapters ("Philosophy of Technical Analysis," "Dow Theory," "Chart Construction," "Basic Concepts of Trend") into a single chapter in this project's house style (opening block, THIS CHAPTER COVERS, numbered N.x sections and sub-sections, data tables, EDGE/WARNING/DATA/PROOF callouts, KEY INSIGHT, Chapter Summary, Key Terms, What's Next) -- following the same pattern used for this project's Money Management and Intermarket Analysis chapters (drafted under earlier chapter numbers 16 and 17 at the time this note was originally written; those chapters are now Chapter 10 and Chapter 6 respectively in this project's current numbering). No code listings, per the same prose-only decision applied to those two chapters: this chapter's source material is philosophy/definitions/vocabulary, not code.*

**Updated 2026-09-22** -- this chapter was renamed and renumbered from its original standalone draft slot ("Chapter 1") to Chapter 11 in this project's book, per user request. All internal section, table, and listing references were renumbered from 1.x to 11.x throughout (including THIS CHAPTER COVERS, the six-tenet Dow Theory table, the chart-type and gap-type tables, the percentage-retracement table, and the closing PROOF checklist). The header digit box was updated accordingly. This chapter now opens a new Part IV -- Technical Analysis, immediately following Chapter 10 (Behavioral Finance, which closes Part III -- Trading Psychology); its Prereqs remain None, since the philosophy/vocabulary content here does not actually depend on the earlier chapters, only its position in the book does. The WHAT'S NEXT box, which previously pointed to a "Chapter 2 -- Markets, Instruments & Data" that does not exist in this project's current numbering (that pointer belonged to an earlier, separate draft sequence), was rewritten to describe this chapter's role as opening Part IV rather than naming a specific next chapter, since no Chapter 12 yet exists. The Source note's reference to "Chapters 16 and 17" (an earlier draft numbering for this project's Money Management and Intermarket Analysis chapters) was clarified to name those chapters by their current numbers (9 and 5) rather than left as a stale, unexplained pointer.

**Updated 2026-10-03** -- Dividend Investing (formerly Chapter 6) was removed from the manuscript; Chapters 7-15 shifted down by one to 6-14. All internal section, table, listing and figure numbers and cross-chapter references in the body were decremented accordingly. Historical dated notes above are left as written.

**Updated 2026-10-06** — Renumbered from Chapter 10 to Chapter 11 after Chapter 2 (Exchange Traded Products) was split into Chapter 2 (ETFs) and Chapter 3 (ETCs and ETNs). Section, subsection, table, figure and listing numbers, the header digit box, Prereqs and cross-chapter references updated; dated notes above keep the numbering of their time.

**Updated 2026-10-06 (c)** — Part label aligned with `.claude/CLAUDE.md` §3.3: Part I — Investing and Stock Market (Ch 1–9), Part II — Technical Analysis (Ch 10–15); "opens/closes Part …" sentences adjusted.

**Updated 2026-10-06 (e)** — Cross-references updated after Futures Trading moved to Chapter 3 and ETCs/ETNs to Chapter 4 (old Ch 3–6 → 4–7).

**Updated 2026-10-07** — Renumbered (−1) after Bonds and Intermarket Analysis were merged into Chapter 6 (Bonds and the Intermarket Chain); section, table, figure and listing numbers and cross-references updated.

**Updated 2026-10-07 (c)** — Prereqs line normalised to "Chapter N (…)"; None → Chapter 1 (Investment Classes and Instruments).
