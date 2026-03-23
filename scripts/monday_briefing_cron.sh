#!/usr/bin/env bash
# monday_briefing_cron.sh — Weekly Monday briefing pipeline
#
# 1) Refreshes data.json via kpi_auto_update.py (Amplitude → Cortex)
# 2) Generates Telegram briefing text to stdout
#
# Usage (manual):
#   ./scripts/monday_briefing_cron.sh
#
# Wire to OpenClaw cron for Monday 10:00 TRT:
#   openclaw cron add \
#     --schedule "0 10 * * 1" \
#     --tz "Europe/Istanbul" \
#     --label "monday-briefing" \
#     --command "cd ~/.openclaw/workspace/projects/cenoa-growth-engine && ./scripts/monday_briefing_cron.sh"
#
# Or via launchd plist (see docs/monday-briefing-setup.md).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV="$HOME/.openclaw/venv/bin/activate"
CORTEX_DATA="$REPO_DIR/../data.json"

# Activate Python venv
# shellcheck disable=SC1090
source "$VENV"

# ── Step 1: Refresh KPI data ──
# Calculate date ranges: last full week (Mon-Sun)
TODAY=$(python3 -c "
from datetime import datetime, timedelta
try:
    from zoneinfo import ZoneInfo
    now = datetime.now(ZoneInfo('Europe/Istanbul'))
except:
    now = datetime.now()
# Last Monday = most recent Monday before today
days_since_monday = now.weekday()
if days_since_monday == 0:
    days_since_monday = 7  # If today is Monday, use last week
last_monday = now - timedelta(days=days_since_monday)
last_sunday = last_monday + timedelta(days=6)
prev_monday = last_monday - timedelta(days=7)
prev_sunday = last_monday - timedelta(days=1)
print(f'{last_monday:%Y-%m-%d} {last_sunday:%Y-%m-%d} {prev_monday:%Y-%m-%d} {prev_sunday:%Y-%m-%d}')
")

read -r START END PREV_START PREV_END <<< "$TODAY"

echo "📡 Refreshing KPIs: $START → $END (prev: $PREV_START → $PREV_END)" >&2

python3 "$SCRIPT_DIR/kpi_auto_update.py" \
    --start "$START" --end "$END" \
    --prev-start "$PREV_START" --prev-end "$PREV_END" \
    --output "$CORTEX_DATA" >&2 || {
    echo "⚠️  kpi_auto_update failed, using existing data.json" >&2
}

# ── Step 2: Generate briefing ──
python3 "$SCRIPT_DIR/monday_briefing_telegram.py" --data "$CORTEX_DATA"
