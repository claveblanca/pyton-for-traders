|                                                               |
| ------------------------------------------------------------- |
| **PYTHON FOR TRADERS: INVESTING, DERIVATIVES, AND TECHNICAL ANALYSIS APPLIED** |

|                    |       |
| ------------------ | ----- |
| Chapter 3          | **3** |

**Bonds and the Intermarket Chain: Screening Fixed Income, Reading Cross-Asset Signals**

*How to judge a bond twice — as a promise (price, coupon structure, a seven-point risk map and a score) and as a link in the chain that ties currencies, commodities, bonds, and stocks together (lead-lag, relative-strength ratios, the inflation regime, and the stock–bond correlation that sets how much duration to hold)*

Part I — Investing and Stock Market · Prereqs: Chapter 1 (Investment Classes and Instruments), Chapter 2 (Investing in Stocks) · Companion files: `bond_data_endpoints.py`, `code_snippets/intermarket/`

<table>
<thead>
<tr class="header">
<th><strong>THIS CHAPTER COVERS</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>3.1 The Bond Investor's Frame, in Two Sentences</p>
<p>3.2 Bond Mechanics — Clean Price, Dirty Price, and Coupon Structures</p>
<p>3.3 Seven Things to Flag Before Buying — a Risk Map</p>
<p>3.4 From Risk Map to a Score — the weighted, partial-credit methodology</p>
<p>3.5 The Intermarket Chain — Bonds, Stocks, and Commodities</p>
<p>3.6 The Dollar, Commodities, and Gold</p>
<p>3.7 Sector and Industry Links to Rates and Oil</p>
<p>3.8 Relative Strength and the Top-Down Approach</p>
<p>3.9 Disinflation vs. Deflation — Reading the Regime</p>
<p>3.10 Do Bonds Still Hedge Stocks? The Stock–Bond Correlation</p>
<p>3.11 Three Rules for Positioning a Bond Portfolio</p>
<p>3.12 [CODE] Hands-On — Macro and Intermarket Data</p>
<p>3.13 [PROOF] Case Study — Reading the Correlation and Investing €20,000</p></td>
</tr>
</tbody>
</table>

|                                    |
| ---------------------------------- |
| **3.1 THE BOND INVESTOR'S FRAME, IN TWO SENTENCES** |

Every equity strategy in this book is ultimately a bet on growth. Buying a bond is a bet on being paid back — on a fixed schedule, at a fixed price, by a specific date — which is why the right first question is "how confident am I in that schedule?", not "how much upside is here?" That reframing is the whole of the philosophy this chapter needs from the source material; everything that follows is about how to test it with numbers rather than a prospectus read alone.

| **◆ EDGE — A bond is a promise with a due date**                                                                                                                                                                                                                                            |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A stock's return is open-ended in both directions. A bond's return is capped by design — the best case is getting exactly what was promised, on time. Every indicator in this chapter exists to answer one question: how much confidence can I have that the promise is kept in full, and that I'm not overpaying for that promise today? |

|                                    |
| ---------------------------------- |
| **3.2 BOND MECHANICS — CLEAN PRICE, DIRTY PRICE, AND COUPON STRUCTURES** |

**3.2.1 What a bond is.** A bond is a debt security issued by a company (corporate bond) or a state (government bond). The buyer becomes a creditor of the issuer, with a contractual right to periodic interest (the coupon) and repayment of capital at maturity, usually at a face value of 100. Unlike equity, the coupon flow and redemption value are fixed at issuance, not left to the market's opinion of future cash flows.

**3.2.2 Clean price vs. dirty price.** The secondary market quotes the **clean price** — the capital's market value only, and the number shown in trading books and financial press. What actually settles is the **dirty price** ("tel quel"): the clean price plus the **accrued coupon**, the portion of interest earned since the last coupon date.

$$\text{Dirty Price} = \text{Clean Price} + \text{Accrued Coupon}$$

**3.2.3 The coupon-structure taxonomy.** Six structures cover most of what a retail investor will encounter:

*Table 3.1 — Coupon structures and their defining mechanic*

| **Structure** | **Coupon mechanic** | **Example** |
| --- | --- | --- |
| Fixed rate | Predetermined, constant for the bond's life | US Treasury note / bond |
| Step-up / step-down | Fixed, but on a rising/falling schedule set at issuance | — |
| Floating rate | Reference rate (e.g. 3M/6M Euribor) + spread | US Treasury FRN |
| Zero coupon | No periodic coupon; return = discount-to-100 at issuance | T-bill, Treasury STRIPS |
| Reverse floater | Coupon = Fixed Parameter − Euribor; high price sensitivity | — |
| Inflation-linked | Real coupon revalued by an inflation index | TIPS, euro-area inflation-linked govvies |

Three further structured variants worth knowing by name: **fix floater** (fixed rate that converts to floating after a set date), **convertible** (option to convert the credit into issuer equity), and **amortizing** (principal repaid progressively alongside coupons, rather than in one bullet at maturity). Figure 3.1 draws the three most common structures as the cash a holder receives each year from a 10-year bond with a face value of 100.

![Cash flows of a fixed-rate, a floating-rate and a zero-coupon 10-year bond](../images/Bonds_1_coupon_structures.png)

*Figure 3.1 — Three coupon structures, one repayment at maturity. Fixed: 5 every year, known in advance. Floating: the coupon is reset each year to Euribor plus a spread, so its size is unknown until each fixing (heights illustrative). Zero coupon: nothing until maturity. All three repay 100 in one bullet at the end.*

Read the three panels as three answers to one question: what do I receive before maturity? The fixed-rate holder knows every payment on the day of purchase. The floating-rate holder knows only the formula: when rates rise the coupons grow, when they fall the coupons shrink — which is why a floater's price stays close to 100 while its income moves. The zero-coupon holder receives nothing until the end, so the whole return depends on the issuer still being able to pay on that one date, and there are no coupons to reinvest along the way (risk 6 of Table 3.2). In every case most of the money arrives on the last day, which is why the credit check of Section 3.3 comes before anything else.

**3.2.4 Effective yield: what you earn depends on what you pay.** The charts above show only what the bond pays. An investor's cash flows start one step earlier, with the money paid to buy it. Figure 3.2 adds that step for the fixed-rate bond: −100 on the purchase date, +5 a year for nine years, +105 at maturity.

![Investor cash flows of a 10-year 5% bond bought at 100, with the effective yield at prices of 95, 100 and 105](../images/Bonds_2_investor_cash_flows.png)

*Figure 3.2 — Pay first, then collect. The effective yield is the single rate at which the inflows exactly repay the price paid: 5.67% at 95 (with a 5-point gain at maturity), 5.00% at 100, 4.37% at 105 (with a 5-point loss).*

The **effective yield** (the internal rate of return of this schedule, computed in a spreadsheet with `XIRR` or in Python with a root-finder) is the one discount rate at which the present value of all the inflows equals the outflow. Bought at 100, the bond yields exactly its 5% coupon. Bought at 95, the investor collects the same coupons plus a 5-point gain at maturity, and the yield rises to 5.67%; bought at 105, the 5-point loss at maturity pulls it down to 4.37%. The coupon is the issuer's promise; the effective yield is what the buyer actually earns, and it is set by the price paid on day 0 — the dirty price of Section 3.2.2, accrued coupon included. Compare bonds on effective yield, never on coupon.

|                                    |
| ---------------------------------- |
| **3.3 SEVEN THINGS TO FLAG BEFORE BUYING — A RISK MAP** |

Bond selection collapses to seven measurable checks. Each one exists to catch a specific way a bond's promised return can quietly fail to materialize before a default is ever declared.

*Table 3.2 — The seven checks, what they measure, and what each one catches*

| **#** | **Check** | **What it measures** | **What it catches** |
| --- | --- | --- | --- |
| 1 | Credit / default safety | Issuer rating tier, or a credit-spread proxy (OAS) when no rating is on hand | Issuer unable to pay coupons or principal — the most direct threat to the whole promise |
| 2 | Duration / price-risk fit | Modified duration vs. the investor's actual holding horizon | A rate shock forcing a loss if the bond must be sold before maturity |
| 3 | Structural clause risk | Presence of Call, Cap, or Tarn clauses in the prospectus | Upside capped or principal returned early, right when reinvestment rates are worst |
| 4 | Liquidity | Regulated-market listing (MOT/TLX) + average daily volume | Inability to exit before maturity without a material price concession |
| 5 | Inflation-protection fit | Whether the coupon structure is real (inflation-linked) vs. nominal, checked against the current inflation regime | Purchasing power erosion when nominal coupons are held through a high-inflation period |
| 6 | Reinvestment exposure | Share of total return delivered as periodic coupons vs. as a single redemption (zero-coupon) | The need to reinvest coupon cash at rates that may be lower than today's |
| 7 | Subordination tier | Position in the bail-in loss-absorption hierarchy — senior/government vs. Tier I/II/III | Where the bond sits in line if the issuer enters resolution, independent of a headline coupon or rating |

**3.3.1 The clause check, expanded.** A **Call option** lets the issuer redeem at 100 early if rates fall, cutting off exactly the higher coupons that made the bond attractive. A **Cap** limits how high a floating coupon can go; a **Tarn** caps the cumulative sum of all coupons ever paid and redeems the bond early once that ceiling is hit. **CACs** (Collective Action Clauses), standard on Eurozone sovereign debt issued since 2013 with maturities over 12 months, allow a restructuring — extended maturities or cut coupons — with 75% creditor consent; they're a feature of the instrument class, not a red flag on any one issue, but worth knowing is there.

**3.3.2 The subordination hierarchy.** Under the EU Bail-in directive (in force since 1 January 2016), a banking-crisis loss is absorbed internally in this order:

$$\text{Shareholders} \longrightarrow \text{Subordinated Bondholders} \longrightarrow \text{Senior Bondholders} \longrightarrow \text{Depositors (>€100,000)}$$

Within "subordinated," four tiers run from highest to lowest risk: **Tier I (Perpetual)** — effectively equity-like; **Upper Tier II** — coupons suspendable on operating losses; **Lower Tier II** — coupon guaranteed, principal still at risk on insolvency; **Tier III** — short-term subordination. Operating rule: keep subordinated exposure to a hard cap (5% of the fixed-income portfolio is the source material's figure) and restrict it to the strongest issuers only.

|                                    |
| ---------------------------------- |
| **3.4 FROM RISK MAP TO A SCORE**  |

A pure pass/fail screen throws away information: a bond whose modified duration overshoots the investor's horizon by three months is treated identically to one that overshoots by seven years. The scoring methodology below fixes that with a three-layer approach: weighted rules, partial credit near each threshold, and a penalty for missing data.

**3.4.1 Layer one — binary rules, weighted by importance.**

*Table 3.3 — Rule weights (sum to 100)*

| **Rule** | **Weight** | **Rationale for the weight** |
| --- | --- | --- |
| Credit / default safety | 20 | The most direct test — a failure here threatens both coupons and principal |
| Duration fits the holding horizon | 15 | Determines whether a rate shock can force a loss on an early sale |
| No adverse structural clauses | 15 | Protects the yield actually being screened for from being called or capped away |
| Liquidity (regulated market + volume) | 15 | Determines whether the position can be exited without a haircut |
| Inflation protection matches the regime | 15 | Determines whether real return is protected when it's actually needed |
| Reinvestment exposure is laddered or zero-coupon | 10 | A secondary signal — reinforces the other six rather than standing alone |
| Senior or government-tier subordination | 10 | A capital-structure-seniority bonus, not a requirement for a passing score |

**3.4.2 Layer two — partial credit near the threshold.** A bond that misses a sliding-scale rule by a small margin isn't scored identically to one that misses it badly — a duration of 6.2 years against a 6-year horizon recovers most of that rule's partial credit; a duration of 15 years recovers none of it. Liquidity and inflation-fit follow the same sliding-scale logic.

**3.4.3 Layer three — a penalty for missing data.** If any of three essential fields — credit-spread proxy, modified duration, or effective yield — comes back unavailable (a data gap, not a computed zero), the final score is discounted 15% per missing field. A high score built on incomplete data is explicitly worth less than the same score built on a complete one.

The result is a single number in `[0, 100]` — comparable across candidates, and honest about both near-misses and data gaps in a way a bare pass/fail list is not.

|                                                        |
| -------------------------------------------------------- |
| **3.5 THE INTERMARKET CHAIN — BONDS, STOCKS, AND COMMODITIES** |

The core principle here: all financial markets are interlinked and interdependent. Movements in one market ripple through others across national and global boundaries — which means a market studied entirely in isolation is being read with less information than is actually available.

**3.5.1 The four major asset classes.** Currencies (led by the U.S. Dollar), commodities (energy, metals, agriculture), bonds (Treasury yields / interest rates), and stocks (equities and stock market sectors) form the full chain this chapter works through link by link.

**3.5.2 Why this matters beyond single-market technical analysis.** Traditional technical analysis often looks at one market at a time. Intermarket analysis provides a broader framework that explains market sequence and sector rotation based on the flow of capital across these four asset classes — it is a lens for *why* a single-market signal is firing, not a replacement for single-market analysis.

| **◆ EDGE — Intermarket analysis explains sequence, not just direction**                                                                                                                                                                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Knowing that bonds and stocks usually move together is less useful than knowing which one typically moves first. The value of this chapter's chain of relationships is largely in the leads and lags between links — a bond market turn that historically precedes a stock market turn is actionable in a way that a same-day correlation is not. |

**3.5.3 Bonds and stocks — the normal relationship.** Bond prices and stock prices typically move in the same direction. Rising bond prices (falling interest rates/yields) lower borrowing costs and stimulate economic growth, which benefits equity prices.

**3.5.4 Bonds lead stocks.** Bond market turns frequently precede stock market turns. Major bond-market bottoms in 1981, 1984, 1988, 1991, and 1995 preceded stock bull runs; bond-market tops in 1987, 1990, and 1994 warned of equity headwinds ahead of time. The lead-lag relationship, not just the co-movement, is the actionable part.

**3.5.5 Bonds and commodities — the inverse relationship.** Bond prices and commodity prices move in opposite directions, because commodities function as a leading indicator of inflation. Rising commodity prices signal accelerating inflationary pressure, which drives bond yields higher and bond prices lower; falling commodity prices signal disinflation or economic cooling, which supports bond prices.

*Table 3.4 — The core three-way chain*

| **Link**                    | **Relationship** | **Mechanism**                                                       |
| ------------------------------ | ------------------- | -------------------------------------------------------------------- |
| Bonds → Stocks                   | Same direction, bonds lead | Falling yields lower borrowing costs, stimulating equities             |
| Commodities → Bonds                | Opposite direction        | Rising commodities signal inflation, pushing yields up and bond prices down |

**3.5.6 When the bonds→stocks link decouples.** The 3.5.3 relationship assumes a rate move is growth-driven — falling yields because growth is slowing, easing borrowing costs and supporting equity valuations. During a policy-tightening cycle driven by inflation control rather than growth, the mechanism runs differently: yields rise because policy is tightening, and *both* bonds and stocks can fall together, since rising real rates pressure equity valuations at the same time they pressure bond prices. This is not a failure of the link so much as a different regime feeding it — Section 3.9 formalizes the distinction with a third row added to Table 3.7. Before reading a bonds-stocks correlation as confirming or denying 3.5.3, check which regime is in force. Section 3.10.1's stock–bond dashboard is the live bond-side read of this link.

|                                              |
| ------------------------------------------------ |
| **3.6 THE DOLLAR, COMMODITIES, AND GOLD** |

**3.6.1 Dollar and commodities — the inverse relationship.** A strengthening U.S. Dollar depresses commodity prices denominated in dollars, and exerts a broadly non-inflationary effect on the domestic economy as a result.

**3.6.2 Gold as the key link.** The U.S. Dollar and gold prices trend in opposite directions, and because gold acts as a leading indicator for the broader commodity spectrum (tracked via indices such as the CRB Index), tracking currency strength provides an early read on both inflation direction and the likely direction of commodities generally — gold is treated here as a leading proxy for the whole commodity link in the chain, not just one commodity among many.

**3.6.3 A modern exception worth watching.** The dollar-gold inverse relationship in 3.6.2 held reliably for decades, but gold has at times decoupled from it for extended stretches — rallying alongside a flat-to-strong dollar rather than against it. The usual drivers cited are sustained central-bank gold buying and de-dollarization flows, which add a demand source for gold that has nothing to do with the U.S. currency's direction. This does not invalidate 3.6.2 as the default read; it means a dollar-gold correlation check (Section 3.12's Dollar-Gold-Commodity Panel) should be read alongside the correlation's own strength, not assumed from the historical relationship alone.

|                                                          |
| ------------------------------------------------------------ |
| **3.7 SECTOR AND INDUSTRY LINKS TO RATES AND OIL** |

The intermarket chain does not stop at the index level — specific stock sectors are structurally tied to specific links in the chain, which means a sector can be read as an early proxy for a macro move before that move shows up in the broad averages. Table 3.5 uses futures prices — the exchange-traded price for delivery of a commodity or bond at a later date (Chapter 5) — simply as the market's quote for oil and long-dated Treasuries.

*Table 3.5 — Sector links to the intermarket chain*

| **Sector**              | **Linked to**            | **Relationship**                                                     |
| -------------------------- | ---------------------------- | -------------------------------------------------------------------------- |
| Utilities                   | Treasury Bond futures            | Highly rate-sensitive; utility stocks often lead bond market turning points |
| Gold mining shares            | Physical gold prices             | Directly linked; often lead gold price moves                               |
| Energy                        | Crude oil futures                | Rising oil benefits energy equities                                       |
| Airlines                      | Crude oil futures                | Rising oil harms airline stocks (opposite of energy)                       |

**3.7.1 A caveat on the airlines/oil example.** Of the four pairs in Table 3.5, this is the noisiest to verify in practice: airlines routinely hedge a portion of forward fuel costs, which weakens and delays the inverse relationship relative to the energy/oil pair directly above it (a purely mechanical link with no comparable hedging offset). Treat gold miners/gold and energy/oil as the cleaner teaching examples for this table, and airlines/oil as a real but noisier illustration rather than a reliable screening signal on its own.

**3.7.2 Large caps vs. small caps and the dollar.** A strong dollar often favors large-cap multinational companies (whose overseas earnings translate differently) whereas domestic small-cap stocks — the Russell 2000 being the standard proxy — respond differently to currency fluctuations, since their revenue base is more domestically concentrated.

|                                                        |
| ------------------------------------------------------- |
| **3.8 RELATIVE STRENGTH AND THE TOP-DOWN APPROACH** |

**3.8.1 The ratio method.** Divide the price of one asset or market by another — for example, the CRB Index divided by Treasury Bond futures — to produce a single ratio line whose direction reveals which side of the pair is actually outperforming, independent of either asset's absolute price level.

**3.8.2 Interpreting the ratio line.** A rising ratio line means the numerator is outperforming the denominator, favoring inflation-sensitive assets/commodities. A falling ratio line means the denominator is outperforming the numerator, favoring interest-rate-sensitive assets/bonds.

**3.8.3 Application to equity rotation.** When the CRB/Bond ratio falls, capital rotates out of cyclical and commodity-linked stocks and into defensive groups — utilities, financial services, consumer staples — giving a macro ratio a direct, tradeable equity-sector implication.

**3.8.4 The top-down approach — market, sector, stock.** The ratio method of Sections 3.8.1–3.8.3 generalizes into a three-step selection process that starts at the macro level and narrows down to an individual position.

*Table 3.6 — The three-step top-down approach*

| **Step**             | **What it determines**                                        | **Method**                                                          |
| ----------------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| 1. Overall market          | Broad market direction                                                | Read stock market averages — S&P 500, Dow Jones, Nasdaq                    |
| 2. Sector selection         | Which sectors have rising relative strength                            | Divide sector indices (e.g. High Tech, Oil, Utilities) by the S&P 500 benchmark |
| 3. Stock selection           | Which individual stocks are outperforming within a chosen sector       | Divide each stock's price by its sector index; avoid falling ratio lines    |

**3.8.5 Why the order matters.** Selecting a strong individual stock inside a weak sector, or a strong sector inside a weak broad market, means fighting the two larger currents this method exists to identify. The top-down order is not a stylistic preference — each step's ratio is only informative in the context the step above it establishes.

|                                                               |
| ------------------------------------------------------------- |
| **3.9 DISINFLATION VS. DEFLATION — READING THE REGIME** |

Two economic environments produce superficially similar falling-commodity-price conditions, but with opposite implications for stocks — distinguishing between them is where the chain from Sections 3.5–3.6 pays off in practice.

*Table 3.7 — Disinflation vs. deflation*

| **Regime**       | **Commodities** | **Bonds** | **Stocks**                                          |
| -------------------- | -------------------- | ------------ | ----------------------------------------------------------- |
| Disinflation            | Fall                    | Rise            | Rise (beneficial for traditional financial assets)              |
| Deflation                | Collapse                | Rise            | Fall — decouples from bonds due to corporate earnings collapse and economic contraction |
| Reflation-by-tightening  | Mixed to falling         | Fall (yields rise) | Pressured initially; outcome then splits on earnings resilience rather than following bonds |

**3.9.1 Why the same bond move can accompany opposite stock outcomes.** In disinflation, falling commodity prices without a broader collapse allow bonds and stocks to rise together, following the normal 3.5.3 relationship. In deflation, the commodity collapse is severe enough to signal outright economic contraction — bonds still rise on falling rates, but stocks decouple and fall because corporate earnings themselves are collapsing. The bond/commodity leg of the chain looks similar in both cases; the magnitude of the commodity move is what tells the two regimes apart.

**3.9.2 A third regime: reflation-by-tightening.** Disinflation and deflation both share one condition Table 3.7's original two rows take for granted — bonds rising, i.e. yields falling. That condition does not hold during a sustained policy-tightening cycle aimed at fighting inflation: yields rise by design, so bond prices fall instead of rising, and the 3.5.3 co-movement described in 3.5.6 can break down as both bonds and stocks come under pressure from the same rising-rate driver. Commodities in this regime tend to be mixed rather than cleanly falling, since the tightening itself is often a policy response to commodity-driven inflation rather than a symptom of collapsing demand. This regime does not fit cleanly into either of Table 3.7's original two rows and is worth checking for explicitly — via a rolling bond-return sign check, as in the accompanying Regime Classifier script — before applying Table 3.7's original two-way read to a rising-rate market. On the bond side, the 90-day stock–bond correlation of Section 3.10.1 is the quickest live read of which regime is in force, and Rule A of Section 3.11 turns that read into a duration decision.

**3.9.3 Ten years of euro-area prices, four regimes.** Table 3.7 classifies a regime by what commodities, bonds and stocks do. A consumer-price index shows the other side of the same story — the inflation those markets are reacting to — and its shape makes the regimes visible on a single line. Figure 3.3 plots the euro-area harmonised index of consumer prices (HICP, 2015 = 100) from 2016 to September 2026. The line is the price level; its slope is the inflation rate.

![Euro-area HICP index 2016–2026 with four shaded regimes: low stable inflation, a 2020 deflation scare, reflation-by-tightening 2021–2023, disinflation since late 2023](../images/Bonds_0_hicp_regimes.png)

*Figure 3.3 — Ten years of euro-area prices, four regimes. The September 2026 reading is 129.56 (annual rate 1.90%); earlier points are approximate. The black bar marks the ECB's rate hikes, July 2022 to September 2023.*

Table 3.8 reads the four periods: what the index does, and what the markets did at the same time.

*Table 3.8 — Reading the regimes on the price index*

| **Period** | **What the index does** | **Regime** | **What the markets did** |
| --- | --- | --- | --- |
| ① 2016–2019 | Rises slowly, about 1% a year | Low, stable inflation | Growth shocks dominate; Treasuries hedge stocks (Section 3.10) |
| ② 2020 | Flattens and dips; annual inflation briefly below zero late in the year | Deflation scare | Commodities collapse, bonds rise, stocks crash — then recover quickly, so no lasting deflation |
| ③ 2021–2023 | Steepest climb; euro-area inflation peaks above 10% in late 2022 | Reflation-by-tightening (Section 3.9.2) | The ECB raises rates from July 2022 to September 2023; yields rise, and bonds and stocks fall together |
| ④ Late 2023–2026 | Still rising, but more slowly — about 1.9% a year | Disinflation | Commodities ease; the benign row of Table 3.7 for bonds and stocks |

The key distinction is in the slope, not the level. **Disinflation is not deflation:** in period ④ prices still rise, only more slowly, so the line flattens but keeps climbing. Deflation means the line turns down — on ten years of this chart that happens only briefly, in 2020. Read the index with care, though: it shows the inflation side only. Before naming a regime, check the market legs of Table 3.7 — in 2020 a deflation scare came with a stock crash and a fast recovery, not the lasting decoupling of true deflation.

|                                    |
| ---------------------------------- |
| **3.10 DO BONDS STILL HEDGE STOCKS? THE STOCK–BOND CORRELATION** |

Sections 3.3 and 3.4 judge one bond at a time. Before choosing bonds, one market-level question decides how much long duration a portfolio should hold: on the days stocks fall, do Treasuries rise? The answer changes with the regime, so it has to be measured rather than assumed. Bond positioning moves slowly, so the reading is checked monthly, not daily.

**3.10.1 What the dashboard measures.** Figure 3.4 rebases the S&P 500 and a long-dated Treasury ETF (TLT — an exchange-traded fund that holds US Treasury bonds and trades like a share; Chapter 4) to 100 on 30 July 2002, and plots underneath the rolling correlation of their daily returns over 30, 60 and 90 days. A correlation of −1 means that on the days stocks fall, bonds rise; 0 means no link; +1 means both rise and fall on the same days. The top panel shows what each asset has paid over the long run — the S&P 500 about +753%, TLT about +123% since 2002 — and also how a shared linear axis misleads: next to the S&P 500, the Treasury line looks motionless. The correlation panel is the one to read.

![Stock vs Bond dashboard — S&P 500 vs TLT indexed to 100, with rolling 30/60/90-day correlation](../images/StockBond_dashboard_2026-10.png)

*Figure 3.4 — Stock vs Bond dashboard, 1-year range, September 2026. Top: S&P 500 and TLT rebased to 100 on 2002-07-30. Bottom: rolling correlation of daily returns, 30-day, 60-day and 90-day, with the zero line dotted.*

**3.10.2 Reading the regime.** Table 3.9 turns the 90-day line into three regimes.

*Table 3.9 — Reading the stock–bond correlation (90-day line)*

| **Correlation** | **Regime** | **What it means for a bond investor** |
| --- | --- | --- |
| Below 0 | Bonds hedge stocks | Long bonds tend to rise when stocks fall, so long duration works as portfolio insurance |
| 0 to +0.2 | Neutral | Bonds diversify, but will not protect the portfolio in a selloff |
| Above +0.2 | Stocks and bonds move together | Usually driven by inflation or rates; both can fall at once, so long duration adds risk instead of reducing it |

The 90-day line sets the regime. The 30-day line gives earlier warnings, but also false ones — in March 2026 it dipped to about −0.35 and went straight back up. In September 2026 the 90-day line stands at +0.44 and the 30-day at +0.50: stocks and long Treasuries are rising and falling on the same days. Figure 3.5 places that reading on the scale and shows how it got there — negative until January 2026, through zero in February, above +0.2 from April.

![The stock–bond correlation regime: today's readings on the scale, and the 90-day line over the last year](../images/Bonds_3_correlation_regime.png)

*Figure 3.5 — Today's regime and how it got there. Top: the 90-day (+0.44) and 30-day (+0.50) readings on the scale of Table 3.9. Bottom: monthly path of the 90-day line, October 2025 to September 2026, read from Figure 3.4 (approximate).*

**3.10.3 Why the sign flips.** A bond's price falls when interest rates rise; a stock's price is the value today of the profits expected in future. Two kinds of news move both, and whichever dominates sets the sign of the correlation (Table 3.10).

*Table 3.10 — Which shock is driving the market*

| **Shock** | **Stocks** | **Treasury yields** | **Treasury prices** | **Correlation** |
| --- | --- | --- | --- | --- |
| Growth scare — recession fears, a crisis | Fall: profits expected lower | Fall: flight to safety, rate cuts expected | Rise | Negative — bonds hedge |
| Inflation or rate scare — inflation, central-bank hikes | Fall: higher rates shrink the value of future profits | Rise | Fall | Positive — no hedge |

When inflation is low and stable, most shocks are growth shocks and the correlation is negative — roughly the 2000–2021 period, when a stock-and-bond portfolio was well protected. When inflation becomes the main worry, the second row takes over: in 2022 the S&P 500 lost about 19% and TLT about 30% in the same year. With the US 10-year yield at 5.11% in September 2026, above its October 2023 peak, today's positive reading belongs to the second row.

**3.10.4 Trend and daily moves are different questions.** Section 3.5.3 says that bond and stock prices typically move in the same direction, and Section 3.5.4 that bonds lead stocks. Both describe trends over months: falling yields lower borrowing costs, and a bond rally tends to come before a stock rally. The correlation measures something else — whether the two move in opposite directions on the same days, which is what decides whether bonds protect a portfolio in a sell-off. Two assets can trend up together for years, as the top panel of Figure 3.4 shows, and still hedge each other day to day — or not. Section 3.5.6 covers the case where even the trend link breaks because rates are moving for inflation reasons, and Section 3.9 which macro regime each sign usually belongs to.

**3.10.5 What to do with the reading.** Below 0, long fixed-rate bonds work as portfolio insurance and more duration is justified. Above +0.2, as now, long duration adds risk instead of reducing it: keep it small, prefer short maturities and floating-rate bonds, and look for protection elsewhere — cash, a short ladder, inflation-linked bonds. Between the two, bonds diversify but will not protect the portfolio in a sell-off. Decide on the 1-year view of the 90-day line, check it against the long view (All, 10 years), and re-check monthly: the regime changes over quarters, not days.

|                                    |
| ---------------------------------- |
| **3.11 THREE RULES FOR POSITIONING A BOND PORTFOLIO** |

The correlation reading and two holding rules make three rules. The first sets how much duration to hold and which kinds of bond to favour; the other two govern how the fixed-rate part is held.

*Table 3.11 — From correlation reading to portfolio action*

| **Rule** | **Signal** | **Action** |
| --- | --- | --- |
| A. Regime first | 90-day stock–bond correlation below 0 | Long fixed-rate bonds (7–10 years and more) work as a hedge; more duration is justified |
| | 90-day correlation above +0.2 | Keep long duration small; favour floaters, short maturities and inflation-linked bonds |
| B. Ladder the fixed part | — | Split fixed-rate capital into equal slices maturing one year apart; reinvest each maturing slice at the far end |
| C. Hold to maturity | Correlation regime unchanged | A bond held to maturity repays its full notional whatever its price does in between; rebalance only when the regime changes |


| **◆ EDGE — The correlation chooses the mix; the risk map chooses the bond** |
| ------------------------------------------------------------------------- |
| Rule A decides *what kind* of bond to buy — short or long, fixed or floating. It says nothing about *which* bond. Once the mix is set, every candidate within it still goes through the seven checks of Section 3.3 and the score of Section 3.4: a floater with a Cap clause, or an inflation-linked bond from a subordinated issuer, fails there however well it fits the regime. |

|                                                                     |
| ------------------------------------------------------------------- |
| **3.12 [CODE] HANDS-ON — MACRO AND INTERMARKET DATA** |

**3.12.1 Why this section exists.** Sections 3.5–3.9 read the chain conceptually, and Section 3.10 reads the stock–bond correlation. Building either in Python — the ratio of Section 3.8, the lead-lag check of Section 3.5, the regime read of Section 3.9 — needs Treasury yields, a dollar index, and commodity and sector series that the equity-focused providers used elsewhere in this book do not cover well on their own. `bond_data_endpoints.py` covers the euro rates (€STR, Euribor) and inflation series used in Section 3.13; this section adds the cross-asset series. Full provider setup (keys, rate limits, error handling) lives in `code_snippets/ch01/free_paid_data_sources.md`.

**3.12.2 FRED — Treasury yields, oil, and the dollar.** The Federal Reserve's FRED database is the free, official source for U.S. yields and the commodity and dollar series that have no clean equity-style ticker.

**💻 PYTHON · Listing 3.1 — FRED series for the intermarket chain**

```python
import os
from fredapi import Fred                                   # pip install fredapi

fred = Fred(api_key=os.environ["FRED_API_KEY"])            # free key: fred.stlouisfed.org
SERIES = {"y10": "DGS10", "y2": "DGS2",                    # Treasury yields (Section 3.5)
          "wti": "DCOILWTICO", "dollar": "DTWEXBGS",       # oil, broad dollar (Section 3.6)
          "ppi_commodities": "PPIACO"}                     # commodity price level (Section 3.9)
macro = {name: fred.get_series(code) for name, code in SERIES.items()}
```

**3.12.3 yfinance — the market legs of the chain.** The bond leg of the ratio method, gold, the dollar index, and every sector proxy in Table 3.5 are ordinary yfinance tickers.

**💻 PYTHON · Listing 3.2 — Market tickers for the bond, dollar, gold, and sector legs**

```python
import yfinance as yf

TICKERS = {"bond_10y_fut": "ZN=F", "dollar_index": "DX-Y.NYB", "gold": "GC=F",
           "utilities": "XLU", "gold_miners": "GDX", "energy": "XLE",
           "airlines": "JETS", "small_caps": "^RUT", "commodities": "DBC"}
data = yf.download(list(TICKERS.values()), period="5y", auto_adjust=True,
                   progress=False)["Close"]
```

Full version, with the long-bond future and the S&P 500 legs: `code_snippets/intermarket/core_chain_monitor.py`.

| **⚠ WARNING — `^TNX` and `^TYX` are yields, not prices** |
| -------------------------------------------------------- |
| `^TNX` and `^TYX` are yield-index quotes (already ×10 — 45.0 means 4.50%), not bond prices. Fed into the ratio method of Section 3.8 as if they were a price series they silently produce a meaningless ratio. Use `ZN=F` / `ZB=F`, or a bond ETF such as `TLT` or `IEF`, for the bond leg of any ratio. |

**3.12.4 The CRB Index has no free API — and the ratio built without it.** Sections 3.6, 3.8, and Table 3.7 lean on "the CRB Index" as the broad-commodity benchmark. Its modern successor, the FTSE/CoreCommodity CRB Index, is proprietary; free access is limited to delayed charts. Three free substitutes cover the same ground: the DBC commodity ETF (used below), FRED's PPIACO price-level index (fetched in Listing 3.1), or a self-built equal-weighted basket of gold, oil, copper, and corn when an example needs the CRB's multi-sector spread.

**💻 PYTHON · Listing 3.3 — The commodity/bond ratio of Section 3.8, with a free CRB substitute**

```python
ratio = data["DBC"] / data["ZN=F"]                 # commodities / Treasury note future
ratio_ma = ratio.rolling(50).mean()                # smoothed trend line (Section 3.8.2)
# ratio_ma rising -> commodities outperform -> cyclical stocks (Section 3.8.3);
# falling -> bonds outperform -> defensives.
```

Full version, as a multi-pair ratio board: `code_snippets/intermarket/relative_strength_ratio_board.py`.

**3.12.5 Stooq — a free backup source.** Stooq needs no key and serves as the second source when cross-checking a data point before trusting a multi-year pull: `pd.read_csv(f"https://stooq.com/q/d/l/?s={symbol}&i=d")` returns daily OHLC for symbols such as `xauusd` (gold) or `cl.f` (WTI).

| **▣ DATA — Three checks before trusting a series** |
| -------------------------------------------------- |
| Before using any series from this section: (a) resample every leg of the chain to the same daily frequency; (b) never let a yield series (`^TNX`, `^TYX`, FRED's `DGSxx`) stand in for a price in a ratio; (c) cross-check one recent data point against a second source (FRED, yfinance, Stooq) before pulling years of history. `code_snippets/intermarket/data_integrity_checks.py` runs all three on a fetched DataFrame. |

|                                    |
| ---------------------------------- |
| **3.13 [PROOF] CASE STUDY — READING THE CORRELATION AND INVESTING €20,000** |

**3.13.1 The reading (snapshot 2026-09-23).** Three numbers set the allocation:

- **Correlation is positive.** 30-day 0.50, 60-day 0.44, 90-day 0.44. It was negative until early 2026, crossed zero in February and has been above +0.2 since April (Figure 3.5). Bonds are not currently hedging stocks (rule A).
- **The US 10-year yield is 5.11%,** above its October 2023 peak — the inflation-and-rates regime of Table 3.10, consistent with the positive correlation.
- **Cash pays 2.44%.** €STR, the euro overnight rate, stepped up twice in 2026 from about 1.93%; 6-month Euribor, the reference rate for euro floaters, is 2.713% (fixing of 2026-08-01). Both come from the ECB series of Section 3.12.

Together they describe a "short and floating" environment: earn close to cash-plus from floaters and a short ladder, and hold only a small long-duration position until the correlation turns negative.

**3.13.2 The allocation.** Table 3.12 turns that reading into a €20,000 portfolio. The spread and the fixed-bond yields are illustrative assumptions chosen to show the arithmetic, not quotes; the market rates come from the reading above. All figures are gross — tax on interest depends on the investor's country of residence and on the issuer.

*Table 3.12 — A €20,000 bond allocation for the 2026-09-23 reading*

| **Slice** | **Amount** | **Instrument (assumed terms)** | **Rule** |
| --- | --- | --- | --- |
| Floating | €12,000 | Euro government floater, 6-month Euribor + 0.80% | A — correlation above +0.2: favour floaters |
| Short ladder | €6,000 | Three fixed-rate bonds of €2,000 maturing in 1, 2 and 3 years, yielding 2.40%, 2.55% and 2.70% | B — fixed income without much duration |
| Long fixed | €2,000 | 10-year fixed-rate bond yielding 3.60% | A — a small hedge, to be increased if correlation turns negative |

**3.13.3 The income, slice by slice.**

- **Floater.** Coupon rate = 2.713% + 0.80% = 3.513%, or €421.56 a year on €12,000, paid as two half-yearly coupons of about €210.78. The rate resets at every six-month fixing, so if the ECB keeps hiking, this income rises with it.
- **Ladder.** €2,000 × (2.40% + 2.55% + 2.70%) = €48 + €51 + €54 = €153 a year. In twelve months the 1-year bond repays €2,000, which buys a new 3-year bond at the rate prevailing then.
- **Long bond.** €2,000 × 3.60% = €72 a year.

Total: €421.56 + €153 + €72 = **€646.56 a year, about 3.23%** on €20,000 — roughly 0.8 points above €STR.

**3.13.4 The stress test: rates up one point.** Price change ≈ −modified duration × rate change. Table 3.13 applies it slice by slice.

*Table 3.13 — Price impact of a +1% parallel rise in rates*

| **Slice** | **Approx. duration** | **Price change** |
| --- | --- | --- |
| Floater €12,000 | 0.5 or less (until the next reset) | about −€60 |
| Ladder €6,000 | about 1.9 on average | about −€114 |
| Long fixed €2,000 | about 8.3 | about −€166 |
| **Portfolio** | | **about −€340 (−1.7%)** |
| *All €20,000 in the 10-year bond* | *about 8.3* | *about −€1,660 (−8.3%)* |

▶  PROOF — Three checks that the allocation does what the correlation reading asked of it

- **Price risk is a fraction of the all-long alternative.** A one-point rise costs about €340 against about €1,660 for the same money in the 10-year bond — roughly one-fifth of the risk, at a time when rule A says long bonds are not hedging the rest of the portfolio.
- **Income beats cash by enough to justify the risk.** About 3.23% gross against 2.44% on €STR clears the cash benchmark, and the floater slice keeps that margin intact if rates keep rising.
- **Every slice traces to a rule.** Each line of Table 3.12 cites the reading behind it. A slice that cannot name its rule is a position taken on habit — and each still has to pass the Section 3.3 checks before it is bought.

**3.13.5 When to rebalance.** The allocation is held until the reading crosses one of the thresholds in Table 3.14.

*Table 3.14 — Rebalancing triggers*

| **Signal** | **Action** |
| --- | --- |
| 90-day correlation below 0 for a month | Move part of the floater slice into 7–10-year fixed-rate bonds |
| 90-day correlation back between 0 and +0.2 | Hold; bonds diversify again but do not yet hedge |
| A ladder rung matures | Reinvest at the far end of the ladder |

Trading costs belong in every one of these moves: broker commission, the bid-ask spread (wider on small orders and thinly traded issues) and accrued interest, which the buyer pays to the seller on top of the clean price (Section 3.2.2).

| **⚠ WARNING — Six mistakes to avoid when positioning bonds** |
| ------------------------------------------------------------------ |
| **Assuming bonds always hedge stocks** — in 2022, and again since April 2026, both fell together; check the correlation before relying on it. **Reading a flat line as a flat market** — on a shared linear axis the Treasury ETF looks motionless next to the S&P 500; read the correlation panel or switch to a log scale. **Using a stale Euribor** — Euribor fixings are published monthly in most free series while €STR is daily; check the fixing date before computing a coupon. **Confusing coupon with yield** — a bond bought above 100 yields less than its coupon; compare yields, not coupons. **Chasing the highest yield** — a yield well above similar bonds usually signals credit or liquidity risk (Section 3.3), not a bargain. **Selling on a rate rise** — for a bond held to maturity, a price drop in between is temporary. |

<table>
<tbody>
<tr class="odd">
<td><p><strong>◈ KEY INSIGHT<br />
</strong></p>
<p><em>"A bond is judged twice: once as a promise — will this issuer pay on schedule, and what can the clauses take away? — and once as a link in the intermarket chain — what are rates, inflation, and stocks doing around it? The risk map answers the first question; the chain and the stock–bond correlation answer the second, and neither answer substitutes for the other."</em></p></td>
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
<td><p>A bond is a fixed, contractual promise — coupon and redemption defined at issuance — which is why clean/dirty price reconciliation and effective-yield (XIRR) calculation matter more here than for equities.</p>
<p>Seven checks drive the screen: credit/default safety, duration fit to the holding horizon, structural clause risk (Call/Cap/Tarn), liquidity, inflation-protection fit, reinvestment exposure, and subordination tier.</p>
<p>The methodology scores in three layers: weighted binary rules (summing to 100), partial credit for near-misses on sliding-scale rules, and a 15%-per-field penalty for missing essential data.</p>
<p>All financial markets are interlinked across four major asset classes -- currencies, commodities, bonds, and stocks -- and reading them together explains market sequence and sector rotation in a way single-market analysis cannot.</p>
<p>The core chain: bonds and stocks normally move together with bonds leading; commodities and bonds move inversely (commodities lead inflation); the dollar and commodities move inversely, with gold as the leading proxy for the whole commodity link.</p>
<p>Specific sectors (utilities, gold miners, energy, airlines) are structurally tied to specific links in the chain and can serve as early proxies for a macro move.</p>
<p>The ratio method (one asset's price divided by another) turns the chain into a single, directly readable line, and generalizes into a three-step top-down approach: overall market, then sector, then individual stock.</p>
<p>Disinflation and deflation both show falling commodity prices and rising bond prices, but only deflation decouples stocks and sends them lower -- the severity of the commodity move is what tells the two regimes apart.</p>
<p>The rolling correlation of daily stock and Treasury returns decides whether long duration hedges or adds risk: below 0 bonds hedge stocks, above +0.2 both fall together. The sign depends on the shock — growth scares push it negative, inflation and rate scares positive — and it measures daily co-movement, not the long-run trend of Section 3.5.3.</p>
<p>Three rules turn the reading into action — regime first, ladder the fixed part, hold to maturity unless the regime changes — and every candidate bond still has to pass the Section 3.3 checks.</p>
<p>Section 3.12 supplies the free data sources (FRED, yfinance, Stooq) and short fetch code for the cross-asset series, including a free substitute for the proprietary CRB Index; `bond_data_endpoints.py` covers the euro rates (€STR, Euribor) used in the case study.</p>
<p>On the 2026-09-23 reading (90-day correlation +0.44, 10-year yield 5.11%, €STR 2.44%) a €20,000 portfolio of floaters, a short ladder and a small long bond earns about 3.23% gross with roughly one-fifth of the rate risk of holding the 10-year bond alone.</p></td>
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
<td><p><strong>Clean price</strong> The quoted market value of a bond's capital only, excluding accrued interest.</p>
<p><strong>Dirty price (Tel Quel)</strong> The actual settlement amount: clean price plus accrued coupon.</p>
<p><strong>Modified duration</strong> A measure of a bond's price sensitivity to a change in market rates; the basis for this chapter's duration-fit rule.</p>
<p><strong>Effective yield (XIRR)</strong> The internal rate of return on the full cash-flow schedule — purchase outlay, coupons, redemption — as opposed to the nominal coupon rate.</p>
<p><strong>Subordination tier</strong> A bond's position in the bail-in loss-absorption hierarchy, from senior/government (safest) to Tier I Perpetual (equity-like risk).</p>
<p><strong>Call option</strong> An issuer's right to redeem a bond early at par, typically exercised when falling rates make the bond's coupon expensive to keep paying.</p>
<p><strong>Weighted score</strong> The `[0, 100]` output of the Section 3.4 methodology — binary rule weights plus partial credit for near-misses, discounted for missing data.</p>
<p><strong>Floating-rate bond (floater)</strong> A bond whose coupon resets periodically to a reference rate, such as 6-month Euribor, plus a fixed spread.</p>
<p><strong>€STR</strong> The euro short-term (overnight) rate, which tracks the ECB's policy rate; the cash benchmark for euro bond returns.</p>
<p><strong>Stock–bond correlation</strong> The rolling correlation of daily stock and bond returns; below zero, bonds hedge equities, above zero, they add to equity risk.</p>
<p><strong>Laddering</strong> Splitting bond capital into equal portions across progressive maturities to smooth reinvestment risk and cash flow.</p>
<p><strong>Intermarket analysis</strong> Reading markets as an interlinked system across currencies, commodities, bonds, and stocks rather than in isolation.</p>
<p><strong>Lead-lag relationship</strong> One market's turns consistently preceding another's, as with bonds leading stocks.</p>
<p><strong>CRB Index</strong> A broad commodity index commonly used as the numerator in commodity/bond ratio analysis; proprietary today, with no free API (Section 3.12.4).</p>
<p><strong>Relative strength ratio</strong> One asset's price divided by another's, used to reveal which side of the pair is outperforming.</p>
<p><strong>Top-down approach</strong> Selecting positions by narrowing from overall market, to sector, to individual stock, in that order.</p>
<p><strong>Disinflation</strong> Falling commodity prices with rising bond AND stock prices -- benign for financial assets.</p>
<p><strong>Deflation</strong> Collapsing commodity prices with rising bonds but falling stocks, due to an earnings collapse.</p>
<p><strong>Sector rotation</strong> Capital moving between sectors (e.g. cyclical to defensive) as the intermarket regime shifts.</p></td>
</tr>
</tbody>
</table>

| **WHAT'S NEXT** |
| -------------------- |
| This chapter closes the two asset chapters of Part I — Investing and Stock Market with a cross-asset, top-down lens for everything that follows. Chapter 4 (Exchange Traded Products) turns from the assets to the funds that hold them — equity and bond ETFs first, then the commodity and note products built on futures in Chapters 5 and 6; carry the bond/stock/commodity/dollar chain from Section 3.5 and the ratio method from Section 3.8 forward as context for those instrument chapters, not as a one-time read. `bond_data_endpoints.py` and Section 3.12 supply the free public data sources (ECB, US Treasury, FRED, Eurostat, `yfinance`, Stooq) behind every dashboard and ratio in the chapter. |


---

**Updated 2026-09-22** — this chapter shifted from Chapter 7 to Chapter 4 (all internal section, table, and listing numbers decremented by three accordingly) as part of a project-wide left-shift across the six chapters previously numbered 7–12, to close the gap opened when Chapters 1–3 (Investment Classes and Instruments, Exchange Traded Products, and Investing in Stocks) were added ahead of this reference set. This chapter keeps its "Reference Chapter" / standalone framing (Prereqs: None, "WHERE THIS FITS" instead of "WHAT'S NEXT"), unchanged from its original draft. The two earlier draft notes about a chapter-number collision with "Intermarket Analysis" and an unfinished `screen_bond()` listing have been removed from this version: the collision was resolved by this and subsequent renumbering passes (Intermarket Analysis is now Chapter 5), and `screen_bond()` remains an intentionally-named-but-undrafted wiring function, consistent with this reference set's other chapters, rather than an open issue specific to this file.

**Updated 2026-09-25** — Sections 4.5–4.8 (Python listings for price, yield and score; screening and laddering; the score-reading PROOF; the EVIDENCE section) removed and replaced by three sections integrated from `writing_plans/Bonds_Trading_Guide.md`: 4.5 Reading the Bond Market with Three Dashboards (Figures 4.1–4.3, Tables 4.4–4.5), 4.6 Five Rules for Positioning a Bond Portfolio (Table 4.6), and 4.7 [PROOF] Case Study — Reading the Dashboards and Investing €20,000 (Tables 4.7–4.9). Listings 4.1–4.4 no longer appear in the chapter.

**Updated 2026-10-06** — Renumbered from Chapter 4 to Chapter 5 after Chapter 2 (Exchange Traded Products) was split into Chapter 2 (ETFs) and Chapter 3 (ETCs and ETNs). Section, subsection, table, figure and listing numbers, the header digit box, Prereqs and cross-chapter references updated; dated notes above keep the numbering of their time.

**Updated 2026-10-06 (b)** — Converted from a standalone reference chapter to a normal main-sequence chapter: standard running banner and "Chapter 5" digit box (the box still showed the pre-split number), Part I label and real Prereqs line, closing WHERE THIS FITS box replaced by WHAT'S NEXT pointing to the next chapter. Generator updated to match.

**Updated 2026-10-06 (c)** — Part label aligned with `.claude/CLAUDE.md` §3.3: Part I — Investing and Stock Market (Ch 1–9), Part II — Technical Analysis (Ch 10–15); "opens/closes Part …" sentences adjusted.

**Updated 2026-10-06 (e)** — Renumbered (+1) after Futures Trading moved to Chapter 3 ahead of ETCs and ETNs; section, table, figure and listing numbers and cross-references updated.

**Updated 2026-10-07** — Merged with the former Chapter 7 (Intermarket Analysis) into "Bonds and the Intermarket Chain". Bond §6.1–6.4 unchanged; intermarket §7.1+7.3 → §6.5, §7.4 → §6.6, §7.5 → §6.7 (7.5.0/7.5.1 → 6.7.1/6.7.2), §7.6+7.7 → §6.8, §7.8 → §6.9; bond dashboards §6.5 → §6.10, rules §6.6 → §6.11; data section §7.9 rewritten and trimmed → §6.12 (4 labelled listings → 3, ~30 lines; program-trading tickers removed; blockquotes → WARNING and DATA callouts); bond PROOF §6.7 → §6.13. Dropped: §7.2 Program Trading, §7.10 Quantitative and Neural Network Tools, §7.11 [PROOF] (only the bond PROOF kept). Cross-links added between §6.5.6/§6.9 and §6.10.1/§6.11. FRAMING callout → EDGE. New title, subtitle, covers, KEY INSIGHT; summary and key terms combined (program trading and correlation filter dropped). Chapters 8–15 renumbered 7–14.

**History of the former Chapter 7 (Intermarket Analysis):**


*Source: Chapter summary restructured into this project's house style (opening block, THIS CHAPTER COVERS, numbered N.x sections, data tables, EDGE/PROOF callouts, KEY INSIGHT, Chapter Summary, Key Terms, What's Next), following the same pattern used for Chapters 1, 4, and 6. Sections 6.1-6.8 and 6.10-6.11 remain prose/relationship-based per the original project decision to keep the narrative content code-free; Section 6.9 was added on 2026-09-11 as a deliberate exception — a data-reference section supplying the free public sources and fetch code the chapter's ratios and lead-lag checks require, condensed from `code_snippets/ch01/free_paid_data_sources.md` Section 9. Sections 6.9 (originally Quant/Neural Tools) and the closing PROOF section were renumbered to 6.10 and 6.11 to make room; the THIS CHAPTER COVERS table above reflects that numbering.*

**Updated 2026-09-13** to match `.claude/CLAUDE.md` §3.3's continuous manuscript numbering: this chapter opened Part II — Investing and Stock Market. All internal section/table references (previously 17.x, per the original source chapter numbering) were renumbered to this project's continuous sequence; the header digit box, chapter title line, Prereqs, WHAT'S NEXT box, and this footer were updated accordingly. The earlier notes' own internal chapter mentions (1, 3, 6), which already refer to this project's stable Part I numbers, were left unchanged. The Prereqs line was simplified to Ch 2 (Markets, Instruments & Data) only — the earlier Ch 16 (Money Management) prereq was dropped per the user's decision, since Money Management now comes later in the book (Chapter 9) and can no longer be a prereq for a chapter that precedes it. The stale Part VII / "Trading Practice & Market Structure" label and its unresolved mismatch with CLAUDE.md's Infra/Cloud-Deployment assignments (noted in the paragraph above) are superseded by this update and no longer apply. Note that CLAUDE.md's Part IV table has not yet been converted to continuous numbering (still shows 1-7 instead of 19-25) -- a future cross-reference from this chapter to a Part IV chapter would need re-checking once that catches up.

**Updated 2026-09-13 (2)** -- five content additions made after building and real-data-testing the ten `code_snippets/intermarket/` dashboard scripts against this chapter's claims: (1) new 5.3.4 caveat on the bonds->stocks link decoupling under a policy-tightening regime; (2) new 5.4.3 note on gold's documented dollar-decoupling episodes (central-bank buying / de-dollarization flows); (3) new 5.5.0 caveat flagging the airlines/oil pair as noisier than the other three Table 5.2 links, due to fuel hedging; (4) new Table 5.4 third row and 5.8.2 section adding a "reflation-by-tightening" regime, alongside the existing disinflation/deflation pair, plus a pointer to the Regime Classifier script for detecting it; (5) the Section 5.9 PROOF paragraph now names `data_integrity_checks.py` as the script that runs its three checks in code. None of these change the chapter's existing section numbering (5.9-5.11 and Tables 5.1-5.3 are untouched) -- 5.3.4, 5.4.3, 5.5.0, and 5.8.2 are additions within their existing sections. Source: user-requested "propose improvements to the chapter or the scripts" review of the real 2017-2026 chart outputs discussed in this session.

**Updated 2026-09-22** -- this chapter previously shifted from Chapter 7 to Chapter 8 (a project-wide +1 renumbering across the five chapters then numbered 7-11, to open up Chapter 7 for a new "Investing in Bonds" reference chapter), and now shifts again from Chapter 8 to Chapter 5 (all internal section, table, and cross-reference numbers decremented by three accordingly) as part of a further project-wide left-shift across the six chapters then numbered 7-12, to close the gap opened when Chapters 1-3 (Investment Classes and Instruments, Exchange Traded Products, and Investing in Stocks) were added ahead of this reference set. The WHAT'S NEXT pointer to Dividend Investing was updated to "Chapter 6" to match that chapter's own shift. Historical dated notes above have had their internal chapter/section numbers updated for consistency with the current numbering; where a note describes an intermediate historical state, it now reflects the final current number rather than the intermediate one.

**Updated 2026-10-06** — Renumbered from Chapter 5 to Chapter 6 after Chapter 2 (Exchange Traded Products) was split into Chapter 2 (ETFs) and Chapter 3 (ETCs and ETNs). Section, subsection, table, figure and listing numbers, the header digit box, Prereqs and cross-chapter references updated; dated notes above keep the numbering of their time.

**Updated 2026-10-06 (c)** — Part label aligned with `.claude/CLAUDE.md` §3.3: Part I — Investing and Stock Market (Ch 1–9), Part II — Technical Analysis (Ch 10–15); "opens/closes Part …" sentences adjusted.

**Updated 2026-10-06 (e)** — Renumbered (+1) after Futures Trading moved to Chapter 3 ahead of ETCs and ETNs; section, table, figure and listing numbers and cross-references updated.

**Updated 2026-10-08 (reorder)** — Part I reordered: Stocks 5→2, Bonds+Intermarket 6→3, ETFs 2→4, Futures 3→5, ETCs/ETNs 4→6. Chapter, section, table, figure and listing numbers and all cross-references remapped; WHAT'S NEXT chain and Prereqs adjusted.

**Updated 2026-10-08 (cash flows)** — §3.2.3 extended with Figure 3.1 (fixed / floating / zero-coupon cash flows) and a reading paragraph; new §3.2.4 Effective yield with Figure 3.2 (investor cash flows −100 / +5 / +105; yield 5.67% / 5.00% / 4.37% at 95 / 100 / 105). Dashboard figures renumbered 3.1–3.3 → 3.3–3.5.

**Updated 2026-10-08 (cash flows b)** — Figures 3.1–3.2 redrawn from the improved design: amounts on every bar, a one-line reading under each coupon structure, hatched day-0 price bar, and a gain/loss-at-maturity column beside the three yields. Figure 3.2 caption updated.

**Updated 2026-10-08 (correlation)** — §3.10 replaced: "Do Bonds Still Hedge Stocks? The Stock–Bond Correlation" (3.10.1 what the dashboard measures, Figure 3.3 new Sept-2026 screenshot; 3.10.2 reading the regime, Table 3.8 + new Figure 3.4 gauge and 1-year path; 3.10.3 why the sign flips, new Table 3.9; 3.10.4 trend vs daily moves; 3.10.5 what to do). Removed: Rate & Coupon-Reset dashboard, Inflation-Linked tracker, old Table 3.9, old Figures 3.4–3.5. §3.11 now three rules (A regime, B ladder, C hold), 3.11.1 dropped. §3.13 PROOF rebuilt on the correlation reading: €12,000 floater / €6,000 ladder / €2,000 long, 3.23% gross, −€340 on +1% rates; linker slice removed. Summary, key terms (breakeven removed), key insight, warning box, TOC updated.

**Updated 2026-10-08 (hicp)** — New §3.9.3 "Ten years of euro-area prices, four regimes": Figure 3.3 (euro-area HICP 2016–2026 with four shaded regimes, B&W, from the user's Inflation-Linked Revaluation Tracker; endpoint 129.56, earlier points approximate) and Table 3.8 (period / index / regime / markets), plus the disinflation-is-not-deflation paragraph. Later tables +1 (3.8–3.13 → 3.9–3.14), figures +1 (3.3–3.4 → 3.4–3.5).
