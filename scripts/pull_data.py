#!/usr/bin/env python3
"""Master data pipeline — pulls all sources and outputs unified data.json.

Sources:
  1. Amplitude — funnel metrics (install → signup → KYC → withdraw) by country, platform
  2. GA4 — web traffic (sessions, users, source/medium, country)
  3. BigQuery — AppsFlyer campaign installs by media source, campaign
  4. Google Sheets — budget tracking (monthly target, spent, remaining)

Usage:
  source ~/.openclaw/venv/bin/activate
  export GOOGLE_APPLICATION_CREDENTIALS=~/.openclaw/credentials/cenoa-marketingdatawarehouse-82b8600e66d6.json
  python3 projects/cenoa-growth-engine/scripts/pull_data.py

Optional env vars:
  GA4_PROPERTY_ID  — numeric GA4 property id (if not set, GA4 section is skipped)
"""

import json
import os
import sys
import traceback
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


def _now_iso():
    ist = timezone(timedelta(hours=3))
    return datetime.now(ist).isoformat(timespec="seconds")


def main():
    print("=" * 60)
    print("  CENOA GROWTH ENGINE — DATA PIPELINE")
    print(f"  {_now_iso()}")
    print("=" * 60)

    errors = []
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
        print("  OK")
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        traceback.print_exc()
        errors.append(f"amplitude: {e}")
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
            print("  OK")
        else:
            unified["traffic"] = {"sessions": 0, "users": 0, "bySource": [], "byCountry": []}
            unified["sources"]["ga4"] = {"status": "skipped", "reason": "GA4_PROPERTY_ID not set"}
            print("  SKIPPED")
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        traceback.print_exc()
        errors.append(f"ga4: {e}")
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
            print("  OK")
        else:
            unified["campaigns"] = []
            unified["campaignSummary"] = {"byMediaSource": {}, "totalInstalls": 0}
            unified["sources"]["bigquery"] = {"status": "error", "error": "No data"}
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        traceback.print_exc()
        errors.append(f"bigquery: {e}")
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
        print("  OK")
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        traceback.print_exc()
        errors.append(f"sheets: {e}")
        unified["budget"] = {"monthly_target": None, "spent": None, "remaining": None}
        unified["sources"]["sheets"] = {"status": "error", "error": str(e)}

    # ── Write output ──────────────────────────────────────────
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(unified, f, indent=2, ensure_ascii=False, default=str)

    print("\n" + "=" * 60)
    print(f"  data.json written to {OUT_PATH}")
    print(f"  Sources: {len(unified['sources'])} attempted")
    if errors:
        print(f"  ERRORS ({len(errors)}):")
        for err in errors:
            print(f"    - {err}")
    else:
        print("  All sources OK")
    print("=" * 60)

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
