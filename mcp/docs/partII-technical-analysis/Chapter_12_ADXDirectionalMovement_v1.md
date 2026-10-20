|                                                             |
| ----------------------------------------------------------- |
| **PYTHON FOR TRADERS: INVESTING, DERIVATIVES, AND TECHNICAL ANALYSIS APPLIED** |

|           |       |
| --------- | ----- |
| Chapter 12 | **12** |

**ADX and the Directional Movement System: Measuring Trend Strength, Not Direction**

*True Range, +DM/−DM, +DI/−DI, and Wilder's Average Directional Index — the theory behind trend-strength filtering, and the pandas/ta code that turns ADX into a regime switch*

Part II — Technical Analysis · Prereqs: Chapter 10 (Moving Averages), Chapter 11 (Oscillators and Contrary Opinion)

<table>
<thead>
<tr class="header">
<th><strong>THIS CHAPTER COVERS</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>12.1 Origins — Wilder's Directional Movement System</p>
<p>12.2 True Range and Directional Movement (+DM, −DM)</p>
<p>12.3 +DI, −DI, and the DX Formula</p>
<p>12.4 ADX — Wilder Smoothing and the Trend-Strength Scale</p>
<p>12.5 ADX Is Not Directional — Reading +DI/−DI Together</p>
<p>12.6 The Extreme Point Rule and Wilder's Original Trading System</p>
<p>12.7 ADX as a Regime Filter and Strategy Selector</p>
<p>12.8 Lag, Warm-Up, and Parameter Sensitivity</p>
<p>12.9 Reading the ADX Dashboard — Signals in Practice</p>
<p>12.10 [CODE] Hands-On — Building ADX, +DI, and −DI in Python</p>
<p>12.11 [PROOF] Validating an ADX Regime Filter Before Trusting It</p></td>
</tr>
</tbody>
</table>

|                                                                     |
| -------------------------------------------------------------------- |
| **12.1 ORIGINS — WILDER'S DIRECTIONAL MOVEMENT SYSTEM** |

J. Welles Wilder Jr. introduced the Directional Movement System — True Range, +DI, −DI, and ADX — in *New Concepts in Technical Trading Systems* (1978), the same book that gave the field RSI, Average True Range, and the Parabolic SAR. RSI and ADX share Wilder's own smoothing method (Section 11.4's Wilder-smoothing WARNING box applies here too: an EMA with alpha = 1/period, not a simple rolling mean), but they answer different questions. RSI asks *is this specific move overextended?* ADX asks a question none of this book's tools so far have answered directly: *is the market trending strongly enough, right now, for a trend-following tool to be worth using at all?*

**12.1.1 The gap ADX fills.** Chapter 10's crossover systems and Chapter 11's oscillators are both correct in their own regime and both wrong in the other one — a moving-average crossover whipsaws in a range, and an oscillator's overbought reading gets run over in a strong trend. Neither tool measures which regime is currently in force. ADX was built specifically to answer that prior question, as a filter that sits in front of both toolkits rather than beside them.

|                                                                     |
| -------------------------------------------------------------------- |
| **12.2 TRUE RANGE AND DIRECTIONAL MOVEMENT (+DM, −DM)** |

**12.2.1 True Range.** A simple high-minus-low understates a gapping or limit-move day, so Wilder defined True Range (TR) as the largest of three measures: today's high minus today's low, today's high minus yesterday's close (absolute value), and today's low minus yesterday's close (absolute value). TR is the raw volatility unit every other calculation in this chapter is normalized against.

**12.2.2 Directional Movement.** Directional Movement compares today's high and low to yesterday's, not today's close to yesterday's — this is the detail that trips up most manual implementations, including reasonable-looking ones. For each bar:

*Table 12.1 — Directional Movement: how +DM and −DM are assigned*

| **Candle shape**                                                          | **+DM**  | **−DM**  | **Result**                    |
| -------------------------------------------------------------------------- | -------- | -------- | ------------------------------ |
| High rises more than low falls (up-move dominates)                         | positive | 0        | Pure +DM                       |
| Low falls more than high rises (down-move dominates)                       | 0        | positive | Pure −DM                       |
| High falls or ties, and low falls or ties (inside/down bar, no up-move)    | 0        | positive | −DM only, if low fell          |
| Neither the up-move nor the down-move is positive (inside day)             | 0        | 0        | No directional movement at all |

Exactly one of +DM or −DM can be non-zero on any given bar — never both, and Wilder's own definition explicitly rejects the case where both the day's range expanded upward and downward from picking a side by magnitude comparison alone; whichever move is larger wins, and the smaller one is set to zero.

| **▲ WARNING — A bearish close does not guarantee −DM dominance**                                                                                                                                                                                                                                  |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DM compares highs and lows across bars, not closes. A daily candle that gaps or spikes above the prior day's high before selling off hard — but whose low still holds above the prior day's low — produces pure +DM and zero −DM for that bar, regardless of how far the close fell intraday. Traders who expect a red candle to always mean −DI dominance will occasionally see +DI spike on an obviously bearish day and assume the indicator is broken; it isn't. Diagnose a suspicious bar directly (Listing 12.2) before doubting the calculation. A finer timeframe (1H instead of daily) usually resolves the same session into multiple bars and shows the expected −DI-dominant read, because the spike and the subsequent breakdown land in different bars instead of being compressed into one. |

|                                                                     |
| -------------------------------------------------------------------- |
| **12.3 +DI, −DI, AND THE DX FORMULA** |

**12.3.1 From raw movement to a percentage.** +DM and −DM are Wilder-smoothed (alpha = 1/period, the same recursive method as RSI) and then divided by the similarly Wilder-smoothed True Range (Average True Range), scaled to 100. This produces +DI and −DI — two bounded, comparable percentages instead of raw price-unit magnitudes, which is what makes them plottable together and comparable across instruments.

**12.3.2 DX — the directional divergence.** The Directional Index (DX) measures how far apart +DI and −DI currently are, as a percentage of their sum: `DX = 100 × |+DI − −DI| / (+DI + −DI)`. DX is 0 when +DI and −DI are equal (no directional bias) and approaches 100 when one completely dominates the other. DX on its own is noisy bar-to-bar — it is the input to ADX, not the finished indicator.

|                                                                     |
| -------------------------------------------------------------------- |
| **12.4 ADX — WILDER SMOOTHING AND THE TREND-STRENGTH SCALE** |

**12.4.1 A second smoothing pass.** ADX is DX run through Wilder's smoothing a second time. This double-smoothing (once for +DM/−DM into +DI/−DI, once again for DX into ADX) is why ADX reads slower and more stable than either DI line — and why it lags regime changes, a cost covered in Section 12.8.

**12.4.2 Reading the scale.** Wilder's original thresholds, still the market convention, classify the trend-strength regime directly from the ADX value:

*Table 12.2 — ADX regime classification (Wilder's original thresholds)*

| **ADX value** | **Regime**       | **Interpretation**                                                          |
| ------------- | ---------------- | ---------------------------------------------------------------------------- |
| Below 20      | Ranging          | No tradeable trend; trend-following tools whipsaw, oscillators are favored   |
| 20 – 40       | Developing trend | A trend is forming or in force; trend-following tools become viable         |
| 40 – 50       | Strong trend     | High-conviction trend; momentum typically carries                           |
| Above 50      | Extreme / exhausted | Very strong trend, but historically elevated risk of exhaustion or reversal |

**12.4.3 Rising vs. falling — the line's direction matters as much as its level.** The emphasis here sits less on the static bands in Table 12.2 and more on which way the ADX line is *moving*. A **rising ADX line**, at almost any level, signals an active trending phase in which trend-following systems (moving-average crossovers, Chapter 10's Donchian channel breakouts, Wilder's own Parabolic SAR) perform best; a **falling ADX line** signals a nontrending, choppy range in which those same trend-following systems whipsaw and Chapter 11's oscillators (RSI, Stochastics, CCI) are the more appropriate tool. Two specific turns matter most in this dynamic reading:

*Table 12.3 — ADX line direction: a dynamic reading, alongside Table 12.2's static bands*

| **Movement**                    | **Interpretation**                                                                                     |
| --------------------------------- | --------------------------------------------------------------------------------------------------------- |
| ADX rising from below 20           | Signals the onset or resumption of a new trending market                                                  |
| ADX dipping below 40 after being above it | An early warning that the prevailing trend is weakening or ending, often ahead of a move back into a trading range |
| ADX holding above 40               | A mature, highly directional trend — Table 12.2's "strong trend" zone — that may soon consolidate or reverse |

Note the asymmetry with Table 12.2's static bands: a mature trend can sit above 40 (nominally "strong") for a long stretch, but the moment that same line *turns down* — even while still numerically above 40 — is the actual exhaustion signal, not the crossing of any fixed level on the way back down. A regime filter built only on Table 12.2's bands (as Listing 12.3's `classify_adx_regime` is) will miss this turning-point warning entirely; Listing 12.5's rate-of-change check (`adx.diff(3)`) is the same logic applied to the falling side, and is worth computing alongside the rising-side early-warning use already shown there.

| **◆ EDGE — ADX rewards recalibration, not the fixed number 25**                                                                                                                                                                                                                                  |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A fixed threshold of 25 is a reasonable default for daily equity index data — it is not a law of the indicator. A fast-moving instrument or a shorter intraday timeframe often runs at structurally higher ADX values, which makes a fixed 25 threshold fire too early and too often. Section 12.7 builds a percentile-based threshold, calibrated on the instrument's own recent ADX distribution, as the more robust alternative once you're trading anything other than a daily equity chart. |

|                                                                     |
| -------------------------------------------------------------------- |
| **12.5 ADX IS NOT DIRECTIONAL — READING +DI/−DI TOGETHER** |

**12.5.1 The single most common misreading of ADX.** ADX measures how strongly the market is trending — it says nothing about which way. An ADX reading of 45 during a sharp decline and an ADX reading of 45 during a sharp rally look identical on the ADX line itself; only +DI and −DI, plotted alongside it, say which direction that strength belongs to. Any rule built on "ADX rising" without also checking which of +DI or −DI is on top is incomplete by construction.

**12.5.2 The DI crossover as a directional trigger.** When +DI crosses above −DI, buying pressure has just taken the lead in the same Wilder-smoothed sense that defines the rest of this indicator family — this is known as a **DMI buy signal**; the mirrored −DI-over-+DI cross is a **DMI sell signal**. On its own, a DI crossover is a low-conviction signal — it fires constantly in a ranging market, which is exactly the condition Section 12.4's ADX reading is built to flag. Sections 12.6 and 12.7 both use the DI cross only after ADX confirms a trend is actually in force.

|                                                                     |
| -------------------------------------------------------------------- |
| **12.6 THE EXTREME POINT RULE AND WILDER'S ORIGINAL TRADING SYSTEM** |

**12.6.1 Wilder's own entry rule.** Wilder's original Directional Movement trading system does not enter on the DI crossover itself. It waits: on the day +DI crosses above −DI, it records that day's high as the "extreme point." A long entry triggers only if a subsequent day's price exceeds the extreme point — the crossover sets up the trade, price confirmation authorizes it. The mirrored version applies on a −DI-over-+DI cross, using that day's low as the extreme point for a short entry.

**12.6.2 The built-in stop.** The system's initial stop is the opposite extreme — the low of the signal day for a long, the high of the signal day for a short. If price never exceeds the extreme point, no trade is taken at all; if it does, the trade already carries a stop defined by the same bar that generated the signal, at no extra calculation cost.

| **● DATA — Why the Extreme Point Rule still matters after fifty years of indicator design**                                                                                                                                                                                                                                                  |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A raw DI crossover fires on every minor wiggle in a choppy market — this is exactly the false-signal problem Chapter 10 warned about for moving-average crossovers. Requiring price to actually exceed the crossover day's extreme before acting adds a confirmation step that costs some entry price but removes a meaningful share of the whipsaw trades a bare crossover would take. Section 12.10's code implements the DI cross as a signal column; the extreme-point confirmation is a direct filter on top of it (compare the entry bar's high/low against the signal-day extreme before acting), left as a Listing 12.4 extension rather than hard-coded, since the confirmation window (how many bars to wait for the breakout) is a parameter worth testing per instrument. |

|                                                                     |
| -------------------------------------------------------------------- |
| **12.7 ADX AS A REGIME FILTER AND STRATEGY SELECTOR** |

**12.7.1 ADX's real job in this book.** Used as Wilder designed it, ADX generates its own trade signals. Used the way most systematic traders actually deploy it today, ADX is a meta-indicator: a gate that decides which of this book's other tools gets to trade at all in the current regime. High ADX routes control to Chapter 10's trend-following crossovers; low ADX routes control to Chapter 11's oscillators; the regime-switch code in Listing 12.3 implements exactly this split.

**12.7.2 A dynamic alternative to the fixed threshold.** Rather than hard-coding 25, compute the instrument's own rolling ADX percentile and trend on relative extremes instead of an absolute level — Listing 12.3 builds both the fixed-threshold and percentile-based versions side by side so the trade-off is visible directly in the output columns.

**12.7.3 Cross-market screening and the Parabolic SAR filter.** This extends the regime-filter idea in 12.7.1 one level up: rather than applying it to a single instrument, scan a basket of markets or instruments and rank them by their current ADX reading, then concentrate trend-following capital in whichever ones carry the highest ADX — the logic being that a trend-following system deployed against the strongest available trend has better odds than the same system run blind across everything at once. The same gate also pairs naturally with Wilder's own Parabolic SAR: SAR alone reverses and stops-and-reverses constantly in a sideways market, but gating it on a rising ADX (or ADX above the trending threshold) confines its stop-and-reverse signals to periods when a dominant directional move is actually in force, filtering out a meaningful share of the false signals SAR alone would generate in a range. Parabolic SAR itself is outside this book's current chapter scope; the filtering logic is the transferable part, and it applies to any trend-following system Chapter 10 or a future chapter introduces, not to SAR specifically.

|                                                                     |
| -------------------------------------------------------------------- |
| **12.8 LAG, WARM-UP, AND PARAMETER SENSITIVITY** |

**12.8.1 ADX lags regime transitions.** Wilder's double-smoothing (Section 12.4.1) that makes ADX stable also makes it slow: ADX typically lags an actual regime transition by three to five bars. A trend can be several bars old before ADX's own threshold confirms it. Listing 12.5 tracks the *rate of change* of ADX rather than its level, as an earlier — noisier — signal that a trend may be emerging from a low base.

**12.8.2 Warm-up period.** ADX needs roughly `2 × period` bars of history before its value stabilizes: one period's worth of bars for the +DM/−DM smoothing into +DI/−DI, and a second period's worth for the DX-to-ADX smoothing on top of that.

*Table 12.4 — ADX warm-up requirement by period*

| **Period** | **Warm-up bars** | **% of a 1-year daily history (~252 bars)** |
| ---------- | ----------------- | --------------------------------------------- |
| 10         | 20                 | 7.9%                                           |
| 14 (Wilder's default) | 28     | 11.1%                                          |

Drop the warm-up window explicitly (`df.dropna(subset=["adx"])`) before backtesting or computing any statistic on the ADX column — the same discipline this book has applied to every rolling-window indicator since Chapter 10.

**12.8.3 Parameter sensitivity.**

*Table 12.5 — ADX parameter sensitivity by use case*

| **Use case**            | **Period** | **Trend threshold**  | **Timeframe**  |
| ------------------------ | ---------- | ---------------------- | --------------- |
| Equity standard          | 14         | 25                     | Daily           |
| Fast-moving instrument, swing | 14    | 25                     | Daily / 4H      |
| Fast-moving instrument, intraday | 10  | 20                     | 1H              |
| Regime filter only        | 14         | Percentile-based       | Any             |
| ML / statistical feature  | 7 and 14   | —                      | Any             |

|                                                                     |
| -------------------------------------------------------------------- |
| **12.9 READING THE ADX DASHBOARD — SIGNALS IN PRACTICE** |

Sections 12.4–12.7 explained how to read ADX, +DI and −DI, and Listings 12.1–12.5 built them. This section reads the three lines on a live chart, writes the rules as an explicit trigger table, and then uses ADX as intended — as the regime gate — across all the dashboards of Part II.

**12.9.1 The dashboard.** Figure 12.1 shows daily candles above ADX(14), +DI and −DI (Listing 12.1), with the 25 threshold as a dashed line.

![ADX dashboard — BTC/USD daily, July to September 2026](../images/ADX_dashboard_BTC_2026-09_light.png)

*Figure 12.1 — ADX dashboard, BTC/USD daily, late July – mid-September 2026. Bottom pane: ADX, +DI, −DI and the 25 threshold (dashed). Header readings at the snapshot: ADX 42.3, +DI 27.5, −DI 14.0.*

**12.9.2 Reading the chart.**

1. **Late July – Aug 17: range.** ADX sits at 12–15 and the DI lines keep crossing. Table 12.2 says: no trend trades.
2. **Aug 18–21: breakout.** +DI jumps above 50 and −DI collapses. The first DI crossover happens while ADX is still near 13, so the gate ignores it; the trigger fires when ADX rises through 25 with +DI on top.
3. **Late August – early September: a mature trend.** ADX climbs to about 50 — after most of the price move is done. That is Section 12.8.1's lag, made visible.
4. **Mid-September: fading.** ADX has turned down from its peak (Table 12.3's exhaustion reading), the DI spread is narrowing, and price moves sideways between about $76k and $82k. The header still reads "Strong trend · Bull"; the slope says otherwise.

**12.9.3 The signal table.**

*Table 12.6 — ADX trigger conditions*

| **Signal** | **Conditions (all must be true)** | **Action** |
| --- | --- | --- |
| **BUY** | +DI above −DI **and** ADX rising **and** either ADX crosses above 25, or +DI crosses above −DI while ADX > 25 (Listings 12.3–12.4) | Open long; stop at the signal bar's low (Section 12.6) |
| **SELL** | −DI above +DI **and** ADX rising **and** either ADX crosses above 25, or −DI crosses above +DI while ADX > 25 | Open short; stop at the signal bar's high |
| **EXIT** | ADX turns down from above 40, **or** the DI lines cross against the position | Close or reduce |
| **STAND ASIDE** | ADX below 20 | No trend trades; route to Chapter 11's oscillators |

**12.9.4 One market, five dashboards.** Section 12.7.1 described ADX as the gate that decides which of Part II's tools gets to trade. Table 12.7 puts that into practice: the same market, in the same mid-September window, read through every dashboard in Chapters 9–12.

*Table 12.7 — BTC/USD in mid-September 2026, read through each dashboard*

| **Dashboard** | **Reading** | **Verdict** |
| --- | --- | --- |
| ADX (Figure 12.1) | ADX 42 and falling; DI spread narrowing | Trend fading; no new trend entries |
| Moving averages (Figure 10.1) | Price below EMA 9/12, sitting on EMA 26; MACD positive but shrinking | Stack no longer bullish; trend not yet broken |
| RSI (Figure 11.1) | 51.5 after a bearish divergence and a break of 50 | Neutral momentum |
| Volume/OBV (Figure 9.1) | OBV lower highs since late August | Participation fading |
| Bollinger Bands, hourly (Figure 10.2) | Close below the lower band after a squeeze | Short-term break lower |

No single panel is decisive, but all five point the same way: the August trend has lost its strength and the market is consolidating, with the short-term chart starting to break lower. The gate's instruction follows directly: stop taking Chapter 10's trend signals, and if ADX falls below 20, hand control to Chapter 11's range tools.

| **▲ WARNING — A high ADX is not an entry signal** |
| --- |
| ADX peaks near the end of a move, so a high reading is where trends mature, not where they start. It has no direction — a high ADX in a selloff is a strong downtrend — and DI crossovers below ADX 20 are mostly noise. Dashboard labels such as “Strong trend” describe the level; always check the slope before acting on them. |


|                                                                     |
| -------------------------------------------------------------------- |
| **12.10 [CODE] HANDS-ON — BUILDING ADX, +DI, AND −DI IN PYTHON** |

**12.10.1 True Range, Directional Movement, and Wilder smoothing from scratch.**

**💻 PYTHON · Listing 12.1 — `compute_adx`: True Range, +DI/−DI, DX, and ADX with correct Wilder smoothing**

```python
import pandas as pd

def compute_adx(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    Adds 'adx', 'plus_di', 'minus_di' columns to df.
    Requires 'high', 'low', 'close' columns. See Section 12.8.2 for warm-up.
    """
    high, low, close = df["high"], df["low"], df["close"]

    # True Range (Section 12.2.1) -- largest of three measures, not just high-low
    tr = pd.concat([
        high - low,
        (high - close.shift(1)).abs(),
        (low  - close.shift(1)).abs()
    ], axis=1).max(axis=1)

    # Directional Movement (Section 12.2.2, Table 12.1) -- compares highs/lows
    # across bars, NOT today's close to yesterday's. This is the detail every
    # naive implementation gets wrong.
    up_move   = high - high.shift(1)
    down_move = low.shift(1) - low

    plus_dm  = up_move.where((up_move > down_move) & (up_move > 0), 0.0)
    minus_dm = down_move.where((down_move > up_move) & (down_move > 0), 0.0)

    # Wilder smoothing (alpha = 1/period, same method as RSI in Section 11.10.1)
    alpha = 1 / period
    atr      = tr.ewm(alpha=alpha, adjust=False).mean()
    plus_di  = 100 * plus_dm.ewm(alpha=alpha, adjust=False).mean()  / atr
    minus_di = 100 * minus_dm.ewm(alpha=alpha, adjust=False).mean() / atr

    # DX (Section 12.3.2) and a second Wilder-smoothing pass into ADX (12.4.1)
    dx  = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    adx = dx.ewm(alpha=alpha, adjust=False).mean()

    df = df.copy()
    df["adx"]      = adx
    df["plus_di"]  = plus_di
    df["minus_di"] = minus_di
    return df

df = compute_adx(df, period=14)
df = df.dropna(subset=["adx"])   # drop the warm-up window, Section 12.8.2
```

**12.10.2 The library shortcut.** The `ta` package implements the same Wilder recursion; use it once Listing 12.1 has confirmed you understand what's being computed and why.

**💻 PYTHON · Listing 12.2 — ADX via the `ta` library, and diagnosing a suspicious +DI spike**

```python
from ta.trend import ADXIndicator

adx_obj = ADXIndicator(high=df["high"], low=df["low"], close=df["close"], window=14)
df["adx"]      = adx_obj.adx()
df["plus_di"]  = adx_obj.adx_pos()
df["minus_di"] = adx_obj.adx_neg()

# Diagnose a suspicious bar (the WARNING box in Section 12.2.2): inspect the
# raw high/low expansion directly rather than assuming the indicator is wrong.
df["up_move"]   = df["high"]  - df["high"].shift(1)
df["down_move"] = df["low"].shift(1) - df["low"]
df["dm_plus"]   = df["up_move"].where(
    (df["up_move"] > df["down_move"]) & (df["up_move"] > 0), 0.0)
df["dm_minus"]  = df["down_move"].where(
    (df["down_move"] > df["up_move"]) & (df["down_move"] > 0), 0.0)

suspicious_date = "2026-06-24"   # replace with the bar you're investigating
print(df.loc[suspicious_date,
      ["high", "low", "close", "up_move", "down_move", "dm_plus", "dm_minus"]])
```

**12.10.3 Regime classification, fixed and percentile-based (Section 12.4.2, Section 12.7.2).**

**💻 PYTHON · Listing 12.3 — ADX regime labels, a percentile-based dynamic threshold, and the trend/range strategy-selector gate**

```python
def classify_adx_regime(adx_series: pd.Series) -> pd.Series:
    """Categorical regime label from Table 12.2's fixed Wilder thresholds."""
    return pd.cut(
        adx_series,
        bins=[0, 20, 40, 50, 100],
        labels=["ranging", "developing_trend", "strong_trend", "exhausted"]
    )

df["adx_regime"] = classify_adx_regime(df["adx"])

# Percentile-based threshold (Section 12.7.2) -- calibrated on the instrument's
# own recent distribution instead of a fixed 25, per the EDGE box in 12.4.2.
lookback = 126   # ~6 months of daily bars; adjust to the bar size in use
df["adx_p40"] = df["adx"].rolling(lookback).quantile(0.40)
df["adx_p60"] = df["adx"].rolling(lookback).quantile(0.60)

df["adx_regime_dynamic"] = "neutral"
df.loc[df["adx"] < df["adx_p40"], "adx_regime_dynamic"] = "ranging"
df.loc[df["adx"] > df["adx_p60"], "adx_regime_dynamic"] = "trending"

# Strategy-selector gate (Section 12.7.1): route to trend tools above the
# threshold, oscillators below it. This is ADX's most common role in practice.
trending = df["adx"] > 25   # -- swap for df["adx_regime_dynamic"] == "trending"
ranging  = df["adx"] < 20   #    to use the percentile version instead
```

**12.10.4 The DI crossover as a directional confirmation (Section 12.5.2, Section 12.6).**

**💻 PYTHON · Listing 12.4 — +DI/−DI crossover signals, combined with the ADX regime gate from Listing 12.3**

```python
# DI crossover (Section 12.5.2)
df["di_cross_up"]   = (df["plus_di"] > df["minus_di"]) & \
                       (df["plus_di"].shift(1) <= df["minus_di"].shift(1))
df["di_cross_down"] = (df["minus_di"] > df["plus_di"]) & \
                       (df["minus_di"].shift(1) <= df["plus_di"].shift(1))

# Combine with Chapter 10's EMA crossover, gated by the ADX regime (Section 12.7.1):
# only take a trend-following signal when ADX confirms a trend is in force AND
# the DI lines agree with the trade's direction.
df["ema_9"]  = df["close"].ewm(span=9,  adjust=False).mean()
df["ema_21"] = df["close"].ewm(span=21, adjust=False).mean()
ema_cross_up = (df["ema_9"] > df["ema_21"]) & (df["ema_9"].shift(1) <= df["ema_21"].shift(1))

df["trend_long"]  = ema_cross_up  & trending & (df["plus_di"]  > df["minus_di"])
ema_cross_down = (df["ema_9"] < df["ema_21"]) & (df["ema_9"].shift(1) >= df["ema_21"].shift(1))

df["trend_short"] = ema_cross_down & trending & (df["minus_di"] > df["plus_di"])
```

**12.10.5 Detecting an emerging trend before ADX confirms it (Section 12.8.1).**

**💻 PYTHON · Listing 12.5 — ADX rate-of-change as an earlier, noisier regime-change signal**

```python
df["adx_roc"] = df["adx"].diff(3)   # 3-bar rate of change (Section 12.8.1)

# Rising ADX from a low base suggests a trend is emerging, ahead of the
# Table 12.2 threshold confirming it outright -- earlier, and noisier.
df["trend_emerging"] = (df["adx"] < 25) & (df["adx_roc"] > 2.0)
```

|                                                                     |
| -------------------------------------------------------------------- |
| **12.11 [PROOF] VALIDATING AN ADX REGIME FILTER BEFORE TRUSTING IT** |

A rising ADX line looking visually convincing next to a strong trend on a chart is not evidence that gating a strategy on it improves that strategy. The checklist below applies this book's forward-return validation standard specifically to ADX as a filter, not as a standalone signal.

| **▶ PROOF — Three checks before trusting an ADX regime filter in production**                                                                                                                                                                                                                                  |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Stratify, don't eyeball. Bucket a trend-following strategy's forward returns by the ADX quintile in force when each signal fired, and compare Sharpe ratio per bucket (Listing 12.6). A monotonically increasing Sharpe as ADX rises is the expected, falsifiable result — if the top ADX quintile does not outperform the bottom one, the filter is not doing its job on this instrument. |
| Recalibrate thresholds before testing. Section 12.4.2's EDGE box already flags this: Table 12.2's 20/40/50 levels are equity-index conventions. Running Listing 12.6 on the raw fixed-threshold buckets for a structurally faster-moving instrument without first checking the percentile-based version (Listing 12.3) will understate whatever real regime effect is there. |
| Account for ADX's own lag (Section 12.8.1) in the backtest. Because ADX confirms a trend three to five bars after it starts, a naive backtest that enters exactly on the threshold cross is already trading a trend that is partially over; compare results with and without the rate-of-change early-warning signal from Listing 12.5 before concluding the filter adds no edge. |

**💻 PYTHON · Listing 12.6 — Stratifying a trend-following strategy's returns by ADX quintile**

```python
import numpy as np

# df already has 'adx' and a forward-return column for the strategy being gated,
# e.g. df["fwd_return_5"] = df["close"].pct_change(5).shift(-5)
df["adx_quintile"] = pd.qcut(df["adx"], 5, labels=False, duplicates="drop")

quintile_sharpe = (
    df.groupby("adx_quintile")["fwd_return_5"]
      .apply(lambda r: r.mean() / r.std() * np.sqrt(252 / 5))
)
print(quintile_sharpe)
# Expected if the filter works: quintile_sharpe rises roughly monotonically
# from quintile 0 (lowest ADX) to quintile 4 (highest ADX).
```

<table>
<tbody>
<tr class="odd">
<td><p><strong>◈ KEY INSIGHT<br />
</strong></p>
<p><em>"ADX does not tell you which way to trade -- it tells you whether trading a direction is worth attempting right now. Treated as a standalone signal it is a mediocre, laggy trend-follower; treated as the regime gate in front of Chapter 10's moving averages and Chapter 11's oscillators, it answers the one question neither of those tools can answer about itself: which one should even be switched on."</em></p></td>
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
<td><p>ADX, +DI, and −DI form Wilder's Directional Movement System, built from True Range and Directional Movement (+DM/−DM), which compare bar-to-bar highs and lows rather than closes.</p>
<p>+DI and −DI are Wilder-smoothed, percentage-normalized versions of +DM/−DM; DX measures how far apart they are; ADX is DX smoothed a second time, which is why it lags regime changes by three to five bars.</p>
<p>ADX measures trend strength, not direction -- a bearish candle can still produce a pure +DM reading (Section 12.2.2's WARNING box), and only +DI/−DI say which way a trending market is actually moving.</p>
<p>Wilder's original Extreme Point Rule confirms a DI crossover with a subsequent price breakout before entering, rather than trading the crossover itself, and supplies a built-in stop at no extra cost.</p>
<p>ADX's most common modern use is as a regime filter and strategy selector: gate Chapter 10's trend-following tools on high ADX and Chapter 11's oscillators on low ADX, using either a fixed threshold or the more robust percentile-based version.</p>
<p>The line's direction matters as much as its level: a rising ADX favors trend-following tools at almost any value, a falling ADX favors oscillators, and a downturn from above 40 is an early warning of trend exhaustion -- distinct from, and easy to miss under, the static 20/40/50 bands alone.</p>
<p>The regime-filter idea scales beyond one instrument: ranking multiple markets by current ADX and concentrating trend-following capital in the highest-ADX ones, and gating a stop-and-reverse system like Parabolic SAR on a rising ADX, both apply the same filter described for a single moving-average system.</p>
<p>Any ADX-gated strategy needs Section 12.11's quintile-stratified forward-return test before deployment -- a rising ADX line next to a strong trend on a chart is not evidence the filter improves results.</p>
<p>Section 12.9 reads ADX, +DI and −DI on a live chart, writes the rules as a trigger table (Table 12.6), and applies ADX as the regime gate across all five Part II dashboards (Table 12.7).</p></td>
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
<td><p><strong>True Range (TR)</strong> The largest of three measures: high−low, high−prior close, and low−prior close (absolute values); the volatility unit ADX is normalized against.</p>
<p><strong>Directional Movement (+DM, −DM)</strong> The larger of a bar's up-move or down-move in high/low terms, with the smaller of the two set to zero; never both non-zero on the same bar.</p>
<p><strong>+DI / −DI</strong> Wilder-smoothed +DM/−DM divided by Wilder-smoothed True Range, scaled to a percentage; bounded, comparable directional indicators.</p>
<p><strong>DX (Directional Index)</strong> 100 × the absolute difference between +DI and −DI, divided by their sum; the noisy input ADX is built from.</p>
<p><strong>ADX (Average Directional Index)</strong> DX run through a second pass of Wilder smoothing; measures trend strength on a 0-100 scale, not trend direction.</p>
<p><strong>Wilder smoothing</strong> An EMA with alpha = 1/period; the same recursive method underlying RSI (Chapter 11) and ADX.</p>
<p><strong>Extreme Point Rule</strong> Wilder's original entry confirmation: the high (or low) of a DI-crossover day must be exceeded by a subsequent bar before a trade is taken.</p>
<p><strong>Regime filter / strategy selector</strong> Using ADX to decide whether trend-following tools or range-bound oscillators should be active, rather than as a standalone trade signal.</p>
<p><strong>Percentile-based threshold</strong> An ADX trend/range cutoff calibrated on an instrument's own rolling ADX distribution instead of a fixed level like 25.</p>
<p><strong>DMI buy / sell signal</strong> The name for the +DI/−DI crossover: a DMI buy signal on +DI crossing above −DI, a DMI sell signal on the reverse.</p>
<p><strong>Rising / falling ADX line</strong> The slope-based reading of ADX (Section 12.4.3): a rising line signals a trending phase regardless of level, a falling line signals a return to range, and a downturn from above 40 is an early trend-exhaustion warning.</p>
<p><strong>Cross-market screening</strong> Ranking multiple instruments by current ADX reading and concentrating trend-following capital in the highest-ADX markets (Section 12.7.3).</p>
<p><strong>Parabolic SAR</strong> Wilder's stop-and-reverse trend-following system, introduced in the same 1978 book as ADX; gating it on a rising ADX filters out a share of the false stop-and-reverse signals it generates in a sideways market (Section 12.7.3).</p>
<p><strong>Regime dashboard</strong> Reading the same market through ADX, moving averages, RSI, volume and Bollinger Bands together, with ADX deciding which of the other tools' signals are acted on (Section 12.9.4).</p></td>
</tr>
</tbody>
</table>

| **WHAT'S NEXT**                                                                                                                                                                                                                                                                                                                                    |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| This chapter closes out the indicator toolkit built across Chapters 8 through 12 -- foundations, volume/open interest, moving averages, oscillators, and now trend-strength filtering -- giving Part II a complete set of tools for reading price, confirming it with volume and open interest, smoothing it into a trend signal, catching overbought/oversold extremes, and gating all of it on whether a trend is even in force. Carry the ADX regime-filter idea forward as the standing gate in front of Chapter 10's trend-following tools and Chapter 11's oscillators, not as a one-time read. Appendix A follows: the capital-allocation ceilings, the 2% per-trade rule, and the bias checks that sit in front of every signal Part II produces. |


---

*Source: Theory content (origins, True Range, Directional Movement, DX/ADX construction, the Extreme Point Rule, and the rising/falling ADX-line reading) is drawn from Wilder's original Directional Movement System. Code listings 15.1-15.6 are condensed and re-labelled from this project's own ADX rules module and its production SQL views. Not part of this chapter's book material: SQL productionization views, a bug audit, and crypto-exchange-specific fetch helpers from the source project files, which are infrastructure content for this project's own data pipeline rather than book content, and were deliberately left out.*

**Flagged, not resolved in this pass:** Chapter 15's Section 15.7 EDGE box contains a line written before this chapter existed in this project's numbering -- "Section 15.7's ADX-gated approach exists specifically to tell these two cases apart" -- which is a stale forward-reference (Section 15.7 is "Cycles, Multiple Time Frames, and the Weekly/Daily Filter," not an ADX section) that should most likely now read "Chapter 15's ADX-gated approach" instead. Left unedited since it is outside this chapter's own file.

**Updated 2026-09-22** — this chapter was renamed and renumbered from its original standalone draft slot ("Chapter 6") to Chapter 15 in this project's book, per user request ("shift right this chapters (chapter 3 should become chapter12)"), alongside three companion chapters shifting the same +9: Volume and Open Interest (3 -> 12), Moving Averages (4 -> 13), and Oscillators and Contrary Opinion (5 -> 14). All internal section, table, and listing references were renumbered from 6.x to 15.x throughout, including the numerous cross-references to the Moving Averages and Oscillators chapters (old "Chapter 4"/"Section 4.x" -> "Chapter 13"/"Section 13.x"; old "Chapter 5"/"Section 5.x" -> "Chapter 14"/"Section 14.x") scattered through this chapter's theory and code sections. This chapter now closes out Part IV — Technical Analysis (Chapters 11-15); its Prereqs were updated to "Ch 13 (Moving Averages), Ch 14 (Oscillators and Contrary Opinion)" to match. The WHAT'S NEXT box, which previously described this chapter as closing an unrelated "Part I" and handing off to a "Chapter 7 -- Intermarket Analysis" from a separate, unrelated draft-numbering scheme (this project's own Intermarket Analysis is already Chapter 5, elsewhere in the book), was rewritten to describe this chapter's actual role closing out Part IV's five-chapter technical-analysis toolkit, without naming a specific next chapter, since no Chapter 16 yet exists in this project.

**Updated 2026-09-24** — added Section 15.10 (dashboard reading and trigger table, adapted from `writing_plans/*_Trading_Guide.md`), with Figure 15.1 and Tables 15.6–15.7; the PROOF section was renumbered 15.10 → 15.11 (THIS CHAPTER COVERS, cross-references, Chapter Summary and Key Terms updated). Images live in `content_md/images/` (light-gray conversions of the BTC/USD dashboard screenshots; flagged for replacement by print-ready grayscale charts at 300 dpi). Also fixed Listing 15.4: `trend_short` used `~ema_cross_up` (true on almost every bar) instead of a real EMA cross-down.

**Updated 2026-10-03** -- Dividend Investing (formerly Chapter 6) was removed from the manuscript; Chapters 7-15 shifted down by one to 6-14. All internal section, table, listing and figure numbers and cross-chapter references in the body were decremented accordingly. Historical dated notes above are left as written.

**Updated 2026-10-06** — Renumbered from Chapter 14 to Chapter 15 after Chapter 2 (Exchange Traded Products) was split into Chapter 2 (ETFs) and Chapter 3 (ETCs and ETNs). Section, subsection, table, figure and listing numbers, the header digit box, Prereqs and cross-chapter references updated; dated notes above keep the numbering of their time.

**Updated 2026-10-06 (c)** — Part label aligned with `.claude/CLAUDE.md` §3.3: Part I — Investing and Stock Market (Ch 1–9), Part II — Technical Analysis (Ch 10–15); "opens/closes Part …" sentences adjusted.

**Updated 2026-10-06 (e)** — Cross-references updated after Futures Trading moved to Chapter 3 and ETCs/ETNs to Chapter 4 (old Ch 3–6 → 4–7).

**Updated 2026-10-07** — Renumbered (−1) after Bonds and Intermarket Analysis were merged into Chapter 6 (Bonds and the Intermarket Chain); section, table, figure and listing numbers and cross-references updated.

**Updated 2026-10-07 (c)** — Prereqs line normalised to "Chapter N (…)".
