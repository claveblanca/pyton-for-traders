|                                                             |
| ----------------------------------------------------------- |
| **PYTHON FOR TRADERS: INVESTING, DERIVATIVES, AND TECHNICAL ANALYSIS APPLIED** |

|            |        |
| ---------- | ------ |
| Appendix A | **A** |

**Money Management and Trading Psychology**

*The capital-allocation rules that cap what any single trade, market, or sector can cost, the order types that enforce them, and the cognitive and emotional biases that explain why traders break them anyway*

Appendix · Prereqs: Chapter 5 (Futures Trading)

<table>
<thead>
<tr class="header">
<th><strong>THIS APPENDIX COVERS</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>A.1 The Three Elements of Successful Trading</p>
<p>A.2 Money Management — The Four Capital-Allocation Rules</p>
<p>A.3 Reward-to-Risk and Position Sizing</p>
<p>A.4 Trading Tactics and Order Execution</p>
<p>A.5 Intraday Charts and Pivot Points</p>
<p>A.6 Application Beyond Futures — Stocks, Asset Allocation, Managed Funds</p>
<p>A.7 Traditional Finance vs. Behavioral Finance</p>
<p>A.8 The Emotions of Investing</p>
<p>A.9 Cognitive Biases — Errors in the Reasoning Process</p>
<p>A.10 Emotional Biases — Impulses That Cannot Be Eliminated, Only Managed</p>
<p>A.11 Operational Synthesis</p>
<p>A.12 [CODE] Hands-On — The First Four Checks as a Pre-Trade Gate</p>
<p>A.13 [PROOF] Auditing a Trade Plan Against the Rules and the Biases</p></td>
</tr>
</tbody>
</table>

|                                        |
| -------------------------------------- |
| **A.1 THE THREE ELEMENTS OF SUCCESSFUL TRADING** |

The classic three-part framework used here reduces a complete, profitable trading approach to three components, and treats all three as mandatory — a strategy strong on one and weak on another is an incomplete strategy, not a partially-successful one.

**A.1.1 Price forecasting.** Determining market direction — bullish or bearish — through technical or fundamental analysis, in order to decide whether to go long or short. This is the piece most beginners spend all their time on, and the piece that alone is not sufficient.

**A.1.2 Trading tactics — timing.** Pinpointing precise entry and exit levels. Timing is critical in leveraged markets specifically because even a correct directional forecast can produce a significant loss if the position is entered too early or too late relative to that forecast playing out.

**A.1.3 Money management.** Allocating capital, establishing position limits, setting risk-to-reward parameters, and managing stop-loss placement to preserve capital. This is the component the rest of this appendix is built around — the other two can be right and a trader can still be ruined by getting this one wrong.

| **◆ EDGE — Being right on direction is not the same as making money**                                                                                                                                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A correct forecast, entered at the wrong size or the wrong moment, can still lose money — and a mediocre forecast, sized and timed with discipline, can still be profitable over a long run of trades. Money management is not a safety net bolted onto the forecast; it is an equal, independent leg of the system. |

|                                                    |
| -------------------------------------------------- |
| **A.2 MONEY MANAGEMENT — THE FOUR CAPITAL-ALLOCATION RULES** |

Money management dictates how much capital is risked across trades to protect the portfolio from severe drawdowns or ruin. The rule set collapses to four numeric ceilings, each guarding against a different failure mode.

*Table A.1 — The four capital-allocation ceilings*

| **Rule**                     | **Ceiling**                          | **Guards against**                                               |
| ----------------------------- | --------------------------------------- | ---------------------------------------------------------------------- |
| Total equity rule              | 50% of total account equity invested at once | Being fully committed with no reserve for an adverse period             |
| Single-market rule              | 10–15% of total equity in margin on any one market | Concentration risk in a single instrument                               |
| Maximum-risk rule                | 2% of total equity at risk on any one trade (the book's rule); 5% as an absolute ceiling, never a target | A single bad trade doing outsized damage to the account                 |
| Sector-diversification rule      | 20–25% of total equity in any one market group/sector | A sector-wide move (e.g. all precious metals) wiping out correlated positions |

**A.2.1 Why these are ceilings, not targets.** None of the four numbers above is a recommendation to use the full allowance on every trade. They are the outer boundary past which a single position, a single market, or a single sector can do disproportionate damage to the account regardless of how good the setup looked. A trader operating well inside all four ceilings, most of the time, has room to size up on genuinely high-conviction setups without ever approaching account-ending exposure.

**A.2.2 The 2% rule sits inside the 5% ceiling.** The per-trade risk used throughout this book — in Chapter 5's futures sizing and Chapter 7's options sizing — is 2% of account equity, measured as the distance from entry to stop multiplied by position size. The 5% figure in Table A.1 is not an alternative to it: it is the hard limit no single trade may exceed even after slippage, a gap through the stop, or a deliberate high-conviction exception. Size every trade at 2% or less; treat anything between 2% and 5% as an exception that has to be justified in writing; treat anything above 5% as a rule violation. The single-market ceiling works the same way one level up: Chapter 5's 3–5% cap measures combined *open risk* in one market, while the 10–15% figure here measures the *margin* committed to it — check both.

| **⚠ WARNING — The 50% rule is not "50% per trade"**                                                                                                                                                                                                                                                           |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The 50%-total-equity rule caps *all open positions combined*, not any single one. A trader who reads it as permission to commit half the account to one trade has inverted the rule's purpose — the reserve half exists precisely so that one bad stretch in one market does not force the reserve to be used defensively rather than opportunistically. |

|                                                |
| ---------------------------------------------- |
| **A.3 REWARD-TO-RISK AND POSITION SIZING** |

**A.3.1 The 3:1 floor.** Trades should be structured with a minimum expected profit potential of at least 3 times the amount risked — risking $100 to make $300, at minimum. This ratio, not the win rate, is the load-bearing number: a system built around a 3:1 reward-to-risk floor stays profitable even with a win rate of 50% or less, because the average winner more than covers the average loser several times over.

**A.3.2 Trending units vs. trading units.** Multiple-contract or multiple-lot positions should be deliberately split into two behaviorally distinct pieces rather than managed as one block:

*Table A.2 — Splitting a multi-lot position by purpose*

| **Unit type**   | **Purpose**                                            | **Management style**                                  |
| ----------------- | ---------------------------------------------------------- | ------------------------------------------------------- |
| Trading units       | Locking in quick gains                                       | Liquidated at short-term resistance/support targets        |
| Trending units       | Capturing the major long-term move                            | Held with trailing stop-losses, given room to run           |

**A.3.3 Handling win/loss streaks.** Following losing streaks or drawdowns, position size should decrease to preserve capital — not increase in an attempt to "make it back." After winning streaks, the same risk rules apply with undiminished strictness; a streak of wins is exactly when overconfidence tends to erode discipline, and exactly when the rules matter most.

|                                                |
| ----------------------------------------------- |
| **A.4 TRADING TACTICS AND ORDER EXECUTION** |

**A.4.1 Breakout entry vs. pullback entry.** Two structurally different ways to enter the same directional idea, with a real risk/reward trade-off between them: a breakout entry buys as price breaks above major resistance (or shorts below support) — higher probability of catching real momentum, but higher risk from a false breakout. A pullback entry waits for a 38%–50% retracement back toward the broken level, trading a lower probability of the setup materializing at all for a materially better risk-to-reward entry price.

**A.4.2 Order types as enforcement mechanisms.** Each order type below exists to convert an intention into something the exchange itself executes, rather than something the trader has to remember to do manually in real time.

*Table A.3 — Order types and what each one enforces*

| **Order type**              | **Behavior**                                                                 |
| ------------------------------ | ----------------------------------------------------------------------------- |
| Market order                     | Executes immediately at the current market price                                 |
| Limit order                       | Specifies an exact entry/exit price — Buy Limit below market, Sell Limit above market |
| Stop order                        | Becomes a market order once a trigger price is hit — used for loss protection (stop-loss) or breakout initiation (buy stop / sell stop) |
| Market-if-touched (M.I.T.)         | Triggers a market order once a specified target price is touched                   |

| **◆ EDGE — Breakout and pullback entries are not mutually exclusive**                                                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A common practical pattern is a partial breakout entry sized small, with the remainder of the intended position added only on the pullback — combining early participation in the move with a better average entry price on the bulk of the position, at the cost of added order-management complexity. |

|                                            |
| -------------------------------------------- |
| **A.5 INTRADAY CHARTS AND PIVOT POINTS** |

**A.5.1 Fine-tuning a daily-chart decision on a shorter timeframe.** Shorter timeframes — 5-minute, 10-minute, or 1-hour bar charts — combined with sensitive oscillators such as a 14-bar Stochastic, allow a trader to refine the precise entry and exit levels for a decision that was actually made on the daily chart. The intraday chart is not where the directional call is made; it is where that call is executed with better precision.

**A.5.2 Floor trader pivot points.** Derived purely from the prior session's High, Low, and Close, pivot points calculate a set of intraday support (S1, S2) and resistance (R1, R2) benchmark levels for the current session — a fully mechanical, no-lookback-bias way to pre-mark likely intraday turning points before the session opens.

|                                                                   |
| ------------------------------------------------------------------ |
| **A.6 APPLICATION BEYOND FUTURES — STOCKS, ASSET ALLOCATION, MANAGED FUNDS** |

**A.6.1 Stocks.** Equity investors often trade over longer horizons than futures traders, but the principles here — risk management, trailing stops, sector diversification, and disciplined order execution — apply to any position managed on a trading horizon. A long-term holding bought on fundamentals is the exception: Chapter 2 (Section 2.6.3) deliberately drops the rigid stop-loss for that case and exits on valuation or a broken thesis instead. Decide which of the two horizons a position belongs to before choosing its exit discipline.

**A.6.2 Asset allocation.** The same risk-management logic extends from single-market position sizing to macro asset allocation across uncorrelated asset classes: stocks, bonds, commodities, cash, and foreign currencies. The sector-diversification rule from Section A.2 is the position-level version of the same discipline applied at the portfolio level.

**A.6.3 Managed accounts and commodity funds.** Mutual funds and managed commodity products — for example those tracking a commodity index like the GSCI — provide portfolio diversification because commodities frequently exhibit low or inverse correlation to equities and fixed-income assets, making them a genuine diversifier rather than simply another return stream that happens to be labeled differently.

|                                    |
| ---------------------------------- |
| **A.7 TRADITIONAL FINANCE VS. BEHAVIORAL FINANCE** |

**A.7.1 Homo Economicus.** Classical finance — utility theory, Modern Portfolio Theory — models an investor who is perfectly rational, unmoved by emotion, fully informed, and singularly focused on maximizing wealth. Every formula in this book's earlier chapters that assumes an investor acts on the numbers alone is, implicitly, built on this model.

**A.7.2 Homo Sapiens.** Behavioral finance studies the investor who actually shows up to place the trade: one bounded by cognitive shortcuts (*heuristics*) and subject to irrational emotion. The gap between the two models is not a flaw to be corrected once and forgotten — it is a permanent feature of trading that has to be managed on every decision, not just the difficult ones.

**A.7.3 Why the rules need a psychology section.** The goal is not to eliminate the gap between Homo Economicus and Homo Sapiens — it cannot be eliminated — but to know yourself well enough to catch your own systematic errors (*biases*) before they turn into a decision that permanently impairs capital. Every rule in Sections A.1–A.6 — the four capital-allocation ceilings, the 3:1 reward-to-risk floor, the trading/trending-unit split — is a mechanical countermeasure to exactly the psychology described from here on; Sections A.7–A.11 are what those rules are actually defending against.

|                                    |
| ---------------------------------- |
| **A.8 THE EMOTIONS OF INVESTING** |

Investing generates emotional states that can distort rational judgment well before a single number is miscalculated.

**A.8.1 Euphoria.** Follows a run of winning trades and induces a sense of invincibility — often mistaking simple luck in a rising market for personal skill. This is precisely the moment Section A.3.3 warns that discipline erodes fastest, because the trader who feels invincible has the least felt need to check a ceiling before exceeding it.

**A.8.2 Anguish and fear.** Produce decision paralysis: the investor can neither buy nor sell, experiencing the market as a hostile environment rather than merely an uncertain one. A position held through this state is usually being managed by inertia, not by a plan.

**A.8.3 Envy and impatience.** Push a trader to benchmark against someone else's results, or to reach for a high-risk shortcut that has no place in a sized, risk-defined system. Both emotions replace the trader's own setup criteria with someone else's outcome as the measure of success.

**A.8.4 The reliable-car principle.** A financial portfolio should be conceived as a reliable car — dependable, functional, and consistent — not as a race car built for thrills or excitement. A portfolio that is generating excitement rather than a return is itself a signal worth acting on, independent of what its chart is doing.

| **◆ EDGE — Run a portfolio like a reliable car, not a race car**                                                                                                                                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A portfolio built for thrills is a portfolio built to eventually fail. Judge a position on being functional, dependable, and consistent — never on how exciting it feels to hold. |

|                                    |
| ---------------------------------- |
| **A.9 COGNITIVE BIASES — ERRORS IN THE REASONING PROCESS** |

Cognitive biases come from flawed logical process rather than emotional impulse, which makes them the more tractable category — a written checklist is often enough to catch them.

**A.9.1 Confirmation bias.** Three related failure modes cluster under this heading. *Seeking confirmation* is the tendency to select only information that supports an existing thesis, systematically ignoring contrary data or dissenting opinions. *Aggregation* is the tendency to seek out "clubs" or communities of people who already share the same view, avoiding critical challenge rather than inviting it. *Illusion of control* is the mistaken belief that one's own research or effort can influence or control where the market goes — the investor is a passive reader of context, not a helmsman; a useful image is a ship on the ocean, which can interpret the conditions around it but cannot govern the waves.

**A.9.2 Hindsight bias.** The tendency to treat an outcome as having been inevitable after the fact, taking undue credit for wins or rationalizing away losses. The fix is low-effort and specific: keep a written trade journal recording the actual reasoning behind every entry and exit *at the time it is made*, not reconstructed afterward — it is the only reliable defense against a memory that will otherwise edit itself to make every past decision look better-founded than it was.

**A.9.3 Anchoring.** Judging a position's success against its original purchase price rather than its current intrinsic value and evolving fundamentals. A trending unit (Section A.3.2) that should be cut is routinely kept instead because "it's still above what I paid," long after the setup that justified holding it has been invalidated.

**A.9.4 Mental accounting.** Managing capital in separate mental "buckets" according to where it came from — inherited money handled conservatively, speculative winnings played aggressively — instead of treating money as fungible. This directly undermines Section A.2's total-equity rule, which only works when it is applied to the account as a whole, not to a subset the trader has mentally carved out and exempted.

**A.9.5 Laziness and source restriction.** Relying on informational shortcuts — headlines, online forums, unverified tips — instead of analyzing company filings and financial statements directly. The shortcut is faster in the moment and worse on every occasion that matters.

**A.9.6 Home-country bias.** The tendency to concentrate investments in the domestic market by default rather than by analysis. Outside the United States, no single country represents more than a small single-digit share of global equity market capitalization — a domestic-only portfolio is, by construction, ignoring most of the opportunity set without having evaluated it. This works directly against Section A.6.2's asset-allocation principle of diversifying across uncorrelated asset classes and geographies.

*Table A.4 — Cognitive biases at a glance*

| **Bias**                | **What it does**                                                                    | **Where it bites in this book's rules**                                          |
| ------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Confirmation bias           | Seeking only supporting information; clustering into like-minded communities; treating analysis as market control | Justifying a position that has already breached its Section A.4 stop instead of exiting it |
| Hindsight bias               | Treating an outcome as inevitable after the fact; rationalizing losses away              | Skipping the post-trade review that would otherwise catch a real sizing error before it repeats |
| Anchoring                     | Judging a position against its purchase price rather than current fundamentals             | Refusing to cut a trending unit "because it's still above what I paid"                   |
| Mental accounting              | Managing capital in separate buckets by source rather than as one fungible pool             | Undermines the Section A.2 total-equity rule, which requires treating the account as a whole |
| Laziness / source restriction   | Relying on headlines and tips instead of primary financial statements                       | Produces a thesis that was never actually tested against the numbers                     |
| Home-country bias               | Concentrating investments in the domestic market by default                                 | Works against the Section A.6.2 asset-allocation principle of geographic diversification  |

|                                    |
| ---------------------------------- |
| **A.10 EMOTIONAL BIASES — IMPULSES THAT CANNOT BE ELIMINATED, ONLY MANAGED** |

Emotional biases come from impulses, intuitions, and deep-seated human feeling rather than a flawed step in reasoning. Unlike cognitive biases, they cannot be reasoned away with a checklist — they can only be recognized and structurally constrained, which is what Section A.2's ceilings and Section A.3's reward-to-risk floor are actually doing underneath their mechanical framing.

**A.10.1 Loss aversion.** The psychological pain of a loss is felt far more intensely than the pleasure of an equivalent gain. Operationally, this asymmetry produces two mirror-image errors: selling winning positions too early to lock in the safety of a realized profit, and letting losing positions run in the hope of a recovery — or irrationally increasing risk in an attempt to break even. Both are the exact inverse of the trading/trending-unit split Section A.3.2 is designed to produce.

| **⚠ WARNING — Volatility is not the same thing as real risk**                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The S&P 500's 1960–2014 record shows a 6.70% compound annual return excluding dividends — and 14 negative years within that period, 10 of them with declines greater than 10%. Ordinary short-term volatility is physiological to markets, not a signal of impending catastrophe. The real risk an investor should manage against is the permanent impairment of capital, not the volatility itself — confusing the two is exactly what loss aversion does by default. |

**A.10.2 Self-attribution bias (the illusion of knowledge).** The tendency to attribute financial successes exclusively to one's own skill and insight, while attributing failures to external factors, bad luck, or market manipulation. Left unexamined, this bias blocks the honest post-trade review that Section A.13's audit depends on — a trader who never credits luck for a win has no reason to look for a real mistake behind a loss.

**A.10.3 Lack of discipline and quotation stress.** Because equity markets are highly liquid and continuously quoted in real time, they generate a form of psychological stress that an illiquid asset like real estate simply does not produce — there is no minute-by-minute price to react to. The fix is conceptual: deliberately decouple the fluctuating quoted price from the position's underlying fundamental value, so that a price tick is not mistaken for new information about the business itself.

**A.10.4 Status-quo bias.** Decision-making inertia that keeps outdated or inefficient holdings in a portfolio — government bonds paying a negative real yield, or leftover positions from a long-failed speculative bet, kept simply because selling them would require an active decision. The zero-based test provides a low-effort diagnostic: ask "if I held the cash equivalent of this position today instead of the position itself, would I buy it right now?" A "no" answer means the position should be liquidated, independent of how it was acquired or how long it has been held.

**A.10.5 Regret aversion and herd behavior.** Fear of making an autonomous decision that turns out to be wrong drives a trader to "follow the herd" instead — the late-1990s dot-com bubble is the standard example — so that any eventual failure is shared with the crowd rather than owned alone. Chasing a breakout entry (Section A.4.1) purely because "everyone is in it," with no independent read on the setup, is this bias operating on this book's own tactics.

**A.10.6 Endowment bias.** Attributing sentimental or emotional value to a long-held or inherited position — shares in a family company are the classic case — and judging it by non-financial criteria as a result. A trending unit held on habit or attachment long after its trailing stop should have closed it is this bias at work inside Section A.3.2's own framework.

*Table A.5 — Emotional biases at a glance*

| **Bias**                | **What it does**                                                                    | **Where it bites in this book's rules**                                          |
| ------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Loss aversion                | A loss hurts more than an equal gain feels good                                            | Cutting winning trending units early while letting losers run — the inverse of Section A.3.2's intended split |
| Self-attribution bias          | Crediting wins to skill, blaming losses on luck or manipulation                              | Blocks the honest post-trade review Section A.13's audit depends on                       |
| Lack of discipline / quotation stress | Continuous real-time pricing generates reactive stress absent from illiquid assets            | Reacting to a price tick as if it were new fundamental information                        |
| Status-quo bias                 | Inertia that keeps a stale or inefficient position in the portfolio                            | A trending unit held on habit long after its trailing stop should have closed it            |
| Regret aversion / herd behavior  | Fear of an autonomous wrong decision drives following the crowd instead                        | Chasing a Section A.4.1 breakout entry purely because "everyone is in it"                   |
| Endowment bias                   | Sentimental attachment to a long-held or inherited position, judged by non-financial criteria   | Holding a trending unit past its trailing stop out of attachment rather than analysis        |

|                                    |
| ---------------------------------- |
| **A.11 OPERATIONAL SYNTHESIS** |

**A.11.1 Biases compound under stress.** Cognitive and emotional biases frequently overlap and reinforce each other, and they compound fastest during exactly the two conditions Section A.3.3 already flags — losing streaks and winning streaks. A trader rarely encounters just one bias in isolation on a difficult trade; the anchoring, the loss aversion, and the herd instinct tend to arrive together.

**A.11.2 The defenses are the same three, every time.** Discipline, rigorous diversification, and fundamental analysis grounded in a margin of safety are the primary parachutes against these mental traps. None of the three is a one-time fix — each has to be re-applied on every trade, precisely because the biases they defend against do not go away once recognized.

|                                                                       |
| ------------------------------------------------------------------------ |
| **A.12 [CODE] HANDS-ON — THE FIRST FOUR CHECKS AS A PRE-TRADE GATE** |

The first four PROOF checks are arithmetic on the open book plus the trade about to be placed, so they can run before every order without any judgment call. Listing A.1 runs them in one call and returns the verdict Section A.2.2 prescribes: OK, an exception to justify in writing when trade risk sits between 2% and 5%, or not allowed above 5%. The last four checks test the decision, not the numbers; they stay a written exercise, and the trade journal of Section A.9.2 is the record they are run against.

**A.12.1 The capital ceilings, the 2% rule and the 3:1 floor (Sections A.2, A.2.2, A.3.1).** Each position carries its market, sector, committed margin, entry, stop, target, size and point value. Risk per position is the distance from entry to stop times size times point value — the definition used throughout Chapter 5.

**💻 PYTHON · Listing A.1 — `pre_trade_check`: the Appendix A ceilings applied to the book plus one new trade**

```python
import pandas as pd

LIM = {"total": 0.50, "market_margin": 0.15, "market_risk": 0.05,
       "sector": 0.25, "trade_2pct": 0.02, "trade_max": 0.05, "rr_min": 3.0}

def pre_trade_check(book: pd.DataFrame, new: dict, equity: float) -> dict:
    """book: open positions; new: the trade to add. PROOF checks 1-4."""
    p = pd.concat([book, pd.DataFrame([new])], ignore_index=True)
    p["risk"] = (p.entry - p.stop).abs() * p["size"] * p.point_value
    n, mkt = p.iloc[-1], p[p.market == new["market"]]
    rr = abs(n.target - n.entry) / abs(n.entry - n.stop)
    c = {"total":         p.margin.sum() / equity,                 # A.2
         "market_margin": mkt.margin.sum() / equity,               # A.2
         "market_risk":   mkt.risk.sum() / equity,                 # 5.5.3
         "sector":        p[p.sector == new["sector"]].margin.sum() / equity,
         "trade_2pct":    n.risk / equity}                         # A.2.2
    ok = {k: v <= LIM[k] for k, v in c.items()} | {"rr_min": rr >= LIM["rr_min"]}
    if n.risk / equity > LIM["trade_max"]: verdict = "NOT ALLOWED (> 5%)"
    elif not ok["trade_2pct"]:             verdict = "EXCEPTION: justify in writing"
    else: verdict = "OK" if all(ok.values()) else "RESIZE / SKIP"
    return {"ratios": c, "rr": rr, "verdict": verdict}
```

Full version, with self-test: `code_snippets/v1/appendix_a/appx_a_portfolio_limits.py` (adds the maximum size at 2% and an eight-line verdict table).

**A.12.2 Reading the output.** On a $25,000 account holding one Micro Gold and one silver contract, a second Micro Gold with a 100-point stop and a 300-point target returns total commitment 21.2%, gold margin 13.2%, gold open risk 4.8%, metals sector 21.2%, trade risk 4.0% and a reward-to-risk of exactly 3:1 — every ceiling passes except the 2% working rule, so the verdict is *EXCEPTION: justify in writing*. A Micro Crude trade with a 2-point stop on the same book returns *OK*. The PROOF that follows adds the four checks no function can run.

|                                    |
| ---------------------------------- |
| **A.13 [PROOF] AUDITING A TRADE PLAN AGAINST THE RULES AND THE BIASES** |

<table>
<thead>
<tr class="header">
<th><strong>▶ PROOF — Eight checks to run before any trade is placed</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>Total-equity check: sum the margin or capital committed across every open position, including the one about to be placed. If it exceeds 50% of account equity, the trade does not go on as sized — reduce it or skip it (Section A.2).</p>
<p>Single-market check: sum the margin committed to this market across all open positions, including the new trade. If it exceeds 10–15% of account equity, or the combined open risk in this market exceeds Chapter 5's 3–5% cap, the position is oversized for this market.</p>
<p>Maximum-risk check: compute the dollar distance from planned entry to planned stop, multiplied by position size. Above 2% of account equity, cut the size or tighten the stop; above 5%, the trade is not allowed at all (Section A.2.2).</p>
<p>Reward-to-risk check: divide the dollar distance from entry to target by the maximum-risk number above. Below 3:1, the trade fails Section A.3's floor regardless of how confident the forecast is.</p>
<p>Confirmation check: state the strongest argument against this trade as clearly as the argument for it. If you cannot, the thesis has only collected support, not been tested (Section A.9.1).</p>
<p>Anchor check: if you did not already own this position, at today's price and today's fundamentals, would you buy it now? A "no" is the zero-based test of Section A.10.4, and it applies to a losing position exactly as much as a winning one.</p>
<p>Attribution check: write one honest sentence on what role luck played in your three most recent wins, and one on what specific, correctable error — not "bad luck" — produced your most recent loss (Section A.10.2).</p>
<p>Herd check: state the setup criteria without referencing what anyone else is doing, buying, or saying. If the criteria only make sense by reference to the crowd, this is regret aversion or herd behavior wearing the costume of a setup (Section A.10.5).</p>
<p>The first four checks size the trade; the last four test whether the decision behind it is yours. A trade that fails any one of the eight is not ready — adjust size, stop, target, or the thesis itself before entry, not after.</p></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td><p><strong>◈ KEY INSIGHT<br />
</strong></p>
<p><em>"A correct forecast with the wrong position size is not a smaller version of a good trade — it is a different, worse trade. The rules decide how much a mistake can cost; knowing your own biases decides how often you will try to break them."</em></p></td>
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
<td><p>Successful trading requires three independent components — price forecasting, trading tactics (timing), and money management — and being strong in one does not compensate for being weak in another.</p>
<p>Four capital-allocation ceilings guard against different failure modes: 50% of equity invested in total, 10–15% in margin on any one market, 20–25% in any one sector, and a maximum risk per trade of 2% as the working rule with 5% as the absolute ceiling — all ceilings, not targets.</p>
<p>A minimum 3:1 reward-to-risk ratio keeps a system profitable even at a 50% or lower win rate; splitting a multi-lot position into trading units and trending units captures both quick gains and the major move from the same entry.</p>
<p>Position size should shrink after losing streaks and stay disciplined — not loosen — after winning streaks; market, limit, stop, and market-if-touched orders turn those intentions into something the exchange enforces.</p>
<p>The same principles scale from a single futures position to stocks, asset allocation, and managed funds — except that a long-term fundamental holding exits on valuation or a broken thesis rather than on a rigid stop (Chapter 2).</p>
<p>Behavioral finance explains why the rules get broken: classical finance assumes a rational Homo Economicus, while the trader who actually places the order is bounded by heuristics and emotion — a gap that can be managed but not closed.</p>
<p>Cognitive biases (confirmation, hindsight, anchoring, mental accounting, source laziness, home-country bias) are errors of reasoning that a checklist and a trade journal catch; emotional biases (loss aversion, self-attribution, quotation stress, status-quo, regret aversion and herding, endowment) can only be constrained structurally by the rules above.</p>
<p>Loss aversion inverts the trading/trending-unit split — cutting winners early while letting losers run — and biases compound fastest during losing and winning streaks alike; discipline, diversification, and margin-of-safety analysis are the standing defense, re-applied on every trade.</p></td>
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
<td><p><strong>Total equity rule</strong> No more than 50% of account equity committed across all open positions at once.</p>
<p><strong>Single-market rule</strong> No more than 10–15% of account equity in margin on any one market.</p>
<p><strong>Maximum-risk rule</strong> Risk no more than 2% of account equity on a single trade; 5% is the absolute ceiling.</p>
<p><strong>Sector-diversification rule</strong> No more than 20–25% of account equity committed to any one market group or sector.</p>
<p><strong>Reward-to-risk ratio</strong> Expected profit potential divided by amount risked; the floor used here is 3:1.</p>
<p><strong>Trading unit / trending unit</strong> Sub-positions of one entry: the first liquidated at short-term targets, the second held with a trailing stop for the major move.</p>
<p><strong>Breakout / pullback entry</strong> Entering as price breaks a major level, or on a 38%–50% retracement back toward it for a better risk/reward.</p>
<p><strong>Market-if-touched (M.I.T.)</strong> An order that triggers a market order once a specified price is touched.</p>
<p><strong>Floor trader pivot points</strong> Intraday support/resistance levels (S1, S2, R1, R2) derived from the prior session's High, Low, and Close.</p>
<p><strong>Homo Economicus</strong> The fully rational, fully informed investor model classical finance assumes and real trading behavior does not match.</p>
<p><strong>Confirmation bias</strong> Seeking only information that supports an existing thesis while discounting contrary evidence.</p>
<p><strong>Illusion of control</strong> The mistaken belief that research or effort can influence where the market goes, rather than only interpreting it.</p>
<p><strong>Anchoring</strong> Judging a position by its original purchase price rather than its current fundamental value.</p>
<p><strong>Mental accounting</strong> Treating capital differently based on its source rather than as one fungible pool.</p>
<p><strong>Home-country bias</strong> Concentrating investments in the domestic market by default rather than by analysis.</p>
<p><strong>Loss aversion</strong> Feeling a loss more intensely than an equal-sized gain, leading to cutting winners early and letting losers run.</p>
<p><strong>Self-attribution bias</strong> Crediting wins entirely to personal skill; blaming losses on bad luck or external manipulation.</p>
<p><strong>Status-quo / endowment bias</strong> Inertia or sentimental attachment that keeps an outdated position in the portfolio past the point analysis would support.</p>
<p><strong>Regret aversion / herd behavior</strong> Fear of an autonomous wrong decision, which drives following the crowd so that failure is shared.</p>
<p><strong>Zero-based test</strong> Asking whether you would buy a position today, at today's price, if you did not already own it.</p></td>
</tr>
</tbody>
</table>

| **WHERE THIS FITS** |
| --- |
| This appendix is a standing reference, not a chapter to read once. The capital-allocation ceilings and the 2% per-trade rule apply to every position the book's instrument chapters (Chapters 2–7) and technical-analysis chapters (Chapters 8–12) produce, and the bias checks in Section A.13 belong in front of every entry. Read it after Chapter 5 for the sizing rules, and return to it whenever a trade feels too obvious to check. |

---

**Created 2026-10-08** — Merged from Chapter 8 (Money Management and Trading Tactics, v3) and Chapter 9 (Behavioral Finance, v1) into Appendix A, placed after Chapter 12. Ch 8 §8.1–8.6 → A.1–A.6; Ch 9 §9.1–9.5 → A.7–A.11; Ch 8 §8.7 (condensed duplicate of Ch 9) dropped; Ch 8 §8.8 and Ch 9 §9.6 PROOFs merged into A.12 (eight checks). Ch 9 FRAMING box and Ch 9 KEY INSIGHT (Brutus quote) dropped. Risk rule reconciled: 2% per trade as the book rule, 5% as the absolute ceiling (new A.2.2, Table A.1, PROOF, Key Terms). A.6.1 qualified against Chapter 2 §2.6.3 (no rigid stop for long-term fundamental holdings). Tables A.1–A.3 from Ch 8, A.4–A.5 from Ch 9 Tables 9.1–9.2.
