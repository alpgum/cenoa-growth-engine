# [029] Budget efficiency ranking (Channels + Countries)

**Generated:** 2026-03-21  
**Attribution outcomes window:** 2026-03-14 → 2026-03-20 (AppsFlyer/Amplitude media source buckets)  
**Spend used for efficiency:** weekly proxy (avg of 2026-03-01→03-08 and 2026-03-09→03-15) from Sheets “CAC Analysis”.

> **Interpretation rule:** treat **CPI / Cost per Signup** as *directional* (spend+outcomes are from different weeks). For downstream efficiency use **Sheets metrics** (VirtAcc + New Active) because they’re in the same spend table.

---

## Decision Dashboard (one page)

### Do now (this week)
- **Pause Appnext (100%)** — fraud/low-quality signature: huge installs, near-zero downstream.
- **Pause TikTok (100%)** — installs with **0 withdrawals** in attribution week; keep only if KYC-submit / paid-active improves.
- **Scale Pmax** (primary scale lever) — best *cost per active* among paid channels.
- **Keep Google Search + ASA as “intent anchors”** — strong quality; expand cautiously alongside Pmax.
- **Keep Meta capped / under test** until attribution & cohort linkage improves (Meta looks expensive on downstream).

### Concrete weekly reallocation (channel-level, based on spend proxy)
- Budget freed by pausing **Appnext ($446.5/wk)** + **TikTok ($341.0/wk)** = **$787.5/wk**
- Reallocate the freed **$787.5/wk** as:
  - **+ $500/wk to Pmax** (scale)
  - **+ $200/wk to Google Search** (protect high-intent volume)
  - **+ $87.5/wk to Apple Search Ads** (incremental intent)

**Resulting weekly mix (proxy):**
- Google Search **$990/wk** (was $790)
- Pmax **$1,305.5/wk** (was $805.5)
- Apple Search Ads **$688/wk** (was $600.5)
- Meta **$2,754/wk** (unchanged)
- Other **$976.5/wk** (unchanged)
- Appnext **$0** (paused)
- TikTok **$0** (paused)

### Geo reallocation (country-level)
- **Move 10% of TR performance budget to NG/EG as a KYC-unlock test pool** (not a scale move).
  - Suggested split: **60% NG / 40% EG** (keep both alive for signal).
  - **Guardrail:** if **KYC submit clicked stays 0** after fixes + 72h, revert the moved budget to TR.
- **After KYC is fixed outside TR:** shift an additional **20–30%** from TR → NG/EG because NG/EG are dramatically cheaper on paid virt-acc & paid-active in Sheets.

### Non-negotiable guardrails (to avoid “cheap CPI traps”)
- Channel scale gate: **Cost/New Active (Sheets)** and/or **Cost/Paid Active** must improve, not just CPI.
- Country scale gate: **KYC submit clicked > 0** (Amplitude) in NG/EG before scaling.

---

## 1) Channel rankings — Best/Worst by efficiency

Paid channels included: **Google Search, Pmax, Apple Search Ads, Appnext, TikTok, Meta, Other**.

### A) Cost per Install (CPI) — proxy (lower is better)
| Rank | Channel | CPI | Spend (proxy/wk) | Installs (attr wk) |
|---:|---|---:|---:|---:|
| 1 | Appnext | $1.64 | $446.50 | 273 |
| 2 | Other | $6.14 | $976.50 | 159 |
| 3 | TikTok | $6.96 | $341.00 | 49 |
| 4 | Apple Search Ads | $8.01 | $600.50 | 75 |
| 5 | Meta | $22.57 | $2,754.00 | 122 |
| 6 | Google Search | $29.26 | $790.00 | 27 |
| 7 | Pmax | $29.83 | $805.50 | 27 |

**Read:** Appnext “wins” CPI but fails downstream → **do not optimize to CPI**.

### B) Cost per Signup — proxy (lower is better)
| Rank | Channel | Cost/Signup | Spend (proxy/wk) | Signups (attr wk) |
|---:|---|---:|---:|---:|
| 1 | Appnext | $18.60 | $446.50 | 24 |
| 2 | Apple Search Ads | $27.30 | $600.50 | 22 |
| 3 | Other | $31.50 | $976.50 | 31 |
| 4 | TikTok | $42.62 | $341.00 | 8 |
| 5 | Google Search | $112.86 | $790.00 | 7 |
| 6 | Pmax | $115.07 | $805.50 | 7 |
| 7 | Meta | $125.18 | $2,754.00 | 22 |

### C) Cost per Virtual Account (Sheets) — downstream (lower is better)
| Rank | Channel | Cost/VirtAcc | Spend (proxy/wk) | VirtAcc (sheet avg/wk) |
|---:|---|---:|---:|---:|
| 1 | TikTok | $6.26 | $341.00 | 54 |
| 2 | Google Search | $6.37 | $790.00 | 124 |
| 3 | Pmax | $9.26 | $805.50 | 87 |
| 4 | Apple Search Ads | $12.01 | $600.50 | 50 |
| 5 | Other | $13.66 | $976.50 | 72 |
| 6 | Appnext | $19.00 | $446.50 | 24 |
| 7 | Meta | $25.50 | $2,754.00 | 108 |

### D) Cost per Active (Sheets “New Active”) — downstream (lower is better)
| Rank | Channel | Cost/New Active | Spend (proxy/wk) | New Active (sheet avg/wk) |
|---:|---|---:|---:|---:|
| 1 | Pmax | $19.18 | $805.50 | 42 |
| 2 | Apple Search Ads | $22.66 | $600.50 | 26 |
| 3 | Google Search | $25.48 | $790.00 | 31 |
| 4 | TikTok | $28.42 | $341.00 | 12 |
| 5 | Other | $30.52 | $976.50 | 32 |
| 6 | Meta | $82.21 | $2,754.00 | 34 |
| 7 | Appnext | $893.00 | $446.50 | 0 |

**Bottom line:** If we optimize to *downstream activation*, the scale order is:
1) **Pmax** → 2) **ASA** → 3) **Google Search** → 4) **Other (selectively)** → (Meta only after measurement fixes)

---

## 2) Low-quality / fraud-risk flags

### Must-pause
- **Appnext**
  - Attribution week: **273 installs → 24 signups → 1 withdrawal**
  - Sheets: **New Active = 0** ⇒ **$893 / new active**
  - Pattern matches “cheap CPI / no activation” traffic.

- **TikTok**
  - Attribution week: **49 installs → 8 signups → 0 withdrawals**
  - Even if Sheets shows some virt-acc/new-active, the **0 withdrawal** signal is a quality/red-flag in the attribution export.

### Watchlist (don’t scale until fixed)
- **Meta**
  - Very expensive on downstream: **$82 / new active** (Sheets)
  - Also known attribution loss in prior analysis: a lot of downstream is “(none)”.

---

## 3) Country efficiency + why it’s currently not actionable

### Week Mar 9–15 (Sheets CAC Analysis; spend and outcomes aligned)
| Rank | Country | CPI | $/Signup | $/VirtAcc (sheet) | $/Paid Active (sheet) |
|---:|---|---:|---:|---:|---:|
| 1 | NG | $0.35 | $0.79 | $2 | $16 |
| 2 | EG | $3.60 | $6.89 | $8 | $64 |
| 3 | TR | $2.61 | $6.63 | $35 | $864 |

### Funnel reality check (Amplitude, Mar 14–20)
- **KYC submit clicked**: **TR = 170**, **NG = 0**, **EG = 0**

**Conclusion:** NG/EG are *cheaper on paper*, but **cannot be scaled** until KYC submit becomes non-zero. That’s why the recommended TR → NG/EG move is a **test pool** tied to a KYC-submit gate.

---

## 4) Notes on the “Trafik Canavarı” sheet

The parsed `sheets-trafik-canavari.md` export exposes only a single tab (“TR Only”) and does **not** include the requested Pmax vs Search CTA cost breakdown. This analysis therefore uses **Sheets CAC Analysis** “New Active” as the best available CTA/activation proxy for Search vs Pmax.
