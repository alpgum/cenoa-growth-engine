# [S2-022] Withdrawal Volume & LTV Validation

**Data source:** Amplitude API — Event Segmentation  
**Period:** Jan 1 – Mar 21, 2026 (3 monthly buckets: Jan, Feb, Mar partial)  
**Events analyzed:** `Withdraw Completed`, `Deposit Completed`  
**Properties used:** `amount` (USDC, 6 decimal places), `outgoing_amount` (USD string)  
**Generated:** 2026-03-22

---

## 1) Monthly Withdrawal Volumes by Country

### Event Counts (totals)

| Country | Jan 2026 | Feb 2026 | Mar 1–21* | Avg/mo |
|---------|-------:|-------:|-------:|-------:|
| **Turkey** | 4,381 | 4,423 | 3,609 | 4,138 |
| **Nigeria** | 3,134 | 3,036 | 2,504 | 2,891 |
| **Egypt** | 5 | 43 | 52 | 33 |
| **Pakistan** | 1 | 0 | 0 | ~0 |

*Mar is partial (21 days). Full-month estimate: TR ~5,150, NG ~3,577, EG ~74.*

### Unique Withdrawers (distinct users per month)

| Country | Jan 2026 | Feb 2026 | Mar 1–21* | Avg/mo |
|---------|-------:|-------:|-------:|-------:|
| **Turkey** | 1,226 | 1,291 | 1,214 | 1,244 |
| **Nigeria** | 658 | 686 | 604 | 649 |
| **Egypt** | 4 | 20 | 29 | 18 |
| **Pakistan** | ~1 | 0 | 0 | ~0 |

### Withdrawals per User per Month

| Country | Jan | Feb | Mar* | Avg |
|---------|----:|----:|----:|----:|
| **Turkey** | 3.6 | 3.4 | 3.0 | **3.3** |
| **Nigeria** | 4.8 | 4.4 | 4.1 | **4.4** |
| **Egypt** | 1.3 | 2.2 | 1.8 | **1.8** |

**Insight:** Nigeria users withdraw more frequently than Turkey users — 4.4× vs 3.3× per month. Turkey has 2× the unique user base.

---

## 2) Transaction Volume (USD)

### Data Coverage

The `amount` event property is populated on a subset of events:

| Country | Coverage | Notes |
|---------|----------|-------|
| **Turkey** | **47%** of events | ~53% of events have `(none)` for amount — likely older SDK or different rail |
| **Nigeria** | **100%** | Full coverage |
| **Egypt** | **100%** | Full coverage (small N) |

### Measured Withdrawal Volume (from events WITH amount property)

| Country | Jan 2026 | Feb 2026 | Mar 1–21* |
|---------|-------:|-------:|-------:|
| **Turkey** | $1,275,881 | $1,425,553 | $1,100,866 |
| **Nigeria** | $139,811 | $175,098 | $127,727 |
| **Egypt** | $250 | $5,496 | $5,597 |

### Average Transaction Size (USD)

| Country | Jan | Feb | Mar* | Overall Avg |
|---------|----:|----:|----:|----:|
| **Turkey** | $747 | $852 | $798 | **$799** |
| **Nigeria** | $59 | $79 | $71 | **$69** |
| **Egypt** | $125 | $305 | $350 | **$314** |

### Extrapolated Turkey Volume (adjusting for 47% coverage)

Assuming events without `amount` have similar transaction sizes:

| Month | Measured (47%) | Extrapolated (100%) |
|-------|-------:|-------:|
| Jan | $1,275,881 | **~$3,275,000** |
| Feb | $1,425,553 | **~$3,769,000** |
| Mar* | $1,100,866 | **~$2,881,000** |

⚠️ **Extrapolation caveat:** The 53% of events without amount data may differ systematically (different rail, different user segment, or SDK gap). True volume could be 20–40% lower than extrapolated if those events are smaller transactions.

**Conservative estimate (Turkey monthly volume):** $2.0M–$3.8M/month

### Deposit Volume (for reference)

| Country | Jan 2026 | Feb 2026 | Mar 1–21* | Avg Txn |
|---------|-------:|-------:|-------:|-------:|
| **Turkey** | $893,607 | $1,486,682 | $1,133,073 | $1,224 |
| **Nigeria** | $89,139 | $130,194 | $166,779 | $146 |
| **Egypt** | $2,736 | $12,849 | $5,999 | $937 |

*Deposit amounts have 100% coverage for all countries.*

---

## 3) Per-User Monthly Metrics

### Turkey

| Metric | Jan | Feb | Mar* | Avg |
|--------|----:|----:|----:|----:|
| Unique withdrawers | 1,226 | 1,291 | 1,214 | 1,244 |
| Withdrawals/user | 3.6 | 3.4 | 3.0 | 3.3 |
| Measured vol/user | $1,041 | $1,104 | $907 | **$1,017** |
| Extrapolated vol/user | $2,671 | $2,918 | $2,373 | **$2,654** |

### Nigeria

| Metric | Jan | Feb | Mar* | Avg |
|--------|----:|----:|----:|----:|
| Unique withdrawers | 658 | 686 | 604 | 649 |
| Withdrawals/user | 4.8 | 4.4 | 4.1 | 4.4 |
| Volume/user | $212 | $255 | $211 | **$226** |

### Egypt

| Metric | Jan | Feb | Mar* | Avg |
|--------|----:|----:|----:|----:|
| Unique withdrawers | 4 | 20 | 29 | 18 |
| Withdrawals/user | 1.3 | 2.2 | 1.8 | 1.8 |
| Volume/user | $63 | $275 | $193 | **$177** |

*Egypt has very small sample sizes — treat as directional only.*

---

## 4) LTV Model Validation

### Comparing to Original Assumptions (from ltv-model.md)

| Parameter | ltv-model.md Base Assumption | Actual Data | Verdict |
|-----------|------------------------------|-------------|---------|
| **TR monthly vol/user** | $2,000 | $1,017–$2,654 | ✅ Base assumption reasonable (within range) |
| **NG monthly vol/user** | $800 | **$226** | ❌ **3.5× too high** — reality is much lower |
| **EG monthly vol/user** | $600 | ~$177 (tiny N) | ❌ **3.4× too high** — but tiny sample |
| **TR withdrawals/user/mo** | Not modeled | 3.3 | New data point |
| **NG withdrawals/user/mo** | Not modeled | 4.4 | Users are active, just small amounts |
| **TR avg transaction** | Not modeled | $799 | High-value market |
| **NG avg transaction** | Not modeled | $69 | Micro-transaction market |

### Key Findings

1. **Turkey is the high-value market.** ~$800 avg withdrawal, 3.3 withdrawals/month, $1,000–$2,650/user/month in volume. The LTV model base case of $2,000/month is plausible if the 53% unmeasured events carry similar value.

2. **Nigeria volume is 3.5× lower than modeled.** $226/user/month actual vs $800 assumed. However, Nigeria has strong engagement (4.4 withdrawals/month) — users are active but transacting smaller amounts ($69 avg). This may reflect remittance corridors with lower ticket sizes.

3. **Egypt is nascent.** Growing fast (4→20→29 unique users) but sample too small for reliable volume estimates. $177/user/month is directional only.

4. **Pakistan doesn't exist** as a market. 1 event total in 3 months. Remove from planning.

---

## 5) Updated LTV Estimates

Using observed data with the original formula: **LTV = Monthly Volume × FX Margin × Lifetime Months**

### FX Margin Scenarios (unchanged)
- Low: 0.30% | Base: 0.60% | High: 1.00%

### Lifetime Months (unchanged — no retention data yet)
- Low: 3 | Base: 6 | High: 12

### Turkey — Data-Backed LTV

Using **conservative measured** $1,017/user/month and **extrapolated** $2,654/user/month as range:

| Scenario | Conservative ($1,017/mo) | Extrapolated ($2,654/mo) |
|----------|-------:|-------:|
| **Low** (0.3% × 3mo) | **$9.15** | **$23.89** |
| **Base** (0.6% × 6mo) | **$36.61** | **$95.54** |
| **High** (1.0% × 12mo) | **$122.04** | **$318.48** |

**Best estimate (base case):** **$37–$96 per active user**

vs. ltv-model.md base of $72 → ✅ **$72 falls within range. Model is validated for Turkey.**

### Nigeria — Data-Corrected LTV

Using **observed** $226/user/month:

| Scenario | LTV |
|----------|-------:|
| **Low** (0.3% × 3mo) | **$2.03** |
| **Base** (0.6% × 6mo) | **$8.14** |
| **High** (1.0% × 12mo) | **$27.12** |

**Best estimate (base case):** **~$8 per active user**

vs. ltv-model.md base of $28.80 → ❌ **Original model was 3.5× too optimistic for Nigeria.**

### Egypt — Provisional (low confidence)

Using **observed** $177/user/month (tiny sample):

| Scenario | LTV |
|----------|-------:|
| **Low** (0.3% × 3mo) | **$1.59** |
| **Base** (0.6% × 6mo) | **$6.37** |
| **High** (1.0% × 12mo) | **$21.24** |

vs. ltv-model.md base of $21.60 → ❌ **3.4× too high, but extremely low confidence.**

### Summary: Updated LTV Table

| Country | Old Base LTV | New Base LTV | Change | Confidence |
|---------|-------:|-------:|--------|------------|
| **Turkey** | $72 | **$37–$96** | ≈ Validated | 🟡 Medium (47% amount coverage) |
| **Nigeria** | $28.80 | **$8** | **-72%** | 🟢 High (100% amount coverage) |
| **Egypt** | $21.60 | **$6** | **-72%** | 🔴 Low (N=18 users/month) |
| **Pakistan** | n/a | **$0** | Remove | ⬛ No market |

---

## 6) Confidence Assessment

### What We Know (High Confidence)
- ✅ Turkey has ~1,250 monthly active withdrawers, stable across 3 months
- ✅ Nigeria has ~650 monthly active withdrawers, stable across 3 months
- ✅ Nigeria avg withdrawal = $69 (100% coverage, 8,674 events)
- ✅ Nigeria monthly vol/user = $226
- ✅ User frequency: TR 3.3×/mo, NG 4.4×/mo
- ✅ Pakistan is not a market

### What We're Less Sure About (Medium Confidence)
- 🟡 Turkey avg withdrawal ≈ $799 (based on 47% of events)
- 🟡 Turkey monthly volume: $1M–$2.7M extrapolated (depends on unmeasured events)
- 🟡 Turkey vol/user: $1,017–$2,654 range

### What We Don't Know (Low Confidence)
- ❌ Why 53% of Turkey withdraw events lack amount data
- ❌ Cohort retention / actual lifetime months (biggest LTV driver)
- ❌ True FX margin per transaction
- ❌ Egypt's true steady-state behavior (market too young)

### Biggest Risk to LTV Model
**Lifetime months** remains the #1 unknown. If Turkey retention is 3 months instead of 6, base LTV drops from $37–$96 to $18–$48. Cohort retention analysis is the highest-priority next step.

---

## 7) Implications for Performance Marketing

### Turkey (prioritize)
- Base LTV $37–$96 supports a **CAC target of $10–$30** (3:1 LTV:CAC at conservative end)
- High-value market: avg $799/withdrawal, 1,250 MAU
- Volume growing: Feb was the peak month
- **Action:** Continue scaling. Focus on install-to-first-withdrawal conversion optimization.

### Nigeria (recalibrate)
- Base LTV ~$8 means **target CAC must be ≤$2–3**
- High frequency but micro-transactions ($69 avg)
- Significant demand (650 MAU, 3,000+ events/month)
- **Action:** Only viable with extremely cheap acquisition (organic, referral). Paid media at current costs unlikely to work unless volume/user grows significantly.

### Egypt (watch)
- Too early to set budgets. 29 unique withdrawers in March.
- Growing quickly (7× in 3 months)
- **Action:** Monitor. Revisit when MAU > 100.

### Pakistan (remove)
- 1 event in 3 months. No market.
- **Action:** Remove from planning entirely.

---

## Appendix: Raw Data Reference

### Withdraw Completed — All Countries in Dataset (Top 10 by Events)

| Country | Jan Events | Feb Events | Mar Events | Jan Uniques | Feb Uniques | Mar Uniques |
|---------|-------:|-------:|-------:|-------:|-------:|-------:|
| Turkey | 4,381 | 4,423 | 3,609 | 1,226 | 1,291 | 1,214 |
| Nigeria | 3,134 | 3,036 | 2,504 | 658 | 686 | 604 |
| United States | 234 | 240 | 197 | 24 | 21 | 23 |
| Netherlands | 27 | 86 | 80 | 7 | 9 | 12 |
| South Africa | 0 | 38 | 99 | 4 | 20 | 29 |
| United Kingdom | 80 | 61 | 63 | 27 | 24 | 20 |
| Germany | 62 | 67 | 77 | 26 | 28 | 24 |
| Egypt | 5 | 43 | 52 | 4 | 20 | 29 |
| Azerbaijan | 32 | 47 | 21 | 3 | 12 | 6 |
| Sweden | 34 | 29 | 27 | 6 | 9 | 6 |

### Deposit Completed — Target Countries

| Country | Jan Events | Feb Events | Mar Events | Jan Vol | Feb Vol | Mar Vol |
|---------|-------:|-------:|-------:|-------:|-------:|-------:|
| Turkey | 3,656 | 3,647 | 3,078 | $893,607 | $1,486,682 | $1,133,073 |
| Nigeria | 1,793 | 1,750 | 1,447 | $89,139 | $130,194 | $166,779 |
| Egypt | 8 | 44 | 57 | $2,736 | $12,849 | $5,999 |

### Amount Property Distribution — Turkey Withdrawals (Top 10 by Frequency)

| Amount (USD) | Jan | Feb | Mar | Total Events |
|-------:|----:|----:|----:|----:|
| $1,000 | 106 | 78 | 92 | 276 |
| $100 | 81 | 92 | 70 | 243 |
| $2,000 | 48 | 56 | 69 | 173 |
| $10 | 51 | 57 | 42 | 150 |
| $500 | 59 | 49 | 36 | 144 |
| $200 | 55 | 50 | 32 | 137 |
| $50 | 50 | 42 | 39 | 131 |
| $11 | 37 | 37 | 26 | 100 |
| $5 | 32 | 33 | 26 | 91 |
| $20 | 29 | 25 | 17 | 71 |
