#!/usr/bin/env python3
"""Pull platform breakdown from Amplitude for funnel analysis."""

import json
import requests
import urllib.parse
import os

API_KEY = "1adec44d0d2d73321b08f4de26441ebd"
SECRET_KEY = "3a48a09cb7b7ef5ec8379b0a83e24696"

EVENTS = [
    "[AppsFlyer] Install",
    "Application first opened",
    "Cenoa sign-up completed",
    "KYC Started",
    "Bridgexyz KYC Component: Submit clicked",
    "Deposit Completed",
    "Withdraw Completed",
]

BASE_URL = "https://amplitude.com/api/2/events/segmentation"

results = {}

for event_type in EVENTS:
    e_param = json.dumps({
        "event_type": event_type,
        "group_by": [{"type": "user", "value": "platform"}]
    })
    params = {
        "e": e_param,
        "start": "20260314",
        "end": "20260320",
        "m": "totals",
    }
    
    print(f"Fetching: {event_type}...")
    resp = requests.get(
        BASE_URL,
        params=params,
        auth=(API_KEY, SECRET_KEY),
        timeout=30
    )
    
    if resp.status_code == 200:
        data = resp.json()
        results[event_type] = data
        # Extract platform totals
        series = data.get("data", {}).get("series", [])
        labels = data.get("data", {}).get("seriesLabels", [])
        print(f"  Status: OK | Labels: {labels}")
        for i, label in enumerate(labels):
            if i < len(series):
                total = sum(series[i]) if isinstance(series[i], list) else series[i]
                print(f"    {label}: {total}")
    else:
        print(f"  ERROR {resp.status_code}: {resp.text[:200]}")
        results[event_type] = {"error": resp.status_code, "body": resp.text[:500]}

# Save raw data
out_path = os.path.expanduser("~/.openclaw/workspace/projects/cenoa-growth-engine/data/platform-breakdown-20260320.json")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"\nSaved to {out_path}")
