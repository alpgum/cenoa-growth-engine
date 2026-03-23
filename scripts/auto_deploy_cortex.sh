#!/bin/bash
set -e

# Cenoa Growth Engine — Unified Pipeline
# Runs data pulls, analysis, KPI updates, then deploys dashboard via Vercel.

# Load credentials
export $(grep -v '^#' ~/.openclaw/credentials/amplitude.env | xargs)
export GOOGLE_APPLICATION_CREDENTIALS=~/.openclaw/credentials/cenoa-marketingdatawarehouse-82b8600e66d6.json

WORKSPACE=~/.openclaw/workspace
ENGINE_DIR=$WORKSPACE/projects/cenoa-growth-engine

# Activate venv
source ~/.openclaw/venv/bin/activate

# 0) Sync Google Sheets (CaC Analysis, Budget Tracking, Trafik Canavarı)
echo "📋 Syncing Google Sheets..."
python3 $ENGINE_DIR/scripts/sheets_sync.py || true

# 1) Run KPI update (generates data.json at repo root)
echo "📊 Running KPI auto-update..."
python3 $ENGINE_DIR/scripts/kpi_auto_update.py

# 2) Run anomaly detection
echo "🚨 Running anomaly detection..."
python3 $ENGINE_DIR/scripts/anomaly_detection.py || true

# 3) Campaign health
echo "🏥 Running campaign health check..."
python3 $ENGINE_DIR/scripts/campaign_health_check.py || true

# 4) Budget pacing
echo "💰 Running budget pacing..."
python3 $ENGINE_DIR/scripts/budget_pacing.py || true

# 5) Data quality
echo "🔍 Running data quality monitor..."
python3 $ENGINE_DIR/scripts/data_quality_monitor.py || true

# 6) Weekly actions
echo "🎯 Generating weekly actions..."
python3 $ENGINE_DIR/scripts/weekly_actions.py || true

# 7) Weekly report
echo "📝 Generating weekly report..."
python3 $ENGINE_DIR/scripts/weekly_report.py

# 8) Commit & push
echo "📦 Committing and deploying..."
cd $ENGINE_DIR && git add -A && git commit -m "Data refresh $(date +%Y-%m-%d)" && git push || true

echo ""
echo "✅ Pipeline complete! Vercel will auto-deploy."
echo "🌐 Dashboard live at Vercel URL"
