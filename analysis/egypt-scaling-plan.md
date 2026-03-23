# Egypt Scaling Plan (Post-KYC Fix)

**Created:** 2026-03-21  
**Sprint:** 060  
**Status:** 🟡 Blocked — awaiting pre-conditions  
**Sources:** egypt-funnel-activation-gap.md, pre-kyc-survey-investigation.md, country-cac.md, sheets-cac-analysis.md, sheets-trafik-canavari.md

---

## 1) Pre-conditions (Must Fix Before Scaling)

Egypt spend is currently burning into a **completely broken activation funnel**. Two blockers must be resolved before any budget increase:

### Blocker A: Pre-KYC AI Survey Rejection Rate (~63%)
- Egypt: 57 evaluated → 21 approved, **36 rejected** (63% rejection rate)
- The AI survey rejects nearly 2 out of 3 Egyptian applicants
- **Action:** Audit rejection criteria, calibrate threshold for EG population, A/B test more permissive settings
- **Target:** ≥50% approval rate (from current 37%)

### Blocker B: KYC Handoff Bug (0 Bridgexyz KYC Shown)
- 21 Egypt users were **approved** by the Pre-KYC survey but **none** saw the Bridgexyz KYC component
- This is a **technical bug** — approved status is not triggering component render
- **Action:** Engineering must trace the flow after `Pre-KYC Application Evaluated` with status=approved and fix the handoff
- **Target:** 100% of approved users see Bridgexyz KYC

### Combined Impact
```
Current:  62 KYC starts → 21 approved → 0 KYC shown → 0 KYC submit
Target:   62 KYC starts → 31 approved (50%) → 31 KYC shown → 19 KYC submit (60% completion)
```

**Gate:** Do NOT increase Egypt budget until KYC submit > 0 for at least 2 consecutive weeks.

---

## 2) Current State

### Acquisition (Mar 14–20)
| Metric | Value |
|---|---|
| Weekly installs | 197 |
| Weekly signups | 61 |
| KYC started | 62 (96.9% of signups — very strong intent) |
| KYC submit | **0** |
| Deposits | 23 (legacy/returning users) |
| Withdrawals | 23 (legacy/returning users) |

### Cost Efficiency (Mar 9–15)
| Metric | Egypt | Turkey | EG Advantage |
|---|---|---|---|
| Cost/Virtual Account | **$8** | $35 | **4.4× cheaper** |
| Cost/Paid Active | **$64** | $864 | **13.5× cheaper** |
| CPI | $3.60 | $2.61 | TR slightly cheaper |
| $/Signup | $6.89 | $6.63 | Comparable |

### Weekly Spend (Mar 1–15)
- Total Egypt spend: **$5,549** (41.5% of total $13,373 budget)
- Current weekly run rate: ~$1,385/week

### Key Signals
- Install trajectory accelerating: 21 → 12 → 16 → 17 → 26 → 51 → 63 (daily, Mar 14–20)
- Architect LP delivers **27% cheaper CTA** vs standard LP
- KYC follow-up messaging delivers **450% better CVR** (proven in testing)

---

## 3) Budget Allocation — Phased Ramp

### Phase 0: Hold (Current → KYC Fix)
- **Budget:** $1,500/mo (reduce from current ~$5.5K/mo run rate)
- **Purpose:** Maintain learning velocity, validate LP/creative tests only
- **Duration:** Until KYC submit > 0 for 2 consecutive weeks
- **Why reduce:** 41.5% of total budget flowing into a dead funnel is waste

### Phase 1: Validate (Month 1 post-fix)
- **Budget:** $2,000/mo
- **Purpose:** Confirm KYC funnel works end-to-end, establish baseline conversion rates
- **Focus:** Run Architect LP + KYC follow-up sequence as default
- **Success gate:** ≥15 KYC completions/week, Cost/VirtAcc ≤$12

### Phase 2: Scale (Month 2 post-fix)
- **Budget:** $4,000/mo
- **Purpose:** Expand audience targeting, test Arabic creatives, add Google channel
- **Focus:** Multi-channel (Meta + Google), Arabic LP launch
- **Success gate:** ≥30 KYC completions/week, Cost/VirtAcc ≤$15, Cost/Active ≤$80

### Phase 3: Accelerate (Month 3 post-fix)
- **Budget:** $6,000/mo
- **Purpose:** Full-scale acquisition with proven funnel
- **Focus:** Optimize winning channels, scale lookalikes, expand geo within Egypt
- **Success gate:** ≥50 KYC completions/week, Cost/VirtAcc ≤$12, Cost/Active ≤$70

---

## 4) Channel Mix

### Meta (Primary — 60-70% of Egypt budget)
- **What works:** Architect LP delivers 27% cheaper CTA clicks
- **Strategy:**
  - Phase 1: Run existing winning adsets with Architect LP as default
  - Phase 2: Launch Arabic creative variants, expand lookalike audiences
  - Phase 3: Scale winning adsets, test Advantage+ campaigns
- **Targeting:** Interest-based (crypto, remittances, savings) + lookalikes from Egypt converters
- **Formats:** App install + Web2App (test both; Web2App allows LP control)

### Google (Secondary — 20-30% of Egypt budget)
- **What works:** EG Generic campaigns show best CPI (₺325 equivalent in data)
- **Strategy:**
  - Phase 1: Not active (focus on Meta validation)
  - Phase 2: Launch Google Search (generic finance/crypto terms in Arabic)
  - Phase 3: Add Pmax, YouTube discovery
- **Why delay:** Google requires Arabic keyword research and separate campaign structure

### Apple Search Ads (Exploratory — 10% in Phase 3)
- Proven performer in Turkey ($24-35/VirtAcc)
- Launch in Phase 3 with Arabic keywords once funnel is validated

---

## 5) Arabic Creative Requirements

### Content Localization Needs

**Must-have (Phase 1-2):**
- [ ] Arabic ad copy (Meta primary text, headlines, descriptions) — RTL layout
- [ ] Arabic App Store / Play Store screenshots and descriptions
- [ ] Arabic KYC follow-up messaging (push + email — the 450% CVR lift sequence)
- [ ] Arabic error messages and KYC guidance copy

**High priority (Phase 2):**
- [ ] Arabic video ads (15s + 30s) — dubbing or native Arabic VO
- [ ] Arabic social proof / testimonial creatives
- [ ] Culturally relevant imagery (not just translated Turkish assets)
- [ ] Ramadan / local event-aligned campaigns

**Nice-to-have (Phase 3):**
- [ ] Egyptian Arabic dialect variants (vs MSA)
- [ ] Egyptian influencer / UGC content
- [ ] Arabic Google Ads copy + keyword set

### Creative Production Notes
- Egyptian Arabic (عامية مصرية) resonates better than Modern Standard Arabic (فصحى) for ads
- Financial trust signals matter: regulatory mentions, security badges, user counts
- Avoid direct crypto terminology where possible — frame around savings, transfers, USD access

---

## 6) Landing Page: Arabic LP

### Current State
- Architect LP is proven winner (27% cheaper CTA) but is in English/Turkish
- No dedicated Arabic landing page exists

### Requirements
- [ ] Arabic version of Architect LP (RTL layout, Arabic copy, Arabic CTA)
- [ ] Localized value props for Egyptian market:
  - USD savings (protect against EGP devaluation)
  - Low-fee international transfers
  - Easy onboarding (once KYC is fixed)
- [ ] Mobile-first design (Egypt is >95% mobile traffic)
- [ ] Fast load time (<3s — Egyptian mobile networks can be slow)
- [ ] Deep link to app with pre-filled country context

### Priority
- **Phase 1:** Use existing Architect LP (English) — it already outperforms
- **Phase 2:** Launch Arabic Architect LP — expected additional 15-25% CTA improvement based on localization benchmarks

---

## 7) Target Metrics — 30/60/90 Day Milestones

*All milestones start from KYC fix confirmed (submit > 0 for 2 weeks)*

### Day 30 (Phase 1 — Validate)
| Metric | Target | Current |
|---|---|---|
| Monthly budget | $2,000 | ~$5,500 |
| Weekly installs | 200+ | 197 |
| KYC completion rate | ≥25% of starts | 0% |
| KYC completions/week | ≥15 | 0 |
| Cost/Virtual Account | ≤$12 | $8 (pre-KYC fix) |
| Arabic LP | Spec complete | N/A |

### Day 60 (Phase 2 — Scale)
| Metric | Target |
|---|---|
| Monthly budget | $4,000 |
| Weekly installs | 350+ |
| KYC completions/week | ≥30 |
| Cost/Virtual Account | ≤$15 |
| Cost/Paid Active | ≤$80 |
| Arabic LP | Live |
| Google EG | Launched |
| Arabic creatives | 3+ variants live |

### Day 90 (Phase 3 — Accelerate)
| Metric | Target |
|---|---|
| Monthly budget | $6,000 |
| Weekly installs | 500+ |
| KYC completions/week | ≥50 |
| Cost/Virtual Account | ≤$12 |
| Cost/Paid Active | ≤$70 |
| Deposit conversion | ≥40% of KYC complete |
| Egypt % of total new actives | ≥25% |

### North Star
- Egypt becomes the **primary efficiency market**, delivering 3-5× more verified users per dollar than Turkey
- Long-term target: Egypt = 40% of new active users at <$15 Cost/VirtAcc

---

## 8) Risks & Mitigations

### 🔴 High Risk

**Regulatory uncertainty**
- Egypt's central bank (CBE) has historically been restrictive on crypto
- Risk: regulatory action could force market exit or restrict operations
- Mitigation: Monitor CBE announcements, maintain ability to pause campaigns within 24h, keep Egypt as a % of total (not sole market)

**KYC provider availability**
- BridgeXYZ may not fully support Egyptian ID documents or jurisdiction
- Risk: Even after handoff fix, KYC completion rate could be low due to document/OCR issues
- Mitigation: Test with real Egyptian IDs immediately after fix; have backup KYC provider identified; instrument failure reasons

### 🟠 Medium Risk

**Pre-KYC survey remains too aggressive**
- Even with handoff fixed, 63% rejection rate caps the funnel at ~37% of KYC starters
- Risk: Low throughput despite good acquisition efficiency
- Mitigation: A/B test threshold; measure fraud rates at different approval levels; consider removing survey for EG if fraud is low

**Currency / payment rail limitations**
- EGP is subject to capital controls; USD access is the value prop but also the regulatory risk
- Mitigation: Ensure deposit/withdraw methods work for Egyptian users; test full user journey

**Arabic creative quality**
- Machine-translated Arabic performs poorly; need native Egyptian Arabic
- Mitigation: Hire Arabic-native copywriter or use agency; test with small budgets first

### 🟡 Low Risk

**Audience saturation at scale**
- Egypt's crypto-interested audience may be smaller than Turkey's
- Mitigation: Monitor frequency and CPM trends; expand targeting gradually

**Seasonality**
- Ramadan, summer heat, political events can affect engagement
- Mitigation: Plan campaigns around local calendar; adjust budgets seasonally

---

## Decision Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-03-21 | Created scaling plan | Egypt shows 4-13× cheaper CAC than Turkey but has 0 KYC completions |
| 2026-03-21 | Set KYC fix as hard gate | $5.5K/mo flowing into dead funnel — must fix before scaling |
| 2026-03-21 | Phased budget ramp $2K→$4K→$6K | Conservative approach given regulatory + KYC risks |

---

## Appendix: Data Sources

- `analysis/egypt-funnel-activation-gap.md` — Full funnel analysis, KYC = 0 finding
- `analysis/pre-kyc-survey-investigation.md` — Survey rejection + handoff bug discovery
- `analysis/country-cac.md` — Cross-country CAC comparison
- `data/sheets-cac-analysis.md` — $8/VirtAcc for EG, channel performance
- `data/sheets-trafik-canavari.md` — Turkey baseline, Egypt LTV test references


---

> ⚠️ **Attribution caveat:** Web campaigns (Meta/Google → cenoa.com → app store) may appear as "Organic" or "(none)" due to broken web→app attribution. Estimated correction factor: ~6.9×. See [attribution-reconciliation.md](attribution-reconciliation.md) for details.
