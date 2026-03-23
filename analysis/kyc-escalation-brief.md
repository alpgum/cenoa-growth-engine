# KYC Escalation Brief — Product/Eng Action Required Monday

**Date:** 2026-03-22  
**Severity:** P0 — zero KYC completions in two markets  
**Author:** Performance Marketing (automated analysis)

---

## Problem

KYC completions are **zero** in Nigeria and Egypt despite users being approved through the pre-KYC survey. 89 approved users per week hit a dead end. Separately, iOS KYC submit rate is 3.8× worse than Android across all markets.

---

## Evidence (Mar 14–20, Amplitude event totals)

- **89 users approved** by pre-KYC survey in NG+EG → **0 Bridgexyz KYC Component Shown** → **0 submits**
- Pre-KYC AI survey rejects **67% of applicants** (NG: 158/226 rejected, EG: 36/57 rejected)
- iOS Shown→Submit: **2.4%** (39/1,618) vs Android: **9.2%** (140/1,521) — 3.8× gap
- `KYC Updated` fires in NG/EG (NG: 145, EG: 44) but no Bridgexyz events fire — something happens post-evaluation but the KYC component never loads

---

## Root Causes (ranked by severity)

**1. Bridgexyz handoff bug (NG/EG): approved → dead end**  
After `Pre-KYC Application Evaluated {status=approved}`, the app does not render the Bridgexyz KYC component. 89 approved users/week are silently dropped. No error screen, no retry, no telemetry. Possible causes: country→provider routing misconfiguration, Bridge SDK init failure swallowed silently, or feature flag not enabled for NG/EG.

**2. Pre-KYC AI survey: 67% rejection rate**  
The AI survey rejects ~2 out of 3 applicants before they ever reach KYC. NG approval rate: 30.1%. EG approval rate: 36.8%. Rejection reason codes and score distributions are not currently exposed — we cannot tell if the threshold is miscalibrated or if rejections are legitimate.

**3. iOS KYC submit collapse: 2.4% vs Android 9.2%**  
iOS users see the Bridgexyz component (1,618 Shown) but almost none submit (39). Likely causes: CTA below fold or covered by keyboard, disabled submit button with no visible reason, or WKWebView instability (session/cookie loss, upload failures). Instrumentation may also be partially broken on iOS (Shown > Started anomaly: 1,618 > 1,333).

---

## Impact

- **~89 users/week** approved but permanently blocked in NG/EG (handoff bug)
- **~194 users/week** rejected by AI survey in NG/EG (policy question)
- **~110 iOS submits/week lost** globally (if iOS matched Android's 9.2% rate, we'd see ~149 submits vs 39 today)
- **Acquisition spend on NG/EG is wasted** — every install we pay for in these markets converts to zero KYC completions
- NG/EG scaling plans (budget increases, new channels) are blocked until this is fixed

---

## Ask (specific actions)

**1. Debug & fix Bridgexyz handoff for NG/EG** *(1–2 day investigation)*  
Trace what happens after `Pre-KYC Application Evaluated {status=approved}` for a NG/EG user. Verify country→provider routing config. If Bridge init fails, surface an error screen + retry instead of silent failure. Success criteria: `Bridgexyz KYC Component Shown > 0` for NG/EG.

**2. Expose AI survey rejection data** *(1 day)*  
Add `reject_reason_code`, `score`, and `threshold` properties to the `Pre-KYC Application Evaluated` event. Export the score distribution for NG/EG so Product/Risk can evaluate whether the 67% rejection rate is appropriate or needs threshold adjustment.

**3. iOS KYC UX audit** *(2–3 days)*  
Run through the KYC flow on iPhone (iOS 17+). Check: is Submit CTA visible without scrolling? Does keyboard cover it? Is CTA disabled with no explanation? Does camera/photo permission flow break the UI state? Fix: sticky bottom CTA with keyboard-safe inset, scroll-to-first-invalid, inline error summary.

---

## Debug Checklist (Eng reproduction steps)

### Reproduce: NG/EG handoff failure
1. Fresh install, set device locale to Nigeria (or Egypt)
2. Complete sign-up → enter KYC flow → `KYC Started` should fire
3. Complete pre-KYC survey → get `Pre-KYC Application Evaluated {status=approved}`
4. **Expected:** Bridgexyz KYC component renders, `Bridgexyz KYC Component Shown` fires
5. **Actual (bug):** No component renders. No error screen. Silent dead end.
6. **Check:** Remote config / feature flags for NG/EG → is `kyc_provider=bridgexyz` enabled?
7. **Check:** Bridge SDK initialization logs — does it attempt to init? Does it fail silently?
8. **Check:** Network logs — any failed API calls between approval and component render?
9. **Note:** `KYC Updated` still fires (NG: 145, EG: 44) — determine what triggers this if not Bridgexyz

### Reproduce: iOS submit failure
1. iPhone (iOS 17+), fresh install, Turkey locale (where Bridge component is shown)
2. Complete sign-up → enter KYC → confirm `Bridgexyz KYC Component Shown` fires
3. Fill all required fields (document upload, selfie, etc.)
4. **Observe:** Is Submit button visible? Enabled? Covered by keyboard?
5. **Observe:** After camera/photo picker returns, is UI state preserved?
6. Tap Submit → does `Bridgexyz KYC Component: Submit clicked` fire?
7. **Compare:** Repeat same flow on Android — note any behavioral differences
8. Capture: screen recording, console logs, network trace for failed requests

---

*References: kyc-improvement-roadmap.md, pre-kyc-survey-investigation.md, kyc-dropout-deepdive.md, ios-android-ux-gap.md, onboarding-optimization.md*
