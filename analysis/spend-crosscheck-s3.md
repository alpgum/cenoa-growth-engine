# Spend Cross-Check: data.json vs Sheets vs Campaign Reports
**Task:** S3-012 | **Date:** 2026-03-23

---

## Sources Compared

| # | Source | File | Time Period | Total Spend |
|---|--------|------|-------------|------------:|
| 1a | data.json `channelPerformance` | `cenoa-cortex/data.json` | "Mar 14-20" (labeled) | **$5,714.00** |
| 1b | data.json `countrySpend` | `cenoa-cortex/data.json` | "Mar 14-20" (labeled) | **$6,147.00** |
| 2 | Sheets CAC Analysis | `data/sheets-cac-analysis.json` | Mar 9-15 (actuals) | **$6,147.00** |
| 3 | Campaign Performance Report | `analysis/campaign-performance-weekly-mar15-21.md` | Mar 15-21 (estimated) | **$6,147.00** |
| 4 | Weekly Spend Report | `analysis/weekly-spend-mar15-21.md` | Mar 15-21 (estimated) | **$6,147.00** |

### ⚠️ Critical Finding: Internal Discrepancy in data.json

data.json contains **two spend aggregations that disagree**:
- `channelPerformance` sums to **$5,714** (7 channel buckets)
- `countrySpend` sums to **$6,147** (4 country buckets)
- **Gap: $433 (7.0%)** — exceeds 5% threshold

---

## 1. Per-Channel Comparison

### A. Country-Level Totals

| Country | data.json `countrySpend` | Sheets | Campaign Report | Max Δ% |
|---------|-------------------------:|-------:|----------------:|-------:|
| 🇹🇷 Turkey | $4,320 | $4,320 | $4,320 | **0%** ✅ |
| 🇪🇬 Egypt | $1,598 | $1,598 | $1,598 | **0%** ✅ |
| 🇳🇬 Nigeria | $229 | $229 | $229 | **0%** ✅ |
| 🇵🇰 Pakistan | $0 | $0 | $0 | **0%** ✅ |
| **Total** | **$6,147** | **$6,147** | **$6,147** | **0%** ✅ |

Country-level spend is consistent across all three sources because the campaign reports explicitly used Sheets Mar 9-15 actuals as their spend source, and data.json `countrySpend` was populated from the same Sheets data.

### B. Channel-Level Comparison (Turkey)

| Channel | data.json `channelPerf` | Sheets | Campaign Report | Δ data.json vs Sheets |
|---------|------------------------:|-------:|----------------:|----------------------:|
| Google (all) | $790 + $805.5 = $1,595.5¹ | $1,235² | $1,235 | **+$360.50 (+29.2%)** 🔴 |
| Apple Ads | $600.50 | $500³ | $500 | **+$100.50 (+20.1%)** 🔴 |
| Meta (all) | $2,754.00 | $485⁴ + $101⁵ = $586 | $485 + $101 = $586 | **+$2,168 (+370%)** 🔴 |
| Appnext | $446.50 | $645 | $645 | **-$198.50 (-30.8%)** 🔴 |
| TikTok (all) | $341.00 | $364 | $364 | **-$23.00 (-6.3%)** 🔴 |
| Spaze | — (in "Other") | $900 | $900 | N/A (different grouping) |
| Twitter | — (in "Other") | $90 | $90 | N/A (different grouping) |
| Other | $976.50 | — | — | N/A |
| **TR Total** | **~$5,714⁶** | **$4,320** | **$4,320** | **+$1,394 (+32.3%)** 🔴 |

¹ data.json has "Google Search" ($790) + "Pmax" ($805.5) — combined as Google  
² Sheets: google_search ($782) + google_web2app ($453) = $1,235  
³ Sheets: TR apple_ads only; data.json likely includes EG apple_ads ($33) = $533 total cross-country  
⁴ Sheets: TR meta_web2app only  
⁵ Sheets: onboarding_meta_test  
⁶ channelPerformance is cross-country (not TR-only), making direct comparison invalid

### C. Channel-Level Comparison (Egypt)

| Channel | Sheets | Campaign Report | Δ% |
|---------|-------:|----------------:|---:|
| Apple Ads | $33 | $33 | 0% ✅ |
| Google Search | $116 | $116 | 0% ✅ |
| Meta Get Paid | $637 | — (combined) | — |
| Meta LTV Test | $812 | — (combined) | — |
| Meta Combined | $1,449 | $1,449 | 0% ✅ |
| **EG Total** | **$1,598** | **$1,598** | **0%** ✅ |

### D. Channel-Level Comparison (Nigeria)

| Channel | Sheets | Campaign Report | Δ% |
|---------|-------:|----------------:|---:|
| Google Search | $229 | $229 | 0% ✅ |

---

## 2. Grand Totals

| Source | Total | vs Sheets Δ% |
|--------|------:|-------------:|
| data.json `countrySpend` | $6,147 | **0%** ✅ |
| Sheets (Mar 9-15) | $6,147 | — (baseline) |
| Campaign Report (Mar 15-21 est.) | $6,147 | **0%** ✅ |
| Weekly Spend Report | $6,147 | **0%** ✅ |
| data.json `channelPerformance` | $5,714 | **-7.0%** 🔴 |

---

## 3. Discrepancies Flagged (>5%)

### 🔴 Discrepancy 1: data.json `channelPerformance` total ($5,714) vs all other sources ($6,147)
- **Gap:** $433 (7.0%)
- **Root Cause:** `channelPerformance` is a **cross-country channel roll-up** that groups differently than the country-level breakdown. It appears to:
  - Merge TR + EG + NG spend into single channel buckets (e.g., "Google Search" = TR + partial EG/NG)
  - Exclude or partially count some channels (Spaze, Twitter lumped into "Other")
  - Use **different time-window or partial data** — labeled "Mar 14-20" vs Sheets' "Mar 9-15"
  - Possible rounding or manual entry errors in the aggregation

### 🔴 Discrepancy 2: Channel-level mapping misalignment
- **data.json "Meta": $2,754** vs **Sheets TR+EG Meta total: $2,035** (+35.3%)
  - Root cause: data.json Meta likely includes `campaignPerformance` MTD figures or a different period. The $2,754 doesn't match any single-week Sheets total.
- **data.json "Appnext": $446.50** vs **Sheets Appnext: $645** (-30.8%)
  - Root cause: Different periods — data.json may reflect a partial week or daily average extrapolation.
- **data.json "Apple Search Ads": $600.50** vs **Sheets (TR+EG): $533** (+12.7%)
  - Root cause: Cross-country aggregation plus possible different time window.

### 🟡 Discrepancy 3: Campaign reports use Mar 9-15 spend as Mar 15-21 proxy
- **Gap:** Unknown (actual Mar 15-21 spend not yet available)
- **Root Cause:** Reports explicitly state: *"Mar 15-21 spend proxied from Mar 9-15 Sheets actuals (final figures not yet available)."* Estimated ±15-25% variance per the report's own caveat.
- **Impact:** All "Mar 15-21" spend figures in the campaign report are estimates, not actuals.

---

## 4. Root Cause Summary

| Discrepancy | Root Cause | Severity |
|-------------|-----------|----------|
| data.json `channelPerformance` vs `countrySpend` ($433 gap) | **Different aggregation logic** — channelPerformance groups cross-country and may use different time periods or partial data | 🔴 High |
| Meta spend mismatch ($2,754 vs $2,035) | **Cross-country + time period mismatch** — data.json channelPerformance likely blends MTD or different weekly window | 🔴 High |
| Appnext ($446.50 vs $645) | **Time period difference** — channelPerformance labeled "Mar 14-20" vs Sheets "Mar 9-15" | 🔴 High |
| Campaign report = Sheets (0% diff) | **Same source** — report explicitly used Sheets Mar 9-15 as proxy | ✅ Expected |
| countrySpend = Sheets (0% diff) | **Same source** — countrySpend was populated from Sheets | ✅ Expected |

---

## 5. Recommendations: Source of Truth

| Metric | Recommended Source | Rationale |
|--------|-------------------|-----------|
| **Weekly spend by country** | 📊 **Google Sheets** | Primary data entry point; manually verified; most granular |
| **Weekly spend by channel** | 📊 **Google Sheets** (`channel_2026_all` tab) | Channel × country breakdown with actual platform spend |
| **Channel-level aggregation** | ❌ **NOT data.json `channelPerformance`** | Cross-country grouping is inconsistent; $433 gap unexplained; channel buckets don't map cleanly |
| **Country-level spend** | 📊 **Google Sheets** (use data.json `countrySpend` as mirror — they match) | Both sources agree when populated from same Sheets data |
| **Campaign-level TRUE CAC** | 📊 **Sheets** for spend × **Amplitude** for funnel | Campaign reports already do this correctly |
| **MTD pacing** | 📊 **data.json `budgetPacing`** | Only source tracking cumulative spend vs targets |

### Action Items

1. **Fix `channelPerformance` in data.json** — Either:
   - Derive it from `countrySpend` channel breakdowns (Sheets data) so totals match, OR
   - Add a `source` and `period` field to make the aggregation transparent
2. **Add timestamps to data.json arrays** — `channelPerformance` and `countrySpend` should specify exact date ranges, not inherit the top-level `"week"` label if they cover different periods
3. **Avoid circular references** — Campaign reports should note when spend = Sheets proxy (already done ✅) and flag confidence level
4. **Backfill Mar 15-21 actuals** — Once Sheets is updated with real Mar 15-21 spend, regenerate campaign reports with actual data

---

*Generated: 2026-03-23 00:32 TRT | Task: S3-012*
