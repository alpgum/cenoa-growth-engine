# BigQuery — Campaign Trends (Last 30 Days)

Generated: `2026-03-21T01:23:05.541613+00:00`

## Data coverage & caveats

- Source tables:
  - `cenoa-marketingdatawarehouse.marketing_appsflyer.daily_installs_campaign_tr` (campaign-level, TR-only, daily)
  - `cenoa-marketingdatawarehouse.marketing_appsflyer.weekly_combined_totals` (country/platform/channel, weekly)
- Daily table available range: **2026-02-25 → 2026-03-02** (**6 distinct days**)
- Requested window = last 30 days; effective window used = **2026-02-25 → 2026-03-02** (limited by data availability)

- Week-over-week for campaigns uses ISO weeks: **2026-W10 vs 2026-W09** (note: current week may be partial).



## 1) Top campaigns by installs (Top 20) + WoW trend

| Campaign | Media source | Installs (window) | Installs (2026-W10) | Installs (2026-W09) | WoW % | Trend | Platform split |
|---|---|---|---|---|---|---|---|
| Cenoa_CPI_UA_TR | appnext_int | 10616 | 856 | 9760 | -91.2% | DOWN | android:10616 |
| 890668 | byteboost2_int | 1120 | 48 | 1072 | -95.5% | DOWN | android:920, ios:200 |
| 890670 | byteboost2_int | 720 | 48 | 672 | -92.9% | DOWN | android:600, ios:120 |
| TR_Meta_web2app_MIX_CVR_Android_AddToCart_012126 | zzgtechltmqk_int | 344 | 24 | 320 | -92.5% | DOWN | android:344 |
| cenoa.com homepage | cenoa.com | 152 | 24 | 128 | -81.2% | DOWN | android:120, ios:32 |
| tr_asa_appinstall_brand_exact_all_02.06.2025 | Apple Search Ads | 152 | 0 | 152 | -100.0% | DOWN | ios:152 |
| E-ihracat Yıldızları Home Page | Eihracat Yıldızları | 120 | 24 | 96 | -75.0% | DOWN | android:96, ios:24 |
| TR_Meta_web2app_MIX_RTGT_AddPaymentInfo_022726_Images | zzgtechltmqk_int | 112 | 8 | 104 | -92.3% | DOWN | android:112 |
| cenoa.comtr homepage | cenoacomtr | 112 | 0 | 112 | -100.0% | DOWN | android:80, ios:32 |
| TR-Discovery-24.10.2025 | Apple Search Ads | 72 | 0 | 72 | -100.0% | DOWN | ios:72 |
| TR_Meta_web2app_MIX_RTGT_AddToCart_022726_Images | zzgtechltmqk_int | 56 | 40 | 16 | 150.0% | UP | android:56 |
| Google // Cenoa // Search // TR // Pure Brand | googleadwords_int | 48 | 0 | 48 | -100.0% | DOWN | android:40, ios:8 |
| tr_asa_appinstall_brand_broad_all_02.06.2025 | Apple Search Ads | 48 | 0 | 48 | -100.0% | DOWN | ios:48 |
| Instagram | Social_instagram | 40 | 0 | 40 | -100.0% | DOWN | android:32, ios:8 |
| Invite a Friend | af_app_invites | 32 | 0 | 32 | -100.0% | DOWN | android:16, ios:16 |
| TR_Meta_web2app_MIX_CVR_ALL_AddToCart_022326_ExcVisitors | zzgtechltmqk_int | 32 | 0 | 32 | -100.0% | DOWN | android:32 |
| tr_asa_appinstall_competitor_all_02.06.2025 | Apple Search Ads | 24 | 0 | 24 | -100.0% | DOWN | ios:24 |
| tr_asa_appinstall_generic_all_02.06.2025 | Apple Search Ads | 24 | 0 | 24 | -100.0% | DOWN | ios:24 |
| TR_Meta_web2app_MIX_Leads_ALL_012926 | zzgtechltmqk_int | 16 | 0 | 16 | -100.0% | DOWN | android:16 |
| none | zzgtechltmqk_int | 16 | 0 | 16 | -100.0% | DOWN | android:16 |



### Rising / Falling (campaigns with comparable WoW)

**Rising (WoW ≥ +10%):**

- TR_Meta_web2app_MIX_RTGT_AddToCart_022726_Images — 16→40 (150.0%)


**Falling (WoW ≤ -10%):**

- tr_asa_appinstall_brand_exact_all_02.06.2025 — 152→0 (-100.0%)
- cenoa.comtr homepage — 112→0 (-100.0%)
- TR-Discovery-24.10.2025 — 72→0 (-100.0%)
- Google // Cenoa // Search // TR // Pure Brand — 48→0 (-100.0%)
- tr_asa_appinstall_brand_broad_all_02.06.2025 — 48→0 (-100.0%)



## 2) Splits (where available)

### Daily table (TR) — installs by media_source

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



### Daily table (TR) — installs by platform

| platform | installs |
|---|---|
| android | 13120 |
| ios | 768 |



### Weekly table — country split (installs)

| Country | Installs (2026-W11) | Installs (2026-W12) | WoW % | Trend |
|---|---|---|---|---|
| TR | 1384 | 336 | -75.7% | DOWN |
| NG | 46 | 41 | -10.9% | DOWN |
| EG | 342 | 20 | -94.2% | DOWN |
| PK | 2 | 0 | -100.0% | DOWN |



### Weekly table — TR channel WoW (for spend alignment)

| Weekly channel | Mapped plan channel | Installs (2026-W11) | Installs (2026-W12) | WoW % | Trend |
|---|---|---|---|---|---|
| AppNext | SpazeAppnext | 799 | 95 | -88.1% | DOWN |
| other | InfluencerOther | 164 | 90 | -45.1% | DOWN |
| partner | InfluencerOther | 197 | 85 | -56.9% | DOWN |
| meta | Meta | 128 | 30 | -76.6% | DOWN |
| apple_ads | AppleSearchAds | 70 | 20 | -71.4% | DOWN |
| google | Google | 15 | 10 | -33.3% | DOWN |
| referral_affi | AffiliateRAFCRM | 11 | 6 | -45.5% | DOWN |


### Weekly table — TR platform split (installs)

| Platform | Installs (2026-W11) | Installs (2026-W12) | WoW % | Trend |
|---|---|---|---|---|
| android | 1188 | 240 | -79.8% | DOWN |
| ios | 196 | 96 | -51.0% | DOWN |



## 3) Spend vs installs — misalignment flags (Sheets snapshot)

Spend source: `data/sheets-budget-tracking.json` (exported from Google Sheets).

Heuristic used: flag channels with **top planned March TR budget** where **TR installs are DOWN WoW** in weekly table.


### March TR planned channel budget

| Plan channel | Planned budget (USD) |
|---|---|
| SpazeAppnext | 4500 |
| InfluencerOther | 4500 |
| Google | 3750 |
| AffiliateRAFCRM | 3000 |
| AppleSearchAds | 2800 |
| TikTok | 1200 |
| Reddit | 1000 |
| Twitter | 1000 |
| Meta | 750 |
| LinkedIn | 500 |




### Potential misalignments (review)

| Plan channel | Weekly channel | Planned budget | Installs (2026-W11) | Installs (2026-W12) | WoW % | Note |
|---|---|---|---|---|---|---|
| SpazeAppnext | AppNext | 4500 | 799 | 95 | -88.1% | High planned spend channel shows installs down WoW (weekly table). |
| AppleSearchAds | apple_ads | 2800 | 70 | 20 | -71.4% | High planned spend channel shows installs down WoW (weekly table). |
| Google | google | 3750 | 15 | 10 | -33.3% | High planned spend channel shows installs down WoW (weekly table). |
| InfluencerOther | other | 4500 | 164 | 90 | -45.1% | High planned spend channel shows installs down WoW (weekly table). |
| InfluencerOther | partner | 4500 | 197 | 85 | -56.9% | High planned spend channel shows installs down WoW (weekly table). |
| AffiliateRAFCRM | referral_affi | 3000 | 11 | 6 | -45.5% | High planned spend channel shows installs down WoW (weekly table). |



## 4) Notes / next improvements

- The daily campaign table currently contains only **6 days** of data (2026-02-25→2026-03-02), so 
  campaign WoW is based on **partial weeks** (2026-W10 is only 1 day). Treat campaign trend labels as directional only.
- If/when the daily table is extended (>=30 days), this script will automatically produce true 7-day vs prior-7-day WoW.
- Weekly country/channel table currently includes only **2 weeks** (W11, W12). As more weeks land, the analysis becomes more stable.




---

> ⚠️ **Attribution caveat:** Web campaigns (Meta/Google → cenoa.com → app store) may appear as "Organic" or "(none)" due to broken web→app attribution. Estimated correction factor: ~6.9×. See [attribution-reconciliation.md](attribution-reconciliation.md) for details.
