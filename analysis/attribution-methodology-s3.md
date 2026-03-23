# S3 Attribution Methodology (Channel × Country)

**Owner:** Performance Marketing (S3)

This doc explains how we bucket Amplitude installs/signups into **named channels** (Google / Meta / ASA / etc.) and why the prior **“Other | TR”** bucket could be misleading (and appear to “double count” vs platform-reported campaign totals).

---

## 1) Data source & query

**Source:** Amplitude Event Segmentation API

**Primary events (weekly script):**
- `[AppsFlyer] Install`
- `Cenoa sign-up completed`

**Grouping (weekly channel×country):**
- `gp:[AppsFlyer] media source` (AppsFlyer media_source surfaced in Amplitude)
- `country`

**Script:**
- `projects/cenoa-performance-marketing/scripts/weekly_channel_country.py`
- (Backfill wrapper) `projects/cenoa-performance-marketing/scripts/weekly_backfill.py`

> Note: The scripts support campaign-based sub-bucketing (e.g., Google Pmax vs Search; Meta App vs W2A), **but the weekly channel×country rollup currently groups only by media source + country**, so campaign strings are usually not available at bucketing time. In that case, Google defaults to **Google Search** and Meta defaults to **Meta App**.

---

## 2) Channel bucketing rules (media_source → channel)

Bucketing happens in `get_channel(media_source, campaign="")`.

### 2.1 Direct mapping table

| AppsFlyer media_source (Amplitude) | Bucketed channel |
|---|---|
| `googleadwords_int` | Google → (defaults to **Google Search** if campaign not provided) |
| `Google Ads ACI` | Google → (defaults to **Google Search**) |
| `Architect` | Google → (defaults to **Google Search**) |
| `Facebook Ads` | Meta → (defaults to **Meta App**) |
| `restricted` | Meta → (defaults to **Meta App**) |
| `Social_instagram` | Meta → (defaults to **Meta App**) |
| `Apple Search Ads` | ASA |
| `appnext_int` | Appnext |
| `tiktokglobal_int`, `bytedanceglobal_int` | TikTok |
| `af_app_invites`, `referral`, `Braze_refer-a-friend` | Referral |
| `Organic`, `organic`, `(none)`, empty string, `Web Onboarding`, `cenoa.com`, `cenoacomtr` | Organic |

### 2.2 “Other” definition

A media_source is bucketed as **Other** if:
1) It is in the explicit `OTHER_PAID` allowlist of non-core paid sources, **or**
2) It is not recognized in `CHANNEL_MAP` (fallback).

Current `OTHER_PAID` list includes:
- `zzgtechltmqk_int`
- `byteboost2_int`
- `Auto Pilot Tool`
- `Egypt LTV Test`
- `Eihracat Yıldızları`

### 2.3 Guardrail (prevents ambiguous precedence)

Both scripts now include a runtime check:

- `CHANNEL_MAP ∩ OTHER_PAID` must be empty

This prevents a subtle bug where a media_source could be mapped to a named channel *and* also forced into Other, depending on precedence.

---

## 3) What we found (S3-013)

### 3.1 Why “Other | TR” looked risky

The concern was that **“Other | TR” (~157 installs)** might include Meta or Google traffic **already counted** under separately-tagged Meta/Google campaigns.

Within **Amplitude channel bucketing itself**, installs are not double-counted: each install has exactly one `media_source`, and we assign exactly one channel bucket.

However, two things made **“Other”** confusing:

1) **`Architect` was being forced into “Other”**
   - `media_source = Architect` is a Google Ads buying/automation platform.
   - Those installs should roll up under Google, not Other.
   - This could make “Other” appear inflated and overlap conceptually with “Google” when reconciling to platform reports.

2) **Instagram/Meta labeling**
   - `Social_instagram` appeared as a media_source in Amplitude breakdowns.
   - Previously it was treated as “Other”; it is now treated as **Meta**.

### 3.2 Fix applied

- Reclassified **`Architect`** from Other → **Google**
- Reclassified **`Social_instagram`** from Other → **Meta**
- Added an overlap guardrail to prevent future ambiguous mappings.

---

## 4) How to interpret channel totals vs ad platform totals (avoid “double counting”)

Amplitude channel totals (via AppsFlyer media_source) and ad platform dashboards (Meta/Google/ASA) are **different measurement systems**:

- **Amplitude**: counts attributed installs/events as captured in product analytics, using AppsFlyer fields forwarded into Amplitude.
- **Ad platforms**: report installs/conversions per their own attribution models (SKAN, view-through, modeled conversions, etc.).

✅ **Do:** Compare trends and sanity-check ranges.

❌ **Don’t:** Add “Amplitude Other | TR” to “Meta campaign installs” from platform dashboards as if they were disjoint sources. They are not guaranteed to be disjoint.

---

## 5) Practical checklist for investigating a suspicious “Other” bucket

1) Pull top media_sources for the week (`amplitude_attribution.py` or segmentation API)
2) Confirm whether each media_source is:
   - a core channel (Google/Meta/ASA/TikTok/Appnext/Referral/Organic)
   - a known “Other paid network”
   - a new/unknown string (should be added to mapping)
3) If a media_source is actually a known channel (e.g., a buying platform like Architect), **map it explicitly**.

---

## 6) References

- Weekly script: `scripts/weekly_channel_country.py`
- Backfill: `scripts/weekly_backfill.py`
- Example raw breakdown (Mar 14–20): `data/attribution-breakdown-20260320.json`
- Funnel note: `analysis/attribution-funnel.md`

---

## 7) Spend in Cortex: source of truth & reconciliation (S3-031)

This doc is primarily about **event attribution** (installs/signups). Spend is a separate pipeline:

- **Source of truth for weekly spend** (both `countrySpend[]` and `channelPerformance[]` in `projects/cenoa-cortex/data.json`) is **Google Sheets → `sheets-cac-analysis.json`**.
- `kpi_auto_update.py` builds `channelPerformance[]` **directly from the same Sheets period used for `countrySpend[]`**, so totals reconcile.
- If a country has weekly spend in Sheets but the **channel split is missing/incomplete**, the residual is written as a **`"Unallocated"`** channel row so:

  `sum(channelPerformance.spend) == sum(countrySpend.weeklySpend)` (within rounding)
