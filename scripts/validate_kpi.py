#!/usr/bin/env python3
"""Validate kpi_auto_update.py output against raw Amplitude API responses.

Makes direct Amplitude API calls and compares every number in data.json.
"""

import json
import os
import sys
import requests

# Config
AMPLITUDE_API_URL = "https://amplitude.com/api/2/events/segmentation"
START = "20260314"
END = "20260320"
PREV_START = "20260307"
PREV_END = "20260313"

EVENTS = {
    "installs": "[AppsFlyer] Install",
    "signups": "Cenoa sign-up completed",
    "kycSubmits": "Bridgexyz KYC Component: Submit clicked",
    "virtualAccountOpened": "Virtual account opened",
    "depositCompleted": "Deposit Completed",
    "transferCompleted": "Transfer Completed",
    "withdrawCompleted": "Withdraw Completed",
}

COUNTRY_NAMES = {
    "TR": "Turkey",
    "NG": "Nigeria",
    "EG": "Egypt",
    "PK": "Pakistan",
}

def load_creds():
    env_file = os.path.expanduser("~/.openclaw/credentials/amplitude.env")
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())
    return os.environ["AMPLITUDE_API_KEY"], os.environ["AMPLITUDE_SECRET_KEY"]

def query_total(api_key, secret_key, event_type, start, end, country=None):
    event_obj = {"event_type": event_type}
    if country:
        event_obj["filters"] = [{
            "subprop_type": "user",
            "subprop_key": "country",
            "subprop_op": "is",
            "subprop_value": [country],
        }]
    params = {
        "e": json.dumps(event_obj),
        "start": start,
        "end": end,
        "m": "totals",
    }
    resp = requests.get(AMPLITUDE_API_URL, params=params, auth=(api_key, secret_key), timeout=45)
    if resp.status_code >= 400:
        print(f"  ERROR {resp.status_code}: {resp.text[:200]}")
        return None, resp.text[:500]
    data = resp.json()
    series = data.get("data", {}).get("series", [[]])
    values = [float(v) for v in series[0]] if series and series[0] else []
    total = int(round(sum(values)))
    return total, data

def query_dau_avg(api_key, secret_key, start, end, days):
    event_obj = {"event_type": "_active"}
    params = {
        "e": json.dumps(event_obj),
        "start": start,
        "end": end,
        "m": "uniques",
    }
    resp = requests.get(AMPLITUDE_API_URL, params=params, auth=(api_key, secret_key), timeout=45)
    if resp.status_code >= 400:
        print(f"  ERROR {resp.status_code}: {resp.text[:200]}")
        return None, resp.text[:500]
    data = resp.json()
    series = data.get("data", {}).get("series", [[]])
    values = [float(v) for v in series[0]] if series and series[0] else []
    avg = round(sum(values) / max(days, 1), 1) if values else 0.0
    return avg, data

def pct_diff(a, b):
    """Return absolute percentage difference between a and b."""
    if a == 0 and b == 0:
        return 0.0
    if b == 0:
        return 100.0
    return abs((a - b) / b) * 100.0

def main():
    api_key, secret_key = load_creds()
    
    # Load existing data.json
    data_json_path = os.path.expanduser("~/. openclaw/workspace/projects/cenoa-growth-engine/data.json")
    # Fix path
    data_json_path = os.path.expanduser("~/.openclaw/workspace/projects/cenoa-growth-engine/data.json")
    with open(data_json_path) as f:
        cortex = json.load(f)
    
    results = {
        "raw_api": {},
        "cortex_values": {},
        "discrepancies": [],
    }
    
    print("=" * 70)
    print("VALIDATION: Amplitude API vs data.json (Cortex)")
    print("=" * 70)
    
    # 1. Global KPIs
    print("\n── Global KPIs (Current Week: Mar 14-20) ──")
    for key, event_type in EVENTS.items():
        api_val, raw = query_total(api_key, secret_key, event_type, START, END)
        cortex_val = cortex["kpis"][key]["value"]
        diff = pct_diff(api_val, cortex_val)
        status = "✅" if diff <= 2.0 else "❌"
        print(f"  {status} {key}: API={api_val}, Cortex={cortex_val}, diff={diff:.1f}%")
        results["raw_api"][f"{key}_curr"] = api_val
        results["cortex_values"][f"{key}_curr"] = cortex_val
        if diff > 2.0:
            results["discrepancies"].append({
                "metric": f"{key} (current)", "api": api_val, "cortex": cortex_val, "diff_pct": round(diff, 1)
            })
    
    print("\n── Global KPIs (Previous Week: Mar 7-13) ──")
    for key, event_type in EVENTS.items():
        api_val, raw = query_total(api_key, secret_key, event_type, PREV_START, PREV_END)
        cortex_val = cortex["kpis"][key]["prev"]
        diff = pct_diff(api_val, cortex_val)
        status = "✅" if diff <= 2.0 else "❌"
        print(f"  {status} {key}: API={api_val}, Cortex={cortex_val}, diff={diff:.1f}%")
        results["raw_api"][f"{key}_prev"] = api_val
        results["cortex_values"][f"{key}_prev"] = cortex_val
        if diff > 2.0:
            results["discrepancies"].append({
                "metric": f"{key} (prev)", "api": api_val, "cortex": cortex_val, "diff_pct": round(diff, 1)
            })
    
    # 2. DAU Average
    print("\n── DAU Average ──")
    api_dau_curr, _ = query_dau_avg(api_key, secret_key, START, END, 7)
    api_dau_prev, _ = query_dau_avg(api_key, secret_key, PREV_START, PREV_END, 7)
    cortex_dau_curr = cortex["kpis"]["dauAvg"]["value"]
    cortex_dau_prev = cortex["kpis"]["dauAvg"]["prev"]
    
    for label, api_v, cortex_v, suffix in [
        ("DAU curr", api_dau_curr, cortex_dau_curr, "curr"),
        ("DAU prev", api_dau_prev, cortex_dau_prev, "prev"),
    ]:
        diff = pct_diff(api_v, cortex_v)
        status = "✅" if diff <= 2.0 else "❌"
        print(f"  {status} {label}: API={api_v}, Cortex={cortex_v}, diff={diff:.1f}%")
        results["raw_api"][f"dauAvg_{suffix}"] = api_v
        results["cortex_values"][f"dauAvg_{suffix}"] = cortex_v
        if diff > 2.0:
            results["discrepancies"].append({
                "metric": f"dauAvg ({suffix})", "api": api_v, "cortex": cortex_v, "diff_pct": round(diff, 1)
            })
    
    # 3. Country breakdown
    print("\n── Country Breakdown (Current Week) ──")
    for event_key in ["installs", "signups"]:
        event_type = EVENTS[event_key]
        for cc in ["TR", "NG", "EG", "PK"]:
            country_name = COUNTRY_NAMES[cc]
            api_val, _ = query_total(api_key, secret_key, event_type, START, END, country=country_name)
            cortex_val = cortex["countries"][cc][event_key]["value"]
            diff = pct_diff(api_val, cortex_val)
            status = "✅" if diff <= 2.0 else "❌"
            print(f"  {status} {cc}/{event_key}: API={api_val}, Cortex={cortex_val}, diff={diff:.1f}%")
            results["raw_api"][f"{cc}_{event_key}_curr"] = api_val
            results["cortex_values"][f"{cc}_{event_key}_curr"] = cortex_val
            if diff > 2.0:
                results["discrepancies"].append({
                    "metric": f"{cc}/{event_key} (current)", "api": api_val, "cortex": cortex_val, "diff_pct": round(diff, 1)
                })
    
    print("\n── Country Breakdown (Previous Week) ──")
    for event_key in ["installs", "signups"]:
        event_type = EVENTS[event_key]
        for cc in ["TR", "NG", "EG", "PK"]:
            country_name = COUNTRY_NAMES[cc]
            api_val, _ = query_total(api_key, secret_key, event_type, PREV_START, PREV_END, country=country_name)
            cortex_val = cortex["countries"][cc][event_key]["prev"]
            diff = pct_diff(api_val, cortex_val)
            status = "✅" if diff <= 2.0 else "❌"
            print(f"  {status} {cc}/{event_key}: API={api_val}, Cortex={cortex_val}, diff={diff:.1f}%")
            results["raw_api"][f"{cc}_{event_key}_prev"] = api_val
            results["cortex_values"][f"{cc}_{event_key}_prev"] = cortex_val
            if diff > 2.0:
                results["discrepancies"].append({
                    "metric": f"{cc}/{event_key} (prev)", "api": api_val, "cortex": cortex_val, "diff_pct": round(diff, 1)
                })
    
    # 4. Delta % validation
    print("\n── WoW Delta % Validation ──")
    for key in list(EVENTS.keys()) + ["dauAvg"]:
        curr_api = results["raw_api"].get(f"{key}_curr", 0)
        prev_api = results["raw_api"].get(f"{key}_prev", 0)
        if prev_api == 0:
            expected_delta = 100.0 if curr_api > 0 else 0.0
        else:
            expected_delta = round(((curr_api - prev_api) / prev_api) * 100.0, 1)
        cortex_delta = cortex["kpis"][key]["deltaPct"]
        diff = abs(expected_delta - cortex_delta)
        status = "✅" if diff <= 0.5 else "❌"
        print(f"  {status} {key} delta: Expected={expected_delta}%, Cortex={cortex_delta}%, diff={diff:.1f}pp")
        if diff > 0.5:
            results["discrepancies"].append({
                "metric": f"{key} deltaPct", "api": expected_delta, "cortex": cortex_delta, "diff_pct": diff
            })
    
    # Summary
    print("\n" + "=" * 70)
    print(f"TOTAL DISCREPANCIES (>2%): {len(results['discrepancies'])}")
    for d in results["discrepancies"]:
        print(f"  ⚠️  {d['metric']}: API={d['api']}, Cortex={d['cortex']}, diff={d['diff_pct']}%")
    print("=" * 70)
    
    # Save raw results
    out_path = os.path.expanduser("~/.openclaw/workspace/projects/cenoa-growth-engine/data/kpi-validation-raw.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nRaw results saved to {out_path}")
    
    return results

if __name__ == "__main__":
    main()
