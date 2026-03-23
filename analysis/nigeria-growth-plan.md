# Nigeria Growth Plan (Post-KYC Fix)

**Date:** 2026-03-21  
**Status:** 🟡 Pending — blocked on KYC pre-conditions  
**Owner:** Performance Marketing  

---

## 1) Current State

Nigeria is Cenoa's **highest-potential, lowest-cost market** — but the funnel is completely broken at KYC.

| Metric | Value | Source |
|--------|------:|--------|
| Weekly installs | 458 | Amplitude Mar 14–20 |
| CPI (paid) | **$0.35** | Sheets Mar 9–15 |
| Cost/Virtual Account | **$2** | Sheets Mar 9–15 |
| Cost/Paid Active | **$16** | Sheets Mar 9–15 |
| KYC submits | **0** | Amplitude Mar 14–20 |
| Weekly withdrawals | 492 | Amplitude Mar 14–20 |
| Weekly deposits tapped | 1,185 | Amplitude Mar 14–20 |

**Inverted funnel:** Withdrawals (492) > installs (458). Existing Nigerian users are power-transactors — they withdraw more than the market installs each week. This is a retention signal: the product has real demand from legacy users who completed KYC before the current flow broke.

**Deposit-first market:** Nigeria is the **only country** where "Deposit Tapped" is the #1 feature action (45.2% of all deposit taps globally). Nigerian users index 2× on deposit vs Turkey (18.1% of NG feature mix vs 9.1% for TR).

**Mostly organic:** Mar 9–15 paid spend was only **$229** — virtually all of NG's 458 installs are organic. This is free demand waiting to be activated.

---

## 2) Pre-Conditions (Must Fix Before Scaling)

### 🔴 Pre-Condition A: Fix AI Survey Rejection Rate (70% → target 40%)

| Metric | Current | Target |
|--------|--------:|-------:|
| Survey evaluations/week | 226 | — |
| Approval rate | **30.1%** | **60%** |
| Approved users/week | 68 | ~136 |
| Rejected users/week | 158 | ~90 |

The Pre-KYC AI survey rejects **70% of Nigerian applicants**. This is the primary volume killer.

**Action items:**
- Get rejection reason distribution from engineering
- Audit survey criteria — is the threshold calibrated for NG population?
- A/B test more permissive threshold; measure downstream fraud rates
- Target: reduce rejection to ≤40% (approval rate ≥60%)

### 🔴 Pre-Condition B: Fix Bridgexyz Handoff Bug (0% → 100%)

| Metric | Current | Target |
|--------|--------:|-------:|
| Approved users reaching Bridgexyz | **0** | 100% |
| Bridgexyz KYC shown | **0** | = approved count |
| KYC submit | **0** | 60%+ of shown |

Even the 68 users who **pass** the AI survey never see the Bridgexyz KYC component. This is a technical bug — approved status does not trigger the Bridgexyz component render.

**Action items:**
- Engineering to trace post-approval event flow
- Add observability between "Pre-KYC Approved" → "Bridgexyz KYC Shown"
- Verify Bridgexyz supports Nigerian documents (NIN, BVN, International Passport)
- If unsupported: evaluate Smile Identity, Dojah, or Youverify as NG-specific providers

### Combined Fix Impact Estimate

```
Current:  226 evaluated → 68 approved → 0 KYC shown → 0 completed
Target:   226 evaluated → 136 approved → 136 shown → ~82 completed (60% rate)
```

**~82 new verified users/week from existing organic traffic alone — at zero incremental spend.**

---

## 3) Organic Base Leverage

Nigeria already gets significant organic installs without paid media:

| Metric | Value | Calculation |
|--------|------:|-------------|
| Total organic installs (global) | ~632/wk | Amplitude (paid-attributed subtracted) |
| NG share of installs | ~32% | 458/1,446 total |
| Estimated NG organic installs | **~200/wk** | 632 × 32% |

**These 200 weekly organic installs are free.** Once KYC is fixed:
- At 60% survey approval → 120 reach Bridgexyz
- At 60% KYC completion → **~72 verified users/week**
- At current $2/VirtAcc efficiency → equivalent value of **$144/week in saved CAC**

**Priority:** Fix KYC first, then measure organic conversion before adding paid spend. The organic baseline provides a free control group.

---

## 4) Paid Test Plan: Google Search Pilot

Once KYC pre-conditions are met, run a controlled paid test:

### Why Google Search (not Meta/TikTok)
- NG users show **high deposit intent** — Search captures active seekers ("send money to Nigeria", "USD account Nigeria", "crypto withdrawal Nigeria")
- Lower fraud risk than social (intent-based vs impression-based)
- Easier to measure true incremental lift over organic baseline

### Test Parameters

| Parameter | Phase 1 | Phase 2 | Phase 3 |
|-----------|---------|---------|---------|
| **Monthly budget** | $1,000 | $2,000 | $4,000 |
| **Duration** | 30 days | 30 days | 30 days |
| **Target CPI** | ≤$1.00 | ≤$1.50 | ≤$2.00 |
| **Keyword themes** | USD account, money transfer, crypto withdrawal | + brand, competitor terms | + broad match expansion |
| **Bid strategy** | Manual CPC | Target CPA | Target CPA |
| **Gate to next phase** | Install→Active ≥5% | CAC/Active ≤$25 | Sustained volume + CAC |

### Measurement Framework
- **Primary KPI:** Cost per Paid Active user
- **Secondary KPIs:** Install→Signup rate, Signup→KYC rate, KYC→Active rate
- **Control:** Organic baseline (track organic installs separately via AppsFlyer)
- **Stat sig:** Need ~200 installs/phase minimum for directional reads (not full stat sig at $1K)

---

## 5) Referral Opportunity

Nigerian users are **power withdrawers** — 492 withdrawals/week from an existing base. This makes them ideal referral sources:

### Why NG users are perfect for referral
- **High transaction frequency** → more in-app touchpoints to prompt referral
- **Deposit-first behavior** → new referrals likely also deposit-intent (high LTV)
- **Strong social networks** → Nigerian fintech adoption is heavily word-of-mouth
- **Low CAC benchmark** → even modest referral rewards ($1-2) are competitive

### Referral Design Suggestions
- **Trigger:** Post-withdrawal success screen ("Share Cenoa, earn $X")
- **Incentive:** Both-sides reward ($2 referrer + $2 referee on first deposit)
- **Goal:** 5-10% of active users referring → 25-50 referral installs/week
- **Budget:** $2-4 per referred user (still cheaper than Turkey's $35/VirtAcc)

---

## 6) Target Metrics (30/60/90 Day)

### Assumes: KYC fixes deployed by Day 0

| Metric | Day 30 | Day 60 | Day 90 |
|--------|-------:|-------:|-------:|
| **Weekly installs** | 250 (organic) | 350 (organic + paid P1) | 500 (paid scaling) |
| **Cumulative installs** | 1,000 | 2,400 | 4,400 |
| **Weekly KYC completions** | 50 | 80 | 120 |
| **Cumulative KYC** | 200 | 520 | 1,000 |
| **Weekly new actives** | 15 | 30 | 50 |
| **Cumulative actives** | 60 | 180 | 380 |
| **Paid spend (cumulative)** | $0 (organic only) | $1,000 (P1 test) | $3,000 (P1+P2) |
| **Blended CAC/Active** | $0 (organic) | $5.56 | $7.89 |

### Success Criteria for Scale Decision
- **Go (scale to $4K/mo):** CAC/Active ≤$20, KYC completion rate ≥40% of shown
- **Iterate:** CAC/Active $20-40, adjust targeting/creatives, extend test
- **Kill:** CAC/Active >$40 or KYC completion rate <20%

---

## 7) Risks

| Risk | Likelihood | Impact | Mitigation |
|------|:----------:|:------:|------------|
| KYC fix takes >4 weeks | Medium | High | Parallel-track alternative KYC provider evaluation |
| Survey threshold change increases fraud | Medium | High | Monitor fraud rates weekly; set fraud rate kill switch at 2× baseline |
| Low test volume → no stat sig | High | Medium | Accept directional reads at P1; combine with organic data for larger sample |
| Bridgexyz doesn't support NG documents | Medium | Critical | Pre-validate document support before committing; have Smile Identity/Dojah as backup |
| Naira deposit/withdrawal rails unreliable | Low | High | Test deposit flow end-to-end before launching paid campaigns |
| Organic installs decline | Low | Medium | Monitor weekly; organic has been stable at ~200/wk for 4+ weeks |

---

## 8) Budget Plan

### Phased Budget (Paid Media Only)

| Phase | Timeline | Monthly Budget | Cumulative | Gate |
|-------|----------|---------------:|-----------:|------|
| **Phase 0** | Weeks 1-4 | $0 | $0 | Fix KYC + measure organic conversion |
| **Phase 1** | Weeks 5-8 | $1,000 | $1,000 | Organic KYC rate ≥30% |
| **Phase 2** | Weeks 9-12 | $2,000 | $3,000 | Paid CAC/Active ≤$25 |
| **Phase 3** | Weeks 13-16 | $4,000 | $7,000 | Sustained CAC + volume |

### Total Budget Ask: $7,000 over 4 months (worst case)

**Compare to Turkey:**
- TR spends ~$35/VirtAcc and ~$864/Paid Active
- NG target: $2-5/VirtAcc and $16-25/Paid Active
- **NG is 7-17× more cost-efficient** if the funnel works

### Referral Budget (Separate)
- $500 seed budget for referral rewards
- Self-funding if referral CAC < paid CAC (expected)

---

## Appendix: Data Sources

- `analysis/nigeria-funnel.md` — Amplitude funnel data (Mar 14–20)
- `analysis/pre-kyc-survey-investigation.md` — AI survey rejection analysis
- `analysis/country-cac.md` — Country-level CAC comparison
- `analysis/feature-engagement.md` — Feature usage by country
- `data/sheets-cac-analysis.json` — Weekly spend + outcomes from Sheets

---

*This plan activates only after KYC pre-conditions are met. Phase 0 (organic measurement) can begin immediately upon fix deployment. Do not allocate paid budget until organic KYC conversion is validated.*


---

> ⚠️ **Attribution caveat:** Web campaigns (Meta/Google → cenoa.com → app store) may appear as "Organic" or "(none)" due to broken web→app attribution. Estimated correction factor: ~6.9×. See [attribution-reconciliation.md](attribution-reconciliation.md) for details.
