#!/usr/bin/env python3
"""
Amplitude Funnel Analysis Script
Queries the Amplitude Dashboard REST API (Funnel Analysis endpoint) to compute
conversion rates through the Cenoa acquisition funnel, grouped by country.

Funnel steps (strict ordering):
  1) [AppsFlyer] Install
  2) Cenoa sign-up completed
  3) KYC Started
  4) Bridgexyz KYC Component: Submit clicked
  5) Virtual account opened
  6) Withdraw Completed

Date Convention (S3-014):
  - Weekly = ISO week: Monday 00:00 UTC to Sunday 23:59 UTC
  - MTD = 1st of month 00:00 UTC to current day 23:59 UTC
  - All Amplitude API calls use YYYYMMDD format
  - Default range: last 4 complete ISO weeks (Mon-Sun)

Usage:
    python amplitude_funnel.py                          # last 4 complete ISO weeks
    python amplitude_funnel.py --start 20260220 --end 20260322
    python amplitude_funnel.py --days 28                # last 28 days (rounded to ISO weeks)

Output:
    - data/funnel-api-YYYYMMDD.json   (raw API response + processed data)
    - Human-readable funnel printed to stdout
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

AMPLITUDE_API_URL = "https://amplitude.com/api/2/funnels"
SEGMENTATION_API_URL = "https://amplitude.com/api/2/events/segmentation"

FUNNEL_STEPS = [
    "[AppsFlyer] Install",
    "Cenoa sign-up completed",
    "KYC Started",
    "Bridgexyz KYC Component: Submit clicked",
    "Virtual account opened",
    "Withdraw Completed",
]

COUNTRIES = ["Turkey", "Nigeria", "Egypt", "Pakistan"]
COUNTRY_CODES = {"Turkey": "TR", "Nigeria": "NG", "Egypt": "EG", "Pakistan": "PK"}

DATA_DIR = Path(__file__).resolve().parent.parent / "data" if not os.getenv("DATA_DIR") else Path(os.getenv("DATA_DIR"))


def get_credentials():
    """Load Amplitude credentials from env or credentials file."""
    api_key = os.getenv("AMPLITUDE_API_KEY")
    secret_key = os.getenv("AMPLITUDE_SECRET_KEY")

    if not api_key or not secret_key:
        cred_file = Path.home() / ".openclaw" / "credentials" / "amplitude.env"
        if cred_file.exists():
            for line in cred_file.read_text().strip().splitlines():
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    if k == "AMPLITUDE_API_KEY":
                        api_key = v
                    elif k == "AMPLITUDE_SECRET_KEY":
                        secret_key = v

    if not api_key or not secret_key:
        print("ERROR: AMPLITUDE_API_KEY and AMPLITUDE_SECRET_KEY required", file=sys.stderr)
        sys.exit(1)

    return api_key, secret_key


def query_funnel_api(api_key, secret_key, start, end, group_by="country"):
    """
    Query the Amplitude Funnel Analysis API.

    GET /api/2/funnels?e=...&e=...&start=YYYYMMDD&end=YYYYMMDD&mode=ordered&g=country
    """
    params = []

    # Add event parameters (multiple e= params)
    for step in FUNNEL_STEPS:
        event_json = json.dumps({"event_type": step})
        params.append(("e", event_json))

    params.append(("start", start))
    params.append(("end", end))
    params.append(("mode", "ordered"))
    params.append(("n", "active"))
    params.append(("cs", "2592000"))  # 30-day conversion window
    params.append(("limit", "100"))

    if group_by:
        params.append(("g", group_by))

    print(f"Querying Amplitude Funnel API: {start} → {end}, group_by={group_by}")
    print(f"  Steps: {len(FUNNEL_STEPS)}")

    resp = requests.get(
        AMPLITUDE_API_URL,
        params=params,
        auth=(api_key, secret_key),
        timeout=120,
    )

    if resp.status_code == 429:
        retry_after = int(resp.headers.get("Retry-After", 60))
        print(f"  Rate limited. Waiting {retry_after}s...")
        time.sleep(retry_after)
        resp = requests.get(
            AMPLITUDE_API_URL,
            params=params,
            auth=(api_key, secret_key),
            timeout=120,
        )

    if resp.status_code != 200:
        print(f"  Funnel API error: {resp.status_code}", file=sys.stderr)
        print(f"  Response: {resp.text[:500]}", file=sys.stderr)
        return None

    return resp.json()


def query_funnel_segmented(api_key, secret_key, start, end):
    """
    Query funnel with country segments using segment filters.
    Each country gets its own segment via the s= parameter.
    """
    params = []

    for step in FUNNEL_STEPS:
        event_json = json.dumps({"event_type": step})
        params.append(("e", event_json))

    params.append(("start", start))
    params.append(("end", end))
    params.append(("mode", "ordered"))
    params.append(("n", "active"))
    params.append(("cs", "2592000"))
    params.append(("g", "country"))
    params.append(("limit", "100"))

    print(f"Querying Amplitude Funnel API (segmented): {start} → {end}")

    resp = requests.get(
        AMPLITUDE_API_URL,
        params=params,
        auth=(api_key, secret_key),
        timeout=120,
    )

    if resp.status_code == 429:
        retry_after = int(resp.headers.get("Retry-After", 60))
        print(f"  Rate limited. Waiting {retry_after}s...")
        time.sleep(retry_after)
        resp = requests.get(
            AMPLITUDE_API_URL,
            params=params,
            auth=(api_key, secret_key),
            timeout=120,
        )

    if resp.status_code != 200:
        print(f"  Funnel API error: {resp.status_code}", file=sys.stderr)
        print(f"  Response: {resp.text[:500]}", file=sys.stderr)
        return None

    return resp.json()


def fallback_event_segmentation(api_key, secret_key, start, end):
    """
    Fallback: Use Event Segmentation API to query each funnel step individually,
    grouped by country. This gives totals per step but NOT true funnel conversion
    (users don't need to have completed prior steps).

    NOTE: This is an approximation — not a true funnel analysis.
    """
    print("\n⚠️  FALLBACK: Using Event Segmentation API (not true funnel analysis)")
    print("   Limitation: Counts are independent per step, not sequential conversion.\n")

    results = {}

    for step in FUNNEL_STEPS:
        event_json = json.dumps({"event_type": step})
        params = {
            "e": event_json,
            "start": start,
            "end": end,
            "m": "uniques",
            "i": 30,  # monthly rollup
            "g": "country",
            "limit": 100,
        }

        print(f"  Querying: {step}")
        resp = requests.get(
            SEGMENTATION_API_URL,
            params=params,
            auth=(api_key, secret_key),
            timeout=60,
        )

        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 30))
            print(f"    Rate limited. Waiting {retry_after}s...")
            time.sleep(retry_after)
            resp = requests.get(
                SEGMENTATION_API_URL,
                params=params,
                auth=(api_key, secret_key),
                timeout=60,
            )

        if resp.status_code != 200:
            print(f"    Error: {resp.status_code} — {resp.text[:200]}", file=sys.stderr)
            results[step] = {"error": resp.status_code}
            continue

        data = resp.json().get("data", {})
        series = data.get("series", [])
        labels = data.get("seriesLabels", [])
        collapsed = data.get("seriesCollapsed", [])

        step_data = {}
        for i, label in enumerate(labels):
            # seriesCollapsed gives total uniques over the period
            if collapsed and i < len(collapsed):
                val = collapsed[i]
                if isinstance(val, list) and val:
                    val = val[0].get("value", 0) if isinstance(val[0], dict) else val[0]
                step_data[label] = val
            elif series and i < len(series):
                step_data[label] = sum(series[i]) if series[i] else 0

        results[step] = step_data
        time.sleep(1)  # Be nice to rate limits

    return results


def process_funnel_response(raw_data):
    """
    Process the Funnel API response into a clean structure.
    The response contains an array of group results (one per country when grouped).
    """
    if not raw_data or "data" not in raw_data:
        return None

    data = raw_data["data"]
    if not isinstance(data, list):
        data = [data]

    processed = {
        "steps": FUNNEL_STEPS,
        "groups": {},
        "overall": None,
    }

    # Compute step-by-step from cumulativeRaw
    def calc_step_by_step(raw_counts):
        sbs = [1.0] if raw_counts else []
        for i in range(1, len(raw_counts)):
            if raw_counts[i - 1] > 0:
                sbs.append(raw_counts[i] / raw_counts[i - 1])
            else:
                sbs.append(0)
        return sbs

    # Aggregate for overall
    overall_raw = [0] * len(FUNNEL_STEPS)

    for group in data:
        meta = group.get("meta", {})
        # The segment label is in meta.segment or meta.segments[0]
        group_label = meta.get("segment", meta.get("groupLabel", "Unknown"))

        cumulative_raw = group.get("cumulativeRaw", [])
        cumulative = group.get("cumulative", [])
        step_by_step = group.get("stepByStep", calc_step_by_step(cumulative_raw))

        group_result = {
            "label": group_label,
            "cumulative": cumulative,
            "cumulative_raw": cumulative_raw,
            "step_by_step": step_by_step,
            "median_trans_times_ms": group.get("medianTransTimes", []),
            "avg_trans_times_ms": group.get("avgTransTimes", []),
            "events": group.get("events", []),
        }

        processed["groups"][group_label] = group_result

        # Accumulate overall totals
        for i, val in enumerate(cumulative_raw):
            if i < len(overall_raw):
                overall_raw[i] += val

    # Build overall
    if overall_raw[0] > 0:
        overall_cum = [c / overall_raw[0] for c in overall_raw]
    else:
        overall_cum = [0] * len(overall_raw)

    processed["overall"] = {
        "label": "All Countries",
        "cumulative": overall_cum,
        "cumulative_raw": overall_raw,
        "step_by_step": calc_step_by_step(overall_raw),
    }

    return processed


def process_fallback_results(fallback_data):
    """Convert fallback event segmentation data into funnel-like structure."""
    # Collect all countries seen
    all_countries = set()
    for step_data in fallback_data.values():
        if isinstance(step_data, dict) and "error" not in step_data:
            all_countries.update(step_data.keys())

    processed = {
        "steps": FUNNEL_STEPS,
        "mode": "fallback_event_segmentation",
        "limitation": "Counts are independent per step — NOT true funnel conversion rates",
        "groups": {},
        "overall": None,
    }

    # Build per-country data
    for country in sorted(all_countries):
        counts = []
        for step in FUNNEL_STEPS:
            step_data = fallback_data.get(step, {})
            counts.append(step_data.get(country, 0) if isinstance(step_data, dict) else 0)

        if counts[0] > 0:
            cumulative = [c / counts[0] for c in counts]
        else:
            cumulative = [0] * len(counts)

        step_by_step = [1.0]
        for i in range(1, len(counts)):
            if counts[i - 1] > 0:
                step_by_step.append(counts[i] / counts[i - 1])
            else:
                step_by_step.append(0)

        processed["groups"][country] = {
            "label": country,
            "cumulative": cumulative,
            "cumulative_raw": counts,
            "step_by_step": step_by_step,
        }

    # Build overall (sum across all countries of interest)
    overall_counts = []
    for step in FUNNEL_STEPS:
        step_data = fallback_data.get(step, {})
        total = 0
        if isinstance(step_data, dict):
            for country in COUNTRIES:
                total += step_data.get(country, 0)
        overall_counts.append(total)

    if overall_counts[0] > 0:
        overall_cum = [c / overall_counts[0] for c in overall_counts]
    else:
        overall_cum = [0] * len(overall_counts)

    overall_sbs = [1.0]
    for i in range(1, len(overall_counts)):
        if overall_counts[i - 1] > 0:
            overall_sbs.append(overall_counts[i] / overall_counts[i - 1])
        else:
            overall_sbs.append(0)

    processed["overall"] = {
        "label": "All Target Countries",
        "cumulative": overall_cum,
        "cumulative_raw": overall_counts,
        "step_by_step": overall_sbs,
    }

    return processed


def print_funnel(processed, is_fallback=False):
    """Print a human-readable funnel summary."""
    print("\n" + "=" * 80)
    print("CENOA ACQUISITION FUNNEL — Last 30 Days")
    if is_fallback:
        print("⚠️  FALLBACK MODE: Independent event counts (not true funnel)")
    print("=" * 80)

    # Overall
    overall = processed.get("overall")
    if overall:
        print(f"\n{'─' * 60}")
        print(f"  OVERALL ({overall['label']})")
        print(f"{'─' * 60}")
        _print_funnel_table(processed["steps"], overall)

    # Per-country (filter to target countries)
    groups = processed.get("groups", {})
    target_countries = {}
    for label, data in groups.items():
        for country_name, code in COUNTRY_CODES.items():
            if label == country_name or label == code:
                target_countries[country_name] = data
                break

    # Also include any that match directly
    for country in COUNTRIES:
        if country in groups and country not in target_countries:
            target_countries[country] = groups[country]

    for country in COUNTRIES:
        if country in target_countries:
            data = target_countries[country]
            code = COUNTRY_CODES.get(country, "??")
            print(f"\n{'─' * 60}")
            print(f"  {country} ({code})")
            print(f"{'─' * 60}")
            _print_funnel_table(processed["steps"], data)
        else:
            code = COUNTRY_CODES.get(country, "??")
            print(f"\n  {country} ({code}): No data")

    print(f"\n{'=' * 80}\n")


def _print_funnel_table(steps, data):
    """Print a single funnel table."""
    raw = data.get("cumulative_raw", [])
    cum = data.get("cumulative", [])
    sbs = data.get("step_by_step", [])

    max_step_len = max(len(s) for s in steps)
    header = f"  {'Step':<{max_step_len}}  {'Users':>8}  {'Cumul%':>8}  {'Step%':>8}  {'Drop':>8}"
    print(header)
    print(f"  {'─' * (max_step_len + 38)}")

    for i, step in enumerate(steps):
        users = raw[i] if i < len(raw) else 0
        cum_pct = cum[i] * 100 if i < len(cum) else 0
        sbs_pct = sbs[i] * 100 if i < len(sbs) else 0
        drop = 100 - sbs_pct if i > 0 else 0

        users_str = f"{users:,}" if isinstance(users, (int, float)) else str(users)
        print(f"  {step:<{max_step_len}}  {users_str:>8}  {cum_pct:>7.1f}%  {sbs_pct:>7.1f}%  {drop:>7.1f}%")


def main():
    parser = argparse.ArgumentParser(description="Amplitude Funnel Analysis")
    parser.add_argument("--start", help="Start date YYYYMMDD")
    parser.add_argument("--end", help="End date YYYYMMDD")
    parser.add_argument("--days", type=int, default=28, help="Number of days to look back (default: 28, i.e. 4 ISO weeks)")
    parser.add_argument("--fallback", action="store_true", help="Force fallback to Event Segmentation API")
    parser.add_argument("--output", help="Output JSON file path")
    args = parser.parse_args()

    # Date range
    if args.start and args.end:
        start = args.start
        end = args.end
    else:
        # Default: last N days aligned to ISO week boundaries (Mon-Sun)
        today = datetime.utcnow()
        last_sunday = today - timedelta(days=today.weekday() + 1)
        # Round days to whole weeks (minimum 1 week)
        num_weeks = max(1, args.days // 7)
        start_monday = last_sunday - timedelta(days=num_weeks * 7 - 1)
        start = start_monday.strftime("%Y%m%d")
        end = last_sunday.strftime("%Y%m%d")

    api_key, secret_key = get_credentials()

    # Output path
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    today_str = datetime.now().strftime("%Y%m%d")
    output_path = Path(args.output) if args.output else DATA_DIR / f"funnel-api-{today_str}.json"

    is_fallback = False
    processed = None

    if not args.fallback:
        # Try Funnel API first
        raw_data = query_funnel_api(api_key, secret_key, start, end, group_by="country")

        if raw_data:
            processed = process_funnel_response(raw_data)

            if processed:
                # Save raw + processed
                output = {
                    "meta": {
                        "source": "amplitude_funnel_api",
                        "endpoint": AMPLITUDE_API_URL,
                        "start": start,
                        "end": end,
                        "mode": "ordered",
                        "generated_at": datetime.now().isoformat(),
                        "steps": FUNNEL_STEPS,
                    },
                    "raw": raw_data,
                    "processed": processed,
                }

                output_path.write_text(json.dumps(output, indent=2, default=str))
                print(f"\n✅ Saved to {output_path}")
                print_funnel(processed, is_fallback=False)
                return

        print("\n⚠️  Funnel API failed or returned no data. Falling back...")

    # Fallback: Event Segmentation API
    is_fallback = True
    fallback_data = fallback_event_segmentation(api_key, secret_key, start, end)
    processed = process_fallback_results(fallback_data)

    output = {
        "meta": {
            "source": "amplitude_event_segmentation_fallback",
            "endpoint": SEGMENTATION_API_URL,
            "start": start,
            "end": end,
            "limitation": "Independent event counts, not true funnel conversion",
            "generated_at": datetime.now().isoformat(),
            "steps": FUNNEL_STEPS,
        },
        "raw_per_step": fallback_data,
        "processed": processed,
    }

    output_path.write_text(json.dumps(output, indent=2, default=str))
    print(f"\n✅ Saved to {output_path}")
    print_funnel(processed, is_fallback=True)


if __name__ == "__main__":
    main()
