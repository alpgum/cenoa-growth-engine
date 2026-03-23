#!/usr/bin/env python3
"""Pull country breakdown from Amplitude for Mar 14-20, 2026."""

import json
import requests
import urllib.parse

API_KEY = "1adec44d0d2d73321b08f4de26441ebd"
SECRET_KEY = "3a48a09cb7b7ef5ec8379b0a83e24696"

EVENTS = [
    "[AppsFlyer] Install",
    "Cenoa sign-up completed",
    "Bridgexyz KYC Component: Submit clicked",
    "Withdraw Completed",
    "Deposit Completed",
    "KYC Started",
]

URL = "https://amplitude.com/api/2/events/segmentation"

results = {}

for event_type in EVENTS:
    e_param = json.dumps({
        "event_type": event_type,
        "group_by": [{"type": "user", "value": "country"}]
    })
    params = {
        "e": e_param,
        "start": "20260314",
        "end": "20260320",
        "m": "totals",
    }
    print(f"Fetching: {event_type}...")
    resp = requests.get(URL, params=params, auth=(API_KEY, SECRET_KEY), timeout=30)
    print(f"  Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        results[event_type] = data
    else:
        print(f"  Error: {resp.text[:200]}")
        results[event_type] = {"error": resp.status_code, "body": resp.text[:500]}

output_path = "../data/country-breakdown-20260320.json"
with open(output_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"\nSaved to {output_path}")
print("Done.")
