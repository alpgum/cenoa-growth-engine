#!/usr/bin/env python3
"""Weekly action items auto-generator.

Turns weekly KPI snapshot + anomalies + campaign health flags into a ranked
list of recommended actions.

Primary inputs (required unless noted):
  - projects/cenoa-growth-engine/data.json
  - projects/cenoa-growth-engine/data/anomalies.json (optional)
  - projects/cenoa-growth-engine/data/campaign-health.json (optional)

Optional enrichers (used if present):
  - projects/cenoa-growth-engine/data/budget-pacing.json
  - projects/cenoa-growth-engine/data/country-breakdown-*.json

Output:
  - projects/cenoa-growth-engine/data/weekly-actions.json

Usage:
  python3 scripts/weekly_actions.py
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# scripts/weekly_actions.py -> scripts -> cenoa-growth-engine -> projects -> workspace
WORKSPACE = Path(__file__).resolve().parents[3]

CORTEX_DATA_PATH = WORKSPACE / "projects" / "cenoa-growth-engine" / "data.json"
PM_DATA_DIR = WORKSPACE / "projects" / "cenoa-growth-engine" / "data"
ANOMALIES_PATH = PM_DATA_DIR / "anomalies.json"
CAMPAIGN_HEALTH_PATH = PM_DATA_DIR / "campaign-health.json"
BUDGET_PACING_PATH = PM_DATA_DIR / "budget-pacing.json"
OUTPUT_PATH_DEFAULT = PM_DATA_DIR / "weekly-actions.json"


KPI_LABELS = {
    "installs": "Installs",
    "signups": "Signups",
    "kycSubmits": "KYC Submit",
    "virtualAccountOpened": "Virtual Account Opened",
    "depositCompleted": "Deposits",
    "transferCompleted": "Transfers",
    "withdrawCompleted": "Withdrawals",
    "dauAvg": "DAU",
}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


# ---------------------------
# Country breakdown (optional)
# ---------------------------

COUNTRY_NAME_TO_ISO2 = {
    "Turkey": "TR",
    "Nigeria": "NG",
    "Egypt": "EG",
    "United States": "US",
    "United Kingdom": "GB",
    "Ghana": "GH",
    "Pakistan": "PK",
    "Germany": "DE",
    "France": "FR",
    "Canada": "CA",
    "Saudi Arabia": "SA",
    "United Arab Emirates": "AE",
    "Netherlands": "NL",
    "South Africa": "ZA",
    "Kenya": "KE",
    "Cyprus": "CY",
    "Greece": "GR",
    "Spain": "ES",
    "Italy": "IT",
    "Sweden": "SE",
    "Norway": "NO",
    "Poland": "PL",
    "Russia": "RU",
    "Ukraine": "UA",
    "Thailand": "TH",
    "Indonesia": "ID",
    "Azerbaijan": "AZ",
}


def iso2_from_country_name(name: str) -> str | None:
    name = (name or "").strip()
    if not name or name == "(none)":
        return None
    if name in COUNTRY_NAME_TO_ISO2:
        return COUNTRY_NAME_TO_ISO2[name]
    parts = [p for p in name.replace("(", " ").replace(")", " ").split() if p]
    if not parts:
        return None
    if len(parts) == 1 and len(parts[0]) >= 2:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[1][0]).upper()


def _collapsed_value(entry: Any) -> int:
    try:
        if isinstance(entry, list) and entry:
            maybe = entry[0]
            if isinstance(maybe, dict) and "value" in maybe:
                return int(maybe.get("value") or 0)
    except Exception:
        pass
    return 0


def extract_country_totals(raw: dict, section_key: str) -> dict[str, int]:
    section = (raw or {}).get(section_key, {}).get("data", {})
    labels = section.get("seriesLabels") or []
    collapsed = section.get("seriesCollapsed") or []

    out: dict[str, int] = {}
    for i, label_entry in enumerate(labels):
        if not isinstance(label_entry, list) or len(label_entry) < 2:
            continue
        country_name = label_entry[1]
        if not country_name or country_name == "(none)":
            continue
        if i >= len(collapsed):
            continue
        out[country_name] = _collapsed_value(collapsed[i])
    return out


def load_country_breakdown() -> tuple[dict[str, int], dict[str, int], dict[str, int], Path | None]:
    preferred = PM_DATA_DIR / "country-breakdown-20260320.json"
    path = preferred
    if not path.exists():
        candidates = sorted(PM_DATA_DIR.glob("country-breakdown-*.json"), reverse=True)
        path = candidates[0] if candidates else Path("")

    if not path or not path.exists():
        return {}, {}, {}, None

    raw = load_json(path)
    if not isinstance(raw, dict):
        return {}, {}, {}, path

    installs = extract_country_totals(raw, "[AppsFlyer] Install")
    signups = extract_country_totals(raw, "Cenoa sign-up completed")
    kyc = extract_country_totals(raw, "Bridgexyz KYC Component: Submit clicked")

    return installs, signups, kyc, path


# ---------------------------
# Actions
# ---------------------------

@dataclass
class Action:
    severity: str  # P0/P1/P2
    owner: str  # Acquisition/Product/Data
    title: str
    why: str
    expectedImpact: str
    evidence: dict[str, Any]
    score: float = 0.0


def owner_for_kpi(kpi: str) -> str:
    if kpi == "installs":
        return "Acquisition"
    if kpi in {"signups", "virtualAccountOpened", "depositCompleted", "transferCompleted", "withdrawCompleted", "kycSubmits"}:
        return "Product"
    if kpi == "dauAvg":
        return "Data"
    return "Data"


def severity_from_anomaly(anom: dict[str, Any]) -> str:
    sev = (anom.get("severity") or "").lower().strip()
    try:
        mag = abs(float(anom.get("deltaPct", 0)))
    except Exception:
        mag = 0.0

    if sev == "critical":
        return "P0"

    kpi = (anom.get("kpi") or "")
    if mag >= 30 and kpi in {"installs", "signups", "kycSubmits", "dauAvg", "virtualAccountOpened"}:
        return "P1"

    return "P2"


def fmt_delta(delta_pct: Any) -> str:
    try:
        d = float(delta_pct)
    except Exception:
        return "—"
    arrow = "↓" if d < 0 else "↑"
    return f"{arrow}{abs(d):.1f}%"


def score_action(a: Action) -> float:
    base = {"P0": 100.0, "P1": 70.0, "P2": 40.0}.get(a.severity, 10.0)
    s = base

    if "deltaPct" in a.evidence:
        try:
            s += min(60.0, abs(float(a.evidence.get("deltaPct") or 0)))
        except Exception:
            pass

    # spend/cost weight
    for k in ("cost", "actual_spend_estimate"):
        if a.evidence.get(k) is None:
            continue
        try:
            v = float(a.evidence.get(k) or 0)
            if v > 0:
                s += min(30.0, math.log10(v + 1.0) * 10.0)
        except Exception:
            pass

    # pacing weight
    if "pace_pct" in a.evidence:
        try:
            pace = float(a.evidence.get("pace_pct") or 0)
            if pace > 120:
                s += min(40.0, pace - 120)
        except Exception:
            pass

    return round(s, 2)


def dedupe_key(a: Action) -> str:
    return f"{a.severity}|{a.owner}|{a.title.strip().lower()}"


def generate_actions(
    cortex: dict[str, Any],
    anomalies_raw: Any,
    campaign_health: dict[str, Any] | None,
    budget_pacing: dict[str, Any] | None,
    country_installs: dict[str, int],
    country_signups: dict[str, int],
    country_kyc: dict[str, int],
) -> list[Action]:
    actions: list[Action] = []

    # (1) critical KPI anomalies => P0 diagnose
    anomalies: list[dict[str, Any]] = []
    if isinstance(anomalies_raw, dict) and isinstance(anomalies_raw.get("anomalies"), list):
        anomalies = [a for a in anomalies_raw["anomalies"] if isinstance(a, dict)]
    elif isinstance(anomalies_raw, list):
        anomalies = [a for a in anomalies_raw if isinstance(a, dict)]

    important = {"installs", "signups", "kycSubmits", "dauAvg", "virtualAccountOpened"}
    for anom in anomalies:
        kpi = anom.get("kpi")
        if not isinstance(kpi, str) or kpi not in important:
            continue
        label = KPI_LABELS.get(kpi, kpi)
        sev = severity_from_anomaly(anom)
        actions.append(
            Action(
                severity=sev,
                owner=owner_for_kpi(kpi),
                title=f"Diagnose {label} WoW anomaly ({fmt_delta(anom.get('deltaPct'))})",
                why=f"{label} changed {fmt_delta(anom.get('deltaPct'))} vs last week ({anom.get('prev')} → {anom.get('value')}).",
                expectedImpact="Identify root cause and unblock recovery within 24h (tracking, spend, funnel, outages).",
                evidence={
                    "source": "anomalies.json",
                    "kpi": kpi,
                    "value": anom.get("value"),
                    "prev": anom.get("prev"),
                    "deltaPct": anom.get("deltaPct"),
                    "severity": anom.get("severity"),
                },
            )
        )

    # (2) any DEAD / FRAUD / BLEEDING channel => action
    if isinstance(campaign_health, dict):
        channels = campaign_health.get("channels")
        if isinstance(channels, dict):
            for ch_name, ch in channels.items():
                if not isinstance(ch, dict):
                    continue
                status = (ch.get("status") or "").upper().strip()
                if status not in {"DEAD", "FRAUD", "BLEEDING"}:
                    continue
                sev = "P0" if status in {"DEAD", "FRAUD"} else "P1"
                if status == "DEAD":
                    title = f"Pause {ch_name} (DEAD spend)"
                    expected = "Stop wasted spend and reallocate budget to healthy channels."
                elif status == "FRAUD":
                    title = f"Pause & audit {ch_name} (fraud pattern)"
                    expected = "Reduce low-quality traffic and protect downstream conversion."
                else:
                    title = f"Cap/optimize {ch_name} (BLEEDING CPI)"
                    expected = "Lower CPI and improve paid efficiency within 48h."

                actions.append(
                    Action(
                        severity=sev,
                        owner="Acquisition",
                        title=title,
                        why=str(ch.get("reason") or f"Channel flagged {status}."),
                        expectedImpact=expected,
                        evidence={
                            "source": "campaign-health.json",
                            "level": "channel",
                            "channel": ch_name,
                            "status": status,
                            "reason": ch.get("reason"),
                            "cost": ch.get("cost"),
                            "installs": ch.get("installs"),
                            "signups": ch.get("sign_up"),
                            "virt_acc": ch.get("virt_acc"),
                            "new_active": ch.get("new_active"),
                            "cpi": ch.get("cpi"),
                        },
                    )
                )

    # (3) overspending pace => cap budgets
    if isinstance(budget_pacing, dict):
        status = (budget_pacing.get("status") or "").upper().strip()
        if status == "OVERSPENDING":
            pace_pct = budget_pacing.get("pace_pct")
            expected = budget_pacing.get("expected_spend")
            actual = budget_pacing.get("actual_spend_estimate")
            actions.append(
                Action(
                    severity="P0",
                    owner="Acquisition",
                    title="Cap budgets — overspending monthly pace",
                    why=f"Spend pace at ~{pace_pct}% of expected (expected ${expected:,.0f} vs est. actual ${actual:,.0f}).",
                    expectedImpact="Avoid exceeding monthly budget; force reallocation to highest-quality channels.",
                    evidence={
                        "source": "budget-pacing.json",
                        "status": status,
                        "pace_pct": pace_pct,
                        "expected_spend": expected,
                        "actual_spend_estimate": actual,
                        "budget": budget_pacing.get("budget"),
                        "effective_budget": budget_pacing.get("effective_budget"),
                    },
                )
            )

    # (4) NG/EG KYC submit clicks == 0 despite installs/signups => escalation checklist
    for iso in ("NG", "EG"):
        candidates = [name for name in country_signups.keys() if iso2_from_country_name(name) == iso]
        if not candidates:
            continue
        name = candidates[0]
        inst = int(country_installs.get(name, 0) or 0)
        sig = int(country_signups.get(name, 0) or 0)
        ky = int(country_kyc.get(name, 0) or 0)
        if (inst > 0 or sig > 0) and ky == 0:
            actions.append(
                Action(
                    severity="P0",
                    owner="Product",
                    title=f"Escalate {iso} KYC blocked (0 submits)",
                    why=f"{iso} shows {inst} installs / {sig} signups but 0 KYC submits in country breakdown.",
                    expectedImpact="Unblock onboarding; recover KYC conversion in a priority geo.",
                    evidence={
                        "source": "country-breakdown",
                        "iso": iso,
                        "country_name": name,
                        "installs": inst,
                        "signups": sig,
                        "kyc_submits": ky,
                        "checklist": [
                            "Verify Bridge widget renders + loads in-app",
                            "Check eligibility/geo restrictions for residents + documents",
                            "Check backend KYC session creation errors",
                            "Confirm tracking events firing (Submit clicked)",
                        ],
                    },
                )
            )

    if not actions:
        actions.append(
            Action(
                severity="P2",
                owner="Data",
                title="Review weekly pulse inputs",
                why="No anomalies or campaign flags detected; validate data freshness.",
                expectedImpact="Prevent silent failures in weekly automation.",
                evidence={"source": "weekly_actions.py"},
            )
        )

    # score + dedupe + sort
    uniq: dict[str, Action] = {}
    for a in actions:
        a.score = score_action(a)
        k = dedupe_key(a)
        if k not in uniq or uniq[k].score < a.score:
            uniq[k] = a

    out = list(uniq.values())
    out.sort(key=lambda x: (-x.score, x.severity, x.owner, x.title))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate weekly ranked action items")
    ap.add_argument("--output", "-o", default=str(OUTPUT_PATH_DEFAULT), help="Output JSON path")
    args = ap.parse_args()

    cortex = load_json(CORTEX_DATA_PATH)
    if not isinstance(cortex, dict):
        print(f"ERROR: Missing or invalid cortex data: {CORTEX_DATA_PATH}")
        return 1

    anomalies = load_json(ANOMALIES_PATH)
    campaign_health = load_json(CAMPAIGN_HEALTH_PATH)
    budget_pacing = load_json(BUDGET_PACING_PATH)

    inst, sig, kyc, country_path = load_country_breakdown()

    actions = generate_actions(
        cortex=cortex,
        anomalies_raw=anomalies,
        campaign_health=campaign_health if isinstance(campaign_health, dict) else None,
        budget_pacing=budget_pacing if isinstance(budget_pacing, dict) else None,
        country_installs=inst,
        country_signups=sig,
        country_kyc=kyc,
    )

    output = {
        "generated_at": _utc_now_iso(),
        "week": cortex.get("week") or "unknown",
        "inputs": {
            "cortex": str(CORTEX_DATA_PATH),
            "anomalies": str(ANOMALIES_PATH) if ANOMALIES_PATH.exists() else None,
            "campaign_health": str(CAMPAIGN_HEALTH_PATH) if CAMPAIGN_HEALTH_PATH.exists() else None,
            "budget_pacing": str(BUDGET_PACING_PATH) if BUDGET_PACING_PATH.exists() else None,
            "country_breakdown": str(country_path) if country_path else None,
        },
        "actions": [
            {
                "rank": idx,
                "severity": a.severity,
                "owner": a.owner,
                "title": a.title,
                "why": a.why,
                "expectedImpact": a.expectedImpact,
                "evidence": a.evidence,
                "score": a.score,
            }
            for idx, a in enumerate(actions, start=1)
        ],
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # stdout: keep it pipe-safe (single line)
    print(f"OK: wrote {out_path} ({len(actions)} actions)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
