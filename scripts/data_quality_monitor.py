#!/usr/bin/env python3
"""Data quality monitoring for Cenoa performance marketing artifacts.

Goal
----
Detect when key dashboards/scripts become unreliable due to:
- spikes in missing properties (e.g., "(none)" country/platform)
- attribution oddities (e.g., Organic share too high while paid spend is high)
- BigQuery table coverage gaps
- missing required output files

Outputs
-------
- data/data-quality.json
- analysis/data-quality-monitoring.md

Run
---
  source ~/.openclaw/venv/bin/activate
  GOOGLE_APPLICATION_CREDENTIALS=~/.openclaw/credentials/cenoa-marketingdatawarehouse-82b8600e66d6.json \
    python3 projects/cenoa-growth-engine/scripts/data_quality_monitor.py

Notes
-----
This script is intentionally conservative: if a critical dependency cannot be read/queried,
we mark the corresponding check as CRIT because monitoring itself is degraded.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from google.cloud import bigquery  # type: ignore
except Exception:  # pragma: no cover
    bigquery = None


PROJECT_ID = "cenoa-marketingdatawarehouse"
DATASET = "marketing_appsflyer"
TABLE_DAILY = f"{PROJECT_ID}.{DATASET}.daily_installs_campaign_tr"

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
ANALYSIS_DIR = REPO_ROOT / "analysis"

OUT_JSON = DATA_DIR / "data-quality.json"
OUT_MD = ANALYSIS_DIR / "data-quality-monitoring.md"


SEV_RANK = {"PASS": 0, "INFO": 1, "WARN": 2, "CRIT": 3}


@dataclass
class CheckResult:
    check_id: str
    title: str
    severity: str  # PASS|INFO|WARN|CRIT
    ok: bool
    message: str
    metrics: Dict[str, Any]
    recommended_fix: str


def _now_iso_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _latest_by_prefix(data_dir: Path, prefix: str) -> Optional[Path]:
    """Pick the latest JSON file matching prefix, using filename sort as heuristic."""
    cands = sorted(data_dir.glob(f"{prefix}*.json"))
    return cands[-1] if cands else None


def _extract_none_share(items: List[Dict[str, Any]], key: str) -> Tuple[float, int, int]:
    total = 0
    none_count = 0
    for it in items:
        c = int(it.get("count") or 0)
        total += c
        if str(it.get(key) or "").strip() == "(none)":
            none_count += c
    share = (none_count / total) if total > 0 else 0.0
    return share, none_count, total


def check_amplitude_none_country_platform_share(
    data_dir: Path,
    event_name: str = "Cenoa sign-up completed",
    warn_threshold: float = 0.30,
    crit_threshold: float = 0.50,
) -> CheckResult:
    country_path = _latest_by_prefix(data_dir, "amplitude-country-")
    platform_path = _latest_by_prefix(data_dir, "amplitude-platform-")

    if not country_path or not platform_path:
        missing = []
        if not country_path:
            missing.append("amplitude-country-*.json")
        if not platform_path:
            missing.append("amplitude-platform-*.json")
        return CheckResult(
            check_id="amplitude_none_country_platform",
            title="Amplitude signups: (none) country/platform share",
            severity="CRIT",
            ok=False,
            message=f"Missing required Amplitude breakdown file(s): {', '.join(missing)}",
            metrics={"event": event_name, "missing": missing},
            recommended_fix=(
                "Re-run Amplitude breakdown exports (country + platform) and ensure the event"
                f" `{event_name}` is included. Then re-run this monitor."
            ),
        )

    try:
        country = _load_json(country_path)
        platform = _load_json(platform_path)
        c_items = (country.get("events") or {}).get(event_name, {}).get("countries") or []
        p_items = (platform.get("events") or {}).get(event_name, {}).get("platforms") or []

        c_share, c_none, c_total = _extract_none_share(c_items, "country")
        p_share, p_none, p_total = _extract_none_share(p_items, "platform")

        worst = max(c_share, p_share)
        if worst >= crit_threshold:
            sev = "CRIT"
            ok = False
        elif worst >= warn_threshold:
            sev = "WARN"
            ok = False
        else:
            sev = "PASS"
            ok = True

        msg = (
            f"Event `{event_name}` — (none) country share: {c_share:.1%} ({c_none}/{c_total}); "
            f"(none) platform share: {p_share:.1%} ({p_none}/{p_total})."
        )

        fix = (
            "Investigate why country/platform properties are missing for signups: "
            "(1) verify Amplitude property mapping / SDK initialization, "
            "(2) check web→app or server-side events missing device context, "
            "(3) ensure the event is instrumented consistently across clients, "
            "(4) backfill/patch if possible."
        )

        return CheckResult(
            check_id="amplitude_none_country_platform",
            title="Amplitude signups: (none) country/platform share",
            severity=sev,
            ok=ok,
            message=msg,
            metrics={
                "event": event_name,
                "country_file": str(country_path.name),
                "platform_file": str(platform_path.name),
                "none_country_share": c_share,
                "none_platform_share": p_share,
                "warn_threshold": warn_threshold,
                "crit_threshold": crit_threshold,
            },
            recommended_fix=fix,
        )
    except Exception as e:
        return CheckResult(
            check_id="amplitude_none_country_platform",
            title="Amplitude signups: (none) country/platform share",
            severity="CRIT",
            ok=False,
            message=f"Failed to parse Amplitude breakdown files: {e}",
            metrics={"event": event_name, "country_file": str(country_path), "platform_file": str(platform_path)},
            recommended_fix="Open the JSON exports and verify schema; then re-export via scripts/amplitude_*_breakdown.py.",
        )


def check_appsflyer_organic_share_vs_paid_spend(
    data_dir: Path,
    organic_share_threshold: float = 0.40,
    paid_spend_weekly_threshold_usd: float = 2000.0,
) -> CheckResult:
    """Warn when Organic installs are high while paid spend (proxy) is high.

    Data source:
    - data/channel-cac.json: provides attribution_outcomes installs by bucket + spend_proxy_weekly_usd.
    """

    path = data_dir / "channel-cac.json"
    if not path.exists():
        return CheckResult(
            check_id="appsflyer_organic_share_paid_spend",
            title='AppsFlyer installs: "Organic" share high while paid spend is high',
            severity="CRIT",
            ok=False,
            message="Missing data/channel-cac.json (needed for Organic share vs paid spend check).",
            metrics={"missing": str(path)},
            recommended_fix="Generate channel-cac.json (scripts/channel_cac.py or equivalent) and re-run.",
        )

    try:
        d = _load_json(path)
        buckets = d.get("buckets") or []

        total_installs = 0
        organic_installs = 0
        paid_spend_weekly = 0.0

        for b in buckets:
            inst = int(((b.get("attribution_outcomes") or {}).get("installs")) or 0)
            total_installs += inst

            bucket = str(b.get("bucket") or "").strip()
            if bucket.lower() == "organic":
                organic_installs += inst

            spend = b.get("spend_proxy_weekly_usd")
            try:
                spend_f = float(spend)
            except Exception:
                spend_f = 0.0

            # Count any non-zero spend buckets as paid (proxy).
            if spend_f > 0:
                paid_spend_weekly += spend_f

        organic_share = (organic_installs / total_installs) if total_installs > 0 else 0.0
        paid_spend_high = paid_spend_weekly >= paid_spend_weekly_threshold_usd

        if organic_share > organic_share_threshold and paid_spend_high:
            sev = "WARN"
            ok = False
            msg = (
                f"Organic installs share is {organic_share:.1%} ({organic_installs}/{total_installs}) "
                f"while weekly paid spend proxy is ${paid_spend_weekly:,.0f}."
            )
            fix = (
                "Possible paid→organic attribution loss (web→app handoff, deep link/IDFA/GAID loss, SKAN limitations). "
                "Audit AppsFlyer attribution settings, ensure OneLink/deep links are used, "
                "verify paid campaigns pass correct parameters, and cross-check platform dashboards vs AppsFlyer." 
            )
        else:
            sev = "PASS"
            ok = True
            msg = (
                f"Organic installs share {organic_share:.1%} ({organic_installs}/{total_installs}); "
                f"weekly paid spend proxy ${paid_spend_weekly:,.0f}."
            )
            fix = "No action. Monitor weekly; investigate if Organic share rises while spend stays high."

        return CheckResult(
            check_id="appsflyer_organic_share_paid_spend",
            title='AppsFlyer installs: "Organic" share high while paid spend is high',
            severity=sev,
            ok=ok,
            message=msg,
            metrics={
                "source": str(path.name),
                "organic_installs": organic_installs,
                "total_installs": total_installs,
                "organic_share": organic_share,
                "paid_spend_weekly_proxy_usd": paid_spend_weekly,
                "organic_share_threshold": organic_share_threshold,
                "paid_spend_weekly_threshold_usd": paid_spend_weekly_threshold_usd,
            },
            recommended_fix=fix,
        )

    except Exception as e:
        return CheckResult(
            check_id="appsflyer_organic_share_paid_spend",
            title='AppsFlyer installs: "Organic" share high while paid spend is high',
            severity="CRIT",
            ok=False,
            message=f"Failed to compute Organic share from channel-cac.json: {e}",
            metrics={"source": str(path)},
            recommended_fix="Validate channel-cac.json schema; regenerate it.",
        )


def check_bigquery_daily_table_coverage(
    table: str = TABLE_DAILY,
    min_days_required: int = 21,
) -> CheckResult:
    if bigquery is None:
        return CheckResult(
            check_id="bigquery_daily_table_coverage",
            title="BigQuery: daily_installs_campaign_tr coverage",
            severity="CRIT",
            ok=False,
            message="google-cloud-bigquery is not available in this environment.",
            metrics={"table": table},
            recommended_fix="Install google-cloud-bigquery in the venv and re-run.",
        )

    try:
        client = bigquery.Client(project=PROJECT_ID)
        q = f"""
        SELECT MIN(date) AS min_date, MAX(date) AS max_date, COUNT(DISTINCT date) AS day_count
        FROM `{table}`
        """
        row = list(client.query(q))[0]
        min_date = row["min_date"]
        max_date = row["max_date"]
        day_count = int(row["day_count"] or 0)

        if day_count < min_days_required:
            sev = "WARN"
            ok = False
            msg = (
                f"Daily table has only {day_count} distinct days (min={min_date}, max={max_date}); "
                f"expected >= {min_days_required} days for stable reporting." 
            )
            fix = (
                "Extend the BigQuery load/ELT for daily_installs_campaign_tr to cover at least the last 21-30 days "
                "(backfill missing partitions) and verify the scheduled job is running." 
            )
        else:
            sev = "PASS"
            ok = True
            msg = f"Daily table coverage OK: {day_count} distinct days (min={min_date}, max={max_date})."
            fix = "No action."

        return CheckResult(
            check_id="bigquery_daily_table_coverage",
            title="BigQuery: daily_installs_campaign_tr coverage",
            severity=sev,
            ok=ok,
            message=msg,
            metrics={
                "table": table,
                "min_date": str(min_date),
                "max_date": str(max_date),
                "distinct_days": day_count,
                "min_days_required": min_days_required,
            },
            recommended_fix=fix,
        )

    except Exception as e:
        return CheckResult(
            check_id="bigquery_daily_table_coverage",
            title="BigQuery: daily_installs_campaign_tr coverage",
            severity="CRIT",
            ok=False,
            message=f"BigQuery coverage query failed: {e}",
            metrics={"table": table, "GOOGLE_APPLICATION_CREDENTIALS": os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")},
            recommended_fix=(
                "Ensure GOOGLE_APPLICATION_CREDENTIALS is set to the service account JSON and the account has BigQuery access. "
                "Then re-run the script."
            ),
        )


def check_required_files(data_dir: Path) -> CheckResult:
    required = ["data.json", "anomalies.json", "campaign-health.json"]
    missing = [f for f in required if not (data_dir / f).exists()]

    if missing:
        return CheckResult(
            check_id="required_files_present",
            title="Required output files present",
            severity="CRIT",
            ok=False,
            message=f"Missing required file(s): {', '.join(missing)}",
            metrics={"required": required, "missing": missing},
            recommended_fix=(
                "Re-run the pipelines that generate these artifacts (weekly report / anomalies / campaign health). "
                "If `data.json` is deprecated, update this monitor to the new canonical dataset export name." 
            ),
        )

    return CheckResult(
        check_id="required_files_present",
        title="Required output files present",
        severity="PASS",
        ok=True,
        message="All required files exist.",
        metrics={"required": required},
        recommended_fix="No action.",
    )


def overall_severity(checks: List[CheckResult]) -> str:
    worst = max((SEV_RANK.get(c.severity, 0) for c in checks), default=0)
    for sev, rank in SEV_RANK.items():
        if rank == worst:
            return sev
    return "PASS"


def render_md(ts: str, checks: List[CheckResult], overall: str) -> str:
    failed = [c for c in checks if not c.ok]

    lines = []
    lines.append("# Data Quality Monitoring\n")
    lines.append(f"Generated: `{ts}`\n")
    lines.append(f"Overall severity: **{overall}**\n")

    if failed:
        lines.append("## Failures / Alerts\n")
        for c in failed:
            lines.append(f"- **{c.severity}** — {c.title}: {c.message}")
        lines.append("")

    lines.append("## Checks\n")
    for c in checks:
        status = "PASS" if c.ok else "FAIL"
        lines.append(f"### {c.title}")
        lines.append(f"- ID: `{c.check_id}`")
        lines.append(f"- Status: **{status}**")
        lines.append(f"- Severity: **{c.severity}**")
        lines.append(f"- Message: {c.message}")
        if c.metrics:
            lines.append("- Metrics:")
            for k, v in c.metrics.items():
                if isinstance(v, float):
                    lines.append(f"  - {k}: {v:.6f}")
                else:
                    lines.append(f"  - {k}: {v}")
        lines.append(f"- Recommended fix: {c.recommended_fix}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    ts = _now_iso_utc()

    checks: List[CheckResult] = []
    checks.append(check_amplitude_none_country_platform_share(DATA_DIR))
    checks.append(check_appsflyer_organic_share_vs_paid_spend(DATA_DIR))
    checks.append(check_bigquery_daily_table_coverage())
    checks.append(check_required_files(DATA_DIR))

    overall = overall_severity(checks)
    failures = [
        {
            "check_id": c.check_id,
            "title": c.title,
            "severity": c.severity,
            "message": c.message,
            "recommended_fix": c.recommended_fix,
        }
        for c in checks
        if not c.ok
    ]

    out = {
        "generated_at": ts,
        "overall_severity": overall,
        "checks": [
            {
                "check_id": c.check_id,
                "title": c.title,
                "severity": c.severity,
                "ok": c.ok,
                "message": c.message,
                "metrics": c.metrics,
                "recommended_fix": c.recommended_fix,
            }
            for c in checks
        ],
        "failures": failures,
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_MD.write_text(render_md(ts, checks, overall), encoding="utf-8")

    print(f"Wrote: {OUT_JSON}")
    print(f"Wrote: {OUT_MD}")

    # Exit code convention: non-zero when CRIT exists
    if overall == "CRIT":
        raise SystemExit(2)
    if overall == "WARN":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
