#!/usr/bin/env python3
"""BigQuery campaign trends (last 30 days) + budget misalignment snapshot.

Outputs:
- analysis/bq-campaign-trends-30d.md
- data/bq-campaign-trends-30d.json

Auth:
  source ~/.openclaw/venv/bin/activate
  GOOGLE_APPLICATION_CREDENTIALS=~/.openclaw/credentials/cenoa-marketingdatawarehouse-82b8600e66d6.json \
    python3 scripts/bq_campaign_trends_30d.py
"""

from __future__ import annotations

import json
import math
import os
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from google.cloud import bigquery

PROJECT_ID = "cenoa-marketingdatawarehouse"
DATASET = "marketing_appsflyer"
TABLE_DAILY = f"{PROJECT_ID}.{DATASET}.daily_installs_campaign_tr"
TABLE_WEEKLY = f"{PROJECT_ID}.{DATASET}.weekly_combined_totals"

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_MD = REPO_ROOT / "analysis" / "bq-campaign-trends-30d.md"
OUT_JSON = REPO_ROOT / "data" / "bq-campaign-trends-30d.json"

BUDGET_TRACKING_JSON = REPO_ROOT / "data" / "sheets-budget-tracking.json"


def iso_week(d: date) -> str:
    # BigQuery uses ISO week with %G-W%V.
    iso_year, iso_week_num, _ = d.isocalendar()
    return f"{iso_year}-W{iso_week_num:02d}"


def pct_change(curr: int, prev: int) -> Optional[float]:
    if prev == 0:
        return None
    return (curr - prev) / prev


def trend_label(wow: Optional[float], curr: int, prev: int) -> str:
    if prev == 0 and curr > 0:
        return "NEW"
    if prev == 0 and curr == 0:
        return "FLAT"
    if wow is None:
        return "NA"
    if wow >= 0.10:
        return "UP"
    if wow <= -0.10:
        return "DOWN"
    return "FLAT"


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


@dataclass
class CampaignAgg:
    campaign: str
    media_source: str
    installs_total: int
    installs_curr_week: int
    installs_prev_week: int
    wow_pct: Optional[float]
    trend: str
    platform_installs: Dict[str, int]


def main() -> None:
    client = bigquery.Client(project=PROJECT_ID)

    # ---- Daily table coverage
    coverage_q = f"""
    SELECT MIN(date) AS min_date, MAX(date) AS max_date, COUNT(DISTINCT date) AS day_count
    FROM `{TABLE_DAILY}`
    """
    cov = list(client.query(coverage_q))[0]
    min_date: date = cov["min_date"]
    max_date: date = cov["max_date"]
    day_count: int = cov["day_count"]

    desired_start = max_date - timedelta(days=29)
    start_date = max(min_date, desired_start)

    base_q = f"""
    SELECT date, platform, media_source, campaign, installs
    FROM `{TABLE_DAILY}`
    WHERE date BETWEEN @start_date AND @end_date
    """
    job = client.query(
        base_q,
        job_config=bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
                bigquery.ScalarQueryParameter("end_date", "DATE", max_date),
            ]
        ),
    )
    rows = list(job)

    # Determine ISO weeks present in daily data
    weeks = sorted({iso_week(r["date"]) for r in rows}, reverse=True)
    curr_week = weeks[0] if weeks else None
    prev_week = weeks[1] if len(weeks) >= 2 else None

    # Aggregate by campaign
    camp_total: Dict[str, int] = defaultdict(int)
    camp_media: Dict[str, str] = {}
    camp_week: Dict[Tuple[str, str], int] = defaultdict(int)
    camp_platform: Dict[Tuple[str, str], int] = defaultdict(int)

    for r in rows:
        camp = (r["campaign"] or "(blank)").strip()
        media = (r["media_source"] or "(blank)").strip()
        plat = (r["platform"] or "(blank)").strip()
        inst = int(r["installs"] or 0)
        wk = iso_week(r["date"])

        camp_total[camp] += inst
        if camp not in camp_media:
            camp_media[camp] = media
        camp_week[(camp, wk)] += inst
        camp_platform[(camp, plat)] += inst

    # Top campaigns (up to 20)
    top_campaigns = sorted(camp_total.items(), key=lambda kv: kv[1], reverse=True)[:20]
    campaign_aggs: List[CampaignAgg] = []
    for camp, total in top_campaigns:
        curr = camp_week.get((camp, curr_week), 0) if curr_week else 0
        prev = camp_week.get((camp, prev_week), 0) if prev_week else 0
        wow = pct_change(curr, prev)
        tlabel = trend_label(wow, curr, prev)
        plat_map: Dict[str, int] = {}
        for (c, p), v in camp_platform.items():
            if c == camp:
                plat_map[p] = v
        campaign_aggs.append(
            CampaignAgg(
                campaign=camp,
                media_source=camp_media.get(camp, ""),
                installs_total=total,
                installs_curr_week=curr,
                installs_prev_week=prev,
                wow_pct=wow,
                trend=tlabel,
                platform_installs=dict(sorted(plat_map.items(), key=lambda kv: kv[1], reverse=True)),
            )
        )

    # Rising / falling (only where prev_week > 0 and WoW computable)
    comparable = [c for c in campaign_aggs if c.installs_prev_week > 0 and c.wow_pct is not None]
    rising_candidates = [c for c in comparable if (c.wow_pct or 0) >= 0.10]
    falling_candidates = [c for c in comparable if (c.wow_pct or 0) <= -0.10]
    rising = sorted(rising_candidates, key=lambda c: c.wow_pct or -999, reverse=True)[:5]
    falling = sorted(falling_candidates, key=lambda c: c.wow_pct or 999)[:5]

    # Overall splits from daily table
    by_media = defaultdict(int)
    by_platform = defaultdict(int)
    for r in rows:
        by_media[(r["media_source"] or "(blank)").strip()] += int(r["installs"] or 0)
        by_platform[(r["platform"] or "(blank)").strip()] += int(r["installs"] or 0)

    # ---- Weekly combined totals (country/platform/channel)
    weekly_q = f"SELECT week, platform, country, channel, installs FROM `{TABLE_WEEKLY}`"
    weekly_rows = list(client.query(weekly_q))
    weekly_weeks = sorted({r["week"] for r in weekly_rows}, reverse=True)
    weekly_curr = weekly_weeks[0] if weekly_weeks else None
    weekly_prev = weekly_weeks[1] if len(weekly_weeks) >= 2 else None

    # Weekly country totals
    week_country = defaultdict(int)  # (week,country) -> installs
    week_country_platform = defaultdict(int)  # (week,country,platform) -> installs
    week_channel_country = defaultdict(int)  # (week,country,channel) -> installs
    week_channel_tr = defaultdict(int)  # (week,channel) -> installs for TR
    week_platform_tr = defaultdict(int)  # (week,platform) -> installs for TR

    for r in weekly_rows:
        wk = r["week"]
        ctry = (r["country"] or "(blank)").strip()
        ch = (r["channel"] or "(blank)").strip()
        plat = (r["platform"] or "(blank)").strip()
        inst = int(r["installs"] or 0)

        week_country[(wk, ctry)] += inst
        week_country_platform[(wk, ctry, plat)] += inst
        week_channel_country[(wk, ctry, ch)] += inst
        if ctry == "TR":
            week_channel_tr[(wk, ch)] += inst
            week_platform_tr[(wk, plat)] += inst

    # ---- Spend allocations (from already-exported JSON)
    spend: Dict[str, Any] = {}
    if BUDGET_TRACKING_JSON.exists():
        spend = json.loads(BUDGET_TRACKING_JSON.read_text(encoding="utf-8"))

    march_tr_plan = (spend.get("marchBudget2026") or {}).get("channelByCountryTR") or {}
    feb_tr_realized = ((spend.get("realizedCostFeb2026") or {}).get("channelBreakdown") or {}).get("TR") or {}

    # Misalignment heuristic: top planned spend channels where TR installs WoW is DOWN
    # using weekly_combined_totals (W12 vs W11).
    channel_map_plan = {
        "google": "Google",
        "meta": "Meta",
        "apple_ads": "AppleSearchAds",
        "AppNext": "SpazeAppnext",
        "referral_affi": "AffiliateRAFCRM",
        # other/partner -> InfluencerOther by default
        "other": "InfluencerOther",
        "partner": "InfluencerOther",
    }

    # Compute TR installs WoW per channel/platform (weekly table)
    tr_channel_metrics = []
    channels_in_weekly = sorted({ch for (_wk, ch) in week_channel_tr.keys()})
    for ch in channels_in_weekly:
        curr_i = week_channel_tr.get((weekly_curr, ch), 0) if weekly_curr else 0
        prev_i = week_channel_tr.get((weekly_prev, ch), 0) if weekly_prev else 0
        wow = pct_change(curr_i, prev_i)
        tr_channel_metrics.append(
            {
                "channel_weekly": ch,
                "channel_plan_key": channel_map_plan.get(ch),
                "installs_curr_week": curr_i,
                "installs_prev_week": prev_i,
                "wow_pct": wow,
                "trend": trend_label(wow, curr_i, prev_i),
            }
        )

    tr_platform_metrics = []
    platforms_in_weekly = sorted({p for (_wk, p) in week_platform_tr.keys()})
    for p in platforms_in_weekly:
        curr_i = week_platform_tr.get((weekly_curr, p), 0) if weekly_curr else 0
        prev_i = week_platform_tr.get((weekly_prev, p), 0) if weekly_prev else 0
        wow = pct_change(curr_i, prev_i)
        tr_platform_metrics.append(
            {
                "platform": p,
                "installs_curr_week": curr_i,
                "installs_prev_week": prev_i,
                "wow_pct": wow,
                "trend": trend_label(wow, curr_i, prev_i),
            }
        )

    # Determine top planned spend keys
    plan_items = [(k, v) for k, v in march_tr_plan.items() if k not in ("total",) and isinstance(v, (int, float))]
    plan_items_sorted = sorted(plan_items, key=lambda kv: kv[1], reverse=True)
    top_plan_keys = [k for k, _ in plan_items_sorted[:5]]

    misalign_flags = []
    for m in tr_channel_metrics:
        plan_key = m.get("channel_plan_key")
        if not plan_key:
            continue
        if plan_key in top_plan_keys and m["trend"] == "DOWN":
            misalign_flags.append(
                {
                    "plan_channel": plan_key,
                    "weekly_channel": m["channel_weekly"],
                    "planned_budget": march_tr_plan.get(plan_key),
                    "installs_curr_week": m["installs_curr_week"],
                    "installs_prev_week": m["installs_prev_week"],
                    "wow_pct": m["wow_pct"],
                    "note": "High planned spend channel shows installs down WoW (weekly table).",
                }
            )

    # ---- Build markdown
    generated_at = datetime.now(timezone.utc).isoformat()
    md_parts = []
    md_parts.append("# BigQuery — Campaign Trends (Last 30 Days)\n")
    md_parts.append(f"Generated: `{generated_at}`\n")
    md_parts.append("## Data coverage & caveats\n")
    md_parts.append(
        "- Source tables:\n"
        f"  - `{TABLE_DAILY}` (campaign-level, TR-only, daily)\n"
        f"  - `{TABLE_WEEKLY}` (country/platform/channel, weekly)\n"
        f"- Daily table available range: **{min_date} → {max_date}** (**{day_count} distinct days**)\n"
        f"- Requested window = last 30 days; effective window used = **{start_date} → {max_date}** (limited by data availability)\n"
    )
    if curr_week and prev_week:
        md_parts.append(f"- Week-over-week for campaigns uses ISO weeks: **{curr_week} vs {prev_week}** (note: current week may be partial).\n")
    md_parts.append("\n")

    md_parts.append("## 1) Top campaigns by installs (Top 20) + WoW trend\n")
    t_rows = []
    for c in campaign_aggs:
        wow_str = "" if c.wow_pct is None else f"{c.wow_pct*100:.1f}%"
        plat_str = ", ".join([f"{p}:{v}" for p, v in c.platform_installs.items()])
        t_rows.append(
            [
                c.campaign,
                c.media_source,
                c.installs_total,
                c.installs_curr_week,
                c.installs_prev_week,
                wow_str,
                c.trend,
                plat_str,
            ]
        )
    md_parts.append(
        md_table(
            [
                "Campaign",
                "Media source",
                "Installs (window)",
                f"Installs ({curr_week})" if curr_week else "Installs (curr week)",
                f"Installs ({prev_week})" if prev_week else "Installs (prev week)",
                "WoW %",
                "Trend",
                "Platform split",
            ],
            t_rows,
        )
    )
    md_parts.append("\n\n")

    md_parts.append("### Rising / Falling (campaigns with comparable WoW)\n")
    if not comparable:
        md_parts.append(
            "Not enough history in the daily campaign table to compute meaningful WoW for most campaigns (previous week is 0 / missing).\n"
        )
    else:
        md_parts.append("**Rising (WoW ≥ +10%):**\n")
        if not rising:
            md_parts.append("- (none)\n")
        else:
            md_parts.append(
                "\n".join(
                    [
                        f"- {c.campaign} — {c.installs_prev_week}→{c.installs_curr_week} ({(c.wow_pct or 0)*100:.1f}%)"
                        for c in rising
                    ]
                )
                + "\n"
            )
        md_parts.append("\n**Falling (WoW ≤ -10%):**\n")
        if not falling:
            md_parts.append("- (none)\n")
        else:
            md_parts.append(
                "\n".join(
                    [
                        f"- {c.campaign} — {c.installs_prev_week}→{c.installs_curr_week} ({(c.wow_pct or 0)*100:.1f}%)"
                        for c in falling
                    ]
                )
                + "\n"
            )
    md_parts.append("\n")

    md_parts.append("## 2) Splits (where available)\n")

    md_parts.append("### Daily table (TR) — installs by media_source\n")
    media_rows = [[k, v] for k, v in sorted(by_media.items(), key=lambda kv: kv[1], reverse=True)]
    md_parts.append(md_table(["media_source", "installs"], media_rows))
    md_parts.append("\n\n")

    md_parts.append("### Daily table (TR) — installs by platform\n")
    plat_rows = [[k, v] for k, v in sorted(by_platform.items(), key=lambda kv: kv[1], reverse=True)]
    md_parts.append(md_table(["platform", "installs"], plat_rows))
    md_parts.append("\n\n")

    md_parts.append("### Weekly table — country split (installs)\n")
    if weekly_curr and weekly_prev:
        ctries = sorted({ctry for (wk, ctry) in week_country.keys()})
        rows_ctry = []
        for ctry in ctries:
            curr_i = week_country.get((weekly_curr, ctry), 0)
            prev_i = week_country.get((weekly_prev, ctry), 0)
            wow = pct_change(curr_i, prev_i)
            wow_s = "" if wow is None else f"{wow*100:.1f}%"
            rows_ctry.append([ctry, prev_i, curr_i, wow_s, trend_label(wow, curr_i, prev_i)])
        rows_ctry.sort(key=lambda r: r[2], reverse=True)
        md_parts.append(md_table(["Country", f"Installs ({weekly_prev})", f"Installs ({weekly_curr})", "WoW %", "Trend"], rows_ctry))
    else:
        md_parts.append("Weekly table does not contain >=2 weeks of data; cannot compute WoW.\n")
    md_parts.append("\n\n")

    md_parts.append("### Weekly table — TR channel WoW (for spend alignment)\n")
    if weekly_curr and weekly_prev:
        tr_rows = []
        for m in sorted(tr_channel_metrics, key=lambda x: x["installs_curr_week"], reverse=True):
            wow = m["wow_pct"]
            wow_s = "" if wow is None else f"{wow*100:.1f}%"
            tr_rows.append(
                [
                    m["channel_weekly"],
                    m.get("channel_plan_key") or "(unmapped)",
                    m["installs_prev_week"],
                    m["installs_curr_week"],
                    wow_s,
                    m["trend"],
                ]
            )
        md_parts.append(md_table(["Weekly channel", "Mapped plan channel", f"Installs ({weekly_prev})", f"Installs ({weekly_curr})", "WoW %", "Trend"], tr_rows))

        md_parts.append("\n\n### Weekly table — TR platform split (installs)\n")
        platforms = sorted({p for (_wk, p) in week_platform_tr.keys()})
        plat_rows_tr = []
        for p in platforms:
            curr_i = week_platform_tr.get((weekly_curr, p), 0)
            prev_i = week_platform_tr.get((weekly_prev, p), 0)
            wow = pct_change(curr_i, prev_i)
            wow_s = "" if wow is None else f"{wow*100:.1f}%"
            plat_rows_tr.append([p, prev_i, curr_i, wow_s, trend_label(wow, curr_i, prev_i)])
        plat_rows_tr.sort(key=lambda r: r[2], reverse=True)
        md_parts.append(md_table(["Platform", f"Installs ({weekly_prev})", f"Installs ({weekly_curr})", "WoW %", "Trend"], plat_rows_tr))

    md_parts.append("\n\n")

    md_parts.append("## 3) Spend vs installs — misalignment flags (Sheets snapshot)\n")
    md_parts.append(
        "Spend source: `data/sheets-budget-tracking.json` (exported from Google Sheets).\n\n"
        "Heuristic used: flag channels with **top planned March TR budget** where **TR installs are DOWN WoW** in weekly table.\n"
    )

    if not march_tr_plan:
        md_parts.append("- No March TR plan found in sheets-budget-tracking.json\n")
    else:
        plan_rows = [[k, v] for k, v in plan_items_sorted]
        md_parts.append("\n### March TR planned channel budget\n")
        md_parts.append(md_table(["Plan channel", "Planned budget (USD)"] , plan_rows))
        md_parts.append("\n\n")

    if misalign_flags:
        rows_m = []
        for f in misalign_flags:
            wow_s = "" if f["wow_pct"] is None else f"{f['wow_pct']*100:.1f}%"
            rows_m.append([
                f["plan_channel"],
                f["weekly_channel"],
                f.get("planned_budget"),
                f["installs_prev_week"],
                f["installs_curr_week"],
                wow_s,
                f["note"],
            ])
        md_parts.append("\n### Potential misalignments (review)\n")
        md_parts.append(md_table(["Plan channel", "Weekly channel", "Planned budget", f"Installs ({weekly_prev})", f"Installs ({weekly_curr})", "WoW %", "Note"], rows_m))
        md_parts.append("\n")
    else:
        md_parts.append("\nNo misalignment flags triggered by the heuristic (or insufficient weekly data).\n")

    md_parts.append("\n## 4) Notes / next improvements\n")
    md_parts.append(
        "- The daily campaign table currently contains only **6 days** of data (2026-02-25→2026-03-02), so \n"
        "  campaign WoW is based on **partial weeks** (2026-W10 is only 1 day). Treat campaign trend labels as directional only.\n"
        "- If/when the daily table is extended (>=30 days), this script will automatically produce true 7-day vs prior-7-day WoW.\n"
        "- Weekly country/channel table currently includes only **2 weeks** (W11, W12). As more weeks land, the analysis becomes more stable.\n"
    )
    md_parts.append("\n")

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(md_parts), encoding="utf-8")

    # ---- JSON output
    out = {
        "generated_at": generated_at,
        "sources": {
            "daily_table": TABLE_DAILY,
            "weekly_table": TABLE_WEEKLY,
            "budget_sheet_export": str(BUDGET_TRACKING_JSON),
        },
        "daily_coverage": {
            "min_date": str(min_date),
            "max_date": str(max_date),
            "distinct_days": day_count,
            "requested_30d_start": str(desired_start),
            "effective_start": str(start_date),
            "effective_end": str(max_date),
            "iso_weeks_present": weeks,
            "curr_iso_week": curr_week,
            "prev_iso_week": prev_week,
        },
        "top_campaigns": [
            {
                "campaign": c.campaign,
                "media_source": c.media_source,
                "installs_total": c.installs_total,
                "installs_curr_week": c.installs_curr_week,
                "installs_prev_week": c.installs_prev_week,
                "wow_pct": c.wow_pct,
                "trend": c.trend,
                "platform_installs": c.platform_installs,
            }
            for c in campaign_aggs
        ],
        "rising_campaigns": [c.campaign for c in rising],
        "falling_campaigns": [c.campaign for c in falling],
        "splits": {
            "daily_by_media_source": dict(sorted(by_media.items(), key=lambda kv: kv[1], reverse=True)),
            "daily_by_platform": dict(sorted(by_platform.items(), key=lambda kv: kv[1], reverse=True)),
            "weekly_weeks_present": weekly_weeks,
            "weekly_country_totals": {
                wk: {ctry: week_country.get((wk, ctry), 0) for ctry in sorted({c for (_w, c) in week_country.keys() if _w == wk})}
                for wk in weekly_weeks
            },
            "weekly_tr_channel_wow": tr_channel_metrics,
            "weekly_tr_platform_wow": tr_platform_metrics,
        },
        "spend": {
            "march_tr_plan": march_tr_plan,
            "feb_tr_realized": feb_tr_realized,
        },
        "misalignment_flags": misalign_flags,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Wrote: {OUT_MD}")
    print(f"Wrote: {OUT_JSON}")


if __name__ == "__main__":
    main()
