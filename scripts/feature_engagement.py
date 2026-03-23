#!/usr/bin/env python3
"""Pull feature engagement events by country from Amplitude API."""

import json
import requests
from requests.auth import HTTPBasicAuth

API_KEY = "1adec44d0d2d73321b08f4de26441ebd"
SECRET_KEY = "3a48a09cb7b7ef5ec8379b0a83e24696"
AUTH = HTTPBasicAuth(API_KEY, SECRET_KEY)

EVENTS = [
    "Get Paid Opened",
    "Money Transfer Clicked on Homepage",
    "Deposit Tapped on Homepage",
    "Debit Card Tab Visited",
    "Financial Assistant Opened",
]

BASE_URL = "https://amplitude.com/api/2/events/segmentation"

results = {}

for event_name in EVENTS:
    params = {
        "e": json.dumps({"event_type": event_name}),
        "m": "totals",
        "start": "20260314",
        "end": "20260320",
        "g": "country",
    }
    print(f"Fetching: {event_name}")
    resp = requests.get(BASE_URL, params=params, auth=AUTH)
    print(f"  Status: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        results[event_name] = data
        
        # Parse series
        series = data.get("data", {}).get("series", [])
        labels = data.get("data", {}).get("seriesLabels", [])
        
        print(f"  Labels count: {len(labels)}")
        
        # Calculate totals per country
        country_totals = {}
        for i, label in enumerate(labels):
            country = label[0] if isinstance(label, list) else label
            if i < len(series):
                total = sum(series[i])
                country_totals[country] = total
        
        # Sort by total descending
        sorted_countries = sorted(country_totals.items(), key=lambda x: x[1], reverse=True)
        grand_total = sum(v for v in country_totals.values())
        
        print(f"  Grand total: {grand_total}")
        print(f"  Top 5: {sorted_countries[:5]}")
        print()
    else:
        print(f"  Error: {resp.text[:300]}")
        results[event_name] = {"error": resp.text[:500]}

# Save raw results
output = {
    "period": "2026-03-14 to 2026-03-20",
    "metric": "totals",
    "events": {}
}

for event_name in EVENTS:
    data = results.get(event_name, {})
    if "error" in data:
        output["events"][event_name] = {"error": data["error"]}
        continue
    
    series = data.get("data", {}).get("series", [])
    labels = data.get("data", {}).get("seriesLabels", [])
    
    country_totals = {}
    for i, label in enumerate(labels):
        country = label[0] if isinstance(label, list) else label
        if i < len(series):
            total = sum(series[i])
            if total > 0:
                country_totals[country] = total
    
    sorted_countries = sorted(country_totals.items(), key=lambda x: x[1], reverse=True)
    grand_total = sum(v for v in country_totals.values())
    
    output["events"][event_name] = {
        "total": grand_total,
        "top_countries": [{"country": c, "count": n, "pct": round(n/grand_total*100, 1) if grand_total > 0 else 0} for c, n in sorted_countries[:10]],
        "all_countries": dict(sorted_countries)
    }

with open("projects/cenoa-growth-engine/data/feature-engagement-20260320.json", "w") as f:
    json.dump(output, f, indent=2)

print("\n=== SAVED JSON ===")
print(json.dumps(output, indent=2))
