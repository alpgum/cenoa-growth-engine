#!/usr/bin/env python3
"""
Amplitude Platform Breakdown Script
Pulls core funnel events segmented by platform from Amplitude's Segmentation API.

Usage:
    python amplitude_platform_breakdown.py [--start YYYYMMDD] [--end YYYYMMDD]

Date Convention (S3-014):
  - Weekly = ISO week: Monday 00:00 UTC to Sunday 23:59 UTC
  - MTD = 1st of month 00:00 UTC to current day 23:59 UTC
  - All Amplitude API calls use YYYYMMDD format
  - Default range: last 2 complete ISO weeks (Mon-Sun)
    Default: last 14 days
"""

import argparse
import base64
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path


def load_credentials():
    env_file = os.path.expanduser("~/.openclaw/credentials/amplitude.env")
    creds = {}
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                creds[key.strip()] = val.strip()
    api_key = creds.get("AMPLITUDE_API_KEY", os.environ.get("AMPLITUDE_API_KEY"))
    secret_key = creds.get("AMPLITUDE_SECRET_KEY", os.environ.get("AMPLITUDE_SECRET_KEY"))
    if not api_key or not secret_key:
        print("ERROR: AMPLITUDE_API_KEY and AMPLITUDE_SECRET_KEY required")
        sys.exit(1)
    return api_key, secret_key


FUNNEL_EVENTS = [
    "[AppsFlyer] Install",
    "Cenoa sign-up completed",
    "Bridgexyz KYC Component: Submit clicked",
    "Withdraw Completed",
    "Deposit Completed",
]

API_URL = "https://amplitude.com/api/2/events/segmentation"


def fetch_event_by_platform(api_key, secret_key, event_type, start, end):
    """Fetch a single event segmented by platform."""
    e_param = json.dumps({
        "event_type": event_type,
        "group_by": [{"type": "user", "value": "platform"}]
    })
    params = urllib.parse.urlencode({
        "e": e_param,
        "start": start,
        "end": end,
        "m": "totals",
    })
    url = f"{API_URL}?{params}"

    auth_str = f"{api_key}:{secret_key}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()

    req = urllib.request.Request(url, headers={
        "Authorization": f"Basic {auth_b64}",
        "Content-Type": "application/json",
    })

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"  HTTP {e.code} for '{event_type}': {body[:200]}")
        return None
    except Exception as e:
        print(f"  Error fetching '{event_type}': {e}")
        return None


def parse_platform_data(response_data):
    """Parse Amplitude segmentation response into platform breakdown."""
    if not response_data or "data" not in response_data:
        return {}

    data = response_data["data"]
    series_labels = data.get("seriesLabels", [])
    series_collapsed = data.get("seriesCollapsed", [])

    platform_counts = {}
    for i, label_list in enumerate(series_labels):
        platform = label_list[1] if len(label_list) > 1 else "Unknown"
        if not platform or platform in ("none", "None", ""):
            platform = "Unknown"

        value = 0
        if i < len(series_collapsed):
            collapsed = series_collapsed[i]
            if collapsed and len(collapsed) > 0:
                val_entry = collapsed[0]
                if isinstance(val_entry, dict):
                    value = val_entry.get("value", 0)
                elif isinstance(val_entry, (int, float)):
                    value = val_entry

        if value > 0:
            platform_counts[platform] = platform_counts.get(platform, 0) + value

    return platform_counts


def add_percentages(platform_counts):
    """Add percentage splits to platform data."""
    total = sum(platform_counts.values())
    if total == 0:
        return []

    result = []
    for platform, count in sorted(platform_counts.items(), key=lambda x: -x[1]):
        result.append({
            "platform": platform,
            "count": count,
            "percentage": round(count / total * 100, 2),
        })
    return result


def main():
    parser = argparse.ArgumentParser(description="Amplitude platform breakdown")
    # ISO week boundaries: last 2 complete weeks (Mon-Sun)
    today = datetime.utcnow()
    last_sunday = today - timedelta(days=today.weekday() + 1)  # Most recent Sunday
    two_weeks_ago_monday = last_sunday - timedelta(days=13)    # Monday 2 weeks before
    default_end = last_sunday.strftime("%Y%m%d")
    default_start = two_weeks_ago_monday.strftime("%Y%m%d")

    parser.add_argument("--start", default=default_start, help="Start date YYYYMMDD")
    parser.add_argument("--end", default=default_end, help="End date YYYYMMDD")
    args = parser.parse_args()

    api_key, secret_key = load_credentials()

    print(f"📱 Amplitude Platform Breakdown: {args.start} → {args.end}")
    print("=" * 60)

    results = {}
    for event in FUNNEL_EVENTS:
        print(f"\n🔍 Fetching: {event}")
        resp = fetch_event_by_platform(api_key, secret_key, event, args.start, args.end)
        platform_counts = parse_platform_data(resp)
        breakdown = add_percentages(platform_counts)
        total = sum(c.get("count", 0) for c in breakdown)

        results[event] = {
            "total": total,
            "platforms": breakdown,
        }

        # Print summary
        print(f"  Total: {total:,}")
        for entry in breakdown:
            bar = "█" * int(entry["percentage"] / 2)
            print(f"  {entry['platform']:>15s}: {entry['count']:>6,} ({entry['percentage']:>5.1f}%) {bar}")

    # Save JSON
    end_date_fmt = f"{args.end[:4]}-{args.end[4:6]}-{args.end[6:8]}"
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    output_path = data_dir / f"amplitude-platform-{end_date_fmt}.json"

    output = {
        "date_range": {"start": args.start, "end": args.end},
        "generated_at": datetime.now().isoformat(),
        "events": results,
    }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n✅ Saved to {output_path}")


if __name__ == "__main__":
    main()
