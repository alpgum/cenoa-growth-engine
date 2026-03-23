# Retention & Engagement Analysis
**Generated:** 2026-03-21 03:12
**Period:** Last 30 days ending 2026-03-20

---

## ⚠️ Methodology & Caveats

Amplitude's Event Segmentation API returns **daily unique counts** but does NOT support:
- True cohort retention (D1/D7/D30 by signup date)
- User-level intersection between events across days
- Deduplication of unique users across multiple days

What we CAN compute are **proxy metrics** that directionally indicate retention health.

---

## 1. Engagement Depth (DAU Trends)

| Metric | Value |
|--------|-------|
| Avg DAU (7d) | **3,075** |
| Avg DAU (30d) | **5,044** |

### DAU Last 7 Days

| Date | DAU |
|------|-----|
| 2026-03-14 | 2,879 |
| 2026-03-15 | 2,479 |
| 2026-03-16 | 3,056 |
| 2026-03-17 | 2,879 |
| 2026-03-18 | 3,155 |
| 2026-03-19 | 4,120 |
| 2026-03-20 | 2,954 |

## 2. Retention Proxy (DAU / Cumulative Signups)

This metric shows what percentage of all-time signups (in the period) are active on any given day.
It's a **floor estimate** — true retention would be higher since not all signups are expected to be active daily.

| Metric | Value |
|--------|-------|
| Total Signups (period) | **6,082** |
| Recent Avg DAU | **3,075** |
| Crude Retention % | **50.5%** |

> _This is DAU/cumulative_signups — a floor estimate. True retention requires cohort analysis._

### Daily Breakdown (Last 7 Days)

| Date | Signups | DAU | Cumul. Signups | DAU/Cumul % |
|------|---------|-----|---------------|-------------|
| 2026-03-14 | 181 | 2,879 | 5,044 | 57.1% |
| 2026-03-15 | 204 | 2,479 | 5,248 | 47.2% |
| 2026-03-16 | 164 | 3,056 | 5,412 | 56.5% |
| 2026-03-17 | 164 | 2,879 | 5,576 | 51.6% |
| 2026-03-18 | 149 | 3,155 | 5,725 | 55.1% |
| 2026-03-19 | 191 | 4,120 | 5,916 | 69.6% |
| 2026-03-20 | 166 | 2,954 | 6,082 | 48.6% |

## 3. Activity by Country (Application Opened)

Top countries by 'Application opened' events in the last 30 days.

| Country | Total Opens (30d) | Avg Daily (7d) |
|---------|-------------------|----------------|
| 0 | 1 | 0 |

---

## 4. Interpretation & Next Steps

### What these numbers tell us:
- **DAU trend** shows whether the user base is growing, stable, or declining
- **DAU/Cumulative Signups %** declining over time suggests poor retention (new users churn)
- **DAU/Cumulative Signups %** stable or rising suggests decent retention (users stick around)
- **Country breakdown** reveals geographic concentration and growth markets

### For true D1/D7/D30 retention:
- Use Amplitude's **Retention Analysis** chart in the UI (not available via segmentation API)
- Or use the **Behavioral Cohorts API** + **Export API** for user-level data
- Or set up a BigQuery export and compute cohort retention via SQL

### Recommended actions:
1. Monitor DAU/Signup ratio weekly — declining = retention problem
2. Compare country-level DAU to signups — find where users stick vs churn
3. Set up Amplitude Retention chart for precise D1/D7/D30 numbers
