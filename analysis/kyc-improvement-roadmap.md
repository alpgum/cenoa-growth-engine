# [095] KYC improvement roadmap (conversion + observability)

**Created:** 2026-03-21  
**Window referenced (baseline):** 2026-03-14 → 2026-03-20 (Amplitude, mostly `m=totals`)  
**Primary references:**
- [051] `analysis/pre-kyc-survey-investigation.md` (NG/EG survey reject + approved→KYC handoff bug)
- [060] `analysis/egypt-scaling-plan.md` (EG scaling gated on KYC fix)
- [061] `analysis/nigeria-growth-plan.md` (NG scaling gated on KYC fix)
- [084] `analysis/ios-android-ux-gap.md` (iOS submit collapse)
- [086] `analysis/onboarding-optimization.md` (cross-cutting funnel + instrumentation spec)
- [085] `analysis/web-to-app-handoff.md` (attribution + deep-link persistence; missing platform/country)

---

## 0) Executive summary (what’s broken)

KYC is currently the dominant activation bottleneck **and it’s failing in 3 distinct ways**:

1) **NG/EG are hard-blocked before Bridge KYC UI**
   - Pre‑KYC AI survey rejects **~67%** of applicants (NG 70%, EG 63%).
   - Worse: even **approved** users never see Bridge KYC (**`Bridgexyz KYC Component Shown = 0`**).

2) **iOS sees the Bridge component but doesn’t reach submit**
   - iOS: `Shown → Submit` proxy **2.4%** (39/1,618)
   - Android: **9.2%** (140/1,521)
   - Likely mixture of UX friction + iOS-specific technical/instrumentation issues.

3) **Turkey (the only working market) has a major “Shown → Submit” leak**
   - TR: `Shown → Submit` proxy **5.6%** (170/3,025)
   - Even in the “best” market, most users abandon inside the KYC component.

**Cross-cutting:** measurement gaps (`Shown > Started`, `Updated >> Submit`, missing platform/country on key events) block confident diagnosis and A/B iteration.

---

## 1) Problem tree (root causes → symptoms → impact)

### Top symptom: **Low KYC submissions / completions outside TR**

#### A) NG/EG gating failure (survey + handoff)
- **A1 — Pre‑KYC AI survey rejects too many users**
  - Symptom: ~67% rejection (NG 158/226; EG 36/57).
  - Impact: caps max KYC throughput even if UI is perfect.
- **A2 — Approved users never reach Bridge KYC UI (handoff bug)**
  - Symptom: approved=89 (NG+EG) but `Bridgexyz KYC Component Shown = 0`.
  - Impact: **effective KYC completion = 0** despite high intent.

#### B) iOS friction / tech gap inside Bridge flow
- **B1 — CTA accessibility / disabled-state confusion** (below fold, keyboard overlap, missing scroll affordance)
- **B2 — iOS WKWebView / session / upload instability** (permissions, cookies, redirects)
- **B3 — Instrumentation mismatch** (submit occurs but `Submit clicked` not recorded; or multiple submit paths)

#### C) TR “Shown → Submit” leak (baseline UX + error recovery)
- **C1 — Validation/upload errors not surfaced clearly**
- **C2 — Long/unclear step sequence** (missing progress cues)
- **C3 — Low resilience** (no retry/resume; users bounce on transient errors)

#### D) Observability + identity attribution gaps (amplifies all issues)
- Missing/incorrect props: `platform=(none)`, `country=(none)` on key events.
- Step ordering anomalies: `Shown > Started`.
- Downstream ambiguity: `KYC Updated` is not a clean post-submit success signal.

---

## 2) Baseline metrics snapshot (directional)

> **Caveat:** most numbers are event totals; use uniques-based funnel once instrumentation is fixed.

### 2.1 Global KYC micro-funnel (Bridge events)
- `KYC Started`: 3,098
- `Bridgexyz KYC Component Shown`: 3,139
- `Bridgexyz Submit clicked`: 179
- Proxy `Shown → Submit`: **5.7%**

### 2.2 By country (focus)
- **Turkey:** `Shown 3,025 → Submit 170` (**5.6%**)
- **Nigeria:** `KYC Started 230`, `Bridge Shown 0`, `Submit 0`
- **Egypt:** `KYC Started 62`, `Bridge Shown 0`, `Submit 0`

### 2.3 By platform
- **Android:** `Shown 1,521 → Submit 140` (**9.2%**)
- **iOS:** `Shown 1,618 → Submit 39` (**2.4%**)

---

## 3) Prioritized roadmap (P0/P1/P2) + owners

### P0 (0–2 weeks): unblock submissions + make funnels measurable

**P0.1 Fix NG/EG approved→KYC handoff (hard bug)**
- **Owner:** Eng (Mobile + Backend) + Product for acceptance criteria
- **Deliverable:** After `Pre-KYC Application Evaluated {status=approved}` user deterministically reaches the KYC UI.
- **DoD:**
  - NG/EG `Bridgexyz KYC Component Shown` > 0 (same-day) and scales with approvals.
  - Add explicit failure path: if provider init fails, show an error screen + retry (no silent drop).

**P0.2 Add provider routing visibility (stop guessing which flow users see)**
- **Owner:** Eng + Data
- **Deliverable:** `KYC Provider Selected` event (provider + reason + country + feature flag).
- **DoD:** coverage ≥98% of `KYC Started` across platforms/countries.

**P0.3 iOS submit gap: “CTA reachable + reason visible + parity tracking” hotfix**
- **Owner:** Eng (iOS) + Product
- **Deliverable:**
  - sticky bottom CTA (keyboard-safe safe-area)
  - scroll-to-first-invalid + inline error summary near CTA
  - ensure submit tap triggers the same event + backend call path as Android
- **DoD:** iOS `KYC Submit Attempted` rate materially increases; iOS error codes become visible.

**P0.4 Minimum viable KYC instrumentation (Attempted/Succeeded/Failed + exit reasons)**
- **Owner:** Data + Eng
- **Deliverable:** replace “submit clicked only” with outcome events + error taxonomy (see §4).
- **DoD:** for ≥95% of KYC sessions, we can classify the outcome: success, failure (with error_code), or exit (with exit_reason).

---

### P1 (2–6 weeks): increase throughput (policy + UX) and stabilize non‑TR scale

**P1.1 Pre‑KYC AI survey: rejection reason distribution + threshold tuning test**
- **Owner:** Product (Risk) + Data + Eng
- **Deliverable:** exportable distribution of `reject_reason_code`, `score`, `threshold` and controlled experiment for NG/EG.
- **DoD:**
  - Approval rate moves from ~33% → **45–60%** (market-dependent)
  - Fraud/chargeback signals monitored with a kill-switch rule.

**P1.2 TR KYC UX improvements (benefits everyone; TR is biggest volume)**
- **Owner:** Product + Eng (Mobile)
- **Deliverable:** progress indicator + step checklist + better upload retry/resume + clearer doc requirements.
- **DoD:** TR `Shown → Submit Attempted` improves by +20–50% relative.

**P1.3 Web→app handoff hardening (identity + attribution props on signup/KYC)**
- **Owner:** Eng (Web + Mobile + Backend) + Data
- **Why it’s in KYC roadmap:** missing `platform/country/acquisition` props break segmentation and can mis-route provider gating.
- **Deliverable:** OneLink + deferred deep link + `web_session_id` persistence; propagate to Amplitude user props.
- **DoD:** `Sign-up Completed` has non-null `platform` on **>95%** of events; country/platform parity across KYC events.

---

### P2 (6–12 weeks): “KYC reliability platform” + scaling-ready ops

**P2.1 Provider-agnostic KYC orchestration layer + step tracking**
- **Owner:** Eng (Backend platform) + Data
- **Deliverable:** canonical KYC state machine (country → provider → steps → outcomes) + consistent telemetry.
- **DoD:** same step events and error codes regardless of KYC provider.

**P2.2 Alternative provider / fallback path for non-TR markets**
- **Owner:** Product (Risk) + Eng
- **Deliverable:** evaluate and integrate backup provider for NG/EG if Bridge constraints persist.
- **DoD:** ability to switch providers via remote config; measurable performance by provider.

**P2.3 Automated KYC health monitoring + alerts**
- **Owner:** Data + Eng
- **Deliverable:** daily checks for `Shown`, `Submit Attempted`, `Submit Succeeded`, error spikes by country/platform/app_version.
- **DoD:** alerts on:
  - `Component Shown = 0` in any market with >X KYC starts
  - `Submit Attempted` drops >Y% WoW
  - error_code spikes >Z× baseline

---

## 4) Instrumentation requirements (exact events, properties, error codes)

### 4.1 Required events (canonical)

> Naming can be adapted, but **semantics must match** and be consistent across iOS/Android/Web.

1) **Entry + routing**
- `KYC Started`
  - props: `kyc_entrypoint` (onboarding/settings/deeplink), `country`, `platform`, `app_version`, `build_number`, `kyc_session_id`
- `KYC Provider Selected`
  - props: `kyc_provider` (bridgexyz/other/manual), `selection_reason` (country/feature_flag/risk_score/fallback), `feature_flag_key`, `country`, `platform`, `kyc_session_id`

2) **Pre‑KYC survey (NG/EG)**
- `Pre-KYC Survey Opened`
  - props: `survey_version`, `country`, `platform`, `kyc_session_id`
- `Pre-KYC Survey Submitted`
  - props: `survey_version`, `time_to_complete_ms`, `questions_count`, `country`, `platform`, `kyc_session_id`
- `Pre-KYC Application Evaluated`
  - props:
    - `status` (approved/rejected)
    - `score` (number)
    - `threshold` (number)
    - `reject_reason_code` (string enum)
    - `model_version`
    - `country`, `platform`, `kyc_session_id`

3) **KYC UI + step tracking (provider-agnostic)**
- `KYC Step Shown`
- `KYC Step Completed`
  - props: `step_name` (doc_select, doc_upload_front, doc_upload_back, selfie, address, review), `time_in_step_ms`, `kyc_provider`, `country`, `platform`, `kyc_session_id`

4) **Submit outcomes (replace “Submit clicked” with outcomes)**
- `KYC Submit Attempted`
  - props: `kyc_provider`, `network_type`, `country`, `platform`, `app_version`, `kyc_session_id`
- `KYC Submit Succeeded`
  - props: `kyc_provider`, `provider_submission_id` (if allowed), `country`, `platform`, `kyc_session_id`
- `KYC Submit Failed`
  - props: `error_domain`, `error_code`, `http_status`, `retryable`, `step_name`, `kyc_provider`, `country`, `platform`, `app_version`, `kyc_session_id`

5) **Exit / abandonment**
- `KYC Exited`
  - props: `exit_reason` (back_pressed/close_tapped/app_backgrounded/crash/timeout/error_screen), `current_step_name`, `kyc_provider`, `country`, `platform`, `kyc_session_id`

### 4.2 Properties that must be present on *all* KYC events
- `kyc_session_id` (UUID per KYC run)
- `user_id` (post-signup) + stable device identifier (pre-signup)
- `platform`, `os_version`, `device_model`
- `country` + `ip_country` (if allowed)
- `app_version`, `build_number`
- `locale`, `language`
- `kyc_provider`, `kyc_flow_version`

### 4.3 Error taxonomy (minimum viable)

**error_domain (enum):**
- `prekyc` | `provider_init` | `webview` | `validation` | `upload` | `network` | `provider_api` | `unknown`

**error_code (examples; must be stable strings):**
- `PREKYC_REJECTED_THRESHOLD`
- `PREKYC_REJECTED_RULE_<X>`
- `KYC_PROVIDER_CONFIG_MISSING`
- `KYC_PROVIDER_INIT_FAILED`
- `BRIDGE_WEBVIEW_LOAD_FAILED`
- `SUBMIT_DISABLED_MISSING_REQUIRED_FIELDS`
- `UPLOAD_FAILED_TIMEOUT`
- `UPLOAD_FAILED_PERMISSION_DENIED`
- `PROVIDER_API_4XX_<STATUS>` / `PROVIDER_API_5XX_<STATUS>`
- `NETWORK_OFFLINE`

**Rule:** every `KYC Submit Failed` must include `error_domain` + `error_code`, and ideally `retryable`.

---

## 5) Debug checklists (by issue)

### 5.1 NG/EG: `Bridgexyz KYC Component Shown = 0` after approval

**Goal:** identify whether this is (a) routing/config, (b) provider init failure, or (c) missing instrumentation.

1) **Confirm routing + flags**
- Validate country → provider mapping in remote config / backend routing.
- Ensure `KYC Provider Selected` fires with `kyc_provider=bridgexyz` for NG/EG after approval.

2) **Trace the exact post-approval state transition**
- For an approved test user, verify sequence:
  - `Pre-KYC Application Evaluated {status=approved}`
  - `KYC Provider Selected`
  - `KYC Step Shown {step_name=...}` OR `Bridgexyz KYC Component Shown`
- If sequence breaks: log the last successful step.

3) **Check provider initialization / config**
- Confirm Bridge credentials/config present for NG/EG environments.
- Verify supported document types for NG/EG; if unsupported, show explicit “not supported” UI + emit `KYC Submit Failed` (domain=`provider_init`, code=`KYC_COUNTRY_UNSUPPORTED`).

4) **Instrument the dead zone (must not be silent)**
- Add a forced event on UI render attempt:
  - `KYC Provider Init Started` / `KYC Provider Init Failed` (optional but high value)
- If init fails, show an error screen with retry and emit failure code.

5) **QA repro**
- Fresh install, NG/EG locale, go through survey → approved.
- Capture device logs, network logs, and the exact screen state.


### 5.2 iOS: `Shown → Submit` collapse (2.4% vs Android 9.2%)

1) **Establish whether it’s real or tracking**
- Add/verify `KYC Submit Attempted` (not just click).
- Compare iOS vs Android:
  - `Attempted` parity
  - `Succeeded` / `Failed` split
- If iOS has attempts but no events: tracking bug.

2) **UI/CTA reachability checks (highest likelihood)**
- Is CTA below fold? Is there a scroll affordance?
- Does keyboard cover the CTA?
- Is CTA disabled? If yes, is the reason shown inline?
- Does permission flow (camera/photos) return to a broken state?

3) **Webview/session stability**
- Test on multiple iPhones + iOS versions (at least one older OS).
- Observe:
  - cookie/session loss
  - redirect loops
  - upload failures
  - blank screens
- If failures occur, map them to `error_domain=webview/upload/provider_api`.

4) **Concrete acceptance tests**
- In QA run, confirm this ordered sequence fires exactly once:
  - `KYC Started` → `KYC Provider Selected` → `KYC Step Shown`… → `KYC Submit Attempted` → (Succeeded/Failed)


### 5.3 TR: “Shown → Submit” leak (5.6%)

1) **Break down by step + error codes**
- Segment by `step_name`, `error_code`, `app_version`, `platform`.
- Identify top 3 failure modes (e.g., upload timeout, validation missing, provider error).

2) **Fix highest-frequency failure + add resilience**
- Retry/resume uploads
- Better validation messaging
- Progress indicator and checklist

---

## 6) Expected KPI lift ranges (directional)

> Convert these into uniques-based metrics once `kyc_session_id` + Attempted/Succeeded/Failed are live.

### Baseline (proxy, Mar 14–20)
- Global `Shown → Submit clicked`: **~5.7%**
- iOS `Shown → Submit clicked`: **~2.4%**
- NG/EG: **0 submits** due to gating + handoff bug

### P0 impact (2 weeks): unblock + iOS hotfix + outcomes instrumentation

**iOS improvement (largest immediate lever)**
- Target iOS `Shown → Submit Attempted` from **2.4% → 5–8%**.
- With iOS shown ≈ 1,618 events/week, directional submits become **81–129** vs 39 ⇒ **+42 to +90** incremental submit attempts.

**NG/EG handoff fix (enables future throughput; immediate lift small but non-zero)**
- Approved users/week ≈ **89** can now reach KYC UI.
- If `Shown → Attempted` reaches **5–12%** quickly, that’s **+4 to +11** attempts/week initially.

**Net effect (2-week realistic range):**
- Global submit attempts: **+25% to +60%** (mostly iOS-driven)

### P1 impact (6 weeks): survey tuning + TR UX + better resilience

- Raise NG/EG approval from ~33% → **45–60%** ⇒ approvals rise from 89 → **~122–175** / week (given similar KYC start volume).
- If post-approval `Shown → Attempted` reaches **8–15%** after UX/resilience work ⇒ **+10 to +26** attempts/week.
- TR improvements: aim **+20–50%** improvement in TR `Shown → Attempted`.

### Translating to “active users” (rough)
Assumptions to validate:
- `Submit Succeeded → KYC Approved` ~50–80% (provider dependent)
- `KYC Approved → New Active` ~20–40% within 7 days

Directional: **every +100 successful submits/week** could yield **+10 to +30 new actives/week**.

---

## 7) Milestones (2-week / 6-week / 12-week)

### By week 2 (P0 done)
- NG/EG: Bridge component shown > 0; no more silent dead-ends after approval.
- iOS: sticky CTA + keyboard-safe layout shipped.
- KYC telemetry: Attempted/Succeeded/Failed + error codes + exit reasons live.
- Dashboard: uniques-based funnel draft (or at least `kyc_session_id`-based proxy).

### By week 6 (P1 done)
- Pre‑KYC: top rejection reasons known; threshold test complete; approval improved toward 45–60%.
- TR: progress UI + upload retry/resume shipped; measurable uplift in step completion.
- Web→app: platform on signup fixed to >95%; KYC segmentation reliable by platform/country.

### By week 12 (P2 done)
- Provider-agnostic KYC orchestration layer live with consistent step telemetry.
- Provider fallback available for NG/EG via remote config.
- Automated KYC health monitoring + alerts running (detects `Shown=0`, attempt drops, error spikes).

---

## Appendix: how this roadmap unblocks country scaling

- EG/NG scaling plans are explicitly gated on KYC being functional:
  - EG: `analysis/egypt-scaling-plan.md` (hold budgets until submit > 0 for 2 weeks)
  - NG: `analysis/nigeria-growth-plan.md` (organic demand waiting; fix KYC first)

This roadmap converts those plans from “blocked strategy” into an executable engineering + data plan with measurable gates.
