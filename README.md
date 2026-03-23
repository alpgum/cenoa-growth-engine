# Cenoa Growth Engine

Unified marketing ops platform — data pipeline + analytics + dashboard.

Merges **cenoa-cortex** (dashboard & reporting) and **cenoa-performance-marketing** (data pipeline & analysis) into a single repo.

## Structure

```
cenoa-growth-engine/
├── index.html              # Main dashboard (Vercel-deployed)
├── data.json               # Live KPI data (auto-updated by pipeline)
├── architecture.html       # System architecture diagram
├── country-*.html          # Country-specific dashboards (TR, PK, NG, EG)
├── sprint-*-report.html    # Sprint reports
├── scripts/                # Data pipeline & automation
│   ├── auto_deploy_cortex.sh   # Full pipeline runner
│   ├── kpi_auto_update.py      # Amplitude → data.json
│   ├── weekly_report.py        # Weekly report generator
│   ├── anomaly_detection.py    # KPI anomaly alerts
│   ├── budget_pacing.py        # Budget tracking
│   ├── campaign_health_check.py
│   ├── sheets_sync.py          # Google Sheets sync
│   └── ...
├── analysis/               # Marketing analysis & strategy docs
├── data/                   # Raw data snapshots (JSON, MD)
├── TASK_QUEUE*.md           # Sprint task queues
├── PRD.md                  # Product requirements
└── ROADMAP_100.md          # 100-day roadmap
```

## Deployment

Static HTML served via Vercel. Push to `main` triggers auto-deploy.

```bash
# Run full data pipeline + deploy
./scripts/auto_deploy_cortex.sh

# Manual Vercel deploy
vercel --prod --yes
```

## Data Pipeline

1. Pull KPIs from Amplitude, BigQuery, Google Sheets
2. Generate `data.json` at repo root
3. Run anomaly detection, budget pacing, campaign health
4. Generate weekly report
5. Commit & push → Vercel auto-deploys

## Previous Repos

- `alpgum/cenoa-cortex` — Dashboard (now merged here)
- `alpgum/cenoa-performance-marketing` — Data pipeline (now merged here)
