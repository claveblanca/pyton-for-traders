|                                                             |
| ----------------------------------------------------------- |
| **PYTHON FOR TRADERS: INVESTING, DERIVATIVES, AND TECHNICAL ANALYSIS APPLIED** |

|            |        |
| ---------- | ------ |
| Chapter 11 | **11** |

**Oscillators and Contrary Opinion: RSI, MACD, and Trading the Range**

*Momentum, RSI, MACD, CCI, and Stochastics — the underlying theory for nontrending markets, and the pandas/ta code that turns RSI and MACD into tested signals*

Part II — Technical Analysis · Prereqs: Chapter 10 (Moving Averages)

<table>
<thead>
<tr class="header">
<th><strong>THIS CHAPTER COVERS</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>11.1 Oscillators: Purpose and the Three Interpretation Rules</p>
<p>11.2 Momentum and Rate of Change (ROC)</p>
<p>11.3 MACD — Moving Average Convergence/Divergence and the Histogram</p>
<p>11.4 The Relative Strength Index (RSI)</p>
<p>11.5 Commodity Channel Index (CCI)</p>
<p>11.6 Stochastics and Larry Williams %R</p>
<p>11.7 Cycles, Multiple Time Frames, and the Weekly/Daily Filter</p>
<p>11.8 The Principle of Contrary Opinion</p>
<p>11.9 Reading the RSI Dashboard — Signals in Practice</p>
<p>11.10 [CODE] Hands-On — Building RSI and MACD in Python</p>
<p>11.11 [PROOF] Validating an Oscillator Signal Before Trusting It</p></td>
</tr>
</tbody>
</table>

|                                                                            |
| -------------------------------------------------------------------------- |
| **11.1 OSCILLATORS: PURPOSE AND THE THREE INTERPRETATION RULES** |

Oscillators exist to profit from the market condition trend-following tools handle worst: nontrending, horizontal trading ranges, where a moving average system whipsaws repeatedly because price keeps crossing back and forth over a flat line. Used alongside trend tools during active trending phases, an oscillator's job shifts — it alerts the trader to short-term overbought or oversold extremes and warns that a trend is losing momentum before price itself reflects the reversal.

**11.1.1 Three rules govern every oscillator in this chapter.** Plotted at the bottom of a chart, an oscillator is read the same way regardless of its specific formula.

*Table 11.1 — The three oscillator interpretation rules*

| **Rule**                       | **What it signals**                                                                          |
| ------------------------------- | ----------------------------------------------------------------------------------------------- |
| Market extremes                     | Reaching an upper or lower boundary signals an overextended rally (overbought) or decline (oversold) |
| Divergence                          | Oscillator failing to confirm a new price extreme, while in an extreme zone, warns of an impending reversal |
| Zero / midpoint crossover           | Crossing the zero line (or 50% midline) generates a trade signal in the direction of the broader trend |

| **◆ EDGE — An oscillator is a range tool wearing a trend tool's clothes**                                                                                                                                                                                                                                  |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The same RSI or MACD reading means something different depending on regime: in a range, an extreme reading is a fade signal; in a strong trend, the same extreme reading is often just the oscillator confirming trend strength and staying pinned there. Chapter 12's ADX-gated approach exists specifically to tell these two cases apart before acting on either. |

|                                                                     |
| -------------------------------------------------------------------- |
| **11.2 MOMENTUM AND RATE OF CHANGE (ROC)** |

**11.2.1 Momentum.** The simplest oscillator: M = V − Vx, where V is the latest close and Vx is the close x days ago. A rising momentum line above zero means an accelerating uptrend; a flattening or falling momentum line means decelerating momentum even while price is still technically rising — momentum measures the *rate* of ascent or descent, not the direction alone. Momentum has no natural fixed boundary, so overbought/oversold thresholds must be drawn from visual inspection of past price history rather than read off a fixed scale.

**11.2.2 Rate of Change (ROC).** The same idea expressed as a ratio instead of a difference: ROC = 100 × (V / Vx), oscillating around a central baseline of 100 rather than zero. RSI, CCI, and Stochastics (Sections 11.4–11.6) are all, in effect, more sophisticated answers to momentum's boundary problem — each imposes a fixed 0–100 (or ±100) scale that momentum itself lacks.

|                                                                                    |
| ------------------------------------------------------------------------------------- |
| **11.3 MACD — MOVING AVERAGE CONVERGENCE/DIVERGENCE AND THE HISTOGRAM** |

**11.3.1 Construction.** Developed by Gerald Appel, MACD combines two exponential moving averages — a 12-period and a 26-period EMA by default — into a single MACD line (fast EMA minus slow EMA), paired with a 9-period EMA of that line as the signal line. It is, functionally, a dual-moving-average oscillator: the same idea as Section 10.4's crossover methods, replotted around a zero line instead of as two overlaid price-chart lines.

**11.3.2 The histogram.** Plots the difference between the MACD line and the signal line as vertical bars. The histogram's turning points precede the actual MACD line/signal-line crossover — a histogram that is shrinking toward zero is warning of an approaching crossover before the crossover itself fires, which is the operationally useful part of the indicator.

**11.3.3 Combining weeklies and dailies.** As with moving averages (Section 10.6.3), a weekly MACD read as the primary trend filter, with daily MACD signals taken only when they agree with the weekly's direction, is the standard multi-timeframe discipline applied to this indicator.

|                                                                    |
| --------------------------------------------------------------------- |
| **11.4 THE RELATIVE STRENGTH INDEX (RSI)** |

**11.4.1 Definition.** Developed by J. Welles Wilder, Jr., RSI solves momentum's scale problem by constraining every reading to a fixed 0–100 range, computed from the ratio of average gains to average losses over a lookback period (14 days classically).

**11.4.2 Standard levels.** 70 and 30 are the standard overbought/oversold thresholds, shifted to 80/20 during strong bull or bear markets, where the classic 70/30 levels trigger too early and get repeatedly run over by trend strength.

**11.4.3 Failure swings.** A top or bottom failure swing occurs when RSI fails to confirm a new price extreme while sitting in overbought or oversold territory, then breaks a prior RSI trough or peak — this is Wilder's own strongest RSI signal, distinct from a simple 70/30 threshold cross and generally treated as more reliable.

| **⚠ WARNING — `pandas.rolling().mean()` on the gain/loss legs produces the wrong RSI**                                                                                                                                                                                                                     |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Wilder's original formula smooths gains and losses with his own smoothing method — mathematically an EMA with alpha = 1/period — not a simple moving average. Computing RSI with `.rolling().mean()` on the gain/loss legs gives an SMA-smoothed RSI that diverges from the Wilder/TradingView standard used everywhere else in this book. Section 11.10.1's implementation uses `.ewm(alpha=1/period, adjust=False)` specifically to avoid this. |

|                                                                     |
| ------------------------------------------------------------------ |
| **11.5 COMMODITY CHANNEL INDEX (CCI)** |

Developed by Donald R. Lambert, CCI compares price to a 20-day moving average normalized by mean deviation, oscillating between roughly +100 and −100. Readings above +100 signal overbought conditions; readings below −100 signal oversold conditions. Unlike RSI's fixed 0–100 scale, CCI is technically unbounded — the ±100 levels are conventional thresholds, not hard limits, so an extended trend can push CCI well past ±200 without any mathematical ceiling stopping it.

|                                                                          |
| --------------------------------------------------------------------------- |
| **11.6 STOCHASTICS AND LARRY WILLIAMS %R** |

**11.6.1 Stochastics (%K, %D).** Popularized by George Lane, Stochastics measures where the current close sits relative to the total price range over a set lookback (14 days is standard). The faster %K line crossing the slower %D line generates buy/sell triggers, read as significant specifically when %D is above 80 (overbought) or below 20 (oversold) — a %K/%D cross in the middle of the range carries much less weight than the same cross at an extreme.

**11.6.2 Larry Williams %R.** Measures the close relative to the high-low range over a lookback period, plotted inverted on a 0 to −100 scale: readings between −20 and 0 indicate overbought conditions, and readings between −80 and −100 indicate oversold conditions — the inversion is a common source of confusion when reading %R against RSI or Stochastics on the same chart.

*Table 11.2 — Oscillator families and their scale*

| **Oscillator**    | **Scale**                    | **Overbought / oversold**                     |
| ---------------------- | -------------------------------- | -------------------------------------------------- |
| Momentum                  | Unbounded, zero-centred              | No fixed level — set by visual inspection               |
| Rate of Change (ROC)      | Unbounded, centred on 100            | No fixed level — set by visual inspection               |
| MACD                       | Unbounded, zero-centred              | No fixed level — read via histogram / zero-line cross     |
| RSI                        | Fixed 0–100                          | 70 / 30 (80 / 20 in strong trends)                        |
| CCI                        | Conventionally ±100 (unbounded)      | +100 / −100                                                |
| Stochastics (%K, %D)       | Fixed 0–100                          | 80 / 20                                                    |
| Williams %R                | Fixed 0 to −100 (inverted)           | −20 / −80 (inverted vs. the others)                        |

|                                                                                     |
| -------------------------------------------------------------------------------------- |
| **11.7 CYCLES, MULTIPLE TIME FRAMES, AND THE WEEKLY/DAILY FILTER** |

**11.7.1 Cycle-synchronized periods.** As with moving averages (Section 10.6.1), oscillator lookback periods are often set to half the dominant market cycle — a 10-day oscillator for a 20-day trading cycle, or a 14-day RSI justified by a roughly 28-calendar-day monthly cycle — rather than defaulting to a round number.

**11.7.2 The weekly/daily combination.** Weekly-chart oscillator signals serve as the primary trend filter for daily-chart signals: a daily buy/sell trigger is taken only when it agrees with the direction implied by the weekly reading. This is the same multi-timeframe discipline Section 11.3.3 applies to MACD specifically, generalized to any oscillator in this chapter.

| **▣ DATA — A three-layer RSI stack turns this into a concrete filter, not just a rule of thumb**                                                                                                                                                                                                          |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Section 11.10's Python implementation encodes Section 11.7.2 directly: daily RSI sets the regime bias (bull above 50, bear below), 4H RSI defines a pullback "setup zone" (40–55 for a long), and 1H RSI supplies the entry trigger (exit from oversold) — three timeframes, three roles, shifted forward before joining so no timeframe leaks future information into another. |

|                                                                    |
| --------------------------------------------------------------------- |
| **11.8 THE PRINCIPLE OF CONTRARY OPINION** |

**11.8.1 Concept.** Formulated by Humphrey B. Neill, Contrary Opinion holds that when the large majority of market participants agree on a trend's direction, they are usually about to be wrong — not because the crowd is inherently foolish, but because near-unanimous agreement means most of the buying (or selling) power that would extend the move has already been committed, leaving little capital left to push the trend further.

**11.8.2 Bullish Consensus (Market Vane).** Tracks professional advisory opinion, with an equilibrium point around 55% bullish. Readings above 90% or below 20% are treated as extreme warning zones where a contrarian starts looking for a reversal.

**11.8.3 Investors Intelligence.** Polls stock market advisors into Bullish, Bearish, and Correction categories. Bullish readings above 55% signal excessive optimism; readings below 35% signal excessive pessimism — the same asymmetric-crowding logic as Section 11.8.1, applied to a different survey.

Contrary Opinion is a sentiment overlay, not a standalone signal — it is one more input to weigh against the oscillator and trend readings from Sections 11.1–11.7, not a system that trades on its own.

|                                                                     |
| -------------------------------------------------------------------- |
| **11.9 READING THE RSI DASHBOARD — SIGNALS IN PRACTICE** |

Section 11.4 defined RSI, Section 11.4 set out its threshold and divergence rules, and Listings 11.1–11.2 built them. This section reads RSI on a live chart and turns those rules into an explicit trigger table.

**11.9.1 The dashboard.** Figure 11.1 shows the daily closing price above RSI(14), computed with Wilder's smoothing (Listing 11.1), with reference lines at 70, 50 and 30.

![RSI dashboard — BTC/USD daily, August 26 – September 17, 2026](../images/RSI_dashboard_BTC_2026-09_light.png)

*Figure 11.1 — RSI dashboard, BTC/USD daily, Aug 26 – Sep 17, 2026. Top: close. Bottom: RSI(14) with the 70 / 50 / 30 levels.*

**11.9.2 Reading the chart.**

1. **Aug 26–27: overbought at about 80–82.** This came straight after the August breakout, while ADX was still rising. In a trend, an overbought reading is strength, not a sell signal — the reason Section 11.4.2 recalibrates crypto thresholds to 80/20.
2. **Aug 27 → Sep 3: bearish divergence.** Price makes a higher high ($80.3k → $81.3k) while RSI makes a lower high (82 → 73): the warning Listing 11.2's `bearish_div` column is built to catch, and it preceded the whole September decline.
3. **Sep 4–10: range shift down.** RSI slides from the high 60s to the low 50s, each bounce lower than the last.
4. **Sep 15: the 50 line breaks.** RSI dips to about 48 at the price low near $75.6k — the first loss of the bullish floor.
5. **Sep 17: RSI 51.5.** Price made a lower low and so did RSI, so there is no bullish divergence yet. The dashboard's "Bullish" label comes from RSI sitting above 50, but 51.5 is a coin flip: anything between 45 and 55 is neutral.

**11.9.3 The signal table.** RSI's rules depend on the regime, so Table 11.3 states the regime condition explicitly for each trigger.

*Table 11.3 — RSI trigger conditions*

| **Signal** | **Conditions** | **Action** |
| --- | --- | --- |
| **BUY (range)** | ADX < 20 **and** `rsi_exit_os` true — RSI crosses back above 30 (Listing 11.2) | Open long; target the range midpoint |
| **SELL (range)** | ADX < 20 **and** `rsi_exit_ob` true — RSI crosses back below 70 | Open short, or exit longs |
| **BUY (trend pullback)** | ADX > 25, uptrend, RSI dips to 40–50 and turns up | Add to or enter the trend |
| **SELL (trend rally)** | ADX > 25, downtrend, RSI rallies to 50–60 and turns down | Add to or enter the short |
| **EXIT / WARNING** | `bearish_div` (or `bullish_div` for shorts) against the position, confirmed by a price break | Tighten the stop or close |
| **STAND ASIDE** | RSI between 45 and 55 with no divergence | No RSI-based trade |

| **▲ WARNING — Overbought is not a sell signal in a trend** |
| --- |
| RSI can stay above 70 for weeks in a strong trend, as it did in August. Enter on the cross back through the level, never on the level itself; treat a divergence as a warning until price confirms it, since divergences can repeat two or three times before price turns; and make sure the code uses Wilder's smoothing, or the values will not match any charting platform. |


|                                                                |
| ------------------------------------------------------------------ |
| **11.10 [CODE] HANDS-ON — BUILDING RSI AND MACD IN PYTHON** |

The rest of this chapter turns Sections 11.3 and 11.4's definitions into code — Wilder-smoothed RSI, threshold and divergence signals, the full MACD line/signal/histogram construction, and a statistical check of whether an RSI regime actually carries forward-return information.

**11.10.1 RSI — Wilder's smoothing, not a simple rolling mean.**

<table>
<thead>
<tr class="header">
<th><strong>💻 PYTHON · Listing 11.1 — RSI with correct Wilder smoothing</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>def compute_rsi(series: pd.Series, period: int = 14) -&gt; pd.Series:</p>
<p>    delta = series.diff()</p>
<p>    gain  = delta.clip(lower=0)</p>
<p>    loss  = -delta.clip(upper=0)</p>
<p></p>
<p>    # Wilder's smoothing: equivalent to an EMA with alpha = 1/period --</p>
<p>    # see Section 11.4's WARNING box. NOT .rolling().mean().</p>
<p>    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()</p>
<p>    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()</p>
<p></p>
<p>    rs  = avg_gain / avg_loss</p>
<p>    rsi = 100 - (100 / (1 + rs))</p>
<p>    return rsi</p>
<p></p>
<p>df['rsi_14'] = compute_rsi(df['close'], period=14)</p>
<p>df['rsi_9']  = compute_rsi(df['close'], period=9)  # faster variant for 1H crypto</p>
<p></p>
<p># Equivalent via the ta library:</p>
<p># from ta.momentum import RSIIndicator</p>
<p># df['rsi_14'] = RSIIndicator(close=df['close'], window=14).rsi()</p></td>
</tr>
</tbody>
</table>

**11.10.2 RSI threshold and divergence signals — Sections 11.4.2 and 11.4.3, in code.**

<table>
<thead>
<tr class="header">
<th><strong>💻 PYTHON · Listing 11.2 — RSI overbought/oversold crosses and divergence detection</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>OB, OS = 70, 30  # recalibrate to 80/20 for crypto bull/bear markets (Section 11.4.2)</p>
<p></p>
<p># Entry on cross, not on level -- more precise than "RSI is above 70"</p>
<p>df['rsi_exit_ob'] = (df['rsi_14'] &lt; OB) &amp; (df['rsi_14'].shift(1) &gt;= OB)  # exit overbought -&gt; short signal</p>
<p>df['rsi_exit_os'] = (df['rsi_14'] &gt; OS) &amp; (df['rsi_14'].shift(1) &lt;= OS)  # exit oversold  -&gt; long signal</p>
<p></p>
<p>def detect_rsi_divergence(df: pd.DataFrame, lookback: int = 14) -&gt; pd.DataFrame:</p>
<p>    """Tags Section 11.4.3 failure-swing-style divergence: price makes a new</p>
<p>    high/low that RSI does not confirm."""</p>
<p>    price_hh = df['close']  == df['close'].rolling(lookback).max()</p>
<p>    rsi_hh   = df['rsi_14'] == df['rsi_14'].rolling(lookback).max()</p>
<p>    price_ll = df['close']  == df['close'].rolling(lookback).min()</p>
<p>    rsi_ll   = df['rsi_14'] == df['rsi_14'].rolling(lookback).min()</p>
<p></p>
<p>    df['bearish_div'] = price_hh &amp; ~rsi_hh  # price high, RSI not confirming</p>
<p>    df['bullish_div'] = price_ll &amp; ~rsi_ll  # price low, RSI not confirming</p>
<p>    return df</p>
<p></p>
<p>df = detect_rsi_divergence(df, lookback=14)</p></td>
</tr>
</tbody>
</table>

**11.10.3 MACD — line, signal, and histogram (Section 11.3, in code).**

<table>
<thead>
<tr class="header">
<th><strong>💻 PYTHON · Listing 11.3 — MACD line, signal line, and histogram</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>fast, slow, signal = 12, 26, 9  # crypto 4H swing: try (8, 21, 5) -- keep the ~1:2.25 ratio</p>
<p></p>
<p>ema_fast = df['close'].ewm(span=fast, adjust=False).mean()</p>
<p>ema_slow = df['close'].ewm(span=slow, adjust=False).mean()</p>
<p></p>
<p>df['macd_line']   = ema_fast - ema_slow</p>
<p>df['macd_signal'] = df['macd_line'].ewm(span=signal, adjust=False).mean()</p>
<p>df['macd_hist']   = df['macd_line'] - df['macd_signal']</p>
<p></p>
<p># Equivalent via the ta library:</p>
<p># from ta.trend import MACD</p>
<p># macd = MACD(close=df['close'], window_fast=12, window_slow=26, window_sign=9)</p>
<p># df['macd_line'], df['macd_signal'], df['macd_hist'] = macd.macd(), macd.macd_signal(), macd.macd_diff()</p>
<p></p>
<p>df.dropna(subset=['macd_hist'], inplace=True)</p></td>
</tr>
</tbody>
</table>

**11.10.4 Histogram momentum and crossover events — Section 11.3.2's lead indicator, in code.**

<table>
<thead>
<tr class="header">
<th><strong>💻 PYTHON · Listing 11.4 — MACD signal-line crossover and histogram turning points</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p># Signal-line crossover</p>
<p>df['macd_cross_up']   = (df['macd_line'] &gt; df['macd_signal']) &amp; \</p>
<p>                         (df['macd_line'].shift(1) &lt;= df['macd_signal'].shift(1))</p>
<p>df['macd_cross_down'] = (df['macd_line'] &lt; df['macd_signal']) &amp; \</p>
<p>                         (df['macd_line'].shift(1) &gt;= df['macd_signal'].shift(1))</p>
<p></p>
<p># Histogram turning point -- fires BEFORE the signal-line crossover above (Section 11.3.2)</p>
<p>df['hist_peak']   = (df['macd_hist'] &lt; df['macd_hist'].shift(1)) &amp; \</p>
<p>                    (df['macd_hist'].shift(1) &gt;= df['macd_hist'].shift(2))</p>
<p>df['hist_trough'] = (df['macd_hist'] &gt; df['macd_hist'].shift(1)) &amp; \</p>
<p>                    (df['macd_hist'].shift(1) &lt;= df['macd_hist'].shift(2))</p>
<p></p>
<p># Trend-following entries, gated to zero-line side (stronger setup -- Section 11.1's EDGE box)</p>
<p>df['long_signal']  = df['macd_cross_up']   &amp; (df['macd_line'] &lt; 0)</p>
<p>df['short_signal'] = df['macd_cross_down'] &amp; (df['macd_line'] &gt; 0)</p></td>
</tr>
</tbody>
</table>

*Table 11.4 — MACD parameter sensitivity by use case*

| **Use case**            | **Fast** | **Slow** | **Signal** | **Timeframe** |
| ---------------------------- | ------------ | ------------ | -------------- | ------------------ |
| Equity / crypto daily standard    | 12               | 26               | 9                   | Daily                     |
| Crypto 4H swing                     | 8                | 21               | 5                   | 4H                         |
| Crypto 1H intraday                   | 6                | 13               | 5                   | 1H                         |

**11.10.5 Statistical validation — does the RSI regime actually carry information?**

<table>
<thead>
<tr class="header">
<th><strong>💻 PYTHON · Listing 11.5 — RSI regime bucketing and a forward-return significance test</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>import scipy.stats as stats</p>
<p></p>
<p># Bucket every bar by RSI zone (Section 11.4.2's thresholds)</p>
<p>bins   = [0, 30, 50, 70, 100]</p>
<p>labels = ['oversold', 'bearish', 'bullish', 'overbought']</p>
<p>df['rsi_regime'] = pd.cut(df['rsi_14'], bins=bins, labels=labels)</p>
<p></p>
<p>df['fwd_return_5'] = df['close'].pct_change(5).shift(-5)</p>
<p>print(df.groupby('rsi_regime')['fwd_return_5'].describe())</p>
<p></p>
<p># Kruskal-Wallis across the four regime buckets -- nonparametric, no normality</p>
<p># assumption on returns. p &lt; 0.05 -&gt; RSI regime carries real information about</p>
<p># forward returns, not just noise dressed up as four different-looking buckets.</p>
<p>groups = [g.dropna().values for _, g in df.groupby('rsi_regime')['fwd_return_5']]</p>
<p>h_stat, p_value = stats.kruskal(*groups)</p>
<p>print(f'H={h_stat:.3f}, p={p_value:.4f}')</p></td>
</tr>
</tbody>
</table>

|                                                                                 |
| ----------------------------------------------------------------------------------- |
| **11.11 [PROOF] VALIDATING AN OSCILLATOR SIGNAL BEFORE TRUSTING IT** |

A convincing-looking RSI divergence or MACD crossover on a chart is not evidence that it predicts anything. The checklist below applies Listing 11.5's discipline to any oscillator in this chapter before it goes into a live rule set.

<table>
<thead>
<tr class="header">
<th><strong>▶ PROOF — Three checks before trusting an RSI or MACD signal in production</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>Recalibrate thresholds to the actual instrument before testing. Section 11.4.2's 70/30 and Section 11.6's 80/20 levels are equity-market conventions; running Listing 11.5's Kruskal-Wallis test on the raw 70/30 buckets for a fast-moving crypto pair without first checking whether 80/20 fits better will understate whatever real signal is there.</p>
<p>Count your events before trusting a crossover hit rate. MACD signal-line crossovers (Listing 11.4) and RSI overbought/oversold exits (Listing 11.2) are sparse on a 90-day sample -- treat any hit rate built on fewer than ~30 events as preliminary, consistent with Chapter 10's PROOF standard for moving-average crossovers.</p>
<p>Test divergence systematically, not visually. Listing 11.2's `detect_rsi_divergence` flags every qualifying bar mechanically; scanning a chart by eye for "RSI didn't confirm that high" is prone to seeing divergences that fit a story already formed and missing the ones that don't.</p></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td><p><strong>◈ KEY INSIGHT<br />
</strong></p>
<p><em>"An oscillator does not replace a trend-following tool -- it covers the case a trend-following tool handles worst. RSI, MACD, CCI, and Stochastics are four different answers to the same underlying question (where, on a bounded scale, does current momentum sit relative to its own recent history), and none of them is validated by looking convincing on a chart -- only by testing whether the regime or the crossover it defines actually predicts what happens next."</em></p></td>
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
<td><p>Oscillators exist to trade nontrending, range-bound markets where moving-average systems whipsaw; three rules govern every one of them: market extremes, divergence, and zero/midline crossover.</p>
<p>Momentum and Rate of Change are the simplest oscillators but lack a fixed boundary; RSI, CCI, and Stochastics each impose a fixed scale (0-100, roughly &plusmn;100, and 0-100 respectively) to solve that problem.</p>
<p>MACD is a dual-EMA oscillator (12/26-period by default) plotted around a zero line, with a signal line (9-period EMA of the MACD line) and a histogram whose turning points precede the line/signal crossover itself.</p>
<p>RSI must be computed with Wilder's own smoothing (EMA, alpha = 1/period) rather than a simple rolling mean -- the two methods diverge from the TradingView/broker-platform standard used throughout this book.</p>
<p>Cycle-synchronized periods and a weekly-trend/daily-signal filter apply to oscillators the same way they apply to moving averages (Chapter 10); the Principle of Contrary Opinion adds a sentiment overlay (Bullish Consensus, Investors Intelligence) on top of the same crowding logic.</p>
<p>Every RSI/MACD signal built in Section 11.10 -- threshold crosses, divergence, histogram turning points -- needs the same forward-return significance test this book applies to every indicator, not just a chart that looks right.</p>
<p>Section 11.9 reads RSI on a live chart — an overbought reading that was strength, a bearish divergence that preceded the decline, and a 'Bullish' label at 51.5 that was really neutral — and states every RSI trigger with its regime condition (Table 11.3).</p></td>
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
<td><p><strong>Oscillator</strong> An indicator bounded (or conventionally bounded) around a fixed range, used to identify overbought/oversold extremes in nontrending markets.</p>
<p><strong>Momentum</strong> The simplest oscillator: today's close minus the close x days ago.</p>
<p><strong>Rate of Change (ROC)</strong> Momentum expressed as a ratio, centred on 100 instead of zero.</p>
<p><strong>MACD</strong> Moving Average Convergence/Divergence -- the difference between a fast and slow EMA, paired with a signal-line EMA of that difference.</p>
<p><strong>MACD histogram</strong> The difference between the MACD line and its signal line; turning points precede the line/signal crossover.</p>
<p><strong>Relative Strength Index (RSI)</strong> Wilder's 0-100-bounded oscillator built from smoothed average gains and losses.</p>
<p><strong>Wilder smoothing</strong> An EMA with alpha = 1/period; the correct smoothing method for RSI's gain/loss legs.</p>
<p><strong>Failure swing</strong> RSI's strongest signal: a failure to confirm a new price extreme while in overbought/oversold territory, followed by a break of a prior RSI trough or peak.</p>
<p><strong>Commodity Channel Index (CCI)</strong> Price compared to a moving average, normalized by mean deviation; conventionally read at &plusmn;100.</p>
<p><strong>Stochastics (%K, %D)</strong> Measures the close's position within its recent high-low range; %K/%D crosses at 80/20 are the significant signals.</p>
<p><strong>Larry Williams %R</strong> An inverted close-within-range oscillator on a 0 to −100 scale; −20 to 0 is overbought, −80 to −100 oversold.</p>
<p><strong>Contrary Opinion</strong> Humphrey B. Neill's principle that near-unanimous crowd agreement on a trend signals exhausted buying/selling power.</p>
<p><strong>Divergence</strong> An oscillator failing to confirm a new price high or low while in an extreme zone.</p>
<p><strong>Range shift</strong> The tendency of RSI to oscillate roughly between 40 and 80 in an uptrend and between 20 and 60 in a downtrend; a break out of the band warns of a regime change.</p></td>
</tr>
</tbody>
</table>

| **WHAT'S NEXT**                                                                                                                                                                                                                                                                                                                                    |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Chapter 12 — ADX and Directional Movement. This chapter's Listing 11.5 ran a single Kruskal-Wallis test on a single indicator; the same forward-return validation discipline applies to whatever indicator Chapter 12 builds, where ADX is used as a regime filter gating this chapter's oscillators against Chapter 10's trend-following tools. |


---

*Source: Restructured from `writing_plans/chapter_10_summary.md`, condensing source material on oscillators and contrary opinion into this project's house style (opening block, THIS CHAPTER COVERS, numbered N.x sections and sub-sections, data tables, EDGE/WARNING/DATA/PROOF callouts, KEY INSIGHT, Chapter Summary, Key Terms, What's Next). Code listings 14.1-14.5 are drawn from and cross-referenced against `code_snippets/ch06/rsi_v2.md` and `macd.md` -- the Wilder-smoothed RSI construction, threshold/divergence signals, and MACD line/signal/histogram code is functionally identical to those files, condensed and re-labelled to this chapter's listing numbers.*

**Updated 2026-09-22** — this chapter was renamed and renumbered from its original standalone draft slot ("Chapter 5") to Chapter 14 in this project's book, per user request ("shift right this chapters (chapter 3 should become chapter12)"), alongside three companion chapters shifting the same +9: Volume and Open Interest (3 -> 12), Moving Averages (4 -> 13), and ADX and Directional Movement (6 -> 15). All internal section, table, and listing references were renumbered from 5.x to 14.x throughout, including cross-references to the Moving Averages chapter (old "Chapter 4"/"Section 4.x" -> "Chapter 13"/"Section 13.x"). This chapter now sits in Part IV — Technical Analysis, immediately after Chapter 13 (Moving Averages); its Prereqs were updated to "Ch 13 (Moving Averages)" to match. WHAT'S NEXT was updated to point to Chapter 15 (ADX and Directional Movement), which is drafted and included in this same renumbering batch, replacing the draft's earlier note that it was "not yet drafted."

**Updated 2026-09-24** — added Section 14.10 (dashboard reading and trigger table, adapted from `writing_plans/*_Trading_Guide.md`), with Figure 14.1 and Table 14.4; the PROOF section was renumbered 14.10 → 14.11 (THIS CHAPTER COVERS, cross-references, Chapter Summary and Key Terms updated). Images live in `content_md/images/` (light-gray conversions of the BTC/USD dashboard screenshots; flagged for replacement by print-ready grayscale charts at 300 dpi).

**Updated 2026-10-03** -- Dividend Investing (formerly Chapter 6) was removed from the manuscript; Chapters 7-15 shifted down by one to 6-14. All internal section, table, listing and figure numbers and cross-chapter references in the body were decremented accordingly. Historical dated notes above are left as written.

**Updated 2026-10-06** — Renumbered from Chapter 13 to Chapter 14 after Chapter 2 (Exchange Traded Products) was split into Chapter 2 (ETFs) and Chapter 3 (ETCs and ETNs). Section, subsection, table, figure and listing numbers, the header digit box, Prereqs and cross-chapter references updated; dated notes above keep the numbering of their time.

**Updated 2026-10-06 (c)** — Part label aligned with `.claude/CLAUDE.md` §3.3: Part I — Investing and Stock Market (Ch 1–9), Part II — Technical Analysis (Ch 10–15); "opens/closes Part …" sentences adjusted.

**Updated 2026-10-06 (e)** — Cross-references updated after Futures Trading moved to Chapter 3 and ETCs/ETNs to Chapter 4 (old Ch 3–6 → 4–7).

**Updated 2026-10-07** — Renumbered (−1) after Bonds and Intermarket Analysis were merged into Chapter 6 (Bonds and the Intermarket Chain); section, table, figure and listing numbers and cross-references updated.

**Updated 2026-10-07 (c)** — Prereqs line normalised to "Chapter N (…)".
