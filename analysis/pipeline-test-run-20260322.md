# Pipeline Test Run — 2026-03-22

Full end-to-end run of the weekly automation pipeline.

## Results Summary

| # | Script | Status | Exit Code | Notes |
|---|--------|--------|-----------|-------|
| a | Environment setup | ✅ | 0 | Amplitude + GCP creds loaded |
| b | `kpi_auto_update.py` | ✅ (after fix) | 0 | Initially failed with 429 rate limit. Added exponential backoff retry (5 attempts, 5→80s). Retry succeeded. |
| c | `anomaly_detection.py` | ✅ | 0 | Found 1 critical (DAU ▼45.6%), 4 warnings |
| d | `campaign_health_check.py` | ✅ | 0 | 14 healthy, 3 bleeding, 2 fraud, 1 dead channel |
| e | `budget_pacing.py` | ✅ | 2 (by design) | Exit 2 = overspending alert. March pacing at 159.7% ($56.7K vs $50K target). Script functioning correctly. |
| f | `data_quality_monitor.py` | ✅ | 2 (by design) | Exit 2 = warnings found. Output written to data/ and analysis/ |
| g | `weekly_actions.py` | ✅ | 0 | Generated 14 actions |
| h | `weekly_report.py` | ✅ | 0 | Full weekly pulse generated |

## Fix Applied

### `kpi_auto_update.py` — Amplitude 429 Rate Limit

**Problem:** Script made many sequential Amplitude API calls without backoff. Hit concurrent query limit on the country breakdown queries.

**Fix:** Added exponential backoff retry loop (5 attempts, delays: 5s, 10s, 20s, 40s, 80s) around the `requests.get` call in `_query_segmentation()`. On 429 response, sleeps and retries instead of raising immediately.

**Result:** After fix, script completes successfully (takes ~2 min with retries).

## Script Output Details

### b) kpi_auto_update.py
- Week: Mar 16-22, 2026
- Installs: 1,265 (▼40.4%)
- Signups: 1,131 (▼25.7%)
- KYC Submits: 140 (▼52.9%)
- DAU avg: 3,128 (▼29.6%)
- Country breakdown: TR (446 inst), NG (412), EG (298), PK (27)
- Channel perf, budget pacing, campaign health, attribution quality all computed
- Dry-run mode: JSON output printed, no sheets updated

### c) anomaly_detection.py
- 🔴 DAU avg: 3,094 (▼45.6%) — critical
- 🟡 KYC Submits: 185 (▼39.7%) — warning
- 🟡 Installs: 1,455 (▼36.0%) — warning
- 🟡 Virtual Account Opened: 436 (▼31.0%) — warning
- 🟡 Signups: 1,219 (▼27.0%) — warning

### d) campaign_health_check.py
- **Fraud:** appnext (2.6% virt_acc rate), appnext_dsp (1.8% signup rate)
- **Dead:** twitter_ads ($183 for 1 install)
- **Bleeding:** google_app_ios (CPI $24.35), tiktok_web2app (CPI $10.31), onboarding_meta_test (CPI $33.67)
- **Healthy:** 14 channels including pmax_search, meta_web2app, apple_ads, google_search

### e) budget_pacing.py
- Monthly budget: $50,000
- Actual (estimated): $56,658 at day 22/31
- Pace: 159.7% — ⚠️ OVERSPENDING
- Method: weekly TR extrapolation

### f) data_quality_monitor.py
- Wrote data-quality.json and data-quality-monitoring.md
- Exit 2 = quality warnings detected

### g) weekly_actions.py
- Generated 14 prioritized actions
- Written to data/weekly-actions.json

### h) weekly_report.py
- Weekly Pulse: Mar 14-20, 2026
- Key actions: Fix KYC for NG/EG, Pause Appnext + TikTok, Scale Pmax + ASA

## Pipeline Health

**Overall: ✅ All 7 scripts functional** (after rate-limit fix)

Non-zero exit codes from budget_pacing (2) and data_quality_monitor (2) are intentional alert signals, not errors.

The kpi_auto_update.py fix (exponential backoff) should be permanent — Amplitude's concurrent query limits are expected behavior.
