#!/usr/bin/env bash
# dead_campaign_sweep_cron.sh — Run campaign health check and output Telegram alert if DEAD/BLEEDING/FRAUD found.
# Designed for OpenClaw cron: stdout is piped to Telegram. Silent on healthy runs.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV="$HOME/.openclaw/venv"
HEALTH_JSON="$PROJECT_DIR/data/campaign-health.json"

# Activate venv
source "$VENV/bin/activate"

# Run health check (suppress stdout — we build our own message)
# Remove previous output to avoid sending stale alerts if the run fails.
rm -f "$HEALTH_JSON"
python3 "$SCRIPT_DIR/campaign_health_check.py" > /dev/null 2>&1

# If output missing, exit silently (avoid noise)
if [ ! -f "$HEALTH_JSON" ]; then
  exit 0
fi

# Build Telegram-friendly HTML alert (stdout) only when problems exist
HEALTH_JSON="$HEALTH_JSON" python3 - << 'PY'
import json
import os
import sys
from html import escape
from pathlib import Path

health_path_str = os.environ.get("HEALTH_JSON", "").strip()
health_path = Path(health_path_str) if health_path_str else None

try:
    if not health_path:
        raise RuntimeError("HEALTH_JSON env var not set")
    data = json.loads(health_path.read_text(encoding="utf-8"))
except Exception as e:
    # Keep stdout silent; cron can still capture stderr if needed
    print(f"Failed to read campaign health JSON: {e}", file=sys.stderr)
    sys.exit(1)

FLAGGED = {"DEAD", "BLEEDING", "FRAUD"}


def flagged_items(section: str):
    items = []
    for name, r in (data.get(section) or {}).items():
        status = (r.get("status") or "").upper()
        if status in FLAGGED:
            items.append((name, r))
    return items

channels = flagged_items("channels")
campaigns = flagged_items("campaigns")
sources = flagged_items("attribution_sources")

if not (channels or campaigns or sources):
    sys.exit(0)  # silent

# Sort + cap to keep Telegram message readable

def sort_key(item):
    name, r = item
    return (0 if r.get("status") == "DEAD" else 1 if r.get("status") == "FRAUD" else 2, -(r.get("installs") or 0), name)

channels = sorted(channels, key=sort_key)
campaigns = sorted(campaigns, key=sort_key)
sources = sorted(sources, key=sort_key)

MAX_PER_SECTION = 12


def fmt_status(s: str) -> str:
    s = (s or "").upper()
    icon = {"DEAD": "💀", "BLEEDING": "🩸", "FRAUD": "🚨"}.get(s, "⚠️")
    return f"{icon} <b>{s}</b>"


def bullet(name: str, r: dict) -> str:
    status = fmt_status(r.get("status"))
    reason = escape(str(r.get("reason") or ""))
    return f"• <code>{escape(name)}</code> — {status}: {reason}"

lines = []
lines.append("🚨 <b>Campaign Health Alert</b>")
lines.append(f"<i>Generated:</i> <code>{escape(str(data.get('generated_at','unknown')))}</code>")
if "avg_cpi" in data:
    lines.append(f"<i>Avg CPI (paid):</i> <code>${data['avg_cpi']}</code>")
lines.append("")


def add_section(title: str, items: list[tuple[str, dict]]):
    if not items:
        return
    lines.append(f"<b>{escape(title)}</b>")
    for name, r in items[:MAX_PER_SECTION]:
        lines.append(bullet(name, r))
    if len(items) > MAX_PER_SECTION:
        lines.append(f"• <i>…and {len(items) - MAX_PER_SECTION} more</i>")
    lines.append("")

add_section("Channels", channels)
add_section("Campaigns", campaigns)
add_section("Attribution Sources", sources)

lines.append("Next: check <code>campaign_health_check.py</code> output in <code>data/campaign-health.json</code>.")

print("\n".join(lines).rstrip())
PY