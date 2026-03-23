#!/usr/bin/env python3
"""Monday Telegram briefing generator.

Reads data.json (Cenoa Cortex KPI data) and prints a compact Telegram-formatted
briefing to stdout (< 4096 chars).

Usage:
    source ~/.openclaw/venv/bin/activate
    python3 scripts/monday_briefing_telegram.py [--data PATH]

Default data path: ../data.json (relative to this script's parent dir)
or set DATA_JSON_PATH env var.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None  # type: ignore


def _arrow(direction: str, delta: float) -> str:
    if direction == "up":
        return f"▲{abs(delta)}%"
    elif direction == "down":
        return f"▼{abs(delta)}%"
    return "→0%"


def _fmt_money(v: float) -> str:
    if v >= 1000:
        return f"${v:,.0f}"
    return f"${v:.2f}"


def _week_range_for_monday() -> str:
    """Return 'Mon DD – Sun DD, Mon YYYY' for the current week."""
    if ZoneInfo:
        now = datetime.now(ZoneInfo("Europe/Istanbul"))
    else:
        now = datetime.now()
    monday = now - timedelta(days=now.weekday())
    sunday = monday + timedelta(days=6)
    return f"{monday.strftime('%b %d')} – {sunday.strftime('%b %d, %Y')}"


def generate_briefing(data: dict) -> str:
    """Build the Telegram briefing string from data.json contents."""
    lines: list[str] = []

    # Header
    week_label = data.get("week", _week_range_for_monday())
    lines.append("📊 CENOA GROWTH ENGINE — Weekly Pulse")
    lines.append(f"Week of {week_label}")
    lines.append("")

    # ── KPI Snapshot ──
    kpis = data.get("kpis", {})
    lines.append("📈 KPI Snapshot")

    kpi_rows = [
        ("Installs", "installs"),
        ("Signups", "signups"),
        ("KYC Submits", "kycSubmits"),
        ("Virtual Accts", "virtualAccountOpened"),
        ("Deposits", "depositCompleted"),
        ("DAU (avg)", "dauAvg"),
    ]
    for label, key in kpi_rows:
        k = kpis.get(key, {})
        val = k.get("value", 0)
        val_str = f"{val:,.0f}" if isinstance(val, (int, float)) else str(val)
        delta = k.get("deltaPct", 0)
        direction = k.get("direction", "flat")
        lines.append(f"• {label}: {val_str} ({_arrow(direction, delta)})")

    # TRUE CAC (blended) — compute from campaign data
    campaigns = data.get("campaignPerformance", data.get("channelPerformance", []))
    total_spend = sum(c.get("spend", 0) for c in campaigns)
    total_actives = sum(c.get("newActives", c.get("new_active", 0)) for c in campaigns)
    true_cac = total_spend / total_actives if total_actives > 0 else 0

    bp = data.get("budgetPacing", {})
    budget_target = bp.get("target", 50000)
    mtd_spend = bp.get("mtd_spend", 0)
    pacing_pct = bp.get("pacing_pct", 0)

    lines.append(f"• TRUE CAC: {_fmt_money(true_cac)}")
    lines.append(f"• Budget: {_fmt_money(mtd_spend)} of {_fmt_money(budget_target)} ({pacing_pct}%)")
    lines.append("")

    # ── Top 3 Winners ──
    valid_campaigns = [c for c in campaigns if c.get("newActives", c.get("new_active", 0)) > 0]
    by_cac = sorted(valid_campaigns, key=lambda c: c.get("trueCAC") or c.get("true_cac") or 999)

    lines.append("🏆 Top 3 Winners")
    for c in by_cac[:3]:
        name = c.get("name", "?")
        cac = c.get("trueCAC", c.get("true_cac", 0))
        actives = c.get("newActives", c.get("new_active", 0))
        flag = c.get("countryFlag", "")
        lines.append(f"• {flag}{name} — ${cac:.0f} CAC, {actives} actives")
    lines.append("")

    # ── Top 3 to Kill ──
    by_cac_worst = sorted(valid_campaigns, key=lambda c: c.get("trueCAC") or c.get("true_cac") or 0, reverse=True)
    # Also include zero-active campaigns
    zero_active = [c for c in campaigns if c.get("newActives", c.get("new_active", 0)) == 0 and c.get("spend", 0) > 50]

    lines.append("🛑 Top 3 to Kill")
    kill_list: list[dict] = []
    for c in zero_active[:2]:
        kill_list.append(c)
    for c in by_cac_worst:
        if c not in kill_list and len(kill_list) < 3:
            kill_list.append(c)
    for c in kill_list[:3]:
        name = c.get("name", "?")
        cac = c.get("trueCAC", c.get("true_cac", 0))
        actives = c.get("newActives", c.get("new_active", 0))
        spend = c.get("spend", 0)
        flag = c.get("countryFlag", "")
        if actives == 0:
            reason = f"${spend:.0f} spent, 0 actives"
        else:
            reason = f"${cac:.0f} CAC"
        lines.append(f"• {flag}{name} — {reason}")
    lines.append("")

    # ── Budget Pacing ──
    lines.append("💰 Budget Pacing")
    days_elapsed = bp.get("days_elapsed", 0)
    days_total = bp.get("days_total", 31)
    target_pct = round((days_elapsed / days_total) * 100, 1) if days_total > 0 else 0
    lines.append(f"• Overall: {pacing_pct}% (target {target_pct}%)")

    # Country-level pacing
    country_spend = data.get("countrySpend", [])
    over = []
    under = []
    for cs in country_spend:
        cc = cs.get("country", "??")
        p = cs.get("pacing_pct", 0)
        if p > target_pct + 10:
            over.append(f"{cc} ({p}%)")
        elif p < target_pct - 10:
            under.append(f"{cc} ({p}%)")
    if over:
        lines.append(f"• Over: {', '.join(over)}")
    if under:
        lines.append(f"• Under: {', '.join(under)}")
    lines.append("")

    # ── #1 Priority ──
    lines.append("🎯 #1 Priority This Week")
    # Derive from data: if underspending, priority is scaling; if high CAC, cut
    status = bp.get("status", "")
    if "UNDER" in status.upper():
        lines.append("Scale winners to hit budget target — currently underspending.")
    elif "OVER" in status.upper():
        lines.append("Cut underperformers — overspending vs plan.")
    else:
        lines.append("Maintain current pacing and optimize CAC on bottom-3 channels.")
    lines.append("")

    # ── Attribution ──
    aq = data.get("attributionQuality", {})
    none_pct = aq.get("none_pct", 0)
    lines.append(f"⚠️ Attribution: {none_pct}% unattributed")

    # ── Updated ──
    updated = data.get("updated", "")
    if updated:
        lines.append(f"\n🕐 Data as of {updated}")

    text = "\n".join(lines)

    # Safety: Telegram message limit
    if len(text) > 4096:
        text = text[:4090] + "\n…"

    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Monday Telegram briefing")
    parser.add_argument(
        "--data",
        default=os.environ.get("DATA_JSON_PATH"),
        help="Path to data.json (default: ../data.json or DATA_JSON_PATH env)",
    )
    args = parser.parse_args()

    if args.data:
        data_path = Path(args.data).expanduser()
    else:
        # Default: projects/cenoa-growth-engine/data.json relative to repo root
        script_dir = Path(__file__).resolve().parent
        data_path = script_dir.parent / "data.json"

    if not data_path.exists():
        print(f"❌ data.json not found at {data_path}", file=sys.stderr)
        return 1

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    briefing = generate_briefing(data)
    print(briefing)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
