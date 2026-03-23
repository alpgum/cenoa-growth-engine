# ✅ Campaign Pause Execution Checklist

**Created:** 2026-03-23  
**Purpose:** Step-by-step checklist for pausing all kill-list campaigns from the Mar 22 commentary  
**Total budget freed:** ~$2,530/wk = ~$10,120/mo  
**Reallocation targets:** Pmax, ASA, Google Search, Meta LTV EG, Referral

---

## 1. Google Demand Gen Retargeting — TR

| Field | Detail |
|---|---|
| Campaign name | **TR-Discovery-24.10.2025** |
| Platform | Google Ads |
| Platform URL | https://ads.google.com → Campaigns |
| Budget freed | ₺19,620/period (~**$560/wk**) |
| Reallocate to | Pmax (+$300/wk), ASA (+$260/wk) |

**Steps:**

- [ ] Log into Google Ads console
- [ ] Navigate to **Campaigns** in left sidebar
- [ ] Search / filter for **TR-Discovery-24.10.2025**
- [ ] Click the green dot under **Status** column → select **Paused**
- [ ] Confirm status shows "Paused" (grey icon)
- [ ] Screenshot the paused state for records
- [ ] Increase Pmax budget by +₺10,500/wk (~$300)
- [ ] Increase ASA budget by +$260/wk in Apple Search Ads
- [ ] Optional: Run diagnostics per [demand-gen-pause-memo.md](demand-gen-pause-memo.md) before any relaunch consideration
- [ ] Set Google Ads automated rule: pause any campaign with spend >₺10,000 and conversions = 0 in trailing 7 days (prevention)

**Why:** 0 installs over ~5 months. ₺392K (~$11.2K) estimated total waste. See [demand-gen-pause-memo.md](demand-gen-pause-memo.md).

---

## 2. Appnext — TR (All Campaigns)

| Field | Detail |
|---|---|
| Campaigns | All active Appnext + Appnext DSP campaigns |
| Platform | Appnext Dashboard |
| Platform URL | https://console.appnext.com (or equivalent dashboard) |
| Budget freed | ~**$645/wk** ($893 + $115 biweekly run-rate) |
| Reallocate to | ASA (+$100/wk), Pmax (+$120/wk), reserve (+$425/wk) |

**Steps:**

- [ ] Log into Appnext dashboard
- [ ] Navigate to **Campaigns** section
- [ ] Pause **every active campaign** (both Appnext direct and Appnext DSP)
- [ ] Confirm all campaigns show "Paused" status
- [ ] Screenshot each paused campaign for records
- [ ] Monitor for residual installs over next 7 days (if installs continue post-pause → confirms bot traffic)
- [ ] Send refund request email to Appnext account manager (template below)
- [ ] Add Appnext to **permanent exclusion list** — do not reactivate

**Refund Request Email Template:**

> **Subject:** Fraud Evidence & Credit Request — Cenoa Account
>
> Hi [Account Manager Name],
>
> We're writing to formally flag fraudulent install activity on our Appnext campaigns and request a full credit/refund.
>
> **Evidence summary:**
> - 1,779 installs at $0.50 CPI, but only 47 virtual accounts (2.6% conversion vs 25% paid average)
> - Only **1 new active user** out of 1,779 installs (0.06% activation rate)
> - Appnext DSP: 113 installs, 2 sign-ups, 0 active users
> - Wild week-over-week install volatility (-77% swings) consistent with bot-farm rotation
> - CPI too low to be legitimate ($0.50 vs $4.59 portfolio average)
>
> **Refund requested:** $1,008 ($893 Appnext + $115 DSP)
>
> We have paused all campaigns effective immediately. Full fraud analysis attached.
>
> Please confirm receipt and next steps for the credit/refund process.
>
> Best regards,
> [Your Name]

**Why:** Confirmed install fraud — $893/active user, 0.06% activation. See [appnext-fraud-summary.md](appnext-fraud-summary.md).

---

## 3. Twitter/X Ads — TR

| Field | Detail |
|---|---|
| Campaign | All Twitter/X Ads TR campaigns |
| Platform | Twitter Ads Manager |
| Platform URL | https://ads.twitter.com |
| Budget freed | ~**$90/wk** |
| Reallocate to | Google Search (+$90/wk) |

**Steps:**

- [ ] Log into Twitter Ads Manager
- [ ] Navigate to **Campaigns**
- [ ] Select all active Turkey campaigns
- [ ] Set status to **Paused**
- [ ] Confirm all campaigns show paused
- [ ] Screenshot for records
- [ ] Do **not** reactivate unless a completely new strategy is tested (brand awareness only, not performance)

**Why:** $183 CPI, 1 install, 0 sign-ups, 0 active users. Dead channel for app installs. Kill permanently.

---

## 4. Onboarding Meta Test — TR

| Field | Detail |
|---|---|
| Campaign | Onboarding Meta Test (TR) |
| Platform | Meta Business Manager |
| Platform URL | https://business.facebook.com/adsmanager |
| Budget freed | ~**$101/wk** |
| Reallocate to | Meta App iOS TR (+$101/wk) |

**Steps:**

- [ ] Log into Meta Business Manager → Ads Manager
- [ ] Search for **Onboarding Meta Test** campaign (TR market)
- [ ] Toggle campaign status to **Off**
- [ ] Confirm the campaign shows "Off" status
- [ ] Screenshot for records
- [ ] Increase Meta App iOS TR budget by +$101/wk

**Why:** $33.67 CPI (7.3× portfolio average), 3 installs, 0 active users. Not viable at any scale.

---

## 5. Meta W2A Turkey — Prospecting (Non-Retargeting)

| Field | Detail |
|---|---|
| Campaigns | All TR Meta W2A **prospecting** campaigns (KEEP retargeting!) |
| Platform | Meta Business Manager |
| Platform URL | https://business.facebook.com/adsmanager |
| Budget freed | ~**$485/wk** (keep RTGT at $500/wk = $2K/mo cap) |
| Reallocate to | Pmax (+$200/wk), Meta LTV EG (+$285/wk) |

**Steps:**

- [ ] Log into Meta Business Manager → Ads Manager
- [ ] Filter for Turkey W2A campaigns
- [ ] Identify **prospecting** campaigns vs **retargeting** campaigns
- [ ] ⚠️ **DO NOT PAUSE** the retargeting campaign (Meta W2A RTGT) — this is the only W2A campaign showing withdrawals
- [ ] Pause **all prospecting W2A campaigns** only
- [ ] Confirm retargeting campaign is still active with $500/wk ($2K/mo) budget cap
- [ ] Screenshot showing prospecting = paused, retargeting = active
- [ ] Increase Pmax budget by additional +$200/wk
- [ ] Increase Meta LTV Test EG budget by +$285/wk

**Why:** Cost/Active: $3,536 (Jan) → ∞ (Feb, 0 paid active). Structural failure — funnel friction, attribution collapse. Do not reactivate until web→app attribution is fixed end-to-end.

---

## 📊 Summary

| # | Campaign | Platform | Weekly Freed | Reallocate To |
|---|---|---|---:|---|
| 1 | Google Demand Gen TR | Google Ads | $560 | Pmax +$300, ASA +$260 |
| 2 | Appnext (all) | Appnext | $645 | ASA +$100, Pmax +$120, reserve +$425 |
| 3 | Twitter/X Ads TR | Twitter Ads | $90 | Google Search +$90 |
| 4 | Onboarding Meta Test TR | Meta | $101 | Meta App iOS +$101 |
| 5 | Meta W2A TR (prospecting) | Meta | $485 | Pmax +$200, Meta LTV EG +$285 |
| | **TOTAL** | | **~$1,881/wk** | |

> **Note:** The commentary estimates ~$2,530/wk total freed. The difference (~$649) comes from varying weekly run-rates vs period averages. Use $1,881–$2,530/wk as the range; actual freed depends on the exact pause date within the billing cycle.

### Reallocation Summary

| Destination | Total Weekly Add | Source |
|---|---:|---|
| Pmax (Google) | +$620/wk | Demand Gen $300 + Appnext $120 + Meta W2A $200 |
| ASA (Apple) | +$360/wk | Demand Gen $260 + Appnext $100 |
| Google Search | +$90/wk | Twitter |
| Meta App iOS TR | +$101/wk | Onboarding Meta |
| Meta LTV Test EG | +$285/wk | Meta W2A prospecting |
| Reserve / buffer | +$425/wk | Appnext remainder |

---

## ✈️ Post-Pause Verification (48h after)

- [ ] Check each platform: confirm $0 spend accruing on paused campaigns
- [ ] Verify Appnext: any residual installs = additional fraud evidence
- [ ] Verify reallocated budgets are live and spending on target channels
- [ ] Update [campaign-commentary](campaign-commentary-mar22.md) with pause confirmation dates
- [ ] Send Appnext refund email if not already sent

---

*Reference documents:*
- [Campaign Commentary — Mar 22](campaign-commentary-mar22.md)
- [Demand Gen Pause Memo](demand-gen-pause-memo.md)
- [Appnext Fraud Summary](appnext-fraud-summary.md)
