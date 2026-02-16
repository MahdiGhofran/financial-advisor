# Personal Financial Advisor — Gold & Currency Analytics for the Iranian Market

> **A real-time, algorithmic decision-support system for personal investment in Iran's gold, coin, and foreign-exchange markets.**

Built with **Streamlit** and powered by live data from [Bonbast.com](https://bonbast.com), [GoldPrice.org](https://goldprice.org), the [ECB Frankfurter API](https://api.frankfurter.dev), and the [World Bank Open Data API](https://data.worldbank.org/), this tool provides quantitative buy/sell signals, portfolio analytics, and risk-managed investment guidance — all tailored to the unique structure of Iran's parallel (free-market) currency and bullion markets.

---

## Context & Motivation

Iran operates a **multi-tier exchange-rate regime** where the Central Bank of Iran (CBI) administered rate, the NIMA platform rate, and the free-market ("open") rate can diverge significantly. Retail investors buying gold coins, melted gold, or foreign currency in the open market face:

- **Coin premiums ("bubble")** that fluctuate independently of the underlying gold content.
- **Melted-gold spreads** where the domestic _Mazaneh_ (benchmark quote) can deviate from the theoretical value derived from the international ounce price.
- **Currency mis-pricings** caused by sanctions-related friction, liquidity constraints, and speculative flows.
- **AED-USD parity gaps** where the free-market dollar price diverges from the value implied by the Dirham — the primary forex conduit for Iranian trade (~85% of Iran's foreign exchange flows transit through the UAE).

This tool quantifies each of these inefficiencies, generates tiered signals, and delivers actionable, risk-managed recommendations — designed for personal use, **not** institutional trading.

---

## Features at a Glance

| Tab | Purpose |
|-----|---------|
| **Dashboard** | Unified view: 4 simultaneous signal channels (coin, melted gold, dollar/inflation, dollar/Dirham) + combined recommendation |
| **Coin Bubble** | Intrinsic-value vs. market-price analysis for Emami, Half, Quarter, and Gerami coins |
| **Melted Gold** | Formula-A theoretical pricing vs. live _Mazaneh_ — best buy/sell timing |
| **Dollar Analysis** | Inflation-differential real-value model with 6-tier buy/sell zones |
| **Dirham-Dollar Signal** | AED-peg cross-rate arbitrage + multi-currency consensus + spread analysis |
| **Calculator** | 18K gold pricing, _Mazaneh_-to-gram conversion, mixed-karat valuation |
| **Currency Exchange** | Cross-rate premiums for 7 currencies + weekly trend from ECB data |
| **Portfolio** | Holdings tracker, sector allocation, 10-rule smart advisor engine, 12-month projection |
| **DCA Planner** | Dollar Cost Averaging — record past purchases or generate forward plans |
| **Roadmap** | Phase-by-phase investment plan with risk management rules |

---

## Data Sources

| Source | Data | Update Interval | Method |
|--------|------|-----------------|--------|
| [Bonbast.com](https://bonbast.com) | USD, EUR, GBP, CHF, TRY, AED, CAD, CNY (buy/sell), gold coins, melted gold, 18K gold | 5 min cache | `bonbast` Python package (token + API) |
| [GoldPrice.org](https://data-asg.goldprice.org) | XAU/USD spot price, daily change | 5 min cache | REST JSON |
| [ECB Frankfurter](https://api.frankfurter.dev) | EUR, GBP, CHF, TRY, AED, CAD, CNY vs. USD — spot + 7-day history | 5 min / 10 min cache | REST JSON |
| [World Bank](https://api.worldbank.org) | Iran annual CPI inflation (supplementary) | 24 hr cache | REST JSON |
| **Central Bank of Iran (CBI)** | Point-to-point inflation rates (hardcoded verified defaults) | Manual / sidebar override | Hardcoded + user input |

All prices are denominated in **Iranian Tomans** (1 Toman = 10 Rials).

---

## Algorithms & Formulas

### 1. Coin Intrinsic Value & Bubble Percentage

Each Iranian gold coin has a known **fine gold weight** (in grams). The intrinsic value strips away the collector/minting premium:

```
Intrinsic = (Ounce_USD × Dollar_Toman × Weight_g × 0.9) / 31.1035 + Minting_Cost
```

| Coin | Fine Weight (g) | Minting Cost (T) |
|------|----------------|-------------------|
| Emami (Full) | 8.133 | 7,000 |
| Half | 4.065 | 7,000 |
| Quarter | 2.032 | 7,000 |
| Gerami (1g) | 1.000 | 7,000 |

**Bubble percentage:**

```
Bubble% = (Market_Price / Intrinsic_Value − 1) × 100
```

**Signal thresholds:**

| Bubble % | Signal | Action |
|----------|--------|--------|
| < 13% | BUY | Coin is near intrinsic — accumulate |
| 13–25% | WAIT | Normal premium — hold |
| > 25% | SELL | Excessive premium — liquidate to melted gold or USD |

### 2. Melted Gold — Formula A (Theoretical Mazaneh)

The _Mazaneh_ is the per-_mithqal_ benchmark used in Iran's gold bazaar. Its theoretical value is:

```
A = Dollar_Toman × Ounce_USD × 0.1045
```

The constant `0.1045` is the empirical conversion factor from troy-ounce-dollar space to the Iranian _mithqal_ pricing convention (1 mithqal ≈ 4.6083 grams; combined with bazaar markup conventions).

**Deviation:**

```
Deviation% = (Mazaneh_Market − A) / A × 100
```

| Deviation % | Signal | Action |
|-------------|--------|--------|
| < 1% | BUY | Melted gold near fair value — best entry |
| 1–3% | WAIT | Normal range |
| 3–5% | WAIT | Expensive — patience |
| > 5% | SELL | Significantly overpriced — exit |

### 3. 18-Karat Gold Theoretical Price

```
Price_18K_per_gram = (Ounce_USD × Dollar_Toman) / 31.1035 × 0.75
```

The factor `0.75` represents the 18/24 purity ratio. Comparing this with the live bazaar 18K price reveals the domestic premium.

### 4. Dollar Real Value — Inflation-Differential Model

Since US inflation is negligible relative to Iran's (typically 30–50% annually), the real value of the dollar in Tomans compounds at approximately the Iranian CPI rate:

**Completed years (annual compounding):**

```
V(N) = V(N−1) × (1 + π_N)
```

Where `π_N` is the CBI-reported annual point-to-point inflation rate for Jalali year `N`.

**Current year (partial-year interpolation):**

```
V_now = V(Y−1) × (1 + π_p2p × M / 12)
```

Where `π_p2p` is the latest monthly point-to-point inflation rate and `M` is the current Jalali month.

**Base value:** `V(1399) = 22,018.36 Tomans` (verified anchor).

**Default CBI rates (verified):**

| Jalali Year | Inflation Rate |
|-------------|---------------|
| 1400 | 40.21% |
| 1401 | 46.50% |
| 1402 | 52.30% |
| 1403 | 34.05% |

**Automatic year-transition:** For years without hardcoded rates, the system uses the average of the last 3 known rates as an intelligent fallback, supplemented by World Bank API data when available.

**6-tier signal logic:**

| Condition | Signal | Tier |
|-----------|--------|------|
| Price ≤ Previous Year Value | STRONG BUY | Maximum safety margin |
| Price < 90% of Current Value | BUY | Good safety margin |
| Price < 100% of Current Value | CAUTIOUS BUY | Low margin |
| Price < 105% of Current Value | HOLD | Near fair value |
| Price < 115% of Current Value | HOLD (Bubble) | Overpriced — do not buy |
| Price ≥ 115% of Current Value | SELL | Exit zone |

### 5. Dirham-Dollar Cross-Rate Analysis (AED Parity Method)

The UAE Dirham has been pegged to the US Dollar at a **fixed rate** since 1997:

```
1 USD = 3.6725 AED    (UAE Central Bank official peg)
```

Since this peg is maintained by the UAE Central Bank and is considered deterministic, the Dirham price in Iran's free market directly implies a dollar value:

```
USD_implied = AED_price_Toman × 3.6725
```

**Why AED is the primary indicator:**
- ~85% of Iran's foreign exchange transactions flow through the UAE (Dubai)
- The AED is the most liquid currency after USD in Iran's market
- The fixed peg eliminates international forex noise — any deviation is purely a domestic market inefficiency
- Exchange houses typically trade AED with tighter spreads than USD

**5-tier signal thresholds:**

| Market vs. Implied | Signal | Interpretation |
|--------------------|--------|----------------|
| > +3% | SELL | Dollar overpriced vs. AED parity |
| +1.5% to +3% | CAUTION | Slightly overpriced |
| ±1.5% | NEUTRAL | Fair range — balanced market |
| −1.5% to −3% | BUY | Dollar underpriced |
| < −3% | STRONG BUY | Significant discount — arbitrage opportunity |

### 6. Multi-Currency Cross-Rate Consensus

Beyond AED, the system computes implied USD values from 7 currencies simultaneously:

```
USD_implied(C) = Iran_Price(C) × Forex_Rate(C/USD)
```

Where `Forex_Rate(C/USD)` is the ECB-published rate (units of currency C per 1 USD).

**Weighted consensus:**

```
USD_consensus = Σ(USD_implied(C) × Weight(C)) / Σ(Weight(C))
```

| Currency | Weight | Rationale |
|----------|--------|-----------|
| AED (Dirham) | 50% | Fixed peg, primary trade channel |
| EUR (Euro) | 20% | Major world reserve currency |
| GBP (Pound) | 10% | High liquidity |
| CHF (Franc) | 10% | Safe-haven benchmark |
| CAD (C. Dollar) | 5% | Commodity-correlated |
| TRY (Lira) | 3% | Regional peer (high-inflation economy) |
| CNY (Yuan) | 2% | Growing trade partner |

**Signal agreement voting:** Each currency "votes" BUY (deviation < −1%), SELL (> +1%), or NEUTRAL. When a majority agrees, the signal confidence increases.

### 7. Spread & Arbitrage Analysis

```
Spread(AED) = (AED_sell − AED_buy) / AED_buy × 100
Spread(USD) = (USD_sell − USD_buy) / USD_buy × 100
```

When `|AED_deviation| > 2%`, an **arbitrage alert** is triggered — the price gap between buying/selling through AED vs. direct USD is large enough to be actionable (net of typical transaction costs).

**Spread divergence:** If `|Spread(AED) − Spread(USD)| > 1%`, market stress is indicated and signal reliability may be reduced.

### 8. Combined Signal Engine (Dashboard)

The dashboard synthesizes coin bubble, melted-gold deviation, and dollar analysis into a **single combined recommendation** using a decision matrix:

| Coin Bubble | Gold Deviation | Combined Recommendation |
|-------------|---------------|-------------------------|
| HIGH (>25%) | LOW (<1%) | **Golden Cycle:** Sell coins, buy melted gold |
| HIGH (>25%) | NORMAL (1–5%) | Sell coins, hold USD |
| HIGH (>25%) | HIGH (>5%) | Liquidate all to USD |
| LOW (<13%) | LOW (<1%) | **Golden Opportunity:** Buy both coins and melted gold |
| LOW (<13%) | NORMAL | Buy coins only |
| LOW (<13%) | HIGH (>5%) | Buy coins, sell melted gold |
| NORMAL | LOW (<1%) | Buy melted gold only |
| NORMAL | HIGH (>5%) | Sell melted gold |
| NORMAL | NORMAL | Hold — monitor daily |

### 9. Portfolio Smart Advisor Engine

A 10-rule priority-based recommendation engine processes the user's holdings across asset classes:

1. **Golden Cycle Detection** — Highest priority: coin bubble high + melted gold cheap
2. **Individual Coin Sells** — Any coin with bubble > 25%
3. **Melted Gold Exit** — Deviation > 5%
4. **Expensive Foreign Currency** — Premium > 4% → sell to USD
5. **USD → Melted Gold** — If gold is cheap and user holds USD
6. **USD → Coins** — If coin bubble is low and gold is not cheap
7. **Cash (Toman) Deployment** — Idle cash → best available asset
8. **Cross-Currency Arbitrage** — If any currency is >2% below fair value
9. **Cross-Signal Opportunities** — EUR/GBP premium 2–4% + gold cheap → dual profit
10. **Diversification Alerts** — >50% in any single asset, <10% liquidity reserve

### 10. Dollar Cost Averaging (DCA) Calculator

Supports two modes:

**Recording mode:** User enters historical purchase amounts and prices. The system computes:
```
Average_Price = Total_Spent / Total_Units
Profit% = (Current_Value − Total_Spent) / Total_Spent × 100
```

**Planning mode:** Given total budget and step count, generates a time-phased purchase schedule with per-step amounts and projected unit accumulation.

---

## Architecture

```
financial-advisor/
├── app.py              # Single-file Streamlit application (≈1,780 lines)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

**Design decisions:**
- **Single-file architecture** — Streamlit's execution model (top-to-bottom re-run on every interaction) favors co-located code for this scale of application.
- **Aggressive caching** — All API calls are cached with `@st.cache_data` (TTL: 5 min for market data, 24 hr for inflation data) to minimize external requests and improve responsiveness.
- **Graceful degradation** — Every data source has hardcoded fallback values. The app remains fully functional even if all APIs are unreachable.
- **Jalali calendar support** — Custom Gregorian-to-Jalali conversion for accurate month-by-month inflation interpolation, without requiring the `jdatetime` dependency.
- **RTL-first UI** — All text, tables, and layouts are designed for right-to-left Persian rendering.

---

## Installation & Usage

### Prerequisites

- Python 3.9+
- Internet connection (for live market data; works offline with fallback values)

### Setup

```bash
cd financial-advisor
pip install -r requirements.txt
```

### Run

```bash
streamlit run app.py
```

The application opens in your default browser at `http://localhost:8501`.

### Configuration

All parameters are configurable via the **sidebar**:
- Market prices auto-populate from Bonbast but can be manually overridden
- Inflation rates for each Jalali year are editable
- Current-year monthly point-to-point inflation rate is adjustable
- Portfolio holdings are entered directly in the Portfolio tab

---

## Disclaimer

This tool is an **educational and analytical instrument** designed for personal investment decision support in the Iranian market. It is **not** financial advice, and it does **not** constitute a recommendation to buy or sell any asset. All signals are algorithmic outputs based on mathematical models — they do not account for geopolitical events, regulatory changes, or black-swan scenarios. **Investment decisions are solely the user's responsibility.**

---

## License

Personal use. Built by Mahdi Ghofran.
