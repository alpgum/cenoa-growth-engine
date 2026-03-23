# Global Funnel Analysis — Mar 14–20, 2026

**Period:** March 14–20, 2026 vs March 7–13, 2026  
**Sources:** Amplitude Event Segmentation API

---

## Full Funnel (Mar 14–20)

| Stage | Volume | Conversion from Prior | WoW Δ |
|---|---:|---:|---:|
| **Install** | 1,445 | — | ↓ -36.5% |
| **Sign-up** | 1,207 | 83.5% (Install→Signup) | ↓ -27.8% |
| **KYC Started** | 3,098 | 256.5%¹ | ↓ -7.5% |
| **KYC Submit** | 179 | 5.8% (KYC Started→Submit) | ↓ -41.7% |
| **Deposit** | 1,546 | — ² | ↓ -5.8% |
| **Withdrawal** | 2,227 | — ² | ↑ +0.6% |
| **DAU (avg)** | 3,060 | — | ↓ -46.1% |

¹ KYC Started > Installs because existing users also trigger KYC events.  
² Deposits/Withdrawals include returning users, not just this week's cohort.

---

## Funnel Conversion Rates (New User Cohort Approximation)

Using Install as the cohort entry point:

| Step | Rate | Assessment |
|---|---:|---|
| Install → Sign-up | **83.5%** | ✅ Strong — most installers sign up |
| Sign-up → KYC Submit | **14.8%** | ⚠️ Major dropout — 85% of signups don't submit KYC |
| KYC Started → KYC Submit | **5.8%** | 🚨 Critical — 94.2% abandon KYC flow |

---

## Week-over-Week Comparison

| Metric | This Week | Prev Week | Change | Direction |
|---|---:|---:|---:|---|
| Installs | 1,445 | 2,274 | -36.5% | 📉 Significant drop |
| Sign-ups | 1,207 | 1,671 | -27.8% | 📉 Notable drop |
| KYC Submits | 179 | 307 | -41.7% | 📉 Steep drop |
| Withdrawals | 2,227 | 2,214 | +0.6% | ➡️ Flat/stable |
| Deposits | 1,546 | 1,642 | -5.8% | ➡️ Slight dip |
| KYC Started | 3,098 | 3,351 | -7.5% | 📉 Moderate drop |
| DAU | 3,060 | 5,678 | -46.1% | 📉 Severe drop |

---

## Bottleneck Analysis

### 🚨 #1: KYC Completion (94.2% dropout)
- 3,098 users start KYC, only 179 submit → **5.8% completion rate**
- This is the single biggest funnel bottleneck
- Country breakdown shows KYC Submit is almost entirely Turkey (95%)
- Nigeria and Egypt have near-zero KYC submits despite significant installs
- **Hypothesis:** KYC provider (Bridge/Bridgexyz) may not support NG/EG documents, or the flow is broken for non-TR users

### ⚠️ #2: Install Volume Decline (-36.5% WoW)
- Installs dropped from 2,274 → 1,445
- Likely caused by ad spend changes or campaign pausing
- appnext_int (273 installs, near-zero withdrawals) may have been scaled back
- TikTok campaigns paused mid-week (49 installs, 0 withdrawals)

### ⚠️ #3: DAU Crash (-46.1%)
- DAU dropped from 5,678 → 3,060
- This is a lagging indicator of the install drop
- May also reflect seasonal patterns or app update issues
- Needs investigation: is this a data anomaly or real engagement drop?

### ✅ Positive Signal: Withdrawals Stable (+0.6%)
- Despite install/signup drops, withdrawal volume held steady
- This suggests the existing user base is healthy and transacting
- Core monetization is not affected by the top-of-funnel decline

---

## Key Insights

1. **Install-to-signup conversion is excellent (83.5%)** — the onboarding flow works well
2. **KYC is the death zone** — 94% dropout, almost exclusively a non-TR problem
3. **Existing users keep transacting** — withdrawals flat despite acquisition dip
4. **Top-of-funnel is volatile** — heavily dependent on ad spend levels
5. **Quality > Quantity pattern:** Apple Search Ads (75 installs, 254 withdrawals) dramatically outperforms appnext (273 installs, 1 withdrawal)

---

## Recommended Actions

1. **Urgent:** Investigate KYC flow for NG/EG users — is Bridge KYC even functional outside TR?
2. **Audit ad spend:** The install drop correlates with channel changes — understand which campaigns were paused/modified
3. **DAU investigation:** Verify if the -46% DAU drop is a real trend or data issue
4. **Shift budget:** Move spend from low-quality channels (appnext, TikTok) to high-quality ones (Apple Search Ads, Google Ads)
5. **Retention focus:** With stable withdrawals from existing users, prioritize keeping current users vs chasing new installs

---

*Generated from Amplitude data. Cross-cohort conversion rates are directional — users who withdrew this week may have installed weeks/months ago.*
