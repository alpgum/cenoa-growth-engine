#!/bin/bash
# Run 12-week backfill with 5s delays between weeks
set -e

cd "$(dirname "$0")/.."
source ~/.openclaw/venv/bin/activate

WEEKS=(
    "20251230 20260105"
    "20260106 20260112"
    "20260113 20260119"
    "20260120 20260126"
    "20260127 20260202"
    "20260203 20260209"
    "20260210 20260216"
    "20260217 20260223"
    "20260224 20260302"
    "20260303 20260309"
    "20260310 20260316"
    "20260317 20260323"
)

for i in "${!WEEKS[@]}"; do
    WEEK=(${WEEKS[$i]})
    START=${WEEK[0]}
    END=${WEEK[1]}
    WN=$((i + 1))
    echo ""
    echo "=== Week $WN: $START - $END ==="
    python3 scripts/weekly_backfill.py "$START" "$END"
    
    if [ $WN -lt 12 ]; then
        echo "  Waiting 5s before next week..."
        sleep 5
    fi
done

echo ""
echo "=== All 12 weeks complete ==="
