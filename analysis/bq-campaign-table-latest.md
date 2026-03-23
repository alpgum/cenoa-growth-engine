# BigQuery Campaign Table (Latest 6 Days; max 7)

**Country:** TR (table is TR-only)
**Date range:** 2026-02-25 → 2026-03-02 (inclusive)
**Generated at:** 2026-03-23T00:47:05.985489+03:00

## BigQuery coverage
- daily_installs_campaign_tr: min=2026-02-25, max=2026-03-02, distinct days=6

## Media source totals (installs)

| media_source | installs |
|---|---|
| appnext_int | 10616 |
| byteboost2_int | 1840 |
| zzgtechltmqk_int | 576 |
| Apple Search Ads | 320 |
| cenoa.com | 152 |
| Eihracat Yıldızları | 120 |
| cenoacomtr | 112 |
| googleadwords_int | 64 |
| Social_instagram | 40 |
| af_app_invites | 32 |
| Facebook Ads | 8 |
| easyinventory | 8 |

## Top 24 campaigns by installs

| rank | media_source | campaign | installs | cost_usd | cpi_usd |
|---|---|---|---|---|---|
| 1 | appnext_int | Cenoa_CPI_UA_TR | 10616 |  |  |
| 2 | byteboost2_int | 890668 | 1120 |  |  |
| 3 | byteboost2_int | 890670 | 720 |  |  |
| 4 | zzgtechltmqk_int | TR_Meta_web2app_MIX_CVR_Android_AddToCart_012126 | 344 |  |  |
| 5 | cenoa.com | cenoa.com homepage | 152 |  |  |
| 6 | Apple Search Ads | tr_asa_appinstall_brand_exact_all_02.06.2025 | 152 |  |  |
| 7 | Eihracat Yıldızları | E-ihracat Yıldızları Home Page | 120 |  |  |
| 8 | zzgtechltmqk_int | TR_Meta_web2app_MIX_RTGT_AddPaymentInfo_022726_Images | 112 |  |  |
| 9 | cenoacomtr | cenoa.comtr homepage | 112 |  |  |
| 10 | Apple Search Ads | TR-Discovery-24.10.2025 | 72 |  |  |
| 11 | zzgtechltmqk_int | TR_Meta_web2app_MIX_RTGT_AddToCart_022726_Images | 56 |  |  |
| 12 | googleadwords_int | Google // Cenoa // Search // TR // Pure Brand | 48 |  |  |
| 13 | Apple Search Ads | tr_asa_appinstall_brand_broad_all_02.06.2025 | 48 |  |  |
| 14 | Social_instagram | Instagram | 40 |  |  |
| 15 | af_app_invites | Invite a Friend | 32 |  |  |
| 16 | zzgtechltmqk_int | TR_Meta_web2app_MIX_CVR_ALL_AddToCart_022326_ExcVisitors | 32 |  |  |
| 17 | Apple Search Ads | tr_asa_appinstall_competitor_all_02.06.2025 | 24 |  |  |
| 18 | Apple Search Ads | tr_asa_appinstall_generic_all_02.06.2025 | 24 |  |  |
| 19 | zzgtechltmqk_int | TR_Meta_web2app_MIX_Leads_ALL_012926 | 16 |  |  |
| 20 | zzgtechltmqk_int | none | 16 |  |  |
| 21 | googleadwords_int | Cenoa // Search // TR // Freelancer // Platform | 8 |  |  |
| 22 | googleadwords_int | Google // Cenoa // Pmax // TR // E-ihracat // Architect // KYC_Start | 8 |  |  |
| 23 | Facebook Ads | TR_Meta_App_MIX_CVR_iOS_AddToCart_022526_ExcAppUsers | 8 |  |  |
| 24 | easyinventory | easyinventory-payin | 8 |  |  |

## CPI join (Sheets)

Tried to detect campaign-level cost/spend in `data/sheets-trafik-canavari.json`, but the synced export appears aggregated (no campaign dimension). So `cost_usd` / `cpi_usd` are currently **null** in the JSON.

## How to reproduce

```bash
source ~/.openclaw/venv/bin/activate
GOOGLE_APPLICATION_CREDENTIALS=~/.openclaw/credentials/cenoa-marketingdatawarehouse-82b8600e66d6.json \
  python3 projects/cenoa-performance-marketing/scripts/bq_campaign_table_latest.py
```
