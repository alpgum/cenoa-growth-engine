#!/usr/bin/env python3
"""
Retention curve analysis via Amplitude APIs.
Try Retention API first, fall back to Segmentation/Export approach.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse
import base64
from datetime import datetime, timedelta

API_KEY = os.environ["AMPLITUDE_API_KEY"]
SECRET_KEY = os.environ["AMPLITUDE_SECRET_KEY"]

auth_string = base64.b64encode(f"{API_KEY}:{SECRET_KEY}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {auth_string}",
    "Content-Type": "application/json"
}

END_DATE = "20260322"
START_DATE = "20251222"  # ~90 days back

def amplitude_get(url):
    """Make authenticated GET request to Amplitude."""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"HTTP {e.code}: {body[:500]}", file=sys.stderr)
        return None

def try_retention_api():
    """Try the Amplitude Retention Analysis API."""
    # Retention API endpoint
    # https://www.docs.developers.amplitude.com/analytics/apis/dashboard-rest-api/#retention-analysis
    
    base = "https://amplitude.com/api/2/retention"
    
    # Try with different first/return event configs
    configs = [
        {
            "name": "install_any",
            "se": json.dumps({"event_type": "[AppsFlyer] Install"}),
            "re": json.dumps({"event_type": "_active"}),  # any active event
        },
        {
            "name": "signup_any",
            "se": json.dumps({"event_type": "Cenoa sign-up completed"}),
            "re": json.dumps({"event_type": "_active"}),
        },
        {
            "name": "signup_withdraw",
            "se": json.dumps({"event_type": "Cenoa sign-up completed"}),
            "re": json.dumps({"event_type": "Withdraw Completed"}),
        },
    ]
    
    results = {}
    for cfg in configs:
        params = {
            "se": cfg["se"],
            "re": cfg["re"],
            "s": START_DATE,
            "e": END_DATE,
            "rm": "bracket",  # bracket retention mode
            "rb": "1,7,14,30",  # retention brackets D1,D7,D14,D30
        }
        url = base + "?" + urllib.parse.urlencode(params)
        print(f"Trying retention API with config: {cfg['name']}")
        print(f"URL: {url[:200]}...")
        
        data = amplitude_get(url)
        if data:
            results[cfg["name"]] = data
            print(f"  -> Success! Keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
        else:
            print(f"  -> Failed")
    
    return results

def try_retention_with_group_by():
    """Try retention API with country group-by."""
    base = "https://amplitude.com/api/2/retention"
    
    params = {
        "se": json.dumps({"event_type": "Cenoa sign-up completed"}),
        "re": json.dumps({"event_type": "_active"}),
        "s": START_DATE,
        "e": END_DATE,
        "rm": "bracket",
        "rb": "1,7,14,30",
        "g": "country",  # group by country
    }
    url = base + "?" + urllib.parse.urlencode(params)
    print(f"\nTrying retention API with country group-by...")
    
    data = amplitude_get(url)
    if data:
        print(f"  -> Success! Keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
    return data

def try_segmentation_active_users():
    """Fall back to segmentation API for user counts by cohort."""
    base = "https://amplitude.com/api/2/events/segmentation"
    
    # Get signup counts by country
    params = {
        "e": json.dumps({"event_type": "Cenoa sign-up completed"}),
        "s": START_DATE,
        "e2": END_DATE,
        "m": "uniques",
        "g": "country",
        "i": "7",  # weekly intervals
    }
    # Note: 'e2' should be 'end' - let me use the right param name
    url = base + "?" + urllib.parse.urlencode({
        "e": json.dumps({"event_type": "Cenoa sign-up completed"}),
        "start": START_DATE,
        "end": END_DATE,
        "m": "uniques",
        "g": "country",
        "i": "7",
    })
    print(f"\nTrying segmentation API for signups by country...")
    
    data = amplitude_get(url)
    if data:
        print(f"  -> Success!")
    return data

def try_retention_n_day():
    """Try retention API with n-day mode instead of bracket."""
    base = "https://amplitude.com/api/2/retention"
    
    for ret_mode in ["rolling", "n-day", "bracket", "unbounded"]:
        params = {
            "se": json.dumps({"event_type": "Cenoa sign-up completed"}),
            "re": json.dumps({"event_type": "_active"}),
            "s": START_DATE,
            "e": END_DATE,
            "rm": ret_mode,
        }
        url = base + "?" + urllib.parse.urlencode(params)
        print(f"\nTrying retention API mode={ret_mode}...")
        
        data = amplitude_get(url)
        if data:
            print(f"  -> Success! Keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
            # Print first few lines of data
            preview = json.dumps(data, indent=2)[:1000]
            print(f"  Preview: {preview}")
            return data, ret_mode
    
    return None, None

def try_simple_retention():
    """Simplest possible retention API call."""
    base = "https://amplitude.com/api/2/retention"
    
    params = {
        "se": json.dumps({"event_type": "Cenoa sign-up completed"}),
        "re": json.dumps({"event_type": "Withdraw Completed"}),
        "s": START_DATE,
        "e": END_DATE,
    }
    url = base + "?" + urllib.parse.urlencode(params)
    print(f"\nTrying simplest retention API call...")
    
    data = amplitude_get(url)
    if data:
        print(f"  -> Success! Type: {type(data)}")
        preview = json.dumps(data, indent=2)[:2000]
        print(f"  Preview: {preview}")
    return data


if __name__ == "__main__":
    print("=" * 60)
    print("Amplitude Retention Curve Analysis")
    print(f"Period: {START_DATE} to {END_DATE}")
    print("=" * 60)
    
    # Try 1: Simple retention
    simple = try_simple_retention()
    
    # Try 2: Multiple configs
    multi = try_retention_api()
    
    # Try 3: N-day modes
    nday_data, nday_mode = try_retention_n_day()
    
    # Try 4: With country group-by
    country_data = try_retention_with_group_by()
    
    # Try 5: Segmentation fallback
    seg_data = try_segmentation_active_users()
    
    # Collect all results
    all_results = {
        "simple_retention": simple,
        "multi_config": multi,
        "nday": {"data": nday_data, "mode": nday_mode} if nday_data else None,
        "country_retention": country_data,
        "segmentation": seg_data,
    }
    
    # Save raw results
    with open("data/retention-api-raw.json", "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    
    print("\n\nResults saved to data/retention-api-raw.json")
