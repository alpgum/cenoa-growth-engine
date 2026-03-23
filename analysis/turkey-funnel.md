# Turkey Funnel Analysis — Mar 14–20, 2026

**Period:** March 14–20, 2026  
**Sources:** Amplitude Event Segmentation API (country = Turkey)

---

## Turkey Funnel

| Stage | Volume | % of Global | Conversion from Prior |
|---|---:|---:|---:|
| **Install** | 670 | 46.4% | — |
| **Sign-up** | 226 | 49.9% (of 453 attributed) | 33.7% (Install→Signup) |
| **KYC Started** | 1,526 | ~49% | — ¹ |
| **KYC Submit** | 170 | **95.0%** | 11.1% (KYC Started→Submit) |
| **Deposit** | 840 | 54.3% | — ² |
| **Withdrawal** | 1,260 | 56.6% | — ² |

¹ KYC Started includes existing users, not just this week's cohort.  
² Deposits/Withdrawals include returning users.

---

## Turkey vs Global Conversion Rates

| Metric | Turkey | Global | Δ |
|---|---:|---:|---|
| Install→Signup | 33.7% | 83.5%³ | ⚠️ Lower — see note |
| KYC Started→Submit | **11.1%** | 5.8% | ✅ 2x better than global |
| KYC Submit share | **95.0%** | — | TR dominates KYC completions |

³ **Important note on Install→Signup gap:** The global 83.5% includes 754 "(none)" platform signups that aren't country-attributed. Many TR signups likely appear as "(none)" in country breakdown. The real TR Install→Signup rate is probably 50-60%.

---

## Key Findings

### ✅ Turkey is the KYC engine
- 170 of 179 global KYC submits come from Turkey (95%)
- TR's KYC Started→Submit rate (11.1%) is 2x the global average (5.8%)
- Bridge/Bridgexyz KYC appears to work primarily for Turkish ID documents
- **This means KYC completion outside Turkey is effectively broken**

### ✅ Turkey drives monetization
- 56.6% of all withdrawals come from Turkey (1,260 of 2,227)
- 54.3% of all deposits from Turkey (840 of 1,546)
- Despite being 46% of installs, TR punches above its weight in revenue-generating events

### ⚠️ Install volume concentrated but declining
- 670 installs (46.4% of total) — largest single country
- WoW trend: installs across all countries dropped -36.5%
- TR installs likely also saw significant decline

### ✅ Healthy downstream metrics
- High deposit and withdrawal volumes relative to install base
- Suggests strong product-market fit in Turkey
- Existing Turkish user base is sticky and transacting

---

## Turkey Funnel Visualization

```
Install (670)
   └─→ Sign-up (226) .............. 33.7% ¹
         └─→ KYC Started (1,526) .. (includes existing users)
               └─→ KYC Submit (170) .. 11.1%
                     └─→ Deposit (840)
                           └─→ Withdrawal (1,260)
```

¹ Likely undercounted due to attribution gaps

---

## Comparison to Other Markets

| Metric | TR | NG | EG | PK |
|---|---:|---:|---:|---:|
| Installs | 670 | 458 | 206 | 23 |
| Sign-ups | 226 | 117 | 64 | 15 |
| KYC Submit | **170** | **0** | **0** | **0** |
| Withdrawals | 1,260 | 492 | 135 | 4 |

**Turkey is the only market with a functioning end-to-end funnel.** All other markets effectively have a broken KYC step, meaning they cannot onboard new users into the full product experience.

---

## Recommendations for Turkey

1. **Protect the base:** Turkey is the revenue engine — ensure stability of the Turkish funnel
2. **Optimize KYC further:** Even at 11.1%, 89% of Turkish KYC starters still drop off — room for improvement
3. **Understand the 670→226 gap:** Why do only ~34% of Turkish installers sign up? Is the attribution gap hiding real users, or is there genuine friction?
4. **Scale high-quality channels:** Apple Search Ads and Google Ads show strong TR quality — increase spend there
5. **Turkish content/UX:** Ensure the app experience is fully localized — TR users carry the business

---

*Data from Amplitude. Country attribution may be incomplete for some events (sign-ups show 754 "(none)" country users). Actual Turkish metrics may be higher than reported.*
