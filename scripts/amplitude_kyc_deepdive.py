#!/usr/bin/env python3
"""Amplitude KYC dropout deep-dive

Pulls KYC funnel events from Amplitude Segmentation API for a fixed date range.
Saves *raw* API responses (totals + group_by country + group_by platform).

Requested events:
- KYC Started
- Bridgexyz KYC Component Shown
- Bridgexyz KYC Component: Submit clicked
- KYC Updated

Usage:
  python amplitude_kyc_deepdive.py --start 20260314 --end 20260320 \
    --out ../data/kyc-deepdive-20260320.json

Date Convention (S3-014):
  - Weekly = ISO week: Monday 00:00 UTC to Sunday 23:59 UTC
  - MTD = 1st of month 00:00 UTC to current day 23:59 UTC
  - All Amplitude API calls use YYYYMMDD format
  - --start should be a Monday, --end should be a Sunday

Notes:
- We use m=totals per request.
- Counts are *event totals* (not unique users) unless Amplitude is configured differently.
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

API_URL = "https://amplitude.com/api/2/events/segmentation"

EVENTS = [
    "KYC Started",
    "Bridgexyz KYC Component Shown",
    "Bridgexyz KYC Component: Submit clicked",
    "KYC Updated",
]

SEGMENTS = {
    "totals": None,
    "country": "country",
    "platform": "platform",
}


def load_credentials():
    env_file = os.path.expanduser("~/.openclaw/credentials/amplitude.env")
    creds = {}
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                creds[k.strip()] = v.strip()

    api_key = creds.get("AMPLITUDE_API_KEY", os.environ.get("AMPLITUDE_API_KEY"))
    secret_key = creds.get("AMPLITUDE_SECRET_KEY", os.environ.get("AMPLITUDE_SECRET_KEY"))
    if not api_key or not secret_key:
        print("ERROR: AMPLITUDE_API_KEY and AMPLITUDE_SECRET_KEY required")
        sys.exit(1)
    return api_key, secret_key


def _basic_auth_header(api_key: str, secret_key: str) -> str:
    token = base64.b64encode(f"{api_key}:{secret_key}".encode()).decode()
    return f"Basic {token}"


def fetch_segmentation(api_key, secret_key, event_type, start, end, group_by_user_prop=None, timeout=45):
    e_obj = {"event_type": event_type}
    if group_by_user_prop:
        e_obj["group_by"] = [{"type": "user", "value": group_by_user_prop}]

    params = urllib.parse.urlencode(
        {
            "e": json.dumps(e_obj),
            "start": start,
            "end": end,
            "m": "totals",
        }
    )
    url = f"{API_URL}?{params}"

    req = urllib.request.Request(
        url,
        headers={
            "Authorization": _basic_auth_header(api_key, secret_key),
            "Content-Type": "application/json",
        },
    )

    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def parse_total(response):
    if not response or "data" not in response:
        return 0
    data = response["data"]
    sc = data.get("seriesCollapsed", [])
    if not sc:
        return 0
    # Expect first series, first bucket
    try:
        val_entry = sc[0][0]
    except Exception:
        return 0
    if isinstance(val_entry, dict):
        return val_entry.get("value", 0) or 0
    if isinstance(val_entry, (int, float)):
        return val_entry
    return 0


def parse_group_counts(response, label_index=1):
    """Return dict of group_value -> count."""
    if not response or "data" not in response:
        return {}

    data = response["data"]
    labels = data.get("seriesLabels", [])
    sc = data.get("seriesCollapsed", [])

    out = {}
    for i, label_list in enumerate(labels):
        group = None
        if isinstance(label_list, list) and len(label_list) > label_index:
            group = label_list[label_index]
        group = group or "Unknown"
        if group in ("none", "None", ""):
            group = "Unknown"

        value = 0
        if i < len(sc) and sc[i] and len(sc[i]) > 0:
            val_entry = sc[i][0]
            if isinstance(val_entry, dict):
                value = val_entry.get("value", 0) or 0
            elif isinstance(val_entry, (int, float)):
                value = val_entry

        if value:
            out[group] = out.get(group, 0) + value

    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument(
        "--out",
        default=None,
        help="Output path for raw JSON (default: ../data/kyc-deepdive-<end>.json)",
    )
    ap.add_argument("--sleep", type=float, default=0.3, help="Sleep seconds between API calls")
    args = ap.parse_args()

    api_key, secret_key = load_credentials()

    script_dir = Path(__file__).resolve().parent
    if args.out:
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = (script_dir / out_path).resolve()
    else:
        out_path = (script_dir.parent / "data" / f"kyc-deepdive-{args.end}.json").resolve()

    pulls = {
        "meta": {
            "date_range": {"start": args.start, "end": args.end},
            "generated_at": datetime.now().isoformat(),
            "api": {"endpoint": API_URL, "m": "totals"},
        },
        "pulls": {},
    }

    for event in EVENTS:
        pulls["pulls"][event] = {}
        for seg_name, prop in SEGMENTS.items():
            try:
                resp = fetch_segmentation(api_key, secret_key, event, args.start, args.end, prop)
            except Exception as e:
                pulls["pulls"][event][seg_name] = {"error": str(e)}
                continue
            pulls["pulls"][event][seg_name] = resp
            time.sleep(args.sleep)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(pulls, f, indent=2)

    # Print a quick summary for sanity
    def safe_total(event):
        resp = pulls["pulls"].get(event, {}).get("totals")
        if isinstance(resp, dict) and resp.get("error"):
            return None
        return parse_total(resp)

    print(f"Saved raw pulls -> {out_path}")
    print("Totals:")
    for event in EVENTS:
        print(f"  {event:45s} {safe_total(event)}")


if __name__ == "__main__":
    main()
