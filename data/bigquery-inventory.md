# BigQuery Inventory — cenoa-marketingdatawarehouse

## Datasets & Tables

### marketing_appsflyer

- `marketing_appsflyer.daily_installs_campaign_tr`
- `marketing_appsflyer.weekly_combined_totals`

## marketing_appsflyer.daily_installs_campaign_tr

**Row count:** 792

**date range:** 2026-02-25 → 2026-03-02

### Schema

| Column | Type | Mode |
|--------|------|------|
| `date` | DATE | NULLABLE |
| `platform` | STRING | NULLABLE |
| `media_source` | STRING | NULLABLE |
| `campaign` | STRING | NULLABLE |
| `installs` | INTEGER | NULLABLE |

### Dimensions

#### platform (2 unique)

- android
- ios

#### media_source (12 unique)

- Apple Search Ads
- Eihracat Yıldızları
- Facebook Ads
- Social_instagram
- af_app_invites
- appnext_int
- byteboost2_int
- cenoa.com
- cenoacomtr
- easyinventory
- googleadwords_int
- zzgtechltmqk_int

#### campaign (24 unique)

- 890668
- 890670
- Cenoa // Search // TR // Freelancer // Platform
- Cenoa_CPI_UA_TR
- E-ihracat Yıldızları Home Page
- Google // Cenoa // Pmax // TR // E-ihracat // Architect // KYC_Start
- Google // Cenoa // Search // TR // Pure Brand
- Instagram
- Invite a Friend
- TR-Discovery-24.10.2025
- TR_Meta_App_MIX_CVR_iOS_AddToCart_022526_ExcAppUsers
- TR_Meta_web2app_MIX_CVR_ALL_AddToCart_022326_ExcVisitors
- TR_Meta_web2app_MIX_CVR_Android_AddToCart_012126
- TR_Meta_web2app_MIX_Leads_ALL_012926
- TR_Meta_web2app_MIX_RTGT_AddPaymentInfo_022726_Images
- TR_Meta_web2app_MIX_RTGT_AddToCart_022726_Images
- cenoa.com homepage
- cenoa.comtr homepage
- easyinventory-payin
- none
- tr_asa_appinstall_brand_broad_all_02.06.2025
- tr_asa_appinstall_brand_exact_all_02.06.2025
- tr_asa_appinstall_competitor_all_02.06.2025
- tr_asa_appinstall_generic_all_02.06.2025

## marketing_appsflyer.weekly_combined_totals

**Row count:** 147

### Schema

| Column | Type | Mode |
|--------|------|------|
| `week` | STRING | NULLABLE |
| `platform` | STRING | NULLABLE |
| `country` | STRING | NULLABLE |
| `channel` | STRING | NULLABLE |
| `installs` | INTEGER | NULLABLE |
| `clicks` | INTEGER | NULLABLE |
| `total_events` | INTEGER | NULLABLE |
| `unique_event_users` | INTEGER | NULLABLE |

### Dimensions

#### week (2 unique)

- 2026-W11
- 2026-W12

#### platform (2 unique)

- android
- ios

#### country (4 unique)

- EG
- NG
- PK
- TR

#### channel (7 unique)

- AppNext
- apple_ads
- google
- meta
- other
- partner
- referral_affi
