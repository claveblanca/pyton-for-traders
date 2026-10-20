|                                                             |
| ----------------------------------------------------------- |
| **PYTHON FOR TRADERS: INVESTING, DERIVATIVES, AND TECHNICAL ANALYSIS APPLIED** |

|           |       |
| --------- | ----- |
| Chapter 10 | **10** |

**Moving Averages: From Smoothing Device to Tested Signal**

*SMA, EMA, and Bollinger Bands — the underlying theory, and the pandas/ta code that turns it into a testable signal*

Part II — Technical Analysis · Prereqs: Chapter 9 (Volume and Open Interest)

<table>
<thead>
<tr class="header">
<th><strong>THIS CHAPTER COVERS</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>10.1 The Moving Average as a Smoothing Device — Types and Lag</p>
<p>10.2 Sensitivity and Whipsaws — Choosing a Period</p>
<p>10.3 The Single Moving Average Strategy and Confirmation by Slope</p>
<p>10.4 Crossover Methods — Dual and the 4-9-18 Triple System</p>
<p>10.5 Moving Average Envelopes and Bollinger Bands</p>
<p>10.6 Cycles, Fibonacci Periods, and Long-Term Weekly Charts</p>
<p>10.7 Donchian's Weekly Rule — Price Channel Breakouts</p>
<p>10.8 Adaptive Moving Averages and the Risk of Optimization</p>
<p>10.9 Reading the Moving-Average and Bollinger Dashboards — Signals in Practice</p>
<p>10.10 [CODE] Hands-On — Building SMA, EMA, and Bollinger Bands in Python</p>
<p>10.11 [PROOF] Testing Whether a Crossover Signal Actually Predicts Returns</p></td>
</tr>
</tbody>
</table>

|                                                                |
| ------------------------------------------------------------------ |
| **10.1 THE MOVING AVERAGE AS A SMOOTHING DEVICE — TYPES AND LAG** |

A moving average is a trend-following smoothing device: it calculates the average price of a security over a specified window, dropping the oldest data point as new price data arrives. Because it is calculated purely from historical price data, it inherently operates with a time lag and follows trends rather than leading or predicting them — a moving average never tells you a trend is starting, only that one has already been underway long enough to move the average.

**10.1.1 Three calculation methods.** Every moving average variant used in this book reduces to one of three weighting schemes.

*Table 10.1 — Moving average types and their weighting scheme*

| **Type**                          | **Weighting**                                             |
| -------------------------------------- | ---------------------------------------------------------------- |
| Simple Moving Average (SMA)                | Unweighted mean of closing prices over N days — every bar in the window carries equal weight |
| Linearly Weighted Moving Average (LWMA)      | Greater weight on the most recent price points — more responsive to recent activity |
| Exponentially Smoothed Moving Average (EMA)    | Exponentially decreasing weights on older data, but every historical bar retains some non-zero weight forever |

**10.1.2 Price inputs beyond the close.** While closing prices are most common, a moving average can also be calculated on highs, lows, midpoints (High + Low / 2), or typical prices (High + Low + Close / 3) — the choice of input is a separate decision from the choice of averaging method.

| **◆ EDGE — Lag is not pure disadvantage**                                                                                                                                                                                                                                                                  |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A smoother, laggier average produces fewer whipsaw signals in choppy markets and makes a better baseline for regime classification (bull/bear) than a reactive, fast-responding average. The right amount of lag depends on the job the average is doing — a regime filter wants more lag than an entry trigger does. |

|                                                        |
| ---------------------------------------------------------- |
| **10.2 SENSITIVITY AND WHIPSAWS — CHOOSING A PERIOD** |

**10.2.1 The core trade-off.** Short-term averages (5 or 10 days) track price closely but generate frequent false signals — whipsaws — during choppy, range-bound markets. Longer-term averages (50 or 200 days) filter out market noise but lag significantly behind major turning points, giving back a large share of any move before confirming it.

**10.2.2 There is no period that avoids the trade-off.** Every choice of window length is a choice about which failure mode to accept more of: a shorter window accepts more whipsaws in exchange for less lag at genuine turns; a longer window accepts more lag in exchange for fewer false signals in a directionless market. Section 10.6's cycle-based sizing and Section 10.8's adaptive averages are both attempts to reduce this trade-off rather than eliminate it.

|                                                                          |
| ------------------------------------------------------------------------- |
| **10.3 THE SINGLE MOVING AVERAGE STRATEGY AND CONFIRMATION BY SLOPE** |

The single moving average strategy generates a buy signal when price closes above the moving average line, and a sell signal when price closes below it. Confirmation strengthens when the slope of the average itself turns in the direction of the move — a price crossing a still-declining average is a weaker signal than a price crossing an average that has already begun to flatten or turn up.

| **⚠ WARNING — A close above a flat or falling average is not the same signal as a close above a rising one**                                                                                                                                                                                             |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Treating every price/average crossover identically, without checking the average's own slope, discards information that is explicitly built into the strategy. A mechanical crossover system that ignores slope will fire on plenty of setups that a slope-aware version would have filtered out. |

|                                                                     |
| ----------------------------------------------------------------------- |
| **10.4 CROSSOVER METHODS — DUAL AND THE 4-9-18 TRIPLE SYSTEM** |

**10.4.1 The double (dual) crossover method.** Uses two moving averages — a shorter fast average and a longer slow average. A bullish crossover ("golden cross") occurs when the fast average crosses above the slow average; a bearish crossover ("death cross") occurs when the fast average crosses below. Popular pairings include 5/20-day for futures and 10/50-day or 50/200-day for equities.

**10.4.2 The triple crossover method — the 4-9-18 day system.** Popularized by R.C. Allen for futures trading. A buying alert fires when the 4-day average crosses above both the 9-day and 18-day averages; the signal is confirmed once the 9-day average also crosses above the 18-day, producing a fully stacked sequence: 4 > 9 > 18. The extra confirmation step over the dual method trades signal frequency for signal quality.

*Table 10.2 — Crossover method comparison*

| **Method**       | **Averages used**   | **Signal**                                                   |
| ------------------- | ---------------------- | -------------------------------------------------------------------- |
| Dual crossover          | 2 (fast, slow)             | Fast crosses above/below slow — golden/death cross                        |
| Triple crossover (4-9-18) | 3 (4, 9, 18-day)            | 4 crosses above 9 and 18; confirmed when 9 crosses above 18 (stacked 4 &gt; 9 &gt; 18) |

|                                                              |
| ------------------------------------------------------------- |
| **10.5 MOVING AVERAGE ENVELOPES AND BOLLINGER BANDS** |

**10.5.1 Moving average envelopes.** Lines drawn at a fixed percentage above and below a moving average — 3% or 5% are common — to define a mechanical overbought/oversold band around the trendline. The band width is fixed regardless of how volatile the market currently is, which is the specific limitation Bollinger Bands were designed to fix.

**10.5.2 Bollinger Bands.** Developed by John Bollinger, these bands are placed two standard deviations above and below a 20-period simple moving average. Because standard deviation measures statistical volatility directly, the bands expand during volatile trend expansions and contract — "squeeze" — during low-volatility consolidations, unlike a fixed-percentage envelope. Price touching an outer band acts as a volatility-relative target or a signal of an overextended move, not a fixed price level.

**10.5.3 Band width as its own volatility measure.** The distance between the upper and lower band, normalized by the middle band, is itself a usable indicator independent of price direction — a rolling multi-month low in band width ("the squeeze") is commonly read as a setup for an imminent volatility expansion, in either direction.

|                                                                     |
| ----------------------------------------------------------------------- |
| **10.6 CYCLES, FIBONACCI PERIODS, AND LONG-TERM WEEKLY CHARTS** |

**10.6.1 Cycle-synchronized periods.** Moving average lengths are often synchronized with a market's dominant cycle. Using a period equal to half the dominant cycle length — a 10-day average for a dominant 20-day trading cycle, for example — provides optimal trend smoothing without excessive lag, rather than choosing a round-number period arbitrarily.

**10.6.2 Fibonacci periods.** Sequence numbers such as 13, 21, 34, 55, and 89 are widely applied as moving average parameters on both daily and weekly charts — the appeal is partly mathematical and partly the same institutional-adherence effect noted for SMA-50/200 in Section 10.1.

**10.6.3 Weekly charts for the primary trend.** 10-week and 40-week (or 13-week and 34-week) moving averages applied to weekly charts track the primary bull/bear trend and provide key support/resistance zones during pullbacks — the same "compress the timeframe to see the bigger structure" logic used throughout this book's own multi-timeframe stack.

|                                                                |
| ------------------------------------------------------------------ |
| **10.7 DONCHIAN'S WEEKLY RULE — PRICE CHANNEL BREAKOUTS** |

**10.7.1 The 4-week rule.** Developed by Richard Donchian, this purely mechanical breakout system generates a buy signal whenever price exceeds the highest high of the previous 4 weeks (20 trading days), and a sell/short signal whenever price falls below the lowest low of the same 4-week window. Unlike a moving average, the channel is defined entirely by realized extremes, not by any averaging or smoothing step.

**10.7.2 Modified channel rules.** Traders often use a shorter channel — a 1-week or 2-week rule — for liquidating positions or trailing protective stops, while keeping the longer 4-week channel for the entry signal itself: a wide channel to get in, a tighter one to manage the position once it's on.

|                                                                    |
| ------------------------------------------------------------------ |
| **10.8 ADAPTIVE MOVING AVERAGES AND THE RISK OF OPTIMIZATION** |

**10.8.1 The optimization trap.** Curve-fitting moving average parameters to past historical data routinely produces performance expectations that fail to hold in forward, out-of-sample trading — the parameter set that would have worked perfectly on the last two years of data is frequently a poor forward choice, because it was fit to noise specific to that window rather than to a persistent structural property of the market.

**10.8.2 The Adaptive Moving Average (AMA).** Developed by Perry Kaufman, the AMA automatically adjusts its own sensitivity based on measured market volatility — smoothing out (behaving like a slow average) during noise-filled sideways markets, and speeding up (behaving like a fast average) during clear, directional trends, without the trader manually re-fitting a fixed period.

| **▣ DATA — An adaptive average changes the tuning problem, not the trade-off from Section 10.2**                                                                                                                                                                                                       |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The AMA does not escape the lag/whipsaw trade-off from Section 10.2 — it re-derives an appropriate point on that trade-off automatically, continuously, based on current volatility, rather than requiring a single static period to be chosen once and left fixed regardless of regime. |

|                                                                     |
| -------------------------------------------------------------------- |
| **10.9 READING THE MOVING-AVERAGE AND BOLLINGER DASHBOARDS — SIGNALS IN PRACTICE** |

Sections 10.3–10.5 set out the moving-average and Bollinger Band rules, and Listings 10.2–10.4 built them. This section reads both tools on live BTC/USD charts and condenses the rules into two trigger tables.

**10.9.1 The moving-average dashboard.** Figure 10.1 shows the daily chart with three EMAs (9, 12 and 26, built as in Listing 10.2). The header's MACD value is simply EMA 12 − EMA 26 (Section 11.3): positive while the fast average sits above the slow one.

![Moving-average dashboard — BTC/USD daily, EMA 9 / 12 / 26](../images/MA_dashboard_BTC_2026-09_light.png)

*Figure 10.1 — Moving-average dashboard, BTC/USD daily, July – mid-September 2026. EMA 9, EMA 12 and EMA 26; header MACD = EMA 12 − EMA 26.*

1. **July – mid-August: braided averages.** The three EMAs are tangled around $63–65k and price crosses them constantly. Several crossovers fire and none follows through: Section 10.2's whipsaw problem, live.
2. **Aug 17–21: breakout and a bullish stack.** Price jumps from about $64k to $78k and the EMAs fan out in order (price > 9 > 12 > 26), all rising. The 12/26 crossover confirms the trend, well after the first leg of the move.
3. **Late August – early September: trend holding.** Price stays above the fast EMAs and EMA 26 climbs steadily; pullbacks to EMA 12 are buyable.
4. **Sep 8–10: momentum fading.** EMA 9 crosses below EMA 12 and both flatten near $78k — the first warning for an aggressive trailing exit.
5. **Mid-September: test of EMA 26.** Price dips below EMA 26 for a day, then recovers to sit on it, below the fast EMAs. MACD is still positive but far below its August peak: the stack is no longer bullish, but the 12/26 trend is not yet broken.

**10.9.2 The Bollinger Band dashboard.** Figure 10.2 shows hourly candles with 20-period, 2-standard-deviation bands (Listing 10.4). Note that Table 10.5 suggests a 50-period average for crypto intraday work; the dashboard uses the standard 20, which reacts faster and squeezes more often.

![Bollinger Band dashboard — BTC/USD hourly, September 19–24, 2026](../images/BB_dashboard_BTC_2026-09_light.png)

*Figure 10.2 — Bollinger Band dashboard, BTC/USD hourly, Sep 19–24, 2026. Middle band (20-period SMA) and upper/lower bands at ±2 standard deviations.*

1. **Sep 19–21: squeeze.** The bands contract into a narrow channel around $80–82k: the setup Section 10.5 describes, direction unknown.
2. **Sep 21: breakout and band walk.** A large candle closes well above the upper band, the bands open sharply, and price walks the upper band to about $87.4k. Selling "because price touched the upper band" would have been exactly wrong.
3. **Sep 22–23: pause and a failed retest.** Price returns to the middle band and ranges; a second push reaches the upper band just below the prior high — a possible M-top.
4. **Sep 23: breakdown.** Price closes below the middle band and walks the lower band down to about $83.5k.
5. **Sep 24: a second squeeze resolves lower.** The bands tighten again around a falling middle band, and the last candle closes below the lower band: a bearish squeeze breakout, not a mean-reversion buy.

**10.9.3 The signal tables.**

*Table 10.3 — Moving-average trigger conditions*

| **Signal** | **Conditions** | **Action** |
| --- | --- | --- |
| **BUY** | Fast EMA crosses above slow EMA (Listing 10.3's cross logic applied to Listing 10.2's EMAs) **and** ADX > 25 (Chapter 12) | Open long |
| **BUY (pullback)** | Fast above slow, slow EMA rising, price touches the slow EMA and closes back above it | Add or enter; stop below the pullback low |
| **SELL** | Fast EMA crosses below slow EMA **and** ADX > 25 | Open short, or exit longs |
| **EXIT** | Daily close below the trailing EMA (9 aggressive, 26 patient), or the opposite cross | Close the position |
| **STAND ASIDE** | EMAs flat and braided; ADX < 20 | No crossover trades; hand over to Chapter 11's oscillators |

*Table 10.4 — Bollinger Band trigger conditions*

| **Signal** | **Conditions** | **Action** |
| --- | --- | --- |
| **BUY (breakout)** | `squeeze` true within the last few bars (Listing 10.4) **and** close above the upper band | Open long; stop at the middle band |
| **SELL (breakout)** | Recent squeeze **and** close below the lower band | Open short; stop at the middle band |
| **HOLD (band walk)** | Closes stay between the middle and the outer band | Stay with the trend |
| **EXIT** | Close on the far side of the middle band, or a head fake (close back inside the bands within 1–3 bars) | Close or reverse |
| **MEAN REVERSION** | ADX < 20 only: `bb_pct_b` crosses back above 0 (buy) or back below 1 (sell) | Target the middle band |

| **▲ WARNING — The same band touch means opposite things** |
| --- |
| In a range, a close outside the upper band is a sell; in a trend it is a sign of strength, and price can walk the band for days (Figure 10.2, Sep 21). A squeeze says *that* a move is coming, never *which way*. Moving averages lag by construction, and parameters tuned to one chart's history rarely survive out of sample. The regime — Chapter 12's ADX — decides which reading of either tool applies. |


|                                                                     |
| ------------------------------------------------------------------- |
| **10.10 [CODE] HANDS-ON — BUILDING SMA, EMA, AND BOLLINGER BANDS IN PYTHON** |

The rest of this chapter turns Sections 10.1–10.5's definitions into code — SMA and EMA computed two ways each, a regime classifier, crossover-event detection, and the full Bollinger Bands construction with %B and bandwidth.

**10.10.1 SMA — the deterministic baseline.**

<table>
<thead>
<tr class="header">
<th><strong>💻 PYTHON · Listing 10.1 — SMA construction and a bull/bear regime classifier</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p># pandas.rolling().mean() -- deterministic, vectorised, identical across platforms</p>
<p>df['sma_20']  = df['close'].rolling(window=20).mean()</p>
<p>df['sma_50']  = df['close'].rolling(window=50).mean()</p>
<p>df['sma_200'] = df['close'].rolling(window=200).mean()</p>
<p></p>
<p># Equivalent via the ta library, for a uniform signal-library API</p>
<p># from ta.trend import SMAIndicator</p>
<p># df['sma_200'] = SMAIndicator(close=df['close'], window=200).sma_indicator()</p>
<p></p>
<p># Bull/bear regime classifier -- SMA-200 as the dividing line</p>
<p>df['above_sma200'] = (df['close'] &gt; df['sma_200']).astype(int)  # 1 = bull, 0 = bear</p>
<p></p>
<p># Never forward-fill or interpolate the warm-up NaNs (first n-1 bars) --</p>
<p># a filled SMA-200 at bar 150 is a fabricated value, not a real SMA-200,</p>
<p># and will introduce look-ahead bias into any backtest.</p>
<p>df.dropna(subset=['sma_200'], inplace=True)</p></td>
</tr>
</tbody>
</table>

**10.10.2 EMA — the responsive counterpart, and the `adjust=False` trap.**

<table>
<thead>
<tr class="header">
<th><strong>💻 PYTHON · Listing 10.2 — EMA construction with the platform-matching adjust=False flag</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p># adjust=False replicates the standard recursive formula used by</p>
<p># TradingView, Binance, and most broker platforms:</p>
<p>#   EMA_t = alpha * Close_t + (1 - alpha) * EMA_{t-1},  alpha = 2 / (span + 1)</p>
<p># adjust=True (pandas' default) corrects for initialisation bias instead --</p>
<p># useful for statistics, but it will NOT match what your broker's chart shows.</p>
<p>df['ema_9']  = df['close'].ewm(span=9,  adjust=False).mean()</p>
<p>df['ema_21'] = df['close'].ewm(span=21, adjust=False).mean()</p>
<p>df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()</p>
<p></p>
<p># EMA - SMA spread at the same period: a scale-invariant momentum feature.</p>
<p># Positive = recent bars are dragging price above the historical average.</p>
<p>df['ema_sma_spread_pct'] = (df['ema_50'] - df['sma_50']) / df['sma_50']</p></td>
</tr>
</tbody>
</table>

**10.10.3 Dual crossover events — Section 10.4's golden/death cross, in code.**

<table>
<thead>
<tr class="header">
<th><strong>💻 PYTHON · Listing 10.3 — Detecting golden/death cross events from Listing 10.1's SMAs</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>df['cross_signal'] = 0</p>
<p></p>
<p># Golden cross: fast SMA crosses above slow SMA</p>
<p>golden = (df['sma_20'] &gt; df['sma_50']) &amp; \</p>
<p>         (df['sma_20'].shift(1) &lt;= df['sma_50'].shift(1))</p>
<p>df.loc[golden, 'cross_signal'] = 1</p>
<p></p>
<p># Death cross: fast SMA crosses below slow SMA</p>
<p>death = (df['sma_20'] &lt; df['sma_50']) &amp; \</p>
<p>        (df['sma_20'].shift(1) &gt;= df['sma_50'].shift(1))</p>
<p>df.loc[death, 'cross_signal'] = -1</p>
<p></p>
<p># Crossover signals lag the move by construction -- the cross event fires</p>
<p># AFTER price has already shifted. On ~2,160 hourly bars (90 days), expect</p>
<p># only 5-15 SMA-20/50 crossover events -- too sparse for standalone</p>
<p># statistical significance. Use as confirmation, not a primary entry.</p></td>
</tr>
</tbody>
</table>

**10.10.4 Bollinger Bands — bands, %B, and the squeeze.**

<table>
<thead>
<tr class="header">
<th><strong>💻 PYTHON · Listing 10.4 — Bollinger Bands, %B, bandwidth, and squeeze detection</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>window, num_std = 20, 2.0</p>
<p></p>
<p>df['bb_mid']   = df['close'].rolling(window=window).mean()</p>
<p># ddof=0 (population std) matches TradingView and most platforms;</p>
<p># pandas' default ddof=1 (sample std) gives slightly wider bands.</p>
<p>df['bb_std']   = df['close'].rolling(window=window).std(ddof=0)</p>
<p>df['bb_upper'] = df['bb_mid'] + num_std * df['bb_std']</p>
<p>df['bb_lower'] = df['bb_mid'] - num_std * df['bb_std']</p>
<p></p>
<p># Bandwidth: normalised distance between the bands -- a volatility gauge</p>
<p># independent of price direction (Section 10.5.3).</p>
<p>df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_mid']</p>
<p></p>
<p># %B: where price sits within the bands.</p>
<p># %B &gt; 1.0 -&gt; above the upper band (overbought); %B &lt; 0.0 -&gt; below the</p>
<p># lower band (oversold); %B = 0.5 -&gt; exactly at the midline.</p>
<p>df['bb_pct_b'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])</p>
<p></p>
<p># Squeeze: bandwidth at a rolling multi-day low -- a breakout setup,</p>
<p># direction unknown until it resolves.</p>
<p>df['bb_width_min'] = df['bb_width'].rolling(window=130).min()  # ~6 days on 1H</p>
<p>df['squeeze'] = df['bb_width'] &lt;= df['bb_width_min']</p></td>
</tr>
</tbody>
</table>

*Table 10.5 — Bollinger Bands parameter sensitivity by use case*

| **Use case**            | **SMA period** | **Std dev multiplier** | **Timeframe** |
| ---------------------------- | ------------------- | ---------------------------- | ------------------ |
| Equity swing trading             | 20                       | 2.0                                | Daily                     |
| Crypto swing (BTC/ETH)             | 20                       | 2.5 (wider, fat-tail returns)        | Daily                     |
| Crypto intraday                     | 50                       | 2.0                                | 1H                         |
| Squeeze breakout                     | 20                       | 2.0                                | 4H                         |

| **⚠ WARNING — `ddof` and the wrong std-dev convention silently widens every band**                                                                                                                                                                                                                       |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| pandas' `.std()` defaults to `ddof=1` (sample standard deviation); most charting platforms use `ddof=0` (population standard deviation). The difference is small per-bar but compounds into visibly different band widths and a different %B reading at every point -- always set `ddof=0` explicitly rather than relying on the pandas default. |

|                                                                                    |
| ------------------------------------------------------------------------------------- |
| **10.11 [PROOF] TESTING WHETHER A CROSSOVER SIGNAL ACTUALLY PREDICTS RETURNS** |

A crossover looking visually convincing on a chart is not evidence it predicts anything. The listing below runs the regime classifier from Listing 10.1 through a two-sample t-test comparing forward returns above vs. below SMA-200 — the same discipline this book's later validation chapters apply formally.

<table>
<thead>
<tr class="header">
<th><strong>💻 PYTHON · Listing 10.5 — Forward-return significance test for the SMA-200 regime filter</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>import scipy.stats as stats</p>
<p></p>
<p>df['fwd_return_1h'] = df['close'].pct_change().shift(-1)</p>
<p></p>
<p>bull_returns = df.loc[df['above_sma200'] == 1, 'fwd_return_1h'].dropna()</p>
<p>bear_returns = df.loc[df['above_sma200'] == 0, 'fwd_return_1h'].dropna()</p>
<p></p>
<p>t_stat, p_value = stats.ttest_ind(bull_returns, bear_returns)</p>
<p>print(f'Bull mean: {bull_returns.mean():.5f} | Bear mean: {bear_returns.mean():.5f}')</p>
<p>print(f't={t_stat:.3f}, p={p_value:.4f}')</p>
<p># p &lt; 0.05 -&gt; the regime distinction is statistically significant</p>
<p></p>
<p># Same discipline applied to the Listing 10.3 crossover events:</p>
<p># tag each event's N-bar forward return, compare sign(cross_signal) against</p>
<p># sign(forward_return), and report a hit rate -- 50% is random; treat</p>
<p># anything below ~55% with n &gt;= 30 events as not yet distinguishable from luck.</p></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><strong>▶ PROOF — Three checks before trusting a moving-average signal in production</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>Run Listing 10.5's t-test (or the crossover hit-rate variant) on the actual instrument and timeframe you intend to trade -- Section 10.1's SMA-50/200 "institutional adherence" argument is a real effect on liquid large-caps and BTC, but it is not guaranteed to transfer to a thin altcoin or a timeframe nobody else is charting.</p>
<p>Count your events before trusting the result. A 90-day sample commonly yields only 5-15 crossover events (Listing 10.3) -- report n alongside any hit rate or p-value, and treat a result built on fewer than ~30 events as preliminary, not confirmed.</p>
<p>Re-run the test after any parameter change. Section 10.8's optimization warning applies directly here: a period or std-dev multiplier chosen because it tested well on the same window used to choose it is not validated -- it is curve-fit. Hold out data the parameter search never saw.</p></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td><p><strong>◈ KEY INSIGHT<br />
</strong></p>
<p><em>"A moving average is a smoothing device with a time lag, not a forecast. Every strategy built on top of one -- single-line, dual crossover, 4-9-18, Bollinger Bands, Donchian channels -- is really a choice about how much lag to accept in exchange for how much noise to filter, and that choice is only validated once it has been tested against forward returns, not just admired on a chart."</em></p></td>
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
<td><p>A moving average smooths price at the cost of lag; SMA weighs every bar equally, LWMA and EMA weight recent bars more heavily, and EMA retains a decaying trace of every historical bar forever.</p>
<p>Shorter periods reduce lag but increase whipsaws in choppy markets; longer periods do the reverse -- there is no period that escapes this trade-off, only ones that trade it off differently for a given job.</p>
<p>The single-average strategy trades price crossing the line, strengthened by confirming the average's own slope; the dual crossover (golden/death cross) and 4-9-18 triple system add one and two further confirmation layers respectively.</p>
<p>Bollinger Bands improve on fixed-percentage envelopes by scaling with realized volatility (2 standard deviations around a 20-period SMA); band width is itself a volatility indicator, and a "squeeze" (multi-day low in band width) is read as a breakout setup.</p>
<p>Cycle-synchronized and Fibonacci periods, and 10/40-week (or 13/34-week) charts for the primary trend, are ways of choosing a period deliberately rather than defaulting to round numbers.</p>
<p>Donchian's 4-week rule is a pure price-channel breakout system, independent of any averaging; the Adaptive Moving Average automatically re-derives its own speed from measured volatility rather than using one fixed period.</p>
<p>Curve-fitting parameters to historical data is the single biggest risk in this chapter's whole toolkit -- every signal here needs a forward-return significance test (Section 10.11), not just a convincing-looking backtest on the window used to tune it.</p>
<p>Section 10.9 reads both tools on live BTC/USD charts and writes their rules as trigger tables (Tables 10.3 and 10.4): EMA crossovers only when ADX confirms a trend, pullbacks to the slow EMA, squeeze breakouts and band walks, and mean reversion only in a range.</p></td>
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
<td><p><strong>Simple Moving Average (SMA)</strong> Unweighted mean of closing prices over N days.</p>
<p><strong>Linearly Weighted Moving Average (LWMA)</strong> A moving average giving greater weight to more recent prices.</p>
<p><strong>Exponentially Smoothed Moving Average (EMA)</strong> A moving average with exponentially decaying weights; every historical bar retains nonzero weight.</p>
<p><strong>Whipsaw</strong> A false signal produced by a short-period average reacting to noise in a choppy, range-bound market.</p>
<p><strong>Golden cross / death cross</strong> A fast moving average crossing above (golden) or below (death) a slow moving average.</p>
<p><strong>4-9-18 system</strong> R.C. Allen's triple crossover method using 4-, 9-, and 18-day averages, confirmed by a fully stacked sequence.</p>
<p><strong>Moving average envelope</strong> Fixed-percentage bands above/below a moving average, defining a static overbought/oversold zone.</p>
<p><strong>Bollinger Bands</strong> Bands set 2 standard deviations above/below a 20-period SMA; expand and contract with realized volatility.</p>
<p><strong>%B</strong> Price's position within the Bollinger Bands, normalized 0 (lower band) to 1 (upper band).</p>
<p><strong>Squeeze</strong> A multi-period low in Bollinger Band width, read as a setup for a volatility breakout.</p>
<p><strong>Donchian's 4-week rule</strong> A breakout system: buy above the prior 4-week high, sell/short below the prior 4-week low.</p>
<p><strong>Adaptive Moving Average (AMA)</strong> Perry Kaufman's moving average that adjusts its own sensitivity based on measured volatility.</p>
<p><strong>Curve-fitting</strong> Tuning parameters to historical data in a way that fails to generalize to forward, out-of-sample data.</p>
<p><strong>Band walk / head fake</strong> A band walk is a run of closes hugging one Bollinger Band during a strong trend; a head fake is a squeeze breakout that closes back inside the bands within a few bars and reverses.</p></td>
</tr>
</tbody>
</table>

| **WHAT'S NEXT**                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Chapter 11 — Oscillators and Contrary Opinion. This chapter built the trend-following half of the indicator toolkit (moving averages, crossovers, Bollinger Bands); the next chapter adds the momentum/reversal half (RSI, MACD, CCI, Stochastics) that reads overbought/oversold conditions a trend-following average is structurally blind to. |


---

*Source: Restructured from `writing_plans/chapter_9_summary.md`, condensing source material on moving averages into this project's house style (opening block, THIS CHAPTER COVERS, numbered N.x sections and sub-sections, data tables, EDGE/WARNING/DATA/PROOF callouts, KEY INSIGHT, Chapter Summary, Key Terms, What's Next). Code listings 13.1-13.5 are drawn from and cross-referenced against `code_snippets/ch06/sma.md`, `ema.md`, and `bollinger_bands.md` -- the SMA/regime-classifier, EMA `adjust=False` construction, and Bollinger Bands/%B/squeeze code is functionally identical to those files, condensed and re-labelled to this chapter's listing numbers.*

**Updated 2026-09-22** — this chapter was renamed and renumbered from its original standalone draft slot ("Chapter 4") to Chapter 13 in this project's book, per user request ("shift right this chapters (chapter 3 should become chapter12)"), alongside three companion chapters shifting the same +9: Volume and Open Interest (3 -> 12), Oscillators and Contrary Opinion (5 -> 14), and ADX and Directional Movement (6 -> 15). All internal section, table, and listing references were renumbered from 4.x to 13.x throughout. This chapter now sits in Part IV — Technical Analysis, immediately after Chapter 12 (Volume and Open Interest); its Prereqs were updated to "Ch 12 (Volume and Open Interest)" to match. WHAT'S NEXT was updated to point to Chapter 14 (Oscillators and Contrary Opinion), the next chapter in this same renumbering batch.

**Updated 2026-09-24** — added Section 13.10 (dashboard reading and trigger table, adapted from `writing_plans/*_Trading_Guide.md`), with Figures 13.1–13.2 and Tables 13.4–13.5; the PROOF section was renumbered 13.10 → 13.11 (THIS CHAPTER COVERS, cross-references, Chapter Summary and Key Terms updated). Images live in `content_md/images/` (light-gray conversions of the BTC/USD dashboard screenshots; flagged for replacement by print-ready grayscale charts at 300 dpi).

**Updated 2026-10-03** -- Dividend Investing (formerly Chapter 6) was removed from the manuscript; Chapters 7-15 shifted down by one to 6-14. All internal section, table, listing and figure numbers and cross-chapter references in the body were decremented accordingly. Historical dated notes above are left as written.

**Updated 2026-10-06** — Renumbered from Chapter 12 to Chapter 13 after Chapter 2 (Exchange Traded Products) was split into Chapter 2 (ETFs) and Chapter 3 (ETCs and ETNs). Section, subsection, table, figure and listing numbers, the header digit box, Prereqs and cross-chapter references updated; dated notes above keep the numbering of their time.

**Updated 2026-10-06 (c)** — Part label aligned with `.claude/CLAUDE.md` §3.3: Part I — Investing and Stock Market (Ch 1–9), Part II — Technical Analysis (Ch 10–15); "opens/closes Part …" sentences adjusted.

**Updated 2026-10-06 (e)** — Cross-references updated after Futures Trading moved to Chapter 3 and ETCs/ETNs to Chapter 4 (old Ch 3–6 → 4–7).

**Updated 2026-10-07** — Renumbered (−1) after Bonds and Intermarket Analysis were merged into Chapter 6 (Bonds and the Intermarket Chain); section, table, figure and listing numbers and cross-references updated.

**Updated 2026-10-07 (c)** — Prereqs line normalised to "Chapter N (…)".
