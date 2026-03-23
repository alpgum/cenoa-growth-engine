#!/usr/bin/env python3
"""
Budget Pacing Alert — Cenoa Performance Marketing

Compares actual spend against expected linear pace for the current month.
Reads budget targets and realized cost data from sheets-budget-tracking.json.

Outputs:
  - data/budget-pacing.json  (structured pacing report)
  - stdout summary

Note: Real-time current-month spend requires fresh Sheets/API pull.
      This script uses the latest available monthly data as a proxy and
      flags when live data is unavailable.
"""

import json
import os
import sys
from datetime import datetime, date
from calendar import monthrange
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_DIR = PROJECT_DIR / "data"

SHEETS_FILE = DATA_DIR / "sheets-budget-tracking.json"
OUTPUT_FILE = DATA_DIR / "budget-pacing.json"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_sheets_data() -> dict:
    with open(SHEETS_FILE, "r") as f:
        return json.load(f)


def get_month_budget(data: dict, year: int, month: int) -> dict:
    """Return {budget, label, source} for the requested month."""
    # March 2026 has its own tab
    if year == 2026 and month == 3:
        march = data.get("marchBudget2026", {})
        return {
            "budget": march.get("totalBudget", 50_000),
            "effective_budget": march.get("effectiveBudget", 42_500),
            "label": "March 2026 (dedicated tab)",
            "source": "marchBudget2026",
        }

    # Default: use the top-level estimated budget ($50K/mo)
    dist = data.get("budgetDistribution2026", {})
    return {
        "budget": dist.get("estimatedBudget", 50_000),
        "effective_budget": dist.get("estimatedBudget", 50_000),
        "label": f"{date(year, month, 1):%B %Y} (default plan)",
        "source": "budgetDistribution2026",
    }


def get_realized_spend(data: dict, year: int, month: int) -> dict | None:
    """Return realized spend for a completed month, or None."""
    key_map = {
        (2026, 1): "realizedCostJan2026",
        (2026, 2): "realizedCostFeb2026",
    }
    key = key_map.get((year, month))
    if not key or key not in data:
        return None
    section = data[key]
    total = section.get("summary", {}).get("grandTotal", {}).get("total")
    return {
        "period": section.get("period", ""),
        "total": total,
        "source": key,
    }


def estimate_current_month_spend(data: dict, today: date) -> dict:
    """
    For the current (potentially incomplete) month, try to find partial data.
    Falls back to last known month pro-rated or weekly TR data for March.
    """
    year, month = today.year, today.month

    # If we have realized data for this month already (unlikely mid-month), use it
    realized = get_realized_spend(data, year, month)
    if realized and realized["total"]:
        return {
            "actual_spend": realized["total"],
            "data_fresh": True,
            "method": "realized_cost_tab",
            "note": f"Full realized data from {realized['source']}",
        }

    # March 2026: use weekly TR performance data to extrapolate
    if year == 2026 and month == 3:
        march = data.get("marchBudget2026", {})
        weekly_tr = march.get("weeklyPerformanceTR", {})
        if weekly_tr:
            weekly_total_cost = sum(
                ch.get("cost", 0) for ch in weekly_tr.values() if isinstance(ch, dict)
            )
            days_elapsed = today.day
            # weekly cost → daily cost → elapsed spend
            daily_cost_tr = weekly_total_cost / 7.0 if weekly_total_cost else 0
            # TR is ~55% of total March budget based on plan ($23K / $42.5K)
            tr_share = 23_000 / 42_500
            daily_cost_all = daily_cost_tr / tr_share if tr_share else daily_cost_tr
            estimated = daily_cost_all * days_elapsed
            return {
                "actual_spend": round(estimated, 2),
                "data_fresh": False,
                "method": "weekly_tr_extrapolation",
                "note": (
                    f"Extrapolated from TR weekly cost (${weekly_total_cost}/wk) "
                    f"scaled to all geos. {days_elapsed} days elapsed. "
                    "⚠️ Real-time pacing needs fresh Sheets or ad-platform API pull."
                ),
            }

    # Fallback: use previous month realized, pro-rated
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    prev = get_realized_spend(data, prev_year, prev_month)
    if prev and prev["total"]:
        days_in_month = monthrange(year, month)[1]
        days_elapsed = today.day
        daily_avg_prev = prev["total"] / monthrange(prev_year, prev_month)[1]
        estimated = daily_avg_prev * days_elapsed
        return {
            "actual_spend": round(estimated, 2),
            "data_fresh": False,
            "method": "prev_month_prorated",
            "note": (
                f"Pro-rated from {prev['period']} total ${prev['total']:,.0f}. "
                f"{days_elapsed}/{days_in_month} days elapsed. "
                "⚠️ Real-time pacing needs fresh Sheets or ad-platform API pull."
            ),
        }

    return {
        "actual_spend": None,
        "data_fresh": False,
        "method": "no_data",
        "note": "No realized cost data available. Cannot estimate pacing.",
    }


def classify_pace(pace_pct: float | None) -> str:
    if pace_pct is None:
        return "UNKNOWN"
    if pace_pct > 120:
        return "OVERSPENDING"
    if pace_pct < 80:
        return "UNDERSPENDING"
    return "ON TRACK"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    today = date.today()
    year, month = today.year, today.month
    days_in_month = monthrange(year, month)[1]
    days_elapsed = today.day

    data = load_sheets_data()

    # Budget target
    budget_info = get_month_budget(data, year, month)
    monthly_budget = budget_info["budget"]

    # Expected linear spend
    expected_spend = round(monthly_budget * (days_elapsed / days_in_month), 2)

    # Actual / estimated spend
    spend_info = estimate_current_month_spend(data, today)
    actual_spend = spend_info["actual_spend"]

    # Pace calculation
    pace_pct = None
    if actual_spend is not None and expected_spend > 0:
        pace_pct = round((actual_spend / expected_spend) * 100, 1)

    status = classify_pace(pace_pct)

    # Build output
    report = {
        "generated_at": datetime.now().isoformat(),
        "month": f"{today:%Y-%m}",
        "month_label": budget_info["label"],
        "budget": monthly_budget,
        "effective_budget": budget_info.get("effective_budget", monthly_budget),
        "days_in_month": days_in_month,
        "days_elapsed": days_elapsed,
        "expected_spend": expected_spend,
        "actual_spend_estimate": actual_spend,
        "pace_pct": pace_pct,
        "status": status,
        "estimation_method": spend_info["method"],
        "data_fresh": spend_info["data_fresh"],
        "note": spend_info["note"],
        "thresholds": {
            "overspending": ">120% of expected pace",
            "on_track": "80-120% of expected pace",
            "underspending": "<80% of expected pace",
        },
        "historical_context": {},
    }

    # Add historical months for context
    for hist_year, hist_month, key_label in [
        (2026, 1, "jan_2026"),
        (2026, 2, "feb_2026"),
    ]:
        r = get_realized_spend(data, hist_year, hist_month)
        if r and r["total"]:
            report["historical_context"][key_label] = {
                "period": r["period"],
                "total_spend": r["total"],
                "budget": 50_000,
                "utilization_pct": round((r["total"] / 50_000) * 100, 1),
            }

    # Write JSON
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(report, f, indent=2)

    # Print summary
    print("=" * 60)
    print(f"  BUDGET PACING ALERT — {budget_info['label']}")
    print("=" * 60)
    print(f"  Monthly budget:    ${monthly_budget:>10,.0f}")
    print(f"  Days elapsed:      {days_elapsed:>10} / {days_in_month}")
    print(f"  Expected spend:    ${expected_spend:>10,.0f}")
    if actual_spend is not None:
        print(f"  Actual (est.):     ${actual_spend:>10,.0f}")
        print(f"  Pace:              {pace_pct:>10.1f}%")
    else:
        print(f"  Actual (est.):     {'N/A':>10}")
        print(f"  Pace:              {'N/A':>10}")
    print(f"  Status:            {'⚠️  ' if status != 'ON TRACK' else '✅ '}{status}")
    print("-" * 60)
    print(f"  Method: {spend_info['method']}")
    print(f"  Note:   {spend_info['note']}")
    print("-" * 60)

    # Historical context
    if report["historical_context"]:
        print("  Historical:")
        for k, v in report["historical_context"].items():
            print(f"    {k}: ${v['total_spend']:,.0f} / ${v['budget']:,.0f} ({v['utilization_pct']}%)")
    print("=" * 60)

    # Write output path
    print(f"\n  Output: {OUTPUT_FILE}")

    # Exit code: non-zero for alerts
    if status == "OVERSPENDING":
        sys.exit(2)
    elif status == "UNDERSPENDING":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
