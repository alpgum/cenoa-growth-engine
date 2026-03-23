#!/usr/bin/env python3
"""[S3-032] Build a campaign-level installs table for the latest available (up to) 7 days.

Why:
  Amplitude gp:[AppsFlyer] campaign is blank, so campaign-level analysis cannot
  be done reliably inside Amplitude. AppsFlyer attribution data is available in
  BigQuery, so we build a reproducible extract.

BigQuery inputs:
  - cenoa-marketingdatawarehouse.marketing_appsflyer.daily_installs_campaign_tr

Outputs:
  - analysis/bq-campaign-table-latest.md
  - data/bq-campaign-table-latest.json

Run:
  source ~/.openclaw/venv/bin/activate
  GOOGLE_APPLICATION_CREDENTIALS=~/.openclaw/credentials/cenoa-marketingdatawarehouse-82b8600e66d6.json \
    python3 projects/cenoa-growth-engine/scripts/bq_campaign_table_latest.py

Notes:
  - The underlying table is TR-only (no country column). We emit country='TR'.
  - Optional CPI join: if a campaign-level cost source is detected in Sheets,
    we'll attach cost_usd and cpi_usd. (Currently not found in synced sheets.)
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from google.cloud import bigquery

PROJECT_ID = "cenoa-marketingdatawarehouse"
DATASET = "marketing_appsflyer"
TABLE_DAILY = f"{PROJECT_ID}.{DATASET}.daily_installs_campaign_tr"

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_MD = REPO_ROOT / "analysis" / "bq-campaign-table-latest.md"
OUT_JSON = REPO_ROOT / "data" / "bq-campaign-table-latest.json"

SHEETS_TRAFIK_JSON = REPO_ROOT / "data" / "sheets-trafik-canavari.json"


def _now_trt_iso() -> str:
    # Keep it simple: use local clock; other scripts already write TRT.
    return datetime.now().astimezone().isoformat()


def md_table(headers: List[str], rows: List[List[Any]]) -> str:
    def esc(x: Any) -> str:
        s = "" if x is None else str(x)
        return s.replace("\n", " ").replace("|", "\\|")

    out = []
    out.append("| " + " | ".join(map(esc, headers)) + " |")
    out.append("|" + "|".join(["---"] * len(headers)) + "|")
    for r in rows:
        out.append("| " + " | ".join(esc(c) for c in r) + " |")
    return "\n".join(out)


def _safe_float(x: Any) -> Optional[float]:
    try:
        if x is None:
            return None
        if isinstance(x, (int, float)):
            return float(x)
        s = str(x).strip().replace(",", "")
        if not s:
            return None
        return float(s)
    except Exception:
        return None


def _load_costs_by_campaign_best_effort() -> Dict[str, float]:
    """Try to load a {campaign -> cost_usd} map from synced Sheets JSON.

    The repo currently has a trafik-canavari export, but it appears aggregated
    and not campaign-level. This function is defensive and returns {} when it
    cannot find a recognizable campaign-cost tab.
    """

    if not SHEETS_TRAFIK_JSON.exists():
        return {}

    try:
        with open(SHEETS_TRAFIK_JSON, "r", encoding="utf-8") as f:
            obj = json.load(f)
    except Exception:
        return {}

    costs: Dict[str, float] = {}

    tabs = obj.get("tabs")
    if not isinstance(tabs, dict):
        return {}

    for _tab_name, tab in tabs.items():
        rows = None
        # sheets_sync.py format
        if isinstance(tab, dict) and isinstance(tab.get("rows"), list):
            rows = tab.get("rows")
        # custom parser format
        elif isinstance(tab, dict) and isinstance(tab.get("data"), list):
            rows = tab.get("data")

        if not isinstance(rows, list):
            continue

        for r in rows:
            if not isinstance(r, dict):
                continue

            keys_l = {str(k).strip().lower(): k for k in r.keys()}

            campaign_key = None
            for k in ["campaign", "campaign name", "kampanya", "ad name", "adset", "ad set"]:
                if k in keys_l:
                    campaign_key = keys_l[k]
                    break

            cost_key = None
            for k in ["cost", "spend", "amount", "usd", "cost_usd", "spend_usd"]:
                if k in keys_l:
                    cost_key = keys_l[k]
                    break

            if not campaign_key or not cost_key:
                continue

            camp = str(r.get(campaign_key) or "").strip()
            cost = _safe_float(r.get(cost_key))
            if camp and cost is not None:
                costs[camp] = costs.get(camp, 0.0) + float(cost)

    return costs


@dataclass
class CampaignRow:
    country: str
    date_start: date
    date_end: date
    media_source: str
    campaign: str
    installs: int
    cost_usd: Optional[float] = None
    cpi_usd: Optional[float] = None


def main() -> None:
    client = bigquery.Client(project=PROJECT_ID)

    cov_q = f"""
    SELECT MIN(date) AS min_date, MAX(date) AS max_date, COUNT(DISTINCT date) AS day_count
    FROM `{TABLE_DAILY}`
    """
    cov = list(client.query(cov_q))[0]
    min_date: date = cov["min_date"]
    max_date: date = cov["max_date"]
    day_count: int = int(cov["day_count"])

    date_end = max_date
    desired_start = max_date - timedelta(days=6)
    date_start = max(min_date, desired_start)
    days_in_range = (date_end - date_start).days + 1

    q = f"""
    SELECT media_source, campaign, SUM(installs) AS installs
    FROM `{TABLE_DAILY}`
    WHERE date BETWEEN @start_date AND @end_date
    GROUP BY 1, 2
    """
    job = client.query(
        q,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("start_date", "DATE", date_start),
                bigquery.ScalarQueryParameter("end_date", "DATE", date_end),
            ]
        ),
    )
    rows = list(job)

    # Aggregate (defensive; query already groups)
    agg: Dict[Tuple[str, str], int] = defaultdict(int)
    for r in rows:
        media = (r.get("media_source") or "(blank)").strip()
        camp = (r.get("campaign") or "(blank)").strip()
        inst = int(r.get("installs") or 0)
        agg[(media, camp)] += inst

    costs_by_campaign = _load_costs_by_campaign_best_effort()

    out_rows: List[CampaignRow] = []
    for (media, camp), installs in agg.items():
        cost = costs_by_campaign.get(camp)
        cpi = (float(cost) / installs) if (cost is not None and installs > 0) else None
        out_rows.append(
            CampaignRow(
                country="TR",
                date_start=date_start,
                date_end=date_end,
                media_source=media,
                campaign=camp,
                installs=installs,
                cost_usd=round(cost, 2) if cost is not None else None,
                cpi_usd=round(cpi, 4) if cpi is not None else None,
            )
        )

    out_rows.sort(key=lambda r: r.installs, reverse=True)

    # ---- JSON
    json_obj = {
        "metadata": {
            "source": "BigQuery AppsFlyer daily_installs_campaign_tr",
            "table": TABLE_DAILY,
            "country": "TR",
            "dateStart": date_start.isoformat(),
            "dateEnd": date_end.isoformat(),
            "days": days_in_range,
            "generatedAt": _now_trt_iso(),
            "bqCoverage": {
                "minDate": min_date.isoformat(),
                "maxDate": max_date.isoformat(),
                "distinctDayCount": day_count,
            },
            "costJoin": {
                "attempted": True,
                "costRowsFound": len(costs_by_campaign),
                "note": "Best-effort scan of sheets-trafik-canavari.json for campaign-level cost/spend."
                if costs_by_campaign
                else "No campaign-level cost source detected in synced sheets; cost_usd/cpi_usd are null.",
            },
        },
        "campaigns": [
            {
                "country": r.country,
                "dateStart": r.date_start.isoformat(),
                "dateEnd": r.date_end.isoformat(),
                "dateRange": f"{r.date_start.isoformat()}..{r.date_end.isoformat()}",
                "media_source": r.media_source,
                "campaign": r.campaign,
                "installs": r.installs,
                "cost_usd": r.cost_usd,
                "cpi_usd": r.cpi_usd,
            }
            for r in out_rows
        ],
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(json_obj, f, ensure_ascii=False, indent=2)

    # ---- Markdown
    top_n = 30
    top = out_rows[:top_n]

    # Media source totals
    by_media: Dict[str, int] = defaultdict(int)
    for r in out_rows:
        by_media[r.media_source] += r.installs

    media_rows = [[m, v] for m, v in sorted(by_media.items(), key=lambda kv: kv[1], reverse=True)]

    md_lines: List[str] = []
    md_lines.append(f"# BigQuery Campaign Table (Latest {days_in_range} Days; max 7)")
    md_lines.append("")
    md_lines.append(f"**Country:** TR (table is TR-only)")
    md_lines.append(f"**Date range:** {date_start.isoformat()} → {date_end.isoformat()} (inclusive)")
    md_lines.append(f"**Generated at:** {_now_trt_iso()}")
    md_lines.append("")
    md_lines.append("## BigQuery coverage")
    md_lines.append(
        f"- daily_installs_campaign_tr: min={min_date.isoformat()}, max={max_date.isoformat()}, distinct days={day_count}"
    )
    md_lines.append("")

    md_lines.append("## Media source totals (installs)")
    md_lines.append("")
    md_lines.append(md_table(["media_source", "installs"], media_rows))
    md_lines.append("")

    md_lines.append(f"## Top {min(top_n, len(out_rows))} campaigns by installs")
    md_lines.append("")
    md_lines.append(
        md_table(
            ["rank", "media_source", "campaign", "installs", "cost_usd", "cpi_usd"],
            [
                [
                    i + 1,
                    r.media_source,
                    r.campaign,
                    r.installs,
                    r.cost_usd,
                    r.cpi_usd,
                ]
                for i, r in enumerate(top)
            ],
        )
    )
    md_lines.append("")

    if not costs_by_campaign:
        md_lines.append("## CPI join (Sheets)")
        md_lines.append("")
        md_lines.append(
            "Tried to detect campaign-level cost/spend in `data/sheets-trafik-canavari.json`, "
            "but the synced export appears aggregated (no campaign dimension). "
            "So `cost_usd` / `cpi_usd` are currently **null** in the JSON."
        )
        md_lines.append("")

    md_lines.append("## How to reproduce")
    md_lines.append("")
    md_lines.append("```bash")
    md_lines.append("source ~/.openclaw/venv/bin/activate")
    md_lines.append(
        "GOOGLE_APPLICATION_CREDENTIALS=~/.openclaw/credentials/cenoa-marketingdatawarehouse-82b8600e66d6.json \\\n  python3 projects/cenoa-growth-engine/scripts/bq_campaign_table_latest.py"
    )
    md_lines.append("```")
    md_lines.append("")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print(f"✅ Wrote {OUT_JSON.relative_to(REPO_ROOT)}")
    print(f"✅ Wrote {OUT_MD.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
