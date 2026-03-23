# Country CAC (TR vs NG vs EG)

**Goal:** compute country-level acquisition costs (CAC / CPI) for **installs, signups, KYC, virtual account, paid active** where data allows.

**Data sources (available in repo):**
- Spend + Jan/Feb realized: `data/sheets-budget-tracking.json|md`
- Weekly country performance (installs/signups/virt/payer active): `data/sheets-cac-analysis.json|md`
- Country outcomes (installs, signups, KYC submit, deposits, withdrawals): `analysis/country-breakdown.md` (Amplitude, **Mar 14–20**)

> ⚠️ Important: not all metrics are cohort-pure. In particular **deposits/withdrawals** and **KYC started** include returning users.

---

## 1) Spend by country (context)

### Jan 2026 (actual spend)
| Country | Spend | Installs | CPI | KYC Start | $/KYC Start | VirtAcc | $/VirtAcc |
|---|---:|---:|---:|---:|---:|---:|---:|
| TR | $26,235 | 4,238 | $6.19 | 2,258 | $11.62 | 1,895 | **$54** |
| NG | $4,647 | 6,902 | **$0.67** | 3,416 | **$1.36** | 88 | $83 |
| EG | $4,670 | 3,540 | $1.32 | 931 | $5.02 | 20 | **$359** |

**Read:** Nigeria is ultra-cheap on CPI and KYC-start, but very weak on virtual-account creation in Jan (high $/VirtAcc). Egypt is extremely inefficient on VirtAcc in Jan.

### Feb 2026 (actual spend only)
Feb outcomes weren’t populated in the export (sheet shows `#DIV/0!`), so only spend is reliable:
- TR: **$35,435**
- NG: **$12,210**
- EG: **$9,925**

### Mar 1–15 2026 (actual spend summary)
- TR: **$7,824**
- EG: **$5,549**
- NG: “minimal” (weekly breakdown shows **$229** for Mar 9–15)

---

## 2) Weekly CAC (where we can compute installs/signups + sheet CACs)

These are the **only periods** in the provided files where we have **spend + country outcomes in the same table**.

### Week: Mar 9–15 (best comparable week)
| Country | Spend | Installs | CPI | Signups | $/Signup | Cost/VirtAcc (sheet) | Cost/Paid Active (sheet) |
|---|---:|---:|---:|---:|---:|---:|---:|
| TR | $4,320 | 1,654 | $2.61 | 652 | $6.63 | **$35** | **$864** |
| NG | $229 | 660 | **$0.35** | 289 | **$0.79** | **$2** | **$16** |
| EG | $1,598 | 444 | $3.60 | 232 | $6.89 | **$8** | **$64** |

**What this implies (if downstream activation worked):**
- **NG and EG look dramatically more efficient** than TR on the *sheet-defined* “Cost/VirtAcc” and “Cost/Paid Active”.
- But this must be reconciled with Amplitude: **NG/EG have 0 KYC submit** in Mar 14–20 (see §3). Cheap CAC is not bankable if KYC blocks the funnel.

> Note on definitions: in `sheets-cac-analysis.json`, **Cost/Paid Active = cost / paid_active** (not cost / new_active). Also, **Cost/VirtAcc appears paid-only** (virt_acc_total includes other sources), so treat it as a “paid efficiency” metric rather than total blended.

### Week: Mar 1–8 (directional)
- TR: Spend $3,504; CPI $2.14; $/Signup $6.69; Cost/VirtAcc (sheet) $21; Cost/Paid Active (sheet) $210
- EG: Spend $3,951; CPI $4.89; $/Signup $8.39; Cost/VirtAcc (sheet) $10; Cost/Paid Active (sheet) $107
- NG: Spend recorded as $1 (likely missing data) → ignore this week for NG CAC.

---

## 3) Amplitude outcomes (Mar 14–20) — funnel reality check

From `analysis/country-breakdown.md` (Amplitude):

| Country | Installs | Signups | KYC Started | **KYC Submit clicked** | Deposits | Withdrawals |
|---|---:|---:|---:|---:|---:|---:|
| TR | 670 | 226 | 2,594 | **170** | 961 | 1,177 |
| NG | 458 | 117 | 230 | **0** | 448 | 778 |
| EG | 206 | 64 | 62 | **0** | 22 | 23 |

**Hard conclusion:**
- **KYC completion is effectively Turkey-only.** NG/EG show **0** KYC submit clicks despite meaningful installs/signups and even KYC starts.
- That means **spend in NG/EG cannot translate into fully onboarded new users** until KYC is fixed/unblocked.

**Interpretation of deposits/withdrawals:** these are **not** new-user conversions for the week; they likely come from legacy users or non-KYC rails.

---

## 4) Confidence scoring (practical)

Scale: 0.0–1.0.

- **Spend (Sheets): 0.8–0.9** (good)
- **Installs/signups (Sheets weekly): 0.6–0.7** (OK; definitions may differ from Amplitude)
- **VirtAcc + Paid Active CAC (Sheets): 0.6** (internally consistent within sheet, but paid-only vs blended ambiguity)
- **Amplitude KYC submit clicked: 0.9** (pattern is too strong to be noise)
- **Amplitude deposits/withdrawals: 0.4** (returning-user contamination)

---

## 5) Recommendations (budget reallocation)

### A) Short-term (this week): protect ROI + stop bleeding into a broken funnel
1) **Do not scale NG/EG performance budgets** until KYC submit is non-zero.
   - Keep **small test budgets** only (to validate KYC fixes + track KYC submit events).
2) **Shift incremental budget to Turkey** (the only market with KYC completion functioning) while you fix KYC coverage.
3) Use NG/EG primarily as **top-of-funnel learning markets** (creative/LP tests), but gate scaling on a **KYC submit KPI**.

### B) Fix the binding constraint: KYC availability outside TR
- Treat **KYC Submit clicked by country** as the gating metric.
- Investigate Bridge/Bridgexyz support for **NG + EG documents/jurisdictions**; if unsupported, route those countries to an alternative KYC provider.

### C) Once KYC is fixed: EG/NG become the efficiency lever
Based on Mar 9–15 sheet CACs:
- NG: **$2 / paid virtual account**, **$16 / paid active**
- EG: **$8 / paid virtual account**, **$64 / paid active**
- TR: **$35 / paid virtual account**, **$864 / paid active**

If KYC becomes functional, **EG and NG are the obvious scale candidates** for cost-efficient growth.

---

## Appendix: machine-readable export
- `data/country-cac.json` (periodized spend + outcomes + confidence notes)
