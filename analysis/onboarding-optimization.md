# [086] Onboarding flow optimization brief (Install → Sign-up → KYC)

**Date:** 2026-03-21  
**Inputs (existing analyses):**
- `analysis/global-funnel.md`
- `analysis/kyc-dropout-deepdive.md`
- `analysis/ios-android-ux-gap.md`
- `analysis/audience-insights.md`
- `analysis/web-to-app-handoff.md`
- (supporting) `analysis/pre-kyc-survey-investigation.md`

> **Data caveat:** several KYC step counts come from Amplitude **event totals** (not unique users), so step ratios are *proxy* conversion rates. Use this brief to prioritize fixes; validate with a uniques-based funnel once instrumentation is repaired.

---

## 1) Current onboarding funnel map (install → signup → KYC started → shown → submit)

### 1.1 Top-level funnel (global, Mar 14–20)
From `global-funnel.md`:

| Stage | Volume | Notes |
|---|---:|---|
| Install | **1,445** | AppsFlyer installs (new users) |
| Sign-up | **1,207** | Strong install→signup (**83.5%**) |
| KYC Started | **3,098** | **Not cohort-pure** (includes existing users re-triggering KYC) |
| Bridgexyz KYC Component Shown | **3,139** | From `kyc-dropout-deepdive.md` |
| Bridgexyz Submit clicked | **179** | Proxy “KYC submit” step |

**Directional proxy ratios (event totals):**
- Install → Sign-up: **83.5%**
- KYC Started → Submit: **5.8%**
- Shown → Submit: **~5.7%**

### 1.2 KYC micro-funnel by country (what actually happens)
From `kyc-dropout-deepdive.md` + `pre-kyc-survey-investigation.md`:

**Turkey (TR):**
- Bridgexyz component is shown at high volume, but users don’t reach submit.
- TR Shown→Submit proxy: **5.6%** (170/3,025)

**Nigeria (NG) + Egypt (EG): two-step failure**

```
KYC Started
  → Pre-KYC AI Survey Evaluated
       → Rejected (~67%)  → dead end
       → Approved (~33%)  → BUG: Bridgexyz shown = 0 → submit = 0
```

NG/EG funnel facts (Mar 14–20):
- KYC Started: **NG 230**, **EG 62**
- Pre-KYC Approved: **NG 68**, **EG 21** (total **89**) 
- Bridgexyz shown: **0** (handoff broken)

### 1.3 KYC micro-funnel by platform (iOS vs Android)
From `kyc-dropout-deepdive.md` + `ios-android-ux-gap.md`:

| Step | Android | iOS | Takeaway |
|---|---:|---:|---|
| KYC Started | 1,717 | 1,333 | similar order |
| Bridgexyz shown | 1,521 | 1,618 | iOS is shown *more* |
| Submit clicked | 140 | 39 | iOS collapses |
| **Shown → Submit (proxy)** | **9.2%** | **2.4%** | iOS is **~3.8× worse** |

---

## 2) Biggest friction points (root causes to fix first)

### A) Pre‑KYC AI survey is blocking volume (NG/EG)
From `pre-kyc-survey-investigation.md`:
- **~67% rejection rate** in NG/EG (NG 70%, EG 63%)
- Users are hard-stopped after rejection (no alternative path)

**Why it matters:** even if KYC UI was perfect, most NG/EG users never reach it.

### B) Handoff bug: approved Pre‑KYC users never see Bridgexyz KYC (NG/EG)
- **89 approved users/week** (NG+EG) never render the Bridgexyz component (0 shown, 0 submit).

**This is a bug, not an optimization.** Fixing it is the fastest “submit” unlock in NG/EG.

### C) iOS KYC submit gap (shown → submit)
From `ios-android-ux-gap.md`:
- iOS **2.4%** shown→submit vs Android **9.2%**.

Likely causes (ranked):
1) iOS UI/CTA accessibility (below fold, keyboard overlay, disabled CTA with no reason)
2) iOS instrumentation mismatch for “Submit clicked”
3) WKWebView / Bridge flow instability (session/cookies, upload failures)

### D) Data quality gaps block diagnosis (cross-cutting)
From `audience-insights.md` + `web-to-app-handoff.md`:
- **62.5% of sign-ups have platform = (none)** → identity + attribution + platform properties are missing on a core onboarding event.
- “Shown > Started” indicates step ordering / dedupe issues.

**Impact:** we risk chasing UX changes while measurement is broken.

---

## 3) 10 concrete UX fixes (ship-ready, specific)

> Organize these into: **Bug fixes**, **UX clarity**, **Error recovery**, **Localization**, **Eligibility transparency**.

1) **Fix NG/EG approved→Bridgexyz routing (hard bug)**
   - After `Pre-KYC Application Evaluated = approved`, route deterministically to KYC provider screen.
   - If provider initialization fails, show a visible error state + retry (not a silent dead end).

2) **Make KYC progress explicit (multi-step progress bar + checklist)**
   - Show “Step 1/4: Identity”, “2/4: Document”, “3/4: Selfie”, “4/4: Review & submit”.
   - Add a checklist of missing requirements; tapping an item scrolls to the field.

3) **Sticky bottom CTA + keyboard-safe layout (especially iOS)**
   - Ensure Submit/Continue CTA is always reachable.
   - Handle safe-area + keyboard insets; avoid CTA being covered.

4) **Disable-state clarity: if CTA is disabled, show why**
   - Inline message near CTA: “To continue, upload front + back of ID” / “Accept terms to submit”.
   - Auto-focus the first invalid field.

5) **Inline doc requirements by country + example images**
   - TR: “Accepted: Kimlik, Passport, Driver’s License” etc.
   - NG/EG: show accepted docs; if unsupported, communicate before user starts KYC.

6) **Pre-KYC survey: reduce ambiguity + set expectations**
   - Add microcopy: “This takes ~60 seconds. We use it to check eligibility.”
   - Add a visible “Why we ask” link; avoid “AI” language if it scares users.

7) **Pre-KYC rejection UX: provide next steps (don’t dead-end)**
   - Show *reason category* (e.g., “document type not supported”, “country not supported”, “information mismatch”).
   - Offer: retry later, contact support, or alternative verification path (manual review).

8) **Improve upload robustness + recovery**
   - Add upload progress, retry button, and clear error messaging (network vs validation).
   - Persist partially completed state so users can resume.

9) **Localization & locale handling**
   - Ensure KYC strings match user locale (TR Turkish; NG/EG English/Arabic as applicable).
   - Localize date formats, document labels, and example images.

10) **Exit handling: confirm intent + save state**
   - On back/close: modal “Leave verification? Your progress is saved.”
   - Provide “Save & exit” vs “Continue”.

---

## 4) Instrumentation spec (events + properties to add)

### 4.1 Principles
- Instrument **provider-agnostic** steps (so NG/EG aren’t invisible if provider differs).
- Add **error codes** and **exit reasons** around the dead zones.
- Make funnels measurable via **uniques** with dedupe keys.

### 4.2 New/updated events (recommended)

**Onboarding + identity basics**
- `Onboarding Started`
- `Sign-up Started`
- `Sign-up Completed`
  - Ensure `platform`, `country`, `app_version`, `os_version`, `device_model` are always present.

**KYC entry + routing**
- `KYC Started` *(ensure 1x per session entry; include `kyc_entrypoint`)*
- `KYC Provider Selected`
  - props: `kyc_provider` (bridgexyz/other/manual), `selection_reason` (country, feature_flag, risk_score, fallback)

**Pre-KYC survey**
- `Pre-KYC Survey Opened`
- `Pre-KYC Survey Submitted`
  - props: `survey_version`, `questions_count`, `time_to_complete_ms`
- `Pre-KYC Application Evaluated`
  - props: `status` (approved/rejected), `score` (numeric), `threshold`, `reject_reason_code` (enum), `model_version`

**KYC UI steps (provider-agnostic)**
- `KYC Step Shown`
  - props: `step_name` (doc_select, doc_upload_front, doc_upload_back, selfie, address, review)
- `KYC Step Completed`
  - props: `step_name`, `time_in_step_ms`

**Submit + results (critical)**
- `KYC Submit Attempted`
  - props: `kyc_provider`, `flow_version`, `client_state_hash` (optional), `network_type`
- `KYC Submit Succeeded`
- `KYC Submit Failed`
  - props: `error_code`, `error_domain` (validation/upload/network/provider/sdk), `http_status`, `retryable` (bool)

**Exit / abandonment diagnostics**
- `KYC Exited`
  - props: `exit_reason` (back_pressed, close_tapped, app_backgrounded, crash, timeout, error_screen)
  - props: `current_step_name`, `has_unsent_uploads` (bool)

### 4.3 Properties to standardize on all onboarding/KYC events
- `platform`, `os_version`, `device_model`
- `country` (and `ip_country` if allowed)
- `app_version`, `build_number`
- `locale`, `language`
- `kyc_provider`, `kyc_flow_version`
- `kyc_session_id` (new; UUID per KYC run)

### 4.4 Instrumentation quality KPI (definition of done)
- `Sign-up Completed` has non-null `platform` for **>95%** of events.
- `KYC Started` → `KYC Provider Selected` coverage **>98%**.
- `KYC Submit` events split into `Attempted/Succeeded/Failed` (no more ambiguous single “submit clicked”).
- iOS/Android parity: same event names + properties + firing points.

---

## 5) 2-week execution plan (what to do first)

### Week 1 — unblock submissions + make it measurable
**Day 1–2 (Eng + QA):**
1) **Fix NG/EG handoff bug**: after `Pre-KYC approved`, guarantee Bridgexyz (or intended provider) renders.
2) Add a visible error screen + retry if provider init fails (no silent failure).

**Day 2–4 (Product + Eng):**
3) **iOS submit accessibility hotfix**: sticky CTA + keyboard-safe layout + scroll-to-first-error.
4) Add explicit disabled-state reasons for CTA.

**Day 3–5 (Analytics + Eng):**
5) Ship instrumentation changes (minimum viable):
   - `KYC Provider Selected`
   - `KYC Submit Attempted/Succeeded/Failed` with `error_code`
   - `KYC Exited` with `exit_reason`
   - ensure `platform/country/app_version` present on `Sign-up Completed`

**Day 5 (Analytics):**
6) Build a uniques-based funnel view (Amplitude Funnel) segmented by `platform` and `country`.

### Week 2 — lift conversion (UX + policy tuning)
**Day 6–8 (Product):**
7) Update KYC copy + progress UI (progress bar/checklist) and doc requirement screens.

**Day 8–10 (Risk/Product/Eng):**
8) **Pre-KYC threshold review**: pull score distribution + top reject_reason_code; adjust threshold for NG/EG (controlled rollout).

**Day 10–12 (Eng):**
9) Upload reliability improvements (retry/resume; better error categorization).

**Day 12–14 (QA + Analytics):**
10) Run regression matrix (iOS/Android, TR/NG/EG, Wi‑Fi/cellular) + verify event parity and funnel movement.

---

## 6) Expected impact ranges (submit uplift targets)

Baseline (Mar 14–20):
- **KYC submit proxy:** 179 total submit clicks
- **Global shown→submit proxy:** ~5.7%
- **iOS shown→submit proxy:** 2.4% (39/1,618)
- **Android shown→submit proxy:** 9.2% (140/1,521)
- **NG/EG submits:** 0 (blocked)

### Impact scenario 1 — iOS CTA + error clarity (fast win)
- Target: raise iOS shown→submit from **2.4% → 5–8%** (still below Android parity).
- Expected incremental submits (directional, using shown totals):
  - iOS shown 1,618 × (5–8%) = **81–129** submits vs 39 now → **+42 to +90** submits.

### Impact scenario 2 — Fix NG/EG approved→KYC handoff (bug fix)
- Immediate unlock: up to **89 approved/week** can now reach KYC UI.
- If those users reach even **5–10% submit** (conservative vs TR), that’s **+4 to +9** submits/week.
- If Pre-KYC threshold is later relaxed (see scenario 3), this grows materially.

### Impact scenario 3 — Pre-KYC threshold tuning (policy lever)
- Move approval rate from ~33% to **45–55%** (controlled test).
- For NG/EG combined 292 KYC starts/week → 131–161 approvals.
- If post-approval shown→submit reaches **8–15%** after UX + stability work → **+10 to +24** submits/week.

### Combined target (2 weeks)
A realistic 2-week goal (with instrumentation fixed):
- **Total KYC submit uplift:** **+25% to +60%** vs baseline, primarily driven by iOS improvements.
- Stretch goal (if iOS reaches Android parity and NG/EG handoff fully fixed): **+60% to +100%**.

---

## Appendix: key references
- Global funnel volumes + KYC bottleneck: `analysis/global-funnel.md`
- KYC step dropoffs by country/platform: `analysis/kyc-dropout-deepdive.md`
- iOS-specific collapse hypotheses + experiments: `analysis/ios-android-ux-gap.md`
- Market/platform/device mix + data quality flags: `analysis/audience-insights.md`
- Web→app attribution/payload persistence blueprint: `analysis/web-to-app-handoff.md`
- Pre-KYC survey rejection + NG/EG handoff bug: `analysis/pre-kyc-survey-investigation.md`
