#!/usr/bin/env python3
"""
Amplitude Attribution Breakdown Script
Pulls funnel events grouped by media source and campaign from Amplitude Segmentation API.

Date Convention (S3-014):
  - Weekly = ISO week: Monday 00:00 UTC to Sunday 23:59 UTC
  - MTD = 1st of month 00:00 UTC to current day 23:59 UTC
  - All Amplitude API calls use YYYYMMDD format
  - Default range: last 2 complete ISO weeks (Mon-Sun)
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_DIR = PROJECT_DIR / "data"

API_URL = "https://amplitude.com/api/2/events/segmentation"

FUNNEL_EVENTS = [
    "[AppsFlyer] Install",
    "Cenoa sign-up completed",
    "Withdraw Completed",
]


def load_credentials():
    env_file = Path.home() / ".openclaw" / "credentials" / "amplitude.env"
    creds = {}
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                creds[k.strip()] = v.strip()
    return creds["AMPLITUDE_API_KEY"], creds["AMPLITUDE_SECRET_KEY"]


def fetch_segmentation(api_key, secret_key, event_type, group_by_prop, start, end):
    """Fetch segmentation data from Amplitude using curl."""
    e_param = json.dumps({
        "event_type": event_type,
        "group_by": [{"type": "user", "value": group_by_prop}]
    })

    cmd = [
        "curl", "-s", "-u", f"{api_key}:{secret_key}",
        "--data-urlencode", f"e={e_param}",
        "--data-urlencode", "m=totals",
        "--data-urlencode", f"start={start}",
        "--data-urlencode", f"end={end}",
        "-G", API_URL,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: curl failed for {event_type}: {result.stderr}", file=sys.stderr)
        return None

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"  ERROR: Invalid JSON for {event_type}: {result.stdout[:200]}", file=sys.stderr)
        return None

    if "data" not in data:
        print(f"  ERROR: No data key for {event_type}: {json.dumps(data)[:300]}", file=sys.stderr)
        return None

    return data["data"]


def parse_series(data):
    """Parse seriesLabels and seriesCollapsed into {label: value} dict."""
    results = {}
    labels = data.get("seriesLabels", [])
    collapsed = data.get("seriesCollapsed", [])

    for i, label_arr in enumerate(labels):
        label = label_arr[1] if len(label_arr) > 1 else label_arr[0]
        value = 0
        if i < len(collapsed) and len(collapsed[i]) > 0:
            val_entry = collapsed[i][0]
            if isinstance(val_entry, dict):
                value = val_entry.get("value", 0)
            else:
                value = val_entry
        results[label] = value

    # Sort descending by value
    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))


def main():
    parser = argparse.ArgumentParser(description="Amplitude attribution breakdown")
    # ISO week boundaries: last 2 complete weeks (Mon-Sun)
    today = datetime.utcnow()
    last_sunday = today - timedelta(days=today.weekday() + 1)  # Most recent Sunday
    two_weeks_ago_monday = last_sunday - timedelta(days=13)    # Monday 2 weeks before
    default_end = last_sunday.strftime("%Y%m%d")
    default_start = two_weeks_ago_monday.strftime("%Y%m%d")

    parser.add_argument("--start", default=default_start, help="Start date YYYYMMDD")
    parser.add_argument("--end", default=default_end, help="End date YYYYMMDD")
    args = parser.parse_args()

    start, end = args.start, args.end
    print(f"Amplitude Attribution Breakdown: {start} → {end}\n")

    api_key, secret_key = load_credentials()
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    output = {
        "date_range": {"start": start, "end": end},
        "by_media_source": {},
        "by_campaign": {},
    }

    # 1) Funnel events by media source
    print("=" * 60)
    print("FUNNEL EVENTS BY MEDIA SOURCE")
    print("=" * 60)

    for event in FUNNEL_EVENTS:
        print(f"\n📊 {event}")
        data = fetch_segmentation(api_key, secret_key, event, "gp:[AppsFlyer] media source", start, end)
        if data is None:
            output["by_media_source"][event] = {}
            continue
        parsed = parse_series(data)
        output["by_media_source"][event] = parsed

        for source, count in parsed.items():
            print(f"  {source}: {count:,.0f}")
        if not parsed:
            print("  (no data)")

    # 2) Installs by campaign
    print(f"\n{'=' * 60}")
    print("INSTALLS BY CAMPAIGN")
    print("=" * 60)

    event_campaign = "[AppsFlyer] Install"
    print(f"\n📊 {event_campaign} (by campaign)")
    data = fetch_segmentation(api_key, secret_key, event_campaign, "gp:[AppsFlyer] campaign", start, end)
    if data:
        parsed = parse_series(data)
        output["by_campaign"][event_campaign] = parsed
        for campaign, count in parsed.items():
            print(f"  {campaign}: {count:,.0f}")
        if not parsed:
            print("  (no data)")
    else:
        output["by_campaign"][event_campaign] = {}

    # Save JSON
    out_file = DATA_DIR / f"amplitude-attribution-{end}.json"
    with open(out_file, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n✅ Saved to {out_file}")


if __name__ == "__main__":
    main()
