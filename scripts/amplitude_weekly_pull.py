#!/usr/bin/env python3
"""
Amplitude Weekly KPI Pull Script
Pulls key metrics from Amplitude's Event Segmentation API for two consecutive weeks,
calculates WoW deltas, and outputs JSON + human-readable summary.

Date Convention (S3-014):
  - Weekly = ISO week: Monday 00:00 UTC to Sunday 23:59 UTC
  - MTD = 1st of month 00:00 UTC to current day 23:59 UTC
  - All Amplitude API calls use YYYYMMDD format
  - Default range: last complete ISO week (Mon-Sun) vs prior week

Usage:
    python amplitude_weekly_pull.py                                        # last complete ISO week
    python amplitude_weekly_pull.py --start 2025-03-10 --end 2025-03-16    # custom range (Mon-Sun)
    python amplitude_weekly_pull.py --start 2025-03-10 --end 2025-03-16 --prev-start 2025-03-03 --prev-end 2025-03-09
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

AMPLITUDE_API_URL = "https://amplitude.com/api/2/events/segmentation"

# Events to pull (key → Amplitude event_type)
EVENTS = {
    "installs":   "[AppsFlyer] Install",
    "signups":    "Cenoa sign-up completed",
    "kyc_submits": "Bridgexyz KYC Component: Submit clicked",
    "withdrawals": "Withdraw Completed",
    "deposits":   "Deposit Completed",
    "kyc_started": "KYC Started",
}

# DAU uses the special "_active" event with m=uniques
DAU_EVENT = "_active"

LABEL_MAP = {
    "installs":    "Installs",
    "signups":     "Sign-ups",
    "kyc_submits": "KYC Submits",
    "withdrawals": "Withdrawals",
    "deposits":    "Deposits",
    "kyc_started": "KYC Started",
    "dau":         "DAU (avg)",
}


def load_credentials():
    """Load Amplitude credentials from env file or environment."""
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
        print("ERROR: AMPLITUDE_API_KEY and AMPLITUDE_SECRET_KEY must be set.", file=sys.stderr)
        sys.exit(1)
    return api_key, secret_key


def query_event(api_key: str, secret_key: str, event_type: str,
                start: str, end: str, metric: str = "totals") -> float:
    """
    Query Amplitude Event Segmentation API.
    start/end: YYYYMMDD strings.
    metric: 'totals' or 'uniques'.
    Returns the sum across all days in the range (or average for DAU).
    """
    e_param = json.dumps({"event_type": event_type})
    params = {
        "e": e_param,
        "start": start,
        "end": end,
        "m": metric,
    }

    resp = requests.get(
        AMPLITUDE_API_URL,
        params=params,
        auth=(api_key, secret_key),
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    # data.data.series is [[values_per_day]]
    series = data.get("data", {}).get("series", [[]])
    if not series or not series[0]:
        return 0

    values = series[0]

    # For DAU we want the daily average, for others we want the total
    if event_type == DAU_EVENT and metric == "uniques":
        non_zero = [v for v in values if v > 0]
        return round(sum(non_zero) / len(non_zero), 1) if non_zero else 0
    else:
        return sum(values)


def compute_delta(current: float, previous: float) -> dict:
    """Compute WoW delta percentage and direction."""
    if previous == 0:
        delta = 100.0 if current > 0 else 0.0
    else:
        delta = round(((current - previous) / previous) * 100, 1)

    if delta > 0:
        direction = "up"
    elif delta < 0:
        direction = "down"
    else:
        direction = "flat"

    return {
        "value": current if isinstance(current, int) else current,
        "prev": previous if isinstance(previous, int) else previous,
        "delta": delta,
        "direction": direction,
    }


def parse_date(s: str) -> datetime:
    """Parse YYYY-MM-DD or YYYYMMDD string to datetime."""
    s = s.strip()
    if "-" in s:
        return datetime.strptime(s, "%Y-%m-%d")
    return datetime.strptime(s, "%Y%m%d")


def fmt_date(dt: datetime) -> str:
    """Format datetime to YYYYMMDD."""
    return dt.strftime("%Y%m%d")


def iso_date(dt: datetime) -> str:
    """Format datetime to YYYY-MM-DD."""
    return dt.strftime("%Y-%m-%d")


def main():
    parser = argparse.ArgumentParser(description="Pull weekly KPIs from Amplitude")
    parser.add_argument("--start", help="Current period start (YYYY-MM-DD)")
    parser.add_argument("--end", help="Current period end (YYYY-MM-DD)")
    parser.add_argument("--prev-start", help="Previous period start (YYYY-MM-DD)")
    parser.add_argument("--prev-end", help="Previous period end (YYYY-MM-DD)")
    parser.add_argument("--output-dir", default=None, help="Output directory for JSON")
    args = parser.parse_args()

    # Determine date ranges
    if args.start and args.end:
        curr_start = parse_date(args.start)
        curr_end = parse_date(args.end)
    else:
        # Default: last complete ISO week (Monday-Sunday)
        today = datetime.utcnow()
        # Find last Sunday (end of most recent complete week)
        curr_end = today - timedelta(days=today.weekday() + 1)
        curr_start = curr_end - timedelta(days=6)  # Monday of that week

    if args.prev_start and args.prev_end:
        prev_start = parse_date(args.prev_start)
        prev_end = parse_date(args.prev_end)
    else:
        delta = (curr_end - curr_start).days + 1
        prev_end = curr_start - timedelta(days=1)
        prev_start = prev_end - timedelta(days=delta - 1)

    print(f"Current week:  {iso_date(curr_start)} → {iso_date(curr_end)}")
    print(f"Previous week: {iso_date(prev_start)} → {iso_date(prev_end)}")
    print()

    api_key, secret_key = load_credentials()

    results = {}

    # Pull standard events
    for key, event_type in EVENTS.items():
        print(f"  Pulling {LABEL_MAP[key]}...", end=" ", flush=True)
        curr_val = int(query_event(api_key, secret_key, event_type,
                                   fmt_date(curr_start), fmt_date(curr_end), "totals"))
        prev_val = int(query_event(api_key, secret_key, event_type,
                                   fmt_date(prev_start), fmt_date(prev_end), "totals"))
        results[key] = compute_delta(curr_val, prev_val)
        print(f"{curr_val} (prev: {prev_val})")

    # Pull DAU
    print(f"  Pulling {LABEL_MAP['dau']}...", end=" ", flush=True)
    curr_dau = query_event(api_key, secret_key, DAU_EVENT,
                           fmt_date(curr_start), fmt_date(curr_end), "uniques")
    prev_dau = query_event(api_key, secret_key, DAU_EVENT,
                           fmt_date(prev_start), fmt_date(prev_end), "uniques")
    # Round DAU to nearest int for display but keep float if fractional
    curr_dau_int = int(round(curr_dau))
    prev_dau_int = int(round(prev_dau))
    results["dau"] = compute_delta(curr_dau_int, prev_dau_int)
    print(f"{curr_dau_int} (prev: {prev_dau_int})")

    # Add metadata
    output = {
        "period": {
            "current": {"start": iso_date(curr_start), "end": iso_date(curr_end)},
            "previous": {"start": iso_date(prev_start), "end": iso_date(prev_end)},
        },
        "generated_at": datetime.now().isoformat(),
        **results,
    }

    # Write JSON
    if args.output_dir:
        out_dir = Path(args.output_dir)
    else:
        out_dir = Path(__file__).resolve().parent.parent / "data"
    out_dir.mkdir(parents=True, exist_ok=True)

    end_str = iso_date(curr_end)
    out_path = out_dir / f"amplitude-weekly-{end_str}.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\n✅ JSON saved to {out_path}")

    # Human-readable summary
    print(f"\n{'='*55}")
    print(f"  WEEKLY KPI SUMMARY")
    print(f"  {iso_date(curr_start)} → {iso_date(curr_end)} vs prior week")
    print(f"{'='*55}")

    for key in list(EVENTS.keys()) + ["dau"]:
        r = results[key]
        arrow = "↑" if r["direction"] == "up" else ("↓" if r["direction"] == "down" else "→")
        sign = "+" if r["delta"] > 0 else ""
        label = LABEL_MAP[key].ljust(14)
        print(f"  {label}  {r['value']:>8,}   {arrow} {sign}{r['delta']}%  (prev: {r['prev']:,})")

    print(f"{'='*55}")


if __name__ == "__main__":
    main()
