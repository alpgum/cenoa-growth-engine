# Cortex SaaS — Performance Marketing Intelligence Module

> **Purpose:** Document how the *Performance Marketing Intelligence* module plugs into **Cortex SaaS** (the external product), so it can be reused beyond the Cenoa-specific implementation.
>
> **Mental model:** Cortex SaaS is the *host platform* (multi-tenant dashboards + scheduler + alerting + action execution). This module is a *tenant-configured package* that ingests marketing/product data, computes decision-grade metrics, and continuously publishes dashboards + action lists.

---

## 1) What the module does (end-to-end)

### 1.1 Data → Analysis → Dashboard → Actions → Campaign management

**A) Data ingestion (connectors / adapters)**
- Pulls raw and semi-aggregated data from:
  - Product analytics (Amplitude)
  - Web analytics (GA4)
  - Paid media spend sources (Google Ads / Meta / TikTok / X / ASA, etc.)
  - Optional warehouse (BigQuery) for raw, cross-channel, or MMP exports

**B) Normalization (metric contract / canonical schema)**
- Converts source-specific fields into a canonical marketing schema:
  - `week`, `updated`, KPI totals, country/platform splits
  - acquisition → activation funnel stages
  - cost/spend + budget plans
  - attribution keys (source, campaign, medium)

**C) Analysis jobs (scheduled compute)**
- Computes:
  - Weekly KPI snapshot + WoW deltas
  - Funnel and segment breakdowns (country / platform / attribution)
  - Anomaly detection (spikes/drops)
  - Campaign health flags (DEAD / BLEEDING / FRAUD)
  - Budget pacing (expected vs actual spend)
  - Auto-generated action items (ranked)

**D) Publish layer (Cortex SaaS dashboards)**
- Writes computed outputs to Cortex SaaS “module outputs” storage (DB/object storage) and exposes them to dashboard components.
- In the current Cenoa reference implementation, this is a single file contract:
  - `projects/cenoa-cortex/data.json` (consumed by a static dashboard)

**E) Actions & ops workflow**
- Produces:
  - A weekly pulse report (human-readable)
  - Alerts when metrics move materially
  - A prioritized action list (“what to do next”)

**F) Campaign management (optional closed loop)**
- Cortex SaaS can optionally execute actions directly:
  - Pause campaigns/ad sets, cap budgets, reallocate spend
  - Create tickets / send Slack/Telegram notifications
  - Enforce naming/UTM hygiene via QA checks

> The key product promise: **from raw data → to a weekly operating system** (dashboards + alerts + recommended actions), with an option to push changes back to ad platforms.

---

## 2) Inputs required (and how they map)

### 2.1 Required inputs

#### A) Amplitude (product funnel truth)
**Used for:** installs → signup → KYC → activation / deposits / withdrawals, retention, attribution breakdowns.

**Credentials (current implementation):**
- `~/.openclaw/credentials/amplitude.env`
  - `AMPLITUDE_API_KEY=...`
  - `AMPLITUDE_SECRET_KEY=...`

**Data pulled by scripts (examples):**
- Weekly KPI totals (Event Segmentation API)
- Country / platform / attribution segmentation

#### B) GA4 (web acquisition + landing page performance)
**Used for:** sessions, source/medium, landing pages, CTA proxy metrics, UTM hygiene.

**Credentials (current implementation):**
- Service account JSON (also used for BigQuery in Cenoa):
  - `~/.openclaw/credentials/cenoa-marketingdatawarehouse-82b8600e66d6.json`

**Required config:**
- `GA4_PROPERTY_ID=<numeric>`
- `GOOGLE_APPLICATION_CREDENTIALS=<path_to_service_account_json>`

> In Cortex SaaS, these should be tenant secrets + a tenant config row (property id).

#### C) Ads spend sources (cost side)
**Used for:** CAC, blended cost, budget pacing, campaign health (cost vs outcomes).

Minimum viable approach (works even when APIs are blocked):
- **Google Sheets / CSV spend exports** ingested into Cortex as a spend table

Preferred approach (SaaS-grade):
- Direct API connectors (per tenant) for:
  - Google Ads
  - Meta Ads
  - TikTok Ads
  - X Ads
  - Apple Search Ads

> The module is designed so spend can come from *any* source as long as it lands in a canonical `spend_daily` / `spend_weekly` schema.

### 2.2 Optional inputs

#### BigQuery (warehouse / cross-check / raw exports)
**Used for:**
- joining multiple sources
- AppsFlyer / MMP raw tables
- longer retention windows
- campaign trends over 30d+ with consistent spend tables

**Credentials:**
- `GOOGLE_APPLICATION_CREDENTIALS=<service_account_json>`

**In this repo:** BigQuery access is confirmed for `cenoa-marketingdatawarehouse` (see `TOOLS.md`).

---

## 3) Outputs (what Cortex SaaS exposes)

### 3.1 Dashboard outputs (module surfaces)

#### A) Weekly KPI snapshot (canonical “topline”)
- KPI totals + previous week + WoW delta
- Example schema (current): `projects/cenoa-cortex/data.json`
  - `week`, `updated`
  - `kpis.{installs, signups, kycSubmits, ...}`
  - `countries.{TR,NG,EG,PK}.{installs, signups}`
  - `highlights[]`

#### B) KPI trends (multi-week)
- Sparkline-ready time series per KPI (recommended for SaaS)
- In the current Cenoa static dashboard, only “this week vs last week” is required, but Cortex SaaS should store a full history table.

#### C) Campaign health
- Flags channels/campaigns as:
  - `DEAD` (spend, no outcomes)
  - `BLEEDING` (CPI/CPA too high)
  - `FRAUD` (installs without downstream)
  - `HEALTHY`
- Current output file: `projects/cenoa-performance-marketing/data/campaign-health.json`

#### D) Budget pacing
- Expected linear pace vs estimated/actual spend
- Current output file: `data/budget-pacing.json`

### 3.2 Alert outputs

#### A) Anomalies
- Per KPI: `prev`, `value`, `deltaPct`, `severity`
- Current output file: `data/anomalies.json`
- Trigger: post-refresh weekly

### 3.3 Reporting outputs

#### Weekly Pulse report (human-readable)
- A single message that summarizes:
  - what moved WoW
  - key anomalies
  - key country changes
  - campaign health flags
  - recommended actions
- Current output file: `data/weekly-report-latest.md`

### 3.4 Action outputs

#### Ranked action list
- Prioritized tasks with:
  - severity (P0/P1/P2)
  - owner (Acquisition/Product/Data)
  - rationale + evidence
- Current output file: `data/weekly-actions.json`

### 3.5 Campaign management outputs (optional)

If the tenant has ad-platform write access enabled, Cortex SaaS can:
- execute a subset of actions automatically (with safeguards), e.g.
  - pause `DEAD` campaigns
  - cap `OVERSPENDING` budgets
  - create “needs review” tickets for `FRAUD` patterns

---

## 4) Setup steps (credentials, scripts, cron wrappers)

This section describes **today’s reference implementation** (OpenClaw + local scripts), and how to map it into Cortex SaaS.

### 4.1 Credentials / secret files (reference implementation)

1) **Amplitude**
- Create:
  - `~/.openclaw/credentials/amplitude.env`
- Contents:
  ```bash
  AMPLITUDE_API_KEY=...
  AMPLITUDE_SECRET_KEY=...
  ```

2) **GA4 (service account)**
- Place service account JSON at:
  - `~/.openclaw/credentials/<tenant-ga4-service-account>.json`
- Set env:
  ```bash
  export GOOGLE_APPLICATION_CREDENTIALS=~/.openclaw/credentials/<file>.json
  export GA4_PROPERTY_ID=<numeric>
  ```

3) **BigQuery (optional)**
- Same `GOOGLE_APPLICATION_CREDENTIALS` pattern.

4) **Ads spend sources**
- Minimum viable: ingest a weekly/monthly spend export into Cortex and produce a canonical spend table (or JSON) consumed by the module.
- Preferred: configure API connectors per tenant (OAuth tokens) in Cortex secrets.

### 4.2 Scripts (what runs)

Core scripts in this repo (computation layer):

- **Weekly KPI snapshot**
  - `scripts/kpi_auto_update.py` (Amplitude → canonical weekly KPIs)
- **Anomaly detection**
  - `scripts/anomaly_detection.py` (diff vs previous, severity)
- **Weekly report generation**
  - `scripts/weekly_report.py` (Markdown/Telegram formatted)
- **Campaign health**
  - `scripts/campaign_health_check.py` (DEAD/BLEEDING/FRAUD)
- **Budget pacing**
  - `scripts/budget_pacing.py`
- **Action generation**
  - `scripts/weekly_actions.py` (ranked actions from anomalies + health + pacing)

### 4.3 Cron wrappers (how it’s operationalized today)

Wrappers designed for scheduling (and piping stdout to messaging):

- `scripts/weekly_kpi_cron.sh`
  - computes last week window
  - runs KPI pull
  - commits/pushes `data.json`
  - deploys dashboard (Vercel)

- `scripts/anomaly_alert_cron.sh`
  - runs anomaly detection and prints an alert if needed

- `scripts/weekly_report_cron.sh`
  - prints a weekly report (saves `data/weekly-report-latest.md`)

- `scripts/dead_campaign_sweep_cron.sh`
  - runs campaign health, prints alert if flags exist

See: `analysis/automation-setup.md` for current schedules/order.

### 4.4 Cortex SaaS mapping (how to port the setup)

In Cortex SaaS, replace filesystem + git deploy with platform primitives:

- **Secrets manager**
  - Store Amplitude key/secret
  - Store GA4 service account JSON (or OAuth)
  - Store ad platform tokens

- **Scheduler**
  - Schedule jobs per tenant:
    - `weekly_kpi_refresh` (Mon 09:00 tenant TZ)
    - `anomaly_detection` (after refresh)
    - `weekly_report` (Mon 10:00)
    - `campaign_health` (Mon 09:05)
    - `budget_pacing` (daily or weekly)
    - `weekly_actions` (after anomalies + campaign health)

- **Storage**
  - Persist outputs into:
    - `weekly_kpi_snapshots` table (history)
    - `anomalies` table
    - `campaign_health` table
    - `weekly_reports` table
    - `action_items` table

- **Dashboard components**
  - Read from the above tables instead of `data.json`.

---

## 5) Limitations + roadmap

### 5.1 Current limitations (as seen in the reference implementation)

1) **Meta Ads API access constraints**
- In this workspace, Meta programmatic access is inconsistent (MCP not reliably available to subagents).
- Impact: campaign-level insights are limited; some spend is proxied from Sheets rather than pulled directly.

2) **Attribution gaps (web → app leakage)**
- Downstream events can land in `(none)` / misattributed buckets.
- Impact: channel-level CAC/ROI is directionally useful but not decision-grade until attribution is repaired.

3) **Spend granularity and freshness**
- If spend comes from Sheets/exports, pacing and campaign health can lag (and may rely on proxies).

4) **Schema is file-centric (today)**
- The static dashboard reads a single `data.json`; SaaS needs a first-class historical metrics model.

### 5.2 Roadmap (SaaS-grade module)

**A) First-class connectors**
- Meta Ads, Google Ads, TikTok Ads connectors with:
  - daily spend, impressions/clicks
  - campaign/adset/ad level breakdown
  - creative metadata

**B) Attribution fixes (highest leverage)**
- MMP / deep-linking:
  - AppsFlyer OneLink + deferred deep linking
  - UTM persistence web → app
  - consistent campaign naming + parameter contracts
- Add “attribution confidence” scoring per metric segment (surface it in dashboards).

**C) Closed-loop campaign management (guardrailed)**
- Add action execution policies:
  - require human approval above thresholds
  - auto-pause only for strict DEAD cases
  - rate-limited changes + audit log

**D) Data quality monitoring (platform-native)**
- Detect:
  - missing events
  - sudden zeros
  - rising `(none)` for country/platform/attribution
  - duplicate events / instrumentation regressions

**E) Multi-tenant parameterization**
- Everything tenant-specific becomes config:
  - KPI event names and mapping
  - country lists / priority markets
  - KPI thresholds and anomaly sensitivity
  - channel taxonomy + spend source mapping

---

## Appendix A — Reference file map (current repo)

### Canonical KPI surface consumed by Cortex dashboard
- `projects/cenoa-cortex/data.json`

### Module outputs (audit trail)
- `projects/cenoa-performance-marketing/data/anomalies.json`
- `projects/cenoa-performance-marketing/data/campaign-health.json`
- `projects/cenoa-performance-marketing/data/budget-pacing.json`
- `projects/cenoa-performance-marketing/data/weekly-actions.json`
- `projects/cenoa-performance-marketing/data/weekly-report-latest.md`

### Ops docs
- `projects/cenoa-performance-marketing/analysis/automation-setup.md`
- `projects/cenoa-performance-marketing/analysis/sprint-1-retrospective.md`
