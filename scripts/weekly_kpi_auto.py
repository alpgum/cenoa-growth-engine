#!/usr/bin/env python3
"""Weekly KPI Auto-Calculator — reads data.json and produces KPI summary + markdown report.

Calculates:
  1. Install → Signup conversion rate + WoW trend
  2. Signup → KYC Start conversion + country breakdown
  3. KYC Start → KYC Complete (flags the ~92% dropout)
  4. TRUE CAC per channel
  5. Output: summary JSON + markdown report

Usage:
  python3 scripts/weekly_kpi_auto.py
  # Reads: data.json
  # Writes: data/weekly_kpi_summary.json + data/weekly_kpi_report.md
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
DATA_PATH = ROOT / "data.json"
OUT_DIR = ROOT / "data"
SUMMARY_PATH = OUT_DIR / "weekly_kpi_summary.json"
REPORT_PATH = OUT_DIR / "weekly_kpi_report.md"
HISTORY_PATH = OUT_DIR / "kpi_history.json"

IST = timezone(timedelta(hours=3))

# Target benchmarks
TARGETS = {
    "CPI": {"TR": 2.50, "EG": 3.50, "NG": 3.00, "PK": 2.00, "default": 3.00},
    "activation_rate": 0.15,
    "kyc_completion_rate": 0.20,
}


def _now_iso():
    return datetime.now(IST).isoformat(timespec="seconds")


def _safe_div(a, b):
    if not b:
        return None
    return round(a / b, 4)


def _pct(val):
    """Format ratio as percentage string."""
    if val is None:
        return "N/A"
    return f"{val * 100:.1f}%"


def _delta_str(current, previous):
    """Return WoW delta string like '+3.2pp' or '-1.1pp'."""
    if current is None or previous is None:
        return "N/A (no prior week)"
    diff = (current - previous) * 100  # percentage points
    sign = "+" if diff >= 0 else ""
    return f"{sign}{diff:.1f}pp"


def load_data():
    if not DATA_PATH.exists():
        print(f"ERROR: {DATA_PATH} not found. Run unified_data_pipeline.py first.", file=sys.stderr)
        sys.exit(1)
    with open(DATA_PATH) as f:
        return json.load(f)


def load_history():
    """Load KPI history for WoW comparison."""
    if HISTORY_PATH.exists():
        with open(HISTORY_PATH) as f:
            return json.load(f)
    return []


def save_history(history, current_kpis):
    """Append current KPIs to history, keep last 8 weeks."""
    entry = {
        "date": _now_iso(),
        "funnel": current_kpis.get("funnel_rates", {}),
    }
    history.append(entry)
    history = history[-8:]  # keep last 8 weeks
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)
    return history


def calc_funnel_rates(funnel):
    """Calculate funnel conversion rates."""
    install = funnel.get("install", 0)
    signup = funnel.get("signup", 0)
    kyc_start = funnel.get("kycStart", 0)
    kyc_complete = funnel.get("kycComplete", 0)
    withdraw = funnel.get("withdraw", 0)

    return {
        "install": install,
        "signup": signup,
        "kycStart": kyc_start,
        "kycComplete": kyc_complete,
        "withdraw": withdraw,
        "install_to_signup": _safe_div(signup, install),
        "signup_to_kycStart": _safe_div(kyc_start, signup),
        "kycStart_to_kycComplete": _safe_div(kyc_complete, kyc_start),
        "kycComplete_to_withdraw": _safe_div(withdraw, kyc_complete),
        "install_to_withdraw": _safe_div(withdraw, install),
    }


def calc_country_breakdown(funnel_by_country):
    """Calculate per-country funnel rates with KYC dropout flagging."""
    countries = {}
    for code, data in funnel_by_country.items():
        install = data.get("install", 0)
        signup = data.get("signup", 0)
        kyc_start = data.get("kycStart", 0)
        kyc_complete = data.get("kycComplete", 0)
        withdraw = data.get("withdraw", 0)

        kyc_rate = _safe_div(kyc_complete, kyc_start)
        kyc_dropout = round(1 - kyc_rate, 4) if kyc_rate is not None else None

        countries[code] = {
            "install": install,
            "signup": signup,
            "kycStart": kyc_start,
            "kycComplete": kyc_complete,
            "withdraw": withdraw,
            "install_to_signup": _safe_div(signup, install),
            "signup_to_kycStart": _safe_div(kyc_start, signup),
            "kycStart_to_kycComplete": kyc_rate,
            "kyc_dropout_rate": kyc_dropout,
            "kyc_blocked": kyc_start > 0 and kyc_complete == 0,
        }

    return countries


def calc_channel_cac(channel_performance):
    """Extract TRUE CAC per channel from normalized channel data."""
    result = []
    for ch in channel_performance:
        result.append({
            "channel": ch.get("channel"),
            "spend": ch.get("spend"),
            "installs": ch.get("installs"),
            "CPI": ch.get("CPI"),
            "new_active": ch.get("new_active"),
            "TRUE_CAC": ch.get("TRUE_CAC"),
            "activation_rate": ch.get("activation_rate"),
        })
    return sorted(result, key=lambda x: x.get("TRUE_CAC") or 9999)


def generate_summary(data):
    """Generate full KPI summary dict."""
    funnel = data.get("funnel", {})
    funnel_by_country = data.get("funnelByCountry", {})
    channel_perf = data.get("channelPerformance", [])
    budget = data.get("budget", {})

    funnel_rates = calc_funnel_rates(funnel)
    country_breakdown = calc_country_breakdown(funnel_by_country)
    channel_cac = calc_channel_cac(channel_perf)

    # Identify critical issues
    alerts = []

    # KYC dropout alert
    kyc_rate = funnel_rates.get("kycStart_to_kycComplete")
    if kyc_rate is not None and kyc_rate < 0.10:
        dropout = round((1 - kyc_rate) * 100, 1)
        alerts.append({
            "severity": "P0",
            "type": "kyc_dropout",
            "message": f"KYC completion rate is {_pct(kyc_rate)} — {dropout}% dropout. This is the #1 growth blocker.",
        })

    # KYC blocked countries
    for code, cd in country_breakdown.items():
        if cd.get("kyc_blocked") and cd.get("kycStart", 0) >= 5:
            alerts.append({
                "severity": "P1",
                "type": "kyc_blocked",
                "message": f"{code}: KYC BLOCKED — {cd['kycStart']} started, 0 completed",
            })

    # Budget overspend
    if budget.get("remaining") is not None and budget["remaining"] < 0:
        alerts.append({
            "severity": "P1",
            "type": "budget_overspend",
            "message": f"Budget overspent by ${abs(budget['remaining']):,.0f} (target: ${budget.get('monthly_target', 0):,.0f})",
        })

    # WoW comparison
    history = load_history()
    wow = {}
    if history:
        prev = history[-1].get("funnel", {})
        for key in ["install_to_signup", "signup_to_kycStart", "kycStart_to_kycComplete", "install_to_withdraw"]:
            wow[key] = _delta_str(funnel_rates.get(key), prev.get(key))

    summary = {
        "generated_at": _now_iso(),
        "data_as_of": data.get("lastUpdated"),
        "funnel_rates": funnel_rates,
        "wow_delta": wow,
        "country_breakdown": country_breakdown,
        "channel_cac": channel_cac,
        "budget": {
            "target": budget.get("monthly_target"),
            "spent": budget.get("spent"),
            "remaining": budget.get("remaining"),
        },
        "alerts": alerts,
    }

    # Save to history for next week's comparison
    save_history(history, summary)

    return summary


def generate_markdown_report(summary):
    """Generate human-readable markdown report."""
    lines = []
    lines.append("# Cenoa Growth Engine — Weekly KPI Report")
    lines.append(f"**Generated:** {summary['generated_at']}")
    lines.append(f"**Data as of:** {summary.get('data_as_of', 'N/A')}")
    lines.append("")

    # Alerts
    alerts = summary.get("alerts", [])
    if alerts:
        lines.append("## Alerts")
        for a in alerts:
            icon = "🔴" if a["severity"] == "P0" else "🟡"
            lines.append(f"- {icon} **[{a['severity']}]** {a['message']}")
        lines.append("")

    # Funnel
    fr = summary.get("funnel_rates", {})
    wow = summary.get("wow_delta", {})
    lines.append("## Funnel Conversion Rates")
    lines.append("")
    lines.append("| Step | Count | Rate | WoW |")
    lines.append("|------|------:|-----:|----:|")
    lines.append(f"| Install | {fr.get('install', 0):,} | — | — |")
    lines.append(f"| → Signup | {fr.get('signup', 0):,} | {_pct(fr.get('install_to_signup'))} | {wow.get('install_to_signup', '—')} |")
    lines.append(f"| → KYC Start | {fr.get('kycStart', 0):,} | {_pct(fr.get('signup_to_kycStart'))} | {wow.get('signup_to_kycStart', '—')} |")
    lines.append(f"| → KYC Complete | {fr.get('kycComplete', 0):,} | {_pct(fr.get('kycStart_to_kycComplete'))} | {wow.get('kycStart_to_kycComplete', '—')} |")
    lines.append(f"| → Withdraw | {fr.get('withdraw', 0):,} | {_pct(fr.get('kycComplete_to_withdraw'))} | — |")
    lines.append("")
    lines.append(f"**End-to-end activation (Install → Withdraw):** {_pct(fr.get('install_to_withdraw'))}")
    lines.append("")

    # KYC Dropout callout
    kyc_rate = fr.get("kycStart_to_kycComplete")
    if kyc_rate is not None and kyc_rate < 0.10:
        dropout = round((1 - kyc_rate) * 100, 1)
        lines.append(f"> **🚨 KYC DROPOUT: {dropout}%** — Only {_pct(kyc_rate)} of users who start KYC complete it.")
        lines.append(f"> This is the single biggest funnel leak. Investigate: UX friction, document requirements, provider issues.")
        lines.append("")

    # Country breakdown (top markets)
    lines.append("## Country Breakdown (Top Markets)")
    lines.append("")
    lines.append("| Country | Installs | Signup Rate | KYC Start Rate | KYC Complete Rate | KYC Blocked? |")
    lines.append("|---------|--------:|-----------:|---------------:|------------------:|:------------:|")

    cbd = summary.get("country_breakdown", {})
    # Sort by installs descending, show top 10
    top_countries = sorted(cbd.items(), key=lambda x: x[1].get("install", 0), reverse=True)[:10]
    for code, cd in top_countries:
        blocked = "🔴 YES" if cd.get("kyc_blocked") else "—"
        lines.append(
            f"| {code} | {cd.get('install', 0):,} | {_pct(cd.get('install_to_signup'))} "
            f"| {_pct(cd.get('signup_to_kycStart'))} | {_pct(cd.get('kycStart_to_kycComplete'))} | {blocked} |"
        )
    lines.append("")

    # Channel CAC
    lines.append("## TRUE CAC by Channel")
    lines.append("")
    lines.append("| Channel | Installs | Est. Spend | CPI | New Actives | TRUE CAC |")
    lines.append("|---------|--------:|-----------:|----:|------------:|---------:|")

    for ch in summary.get("channel_cac", [])[:10]:
        spend = f"${ch['spend']:,.0f}" if ch.get("spend") else "—"
        cpi = f"${ch['CPI']:.2f}" if ch.get("CPI") else "—"
        cac = f"${ch['TRUE_CAC']:.2f}" if ch.get("TRUE_CAC") else "—"
        active = str(ch.get("new_active", 0)) if ch.get("new_active") else "—"
        lines.append(f"| {ch['channel']} | {ch.get('installs', 0):,} | {spend} | {cpi} | {active} | {cac} |")
    lines.append("")

    # Budget
    b = summary.get("budget", {})
    if b.get("target"):
        lines.append("## Budget Status")
        lines.append("")
        lines.append(f"- **Monthly Target:** ${b['target']:,.0f}")
        spent = b.get("spent")
        if spent is not None:
            lines.append(f"- **Spent:** ${spent:,.0f}")
            remaining = b.get("remaining")
            if remaining is not None:
                status = "🔴 OVER BUDGET" if remaining < 0 else "🟢 On track"
                lines.append(f"- **Remaining:** ${remaining:,.0f} {status}")
        lines.append("")

    # Recommendations
    lines.append("## Recommended Actions")
    lines.append("")
    lines.append("1. **P0 — Fix KYC dropout:** Investigate the ~92% KYC dropout. Check UX flow, document upload, KYC provider success rates.")
    if any(cd.get("kyc_blocked") for cd in cbd.values()):
        blocked_list = [code for code, cd in cbd.items() if cd.get("kyc_blocked") and cd.get("kycStart", 0) >= 5]
        if blocked_list:
            lines.append(f"2. **P1 — KYC blocked markets:** {', '.join(blocked_list)} have 0% KYC completion. Verify KYC provider coverage.")
    if b.get("remaining") is not None and b["remaining"] < 0:
        lines.append(f"3. **P1 — Budget overspend:** Reduce spend or reallocate from low-performing channels.")
    lines.append("")

    lines.append("---")
    lines.append(f"*Auto-generated by weekly_kpi_auto.py at {summary['generated_at']}*")

    return "\n".join(lines)


def main():
    print("=" * 60)
    print("  CENOA GROWTH ENGINE — WEEKLY KPI AUTO-CALCULATOR")
    print(f"  {_now_iso()}")
    print("=" * 60)

    data = load_data()
    print(f"\n  Data loaded: {data.get('lastUpdated', 'unknown')}")

    # Generate summary
    print("  Calculating KPIs...")
    summary = generate_summary(data)

    # Write JSON summary
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    print(f"  ✓ Summary JSON → {SUMMARY_PATH}")

    # Write markdown report
    report = generate_markdown_report(summary)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  ✓ Markdown report → {REPORT_PATH}")

    # Print quick summary to console
    fr = summary.get("funnel_rates", {})
    print(f"\n  --- Quick Summary ---")
    print(f"  Install → Signup:      {_pct(fr.get('install_to_signup'))}")
    print(f"  Signup → KYC Start:    {_pct(fr.get('signup_to_kycStart'))}")
    print(f"  KYC Start → Complete:  {_pct(fr.get('kycStart_to_kycComplete'))}")
    print(f"  Install → Withdraw:    {_pct(fr.get('install_to_withdraw'))}")

    alerts = summary.get("alerts", [])
    if alerts:
        print(f"\n  🚨 ALERTS ({len(alerts)}):")
        for a in alerts:
            print(f"    [{a['severity']}] {a['message']}")

    print("\n" + "=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
