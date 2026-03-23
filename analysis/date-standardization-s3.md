# [S3-014] Date Range Standardization Audit

**Date:** 2026-03-23
**Convention:** ISO weeks (Monday 00:00 UTC → Sunday 23:59 UTC)

---

## Convention Rules

1. **Weekly** = Monday 00:00 UTC to Sunday 23:59 UTC (ISO 8601 week)
2. **MTD** = 1st of month 00:00 UTC to current day 23:59 UTC
3. **All Amplitude API calls** use `YYYYMMDD` format
4. **No "N days ago"** — all defaults snap to ISO week boundaries
5. Each script documents the convention in a comment block at the top

---

## Script Audit

### ❌ Scripts That Were Inconsistent (Fixed)

| Script | Before | After | Issue |
|--------|--------|-------|-------|
| `amplitude_attribution.py` | `today - 14 days` / `today - 1` (arbitrary) | Last 2 complete ISO weeks (Mon-Sun) | Not week-aligned; could start/end mid-week |
| `amplitude_country_breakdown.py` | `today - 14 days` / `today - 1` (arbitrary) | Last 2 complete ISO weeks (Mon-Sun) | Same as above |
| `amplitude_platform_breakdown.py` | `today - 14 days` / `today - 1` (arbitrary) | Last 2 complete ISO weeks (Mon-Sun) | Same as above |
| `amplitude_weekly_pull.py` | `today - 7 days` / `today - 1` (rolling) | Last complete ISO week (Mon-Sun) | "last 7 days" not aligned to week boundaries |
| `amplitude_funnel.py` | `today - 30 days` (arbitrary) | Last 4 complete ISO weeks (28d, Mon-Sun) | 30 days ≠ whole weeks; default changed to 28 |
| `amplitude_retention.py` | `today - 30 days` / `today - 1` | Last 4 complete ISO weeks (28d, Mon-Sun) | Same as funnel; default changed to 28 |
| `weekly_channel_country.py` | Hardcoded `20260315`-`20260321` | Dynamic ISO week computation | Dates frozen; wouldn't update on next run |
| `ga4_web_traffic_deepdive.py` | `today - 7 days` / `today - 28 days` (rolling) | Last 1/4 complete ISO weeks (Mon-Sun) | Not week-aligned |

### ✅ Scripts Already Consistent (Convention Documented)

| Script | Status | Notes |
|--------|--------|-------|
| `kpi_auto_update.py` | ✅ OK | Requires explicit `--start`/`--end`; added convention comment noting start=Monday, end=Sunday |
| `amplitude_kyc_deepdive.py` | ✅ OK | Requires explicit `--start`/`--end`; added convention comment |
| `weekly_backfill.py` | ✅ OK | Requires explicit `START_YYYYMMDD END_YYYYMMDD` args; caller responsible for ISO weeks |
| `weekly_report.py` | ✅ N/A | Reads JSON files, no date generation |
| `weekly_actions.py` | ✅ N/A | Timestamp-only (`generated_at`), no date ranges |
| `anomaly_detection.py` | ✅ N/A | Uses `datetime.now(timezone.utc)` for detection timestamp only |
| `sheets_sync.py` | ✅ N/A | Timestamp-only for sync tracking |
| `budget_pacing.py` | ✅ N/A | MTD calculations from Sheets data, no Amplitude date ranges |
| `campaign_health_check.py` | ✅ N/A | Timestamp-only |
| `data_quality_monitor.py` | ✅ N/A | Timestamp-only |
| `monthly_deck.py` | ✅ N/A | Monthly granularity (calendar month), not weekly |
| `bq_campaign_trends_30d.py` | ✅ OK | 30-day rolling window by design (BQ data availability); already uses `isocalendar()` for week labels |
| `retention_curves*.py` | ✅ N/A | Visualization scripts, dates come from input data |

### Shell Scripts (No Date Changes Needed)

| Script | Notes |
|--------|-------|
| `weekly_kpi_cron.sh` | Orchestrator; dates flow from Python scripts |
| `weekly_report_cron.sh` | Orchestrator |
| `anomaly_alert_cron.sh` | Orchestrator |
| `dead_campaign_sweep_cron.sh` | Orchestrator |
| `auto_deploy_cortex.sh` | Deployment only |
| `run_backfill_12weeks.sh` | Generates Monday-Sunday pairs (already ISO-week aligned) |

---

## Key Changes Summary

1. **`datetime.now()` → `datetime.utcnow()`** in all default-date computations to ensure UTC consistency
2. **"N days ago" → ISO week snap**: `today.weekday()` used to find last Sunday, then compute Monday
3. **Default periods changed**: 30 → 28 days (4 complete ISO weeks) where applicable
4. **Hardcoded dates removed** from `weekly_channel_country.py` — now computed dynamically
5. **Convention comment block** added to all date-parameterized scripts
