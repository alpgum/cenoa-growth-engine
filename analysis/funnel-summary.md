# Cenoa Funnel Summary — Executive Report
**Period:** March 14–20, 2026  
**Sources:** Amplitude, AppsFlyer, Google Sheets, BigQuery  
**Generated:** 2026-03-21

---

## One-Page Summary

### Key Numbers (Mar 14–20)

| Metric | Value | WoW |
|--------|------:|-----|
| Installs | 1,445 | ↓ 36.5% |
| Sign-ups | 1,207 | ↓ 27.8% |
| KYC Submits | 179 | ↓ 41.7% |
| Deposits | 1,546 | ↓ 5.8% |
| Withdrawals | 2,227 | ↑ 0.6% |
| DAU (avg) | 3,060 | ↓ 46.1% |

### The 3 Biggest Issues

1. **🚨 KYC is broken outside Turkey.** Nigeria (230 KYC starts → 0 submits), Egypt (62 starts → 0 submits), Pakistan (17 starts → 0 submits). The BridgeXYZ KYC component never renders for non-TR users. Only 7 countries have any KYC submits at all — Turkey accounts for **95% (170/179)**. This single issue blocks activation in every growth market.

2. **🚨 Even in Turkey, KYC leaks 94%.** Of 3,025 users who see the BridgeXYZ component, only 170 submit (5.6%). iOS is 3.8× worse than Android (2.4% vs 9.2% Shown→Submit). The KYC UX is a conversion killer on every platform.

3. **⚠️ Low-quality paid channels burning budget.** appnext delivered 273 installs with 1 withdrawal (0.4% conversion). TikTok: 49 installs, 0 withdrawals. Meanwhile Apple Search Ads: 75 installs, 254 withdrawals. Channel quality variance is extreme and budget allocation doesn't match.

---

## Full Funnel (Global, Mar 14–20)

```
Install          1,445  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  100%
  │ 83.5%
Sign-up          1,207  ━━━━━━━━━━━━━━━━━━━━━━━━━       83.5%
  │ 14.8%
KYC Submit         179  ━━━                              12.4%
  │ (mixed cohort below)
Deposit          1,546  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   (includes returning users)
Withdrawal       2,227  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  (includes returning users)
```

**Critical conversion rates:**
| Step | Rate | Verdict |
|------|-----:|---------|
| Install → Sign-up | 83.5% | ✅ Healthy |
| Sign-up → KYC Submit | 14.8% | ⚠️ Major leak |
| KYC Started → KYC Submit | 5.8% | 🚨 Critical — 94.2% dropout |
| KYC Shown → KYC Submit | 5.7% | 🚨 UX failure at component level |

---

## Country Comparison

| Metric | Turkey | Nigeria | Egypt | Pakistan |
|--------|-------:|--------:|------:|---------:|
| **Installs** | 670 (46%) | 458 (32%) | 206 (14%) | 23 (2%) |
| **Sign-ups** | 226 | 117 | 64 | 15 |
| **Install→Signup** | 33.7%¹ | 25.5% | 31.1% | 65.2% |
| **KYC Started** | 2,594 | 230 | 62 | 17 |
| **KYC Component Shown** | 3,025 | **0** | **0** | **0** |
| **KYC Submit** | **170** | **0** | **0** | **0** |
| **KYC Started→Submit** | 6.6% | 🚫 0% | 🚫 0% | 🚫 0% |
| **Deposits** | 840 (54%) | 300 (19%) | 22 (1%) | 0 |
| **Withdrawals** | 1,260 (57%) | 492 (22%) | 23 (1%) | 0 |
| **CAC (virtual acct)** | $35 | — | $8 | — |

¹ Turkey Install→Signup appears low due to 754 unattributed "(none)" sign-ups — real rate likely 50-60%.

**Key insight:** Turkey is the only functioning end-to-end funnel. Nigeria has 68% of Turkey's install volume but 0% of its KYC completions. Egypt has 5× cheaper CAC but a completely blocked funnel.

### Feature Engagement Mix (normalized per country)

| Feature | Turkey | Nigeria | Egypt |
|---------|-------:|--------:|------:|
| Get Paid | 29.8% | 36.9% | 35.1% |
| Money Transfer | 29.8% | 28.3% | 13.9% |
| Deposit | 9.1% | **18.1%** | 13.0% |
| Debit Card | **31.3%** | 16.7% | **38.0%** |

- Nigeria is deposit-first (highest Deposit share at 18.1%)
- Egypt is card-curious (38% of engagement on Debit Card tab)
- Turkey splits evenly between card, transfer, and get-paid

---

## Platform Comparison

| Metric | Android | iOS | Web |
|--------|--------:|----:|----:|
| **Installs** | 1,275 (88%) | 170 (12%) | — |
| **Sign-ups** | 221 (18%) | 232 (19%) | 754 (63%) |
| **KYC Submit** | 140 (78%) | 39 (22%) | 0 |
| **KYC Shown→Submit** | **9.2%** | **2.4%** | — |
| **Deposits** | 718 (46%) | 813 (53%) | 15 (1%) |
| **Withdrawals** | 1,033 (46%) | 1,187 (53%) | 7 (<1%) |

**Key findings:**
- **Android dominates installs** (88%) but iOS dominates monetization (53% of deposits/withdrawals)
- **iOS KYC submit rate is 3.8× worse than Android** (2.4% vs 9.2%) — likely a UX/SDK bug
- **Web captures 63% of sign-ups** but converts almost none downstream (2% deposit rate) — web→app handoff is broken
- iOS users are higher-value but get 7.5× less acquisition budget

---

## Channel Quality Ranking

Ranked by downstream conversion quality (withdrawals per install):

| Rank | Channel | Installs | Withdrawals | Signup % | Quality |
|------|---------|----------|-------------|----------|---------|
| 1 | **af_app_invites** (Referral) | 7 | 13 | 42.9% | ⭐⭐⭐ Best per-user |
| 2 | **Apple Search Ads** | 75 | 254 | 29.3% | ⭐⭐⭐ Best at scale |
| 3 | **Google Ads** | 54 | 29 | 25.9% | ⭐⭐ High quality |
| 4 | **cenoa.com** | 69 | 8 | 26.1% | ⭐ Decent signup |
| 5 | **Organic** | 632 | 487 | 12.2% | ⭐⭐⭐ Backbone |
| 6 | **byteboost2_int** | 71 | 34 | 12.7% | ⚠️ Moderate |
| 7 | **zzgtechltmqk_int** | 120 | 22 | 16.7% | ⚠️ Watch closely |
| 8 | **Architect (NG)** | 73 | 0 | 26.0% | 🚩 Good signup, 0 withdrawals |
| 9 | **TikTok** | 49 | 0 | 16.3% | 🚩 Zero downstream |
| 10 | **appnext_int** | 273 | 1 | 8.8% | 🚩 CPI fraud pattern |

**Best campaign:** `tr_asa_appinstall_brand_exact` — 26 installs, 114 withdrawals (historical LTV)  
**Worst campaign:** `Cenoa_CPI_UA_TR` (appnext) — 273 installs, 1 withdrawal (already paused)

---

## KYC Bottleneck — The #1 Issue

### The Problem

KYC is a **two-layer failure:**

**Layer 1: Non-TR users never see the KYC component**
- BridgeXYZ KYC Component Shown = **0** for Nigeria, Egypt, Pakistan, Ghana, Indonesia
- Users fire `KYC Started` but the Bridge component never renders
- Root cause: BridgeXYZ likely doesn't support these countries' documents, or there's a country/eligibility gate before the component loads

**Layer 2: Even when shown (TR), 94.4% abandon**
- 3,025 component impressions → 170 submits (5.6%)
- iOS is 3.8× worse than Android (2.4% vs 9.2%)
- Likely causes: document capture friction, upload failures, validation errors, unclear UX

### Evidence Summary

| Country | KYC Started | Component Shown | Submit | Submit Rate |
|---------|------------:|----------------:|-------:|------------:|
| Turkey | 2,594 | 3,025 | 170 | 5.6% (Shown→Submit) |
| Nigeria | 230 | 0 | 0 | 🚫 Blocked |
| Egypt | 62 | 0 | 0 | 🚫 Blocked |
| Pakistan | 17 | 0 | 0 | 🚫 Blocked |
| Ghana | 22 | 0 | 0 | 🚫 Blocked |

### Paradox: Withdrawals exist without KYC

Nigeria has 492 withdrawals and Egypt has 23 withdrawals despite 0 KYC submits this week. These are legacy/returning users who completed KYC previously (different provider or manual verification). This proves **demand exists** — the product works, users transact, but new users can't get through KYC.

### Impact If Fixed

- **Nigeria alone:** ~230 KYC starts × 11% TR benchmark = ~25 additional submits/week (conservative)
- **All non-TR markets:** Could add 50-100+ KYC submits/week, nearly doubling the 179 current total
- **Egypt specifically:** 5× cheaper CAC than Turkey — fixing KYC here is the highest-ROI move

---

## Retention & Engagement Health

| Metric | Value |
|--------|-------|
| Avg DAU (7d) | 3,075 |
| Avg DAU (30d) | 5,044 |
| DAU/Cumulative Signups | ~50.5% |
| Withdrawal trend | Flat (+0.6% WoW) |

- Existing user base is **stable and transacting** — withdrawals held steady despite install decline
- DAU dropped 46% WoW — correlated with install volume drop, needs monitoring
- True cohort retention (D1/D7/D30) unavailable via API — requires Amplitude UI or BigQuery export

---

## Top 10 Action Items (Prioritized)

| # | Action | Impact | Effort | Owner |
|---|--------|--------|--------|-------|
| 1 | **Confirm BridgeXYZ country support** — get hard yes/no for NG, EG, PK, GH | 🔴 Critical | Low | Product/Eng |
| 2 | **Add alternative KYC for non-TR markets** — Smile Identity (NG), Dojah, or Youverify | 🔴 Critical | High | Product/Eng |
| 3 | **Fix iOS KYC submit** — investigate 2.4% vs Android's 9.2% (3.8× gap) | 🔴 High | Medium | Eng |
| 4 | **Kill low-quality channels** — confirm appnext stays off, pause TikTok, set review date for zzgtechltmqk | 🟡 High | Low | Growth |
| 5 | **Scale Apple Search Ads** — best paid channel, expand to broad + generic + competitor terms | 🟡 High | Medium | Growth |
| 6 | **Fix web→app handoff** — 754 web sign-ups converting at 2% to deposit is a massive leak | 🟡 High | Medium | Product/Eng |
| 7 | **Increase iOS acquisition budget** — iOS users are 13-15% more valuable at monetization | 🟡 Medium | Low | Growth |
| 8 | **Cap Egypt spend until KYC is fixed** — $5.5K/mo flowing into a blocked funnel | 🟡 Medium | Low | Growth |
| 9 | **Instrument KYC failure events** — add `kyc_error_type`, `kyc_provider_response` by country | 🟡 Medium | Medium | Eng |
| 10 | **Invest in referral program** — 42.9% signup rate, highest quality per-user channel | 🟢 Medium | Medium | Product |

### Attribution & Measurement Fixes (Parallel Track)

- Audit AppsFlyer attribution settings — 986 unattributed sign-ups (82% of total) masks true channel ROI
- Extend AF lookback window, fix web→app attribution passthrough
- Set up Amplitude Retention chart for true D1/D7/D30 cohort analysis

---

## Bottom Line

**The funnel has one dominant failure mode: KYC.** Fix KYC for non-TR markets and improve the iOS KYC flow, and the business roughly doubles its activation pipeline. Everything else — channel optimization, platform mix, retention — is secondary until the KYC wall is removed. Turkey carries the business today; Nigeria and Egypt are the unlock.

---

*Compiled from: global-funnel.md, turkey-funnel.md, nigeria-funnel.md, egypt-funnel-activation-gap.md, pakistan-funnel.md, platform-funnel.md, attribution-funnel.md, kyc-dropout-deepdive.md, retention.md, feature-engagement.md*
