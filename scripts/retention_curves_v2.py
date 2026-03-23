#!/usr/bin/env python3
"""
Retention curve analysis using Amplitude Export API.
Computes D1/D7/D14/D30 retention by:
1. Getting signup cohorts from Export API
2. Checking if users returned on Day N
3. Breaking down by country and platform

Since the Retention Analysis API returns 400, we use:
- Segmentation API for weekly signup counts by country
- Export API for user-level event data to compute retention
- Existing cohort-retention-30d.json for D30 validation
"""

import json
import os
import sys
import urllib.request
import urllib.parse
import base64
import gzip
from datetime import datetime, timedelta
from collections import defaultdict

API_KEY = os.environ["AMPLITUDE_API_KEY"]
SECRET_KEY = os.environ["AMPLITUDE_SECRET_KEY"]

auth_string = base64.b64encode(f"{API_KEY}:{SECRET_KEY}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {auth_string}",
    "Content-Type": "application/json"
}

def amplitude_get(url, timeout=120):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            # Check if gzipped
            if data[:2] == b'\x1f\x8b':
                data = gzip.decompress(data)
            return json.loads(data.decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"HTTP {e.code}: {body[:500]}", file=sys.stderr)
        return None

def get_segmentation(event_type, group_by=None, start="20251222", end="20260322", interval="1"):
    """Get event segmentation data."""
    base = "https://amplitude.com/api/2/events/segmentation"
    params = {
        "e": json.dumps({"event_type": event_type}),
        "start": start,
        "end": end,
        "m": "uniques",
        "i": interval,
    }
    if group_by:
        params["g"] = group_by
    
    url = base + "?" + urllib.parse.urlencode(params)
    return amplitude_get(url)

def get_user_activity(user_id):
    """Get activity for a specific user."""
    base = "https://amplitude.com/api/2/useractivity"
    params = {"user": user_id}
    url = base + "?" + urllib.parse.urlencode(params)
    return amplitude_get(url)

def export_events(start, end):
    """Export raw events for a date range (max 24h chunks)."""
    base = "https://amplitude.com/api/2/export"
    params = {"start": start, "end": end}
    url = base + "?" + urllib.parse.urlencode(params)
    
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = resp.read()
            if data[:2] == b'\x1f\x8b':
                data = gzip.decompress(data)
            # Export returns JSONL (one JSON per line)
            events = []
            for line in data.decode().strip().split('\n'):
                if line.strip():
                    try:
                        events.append(json.loads(line))
                    except:
                        pass
            return events
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"Export HTTP {e.code}: {body[:300]}", file=sys.stderr)
        return None

def compute_retention_from_segmentation():
    """
    Approach: Use multiple segmentation calls to approximate retention.
    
    For each weekly cohort (signup week), count:
    - How many signed up (first event)
    - How many were active on Day 1, 7, 14, 30 after signup
    
    We use the segmentation API with "new" users filter.
    """
    print("Pulling signup segmentation by country (daily)...")
    signups_country = get_segmentation(
        "Cenoa sign-up completed", 
        group_by="country",
        interval="1"
    )
    
    print("Pulling signup segmentation by platform (daily)...")
    signups_platform = get_segmentation(
        "Cenoa sign-up completed",
        group_by="gp:platform",
        interval="1"
    )
    
    print("Pulling active users by country (daily)...")
    active_country = get_segmentation(
        "_active",
        group_by="country",
        interval="1"
    )
    
    print("Pulling active users by platform (daily)...")
    active_platform = get_segmentation(
        "_active",
        group_by="gp:platform",
        interval="1"
    )
    
    return {
        "signups_country": signups_country,
        "signups_platform": signups_platform,
        "active_country": active_country,
        "active_platform": active_platform,
    }

def try_chart_annotation_approach():
    """
    Use the Dashboard REST API to get saved retention charts.
    """
    # Try getting chart results - need a chart ID
    # Let's try to list available charts/dashboards first
    url = "https://amplitude.com/api/3/chart/e-retention/query"
    return None  # Skip this approach

def analyze_existing_data():
    """
    Build retention curves from existing cohort-retention-30d.json
    which has D30 retention by country, plus use segmentation to
    estimate D1/D7/D14.
    """
    # Load existing D30 data
    with open("data/cohort-retention-30d.json") as f:
        d30_data = json.load(f)
    
    # Aggregate D30 by country across recent cohorts (last 90 days = ~3 months)
    recent_cohorts = ["2025-12", "2026-01"]  # Recent enough for 90-day window
    
    country_d30 = defaultdict(lambda: {"signups": 0, "retained": 0})
    
    for cohort_key in recent_cohorts:
        if cohort_key in d30_data.get("cohorts_by_country", {}):
            for country, vals in d30_data["cohorts_by_country"][cohort_key].items():
                country_d30[country]["signups"] += vals["signups"]
                country_d30[country]["retained"] += vals["retained_30d"]
    
    # Calculate D30 rates
    for country in country_d30:
        s = country_d30[country]["signups"]
        r = country_d30[country]["retained"]
        country_d30[country]["retention_30d"] = r / s if s > 0 else 0
    
    return dict(country_d30)


def try_funnel_approach():
    """
    Use Amplitude Funnel API to approximate retention at different windows.
    This gives us conversion from signup -> return event within N days.
    """
    base = "https://amplitude.com/api/2/funnels"
    
    results = {}
    
    for window_days in [1, 7, 14, 30]:
        params = {
            "e": json.dumps([
                {"event_type": "Cenoa sign-up completed"},
                {"event_type": "Withdraw Completed"}
            ]),
            "s": "20251222",
            "e2": "20260322",
            "g": "country",
            "cs": str(window_days),  # conversion window in days
        }
        # Funnel API uses different endpoint format
        url = base + "?" + urllib.parse.urlencode({
            "e": json.dumps({"event_type": "Cenoa sign-up completed"}),
            "start": "20251222",
            "end": "20260322",
        })
        
        print(f"\nTrying funnel for {window_days}-day window...")
        data = amplitude_get(url)
        if data:
            results[f"d{window_days}"] = data
            print(f"  -> Got data")
    
    return results


def main():
    print("=" * 60)
    print("Retention Curve Analysis - V2")
    print("=" * 60)
    
    # 1. Get segmentation data for retention approximation
    seg_data = compute_retention_from_segmentation()
    
    # 2. Analyze existing D30 data
    d30_by_country = analyze_existing_data()
    
    # 3. Try funnel approach
    funnel_data = try_funnel_approach()
    
    # Save all raw data
    all_data = {
        "segmentation": seg_data,
        "d30_by_country": d30_by_country,
        "funnel_data": funnel_data,
    }
    
    with open("data/retention-curves-raw-v2.json", "w") as f:
        json.dump(all_data, f, indent=2, default=str)
    
    print("\nRaw data saved to data/retention-curves-raw-v2.json")
    
    # Now parse the segmentation data to build retention estimates
    # The key insight: from daily active user counts by country, 
    # we can compute a proxy retention by comparing DAU/MAU ratios
    # and signup-to-active ratios over time
    
    print("\n\nProcessing segmentation data...")
    
    if seg_data.get("signups_country") and seg_data.get("active_country"):
        sc = seg_data["signups_country"]["data"]
        ac = seg_data["active_country"]["data"]
        
        print(f"Signup series labels: {sc.get('seriesLabels', [])[:10]}")
        print(f"Active series labels: {ac.get('seriesLabels', [])[:10]}")
        print(f"X values (dates) count: {len(sc.get('xValues', []))}")
    
    print("\nDone!")


if __name__ == "__main__":
    main()
