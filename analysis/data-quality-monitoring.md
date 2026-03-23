# Data Quality Monitoring

Generated: `2026-03-22T15:57:46.814441+00:00`

Overall severity: **CRIT**

## Failures / Alerts

- **CRIT** — Amplitude signups: (none) country/platform share: Event `Cenoa sign-up completed` — (none) country share: 62.5% (754/1207); (none) platform share: 62.5% (754/1207).
- **WARN** — AppsFlyer installs: "Organic" share high while paid spend is high: Organic installs share is 43.8% (632/1444) while weekly paid spend proxy is $6,714.
- **WARN** — BigQuery: daily_installs_campaign_tr coverage: Daily table has only 6 distinct days (min=2026-02-25, max=2026-03-02); expected >= 21 days for stable reporting.
- **CRIT** — Required output files present: Missing required file(s): data.json

## Checks

### Amplitude signups: (none) country/platform share
- ID: `amplitude_none_country_platform`
- Status: **FAIL**
- Severity: **CRIT**
- Message: Event `Cenoa sign-up completed` — (none) country share: 62.5% (754/1207); (none) platform share: 62.5% (754/1207).
- Metrics:
  - event: Cenoa sign-up completed
  - country_file: amplitude-country-2026-03-20.json
  - platform_file: amplitude-platform-2026-03-20.json
  - none_country_share: 0.624689
  - none_platform_share: 0.624689
  - warn_threshold: 0.300000
  - crit_threshold: 0.500000
- Recommended fix: Investigate why country/platform properties are missing for signups: (1) verify Amplitude property mapping / SDK initialization, (2) check web→app or server-side events missing device context, (3) ensure the event is instrumented consistently across clients, (4) backfill/patch if possible.

### AppsFlyer installs: "Organic" share high while paid spend is high
- ID: `appsflyer_organic_share_paid_spend`
- Status: **FAIL**
- Severity: **WARN**
- Message: Organic installs share is 43.8% (632/1444) while weekly paid spend proxy is $6,714.
- Metrics:
  - source: channel-cac.json
  - organic_installs: 632
  - total_installs: 1444
  - organic_share: 0.437673
  - paid_spend_weekly_proxy_usd: 6714.000000
  - organic_share_threshold: 0.400000
  - paid_spend_weekly_threshold_usd: 2000.000000
- Recommended fix: Possible paid→organic attribution loss (web→app handoff, deep link/IDFA/GAID loss, SKAN limitations). Audit AppsFlyer attribution settings, ensure OneLink/deep links are used, verify paid campaigns pass correct parameters, and cross-check platform dashboards vs AppsFlyer.

### BigQuery: daily_installs_campaign_tr coverage
- ID: `bigquery_daily_table_coverage`
- Status: **FAIL**
- Severity: **WARN**
- Message: Daily table has only 6 distinct days (min=2026-02-25, max=2026-03-02); expected >= 21 days for stable reporting.
- Metrics:
  - table: cenoa-marketingdatawarehouse.marketing_appsflyer.daily_installs_campaign_tr
  - min_date: 2026-02-25
  - max_date: 2026-03-02
  - distinct_days: 6
  - min_days_required: 21
- Recommended fix: Extend the BigQuery load/ELT for daily_installs_campaign_tr to cover at least the last 21-30 days (backfill missing partitions) and verify the scheduled job is running.

### Required output files present
- ID: `required_files_present`
- Status: **FAIL**
- Severity: **CRIT**
- Message: Missing required file(s): data.json
- Metrics:
  - required: ['data.json', 'anomalies.json', 'campaign-health.json']
  - missing: ['data.json']
- Recommended fix: Re-run the pipelines that generate these artifacts (weekly report / anomalies / campaign health). If `data.json` is deprecated, update this monitor to the new canonical dataset export name.
