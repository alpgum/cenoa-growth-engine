# ⛔ PAUSE MEMO: Google Ads Demand Gen Retargeting

**Date:** 2026-03-22  
**Priority:** IMMEDIATE  
**Action required:** 5 minutes in Google Ads console

---

## Recommendation

**Pause the Google Ads Demand Gen Retargeting campaign IMMEDIATELY.**

Zero installs over ~5 months of spend. No diagnostic is needed before pausing — pause first, investigate second.

---

## Campaign Details

| Field | Value |
|---|---|
| Campaign name | **TR-Discovery-24.10.2025** |
| Campaign type | Demand Gen (Retargeting) |
| Platform | Google Ads |
| Market | Turkey (TR) |
| Live since | ~October 24, 2025 |

---

## Evidence

| Metric | Value |
|---|---|
| Mar 14–20 clicks | 1,627 |
| Mar 14–20 installs (AppsFlyer) | **0** |
| Mar 14–20 spend | ₺19,620 (~$560) |
| Cost per install | **∞** |
| Campaign age | ~5 months |
| Estimated total waste | **~₺392,000 (~$11,200)** |

For comparison: during the same week, Google Pmax delivered **27 installs** at ~$30 CPI and Search delivered **27 installs** at ~$29 CPI — with similar spend levels.

---

## Root Cause Hypotheses (Top 3)

1. **Retargeting existing app users** (HIGH probability) — The audience likely consists of people who already installed the app. No new install event fires, so spend is wasted on re-engaging existing users with no measurable outcome.

2. **Wrong conversion action configured** (HIGH probability) — Campaign may be optimizing toward a web conversion (page visit) rather than an app install event. Google happily optimizes for clicks that never reach the app store.

3. **Broken attribution chain** (MEDIUM probability) — Landing page → App Store redirect may break AppsFlyer click-through attribution. Deep links may not be configured, so users land on a generic web page and manually search for the app.

---

## Action Plan

### Step 1 — Pause campaign today ⏱️ 5 min

Go to Google Ads → Campaigns → **TR-Discovery-24.10.2025** → Pause.

### Step 2 — Reallocate freed budget

Redirect the ₺19,620/week to proven channels:

| Destination | Suggested allocation | Rationale |
|---|---|---|
| Google Pmax (scale up) | ₺14,000/wk | Currently delivering installs at ~₺1,050 CPI; scaling 40% is low-risk |
| Apple Search Ads (scale up) | ₺5,620/wk | Proven install channel, incremental budget |

### Step 3 — Optional diagnostics (if considering relaunch later)

Before relaunching, check these in Google Ads console:

1. **Conversion action assignment** — Is the campaign tracking app installs or web page visits?
2. **"All conversions" column** — Does the campaign show ANY conversions at all (even view-through)?
3. **Audience definition** — Are existing app installers excluded? What's the recency window?
4. **Landing page destination** — Does the ad click go to app store, web page, or deep link?
5. **AppsFlyer retargeting dashboard** — Any re-engagements attributed to Google?

If diagnostics show some value, relaunch at ₺5,000/wk with a 2-week trial. Kill permanently if CPI > ₺500.

---

## Expected Impact

| Metric | Before (current) | After (pause) |
|---|---|---|
| Google weekly spend (TR) | ~₺56,000 | ~₺36,380 |
| Google weekly installs (TR) | 54 | 54 (unchanged — campaign produces 0) |
| **Google blended CPI (TR)** | **~₺1,037** | **~₺674 (35% improvement)** |
| Freed budget → new installs (Pmax) | — | ~19 additional installs/wk |
| **New total installs** | **54/wk** | **~73/wk (+35%)** |

---

## Prevention

To avoid similar waste in the future:

- **Weekly alert:** Flag any campaign with spend > ₺5,000 and 0 conversions
- **Google Ads automated rule:** Pause any campaign with spend > ₺10,000 and conversions = 0 in trailing 7 days
- **Monthly campaign-level CPI review** (not just channel-level aggregates)

---

*This memo can be forwarded directly to whoever manages Google Ads. The only action needed is to pause the campaign — everything else is optional follow-up.*
