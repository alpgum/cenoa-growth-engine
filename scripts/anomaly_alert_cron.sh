#!/usr/bin/env bash
# anomaly_alert_cron.sh — Run anomaly detection and output Telegram alert if anomalies found.
# Designed for OpenClaw cron: stdout is piped to Telegram.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE="$(cd "$PROJECT_DIR/../.." && pwd)"
VENV="$HOME/.openclaw/venv"
ANOMALIES_JSON="$PROJECT_DIR/data/anomalies.json"

# Activate venv
source "$VENV/bin/activate"

# Run anomaly detection (suppress stdout — we build our own message)
python3 "$SCRIPT_DIR/anomaly_detection.py" \
  --input "$WORKSPACE/projects/cenoa-growth-engine/data.json" \
  --output "$ANOMALIES_JSON" \
  > /dev/null 2>&1

# Check if anomalies.json exists and has anomalies
if [ ! -f "$ANOMALIES_JSON" ]; then
  exit 0
fi

ANOMALY_COUNT=$(python3 -c "
import json, sys
with open('$ANOMALIES_JSON') as f:
    data = json.load(f)
print(len(data.get('anomalies', [])))
")

if [ "$ANOMALY_COUNT" -eq 0 ]; then
  # No anomalies — silent exit
  exit 0
fi

# Format Telegram-friendly alert
python3 -c "
import json

with open('$ANOMALIES_JSON') as f:
    data = json.load(f)

anomalies = data['anomalies']
week = data.get('week', 'unknown')
threshold = data.get('threshold', 20)
critical = [a for a in anomalies if a['severity'] == 'critical']
warnings = [a for a in anomalies if a['severity'] == 'warning']

lines = []
lines.append('🚨 <b>Anomaly Alert — {}</b>'.format(week))
lines.append('Threshold: ±{}%  |  {} critical, {} warning'.format(
    int(threshold), len(critical), len(warnings)))
lines.append('')

for a in anomalies:
    icon = '🔴' if a['severity'] == 'critical' else '🟡'
    arrow = '↓' if a['deltaPct'] < 0 else '↑'
    lines.append('{} <b>{}</b>: {} → {} ({}{:.1f}%)'.format(
        icon, a['kpi'], a['prev'], a['value'], arrow, abs(a['deltaPct'])))

lines.append('')
lines.append('📊 Run <code>weekly_report.py</code> for full breakdown.')

print('\n'.join(lines))
"
