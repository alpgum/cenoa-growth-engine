# Meta Ads — Underperforming Campaign Identification & Reallocation Plan

**Date:** 2026-03-21 | **Sprint:** 057  
**Sources:** Sheets CaC Analysis, Amplitude attribution funnel, channel-cac scorecard, meta-ads-analysis

---

## 1. All Meta Campaigns/Channels — Performance Summary

### Turkey (Primary Market)

| Campaign / Channel | Period | Spend | Installs | Sign-ups | VirtAcc | New Active | Paid Active | Cost/Active | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **meta_w2a** (Web2App) | Jan 2026 | $10,607 | 1,405 | 987 | 100 | — | 3 | **$3,536** | 🚩 STOP |
| **meta_w2a** | Dec 2025 | $4,497 | — | 400 | 71 | — | 4 | **$1,124** | 🚩 |
| **meta_w2a** | Nov 2025 | $4,378 | — | 144 | 16 | — | — | n/a (0?) | 🚩 |
| **meta_w2a** | Feb 1-7, 2026 | $1,452 | 213 | 136 | 9 | — | 0 | **∞** | 🚩 |
| **meta_w2a** | Feb 1-15, 2026 | $3,188 | 607 | 409 | 124 | 48 | 0 | **∞** (0 paid) | 🚩 |
| **meta_w2a** | Mar 1-8, 2026 | $741 | 82 | 62 | 54 | 16 | 0 | n/a | ⚠️ |
| **meta_w2a** | Mar 9-15, 2026 | $485 | 122 | 38 | 31 | 6 | 0 | n/a | 🚩 |
| **meta_app** (App Install) | Jan 2026 | $852 | 313 | 184 | 39 | — | 4 | **$213** | ⚠️ |
| **meta_app** | Feb 1-7, 2026 | $667 | 166 | 77 | 18 | — | 1 | **$667** | ⚠️ |
| **meta_app_ios** | Feb 1-15, 2026 | $936 | 164 | 107 | 49 | 32 | 1 | **$936** | ⚠️ |
| **meta_app_ios** | Mar (planned) | $3,000 | — | — | — | — | — | — | Budget |
| **onboarding_meta_test** | Mar 9-15 | $101 | 3 | 3 | 4 | 0 | 0 | — | 🚩 Tiny |

### Egypt (Growing Market)

| Campaign / Channel | Period | Spend | Installs | Sign-ups | VirtAcc | New Active | Paid Active | Cost/Active | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **meta_get_paid_test** | Mar 1-8 | $1,340 | 266 | 194 | 58 | 20 | 14 | **$96** | ⭐ Keep |
| **meta_get_paid_test** | Mar 9-15 | $637 | 107 | 58 | 12 | 2 | 1 | **$637** | ⚠️ Declining |
| **meta_ltv_test** | Mar 1-8 | $1,392 | 158 | 86 | 20 | 8 | 8 | **$174** | ⭐ Promising |
| **meta_ltv_test** | Mar 9-15 | $812 | 244 | 111 | 37 | 15 | 12 | **$68** | ⭐⭐ Best Meta |

### Attribution-Level (zzgtechltmqk_int = Meta W2A identifier)

| Campaign | Week Mar 14-20 | Installs | Sign-ups | Withdrawals | Quality |
|---|---|---:|---:|---:|---|
| TR_Meta_web2app_RTGT | Retargeting | 17 | 6 | 9 | ⭐ Only W2A campaign with withdrawals |
| EG_Meta_web2app_CVR_Android | New (Mar 18) | 44 | 3 | 0 | 🚩 Too early / low quality |
| EG_Meta_web2app_ALL | New (Mar 20) | 20 | 4 | 0 | ⚠️ Just launched |
| 1764668627 (legacy) | Historical | — | — | 76 | ⭐⭐ Proves Meta CAN work |

---

## 2. Underperformer Flags

### 🚩 Flag 1: meta_w2a (Turkey) — $3,536/active, Structural Downstream Failure

**The numbers are damning:**
- Jan 2026: $10,607 spend → 987 sign-ups → only **3 paid active users** → **$3,536/active**
- Dec 2025: $4,497 → 400 sign-ups → **4 paid active** → **$1,124/active**
- Nov 2025: $4,378 → 144 sign-ups → 16 VirtAcc → **0 paid active reported**
- Feb 2026: $3,188 (half-month) → 409 sign-ups → 124 VirtAcc → **0 paid active**

**Comparison to other channels (Jan 2026, Turkey):**

| Channel | Spend | Paid Active | Cost/Active | vs meta_w2a |
|---|---:|---:|---:|---|
| meta_w2a | $10,607 | 3 | $3,536 | — |
| meta_app | $852 | 4 | $213 | **16.6× cheaper** |
| apple_ads | $2,817 | 18 | $157 | **22.5× cheaper** |
| referral_affi | $300 | 10 | $30 | **117.9× cheaper** |
| pmax_search | — | — | — | (not in Jan data) |

**Root cause: Structural, not fixable by creative optimization alone.**

1. **Funnel friction:** W2A flow = ad → landing page → app store → download → open → sign up → activate. Each step loses 40-60%. Direct install campaigns skip 2-3 steps.
2. **Attribution collapse:** W2A breaks attribution at every handoff. The 986 unattributed sign-ups and 1,355 unattributed withdrawals are partially Meta W2A users lost in the "(none)" bucket — but even generous attribution doesn't fix $3,536/active.
3. **Optimization signal delay:** Active user event happens days/weeks post-install. Meta's ML can't optimize to this target within its attribution window.
4. **VirtAcc→Active collapse:** In Jan, meta_w2a got 100 VirtAcc but only 3 became active (3% conversion). Apple Ads got 80 VirtAcc → 18 active (22.5%). The *quality* of W2A users is fundamentally lower.

**Verdict:** Even if attribution captured 50% more conversions, meta_w2a would still be the worst channel by 5-10×. This is a structural failure.

### 🚩 Flag 2: zzgtechltmqk_int — High Install Volume, Attribution Gap

**What we see in attribution (Mar 14-20):**
- 120 installs (spiked from 5/day to 44/day by Mar 20 — new campaigns launching)
- 20 sign-ups (16.7% install→signup, below Google 25.9% and ASA 29.3%)
- 22 withdrawals (includes historical cohorts, not same-week)

**The gap:** 120 installs → 20 sign-ups is middling, but the attribution data doesn't match Sheets:
- Sheets shows meta_web2app Mar 9-15: 122 installs, 38 sign-ups, 31 VirtAcc, 6 New Active
- Attribution shows similar installs but fewer sign-ups — suggesting attribution loss between install and sign-up events

**Risk:** Volume is scaling fast without evidence of quality improving. Egypt W2A campaigns just launched (Mar 18-20) with zero withdrawals so far.

### 📊 Flag 3: Meta App vs Meta W2A — Head-to-Head

| Metric | meta_app (App Install) | meta_w2a (Web2App) | Winner |
|---|---:|---:|---|
| **Jan spend** | $852 | $10,607 | app (12× less) |
| **Jan paid active** | 4 | 3 | app |
| **Jan cost/active** | $213 | $3,536 | **app (16.6×)** |
| **Feb VirtAcc/$ spent** | 18/$667 = $37/VA | 9/$1,452 = $161/VA | **app (4.4×)** |
| **Feb 1-15 new active** | 32 | 48 | w2a (volume) |
| **Feb 1-15 cost/new active** | $29 | $66 | **app (2.3×)** |
| **Feb 1-15 paid active** | 1 | 0 | app |
| **Sign-up rate** | ~46% | ~67% | w2a (misleading — web form, not app signup) |

**Key insight:** meta_app delivers better downstream users at lower cost. The W2A flow inflates sign-up numbers (web form is easier than app signup) but these users don't activate. Meta App users who go through the full app install flow self-select for higher intent.

---

## 3. Specific Pause/Scale Recommendations

### 🛑 PAUSE — Immediate

| Campaign | Current Budget | Action | Rationale |
|---|---|---|---|
| **meta_w2a (Turkey)** | $6,000/mo planned | **Pause entirely** | $3,536/active (Jan), $1,124/active (Dec). Structural failure. 4 months of consistent terrible downstream. |
| **onboarding_meta_test** | $101/wk | **Pause** | $101 for 3 installs, 0 active. Not viable at any scale. |
| **Turkey W2A retargeting exception** | ~$500/wk | **Keep at reduced budget** | TR_Meta_web2app_RTGT shows 9 withdrawals — only W2A campaign proving downstream value. Cap at $500/wk. |

### ⚠️ EVALUATE (2-week deadline: by Apr 3)

| Campaign | Current Budget | Action | Rationale |
|---|---|---|---|
| **EG_Meta_web2app_CVR_Android** | Part of Egypt budget | **Monitor** | Launched Mar 18. 44 installs, 3 sign-ups, 0 withdrawals. If no downstream by Apr 3, pause. |
| **EG_Meta_web2app_ALL** | Part of Egypt budget | **Monitor** | Launched Mar 20. Too early. Same deadline. |
| **meta_get_paid_test (Egypt)** | ~$1,000/wk | **Watch** | Declining: cost/active went from $96 (wk1) to $637 (wk2). If week 3 doesn't recover, reallocate to ltv_test. |

### ✅ SCALE — Increase Budget

| Campaign | Current Budget | Proposed | Rationale |
|---|---|---|---|
| **meta_ltv_test (Egypt)** | ~$800-1,400/wk | **Scale to $2,000/wk** | Best Meta campaign: $68/active (Mar 9-15), 12 paid active. Cost-competitive with Google. |
| **meta_app_ios (Turkey)** | $3,000/mo | **Scale to $5,000/mo** | $213/active (Jan) — bad vs ASA/Google but 16× better than W2A. Test with better creatives before scaling further. |

---

## 4. Budget Freed if Underperformers Paused

### Immediate Savings (Monthly)

| Paused Campaign | Monthly Budget | Notes |
|---|---:|---|
| meta_w2a (Turkey) — full pause | $6,000 | Planned March allocation |
| onboarding_meta_test | $400 | ~$100/wk |
| W2A RTGT (reduced, not paused) | -$2,000 | Keep $2,000/mo for RTGT |
| **Total freed** | **$4,400/mo** | Net of RTGT budget kept |

### If we include meta_app_ios scale-up offset:

| Line | Monthly |
|---|---:|
| Budget freed from W2A pause | $6,400 |
| meta_app_ios scale-up (from $3K to $5K) | -$2,000 |
| meta_ltv_test Egypt scale-up | -$2,400 |
| **Net freed for reallocation** | **$2,000/mo** |

### Alternate scenario — aggressive pause (include meta_app Turkey):

| Line | Monthly |
|---|---:|
| All Turkey Meta paused | $9,000 |
| Keep RTGT only ($2K) | -$2,000 |
| **Net freed** | **$7,000/mo** |

---

## 5. Where to Reallocate Freed Meta Budget

### Priority Reallocation Matrix

| Destination | Monthly Add | Expected Impact | Rationale |
|---|---:|---|---|
| **Apple Search Ads** | +$2,200 | ~97 additional active users | Best channel: $22.66/active. Currently at $2,800/mo — massively underinvested. Scale to $5,000. |
| **Google Search** | +$1,000 | ~39 additional active users | $25.48/active, reliable quality. Currently ~$3,200/mo. |
| **Referral/Affiliate** | +$500 | ~17 additional active users | $30/active. Highest conversion rate (42.9% signup). Scale referral program incentives. |
| **Egypt Meta ltv_test** | +$2,400 | ~35 additional active users | $68/active — proving Meta CAN work in Egypt with right targeting. |
| **Reserve / Test** | +$900 | Buffer for new tests | Keep dry powder for TikTok creative rework, new market tests. |
| **Total reallocated** | **$7,000** | **~188 additional active users** | Aggressive scenario |

### Conservative Reallocation (net $2,000 freed):

| Destination | Monthly Add | Rationale |
|---|---:|---|
| Apple Search Ads | +$1,200 | Priority #1 — proven best downstream |
| Google Search | +$500 | Incremental scale on proven channel |
| Referral program | +$300 | Low cost, high quality |
| **Total** | **$2,000** | |

### Expected Blended CAC Impact

| Scenario | Current Blended Meta Cost/Active | Projected After Reallocation |
|---|---:|---:|
| Current (all Meta, Turkey) | $82.21 | — |
| After W2A pause + ASA/Google scale | — | ~$35-45 blended across reallocated |
| Portfolio improvement | — | **52-57% reduction in Meta CAC** |

---

## Summary

**Meta Web2App (Turkey) is the single biggest budget drain in the paid portfolio.** At $3,536/active (Jan) and consistently $1,000+/active across Nov-Feb, it fails at every stage of the funnel beyond sign-up. The structural issues (funnel friction, attribution collapse, optimization signal delay) are not fixable with creative changes alone.

**Action plan:**
1. **Pause** meta_w2a Turkey immediately (keep RTGT at $2K/mo cap)
2. **Scale** meta_ltv_test Egypt ($68/active — best Meta campaign)  
3. **Reallocate** $2K-7K/mo to ASA, Google Search, and referral
4. **Fix attribution** before considering any Meta W2A reactivation
5. **Evaluate** Egypt W2A campaigns by Apr 3 — pause if no downstream

**Bottom line:** Shifting $7K/mo from failing Meta W2A to proven channels could yield ~188 additional active users — a transformative improvement in portfolio efficiency.

---

*Generated: 2026-03-21 | Sprint 057*


---

> ⚠️ **Attribution caveat:** Web campaigns (Meta/Google → cenoa.com → app store) may appear as "Organic" or "(none)" due to broken web→app attribution. Estimated correction factor: ~6.9×. See [attribution-reconciliation.md](attribution-reconciliation.md) for details.
