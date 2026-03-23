# [020] KYC dropout deep-dive (Amplitude)

**Date range:** 2026-03-14 → 2026-03-20 (Amplitude params: `start=20260314`, `end=20260320`)

**Raw pulls (saved):** `projects/cenoa-performance-marketing/data/kyc-deepdive-20260320.json`

**Events analyzed (as requested):**
1. `KYC Started`
2. `Bridgexyz KYC Component Shown`
3. `Bridgexyz KYC Component: Submit clicked`
4. `KYC Updated`

**Segmentation pulls included for each event:**
- totals (`m=totals`)
- grouped by `country` (user property)
- grouped by `platform` (user property)

> ⚠️ Important caveat: all counts are **event totals** (`m=totals`), not unique users. “Conversion rates” below are therefore **proxy ratios** between event totals, and can exceed 100% if events are fired with different frequency, re-fired, or if the numerator includes users whose prior-step happened outside the date range.

---

## 1) Executive summary

- **NG / EG:** we see meaningful **`KYC Started` volume** (NG=230, EG=62) but **0 `Bridgexyz KYC Component Shown`** and therefore **0 `Submit clicked`**. This strongly suggests **either provider/path gating before the Bridgexyz component is rendered** (eligibility / unsupported country / feature flag), or **a different KYC flow** is used and only `KYC Started` + `KYC Updated` are instrumented.

- **TR (Turkey):** the dominant leak is **`Shown → Submit`**. TR has very high `Shown` (3,025) but only **170 submits** ⇒ **5.6% Shown→Submit**.

- **Platform parity:** **Android converts much better than iOS** at the `Shown → Submit` step.
  - Android: **9.2%** (140 / 1,521)
  - iOS: **2.4%** (39 / 1,618)

- **Instrumentation mismatch flags:**
  - Overall `Shown` is **higher than** `Started` (3,139 vs 3,098 → 101.3%).
  - iOS `Shown` is **higher than** iOS `Started` (1,618 vs 1,333 → 121.4%).
  - `KYC Updated` is far higher than `Submit clicked` (1,480 vs 179 → 826.8%). This means `KYC Updated` is **not a clean downstream step** of `Submit clicked` within this window (likely backend status updates for submissions that happened earlier, or `Submit clicked` under-instrumented).

---

## 2) Totals (all countries, all platforms)

| Metric | Count |
|---|---:|
| KYC Started | 3,098 |
| Bridgexyz KYC Component Shown | 3,139 |
| Bridgexyz KYC Component: Submit clicked | 179 |
| KYC Updated | 1,480 |

**Proxy conversion ratios (event totals):**
- Started → Shown: **101.3%**
- Shown → Submit: **5.7%**
- Started → Submit: **5.8%**
- Submit → Updated: **826.8%** *(not interpretable as a conversion; see caveat above)*

---

## 3) Country breakdown (focus on TR / NG / EG)

### 3.1 Focus countries (counts + proxy conversion ratios)

| country | started | shown | submit | updated | Started→Shown | Shown→Submit | Started→Submit | Submit→Updated |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Turkey | 2,594 | 3,025 | 170 | 1,155 | 116.6% | 5.6% | 6.6% | 679.4% |
| Nigeria | 230 | 0 | 0 | 145 | 0.0% | — | 0.0% | — |
| Egypt | 62 | 0 | 0 | 44 | 0.0% | — | 0.0% | — |
| Ghana | 22 | 0 | 0 | 19 | 0.0% | — | 0.0% | — |
| Indonesia | 19 | 3 | 0 | 5 | 15.8% | 0.0% | 0.0% | — |
| Pakistan | 17 | 0 | 0 | 5 | 0.0% | — | 0.0% | — |

> Note: Amplitude shows **`(none)`** for missing country user property. In this window, `(none)` had **48 starts** and **58 updates** but **0 shown / 0 submit**, which looks like a separate instrumentation/identity issue (country missing on those users).

### 3.2 What this implies for NG / EG (Key question #1)

**Observation:**
- NG: `Started=230`, `Shown=0`, `Submit=0`, `Updated=145`
- EG: `Started=62`, `Shown=0`, `Submit=0`, `Updated=44`

**Most likely explanations (ranked):**
1. **Provider/path gating before Bridgexyz UI:** users can initiate KYC (fires `KYC Started`) but are blocked before the Bridgexyz component renders (so `Component Shown` never fires). Common causes: unsupported country, unsupported document type, feature flag off, eligibility checks, service outage.
2. **Different KYC provider / different UI flow for NG & EG:** if NG/EG are routed to a non-Bridgexyz KYC, we would expect Bridgexyz-specific events to be absent, exactly as observed.
3. **Instrumentation gap:** `Bridgexyz KYC Component Shown` and/or `Submit clicked` may not be fired on the NG/EG code path (e.g., error screen, webview variant, or SDK callback not wired).

**Why `KYC Updated` still appears in NG/EG:**
- Because `KYC Updated` is likely a **backend-driven status update event** that can occur for users who submitted earlier (outside the window), or via a separate provider. With `m=totals`, it’s not safe to interpret it as downstream of `Submit clicked` in the same timeframe.

**Concrete follow-ups:**
- Confirm **KYC provider routing** by country (is Bridgexyz enabled for NG/EG in prod?)
- If Bridgexyz is intended for NG/EG: inspect **client logs / error telemetry** between “start KYC” and “component shown” for NG/EG.
- If another provider is used: ensure equivalent events exist (e.g., `OtherProvider KYC Component Shown`, `OtherProvider Submit clicked`) or add a provider-agnostic step event.

---

## 4) Turkey leak location (Key question #2)

Turkey dominates volume:
- Started: **2,594**
- Shown: **3,025**
- Submit clicked: **170**

**Leak diagnosis:**
- The bottleneck is **`Shown → Submit` = 5.6%**.
- `Started → Shown` is >100% (116.6%), which is an **instrumentation consistency** problem rather than a user funnel improvement lever.

**Hypotheses for low `Shown → Submit` in TR:**
- Real UX friction: document capture / selfie, validation errors, unclear CTA, long form.
- Technical issues: upload failures, submit button disabled due to validations, Bridgexyz SDK issues.
- Event instrumentation: submit click might not be tracked reliably (especially on iOS; see next section).

---

## 5) Platform parity (Key question #3)

| platform | started | shown | submit | updated | Started→Shown | Shown→Submit | Started→Submit |
|---|---:|---:|---:|---:|---:|---:|---:|
| Android | 1,717 | 1,521 | 140 | 726 | 88.6% | **9.2%** | **8.2%** |
| iOS | 1,333 | 1,618 | 39 | 696 | 121.4% | **2.4%** | **2.9%** |
| (none) | 48 | 0 | 0 | 58 | 0.0% | — | 0.0% |

**Takeaway:** iOS `Shown → Submit` is ~**3.8x worse** than Android (2.4% vs 9.2%).

**What to check next (high ROI):**
- Validate the **submit CTA** on iOS (enabled state, keyboard covering button, scroll-to-bottom requirement, webview interactions).
- Validate whether `Bridgexyz KYC Component: Submit clicked` is actually fired on iOS (instrumentation parity), since iOS has *more* `Shown` but far fewer submits.

---

## 6) Instrumentation notes / recommended next query

Because `Shown > Started` and `Updated >> Submit`, a user-level funnel would be more actionable.

**Recommended next step (if we want “real” conversion):**
- Re-run using Amplitude’s **Funnel API** (or Segmentation with `m=uniques`) for the same events, segmented by `country` and `platform`.
- Specifically: measure **unique users** progressing from `KYC Started` → `Component Shown` → `Submit clicked` → (status approved), and ensure the “approval” step is an event that is *causally downstream* of submit within the same window.

---

## Appendix: files produced

- Raw JSON: `data/kyc-deepdive-20260320.json`
- Pull script: `scripts/amplitude_kyc_deepdive.py`
