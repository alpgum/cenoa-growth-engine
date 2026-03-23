# Unified Data Dictionary (Single Source of Truth)

**Project:** Cenoa Performance Marketing

**Goal:** one canonical set of KPI definitions + source-of-truth priorities across **Amplitude**, **AppsFlyer**, **GA4**, **Google Sheets**, and **BigQuery**.

**Why this exists:** today, the same label (e.g., “Virtual account”, “Active”, “Organic”) can mean different things depending on the export/tab/dashboard. This document defines **what we mean** and **where to pull it from** so reporting stays consistent.

---

## 0) Ground rules (read this first)

### 0.1 Counts: event totals vs unique users
- **Event totals** (`m=totals` in Amplitude Segmentation) count *all fires* of an event.
- **Unique users** (`m=uniques` / Funnel uniques) count *distinct users* who performed the event.

**Reporting default:**
- Funnel conversion rates: **unique users**.
- Operational volume monitoring (alerts, week-over-week spikes): event totals are acceptable *only if* noted.

### 0.2 Cohorts: “new user funnel” vs “all users activity”
Some KPIs can be triggered by returning users (e.g., KYC start, deposits, withdrawals). Therefore:
- **New-user funnel** KPIs must be calculated on a cohort anchored to **Install** or **Signup**.
- **All-users activity** (Deposits/Withdrawals/DAU) should be reported separately and never presented as a conversion step from installs.

### 0.3 Attribution flavors (never mix)
- **Paid-attributed:** denominators filtered to paid-attributed users/events (AppsFlyer or persisted first-touch). Used for **channel optimization**.
- **Blended:** total paid spend / total outcomes (paid+organic). Used for **exec-level efficiency**.

---

## 1) KPI definitions (canonical)

Each KPI below includes:
- **Canonical definition** (what it *means*)
- **Implementation** (how it’s measured per system)
- **Source-of-truth priority** (what to use when numbers disagree)
- **Caveats** (how it can mislead)

> Naming note: event names shown below reflect the current instrumentation used in our Amplitude pulls (see `scripts/kpi_auto_update.py`).

---

### 1.1 Install
**Canonical definition:** A new app install attributed by AppsFlyer (first install of the app on a device; deduped per AppsFlyer rules).

**Implementations**
- **AppsFlyer:** `install` (standard AppsFlyer install).
- **BigQuery:** `marketing_appsflyer.*` tables (currently installs by day/campaign/platform).
- **Amplitude:** event type **`[AppsFlyer] Install`**.
- **GA4:** `first_open` (app) — *not canonical for paid attribution*, but useful as a sanity check.

**Source-of-truth priority (use case dependent)**
1) **BigQuery (AppsFlyer-derived)** for **campaign/platform breakdowns** and reproducible SQL.
2) **AppsFlyer exports/dashboard** when BQ coverage is missing.
3) **Amplitude `[AppsFlyer] Install`** for **product funnel context** (but treat as a downstream copy of AppsFlyer, not the canonical acquisition system).
4) **GA4 `first_open`** only as a cross-check.

**Caveats**
- Web→App flows can inflate **Organic** installs when the click context is lost (see §3.2).

---

### 1.2 Signup
**Canonical definition:** A user successfully creates an account (first-time signup completion). Counted as **unique users**.

**Implementations**
- **Amplitude:** event type **`Cenoa sign-up completed`**.
- **GA4:** `sign_up` (web/app) if instrumented equivalently — validate.
- **Sheets:** `sign_up` is a *legacy denominator* used in historical CAC tabs (not guaranteed to match Amplitude).

**Source-of-truth priority**
1) **Amplitude (`Cenoa sign-up completed`, uniques)** for funnel + cohort reporting.
2) **Backend auth DB** (if/when available) for absolute truth of account creation.
3) **GA4** for web-only signup intent flows (not canonical for app signup).
4) **Sheets** only for historical series where no better backfill exists.

**Caveats**
- If signup is server-side and attribution properties aren’t joined, signups can appear as **(none)** source even when the install is paid.

---

### 1.3 KYC Started
**Canonical definition:** The user initiates the KYC process.

**Implementations**
- **Amplitude:** event type **`KYC Started`**.

**Source-of-truth priority**
1) **Amplitude (`KYC Started`, uniques for funnel)**.
2) **Backend KYC initiation logs** (future preferred for reliability).

**Caveats**
- `KYC Started` is frequently **not cohort-pure** (returning users can start/restart KYC). Do not compare directly to installs/signups without cohorting.

---

### 1.4 KYC Shown
**Canonical definition:** The KYC provider UI component is rendered for the user (provider-UI step).

**Implementations**
- **Amplitude:** event type **`Bridgexyz KYC Component Shown`**.

**Source-of-truth priority**
1) **Amplitude (`Bridgexyz KYC Component Shown`)**.
2) Provider-specific logs (future), if available.

**Caveats**
- If multiple providers exist by country (or gating happens before the widget), this KPI can be **0** even when KYC Started is non-zero (observed in NG/EG).

---

### 1.5 KYC Submit
**Canonical definition:** The user clicks submit on the KYC provider component.

**Implementations**
- **Amplitude:** event type **`Bridgexyz KYC Component: Submit clicked`**.

**Source-of-truth priority**
1) **Amplitude (Submit clicked, uniques)** for funnel.
2) **Backend “KYC application submitted”** (future preferred) to avoid UI-click ambiguity.

**Caveats**
- **Submit clicked ≠ approved**. Treat as “submission attempt”, not “passed KYC”.

---

### 1.6 Deposit
**Canonical definition:** A successful deposit transaction (money in).

**Implementations**
- **Amplitude:** event type **`Deposit Completed`**.
- **Ledger/transaction system:** preferred future canonical (not currently in this repo).

**Source-of-truth priority**
1) **Ledger / core transactions DB** (future canonical).
2) **Amplitude (`Deposit Completed`)** for directional monitoring.

**Caveats**
- Deposits in a week are **not** a conversion step from that week’s installs; they include returning users.

---

### 1.7 Withdrawal
**Canonical definition:** A successful withdrawal transaction (money out).

**Implementations**
- **Amplitude:** event type **`Withdraw Completed`**.
- **Ledger/transaction system:** preferred future canonical.

**Source-of-truth priority**
1) **Ledger / core transactions DB** (future canonical).
2) **Amplitude (`Withdraw Completed`)** for directional monitoring + top-line.

**Caveats**
- Strong returning-user contamination; do not use as “install→withdraw conversion” unless calculated as a cohort.

---

### 1.8 Virtual account opened
**Canonical definition:** The user successfully opens/creates a virtual account (product milestone).

**Implementations**
- **Amplitude:** event type **`Virtual account opened`**.
- **Sheets:** `virt_acc` (multiple competing definitions across tabs; see §3.3).

**Source-of-truth priority**
1) **Amplitude (`Virtual account opened`, uniques)** for product funnel.
2) **Core banking / virtual account provider logs** (future canonical).
3) **Sheets** only for legacy historical series until backfilled.

**Caveats**
- Current sheets exports show **multiple non-matching “virtual account” counts**, indicating definition drift.

---

### 1.9 New active
**Canonical definition (marketing):** A newly acquired user who reaches “activated” status for the **first time**.

**Canonical measurement (recommended going forward):**
- **New active = unique users whose first successful withdrawal occurs within 30 days of signup**
- Optional stricter gate: user also has **Virtual account opened** before the first withdrawal.

**Current legacy measurements (not consistent)**
- **Sheets `new_active`** (Sum tab) and **Sheets `paid_active`** (Channels tab) are **not interchangeable** and currently disagree materially.

**Source-of-truth priority**
1) **BigQuery fact model (future):** user-level table joining signup → virtual account → first withdrawal.
2) **Amplitude (future):** computed cohort metric using uniques + user_id.
3) **Sheets** only as a legacy KPI for historical CAC until rebuilt.

**Caveats**
- Do not compare “New active” across sources without stating which definition is used.

---

## 2) Source-of-truth matrix (quick lookup)

### 2.1 Recommended defaults by reporting need

**A) Weekly exec pulse (blended, stable definitions)**
- Installs: **BigQuery AppsFlyer-derived** (or AppsFlyer if BQ not updated)
- Signups: **Amplitude**
- KYC Started / Shown / Submit: **Amplitude**
- Virtual account opened: **Amplitude**
- Deposits / Withdrawals: **Amplitude** (label clearly as “all-user transactions in period”)
- New active: **do not report** until rebuilt (or report Sheets legacy with a “legacy definition” tag)

**B) Channel optimization (paid-attributed)**
- Spend: **Sheets Budget Tracking (realized)** or platform exports (but must map to channel taxonomy)
- Installs: **AppsFlyer / BigQuery** by `media_source` + `campaign`
- Down-funnel outcomes (signup/kyc/virt/active): only report by channel if attribution coverage is high (see Do/Don’t)

**C) Product funnel diagnostics (conversion rates)**
- Use **Amplitude Funnel (uniques)** whenever possible.
- Avoid segmentation `m=totals` ratios for conversion.

---

## 3) Known mismatches (what breaks today)

### 3.1 Country / platform / device “(none)”
**Symptom:** Amplitude segmentations show `(none)` for `country` or `platform` user property.

**Impact:**
- Country/platform splits become misleading.
- “(none)” often indicates missing identity stitching or missing user property propagation.

**Rule:** Always show `(none)` explicitly in diagnostic tables; do not silently drop it in KPI rollups.

### 3.2 Organic inflated due to Web→App handoff
**Symptom:** users acquired via web2app show up as **Organic/(none)** in app attribution because click context is lost at LP→store→install.

**Impact:**
- Paid channels look worse than reality.
- Organic looks artificially strong.

**Fix requirements:** OneLink + deferred deep linking + server-side persistence of `web_session_id` and click IDs (see §4.3).

### 3.3 Spend definition mismatch (Sheets)
**Symptom:** “Spend” differs between CAC Analysis vs Budget Tracking (notably Feb 2026 ≈ +37% gap).

**Impact:** CAC can move purely due to numerator definition.

**Rule:** For any CAC metric, label numerator explicitly:
- `spend_attributed` (CAC Analysis style) vs
- `spend_realized` (Budget Tracking / finance style)

---

## 4) Required properties & joins (minimum viable model)

### 4.1 AppsFlyer dimensions (must exist everywhere)
For any **channel/campaign** reporting, we must have at least:
- `media_source`
- `campaign`

**Where they appear today**
- **Amplitude (user properties):**
  - `gp:[AppsFlyer] media source`
  - `gp:[AppsFlyer] campaign`
- **BigQuery tables:**
  - `media_source`, `campaign`, `platform`, `installs`

### 4.2 Country / platform / device
Required standard dimensions:
- `country` (ISO2 preferred; e.g., TR/EG/NG)
- `platform` (ios/android/web)
- `device_type` (optional but recommended)

**Rule:** If country/platform are missing, treat as **data quality issue**, not a “real” segment.

### 4.3 Web→App join keys (to repair attribution)
Minimum fields to persist and join:
- `web_session_id` (first-party generated UUID)
- click IDs where present: `gclid`, `gbraid`, `wbraid`, `fbclid`, `ttclid`

**Join chain (recommended)**
1) Web LP view creates `web_session_id` and stores UTMs + click IDs.
2) “Get the app” uses AppsFlyer OneLink and passes `af_sub1 = web_session_id`.
3) App reads AppsFlyer conversion payload on first open and sends `web_session_id + appsflyer_id + device identifiers` to backend.
4) Backend attaches first-touch fields to the user on signup and propagates them to Amplitude user + event properties.

---

## 5) Do / Don’t rules (reporting hygiene)

### Do
- **Do** state whether metrics are **uniques** or **totals**.
- **Do** separate **new-user funnel** metrics from **all-user activity** (transactions/DAU).
- **Do** show the **(none)** bucket in attribution and country/platform splits.
- **Do** use **BigQuery/AppsFlyer** for campaign-level installs and Amplitude for product-funnel steps.
- **Do** label CAC numerator explicitly (`realized` vs `attributed`).

### Don’t
- **Don’t** compute conversion rates using `m=totals` ratios between events (can exceed 100% and mislead).
- **Don’t** present deposits/withdrawals as conversion steps from the same-week install cohort unless cohorting is explicitly done.
- **Don’t** break down downstream KPIs by channel/campaign unless attribution coverage is acceptable.
  - Practical guardrail: if **>(30–40%)** of signups/withdrawals are `(none)`, channel ROI tables are *directional only*.
- **Don’t** mix Sheets “virt_acc/new_active/paid_active” definitions with Amplitude events without an explicit mapping.

---

## Appendix A) Current canonical Amplitude event names (as used in automation)

From `projects/cenoa-performance-marketing/scripts/kpi_auto_update.py`:
- `[AppsFlyer] Install`
- `Cenoa sign-up completed`
- `KYC Started`
- `Bridgexyz KYC Component Shown`
- `Bridgexyz KYC Component: Submit clicked`
- `Virtual account opened`
- `Deposit Completed`
- `Withdraw Completed`
- `Transfer Completed`

---

## Appendix B) Current BigQuery tables (AppsFlyer-derived)

From `data/bigquery-inventory.md`:
- `marketing_appsflyer.daily_installs_campaign_tr` (date × platform × media_source × campaign → installs)
- `marketing_appsflyer.weekly_combined_totals` (week × platform × country × channel → installs/clicks/events/users)
