#!/usr/bin/env python3
"""
Campaign Health Check — flags campaigns as DEAD / BLEEDING / FRAUD / HEALTHY.

Reads:
  - data/sheets-cac-analysis.json   (channel spend + downstream metrics)
  - data/attribution-breakdown-20260320.json  (install/signup by source & campaign)
  - analysis/channel-cac.md          (CPI benchmarks — parsed inline)

Outputs:
  - data/campaign-health.json        (structured flags per campaign)
  - Human-readable summary to stdout
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths (relative to project root)
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

SHEETS_PATH = DATA_DIR / "sheets-cac-analysis.json"
ATTRIBUTION_PATH = DATA_DIR / "attribution-breakdown-20260320.json"
OUTPUT_PATH = DATA_DIR / "campaign-health.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def sum_series(series: list[list[int]]) -> int:
    return sum(sum(day) for day in [series]) if isinstance(series[0], int) else sum(sum(row) for row in series)


# ---------------------------------------------------------------------------
# 1. Build channel-level view from Sheets (most recent period: 9-15 Mar 2026)
# ---------------------------------------------------------------------------
def build_channel_spend(sheets: dict) -> dict[str, dict]:
    """
    Returns {channel_name: {cost, installs, sign_up, virt_acc, new_active}} 
    from the two most recent weekly periods, averaged.
    """
    channels: dict[str, dict] = {}
    periods = sheets.get("channel_2026_all", {}).get("periods", {})

    for period_key, period_data in periods.items():
        for country, country_data in period_data.items():
            if country == "total":
                continue
            ch_data = country_data.get("channels", {})
            for ch_name, metrics in ch_data.items():
                if ch_name not in channels:
                    channels[ch_name] = {"cost": 0, "installs": 0, "sign_up": 0, "virt_acc": 0, "new_active": 0, "country": country}
                for k in ("cost", "installs", "sign_up", "virt_acc", "new_active"):
                    channels[ch_name][k] += metrics.get(k, 0)

    # Also pull Feb 2026 1-15 actuals for extra coverage
    feb_actual = sheets.get("tr_mart_projections", {}).get("feb_2026_1_15_actual", {}).get("channels", {})
    for ch_name, metrics in feb_actual.items():
        if ch_name not in channels:
            channels[ch_name] = {"cost": 0, "installs": 0, "sign_up": 0, "virt_acc": 0, "new_active": 0, "country": "turkey"}
        for k in ("cost", "installs", "sign_up", "virt_acc", "new_active"):
            channels[ch_name][k] += metrics.get(k, 0)

    return channels


# ---------------------------------------------------------------------------
# 2. Build source-level view from Attribution (Amplitude export)
# ---------------------------------------------------------------------------
def build_attribution_sources(attr: dict) -> dict[str, dict]:
    """
    Returns {source_name: {installs, signups, withdrawals}} from 7-day attribution data.
    """
    sources: dict[str, dict] = {}

    # Installs by source
    install_data = attr.get("[AppsFlyer] Install_by_source", {}).get("data", {})
    for i, (_, label) in enumerate(install_data.get("seriesLabels", [])):
        total = sum(install_data["series"][i])
        sources.setdefault(label, {"installs": 0, "signups": 0, "withdrawals": 0})
        sources[label]["installs"] += total

    # Sign-ups by source
    signup_data = attr.get("Cenoa sign-up completed_by_source", {}).get("data", {})
    for i, (_, label) in enumerate(signup_data.get("seriesLabels", [])):
        total = sum(signup_data["series"][i])
        sources.setdefault(label, {"installs": 0, "signups": 0, "withdrawals": 0})
        sources[label]["signups"] += total

    # Withdrawals by source
    withdraw_data = attr.get("Withdraw Completed_by_source", {}).get("data", {})
    for i, (_, label) in enumerate(withdraw_data.get("seriesLabels", [])):
        total = sum(withdraw_data["series"][i])
        sources.setdefault(label, {"installs": 0, "signups": 0, "withdrawals": 0})
        sources[label]["withdrawals"] += total

    return sources


def build_campaign_level(attr: dict) -> dict[str, dict]:
    """
    Returns {campaign_name: {installs, signups, withdrawals}} from campaign-level data.
    """
    campaigns: dict[str, dict] = {}

    install_data = attr.get("install_by_campaign", {}).get("data", {})
    for i, (_, label) in enumerate(install_data.get("seriesLabels", [])):
        total = sum(install_data["series"][i])
        campaigns.setdefault(label, {"installs": 0, "signups": 0, "withdrawals": 0})
        campaigns[label]["installs"] += total

    signup_data = attr.get("Cenoa sign-up completed_by_campaign", {}).get("data", {})
    for i, (_, label) in enumerate(signup_data.get("seriesLabels", [])):
        total = sum(signup_data["series"][i])
        campaigns.setdefault(label, {"installs": 0, "signups": 0, "withdrawals": 0})
        campaigns[label]["signups"] += total

    withdraw_data = attr.get("Withdraw Completed_by_campaign", {}).get("data", {})
    for i, (_, label) in enumerate(withdraw_data.get("seriesLabels", [])):
        total = sum(withdraw_data["series"][i])
        campaigns.setdefault(label, {"installs": 0, "signups": 0, "withdrawals": 0})
        campaigns[label]["withdrawals"] += total

    return campaigns


# ---------------------------------------------------------------------------
# 3. Map media sources to canonical channel names + spend
# ---------------------------------------------------------------------------
SOURCE_TO_CHANNEL = {
    "appnext_int": "appnext",
    "zzgtechltmqk_int": "meta_web2app",
    "Apple Search Ads": "apple_ads",
    "Architect": "google_search",
    "googleadwords_int": "google_search",
    "cenoa.com": "website",
    "cenoacomtr": "website",
    "tiktokglobal_int": "tiktok",
    "byteboost2_int": "spaze",
    "af_app_invites": "referral",
    "Social_instagram": "meta",
    "Facebook Ads": "meta",
    "metaweb_int": "meta",
    "Organic": "organic",
}

# Spend from channel-cac.md scorecard (weekly proxy, USD)
CHANNEL_SPEND_WEEKLY = {
    "google_search": 790.00,
    "pmax_search": 805.50,
    "apple_ads": 600.50,
    "appnext": 446.50,
    "tiktok": 341.00,
    "tiktok_web2app": 341.00,
    "tiktok_android_app": 170.00,
    "tiktok_app": 170.00,
    "meta_web2app": 2754.00,
    "meta": 2754.00,
    "spaze": 900.00,
    "website": 976.50,
    "referral": 0,
    "organic": 0,
    "onboarding_meta_test": 101.00,
    "twitter_ads": 90.00,
    "google_web2app": 453.00,
    "meta_app_ios": 936.00,
    "google_app_ios": 1510.00,
    "meta_get_paid_test": 637.00,
    "meta_ltv_test": 812.00,
    "appnext_dsp": 115.00,
    "spaze_dsp": 1460.00,
}


def get_channel_spend(channel: str) -> float:
    """Look up weekly spend proxy for a channel."""
    return CHANNEL_SPEND_WEEKLY.get(channel, 0)


# ---------------------------------------------------------------------------
# 4. Classification logic
# ---------------------------------------------------------------------------
def classify_channel(name: str, cost: float, installs: int, signups: int,
                     virt_acc: int, new_active: int, avg_cpi: float) -> tuple[str, str]:
    """
    Returns (status, reason).
    
    Thresholds:
      DEAD:     >$100 spend, 0 installs
      BLEEDING: CPI > 2× average
      FRAUD:    high installs but <5% signup conversion (signup/install < 5%)
      HEALTHY:  everything else within range
    """
    cpi = cost / installs if installs > 0 else float("inf")
    signup_rate = signups / installs if installs > 0 else 0
    downstream_rate = virt_acc / installs if installs > 0 else 0

    # DEAD: spending money, getting nothing
    if cost > 100 and installs == 0:
        return "DEAD", f"${cost:.0f} spent, 0 installs"

    # DEAD: spending money, zero signups AND zero activations
    if cost > 100 and installs > 0 and signups == 0 and new_active == 0:
        return "DEAD", f"${cost:.0f} spent, {installs} installs but 0 signups & 0 activations"

    # FRAUD: lots of installs but terrible downstream (<5% signup rate)
    if installs >= 50 and signup_rate < 0.05:
        return "FRAUD", (
            f"{installs} installs but only {signups} signups "
            f"({signup_rate:.1%} conversion) — fraud pattern"
        )

    # FRAUD: decent signups but near-zero downstream activation
    if installs >= 50 and signups > 10 and virt_acc > 0 and downstream_rate < 0.03:
        return "FRAUD", (
            f"{installs} installs, {signups} signups but only {virt_acc} virt_acc "
            f"({downstream_rate:.1%}) — suspicious downstream"
        )

    # BLEEDING: CPI > 2× average
    if cost > 50 and installs > 0 and cpi > 2 * avg_cpi:
        return "BLEEDING", f"CPI ${cpi:.2f} is {cpi/avg_cpi:.1f}× the average (${avg_cpi:.2f})"

    # HEALTHY
    if cost == 0 and installs == 0:
        return "INACTIVE", "No spend, no installs"

    return "HEALTHY", f"CPI ${cpi:.2f}, {signup_rate:.0%} signup rate, {new_active} activations"


def classify_campaign(name: str, installs: int, signups: int, withdrawals: int,
                      source_channel: str | None = None) -> tuple[str, str]:
    """Campaign-level classification using attribution data only (no spend per campaign)."""
    signup_rate = signups / installs if installs > 0 else 0

    # Skip unattributed
    if name in ("N/A", "(none)", "none"):
        return "UNATTRIBUTED", "No campaign attribution"

    # Fraud pattern at campaign level
    if installs >= 20 and signup_rate < 0.05:
        return "FRAUD", f"{installs} installs, {signups} signups ({signup_rate:.1%}) — fraud pattern"

    # Low-quality: installs but zero downstream
    if installs >= 10 and signups == 0 and withdrawals == 0:
        return "DEAD", f"{installs} installs but 0 signups, 0 withdrawals"

    if installs >= 5 and signups > 0:
        if withdrawals == 0 and installs > 20:
            return "BLEEDING", f"{installs} installs, {signups} signups but 0 withdrawals — no downstream value"
        return "HEALTHY", f"{installs} installs, {signups} signups, {withdrawals} withdrawals"

    if installs < 5:
        return "LOW_VOLUME", f"Only {installs} installs — insufficient data"

    return "HEALTHY", f"{installs} installs, {signups} signups, {withdrawals} withdrawals"


# ---------------------------------------------------------------------------
# 5. Main
# ---------------------------------------------------------------------------
def main():
    sheets = load_json(SHEETS_PATH)
    attr = load_json(ATTRIBUTION_PATH)

    # Build data
    channel_spend = build_channel_spend(sheets)
    attr_sources = build_attribution_sources(attr)
    campaigns = build_campaign_level(attr)

    # Compute average CPI across all paid channels with installs
    total_cost = sum(m["cost"] for m in channel_spend.values() if m["cost"] > 0)
    total_installs = sum(m["installs"] for m in channel_spend.values() if m["cost"] > 0 and m["installs"] > 0)
    avg_cpi = total_cost / total_installs if total_installs > 0 else 5.0

    # ---- Classify channels ----
    channel_results = {}
    for ch_name, metrics in sorted(channel_spend.items()):
        status, reason = classify_channel(
            ch_name, metrics["cost"], metrics["installs"],
            metrics["sign_up"], metrics["virt_acc"], metrics["new_active"],
            avg_cpi
        )
        channel_results[ch_name] = {
            "status": status,
            "reason": reason,
            "cost": metrics["cost"],
            "installs": metrics["installs"],
            "sign_up": metrics["sign_up"],
            "virt_acc": metrics["virt_acc"],
            "new_active": metrics["new_active"],
            "cpi": round(metrics["cost"] / metrics["installs"], 2) if metrics["installs"] > 0 else None,
        }

    # ---- Classify campaigns ----
    campaign_results = {}
    for camp_name, metrics in sorted(campaigns.items(), key=lambda x: x[1]["installs"], reverse=True):
        status, reason = classify_campaign(
            camp_name, metrics["installs"], metrics["signups"], metrics["withdrawals"]
        )
        campaign_results[camp_name] = {
            "status": status,
            "reason": reason,
            "installs": metrics["installs"],
            "signups": metrics["signups"],
            "withdrawals": metrics["withdrawals"],
        }

    # ---- Classify attribution sources ----
    source_results = {}
    for src_name, metrics in sorted(attr_sources.items(), key=lambda x: x[1]["installs"], reverse=True):
        ch = SOURCE_TO_CHANNEL.get(src_name, src_name.lower())
        spend = get_channel_spend(ch)
        signup_rate = metrics["signups"] / metrics["installs"] if metrics["installs"] > 0 else 0

        if src_name in ("Organic", "(none)"):
            status, reason = "ORGANIC", "Not a paid channel"
        elif metrics["installs"] >= 50 and signup_rate < 0.05:
            status, reason = "FRAUD", f"{metrics['installs']} installs, {metrics['signups']} signups ({signup_rate:.1%})"
        elif spend > 100 and metrics["installs"] == 0:
            status, reason = "DEAD", f"${spend:.0f} spend proxy, 0 installs"
        elif metrics["installs"] > 0 and spend > 0:
            cpi = spend / metrics["installs"]
            if cpi > 2 * avg_cpi:
                status, reason = "BLEEDING", f"CPI ${cpi:.2f} > 2× avg ${avg_cpi:.2f}"
            else:
                status, reason = "HEALTHY", f"CPI ${cpi:.2f}, {signup_rate:.0%} signup rate"
        else:
            status, reason = "HEALTHY", f"{metrics['installs']} installs, {metrics['signups']} signups"

        source_results[src_name] = {
            "status": status,
            "reason": reason,
            "installs": metrics["installs"],
            "signups": metrics["signups"],
            "withdrawals": metrics["withdrawals"],
            "spend_proxy": spend,
        }

    # ---- Build output ----
    output = {
        "generated_at": datetime.now().isoformat(),
        "avg_cpi": round(avg_cpi, 2),
        "thresholds": {
            "DEAD": ">$100 spend + 0 installs (or 0 signups & 0 activations)",
            "BLEEDING": "CPI > 2× average",
            "FRAUD": "High installs + <5% signup conversion",
            "HEALTHY": "Within normal CPI + reasonable downstream",
        },
        "channels": channel_results,
        "attribution_sources": source_results,
        "campaigns": campaign_results,
    }

    # Write JSON
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # ---- Print summary ----
    print("=" * 72)
    print("  CAMPAIGN HEALTH CHECK")
    print(f"  Generated: {output['generated_at']}")
    print(f"  Average CPI (paid channels): ${avg_cpi:.2f}")
    print("=" * 72)

    # Channel summary
    print("\n📊 CHANNEL HEALTH (Sheets + Attribution)")
    print("-" * 72)
    for status_filter in ("DEAD", "FRAUD", "BLEEDING", "HEALTHY", "INACTIVE"):
        items = [(k, v) for k, v in channel_results.items() if v["status"] == status_filter]
        if not items:
            continue
        emoji = {"DEAD": "💀", "FRAUD": "🚨", "BLEEDING": "🩸", "HEALTHY": "✅", "INACTIVE": "⏸️"}[status_filter]
        print(f"\n  {emoji} {status_filter}")
        for name, r in items:
            cost_str = f"${r['cost']:,.0f}" if r["cost"] else "$0"
            cpi_str = f"${r['cpi']:.2f}" if r["cpi"] else "—"
            print(f"    • {name:25s} | {cost_str:>8s} spend | {r['installs']:>5d} installs | CPI {cpi_str:>7s} | {r['reason']}")

    # Campaign-level flags
    print(f"\n\n📋 CAMPAIGN-LEVEL FLAGS (Attribution, top campaigns)")
    print("-" * 72)
    for status_filter in ("DEAD", "FRAUD", "BLEEDING", "HEALTHY"):
        items = [(k, v) for k, v in campaign_results.items()
                 if v["status"] == status_filter and v["installs"] >= 5]
        if not items:
            continue
        emoji = {"DEAD": "💀", "FRAUD": "🚨", "BLEEDING": "🩸", "HEALTHY": "✅"}[status_filter]
        print(f"\n  {emoji} {status_filter}")
        for name, r in sorted(items, key=lambda x: x[1]["installs"], reverse=True):
            short_name = name[:55] + "…" if len(name) > 55 else name
            print(f"    • {short_name:58s} | {r['installs']:>4d} inst | {r['signups']:>3d} sign | {r['withdrawals']:>4d} wdraw")

    # Attribution source flags
    print(f"\n\n📡 ATTRIBUTION SOURCE FLAGS")
    print("-" * 72)
    for status_filter in ("DEAD", "FRAUD", "BLEEDING", "HEALTHY"):
        items = [(k, v) for k, v in source_results.items()
                 if v["status"] == status_filter]
        if not items:
            continue
        emoji = {"DEAD": "💀", "FRAUD": "🚨", "BLEEDING": "🩸", "HEALTHY": "✅"}[status_filter]
        print(f"\n  {emoji} {status_filter}")
        for name, r in sorted(items, key=lambda x: x[1]["installs"], reverse=True):
            print(f"    • {name:30s} | {r['installs']:>5d} installs | {r['signups']:>3d} signups | {r['withdrawals']:>4d} withdrawals")

    # Summary counts
    print("\n" + "=" * 72)
    for level, label in [("channels", "Channels"), ("campaigns", "Campaigns"), ("attribution_sources", "Sources")]:
        data = output[level]
        counts = {}
        for v in data.values():
            s = v["status"]
            counts[s] = counts.get(s, 0) + 1
        parts = " | ".join(f"{s}: {c}" for s, c in sorted(counts.items()))
        print(f"  {label}: {parts}")
    print("=" * 72)

    print(f"\n✅ Output written to: {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
