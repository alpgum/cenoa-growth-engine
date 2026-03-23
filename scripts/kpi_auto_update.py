#!/usr/bin/env python3
"""KPI auto-update (Amplitude → Cortex)

Pulls weekly KPI totals from Amplitude Event Segmentation API for a given week and
its previous week, computes WoW deltas, and writes a single JSON file consumed by
Cenoa Cortex.

How to run (recommended):

  source ~/.openclaw/venv/bin/activate
  python3 projects/cenoa-growth-engine/scripts/kpi_auto_update.py \
    --start 2026-03-14 --end 2026-03-20 \
    --prev-start 2026-03-07 --prev-end 2026-03-13

Dry run (no file write):

  source ~/.openclaw/venv/bin/activate
  python3 projects/cenoa-growth-engine/scripts/kpi_auto_update.py \
    --start 2026-03-14 --end 2026-03-20 \
    --prev-start 2026-03-07 --prev-end 2026-03-13 \
    --dry-run

Date Convention (S3-014):
  - Weekly = ISO week: Monday 00:00 UTC to Sunday 23:59 UTC
  - MTD = 1st of month 00:00 UTC to current day 23:59 UTC
  - All Amplitude API calls use YYYYMMDD format
  - --start should be a Monday, --end should be a Sunday

Credentials:
  Reads ~/.openclaw/credentials/amplitude.env (AMPLITUDE_API_KEY, AMPLITUDE_SECRET_KEY)

Output:
  Writes to projects/cenoa-growth-engine/data.json by default.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

import requests

try:
    from zoneinfo import ZoneInfo  # py3.9+
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore


AMPLITUDE_API_URL = "https://amplitude.com/api/2/events/segmentation"

# Required KPI events (key -> Amplitude event_type)
EVENTS: dict[str, str] = {
    "installs": "[AppsFlyer] Install",
    "signups": "Cenoa sign-up completed",
    "kycSubmits": "Bridgexyz KYC Component: Submit clicked",
    "virtualAccountOpened": "Virtual account opened",
    "depositCompleted": "Deposit Completed",
    "transferCompleted": "Transfer Completed",
    "withdrawCompleted": "Withdraw Completed",
}

DAU_EVENT = "_active"  # special Amplitude event


@dataclass
class KPI:
    value: float
    prev: float
    deltaPct: float
    direction: str


def _load_amplitude_credentials() -> tuple[str, str]:
    """Load Amplitude creds from ~/.openclaw/credentials/amplitude.env (or env)."""
    env_file = os.path.expanduser("~/.openclaw/credentials/amplitude.env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

    api_key = os.environ.get("AMPLITUDE_API_KEY")
    secret_key = os.environ.get("AMPLITUDE_SECRET_KEY")
    if not api_key or not secret_key:
        raise RuntimeError(
            "Missing AMPLITUDE_API_KEY / AMPLITUDE_SECRET_KEY. "
            "Expected in ~/.openclaw/credentials/amplitude.env or environment."
        )
    return api_key, secret_key


def _parse_ymd(s: str) -> datetime:
    return datetime.strptime(s.strip(), "%Y-%m-%d")


def _fmt_yyyymmdd(d: datetime) -> str:
    return d.strftime("%Y%m%d")


def _days_inclusive(start: datetime, end: datetime) -> int:
    return (end - start).days + 1


def _week_label(start: datetime, end: datetime) -> str:
    """Human label like 'Mar 14-20, 2026' or 'Mar 28-Apr 3, 2026'."""
    if start.year == end.year:
        year = start.year
        if start.month == end.month:
            mon = start.strftime("%b")
            return f"{mon} {start.day}-{end.day}, {year}"
        return f"{start.strftime('%b')} {start.day}-{end.strftime('%b')} {end.day}, {year}"
    # Rare case: spans years
    return f"{start.strftime('%b %d, %Y')}-{end.strftime('%b %d, %Y')}"


def _updated_label(now: datetime) -> str:
    # Requirement wants 'TRT' suffix.
    return now.strftime("%Y-%m-%d %H:%M") + " TRT"


def _direction(delta_pct: float) -> str:
    if delta_pct > 0:
        return "up"
    if delta_pct < 0:
        return "down"
    return "flat"


def _compute_kpi(curr: float, prev: float) -> KPI:
    if prev == 0:
        delta = 100.0 if curr > 0 else 0.0
    else:
        delta = round(((curr - prev) / prev) * 100.0, 1)

    return KPI(
        value=curr,
        prev=prev,
        deltaPct=delta,
        direction=_direction(delta),
    )


COUNTRY_CODES = ["TR", "NG", "EG", "PK"]
# Amplitude 'country' user property uses full names
COUNTRY_NAMES: dict[str, str] = {
    "TR": "Turkey",
    "NG": "Nigeria",
    "EG": "Egypt",
    "PK": "Pakistan",
}
COUNTRY_EVENTS = ["installs", "signups"]  # events to break down by country


def _query_segmentation(
    api_key: str,
    secret_key: str,
    event_type: str,
    start_yyyymmdd: str,
    end_yyyymmdd: str,
    metric: str,
    country_filter: str | None = None,
) -> list[float]:
    """Return per-day series values for the event.

    If country_filter is set, segments results by that country code.
    """
    event_obj: dict = {"event_type": event_type}
    if country_filter:
        event_obj["filters"] = [{
            "subprop_type": "user",
            "subprop_key": "country",
            "subprop_op": "is",
            "subprop_value": [country_filter],
        }]
    e_param = json.dumps(event_obj)
    params: dict[str, str] = {
        "e": e_param,
        "start": start_yyyymmdd,
        "end": end_yyyymmdd,
        "m": metric,
    }

    resp = requests.get(
        AMPLITUDE_API_URL,
        params=params,
        auth=(api_key, secret_key),
        timeout=45,
    )
    # Helpful error context without leaking creds
    if resp.status_code >= 400:
        raise RuntimeError(f"Amplitude API error {resp.status_code}: {resp.text[:500]}")

    data = resp.json()
    series = data.get("data", {}).get("series", [[]])
    if not series or not series[0]:
        return []
    return [float(v) for v in series[0]]


def _query_total(
    api_key: str, secret_key: str, event_type: str, start: str, end: str,
    country: str | None = None,
) -> int:
    values = _query_segmentation(
        api_key, secret_key, event_type, start, end,
        metric="totals", country_filter=country,
    )
    return int(round(sum(values))) if values else 0


def _query_country_totals(
    api_key: str, secret_key: str, event_type: str, start: str, end: str
) -> dict[str, int]:
    """Return {country_code: total} for COUNTRY_CODES (one API call each)."""
    result: dict[str, int] = {}
    for cc in COUNTRY_CODES:
        full_name = COUNTRY_NAMES[cc]
        result[cc] = _query_total(api_key, secret_key, event_type, start, end, country=full_name)
    return result


def _query_dau_avg(api_key: str, secret_key: str, start: str, end: str, days: int) -> float:
    """Average daily active users for the date range (m=uniques on _active)."""
    values = _query_segmentation(api_key, secret_key, DAU_EVENT, start, end, metric="uniques")
    if not values:
        return 0.0
    # Requirement: average daily (include zero days if any)
    return round(sum(values) / max(days, 1), 1)


def _default_output_path() -> Path:
    # scripts/ -> cenoa-growth-engine/ -> projects/ -> workspace/ -> projects/cenoa-growth-engine/data.json
    this_file = Path(__file__).resolve()
    workspace = this_file
    # Walk up until we find workspace marker 'projects' directory.
    # (defensive: avoids hardcoding absolute path)
    for _ in range(10):
        if (workspace / "projects").exists():
            break
        workspace = workspace.parent
    return workspace / "projects" / "cenoa-growth-engine" / "data.json"


def _build_campaign_performance() -> list[dict]:
    """Build campaignPerformance[] array for Cortex dashboard.

    TODO: Pull real data from AppsFlyer/BigQuery/Sheets when pipeline is live.
    For now returns hardcoded best-effort data from campaign-commentary-mar22.md.

    Each entry:
      name, country, countryFlag, channel, channelIcon, spend, installs, cpi,
      newActives, trueCAC, wowDelta, health (healthy|bleeding|dead|fraud),
      action (scale|maintain|watch|kill), commentary (1-line)
    """
    # Prefer real campaign names/installs from BigQuery extract when present.
    # This is best-effort: if the file is missing or malformed, we fall back to
    # the hardcoded table.
    bq_path = Path(__file__).resolve().parent.parent / "data" / "bq-campaign-table-latest.json"
    if bq_path.exists():
        try:
            with open(bq_path, "r", encoding="utf-8") as f:
                bq_obj = json.load(f)

            bq_rows = bq_obj.get("campaigns", [])
            if isinstance(bq_rows, list) and bq_rows:
                def _channel_from_media_source(ms: str) -> tuple[str, str]:
                    m = (ms or "").lower()
                    if "apple" in m or "asa" in m:
                        return ("Apple", "🍎")
                    if "google" in m or "adwords" in m:
                        return ("Google", "🔍")
                    if "facebook" in m or "meta" in m or "instagram" in m or "zzgtech" in m:
                        return ("Meta", "📘")
                    if "tiktok" in m:
                        return ("TikTok", "🎵")
                    if "appnext" in m:
                        return ("Appnext", "⚠️")
                    return ("Other", "📡")

                def _country_flag(cc: str) -> str:
                    return {"TR": "🇹🇷", "EG": "🇪🇬", "NG": "🇳🇬", "PK": "🇵🇰"}.get((cc or "").upper(), "")

                out: list[dict] = []
                # Sort by installs desc; take top 25 to keep table readable.
                bq_rows_sorted = sorted(
                    [r for r in bq_rows if isinstance(r, dict)],
                    key=lambda r: int(r.get("installs") or 0),
                    reverse=True,
                )[:25]

                for r in bq_rows_sorted:
                    country = (r.get("country") or "TR").upper()
                    media_source = str(r.get("media_source") or "").strip()
                    name = str(r.get("campaign") or "(blank)").strip()
                    installs = int(r.get("installs") or 0)
                    spend = r.get("cost_usd")
                    cpi = r.get("cpi_usd")

                    channel, icon = _channel_from_media_source(media_source)

                    out.append(
                        {
                            "name": name,
                            "country": country,
                            "countryFlag": _country_flag(country),
                            "channel": channel,
                            "channelIcon": icon,
                            "spend": spend,
                            "installs": installs,
                            "cpi": cpi,
                            "newActives": None,
                            "trueCAC": None,
                            "wowDelta": 0,
                            "health": "healthy",
                            "action": "watch",
                            "commentary": f"(BQ extract) media_source={media_source}",
                        }
                    )

                if out:
                    return out
        except Exception:
            pass

    # Read from campaign-health.json if available
    health_path = Path(__file__).resolve().parent.parent / "data" / "campaign-health.json"
    if health_path.exists():
        try:
            with open(health_path, "r", encoding="utf-8") as f:
                health_data = json.load(f)
            # Map channel health statuses to build entries
            channels = health_data.get("channels", {})
            # For now, we still use the hardcoded commentary; real pipeline
            # would merge health_data with spend/install data from BQ/Sheets.
        except Exception:
            pass

    # Hardcoded from campaign-commentary-mar22.md — best-effort until API pipeline
    return [
        {"name":"Pmax Search","country":"TR","countryFlag":"🇹🇷","channel":"Google","channelIcon":"🔍","spend":16844,"installs":2050,"cpi":8.22,"newActives":182,"trueCAC":19.18,"wowDelta":0,"health":"healthy","action":"scale","commentary":"Best cost/active in portfolio at $19.18. Scale budget +50% to $1,200/wk."},
        {"name":"ASA Brand Exact","country":"TR","countryFlag":"🇹🇷","channel":"Apple","channelIcon":"🍎","spend":2217,"installs":407,"cpi":5.45,"newActives":93,"trueCAC":22.66,"wowDelta":0,"health":"healthy","action":"scale","commentary":"Highest-LTV channel. 114 withdrawals from 26 installs. Scale to $5K/mo."},
        {"name":"Meta LTV Test","country":"EG","countryFlag":"🇪🇬","channel":"Meta","channelIcon":"📘","spend":2204,"installs":402,"cpi":5.48,"newActives":23,"trueCAC":68.0,"wowDelta":-61.0,"health":"healthy","action":"scale","commentary":"Cost/active improved $174→$68 WoW. Scale to $2K/wk — best Meta campaign."},
        {"name":"Google Search","country":"TR","countryFlag":"🇹🇷","channel":"Google","channelIcon":"🔍","spend":1127,"installs":801,"cpi":1.41,"newActives":47,"trueCAC":25.48,"wowDelta":0,"health":"healthy","action":"scale","commentary":"CPI $1.41 with 49% signup rate. High-intent capture. +$200/wk budget."},
        {"name":"Spaze","country":"TR","countryFlag":"🇹🇷","channel":"Spaze","channelIcon":"📡","spend":1770,"installs":363,"cpi":4.88,"newActives":64,"trueCAC":27.66,"wowDelta":0,"health":"healthy","action":"maintain","commentary":"Solid mid-tier performer. 43% signup rate, good downstream quality."},
        {"name":"Spaze DSP","country":"TR","countryFlag":"🇹🇷","channel":"Spaze","channelIcon":"📡","spend":1460,"installs":243,"cpi":6.01,"newActives":23,"trueCAC":63.48,"wowDelta":0,"health":"healthy","action":"maintain","commentary":"Acceptable quality at reasonable cost. Watch if signup rate drops below 30%."},
        {"name":"Meta App iOS","country":"TR","countryFlag":"🇹🇷","channel":"Meta","channelIcon":"📘","spend":936,"installs":164,"cpi":5.71,"newActives":32,"trueCAC":29.25,"wowDelta":0,"health":"healthy","action":"maintain","commentary":"Strong 65% signup rate. 16× more efficient than Meta W2A on cost/active."},
        {"name":"Pmax Get Paid","country":"EG","countryFlag":"🇪🇬","channel":"Google","channelIcon":"🔍","spend":650,"installs":192,"cpi":3.39,"newActives":11,"trueCAC":59.09,"wowDelta":0,"health":"healthy","action":"maintain","commentary":"Solid CPI in new market. Hold until Egypt KYC issues are resolved."},
        {"name":"Pmax LTV Test","country":"EG","countryFlag":"🇪🇬","channel":"Google","channelIcon":"🔍","spend":423,"installs":132,"cpi":3.20,"newActives":6,"trueCAC":70.50,"wowDelta":0,"health":"healthy","action":"maintain","commentary":"Low CPI but fewer activations than Get Paid variant. May consolidate."},
        {"name":"Google Web2App","country":"TR","countryFlag":"🇹🇷","channel":"Google","channelIcon":"🔍","spend":453,"installs":92,"cpi":4.92,"newActives":15,"trueCAC":30.20,"wowDelta":0,"health":"healthy","action":"maintain","commentary":"Decent W2A efficiency. Much better than Meta W2A. Good supplementary volume."},
        {"name":"Meta Get Paid Test","country":"EG","countryFlag":"🇪🇬","channel":"Meta","channelIcon":"📘","spend":1977,"installs":373,"cpi":5.30,"newActives":22,"trueCAC":637.0,"wowDelta":563.0,"health":"bleeding","action":"watch","commentary":"Collapsed from $96→$637/active W2. Classic creative fatigue. 1 more week."},
        {"name":"TikTok App","country":"TR","countryFlag":"🇹🇷","channel":"TikTok","channelIcon":"🎵","spend":572,"installs":381,"cpi":1.50,"newActives":17,"trueCAC":33.65,"wowDelta":0,"health":"bleeding","action":"watch","commentary":"Cheap CPI but 0 withdrawals — quality red flag. 1 more week to prove."},
        {"name":"TikTok Web2App","country":"TR","countryFlag":"🇹🇷","channel":"TikTok","channelIcon":"🎵","spend":1279,"installs":124,"cpi":10.31,"newActives":16,"trueCAC":79.94,"wowDelta":0,"health":"bleeding","action":"watch","commentary":"CPI 2.2× avg but 75% signup rate is promising. Cut budget 30%."},
        {"name":"Google App iOS","country":"TR","countryFlag":"🇹🇷","channel":"Google","channelIcon":"🔍","spend":1510,"installs":62,"cpi":24.35,"newActives":7,"trueCAC":215.71,"wowDelta":0,"health":"bleeding","action":"watch","commentary":"CPI 5.3× avg — classified BLEEDING. Test tCPA at ₺600 before killing."},
        {"name":"NG Architect (all)","country":"NG","countryFlag":"🇳🇬","channel":"Google","channelIcon":"🔍","spend":790,"installs":68,"cpi":11.62,"newActives":0,"trueCAC":None,"wowDelta":0,"health":"bleeding","action":"watch","commentary":"Good signups but 0 withdrawals. Blocked by NG KYC = 0. Pivot messaging."},
        {"name":"Meta W2A RTGT","country":"TR","countryFlag":"🇹🇷","channel":"Meta","channelIcon":"📘","spend":485,"installs":17,"cpi":28.53,"newActives":6,"trueCAC":80.83,"wowDelta":0,"health":"healthy","action":"watch","commentary":"Only TR W2A with withdrawals. Retargeting works — cap at $500/wk."},
        {"name":"Appnext + DSP","country":"TR","countryFlag":"🇹🇷","channel":"Appnext","channelIcon":"⚠️","spend":1008,"installs":1892,"cpi":0.53,"newActives":1,"trueCAC":1008.0,"wowDelta":0,"health":"fraud","action":"kill","commentary":"⛔ FRAUD. 1,892 installs, 1 active. Bot farms. Pause + request $1K refund."},
        {"name":"Meta W2A TR","country":"TR","countryFlag":"🇹🇷","channel":"Meta","channelIcon":"📘","spend":4414,"installs":811,"cpi":5.44,"newActives":70,"trueCAC":None,"wowDelta":0,"health":"dead","action":"kill","commentary":"Structural failure. $3,536/active in Jan → $∞ in Feb. Pause all prospecting."},
        {"name":"Demand Gen RTGT","country":"TR","countryFlag":"🇹🇷","channel":"Google","channelIcon":"🔍","spend":560,"installs":0,"cpi":None,"newActives":0,"trueCAC":None,"wowDelta":0,"health":"dead","action":"kill","commentary":"0 installs after 5 months. Est. waste: $5,600–$11,200. Pause immediately."},
        {"name":"Onboarding Meta","country":"TR","countryFlag":"🇹🇷","channel":"Meta","channelIcon":"📘","spend":101,"installs":3,"cpi":33.67,"newActives":0,"trueCAC":None,"wowDelta":0,"health":"dead","action":"kill","commentary":"CPI $33.67 (7.3× avg), 0 active. Not viable at any scale. Pause."},
        {"name":"Twitter Ads","country":"TR","countryFlag":"🇹🇷","channel":"Twitter","channelIcon":"🐦","spend":183,"installs":1,"cpi":183.0,"newActives":0,"trueCAC":None,"wowDelta":0,"health":"dead","action":"kill","commentary":"$183/install, 0 downstream. Dead channel. Kill permanently."},
    ]


# ── Spend inputs (Sheets) ─────────────────────────────────────────────

COUNTRY_FLAGS: dict[str, str] = {"TR": "🇹🇷", "EG": "🇪🇬", "NG": "🇳🇬", "PK": "🇵🇰"}
COUNTRY_DEEP_DIVE: dict[str, str] = {"TR": "country-tr.html", "EG": "country-eg.html", "NG": "country-ng.html", "PK": "country-pk.html"}

_MONTHS: dict[str, int] = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}


def _load_json_file(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_period_key(period_key: str) -> tuple[int, int, int, int] | None:
    """Parse period keys like '9_15_march_26' into sortable tuples.

    Returns (year, month, end_day, start_day) for max() sorting.
    """
    parts = (period_key or "").lower().split("_")
    if len(parts) < 4:
        return None
    try:
        start_day = int(parts[0])
        end_day = int(parts[1])
        month_s = parts[2]
        year_raw = int(parts[3])
    except Exception:
        return None

    month = _MONTHS.get(month_s, _MONTHS.get(month_s[:3]))
    if not month:
        return None

    year = (2000 + year_raw) if year_raw < 100 else year_raw
    return (year, month, end_day, start_day)


def _pick_latest_period_key(periods: dict) -> str | None:
    if not periods:
        return None
    scored: list[tuple[tuple[int, int, int, int], str]] = []
    for k in periods.keys():
        sk = _parse_period_key(k)
        if sk:
            scored.append((sk, k))
    if not scored:
        return None
    scored.sort()
    return scored[-1][1]


def _channel_bucket(sheet_channel_key: str) -> str:
    k = (sheet_channel_key or "").lower().strip()
    if not k:
        return "Other"

    # Canonical buckets used in Cortex + cacTracking
    if k.startswith("pmax"):
        return "Pmax"
    if k.startswith("google"):
        return "Google Search"
    if k.startswith("apple"):
        return "Apple Search Ads"
    if k.startswith("meta") or "meta" in k:
        return "Meta"
    if k.startswith("tiktok"):
        return "TikTok"
    if k.startswith("appnext"):
        return "Appnext"

    # Everything else (Spaze, Twitter, affiliates, etc.)
    return "Other"


def _safe_div(n: float, d: float) -> float | None:
    if not d:
        return None
    return round(n / d, 2)


def _build_country_spend() -> tuple[list[dict], dict]:
    """Build countrySpend[] from Sheets budget-tracking and CAC analysis data.

    Source of truth for spend is Sheets.

    Reads:
      - sheets-budget-tracking.json → planned monthly budgets (marchBudget2026)
      - sheets-cac-analysis.json → weekly actuals (channel_2026_all periods)

    Returns: (countrySpend_list, spend_ctx)
      spend_ctx includes: period_key, period_sort_key, weekly_total
    """
    this_file = Path(__file__).resolve()
    data_dir = this_file.parent.parent / "data"

    budget_path = data_dir / "sheets-budget-tracking.json"
    cac_path = data_dir / "sheets-cac-analysis.json"

    # Default planned budgets (March 2026)
    planned = {"TR": 23000.0, "EG": 8500.0, "NG": 2200.0, "PK": 6000.0}

    # Try to load planned monthly from Sheets budget-tracking
    if budget_path.exists():
        try:
            bt = _load_json_file(budget_path)
            march_tab = bt.get("marchBudget2026", bt.get("march_26_budget", {}))

            # Prefer objective totals when available (more stable than byCountry.amount)
            obj = march_tab.get("objectiveByCountry") if isinstance(march_tab, dict) else None
            if isinstance(obj, dict):
                for cc, info in obj.items():
                    if cc.upper() in planned and isinstance(info, dict):
                        planned[cc.upper()] = float(info.get("total", planned[cc.upper()]))

            by_country = march_tab.get("byCountry") if isinstance(march_tab, dict) else None
            if isinstance(by_country, dict):
                for cc, info in by_country.items():
                    if cc.upper() in planned and isinstance(info, dict):
                        # Only fall back to byCountry.amount if objective total missing/0
                        if not planned.get(cc.upper()):
                            planned[cc.upper()] = float(info.get("amount", planned[cc.upper()]))
        except Exception:
            pass  # Use defaults

    # ── Weekly + MTD actuals from CAC analysis (Sheets) ───────────────
    weekly = {"TR": 0.0, "EG": 0.0, "NG": 0.0, "PK": 0.0}
    mtd = {"TR": 0.0, "EG": 0.0, "NG": 0.0, "PK": 0.0}
    totals = {"TR": {}, "EG": {}, "NG": {}, "PK": {}}

    period_key: str | None = None
    period_sort_key: tuple[int, int, int, int] | None = None

    if cac_path.exists():
        try:
            cac = _load_json_file(cac_path)
            periods = (cac.get("channel_2026_all", {}) or {}).get("periods", {}) or {}

            period_key = _pick_latest_period_key(periods)
            if period_key:
                period_sort_key = _parse_period_key(period_key)

            # For MTD, sum all periods in the same month as the selected weekly period
            if period_sort_key:
                sel_year, sel_month, _, _ = period_sort_key
                for pk, pdata in periods.items():
                    sk = _parse_period_key(pk)
                    if not sk:
                        continue
                    y, m, _, _ = sk
                    if (y, m) != (sel_year, sel_month):
                        continue

                    for c_name, c_data in (pdata or {}).items():
                        cc = {
                            "turkey": "TR", "egypt": "EG", "nigeria": "NG", "pakistan": "PK"
                        }.get((c_name or "").lower())
                        if not cc or not isinstance(c_data, dict):
                            continue
                        total = c_data.get("total", {}) if isinstance(c_data.get("total"), dict) else {}
                        mtd[cc] += float(total.get("cost", 0) or 0)

            # Weekly spend = selected period totals
            if period_key and period_key in periods:
                pdata = periods[period_key] or {}
                for c_name, c_data in pdata.items():
                    cc = {
                        "turkey": "TR", "egypt": "EG", "nigeria": "NG", "pakistan": "PK"
                    }.get((c_name or "").lower())
                    if not cc or not isinstance(c_data, dict):
                        continue
                    total = c_data.get("total", {}) if isinstance(c_data.get("total"), dict) else {}
                    weekly[cc] = float(total.get("cost", 0) or 0)
                    totals[cc] = total
        except Exception:
            pass

    result: list[dict] = []
    weekly_total = 0.0
    for cc in ["TR", "EG", "NG", "PK"]:
        p = float(planned[cc])
        m = float(mtd[cc])
        w = float(weekly[cc])
        weekly_total += w

        # Optional efficiency metrics based on Sheets totals
        t = totals.get(cc) or {}
        installs = float(t.get("installs", 0) or 0)
        new_active = float(t.get("new_active", 0) or 0)

        pacing = round((m / p) * 100, 1) if p > 0 else 0.0
        result.append({
            "code": cc,
            "country": cc,
            "flag": COUNTRY_FLAGS.get(cc, "🏳️"),
            "name": COUNTRY_NAMES.get(cc, cc),
            "weeklySpend": w,
            "weekly_spend": w,
            "mtdSpend": m,
            "mtd_spend": m,
            "monthlyTarget": p,
            "planned_monthly": p,
            "pacing_pct": pacing,
            "cpi": _safe_div(w, installs),
            "trueCAC": _safe_div(w, new_active),
            "deepDiveUrl": COUNTRY_DEEP_DIVE.get(cc),
        })

    spend_ctx = {
        "period_key": period_key,
        "period_sort_key": period_sort_key,
        "weekly_total": round(weekly_total, 2),
    }
    return result, spend_ctx


def _build_channel_performance(spend_ctx: dict) -> list[dict]:
    """Build channelPerformance[] directly from Sheets.

    Requirement (S3-031): channelPerformance spend MUST reconcile to countrySpend.

    If channel-level split is incomplete, the residual is captured as 'Unallocated'.
    """
    this_file = Path(__file__).resolve()
    data_dir = this_file.parent.parent / "data"
    cac_path = data_dir / "sheets-cac-analysis.json"

    period_key = spend_ctx.get("period_key")
    target_total = float(spend_ctx.get("weekly_total") or 0)

    if not cac_path.exists() or not period_key:
        # Safe fallback: preserve reconciliation by emitting Unallocated only.
        return ([{"name": "Unallocated", "spend": target_total, "installs": 0, "cpi": None,
                  "signups": 0, "virt_acc": 0, "new_active": 0, "true_cac": None, "wow_delta": 0.0}]
                if target_total else [])

    cac = _load_json_file(cac_path)
    periods = (cac.get("channel_2026_all", {}) or {}).get("periods", {}) or {}
    pdata = periods.get(period_key) or {}

    agg: dict[str, dict[str, float]] = {}

    for _country_name, c_data in (pdata or {}).items():
        if not isinstance(c_data, dict):
            continue
        channels = c_data.get("channels") or {}
        if not isinstance(channels, dict):
            continue

        for ch_key, ch_obj in channels.items():
            if not isinstance(ch_obj, dict):
                continue
            bucket = _channel_bucket(str(ch_key))
            a = agg.setdefault(bucket, {
                "spend": 0.0,
                "installs": 0.0,
                "signups": 0.0,
                "virt_acc": 0.0,
                "new_active": 0.0,
            })
            a["spend"] += float(ch_obj.get("cost", 0) or 0)
            a["installs"] += float(ch_obj.get("installs", 0) or 0)
            a["signups"] += float(ch_obj.get("sign_up", 0) or 0)
            a["virt_acc"] += float(ch_obj.get("virt_acc", 0) or 0)
            a["new_active"] += float(ch_obj.get("new_active", 0) or 0)

    rows: list[dict] = []
    total = 0.0
    for name, a in agg.items():
        spend = round(float(a.get("spend", 0) or 0), 2)
        inst = int(round(float(a.get("installs", 0) or 0)))
        sig = int(round(float(a.get("signups", 0) or 0)))
        va = int(round(float(a.get("virt_acc", 0) or 0)))
        na = int(round(float(a.get("new_active", 0) or 0)))
        total += spend

        rows.append({
            "name": name,
            "spend": spend,
            "installs": inst,
            "cpi": _safe_div(spend, inst),
            "signups": sig,
            "virt_acc": va,
            "new_active": na,
            "true_cac": _safe_div(spend, na),
            "wow_delta": 0.0,
        })

    delta = round(target_total - total, 2)
    if abs(delta) >= 0.01:
        rows.append({
            "name": "Unallocated",
            "spend": delta,
            "installs": 0,
            "cpi": None,
            "signups": 0,
            "virt_acc": 0,
            "new_active": 0,
            "true_cac": None,
            "wow_delta": 0.0,
        })

    # Sort: highest spend first (Unallocated last if present)
    def _sort_key(r: dict) -> tuple[int, float]:
        return (1 if r.get("name") == "Unallocated" else 0, -(r.get("spend") or 0))

    rows.sort(key=_sort_key)

    # Final guardrail: enforce exact reconciliation within rounding
    recon = round(sum(float(r.get("spend") or 0) for r in rows), 2)
    if round(recon - target_total, 2) != 0:
        # Force-adjust Unallocated
        fix = round(target_total - recon, 2)
        for r in rows:
            if r.get("name") == "Unallocated":
                r["spend"] = round(float(r.get("spend") or 0) + fix, 2)
                break
        else:
            rows.append({"name": "Unallocated", "spend": fix, "installs": 0, "cpi": None,
                         "signups": 0, "virt_acc": 0, "new_active": 0, "true_cac": None, "wow_delta": 0.0})

    return rows


def main() -> int:
    p = argparse.ArgumentParser(description="Pull weekly KPIs from Amplitude and write Cortex data.json")
    p.add_argument("--start", required=True, help="Current week start (YYYY-MM-DD)")
    p.add_argument("--end", required=True, help="Current week end (YYYY-MM-DD)")
    p.add_argument("--prev-start", required=True, help="Previous week start (YYYY-MM-DD)")
    p.add_argument("--prev-end", required=True, help="Previous week end (YYYY-MM-DD)")
    p.add_argument("--output", default=None, help="Output JSON path (default: projects/cenoa-growth-engine/data.json)")
    p.add_argument("--dry-run", action="store_true", help="Do not write file; print JSON only")
    args = p.parse_args()

    curr_start = _parse_ymd(args.start)
    curr_end = _parse_ymd(args.end)
    prev_start = _parse_ymd(args.prev_start)
    prev_end = _parse_ymd(args.prev_end)

    if curr_end < curr_start:
        raise SystemExit("--end must be >= --start")
    if prev_end < prev_start:
        raise SystemExit("--prev-end must be >= --prev-start")

    api_key, secret_key = _load_amplitude_credentials()

    curr_start_s = _fmt_yyyymmdd(curr_start)
    curr_end_s = _fmt_yyyymmdd(curr_end)
    prev_start_s = _fmt_yyyymmdd(prev_start)
    prev_end_s = _fmt_yyyymmdd(prev_end)

    curr_days = _days_inclusive(curr_start, curr_end)
    prev_days = _days_inclusive(prev_start, prev_end)

    kpis: dict[str, dict] = {}

    # Totals
    for key, event_type in EVENTS.items():
        curr_val = _query_total(api_key, secret_key, event_type, curr_start_s, curr_end_s)
        prev_val = _query_total(api_key, secret_key, event_type, prev_start_s, prev_end_s)
        kpi = _compute_kpi(float(curr_val), float(prev_val))
        kpis[key] = {
            "value": int(kpi.value),
            "prev": int(kpi.prev),
            "deltaPct": kpi.deltaPct,
            "direction": kpi.direction,
        }

    # DAU avg
    curr_dau = _query_dau_avg(api_key, secret_key, curr_start_s, curr_end_s, curr_days)
    prev_dau = _query_dau_avg(api_key, secret_key, prev_start_s, prev_end_s, prev_days)
    dau_kpi = _compute_kpi(curr_dau, prev_dau)
    kpis["dauAvg"] = {
        "value": dau_kpi.value,
        "prev": dau_kpi.prev,
        "deltaPct": dau_kpi.deltaPct,
        "direction": dau_kpi.direction,
    }

    # ── Country breakdown (installs / signups per country) ──────────────
    countries: dict[str, dict] = {}
    for cc in COUNTRY_CODES:
        countries[cc] = {}

    for event_key in COUNTRY_EVENTS:
        event_type = EVENTS[event_key]
        curr_by_country = _query_country_totals(api_key, secret_key, event_type, curr_start_s, curr_end_s)
        prev_by_country = _query_country_totals(api_key, secret_key, event_type, prev_start_s, prev_end_s)
        for cc in COUNTRY_CODES:
            c_kpi = _compute_kpi(float(curr_by_country[cc]), float(prev_by_country[cc]))
            countries[cc][event_key] = {
                "value": int(c_kpi.value),
                "prev": int(c_kpi.prev),
                "deltaPct": c_kpi.deltaPct,
            }

    # ── Highlights: top 3 biggest movers by |deltaPct| ───────────────
    FRIENDLY_NAMES: dict[str, str] = {
        "installs": "Installs",
        "signups": "Signups",
        "kycSubmits": "KYC Submit",
        "virtualAccountOpened": "Virtual Acct Opened",
        "depositCompleted": "Deposit",
        "transferCompleted": "Transfer",
        "withdrawCompleted": "Withdraw",
        "dauAvg": "DAU",
    }

    movers = []
    for key, obj in kpis.items():
        arrow = "▲" if obj["direction"] == "up" else "▼" if obj["direction"] == "down" else "→"
        label = FRIENDLY_NAMES.get(key, key)
        movers.append((abs(obj["deltaPct"]), f"{label} {arrow}{abs(obj['deltaPct'])}%"))
    movers.sort(key=lambda x: x[0], reverse=True)
    highlights = [m[1] for m in movers[:3]]

    # Timestamps
    if ZoneInfo is not None:
        now = datetime.now(ZoneInfo("Europe/Istanbul"))
    else:
        now = datetime.now()

    # ── Campaign Performance (best-effort from campaign-health + commentary) ──
    # When run live, this should pull from AppsFlyer/BigQuery/Sheets.
    # For now, we include hardcoded data from campaign-commentary-mar22.md.
    # The dashboard reads data.campaignPerformance[] for the upgraded table.
    campaign_performance = _build_campaign_performance()

    # ── Country + Channel Spend (Sheets = source of truth) ────────────
    country_spend, spend_ctx = _build_country_spend()
    channel_performance = _build_channel_performance(spend_ctx)

    # ISO 8601 timestamp with TRT offset for machine-readable "last updated"
    last_updated_iso = now.isoformat()  # e.g. 2026-03-22T23:45:12.123456+03:00

    patch_obj = {
        "week": _week_label(curr_start, curr_end),
        "updated": _updated_label(now),
        "lastUpdated": last_updated_iso,
        "kpis": kpis,
        "countries": countries,
        "highlights": highlights,
        "countrySpend": country_spend,
        "channelPerformance": channel_performance,
        "campaignPerformance": campaign_performance,
    }

    out_path = Path(args.output).expanduser() if args.output else _default_output_path()

    # Merge into existing Cortex data.json so we don't drop manually-maintained sections
    base_obj: dict = {}
    if out_path.exists():
        try:
            base_obj = json.loads(out_path.read_text(encoding="utf-8"))
        except Exception:
            base_obj = {}

    base_obj.update(patch_obj)

    rendered = json.dumps(base_obj, indent=2, ensure_ascii=False)

    if args.dry_run:
        print(rendered)
        return 0

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered + "\n", encoding="utf-8")
    print(f"✅ Wrote {out_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
