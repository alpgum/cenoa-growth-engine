#!/usr/bin/env python3
"""Unified Data Pipeline — pulls all sources, normalizes channel data, writes data.json.

Calls:
  1. pull_amplitude.py  → funnel metrics (install → signup → KYC → withdraw)
  2. pull_ga4.py        → web traffic (sessions, users, source/medium)
  3. pull_bigquery.py   → AppsFlyer campaign installs
  4. pull_sheets.py     → budget tracking (monthly target, spent, remaining)

Normalizes all channel data into unified format:
  {channel, spend, installs, CPI, activation_rate, TRUE_CAC}

Error handling: if one source fails, continues with others + logs warning.

Usage:
  source ~/.openclaw/venv/bin/activate
  python3 scripts/unified_data_pipeline.py
"""

import json
import os
import sys
import traceback
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Ensure scripts dir is on path for sibling imports
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from pull_amplitude import pull as pull_amplitude
from pull_ga4 import pull as pull_ga4
from pull_bigquery import pull as pull_bigquery
from pull_sheets import pull as pull_sheets

ROOT = SCRIPT_DIR.parent
OUT_PATH = ROOT / "data.json"
IST = timezone(timedelta(hours=3))


def _now_iso():
    return datetime.now(IST).isoformat(timespec="seconds")


def _safe_div(a, b):
    """Safe division, returns None if b is 0 or None."""
    if not b:
        return None
    return round(a / b, 4)


def _normalize_channels(unified):
    """Build unified channelPerformance array from campaigns + funnel data.

    Output format per channel:
      {channel, spend, installs, CPI, activation_rate, TRUE_CAC}

    TRUE_CAC = spend / new_actives (activated users, not just installs).
    activation_rate = withdraw / install (proxy: completed withdrawal = activated).
    """
    campaigns = unified.get("campaigns", [])
    budget = unified.get("budget", {})
    funnel = unified.get("funnel", {})

    # Aggregate installs by channel from campaign data
    channel_installs = defaultdict(int)
    for c in campaigns:
        ch = c.get("channel") or "(unknown)"
        channel_installs[ch] += c.get("installs", 0)

    # Total installs and activation rate from funnel
    total_installs = funnel.get("install", 0) or 0
    total_withdrawals = funnel.get("withdraw", 0) or 0
    global_activation_rate = _safe_div(total_withdrawals, total_installs)

    # Total spend from budget
    total_spend = budget.get("spent") or 0

    # Estimate spend per channel proportionally (no per-channel spend data yet)
    total_campaign_installs = sum(channel_installs.values()) or 1

    channel_performance = []
    for ch, installs in sorted(channel_installs.items(), key=lambda x: -x[1]):
        # Proportional spend estimate
        spend_share = installs / total_campaign_installs
        est_spend = round(total_spend * spend_share, 2) if total_spend else None

        # CPI
        cpi = _safe_div(est_spend, installs) if est_spend else None

        # Estimated new actives (apply global activation rate to channel installs)
        est_actives = round(installs * global_activation_rate) if global_activation_rate else 0

        # TRUE CAC = spend / new_actives
        true_cac = _safe_div(est_spend, est_actives) if est_spend and est_actives else None

        channel_performance.append({
            "channel": ch,
            "spend": est_spend,
            "installs": installs,
            "CPI": round(cpi, 2) if cpi else None,
            "activation_rate": round(global_activation_rate, 4) if global_activation_rate else None,
            "new_active": est_actives,
            "TRUE_CAC": round(true_cac, 2) if true_cac else None,
        })

    return channel_performance


def run_pipeline():
    print("=" * 60)
    print("  CENOA GROWTH ENGINE — UNIFIED DATA PIPELINE")
    print(f"  {_now_iso()}")
    print("=" * 60)

    errors = []
    warnings = []
    unified = {
        "lastUpdated": _now_iso(),
        "sources": {},
    }

    # ── 1. Amplitude ──────────────────────────────────────────
    print("\n[1/4] Amplitude funnel data")
    try:
        amp = pull_amplitude()
        unified["funnel"] = amp["funnel"]
        unified["funnelByCountry"] = amp["funnelByCountry"]
        unified["funnelByPlatform"] = amp["funnelByPlatform"]
        unified["sources"]["amplitude"] = {"status": "ok", "period": amp["period"]}
        print("  ✓ OK")
    except Exception as e:
        msg = f"amplitude: {e}"
        print(f"  ✗ ERROR: {e}", file=sys.stderr)
        traceback.print_exc()
        errors.append(msg)
        warnings.append(f"[WARN] Amplitude failed: {e}")
        unified["funnel"] = {}
        unified["funnelByCountry"] = {}
        unified["funnelByPlatform"] = {}
        unified["sources"]["amplitude"] = {"status": "error", "error": str(e)}

    # ── 2. GA4 ────────────────────────────────────────────────
    print("\n[2/4] GA4 traffic data")
    try:
        ga4 = pull_ga4()
        if ga4:
            unified["traffic"] = {
                "sessions": ga4["sessions"],
                "users": ga4["users"],
                "bySource": ga4["bySource"],
                "byCountry": ga4["byCountry"],
            }
            unified["sources"]["ga4"] = {"status": "ok", "period": ga4["period"]}
            print("  ✓ OK")
        else:
            unified["traffic"] = {"sessions": 0, "users": 0, "bySource": [], "byCountry": []}
            unified["sources"]["ga4"] = {"status": "skipped", "reason": "GA4_PROPERTY_ID not set"}
            warnings.append("[WARN] GA4 skipped — GA4_PROPERTY_ID not set")
            print("  ⊘ SKIPPED")
    except Exception as e:
        msg = f"ga4: {e}"
        print(f"  ✗ ERROR: {e}", file=sys.stderr)
        traceback.print_exc()
        errors.append(msg)
        warnings.append(f"[WARN] GA4 failed: {e}")
        unified["traffic"] = {"sessions": 0, "users": 0, "bySource": [], "byCountry": []}
        unified["sources"]["ga4"] = {"status": "error", "error": str(e)}

    # ── 3. BigQuery ───────────────────────────────────────────
    print("\n[3/4] BigQuery AppsFlyer campaigns")
    try:
        bq = pull_bigquery()
        if bq:
            unified["campaigns"] = bq["campaigns"]
            unified["campaignSummary"] = {
                "byMediaSource": bq["byMediaSource"],
                "totalInstalls": bq["totalInstalls"],
            }
            unified["sources"]["bigquery"] = {"status": "ok", "period": bq["period"]}
            print("  ✓ OK")
        else:
            unified["campaigns"] = []
            unified["campaignSummary"] = {"byMediaSource": {}, "totalInstalls": 0}
            unified["sources"]["bigquery"] = {"status": "error", "error": "No data"}
            warnings.append("[WARN] BigQuery returned no data")
    except Exception as e:
        msg = f"bigquery: {e}"
        print(f"  ✗ ERROR: {e}", file=sys.stderr)
        traceback.print_exc()
        errors.append(msg)
        warnings.append(f"[WARN] BigQuery failed: {e}")
        unified["campaigns"] = []
        unified["campaignSummary"] = {"byMediaSource": {}, "totalInstalls": 0}
        unified["sources"]["bigquery"] = {"status": "error", "error": str(e)}

    # ── 4. Google Sheets ──────────────────────────────────────
    print("\n[4/4] Google Sheets budget")
    try:
        budget = pull_sheets()
        unified["budget"] = {
            "monthly_target": budget.get("monthly_target"),
            "spent": budget.get("spent"),
            "remaining": budget.get("remaining"),
            "byCountry": budget.get("byCountry", {}),
        }
        unified["sources"]["sheets"] = {"status": "ok"}
        print("  ✓ OK")
    except Exception as e:
        msg = f"sheets: {e}"
        print(f"  ✗ ERROR: {e}", file=sys.stderr)
        traceback.print_exc()
        errors.append(msg)
        warnings.append(f"[WARN] Sheets failed: {e}")
        unified["budget"] = {"monthly_target": None, "spent": None, "remaining": None}
        unified["sources"]["sheets"] = {"status": "error", "error": str(e)}

    # ── 5. Normalize channels ─────────────────────────────────
    print("\n[5/5] Normalizing channel data")
    try:
        unified["channelPerformance"] = _normalize_channels(unified)
        print(f"  ✓ {len(unified['channelPerformance'])} channels normalized")
    except Exception as e:
        print(f"  ✗ ERROR normalizing channels: {e}", file=sys.stderr)
        traceback.print_exc()
        unified["channelPerformance"] = []
        warnings.append(f"[WARN] Channel normalization failed: {e}")

    # ── Write output ──────────────────────────────────────────
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(unified, f, indent=2, ensure_ascii=False, default=str)

    # ── Summary ───────────────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"  data.json written → {OUT_PATH}")
    print(f"  Timestamp: {unified['lastUpdated']}")
    print(f"  Sources: {len(unified['sources'])} attempted")

    ok_count = sum(1 for s in unified["sources"].values() if s.get("status") == "ok")
    print(f"  Success: {ok_count}/{len(unified['sources'])}")

    if unified.get("channelPerformance"):
        print(f"  Channels: {len(unified['channelPerformance'])} normalized")

    if warnings:
        print(f"\n  WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"    {w}")

    if errors:
        print(f"\n  ERRORS ({len(errors)}):")
        for err in errors:
            print(f"    ✗ {err}")
    else:
        print("\n  All sources OK ✓")
    print("=" * 60)

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(run_pipeline())
