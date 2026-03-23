# [023] Blended CAC (monthly, last 6 months)

**Generated:** 2026-03-21  
**Primary scope:** Turkey (TR) — last 6 months (Sep 2025 → Feb 2026)  
**Why TR-only for the 6-month view:** The `CaC Analysis` sheet contains a complete monthly time series (spend + signups + virtual accounts + new actives) for **Turkey**. Budget Tracking has multi-country spend, but consistent multi-country monthly denominators are not present in the provided exports.

---

## 0) Definitions (denominators)

We compute 3 blended CACs:

1) **Cost per signup** = Spend / Sign-ups  
2) **Cost per virtual account** = Spend / Virtual Accounts  
3) **Cost per new active** = Spend / New Active Users

**Important:** “Virtual account” and “New active” are taken *as-defined in the CAC Analysis sheet* (AppsFlyer attribution model). Treat as the canonical marketing-funnel denominators until we unify definitions across sheets.

---

## 1) Spend overview (Budget vs Realized) — 2026

**Plan:** $50,000 / month (Budget Distribution 2026)

**Realized spend (global, all countries) — Budget Tracking**

| Month | Planned | Realized | Utilization | Confidence |
|---|---:|---:|---:|---|
| 2026-01 | 50,000 | 35,552 | 71% | **High** (finance/ops sheet) |
| 2026-02 | 50,000 | 57,570 | 115% | **High** |

**Realized spend (Turkey only) — Budget Tracking**

| Month | TR Spend | Confidence |
|---|---:|---|
| 2026-01 | 26,235 | **High** |
| 2026-02 | 35,435 | **High** |

---

## 2) Blended CAC — Turkey (last 6 months)

### 2.1 TR blended CAC (internally consistent view)
Source: `sheets-cac-analysis.json → sum_turkey.months_2025 + months_2026`  
This is the cleanest time series because **numerator and denominators come from the same model**.

| Month | Spend | Sign-ups | Virt Acc | New Active | $/Signup | $/VirtAcc | $/Active | Confidence |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 2025-09 | 35,839 | 2,357 | 687 | 283 | 15.2 | 52.2 | 126.6 | **Med** |
| 2025-10 | 29,556 | 1,566 | 550 | 242 | 18.9 | 53.7 | 122.1 | **Med** |
| 2025-11 | 26,850 | 1,500 | 628 | 221 | 17.9 | 42.8 | 121.5 | **Med** |
| 2025-12 | 23,312 | 1,719 | 754 | 271 | 13.6 | 30.9 | 86.0 | **Med** |
| 2026-01 | 27,088 | 2,751 | 900 | 226 | 9.8 | 30.1 | 119.9 | **Med** |
| 2026-02 | 25,811 | 1,721 | 580 | 124 | 15.0 | 44.5 | 208.2 | **Med** |

**Read of the trend (TR):**
- Dec 2025 looks like the efficiency peak (**$86 / new active**).
- Feb 2026 is the outlier worst month (**$208 / new active**), driven by lower downstream conversion (new actives).

### 2.2 TR blended CAC (finance spend numerator, mixed denominators)
Spend source: Budget Tracking (TR)  
Denominators source: CAC Analysis (TR)

Use this when you want CAC *closer to “what we actually spent”*, but it’s **definition-mismatched**, so treat as directional.

| Month | TR Spend (Budget Tracking) | Sign-ups | Virt Acc | New Active | $/Signup | $/VirtAcc | $/Active | Confidence |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 2026-01 | 26,235 | 2,751 | 900 | 226 | 9.5 | 29.1 | 116.1 | **Low** |
| 2026-02 | 35,435 | 1,721 | 580 | 124 | 20.6 | 61.1 | 285.8 | **Low** |

**Reconciliation note:** Feb has a big spend gap between sheets (TR Budget Tracking **$35.4k** vs CAC Analysis **$25.8k**). Likely causes: attribution filtering, missing channels, or inclusion of non-attributed costs in Budget Tracking.

---

## 3) Channel-level insights (TR) — best vs worst

Source: `sheets-cac-analysis.json → channels_2025_turkey` (channel-level)

### Jan 2026 (TR) — Cost per **Active** (paid_active proxy)
**Best (lower is better):**
- **referral_affi:** **$30 / active** (cost $300, actives 10)
- **apple_ads:** **$157 / active**
- **spaze:** **$180 / active**

**Worst:**
- **meta_w2a:** **$3,536 / active** (very poor downstream)
- **website:** **$320 / active**
- **tiktok_app:** **$284 / active**

### Jan 2026 (TR) — Cost per **Virtual Account**
**Best:**
- **referral_affi:** **$7.7 / virt acc**
- **meta_app:** **$21.8 / virt acc**
- **apple_ads / google_app:** **~$35 / virt acc**

**Worst:**
- **meta_w2a:** **$106.1 / virt acc**
- **website:** **$48.7 / virt acc**

### Late 2025 watch-outs
- **Dec 2025:** `meta_w2a` at **$1,124 / active** (still structurally weak).
- **Oct 2025:** `apple_ads` was extremely strong at **$59 / active**.

---

## 4) Optional: Global blended snapshot (Jan 2026 only, mixed sources)

This is provided because Budget Tracking includes NG/EG spend for Jan, but denominators are incomplete.

**Method (mixed):**
- Spend: Budget Tracking (TR+NG+EG)
- TR signups/virt: CAC Analysis TR channel table
- NG/EG signups: inferred from `spend / costPerSignup` (Budget Tracking)
- NG/EG virtual accounts: Budget Tracking totals

| Month | Spend | Sign-ups | Virt Acc | $/Signup | $/VirtAcc | Confidence |
|---|---:|---:|---:|---:|---:|---|
| 2026-01 | 35,552 | 6,655 | 639 | 5.34 | 55.64 | **Low** |

Interpretation: useful only as a **rough blended** reference until we have consistent global monthly denominators.

---

## 5) What I would fix next (to make this “High confidence”)

1) **Unify definitions** of “Virtual Account” + “New Active” across:
   - Budget Tracking (where TR Jan virt acc counts look inflated vs CAC Analysis)
   - CAC Analysis sheet
   - Amplitude events (preferred source of truth for activation)
2) Export **monthly** (not weekly) denominators for NG/EG/PK from Amplitude or AppsFlyer so we can compute a real global blended CAC time series.
3) Create a single “source of truth” table: `month × country × channel × spend × signup × virt_acc × active`.

---

## Files
- Machine-readable: `projects/cenoa-performance-marketing/data/blended-cac.json`
