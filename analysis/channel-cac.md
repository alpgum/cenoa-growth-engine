# Channel CAC (proxy) — Spend vs Outcomes by Channel

**Attribution outcomes period:** 2026-03-14 → 2026-03-20 (Amplitude / AppsFlyer media source)  
**Spend proxy:** weekly average of 2026-03-01→03-08 and 2026-03-09→03-15 (Sheets “CaC Analysis”)

## 1) Scorecard (weekly proxy)

> Caveat: spend + outcomes are from different weeks; treat CPI/CPA numbers as directional. “Cost/Withdrawal” is especially noisy (withdrawals include older cohorts).

| Bucket | Spend (proxy/wk) | Installs | Sign-ups | Withdrawals | CPI | Cost/Signup | Cost/Withdrawal | Confidence |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Google Search | $790.00 | 27 | 7 | 14 | $29.26 | $112.86 | $56.43 | Medium |
| Pmax | $805.50 | 27 | 7 | 15 | $29.83 | $115.07 | $53.70 | Low |
| Apple Search Ads | $600.50 | 75 | 22 | 254 | $8.01 | $27.30 | $2.36 | Medium |
| Appnext | $446.50 | 273 | 24 | 1 | $1.64 | $18.60 | $446.50 | High |
| TikTok | $341.00 | 49 | 8 | 0 | $6.96 | $42.62 | — | Medium |
| Meta | $2,754.00 | 122 | 22 | 22 | $22.57 | $125.18 | $125.18 | Low |
| Referral | $0.00 | 7 | 3 | 13 | $0.00 | $0.00 | $0.00 | Low |
| Organic | $0.00 | 632 | 77 | 487 | $0.00 | $0.00 | $0.00 | High |
| Architect | $0.00 | 73 | 19 | 0 | $0.00 | $0.00 | — | Low |
| Other | $976.50 | 159 | 31 | 65 | $6.14 | $31.50 | $15.02 | Low |
| Unattributed | $0.00 | 0 | 986 | 1,355 | — | $0.00 | $0.00 | Low |

## 2) Downstream efficiency from Sheets (weekly avg, early March)

Sheets has **virt_acc** and **new_active** (better “activation” proxies than withdrawals).

| Bucket | Spend (proxy/wk) | VirtAcc (avg/wk) | New Active (avg/wk) | Cost/VirtAcc | Cost/New Active |
|---|---:|---:|---:|---:|---:|
| Google Search | $790.00 | 124 | 31 | $6.37 | $25.48 |
| Pmax | $805.50 | 87 | 42 | $9.26 | $19.18 |
| Apple Search Ads | $600.50 | 50 | 26 | $12.01 | $22.66 |
| Appnext | $446.50 | 24 | 0 | $19.00 | $893.00 |
| TikTok | $341.00 | 54 | 12 | $6.26 | $28.42 |
| Meta | $2,754.00 | 108 | 34 | $25.50 | $82.21 |
| Other | $976.50 | 72 | 32 | $13.66 | $30.52 |

## 3) Recommendations (stop/scale)

**Scale:**
- **Apple Search Ads** — strongest intent + best downstream activity; keep expanding brand exact/broad + competitor/generic.  
- **Google Search (+Pmax)** — reliable quality. Fix reporting so Search vs Pmax are separated consistently.

**Stop / keep paused:**
- **Appnext** — classic CPI fraud pattern (high installs, near-zero withdrawals; terrible virt_acc efficiency in Sheets).
- **TikTok** — installs without downstream (0 withdrawals in attribution; weak activations in Sheets).

**Watchlist (run controlled tests):**
- **Meta** — meaningful volume but attribution loss is huge (“(none)” sign-ups/withdrawals). Needs measurement fix + creative/targeting iteration.
- **Architect** — decent sign-up rate but 0 withdrawals in the attribution week; validate cohort maturation and ensure spend is tracked in Sheets.
- **Other (Spaze/byteboost/website)** — mixed quality; keep only placements with verified virt_acc/new_active.

## 4) Measurement gaps (why confidence is not “High”)

- **Unattributed dominates downstream:** 986 sign-ups and 1,355 withdrawals are “(none)” in the attribution export. Channel ROI is undercounted, especially for Meta/Web2App flows.
- **Withdrawals are not same-cohort:** they include existing users; don’t treat cost/withdrawal as true CAC for the week.
- **Google Search vs Pmax:** attribution only exposes `googleadwords_int` at source level; split here is based on spend share (proxy).
