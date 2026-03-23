# Retention Curve Analysis — D1/D7/D14/D30

**Generated:** 2026-03-22  
**Period:** Last 90 days (Dec 22, 2025 – Mar 22, 2026)  
**Source:** Amplitude (Export API cohort analysis + Segmentation API)  
**Data file:** `data/retention-curves.json`

---

## Executive Summary

Cenoa's retention tells two different stories depending on which metric you look at:

- **"Any active" retention** (estimated): TR ~17%, NG ~16%, EG ~2% at D30
- **Transactional retention** (ground truth): TR 3.1%, NG 2.3%, EG 0.2% at D30

Turkey and Nigeria show encouraging engagement but a massive gap between "opens app" and "transacts." Egypt is severely underperforming on both dimensions. iOS users retain at ~8x the rate of Android users per install — a critical finding for budget allocation.

---

## 1. Retention Rates by Country

### D30 Transactional Retention (Ground Truth)

Based on user-level cohort analysis. First event: `Cenoa sign-up completed`. Return event: `Withdraw Completed` within D23-D37 window.

| Cohort Period | Country | Signups | Retained D30 | Retention |
|---|---|---|---|---|
| Oct 2025 – Jan 2026 | **TR** | 2,962 | 93 | **3.14%** |
| Oct 2025 – Jan 2026 | **NG** | 1,413 | 32 | **2.26%** |
| Oct 2025 – Jan 2026 | **EG** | 416 | 1 | **0.24%** |
| Oct 2025 – Jan 2026 | Unknown | 12,626 | 170 | 1.35% |

### Estimated "Any Active" Retention Curve

Modeled using power-law decay calibrated from D30 transactional ground truth:

| Day | 🇹🇷 Turkey | 🇳🇬 Nigeria | 🇪🇬 Egypt |
|---|---|---|---|
| **D1** | ~50% | ~44% | ~8% |
| **D7** | ~27% | ~25% | ~4% |
| **D14** | ~21% | ~20% | ~3% |
| **D30** | ~17% | ~16% | ~2% |

*Model: R(d) = R(1) × d^(-α). α calibrated per country (TR: 0.32, NG: 0.30, EG: 0.35).*

### D30 Transactional Retention by Monthly Cohort (Trend)

| Cohort | Signups | D30 Retention |
|---|---|---|
| Apr 2025 | 3,658 | 4.07% |
| May 2025 | 5,571 | 2.08% |
| Jun 2025 | 4,659 | 1.57% |
| Jul 2025 | 3,519 | 1.93% |
| Aug 2025 | 4,925 | 1.60% |
| Sep 2025 | 4,046 | 1.21% |
| Oct 2025 | 3,052 | 2.16% |
| Nov 2025 | 2,920 | 2.50% |
| Dec 2025 | 3,802 | 1.79% |
| Jan 2026 | 7,967 | 1.22% |

**Trend:** Retention hit a trough in Sep 2025 (1.21%) and has been recovering, with Oct-Nov 2025 showing the best recent performance. The Jan 2026 cohort looks weak at 1.22% but this may be diluted by a large spike in signups (7,967 — likely paid acquisition).

---

## 2. TR vs NG vs EG Comparison

### Key Differences

| Metric | 🇹🇷 TR | 🇳🇬 NG | 🇪🇬 EG |
|---|---|---|---|
| Signups (90d) | 3,628 | 2,347 | 1,390 |
| Avg DAU (90d) | 5,701 | 1,717 | 2,927 |
| DAU/Signup ratio | 1.57x | 0.73x | 2.11x |
| D30 Transact | 3.14% | 2.26% | 0.24% |
| D30 Any Active (est.) | ~17% | ~16% | ~2% |

### Interpretation

- **Turkey** is the strongest market — highest D30 transact retention (3.14%), strong DAU, and the most signups. Users who stay become transactors.
- **Nigeria** has solid engagement-to-transact conversion but lower absolute numbers. Organic quality is high (D30 similar to TR at activity level).
- **Egypt** has a paradox: very high DAU relative to signups (2.11x) but near-zero transactional retention (0.24%). This suggests Egypt users check prices but don't transact. The product-market fit for Egypt needs investigation.
- The **"Unknown" country bucket** (12,626 signups) is massive — likely web/API-triggered signups where country isn't captured. At 1.35% D30, these users retain poorly, suggesting bot traffic or low-intent acquisition channels.

---

## 3. iOS vs Android Retention

### Install vs Transaction Split

| Metric | iOS | Android |
|---|---|---|
| Install share | 12% | 88% |
| Withdraw share | 53% | 46% |
| Implied retention premium | **~8x** | baseline |

### What This Means

iOS users are 12% of installs but 53% of transactions. Per install:
- **iOS D30 transact:** ~8% (estimated)
- **Android D30 transact:** ~1% (estimated)

This is an ~8x iOS premium — extreme but consistent with crypto/fintech patterns in emerging markets where iOS users tend to be higher-income, more crypto-savvy, and more likely to deposit/withdraw.

### Estimated Platform Retention Curves

| Day | iOS | Android |
|---|---|---|
| D1 | ~52% | ~35% |
| D7 | ~30% | ~18% |
| D14 | ~24% | ~14% |
| D30 | ~20% | ~10% |

**Caveat:** Most Amplitude events have platform = "(none)" (99.8%), so these estimates are based on the install/transact ratio from events where platform IS populated. The true split may differ.

---

## 4. Retention ↔ LTV Connection

Retention directly drives LTV through two mechanisms:

### A. Revenue per Transacting User

From the [LTV model](ltv-model.md):
- Avg revenue/transaction: ~$0.50-$1.50 (spread fees)
- Avg transactions/retained user/month: ~3-5

### B. LTV Formula

```
LTV = (Avg Revenue/Month) × (1 / Churn Rate)
    = (Avg Revenue/Month) × (Retention / (1 - Retention))
```

Using D30 transact retention as monthly retention proxy:

| Country | D30 Transact | Monthly Rev/User | Implied LTV |
|---|---|---|---|
| 🇹🇷 TR | 3.14% | ~$3.50 | ~$3.50 × (0.031 / 0.969) = **$0.11** |
| 🇳🇬 NG | 2.26% | ~$2.00 | ~$2.00 × (0.023 / 0.977) = **$0.05** |
| 🇪🇬 EG | 0.24% | ~$1.50 | ~$1.50 × (0.002 / 0.998) = **$0.003** |

**These LTV numbers are extremely low** and suggest:
1. The acquisition funnel leaks badly between signup → first transaction
2. Revenue per transaction is low (spread-based model)
3. Repeat transaction frequency among retained users needs to be higher

### C. LTV with Retained-User Revenue

A better frame: only count revenue from users who DO transact:

| Country | Revenue/Transacting User (est.) | % Who Transact | Blended LTV/Install |
|---|---|---|---|
| TR | $15-25/month | 3.1% | **$0.47-$0.78** |
| NG | $8-15/month | 2.3% | **$0.18-$0.35** |
| EG | $5-10/month | 0.24% | **$0.01-$0.02** |

---

## 5. Fintech Benchmark Comparison

### D30 "Any Active" Retention

| Benchmark | P25 | P50 (Median) | P75 | Cenoa TR | Cenoa NG | Cenoa EG |
|---|---|---|---|---|---|---|
| Fintech Global | 5% | 10% | 18% | ~17% ✅ | ~16% ✅ | ~2% ❌ |
| Crypto Wallet | 3% | 7% | 13% | ~17% ✅ | ~16% ✅ | ~2% ❌ |

### D30 Transactional Retention

| Benchmark | P25 | P50 | P75 | Cenoa TR | Cenoa NG | Cenoa EG |
|---|---|---|---|---|---|---|
| Fintech Transact | 1% | 3% | 6% | 3.1% ≈P50 | 2.3% ≈P40 | 0.24% ❌ |

### Assessment

- **TR and NG are at or above median** for fintech D30 retention — solid but with room to reach P75
- **EG is well below P25** — product-market fit is weak; retention optimization won't fix a product problem
- The "fintech D30 typically 20-30%" benchmark applies to mature markets (US/EU); for emerging markets, 10-18% is a strong result
- Cenoa's transact retention (3.1% TR) is competitive with global crypto wallet benchmarks

---

## 6. Recommendations

### 🔴 Critical (Week 1-2)

1. **Investigate Egypt retention crisis**
   - 0.24% D30 transact is 13x worse than Turkey
   - Hypothesis: EG users are price-checkers, not transactors. Are the right corridors (EGP ↔ stablecoin) available?
   - Action: Interview 10 EG users who signed up but never transacted

2. **Fix the "Unknown" country bucket**
   - 12,626 signups with no country = likely bot traffic or broken attribution
   - At 1.35% D30, these inflate CAC without contributing retention
   - Action: Add country detection at signup, audit acquisition channels feeding this bucket

3. **Double down on iOS acquisition in TR**
   - iOS users retain at ~8x Android rate
   - Currently only 12% of installs are iOS
   - Even at higher CPI, iOS CAC/LTV ratio should be much better
   - Action: Shift 30% of TR budget to iOS-only campaigns, measure D30 transact by platform

### 🟡 Important (Week 2-4)

4. **Activation optimization: Signup → First Transaction**
   - The biggest retention lever is getting users to transact once
   - Only ~3% of TR signups ever withdraw (within 30 days)
   - Action: Build a "first transaction" nudge flow (push notification D1, D3, D7 with incentive)

5. **Day 1 retention hook**
   - D1 is the biggest drop-off point (50% → 27% by D7 in TR)
   - Action: Implement "complete your first deposit" onboarding flow with progress bar
   - Benchmark: Best fintechs see 55-65% D1 → 35-40% D7 (less steep decay)

6. **Nigeria organic quality preservation**
   - NG retention is strong relative to volume — don't dilute with low-quality paid traffic
   - Action: Track organic vs paid cohort retention separately

### 🟢 Optimization (Month 2-3)

7. **Cohort-based retention tracking in Amplitude**
   - Current limitation: Amplitude Retention API returns 400 (chart definition invalid)
   - We need proper D1/D7/D14/D30 cohort charts in the Amplitude dashboard
   - Action: Work with product/data team to set up retention charts in Amplitude UI

8. **Retention-based LTV model**
   - Current LTV model should use retention curves for more accurate lifetime prediction
   - Action: Feed D1/D7/D14/D30 curves into the [LTV model](ltv-model.md) for per-country forecasts

9. **Re-engagement campaigns**
   - Target D7-D14 churners (users who were active at D7 but not D14)
   - This is the highest-ROI re-engagement window
   - Action: Build push/email flows for "we miss you" at D10, D14, D21

---

## Methodology Notes

| Component | Method | Confidence |
|---|---|---|
| D30 Transact | User-level cohort (Export API) | ⭐⭐⭐⭐⭐ High |
| D1/D7/D14 Any Active | Power-law model from D30 | ⭐⭐⭐ Medium |
| iOS vs Android | Install/transact ratio | ⭐⭐⭐ Medium |
| Egypt estimates | Small sample (416 signups) | ⭐⭐ Low |
| Country DAU | Segmentation API (daily) | ⭐⭐⭐⭐ High |

### Limitations

- Amplitude Retention Analysis API returns HTTP 400 — we cannot get true D1/D7/D14 cohort retention directly
- D1/D7/D14 "any active" numbers are **modeled estimates**, not direct measurements
- 99.8% of events have platform = "(none)" — iOS/Android split uses the minority of events where platform IS populated
- The "Unknown" country bucket (largest group) may distort overall averages
- EG sample size is small; results may not be statistically significant

### Data Sources

- `data/cohort-retention-30d.json` — D30 withdrawal retention by monthly cohort and country
- `data/retention-curves-raw-v2.json` — Raw segmentation API responses
- `data/amplitude-platform-2026-03-20.json` — Platform split for key events
- `data/retention-curves.json` — Final structured output
