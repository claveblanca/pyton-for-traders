|                                                               |
| ------------------------------------------------------------- |
| **PYTHON FOR TRADERS: INVESTING, DERIVATIVES, AND TECHNICAL ANALYSIS APPLIED** |

|                    |        |
| ------------------ | ------ |
| Chapter 7          | **7** |

**Options Trading: Leverage, Levels, and the Greeks That Actually Matter**

*A practitioner's framework for trading options*

Part I — Investing and Stock Market · Prereqs: Chapter 5 (Futures Trading), Chapter 2 (Investing in Stocks) · Companion files: `Options_Trading_Rules.md`, `code_snippets/options_trading/options_rules_screener.py`

<table>
<thead>
<tr class="header">
<th><strong>THIS CHAPTER COVERS</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>7.1 Options Mechanics — Calls, Puts, and the 100-Share Multiplier</p>
<p>7.2 Strike and Expiration — Fixed at Entry, Driving Value Every Day After</p>
<p>7.3 Broker Access Levels — Matching Strategy to Permission</p>
<p>7.4 Multi-Leg Strategies — Capping Risk or Trading Volatility Itself</p>
<p>7.5 The Greeks — Delta, Theta, Gamma</p>
<p>7.6 The 2% Rule Applied to Options Sizing</p>
<p>7.7 Matching Platform to Strategy</p>
<p>7.8 [CODE] Hands-On — Automating the Screen in Python</p>
<p>7.9 [PROOF] Running the Full Screen — a worked scorecard and a Black-Scholes cross-check</p></td>
</tr>
</tbody>
</table>

|                                    |
| ---------------------------------- |
| **7.1 OPTIONS MECHANICS — CALLS, PUTS, AND THE 100-SHARE MULTIPLIER** |

An option contract gives its buyer the right, but not the obligation, to buy or sell 100 shares of the underlying stock at a fixed price before a fixed date. Put directly: options let a trader control 100 shares of stock per contract for a fraction of the capital required to own the shares outright — a structurally higher potential ROI than buying the stock directly, purchased at the cost of expiration, time decay, and, at higher trading levels, undefined risk.

**7.1.1 The multiplier is the whole point, and the whole risk.** A single contract representing 100 shares means a modest-looking premium controls a much larger notional exposure. This is exactly the same leverage dynamic covered for futures in this project's Chapter 5 (Futures Trading), arrived at through a different mechanism: instead of margin against a large contract, it is a small premium against a large share-equivalent position.

**7.1.2 Calls and puts are opposite bets, and mixing them up is the single most common beginner error.** A **call** profits when the underlying price rises above the strike (plus premium paid); a **put** profits when it falls below the strike (minus premium paid). Confirming which side of the bet a given trade actually represents — before entry, not after watching it move the "wrong" way — is a foundational rule, and it earns first billing because the failure mode it prevents is so basic and so common.

| **◆ EDGE — Buying an option is a bet on direction AND magnitude AND timing, simultaneously**                                                                                                                                                                                                                          |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A stock trader who is right on direction makes money. An option buyer who is right on direction but wrong on timing or magnitude can still lose the entire premium — the underlying has to move far enough, fast enough, before expiration, to overcome the price already paid for the option. This is why "I was right about the stock" and "the option trade worked" are two different claims. |

|                                    |
| ---------------------------------- |
| **7.2 STRIKE AND EXPIRATION — FIXED AT ENTRY, DRIVING VALUE EVERY DAY AFTER** |

Both the strike price and the expiration date are locked in the moment a trade opens, and both drive the option's value for the rest of its life. The strike determines intrinsic value — how much the option would be worth if exercised right now. The expiration date drives time decay, discussed in full under Theta in Section 7.5, but the mechanical point belongs here: every day that passes without a favorable move is a day of value quietly leaking out of a long option position, independent of what the underlying stock does.

**7.2.1 Why this makes options fundamentally different from owning the stock.** A stock position has no clock running against it — a shareholder can simply wait out an unfavorable move. A long option position cannot wait indefinitely; it has a fixed, shrinking runway. This single structural difference is the reason the rest of this chapter (broker levels, the Greeks, position sizing) exists as a distinct discipline rather than being "stock trading with extra steps."

|                                    |
| ---------------------------------- |
| **7.3 BROKER ACCESS LEVELS — MATCHING STRATEGY TO PERMISSION** |

Brokers assign every options account a trading level, typically 1 through 4, that gates which strategies are permitted. The levels exist because risk profile — not sophistication or interest — is what the broker is actually screening for.

*Table 7.1 — Broker option levels and risk profile*

| **Level** | **Strategy examples**                  | **Risk profile**                                                        |
| ----------- | ----------------------------------------- | ---------------------------------------------------------------------------- |
| 1           | Covered calls, cash-secured puts          | Defined risk — requires owning or collateralizing the underlying              |
| 2           | Long calls, long puts                     | Defined risk — max loss is the premium paid                                   |
| 3           | Vertical spreads, straddles, iron condors | Defined risk both ways when bought/structured as a net-debit or defined-width position |
| 4           | Naked calls, naked puts                   | **Undefined / unlimited risk** — highest level, discouraged for beginners      |

**7.3.1 The level system is a risk filter, not a skill badge.** It is tempting to read "Level 4" as "advanced trader" and treat unlocking it as a goal. The reality is closer to the opposite: naked options carry genuinely unlimited loss potential (a naked call has no ceiling on how high a stock can rise against it), and the level gate exists specifically to keep undercapitalized or inexperienced accounts away from that exposure by default, not to reward ambition.

**7.3.2 Trade only what your level — and your risk tolerance — actually supports.** A strategy being *approved* at your account level is necessary, not sufficient. Rule 4 is explicit that both the broker's permission and the trader's own risk tolerance have to clear the bar before a strategy is used, and the two checks are not the same thing.

|                                    |
| ---------------------------------- |
| **7.4 MULTI-LEG STRATEGIES — CAPPING RISK OR TRADING VOLATILITY ITSELF** |

A single long call or put is a pure directional bet with one moving part. Multi-leg strategies — spreads, straddles, iron condors — combine two or more options specifically to define maximum loss up front, or to take a position on volatility itself rather than pure direction.

**7.4.1 Vertical spreads define both sides of the outcome.** Buying one option and selling another at a different strike (same expiration) caps both the maximum profit and the maximum loss at entry — the trader knows the worst case and the best case before placing the trade, at the cost of giving up some of the unlimited upside a naked long option would theoretically offer.

**7.4.2 Straddles and iron condors are bets on movement, not direction.** A long straddle (buying a call and a put at the same strike) profits if the underlying moves sharply in *either* direction — it is a bet that volatility will exceed what the market has priced in, with no view on which way the move goes. An iron condor is close to the opposite: a defined-risk bet that the underlying stays *within* a range through expiration. Both structures illustrate a point worth internalizing early — options let a trader take a position on how much a stock moves, independent of a directional opinion, which single-leg calls and puts cannot do.

*Table 7.2 — Defined risk by strategy*

| **Strategy**        | **Defined risk?**                                                        |
| ---------------------- | ----------------------------------------------------------------------------- |
| Covered call            | Yes                                                                            |
| Cash-secured put        | Yes                                                                            |
| Long call / long put    | Yes — capped at premium paid                                                   |
| Vertical spread         | Yes                                                                            |
| Straddle                | Yes when bought (long straddle); a sold/naked straddle is not                 |
| Iron condor             | Yes                                                                            |
| Naked call / naked put  | **No** — undefined/unlimited risk                                             |

|                                    |
| ---------------------------------- |
| **7.5 THE GREEKS — DELTA, THETA, GAMMA** |

The Greeks translate an option's price behavior into numbers a trader can actually act on before entry, rather than discovering the exposure after the fact.

**7.5.1 Delta — directional exposure.** Delta measures how much an option's price moves per $1 move in the underlying. It doubles as a rough proxy for the probability of finishing in the money: a 0.30 delta call is often read informally as "roughly a 30% chance of expiring in the money," though this is an approximation, not an exact probability.

**7.5.2 Theta — time decay.** Every option loses value as expiration approaches, and that decay is not linear — it accelerates sharply in the final weeks before expiration, commonly flagged inside the last ~21 days. A long option position held into this window is fighting an increasingly strong headwind even if the underlying is stationary.

**7.5.3 Gamma — how fast Delta itself changes.** Gamma is highest for at-the-money options near expiration, which means a position's directional exposure (its Delta) can shift quickly with little warning exactly when Theta decay is also at its most aggressive. The two effects compound at the same point in an option's life, which is precisely why short-dated, at-the-money positions demand the closest monitoring.

| **◆ EDGE — The Greeks describe risk that already exists — they don't remove it**                                                                                                                                                                                                                                     |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Checking Delta, Theta, and Gamma before a trade doesn't change the trade's actual risk — it changes whether the trader knows about that risk in advance. A position with high Gamma and heavy Theta decay is exactly as risky whether or not anyone looked at the numbers; the value of the Greeks is entirely in surfacing exposure before it becomes a surprise. |

|                                    |
| ---------------------------------- |
| **7.6 THE 2% RULE APPLIED TO OPTIONS SIZING** |

The book's overarching 2% rule — never risk more than 2% of total capital on a single trade — applies to options exactly as it does to the futures positions in Chapter 5, adjusted for how "risk" is measured. For an options trade, the relevant number is the worst-case dollar loss per contract: the full premium paid for a long call or put, or the spread width minus credit received for a defined-risk spread.

**7.6.1 Why defined-risk strategies make this rule easy to apply, and undefined risk breaks it.** Sizing a position under the 2% rule requires knowing the maximum possible loss per contract in advance. Every strategy in Table 7.2 marked "Yes" has that number available before entry. Naked calls and puts do not — there is no fixed worst case to divide the account's 2% risk budget by, which is a second, independent reason (beyond the broker-level gate) that the book treats undefined-risk strategies as something to avoid rather than merely something to size carefully.

|                                    |
| ---------------------------------- |
| **7.7 MATCHING PLATFORM TO STRATEGY** |

A beginner-friendly platform is entirely sufficient for Level 1–2 strategies — covered calls, cash-secured puts, long calls and puts. Trading spreads, straddles, or anything requiring live Greeks and full option-chain visibility calls for a platform actually built for that; tastyworks and MT4 are examples aimed at more advanced traders. The practical implication: outgrowing a strategy level often means outgrowing the platform at the same time, not just requesting a permission upgrade from the same broker.

|                                    |
| ---------------------------------- |
| **7.8 [CODE] HANDS-ON — AUTOMATING THE SCREEN IN PYTHON** |

Every rule above that reduces to a lookup or a number has already been encoded in `code_snippets/options_trading/options_rules_screener.py`, built against the Tradier Brokerage API (free with a Tradier account; a free sandbox environment covers testing with delayed data and no live orders) — plus a from-scratch Black-Scholes Greeks calculator that needs no API key or account at all.

*Table 7.3 — Rule-to-function map*

| **Rule(s)**       | **Function**                                                                                          | **What it checks**                                                              |
| -------------------- | ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| 4–8                  | `broker_level_required(strategy)` / `account_level_allows(strategy, account_level)`                        | Minimum broker level a strategy needs; whether the account's level clears it            |
| 9                    | `broker_level_required(strategy)["is_defined_risk"]`                                                       | Whether the strategy has a defined (capped) max loss                                    |
| 10, 11, 12           | `greeks_exposure_screen(chain_df, days_to_expiration)`                                                     | Pulls Delta/Theta/Gamma from a live Tradier chain; flags the Theta decay zone and high-Gamma contracts |
| 10, 11, 12 (offline) | `black_scholes_greeks(spot, strike, days_to_expiration, risk_free_rate, iv, option_type)`                  | From-scratch Delta/Theta/Gamma — no API key or account needed                           |
| 13                   | `position_size_by_risk(account_equity, max_loss_per_contract)`                                             | Max contracts allowed within the 2% risk rule                                           |
| all of the above     | `screen_option_trade(strategy, account_level, account_equity, max_loss_per_contract, days_to_expiration)`  | Master scorecard — one pass/fail dict per proposed trade                                |

Rules 1–3 and 14 are mechanics/product-selection rules, intentionally left as reading rather than code — there is no meaningful "screen" for confirming a call is a call.

**7.8.1 Running the master scorecard.**

<table>
<thead>
<tr class="header">
<th><strong>💻 PYTHON · Listing 7.1 — Screening a proposed options trade end to end</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>from code_snippets.options_trading.options_rules_screener import (</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;screen_option_trade, black_scholes_greeks,</p>
<p>)</p>
<p></p>
<p>trade_check = screen_option_trade(</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;strategy="vertical_spread",</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;account_level=2,</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;account_equity=20_000,</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;max_loss_per_contract=350,   # e.g. $3.50 spread width x 100</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;days_to_expiration=18,</p>
<p>)</p>
<p>print("Trade scorecard:", trade_check)</p>
<p></p>
<p># From-scratch Greeks check -- no API key needed:</p>
<p>greeks = black_scholes_greeks(</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;spot=225, strike=230, days_to_expiration=18,</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;risk_free_rate=0.045, iv=0.28, option_type="call",</p>
<p>)</p>
<p>print("Black-Scholes Greeks:", greeks)</p>
<p></p>
<p># Live chain (requires a free Tradier sandbox token):</p>
<p># from code_snippets.options_trading.options_rules_screener import (</p>
<p>#     fetch_option_chain, greeks_exposure_screen,</p>
<p># )</p>
<p># chain = fetch_option_chain("AAPL", "2026-09-18", API_KEY, sandbox=True)</p>
<p># print(greeks_exposure_screen(chain, days_to_expiration=18).head())</p></td>
</tr>
</tbody>
</table>

**7.8.2 Reading the output.** `screen_option_trade()` returns keys like `rule4_8_level_ok`, `rule9_defined_risk`, `rule11_in_theta_decay_zone`, and `rule13_max_contracts_allowed` — a candidate trade can fail on account permissions alone even when the sizing math and defined-risk check both pass, which is exactly what Section 7.9 walks through next.

|                                    |
| ---------------------------------- |
| **7.9 [PROOF] RUNNING THE FULL SCREEN** |

Consider a $20,000 account proposing a vertical spread with $350 max loss per contract (a $3.50-wide spread) and 18 days to expiration, held at broker Level 2.

Running `screen_option_trade()` on this exact proposal returns `rule4_8_level_ok: False` alongside `rule4_8_min_level_required: 3` — the account's Level 2 permission does not clear the Level 3 requirement Table 7.1 sets for vertical spreads, regardless of how well-sized or well-timed the trade otherwise is. In parallel, the sizing math still runs: at 2% risk on $20,000 ($400 max risk) against a $350 per-contract loss, `rule13_max_contracts_allowed` returns 1 contract, using $350 of the $400 budget. And because 18 days sits inside the 21-day Theta decay zone, `rule11_in_theta_decay_zone` returns `True`.

The scorecard result is a trade that is correctly *sized* (1 contract, within the 2% budget) and correctly *defined-risk* (`rule9_defined_risk: True`), but not currently *permitted* — a distinct and earlier failure than either of the other two checks. This is the practical value of running the full screen rather than checking rules individually: a trade can clear every numerical hurdle and still be one account-permission upgrade away from being tradeable at all.

<table>
<thead>
<tr class="header">
<th><strong>▶ PROOF — Three checks, one trade, an earlier failure than expected</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>Size: at 2% of $20,000 ($400) against $350 maximum loss per contract, the screen allows 1 contract — pass.</p>
<p>Defined risk: a vertical spread caps the loss at the spread width — pass.</p>
<p>Permission: vertical spreads need broker Level 3; the account holds Level 2 — fail.</p>
<p>Result: the trade is not tradeable as proposed, however well it is sized. Checking only the numbers would have missed the one failure that blocks it.</p></td>
</tr>
</tbody>
</table>

**7.9.1 Cross-checking with the from-scratch Greeks.** `black_scholes_greeks(spot=225, strike=230, days_to_expiration=18, risk_free_rate=0.045, iv=0.28, option_type="call")` returns Delta, Gamma, and per-day Theta computed independently of any broker feed. Running this alongside a live Tradier chain for the same contract is a useful sanity check before trusting a broker-reported Greek at face value — a large mismatch between the two usually means either a stale quote or a difference in the volatility input, not that one of the two calculations is simply wrong.

▶ See `code_snippets/options_trading/options_rules_screener.py` for the full runnable implementation referenced throughout this chapter.

<table>
<tbody>
<tr class="odd">
<td><p><strong>◈ KEY INSIGHT<br />
</strong></p>
<p><em>"An options trade can be sized correctly and capped correctly and still not be permitted. Run the whole screen, permission included, before the trade: the first check that fails ends it."</em></p></td>
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
<td><p>An option contract controls 100 shares of leverage per contract -- calls profit on a rise, puts on a fall, and confirming which side of that bet a trade represents is the single most common beginner check to skip.</p>
<p>Strike and expiration are fixed at entry and drive value every day after -- expiration in particular means a long option position, unlike a stock, is racing a clock it cannot pause.</p>
<p>Broker levels (1-4) gate strategies by risk profile, not by trader sophistication -- Level 4 (naked options) carries undefined/unlimited risk and is a risk-tolerance question, not an achievement to unlock.</p>
<p>Multi-leg strategies (spreads, straddles, iron condors) let a trader cap risk or bet on volatility itself, independent of direction -- a capability single-leg calls and puts don't have.</p>
<p>Delta = directional exposure, Theta = time decay (accelerating inside ~21 days to expiration), Gamma = how fast Delta itself changes (highest at-the-money, near expiration) -- the Greeks surface risk that already exists, they don't reduce it.</p>
<p>The 2% rule applies to options via the worst-case dollar loss per contract -- easy to apply for defined-risk strategies, and inapplicable by construction to naked/undefined-risk ones.</p>
<p>`screen_option_trade()` can fail a trade on broker permission alone even when sizing and defined-risk checks both pass -- run the full scorecard, not just the numeric checks in isolation.</p></td>
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
<td><p><strong>Call</strong> An option that profits when the underlying's price rises above the strike.</p>
<p><strong>Put</strong> An option that profits when the underlying's price falls below the strike.</p>
<p><strong>Strike price</strong> The fixed price at which the option can be exercised; set at entry.</p>
<p><strong>Expiration</strong> The fixed date after which the option ceases to exist; set at entry.</p>
<p><strong>Broker option level</strong> A 1-4 permission tier gating which strategies an account may trade.</p>
<p><strong>Defined risk</strong> A strategy whose maximum possible loss is known and capped before entry.</p>
<p><strong>Naked option</strong> A short call or put with no offsetting position -- undefined/unlimited risk.</p>
<p><strong>Vertical spread</strong> Buying and selling options at different strikes, same expiration, to cap profit and loss.</p>
<p><strong>Straddle</strong> A call and put at the same strike/expiration -- profits from a large move in either direction.</p>
<p><strong>Iron condor</strong> A defined-risk, range-bound strategy profiting if the underlying stays within a band through expiration.</p>
<p><strong>Delta</strong> Price sensitivity to a $1 move in the underlying; a rough proxy for probability of finishing ITM.</p>
<p><strong>Theta</strong> Time decay -- value an option loses per day, accelerating inside roughly the last 21 days.</p>
<p><strong>Gamma</strong> The rate of change of Delta itself; highest for at-the-money options near expiration.</p>
<p><strong>Intrinsic value</strong> The value an option would have if exercised immediately, driven by the strike vs. current price.</p></td>
</tr>
</tbody>
</table>

| **WHAT'S NEXT**                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| This chapter closes Part I — Investing and Stock Market. Part II opens with Chapter 8 (Technical Analysis Foundations) and moves from choosing instruments to timing them. The sizing rules used here and in Chapter 5 — the 2% rule, defined risk, reward-to-risk — are collected in Appendix A (Money Management and Trading Psychology), together with the capital-allocation ceilings that apply to every instrument in the book and the bias checks to run before any entry. `Options_Trading_Rules.md` holds the condensed rule list and quick-reference checklist this chapter expands on; `code_snippets/options_trading/options_rules_screener.py` holds the runnable code referenced in Section 7.8. |

---

**Updated 2026-09-13** to match `.claude/CLAUDE.md` §3.3's continuous manuscript numbering: this chapter was Chapter 11, in Part II -- Investing and Stock Market. All internal section/table/listing references (previously O.x) were renumbered to this project's continuous sequence, and the header digit box changed from "O" to a number -- the chapter keeps its "Reference Chapter" / standalone framing (Prereqs: None, "WHERE THIS FITS" instead of "WHAT'S NEXT") per the same decision applied to the Dividend Investing and Futures Trading chapters. Two cross-references to "Chapter F" (Sections 8.1.1 and 8.6, pointing to the Futures Trading chapter) were updated to point at that chapter's number.

**Updated 2026-09-22** -- this chapter previously shifted from Chapter 10 to Chapter 11 (a project-wide +1 renumbering across the five chapters then numbered 7-11, to open up Chapter 7 for a new "Investing in Bonds" reference chapter), and now shifts again from Chapter 11 to Chapter 8 (all internal section, table, and listing numbers decremented by three accordingly) as part of a further project-wide left-shift across the six chapters then numbered 7-12, to close the gap opened when Chapters 1-3 (Investment Classes and Instruments, Exchange Traded Products, and Investing in Stocks) were added ahead of this reference set. The two cross-references to the Futures Trading chapter (Sections 8.1.1 and 8.6) were updated from "Chapter 10" to "Chapter 7" to match that chapter's own shift. Historical dated notes above have had their internal chapter/section numbers updated for consistency with the current numbering; where a note describes an intermediate historical state, it now reflects the final current number rather than the intermediate one.

**Updated 2026-10-03** -- Dividend Investing (formerly Chapter 6) was removed from the manuscript; Chapters 7-15 shifted down by one to 6-14. All internal section, table, listing and figure numbers and cross-chapter references in the body were decremented accordingly. Historical dated notes above are left as written.

**Updated 2026-10-06** — Renumbered from Chapter 7 to Chapter 8 after Chapter 2 (Exchange Traded Products) was split into Chapter 2 (ETFs) and Chapter 3 (ETCs and ETNs). Section, subsection, table, figure and listing numbers, the header digit box, Prereqs and cross-chapter references updated; dated notes above keep the numbering of their time.

**Updated 2026-10-06 (b)** — Converted from a standalone reference chapter to a normal main-sequence chapter: standard running banner and "Chapter 8" digit box (the box still showed the pre-split number), Part I label and real Prereqs line, closing WHERE THIS FITS box replaced by WHAT'S NEXT pointing to the next chapter. Generator updated to match.

**Updated 2026-10-06 (c)** — Part label aligned with `.claude/CLAUDE.md` §3.3: Part I — Investing and Stock Market (Ch 1–9), Part II — Technical Analysis (Ch 10–15); "opens/closes Part …" sentences adjusted.

**Updated 2026-10-06 (e)** — Cross-references updated after Futures Trading moved to Chapter 3 and ETCs/ETNs to Chapter 4 (old Ch 3–6 → 4–7).

**Updated 2026-10-07** — Renumbered (−1) after Bonds and Intermarket Analysis were merged into Chapter 6 (Bonds and the Intermarket Chain); section, table, figure and listing numbers and cross-references updated.

**Updated 2026-10-07 (c)** — §7.9 [EVIDENCE] renamed [PROOF] with a PROOF box (size / defined risk / permission); KEY INSIGHT added; internal path-discrepancy note removed from the companion-file pointer.
