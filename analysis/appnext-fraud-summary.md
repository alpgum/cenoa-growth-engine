# ⛔ Appnext Fraud Investigation — Executive Summary

**Date:** 2026-03-22  
**Status:** 🔴 IMMEDIATE ACTION REQUIRED  
**Author:** Performance Marketing Analysis

---

## Recommendation

**Pause all Appnext campaigns immediately and request a refund/credit for fraudulent installs.**

---

## Evidence

### 1. Near-zero downstream conversion despite high install volume

| Metric | Appnext | Appnext DSP | Paid Avg | Organic |
|---|---:|---:|---:|---:|
| Spend | $893 | $115 | — | — |
| Installs | 1,779 | 113 | — | 632 |
| Sign-ups | 349 | 2 | — | 77 |
| Virtual accounts | 47 | 1 | ~25% rate | — |
| New active users | 1 | 0 | — | — |
| Withdrawals (attr week) | 1 | — | — | 487 |
| **Virt account rate** | **2.6%** | **0.9%** | **~25%** | — |
| **Signup rate (DSP)** | — | **1.8%** | ~30%+ | 12.2% |
| **Cost / new active** | **$893** | **∞** | $19–$30 | $0 |

Appnext's 2.6% virtual account rate is **10× worse** than the paid channel average (~25%). Its cost per new active ($893) is **30–47× worse** than healthy channels like Pmax ($19.18) or ASA ($22.66).

### 2. Suspicious install volatility

- Week-over-week install cliff: **-77%** (164 → 712 pattern with wild swings)
- Legitimate channels show gradual, predictable volume changes
- Sudden spikes and crashes are a hallmark of bot-farm traffic rotation

### 3. Classic install fraud pattern

| Fraud Indicator | Present? | Detail |
|---|---|---|
| High install volume at low CPI | ✅ | $0.50 CPI vs $4.59 avg — too cheap to be real |
| Near-zero downstream conversion | ✅ | 1 withdrawal out of 1,779 installs (0.06%) |
| Inconsistent with organic quality | ✅ | Organic: 12.2% signup, 487 withdrawals/wk |
| Volume volatility | ✅ | -77% WoW swings |
| Low signup-to-activation ratio | ✅ | 349 signups → 47 virt acc → 1 active |

### 4. Comparison with healthy channels

| Channel | CPI | Cost/New Active | Withdrawals | Verdict |
|---|---:|---:|---:|---|
| Pmax | $8.22 | $19.18 | 182 | ✅ Healthy |
| Apple Search Ads | $5.45 | $22.66 | 254 | ✅ Best quality |
| Google Search | $1.41 | $25.48 | 29 | ✅ Efficient |
| **Appnext** | **$0.50** | **$893.00** | **1** | ⛔ **Fraud** |
| **Appnext DSP** | **$1.02** | **∞** | **0** | ⛔ **Fraud** |

---

## Action Plan

| # | Action | Owner | Timeline |
|---|---|---|---|
| 1 | **Pause all Appnext campaigns** | Media Buyer | Today |
| 2 | **Send fraud evidence to Appnext account manager** | Media Buyer | Today |
| 3 | **Request credit/refund** for fraudulent installs ($893 + $115 = $1,008) | Media Buyer | This week |
| 4 | **Add Appnext to permanent exclusion list** | Team | Permanent |
| 5 | **Monitor for residual installs** post-pause (confirms bot traffic) | Analyst | Next 7 days |

---

## Budget Impact

**~$220/week freed** from Appnext pause (based on recent weekly run-rate).

### Recommended reallocation:

| Destination | Amount | Rationale |
|---|---:|---|
| Apple Search Ads | +$100/wk | Best downstream quality (29.3% signup rate, highest LTV) |
| Pmax | +$120/wk | Best cost/new active ($19.18), primary scale lever |

**Expected outcome:** Reallocating $220/wk from fraudulent installs to proven channels should yield **~8–10 incremental real active users/week** vs the **1 active user** Appnext delivered across its entire $893 spend.

---

## Appendix: Data Sources

- **Spend & channel health:** `campaign-health.json` (AppsFlyer + Amplitude, generated 2026-03-21)
- **Attribution funnel:** `attribution-funnel.md` (Amplitude Event Segmentation, Mar 14–20)
- **Budget efficiency:** `budget-efficiency.md` (Sheets CAC Analysis + attribution data)
- **Fraud classification threshold:** High installs + <5% signup conversion (per campaign-health.json)

---

*Both `appnext` and `appnext_dsp` are flagged as `FRAUD` status in campaign-health.json automated classification.*
