#!/usr/bin/env python3
"""Telegram-formatted weekly performance report (polished v2).

Reads:
  1) projects/cenoa-growth-engine/data.json
  2) projects/cenoa-growth-engine/data/anomalies.json
  3) projects/cenoa-growth-engine/data/country-breakdown-*.json
  4) projects/cenoa-growth-engine/data/channel-cac.json
  5) projects/cenoa-growth-engine/data/budget-pacing.json
  6) projects/cenoa-growth-engine/data/weekly-actions.json
  7) projects/cenoa-growth-engine/data/weekly-channel-country-*.json (last 4 for trends)

Outputs:
  - Report text to stdout (no extra noise; safe for piping)
  - Also saves to: .../data/weekly-report-latest.md

All lines ≤80 chars for Telegram readability.
"""

from __future__ import annotations

import glob
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parents[3]
CORTEX_DATA_PATH = WORKSPACE / "projects" / "cenoa-growth-engine" / "data.json"
PM_DATA_DIR = WORKSPACE / "projects" / "cenoa-growth-engine" / "data"
ANALYSIS_DIR = WORKSPACE / "projects" / "cenoa-growth-engine" / "analysis"
ANOMALIES_PATH = PM_DATA_DIR / "anomalies.json"
CHANNEL_CAC_PATH = PM_DATA_DIR / "channel-cac.json"
BUDGET_PACING_PATH = PM_DATA_DIR / "budget-pacing.json"
WEEKLY_ACTIONS_PATH = PM_DATA_DIR / "weekly-actions.json"
OUTPUT_PATH = PM_DATA_DIR / "weekly-report-latest.md"
COUNTRY_BREAKDOWN_PREFERRED = PM_DATA_DIR / "country-breakdown-20260320.json"


# ── Formatting helpers ─────────────────────────────

def fmt_n(v: Any) -> str:
    """Format number compactly."""
    if v is None:
        return "—"
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, int):
        return f"{v:,}"
    if isinstance(v, float):
        if v >= 1000:
            return f"{v:,.0f}"
        if v.is_integer():
            return f"{int(v):,}"
        return f"{v:,.1f}"
    return str(v)


def fmt_usd(v: Any) -> str:
    if v is None:
        return "—"
    try:
        f = float(v)
    except Exception:
        return "—"
    if f >= 1000:
        return f"${f:,.0f}"
    return f"${f:,.1f}"


def fmt_delta(delta_pct: Any, flat_threshold: float = 1.0) -> str:
    if delta_pct is None:
        return "—"
    try:
        d = float(delta_pct)
    except Exception:
        return "—"
    if abs(d) <= flat_threshold:
        return "▬ flat"
    if d > 0:
        return f"▲{abs(d):.1f}%"
    return f"▼{abs(d):.1f}%"


def spark(values: list[float | int]) -> str:
    """Mini ASCII sparkline from values (last N weeks).
    Uses ▁▂▃▄▅▆▇█ blocks.
    """
    bars = "▁▂▃▄▅▆▇█"
    if not values or all(v == 0 for v in values):
        return "▁▁▁▁"
    mn, mx = min(values), max(values)
    rng = mx - mn if mx != mn else 1
    return "".join(
        bars[min(int((v - mn) / rng * 7), 7)] for v in values
    )


def vs_target_str(actual: Any, target: Any) -> str:
    """Return 'vs T: 1,200 (▲5%)' or similar."""
    if target is None or actual is None:
        return ""
    try:
        a, t = float(actual), float(target)
    except Exception:
        return ""
    if t == 0:
        return ""
    pct = (a - t) / t * 100
    arrow = "▲" if pct > 0 else "▼" if pct < 0 else "▬"
    return f"  vs T: {fmt_n(t)} ({arrow}{abs(pct):.0f}%)"


# ── Country helpers ────────────────────────────────

COUNTRY_NAME_TO_ISO2 = {
    "Turkey": "TR", "Nigeria": "NG", "Egypt": "EG",
    "United States": "US", "United Kingdom": "GB",
    "Ghana": "GH", "Pakistan": "PK", "Germany": "DE",
    "France": "FR", "Canada": "CA", "Saudi Arabia": "SA",
    "United Arab Emirates": "AE", "Netherlands": "NL",
    "South Africa": "ZA", "Kenya": "KE", "Cyprus": "CY",
    "Azerbaijan": "AZ",
}


def iso2(name: str) -> str | None:
    name = (name or "").strip()
    if not name or name == "(none)":
        return None
    if name in COUNTRY_NAME_TO_ISO2:
        return COUNTRY_NAME_TO_ISO2[name]
    parts = name.split()
    if len(parts) == 1 and len(parts[0]) >= 2:
        return parts[0][:2].upper()
    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()
    return None


def flag(code: str | None) -> str:
    if not code or len(code) != 2:
        return "🏳️"
    code = code.upper()
    return chr(127397 + ord(code[0])) + chr(127397 + ord(code[1]))


def _collapsed_val(entry: Any) -> int:
    try:
        if isinstance(entry, list) and entry:
            m = entry[0]
            if isinstance(m, dict) and "value" in m:
                return int(m.get("value") or 0)
    except Exception:
        pass
    return 0


def extract_country_totals(raw: dict, section_key: str) -> dict[str, int]:
    section = (raw or {}).get(section_key, {}).get("data", {})
    labels = section.get("seriesLabels") or []
    collapsed = section.get("seriesCollapsed") or []
    out: dict[str, int] = {}
    for i, le in enumerate(labels):
        if not isinstance(le, list) or len(le) < 2:
            continue
        cn = le[1]
        if not cn or cn == "(none)":
            continue
        if i < len(collapsed):
            out[cn] = _collapsed_val(collapsed[i])
    return out


def load_country_breakdown() -> tuple[dict, dict, dict]:
    path = COUNTRY_BREAKDOWN_PREFERRED
    if not path.exists():
        cands = sorted(PM_DATA_DIR.glob("country-breakdown-*.json"), reverse=True)
        if cands:
            path = cands[0]
    if not path.exists():
        return {}, {}, {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}, {}, {}
    return (
        extract_country_totals(raw, "[AppsFlyer] Install"),
        extract_country_totals(raw, "Cenoa sign-up completed"),
        extract_country_totals(raw, "Bridgexyz KYC Component: Submit clicked"),
    )


# ── Data loaders ───────────────────────────────────

def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def load_anomalies() -> list[dict]:
    raw = load_json(ANOMALIES_PATH)
    if isinstance(raw, dict):
        a = raw.get("anomalies")
        if isinstance(a, list):
            return [x for x in a if isinstance(x, dict)]
        return []
    if isinstance(raw, list):
        return [x for x in raw if isinstance(x, dict)]
    return []


def load_weekly_history(kpi: str, n: int = 4) -> list[int]:
    """Pull last N weeks of a KPI from weekly-channel-country files.

    These files have install/signup totals as sum of channel|country
    wow entries. As a simpler approach, use cortex prev+current
    and anomalies for 2 data points, then pad.
    """
    # Best effort: use cortex current + prev for 2 points
    # For a fuller picture, scan weekly files
    files = sorted(PM_DATA_DIR.glob("weekly-channel-country-*.json"))[-n:]
    values: list[int] = []

    event_map = {
        "installs": "install",
        "signups": "signup",
        "kycSubmits": "kyc_submit",
        "withdrawCompleted": "withdrawal",
        "dauAvg": None,  # not in these files
    }

    mapped = event_map.get(kpi)
    if not mapped:
        return values

    for f in files:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            section = d.get(mapped, {})
            wow = section.get("wow", {})
            total = sum(
                entry.get("current", 0)
                for entry in wow.values()
                if isinstance(entry, dict)
            )
            values.append(total)
        except Exception:
            continue
    return values[-n:]


# ── KPI targets (from cortex + budget allocation model) ──

KPI_TARGETS: dict[str, float] = {
    # Weekly targets derived from monthly budget allocation
    # model & historical benchmarks
    "installs": 2000,    # ~8k/mo target
    "signups": 1500,     # ~6k/mo
    "kycSubmits": 250,   # ~1k/mo
    "withdrawCompleted": 2000,
    "dauAvg": 5000,
}


# ── Report builder ─────────────────────────────────

KPI_LABELS = {
    "installs": "Installs",
    "signups": "Signups",
    "kycSubmits": "KYC Submit",
    "withdrawCompleted": "Withdrawals",
    "dauAvg": "DAU",
    "virtualAccountOpened": "Virtual Account Opened",
    "depositCompleted": "Deposits",
    "transferCompleted": "Transfers",
}

ANOMALY_SORT = {
    "installs": 10, "signups": 20, "kycSubmits": 30,
    "withdrawCompleted": 40, "dauAvg": 50,
}


@dataclass(frozen=True)
class KPIRow:
    key: str
    emoji: str
    label: str
    show_delta: bool


KPI_ROWS = [
    KPIRow("installs", "📲", "Installs", True),
    KPIRow("signups", "📝", "Signups", True),
    KPIRow("kycSubmits", "✅", "KYC Submit", True),
    KPIRow("withdrawCompleted", "💳", "Withdrawals", True),
    KPIRow("dauAvg", "👤", "DAU avg", False),
]


def build_report() -> str:
    if not CORTEX_DATA_PATH.exists():
        raise FileNotFoundError(f"Missing: {CORTEX_DATA_PATH}")

    cortex = json.loads(
        CORTEX_DATA_PATH.read_text(encoding="utf-8")
    )
    week = cortex.get("week") or "Unknown"
    kpis = cortex.get("kpis") or {}
    channel_perf = cortex.get("channelPerformance") or []
    cac_tracking = cortex.get("cacTracking") or []
    attr_quality = cortex.get("attributionQuality") or {}
    kyc_by_country = cortex.get("kycByCountry") or []
    budget_pacing_cortex = cortex.get("budgetPacing") or {}

    # External data
    inst_c, sig_c, kyc_c = load_country_breakdown()
    anomalies = load_anomalies()
    budget_pacing = load_json(BUDGET_PACING_PATH) or {}
    actions_raw = load_json(WEEKLY_ACTIONS_PATH) or {}

    lines: list[str] = []

    # ── Header ──
    lines.append(f"📊 Cenoa Weekly Pulse — {week}")
    lines.append("")

    # ── KPIs with trend + vs target ──
    for row in KPI_ROWS:
        k = kpis.get(row.key) or {}
        value = k.get("value", 0)
        delta = k.get("deltaPct")

        if row.key == "dauAvg":
            try:
                value = int(round(float(value)))
            except Exception:
                pass

        # Sparkline from history
        hist = load_weekly_history(row.key)
        if row.key == "dauAvg" and not hist:
            # Fallback: use prev + current
            prev = k.get("prev")
            if prev:
                hist = [int(prev), int(value)]
        spark_str = f" {spark(hist)}" if hist else ""

        # Build line
        if row.show_delta:
            line = (
                f"{row.emoji} {row.label}: "
                f"{fmt_n(value)} ({fmt_delta(delta)})"
                f"{spark_str}"
            )
        else:
            line = (
                f"{row.emoji} {row.label}: "
                f"{fmt_n(value)}{spark_str}"
            )
        lines.append(line)

        # vs Target on next line (indented)
        target = KPI_TARGETS.get(row.key)
        if target:
            try:
                a = float(value)
                pct = (a - target) / target * 100
                sign = "▲" if pct > 0 else "▼" if pct < 0 else "▬"
                lines.append(
                    f"   vs Target {fmt_n(target)}: "
                    f"{sign}{abs(pct):.0f}%"
                )
            except Exception:
                pass

    # ── Budget Alert ──
    bp = budget_pacing or budget_pacing_cortex
    pace_pct = bp.get("pace_pct") or bp.get("pacing_pct")
    status = (bp.get("status") or "").upper()
    if status == "OVERSPENDING" or (
        pace_pct and float(pace_pct) > 120
    ):
        lines.append("")
        lines.append("🚨 BUDGET ALERT")
        budget = bp.get("budget") or bp.get("target")
        actual = bp.get("actual_spend_estimate") or bp.get(
            "mtd_spend"
        )
        expected = bp.get("expected_spend")
        lines.append(
            f"  Monthly budget: {fmt_usd(budget)}"
        )
        if actual:
            lines.append(
                f"  Est. spend MTD: {fmt_usd(actual)} "
                f"({fmt_n(pace_pct)}% pace)"
            )
        if expected:
            lines.append(
                f"  Expected by now: {fmt_usd(expected)}"
            )
        note = bp.get("note", "")
        if note and len(note) < 70:
            lines.append(f"  ⚠️ {note}")
        else:
            lines.append(
                "  ⚠️ Cap budgets now or reallocate"
            )
        lines.append(
            f"  📄 analysis/budget-efficiency.md"
        )

    # ── Channel Ranking (TRUE CAC) ──
    if channel_perf or cac_tracking:
        lines.append("")
        lines.append("📡 Channel Ranking (TRUE CAC):")

        # Merge cac_tracking targets into channel_perf
        target_map = {
            c["name"]: c.get("target_cac")
            for c in cac_tracking
        }
        status_map = {
            c["name"]: c.get("status", "")
            for c in cac_tracking
        }

        # Sort by true_cac ascending (best first)
        ranked = sorted(
            channel_perf,
            key=lambda c: (
                c.get("true_cac") or 9999
            ),
        )

        for i, ch in enumerate(ranked[:6], 1):
            name = ch.get("name", "?")
            cac = ch.get("true_cac")
            cpi = ch.get("cpi")
            spend = ch.get("spend")
            target = target_map.get(name)

            # Status emoji
            st = status_map.get(name, "")
            st_icon = "✅" if st == "on_target" else "⚠️"

            cac_str = fmt_usd(cac) if cac else "n/a"
            tgt_str = (
                f" (T:{fmt_usd(target)})" if target else ""
            )

            lines.append(
                f"  {i}. {st_icon} {name}: "
                f"CAC {cac_str}{tgt_str} "
                f"| CPI {fmt_usd(cpi)} "
                f"| ${fmt_n(spend)}/wk"
            )

    # ── Attribution Health ──
    if attr_quality:
        known = attr_quality.get("known_pct", 0)
        none_pct = attr_quality.get("none_pct", 0)
        trend = attr_quality.get("trend", "")
        factor = attr_quality.get("correction_factor")
        lines.append("")

        health_icon = "🟢" if known > 40 else (
            "🟡" if known > 20 else "🔴"
        )
        lines.append(
            f"🔍 Attribution Health: {health_icon} "
            f"{known}% known / {none_pct}% none"
        )
        if factor:
            lines.append(
                f"   Correction factor: {factor}x | "
                f"Trend: {trend}"
            )
        lines.append(
            "   📄 analysis/attribution-reconciliation.md"
        )

    # ── Country Breakdown ──
    top_countries: list[str] = []
    if inst_c:
        top_countries = [
            n for n, _ in sorted(
                inst_c.items(),
                key=lambda kv: kv[1], reverse=True
            )
            if n != "(none)"
        ][:3]

    if top_countries:
        lines.append("")
        lines.append("🌍 Country Breakdown:")
        for name in top_countries:
            code = iso2(name)
            fl = flag(code)
            inst = inst_c.get(name, 0)
            sig = sig_c.get(name, 0)
            ky = kyc_c.get(name, 0)
            warn = " ⚠️" if (inst or sig) and not ky else ""
            lines.append(
                f"  {fl} {code or '—'}: {fmt_n(inst)} inst, "
                f"{fmt_n(sig)} sign, {fmt_n(ky)} KYC{warn}"
            )

    # ── KYC Status by Country ──
    if kyc_by_country:
        lines.append("")
        lines.append("🪪 KYC Status:")
        for entry in kyc_by_country:
            cn = entry.get("country", "?")
            code = iso2(cn)
            fl = flag(code)
            started = entry.get("kyc_started", 0)
            submit = entry.get("kyc_submit", 0)
            rate = entry.get("conversion_rate", 0)
            icon = "✅" if rate > 5 else (
                "⚠️" if rate > 0 else "🔴"
            )
            lines.append(
                f"  {fl} {code}: {icon} "
                f"{fmt_n(started)} started → "
                f"{fmt_n(submit)} submit ({rate}%)"
            )

    # ── Anomalies ──
    if anomalies:
        filtered = [
            a for a in anomalies
            if (a.get("severity", "").lower() == "critical"
                or abs(float(a.get("deltaPct", 0))) >= 30)
        ]
        if filtered:
            lines.append("")
            lines.append("🚨 Anomalies:")
            for a in sorted(
                filtered,
                key=lambda x: (
                    ANOMALY_SORT.get(x.get("kpi", ""), 999),
                    -abs(float(x.get("deltaPct", 0)))
                ),
            )[:8]:
                kpi = a.get("kpi", "")
                label = KPI_LABELS.get(kpi, kpi)
                sev = a.get("severity", "?").lower()
                lines.append(
                    f"  • {label} {fmt_delta(a.get('deltaPct'))}"
                    f" ({sev})"
                )

    # ── Actions (with doc links) ──
    actions_list = []
    if isinstance(actions_raw, dict):
        actions_list = actions_raw.get("actions", [])
    elif isinstance(actions_raw, list):
        actions_list = actions_raw

    # Map evidence sources to analysis docs
    DOC_MAP = {
        "budget-pacing.json": "budget-efficiency.md",
        "anomalies.json": "12-week-trends.md",
        "campaign-health.json": "appnext-fraud-summary.md",
    }

    if actions_list:
        lines.append("")
        lines.append("🎯 Actions:")
        for a in actions_list[:5]:
            sev = a.get("severity", "")
            title = a.get("title", "")
            evidence = a.get("evidence", {})
            src = evidence.get("source", "")
            doc = DOC_MAP.get(src, "")

            sev_str = f"[{sev}] " if sev else ""
            doc_str = f"\n   📄 analysis/{doc}" if doc else ""
            lines.append(f"  • {sev_str}{title}{doc_str}")
    else:
        # Fallback actions
        lines.append("")
        lines.append("🎯 Actions:")
        # Build from country data
        kyc_zero = [
            iso2(n)
            for n in top_countries
            if (inst_c.get(n, 0) or sig_c.get(n, 0))
            and not kyc_c.get(n, 0)
        ]
        if kyc_zero:
            lines.append(
                f"  • Fix KYC for {'/'.join(filter(None, kyc_zero))}"
                "\n   📄 analysis/kyc-escalation-brief.md"
            )
        lines.append(
            "  • Pause Appnext + TikTok"
            "\n   📄 analysis/appnext-fraud-summary.md"
        )
        lines.append(
            "  • Scale Pmax + ASA"
            "\n   📄 analysis/budget-allocation-model.md"
        )

    # ── Footer ──
    lines.append("")
    lines.append("— auto-generated by cenoa-growth-engine")

    report = "\n".join(lines).rstrip() + "\n"

    # Enforce 80-char limit per line (soft-wrap long lines)
    final_lines = []
    for line in report.split("\n"):
        if len(line) <= 80:
            final_lines.append(line)
        else:
            # Wrap at 80, indent continuation
            words = line.split(" ")
            cur = ""
            for w in words:
                test = f"{cur} {w}".strip() if cur else w
                if len(test) <= 80:
                    cur = test
                else:
                    if cur:
                        final_lines.append(cur)
                    cur = f"   {w}"
            if cur:
                final_lines.append(cur)
    return "\n".join(final_lines).rstrip() + "\n"


def main() -> int:
    try:
        report = build_report()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    sys.stdout.write(report)

    try:
        PM_DATA_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(report, encoding="utf-8")
    except Exception as e:
        print(f"WARN: Failed to write {OUTPUT_PATH}: {e}",
              file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
