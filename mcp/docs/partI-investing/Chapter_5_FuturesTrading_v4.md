|                                                               |
| ------------------------------------------------------------- |
| **PYTHON FOR TRADERS: INVESTING, DERIVATIVES, AND TECHNICAL ANALYSIS APPLIED** |

|                    |        |
| ------------------ | ------ |
| Chapter 5          | **5** |

**Futures Trading: Leverage, Discipline, and Getting Real Market Access**

*A practitioner's framework for trading commodity futures — the contract, the curve that decides what a held position earns, leverage, and sizing — extended with a practical survey of futures exchange/broker APIs and runnable Python examples*

Part I — Investing and Stock Market · Prereqs: Chapter 1 (Investment Classes and Instruments) · Companion files: `futures_trading/` (ib_futures_client.py, ch06_*.py; figures/ for Figures 5.1–5.8)

<table>
<thead>
<tr class="header">
<th><strong>THIS CHAPTER COVERS</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>5.1 What a Futures Contract Actually Is</p>
<p>5.2 The Futures Curve — Carry, Contango, and Backwardation</p>
<p>5.3 Leverage and Margin — Why Futures Cut Both Ways</p>
<p>5.4 Micro Futures — How 2019 Changed Retail Access</p>
<p>5.5 The 2% Rule and Position Sizing</p>
<p>5.6 Order Types and Checks That Enforce Discipline</p>
<p>5.7 Where Commodity Futures Actually Trade — USA and Europe</p>
<p>5.8 [CODE] Hands-On — Risk Checks, Interactive Brokers, and Data</p>
<p>5.9 [PROOF] What the 2% Rule and Micro Contracts Actually Change</p></td>
</tr>
</tbody>
</table>

|                                    |
| ---------------------------------- |
| **5.1 WHAT A FUTURES CONTRACT ACTUALLY IS** |

A futures contract is a standardized, exchange-traded agreement to buy or sell a fixed quantity of an asset — a commodity, an index, a currency — at a set price on a specified future date. Futures are defined by two key traits: high leverage and high risk, and both traits trace back to the same mechanical source: a futures position controls a large notional exposure for a small upfront cash outlay.

**5.1.1 From grain to indices.** Futures began as a hedging tool, not a speculative one. The Chicago Board of Trade (CBOT) opened in 1848 as a central market where farmers and grain dealers could fix a price before harvest, and by 1865 it had standardized those agreements into the first exchange-traded futures contracts — quantity, quality and delivery terms written into the contract instead of negotiated each time. Grain was followed by livestock, cotton and other agricultural products. The modern market took shape in the 1970s and 1980s, when futures moved from physical goods to financial ones: currencies in 1972, interest rates later in the decade, and stock indices in 1982. That history explains a feature of every contract in this chapter: each one was designed so that one side could transfer price risk to the other, and the speculator is the counterparty who accepts it.

*Table 5.1 — Milestones of the futures market*

| **Year** | **Milestone** | **Why it matters today** |
| --- | --- | --- |
| 1848 | Chicago Board of Trade founded | Central marketplace for grain price risk |
| 1865 | First standardized futures contracts at the CBOT | Fixed size, quality and delivery terms: the template every contract still follows |
| 1972 | Currency futures at the CME's International Monetary Market | First financial (non-physical) underlyings |
| 1970s | Interest-rate futures | Hedging for bond portfolios and lenders |
| 1982 | Stock index futures | One contract for a whole equity market |
| 2019 | Micro E-mini index futures | Contract sizes small enough for retail accounts (Section 5.4) |

**5.1.2 Contract specifications are not optional reading.** Every futures contract has a fixed contract size (e.g., 1,000 barrels for WTI crude, 5,000 bushels for corn, 100 troy ounces for gold), a minimum tick size with a fixed dollar value per tick, and an expiration date. Unlike a stock, a futures position does not exist indefinitely — it must be closed, offset, or rolled into the next contract month before expiration, or (for physically-settled contracts) the holder may be obligated to make or take delivery of the underlying commodity.

**5.1.3 Mark-to-market changes the cash-flow picture daily.** Futures accounts are marked to market at the end of every trading session: gains and losses are credited or debited to the account in cash immediately, rather than only being realized on exit as with a stock position. This is why a futures account can receive a margin call mid-trade even on a position the trader still believes in — the daily settlement does not wait for conviction to be proven right.

**5.1.4 Physical delivery vs. cash settlement.** Some contracts (many agricultural and energy futures) are physically settled — a trader holding a position through expiration can be required to deliver or accept the underlying commodity. Others (most stock index futures, and increasingly many commodity variants) are cash-settled, closing out the price difference in cash with no physical asset changing hands. Retail traders almost always close or roll before the delivery notice period specifically to avoid this — confusing the two is a well-known way for a new futures trader to end up owning something inconvenient.

**5.1.5 Reading a contract symbol.** Every listed contract month has its own symbol, built from three parts: the product root, a one-letter month code, and the year. `CLZ6` is WTI crude oil (`CL`) for December (`Z`) 2026 (`6`); `MGCZ6` is Micro Gold for the same month. The twelve month codes are fixed across exchanges and worth memorizing, because order tickets, data vendors and broker APIs all use them. The year is written with one digit on CME Globex and most data feeds, and with two digits on some charting platforms (`CLZ26`) — a one-digit year repeats every decade, so code that parses symbols has to decide which decade is meant.

*Table 5.2 — Futures month codes*

| **Code** | **Month** | **Code** | **Month** | **Code** | **Month** |
| --- | --- | --- | --- | --- | --- |
| F | January | K | May | U | September |
| G | February | M | June | V | October |
| H | March | N | July | X | November |
| J | April | Q | August | Z | December |

Not every product lists every month. Equity index and Treasury futures trade a quarterly cycle (H, M, U, Z); crude oil lists every month; gold's most active months are G, J, M, Q, V and Z. The most liquid contract is usually the nearest one in the cycle — the *front month* — until volume rolls to the next one shortly before expiry (Section 5.6.5).

**5.1.6 Three ways a position ends.** Every futures position ends in one of three ways. (1) **Offset before expiry** — the trader takes the opposite side (sells what was bought, or buys back what was sold) at the current market price; this is how nearly all retail and day-trading positions close. (2) **Expiry or roll** — a position held to the last trading day is closed at the final settlement price, or rolled: the expiring month is closed and the same position is opened in a later month, a step most brokers will not do automatically. (3) **Delivery** — for physically settled contracts, the commodity itself changes hands; this is a small minority of contracts and is reserved for commercial users with the logistics to handle it.

| **◆ EDGE — Leverage is a magnifier, not a strategy**                                                                                                                                                                                                                          |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A futures contract's margin requirement might be 5-10% of the contract's notional value. That means a 5% adverse move in the underlying can represent a 50-100% loss of the margin posted. Leverage does not create edge — it amplifies whatever edge (or lack of one) the underlying strategy already has, in both directions equally. |

|                                                                    |
| ------------------------------------------------------------------ |
| **5.2 THE FUTURES CURVE — CARRY, CONTANGO, AND BACKWARDATION** |

A futures price is not a forecast of the spot price. It is the spot price plus the cost of carrying the commodity to the delivery date, and the shape that cost gives the whole row of contract months decides what a position earns every time it is rolled forward — for a trader who rolls by hand and for every commodity ETC that rolls automatically (Chapter 6).

**5.2.1 Cost of carry and the spot/forward relationship.** Anyone holding the physical commodity to deliver it later bears a **cost of carry** — storage, preservation, insurance, and financing — and the forward price reflects that cost directly:

$$\text{Forward Price} = \text{Spot Price} + \text{Cost of Carry}$$

Arbitrageurs holding the physical commodity step in whenever futures prices drift away from spot-plus-carry, which is what keeps the relationship in equilibrium.

**5.2.2 Contango, backwardation, and roll yield.** The **forward curve** plots futures prices by time to expiration. In **contango** (the standard shape when supply comfortably meets demand), longer-dated futures trade above near-dated ones — and because a long position that wants to stay in the market must periodically sell its expiring contract and buy the next, more expensive one (the **roll**), contango produces a **negative roll yield** that erodes the position even while the spot price sits still. In **backwardation** (near-dated prices above far-dated ones, typically signaling a market in deficit), the roll instead sells high and buys low, producing a **positive roll yield**.

*Table 5.3 — Contango vs. backwardation*

| **Curve shape** | **Typical market condition** | **Roll yield for a long position that rolls** |
| :--- | :--- | :--- |
| Contango (upward-sloping) | Ample supply relative to demand | **Negative** — erodes capital on a long hold |
| Backwardation (downward-sloping) | Tight supply / demand exceeding supply | **Positive** — adds to return on a long hold |

**5.2.3 A real curve: cocoa on 6 October 2026.** Figure 5.1 shows the New York cocoa contract (ICE Futures US, root `CC`, US dollars per tonne, 10 tonnes per contract) as quoted on 6 October 2026, from the nearest month (M1) to the sixth (M6). It shows all three ideas of this section on one curve; the numbers ① to ③ in the figure match the three points below.

![Cocoa futures curve on 6 October 2026 — contango from December 2026 to September 2027, then a dip at December 2027](../images/Ch3_Futures_00_cocoa_curve.png)

*Figure 5.1 — The cocoa forward curve, M1 to M6, 6 October 2026: ① contango, ② the dip at the far end, ③ the December–March roll. M4 and M5 are read from a chart and approximate; the other prices are quotes.*

1. **Contango.** From December 2026 (5,796) to September 2027 (about 6,035), each month is priced above the one before. The step from December to March is 5,922 − 5,796 = **126 $/t**: the market's price for storing, insuring and financing cocoa for three months — the cost of carry of Section 5.2.1.
2. **Backwardation at the far end.** December 2027 (5,962) sits below September. Near the front the curve says supply is comfortable today; at the far end the market prices in more supply by late 2027. One curve can hold both shapes, and the part that matters is the part your position will roll through.
3. **Roll yield.** A long December position must be rolled before expiry: sell December at 5,796, buy March at 5,922. If the curve keeps its shape, March drifts down toward the spot price as it nears expiry, and the 126 $/t is lost even though cocoa itself did not move: −126 ÷ 5,922 = **−2.13% per roll**, about −$1,260 on one 10-tonne contract. December to March is a quarter of a year, so the same roll every quarter compounds to (1 − 0.0213)⁴ − 1 ≈ **−8.3% a year**. Dashboards annualize differently — one showed −12.11% for this same curve by spreading the 2.13% over the 61 days left before the December contract had to be rolled, rather than over the three months between contracts. Check which period an annualized roll yield assumes before comparing two of them. Figure 5.2 sets the three numbers side by side.

![The December–March cocoa roll measured three ways — per roll, per year, and a dashboard's annualization](../images/Ch3_Futures_01_roll_yield.png)

*Figure 5.2 — One roll cost, three numbers: −2.13% per roll, about −8.3% a year rolled quarterly, and −12.11% from a dashboard that annualizes over the 61 days left before the roll.*

In backwardation every sign flips: the roll sells the dearer front month, buys the cheaper next one, and the position earns the difference.

|                                    |
| ---------------------------------- |
| **5.3 LEVERAGE AND MARGIN — WHY FUTURES CUT BOTH WAYS** |

**5.3.1 Margin is a deposit, not a loan.** Buying a stock on margin means borrowing part of the price from the broker: you own the shares, owe the loan, and pay interest on it. A futures position works differently. Nothing is bought and nothing is borrowed — the contract is an agreement to buy or sell later at today's price. The margin is cash left with the broker as a good-faith deposit, proof that you can cover the losses the position may produce. It is not a payment toward the contract, and there is no interest to pay, because there is no loan.

**5.3.2 Where the leverage comes from.** The contract controls a large quantity of the commodity — its *notional value*, price × contract size — while the deposit is small. Take one Micro Gold contract (Section 5.4) with gold at $3,000, using the illustrative margins of Section 5.9:

- Notional value: 10 ounces × $3,000 = **$30,000**.
- Initial margin: **$1,650**, so $1,650 controls $30,000 of gold — leverage of about **18:1**.
- A 1% move in gold is 30 points × $10 = **$300**, about **18%** of the deposit.

Leverage multiplies gains and losses by the same factor. It changes the size of the swing, not the odds of the trade (Figure 5.3).

![A $1,650 deposit against a $30,000 contract value](../images/Ch3_Futures_0a_margin_deposit.png)

*Figure 5.3 — One Micro Gold contract with gold at $3,000: the deposit is about 1/18 of the value it controls.*

**5.3.3 Marked to market every day: initial margin, maintenance margin, margin call.** Gains and losses are not settled when the trade is closed but every evening: the day's result is paid into or taken out of the account in cash (*mark-to-market*). Two levels govern the account. *Initial margin* is the amount required to open the position; *maintenance margin* is the lower floor equity must stay above once it is open. When losses push equity below maintenance, the broker issues a *margin call*: deposit enough to bring the account back to **initial** margin — not merely to maintenance — or the position is closed, often automatically and at the worst moment of a fast market. With the figures above, an ordinary week of gold prices (the path of Listing 5.6) breaches the $1,500 floor twice and costs $400 in new cash on top of a $460 trading loss (Figure 5.4).

![Account equity over one week with two margin calls](../images/Ch3_Futures_0b_margin_call.png)

*Figure 5.4 — Account equity over one week, one Micro Gold contract: two falls below maintenance margin, each topped back up to initial. Illustrative margins as in Section 5.9; the price path is that of Listing 5.6.*

**5.3.4 Who sets margin, and who stands behind it.** The exchange sets minimum margins from the contract's recent volatility; brokers often require more. Margins are not fixed: in turbulent markets exchanges raise them, sometimes overnight, and traders already stretched receive margin calls even if their price has not moved. Behind the trader sits a layer never seen directly. The broker, as a clearing member, posts *clearing margin* with the exchange's clearing house for every open position, and the clearing house becomes the buyer to every seller and the seller to every buyer. That guarantee is what makes a futures contract safe to hold against a counterparty you never meet — and the broker's own margin rules exist to protect the deposit it must post (Figure 5.5).

![Trader, broker and clearing house, with the margin each one posts](../images/Ch3_Futures_0c_margin_layers.png)

*Figure 5.5 — Three layers of margin: the trader's initial and maintenance margin, the broker's clearing margin, and the clearing house that guarantees every trade.*

**5.3.5 Your leverage is your choice, not the exchange's.** Reg-T margin caps retail stock leverage near 2:1; futures margins commonly allow 10:1 to 20:1 or more. But the 18:1 of Section 5.3.2 assumes the account holds only the minimum deposit. Effective leverage is the notional value divided by the **whole account**, not by the margin: one Micro Gold contract in a $30,000 account is 1:1 leverage, and a 1% move costs 1% of the account; the same contract in a $1,650 account is 18:1, and an ordinary bad week ends it. Margin is the minimum the broker requires to hold a position — not a measure of what you can afford to lose. This is why Sections 5.5–5.6 size every trade by its stop, at no more than 2% of the account, never by how many contracts the margin allows; Section 5.9 shows the two methods side by side, and Figure 5.6 shows how the same contract changes character with the size of the account.

![Effective leverage of one Micro Gold contract in $1,650, $5,000 and $30,000 accounts](../images/Ch3_Futures_0d_effective_leverage.png)

*Figure 5.6 — Effective leverage is contract value divided by the whole account: 18:1, 6:1 and 1:1 for the same contract.*

|                                    |
| ---------------------------------- |
| **5.4 MICRO FUTURES — HOW 2019 CHANGED RETAIL ACCESS** |

**5.4.1 The accessibility problem micro contracts solved.** A standard E-mini S&P 500 futures contract, for example, controls a notional exposure that can run into six figures — putting it out of reach for most small accounts on a properly risk-managed basis. In 2019, the CME Group introduced Micro E-mini contracts at 1/10th the notional size of their standard counterparts, and micro-sized versions of commodity contracts followed the same pattern. This is a genuine structural shift: for the first time, index and commodity futures exposure became sized appropriately for accounts that would previously have been forced to either skip futures entirely or take on outsized risk relative to their capital.

**5.4.2 Micro contracts do not remove leverage — they right-size it.** A Micro contract still carries the same percentage leverage characteristics as its standard-sized counterpart; what changes is the absolute dollar amount at stake per contract. This matters directly for Section 5.5's 2% rule: a smaller contract size means the position-sizing math can actually produce a whole-number contract count that respects the rule, rather than forcing an account to either violate the rule or sit out the trade entirely.

**5.4.3 Starter contracts and their point values.** Four products recur in almost every beginner's watchlist because they combine deep liquidity with long trading hours: the S&P 500 index, WTI crude oil, gold, and the 10-year US Treasury note. Table 5.4 gives the number that matters for sizing — the dollar value of a one-point move — for the standard and micro versions. Notional value is simply price × point value, so it moves with the market; margin is set by the exchange from recent volatility and changes often. Neither is printed here as a fixed figure — read both from the exchange or broker on the day you trade. (The original "big" S&P 500 contract at $250 per point was delisted in September 2021; the E-mini is now the standard size.)

*Table 5.4 — Starter contracts: size and value of a one-point move*

| **Market** | **Standard (root)** | **$ per point** | **Micro (root)** | **$ per point** | **Minimum tick** |
| --- | --- | --- | --- | --- | --- |
| S&P 500 index | E-mini (ES) | $50 | Micro E-mini (MES) | $5 | 0.25 pt = $12.50 / $1.25 |
| WTI crude oil | CL, 1,000 bbl | $1,000 | MCL, 100 bbl | $100 | $0.01 = $10 / $1 |
| Gold | GC, 100 oz | $100 | MGC, 10 oz | $10 | $0.10 = $10 / $1 |
| 10-year T-Note | ZN, $100,000 face | $1,000 | — | — | 1/64 of a point = $15.625 |

| **⚠ WARNING — Margin figures in books and blog posts go stale**                                                                                                                                                       |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Exchanges revise margins whenever volatility changes, and brokers add their own day-trading and overnight rates on top. A margin figure copied from a book or an old article can be wrong by a factor of two. Size positions from the stop-loss (Section 5.5), and treat the current margin only as the cash the broker will lock up — never as a measure of risk. |

|                                    |
| ---------------------------------- |
| **5.5 THE 2% RULE AND POSITION SIZING** |

The central risk-control rule: never risk more than 2% of total account equity on a single trade. In futures terms, "risk" means the dollar distance from entry to the pre-planned stop-loss, multiplied by the contract's point value and the number of contracts held — not the margin posted, and not the notional contract value.

**5.5.1 The rule in formula form.** The number of contracts allowed is the 2% risk budget divided by the dollar risk of one contract, rounded down: *contracts = ⌊ equity × 2% ÷ (stop distance in points × point value) ⌋*. A $25,000 account with a 20-point stop on Micro Gold ($10 a point) may hold ⌊ 500 ÷ 200 ⌋ = 2 contracts. Listing 5.1 (Section 5.8.1) states the rule, and the per-market cap of Section 5.5.3, as two functions.

**5.5.2 Why this rule is what makes leverage survivable.** Ten consecutive losing trades at 2% risk each reduces an account by roughly 18% (compounding drawdown, not simple subtraction) — painful, but recoverable. Ten consecutive losses at 10% risk each destroys roughly 65% of the account. The 2% rule is not a suggestion about caution in the abstract; it is the specific parameter that determines whether a losing streak — which every strategy eventually has — is a setback or an account-ending event.

**5.5.3 Per-trade limits and per-market limits.** The 2% rule caps one trade. It says nothing about three trades in the same commodity, which will win or lose together because they share one price. A second, coarser limit closes that gap: keep the combined open risk in any single market to 3–5% of equity. With 2% per trade and a 5% per-market cap, at most two full-size positions can share a commodity at once; a third has to wait until one of them is closed or its stop has been moved to break-even. The two rules are complementary, not alternatives — the first protects against one bad trade, the second against one bad market. (Appendix A, Section A.2, adds a third ceiling one level up: total exposure to a whole market group, such as all precious metals.)

Listing 5.1 includes this cap as `market_risk_ok()`.

|                                    |
| ---------------------------------- |
| **5.6 ORDER TYPES AND CHECKS THAT ENFORCE DISCIPLINE** |

**5.6.1 Stop-loss orders.** A stop-loss order automatically closes a position once price reaches a pre-specified adverse level, converting the 2% rule from an intention into an enforced, mechanical outcome. Without a working stop-loss order actually resting on the exchange (not just "a level I'm watching"), the 2% rule is a plan, not a control.

**5.6.2 OCO — One Cancels the Other.** An OCO order pairs a stop-loss and a take-profit order such that filling either one automatically cancels the other. This removes a specific failure mode: a trader who manually cancels a stop-loss after a profit target fills, forgets, and is left with an unprotected position. OCO orders are standard functionality on virtually every futures-capable broker platform and are one of the more mechanical, low-effort risk controls available.

**5.6.3 Time in force — Day vs. GTC.** Every order also carries an instruction for how long it stays alive. A *Day* order is cancelled automatically at the end of the trading session if it has not been filled; a *Good-Till-Cancelled* (GTC) order stays on the book until it is filled or cancelled by the trader, although most brokers cap its life at 30–90 days. The choice matters most for protective orders: a stop-loss entered as a Day order silently disappears at the session close and leaves an overnight position unprotected.

*Table 5.5 — Time-in-force instructions*

| **Instruction** | **Lives until** | **Use it for** | **Watch out for** |
| --- | --- | --- | --- |
| Day | End of the current session | Intraday entries and exits | A Day stop-loss expires at the close, leaving overnight positions unprotected |
| GTC | Filled or cancelled (broker limit, often 30–90 days) | Stop-losses and targets on positions held overnight | Forgotten GTC orders on positions already closed elsewhere |

**5.6.4 Trailing stops.** A trailing stop follows price at a fixed distance as the trade moves in your favor and never moves back. On a long position the stop rises with each new high; if price then falls by the trailing distance, the position is closed. The trailing stop keeps the 2% rule intact at entry — the initial distance is the risk — while gradually converting open profit into locked-in profit. Most broker platforms offer it as a native order type; Listing 5.2 (Section 5.8.2) shows the logic, which is also what a backtest needs to reproduce.

**5.6.5 Check liquidity before you trade.** Two numbers published for every contract month tell you whether a market can take your order at a fair price. *Volume* is the number of contracts traded in a session: high volume means tight spreads and fills close to the quoted price. *Open interest* is the number of contracts still open at the end of the session: it shows how many positions are actually held, and it identifies the active month, because both volume and open interest migrate from the expiring contract to the next one in the days before expiry. Trade the month where they are concentrated, and keep your own size a small fraction of daily volume. Chapter 9 reads the same two series as market signals; here they are simply a gate. Listing 5.3 (Section 5.8.3) turns both checks into one pre-trade gate.

|                                    |
| ---------------------------------- |
| **5.7 WHERE COMMODITY FUTURES ACTUALLY TRADE — USA AND EUROPE** |

**5.7.1 The US landscape.** Nearly all US-listed commodity futures sit under two umbrellas. **CME Group** owns three divisions: NYMEX (energy: WTI crude oil, natural gas), COMEX (metals: gold, silver, copper) and CBOT (grains: corn, wheat, soybeans). **ICE Futures US**, in New York, lists the softs: arabica coffee, cocoa, sugar No. 11 and cotton. Figure 5.7 counts the benchmark contracts on each venue.

![US commodity futures venues — CME Group's NYMEX, COMEX and CBOT against ICE Futures US](../images/Ch3_Futures_1_us_venues.png)

*Figure 5.7 — US commodity futures venues. Slices count the benchmark contracts named, one per commodity, not traded volume.*

**5.7.2 The European landscape.** Europe has no single umbrella. Five venues share the main contracts, and two of them are in London, outside the EU:

- **ICE Futures Europe** (London): Brent crude oil — the world's main oil benchmark, and a London contract, not a US one — plus gasoil, London cocoa, robusta coffee and white sugar.
- **ICE Endex** (Amsterdam): Dutch TTF natural gas, Europe's gas benchmark.
- **LME** (London Metal Exchange): copper, aluminium, nickel, zinc.
- **Euronext** (Paris, the former MATIF): milling wheat, rapeseed, corn.
- **EEX** (European Energy Exchange, Leipzig): European power.

Figure 5.8 puts the two regions side by side.

![USA vs Europe — 12 benchmark contracts on two US venue groups, 14 on five European venues](../images/Ch3_Futures_2_us_vs_europe.png)

*Figure 5.8 — USA vs Europe. Counts of the benchmark contracts named, not traded volume.*

**5.7.3 Same commodity, two contracts.** Cocoa, coffee, sugar, copper and corn trade on both sides of the Atlantic, and the contracts are not interchangeable. New York cocoa is priced in US dollars, London cocoa in pounds sterling; arabica (New York) and robusta (London) are different beans with different prices. Before reading a quote or a chart, check which venue and which contract it belongs to.

**5.7.4 The exchange itself is not where a retail trader connects.** None of these venues offers a simple, sign-up-and-go public API the way a crypto exchange like Kraken does elsewhere in this project's code. Direct connectivity (CME iLink, ICE gateways, co-located matching-engine access) is built for exchange members and clearing firms, with the cost and infrastructure requirements to match. Retail access, for both orders and market data, runs through a broker. This book uses one, Interactive Brokers, because a single account reaches most of the venues in Table 5.6.

*Table 5.6 — Commodity futures venues in the USA and Europe, and Interactive Brokers access*

| **Venue** | **Location** | **Main commodities** | **IB exchange code** | **IB access** |
| --- | --- | --- | --- | --- |
| CME Group (NYMEX, COMEX, CBOT) | Chicago, New York | Energy, metals, grains | NYMEX, COMEX, CBOT | Yes |
| ICE Futures US | New York | Softs | NYBOT | Yes |
| ICE Futures Europe | London | Brent, gasoil, London softs | IPE | Yes |
| ICE Endex | Amsterdam | TTF gas, power | ENDEX | Yes |
| Euronext | Paris | Milling wheat, rapeseed, corn | MATIF | Yes |
| LME | London | Base metals | — | Only IB's OTC look-alike futures, with IB UK as counterparty; not offered to US residents |
| EEX | Leipzig | European power | — | Not listed by IB at the time of writing |

Exchange codes are as IB names them on its fee and market-data pages; confirm each in IB's Contract Search before use.

|                                    |
| ---------------------------------- |
| **5.8 [CODE] HANDS-ON — RISK CHECKS, INTERACTIVE BROKERS, AND DATA** |

This section collects the chapter's code: first the three checks of Sections 5.5–5.6 that every order must pass, then the Interactive Brokers connection that places the order and the data sources behind it. The risk functions run offline; the IB listings run against a free paper account.

**5.8.1 The 2% rule and the per-market cap (Sections 5.5.1 and 5.5.3).**

**💻 PYTHON · Listing 5.1 — `max_contracts` and `market_risk_ok`: the 2% rule and the per-market cap**

```python
def max_contracts(equity, risk_pct, stop_points, point_value):
    """Contracts allowed by the 2% rule (risk_pct=0.02); point_value = $ per full point."""
    return int(equity * risk_pct // (stop_points * point_value))

def market_risk_ok(open_risks, new_risk, equity, cap_pct=0.05):
    """Per-market cap (Section 5.5.3): total open $ risk in one market <= 5% of equity."""
    return sum(open_risks) + new_risk <= equity * cap_pct

# max_contracts(25_000, 0.02, 20, 10)     -> 2     Micro Gold, 20-point stop, $400 at risk
# market_risk_ok([200, 200], 200, 10_000) -> False 6% of equity in one market > 5%
```

Full version, with self-test: `code_snippets/futures_trading/ch06_risk.py`.

**5.8.2 The trailing stop (Section 5.6.4).**

**💻 PYTHON · Listing 5.2 — `trailing_stop`: a stop that follows price and never moves back**

```python
def trailing_stop(prices, distance):
    """Long-side trailing stop: the stop after each price, and the index where it is hit."""
    stops = []
    for i, p in enumerate(prices):
        if stops and p <= stops[-1]:
            return stops, i
        stops.append(max(stops[-1], p - distance) if stops else p - distance)
    return stops, None

# trailing_stop([100, 102, 105, 104, 101], 3) -> ([97, 99, 102, 102], 4)
```

Full version, with self-test: `code_snippets/futures_trading/ch06_risk.py (long and short side)`.

**5.8.3 The liquidity gate (Section 5.6.5).**

**💻 PYTHON · Listing 5.3 — `liquidity_gate`: volume and open interest as a pre-trade check**

```python
def liquidity_gate(volume, open_interest, my_contracts, min_avg_volume=10_000,
                   min_oi=20_000, max_share=0.01, window=20):
    """Pass only a liquid contract month, and only if my order is a small share of it."""
    avg_vol = volume.tail(window).mean()
    oi = open_interest.dropna().iloc[-1]
    return (avg_vol >= min_avg_volume and oi >= min_oi
            and my_contracts <= max_share * avg_vol)
```

Full version, with self-test: `code_snippets/futures_trading/ch06_liquidity.py (returns each check separately)`.

**5.8.4 Orders through `ib_async`.** IB requires the TWS desktop application or IB Gateway running locally (or on a server) as the connection point; the Python library then talks to that local process. `ib_async` is the maintained successor of the archived `ib_insync` library and keeps the same interface. A paper-trading account is free and uses a separate port, so every listing below can be run without risking money.

**💻 PYTHON · Listing 5.4 — Streaming a commodity future's quote and placing a bracket order (Interactive Brokers)**

```python
from ib_async import IB, Future

ib = IB()
ib.connect("127.0.0.1", 7497, clientId=1)            # 7497 = paper-trading port
cl = Future("CL", "202612", "NYMEX")                 # WTI crude, December 2026 (CLZ6)
ib.qualifyContracts(cl)
tick = ib.reqMktData(cl)
ib.sleep(2)

for order in ib.bracketOrder("BUY", 1, limitPrice=tick.ask,      # entry + OCO exits
                             takeProfitPrice=tick.ask + 2.00,
                             stopLossPrice=tick.ask - 1.00):
    ib.placeOrder(cl, order)
```

Full version, with self-test: `code_snippets/futures_trading/ib_futures_client.py`.

**5.8.5 Market data through IB: delayed for free, real time by subscription.** IB streams delayed quotes at no charge: about 10 minutes behind for CME, ICE Futures US and ICE Futures Europe commodities, 15 minutes for Euronext. That is enough to learn the API, test a strategy's plumbing and do end-of-day research. Real-time quotes, and in practice most historical bars, need that exchange's monthly market-data subscription. Listing 5.5 switches to delayed data and requests one US and two European contracts with the same call.

**💻 PYTHON · Listing 5.5 — Delayed quotes and daily bars for US and European contracts (Interactive Brokers)**

```python
from ib_async import IB, Future

ib = IB()
ib.connect("127.0.0.1", 7497, clientId=2)
ib.reqMarketDataType(3)                    # 3 = delayed (free); 1 = real time (subscription)

contracts = {                              # symbol and exchange as IB's Contract Search shows them
    "WTI crude, NYMEX":           Future("CL",   "202612", "NYMEX"),
    "Brent, ICE Futures Europe":  Future("COIL", "202612", "IPE"),
    "Milling wheat, Euronext":    Future("EBM",  "202612", "MATIF"),
}
for name, c in contracts.items():
    if not ib.qualifyContracts(c):
        print(f"{name}: not found - check symbol and exchange"); continue
    bars = ib.reqHistoricalData(c, endDateTime="", durationStr="1 Y",
                                barSizeSetting="1 day", whatToShow="TRADES", useRTH=True)
    print(f"{name}: {len(bars)} daily bars")   # 0 bars: subscription missing
```

**5.8.6 Where else the data comes from.** IB is the only connection this chapter needs, but it is not the only source of prices, and an independent source is the way to check what the broker shows. Table 5.7 lists, for each venue, what is free, what IB charges for real time, and who sells the full history.

*Table 5.7 — Market-data sources for US and European commodity futures*

| **Venue** | **Free (delayed or end of day)** | **IB real time, monthly (non-professional)** | **Paid history and full feeds** |
| --- | --- | --- | --- |
| CME Group | Delayed quotes and daily settlement prices on cmegroup.com; IB delayed (~10 min); daily front-month history via `yfinance` (`CL=F`, `NG=F`, `GC=F`, `ZW=F`) | US$1.55 per exchange, top of book | CME DataMine; vendors such as Databento (dataset GLBX.MDP3) |
| ICE Futures US | Delayed quotes and settlement prices on ice.com; IB delayed (~10 min); daily front-month history via `yfinance` (`CC=F`, `KC=F`, `SB=F`, `CT=F`) | US$142 | ICE Data Services; Databento (IFUS.IMPACT) |
| ICE Futures Europe | Delayed quotes and settlement prices on ice.com; IB delayed (~10 min) | US$155 | ICE Data Services; Databento (IFEU.IMPACT, from December 2018) |
| ICE Endex | Settlement prices on ice.com | US$155 | ICE Data Services; Databento (NDEX.IMPACT) |
| Euronext | Delayed quotes and settlement prices on live.euronext.com; IB delayed (15 min) | €20 | Euronext market-data services |
| LME | Official and closing prices, next day, free after registration on lme.com | — | LMElive (real time or 30-minute delayed); LME historical data; licensed distributors |
| EEX | Settlement prices on eex.com | — | EEX market-data services |
| Positioning (all) | Weekly Commitments of Traders: CFTC for US venues; ICE Futures Europe and Euronext publish their own | — | — |

`yfinance` reads Yahoo Finance's free daily series for US venues only — the `=F` tickers are one continuous front-month series per commodity, not adjusted for rolls, so each roll shows as a price jump (Section 5.2) and the separate contract months needed for a forward curve are not covered. It is an unofficial library and can break when Yahoo changes its site. No European contract is available this way. IB fees are those published on its market-data pricing page in October 2026; some subscriptions require a base bundle, and all of them change. Check the page before subscribing.

|                                    |
| ---------------------------------- |
| **5.9 [PROOF] WHAT THE 2% RULE AND MICRO CONTRACTS ACTUALLY CHANGE** |

**5.9.1 The 2% rule makes the standard contract impossible.** Consider a $10,000 account, a common starting size for a retail futures trader, evaluating a Gold futures trade with a planned stop 4 points away.

Standard Gold (GC) has a point value of $100. A 4-point stop therefore risks $400 per contract — already 4% of a $10,000 account with just *one* contract, before the 2% rule is even applied. The rule mathematically forbids trading a full-size GC contract on this setup at this account size; `max_contracts()` from Listing 5.1 returns 0 for the standard contract at 2% risk.

Micro Gold (MGC) has a point value of $10 — one-tenth of GC. The same 4-point stop now risks $40 per contract, or 0.4% of the $10,000 account. `max_contracts(10_000, 0.02, 4, 10)` returns 5 — the account can now take a properly risk-managed position that respects the 2% rule, something the standard contract made mathematically impossible at this account size.

This is the concrete mechanism behind Section 5.4's claim that Micro contracts were a structural shift, not a marketing gimmick: they are the specific change that lets a small account satisfy the 2% risk rule rather than being forced to either oversize a position or sit out the trade entirely.

**5.9.2 Margin is not a risk limit.** A broker will let the same $10,000 account open as many Micro Gold contracts as its initial margin covers. Listing 5.6 replays one ordinary week of gold prices — seven sessions, a net decline of about 1.5% — through the daily mark-to-market for four ways of sizing the same trade. The margin figures are illustrative (maintenance margin at 5% of notional, initial margin at 110% of maintenance, entry at 3,000); the conclusions depend on the ratios, not on the exact numbers.

**💻 PYTHON · Listing 5.6 — Daily mark-to-market: which sizing ends at its stop, which ends in a margin call**

```python
ENTRY, POINT_VALUE, EQUITY = 3_000.0, 10.0, 10_000.0   # Micro Gold (MGC)
MAINT = 0.05 * ENTRY * POINT_VALUE      # $1,500 per contract (illustrative)
INITIAL = 1.10 * MAINT                  # $1,650 per contract
PATH = [-12, -9, 6, -15, -10, 8, -14]   # daily moves in points

def run(n, stop_points=None, equity=EQUITY):
    move = 0.0
    for day, d in enumerate(PATH, start=1):
        move += d
        if stop_points is not None and move <= -stop_points:
            return day, "stopped", stop_points * POINT_VALUE * n
        if equity + move * POINT_VALUE * n < n * MAINT:
            return day, "MARGIN CALL", -move * POINT_VALUE * n
    return None, "open", -move * POINT_VALUE * n

def points_to_margin_call(n, equity=EQUITY):
    return (equity - n * MAINT) / (n * POINT_VALUE)

# run(6) -> (2, 'MARGIN CALL', 1260.0)    margin-max: int(10_000 // 1_650) = 6
# run(1, 20) -> (2, 'stopped', 200.0)     2% rule with a 20-point stop
```

*Table 5.8 — Four sizings of the same Micro Gold trade on one ordinary week*

| **Sizing** | **Contracts** | **Notional leverage** | **Adverse move to margin call** | **Outcome** | **Loss** |
| --- | --- | --- | --- | --- | --- |
| Margin-max, no stop | 6 | 18.0x | 16.7 points (0.6%) | Margin call, day 2 | $1,260 (12.6%) and forced liquidation |
| Margin-max, 20-pt stop | 6 | 18.0x | 16.7 points (0.6%) | Stopped, day 2 | $1,200 (12.0%) |
| 2% rule, 4-pt stop | 5 | 15.0x | 50 points (1.7%) | Stopped, day 1 | $200 (2.0%) |
| 2% rule, 20-pt stop | 1 | 3.0x | 850 points (28%) | Stopped, day 2 | $200 (2.0%) |

<table>
<thead>
<tr class="header">
<th><strong>▶ PROOF — What the four sizings show</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>Sizing by margin is sizing for a margin call. Six contracts is the most the broker allows, and at that size a 0.6% move — less than one ordinary day — puts the account below maintenance margin. The position is liquidated at the broker's price on day 2, with a 12.6% loss.</p>
<p>A stop does not rescue an oversized position. With the same six contracts and a 20-point stop, the stop fires before the margin call, but it still costs 12% of the account. The stop defines where you exit; only the contract count defines how much that exit costs.</p>
<p>The 2% rule caps the loss whatever the stop width. A tight 4-point stop allows 5 contracts and a wide 20-point stop allows 1, yet both lose exactly $200. The rule converts stop width into position size, so the dollar risk stays fixed.</p>
<p>The 2% rule is not a low-leverage rule. Five contracts with a 4-point stop is 15x notional leverage, almost as high as the margin-max position, but the loss is still capped at 2% because the stop sits far inside the margin-call distance (4 points vs. 50). What matters is not the leverage itself but whether the stop is triggered long before the margin call.</p>
<p>Caveats: one illustrative path, settlement at the daily close, stops assumed to fill exactly at their level. A price gap through a stop makes every loss larger, which strengthens rather than weakens the case for small size.</p></td>
</tr>
</tbody>
</table>

▶ `futures_trading/ib_futures_client.py` implements this pattern end to end: `max_contracts_2pct()` mirrors Listing 5.1, `make_future_contract()`/`get_snapshot()`/`fetch_historical_bars()` wrap Interactive Brokers market data, and `place_protected_order()` wraps the bracket-order pattern from Listing 5.4 -- with an `is_paper_account()` guard rail that refuses to submit unless the connected account is a paper ("DU"-prefixed) account. The listings in this chapter ship as `futures_trading/ch06_risk.py`, `ch06_liquidity.py` and `ch06_margin_proof.py`, each with an offline `--selftest`; `ch06_symbols.py` parses and builds contract symbols (Section 5.1.5) without being printed here.

<table>
<tbody>
<tr class="odd">
<td><p><strong>◈ KEY INSIGHT<br />
</strong></p>
<p><em>"Margin tells you how much a broker will let you hold; the 2% rule tells you how much you can afford to lose. Size by the second, and the first never becomes a margin call."</em></p></td>
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
<td><p>A futures contract is a standardized, exchange-traded, expiring agreement — mark-to-market settlement and fixed contract sizes make it behave differently from a stock position in ways that matter for risk management.</p>
<p>Futures began in 1848–1865 as a grain-hedging tool and moved to currencies (1972), interest rates and stock indices (1982); every contract still exists so that one side can transfer price risk to the other.</p>
<p>A contract symbol is root + month code + year (CLZ6 = WTI crude, December 2026); the twelve month codes run F G H J K M N Q U V X Z.</p>
<p>Positions end by offset (nearly all retail trades), by expiry or roll, or by delivery (a small minority, for commercial users).</p>
<p>A futures price is spot plus the cost of carry. In contango the curve slopes up and every roll of a long position sells cheap and buys dear (negative roll yield); in backwardation the roll pays. On 6 October 2026 the cocoa curve was in contango from December to September: rolling December into March cost 2.13%, about 8% a year if repeated every quarter with the spot price unchanged.</p>
<p>Futures leverage (often 10:1-20:1+) is structurally higher than Reg-T stock margin (2:1) -- the same percentage price move produces a much larger swing in account equity; clearing margin at the clearing house sits behind the initial and maintenance margin the trader sees.</p>
<p>Micro futures contracts (introduced 2019, roughly 1/10th standard size) right-sized futures exposure for small accounts -- they don't remove leverage, they make the 2% rule mathematically satisfiable.</p>
<p>The 2% rule caps risk-per-trade as stop-distance-in-dollars, not margin or notional value; a 3–5% cap on combined open risk per market protects against several trades failing together.</p>
<p>Stop-loss, OCO, GTC time-in-force and trailing stops convert the rules into exchange-enforced outcomes; volume and open interest decide which contract month is liquid enough to trade.</p>
<p>Sizing by margin is sizing for a margin call: on the same week of prices, the margin-max position loses 12–13% while both 2%-rule positions lose exactly 2%.</p>
<p>US commodity futures sit under CME Group (NYMEX, COMEX, CBOT) and ICE Futures US; Europe is split across ICE Futures Europe and the LME in London, ICE Endex, Euronext and EEX — Brent is a London contract. Retail traders connect through a broker: Interactive Brokers reaches all of them except EEX (and the LME only through OTC look-alikes), with free delayed data and paid real-time subscriptions.</p></td>
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
<td><p><strong>Futures contract</strong> A standardized, exchange-traded agreement to buy/sell a fixed quantity of an asset at a set price on a future date.</p>
<p><strong>Mark-to-market</strong> Daily cash settlement of gains/losses on an open futures position.</p>
<p><strong>Initial margin</strong> Cash required to open a futures position; a fraction of notional contract value.</p>
<p><strong>Maintenance margin</strong> The equity floor that triggers a margin call if breached.</p>
<p><strong>Clearing margin</strong> The deposit a clearing member posts with the clearing house for each open position; it backs the clearing house's guarantee of every trade.</p>
<p><strong>Month code</strong> The one-letter code for a contract month: F G H J K M N Q U V X Z for January to December.</p>
<p><strong>Front month</strong> The nearest contract month in a product's cycle, usually the most liquid until volume rolls to the next one.</p>
<p><strong>Offset</strong> Closing a futures position by taking the opposite side before expiry.</p>
<p><strong>Micro futures</strong> Contracts sized at roughly 1/10th of their standard counterpart, introduced industry-wide starting in 2019.</p>
<p><strong>2% rule</strong> Never risk more than 2% of account equity (measured as stop-distance x point value x contracts) on one trade.</p>
<p><strong>Per-market cap</strong> A 3–5% limit on the combined open risk of all trades in one market.</p>
<p><strong>Point value</strong> Dollar value of one full point move in a given futures contract; varies by contract.</p>
<p><strong>OCO (One Cancels the Other)</strong> A paired stop-loss/take-profit order where filling one cancels the other.</p>
<p><strong>Day order / GTC</strong> Time-in-force instructions: a Day order expires at the session close; a Good-Till-Cancelled order stays live until filled or cancelled.</p>
<p><strong>Trailing stop</strong> A stop that follows price at a fixed distance in the trade's favor and never moves back.</p>
<p><strong>Open interest</strong> The number of contracts still open at the end of a session.</p>
<p><strong>Physical delivery</strong> Contract settlement requiring the actual underlying commodity to change hands.</p>
<p><strong>Cash settlement</strong> Contract settlement by paying/receiving the price difference in cash, no physical delivery.</p>
<p><strong>Roll</strong> Closing a near-expiration futures position and opening the equivalent position in a later contract month.</p>
<p><strong>Cost of carry</strong> Storage, insurance, and financing costs of holding the physical commodity to delivery; forward price = spot price + cost of carry.</p>
<p><strong>Forward curve</strong> The prices of successive contract months at one moment (the term structure).</p>
<p><strong>Contango</strong> A forward curve where later months trade above nearer ones — negative roll yield for a long position.</p>
<p><strong>Backwardation</strong> A forward curve where nearer months trade above later ones — positive roll yield for a long position.</p>
<p><strong>Roll yield</strong> The gain or loss from selling an expiring contract and buying the next one out.</p>
<p><strong>Benchmark contract</strong> The futures contract whose price the market uses as the reference for a commodity (WTI and Brent for crude oil, TTF for European gas).</p>
<p><strong>Delayed market data</strong> Quotes released 10–15 minutes after real time; free at most brokers, enough for learning and end-of-day research, not for placing orders.</p></td>
</tr>
</tbody>
</table>

| **WHAT'S NEXT**                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Chapter 6 (ETCs and ETNs) packages the position this chapter trades by hand: a commodity ETC holds futures and executes the roll of Section 5.2 for you, so its return is the futures return — roll yield included — rather than the spot price. Further on, Chapter 7 (Options Trading) carries the same leverage-and-sizing discipline over to options, Appendix A (Money Management and Trading Psychology) generalizes the sizing rules, and Chapter 9 reads the volume and open-interest series this chapter's liquidity check uses as signals. Venue, broker and data-source details (Sections 5.7–5.8) were compiled in October 2026 from the exchanges', Interactive Brokers' and data vendors' own pages — verify exchange codes, contract specifications, margins and data fees against those sources before running the code, as they change over time. |

---

**Updated 2026-09-13** to match `.claude/CLAUDE.md` §3.3's continuous manuscript numbering: this chapter was Chapter 10, in Part II -- Investing and Stock Market. All internal section/table/listing references (previously F.x) were renumbered to this project's continuous sequence, and the header digit box changed from "F" to a number -- the chapter keeps its "Reference Chapter" / standalone framing (Prereqs: None, "WHERE THIS FITS" instead of "WHAT'S NEXT") per the user's decision to renumber sections only, not restructure format.

**Updated 2026-09-22** -- this chapter previously shifted from Chapter 9 to Chapter 10 (a project-wide +1 renumbering across the five chapters then numbered 7-11, to open up Chapter 7 for a new "Investing in Bonds" reference chapter), and now shifts again from Chapter 10 to Chapter 7 (all internal section, table, and listing numbers decremented by three accordingly) as part of a further project-wide left-shift across the six chapters then numbered 7-12, to close the gap opened when Chapters 1-3 (Investment Classes and Instruments, Exchange Traded Products, and Investing in Stocks) were added ahead of this reference set. This chapter remains self-contained, with no cross-references into other chapters of this set to update. Historical dated notes above have had their internal chapter/section numbers updated for consistency with the current numbering; where a note describes an intermediate historical state, it now reflects the final current number rather than the intermediate one.

**Updated 2026-10-03** -- Dividend Investing (formerly Chapter 6) was removed from the manuscript; Chapters 7-15 shifted down by one to 6-14. All internal section, table, listing and figure numbers and cross-chapter references in the body were decremented accordingly. Historical dated notes above are left as written.

**Updated 2026-10-05** -- integrated material from a summary of futures-trading notes (user-supplied; no book or author named, per house rule 8). Added: 6.1.1 history (Table 6.1), 6.1.5 contract symbols and month codes (Table 6.2, Listing 6.1), 6.1.6 three ways a position ends, clearing margin in 6.2.1, 6.3.3 starter contracts and point values (Table 6.3) + WARNING on stale margin figures, 6.4.3 per-market 3-5% cap (Listing 6.3), 6.5.3 Day vs. GTC (Table 6.4), 6.5.4 trailing stops (Listing 6.4), 6.5.5 liquidity check with volume/open interest (Listing 6.5), stop-moving and hindsight habits in 6.6, 6.9 retitled [PROOF] with 6.9.2 margin-call simulation (Listing 6.9, Table 6.7, PROOF box), new 6.10 advantages vs. costs (Table 6.8). Corrected from the source: November month code X (missing), Globex hours (not 24/7), the delisted $250 S&P contract, date-sensitive margin/commission/volume figures replaced by formulas. Also fixed: Listing 6.2 example (Micro Gold is $10/point, not $1), expired 2025 contract months -> December 2026, `ib_insync` -> `ib_async`, stale Chapter_D reference in WHERE THIS FITS. Listings converted from HTML tables to fenced code; Tables 6.1/6.2 -> 6.5/6.6, Listings 6.1-6.4 -> 6.2/6.6/6.7/6.8. Code: `code_snippets/futures_trading/ch06_{symbols,risk,liquidity,margin_proof}.py` (selftests pass).

**Updated 2026-10-06** — Renumbered from Chapter 6 to Chapter 7 after Chapter 2 (Exchange Traded Products) was split into Chapter 2 (ETFs) and Chapter 3 (ETCs and ETNs). Section, subsection, table, figure and listing numbers, the header digit box, Prereqs and cross-chapter references updated; dated notes above keep the numbering of their time.

**Updated 2026-10-06 (b)** — Converted from a standalone reference chapter to a normal main-sequence chapter: standard running banner and "Chapter 7" digit box (the box still showed the pre-split number), Part I label and real Prereqs line, closing WHERE THIS FITS box replaced by WHAT'S NEXT pointing to the next chapter. Generator updated to match.

**Updated 2026-10-06 (c)** — Part label aligned with `.claude/CLAUDE.md` §3.3: Part I — Investing and Stock Market (Ch 1–9), Part II — Technical Analysis (Ch 10–15); "opens/closes Part …" sentences adjusted.

**Updated 2026-10-06 (e)** — Moved from Chapter 7 to Chapter 3, ahead of ETCs and ETNs. New §3.2 The Futures Curve — Carry, Contango, and Backwardation (cost of carry, contango/backwardation table, natural-gas case, moved and reworded from the ETC chapter); old §7.2–7.10 → §3.3–3.11; tables/listings renumbered in order. Code listings trimmed (9 → 7 listings, 173 → 85 lines): market_risk_ok merged into the sizing listing, Tradovate listing moved to code_snippets/futures_trading/tradovate_order_pattern.py, Databento full code to databento_history.py; each listing points to its full version. Prereqs Ch 1; summary bullet and five curve key terms added; WHAT'S NEXT → Ch 4 ETCs.

**Updated 2026-10-07 (c)** — §3.10 Advantages and §3.11 [PROOF] swapped so the PROOF closes the chapter (Tables 3.8/3.9 swapped to keep definition order); KEY INSIGHT added.

**Updated 2026-10-08 (a)** — §3.8 rewritten for USA and Europe (Brent moved to ICE Futures Europe; new §3.8.2 European venues, §3.8.3 same commodity two contracts; Figures 3.1–3.2 venue pies; Table 3.6 now venues + IB access). §3.9 reduced to Interactive Brokers only: Tradovate and Databento listings removed (files to code_snippets/_superseded_2026-10-08); new Listing 3.6 delayed quotes and daily bars for US and European contracts; Table 3.7 now market-data sources per venue. Summary bullet, key terms (Benchmark contract, Delayed market data replace GLBX.MDP3) and closing note updated.

**Updated 2026-10-08 (b)** — Table 3.7: `yfinance` added as the free daily front-month source for CME and ICE Futures US, with a note on its limits (continuous, unadjusted, US only, unofficial).

**Updated 2026-10-08 (c)** — §3.3 rewritten: 3.3.1 margin is a deposit not a loan; 3.3.2 where leverage comes from (Micro Gold notional $30,000 vs $1,650 initial, ~18:1); 3.3.3 daily mark-to-market, initial/maintenance, margin call back to initial; 3.3.4 who sets margin, margin hikes, clearing house guarantee; 3.3.5 effective leverage = notional / whole account, size by stop not margin.

**Updated 2026-10-08 (d)** — New Figure 3.1 (§3.3 leverage and margin in four steps, B&W, image Ch3_Futures_0_margin_leverage.png); venue pies renumbered to Figures 3.2–3.3.

**Updated 2026-10-08 (e)** — Listing 3.1 (parse_symbol/symbol_for) removed (file ch06_symbols.py kept, mentioned in the companion note); Listings 3.2–3.7 → 3.1–3.6. §3.2.3 natural-gas case replaced by a worked cocoa curve (6 Oct 2026, ICE US CC, M1–M6) with new Figure 3.1; margin figure → 3.2, venue pies → 3.3–3.4. Summary bullet updated.

**Updated 2026-10-08 (f)** — §3.2.3 visual split in two: Figure 3.1 cocoa curve now carries ①–③ zone markers matching the three points; new Figure 3.2 (roll cost three ways: −2.13% / ≈ −8.3% / −12.11%) after point 3. Margin figure → 3.3, venue pies → 3.4–3.5.

**Updated 2026-10-08 (g)** — §3.10 Advantages (Table 3.8) removed; §3.11 [PROOF] → §3.10, Table 3.9 → 3.8, all refs. Margin figure split into four, each after its subsection: Fig 3.3 deposit (3.3.2), 3.4 margin calls (3.3.3), 3.5 margin layers (3.3.4), 3.6 effective leverage (3.3.5); venue pies → 3.7–3.8.

**Updated 2026-10-08 (h)** — §3.7 The Psychology of Losses removed; §3.8–3.10 → §3.7–3.9 (headings, subsections, TOC, cross-references).

**Updated 2026-10-08 (reorder)** — Part I reordered: Stocks 5→2, Bonds+Intermarket 6→3, ETFs 2→4, Futures 3→5, ETCs/ETNs 4→6. Chapter, section, table, figure and listing numbers and all cross-references remapped; WHAT'S NEXT chain and Prereqs adjusted.
