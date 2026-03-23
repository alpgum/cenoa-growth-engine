#!/usr/bin/env bash
# weekly_kpi_cron.sh — Weekly KPI auto-update for Cenoa Cortex
#
# Pulls last week's KPIs from Amplitude, writes data.json, commits, pushes,
# and deploys to Vercel.
#
# Designed to run every Monday morning via OpenClaw cron.
# Manual usage:
#   ./scripts/weekly_kpi_cron.sh              # auto-detect last Mon-Sun
#   ./scripts/weekly_kpi_cron.sh 2026-03-16   # override: week starting this Monday
#
set -euo pipefail

WORKSPACE="$HOME/.openclaw/workspace"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PERF_MARKETING="$(cd "$SCRIPT_DIR/.." && pwd)"
CORTEX_DIR="$WORKSPACE/projects/cenoa-growth-engine"
LOG_PREFIX="[KPI-cron]"

log() { echo "$LOG_PREFIX $(date '+%Y-%m-%d %H:%M:%S') $*"; }

# ── Activate venv ──────────────────────────────────────────────────────
source "$HOME/.openclaw/venv/bin/activate"

# ── Calculate date range ───────────────────────────────────────────────
# If an argument is given, treat it as the Monday of the target week.
# Otherwise, calculate last Monday-Sunday relative to today.
if [[ -n "${1:-}" ]]; then
    CURR_MON="$1"
else
    # Today's day-of-week (1=Mon … 7=Sun)
    DOW=$(date +%u)
    # Days since last Monday: if today is Monday (1), last Monday was 7 days ago
    DAYS_BACK=$(( DOW - 1 + 7 ))
    # On macOS (BSD date)
    if date -v-1d +%F &>/dev/null 2>&1; then
        CURR_MON=$(date -v-${DAYS_BACK}d +%F)
    else
        # GNU date
        CURR_MON=$(date -d "$DAYS_BACK days ago" +%F)
    fi
fi

# Compute Sunday = Monday + 6 days
if date -v-1d +%F &>/dev/null 2>&1; then
    CURR_SUN=$(date -j -f "%Y-%m-%d" "$CURR_MON" -v+6d +%F)
    PREV_MON=$(date -j -f "%Y-%m-%d" "$CURR_MON" -v-7d +%F)
    PREV_SUN=$(date -j -f "%Y-%m-%d" "$CURR_MON" -v-1d +%F)
else
    CURR_SUN=$(date -d "$CURR_MON + 6 days" +%F)
    PREV_MON=$(date -d "$CURR_MON - 7 days" +%F)
    PREV_SUN=$(date -d "$CURR_MON - 1 day" +%F)
fi

log "Current week: $CURR_MON → $CURR_SUN"
log "Previous week: $PREV_MON → $PREV_SUN"

# ── Run KPI update script ─────────────────────────────────────────────
log "Running kpi_auto_update.py …"
python3 "$SCRIPT_DIR/kpi_auto_update.py" \
    --start "$CURR_MON" \
    --end "$CURR_SUN" \
    --prev-start "$PREV_MON" \
    --prev-end "$PREV_SUN"

# ── Commit & push data.json ───────────────────────────────────────────
log "Committing data.json to cenoa-growth-engine …"
cd "$CORTEX_DIR"
git add data.json
if git diff --cached --quiet; then
    log "No changes in data.json — skipping commit."
else
    git commit -m "chore: update KPIs for $CURR_MON → $CURR_SUN"
    git push
    log "Pushed to remote."
fi

# ── Deploy to Vercel ──────────────────────────────────────────────────
log "Deploying to Vercel …"
npx vercel --prod --yes --force
log "✅ Done. Cortex updated for week $CURR_MON → $CURR_SUN"
