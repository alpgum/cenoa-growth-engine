# [084] iOS vs Android UX gap — where iOS underperforms + what to test

**Period referenced:** 2026-03-14 → 2026-03-20  
**Primary sources (existing analyses):**
- `analysis/platform-funnel.md`
- `analysis/kyc-dropout-deepdive.md`
- `analysis/audience-insights.md`
- `analysis/global-funnel.md`

> Important caveat: several of the platform/KYC numbers are **event totals (m=totals)**, not unique users. Ratios are therefore **proxy “conversion” ratios** and can exceed 100% (e.g., `Shown > Started`) if events fire multiple times per user or if steps happen outside the date range.

---

## 1) Where iOS underperforms vs Android in the funnel

### 1.1 Acquisition / top-of-funnel (volume vs efficiency)
From `platform-funnel.md`:

| Step | Android | iOS | iOS vs Android |
|---|---:|---:|---:|
| **[AppsFlyer] Install** | 1,275 | 170 | **0.13×** (iOS far lower volume) |
| **Application first opened** | 1,473 | 485 | 0.33× |
| **Cenoa sign-up completed** | 221 | 232 | **1.05×** (parity) |

**Interpretation:** iOS is not failing at sign-up completion once users are in-app. The iOS problem is **not** install→signup efficiency; it’s mainly **volume** (iOS campaigns / budget mix) plus a downstream KYC failure.

### 1.2 KYC funnel (the real iOS gap)
From `kyc-dropout-deepdive.md` (Bridge XYZ events):

| KYC step (Bridge) | Android | iOS | iOS vs Android |
|---|---:|---:|---:|
| **KYC Started** | 1,717 | 1,333 | 0.78× |
| **Bridgexyz KYC Component Shown** | 1,521 | 1,618 | **1.06×** (iOS is shown *more*) |
| **Bridgexyz Submit clicked** | 140 | 39 | **0.28×** (iOS collapses) |
| **Shown → Submit (proxy)** | **9.2%** | **2.4%** | iOS is **~3.8× worse** |

**Key location of underperformance:** **`Bridgexyz KYC Component Shown → Submit clicked`**.

Notably, iOS has **higher “Shown”** but dramatically lower “Submit clicked”, which points to either:
- a **real UX/technical blocker** on iOS between seeing the component and being able to submit, and/or
- an **instrumentation mismatch** where submit clicks aren’t recorded reliably on iOS.

### 1.3 Downstream monetization is NOT the issue (iOS users are high value)
From `platform-funnel.md` + `audience-insights.md`:
- iOS has **more deposits** and **more withdrawals** than Android in the same window (event totals):
  - Deposits: iOS 813 vs Android 718 (**+13%**)
  - Withdrawals: iOS 1,187 vs Android 1,033 (**+15%**)
- Unique withdrawers skew slightly iOS: **53.7% iOS vs 46.0% Android**.

**Implication:** fixing iOS KYC is high-leverage: iOS users who get through tend to transact.

---

## 2) Hypotheses (ranked) for the iOS KYC submit collapse

Ranked by **(a) fit to observed data**, **(b) likelihood**, **(c) fixability**.

### H1 — iOS Bridgexyz UI friction blocks submission (highest likelihood)
**Why it fits:** iOS sees the component (`Shown`) but doesn’t reach `Submit clicked`.

Common iOS-specific blockers to check:
- Submit button **below the fold** with no clear scroll affordance
- **Keyboard overlay** covering the CTA
- “I confirm…” checkbox / terms gate not visible
- Validation states not obvious; CTA stays disabled with no explanation
- Camera / document picker interruptions return to a bad UI state

**Expected signature:** many sessions with repeated `Component Shown` (reloads) and no submit.

### H2 — iOS instrumentation gap for `Submit clicked` (very plausible)
**Why it fits:** iOS `Shown > Started` (121% ratio) strongly hints at tracking inconsistencies on iOS. It’s possible submit happens but the event doesn’t fire.

Examples:
- Click handler not wired on iOS webview
- Event name mismatch / casing mismatch
- Event blocked by ATT consent / analytics SDK state
- Multiple “submit” paths (final submit vs intermediate continue) but only one tracked

**Expected signature:** higher `KYC Updated` / backend status changes on iOS without corresponding submit clicks.

### H3 — iOS webview/deeplink/session handoff issues inside Bridge flow
**Why it fits:** Bridge flows often embed web content; iOS webviews are more restrictive (cookies, cross-site storage, redirects).

Check:
- SSO/session cookie loss in WKWebView
- File upload/camera capture permission differences
- Redirect loops
- Network calls blocked by ATS / TLS settings

**Expected signature:** higher error screens or re-renders on iOS; increased time-in-step.

### H4 — Country/locale mix differences causing iOS “Shown” to be mostly TR, but submit constrained by doc-type edge cases
**Why it fits partially:** Turkey dominates KYC submits overall; if iOS cohort has different doc types or language settings, submission could be worse.

Counterpoint: the iOS vs Android gap is visible *overall*, so this is likely secondary.

### H5 — Performance / low-memory issues on specific iPhone models / iOS versions
**Why it fits sometimes:** heavy KYC components (camera, upload) can crash or freeze.

Counterpoint: iOS device mix in `audience-insights.md` is iPhone-heavy (often decent hardware), so less likely than pure UI/instrumentation.

### H6 — Provider gating / feature flags applied differently on iOS
**Why it fits:** plausible if Bridge SDK versions or feature flags diverge by platform.

**Check:** remote config / feature flag parity and Bridge SDK versions.

---

## 3) Instrumentation checks needed (before we chase UX ghosts)

Goal: confirm whether iOS users truly cannot submit, or if submission happens but tracking is broken.

### 3.1 Re-run with uniques + proper funnel
- Re-run KYC funnel using **Amplitude Funnel API** or Segmentation with **`m=uniques`** for:
  - `KYC Started` → `Bridgexyz KYC Component Shown` → `Bridgexyz Submit clicked` → (true success event)
- Segment by **platform** and **country (TR at minimum)**.

### 3.2 Validate event definitions and parity
For iOS vs Android, verify:
- event names and properties are identical (including casing)
- both platforms fire `Submit clicked` **on the same user action** (final submit, not an intermediate button)
- ensure `platform`, `country`, `app_version`, `os_version`, `device_model`, `kyc_provider`, `kyc_flow_version` are attached

### 3.3 Fix “Shown > Started” inconsistency
Seen in `kyc-dropout-deepdive.md`:
- overall `Shown` (3,139) > `Started` (3,098)
- iOS `Shown` (1,618) > iOS `Started` (1,333)

Actions:
- ensure `KYC Started` fires exactly once per session entry into KYC, and before “Shown”
- ensure “Shown” fires once per render, ideally with a dedupe key (session_id / view_id)

### 3.4 Add diagnostic events around the dead zone
Add (or confirm) these are fired **on both platforms**:
- `Bridgexyz KYC Component: Validation error shown` (with error_code)
- `Bridgexyz KYC Component: Submit attempted` vs `Submit success` vs `Submit failed`
- `KYC Exit` with `exit_reason` (back press, close, crash, timeout)
- `KYC Step Changed` (doc upload, selfie, address, review)

---

## 4) QA checklist for Product/Eng (reproduce systematically)

### 4.1 Test matrix
Run on at least:
- iOS: iPhone 11 + iPhone 14/15 (latest iOS), plus one older iOS version if supported
- Android: one mid-range (Redmi/Samsung A-series) + one high-end
- Networks: Wi‑Fi + cellular

### 4.2 Preconditions
- Use **fresh install** + new account
- Force user country to **Turkey** (since Bridge “Shown” exists and submissions occur there)
- Also test **NG/EG** to confirm the separate issue where `KYC Started` happens but Bridge component is never shown (gating / provider routing)

### 4.3 Repro steps (focus on iOS)
1. Install → open app → complete sign-up
2. Enter KYC start
3. Confirm the Bridge component renders (matches `Component Shown`)
4. Complete all required inputs:
   - document selection
   - camera capture / upload
   - selfie / liveness (if any)
   - terms/consent
5. Attempt to submit

### 4.4 What to observe / record
- Is the **Submit CTA visible without scrolling**?
- Does the **keyboard cover** the CTA?
- Does CTA remain disabled? If yes, is there a clear reason (inline error)?
- Any **spinner loops**, redirects, or silent failures?
- Any permission prompts (camera/photos) causing state loss?
- Does the UI allow returning after permission grant without resetting the form?
- Capture:
  - screen recording
  - console / device logs
  - network failures (upload/submit endpoints)

### 4.5 Instrumentation validation during QA
During the same QA run, verify these fire in order (and once):
- `KYC Started`
- `Bridgexyz KYC Component Shown`
- `Bridgexyz KYC Component: Submit clicked`
- `KYC Updated` (only if it truly represents post-submit progression)

---

## 5) Experiments / fixes (3) + expected impact

### Experiment 1 — iOS KYC CTA accessibility fix (sticky submit + keyboard-safe layout)
**Change:** Ensure Submit/Continue CTA is always reachable:
- sticky bottom CTA
- keyboard-safe inset
- auto-scroll to first invalid field
- explicit checklist of remaining requirements

**Primary metric:** iOS `Shown → Submit clicked` (uniques)

**Expected impact (directional, using current event totals as proxy):**
- iOS is at **2.4%** (39/1,618). If improved to Android’s **9.2%**, expected iOS submits ≈ **149** (1,618×9.2%).
- Incremental iOS submits ≈ **+110** (149–39).
- Total submits would rise from 179 → **~289** (**+61%**).

### Experiment 2 — Instrumentation parity + “submit success” event
**Change:** Make submission tracking reliable and actionable:
- fire `Submit clicked` on actual native tap handler
- add `Submit success` / `Submit failed` with error codes
- switch reporting to uniques-based funnel

**Primary metric:** iOS/Android parity of `Submit clicked` and `Submit success`; reduction of anomalies (`Shown > Started`)

**Expected impact:**
- If the gap is partially measurement, this will **prevent false UX conclusions** and identify the real blocker (validation vs upload vs redirect).
- Should materially reduce time-to-fix and improve confidence in experiments.

### Experiment 3 — Bridge flow hardening on iOS (webview/session + upload reliability)
**Change options (choose based on QA findings):**
- upgrade Bridgexyz SDK / web component version on iOS
- switch to **SFSafariViewController** (or system browser) for the KYC flow if WKWebView is unstable
- implement resumable uploads / better error recovery

**Primary metric:** iOS `Shown → Submit success` and error rate by `error_code`

**Expected impact:**
- If failures are technical (upload/redirect), expect a **step-change improvement** similar to Experiment 1.
- Secondary benefit: fewer repeated `Shown` events (fewer reloads).

---

## Quick take
- **The iOS issue is concentrated in one step:** `Bridgexyz KYC Component Shown → Submit clicked` (2.4% iOS vs 9.2% Android).
- Because iOS transactors are slightly higher-value, fixing iOS KYC should unlock meaningful incremental revenue.
- Before heavy UX iteration: **confirm instrumentation parity** and add success/failure diagnostics so we can see whether the drop is UI, tech, or tracking.
