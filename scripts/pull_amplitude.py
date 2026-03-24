#!/usr/bin/env python3
"""Pull Amplitude funnel data: install, signup, KYC start, KYC complete, withdraw.

Groups by country and platform. Returns a dict ready for unified data.json.
"""

import json
import os
import sys
from datetime import datetime, timedelta

import requests

AMPLITUDE_API_URL = "https://amplitude.com/api/2/events/segmentation"

FUNNEL_EVENTS = {
    "install": "[AppsFlyer] Install",
    "signup": "Cenoa sign-up completed",
    "kycStart": "KYC Started",
    "kycComplete": "Bridgexyz KYC Component: Submit clicked",
    "withdraw": "Withdraw Completed",
}

GROUP_BY_COUNTRY = [{"type": "user", "value": "country"}]
GROUP_BY_PLATFORM = [{"type": "user", "value": "platform"}]

# Map full country names to ISO 2-letter codes (top markets + common ones)
COUNTRY_CODE_MAP = {
    "Turkey": "TR", "Nigeria": "NG", "Egypt": "EG", "Pakistan": "PK",
    "United States": "US", "Germany": "DE", "United Kingdom": "GB",
    "Ghana": "GH", "Kenya": "KE", "Saudi Arabia": "SA",
    "United Arab Emirates": "AE", "France": "FR", "Netherlands": "NL",
    "Greece": "GR", "Cyprus": "CY", "Poland": "PL", "Sweden": "SE",
    "Brazil": "BR", "Russia": "RU", "Ukraine": "UA", "Indonesia": "ID",
    "Malaysia": "MY", "Thailand": "TH", "Iraq": "IQ", "Kuwait": "KW",
    "Georgia": "GE", "Azerbaijan": "AZ", "Hungary": "HU", "Iceland": "IS",
    "Afghanistan": "AF", "Montenegro": "ME", "Serbia": "RS",
    "(none)": "XX",
}


def _country_code(name):
    return COUNTRY_CODE_MAP.get(name, name[:2].upper() if name else "XX")


def load_credentials():
    env_file = os.path.expanduser("~/.openclaw/credentials/amplitude.env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
    api_key = os.environ.get("AMPLITUDE_API_KEY")
    secret_key = os.environ.get("AMPLITUDE_SECRET_KEY")
    if not api_key or not secret_key:
        print("ERROR: AMPLITUDE_API_KEY and AMPLITUDE_SECRET_KEY required", file=sys.stderr)
        sys.exit(1)
    return api_key, secret_key


def _query(api_key, secret_key, event_type, start, end, group_by=None):
    """Query Amplitude segmentation API. Returns {segment_value: total}."""
    e_param = {"event_type": event_type}
    if group_by:
        e_param["group_by"] = group_by

    params = {
        "e": json.dumps(e_param),
        "start": start,
        "end": end,
        "m": "totals",
    }
    resp = requests.get(AMPLITUDE_API_URL, params=params, auth=(api_key, secret_key), timeout=30)
    resp.raise_for_status()
    data = resp.json().get("data", {})

    series = data.get("series", [])
    labels = data.get("seriesLabels", [])

    if not group_by:
        # No grouping: series is [[val, val, ...]]
        return {"_total": sum(series[0]) if series and series[0] else 0}

    # With grouping: series[i] corresponds to labels[i]
    # Labels format: [[0, "Turkey"], [0, "Nigeria"], ...]
    result = {}
    for i, label in enumerate(labels):
        if isinstance(label, list) and len(label) >= 2:
            segment_key = str(label[1])
        else:
            segment_key = str(label)
        vals = series[i] if i < len(series) else []
        result[segment_key] = sum(vals) if vals else 0
    return result


def _iso_week_range():
    """Return (start, end) for the last complete ISO week as YYYYMMDD strings."""
    today = datetime.utcnow()
    last_sunday = today - timedelta(days=today.weekday() + 1)
    last_monday = last_sunday - timedelta(days=6)
    return last_monday.strftime("%Y%m%d"), last_sunday.strftime("%Y%m%d")


def pull(start=None, end=None):
    """Pull Amplitude funnel data. Returns dict for unified data.json."""
    api_key, secret_key = load_credentials()

    if not start or not end:
        start, end = _iso_week_range()

    print(f"  [Amplitude] Pulling {start} → {end}")

    # 1) Totals
    funnel = {}
    for key, event_type in FUNNEL_EVENTS.items():
        print(f"    {key}...", end=" ", flush=True)
        result = _query(api_key, secret_key, event_type, start, end)
        funnel[key] = result["_total"]
        print(funnel[key])

    # 2) By country
    funnel_by_country = {}
    for key, event_type in FUNNEL_EVENTS.items():
        print(f"    {key} by country...", end=" ", flush=True)
        segments = _query(api_key, secret_key, event_type, start, end, GROUP_BY_COUNTRY)
        for country_name, val in segments.items():
            code = _country_code(country_name)
            if code not in funnel_by_country:
                funnel_by_country[code] = {}
            funnel_by_country[code][key] = val
        print(f"{len(segments)} countries")

    # 3) By platform
    funnel_by_platform = {}
    for key, event_type in FUNNEL_EVENTS.items():
        print(f"    {key} by platform...", end=" ", flush=True)
        segments = _query(api_key, secret_key, event_type, start, end, GROUP_BY_PLATFORM)
        for platform, val in segments.items():
            if platform not in funnel_by_platform:
                funnel_by_platform[platform] = {}
            funnel_by_platform[platform][key] = val
        print(f"{len(segments)} platforms")

    return {
        "funnel": funnel,
        "funnelByCountry": funnel_by_country,
        "funnelByPlatform": funnel_by_platform,
        "period": {"start": start, "end": end},
    }


if __name__ == "__main__":
    data = pull()
    print(json.dumps(data, indent=2))
