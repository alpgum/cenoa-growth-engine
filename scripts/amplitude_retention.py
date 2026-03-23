#!/usr/bin/env python3
"""
Amplitude Retention Analysis Script
====================================
Amplitude's segmentation API doesn't support true cohort retention (D1/D7/D30).
This script uses available endpoints to compute retention proxies:

1. DAU / WAU / MAU ratios as engagement depth proxies
2. Daily signups vs daily active users trend
3. "Application opened" by country for activity trends
4. Approximate retention via DAU/signup ratio over time

Date Convention (S3-014):
  - Weekly = ISO week: Monday 00:00 UTC to Sunday 23:59 UTC
  - MTD = 1st of month 00:00 UTC to current day 23:59 UTC
  - All Amplitude API calls use YYYYMMDD format
  - Default range: last 4 complete ISO weeks (28 days, Mon-Sun aligned)

Output:
  - data/retention-YYYYMMDD.json
  - analysis/retention.md

Usage:
    python amplitude_retention.py
    python amplitude_retention.py --days 56  # 8 ISO weeks
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

AMPLITUDE_API_URL = "https://amplitude.com/api/2/events/segmentation"
CREDS_FILE = os.path.expanduser("~/.openclaw/credentials/amplitude.env")

def load_credentials():
    creds = {}
    with open(CREDS_FILE) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                creds[k.strip()] = v.strip()
    return creds["AMPLITUDE_API_KEY"], creds["AMPLITUDE_SECRET_KEY"]

API_KEY, SECRET_KEY = load_credentials()

# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def query_segmentation(event_type, start_date, end_date, metric="uniques",
                       group_by=None, interval=1):
    """Query Amplitude Event Segmentation API."""
    e_param = {"event_type": event_type}
    if group_by:
        e_param["group_by"] = [{"type": "user", "value": group_by}]

    params = {
        "e": json.dumps(e_param),
        "m": metric,
        "start": start_date,
        "end": end_date,
        "i": str(interval),  # 1=daily
    }

    resp = requests.get(
        AMPLITUDE_API_URL,
        params=params,
        auth=(API_KEY, SECRET_KEY),
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def extract_daily_series(api_response):
    """Extract {date: value} from segmentation response (non-grouped)."""
    data = api_response.get("data", {})
    series_list = data.get("series", [])
    labels = data.get("xValues", [])

    if not series_list or not labels:
        return {}

    # series_list[0] is the main series for non-grouped queries
    values = series_list[0]
    return {labels[i]: values[i] for i in range(len(labels))}


def extract_grouped_series(api_response):
    """Extract {group: {date: value}} from grouped segmentation response."""
    data = api_response.get("data", {})
    series_list = data.get("series", [])
    labels = data.get("xValues", [])
    series_labels = data.get("seriesLabels", [])

    if not series_list or not labels:
        return {}

    result = {}
    for idx, group_series in enumerate(series_list):
        group_name = series_labels[idx] if idx < len(series_labels) else f"group_{idx}"
        if isinstance(group_name, list):
            group_name = group_name[0] if group_name else f"group_{idx}"
        values = group_series
        result[group_name] = {labels[i]: values[i] for i in range(len(labels))}

    return result


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------

def compute_engagement_ratios(dau_series):
    """Compute WAU/MAU, DAU/MAU, DAU/WAU ratios from daily active users."""
    dates = sorted(dau_series.keys())
    if len(dates) < 7:
        return {}

    # Last 7 days = WAU proxy, last 30 days = MAU proxy
    last_7 = dates[-7:]
    last_30 = dates[-30:] if len(dates) >= 30 else dates

    avg_dau = sum(dau_series[d] for d in last_7) / len(last_7)
    wau = sum(dau_series[d] for d in last_7)  # Sum of daily uniques (overcounts, but proxy)
    mau = sum(dau_series[d] for d in last_30)

    # Better: use average DAU as proxy
    avg_dau_30 = sum(dau_series[d] for d in last_30) / len(last_30)
    avg_dau_7 = sum(dau_series[d] for d in last_7) / len(last_7)

    # Stickiness = DAU/MAU (classic engagement metric)
    # Since we can't deduplicate across days via this API, we use avg daily uniques
    # as a rough indicator
    return {
        "avg_dau_7d": round(avg_dau_7, 1),
        "avg_dau_30d": round(avg_dau_30, 1),
        "dau_trend_7d": [dau_series[d] for d in last_7],
        "dau_trend_7d_dates": last_7,
        "dau_trend_30d": [dau_series[d] for d in last_30],
        "dau_trend_30d_dates": last_30,
    }


def compute_retention_proxy(signup_series, dau_series):
    """
    Approximate retention using signup vs DAU trends.
    
    True retention requires user-level cohort tracking (not available via segmentation API).
    Instead we compute:
    - Signup-to-DAU ratio over time (are new users sticking?)
    - Cumulative signups vs current DAU (rough retention floor)
    """
    dates = sorted(set(signup_series.keys()) & set(dau_series.keys()))
    if not dates:
        return {}

    daily_data = []
    cumulative_signups = 0
    for d in dates:
        signups = signup_series.get(d, 0)
        dau = dau_series.get(d, 0)
        cumulative_signups += signups
        daily_data.append({
            "date": d,
            "signups": signups,
            "dau": dau,
            "cumulative_signups": cumulative_signups,
            "dau_to_cumulative_ratio": round(dau / cumulative_signups * 100, 2) if cumulative_signups > 0 else 0,
        })

    # Overall retention proxy: current DAU / total signups
    total_signups = cumulative_signups
    recent_avg_dau = sum(dau_series[d] for d in dates[-7:]) / min(7, len(dates))

    return {
        "daily_breakdown": daily_data,
        "total_signups_period": total_signups,
        "recent_avg_dau": round(recent_avg_dau, 1),
        "crude_retention_pct": round(recent_avg_dau / total_signups * 100, 2) if total_signups > 0 else 0,
        "caveat": "This is DAU/cumulative_signups — a floor estimate. True retention requires cohort analysis."
    }


def analyze_country_activity(grouped_data, top_n=10):
    """Analyze activity by country, return top N."""
    country_totals = {}
    for country, daily in grouped_data.items():
        country_totals[country] = sum(daily.values())

    sorted_countries = sorted(country_totals.items(), key=lambda x: x[1], reverse=True)[:top_n]

    result = []
    for country, total in sorted_countries:
        daily = grouped_data[country]
        dates = sorted(daily.keys())
        last_7 = dates[-7:] if len(dates) >= 7 else dates
        avg_7d = sum(daily[d] for d in last_7) / len(last_7) if last_7 else 0
        result.append({
            "country": country,
            "total_opens_30d": total,
            "avg_daily_opens_7d": round(avg_7d, 1),
            "trend_7d": [daily.get(d, 0) for d in last_7],
        })

    return result


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(engagement, retention_proxy, country_activity, dau_series, signup_series, end_date):
    """Generate markdown analysis report."""
    lines = [
        f"# Retention & Engagement Analysis",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Period:** Last 30 days ending {end_date}",
        "",
        "---",
        "",
        "## ⚠️ Methodology & Caveats",
        "",
        "Amplitude's Event Segmentation API returns **daily unique counts** but does NOT support:",
        "- True cohort retention (D1/D7/D30 by signup date)",
        "- User-level intersection between events across days",
        "- Deduplication of unique users across multiple days",
        "",
        "What we CAN compute are **proxy metrics** that directionally indicate retention health.",
        "",
        "---",
        "",
        "## 1. Engagement Depth (DAU Trends)",
        "",
    ]

    if engagement:
        lines.extend([
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Avg DAU (7d) | **{engagement['avg_dau_7d']:,.0f}** |",
            f"| Avg DAU (30d) | **{engagement['avg_dau_30d']:,.0f}** |",
            "",
        ])

        # DAU trend sparkline (last 7 days)
        if engagement.get("dau_trend_7d"):
            lines.append("### DAU Last 7 Days")
            lines.append("")
            lines.append("| Date | DAU |")
            lines.append("|------|-----|")
            for d, v in zip(engagement["dau_trend_7d_dates"], engagement["dau_trend_7d"]):
                lines.append(f"| {d} | {v:,.0f} |")
            lines.append("")

    lines.extend([
        "## 2. Retention Proxy (DAU / Cumulative Signups)",
        "",
        "This metric shows what percentage of all-time signups (in the period) are active on any given day.",
        "It's a **floor estimate** — true retention would be higher since not all signups are expected to be active daily.",
        "",
    ])

    if retention_proxy:
        lines.extend([
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Signups (period) | **{retention_proxy['total_signups_period']:,}** |",
            f"| Recent Avg DAU | **{retention_proxy['recent_avg_dau']:,.0f}** |",
            f"| Crude Retention % | **{retention_proxy['crude_retention_pct']:.1f}%** |",
            "",
            f"> _{retention_proxy['caveat']}_",
            "",
        ])

        # Show daily breakdown (last 7 days)
        daily = retention_proxy.get("daily_breakdown", [])
        if daily:
            recent = daily[-7:]
            lines.append("### Daily Breakdown (Last 7 Days)")
            lines.append("")
            lines.append("| Date | Signups | DAU | Cumul. Signups | DAU/Cumul % |")
            lines.append("|------|---------|-----|---------------|-------------|")
            for row in recent:
                lines.append(
                    f"| {row['date']} | {row['signups']:,} | {row['dau']:,} | "
                    f"{row['cumulative_signups']:,} | {row['dau_to_cumulative_ratio']:.1f}% |"
                )
            lines.append("")

    lines.extend([
        "## 3. Activity by Country (Application Opened)",
        "",
        "Top countries by 'Application opened' events in the last 30 days.",
        "",
    ])

    if country_activity:
        lines.append("| Country | Total Opens (30d) | Avg Daily (7d) |")
        lines.append("|---------|-------------------|----------------|")
        for c in country_activity:
            lines.append(f"| {c['country']} | {c['total_opens_30d']:,} | {c['avg_daily_opens_7d']:,.0f} |")
        lines.append("")
    else:
        lines.append("_No country-level data available._")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## 4. Interpretation & Next Steps",
        "",
        "### What these numbers tell us:",
        "- **DAU trend** shows whether the user base is growing, stable, or declining",
        "- **DAU/Cumulative Signups %** declining over time suggests poor retention (new users churn)",
        "- **DAU/Cumulative Signups %** stable or rising suggests decent retention (users stick around)",
        "- **Country breakdown** reveals geographic concentration and growth markets",
        "",
        "### For true D1/D7/D30 retention:",
        "- Use Amplitude's **Retention Analysis** chart in the UI (not available via segmentation API)",
        "- Or use the **Behavioral Cohorts API** + **Export API** for user-level data",
        "- Or set up a BigQuery export and compute cohort retention via SQL",
        "",
        "### Recommended actions:",
        "1. Monitor DAU/Signup ratio weekly — declining = retention problem",
        "2. Compare country-level DAU to signups — find where users stick vs churn",
        "3. Set up Amplitude Retention chart for precise D1/D7/D30 numbers",
        "",
    ])

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Amplitude Retention Analysis")
    parser.add_argument("--days", type=int, default=28, help="Number of days to analyze (default: 28, i.e. 4 ISO weeks)")
    args = parser.parse_args()

    # ISO week boundaries: align to complete weeks (Mon-Sun)
    today = datetime.utcnow()
    last_sunday = today - timedelta(days=today.weekday() + 1)
    num_weeks = max(1, args.days // 7)
    start_date = last_sunday - timedelta(days=num_weeks * 7 - 1)  # Monday
    end_date = last_sunday  # Sunday

    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")
    start_pretty = start_date.strftime("%Y-%m-%d")
    end_pretty = end_date.strftime("%Y-%m-%d")

    print(f"📊 Amplitude Retention Analysis: {start_pretty} → {end_pretty}")
    print()

    # Determine output paths
    script_dir = Path(__file__).resolve().parent
    project_dir = script_dir.parent
    data_dir = project_dir / "data"
    analysis_dir = project_dir / "analysis"
    data_dir.mkdir(parents=True, exist_ok=True)
    analysis_dir.mkdir(parents=True, exist_ok=True)

    date_tag = end_date.strftime("%Y%m%d")
    results = {}

    # 1. Pull DAU (_active, uniques)
    print("  → Pulling DAU (_active)...")
    try:
        dau_resp = query_segmentation("_active", start_str, end_str, metric="uniques")
        dau_series = extract_daily_series(dau_resp)
        results["dau_daily"] = dau_series
        print(f"    ✓ Got {len(dau_series)} days of DAU data")
    except Exception as e:
        print(f"    ✗ DAU pull failed: {e}")
        dau_series = {}

    # 2. Pull daily signups
    print("  → Pulling signups (Cenoa sign-up completed)...")
    try:
        signup_resp = query_segmentation("Cenoa sign-up completed", start_str, end_str, metric="uniques")
        signup_series = extract_daily_series(signup_resp)
        results["signups_daily"] = signup_series
        print(f"    ✓ Got {len(signup_series)} days of signup data")
    except Exception as e:
        print(f"    ✗ Signup pull failed: {e}")
        signup_series = {}

    # 3. Pull "Application opened" by country
    print("  → Pulling 'Application opened' by country...")
    try:
        country_resp = query_segmentation(
            "Application opened", start_str, end_str,
            metric="uniques", group_by="country"
        )
        country_data = extract_grouped_series(country_resp)
        results["app_opened_by_country"] = country_data
        print(f"    ✓ Got data for {len(country_data)} countries")
    except Exception as e:
        print(f"    ✗ Country pull failed: {e}")
        country_data = {}

    # 4. Compute engagement ratios
    print("  → Computing engagement metrics...")
    engagement = compute_engagement_ratios(dau_series) if dau_series else {}
    results["engagement"] = engagement

    # 5. Compute retention proxy
    print("  → Computing retention proxies...")
    retention_proxy = compute_retention_proxy(signup_series, dau_series) if signup_series and dau_series else {}
    results["retention_proxy"] = {
        k: v for k, v in retention_proxy.items() if k != "daily_breakdown"
    }
    results["retention_proxy_daily"] = retention_proxy.get("daily_breakdown", [])

    # 6. Country activity analysis
    print("  → Analyzing country activity...")
    country_activity = analyze_country_activity(country_data) if country_data else []
    results["country_activity_top10"] = country_activity

    # Write JSON
    json_path = data_dir / f"retention-{date_tag}.json"
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n  💾 JSON → {json_path}")

    # Generate and write report
    report = generate_report(engagement, retention_proxy, country_activity, dau_series, signup_series, end_pretty)
    md_path = analysis_dir / "retention.md"
    with open(md_path, "w") as f:
        f.write(report)
    print(f"  📝 Report → {md_path}")

    # Print summary
    print("\n" + "=" * 60)
    if engagement:
        print(f"  Avg DAU (7d):  {engagement.get('avg_dau_7d', 'N/A'):,.0f}")
        print(f"  Avg DAU (30d): {engagement.get('avg_dau_30d', 'N/A'):,.0f}")
    if retention_proxy:
        print(f"  Total Signups: {retention_proxy.get('total_signups_period', 'N/A'):,}")
        print(f"  Crude Retention: {retention_proxy.get('crude_retention_pct', 'N/A'):.1f}%")
    if country_activity:
        top = country_activity[0]
        print(f"  Top Country: {top['country']} ({top['total_opens_30d']:,} opens)")
    print("=" * 60)


if __name__ == "__main__":
    main()
