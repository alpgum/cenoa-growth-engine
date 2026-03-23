# [026] Historical CAC cross-check (Sheets vs Amplitude-derived)

**Generated:** 2026-03-21  
**Scope:** Turkey (TR) monthly series **Sep 2025 → Feb 2026** + limited sanity checks from Budget Tracking (Jan/Feb 2026) + limited Amplitude weekly snapshot (Mar 2026).

This note answers:
1) what metrics we use and where they come from (by month)
2) where the numbers disagree (between Sheets tabs and between Sheets vs Amplitude)
3) why they might disagree
4) what the canonical CAC method should be going forward

Machine-readable output: `projects/cenoa-performance-marketing/data/cac-crosscheck.json`

---

## 1) Metrics and sources (what we use)

### A) Spend (USD)
We currently have **two different “spend” concepts**:

- **CAC Analysis (Sheet: “Sum”, TR monthly):**
  - Field: `sum_turkey.months_[year].{cost}`
  - Interpretation: *attributed / marketing-model-aligned spend* (numerator consistent with that sheet’s denominators).

- **Budget Tracking (Sheet: “Realized Cost - Jan/Feb 2026”):**
  - Field: `realizedCostJan2026.summary.TR.total` and `realizedCostFeb2026.summary.TR.total`
  - Interpretation: *finance/ops realized spend* (often includes costs that may not be attributed in AppsFlyer-style funnels).

**Availability:** Budget Tracking export only contains realized totals for **Jan–Feb 2026**, not Sep–Dec 2025.

### B) Sign-ups
- **CAC Analysis (Sheet: “Sum”, TR monthly):** `sign_up`
- **CAC Analysis (Sheet: “2025 Channels TR”, Jan 2026 total):** `channels_2025_turkey.jan_2026.total.sign_up`
- **Amplitude weekly snapshot:** `amplitude-weekly-2026-03-20.json → signups.value` (weekly, global; not monthly / not TR-only)

### C) Virtual accounts
We have **3 competing “virtual account” counts** in the exports:

- **CAC Analysis (Sum, TR monthly):** `virt_acc`
- **CAC Analysis (2025 Channels TR, Jan 2026 total):** `jan_2026.total.virt_acc`
- **Budget Tracking (Realized Cost Jan 2026, TR totals):** `channelBreakdown.TR.total.virtAcc`

These are **not numerically consistent**, indicating differing definitions and/or attribution filters.

### D) New active
- **CAC Analysis (Sum, TR monthly):** `new_active`
- **CAC Analysis (2025 Channels TR):** uses `paid_active` (not `new_active`) in Jan 2026 and some weekly blocks
- **Amplitude:** does not provide “new active” in the weekly snapshot export; closest available are `dau`, `kyc_submits`, `deposits/withdrawals`.

---

## 2) Cross-check table (Sep 2025 → Feb 2026)

Source of truth for the *complete* monthly time series (spend + denominators) is:
- **`sheets-cac-analysis.json → sum_turkey`**

Budget Tracking provides an alternate spend numerator for:
- **Jan 2026 + Feb 2026 only**

### 2.1 Spend: Budget Tracking (realized) vs CAC Analysis (Sum)

| Month | CAC Analysis spend (TR) | Budget Tracking spend (TR) | Δ (Budget−CAC) | Ratio (Budget/CAC) |
|---|---:|---:|---:|---:|
| 2026-01 | 27,088 | 26,235 | -853 | 0.97 |
| 2026-02 | 25,811 | 35,435 | +9,624 | 1.37 |

**Key mismatch:** **Feb 2026** has a **large gap** (+$9.6k, +37%) between finance realized spend and CAC Analysis attributed spend.

### 2.2 Internal inconsistency inside CAC Analysis (Jan 2026)

Jan 2026 appears in multiple CAC Analysis tabs and they **do not agree**:

| Metric (TR) | CAC Analysis “Sum” | CAC Analysis “2025 Channels TR” (Jan 2026 total) | Δ (Channels−Sum) |
|---|---:|---:|---:|
| Spend | 27,088 | 26,435 | -653 |
| Sign-ups | 2,751 | 2,402 | -349 |
| Virtual accounts | 900 | 531 | -369 |
| New active vs Paid active | 226 (new_active) | 78 (paid_active) | -148 |

**Interpretation:** these tabs are likely applying different filters/definitions (paid-only vs mixed, different event definitions, different attribution windows, or partial ingestion).

### 2.3 Virtual account definition mismatch (Jan 2026)

| Source | Virt. account count (TR, Jan 2026) |
|---|---:|
| Budget Tracking (Realized Cost Jan) | 1,895 |
| CAC Analysis (Sum) | 900 |
| CAC Analysis (2025 Channels TR) | 531 |

A 3.6× spread strongly suggests these are **not the same event** (or not the same attribution filter).

---

## 3) Why the numbers likely disagree (hypotheses)

### Spend mismatches (esp. Feb 2026)
Most plausible causes:

1) **Channel inclusion mismatch**
   - Budget Tracking likely includes *all* paid costs (awareness + conversion + retargeting + networks + tests).
   - CAC Analysis may include only costs that can be mapped/attributed in the AppsFlyer model, or only conversion campaigns.

2) **Non-attributed costs included in finance sheet**
   - Influencers, fixed fees, agency, production, brand spend may sit in Budget Tracking but not in AppsFlyer-attributed CAC Analysis.

3) **Date cutoffs / time zones**
   - Month boundary differences (UTC vs local), late invoices, or spend recognized differently.

4) **FX / rounding / payment timing**
   - Less likely for a +37% gap, but can contribute.

### Denominator mismatches (signups / virt acc / active)
Most plausible causes:

1) **Different denominator definitions across tabs**
   - `virt_acc` could mean “virtual account created”, “KYC start”, “KYC submitted”, or “new account” depending on tab owner.

2) **Paid-only vs total (paid+organic)**
   - Channels tab may be paid-only (or only certain mapped media sources), while Sum may include broader totals.

3) **Attribution window / reattribution / deduping**
   - AppsFlyer-style attribution can under/over-count vs product analytics depending on dedup logic.

4) **Partial month exports**
   - Feb 2026 channel file contains only **Feb 1–7** totals in the export (`feb_2026_1_7`).

---

## 4) Amplitude cross-check (what we can/can’t do with current export)

`projects/cenoa-performance-marketing/data/amplitude-weekly-2026-03-20.json` provides only a **weekly, global** snapshot:
- Current week: 2026-03-14 → 2026-03-20 (installs=1445, signups=1207, …)
- Previous week: 2026-03-07 → 2026-03-13

**Limitation:** this file does **not** provide:
- monthly totals for Sep 2025 → Feb 2026
- TR-only segmentation
- a “virtual account” or “new active” metric aligned to the CAC Analysis sheet

So we can’t reconcile the historical monthly CAC denominators with Amplitude yet; we can only say: *Amplitude is a better candidate source-of-truth for product events, but we need a monthly export by country (and ideally by paid/organic attribution).* 

---

## 5) Proposed canonical CAC calculation (going forward)

### 5.1 Pick the canonical numerator (spend)
**Recommendation:** Use **Budget Tracking realized spend** as the canonical spend source, because it is closest to what finance considers “actual spend”.

Then define **scopes** explicitly:
- **Paid marketing spend** (what should be used for CAC): ad platform spend + paid networks + paid affiliates.
- **Non-paid growth costs** (tools, subscriptions, headcount): track separately; don’t mix into CAC unless explicitly doing “fully-loaded CAC”.

### 5.2 Pick canonical denominators (product events)
**Recommendation:** Use **Amplitude (product events)** for denominators, with strict event definitions:

- **Signup:** a single user-level “account created” event (deduped).
- **Virtual account:** the exact product event that corresponds to “virtual account created” (not KYC start; not KYC submit).
- **New active:** define explicitly (examples):
  - first deposit, or
  - first successful transaction, or
  - first week with ≥1 key action

### 5.3 Decide the attribution model and keep it consistent
You have two valid CAC flavors — but **don’t mix** them:

1) **Paid-attributed CAC (recommended for channel optimization)**
   - Numerator: paid spend by channel
   - Denominator: paid-attributed signups/virt/actives (AppsFlyer or Amplitude attribution)

2) **Blended CAC (recommended for exec reporting)**
   - Numerator: total paid spend (all channels)
   - Denominator: total signups/virt/actives (paid + organic)
   - Caveat: interpret changes carefully (organic swings will move CAC)

### 5.4 Deliverable table (single source of truth)
Create a canonical fact table:

`month × country × channel × spend_usd × signups × virt_acc × new_active`

- Spend: Budget Tracking (or platform exports) normalized to USD
- Denominators: Amplitude monthly export by country + attribution flag (paid/organic)

This table is the foundation for a “High confidence” CAC dashboard.

---

## Appendix: exact files referenced
- `projects/cenoa-performance-marketing/data/sheets-cac-analysis.json`
- `projects/cenoa-performance-marketing/data/sheets-budget-tracking.json`
- `projects/cenoa-performance-marketing/data/amplitude-weekly-2026-03-20.json`
- `projects/cenoa-performance-marketing/data/cac-crosscheck.json` (this task)
