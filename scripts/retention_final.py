#!/usr/bin/env python3
"""Final retention curves builder with calibrated model."""

import json
import math
from datetime import datetime

# Load data
with open("data/retention-curves-raw-v2.json") as f:
    raw = json.load(f)

with open("data/cohort-retention-30d.json") as f:
    cohort_d30 = json.load(f)

# ============================================================
# 1. GROUND TRUTH: D30 Withdraw retention by country
# ============================================================
# Use Oct 2025 - Jan 2026 cohorts (most recent with full D30 data)
recent_months = ["2025-10", "2025-11", "2025-12", "2026-01"]

from collections import defaultdict
country_agg = defaultdict(lambda: {"signups": 0, "retained_30d": 0})

for ck in recent_months:
    if ck in cohort_d30.get("cohorts_by_country", {}):
        for country, vals in cohort_d30["cohorts_by_country"][ck].items():
            country_agg[country]["signups"] += vals["signups"]
            country_agg[country]["retained_30d"] += vals["retained_30d"]

# D30 withdraw rates
d30_withdraw = {}
for c in ["TR", "NG", "EG", "Unknown"]:
    s = country_agg[c]["signups"]
    r = country_agg[c]["retained_30d"]
    d30_withdraw[c] = {"signups": s, "retained": r, "rate": r/s if s > 0 else 0}

# All cohorts D30 trend
all_cohort_d30 = []
for c in cohort_d30.get("cohorts", []):
    all_cohort_d30.append({
        "cohort": c["cohort"],
        "signups": c["signups"],
        "retention_30d": round(c["retention_30d"] * 100, 2),
    })

# ============================================================
# 2. ACTIVE USER DATA from segmentation
# ============================================================
act_country = raw["segmentation"]["active_country"]["data"]
sig_country = raw["segmentation"]["signups_country"]["data"]
act_platform = raw["segmentation"]["active_platform"]["data"]

# Parse series
def parse_series(seg):
    labels = seg["seriesLabels"]
    series = seg["series"]
    xvals = seg["xValues"]
    result = {}
    for i, lbl in enumerate(labels):
        name = lbl[0] if isinstance(lbl, list) else str(lbl)
        result[name] = dict(zip(xvals, series[i]))
    return result

active_c = parse_series(act_country)
signup_c = parse_series(sig_country)
active_p = parse_series(act_platform)

# Platform split (iOS vs Android DAU)
ios_dau = sum(active_p.get("iOS", {}).values()) / max(len(active_p.get("iOS", {})), 1)
android_dau = sum(active_p.get("Android", {}).values()) / max(len(active_p.get("Android", {})), 1)
total_platform_dau = ios_dau + android_dau

print(f"iOS avg DAU: {ios_dau:.0f} ({ios_dau/total_platform_dau*100:.1f}%)")
print(f"Android avg DAU: {android_dau:.0f} ({android_dau/total_platform_dau*100:.1f}%)")

# ============================================================
# 3. CALIBRATED RETENTION MODEL
# ============================================================
# 
# Ground truth: D30 "Withdraw Completed" = transactional retention
# 
# For "any active" D30:
# - Fintech ratio: any_active / transact ≈ 6-8x
# - But for crypto/fintech in EM with lots of price-checkers: could be 8-12x  
# - Use 7x as base, calibrate per country
#
# Country-specific adjustments:
# - TR: mature market, strong DAU → multiplier ~8x
# - NG: growing market, strong organic → multiplier ~7x  
# - EG: early market, high DAU relative to signups → multiplier ~10x (many price-checkers)
#
# D1/D7/D14 from power-law: R(d) = R(1) * d^(-alpha)
# Typical fintech alpha: 0.30-0.40

COUNTRY_CONFIG = {
    "TR": {"multiplier": 8, "alpha": 0.32, "label": "Turkey"},
    "NG": {"multiplier": 7, "alpha": 0.30, "label": "Nigeria"},
    "EG": {"multiplier": 10, "alpha": 0.35, "label": "Egypt"},
}

retention_curves = {}
for code, cfg in COUNTRY_CONFIG.items():
    d30_w = d30_withdraw[code]["rate"]
    d30_any = min(d30_w * cfg["multiplier"], 0.25)  # cap at 25%
    
    alpha = cfg["alpha"]
    # R(30) = R(1) * 30^(-alpha) => R(1) = R(30) * 30^alpha
    r1 = d30_any * (30 ** alpha)
    r1 = min(r1, 0.50)  # cap at 50% (realistic D1 for fintech)
    
    r7 = r1 * (7 ** (-alpha))
    r14 = r1 * (14 ** (-alpha))
    r30_check = r1 * (30 ** (-alpha))
    
    retention_curves[code] = {
        "label": cfg["label"],
        "d1": round(r1, 4),
        "d7": round(r7, 4),
        "d14": round(r14, 4),
        "d30_any_active": round(r30_check, 4),
        "d30_transact": round(d30_w, 4),
        "signups_recent_4mo": d30_withdraw[code]["signups"],
        "model_params": {"alpha": alpha, "multiplier": cfg["multiplier"]},
    }
    
    print(f"\n{cfg['label']} ({code}):")
    print(f"  D1:  {r1:.1%}  |  D7:  {r7:.1%}  |  D14: {r14:.1%}  |  D30: {r30_check:.1%} (any active)")
    print(f"  D30 transact (Withdraw): {d30_w:.2%}")
    print(f"  Signups (Oct-Jan): {d30_withdraw[code]['signups']}")

# ============================================================
# 4. PLATFORM RETENTION ESTIMATE
# ============================================================
# Signups don't carry platform, but DAU does
# iOS typically has 10-20% higher retention in fintech
# Our split: iOS ~49%, Android ~51% of DAU

ios_retention_boost = 1.15  # iOS typically 15% higher retention
android_baseline = 1.0

# Estimate by adjusting overall retention
platform_retention = {
    "iOS": {
        "dau_share": round(ios_dau / total_platform_dau, 3),
        "avg_dau": round(ios_dau),
        "estimated_d1": None,
        "estimated_d30": None,
        "note": "iOS typically shows 10-20% higher retention in fintech"
    },
    "Android": {
        "dau_share": round(android_dau / total_platform_dau, 3),
        "avg_dau": round(android_dau),
        "estimated_d1": None,
        "estimated_d30": None,
        "note": "Android baseline retention; higher volume, lower per-user retention"
    }
}

# Use blended TR retention as base for platform split
tr_d30 = retention_curves["TR"]["d30_any_active"]
tr_d1 = retention_curves["TR"]["d1"]

# weighted: blended = ios_share * ios_rate + android_share * android_rate
# ios_rate = blended * ios_boost / (ios_share * ios_boost + android_share)
ios_share = ios_dau / total_platform_dau
android_share = android_dau / total_platform_dau
denom = ios_share * ios_retention_boost + android_share * android_baseline

ios_d30 = tr_d30 * ios_retention_boost / denom
android_d30 = tr_d30 * android_baseline / denom
ios_d1 = tr_d1 * ios_retention_boost / denom
android_d1 = tr_d1 * android_baseline / denom

platform_retention["iOS"]["estimated_d1"] = round(ios_d1, 4)
platform_retention["iOS"]["estimated_d30"] = round(ios_d30, 4)
platform_retention["Android"]["estimated_d1"] = round(android_d1, 4)
platform_retention["Android"]["estimated_d30"] = round(android_d30, 4)

print(f"\nPlatform split:")
print(f"  iOS:     D1={ios_d1:.1%}, D30={ios_d30:.1%} (share: {ios_share:.0%})")
print(f"  Android: D1={android_d1:.1%}, D30={android_d30:.1%} (share: {android_share:.0%})")

# ============================================================
# 5. BENCHMARKS
# ============================================================
benchmarks = {
    "fintech_global": {
        "d1": {"p25": 0.20, "p50": 0.30, "p75": 0.42},
        "d7": {"p25": 0.10, "p50": 0.18, "p75": 0.27},
        "d14": {"p25": 0.07, "p50": 0.13, "p75": 0.20},
        "d30": {"p25": 0.05, "p50": 0.10, "p75": 0.18},
    },
    "crypto_wallet": {
        "d1": {"p25": 0.15, "p50": 0.25, "p75": 0.35},
        "d7": {"p25": 0.08, "p50": 0.14, "p75": 0.22},
        "d14": {"p25": 0.05, "p50": 0.10, "p75": 0.17},
        "d30": {"p25": 0.03, "p50": 0.07, "p75": 0.13},
    },
    "source": "Adjust 2024 App Trends, AppsFlyer 2024 Benchmarks, Liftoff Mobile Gaming/Finance 2024"
}

# ============================================================
# 6. SAVE JSON
# ============================================================
output = {
    "generated_at": datetime.now().isoformat(),
    "period": "2025-10 to 2026-01 (D30 cohorts) + 2025-12-22 to 2026-03-22 (DAU)",
    "methodology": {
        "d30_transact": "User-level cohort analysis from Amplitude Export API. First event: 'Cenoa sign-up completed'. Return event: 'Withdraw Completed'. Window: D23-D37 (±7 days around D30).",
        "d1_d7_d14": "Power-law decay model R(d) = R(1) * d^(-alpha), calibrated from D30 ground truth + industry multipliers.",
        "any_active_multiplier": "Country-specific (TR: 8x, NG: 7x, EG: 10x) applied to D30 transact to estimate any-active retention.",
        "platform": "Estimated from DAU split (iOS/Android) with 15% iOS retention premium based on fintech benchmarks.",
        "limitations": [
            "D1/D7/D14 are modeled estimates, not direct measurements",
            "Any-active retention inferred from transact retention * multiplier",
            "Platform retention estimated from DAU share, not user-level cohort",
            "EG sample size is small (416 signups in recent 4 months)",
        ]
    },
    "retention_by_country": retention_curves,
    "platform_retention": platform_retention,
    "d30_monthly_trend": all_cohort_d30,
    "d30_by_country_detail": {
        k: {
            "signups": v["signups"],
            "retained_30d": v["retained"],
            "retention_30d_pct": round(v["rate"] * 100, 2),
        }
        for k, v in d30_withdraw.items()
        if v["signups"] > 20
    },
    "benchmarks": benchmarks,
    "dau_summary": {
        "TR_avg_dau": round(sum(active_c.get("Turkey", {}).values()) / 91),
        "NG_avg_dau": round(sum(active_c.get("Nigeria", {}).values()) / 91),
        "EG_avg_dau": round(sum(active_c.get("Egypt", {}).values()) / 91),
        "total_avg_dau": round(sum(sum(v.values()) for v in active_c.values()) / 91),
        "ios_avg_dau": round(ios_dau),
        "android_avg_dau": round(android_dau),
    },
    "signup_summary": {
        "TR_90d": sum(signup_c.get("Turkey", {}).values()),
        "NG_90d": sum(signup_c.get("Nigeria", {}).values()),
        "EG_90d": sum(signup_c.get("Egypt", {}).values()),
        "total_90d": sum(sum(v.values()) for v in signup_c.values()),
    }
}

with open("data/retention-curves.json", "w") as f:
    json.dump(output, f, indent=2)

print("\n\nSaved data/retention-curves.json")
