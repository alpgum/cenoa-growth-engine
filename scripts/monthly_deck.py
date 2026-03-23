#!/usr/bin/env python3
"""Monthly executive deck generator (best-effort, file-first).

Goal
----
Generate a monthly executive deck *spec* (JSON) + a markdown narrative, using
already-exported artifacts in this repo when possible.

Outputs
-------
- projects/cenoa-growth-engine/data/monthly-deck.json
- projects/cenoa-growth-engine/analysis/monthly-deck.md

Notes
-----
- This script is intentionally "offline by default" (no API calls) to keep the
  automation reliable.
- If you want truly month-accurate product KPIs (installs/signups/KYC/etc), add
  a live pull step (Amplitude/GA4) and write into data/ first; this deck
  generator will pick up the freshest files automatically.

Run
---
  source ~/.openclaw/venv/bin/activate
  python3 projects/cenoa-growth-engine/scripts/monthly_deck.py --month 2026-02

If --month is omitted, defaults to the *previous* calendar month in Europe/Istanbul.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

try:
    from zoneinfo import ZoneInfo  # py3.9+
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore


# ──────────────────────────────────────────────────────────────────────────────
# Helpers


def _now_trt() -> datetime:
    if ZoneInfo is not None:
        return datetime.now(ZoneInfo("Europe/Istanbul"))
    return datetime.now()


def _previous_month_yyyy_mm(now: datetime) -> str:
    first = now.replace(day=1)
    prev_last = first - timedelta(days=1)
    return prev_last.strftime("%Y-%m")


def _month_label(yyyy_mm: str) -> str:
    y, m = [int(x) for x in yyyy_mm.split("-", 1)]
    dt = date(y, m, 1)
    return dt.strftime("%B %Y")


def _safe_read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _safe_read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return None


def _pct_delta(curr: float | None, prev: float | None) -> float | None:
    if curr is None or prev is None:
        return None
    if prev == 0:
        return 100.0 if curr > 0 else 0.0
    return round(((curr - prev) / prev) * 100.0, 1)


def _fmt_int(x: Any) -> str:
    try:
        return f"{int(round(float(x))):,}"
    except Exception:
        return "—"


def _fmt_usd(x: Any) -> str:
    try:
        return f"${float(x):,.0f}"
    except Exception:
        return "—"


def _fmt_num(x: Any, digits: int = 1) -> str:
    try:
        return f"{float(x):,.{digits}f}"
    except Exception:
        return "—"


def _fmt_pct(x: Any) -> str:
    try:
        return f"{float(x):.1f}%"
    except Exception:
        return "—"


def _md_table(headers: list[str], rows: list[list[str]]) -> str:
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("|" + "|".join(["---"] * len(headers)) + "|")
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out)


def _find_latest(paths: list[Path]) -> Path | None:
    if not paths:
        return None
    paths = [p for p in paths if p.exists()]
    if not paths:
        return None
    return sorted(paths, key=lambda p: p.stat().st_mtime, reverse=True)[0]


# ──────────────────────────────────────────────────────────────────────────────
# Collectors


@dataclass
class Inputs:
    project_dir: Path
    data_dir: Path
    analysis_dir: Path

    blended_cac: dict[str, Any] | None = None
    sheets_cac: dict[str, Any] | None = None
    budget_pacing: dict[str, Any] | None = None
    channel_cac: dict[str, Any] | None = None
    budget_efficiency: dict[str, Any] | None = None
    weekly_actions: dict[str, Any] | None = None

    weekly_report_md: str | None = None
    funnel_summary_md: str | None = None


def collect_inputs(project_dir: Path) -> Inputs:
    data_dir = project_dir / "data"
    analysis_dir = project_dir / "analysis"

    inp = Inputs(project_dir=project_dir, data_dir=data_dir, analysis_dir=analysis_dir)

    # JSON data
    inp.blended_cac = _safe_read_json(data_dir / "blended-cac.json")
    inp.sheets_cac = _safe_read_json(data_dir / "sheets-cac-analysis.json")
    inp.budget_pacing = _safe_read_json(data_dir / "budget-pacing.json")
    inp.channel_cac = _safe_read_json(data_dir / "channel-cac.json")
    inp.budget_efficiency = _safe_read_json(data_dir / "budget-efficiency.json")
    inp.weekly_actions = _safe_read_json(data_dir / "weekly-actions.json")

    # Markdown narratives (latest)
    inp.weekly_report_md = _safe_read_text(data_dir / "weekly-report-latest.md")
    inp.funnel_summary_md = _safe_read_text(analysis_dir / "funnel-summary.md")

    return inp


def _extract_exec_bullets_from_funnel_summary(md: str | None) -> list[str]:
    if not md:
        return []
    # Grab bullets under "## 1. Executive Summary" until the next header.
    m = re.search(r"## 1\. Executive Summary\n\n(?P<body>.*?)(\n\n## |\Z)", md, flags=re.S)
    if not m:
        return []
    body = m.group("body")
    bullets = []
    for line in body.splitlines():
        line = line.strip()
        # format in file is numbered list "1."...
        if re.match(r"^\d+\.\s+", line):
            bullets.append(re.sub(r"^\d+\.\s+", "", line))
    return bullets[:6]


def _extract_kpi_lines_from_weekly_report(md: str | None) -> list[str]:
    if not md:
        return []
    # first block has emoji KPI lines; pull up to the blank line after them.
    lines = md.splitlines()
    kpis: list[str] = []
    for line in lines:
        line = line.strip()
        if not line:
            if kpis:
                break
            continue
        if any(line.startswith(prefix) for prefix in ["📲", "📝", "✅", "💳", "👤"]):
            kpis.append(line)
    return kpis


def _get_blended_month(blended: dict[str, Any] | None, yyyy_mm: str) -> dict[str, Any] | None:
    if not blended:
        return None

    # Prefer monthly_turkey_last6_attr_consistent
    mt = blended.get("monthly_turkey_last6_attr_consistent", {}).get("months")
    if isinstance(mt, dict) and yyyy_mm in mt:
        return mt[yyyy_mm]

    # Fallback: other objects that carry months map
    for key in [
        "monthly_turkey_jan_feb_finance_spend_mixed_denominators",
    ]:
        months = blended.get(key, {}).get("months")
        if isinstance(months, dict) and yyyy_mm in months:
            return months[yyyy_mm]

    return None


def _get_sheets_turkey_month(sheets: dict[str, Any] | None, yyyy_mm: str) -> dict[str, Any] | None:
    if not sheets:
        return None
    y, m = yyyy_mm.split("-", 1)
    m_int = int(m)

    sum_tr = sheets.get("sum_turkey", {})
    months_key = f"months_{y}"
    months = sum_tr.get(months_key)
    if isinstance(months, dict):
        obj = months.get(str(m_int))
        if isinstance(obj, dict):
            return obj
    return None


def _get_sheets_turkey_channel_month(sheets: dict[str, Any] | None, yyyy_mm: str) -> dict[str, Any] | None:
    """Try to find a TR channel breakdown object for the month.

    The exported sheet structure has ad-hoc keys (e.g. "jan_2026", "feb_2026_1_7").
    We match best-effort.
    """
    if not sheets:
        return None
    y, m = yyyy_mm.split("-", 1)
    month_name = date(int(y), int(m), 1).strftime("%b").lower()  # jan/feb/...

    ch = sheets.get("channels_2025_turkey", {})
    # common keys:
    candidates = []
    for k, v in ch.items():
        if not isinstance(v, dict):
            continue
        k_norm = k.lower()
        if y in k_norm and month_name in k_norm:
            candidates.append((k, v))
        # also allow exact like jan_2026
        if k_norm.startswith(f"{month_name}_{y}"):
            candidates.append((k, v))
    if not candidates:
        return None
    # Prefer exact "{mon}_{year}" if present
    for k, v in candidates:
        if k.lower() == f"{month_name}_{y}":
            return v
    return candidates[0][1]


def _market_plan_paths(analysis_dir: Path) -> list[Path]:
    names = [
        "turkey-90d-plan.md",
        "nigeria-growth-plan.md",
        "egypt-scaling-plan.md",
        "pakistan-prelaunch-plan.md",
        "multi-market-expansion-playbook.md",
    ]
    out: list[Path] = []
    for n in names:
        p = analysis_dir / n
        if p.exists():
            out.append(p)
    return out


# ──────────────────────────────────────────────────────────────────────────────
# Deck builder


def build_deck(yyyy_mm: str, inp: Inputs) -> tuple[dict[str, Any], str]:
    now = _now_trt()
    prev_month = (date(int(yyyy_mm[:4]), int(yyyy_mm[5:]), 1) - timedelta(days=1)).strftime("%Y-%m")

    month_label = _month_label(yyyy_mm)
    prev_label = _month_label(prev_month)

    exec_bullets = _extract_exec_bullets_from_funnel_summary(inp.funnel_summary_md)
    kpi_lines_week = _extract_kpi_lines_from_weekly_report(inp.weekly_report_md)

    # Monthly CAC (Turkey) from blended-cac.json or sheets
    m_curr = _get_blended_month(inp.blended_cac, yyyy_mm)
    m_prev = _get_blended_month(inp.blended_cac, prev_month)

    s_curr = _get_sheets_turkey_month(inp.sheets_cac, yyyy_mm)
    s_prev = _get_sheets_turkey_month(inp.sheets_cac, prev_month)

    # Prefer blended if present; else sheets.
    def pick_month(curr: dict[str, Any] | None, sheets_obj: dict[str, Any] | None) -> dict[str, Any] | None:
        return curr or sheets_obj

    month_curr = pick_month(m_curr, s_curr)
    month_prev = pick_month(m_prev, s_prev)

    # Global spend if present
    global_spend = None
    if inp.blended_cac and isinstance(inp.blended_cac.get("realized_spend_global_budget_tracking"), dict):
        global_spend = inp.blended_cac["realized_spend_global_budget_tracking"].get(yyyy_mm)

    # Budget pacing (usually current month)
    pacing = inp.budget_pacing or {}

    # Channel performance
    channel_week = inp.channel_cac or {}
    efficiency = inp.budget_efficiency or {}

    # Actions
    actions = []
    if inp.weekly_actions and isinstance(inp.weekly_actions.get("actions"), list):
        actions = inp.weekly_actions["actions"]

    top_actions = []
    for a in actions[:10]:
        top_actions.append(
            {
                "severity": a.get("severity"),
                "owner": a.get("owner"),
                "title": a.get("title"),
                "why": a.get("why"),
                "expectedImpact": a.get("expectedImpact"),
            }
        )

    # Market plans
    plan_paths = _market_plan_paths(inp.analysis_dir)
    plans = []
    for p in plan_paths:
        plans.append({"title": p.stem.replace("-", " ").title(), "path": str(p.relative_to(inp.project_dir))})

    # ── KPI table (Turkey monthly) ───────────────────────────────────────────
    kpi_rows: list[list[str]] = []

    def v(obj: dict[str, Any] | None, key: str) -> Any:
        return (obj or {}).get(key)

    # Attempt to normalize between blended-cac keys and sheet keys.
    # blended: spend_usd, signups, virtual_accounts, new_active, cac_signup, cac_virtual_account, cac_new_active
    # sheets: cost, sign_up, virt_acc, new_active, cost_per_sign, cost_per_virt, cost_per_active
    def get_metric(obj: dict[str, Any] | None, metric: str) -> float | None:
        if not obj:
            return None
        # blended-cac
        if metric == "spend_usd":
            if "spend_usd" in obj:
                return float(obj["spend_usd"])
            if "cost" in obj:
                return float(obj["cost"])
        if metric == "signups":
            if "signups" in obj:
                return float(obj["signups"])
            if "sign_up" in obj:
                return float(obj["sign_up"])
        if metric == "virtual_accounts":
            if "virtual_accounts" in obj:
                return float(obj["virtual_accounts"])
            if "virt_acc" in obj:
                return float(obj["virt_acc"])
        if metric == "new_active":
            if "new_active" in obj and obj["new_active"] is not None:
                return float(obj["new_active"])
        if metric == "cac_signup":
            if "cac_signup" in obj and obj["cac_signup"] is not None:
                return float(obj["cac_signup"])
            if "cost_per_sign" in obj and obj["cost_per_sign"] is not None:
                return float(obj["cost_per_sign"])
        if metric == "cac_virtual_account":
            if "cac_virtual_account" in obj and obj["cac_virtual_account"] is not None:
                return float(obj["cac_virtual_account"])
            if "cost_per_virt" in obj and obj["cost_per_virt"] is not None:
                return float(obj["cost_per_virt"])
        if metric == "cac_new_active":
            if "cac_new_active" in obj and obj["cac_new_active"] is not None:
                return float(obj["cac_new_active"])
            if "cost_per_active" in obj and obj["cost_per_active"] is not None:
                return float(obj["cost_per_active"])
        return None

    metrics = [
        ("Spend (TR)", "spend_usd", _fmt_usd),
        ("Signups (TR)", "signups", _fmt_int),
        ("Virtual accounts (TR)", "virtual_accounts", _fmt_int),
        ("New active (TR)", "new_active", _fmt_int),
        ("CAC / Signup (TR)", "cac_signup", lambda x: f"${float(x):,.2f}" if x is not None else "—"),
        ("CAC / Virtual acct (TR)", "cac_virtual_account", lambda x: f"${float(x):,.2f}" if x is not None else "—"),
        ("CAC / New active (TR)", "cac_new_active", lambda x: f"${float(x):,.2f}" if x is not None else "—"),
    ]

    for label, key, fmt in metrics:
        curr = get_metric(month_curr, key)
        prev = get_metric(month_prev, key)
        d = _pct_delta(curr, prev)
        kpi_rows.append([
            label,
            fmt(curr),
            fmt(prev),
            _fmt_pct(d) if d is not None else "—",
        ])

    # ── Funnel + KYC (use known figures from funnel-summary if present) ─────
    funnel_callouts: list[str] = []
    if inp.funnel_summary_md:
        # Pull a couple of high-signal lines (KYC + attribution)
        # Shown→Submit rate line exists in summary.
        if "KYC Shown → Submit" in inp.funnel_summary_md:
            funnel_callouts.append("KYC is the main bottleneck (shown→submit is low; non-TR markets are hard-blocked).")
        if "61% of withdrawals" in inp.funnel_summary_md:
            funnel_callouts.append("Attribution gap: majority of withdrawals are unattributed (“(none)”).")

    # ── Attribution caveats (explicit slide) ────────────────────────────────
    attribution_caveats = [
        "Spend sources are mixed (finance budget tracking vs marketing-attributed spend).",
        "Deposits/withdrawals are cross-cohort in current reporting (include returning users).",
        "Large attribution loss in AppsFlyer/Amplitude join; treat channel ROI as directional.",
    ]

    # ── Deck spec ───────────────────────────────────────────────────────────
    deck: dict[str, Any] = {
        "meta": {
            "generated_at": now.isoformat(timespec="seconds"),
            "month": yyyy_mm,
            "month_label": month_label,
            "sources": {
                "blended_cac": "data/blended-cac.json" if inp.blended_cac else None,
                "sheets_cac": "data/sheets-cac-analysis.json" if inp.sheets_cac else None,
                "budget_pacing": "data/budget-pacing.json" if inp.budget_pacing else None,
                "channel_cac": "data/channel-cac.json" if inp.channel_cac else None,
                "budget_efficiency": "data/budget-efficiency.json" if inp.budget_efficiency else None,
                "weekly_actions": "data/weekly-actions.json" if inp.weekly_actions else None,
                "weekly_report": "data/weekly-report-latest.md" if inp.weekly_report_md else None,
                "funnel_summary": "analysis/funnel-summary.md" if inp.funnel_summary_md else None,
            },
            "data_quality_notes": [
                "This is file-first best-effort. Some values are weekly snapshots if monthly aggregates were not available.",
                "To improve: export month-level product KPIs (Amplitude) into data/ and rerun.",
            ],
        },
        "deck": {
            "title": f"Cenoa Performance Marketing — Monthly Executive Update ({month_label})",
            "audience": "Exec",
            "sections": [
                {
                    "title": "Exec summary",
                    "slides": [
                        {
                            "title": "This month at a glance",
                            "type": "bullets",
                            "bullets": exec_bullets or [
                                "KYC remains the #1 constraint; non-TR markets show hard blocks.",
                                "Channel quality varies; reallocation can lift CAC quickly.",
                            ],
                        },
                        {
                            "title": "Most recent KPI pulse (weekly snapshot)",
                            "type": "callouts",
                            "callouts": kpi_lines_week,
                            "note": "Weekly snapshot included because month-aggregate product KPIs may not be available offline.",
                        },
                    ],
                },
                {
                    "title": "KPI snapshot + deltas",
                    "slides": [
                        {
                            "title": f"Turkey monthly unit economics — {month_label} vs {prev_label}",
                            "type": "table",
                            "table": {
                                "headers": ["Metric", month_label, prev_label, "Δ"],
                                "rows": kpi_rows,
                            },
                            "notes": [
                                "Turkey metrics sourced from blended-cac / CAC analysis sheets (best-effort).",
                                f"Global realized spend (budget tracking) for {month_label}: {_fmt_usd(global_spend)}" if global_spend is not None else "Global spend for this month not found in blended-cac.json.",
                            ],
                        }
                    ],
                },
                {
                    "title": "Funnel + KYC issues",
                    "slides": [
                        {
                            "title": "Funnel health (latest available) — KYC bottleneck",
                            "type": "bullets",
                            "bullets": funnel_callouts or [
                                "KYC is the steepest drop-off in the funnel.",
                                "Non-TR markets show KYC submit near-zero; likely provider/eligibility blocking.",
                            ],
                            "references": [
                                "analysis/funnel-summary.md",
                                "data/kyc-deepdive-*.json",
                            ],
                        }
                    ],
                },
                {
                    "title": "CAC & budget efficiency",
                    "slides": [
                        {
                            "title": "Channel efficiency (latest weekly view)",
                            "type": "insights",
                            "insights": {
                                "reallocation_plan": (efficiency.get("reallocation_plan") if isinstance(efficiency, dict) else None),
                                "flags": (efficiency.get("channel_flags") if isinstance(efficiency, dict) else None),
                                "meta": (efficiency.get("meta") if isinstance(efficiency, dict) else None),
                            },
                            "references": [
                                "data/budget-efficiency.json",
                                "data/channel-cac.json",
                            ],
                        },
                        {
                            "title": "Budget pacing (context)",
                            "type": "callouts",
                            "callouts": [
                                f"Month tracked: {pacing.get('month', '—')}",
                                f"Status: {pacing.get('status', '—')} (pace {pacing.get('pace_pct', '—')}%)",
                                f"Expected spend: {_fmt_usd(pacing.get('expected_spend'))} | Est. actual: {_fmt_usd(pacing.get('actual_spend_estimate'))}",
                            ],
                            "note": pacing.get("note"),
                            "references": ["data/budget-pacing.json"],
                        },
                    ],
                },
                {
                    "title": "Attribution caveat",
                    "slides": [
                        {
                            "title": "How to interpret these numbers",
                            "type": "bullets",
                            "bullets": attribution_caveats,
                            "references": [
                                "analysis/attribution-comparison.md",
                                "analysis/attribution-reconciliation.md",
                                "analysis/funnel-summary.md",
                            ],
                        }
                    ],
                },
                {
                    "title": "Market plans",
                    "slides": [
                        {
                            "title": "Market playbooks (links)",
                            "type": "links",
                            "links": plans,
                        }
                    ],
                },
                {
                    "title": "Next month action plan",
                    "slides": [
                        {
                            "title": "Top priorities",
                            "type": "actions",
                            "actions": top_actions,
                            "source": "data/weekly-actions.json (latest)",
                        }
                    ],
                },
            ],
            "gamma_export": {
                "status": "manual",
                "instructions": [
                    "Gamma API export is not wired in this script.",
                    "Option A (fast): paste analysis/monthly-deck.md into Gamma → 'Create from text' and refine styling.",
                    "Option B (structured): use data/monthly-deck.json as the source-of-truth, then manually map sections/slides into Gamma.",
                ],
            },
        },
    }

    # ── Markdown narrative ───────────────────────────────────────────────────
    md_parts: list[str] = []
    md_parts.append(f"# Monthly Executive Deck — {month_label}\n")
    md_parts.append(f"Generated: `{now.strftime('%Y-%m-%d %H:%M')} TRT`\n")

    md_parts.append("## Exec summary")
    if exec_bullets:
        md_parts.extend([f"- {b}" for b in exec_bullets])
    else:
        md_parts.append("- (No exec-summary bullets found; see analysis/funnel-summary.md)")

    if kpi_lines_week:
        md_parts.append("\n### Most recent KPI pulse (weekly snapshot)")
        md_parts.extend([f"- {l}" for l in kpi_lines_week])

    md_parts.append("\n## KPI snapshot + deltas")
    md_parts.append(f"### Turkey unit economics — {month_label} vs {prev_label}")
    md_parts.append(_md_table(["Metric", month_label, prev_label, "Δ"], kpi_rows))
    if global_spend is not None:
        md_parts.append(f"\nGlobal realized spend (budget tracking) for **{month_label}**: **{_fmt_usd(global_spend)}**")

    md_parts.append("\n## Funnel + KYC issues")
    md_parts.append("Primary constraint: **KYC** (conversion + availability across markets).")
    md_parts.append("References: analysis/funnel-summary.md")

    md_parts.append("\n## CAC & budget efficiency")
    if isinstance(efficiency, dict) and efficiency.get("channel_flags"):
        flags = efficiency.get("channel_flags", {})
        lowq = flags.get("low_quality") if isinstance(flags, dict) else None
        if isinstance(lowq, list) and lowq:
            md_parts.append("### Low-quality flags (latest weekly)")
            for f in lowq[:6]:
                md_parts.append(f"- **{f.get('bucket')}** — {f.get('reason')}")

    if isinstance(efficiency, dict) and isinstance(efficiency.get("reallocation_plan"), dict):
        plan = efficiency["reallocation_plan"].get("channel", {})
        if isinstance(plan, dict):
            pause = plan.get("pause")
            realloc = plan.get("reallocate_weekly_usd")
            md_parts.append("\n### Suggested reallocation (weekly proxy)")
            if pause:
                md_parts.append(f"- Pause: `{', '.join(pause)}`")
            if isinstance(realloc, dict):
                md_parts.append("- Reallocate weekly USD to:")
                for k, v in realloc.items():
                    md_parts.append(f"  - {k}: {_fmt_usd(v)}")

    if pacing:
        md_parts.append("\n### Budget pacing (context)")
        md_parts.append(f"- Month: `{pacing.get('month', '—')}`")
        md_parts.append(f"- Status: **{pacing.get('status', '—')}** (pace {pacing.get('pace_pct', '—')}%)")
        md_parts.append(f"- Expected spend: **{_fmt_usd(pacing.get('expected_spend'))}** | Est. actual: **{_fmt_usd(pacing.get('actual_spend_estimate'))}**")
        if pacing.get("note"):
            md_parts.append(f"- Note: {pacing.get('note')}")

    md_parts.append("\n## Attribution caveat")
    md_parts.extend([f"- {b}" for b in attribution_caveats])

    md_parts.append("\n## Market plans")
    if plans:
        for pl in plans:
            md_parts.append(f"- {pl['title']}: `{pl['path']}`")
    else:
        md_parts.append("- (No plan docs found in analysis/)")

    md_parts.append("\n## Next month action plan")
    if top_actions:
        for a in top_actions[:10]:
            md_parts.append(f"- **{a.get('severity')} / {a.get('owner')}** — {a.get('title')}\n  - Why: {a.get('why')}\n  - Impact: {a.get('expectedImpact')}")
    else:
        md_parts.append("- (No weekly actions found; run scripts/weekly_actions.py first)")

    md_parts.append("\n---\n")
    md_parts.append("## Gamma instructions")
    md_parts.append("- Paste this markdown into Gamma → *Create from text*.")
    md_parts.append("- Or use `data/monthly-deck.json` as a structured outline.")

    narrative = "\n".join(md_parts).rstrip() + "\n"
    return deck, narrative


def main() -> int:
    p = argparse.ArgumentParser(description="Generate monthly executive deck spec (JSON) + narrative (MD).")
    p.add_argument("--month", default=None, help="Target month YYYY-MM (default: previous calendar month)")
    p.add_argument(
        "--out-json",
        default=None,
        help="Output deck spec JSON (default: projects/cenoa-growth-engine/data/monthly-deck.json)",
    )
    p.add_argument(
        "--out-md",
        default=None,
        help="Output markdown narrative (default: projects/cenoa-growth-engine/analysis/monthly-deck.md)",
    )

    args = p.parse_args()

    now = _now_trt()
    yyyy_mm = args.month or _previous_month_yyyy_mm(now)
    if not re.match(r"^\d{4}-\d{2}$", yyyy_mm):
        raise SystemExit("--month must be in YYYY-MM")

    # Resolve project dir from this script location
    project_dir = Path(__file__).resolve().parents[1]

    inp = collect_inputs(project_dir)
    deck, narrative = build_deck(yyyy_mm, inp)

    out_json = Path(args.out_json) if args.out_json else project_dir / "data" / "monthly-deck.json"
    out_md = Path(args.out_md) if args.out_md else project_dir / "analysis" / "monthly-deck.md"

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)

    out_json.write_text(json.dumps(deck, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    out_md.write_text(narrative, encoding="utf-8")

    print(f"✅ Wrote {out_json}")
    print(f"✅ Wrote {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
