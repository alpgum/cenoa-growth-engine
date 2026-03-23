#!/usr/bin/env python3
"""
[S2B-010] Google Sheets auto-sync script.
Pulls ALL tabs from 3 sheets and saves as JSON.
Uses service account credentials via GOOGLE_APPLICATION_CREDENTIALS.
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta

from google.oauth2 import service_account
from googleapiclient.discovery import build

# ── Config ────────────────────────────────────────────────────────────
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

SHEETS = [
    {
        "id": "1d743wipSvWEfwwXCmy2J73yCAMNYa-hCb-nTvNf3yHc",
        "name": "CaC Analysis",
        "output": "sheets-cac-analysis.json",
    },
    {
        "id": "1VTZQbRD0gZAABLvgjwlymAx0sQ7vcvMUySsWzLhnFKk",
        "name": "Budget Tracking",
        "output": "sheets-budget-tracking.json",
    },
    {
        "id": "1H27QF84Nm02nAhXebP6zWgEG7pwu_UTwcliO_c4mKmM",
        "name": "Trafik Canavarı",
        "output": "sheets-trafik-canavari.json",
    },
]

# ── Paths ─────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

CREDS_PATH = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS",
    os.path.expanduser(
        "~/.openclaw/credentials/cenoa-marketingdatawarehouse-82b8600e66d6.json"
    ),
)


def get_service():
    creds = service_account.Credentials.from_service_account_file(
        CREDS_PATH, scopes=SCOPES
    )
    return build("sheets", "v4", credentials=creds, cache_discovery=False)


def sync_sheet(service, sheet_cfg):
    """Pull all tabs from a sheet, return {tabs: {tab_name: {headers, rows, row_count}}}."""
    spreadsheet = (
        service.spreadsheets()
        .get(spreadsheetId=sheet_cfg["id"], includeGridData=False)
        .execute()
    )

    tab_names = [s["properties"]["title"] for s in spreadsheet["sheets"]]

    # Batch-get all tabs in one call
    ranges = [f"'{t}'!A:ZZ" for t in tab_names]
    result = (
        service.spreadsheets()
        .values()
        .batchGet(spreadsheetId=sheet_cfg["id"], ranges=ranges)
        .execute()
    )

    ist = timezone(timedelta(hours=3))
    now = datetime.now(ist).isoformat()

    data = {
        "metadata": {
            "source": f"Google Sheets - {sheet_cfg['name']}",
            "sheet_id": sheet_cfg["id"],
            "synced_at": now,
            "tab_count": len(tab_names),
            "tabs": tab_names,
        },
        "tabs": {},
    }

    total_rows = 0
    tab_summaries = []

    for vr in result.get("valueRanges", []):
        range_str = vr.get("range", "")
        # Extract tab name from range like "'Tab Name'!A1:ZZ1000"
        tab_name = range_str.split("!")[0].strip("'")

        values = vr.get("values", [])
        if not values:
            data["tabs"][tab_name] = {"headers": [], "rows": [], "row_count": 0}
            tab_summaries.append((tab_name, 0))
            continue

        headers = values[0] if values else []
        rows = values[1:] if len(values) > 1 else []

        # Convert rows to dicts (handle ragged rows)
        row_dicts = []
        for row in rows:
            d = {}
            for i, h in enumerate(headers):
                if not h:
                    continue
                d[h] = row[i] if i < len(row) else ""
            row_dicts.append(d)

        data["tabs"][tab_name] = {
            "headers": headers,
            "rows": row_dicts,
            "row_count": len(row_dicts),
        }
        total_rows += len(row_dicts)
        tab_summaries.append((tab_name, len(row_dicts)))

    # Write JSON
    out_path = os.path.join(DATA_DIR, sheet_cfg["output"])
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return tab_summaries, total_rows


def main():
    print("📊 Google Sheets Auto-Sync")
    print("=" * 50)

    service = get_service()

    for sheet_cfg in SHEETS:
        print(f"\n🔄 Syncing: {sheet_cfg['name']}")
        try:
            tab_summaries, total_rows = sync_sheet(service, sheet_cfg)
            print(f"   📁 {len(tab_summaries)} tabs, {total_rows} total rows")
            for tab_name, row_count in tab_summaries:
                print(f"      • {tab_name}: {row_count} rows")
            print(f"   ✅ Saved → data/{sheet_cfg['output']}")
        except Exception as e:
            print(f"   ❌ Error: {e}", file=sys.stderr)
            raise

    print("\n✅ All sheets synced!")


if __name__ == "__main__":
    main()
