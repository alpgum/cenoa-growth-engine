# Email: KYC Bug in Nigeria & Egypt

**To:** Engineering Team  
**From:** Performance Marketing  
**Date:** 2026-03-23  

---

**Subject: [P0] KYC Completions = 0 in Nigeria & Egypt — Debug Request**

Hi team,

We've identified a critical handoff bug: **zero users** in Nigeria and Egypt can complete KYC. After passing the Pre-KYC AI survey, approved users hit a silent dead end — the Bridgexyz KYC component never renders, no error is shown, and no retry is offered. This means every acquisition dollar we spend in NG/EG currently converts to zero verified users.

**Data (Mar 14–20):**

- 292 users started KYC (NG: 230, EG: 62) → 89 approved by Pre-KYC survey → **0 Bridgexyz KYC Component Shown**
- Pre-KYC survey rejects 67% of applicants (NG: 158/226, EG: 36/57) — rejection criteria not yet auditable
- `KYC Updated` still fires (NG: 145, EG: 44), so *something* triggers post-evaluation, but Bridgexyz never loads
- iOS submit rate is 2.4% vs Android 9.2% globally (separate issue, flagging for awareness)

**Most likely root causes (ranked):**

1. Country→provider routing misconfiguration — Bridgexyz may not be enabled for NG/EG
2. Bridge SDK init failure swallowed silently — no error surface, no telemetry
3. Feature flag not set for these markets

**Our ask (timeline: this week):**

1. **Trace the handoff** — follow a NG/EG user from `Pre-KYC Application Evaluated {status=approved}` → verify whether Bridgexyz component render is attempted. Check remote config, feature flags, and Bridge SDK init logs.
2. **Reproduce** — fresh install, NG locale, complete pre-KYC survey with approval → confirm Bridgexyz component does not render.
3. **Surface errors** — if Bridge init fails, add an error screen + retry instead of silent failure.
4. **Success criteria:** `Bridgexyz KYC Component Shown > 0` for NG/EG.

**Impact:**

- **~89 approved users/week** permanently blocked from completing KYC
- **All NG/EG acquisition spend is wasted** until this is fixed — scaling plans for these markets are on hold
- Estimated **~88 verified users/week recoverable** once handoff + threshold adjustments are in place

Happy to jump on a call or share Amplitude dashboards. Let us know if you need anything from our side.

Thanks!
