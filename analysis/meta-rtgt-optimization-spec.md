# Meta Retargeting Optimization Spec — Egypt Market

**Created:** 2026-03-23  
**Sprint:** 060  
**Task:** S3-019  
**Status:** Actionable — ready for execution  
**Dependencies:** [meta-underperforming.md], [meta-budget-reallocation.md], [lookalike-reco.md], [arabic-lp-content-spec.md]

---

## 1. Current Meta State: Egypt — The Problem

| Metric | Value | Verdict |
|--------|------:|---------|
| **Weekly spend (EG)** | $1,449 | Burning cash |
| **Cost per Active (EG blended)** | $483 | Catastrophic |
| **Withdrawals from EG prospecting** | 0 | Zero downstream value |
| **EG campaigns live since** | Mar 18–20 | 5 days, no signal |

**Context from meta-underperforming.md:**
- `EG_Meta_web2app_CVR_Android` (launched Mar 18): 44 installs, 3 sign-ups, **0 withdrawals**
- `EG_Meta_web2app_ALL` (launched Mar 20): 20 installs, 4 sign-ups, **0 withdrawals**
- `meta_get_paid_test` collapsed from $96/active (wk1) to $637/active (wk2)
- Only `meta_ltv_test` shows promise at $68/active — but this is the exception, not the rule

**Bottom line:** Egypt Meta prospecting is spending $1,449/week to produce zero paying users. At $483 CAC, we'd need to acquire 207 users to match what the same budget produces on Google Pmax ($19/active). This is not optimization territory — it's a structural failure.

---

## 2. What to Pause: ALL Meta EG Prospecting

### 🛑 Immediate Pause — All Egypt Prospecting Campaigns

| Campaign | Weekly Spend | Action | Rationale |
|----------|------------:|--------|-----------|
| `EG_Meta_web2app_CVR_Android` | ~$500 | **PAUSE** | 44 installs → 0 withdrawals in 5 days. W2A structural friction. |
| `EG_Meta_web2app_ALL` | ~$500 | **PAUSE** | 20 installs → 0 withdrawals. Just launched, but same broken flow. |
| `meta_get_paid_test` (EG) | ~$637 | **PAUSE** | Collapsed from $96 to $637/active in one week. Unsustainable decline. |
| **Total paused** | **~$1,449/wk** | | **$5,796/mo freed** |

### ✅ Keep Running (EG)

| Campaign | Weekly Spend | Reason |
|----------|------------:|--------|
| `meta_ltv_test` (EG) | ~$800–1,400 | **Best Meta campaign at $68/active.** Keep and monitor. This is the only EG campaign proving Meta can work with right targeting. |

### ⚠️ Exception: TR Retargeting

| Campaign | Weekly Spend | Reason |
|----------|------------:|--------|
| `TR_Meta_web2app_RTGT` | ~$600 | Only W2A campaign with proven withdrawals (9/wk). Keep at current budget — model for EG retargeting. |

---

## 3. Retargeting Audiences to Create

Replace prospecting with warm-audience retargeting. These audiences have already shown intent — they just need a nudge.

### Audience A: Website Visitors (cenoa.com, last 30 days)

| Parameter | Value |
|-----------|-------|
| **Source** | Meta Pixel on cenoa.com |
| **Window** | Last 30 days |
| **Size (est.)** | ~6,317 sessions/week × 4 weeks = ~25K unique visitors |
| **Exclusions** | Existing app installers, existing customers (KYC completed) |
| **Use case** | Broadest retargeting pool — captures all site visitors who didn't convert |
| **Creative angle** | "You checked us out — here's why freelancers switch" |
| **Priority** | 🟡 Medium — large pool but mixed intent |

### Audience B: App Installers Who Didn't Sign Up (last 14 days)

| Parameter | Value |
|-----------|-------|
| **Source** | AppsFlyer install event, NO "Cenoa sign-up completed" within window |
| **Window** | Last 14 days |
| **Size (est.)** | ~69% of installers don't sign up → significant pool |
| **Exclusions** | Users who completed sign-up |
| **Use case** | High-intent dropoffs — they downloaded but hit friction |
| **Creative angle** | "Your Cenoa account is waiting — finish setup in 3 minutes" |
| **Priority** | 🔴 High — closest to conversion, highest re-engagement potential |

### Audience C: KYC Dropoffs (started but not submitted, last 30 days)

| Parameter | Value |
|-----------|-------|
| **Source** | "KYC Started" event, NO "Bridge KYC Submit" within window |
| **Window** | Last 30 days |
| **Size (est.)** | TR dominates KYC (95%), EG pool is smaller but growing |
| **Exclusions** | Users who completed KYC |
| **Use case** | Mid-funnel rescue — they started verification but dropped |
| **Creative angle** | "Almost there — complete your verification and start receiving payments" |
| **Priority** | 🔴 High — deep funnel, strong intent signal |

### Audience D: Lookalike 1% from Withdrawers

| Parameter | Value |
|-----------|-------|
| **Source** | Users with ≥1 completed withdrawal |
| **Seed sizes** | TR: 1,177 users · NG: 778 users |
| **LAL expansion** | 1% (precision-first) |
| **Markets** | TR and NG initially; EG seed too small (23 users) — build over time |
| **Exclusions** | Existing app installers, existing customers |
| **Use case** | Prospecting replacement — find users who look like proven high-value users |
| **Creative angle** | Arabic content (EG), freelancer payment messaging (TR/NG) |
| **Priority** | 🔴 High — best prospecting seed per lookalike-reco.md |

> **Note on EG Lookalike:** Egypt has only 23 withdrawers — too small for reliable LAL. Use TR/NG withdrawer LALs targeting EG geography as a bridge until EG seed grows.

---

## 4. Creative Refresh: Arabic Content for Egypt

All EG retargeting creatives must use the Arabic content defined in [arabic-lp-content-spec.md](arabic-lp-content-spec.md).

### Key Creative Rules

| Rule | Detail |
|------|--------|
| **Language** | Egyptian Arabic dialect (عامية مصرية) — NOT Modern Standard Arabic |
| **Forbidden terms** | crypto, cryptocurrency, تداول, عملات رقمية, بورصة |
| **Framing** | "Digital wallet" / "Dollar account" |
| **Mobile-first** | >95% of EG traffic is mobile |

### Ad Copy Variants (from arabic-lp-content-spec.md)

**Variant A — Cost-first (primary):**
> بطّل تخسر فلوسك في العمولات — مع Cenoa أقل من 1%
> _Stop losing your money to fees — with Cenoa, less than 1%_

**Variant B — Speed:**
> افتح حسابك بالدولار في 3 دقايق
> _Open your dollar account in 3 minutes_

**Variant C — Savings (concrete number):**
> وفّر أكتر من 750$ في السنة على رسوم التحويلات
> _Save more than $750/year on transfer fees_

### Creative by Audience

| Audience | Primary Message | CTA |
|----------|----------------|-----|
| **Website visitors** | Variant A (cost-first) | افتح حسابك دلوقتي (Open your account now) |
| **App install dropoffs** | Variant B (speed) — "finish in 3 min" angle | ابدأ في دقايق (Start in minutes) |
| **KYC dropoffs** | Custom: "Almost done — complete verification" | كمّل التسجيل (Complete registration) |
| **Withdrawer LAL** | Variant C (savings) — value proof | افتح حسابك دلوقتي (Open your account now) |

### Trust Signals in All Creatives
- Lead Bank (FDIC-insured)
- Stripe infrastructure
- "<1% fees" prominently displayed
- Ref: arabic-lp-content-spec.md §5 for full trust signal copy

---

## 5. Budget Allocation

### Before → After

| Bucket | Before (current) | After (proposed) | Change |
|--------|------------------:|-----------------:|-------:|
| **EG Prospecting** | $1,449/wk | $0/wk | -$1,449 |
| **EG Retargeting (new)** | $0/wk | $500/wk | +$500 |
| **Net freed** | — | — | **~$949/wk** |

### Retargeting Budget Breakdown ($500/wk)

| Audience | Weekly Budget | % of Total | Rationale |
|----------|-------------:|----------:|-----------|
| App install dropoffs (Audience B) | $150 | 30% | Highest intent, closest to conversion |
| KYC dropoffs (Audience C) | $125 | 25% | Deep funnel, strong intent |
| Withdrawer 1% LAL (Audience D) | $125 | 25% | Best seed quality for prospecting replacement |
| Website visitors (Audience A) | $100 | 20% | Broadest pool, lowest intent — smaller allocation |
| **Total** | **$500** | **100%** | |

### Where the Freed ~$949/wk Goes

Per meta-budget-reallocation.md, reallocate to proven channels:

| Destination | Weekly Add | Expected Cost/Active | Expected New Actives |
|-------------|----------:|---------------------:|---------------------:|
| Google Pmax | +$450 | $19.18 | ~23 |
| Apple Search Ads | +$300 | $22.66 | ~13 |
| Google Search | +$199 | $25.48 | ~8 |
| **Total reallocated** | **$949** | **$21.54 blended** | **~44/wk** |

**Comparison:** That $949/wk was producing ~2 active users on Meta EG prospecting ($483/active). Reallocated, it produces ~44 active users. **22× improvement.**

---

## 6. Expected Outcomes

### Primary KPIs

| Metric | Current (Prospecting) | Target (Retargeting) | Improvement |
|--------|----------------------:|---------------------:|-----------:|
| **EG Meta CAC** | $483 | $150–250 | **30–50% reduction** |
| **Weekly spend (EG Meta)** | $1,449 | $500 | -65% |
| **Weekly budget freed** | — | ~$949 | For reallocation |
| **Monthly budget freed** | — | ~$3,796 | For reallocation |
| **EG withdrawals/wk (Meta)** | 0 | 2–4 (target) | From zero to measurable |

### Secondary Benefits

- **Creative learning:** Arabic A/B test data from retargeting informs future prospecting (if reactivated)
- **Audience building:** Retargeting audiences grow the EG withdrawer seed for future LALs
- **Attribution clarity:** Retargeting attribution is cleaner than W2A prospecting (direct app engagement)
- **Risk reduction:** $500/wk is a controlled test vs. $1,449/wk blind spend

### Portfolio Impact

| Scenario | Monthly Active Users (EG Meta) | Monthly Cost |
|----------|-------------------------------:|-----------:|
| Current (prospecting) | ~3 (at $483 each) | $5,796 |
| Proposed (retargeting only) | ~8–13 (at $150–250 each) | $2,000 |
| Freed budget on Google/ASA | ~176 additional | $3,796 |
| **Net improvement** | **+181–186 actives** | **$0 incremental** |

---

## 7. Measurement Plan: 2-Week A/B Test

### Test Design

| Parameter | Detail |
|-----------|--------|
| **Test period** | 2 weeks (Week 1: Mar 24–30, Week 2: Mar 31–Apr 6) |
| **Control** | Historical EG prospecting data (Mar 9–22 baseline) |
| **Treatment** | New retargeting campaigns (Audiences A–D) |
| **Primary metric** | Cost per Active User (withdrawal within 14 days of install) |
| **Secondary metrics** | Install→Signup rate, Signup→KYC rate, KYC→Withdrawal rate |
| **Success threshold** | RTGT CAC < 50% of prospecting CAC ($483 × 0.5 = $241.50) |
| **Failure threshold** | RTGT CAC > $300 after 2 full weeks → reevaluate audience definitions |

### Weekly Checkpoints

#### Week 1 (Mar 24–30): Launch & Validate

| Day | Action | Owner |
|-----|--------|-------|
| Mon Mar 24 | Pause all EG prospecting campaigns | Furkan |
| Mon Mar 24 | Create Custom Audiences (A–D) in Meta Business Manager | Furkan |
| Tue Mar 25 | Launch retargeting campaigns with Arabic creatives | Furkan |
| Wed Mar 26 | Verify campaigns are spending and delivering impressions | Furkan |
| Fri Mar 28 | Week 1 mid-check: impressions, CTR, installs, CPM | Alp |
| Sun Mar 30 | Week 1 full report: installs, sign-ups, cost/install | Alp |

#### Week 2 (Mar 31–Apr 6): Measure Downstream

| Day | Action | Owner |
|-----|--------|-------|
| Mon Mar 31 | Review Week 1 downstream (sign-ups, KYC starts) | Alp |
| Mon Mar 31 | Adjust audience budgets if one audience clearly outperforms | Furkan |
| Wed Apr 2 | Check withdrawal events from Week 1 cohort | Lucas |
| Fri Apr 4 | Week 2 mid-check: cumulative downstream metrics | Alp |
| Sun Apr 6 | **Final decision:** Compare RTGT CAC vs. prospecting CAC | Alp |

### Decision Matrix (End of Week 2)

| RTGT CAC | Prospecting CAC | Decision |
|----------|----------------|----------|
| < $150 | $483 | ⭐ Scale retargeting to $750/wk, keep prospecting paused |
| $150–$250 | $483 | ✅ Continue retargeting at $500/wk, prospecting stays paused |
| $250–$350 | $483 | ⚠️ Optimize audiences/creatives, extend test 2 more weeks |
| > $350 | $483 | 🚩 Reevaluate — check audience sizes, creative quality, attribution |
| > $483 | $483 | 🛑 Pause retargeting too. Meta EG is structurally broken. Reallocate 100% to Google/ASA. |

### Reporting Template

```
WEEKLY RTGT REPORT — Egypt Meta
================================
Period: [date range]
Budget spent: $[X] / $500 target

AUDIENCE PERFORMANCE:
| Audience           | Spend | Installs | Signups | KYC | Withdrawals | CAC   |
|--------------------|-------|----------|---------|-----|-------------|-------|
| Website visitors   | $     |          |         |     |             | $     |
| Install dropoffs   | $     |          |         |     |             | $     |
| KYC dropoffs       | $     |          |         |     |             | $     |
| Withdrawer LAL 1%  | $     |          |         |     |             | $     |
| TOTAL              | $     |          |         |     |             | $     |

COMPARISON:
- Prospecting CAC (baseline): $483
- Retargeting CAC (this week): $[X]
- Delta: [X]% [better/worse]

DECISION: [Continue / Optimize / Pause / Scale]
```

---

## 8. Implementation Checklist

### Pre-Launch (Mar 24)

- [ ] Pause `EG_Meta_web2app_CVR_Android`
- [ ] Pause `EG_Meta_web2app_ALL`
- [ ] Pause `meta_get_paid_test` (EG)
- [ ] Screenshot all paused campaigns (baseline documentation)
- [ ] Create Meta Custom Audience: Website Visitors (cenoa.com, 30d)
- [ ] Create Meta Custom Audience: App Installers No Signup (14d)
- [ ] Create Meta Custom Audience: KYC Started No Submit (30d)
- [ ] Create Meta Lookalike: 1% from Withdrawers (use TR+NG seed → EG geo)
- [ ] Upload Arabic ad creatives (3 headline variants × 4 audiences)
- [ ] Set up exclusion lists (existing customers, withdrawers, KYC completers)
- [ ] Configure budget: $500/wk split per §5 allocation

### Launch (Mar 25)

- [ ] Activate all 4 retargeting ad sets
- [ ] Verify Meta Pixel firing on cenoa.com for audience building
- [ ] Verify AppsFlyer events flowing for install/signup/KYC audiences
- [ ] Set up daily spend alerts (flag if any audience overspends allocation)

### Post-Launch Monitoring

- [ ] Daily: Check spend pacing and delivery
- [ ] Day 3: First CTR/CPM review
- [ ] Day 7: Week 1 report (template above)
- [ ] Day 14: Final decision report + next steps

---

## Summary

**The play:** Kill $1,449/wk in catastrophic EG Meta prospecting ($483 CAC, 0 withdrawals). Replace with $500/wk surgical retargeting across 4 warm audiences. Free ~$949/wk for proven channels (Google Pmax, ASA, Google Search).

**Why it works:**
1. Retargeting audiences have **proven intent** — they've already visited, installed, or started KYC
2. Arabic-first creatives match the market (Egyptian dialect, mobile-first, fee-focused messaging)
3. Withdrawer LALs use the **highest-value seed** (actual money movers) instead of blind prospecting
4. $500/wk is a **controlled test** — we learn before we burn

**Expected result:** 30–50% lower CAC on Meta EG, ~$949/wk freed for channels producing actives at $19–25 each (vs. $483). Net gain: ~44 additional active users/week from reallocation alone.

**Timeline:** 2-week test starting Mar 24. Decision by Apr 6.

---

*Generated: 2026-03-23 | Task: S3-019 | Sprint 060*
