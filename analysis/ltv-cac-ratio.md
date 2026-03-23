# [028] LTV/CAC ratio by country — TR / NG / EG

**Generated:** 2026-03-21  
**Inputs:**
- CAC: `projects/cenoa-performance-marketing/data/country-cac.json` (period **2026-03-09_15**, CAC Analysis sheet)
- LTV: `projects/cenoa-performance-marketing/data/ltv-model.json` ([027] scenario-based LTV per active user)

## What this file computes
For each country (TR/NG/EG) and each LTV scenario (Low/Base/High):
1) **LTV/CAC**
2) **Payback period (months)**

### Metric alignment (important)
- The LTV model is **per monetization-active user** (withdrawal-active).
- The closest CAC proxy available in `country-cac.json` is **Cost / Paid Active** from the CAC Analysis sheet (`cp_paid_active_usd_sheet`).

So we compute:
- **LTV/CAC = LTV_per_active_user / CAC_per_paid_active**
- **Monthly gross profit (scenario) = LTV / lifetime_months**
- **Payback (months) = CAC / monthly_gross_profit**

---

## CAC inputs used (Cost / Paid Active) — Mar 9–15, 2026
From `data/country-cac.json → periods["2026-03-09_15"]`:

| Country | CAC (USD) | Field |
|---|---:|---|
| TR | 864 | `cp_paid_active_usd_sheet` |
| NG | 16 | `cp_paid_active_usd_sheet` |
| EG | 64 | `cp_paid_active_usd_sheet` |

> Note: this CAC is **weekly** and can be noisy (small `paid_active` counts).

---

## LTV inputs (per active user) — from [027]

| Country | Low LTV | Base LTV | High LTV |
|---|---:|---:|---:|
| TR | 9.0 | 72.0 | 600.0 |
| NG | 3.6 | 28.8 | 240.0 |
| EG | 2.7 | 21.6 | 180.0 |

**Lifetime months per scenario (from [027]):** Low=3, Base=6, High=12  
So **monthly gross profit** is simply LTV / months.

| Country | Monthly GP (Low) | Monthly GP (Base) | Monthly GP (High) |
|---|---:|---:|---:|
| TR | 3.00 | 12.00 | 50.00 |
| NG | 1.20 | 4.80 | 20.00 |
| EG | 0.90 | 3.60 | 15.00 |

---

## Results: LTV/CAC (unitless)

| Country | Low | Base | High |
|---|---:|---:|---:|
| **TR** | 0.01× | 0.08× | 0.69× |
| **NG** | 0.23× | 1.80× | 15.00× |
| **EG** | 0.04× | 0.34× | 2.81× |

## Results: Payback (months)

| Country | Low | Base | High |
|---|---:|---:|---:|
| **TR** | 288.0 | 72.0 | 17.3 |
| **NG** | 13.3 | 3.3 | 0.8 |
| **EG** | 71.1 | 17.8 | 4.3 |

---

## Critical gating note (do not ignore)
Amplitude country outcomes show **KYC submit clicked = 0** for **NG and EG** (Mar 14–20):
- **Scaling NG/EG is blocked** until KYC submit is non-zero.
- Treat NG/EG CAC and the above **LTV/CAC + payback** as **"if-KYC-unlocked"** unit economics.

Practically:
- **TR:** ratios reflect a functioning KYC funnel (still expensive CAC).
- **NG/EG:** ratios are only actionable after KYC is fixed/unblocked.

---

## Machine-readable export
- `projects/cenoa-performance-marketing/data/ltv-cac-ratio.json`
