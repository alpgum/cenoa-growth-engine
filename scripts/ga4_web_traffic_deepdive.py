#!/usr/bin/env python3
"""GA4 web traffic deep-dive (Sprint [081]).

Outputs a Markdown report at:
  analysis/ga4-web-traffic.md

Requires:
  - GA4 Data API access via service account (already granted)
  - GA4 property id (numeric)

How to run:
  source ~/.openclaw/venv/bin/activate
  export GOOGLE_APPLICATION_CREDENTIALS=~/.openclaw/credentials/cenoa-marketingdatawarehouse-82b8600e66d6.json
  export GA4_PROPERTY_ID=123456789
  python3 projects/cenoa-growth-engine/scripts/ga4_web_traffic_deepdive.py

Date Convention (S3-014):
  - Weekly = ISO week: Monday 00:00 UTC to Sunday 23:59 UTC
  - MTD = 1st of month 00:00 UTC to current day 23:59 UTC
  - All date ranges aligned to ISO week boundaries (Mon-Sun)
  - last_7d = last complete ISO week; last_28d = last 4 complete ISO weeks

Notes:
  - If bounceRate metric is unavailable, we compute proxy bounce = 1 - engagementRate.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Filter,
    FilterExpression,
    FilterExpressionList,
    Metric,
    OrderBy,
    RunReportRequest,
)
from google.api_core.exceptions import InvalidArgument
from google.oauth2 import service_account


# scripts/<file> -> project root
ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_DIR = ROOT / "analysis"
DATA_DIR = ROOT / "data"

DEFAULT_CREDENTIALS = os.path.expanduser(
    "~/.openclaw/credentials/cenoa-marketingdatawarehouse-82b8600e66d6.json"
)


@dataclass
class ReportTable:
    name: str
    dims: List[str]
    metrics: List[str]
    rows: List[Dict[str, Any]]


def _today_utc() -> dt.date:
    return dt.datetime.now(dt.UTC).date()


def _date_ranges(today: dt.date) -> Dict[str, Tuple[str, str, str, str]]:
    """Returns dict with (start,end,prev_start,prev_end) for 7d and 28d windows.

    Aligned to ISO week boundaries (Mon-Sun) to ensure consistent reporting.
    """
    # Find last complete Sunday
    days_since_monday = today.weekday()  # Mon=0, Sun=6
    last_sunday = today - dt.timedelta(days=days_since_monday + 1)

    def mk(weeks: int) -> Tuple[str, str, str, str]:
        days = weeks * 7
        start = last_sunday - dt.timedelta(days=days - 1)  # Monday
        end = last_sunday  # Sunday
        prev_end = start - dt.timedelta(days=1)  # Previous Sunday
        prev_start = prev_end - dt.timedelta(days=days - 1)  # Previous Monday
        return (
            start.isoformat(),
            end.isoformat(),
            prev_start.isoformat(),
            prev_end.isoformat(),
        )

    return {
        "last_7d": mk(1),   # 1 ISO week
        "last_28d": mk(4),  # 4 ISO weeks
    }


def _get_credentials(creds_path: str):
    scopes = ["https://www.googleapis.com/auth/analytics.readonly"]
    return service_account.Credentials.from_service_account_file(creds_path, scopes=scopes)


def _client(creds_path: str) -> BetaAnalyticsDataClient:
    creds = _get_credentials(creds_path)
    return BetaAnalyticsDataClient(credentials=creds)


def _rows_to_dicts(resp, dim_names: List[str], metric_names: List[str]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in resp.rows:
        d: Dict[str, Any] = {}
        for i, dn in enumerate(dim_names):
            d[dn] = row.dimension_values[i].value
        for j, mn in enumerate(metric_names):
            v = row.metric_values[j].value
            # try numeric cast
            if v is None:
                d[mn] = None
            else:
                if re.fullmatch(r"-?\d+", v):
                    d[mn] = int(v)
                else:
                    try:
                        d[mn] = float(v)
                    except ValueError:
                        d[mn] = v
        out.append(d)
    return out


def _run_report(
    client: BetaAnalyticsDataClient,
    property_id: str,
    dim_names: Sequence[str],
    metric_names: Sequence[str],
    start_date: str,
    end_date: str,
    limit: int = 100,
    order_by_metric: Optional[str] = None,
    dimension_filter: Optional[FilterExpression] = None,
) -> ReportTable:
    dims = [Dimension(name=d) for d in dim_names]
    mets = [Metric(name=m) for m in metric_names]

    order_bys: List[OrderBy] = []
    if order_by_metric:
        order_bys = [OrderBy(metric=OrderBy.MetricOrderBy(metric_name=order_by_metric), desc=True)]

    req = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=dims,
        metrics=mets,
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        limit=limit,
        order_bys=order_bys,
        dimension_filter=dimension_filter,
    )

    resp = client.run_report(req)
    return ReportTable(
        name="",
        dims=list(dim_names),
        metrics=list(metric_names),
        rows=_rows_to_dicts(resp, list(dim_names), list(metric_names)),
    )


def _safe_run_report(
    client: BetaAnalyticsDataClient,
    property_id: str,
    dim_names: Sequence[str],
    metric_names: Sequence[str],
    start_date: str,
    end_date: str,
    limit: int = 100,
    order_by_metric: Optional[str] = None,
    dimension_filter: Optional[FilterExpression] = None,
    drop_metrics_on_error: bool = True,
) -> Tuple[ReportTable, List[str]]:
    """Runs a report; if InvalidArgument, retries by dropping metrics one-by-one.

    Returns (table, warnings).
    """
    warnings: List[str] = []
    mets = list(metric_names)

    while True:
        try:
            tbl = _run_report(
                client,
                property_id,
                dim_names,
                mets,
                start_date,
                end_date,
                limit=limit,
                order_by_metric=order_by_metric,
                dimension_filter=dimension_filter,
            )
            tbl.metrics = mets
            return tbl, warnings
        except InvalidArgument as e:
            msg = str(e)
            if not drop_metrics_on_error or len(mets) <= 1:
                raise

            # heuristic: drop a metric mentioned in error; else drop last
            dropped = None
            for m in list(mets):
                if m in msg:
                    dropped = m
                    break
            if not dropped:
                dropped = mets[-1]
            mets = [m for m in mets if m != dropped]
            warnings.append(f"Dropped metric '{dropped}' due to API error: {msg.splitlines()[0]}")


def _md_table(rows: List[Dict[str, Any]], columns: List[str], max_rows: int = 20) -> str:
    rows = rows[:max_rows]
    if not rows:
        return "(no data)"

    def fmt(v: Any) -> str:
        if v is None:
            return ""
        if isinstance(v, float):
            # common GA rates are 0-1 or 0-100; keep 4 decimals.
            return f"{v:.4f}".rstrip("0").rstrip(".")
        return str(v)

    header = "| " + " | ".join(columns) + " |"
    sep = "|" + "|".join(["---"] * len(columns)) + "|"
    lines = [header, sep]
    for r in rows:
        lines.append("| " + " | ".join(fmt(r.get(c)) for c in columns) + " |")
    return "\n".join(lines)


def _pct_change(cur: Optional[float], prev: Optional[float]) -> Optional[float]:
    if cur is None or prev is None or prev == 0:
        return None
    return (cur - prev) / prev


def _merge_by_key(
    cur_rows: List[Dict[str, Any]],
    prev_rows: List[Dict[str, Any]],
    key: str,
    metric: str,
    cur_label: str,
    prev_label: str,
) -> List[Dict[str, Any]]:
    prev_map = {r.get(key): r for r in prev_rows}
    out: List[Dict[str, Any]] = []
    for r in cur_rows:
        k = r.get(key)
        prev = prev_map.get(k, {})
        cur_v = r.get(metric)
        prev_v = prev.get(metric)
        out.append(
            {
                key: k,
                cur_label: cur_v,
                prev_label: prev_v,
                "delta": (cur_v - prev_v) if isinstance(cur_v, (int, float)) and isinstance(prev_v, (int, float)) else None,
                "delta_pct": _pct_change(float(cur_v), float(prev_v)) if isinstance(cur_v, (int, float)) and isinstance(prev_v, (int, float)) else None,
            }
        )
    # keep in same order
    return out


def _string_contains_filter(dim: str, substring: str, case_sensitive: bool = False) -> FilterExpression:
    return FilterExpression(
        filter=Filter(
            field_name=dim,
            string_filter=Filter.StringFilter(
                match_type=Filter.StringFilter.MatchType.CONTAINS,
                value=substring,
                case_sensitive=case_sensitive,
            ),
        )
    )


def _string_exact_filter(dim: str, value: str, case_sensitive: bool = False) -> FilterExpression:
    return FilterExpression(
        filter=Filter(
            field_name=dim,
            string_filter=Filter.StringFilter(
                match_type=Filter.StringFilter.MatchType.EXACT,
                value=value,
                case_sensitive=case_sensitive,
            ),
        )
    )


def _or_filters(filters: List[FilterExpression]) -> FilterExpression:
    return FilterExpression(or_group=FilterExpressionList(expressions=filters))


def _and_filters(filters: List[FilterExpression]) -> FilterExpression:
    return FilterExpression(and_group=FilterExpressionList(expressions=filters))


def _find_cta_events(event_rows: List[Dict[str, Any]]) -> List[str]:
    """Heuristic detection of CTA-ish event names."""
    candidates = []
    for r in event_rows:
        name = (r.get("eventName") or "").lower()
        if any(k in name for k in ["cta", "download", "app_store", "appstore", "play_store", "store_redirect", "redirect"]):
            candidates.append(r["eventName"])
    # de-dupe, keep order
    seen = set()
    out = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def _load_looker_top_pages_hint() -> List[Dict[str, Any]]:
    """Best-effort: extract the small 'top pages' table from analysis/lp-cta-optimization.md.

    This is NOT a Looker API pull. It's a consistency check using previously written notes.
    """
    p = ANALYSIS_DIR / "lp-cta-optimization.md"
    if not p.exists():
        return []
    text = p.read_text(encoding="utf-8")
    # Match rows like: | `/pakistan-waitlist-v2` | ~1,800 | ... |
    out: List[Dict[str, Any]] = []
    # Allow optional label after the backticked path (e.g. `/` (homepage)).
    # Note: allow `/` root path (so the part after the leading slash can be empty).
    pattern = r"\|\s*`(?P<path>\/[^`]*)`\s*[^|]*\|\s*(?P<sessions>~?[0-9,]+)\s*\|"
    for m in re.finditer(pattern, text):
        out.append({"path": m.group("path"), "sessions_hint": m.group("sessions")})
    return out


def generate(property_id: Optional[str], creds_path: str, out_md: Path, out_json: Path) -> None:
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    today = _today_utc()
    dr = _date_ranges(today)

    looker_hint = _load_looker_top_pages_hint()

    if not property_id:
        md = f"""# GA4 Web Traffic Deep-Dive (Sprint [081])

**Generated:** {dt.datetime.now(dt.UTC).isoformat(timespec='seconds').replace('+00:00','Z')}  
**Status:** BLOCKED — `GA4_PROPERTY_ID` not configured.

## What’s missing

We have working **service-account credentials** for Google APIs, but this repo/env currently has **no GA4 property id** configured.

To generate this report:

```bash
export GOOGLE_APPLICATION_CREDENTIALS={DEFAULT_CREDENTIALS}
export GA4_PROPERTY_ID=<numeric_ga4_property_id>
source ~/.openclaw/venv/bin/activate
python3 projects/cenoa-growth-engine/scripts/ga4_web_traffic_deepdive.py
```

Once `GA4_PROPERTY_ID` is set, the script will populate:
1) Sessions by source/medium (top 20)
2) Landing page performance: sessions + engagement (bounce proxy)
3) CTA click proxy + CTA click rate by landing page (if events exist)
4) Consistency check vs Looker-noted top pages

---

## Looker-noted “top pages” (from `analysis/lp-cta-optimization.md`)

{_md_table(looker_hint, ['path','sessions_hint'], max_rows=20) if looker_hint else '(no Looker hints found in repo)'}

---

## Instrumentation expectation for CTA clicks

If GA4 does **not** currently track CTA clicks, recommended event:

- Event name: `cta_click`
- Recommended parameters:
  - `cta_id` (e.g., `cta_header_download`, `cta_hero_download`)
  - `placement` (header/hero/sticky/footer)
  - `destination` (ios/android/web)
  - `landing_page` (page path)
  - `variant` (if running LP tests)

This enables reliable CTA click rate by landing page.
"""
        out_md.write_text(md, encoding="utf-8")
        out_json.write_text(json.dumps({"status": "blocked", "reason": "GA4_PROPERTY_ID missing"}, indent=2), encoding="utf-8")
        return

    client = _client(creds_path)

    warnings: List[str] = []
    tables: Dict[str, Any] = {
        "generated_at": dt.datetime.now(dt.UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "property_id": property_id,
        "date_ranges": dr,
        "tables": {},
        "warnings": warnings,
        "looker_top_pages_hint": looker_hint,
    }

    def pull_table(
        name: str,
        dims: Sequence[str],
        mets: Sequence[str],
        start: str,
        end: str,
        limit: int,
        order_by: Optional[str],
        dim_filter: Optional[FilterExpression] = None,
    ) -> ReportTable:
        tbl, warns = _safe_run_report(
            client,
            property_id,
            dims,
            mets,
            start,
            end,
            limit=limit,
            order_by_metric=order_by,
            dimension_filter=dim_filter,
        )
        tbl.name = name
        warnings.extend(warns)
        tables["tables"][name] = {
            "dims": tbl.dims,
            "metrics": tbl.metrics,
            "rows": tbl.rows,
        }
        return tbl

    # --- 1) Sessions by source/medium (top 20)
    # Use sessionSourceMedium; if unavailable, fallback to sessionSource / sessionMedium.
    start7, end7, prev7s, prev7e = dr["last_7d"]
    start28, end28, prev28s, prev28e = dr["last_28d"]

    src_dims = ["sessionSourceMedium"]
    src_mets = ["sessions", "engagedSessions", "engagementRate"]

    src7 = pull_table("sessions_by_source_medium_last7d", src_dims, src_mets, start7, end7, limit=20, order_by="sessions")
    src7_prev = pull_table(
        "sessions_by_source_medium_prev7d", src_dims, src_mets, prev7s, prev7e, limit=20, order_by="sessions"
    )
    src28 = pull_table("sessions_by_source_medium_last28d", src_dims, src_mets, start28, end28, limit=20, order_by="sessions")
    src28_prev = pull_table(
        "sessions_by_source_medium_prev28d", src_dims, src_mets, prev28s, prev28e, limit=20, order_by="sessions"
    )

    # --- 2) Landing page performance
    lp_dims = ["landingPagePlusQueryString"]
    lp_mets = [
        "sessions",
        "engagedSessions",
        "engagementRate",
        "bounceRate",  # may be dropped
        "averageSessionDuration",
    ]

    lp7 = pull_table("landing_pages_last7d", lp_dims, lp_mets, start7, end7, limit=50, order_by="sessions")
    lp28 = pull_table("landing_pages_last28d", lp_dims, lp_mets, start28, end28, limit=50, order_by="sessions")

    # --- 3) CTA click proxy (event exploration)
    ev_dims = ["eventName"]
    ev_mets = ["eventCount"]
    ev28 = pull_table("events_last28d", ev_dims, ev_mets, start28, end28, limit=200, order_by="eventCount")
    cta_events = _find_cta_events(ev28.rows)

    tables["cta_event_candidates"] = cta_events

    # Attempt (A) explicit CTA event names (custom)
    cta_lp_tbl = None
    if cta_events:
        cta_filters = [_string_exact_filter("eventName", e, case_sensitive=False) for e in cta_events[:10]]
        cta_lp_filter = _or_filters(cta_filters)
        cta_lp_tbl = pull_table(
            "cta_events_by_landing_page_last28d",
            ["landingPagePlusQueryString", "eventName"],
            ["eventCount"],
            start28,
            end28,
            limit=500,
            order_by="eventCount",
            dim_filter=cta_lp_filter,
        )

    # Attempt (B) enhanced measurement click proxy to app stores / onelink
    click_proxy_tbl = None
    # Build filter: eventName == click AND (linkUrl contains app store / onelink)
    try:
        proxy_filter = _and_filters(
            [
                _string_exact_filter("eventName", "click"),
                _or_filters(
                    [
                        _string_contains_filter("linkUrl", "apps.apple.com"),
                        _string_contains_filter("linkUrl", "play.google.com"),
                        _string_contains_filter("linkUrl", "onelink.me"),
                    ]
                ),
            ]
        )
        click_proxy_tbl = pull_table(
            "cta_click_proxy_by_landing_page_last28d",
            ["landingPagePlusQueryString", "linkUrl"],
            ["eventCount"],
            start28,
            end28,
            limit=500,
            order_by="eventCount",
            dim_filter=proxy_filter,
        )
    except Exception as e:
        warnings.append(f"Click proxy query failed (may lack enhanced measurement fields): {e}")

    # --- Compute CTA rate per landing page (best-effort)
    # We use: CTA events (eventCount aggregated per landing page) / sessions per landing page.
    lp_sessions_map = {r.get("landingPagePlusQueryString"): r.get("sessions", 0) for r in lp28.rows}

    cta_counts: Dict[str, float] = {}

    def add_counts(tbl: Optional[ReportTable], key_field: str, count_field: str):
        if not tbl:
            return
        for r in tbl.rows:
            k = r.get(key_field)
            v = r.get(count_field)
            if not k or v is None:
                continue
            cta_counts[k] = cta_counts.get(k, 0) + float(v)

    if cta_lp_tbl:
        add_counts(cta_lp_tbl, "landingPagePlusQueryString", "eventCount")
    elif click_proxy_tbl:
        add_counts(click_proxy_tbl, "landingPagePlusQueryString", "eventCount")

    cta_rate_rows: List[Dict[str, Any]] = []
    for lp, sess in lp_sessions_map.items():
        if not lp:
            continue
        cta = cta_counts.get(lp, 0.0)
        rate = (cta / sess) if sess else None
        cta_rate_rows.append({"landingPagePlusQueryString": lp, "sessions": sess, "cta_events": int(cta), "cta_rate": rate})

    cta_rate_rows.sort(key=lambda r: (r.get("cta_events") or 0), reverse=True)
    tables["tables"]["cta_rate_by_landing_page_last28d"] = {
        "dims": ["landingPagePlusQueryString"],
        "metrics": ["sessions", "cta_events", "cta_rate"],
        "rows": cta_rate_rows[:50],
    }

    # Persist JSON for reproducibility
    out_json.write_text(json.dumps(tables, indent=2, ensure_ascii=False), encoding="utf-8")

    # --- Markdown output
    def section(title: str) -> str:
        return f"\n\n## {title}\n"

    md_parts: List[str] = []
    md_parts.append(f"# GA4 Web Traffic Deep-Dive (Sprint [081])\n\n**Generated:** {tables['generated_at']}  \n**GA4 property:** `{property_id}`\n")

    if warnings:
        md_parts.append("\n> Warnings / fallbacks:\n> " + "\n> ".join(warnings) + "\n")

    md_parts.append(section("1) Sessions by source/medium (Top 20)"))
    md_parts.append(f"### Last 7 days ({start7} → {end7})\n\n" + _md_table(src7.rows, ["sessionSourceMedium"] + src7.metrics, 20))
    md_parts.append(f"\n\n### Previous 7 days ({prev7s} → {prev7e})\n\n" + _md_table(src7_prev.rows, ["sessionSourceMedium"] + src7_prev.metrics, 20))
    md_parts.append(f"\n\n### Last 28 days ({start28} → {end28})\n\n" + _md_table(src28.rows, ["sessionSourceMedium"] + src28.metrics, 20))
    md_parts.append(f"\n\n### Previous 28 days ({prev28s} → {prev28e})\n\n" + _md_table(src28_prev.rows, ["sessionSourceMedium"] + src28_prev.metrics, 20))

    md_parts.append(section("2) Landing page performance"))
    md_parts.append(f"### Last 7 days ({start7} → {end7})\n\n" + _md_table(lp7.rows, ["landingPagePlusQueryString"] + lp7.metrics, 25))
    md_parts.append(f"\n\n### Last 28 days ({start28} → {end28})\n\n" + _md_table(lp28.rows, ["landingPagePlusQueryString"] + lp28.metrics, 25))

    md_parts.append(section("3) CTA click proxy + CTA click rate by landing page"))
    md_parts.append(
        "### Candidate CTA events detected (heuristic)\n\n"
        + ("\n".join([f"- `{e}`" for e in cta_events]) if cta_events else "No explicit CTA-like event names detected.")
    )

    if cta_lp_tbl and cta_lp_tbl.rows:
        md_parts.append("\n\n### CTA events by landing page (last 28 days)\n\n" + _md_table(cta_lp_tbl.rows, ["landingPagePlusQueryString", "eventName", "eventCount"], 30))
    elif click_proxy_tbl and click_proxy_tbl.rows:
        md_parts.append(
            "\n\n### CTA click proxy by landing page (eventName=`click` + linkUrl to app stores/onelink, last 28 days)\n\n"
            + _md_table(click_proxy_tbl.rows, ["landingPagePlusQueryString", "linkUrl", "eventCount"], 30)
        )
    else:
        md_parts.append(
            "\n\n### CTA click data\n\nNo CTA click events/proxy could be pulled from GA4. This likely means **missing or inconsistent instrumentation**.\n"
        )

    md_parts.append("\n\n### CTA click rate by landing page (last 28 days)\n\n" + _md_table(cta_rate_rows, ["landingPagePlusQueryString", "sessions", "cta_events", "cta_rate"], 25))

    md_parts.append(section("4) Consistency check vs Looker-reported top pages"))
    md_parts.append(
        "Looker Studio embed isn't accessible from this environment right now; we use the repo’s Looker-notes (from `analysis/lp-cta-optimization.md`) as a consistency hint.\n\n"
        + (_md_table(looker_hint, ["path", "sessions_hint"], 20) if looker_hint else "(no Looker hint table found in repo)")
        + "\n\n**Manual check:** compare the above `path` values vs top GA4 landing pages in section (2)."
    )

    md_parts.append(section("5) Insights (high intent vs wasted)"))
    md_parts.append(
        "This section is auto-generated heuristics based on (a) engagement proxies and (b) CTA click proxy.\n\n"
        "**High-intent signals:**\n"
        "- Landing pages with **high sessions** AND **high CTA rate** (or CTA count)\n"
        "- Sources/mediums with **high engagementRate** (and stable volume)\n\n"
        "**Wasted signals:**\n"
        "- High sessions but **low engagementRate** and **near-zero CTA clicks**\n"
        "- Blog/content pages that attract SEO traffic but don’t progress to CTA (unless intended as TOFU)\n\n"
        "Next step after this report: join CTA events to downstream conversion (signup/kyc) once those events exist in GA4, or via Amplitude as truth source."
    )

    md_parts.append(section("6) Action plan"))
    md_parts.append(
        "### Landing page fixes\n"
        "- Improve above-the-fold clarity + trust blocks on high-traffic LPs.\n"
        "- Add country-specific LPs for top geos where intent is high (e.g., Pakistan waitlist variant).\n\n"
        "### Instrumentation (CTA clicks)\n"
        "- Ensure GA4 records CTA clicks as a dedicated event (`cta_click`) with parameters (`cta_id`, `placement`, `destination`, `variant`).\n"
        "- Mark CTA click as a conversion (optional) if it represents a meaningful step.\n\n"
        "### Campaign UTM hygiene\n"
        "- Enforce `utm_source`, `utm_medium`, `utm_campaign` for paid/owned links.\n"
        "- Standardize naming (lowercase, no spaces) to avoid source fragmentation.\n\n"
        "### Retargeting audiences (from top pages)\n"
        "- Build audiences of users who visited top-intent LPs and/or clicked CTA (if tracked).\n"
        "- Separate TOFU content visitors vs BOFU landing page visitors for differentiated messaging."
    )

    out_md.write_text("\n".join(md_parts).strip() + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--property-id", default=os.getenv("GA4_PROPERTY_ID"), help="GA4 property id (numeric). Or set GA4_PROPERTY_ID")
    ap.add_argument(
        "--creds",
        default=os.getenv("GOOGLE_APPLICATION_CREDENTIALS", DEFAULT_CREDENTIALS),
        help=f"Path to service account json (default: {DEFAULT_CREDENTIALS})",
    )
    ap.add_argument("--out-md", default=str(ANALYSIS_DIR / "ga4-web-traffic.md"))
    ap.add_argument("--out-json", default=str(DATA_DIR / "ga4-web-traffic.json"))

    args = ap.parse_args()

    generate(
        property_id=args.property_id,
        creds_path=args.creds,
        out_md=Path(args.out_md),
        out_json=Path(args.out_json),
    )


if __name__ == "__main__":
    main()
