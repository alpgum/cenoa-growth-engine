#!/usr/bin/env python3
"""Pull Google Sheets budget tracking data.

Reads the Budget Tracking sheet and extracts monthly budget, spent, remaining.
Returns a dict ready for unified data.json.
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

BUDGET_SHEET_ID = "1H27QF84Nm02nAhXebP6zWgEG7pwu_UTwcliO_c4mKmM"

DEFAULT_CREDENTIALS = os.path.expanduser(
    "~/.openclaw/credentials/cenoa-marketingdatawarehouse-82b8600e66d6.json"
)


def _get_service(creds_path=None):
    creds_path = creds_path or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", DEFAULT_CREDENTIALS)
    creds = service_account.Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds, cache_discovery=False)


def _safe_float(val):
    if val is None or val == "":
        return None
    try:
        return float(str(val).replace(",", "").replace("$", "").replace("₺", "").strip())
    except (ValueError, TypeError):
        return None


def _read_tab(service, sheet_id, tab_name):
    """Read a tab and return list of dicts (header row = keys)."""
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id, range=f"'{tab_name}'!A:ZZ"
        ).execute()
    except Exception as e:
        print(f"    WARNING: Cannot read tab '{tab_name}': {e}", file=sys.stderr)
        return []

    values = result.get("values", [])
    if len(values) < 2:
        return []

    headers = values[0]
    rows = []
    for row in values[1:]:
        d = {}
        for i, h in enumerate(headers):
            if not h:
                continue
            d[h] = row[i] if i < len(row) else ""
        rows.append(d)
    return rows


def _load_from_pre_synced():
    """Fallback: load budget data from pre-synced JSON file."""
    pre_synced = os.path.join(os.path.dirname(__file__), "..", "data", "sheets-budget-tracking.json")
    if not os.path.exists(pre_synced):
        return None

    print("    Loading from pre-synced budget JSON...")
    with open(pre_synced) as f:
        synced = json.load(f)

    budget_data = {
        "monthly_target": None,
        "spent": None,
        "remaining": None,
        "byCountry": {},
        "tabs": synced.get("tabs", []),
    }

    bd = synced.get("budgetDistribution2026", {})
    if bd:
        budget_data["monthly_target"] = bd.get("estimatedBudget")
        by_country = bd.get("byCountry", {})
        for country, info in by_country.items():
            if isinstance(info, dict) and "amount" in info:
                budget_data["byCountry"][country] = info["amount"]

    # Get latest realized cost
    for key in ["realizedCostMar2026", "realizedCostFeb2026", "realizedCostJan2026"]:
        rc = synced.get(key, {})
        gt = rc.get("summary", {}).get("grandTotal", {})
        if gt and gt.get("total"):
            budget_data["spent"] = gt["total"]
            if budget_data["monthly_target"]:
                budget_data["remaining"] = round(budget_data["monthly_target"] - budget_data["spent"], 2)
            break

    print(f"    Budget: target={budget_data['monthly_target']}, spent={budget_data['spent']}")
    return budget_data


def pull(creds_path=None):
    """Pull budget data from Google Sheets. Returns dict for unified data.json."""
    print("  [Sheets] Reading budget sheet...")

    # Try live API first
    try:
        service = _get_service(creds_path)
        spreadsheet = service.spreadsheets().get(
            spreadsheetId=BUDGET_SHEET_ID, includeGridData=False
        ).execute()
        tab_names = [s["properties"]["title"] for s in spreadsheet["sheets"]]
        print(f"    Tabs: {tab_names}")
    except Exception as e:
        print(f"    Sheets API unavailable ({type(e).__name__}), using fallback...")
        fallback = _load_from_pre_synced()
        if fallback:
            return fallback
        raise

    # Try to find current month's budget tab
    now = datetime.now(timezone(timedelta(hours=3)))
    current_month = now.strftime("%B").lower()  # e.g., "march"
    current_month_short = now.strftime("%b").lower()  # e.g., "mar"

    budget_data = {
        "monthly_target": None,
        "spent": None,
        "remaining": None,
        "byCountry": {},
        "tabs": tab_names,
    }

    # Read all tabs and extract what we can
    all_tabs_data = {}
    for tab in tab_names:
        rows = _read_tab(service, BUDGET_SHEET_ID, tab)
        all_tabs_data[tab] = rows

        tab_lower = tab.lower()

        # Look for budget/spend data in current month tab
        if current_month in tab_lower or current_month_short in tab_lower or "budget" in tab_lower:
            for row in rows:
                row_lower = {k.lower().strip(): v for k, v in row.items()}

                # Try to find total spend
                for key in ["total spend", "total", "spend", "cost", "amount"]:
                    if key in row_lower:
                        val = _safe_float(row_lower[key])
                        if val is not None and val > 0:
                            if budget_data["spent"] is None or val > budget_data["spent"]:
                                budget_data["spent"] = val

                # Try to find budget target
                for key in ["budget", "target", "monthly budget", "total budget"]:
                    if key in row_lower:
                        val = _safe_float(row_lower[key])
                        if val is not None and val > 0:
                            if budget_data["monthly_target"] is None:
                                budget_data["monthly_target"] = val

                # Country-level data
                for key in ["country", "market", "geo"]:
                    if key in row_lower:
                        country = str(row_lower[key]).strip().upper()[:2]
                        if country and len(country) == 2:
                            spend_val = None
                            for sk in ["spend", "cost", "amount", "total"]:
                                if sk in row_lower:
                                    spend_val = _safe_float(row_lower[sk])
                                    if spend_val is not None:
                                        break
                            if spend_val is not None:
                                budget_data["byCountry"][country] = spend_val

    # Calculate remaining
    if budget_data["monthly_target"] and budget_data["spent"]:
        budget_data["remaining"] = round(budget_data["monthly_target"] - budget_data["spent"], 2)

    # Also try to load from the pre-synced JSON if direct extraction was sparse
    pre_synced = os.path.join(os.path.dirname(__file__), "..", "data", "sheets-budget-tracking.json")
    if os.path.exists(pre_synced) and budget_data["monthly_target"] is None:
        print("    Falling back to pre-synced budget JSON...")
        with open(pre_synced) as f:
            synced = json.load(f)
        # Extract from known structure
        bd = synced.get("budgetDistribution2026", {})
        if bd:
            budget_data["monthly_target"] = bd.get("estimatedBudget")
            by_country = bd.get("byCountry", {})
            for country, info in by_country.items():
                if isinstance(info, dict) and "amount" in info:
                    budget_data["byCountry"][country] = info["amount"]

        # Get latest realized cost
        for key in ["realizedCostMar2026", "realizedCostFeb2026", "realizedCostJan2026"]:
            rc = synced.get(key, {})
            gt = rc.get("summary", {}).get("grandTotal", {})
            if gt and gt.get("total"):
                budget_data["spent"] = gt["total"]
                if budget_data["monthly_target"]:
                    budget_data["remaining"] = round(budget_data["monthly_target"] - budget_data["spent"], 2)
                break

    print(f"    Budget: target={budget_data['monthly_target']}, spent={budget_data['spent']}")
    return budget_data


if __name__ == "__main__":
    data = pull()
    print(json.dumps(data, indent=2, default=str))
