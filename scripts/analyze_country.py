#!/usr/bin/env python3
"""Analyze country breakdown data and produce markdown report."""

import json

with open("../data/country-breakdown-20260320.json") as f:
    data = json.load(f)

lines = []
lines.append("# Country Breakdown Analysis — Mar 14–20, 2026\n")
lines.append("Data source: Amplitude Segmentation API\n")
lines.append("Period: March 14–20, 2026 (7 days)\n")

event_summaries = {}

for event_type in data:
    d = data[event_type].get("data", {})
    labels = d.get("seriesLabels", [])
    collapsed = d.get("seriesCollapsed", [])
    
    # Build country -> value mapping
    country_vals = []
    for i, label in enumerate(labels):
        country = label[1] if len(label) > 1 else str(label)
        val = collapsed[i][0]["value"] if i < len(collapsed) and collapsed[i] else 0
        if country and country != "None" and country != "(none)":
            country_vals.append((country, val))
    
    # Sort by value desc
    country_vals.sort(key=lambda x: x[1], reverse=True)
    total = sum(v for _, v in country_vals)
    
    event_summaries[event_type] = {
        "total": total,
        "top": country_vals[:10],
        "all": country_vals,
        "num_countries": len(country_vals),
    }
    
    lines.append(f"## {event_type}\n")
    lines.append(f"**Total:** {total:,} | **Countries:** {len(country_vals)}\n")
    lines.append("| Rank | Country | Count | % |")
    lines.append("|------|---------|------:|---:|")
    
    for rank, (country, val) in enumerate(country_vals[:10], 1):
        pct = (val / total * 100) if total > 0 else 0
        lines.append(f"| {rank} | {country} | {val:,} | {pct:.1f}% |")
    
    # Remaining
    if len(country_vals) > 10:
        rest = sum(v for _, v in country_vals[10:])
        pct = (rest / total * 100) if total > 0 else 0
        lines.append(f"| — | *Others ({len(country_vals)-10} countries)* | {rest:,} | {pct:.1f}% |")
    
    lines.append("")

# Key Insights
lines.append("---\n")
lines.append("## Key Insights\n")

# Find dominant countries per event
for event_type, s in event_summaries.items():
    if s["top"]:
        top_country = s["top"][0][0]
        top_pct = (s["top"][0][1] / s["total"] * 100) if s["total"] > 0 else 0
        short_name = event_type.replace("[AppsFlyer] ", "").replace("Bridgexyz KYC Component: ", "")
        lines.append(f"- **{short_name}**: {top_country} leads with {top_pct:.0f}% ({s['top'][0][1]:,}/{s['total']:,})")

lines.append("")

# Cross-event: Turkey's dominance
lines.append("### Turkey Dominance\n")
for event_type, s in event_summaries.items():
    turkey_val = next((v for c, v in s["all"] if c == "Turkey"), 0)
    pct = (turkey_val / s["total"] * 100) if s["total"] > 0 else 0
    short_name = event_type.replace("[AppsFlyer] ", "").replace("Bridgexyz KYC Component: ", "")
    lines.append(f"- {short_name}: {pct:.0f}% ({turkey_val:,})")

lines.append("")

# Funnel drop-off by country
lines.append("### Funnel Progression (Top Countries)\n")
install_data = event_summaries.get("[AppsFlyer] Install", {})
signup_data = event_summaries.get("Cenoa sign-up completed", {})
kyc_start_data = event_summaries.get("KYC Started", {})
kyc_submit_data = event_summaries.get("Bridgexyz KYC Component: Submit clicked", {})

if install_data.get("top") and signup_data.get("all"):
    lines.append("| Country | Installs | Sign-ups | KYC Started | KYC Submit | Install→Sign-up % |")
    lines.append("|---------|----------|----------|-------------|------------|-------------------|")
    
    for country, installs in install_data["top"][:5]:
        signups = next((v for c, v in signup_data["all"] if c == country), 0)
        kyc_s = next((v for c, v in kyc_start_data.get("all", []) if c == country), 0)
        kyc_sub = next((v for c, v in kyc_submit_data.get("all", []) if c == country), 0)
        conv = (signups / installs * 100) if installs > 0 else 0
        lines.append(f"| {country} | {installs:,} | {signups:,} | {kyc_s:,} | {kyc_sub:,} | {conv:.1f}% |")

lines.append("")

# Anomalies
lines.append("### Anomalies & Notable Patterns\n")

# Check for countries that appear in deposits but not installs (organic/existing users)
deposit_data = event_summaries.get("Deposit Completed", {})
withdraw_data = event_summaries.get("Withdraw Completed", {})

if deposit_data.get("top"):
    lines.append("**Deposit vs Withdraw Activity:**\n")
    for country, dep_val in deposit_data["top"][:5]:
        wd_val = next((v for c, v in withdraw_data.get("all", []) if c == country), 0)
        ratio = f"{dep_val/wd_val:.1f}x" if wd_val > 0 else "∞"
        lines.append(f"- {country}: {dep_val:,} deposits / {wd_val:,} withdrawals (ratio: {ratio})")

lines.append("")

output = "\n".join(lines)
with open("../analysis/country-breakdown.md", "w") as f:
    f.write(output)

print(output)
print("\n--- Saved to analysis/country-breakdown.md ---")
