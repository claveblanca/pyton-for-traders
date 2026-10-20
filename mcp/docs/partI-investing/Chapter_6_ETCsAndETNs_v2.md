|                                                             |
| ----------------------------------------------------------- |
| **PYTHON FOR TRADERS: INVESTING, DERIVATIVES, AND TECHNICAL ANALYSIS APPLIED** |

|           |       |
| --------- | ----- |
| Chapter 6 | **6** |

**ETCs and ETNs: Commodities, Curves, and Collateral**

*How an ETC earns the futures return rather than the spot price — contango, backwardation, roll yield, and the strategies and positioning checks built on them — and how an ETN's protection runs from physical collateral to none at all, across currency, leveraged-index, and crypto notes*

Part I — Investing and Stock Market · Prereqs: Chapter 4 (Exchange Traded Products: Structure, Costs, and ETFs), Chapter 5 (Futures Trading)

<table>
<thead>
<tr class="header">
<th><strong>THIS CHAPTER COVERS</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>6.1 ETCs in Practice — Baskets, Leverage, Currency, Strategies, and Dashboards</p>
<p>6.2 ETNs in Practice — Currency, Leveraged Index, Collateral, and Crypto ETNs</p>
<p>6.3 [CODE] Hands-On — Crypto-ETN Data and the Carry/Positioning Filter</p>
<p>6.4 [PROOF] Reading the Curve and CFTC Positioning — Step by Step</p></td>
</tr>
</tbody>
</table>

|                                                                              |
| --------------------------------------------------------------------------------- |
| **6.1 ETCs IN PRACTICE — BASKETS, LEVERAGE, CURRENCY, STRATEGIES, AND DASHBOARDS**    |

Chapter 4 mapped all three ETP families (Table 4.1), the risk each one carries (Section 4.3), and the cost index used to compare them (Section 4.4); Chapter 5 explained the futures contract and its curve — cost of carry, contango, backwardation, and the roll (Section 5.2). This chapter takes the two families whose return is not simply the return of a basket of securities: **ETCs**, which hold futures and roll them for you, so they earn the futures return — roll yield included — rather than the spot price, and **ETNs**, whose protection depends on the issuer and on whatever collateral sits behind the note.

**6.1.1 Commodity baskets and Longer Dated ETCs.** Broad baskets — All Commodities, Agriculture/Grains/Softs, Livestock, Energy/Petroleum, Industrial Metals, Precious Metals — offer wide diversification within the asset class. **Longer Dated** ETCs deliberately position on the third available futures expiration rather than the first (where the contango slope is steepest), meaningfully dampening negative roll yield during strongly contangoed periods. **Hedged** variants strip out EUR/USD exposure so that performance reflects only the commodity's own move in its native currency.

*Table 6.1 — Commodity basket categories*

| **Basket** | **Typical coverage** |
| :--- | :--- |
| All Commodities | Energy, metals, and agricultural products (gold, oil, corn, copper) |
| Agriculture / Grains / Softs | Agricultural and soft commodities |
| Livestock | Cattle, hogs |
| Energy / Petroleum | WTI, Brent, natural gas, gasoline, heating oil |
| Industrial Metals | Copper, aluminum, zinc, nickel |
| Precious Metals | Gold, silver, platinum, palladium |

**6.1.2 Leverage, daily rebalancing, and volatility decay.** Leveraged (2x, 3x) and short (1x, 2x, 3x) ETCs reset and recalculate their multiplier at the close of every session. Compounded daily rebalancing produces **volatility decay** — a growing gap between the underlying's own return and the leveraged product's return in any choppy, non-trending market. The operating rule follows directly: leveraged and short ETCs are tactical, short-holding-period instruments, never a buy-and-hold position.

| **⚠ WARNING — Daily leverage is not "the same trade, bigger"**                                                                                                                                                                                                                                                                                                                        |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A 3x ETC held for a week in a range-bound market can lose money even if the underlying commodity is unchanged over that same week, purely from the compounding arithmetic of daily resets. The multiplier applies to each day's return, not to the cumulative move — treating a leveraged ETC as a bigger version of the unleveraged trade is the single most common way this instrument family surprises a buy-and-hold investor. |

**6.1.3 The EUR/USD effect.** Because almost all commodities trade in US Dollars, a Euro-based ETC holder is exposed to EUR/USD moves on top of the commodity's own price: a 1% Euro appreciation lowers the ETC's value by roughly 1%, and a 1% Euro depreciation raises it by roughly 1%. In leveraged ETCs, the multiplier applies only to the commodity's own move — **the currency effect always applies at 1x**, never leveraged alongside the commodity itself.

**6.1.4 Strategies that fit ETCs.** An ETC's return is the **futures return, not the spot price**, so the roll is part of every result. The strategies that suit ETCs therefore work with a small set of drivers — trend, curve shape, relative value, fundamentals, positioning and macro — rather than with the spot chart alone.

*Table 6.2 — Strategies that fit ETCs*

| **#** | **Strategy** | **Idea** | **Typical ETCs** | **Holding** | **See** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Trend following** | Long when the price is above its 200-day average and ADX confirms a trend; step aside otherwise. Commodities trend strongly because supply takes months or years to respond. | Oil, gold, copper, broad index | Weeks to months | Ch. 10, 12 |
| 2 | **Carry (curve shape)** | Prefer commodities in backwardation (positive roll yield); avoid those in steep contango, which cost money even when the price stands still. | Energy, agriculture | Months | §5.2.2 |
| 3 | **Momentum rotation** | Each month, rank the commodity ETCs by 3/6/12-month return, hold the top 2–3, drop the rest. | The whole commodity basket | Monthly | Ch. 3 |
| 4 | **Carry + trend combined** | Buy only what is trending up *and* not in steep contango, ranked by momentum — the filter that avoids an ETC that rises on the chart but loses to the roll. | Commodity basket | Monthly | §6.1.6, Ch. 10 |
| 5 | **Relative value (ratios)** | Trade a stretched spread between related commodities — gold/silver, Brent–WTI, copper/gold, corn/wheat: long one ETC, short or underweight the other. | Pairs from one sector | Days to weeks | §3.8, Ch. 11 |
| 6 | **Fundamentals / supply balance** | Low inventories against history (low stock-to-use) point to a tight market and backwardation; high inventories to surplus and contango. | Oil, gas, grains | Months | — |
| 7 | **Positioning (contrarian)** | When speculators hold an extreme net long or short in the weekly COT report, expect a reversal. | Oil, gold, grains | Weeks | §6.4, Ch. 11 |
| 8 | **Seasonality** | Recurring calendar patterns — natural gas into winter, grains around planting and harvest. A filter only, never a signal on its own. | Natural gas, grains | Weeks | — |
| 9 | **Macro / hedge** | Gold against real interest rates and the dollar; oil and broad commodities as an inflation hedge; copper as a growth gauge. | Gold, broad index, copper | Months to years | Ch. 3 |

Three rules apply to all of them. **Leveraged and short ETCs** are for short tactical trades only (days), because of volatility decay (Section 6.1.2). **Every cost goes into the backtest** — ICS, roll yield and EUR/USD (Sections 4.4, 5.2.2, 6.1.3); a strategy that works on the spot price can fail on the ETC. **Issuer exposure is spread**: an ETC is a debt of its issuer, so positions are spread across issuers, and physical ETCs are preferred for precious metals.

**6.1.5 Dashboards that support the analysis.** Six views cover the strategies above.

*Table 6.3 — Dashboards for ETC strategies*

| **Dashboard** | **Main view** | **Supports** | **Data (free unless noted)** |
| :--- | :--- | :--- | :--- |
| **A. Curve & roll monitor** | Futures curve today vs 1 and 3 months ago; annualized roll yield; contango/backwardation badge; ETC vs spot gap (the roll cost made visible) | 2, 4, 6 | Exchange settlement prices (view free); paid tick-data vendors for full history; front and second contracts from Yahoo Finance |
| **B. Trend & momentum board** | Heatmap of 1/3/6/12-month returns in EUR, trend state (200-day average), ADX, rank; combined score = momentum + roll yield | 1, 3, 4 | ETC prices (`yfinance`), EUR/USD (ECB) |
| **C. Fundamentals & positioning** | Inventories vs their 5-year range (crude, gasoline, natural-gas storage); grain stock-to-use; speculator net positioning as a percentile of its history | 6, 7, 8 | EIA API (inventories), USDA WASDE (grains), CFTC COT (`cot_reports` package) |
| **D. Ratio & spread monitor** | Gold/silver, Brent–WTI, copper/gold, corn/wheat ratios, each with its moving average and a ±2 z-score band | 5 | ETC or futures prices |
| **E. Macro drivers** | Gold vs US real 10-year yield (FRED `DFII10`) and the dollar index; oil vs inflation expectations (`T10YIE`); copper/gold vs the 10-year yield | 9, and the regime filter for 1–4 | FRED, ECB |
| **F. Position & cost tracker** | Per holding: days held, roll drag accumulated, ICS paid, leveraged-decay warning, exposure per ETC issuer | All, as a risk check | Your positions file + dashboard A |

They are used on three rhythms. **Monthly**, B and A pick *what* to hold (trend and carry), E confirms the macro backdrop and C explains *why* the curve looks the way it does. **Weekly**, D covers relative-value trades and C the COT update. **Daily**, F runs while positions are open, especially leveraged ones. Figures 6.1 and 6.2 in Section 6.4 show dashboards A and C combined with the ICS header of Section 4.4.

**6.1.6 A carry-plus-trend rule.** Strategy 4 joins the curve analysis of Section 5.2 with the trend tools of Chapters 10–12 and is simple enough to test:

1. **Universe:** one ETC per commodity group — energy, industrial metals, agriculture, gold, broad index.
2. **Filter:** price above its 200-day average **and** annualized roll yield better than −5%.
3. **Rank:** by 6-month return in EUR; hold the **top 3** with equal weights, and hold a euro money-market ETF (cash) for any slot left empty.
4. **Rebalance** monthly.
5. **Test:** backtest *with* roll and ICS against buy-and-hold of the broad commodity ETC, and walk-forward the thresholds rather than optimizing them on the whole history.

The −5% threshold and the top-3 choice are starting points to test, not proven values. Section 6.4 applies the filter by hand to two live ETCs and adds a positioning check.

|                                                                                       |
| ------------------------------------------------------------------------------------------ |
| **6.2 ETNs IN PRACTICE — CURRENCY, LEVERAGED INDEX, COLLATERAL, AND CRYPTO ETNs**      |

**6.2.1 The two currency-ETN structures.** A **Long Foreign Currency / Short Euro** ETN buys the foreign currency and sells the equivalent amount of Euro, profiting from the foreign currency's appreciation (a weakening Euro). A **Short Foreign Currency / Long Euro** ETN does the reverse, profiting from the foreign currency's depreciation (a strengthening Euro).

*Table 6.4 — Currency ETN direction and objective*

| **Structure** | **Mechanism** | **Profits from** |
| :--- | :--- | :--- |
| Long FX / Short EUR | Buy foreign currency, sell EUR | Foreign currency appreciating vs. EUR |
| Short FX / Long EUR | Sell foreign currency, buy EUR | Foreign currency depreciating vs. EUR |

**6.2.2 Leverage and the interest-rate differential.** Leveraged currency ETNs (3x, 4x, 5x) apply their multiplier directly to the exchange rate's *daily* percentage change. Whether the ETN also nets in overnight interest — effectively borrowing the short currency and depositing the long one — needs to be checked against the issuer's own documentation; when it does, the rate differential between the two currencies adds to or subtracts from the instrument's return independent of the spot move itself.

**6.2.3 The recommended alternative for currency diversification.** For an investor whose goal is currency diversification and opportunity rather than short-term tactical leverage, the more prudent route is to buy foreign equities or bonds directly, in their native currency, **without** hedging the exchange rate. This captures the same potential currency appreciation while also collecting the underlying security's real coupons or dividends — a return stream a leveraged currency ETN, by construction, does not provide.

**6.2.4 Leveraged equity and bond index ETNs.** Beyond currencies, ETNs are also the vehicle used for leveraged (3x, 5x) Long and Short exposure to equity and bond indices. The protection question from Section 6.2.6 applies without modification — many of these lines are swap-collateralized, bank-issued ones are unsecured: the leveraged exposure and the level of protection are two separate, independently-important facts about the same instrument.

**6.2.5 Collateralized ETNs — the securitization-style architecture.** An ETN is **not a securitization in the strict sense** — it is a debt security that tracks an index, not a claim on a pool of transferred loans. Many European ETNs and ETCs, however, borrow the securitization architecture: a **special purpose vehicle (SPV)**, usually domiciled in Ireland, Jersey or Luxembourg, issues the listed notes and holds **collateral** — physical metal, crypto-assets, or securities posted against swaps — segregated with a custodian or a **trustee** acting for noteholders. Table 6.5 sets the two side by side.

*Table 6.5 — Securitization (ABS) vs. collateralized ETN/ETC*

| **Feature** | **Securitization (ABS)** | **Collateralized ETN / ETC** |
| :--- | :--- | :--- |
| Issuer | SPV | Issuing SPV (often Irish, Jersey or Luxembourg) |
| What backs the notes | Transferred receivables (mortgages, loans) | Collateral: physical metal, crypto, securities backing swaps |
| Security issued | ABS notes | Listed notes (ETN/ETC) |
| Protection | Segregated assets (*ring-fencing*) | Collateral segregated with a custodian or trustee |
| Classes | Senior, mezzanine and junior tranches | **Single class** — all holders rank equally |
| Main risk | Default of the underlying borrowers | Collateral, swap counterparty, custodian |

**Where the analogy stops.** Four differences matter in practice:

- **No tranches.** There is no protected senior layer; losses hit all holders pro rata.
- **The underlying is a price, not credit.** Gold, copper or bitcoin carry market risk, not borrower default risk.
- **Continuous redemption.** Authorized participants create and redeem notes every day; an ABS instead amortizes with the cash flows of its receivables.
- **Similar structural risks.** The custodian, the swap counterparty, the trustee and the quality of the collateral decide what a holder recovers if something fails.

**6.2.6 Three levels of protection — physical, swap-collateralized, unsecured.** Listed notes can be ranked by what stands behind them, from the structure closest to a clean securitization to plain issuer debt.

*Notes backed by physical assets.* The SPV holds the asset itself. Invesco Physical Gold is issued by an Irish SPV, Invesco Physical Markets plc; each note is backed by allocated gold held in a vault, with a trustee acting for holders. Xetra-Gold is a bearer bond issued by Deutsche Börse Commodities GmbH, backed by physical gold held by Clearstream, and gives the right to physical delivery. Physical crypto ETNs (Section 6.2.8) follow the same model, with BTC or ETH in cold storage at a third-party custodian.

*Notes backed by swaps and collateral.* The return comes from contracts with bank counterparties, which post collateral to the SPV — the ETN equivalent of a synthetic ABS. WisdomTree Copper, issued by a WisdomTree vehicle in Jersey, works this way: if a counterparty defaults, the collateral is liquidated for the benefit of holders. The leveraged and short (3x, −3x) commodity and index lines of the same issuers use the same swap-plus-collateral structure.

*Unsecured notes.* Senior unsecured debt of a bank, with no collateral set aside. The iPath ETNs issued by Barclays (VXX on short-term VIX futures is the best known) and most US bank-issued ETNs are of this type, as are most bank-issued certificates and ETNs listed on European retail certificate segments. If the bank fails, the holder is an ordinary unsecured creditor.

*Table 6.6 — ETN protection levels*

| **Level** | **What backs the note** | **Typical examples** | **If the issuer fails** |
| :--- | :--- | :--- | :--- |
| Physical | Allocated metal or crypto held by a custodian, trustee for holders | Physical gold notes, physical crypto ETNs | Trustee realizes the asset for holders |
| Swap-collateralized | Collateral posted by swap counterparties | Commodity-index notes, 3x / −3x lines | Collateral liquidated for holders; recovery depends on its quality and haircut |
| Unsecured | Issuer's own balance sheet only | Bank-issued US ETNs, bank certificates | Ordinary unsecured creditor claim |

| **◆ EDGE — "ETN" names the legal form, not the level of protection** |
| -------------------------------------------------------------------- |
| Two notes can both be called ETNs while one is backed by vaulted gold under a trustee and the other by nothing but a bank's promise. Before sizing a position, place the product in one of the three rows of Table 6.6 — that row, not the label, sets the worst-case outcome. |

**6.2.7 Reading the prospectus — five collateral checks.** The base prospectus and the final terms of each series say which row of Table 6.6 a note belongs to. Five items decide it:

*Table 6.7 — Collateral checks in an ETN/ETC prospectus*

| **Check** | **What to look for** | **Why it matters** |
| :--- | :--- | :--- |
| Collateral type | Physical, government bonds, cash, equities | Equities or low-grade bonds lose value exactly when a counterparty is failing |
| Reset frequency and *haircut* | How often collateral is marked and topped up; the discount applied to its value | A daily reset with a haircut keeps coverage above 100%; a weekly reset can leave a gap |
| Custodian and trustee | Who holds the collateral and who acts for holders | The trustee enforces the security; the custodian's own soundness becomes a risk |
| *Limited recourse* clause | Repayment limited to the collateral of that series | Holders cannot claim against the issuer's other assets if the collateral falls short |
| Physical delivery | Whether holders can take delivery of the metal or coins | A delivery right ties the note directly to the asset |

| **▣ DATA — Add a collateral field next to the replication field** |
| ----------------------------------------------------------------- |
| A product table that stores only replication (physical / synthetic) misses issuer risk on notes. A second field, <code>collateral</code> with values <code>"physical"</code>, <code>"swap_collateralized"</code> or <code>"unsecured"</code>, captures it — one column per row of Table 6.6 — and lets a screener filter out unsecured notes in one line. |

**6.2.8 Crypto ETNs — notes, not funds.** Europe is the reference market for exchange-traded crypto products, with hundreds of listings on Xetra, SIX, Euronext and the London Stock Exchange. Technically they are **notes issued by an SPV**, not UCITS funds, so everything in Sections 6.2.5 to 6.2.7 applies to them. Most are physically backed: the SPV holds the coins in cold storage with a third-party custodian, and each note carries a fixed **coin entitlement** that shrinks a little every day as the management fee is taken in coins.

*Physical and synthetic in the same family.* The same issuer group can run both structures. Table 6.8 lists the main bitcoin notes; CoinShares Bitcoin Tracker Euro (ISIN SE0007525332) is a **synthetic** certificate even though CoinShares also issues a physical note.

*Table 6.8 — Main European bitcoin ETNs*

| **Product (ticker)** | **Issuer / SPV** | **Structure** |
| :--- | :--- | :--- |
| Bitwise Physical Bitcoin (BTCE) | Bitwise Europe (formerly ETC Group) | Physical, BTC in custody |
| CoinShares Physical Bitcoin (BITC) | CoinShares Digital Securities (Jersey) | Physical |
| 21Shares Bitcoin Core (CBTC) | 21Shares AG (Zurich) | Physical |
| WisdomTree Physical Bitcoin (BTCW) | WisdomTree Issuer X (Jersey) | Physical |
| Invesco Physical Bitcoin (BTIC) | Invesco (Irish SPV) | Physical |
| CoinShares Bitcoin Tracker Euro (COINXBE) | CoinShares XBT Provider AB (Stockholm) | **Synthetic**, certificate |

Identify each product by ISIN from the issuer's own product page or KID before using it in code; tickers differ by exchange.

*Proof of reserves.* For a physical note the question is whether the coins exist. CoinShares (with reserves verified by an independent attestation firm), 21Shares and Bitwise publish proof-of-reserves portals; where the custodian's wallet addresses are public, the holdings can be read directly on-chain and compared with units outstanding × coin entitlement.

| **⚠ WARNING — The note trades on exchange hours, the coin never stops** |
| ----------------------------------------------------------------------- |
| A crypto ETN listed on Xetra trades only during exchange hours, while bitcoin trades around the clock. Over a weekend the underlying can move sharply with no trading in the note, and the note gaps at Monday's open. Any premium/discount calculation must use the spot price at the same timestamp as the note's price — a 17:30 CET close against a midnight UTC spot print produces a false premium. |

**6.2.9 Crypto ETN data — there is no issuer API.** No crypto ETN issuer exposes a documented REST API; they publish product pages, PDFs and Excel files. Table 6.9 lists the practical sources.

*Table 6.9 — Data sources for crypto ETNs*

| **Data** | **Source** | **Access** |
| :--- | :--- | :--- |
| Listing price, volume, history | Yahoo Finance via `yfinance` (e.g. `BTCE.DE`) | Free, unofficial |
| ISIN → ticker and exchange | OpenFIGI mapping API | Free: 25 requests/min without a key, 25 per 6 s with a free key; up to 100 ISINs per request |
| NAV / fair value, AUM, coin entitlement | Issuer product pages | HTML scraping |
| Product lists with data | Issuer downloads (e.g. 21Shares product Excel file) | Downloadable file |
| Proof of reserves | Issuer portals; public custodian addresses on-chain | Portal / blockchain explorer |
| Underlying spot price | CoinGecko API, Kraken or Binance public APIs, `ccxt` | Free |
| Weekly aggregate flows | CoinShares *Digital Asset Fund Flows* weekly report | PDF / blog, no API |
| Institutional NAV, flows, holdings | Commercial data vendors | Paid |

*Mapping ISINs to tickers* is the first step before pulling prices; Listing 6.1 (Section 6.3.1) does it through the OpenFIGI API.

| **⚙ TOOL — OpenFIGI** |
| --------------------- |
| A free mapping service from identifiers (ISIN, CUSIP, ticker) to FIGI records carrying ticker, exchange code and security name. Without a key the limit is 25 requests per minute; a free key raises it to 25 per 6 seconds. Pass the key in the <code>X-OPENFIGI-APIKEY</code> header. |

*Premium/discount to NAV.* For a physical note, the fair value of one note is its coin entitlement times the spot price:

$$\text{Premium} = \frac{\text{Listing price}}{\text{Coin entitlement per note} \times \text{Spot}} - 1$$

A persistent premium points to retail demand the market makers are not arbitraging away quickly — a usable sentiment reading. Use the issuer's daily entitlement, not a constant: it falls by the annual fee spread over the year.

*Flows in coins, not euros.* Units outstanding × coin entitlement gives the coins the SPV holds. The daily change in that number is the flow — cleaner than a flow derived from AUM, which moves with the coin price even when no note is created or redeemed. Listing 6.2 (Section 6.3.2) computes the premium, its z-score and the coin flow.

*Positioning without a European COT.* There is no Commitments of Traders report for European crypto notes. The CFTC does publish the *Traders in Financial Futures* report for **CME Bitcoin and Ether futures**, which serves as the positioning indicator alongside the ETN flows.

|                                                                                     |
| ----------------------------------------------------------------------------------- |
| **6.3 [CODE] HANDS-ON — CRYPTO-ETN DATA AND THE CARRY/POSITIONING FILTER**          |

Three listings turn the chapter's data rules into code: the ISIN mapping and crypto-note signals of Section 6.2.9, then the carry, positioning and combined filter of Sections 6.1.4–6.1.6 that the PROOF applies step by step.

**6.3.1 ISIN to exchange tickers (Section 6.2.9).**

**💻 PYTHON · Listing 6.1 — `isin_to_tickers`: ISIN to exchange tickers via OpenFIGI**

```python
import pandas as pd
import requests

def isin_to_tickers(isins, api_key=None):
    """ISIN -> exchange tickers via OpenFIGI (at most 100 ISINs per call)."""
    headers = {"X-OPENFIGI-APIKEY": api_key} if api_key else {}
    jobs = [{"idType": "ID_ISIN", "idValue": i} for i in isins]
    r = requests.post("https://api.openfigi.com/v3/mapping",
                      json=jobs, headers=headers, timeout=30)
    r.raise_for_status()
    return pd.DataFrame([{"isin": i, "ticker": d.get("ticker"), "exch_code": d.get("exchCode")}
                         for i, res in zip(isins, r.json()) for d in res.get("data", [])])
```

Full version, with self-test: `code_snippets/v1/ch06_etc_etn/ch06_crypto_etn_premium.py`.

**6.3.2 Premium, z-score and coin flows (Section 6.2.9).**

**💻 PYTHON · Listing 6.2 — `crypto_etn_signals`: premium/discount, z-score, and coin flows**

```python
def crypto_etn_signals(df, window=20, z_entry=2.0):
    """df, one row per day: close, spot (EUR), coin_per_note, units."""
    out = pd.DataFrame(index=df.index)
    out["premium"] = df["close"] / (df["coin_per_note"] * df["spot"]) - 1
    out["flow_coins"] = (df["units"] * df["coin_per_note"]).diff()     # coins in / out
    stats = out["premium"].rolling(window)
    out["premium_z"] = (out["premium"] - stats.mean()) / stats.std()
    out["retail_demand"] = out["premium_z"] > z_entry
    return out
```

Full version, with self-test: `code_snippets/v1/ch06_etc_etn/ch06_crypto_etn_premium.py`.

**6.3.3 Carry, positioning and the combined filter (Sections 6.1.4–6.1.6).**

**💻 PYTHON · Listing 6.3 — `roll_yield`, `cot_score` and `etc_signal`: carry, positioning and the combined filter**

```python
def roll_yield(front, nxt, months_between):
    """Per-roll and annualized roll yield of a long position (+ backwardation, - contango)."""
    per_roll = front / nxt - 1
    return per_roll, (1 + per_roll) ** (12 / months_between) - 1

def cot_score(net, window=156):
    """Percentile (0-100) and z-score of managed-money net positioning over 3 years."""
    hist, last = net.tail(window), net.iloc[-1]
    return round((hist < last).mean() * 100), round((last - hist.mean()) / hist.std(), 2)

def etc_signal(roll_annual, above_200d, cot_pct, min_carry=-0.05, crowded=90):
    if roll_annual < min_carry:
        return "AVOID - contango cost"
    if not above_200d:
        return "STAND ASIDE - no uptrend"
    return "LONG, REDUCED SIZE - crowded" if cot_pct >= crowded else "LONG"
```

Full version, with self-test: `code_snippets/v1/ch06_etc_etn/ch06_carry_trend_screen.py` (with `roll_yield` in `ch05_futures/ch05_curve_roll.py`).

The PROOF that follows applies these three functions by hand to two ETCs on the same day.

|                                                                                     |
| ----------------------------------------------------------------------------------- |
| **6.4 [PROOF] READING THE CURVE AND CFTC POSITIONING — STEP BY STEP**              |

Section 6.1 explained why an ETC holder earns the futures return, and Section 6.1.6 set out a carry-plus-trend rule. This section applies both, plus a positioning check, to two dashboards read on 26 September 2026: **BRNT.MI** (WisdomTree Brent Crude Oil, energy) and **COCO.MI** (WisdomTree Cocoa, agriculture). Each dashboard combines three panels: the ETC's ICS header (Section 4.4), a term-structure and roll-yield monitor (dashboard A in Table 6.3), and a CFTC managed-money positioning strip by sector (dashboard C).

![ETC dashboard — BRNT.MI WisdomTree Brent Crude Oil: backwardation, roll 7.06% per period, CFTC positioning by sector](../images/ETC_dashboard_BRNT_2026-09_light.png)

*Figure 6.1 — ETC dashboard for BRNT.MI (WisdomTree Brent Crude Oil, ISIN JE00B78CGV99), 26 September 2026. Left: ETC list and term-structure panel (BACKWARDATION; front BZX26 at 104.32, next BZZ26 at 97.44; roll 7.06% per period, 126.76% annualized). Top right: CFTC managed-money positioning by sector (score and z-score). Right: ICS header (TER 0.49%, spread 3.99%, ICS 8.48%) and 1-year chart, last 88.60.*

![ETC dashboard — COCO.MI WisdomTree Cocoa: contango, roll −2.19% per period, CFTC positioning by sector](../images/ETC_dashboard_COCO_2026-09_light.png)

*Figure 6.2 — ETC dashboard for COCO.MI (WisdomTree Cocoa, ISIN JE00B2QXZK10), 26 September 2026. Term structure: CONTANGO; front CCZ26 at 5,619, next CCH27 at 5,745, M3 CCK27 at 5,818; roll −2.19% per period, −12.46% annualized as displayed; the M1→M6 curve rises to M4–M5 and dips at M6 (5,791). ICS header: TER 0.49%, spread 6.24%, ICS 12.96%; last 7.91.*

**6.4.1 Step 1 — Read the curve badge and check the per-roll number.** The badge says which way the curve slopes between the front and next contracts. The per-roll yield for a long holder is front ÷ next − 1: selling the expiring contract and buying the next one gains when the next is cheaper (backwardation) and loses when it is dearer (contango).

- Brent: 104.32 ÷ 97.44 − 1 = **+7.06%** per roll — backwardation.
- Cocoa: 5,619 ÷ 5,745 − 1 = **−2.19%** per roll — contango.

The per-roll figure assumes the curve keeps its shape until the next roll, so that the next contract drifts up (or down) to the front price. It is a carry reading, not a forecast of the price.

**6.4.2 Step 2 — Annualize by the real gap between expiries.** Annualized roll = (1 + per-roll)^(12 ÷ months between expiries) − 1. Brent lists a contract every month, so the gap is one month: 1.0706¹² − 1 = **126.8%**, matching the dashboard. Cocoa lists March, May, July, September and December; the roll from December (CCZ26) to March (CCH27) spans **three months**, so the correct figure is 0.9781⁴ − 1 = **−8.5%** a year. The dashboard's −12.46% is 0.9781⁶ − 1, which assumes a two-month gap. Always check which gap the tool uses — on quarterly or irregular cycles the annualized number can be off by half.

**6.4.3 Step 3 — Look at the whole curve, not just M1 and M2.** The M1→M6 panel shows where later rolls will land. Cocoa's curve rises from 5,619 (M1) to a peak around M4–M5 and then falls to 5,791 at M6: contango at the front, a slight backwardation further out. A standard ETC rolling at the front pays the steep part; a Longer Dated ETC (Section 6.1.1) would roll on a flatter segment. Brent's very steep front backwardation (6.9 dollars between two consecutive months) is the signature of a tight prompt market — the supply-balance reading of strategy 6 in Table 6.2.

**6.4.4 Step 4 — Apply the carry filter.** The rule of Section 6.1.6 requires an annualized roll better than −5%. Brent passes by a wide margin. Cocoa fails at −8.5% (and at the displayed −12.46%): holding it long costs about 8–9% a year in roll alone, before any price move.

**6.4.5 Step 5 — Apply the trend filter.** Switch on the SMA 200 button and check whether the ETC's price is above its 200-day average (Chapter 10). Brent's ETC has risen from about 40 to 88.60 over the year and is trading near its 1-year high. Cocoa's has recovered from about 4 to 7.91 after a long decline and has pulled back from about 9. The filter is read on the ETC's own price — the price the holder actually earns, roll included — not on the futures contract.

**6.4.6 Step 6 — Check CFTC managed-money positioning.** The CFTC's weekly Commitments of Traders report (Disaggregated) splits futures open interest by trader type; **managed money** — hedge funds and commodity trading advisers — is the speculative, trend-following group. The dashboard turns each sector's net position (longs − shorts) into a 0–100 score against its own history and a z-score:

*Table 6.10 — CFTC managed-money positioning, 26 September 2026*

| **Sector** | **Score** | **z** | **Dashboard reading** |
| :--- | :--- | :--- | :--- |
| Commodities (broad) | 74 | 0.84 | Elevated spec long |
| Energy | 40 | −0.11 | Neutral positioning |
| Precious metals | 74 | 0.22 | Elevated spec long |
| Industrial metals | 96 | 1.35 | Crowded long (contrarian caution) |
| Agriculture | 95 | 1.89 | Crowded long (contrarian caution) |

Read it as contrary opinion (Chapter 11), not as a signal on its own: when speculators are already heavily long, there are few buyers left and many potential sellers if the trend stalls. A practical scale is a score of 90 or more (or z above +1.5) = crowded long; 10 or less (or z below −1.5) = crowded short; in between = no positioning objection. Energy at 40 raises no objection to a Brent long; agriculture at 95 (z 1.89) warns against adding to a cocoa long. The report reflects Tuesday's positions and is published the following Friday, so it lags the market by three days; open the dashboard's Methodology panel to see the history window behind the score.

**6.4.7 Step 7 — Put the costs next to the carry.** Both headers show wide spreads on these Milan listings — 3.99% for Brent and 6.24% for cocoa — giving ICS readings of 8.48% and 12.96% (0.49 + 2 × 3.99 = 8.47 and 0.49 + 2 × 6.24 = 12.97, rounding apart). A single live snapshot is unreliable in both directions, and on a thin listing like these it can overstate the typical spread (Section 4.4.5); at face value Brent's round trip (about 8%) would need a target of about 40% to clear the 5× hurdle of Section 4.8.4. Before trading, check the monthly average spread and the same product on another exchange; a carry signal worth 7% per roll is worth little if the entry and exit cost 8%. Add the EUR/USD effect as well (Section 6.1.3): both contracts are priced in dollars.

**6.4.8 Step 8 — Decide and set the exit conditions.**

*Table 6.11 — Decision for the two ETCs*

| **Check** | **BRNT.MI (Brent)** | **COCO.MI (Cocoa)** |
| :--- | :--- | :--- |
| Curve | Backwardation, +7.06% per roll | Contango, −2.19% per roll |
| Annualized roll (correct gap) | +126.8% | −8.5% |
| Carry filter (> −5%) | Pass | Fail |
| Trend filter (price > 200-day) | Check on SMA 200 — near 1-year high | Check on SMA 200 |
| Sector positioning | Energy 40 — neutral | Agriculture 95 — crowded long |
| Cost (ICS, live snapshot) | 8.48% — check other listings | 12.96% — check other listings |
| Decision | Candidate long, via a listing with a normal spread | Avoid; if bullish, a Longer Dated ETC and reduced size |

Exit, or re-examine, when any input changes: the curve flips to contango worse than −5% a year, the sector score reaches the crowded zone, or the price closes below its 200-day average. Re-read the curve weekly and the COT every Friday.

Run through Listing 6.3 (Section 6.3.3): `roll_yield(104.32, 97.44, 1)` returns (0.0706, 1.2676) and `roll_yield(5619, 5745, 3)` returns (−0.0219, −0.0849). The net-position series for `cot_score` comes from the managed-money long and short columns of the CFTC Disaggregated futures report, which the `cot_reports` package downloads by year.

<table>
<thead>
<tr class="header">
<th><strong>▶ PROOF — What the curve and positioning say about two ETCs on the same day</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>Inputs (dashboards, 26 September 2026): Brent front 104.32, next 97.44, one-month gap, energy managed-money score 40; cocoa front 5,619, next 5,745, three-month gap, agriculture score 95 (z 1.89).</p>
<p>Carry. Brent's roll earns +7.06% per roll, +126.8% annualized while the curve holds; cocoa's roll costs −2.19% per roll, −8.5% annualized. On a flat price a year of cocoa rolls loses about 8.5% — the carry-plus-trend rule rejects it before the chart is even read.</p>
<p>Annualization check. The dashboard's −12.46% for cocoa assumes six rolls a year; with the actual three-month gap between December and March it is −8.5%. A tool that annualizes every curve monthly overstates carry on quarterly cycles by about half.</p>
<p>Positioning. Energy speculators are neutral (score 40), so nothing argues against a Brent long; agriculture is crowded long (95), so a cocoa long would join a trade most speculators already hold — contrarian caution even if the carry were positive.</p>
<p>Cost. The live spreads (3.99% and 6.24%) outweigh a single Brent roll gain; the carry signal is only usable through a listing whose average spread is a fraction of a percent.</p>
<p>Result: Brent is a candidate long — positive carry, neutral positioning, trend to confirm on the 200-day average — provided it is bought through a liquid listing. Cocoa is avoided on carry alone and flagged on positioning. The three numbers that decided it — per-roll yield, the gap between expiries, and the sector positioning score — are all on the dashboard, but only one of them, the annualized roll, needed correcting before use.</p></td>
</tr>
</tbody>
</table>

<table>
<tbody>
<tr class="odd">
<td><p><strong>◈ KEY INSIGHT<br />
</strong></p>
<p><em>"An ETC pays you the futures curve, not the price on the chart, and an ETN pays you only what its issuer and its collateral can honor — read the curve and the prospectus before you read the price."</em></p></td>
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
<td><p>Contango produces negative roll yield and backwardation produces positive roll yield for a long ETC position — natural gas's steep contango can cost a long holder over 14% in 3-4 months on roll alone, with the spot price unchanged.</p>
<p>ETC strategies work on the futures return, not the spot price: trend, carry (curve shape), momentum rotation, carry + trend, ratios, supply balance, positioning, seasonality and macro. A carry-plus-trend rule — price above its 200-day average and annualized roll better than −5%, top 3 by 6-month return, monthly rebalance — is the simplest to test, with roll, ICS and EUR/USD in the backtest.</p>
<p>Reading an ETC before trading takes eight steps: curve badge and per-roll yield (front ÷ next − 1), annualization by the real gap between expiries, the whole M1–M6 curve, the carry filter, the 200-day trend filter, CFTC managed-money positioning (score ≥ 90 = crowded), costs, and exit conditions. On 26 September 2026 Brent passed (+7.06% per roll, energy positioning neutral) and cocoa failed (−8.5% a year in roll, agriculture crowded long).</p>
<p>Leveraged and short ETCs/ETNs reset daily, producing volatility decay in non-trending markets — they are tactical, short-holding-period instruments, never buy-and-hold.</p>
<p>An ETN's protection ranges from physical assets held for holders, through swap collateral, to none at all; five prospectus items place a note in its level — collateral type, reset and haircut, custodian and trustee, limited recourse, physical delivery.</p>
<p>European crypto ETNs are SPV notes, mostly physically backed; premium/discount to NAV (listing price ÷ coin entitlement × spot − 1) and coin flows (units × entitlement) are the two data series worth building, with CME futures COT for positioning.</p>
<p>Currency ETNs let a trader go long or short a foreign currency against the Euro with leverage, but the more prudent route to currency diversification is usually unhedged direct ownership of the foreign security itself.</p></td>
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
<td><p><strong>ETC (Exchange Traded Commodity)</strong> A securitized bond tracking commodity futures or physical precious metals.</p>
<p><strong>ETN (Exchange Traded Note)</strong> A debt security tracking currencies, crypto-assets or leveraged/short indices; unsecured (issuer credit risk) or backed by collateral held through an SPV.</p>
<p><strong>Cost of carry</strong> Storage, preservation, insurance, and financing costs borne by a holder of the physical commodity.</p>
<p><strong>Contango</strong> A forward curve where longer-dated futures trade above near-dated ones — produces negative roll yield for a long position.</p>
<p><strong>Backwardation</strong> A forward curve where near-dated futures trade above longer-dated ones — produces positive roll yield for a long position.</p>
<p><strong>Roll yield</strong> The gain or loss from selling an expiring futures contract and buying the next one out.</p>
<p><strong>Volatility decay</strong> The performance gap between a leveraged product and its underlying, caused by daily compounding in a non-trending market.</p>
<p><strong>Term structure</strong> The prices of successive futures expirations (M1, M2, … M6) at one moment; its slope defines contango or backwardation.</p>
<p><strong>Carry</strong> The return from holding a futures position while the curve keeps its shape — for a long ETC, the roll yield.</p>
<p><strong>COT (Commitments of Traders)</strong> The CFTC's weekly report of futures positions by trader type, reflecting Tuesday's positions and published on Friday.</p>
<p><strong>Managed money</strong> The COT category for hedge funds and commodity trading advisers — the speculative, mostly trend-following positions.</p>
<p><strong>SPV (Special Purpose Vehicle)</strong> A company set up only to issue a series of notes and hold the assets or collateral behind them.</p>
<p><strong>Haircut</strong> The discount applied to a collateral asset's market value when measuring how much of the exposure it covers.</p>
<p><strong>Trustee</strong> The party that holds the security over the collateral and acts for noteholders if the issuer or a counterparty defaults.</p>
<p><strong>Limited recourse</strong> A clause limiting holders' repayment to the collateral of their own series.</p>
<p><strong>Coin entitlement</strong> The quantity of crypto-asset each note represents, reduced daily by the management fee.</p>
<p><strong>Proof of reserves</strong> An issuer's published evidence, often attested or verifiable on-chain, that the coins backing its notes are held.</p>
<p><strong>Premium/discount to NAV</strong> The gap between a product's listing price and the value of its holdings at the same timestamp.</p></td>
</tr>
</tbody>
</table>

| **WHAT'S NEXT**                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| This chapter closes the instrument-selection chapters of Part I — Investing and Stock Market (Chapters 4–6). Together with Chapters 1–3, they establish the five asset-class pillars and the practical vehicles (mutual funds, Sicav, ETFs, ETCs, ETNs) used to access them; the ICS cost framework and its step-by-step trading use, the replication-method and collateral risk map, the contango/backwardation mechanics and the CFTC positioning check introduced here recur throughout the rest of the book wherever a specific instrument choice needs to be justified quantitatively rather than assumed. Chapter 7 (Options Trading) moves to the last derivative of Part I, carrying over the leverage and sizing discipline of Chapter 5. |


---

**Updated 2026-10-06** — Chapter created by splitting the former Chapter 2 (Exchange Traded Products). Contains old §2.6 (ETCs), §2.7 (ETNs) and §2.10 [PROOF] (curve and CFTC positioning), renumbered §3.1–3.3, with their tables, figures and listings renumbered in order of appearance. New: opening bridge paragraph in §3.1, KEY INSIGHT, chapter summary and key terms drawn from the former Chapter 2, Prereqs pointing to Chapter 2. History of this material before the split is in Chapter 2's update notes.

**Updated 2026-10-06 (c)** — Part label aligned with `.claude/CLAUDE.md` §3.3: Part I — Investing and Stock Market (Ch 1–9), Part II — Technical Analysis (Ch 10–15); "opens/closes Part …" sentences adjusted.

**Updated 2026-10-06 (e)** — Renumbered from Chapter 3 to Chapter 4. Curve theory (old §3.1.1–3.1.3, Table 3.1) moved to Chapter 3 §3.2; §4.1 retitled (Baskets, Leverage, Currency, Strategies, and Dashboards) with a new bridge paragraph; Prereqs add Ch 3; WHAT'S NEXT → Ch 5 Stocks. Code listings trimmed (76 → 37 lines), full versions in code_snippets/ch02/.

**Updated 2026-10-08 (reorder)** — Part I reordered: Stocks 5→2, Bonds+Intermarket 6→3, ETFs 2→4, Futures 3→5, ETCs/ETNs 4→6. Chapter, section, table, figure and listing numbers and all cross-references remapped; WHAT'S NEXT chain and Prereqs adjusted.

**Updated 2026-10-08 (ICS)** — Cross-reference to Chapter 4 updated (§4.4.4 → §4.4.5 after the new §4.4.1); arithmetic typo fixed in §6.3.7: 0.49 + 2 × 3.99 = 8.47 (was "2 × 4.99").
