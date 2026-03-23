#!/usr/bin/env bash
# weekly_report_cron.sh — Generate & output the weekly performance report
#
# Designed to run every Monday at 10:00 TRT via OpenClaw cron,
# 1 hour after weekly_kpi_cron.sh (09:00) so data.json is fresh.
#
# Outputs the Telegram-formatted report to stdout for OpenClaw to deliver.
# Also saves a copy to data/weekly-report-latest.md.
#
# Manual usage:
#   cd projects/cenoa-growth-engine && ./scripts/weekly_report_cron.sh
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_PREFIX="[Report-cron]"

log() { echo "$LOG_PREFIX $(date '+%Y-%m-%d %H:%M:%S') $*" >&2; }

# ── Activate venv ──────────────────────────────────────────────────────
source "$HOME/.openclaw/venv/bin/activate"

# ── Verify dependencies ───────────────────────────────────────────────
CORTEX_DATA="$HOME/.openclaw/workspace/projects/cenoa-growth-engine/data.json"
if [[ ! -f "$CORTEX_DATA" ]]; then
    log "ERROR: $CORTEX_DATA not found. Has weekly_kpi_cron.sh run?"
    exit 1
fi

# ── Generate weekly actions (best-effort; keep stdout clean) ───────────
log "Running weekly_actions.py …"
if ! python3 "$SCRIPT_DIR/weekly_actions.py" 1>&2; then
    log "WARN: weekly_actions.py failed; continuing with report (fallback actions)."
fi

# ── Generate report ───────────────────────────────────────────────────
log "Running weekly_report.py …"
python3 "$SCRIPT_DIR/weekly_report.py"
EXIT_CODE=$?

if [[ $EXIT_CODE -ne 0 ]]; then
    log "ERROR: weekly_report.py exited with code $EXIT_CODE"
    exit $EXIT_CODE
fi

log "✅ Weekly report generated."
