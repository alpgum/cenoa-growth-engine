#!/usr/bin/env python3
"""
Wrapper for weekly_channel_country.py - fetches a single week's data.
Usage: python weekly_backfill.py 20251230 20260105
"""
import json
import subprocess
import sys
import time
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_DIR = PROJECT_DIR / "data"

API_URL = "https://amplitude.com/api/2/events/segmentation"

CHANNEL_MAP = {
    "googleadwords_int": "Google",
    "Google Ads ACI": "Google",

    # Meta
    "Facebook Ads": "Meta",
    "restricted": "Meta",
    "Social_instagram": "Meta",

    # Apple
    "Apple Search Ads": "ASA",

    # Google via 3rd-party buying platform
    "Architect": "Google",

    # Other paid networks
    "appnext_int": "Appnext",
    "bytedanceglobal_int": "TikTok",
    "tiktokglobal_int": "TikTok",

    # Referral / owned
    "af_app_invites": "Referral",
    "referral": "Referral",
    "Braze_refer-a-friend": "Referral",

    # Organic / direct / unattributed
    "organic": "Organic",
    "Organic": "Organic",
    "(none)": "Organic",
    "": "Organic",
    "Web Onboarding": "Organic",
    "cenoa.com": "Organic",
    "cenoacomtr": "Organic",
}

OTHER_PAID = {
    "zzgtechltmqk_int",
    "byteboost2_int",
    "Auto Pilot Tool",
    "Egypt LTV Test",
    "Eihracat Yıldızları",
}

_overlap = set(CHANNEL_MAP).intersection(OTHER_PAID)
if _overlap:
    raise RuntimeError(f"Channel mapping overlap between CHANNEL_MAP and OTHER_PAID: {sorted(_overlap)}")

COUNTRY_NAMES = {
    "Turkey": "TR", "Türkiye": "TR", "TR": "TR",
    "Nigeria": "NG", "NG": "NG",
    "Egypt": "EG", "EG": "EG",
    "Pakistan": "PK", "PK": "PK",
}

def get_channel(media_source, campaign=""):
    ms = (media_source or "").strip()
    if ms in OTHER_PAID:
        return "Other"
    base = CHANNEL_MAP.get(ms, None)
    if base == "Google":
        c = (campaign or "").lower()
        if "pmax" in c or "performance max" in c:
            return "Google Pmax"
        if "brand" in c:
            return "Google Brand"
        return "Google Search"
    if base == "Meta":
        c = (campaign or "").lower()
        if "w2a" in c or "web" in c or "web2app" in c:
            return "Meta W2A"
        return "Meta App"
    if base is not None:
        return base
    if not ms or ms in ("(none)", "None", "null"):
        return "Organic"
    return "Other"

def get_country_bucket(country):
    if not country:
        return "Other"
    return COUNTRY_NAMES.get(country.strip(), "Other")

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

def fetch_segmentation(api_key, secret_key, event_type, group_by_props, start, end, metric="uniques"):
    e_param = json.dumps({"event_type": event_type, "group_by": group_by_props})
    cmd = [
        "curl", "-s", "-u", f"{api_key}:{secret_key}",
        "--data-urlencode", f"e={e_param}",
        "--data-urlencode", f"m={metric}",
        "--data-urlencode", f"start={start}",
        "--data-urlencode", f"end={end}",
        "-G", API_URL,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR curl: {event_type}: {result.stderr}", file=sys.stderr)
        return None
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"  ERROR JSON: {event_type}: {result.stdout[:300]}", file=sys.stderr)
        return None
    if "data" not in data:
        print(f"  WARN no data: {event_type}: {json.dumps(data)[:300]}", file=sys.stderr)
        return None
    return data["data"]

def parse_segmentation(data):
    results = []
    labels = data.get("seriesLabels", [])
    collapsed = data.get("seriesCollapsed", [])
    for i, label_entry in enumerate(labels):
        if isinstance(label_entry, list) and len(label_entry) >= 2:
            raw_label = str(label_entry[1])
            group_values = [v.strip() for v in raw_label.split(";")]
        elif isinstance(label_entry, (int, float)):
            group_values = []
        else:
            group_values = [str(label_entry)]
        val = 0
        if i < len(collapsed):
            c = collapsed[i]
            if isinstance(c, list) and len(c) > 0:
                if isinstance(c[0], dict):
                    val = c[0].get("value", 0)
                elif isinstance(c[0], (int, float)):
                    val = c[0]
            elif isinstance(c, dict):
                val = c.get("value", 0)
            elif isinstance(c, (int, float)):
                val = c
        results.append((group_values, int(val)))
    return results

def aggregate_by_ms_and_country(parsed):
    agg = defaultdict(int)
    for group_values, val in parsed:
        if len(group_values) >= 2:
            ms, country = group_values[0], group_values[1]
        elif len(group_values) == 1:
            ms, country = group_values[0], ""
        else:
            ms, country = "", ""
        channel = get_channel(ms)
        cb = get_country_bucket(country)
        agg[(channel, cb)] += val
    return dict(agg)

def aggregate_by_country(parsed):
    agg = defaultdict(int)
    for group_values, val in parsed:
        country = group_values[0] if group_values else ""
        cb = get_country_bucket(country)
        agg[cb] += val
    return dict(agg)

EVENTS_CONFIG = [
    {
        "name": "install",
        "event_type": "[AppsFlyer] Install",
        "group_by": [
            {"type": "user", "value": "gp:[AppsFlyer] media source"},
            {"type": "user", "value": "country"}
        ],
        "aggregator": "ms_country",
    },
    {
        "name": "signup",
        "event_type": "Cenoa sign-up completed",
        "group_by": [
            {"type": "user", "value": "gp:[AppsFlyer] media source"},
            {"type": "user", "value": "country"}
        ],
        "aggregator": "ms_country",
    },
    {
        "name": "kyc_submit",
        "event_type": "Bridgexyz KYC Component: Submit clicked",
        "group_by": [{"type": "user", "value": "country"}],
        "aggregator": "country",
    },
    {
        "name": "virtual_account",
        "event_type": "Virtual account opened",
        "group_by": [{"type": "user", "value": "country"}],
        "aggregator": "country",
    },
    {
        "name": "new_active",
        "event_type": "Withdraw Completed",
        "group_by": [{"type": "user", "value": "country"}],
        "aggregator": "country",
    },
]

def main():
    if len(sys.argv) != 3:
        print("Usage: python weekly_backfill.py START_YYYYMMDD END_YYYYMMDD")
        sys.exit(1)

    start = sys.argv[1]
    end = sys.argv[2]
    
    api_key, secret_key = load_credentials()
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    all_data = {"period": f"{start}-{end}"}

    for ec in EVENTS_CONFIG:
        name = ec["name"]
        print(f"  Fetching {name} ({ec['event_type']}) for {start}-{end}...")

        data = fetch_segmentation(api_key, secret_key, ec["event_type"], ec["group_by"], start, end)
        
        if data is None:
            print(f"    Retrying with totals metric...")
            data = fetch_segmentation(api_key, secret_key, ec["event_type"], ec["group_by"], start, end, metric="totals")

        if data is None:
            print(f"    SKIP {name}: no data", file=sys.stderr)
            all_data[name] = {"error": "no data"}
            continue

        parsed = parse_segmentation(data)
        
        if ec["aggregator"] == "ms_country":
            agg = aggregate_by_ms_and_country(parsed)
        else:
            agg = aggregate_by_country(parsed)

        def key_str(k):
            return " | ".join(k) if isinstance(k, tuple) else str(k)

        all_data[name] = {
            "event_type": ec["event_type"],
            "aggregator": ec["aggregator"],
            "totals": {key_str(k): v for k, v in agg.items()},
        }
        
        total = sum(agg.values())
        print(f"    ✓ {name}: {len(agg)} buckets, total={total}")
        
        # Small delay between API calls within a week
        time.sleep(1)

    out_file = DATA_DIR / f"weekly-channel-country-{start}.json"
    with open(out_file, "w") as f:
        json.dump(all_data, f, indent=2, default=str)
    print(f"  Saved: {out_file}")

if __name__ == "__main__":
    main()
