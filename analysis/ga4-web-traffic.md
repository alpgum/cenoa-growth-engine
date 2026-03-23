# GA4 Web Traffic Deep-Dive (Sprint [081])

**Generated:** 2026-03-21T01:22:36Z  
**Status:** BLOCKED — `GA4_PROPERTY_ID` not configured.

## What’s missing

We have working **service-account credentials** for Google APIs, but this repo/env currently has **no GA4 property id** configured.

To generate this report:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/Users/alperengumusdograyan/.openclaw/credentials/cenoa-marketingdatawarehouse-82b8600e66d6.json
export GA4_PROPERTY_ID=<numeric_ga4_property_id>
source ~/.openclaw/venv/bin/activate
python3 projects/cenoa-performance-marketing/scripts/ga4_web_traffic_deepdive.py
```

Once `GA4_PROPERTY_ID` is set, the script will populate:
1) Sessions by source/medium (top 20)
2) Landing page performance: sessions + engagement (bounce proxy)
3) CTA click proxy + CTA click rate by landing page (if events exist)
4) Consistency check vs Looker-noted top pages

---

## Looker-noted “top pages” (from `analysis/lp-cta-optimization.md`)

| path | sessions_hint |
|---|---|
| /pakistan-waitlist-v2 | ~1,800 |
| / | ~2,500 |
| /blog/accepted-proof | ~600 |

---

## Instrumentation expectation for CTA clicks

If GA4 does **not** currently track CTA clicks, recommended event:

- Event name: `cta_click`
- Recommended parameters:
  - `cta_id` (e.g., `cta_header_download`, `cta_hero_download`)
  - `placement` (header/hero/sticky/footer)
  - `destination` (ios/android/web)
  - `landing_page` (page path)
  - `variant` (if running LP tests)

This enables reliable CTA click rate by landing page.


---

> ⚠️ **Attribution caveat:** Web campaigns (Meta/Google → cenoa.com → app store) may appear as "Organic" or "(none)" due to broken web→app attribution. Estimated correction factor: ~6.9×. See [attribution-reconciliation.md](attribution-reconciliation.md) for details.
