|                                                             |
| ----------------------------------------------------------- |
| **PYTHON FOR TRADERS: INVESTING, DERIVATIVES, AND TECHNICAL ANALYSIS APPLIED** |

|           |       |
| --------- | ----- |
| Chapter 4 | **4** |

**Exchange Traded Products: Structure, Costs, and ETFs**

*The three ETP families and how each one replicates its underlying, the risk each structure leaves you carrying, and the Synthetic Cost Index (ICS) that turns the choice between products into a number — and then drives every step of an ETF trade*

Part I — Investing and Stock Market · Prereqs: Chapter 1 (Investment Classes and Instruments)

<table>
<thead>
<tr class="header">
<th><strong>THIS CHAPTER COVERS</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>4.1 The Three ETP Families, and Where to Find the Data That Matters</p>
<p>4.2 How Replication Actually Works — Physical vs. Synthetic</p>
<p>4.3 Mapping the Risk of Each ETP Family</p>
<p>4.4 The Synthetic Cost Index (ICS) — Comparing Costs Across Products</p>
<p>4.5 ETFs in Practice — Bond, Equity, Smart Beta, Thematic, and REIT Baskets</p>
<p>4.6 Near-Zero Prices, Reverse Splits, and Delisting — What Happens to Your Capital</p>
<p>4.7 [CODE] Hands-On — The ICS and Its Hurdle in Python</p>
<p>4.8 [PROOF] Trading an ETF Informed by the ICS — Step by Step</p></td>
</tr>
</tbody>
</table>

|                                                                        |
| ---------------------------------------------------------------------- |
| **4.1 THE THREE ETP FAMILIES, AND WHERE TO FIND THE DATA THAT MATTERS** |

Chapter 1 introduced **ETPs (Exchange Traded Products)** as the transparent, exchange-listed alternative to actively managed mutual funds and Sicav. That single label, however, covers three legally and structurally distinct instrument families, and the difference between them is not cosmetic — it determines who bears the risk if an issuer fails, how the product's return is actually generated, and how the product should be read before a single euro is committed.

*Table 4.1 — The three ETP families*

| **Type** | **Legal Structure** | **Underlying Replicated** | **Issuer Risk / Assets** |
| :--- | :--- | :--- | :--- |
| **ETF** *(Exchange Traded Fund)* | Passively managed mutual fund | Equity, bond, or REIT indices/baskets | **Segregated assets**: protected from issuer default |
| **ETC** *(Exchange Traded Commodity)* | Securitized bond | Futures on commodities or physical precious metals | Backed by **collateral** or physical metal (*Physical*) |
| **ETN** *(Exchange Traded Note)* | Securitized bond | Currencies, leveraged or short equity/bond indices | Subject to the **issuer's credit risk**, unless backed by collateral (Section 6.2.6) |

**4.1.1 Only the ETF is a fund in the strict sense.** An ETF's assets are segregated from the issuing management company's own balance sheet: if the issuer fails, the fund's holdings are untouched. An ETC and an ETN are both, legally, **securitized bonds** issued by a financial institution to synthetically or physically track a given underlying — the investor is a bondholder of the issuer, not a unit-holder of a segregated fund, and the practical consequences of that distinction run through the rest of this chapter.

**4.1.2 Reading an instrument sheet.** Before committing capital to any ETP, the issuer's own product page (richer than the exchange's own listing page) should be checked for: the **ticker** and **ISIN** (the ticker for fast order entry, the ISIN for unambiguous international identification), the **minimum lot** (normally 1 unit), the **TER** (*Total Expense Ratio* — the annual management fee, deducted pro-rata daily from the fund's assets), the **Market Maker's listing obligations** (the minimum quantity it must quote and the maximum spread it must maintain), the full **basket composition**, the **replication method**, the **NAV**, the **tracking error**, and — for bond ETFs specifically — the aggregate **duration** and average yield to maturity.

| **◆ EDGE — "ETP" is the umbrella; "ETF" is one branch of it, not a synonym**                                                                                                                                                                                                                                          |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Retail conversation routinely uses "ETF" as a catch-all for anything traded like a fund. That habit is harmless for equity and bond exposure, where the instrument usually *is* an ETF — but a commodity or currency position bought under the same mental label is frequently an ETC or an ETN instead, carrying a materially different risk profile the "ETF" habit quietly hides. |

|                                                                |
| ---------------------------------------------------------------- |
| **4.2 HOW REPLICATION ACTUALLY WORKS — PHYSICAL VS. SYNTHETIC** |

The replication structure defines how an ETP actually tracks its benchmark, and it is the single most important line item on the instrument sheet for assessing counterparty risk.

**4.2.1 Full physical replication.** The issuer directly buys every security in the basket, in the correct weights. The securities are owned by the fund and held with a depositary bank. No counterparty risk exists, aside from any securities-lending the fund may separately engage in.

**4.2.2 Sampled physical replication (optimization).** For very broad indices, the issuer buys a representative subset of the basket rather than every constituent, to hold down transaction costs. This lowers acquisition costs but can widen the tracking error.

**4.2.3 Synthetic unfunded replication.** The issuer buys a substitute basket of securities and enters into a **Swap** contract with an investment bank (the counterparty) to exchange that basket's return for the benchmark's return. Under UCITS rules, counterparty risk is capped by law at **10% of NAV**, and is marked to market and reset periodically.

**4.2.4 Synthetic funded replication.** The issuer transfers the subscription proceeds to the Swap counterparty, which in turn deposits **collateral** with a depositary bank — typically over-collateralized above 100% of the position's value. If the counterparty defaults, the fund takes immediate possession of the collateral rather than waiting on a claims process.

![How an ETF replicates its index — physical (full, sampled) vs synthetic (unfunded, funded) replication](../images/Ch2_ETFReplication_diagram.png)

*Figure 4.1 — How an ETF replicates its index. Physical replication (full or sampled) means the fund owns the securities; synthetic replication (unfunded or funded) gets the index return through a swap, and the method decides the counterparty risk.*

**4.2.5 Replication in ETCs specifically.** Gold and precious-metal ETCs (labeled *Physical*) use physical replication: the issuer buys actual bars and vaults them with a certified depositary (e.g., an LBMA-approved custodian), eliminating counterparty risk entirely. Agricultural, energy, and industrial-commodity ETCs, which must track futures rather than a storable physical asset, normally use *funded* synthetic replication with over-collateralization, which similarly holds issuer-default risk close to zero without removing it structurally the way physical gold does.

*Table 4.2 — Replication method vs. structural counterparty risk*

| **Replication method** | **Used by** | **Counterparty risk** |
| :--- | :--- | :--- |
| Full physical | ETF (equity/bond) | None (ex securities lending) |
| Sampled physical | ETF (broad index) | None, but higher tracking error |
| Synthetic unfunded | ETF (Swap-based) | Capped at 10% of NAV by UCITS rules |
| Synthetic funded | ETF (Swap-based) | Mitigated by over-collateralization |
| Physical | ETC (gold/precious metals) | None |
| Synthetic funded | ETC (agricultural/energy/industrial) | Mitigated by over-collateralization |
| Synthetic (issuer's own balance sheet) | ETN | **Full issuer credit risk** — not segregated |

|                                                        |
| -------------------------------------------------------- |
| **4.3 MAPPING THE RISK OF EACH ETP FAMILY**             |

**4.3.1 ETF risk map.** Credit (issuer) risk is **absent** — the fund's assets are segregated and untouched by the issuer's own insolvency. Liquidity and market risk are governed by the mandatory presence of a Market Maker, and ultimately depend on the underlying market's own tradability. Currency risk is present whenever the basket's securities are denominated in a foreign currency (*EUR-Hedged* share classes exist specifically to remove it). Counterparty risk is present only in synthetic-replication products, or in physically replicated ones that lend out securities. Tracking error — the temporary or structural gap between the ETF's return and the index's actual performance — is present to some degree in every replication method.

**4.3.2 ETC risk map.** Physical ETCs (gold, precious metals) carry no counterparty risk at all. Synthetic ETCs on futures-based commodities carry counterparty risk mitigated, but not eliminated, by over-collateralization. Both are additionally exposed to the mechanical cost-of-carry and roll-yield dynamics covered in Section 6.1 — a risk with no equivalent in the ETF world, because it comes from the futures curve itself rather than from the issuer.

**4.3.3 ETN risk map — the one family without a segregated-assets backstop.** Because an ETN is a securitized bond on the issuer's own balance sheet, its holder is a general creditor of that issuer, exposed to the **issuer's own credit risk** exactly as a corporate-bond holder would be — no segregated fund structure stands between the investor and the issuer's solvency. This is the unsecured case; many European ETNs are instead notes of a special purpose vehicle backed by collateral, which changes the answer (Sections 6.2.5–6.2.7). The unsecured case is also the structural fact behind Section 6.2's recommendation to prefer unhedged direct ownership of foreign securities over leveraged currency ETNs where the goal is simply currency diversification rather than short-term tactical leverage.

| **⚠ WARNING — The risk that doesn't show up in the ticker**                                                                                                                                                                                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Two products can trade with visually similar tickers and nearly identical price charts while carrying completely different counterparty exposure — a physically replicated gold ETC and a synthetic gold-linked ETN can both say "gold" on the label, but only one of them survives its issuer's bankruptcy intact. The legal structure in Table 4.1, not the product name, is what determines the answer. |

|                                                                                |
| ---------------------------------------------------------------------------------- |
| **4.4 THE SYNTHETIC COST INDEX (ICS) — COMPARING COSTS ACROSS PRODUCTS**       |

When two or more ETPs — of any family — track the same underlying exposure, cost comparison cannot stop at the TER alone. the **Synthetic Cost Index (ICS)** combines the explicit, ongoing management cost with the implicit, per-transaction cost of actually trading the instrument:

$$\text{ICS} = \text{TER} + 2 \times \text{average bid/ask spread}$$

**4.4.1 The ICS in plain words.** Owning an ETP costs money in two ways. The first is a **yearly fee**, the TER, taken quietly from the fund every year you hold it — like a gym membership. The second is a **toll on every trade**, the bid/ask spread: you buy at the higher price (the ask) and sell at the lower one (the bid), just as a currency-exchange booth keeps a margin when you change money and change it back. The ICS adds one year of the fee to the toll on the way in and the toll on the way out (Figure 4.2).

![ICS = TER, a yearly fee, plus 2 × spread, a toll on each trade](../images/ETF_ICS_1_formula.png)

*Figure 4.2 — The Synthetic Cost Index in two parts: a yearly fee that grows with time, and a toll paid on the way in and on the way out, however long the position is held.*

Table 4.3 runs the arithmetic on €10,000 placed in one of two ETFs that track the same index.

*Table 4.3 — Two ETFs on the same index, €10,000 invested*

| | **TER (yearly fee)** | **Spread (toll per trade)** | **ICS** | **Held 2 months** | **Held 1 year** | **Held 10 years** |
| --- | --- | --- | --- | --- | --- | --- |
| ETF A | 0.10% = €10 a year | 0.10% = €10 each way | 0.30% | €1.67 + €20 = €21.67 | €10 + €20 = **€30** | €100 + €20 = **€120** |
| ETF B | 0.30% = €30 a year | 0.02% = €2 each way | 0.34% | €5 + €4 = **€9** | €30 + €4 = €34 | €300 + €4 = €304 |

On the headline ICS, ETF A wins — and over exactly one year it is indeed cheaper, €30 against €34. Held for two months, ETF B costs less than half as much, because its low toll matters more than its higher fee; held for ten years, ETF A saves €184, because the yearly fee keeps coming back while the toll is paid only twice. Figure 4.3 draws the same two ETFs as cost lines: ETF A starts higher (€20 of tolls) but climbs slowly (€10 a year); ETF B starts low (€4) but climbs fast (€30 a year). The lines cross at about ten months — the break-even holding period. The rest of this section builds on that one observation: **for a trader the spread decides the cost; for a long-term investor the TER does.**

![Total cost of ETF A and ETF B against holding period, crossing at about ten months](../images/ETF_ICS_2_holding_period.png)

*Figure 4.3 — The cheaper ETF changes with the holding period. Before about ten months the lower toll (ETF B) wins; after it, the lower yearly fee (ETF A) wins. Costs ignore compounding and commissions.*

**4.4.2 Why the spread is counted twice.** The bid/ask spread is paid once on entry and once on exit — every round trip pays it twice — while the TER accrues pro-rata for however long the position is actually held. The average spread itself is measured by the exchange monthly, typically for a standardized notional (e.g., €25,000), which keeps the comparison fair across products with very different typical trade sizes. Strictly, a buy-and-sell round trip costs about one *full* quoted spread — half on the way in, half on the way out, measured from the mid-price — so doubling the full spread makes the ICS a deliberately conservative estimate. It still ranks products correctly against each other, because every product is doubled the same way; just do not read 2 × spread as the exact cost of one trade.

**4.4.3 The selection rule.** For any set of ETPs replicating the same basket or the same underlying, the one with the **lowest ICS** is the more cost-efficient choice — a rule that applies identically whether the products being compared are two ETFs, two ETCs, two ETNs, or products across all three families competing for the same exposure, which is exactly the situation Section 4.4.7's worked example walks through; Section 4.8 then applies the whole method, step by step, to a live trade.

**4.4.4 Reading the ICS by holding period.** The ICS as defined above assumes the position is bought, held for exactly one year, and sold. The two terms, however, behave differently over time: the TER grows with every year held, while the spread is paid only twice, whatever the holding period. For any horizon:

$$\text{Cost over the holding period} \approx \text{TER} \times \text{years} + 2 \times \text{average bid/ask spread}$$

Figure 4.4 shows the three inputs on a live dashboard for an S&P 500 UCITS ETF listed on Euronext Paris: TER 0.15%, spread 0.03%, ICS 0.21%. Over one month the cost is 0.15/12 + 0.06 ≈ 0.07%, of which 85% is spread; over ten years it is 1.50 + 0.06 = 1.56%, of which only 4% is spread. **For a trader the spread decides the cost; for a long-term investor the TER does** — and two products with the same headline ICS can rank in opposite order for the two.

![ICS dashboard — Amundi S&P 500 UCITS ETF (500.PA), TER 0.15%, spread 0.03%, ICS 0.21%](../images/ICS_dashboard_500PA_2026-09_light.png)

*Figure 4.4 — ICS dashboard for 500.PA (Amundi S&P 500 UCITS ETF C EUR, Euronext Paris), daily, 1-year range, snapshot 2026-09-24. The header shows the three inputs of the formula: TER 0.15%, spread 0.03% and the resulting ICS 0.21%.*

**4.4.5 Which spread to use.** The formula is only as good as its spread input, and different sources measure different things. Table 4.4 lists the main ones and how each enters the ICS.

*Table 4.4 — Spread sources and how each enters the ICS*

| **Source** | **What it measures** | **How to use it** |
| --- | --- | --- |
| Borsa Italiana monthly spread analysis (ETFplus) | Average spread per ETF for orders of €1, €5,000, €15,000 and €25,000 | Take the €25,000 column — the standard ICS input (Section 4.4.2). ETCs and ETNs are covered by a separate monthly statistics file. |
| Xetra Liquidity Measure (XLM), Deutsche Börse | Round-trip cost in basis points for a set order size | Already counts both entry and exit: ICS ≈ TER + XLM ÷ 100. **Do not double it.** |
| Euronext market-quality publications | Monthly market-quality statistics, including spreads | For products listed in Paris, Amsterdam, Brussels, Milan or Lisbon; coverage per product varies |
| A live quote (broker, dashboard header, data provider) | One snapshot of the best bid and ask | A last resort. Average several readings taken at different times of day. A single live quote is unreliable in both directions: on a liquid listing it usually understates the monthly average, on a thin listing it can overstate it when the market maker briefly widens. Use the exchange's monthly average whenever it exists. |

Whatever the source, record it next to the number — "spread 0.03% (Euronext, snapshot 2026-09-24)" is a comparable input; "spread 0.03%" on its own is not. The TER, by contrast, should always come from the product's KID (ongoing charges); a screener such as justETF is useful for scanning many funds at once, but its figures are unofficial and should be checked against the KID before the final choice.

**4.4.6 What the ICS leaves out.** The index covers the product's running cost and the market's spread. Four further costs sit outside it and can change the ranking:

- **Broker commission.** A fixed €5 per order is €10 per round trip: 0.05% on €20,000, but 0.5% on €2,000. On small orders it can exceed the ICS itself.
- **Roll cost on futures-based ETCs.** An oil or natural-gas ETC can show a low ICS and still lose several percent a year to contango (Section 5.2.2).
- **Tracking difference.** The product's actual return minus its benchmark's. A higher-TER fund can still track better, for example through securities-lending income; check it before the final choice.
- **Currency-hedging cost** on hedged share classes.

The spread also sets a **hurdle for every trade**: the ICS charges 2 × spread for a round trip — a deliberately conservative figure (Section 4.4.2) — so a trade whose target gain is less than about five times that cost is mostly paying the market maker. On a 0.03% spread a 1% target is comfortable; on a 1% spread the same target loses money even when the call is right.

**4.4.7 A worked example: €20,000 in an S&P 500 ETF.** Table 4.5 compares the ETF in Figure 4.4 with two hypothetical competitors on the same index — one with a lower TER, one with a lower spread — and converts each into euros for three holding periods (cost = €20,000 × (TER × years + 2 × spread) ÷ 100, ignoring compounding and commissions).

*Table 4.5 — The same €20,000, three S&P 500 ETFs, three holding periods*

| **ETF** | **TER** | **Spread** | **ICS (1 year)** | **1 month** | **1 year** | **10 years** |
| --- | --- | --- | --- | --- | --- | --- |
| 500.PA | 0.15% | 0.03% | 0.21% | €14.50 | **€42.00** | €312.00 |
| Competitor X (illustrative) | 0.07% | 0.08% | 0.23% | €33.17 | €46.00 | **€172.00** |
| Competitor Y (illustrative) | 0.20% | 0.02% | 0.24% | **€11.33** | €48.00 | €408.00 |

On the headline ICS, 500.PA wins — but only for a one-year hold. Setting the two cost lines equal gives the break-even holding periods: Y and 500.PA cost the same at 0.20t + 0.04 = 0.15t + 0.06, i.e. **t = 0.4 years (about 5 months)**; 500.PA and X at 0.15t + 0.06 = 0.07t + 0.16, i.e. **t = 1.25 years (15 months)**. Below five months the lowest-spread product (Y) is cheapest, between five and fifteen months the lowest-ICS product (500.PA), and beyond fifteen months the lowest-TER product (X) — which saves €140 over ten years against 500.PA and €236 against Y despite sitting in the middle of the ICS ranking.

Adding the broker commission from Section 4.4.6 changes the short horizon most: €10 per round trip takes 500.PA's one-month cost from €14.50 to €24.50, and splitting the same €20,000 into ten €2,000 purchases makes the commission alone 0.5% of each slice. Fewer, larger orders keep the ICS meaningful.

**4.4.8 Monitoring and switching.** An ICS ranking is a monthly reading, not a one-off. Re-check the holding when its spread widens more than 50% month on month, when a competitor cuts its TER, when fund size falls below about €50M (delisting risk, Section 4.6.2), or when tracking difference exceeds the TER by a wide margin (a replication problem, Section 4.2). A switch costs one sale and one purchase — about 2 × spread plus two commissions — so it pays only when the TER saving multiplied by the years remaining exceeds that cost.

| **⚠ WARNING — Five ways to misread an ICS** |
| ------------------------------------------- |
| **Ranking different exposures by ICS** — a cheap bond ETF is not a better S&P 500 ETF; the index only compares products on the same underlying. **Using the one-year figure for every horizon** — recompute for the actual holding period (Section 4.4.4). **Doubling the XLM** — it is already a round-trip cost. **Trusting one live spread** — a quote taken at a quiet moment understates the real average. **Forgetting what sits outside the index** — commissions on small orders and roll cost on futures-based ETCs can outweigh the ICS itself (Section 4.4.6). |

|                                                                                             |
| ----------------------------------------------------------------------------------------------- |
| **4.5 ETFs IN PRACTICE — BOND, EQUITY, SMART BETA, THEMATIC, AND REIT BASKETS**             |

**4.5.1 Bond ETFs.** Available across inflation-linked, money-market, corporate, emerging-market government (hard or local currency), Euro government, single-country government, and world/non-Euro government categories. A short-term government-bill ETF offers automatic diversification with continuous maturity rollover in a single instrument, at the cost of a TER and bid/ask spread (commonly 0.15% and 0.30–0.40% respectively) that can meaningfully erode an already-modest money-market return, and the loss of the flexibility to time individual coupon and redemption cash flows.

Selecting among bond ETFs means checking: issuer type (government/supranational vs. corporate), geographic and currency area, creditworthiness (Investment Grade vs. High Yield), duration bucket (very short, short 1–3y, medium 3–7y, long 7–15y+), basket concentration (no excessive weight in the top 4–5 countries or issuers — a red flag above roughly 10–12%), and cost via TER and ICS.

**4.5.2 Equity ETFs.** Available by geography (single country, Europe, World — often more than 50% weighted to US equities — Emerging Markets), by **Smart Beta** factor (passive replication of a basket selected on a predetermined quantitative factor such as Momentum, High Dividend, or Low Volatility), or **Thematic** (water, renewable energy, luxury, robotics, infrastructure, cybersecurity, ESG), where the main risk is buying into a passing trend or an already-overvalued sector rather than a durable exposure. Volatility and credit-index ETFs (VIX-linked, CDS-based Long/Short) round out the more specialized end of the shelf.

Selecting among equity ETFs means checking: the type of exposure (geographic vs. sector vs. thematic), geographic area, investment style, single-security or single-country concentration within the basket, and cost via TER and ICS.

**4.5.3 REIT ETFs.** Invest in listed Real Estate Investment Trusts holding income-producing commercial property, offices, shopping centers, and healthcare facilities — this is the practical implementation of Chapter 1's real-estate pillar. Low correlation with the other traditional asset classes is the main portfolio benefit; a prudent-portfolio allocation should generally not exceed **20%**. Global Developed, European, Asian, UK, and US baskets are all available.

**4.5.4 Commodity ETFs vs. ETCs.** UCITS-compliant commodity ETFs replicate commodity indices synthetically via Swap, exactly as a synthetic equity ETF would — but because they are funds rather than securitized bonds, they do **not** allow the tax offsetting of capital losses that ETCs on the same exposure typically do. This is a genuine, non-cosmetic decision point between the two families.

|                                                                                               |
| --------------------------------------------------------------------------------------------------- |
| **4.6 NEAR-ZERO PRICES, REVERSE SPLITS, AND DELISTING — WHAT HAPPENS TO YOUR CAPITAL**         |

**4.6.1 When an ETC's price approaches zero.** Cost-of-carry erosion or leverage decay can push a product's price toward infinitesimal values. The issuer typically responds with either a **reverse split** (consolidating existing units — e.g., 1 new unit for every 10 old ones) or an outright **delisting**, liquidating the product and reimbursing investors at the final NAV.

**4.6.2 ETF delisting.** Causes are usually mundane — the fund never reached a critical mass of assets, or the issuer is rationalizing/merging overlapping product ranges — and both the exchange and the issuer give ample advance notice of the delisting date. Critically, delisting **does not itself destroy capital**: the fund is liquidated and the final NAV is paid out by bank transfer. It may also be only a delisting from one exchange while the listing continues elsewhere. The most liquid ETFs, selected using the ICS from Section 4.4, carry a delisting risk close to negligible in practice.

*Table 4.6 — Delisting/wind-down mechanisms by ETP family*

| **Scenario** | **Typical family** | **Effect on invested capital** |
| :--- | :--- | :--- |
| Reverse split | ETC (leveraged/decayed) | No loss — units consolidated, per-unit price restored |
| Delisting / liquidation | ETF, ETC | No loss — paid out at final NAV |
| Cross-listing withdrawal only | ETF | No loss — listing continues on another exchange |
| Issuer default | ETN (collateralized) | **Depends on the collateral** — realized by the trustee; *limited recourse* caps the claim at that series' collateral |
| Issuer default | ETN (unsecured) | **At risk** — general creditor claim on the issuer |

**4.6.3 Why this table's bottom row matters most.** Every scenario above except the last two resolves with the investor's capital intact, paid out at NAV. The unsecured ETN row is the exception precisely because of the structural point from Section 4.3.3: without segregated assets or posted collateral standing behind it, an unsecured ETN's wind-down in an issuer-default scenario is not a routine NAV payout but a creditor claim — the single clearest practical consequence, across this entire chapter, of the legal-structure distinction first drawn in Table 4.1. A collateralized note sits in between: recovery depends on the checks in Table 6.7.

|                                                                       |
| ------------------------------------------------------------------------ |
| **4.7 [CODE] HANDS-ON — THE ICS AND ITS HURDLE IN PYTHON** |

The ICS is simple arithmetic, but it is arithmetic you redo every month (Section 4.4.8), on every product you hold or consider. Listing 4.1 turns Sections 4.4.1–4.4.7 into four functions: the index itself, the euro cost over a holding period, the break-even between two products, and the minimum target a trade needs before its round trip is worth paying. The PROOF that follows applies them to two real dashboards.

**4.7.1 Four functions for the whole section (Sections 4.4.1, 4.4.4, 4.4.6, 4.4.7).** All rates are in percent, as the dashboards print them: a TER of 0.38 means 0.38% a year, a spread of 0.06 means 0.06%.

**💻 PYTHON · Listing 4.1 — `ics`, `cost_eur`, `break_even_years` and `hurdle`: the cost index and what it implies**

```python
def ics(ter, spread):                  # 4.4.1: yearly fee + round-trip toll, %
    return ter + 2 * spread

def cost_eur(amount, ter, spread, years, commission=0.0):   # 4.4.4, 4.8.5
    return amount * (ter * years + 2 * spread) / 100 + 2 * commission

def break_even_years(a, b):            # 4.4.7: a, b = (ter, spread)
    (ta, sa), (tb, sb) = a, b
    if ta == tb:
        return None
    t = 2 * (sb - sa) / (ta - tb)
    return t if t > 0 else None        # None: one product cheaper at every horizon

def hurdle(spread, k=5):               # 4.4.6: minimum target gain, %
    return k * 2 * spread

# ics(0.38, 0.06) -> 0.50 (AMEW.DE)    ics(0.59, 0.34) -> 1.27 (IPRP.L)
# hurdle(0.06)    -> 0.6               hurdle(0.34)    -> 3.4
```

Full version, with self-test: `code_snippets/v1/ch04_etp/ch04_ics.py` (adds the tables of Sections 4.4 and 4.8 and the switch payback of Section 4.4.8).

**4.7.2 Reading the output.** The two `ics` values are the headers the PROOF checks in Step 2 (Section 4.8.2), and the two hurdles are the minimum targets of Step 4 (Section 4.8.4): about 0.6% for the world ETF, about 3.4% for the property ETF. `break_even_years` returns `None` when one product is cheaper at every holding period — the case where the choice needs no timing at all.

|                                                                             |
| --------------------------------------------------------------------------------- |
| **4.8 [PROOF] TRADING AN ETF INFORMED BY THE ICS — STEP BY STEP**            |

Section 4.4 built the tools: the ICS, its restatement by holding period, the spread sources, the costs it leaves out, and the monitoring rules. This section puts them in the order a trader actually uses them, on two live dashboards read on 2026-09-24:

- **AMEW.DE** — Amundi MSCI World UCITS ETF C EUR on Xetra, a broad developed-markets equity ETF (Figure 4.5).
- **IPRP.L** — iShares Developed Markets Property Yield on the London Stock Exchange, a REIT basket of the kind described in Section 4.5.3 (Figure 4.6).

The two track **different exposures**, so they are not ranked against each other — that would break the first rule of the ICS (Section 4.4.3). Each is taken through the same steps to show how differently they come out for a cheap core ETF and a costlier specialist one. The choice between competitors on the *same* exposure is the break-even calculation of Section 4.4.7.

![ICS dashboard — Amundi MSCI World UCITS ETF C EUR (AMEW.DE, Xetra), TER 0.38%, spread 0.06%, ICS 0.51%](../images/ICS_dashboard_AMEW_2026-09_light.png)

*Figure 4.5 — ICS dashboard for AMEW.DE (Amundi MSCI World UCITS ETF C EUR, Xetra, ISIN LU1681043599), daily, 1-year range, snapshot 2026-09-24. Header: TER 0.38%, spread 0.06%, ICS 0.51%; last price 698.24; 2,141 days of history.*

![ICS dashboard — iShares Developed Markets Property Yield (IPRP.L), TER 0.59%, spread 0.34%, ICS 1.28%](../images/ICS_dashboard_IPRP_2026-09_light.png)

*Figure 4.6 — ICS dashboard for IPRP.L (iShares Developed Markets Property Yield, London Stock Exchange, ISIN IE00B1FZS350), daily, 2-year range, snapshot 2026-09-24. Header: TER 0.59%, spread 0.34%, ICS 1.28%; last price 2,340.00; 4,477 days of history.*

**4.8.1 Step 1 — Fix the exposure and the holding period first.** Before any number is read, decide what the position is for. The exposure means the index, the currency treatment (hedged or unhedged) and, if it matters to you, the distribution policy (accumulating or distributing classes of the same fund often have different TERs and spreads). Only products on that same exposure go into the comparison. The holding period then decides which half of the ICS matters:

*Table 4.7 — Which cost decides, by holding period*

| **Holding period** | **Typical use** | **Pick the product with** |
| :--- | :--- | :--- |
| Weeks to a few months | Swing trade | Lowest spread |
| About one year | Tactical allocation | Lowest one-year ICS |
| Several years | Long-term investment | Lowest TER |
| In between | — | Compute the break-even holding period (Section 4.4.7) |

**4.8.2 Step 2 — Read the header and check the arithmetic.** ICS = TER + 2 × spread. For AMEW.DE: 0.38% + 2 × 0.06% = 0.50%; for IPRP.L: 0.59% + 2 × 0.34% = 1.27%. The dashboards show 0.51% and 1.28% because the inputs are rounded to two decimals — a gap of 0.01% is rounding, a larger one means the header is using a different spread from the one displayed. Then label the spread with its source: "spread 0.06% (Xetra, live snapshot 2026-09-24)". A single live snapshot is unreliable in both directions (Table 4.4); for a Xetra listing, the XLM is the better input and is **not doubled**.

**4.8.3 Step 3 — Restate the cost for your holding period.** Cost ≈ TER × years + 2 × spread. On a €20,000 position:

*Table 4.8 — Cost of €20,000 by holding period (dashboard inputs, no commission)*

| **ETF** | **1 month** | **Share of spread** | **1 year** | **10 years** | **Share of TER at 10 years** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| AMEW.DE | €30.33 | 79% | €100.00 | €784.00 | 97% |
| IPRP.L | €145.83 | 93% | €254.00 | €1,316.00 | 90% |

For a one-month trade both costs are almost all spread; over ten years both are almost all TER. The point at which the two halves are equal — the **spread horizon**, 2 × spread ÷ TER — is about 4 months for AMEW.DE (0.12 ÷ 0.38 = 0.32 years) and about 14 months for IPRP.L (0.68 ÷ 0.59 = 1.15 years). Below the spread horizon, choose among competitors by spread; above it, by TER.

**4.8.4 Step 4 — Check that the trade can pay for its round trip.** The ICS charges 2 × spread for a round trip — a deliberately conservative figure (Section 4.4.2) — and a trade whose target is less than about **five times** that cost is mostly paying the market maker (Section 4.4.6).

*Table 4.9 — The trading hurdle on €20,000*

| **ETF** | **Round-trip spread** | **In euros** | **Minimum target (5×)** | **Cost as a share of a +1% (€200) target** |
| :--- | :--- | :--- | :--- | :--- |
| AMEW.DE | 0.12% | €24 | about 0.6% | 12% |
| IPRP.L | 0.68% | €136 | about 3.4% | 68% |

A 1% swing in AMEW.DE is a reasonable trade; the same 1% in IPRP.L hands two-thirds of the gross gain to the spread before any commission.

**4.8.5 Step 5 — Add the broker commission.** At €5 per order, a round trip costs €10 more — 0.05% on €20,000. AMEW.DE's one-month cost rises from €30.33 to €40.33. Split the same €20,000 into ten €2,000 orders and the commission alone becomes 0.5% per order, larger than AMEW.DE's whole one-year ICS. Fewer, larger orders keep the ICS meaningful.

**4.8.6 Step 6 — Add what the ICS does not see.** Three checks before the final choice. **Tracking difference**: the fund's actual return minus its index over as many years as the history allows — 2,141 days for AMEW.DE, 4,477 for IPRP.L; a fund with a higher TER can still track better. **Currency**: IPRP.L is a London listing; check the currency it trades in and whether the share class is hedged, because an unhedged foreign-currency line adds exchange-rate risk that the ICS ignores. **Allocation limits**: IPRP.L is a real-estate basket, and Section 4.5.3's guideline of no more than about 20% of a prudent portfolio applies regardless of cost.

**4.8.7 Step 7 — Separate the choice of product from the timing.** The ICS is the same whether the price is rising or falling; it tells you *which* vehicle to use, not *when* to use it. The two charts make the point: AMEW.DE has climbed from about 590 in March 2026 to 698 and sits near its 1-year high; IPRP.L has fallen from a peak just above 3,000 in early 2026 to 2,340, its lowest level since spring 2025. Whether either is a buy today is a question for the trend and momentum tools of Part II — the moving averages of Chapter 10 (the SMA 10/21/50/200 buttons on the dashboard) and the ADX filter of Chapter 12 — not for the cost index.

**4.8.8 Step 8 — Monitor monthly, switch only when it pays.** Re-read the header once a month, not every day, and act on the triggers of Section 4.4.8: a spread widening more than 50% month on month, a competitor's TER cut, fund size below about €50M, or tracking difference well above the TER. A switch costs one sale and one purchase — about 2 × spread plus two commissions — so it is worth making only when the TER saving × years remaining exceeds that cost. For IPRP.L, a switch costs at least €136 on €20,000 in spread alone; a competitor would need to be 0.10% cheaper in TER to repay it in about seven years.

<table>
<thead>
<tr class="header">
<th><strong>▶ PROOF — What the eight steps show on two real dashboards</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>Inputs (header readings, 2026-09-24): AMEW.DE TER 0.38%, spread 0.06%; IPRP.L TER 0.59%, spread 0.34%. Cost over <em>t</em> years ≈ TER × <em>t</em> + 2 × spread; position €20,000; commission ignored unless stated.</p>
<p>Holding period changes which cost matters. The spread is 79% of AMEW.DE's one-month cost and 93% of IPRP.L's; at ten years the TER is 97% and 90%. The spread horizon (2 × spread ÷ TER) is about 4 months for AMEW.DE and about 14 months for IPRP.L — a trader in IPRP.L is paying mostly spread for over a year.</p>
<p>The trading hurdle separates the two. At five times the round-trip spread, AMEW.DE needs a target above about 0.6%, IPRP.L above about 3.4%. A +1% target costs 12% of the gain in AMEW.DE and 68% in IPRP.L before commission.</p>
<p>The headline ICS alone hides this. 0.51% and 1.28% look like "cheap" and "somewhat dearer"; restated for a one-month trade they are €30 and €146, a factor of almost five, and restated as a hurdle they decide whether a short-term trade is possible at all.</p>
<p>Result: AMEW.DE works both as a trading vehicle and as a long-term holding, and among MSCI World competitors the choice is decided by the break-even of Section 4.4.7. IPRP.L is an investing vehicle: hold it for years, where its TER dominates, and trade it only for moves well above 3.4% — or look for a competing property ETF with a tighter spread. In both cases the ICS chooses the product; the timing comes from the Part II indicators.</p></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td><p><strong>◈ KEY INSIGHT<br />
</strong></p>
<p><em>"ETF, ETC, and ETN are not three spellings of the same idea — they are three different answers to the question 'who is actually on the hook if this goes wrong,' and that answer is decided by the legal structure in Table 4.1, not by how similar the ticker or the price chart looks."</em></p></td>
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
<td><p>ETPs split into three legally distinct families — ETFs (funds, segregated assets), ETCs (securitized bonds, physically or synthetically backed), and ETNs (securitized bonds, full issuer credit risk) — and the family, not the ticker, determines who bears the loss if the issuer fails.</p>
<p>Replication method (full physical, sampled physical, synthetic unfunded, synthetic funded) is what actually determines counterparty risk, independent of the underlying being tracked.</p>
<p>The Synthetic Cost Index (ICS = TER + 2× average bid/ask spread) is the correct cost comparison across any set of ETPs tracking the same exposure — TER alone understates the true cost of trading in and out.</p>
<p>The ICS assumes a one-year hold: over any horizon the cost is TER × years + 2 × spread, so the spread decides for a trader and the TER for a long-term investor — on the chapter's €20,000 example the cheapest of three S&P 500 ETFs changes at about 5 and 15 months.</p>
<p>Delisting and reverse splits do not, by themselves, destroy an ETF or ETC investor's capital — both are typically paid out at NAV; an unsecured ETN's wind-down in an issuer-default scenario is the one structural exception, because it is a creditor claim rather than a fund payout.</p>
<p>Trading an ETF informed by the ICS follows eight steps: fix exposure and horizon, check the header arithmetic, restate cost for the horizon, clear the 5× round-trip hurdle, add commission, add what the ICS misses, separate the product choice from the timing, and monitor monthly. On the chapter's two dashboards a broad MSCI World ETF needs a target above about 0.6% to trade, a property ETF above about 3.4%.</p></td>
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
<td><p><strong>ETP (Exchange Traded Product)</strong> The umbrella category covering ETFs, ETCs, and ETNs.</p>
<p><strong>ETF (Exchange Traded Fund)</strong> A passively managed fund with segregated assets, protected from issuer default.</p>
<p><strong>ETC (Exchange Traded Commodity)</strong> A securitized bond tracking commodity futures or physical precious metals.</p>
<p><strong>ETN (Exchange Traded Note)</strong> A debt security tracking currencies, crypto-assets or leveraged/short indices; unsecured (issuer credit risk) or backed by collateral held through an SPV.</p>
<p><strong>NAV (Net Asset Value)</strong> The per-unit value of the fund's or product's underlying assets.</p>
<p><strong>TER (Total Expense Ratio)</strong> The annual management fee, accrued pro-rata daily from the product's assets.</p>
<p><strong>ICS (Synthetic Cost Index)</strong> TER plus twice the average bid/ask spread — the combined explicit-and-implicit cost comparison across ETPs.</p>
<p><strong>Bid/ask spread</strong> The gap between the best price to sell (bid) and the best price to buy (ask), in % of the price; paid once on entry and once on exit.</p>
<p><strong>XLM (Xetra Liquidity Measure)</strong> Deutsche Börse's round-trip trading cost in basis points for a set order size; enters the ICS without doubling.</p>
<p><strong>Break-even holding period</strong> The holding time at which two products' total costs (TER × years + 2 × spread) are equal.</p>
<p><strong>Tracking error</strong> The deviation between an ETP's return and the actual performance of its replicated benchmark.</p>
<p><strong>Reverse split</strong> Consolidation of existing units into fewer, higher-priced units, typically used when a price nears zero.</p>
<p><strong>Delisting</strong> Removal of a product from listing, typically with liquidation at final NAV.</p>
<p><strong>Trading hurdle</strong> The minimum target gain for a trade to be worth making — about five times the round-trip spread.</p>
<p><strong>Spread horizon</strong> The holding period at which the TER paid equals the round-trip spread (2 × spread ÷ TER, in years); below it the spread is the larger cost.</p></td>
</tr>
</tbody>
</table>

| **WHAT'S NEXT**                                                                                                                                                                                                                                                                                                                                                                                    |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Chapter 5 (Futures Trading) explains the contract under every commodity ETC — expiry, margin, and the futures curve — and Chapter 6 (ETCs and ETNs: Commodities, Curves, and Collateral) then takes the two ETP families this chapter mapped but did not trade: ETCs, whose return is the futures curve rather than the spot price, and ETNs, whose protection runs from physical collateral to none at all. The ICS, the replication-and-risk map, and the step-by-step trading discipline from Section 4.8 carry straight over. |

---

**Updated 2026-09-22** — Chapter 2 created by merging the English translations of the ETF, ETC, and ETN source chapters into a single main-sequence chapter, following the book's house style (matching the structure of Chapters 7–12). Placed in Part I — Investment Foundations and Instruments, with Chapter 1 (Investment Classes and Instruments) as its prerequisite, per the user's confirmed choice of the main-sequence format (digit box "Chapter 2," Prereqs line, "WHAT'S NEXT" closing footer) over the standalone-reference format used by Chapters 9–11. No renumbering of Chapters 7–12 was required, since the three source chapters had not previously been saved to the project under their own chapter numbers.

**Updated 2026-09-25** — Section 2.4 extended with material from `writing_plans/ICS_Trading_Guide.md`: 2.4.3 Reading the ICS by holding period (Figure 2.2), 2.4.4 Which spread to use (Table 2.3), 2.4.5 What the ICS leaves out, 2.4.6 A worked example: €20,000 in an S&P 500 ETF (Table 2.4), 2.4.7 Monitoring and switching, plus a WARNING box. Later tables renumbered 2.3–2.6 → 2.5–2.8; the 2.9 PROOF cost bullet, chapter summary and key terms updated.

**Updated 2026-09-26** — (1) Section 2.9 [PROOF] "Choosing Between Three ETPs on the Same Exposure" removed and replaced by "Trading an ETF Informed by the ICS — Step by Step" (from `writing_plans/ICS_Trading_Guide.md`): eight steps applied to two dashboards, AMEW.DE (Figure 2.3) and IPRP.L (Figure 2.4), both converted to light background; Tables 2.14–2.16; PROOF box on cost by horizon, spread horizon and trading hurdle. KEY INSIGHT kept. (2) ETN/crypto material from `etn-structures-and-crypto-etps.md` (first drafted for the abandoned Chapter 2-3 split) added as Sections 2.7.5–2.7.9 with Tables 2.8–2.12 and Listings 2.1–2.2 (`code_snippets/ch02/ch02_crypto_etn.py`); Table 2.1 ETN row, §2.3.3, §2.7.4 and the wind-down table (now 2.13, with a collateralized-ETN row) adjusted. Cross-references to the old §2.9 updated; summary and key terms extended.

**Updated 2026-09-26 (b)** — ETC strategies and dashboards added from `ETC_Strategies_and_Dashboards.md` as Sections 2.6.7–2.6.9 (Tables 2.7–2.8, carry-plus-trend rule); former Tables 2.7–2.18 renumbered 2.9–2.20 (in the 2026-09-26 note above, read Tables 2.8–2.16 as 2.10–2.18). New Section 2.10 [PROOF] "Reading the Curve and CFTC Positioning — Step by Step": BRNT.MI and COCO.MI dashboards (Figures 2.5–2.6, converted to light background), Tables 2.19–2.20, Listing 2.3 (`code_snippets/ch02/ch02_etc_carry_cot.py`). Cocoa's displayed annualized roll (−12.46%) corrected to −8.5% for the three-month Dec→Mar gap. Summary and key terms extended.

**Updated 2026-10-06** — Chapter split in two. This chapter keeps the three-family map, replication, risk map, ICS, ETFs in practice, delisting and the ICS trading PROOF (old §2.1–2.5, 2.8, 2.9 → §2.1–2.7); ETCs (old §2.6), ETNs (old §2.7) and the curve/CFTC PROOF (old §2.10) moved to Chapter 3 (ETCs and ETNs: Commodities, Curves, and Collateral). Tables, figures and listings renumbered in order of appearance; summary and key terms divided between the two chapters; new WHAT'S NEXT points to Chapter 3. Former Chapters 3–14 renumbered 4–15. Entries above use the pre-split numbering.

**Updated 2026-10-06 (c)** — Part label aligned with `.claude/CLAUDE.md` §3.3: Part I — Investing and Stock Market (Ch 1–9), Part II — Technical Analysis (Ch 10–15); "opens/closes Part …" sentences adjusted.

**Updated 2026-10-06 (e)** — Cross-references updated after Futures Trading moved to Chapter 3 and ETCs/ETNs to Chapter 4 (old Ch 3–6 → 4–7).

**Updated 2026-10-08 (reorder)** — Part I reordered: Stocks 5→2, Bonds+Intermarket 6→3, ETFs 2→4, Futures 3→5, ETCs/ETNs 4→6. Chapter, section, table, figure and listing numbers and all cross-references remapped; WHAT'S NEXT chain and Prereqs adjusted.

**Updated 2026-10-08 (ICS)** — New §4.4.1 "The ICS in plain words" (gym-fee / exchange-booth analogy) with Table 4.3 (ETF A vs B, €10,000, held 2 months / 1 year / 10 years); old §4.4.1–4.4.7 → 4.4.2–4.4.8, Tables 4.3+ → 4.4+; note in §4.4.2 that doubling the full quoted spread is a conservative estimate; research-firm name removed from the ICS definition (house rule 8).

**Updated 2026-10-08 (ICS figures)** — §4.4.1 gains Figure 4.2 (ICS formula as yearly fee + toll) and Figure 4.3 (ETF A vs B cost over holding period, break-even ≈ 10 months), B&W versions of the "ICS Explained" design; existing Figures 4.2–4.4 → 4.4–4.6.
