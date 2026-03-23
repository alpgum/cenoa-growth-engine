#!/usr/bin/env bash
# e2e_test.sh — End-to-end pipeline test for Cenoa Performance Marketing
#
# Runs the full weekly pipeline in sequence, then verifies all outputs
# exist, are recent, and contain valid data.
#
# Usage:
#   cd projects/cenoa-growth-engine && ./scripts/e2e_test.sh
#
# Exit code: 0 if all checks pass, 1 if any fail.
#
set -uo pipefail

# ── Paths ──────────────────────────────────────────────────────────────
WORKSPACE="$HOME/.openclaw/workspace"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PERF_MARKETING="$(cd "$SCRIPT_DIR/.." && pwd)"
CORTEX_DIR="$WORKSPACE/projects/cenoa-growth-engine"
DATA_DIR="$PERF_MARKETING/data"

CORTEX_DATA="$CORTEX_DIR/data.json"

LOG_PREFIX="[E2E-test]"
FAILURES=0
TOTAL=0

# ── Helpers ────────────────────────────────────────────────────────────
log() { echo "$LOG_PREFIX $(date '+%Y-%m-%d %H:%M:%S') $*" >&2; }

pass() {
    TOTAL=$((TOTAL + 1))
    echo "✅ $*"
}

fail() {
    TOTAL=$((TOTAL + 1))
    FAILURES=$((FAILURES + 1))
    echo "❌ $*"
}

# ── 1) Source credentials ──────────────────────────────────────────────
log "Sourcing credentials …"

# Amplitude
if [[ -f "$HOME/.openclaw/credentials/amplitude.env" ]]; then
    set -a
    source "$HOME/.openclaw/credentials/amplitude.env"
    set +a
    log "  Amplitude credentials loaded."
else
    log "  WARN: amplitude.env not found."
fi

# BigQuery / GA4 / Sheets service account
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.openclaw/credentials/cenoa-marketingdatawarehouse-82b8600e66d6.json"
if [[ -f "$GOOGLE_APPLICATION_CREDENTIALS" ]]; then
    log "  Google credentials loaded."
else
    log "  WARN: Google service account JSON not found."
fi

# fal.ai (if needed)
if [[ -f "$HOME/.openclaw/credentials/fal.env" ]]; then
    set -a
    source "$HOME/.openclaw/credentials/fal.env"
    set +a
fi

# ── 2) Activate venv ──────────────────────────────────────────────────
source "$HOME/.openclaw/venv/bin/activate"
log "Python venv activated."

# ── 3) Run pipeline steps ─────────────────────────────────────────────
# Each step: run, capture exit code, report result.

PIPELINE_STEPS=(
    "kpi_auto_update.py"
    "anomaly_detection.py"
    "campaign_health_check.py"
    "budget_pacing.py"
    "data_quality_monitor.py"
    "weekly_actions.py"
    "weekly_report.py"
)

declare -A STEP_EXIT

for step in "${PIPELINE_STEPS[@]}"; do
    log "Running $step …"
    STEP_LOG=$(python3 "$SCRIPT_DIR/$step" 2>&1) || true
    STEP_EXIT[$step]=$?
    if [[ ${STEP_EXIT[$step]} -ne 0 ]]; then
        log "  $step exited with code ${STEP_EXIT[$step]}"
        log "  Output (last 10 lines):"
        echo "$STEP_LOG" | tail -10 | while read -r line; do log "    $line"; done
    else
        log "  $step — OK"
    fi
done

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  CENOA PERFORMANCE MARKETING — E2E PIPELINE TEST RESULTS"
echo "════════════════════════════════════════════════════════════════"
echo ""

# ── 4) Verify pipeline step exit codes ─────────────────────────────────
for step in "${PIPELINE_STEPS[@]}"; do
    if [[ ${STEP_EXIT[$step]} -eq 0 ]]; then
        pass "$step — OK (exit 0)"
    else
        fail "$step — FAILED (exit code ${STEP_EXIT[$step]})"
    fi
done

echo ""

# ── 5) Verify output files exist and are recent (< 5 min old) ─────────
echo "── Output file checks ──────────────────────────────────────────"
echo ""

NOW_EPOCH=$(date +%s)
MAX_AGE_SEC=300  # 5 minutes

check_file_recent() {
    local filepath="$1"
    local label="$2"

    if [[ ! -f "$filepath" ]]; then
        fail "$label — MISSING ($filepath)"
        return 1
    fi

    local file_epoch
    file_epoch=$(stat -f %m "$filepath" 2>/dev/null || stat -c %Y "$filepath" 2>/dev/null)
    local age=$((NOW_EPOCH - file_epoch))

    if [[ $age -gt $MAX_AGE_SEC ]]; then
        fail "$label — STALE (${age}s old, max ${MAX_AGE_SEC}s)"
        return 1
    fi

    pass "$label — exists & fresh (${age}s old)"
    return 0
}

check_file_recent "$CORTEX_DATA"                       "data.json (cortex)"
check_file_recent "$DATA_DIR/anomalies.json"           "anomalies.json"
check_file_recent "$DATA_DIR/campaign-health.json"     "campaign-health.json"
check_file_recent "$DATA_DIR/budget-pacing.json"       "budget-pacing.json"
check_file_recent "$DATA_DIR/data-quality.json"        "data-quality.json"
check_file_recent "$DATA_DIR/weekly-actions.json"      "weekly-actions.json"
check_file_recent "$DATA_DIR/weekly-report-latest.md"  "weekly-report-latest.md"

echo ""

# ── 6) Validate data.json content ─────────────────────────────────────
echo "── data.json content validation ──────────────────────────────"
echo ""

if [[ -f "$CORTEX_DATA" ]]; then
    # Check lastUpdated within 5 min
    LAST_UPDATED=$(python3 -c "
import json, sys
from datetime import datetime, timezone, timedelta
with open('$CORTEX_DATA') as f:
    d = json.load(f)
lu = d.get('lastUpdated', '')
if not lu:
    print('MISSING')
    sys.exit(1)
dt = datetime.fromisoformat(lu.replace('Z', '+00:00'))
age = (datetime.now(timezone.utc) - dt).total_seconds()
if age > 300:
    print(f'STALE:{int(age)}s')
    sys.exit(1)
print(f'OK:{int(age)}s')
" 2>&1) || true

    case "$LAST_UPDATED" in
        OK:*)
            pass "data.json lastUpdated — ${LAST_UPDATED#OK:} ago"
            ;;
        STALE:*)
            fail "data.json lastUpdated — ${LAST_UPDATED#STALE:} ago (max 300s)"
            ;;
        *)
            fail "data.json lastUpdated — $LAST_UPDATED"
            ;;
    esac

    # Check kpis array length >= 8
    KPI_COUNT=$(python3 -c "
import json
with open('$CORTEX_DATA') as f:
    d = json.load(f)
kpis = d.get('kpis', [])
print(len(kpis))
" 2>&1) || KPI_COUNT="0"

    if [[ "$KPI_COUNT" -ge 8 ]] 2>/dev/null; then
        pass "data.json kpis — $KPI_COUNT items (≥8 required)"
    else
        fail "data.json kpis — $KPI_COUNT items (≥8 required)"
    fi

    # Check channelPerformance length >= 3
    CHAN_COUNT=$(python3 -c "
import json
with open('$CORTEX_DATA') as f:
    d = json.load(f)
cp = d.get('channelPerformance', [])
print(len(cp))
" 2>&1) || CHAN_COUNT="0"

    if [[ "$CHAN_COUNT" -ge 3 ]] 2>/dev/null; then
        pass "data.json channelPerformance — $CHAN_COUNT items (≥3 required)"
    else
        fail "data.json channelPerformance — $CHAN_COUNT items (≥3 required)"
    fi

    # Check kycByCountry has 4 items
    KYC_COUNT=$(python3 -c "
import json
with open('$CORTEX_DATA') as f:
    d = json.load(f)
kyc = d.get('kycByCountry', [])
print(len(kyc))
" 2>&1) || KYC_COUNT="0"

    if [[ "$KYC_COUNT" -ge 4 ]] 2>/dev/null; then
        pass "data.json kycByCountry — $KYC_COUNT items (≥4 required)"
    else
        fail "data.json kycByCountry — $KYC_COUNT items (need 4)"
    fi

    # Check platformSplit has iOS + Android
    PLATFORM_CHECK=$(python3 -c "
import json
with open('$CORTEX_DATA') as f:
    d = json.load(f)
ps = d.get('platformSplit', [])
names = [p.get('platform', '').lower() for p in ps]
has_ios = 'ios' in names
has_android = 'android' in names
if has_ios and has_android:
    print('OK')
else:
    missing = []
    if not has_ios: missing.append('iOS')
    if not has_android: missing.append('Android')
    print('MISSING:' + ','.join(missing))
" 2>&1) || PLATFORM_CHECK="ERROR"

    if [[ "$PLATFORM_CHECK" == "OK" ]]; then
        pass "data.json platformSplit — iOS + Android present"
    else
        fail "data.json platformSplit — ${PLATFORM_CHECK#MISSING:} missing"
    fi
else
    fail "data.json — file not found, skipping content checks"
fi

echo ""

# ── 7) Extra: count anomalies found ───────────────────────────────────
if [[ -f "$DATA_DIR/anomalies.json" ]]; then
    ANOMALY_COUNT=$(python3 -c "
import json
with open('$DATA_DIR/anomalies.json') as f:
    d = json.load(f)
anomalies = d.get('anomalies', d if isinstance(d, list) else [])
print(len(anomalies))
" 2>&1) || ANOMALY_COUNT="?"
    echo "ℹ️  Anomalies detected: $ANOMALY_COUNT"
fi

if [[ -f "$DATA_DIR/campaign-health.json" ]]; then
    CAMPAIGN_COUNT=$(python3 -c "
import json
with open('$DATA_DIR/campaign-health.json') as f:
    d = json.load(f)
campaigns = d.get('campaigns', d if isinstance(d, list) else [])
print(len(campaigns))
" 2>&1) || CAMPAIGN_COUNT="?"
    echo "ℹ️  Campaigns checked: $CAMPAIGN_COUNT"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
PASSED=$((TOTAL - FAILURES))
echo "  Result: $PASSED/$TOTAL checks passed"
if [[ $FAILURES -eq 0 ]]; then
    echo "  🎉 ALL CHECKS PASSED"
else
    echo "  ⚠️  $FAILURES CHECK(S) FAILED"
fi
echo "════════════════════════════════════════════════════════════════"

exit $( [[ $FAILURES -eq 0 ]] && echo 0 || echo 1 )
