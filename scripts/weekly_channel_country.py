#!/usr/bin/env python3
"""
S2-001: Weekly channel × country breakdown
Pulls segmentation from Amplitude for two periods, calculates WoW deltas.

Date Convention (S3-014):
  - Weekly = ISO week: Monday 00:00 UTC to Sunday 23:59 UTC
  - MTD = 1st of month 00:00 UTC to current day 23:59 UTC
  - All Amplitude API calls use YYYYMMDD format
  - Default: last complete ISO week vs prior ISO week
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DATA_DIR = PROJECT_DIR / "data"
ANALYSIS_DIR = PROJECT_DIR / "analysis"

API_URL = "https://amplitude.com/api/2/events/segmentation"

# Compute ISO week boundaries dynamically
_today = datetime.utcnow()
_last_sunday = _today - timedelta(days=_today.weekday() + 1)
_curr_monday = _last_sunday - timedelta(days=6)
_prev_sunday = _curr_monday - timedelta(days=1)
_prev_monday = _prev_sunday - timedelta(days=6)

CURRENT = (_curr_monday.strftime("%Y%m%d"), _last_sunday.strftime("%Y%m%d"))
PREVIOUS = (_prev_monday.strftime("%Y%m%d"), _prev_sunday.strftime("%Y%m%d"))

CHANNEL_MAP = {
    "googleadwords_int": "Google",
    "Google Ads ACI": "Google",

    # Meta
    "Facebook Ads": "Meta",
    "restricted": "Meta",
    "Social_instagram": "Meta",  # AppsFlyer sometimes labels Instagram placements separately

    # Apple
    "Apple Search Ads": "ASA",

    # Google via 3rd-party buying platform
    # NOTE: 'Architect' is a Google Ads buying/automation platform; traffic should be treated as Google,
    # not lumped into 'Other'.
    "Architect": "Google",

    # Other paid networks
    "appnext_int": "Appnext",
    "bytedanceglobal_int": "TikTok",
    "tiktokglobal_int": "TikTok",

    # Referral / owned
    "af_app_invites": "Referral",
    "referral": "Referral",
    "Braze_refer-a-friend": "Referral",

    # Organic / direct / unattributed
    "organic": "Organic",
    "Organic": "Organic",
    "(none)": "Organic",
    "": "Organic",
    "Web Onboarding": "Organic",
    "cenoa.com": "Organic",
    "cenoacomtr": "Organic",
}

# Known ad network sources that are clearly "Other" paid
OTHER_PAID = {
    "zzgtechltmqk_int",
    "byteboost2_int",
    "Auto Pilot Tool",
    "Egypt LTV Test",
    "Eihracat Yıldızları",
}

# Guardrail: prevent overlaps that would cause confusing precedence / double-classification.
_overlap = set(CHANNEL_MAP).intersection(OTHER_PAID)
if _overlap:
    raise RuntimeError(f"Channel mapping overlap between CHANNEL_MAP and OTHER_PAID: {sorted(_overlap)}")

def classify_google_campaign(campaign):
    if not campaign:
        return "Google Search"
    c = campaign.lower()
    if "pmax" in c or "performance max" in c:
        return "Google Pmax"
    if "brand" in c:
        return "Google Brand"
    return "Google Search"

def classify_meta_campaign(campaign):
    if not campaign:
        return "Meta App"
    c = campaign.lower()
    if "w2a" in c or "web" in c or "web2app" in c:
        return "Meta W2A"
    return "Meta App"

def get_channel(media_source, campaign=""):
    ms = (media_source or "").strip()
    if ms in OTHER_PAID:
        return "Other"
    base = CHANNEL_MAP.get(ms, None)
    if base == "Google":
        return classify_google_campaign(campaign)
    if base == "Meta":
        return classify_meta_campaign(campaign)
    if base is not None:
        return base
    if not ms or ms in ("(none)", "None", "null"):
        return "Organic"
    return "Other"

COUNTRY_NAMES = {
    "Turkey": "TR", "Türkiye": "TR", "TR": "TR",
    "Nigeria": "NG", "NG": "NG",
    "Egypt": "EG", "EG": "EG",
    "Pakistan": "PK", "PK": "PK",
}

def get_country_bucket(country):
    if not country:
        return "Other"
    c = country.strip()
    return COUNTRY_NAMES.get(c, "Other")


def load_credentials():
    env_file = Path.home() / ".openclaw" / "credentials" / "amplitude.env"
    creds = {}
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                creds[k.strip()] = v.strip()
    return creds["AMPLITUDE_API_KEY"], creds["AMPLITUDE_SECRET_KEY"]


def fetch_segmentation(api_key, secret_key, event_type, group_by_props, start, end, metric="uniques"):
    e_param = json.dumps({
        "event_type": event_type,
        "group_by": group_by_props
    })
    cmd = [
        "curl", "-s", "-u", f"{api_key}:{secret_key}",
        "--data-urlencode", f"e={e_param}",
        "--data-urlencode", f"m={metric}",
        "--data-urlencode", f"start={start}",
        "--data-urlencode", f"end={end}",
        "-G", API_URL,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR curl: {event_type}: {result.stderr}", file=sys.stderr)
        return None
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"  ERROR JSON: {event_type}: {result.stdout[:300]}", file=sys.stderr)
        return None
    if "data" not in data:
        print(f"  WARN no data: {event_type}: {json.dumps(data)[:300]}", file=sys.stderr)
        return None
    return data["data"]


def parse_segmentation(data):
    """Parse Amplitude segmentation response.
    Labels format: [0, 'val'] or [0, 'val1; val2'] for multi-group
    Collapsed format: [{'setId': '', 'value': N}]
    Returns list of (group_values_list, total_value).
    """
    results = []
    labels = data.get("seriesLabels", [])
    collapsed = data.get("seriesCollapsed", [])

    for i, label_entry in enumerate(labels):
        # Extract group values from label
        # label_entry is like [0, 'Organic'] or [0, 'Organic; Nigeria']
        if isinstance(label_entry, list) and len(label_entry) >= 2:
            raw_label = str(label_entry[1])
            group_values = [v.strip() for v in raw_label.split(";")]
        elif isinstance(label_entry, (int, float)):
            group_values = []
        else:
            group_values = [str(label_entry)]

        # Extract value from collapsed
        val = 0
        if i < len(collapsed):
            c = collapsed[i]
            if isinstance(c, list) and len(c) > 0:
                if isinstance(c[0], dict):
                    val = c[0].get("value", 0)
                elif isinstance(c[0], (int, float)):
                    val = c[0]
            elif isinstance(c, dict):
                val = c.get("value", 0)
            elif isinstance(c, (int, float)):
                val = c

        results.append((group_values, int(val)))

    return results


def aggregate_by_ms_and_country(parsed):
    """Aggregate by channel × country from (media_source; country) pairs."""
    agg = defaultdict(int)
    for group_values, val in parsed:
        if len(group_values) >= 2:
            ms, country = group_values[0], group_values[1]
        elif len(group_values) == 1:
            ms, country = group_values[0], ""
        else:
            ms, country = "", ""
        channel = get_channel(ms)
        cb = get_country_bucket(country)
        agg[(channel, cb)] += val
    return dict(agg)


def aggregate_by_country(parsed):
    """Aggregate by country only."""
    agg = defaultdict(int)
    for group_values, val in parsed:
        country = group_values[0] if group_values else ""
        cb = get_country_bucket(country)
        agg[cb] += val
    return dict(agg)


def calc_wow(current, previous):
    all_keys = set(list(current.keys()) + list(previous.keys()))
    result = {}
    for k in all_keys:
        c = current.get(k, 0)
        p = previous.get(k, 0)
        delta = c - p
        pct = (delta / p * 100) if p else (100.0 if c > 0 else 0.0)
        result[k] = {"current": c, "previous": p, "delta": delta, "delta_pct": round(pct, 1)}
    return result


def main():
    api_key, secret_key = load_credentials()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

    events_config = [
        {
            "name": "install",
            "event_type": "[AppsFlyer] Install",
            "group_by": [
                {"type": "user", "value": "gp:[AppsFlyer] media source"},
                {"type": "user", "value": "country"}
            ],
            "aggregator": "ms_country",
        },
        {
            "name": "signup",
            "event_type": "Cenoa sign-up completed",
            "group_by": [
                {"type": "user", "value": "gp:[AppsFlyer] media source"},
                {"type": "user", "value": "country"}
            ],
            "aggregator": "ms_country",
        },
        {
            "name": "kyc_submit",
            "event_type": "Bridgexyz KYC Component: Submit clicked",
            "group_by": [{"type": "user", "value": "country"}],
            "aggregator": "country",
        },
        {
            "name": "virtual_account",
            "event_type": "Virtual account opened",
            "group_by": [{"type": "user", "value": "country"}],
            "aggregator": "country",
        },
        {
            "name": "new_active",
            "event_type": "Withdraw Completed",
            "group_by": [{"type": "user", "value": "country"}],
            "aggregator": "country",
        },
    ]

    all_data = {}

    for ec in events_config:
        name = ec["name"]
        print(f"Fetching {name} ({ec['event_type']})...")

        data_cur = fetch_segmentation(api_key, secret_key, ec["event_type"], ec["group_by"], CURRENT[0], CURRENT[1])
        data_prev = fetch_segmentation(api_key, secret_key, ec["event_type"], ec["group_by"], PREVIOUS[0], PREVIOUS[1])

        if data_cur is None:
            print(f"  Retrying {name} with totals metric...")
            data_cur = fetch_segmentation(api_key, secret_key, ec["event_type"], ec["group_by"], CURRENT[0], CURRENT[1], metric="totals")
            data_prev = fetch_segmentation(api_key, secret_key, ec["event_type"], ec["group_by"], PREVIOUS[0], PREVIOUS[1], metric="totals")

        if data_cur is None:
            print(f"  SKIP {name}: no data", file=sys.stderr)
            all_data[name] = {"error": "no data"}
            continue

        parsed_cur = parse_segmentation(data_cur)
        parsed_prev = parse_segmentation(data_prev) if data_prev else []

        print(f"  Parsed {len(parsed_cur)} segments current, {len(parsed_prev)} segments previous")

        if ec["aggregator"] == "ms_country":
            agg_cur = aggregate_by_ms_and_country(parsed_cur)
            agg_prev = aggregate_by_ms_and_country(parsed_prev)
        else:
            agg_cur = aggregate_by_country(parsed_cur)
            agg_prev = aggregate_by_country(parsed_prev)

        wow = calc_wow(agg_cur, agg_prev)

        # Convert tuple keys to strings for JSON
        def key_str(k):
            return " | ".join(k) if isinstance(k, tuple) else str(k)

        all_data[name] = {
            "event_type": ec["event_type"],
            "aggregator": ec["aggregator"],
            "current_period": f"{CURRENT[0]}-{CURRENT[1]}",
            "previous_period": f"{PREVIOUS[0]}-{PREVIOUS[1]}",
            "wow": {key_str(k): v for k, v in wow.items()},
            "current_totals": {key_str(k): v for k, v in agg_cur.items()},
            "previous_totals": {key_str(k): v for k, v in agg_prev.items()},
        }
        print(f"  ✓ {name}: {len(agg_cur)} buckets current, {len(agg_prev)} buckets previous")

    # Save JSON
    out_json = DATA_DIR / f"weekly-channel-country-{CURRENT[1]}.json"
    with open(out_json, "w") as f:
        json.dump(all_data, f, indent=2, default=str)
    print(f"\nSaved: {out_json}")

    generate_analysis(all_data)


CHANNELS_ORDER = ["Google Pmax", "Google Search", "Google Brand", "Meta App", "Meta W2A", "ASA", "Appnext", "TikTok", "Organic", "Referral", "Other"]
COUNTRIES_ORDER = ["TR", "NG", "EG", "PK", "Other"]


def generate_analysis(all_data):
    lines = []
    # Dynamic header from ISO week boundaries
    curr_start_dt = datetime.strptime(CURRENT[0], "%Y%m%d")
    curr_end_dt = datetime.strptime(CURRENT[1], "%Y%m%d")
    prev_start_dt = datetime.strptime(PREVIOUS[0], "%Y%m%d")
    prev_end_dt = datetime.strptime(PREVIOUS[1], "%Y%m%d")
    lines.append(f"# Weekly Channel × Country Breakdown: {curr_start_dt.strftime('%b %d')}–{curr_end_dt.strftime('%d')} vs {prev_start_dt.strftime('%b %d')}–{prev_end_dt.strftime('%d')}")
    lines.append("")
    lines.append(f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## ⚠️ Attribution Caveats")
    lines.append("")
    lines.append("- **Web→App flow inflates Organic/(none):** Users who discover Cenoa via web ads but install via app store are attributed as Organic in AppsFlyer. Estimated correction factor: **~6.9×** (Organic installs may be ~6.9× over-reported vs true organic).")
    lines.append("- **TRUE CAC definition:** Cost per **new_active** (first withdrawal completed), NOT cost per virtual account opened. This reflects genuine activated users.")
    lines.append("- Country-level data for KYC/Virtual Account/Withdraw shows country only (no channel attribution) — these events occur post-install and AppsFlyer media source propagation varies.")
    lines.append("")
    lines.append("---")
    lines.append("")

    event_labels = {
        "install": "📲 Installs ([AppsFlyer] Install)",
        "signup": "✍️ Sign-ups (Cenoa sign-up completed)",
        "kyc_submit": "🪪 KYC Submissions (Bridgexyz KYC Component: Submit clicked)",
        "virtual_account": "🏦 Virtual Accounts Opened",
        "new_active": "💸 New Actives (Withdraw Completed — proxy for activated users)",
    }

    for event_key, label in event_labels.items():
        lines.append(f"## {label}")
        lines.append("")

        ed = all_data.get(event_key)
        if not ed or "error" in ed:
            lines.append("- ⚠️ No data available for this event")
            lines.append("")
            continue

        wow = ed.get("wow", {})
        aggregator = ed.get("aggregator", "country")

        if aggregator == "ms_country":
            channel_totals_cur = defaultdict(int)
            channel_totals_prev = defaultdict(int)
            for key_str, vals in wow.items():
                parts = key_str.split(" | ")
                ch = parts[0] if parts else "Other"
                channel_totals_cur[ch] += vals["current"]
                channel_totals_prev[ch] += vals["previous"]

            grand_cur = sum(channel_totals_cur.values())
            grand_prev = sum(channel_totals_prev.values())
            grand_delta = grand_cur - grand_prev
            grand_pct = (grand_delta / grand_prev * 100) if grand_prev else 0

            lines.append(f"**Total: {grand_cur:,}** (prev: {grand_prev:,}, {'+' if grand_delta >= 0 else ''}{grand_delta:,} / {'+' if grand_pct >= 0 else ''}{grand_pct:.1f}%)")
            lines.append("")

            for ch in CHANNELS_ORDER:
                c = channel_totals_cur.get(ch, 0)
                p = channel_totals_prev.get(ch, 0)
                if c == 0 and p == 0:
                    continue
                d = c - p
                pct = (d / p * 100) if p else (100.0 if c > 0 else 0.0)
                arrow = "🟢" if d > 0 else ("🔴" if d < 0 else "⚪")
                lines.append(f"- **{ch}:** {c:,} (prev {p:,}) {arrow} {'+' if d >= 0 else ''}{d:,} ({'+' if pct >= 0 else ''}{pct:.1f}%)")

                for co in COUNTRIES_ORDER:
                    key_str = f"{ch} | {co}"
                    if key_str in wow:
                        v = wow[key_str]
                        if v["current"] == 0 and v["previous"] == 0:
                            continue
                        ca = "↑" if v["delta"] > 0 else ("↓" if v["delta"] < 0 else "→")
                        lines.append(f"  - {co}: {v['current']:,} (prev {v['previous']:,}) {ca} {'+' if v['delta'] >= 0 else ''}{v['delta']:,} ({'+' if v['delta_pct'] >= 0 else ''}{v['delta_pct']:.1f}%)")

            lines.append("")
        else:
            grand_cur = sum(v["current"] for v in wow.values())
            grand_prev = sum(v["previous"] for v in wow.values())
            grand_delta = grand_cur - grand_prev
            grand_pct = (grand_delta / grand_prev * 100) if grand_prev else 0

            lines.append(f"**Total: {grand_cur:,}** (prev: {grand_prev:,}, {'+' if grand_delta >= 0 else ''}{grand_delta:,} / {'+' if grand_pct >= 0 else ''}{grand_pct:.1f}%)")
            lines.append("")

            for co in COUNTRIES_ORDER:
                if co in wow:
                    v = wow[co]
                    if v["current"] == 0 and v["previous"] == 0:
                        continue
                    arrow = "🟢" if v["delta"] > 0 else ("🔴" if v["delta"] < 0 else "⚪")
                    lines.append(f"- **{co}:** {v['current']:,} (prev {v['previous']:,}) {arrow} {'+' if v['delta'] >= 0 else ''}{v['delta']:,} ({'+' if v['delta_pct'] >= 0 else ''}{v['delta_pct']:.1f}%)")

            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Funnel Conversion Rates (Current Week)")
    lines.append("")

    def total_current(key):
        d = all_data.get(key, {})
        if "error" in d:
            return 0
        return sum(v["current"] for v in d.get("wow", {}).values())

    install_total = total_current("install")
    signup_total = total_current("signup")
    kyc_total = total_current("kyc_submit")
    va_total = total_current("virtual_account")
    na_total = total_current("new_active")

    if install_total:
        lines.append(f"- Install → Sign-up: {signup_total:,}/{install_total:,} = {signup_total/install_total*100:.1f}%")
    if signup_total:
        lines.append(f"- Sign-up → KYC Submit: {kyc_total:,}/{signup_total:,} = {kyc_total/signup_total*100:.1f}%")
    if kyc_total:
        lines.append(f"- KYC Submit → Virtual Account: {va_total:,}/{kyc_total:,} = {va_total/kyc_total*100:.1f}%")
    if va_total:
        lines.append(f"- Virtual Account → New Active: {na_total:,}/{va_total:,} = {na_total/va_total*100:.1f}%")
    if install_total:
        lines.append(f"- **Install → New Active (end-to-end): {na_total:,}/{install_total:,} = {na_total/install_total*100:.2f}%**")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("_Data source: Amplitude Segmentation API (uniques). Channel attribution via AppsFlyer media source property._")

    out_md = ANALYSIS_DIR / "weekly-channel-country-mar15-21.md"
    with open(out_md, "w") as f:
        f.write("\n".join(lines))
    print(f"Saved: {out_md}")


if __name__ == "__main__":
    main()
