#!/usr/bin/env python3
"""Pull attribution funnel data from Amplitude API."""

import json
import requests
import urllib.parse
from pathlib import Path

API_KEY = "1adec44d0d2d73321b08f4de26441ebd"
SECRET_KEY = "3a48a09cb7b7ef5ec8379b0a83e24696"
BASE = "https://amplitude.com/api/2/events/segmentation"

START = "20260314"
END = "20260320"

results = {}

# 1) Three events grouped by media source
events_by_source = [
    "[AppsFlyer] Install",
    "Cenoa sign-up completed",
    "Withdraw Completed"
]

for evt in events_by_source:
    e_param = json.dumps({
        "event_type": evt,
        "group_by": [{"type": "user", "value": "gp:[AppsFlyer] media source"}]
    })
    params = {"e": e_param, "start": START, "end": END, "m": "totals"}
    print(f"Fetching: {evt} by media source...")
    resp = requests.get(BASE, params=params, auth=(API_KEY, SECRET_KEY), timeout=30)
    print(f"  Status: {resp.status_code}")
    if resp.status_code == 200:
        results[f"{evt}_by_source"] = resp.json()
    else:
        print(f"  Error: {resp.text[:500]}")
        results[f"{evt}_by_source"] = {"error": resp.status_code, "body": resp.text[:500]}

# 2) Install by campaign
e_param = json.dumps({
    "event_type": "[AppsFlyer] Install",
    "group_by": [{"type": "user", "value": "gp:[AppsFlyer] campaign"}]
})
params = {"e": e_param, "start": START, "end": END, "m": "totals"}
print("Fetching: Install by campaign...")
resp = requests.get(BASE, params=params, auth=(API_KEY, SECRET_KEY), timeout=30)
print(f"  Status: {resp.status_code}")
if resp.status_code == 200:
    results["install_by_campaign"] = resp.json()
else:
    print(f"  Error: {resp.text[:500]}")
    results["install_by_campaign"] = {"error": resp.status_code, "body": resp.text[:500]}

# 3) Also pull sign-up and withdraw by campaign for downstream conversion
for evt in ["Cenoa sign-up completed", "Withdraw Completed"]:
    e_param = json.dumps({
        "event_type": evt,
        "group_by": [{"type": "user", "value": "gp:[AppsFlyer] campaign"}]
    })
    params = {"e": e_param, "start": START, "end": END, "m": "totals"}
    print(f"Fetching: {evt} by campaign...")
    resp = requests.get(BASE, params=params, auth=(API_KEY, SECRET_KEY), timeout=30)
    print(f"  Status: {resp.status_code}")
    if resp.status_code == 200:
        results[f"{evt}_by_campaign"] = resp.json()
    else:
        print(f"  Error: {resp.text[:500]}")
        results[f"{evt}_by_campaign"] = {"error": resp.status_code, "body": resp.text[:500]}

# Save
out_path = Path("/Users/alperengumusdograyan/.openclaw/workspace/projects/cenoa-growth-engine/data/attribution-breakdown-20260320.json")
out_path.write_text(json.dumps(results, indent=2, default=str))
print(f"\nSaved to {out_path}")
print(f"Keys: {list(results.keys())}")
