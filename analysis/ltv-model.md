# [027] First-pass LTV model (proxy-based) — TR / NG / EG

**Purpose:** a *directional* LTV model by country for performance marketing decisions, using Amplitude funnel + transaction *count* proxies and explicit parameter assumptions.

**Data window:** Mar 14–20, 2026 (same as the funnel reads)

**Important caveat:** the provided Amplitude exports contain **event counts** (e.g., `Withdraw Completed`) but **not**:
- withdrawal **amounts** / volumes
- unique transacting users (WAU/MAU)
- cohort-clean “new user” transaction outcomes

So this model is intentionally **parameterized** (scenario-based) and should be treated as a starting point.

---

## 1) LTV definition

We use the requested formula:

> **LTV = (Avg monthly gross profit per active user) × (expected lifetime months)**

### Definitions (for this model)
- **Active user (monetization-active):** a user who completes ≥1 withdrawal in a month.
- **Gross profit driver:** **FX margin / spread / fee** on withdrawal volume.

So:

> **Avg monthly gross profit per active user**  
> = (**Avg monthly withdrawal volume per active user**) × (**FX margin %**) 

and:

> **LTV per active user**  
> = (Monthly withdrawal volume per active user × FX margin) × lifetime months

---

## 2) What we *can* observe (Amplitude proxies)

From `projects/cenoa-performance-marketing/data/country-breakdown-20260320.json`:

**Top-of-funnel + KYC (weekly event totals)**
- **Turkey:** Installs 670 | Signups 226 | KYC Started 2,594 | KYC Submit 170
- **Nigeria:** Installs 458 | Signups 117 | KYC Started 230 | KYC Submit 0
- **Egypt:** Installs 206 | Signups 64 | KYC Started 62 | KYC Submit 0

**Transaction proxies (weekly event totals; not cohort-pure)**
- **Turkey:** Withdraw Completed 1,177 | Deposit Completed 961
- **Nigeria:** Withdraw Completed 778 | Deposit Completed 448
- **Egypt:** Withdraw Completed 23 | Deposit Completed 22

Interpretation:
- **TR has functioning KYC + meaningful transaction base.**
- **NG/EG show demand (withdrawals exist) but new-user activation is blocked (0 KYC submits).**
- Transaction events are dominated by **existing users**, so they’re better as a *market maturity / demand signal* than a cohort LTV measure.

---

## 3) Assumptions (parameterized)

Because we don’t have $ volumes or margins in the data, we model three drivers explicitly.

### A) FX margin (take rate on withdrawal volume)
- **Low:** 0.30%
- **Base:** 0.60%
- **High:** 1.00%

*(These are placeholders; replace with finance-confirmed net margin after costs.)*

### B) Avg monthly withdrawal volume per active user (USD)
This is the biggest unknown. We set country-level scenarios based on typical remittance / cashout behavior expectations.

| Country | Low | Base | High |
|---|---:|---:|---:|
| **TR** | $1,000 | $2,000 | $5,000 |
| **NG** | $400 | $800 | $2,000 |
| **EG** | $300 | $600 | $1,500 |

### C) Expected lifetime (months active)
- **Low:** 3 months
- **Base:** 6 months
- **High:** 12 months

---

## 4) LTV scenarios (per active user)

Computed as:

> **LTV = volume × margin × lifetime**

### Turkey (TR)
- **Low:** $1,000 × 0.30% × 3 = **$9**
- **Base:** $2,000 × 0.60% × 6 = **$72**
- **High:** $5,000 × 1.00% × 12 = **$600**

### Nigeria (NG)
- **Low:** $400 × 0.30% × 3 = **$3.6**
- **Base:** $800 × 0.60% × 6 = **$28.8**
- **High:** $2,000 × 1.00% × 12 = **$240**

### Egypt (EG)
- **Low:** $300 × 0.30% × 3 = **$2.7**
- **Base:** $600 × 0.60% × 6 = **$21.6**
- **High:** $1,500 × 1.00% × 12 = **$180**

### Summary table (per active user)

| Country | Low LTV | Base LTV | High LTV |
|---|---:|---:|---:|
| **TR** | $9 | $72 | $600 |
| **NG** | $3.6 | $28.8 | $240 |
| **EG** | $2.7 | $21.6 | $180 |

---

## 5) (Optional) Acquisition-adjusted note: “LTV for *newly acquired* users right now”

Because **KYC Submit = 0** in NG/EG during this week, the *incremental LTV of newly acquired users* is effectively **near-zero** **until KYC is fixed** (assuming KYC is required to transact on the monetized rails).

For Turkey, we can define a rough “activation proxy”:
- **KYC Submit / Install ≈ 170 / 670 = 25.4%** (directional; still not cohort-clean)

Then a *very rough* “LTV per install” proxy would be:

> **LTV_install ≈ LTV_active × (KYC submit per install)**

Using Turkey’s 25.4% proxy:
- TR Low (per install): $9 × 0.254 ≈ **$2.3**
- TR Base (per install): $72 × 0.254 ≈ **$18.3**
- TR High (per install): $600 × 0.254 ≈ **$152**

This is only useful as a sanity check against CAC; it should be replaced with cohort retention + true activation definitions.

---

## 6) What data is missing to make this real (priority order)

1) **Withdrawal volumes ($) by country**
   - Avg withdrawal amount
   - Total withdrawal volume
   - Breakdown by rail / corridor (if relevant)

2) **True unit margin** on that volume
   - FX spread / fee revenue
   - Less: liquidity/hedging costs, provider fees, chargebacks/fraud, support costs
   - Net gross profit per $ volume (by rail)

3) **Cohort retention / lifetime (months)**
   - Monthly retention curve of transacting users by country (cohort by first withdrawal date)
   - Churn hazard (early drop vs long tail)

4) **Unique user counts** (not event counts)
   - # transacting users per month (MAWU)
   - withdrawals per user per month

5) **Cohort-clean activation**
   - install → signup → KYC submit → first withdrawal (by country)
   - impact of the KYC outage on NG/EG conversion

---

## 7) Next step recommendation

If we can pull even one of the following quickly from Amplitude / backend, the model becomes 10× tighter:
- **Total withdrawal volume by country** for the last 30–90 days
- **# unique withdrawers by country** (monthly)
- **Cohort retention**: % of first-withdrawal users who withdraw again in months 1–6

Then we can replace the assumed “monthly withdrawal volume per active user” and “lifetime months” with observed values.
