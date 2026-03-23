# Pre-KYC AI Survey Investigation — NG & EG

**Date:** 2026-03-21  
**Period:** Mar 14–20, 2026  
**Status:** 🔴 TWO blockers identified

---

## Executive Summary

Nigeria and Egypt have a **Pre-KYC AI Survey** that users must pass before seeing the Bridgexyz KYC component. Investigation reveals **two compounding problems**:

1. **~67% rejection rate** — The AI survey rejects most applicants (NG: 70%, EG: 63%)
2. **100% handoff failure** — Even the 89 users who were APPROVED never saw Bridgexyz KYC (0 shown)

Combined effect: **Zero KYC completions** in NG/EG despite 292 users starting KYC.

---

## Event Flow Map

```
KYC Started (NG: 230, EG: 62)
    │
    ▼
Pre-KYC Application Evaluated (NG: 226, EG: 57)
    │
    ├── ❌ REJECTED (NG: 158, EG: 36)  ← 67% of evaluations
    │       └── Dead end. User cannot proceed.
    │
    └── ✅ APPROVED (NG: 68, EG: 21)   ← 33% of evaluations
            │
            ▼
        Bridgexyz KYC Component Shown = 0  ← 🔴 HANDOFF BROKEN
            │
            ▼
        Bridgexyz KYC Submit = 0
```

---

## Funnel Data (Mar 14–20)

| Event | Nigeria | Egypt | Total |
|-------|---------|-------|-------|
| KYC Started | 230 | 62 | 292 |
| Pre-KYC Evaluated | 226 | 57 | 283 |
| Pre-KYC **Approved** | 68 | 21 | 89 |
| Pre-KYC **Rejected** | 158 | 36 | 194 |
| Bridgexyz KYC Shown | **0** | **0** | **0** |
| KYC Updated | 145 | 44 | 189 |

### Approval Rates
- **Nigeria:** 30.1% (68/226)
- **Egypt:** 36.8% (21/57)
- **Global:** 32.8% (118/360)

---

## Problem 1: High Rejection Rate (67%)

The Pre-KYC AI survey rejects ~2 out of 3 applicants. This is the **primary volume killer**.

- NG lost **158 users** at this stage in one week
- EG lost **36 users** at this stage in one week
- Total: **194 rejected** out of 283 evaluated

**Impact:** Even if the handoff were working, only 30-37% of KYC starters would reach Bridgexyz.

**Questions for Engineering:**
- What criteria does the AI survey evaluate?
- What are the top rejection reasons?
- Is the threshold calibrated for NG/EG populations?
- Are legitimate users being falsely rejected?

---

## Problem 2: Bridgexyz Handoff Broken (0 shown)

89 users were **approved** by the Pre-KYC survey but **none** saw the Bridgexyz KYC component. This is a technical failure.

**Evidence:**
- "Pre-KYC Application Evaluated" with status=approved: 89 events
- "Bridgexyz KYC Component Shown" for NG+EG: 0 events
- "KYC Updated" still fires (NG: 145, EG: 44), suggesting *something* happens post-evaluation but the Bridgexyz component never loads

**Possible causes:**
1. Frontend routing bug — approved status not triggering Bridgexyz component render
2. API integration failure — Bridgexyz initialization failing silently
3. Event firing issue — Component shows but event doesn't fire (less likely given Submit is also 0)
4. Country-level config — Bridgexyz not enabled/configured for NG/EG

---

## Native Survey Events (Context)

High-volume survey events exist but appear to be **separate from KYC**:

| Event | Nigeria | Egypt |
|-------|---------|-------|
| Native Survey Step Seen | 4,797 | 1,517 |
| Native Survey Opened | 903 | 338 |
| Native Survey Submitted | 338 | 95 |
| Native Survey Canceled | 383 | 164 |

These volumes are much larger than KYC starts (4,797 vs 230 for NG), suggesting they fire across the app, not just during KYC. The completion rate is also low (~37% in NG, ~28% in EG), with many cancellations.

---

## Recommendations

### 🔴 Critical (This Week)

1. **Fix the Bridgexyz handoff** — 89 approved users got stuck. This is a bug, not a design issue. Engineering needs to trace what happens after `Pre-KYC Application Evaluated` with status=approved.

2. **Check if "KYC Updated" (189 events) represents the approved users completing some flow** — if so, what flow? If not Bridgexyz, what?

### 🟠 High Priority

3. **Audit AI survey rejection criteria** — 67% rejection is extremely high. Get the rejection reasons/scores distribution. Determine if the threshold is too aggressive for NG/EG markets.

4. **Add observability** — Instrument events between "Pre-KYC Approved" and "Bridgexyz Shown" to pinpoint exactly where the handoff breaks.

### 🟡 Medium Priority

5. **Re-evaluate Pre-KYC necessity** — Is the AI survey adding enough fraud prevention value to justify blocking 67% of potential KYC completions? What's the false-positive rate?

6. **A/B test survey thresholds** — Try a more permissive threshold for NG/EG and measure downstream fraud rates.

---

## Revenue Impact Estimate

- **Lost KYC completions/week:** At minimum 89 (approved but stuck), potentially up to 292 (all KYC starters)
- **If handoff fix + threshold adjustment → 50% approval rate:**
  - ~146 users/week reaching Bridgexyz KYC
  - Assuming 60% KYC completion → ~88 verified users/week
  - vs. current: 0

---

## Data Sources

- Amplitude Event Segmentation API (Mar 14–20, 2026)
- Key event: `Pre-KYC Application Evaluated` with property `status` (approved/rejected)
- Raw data: `data/pre-kyc-survey-20260320.json`
