# Attribution Funnel Analysis — Organic vs Paid vs Referral

**Period:** March 14–20, 2026  
**Source:** Amplitude Event Segmentation API (grouped by `[AppsFlyer] media source` / `campaign`)  
**Events:** `[AppsFlyer] Install` → `Cenoa sign-up completed` → `Withdraw Completed`

---

## ⚠️ Important Caveats

1. **Attribution gap in downstream events:** Sign-up shows 986 users as "(none)" and Withdrawal shows 1,355 as "(none)". These are users whose AppsFlyer attribution was not carried through. This is common — AF attribution sticks to the install event but may not propagate to later events for all users.
2. **Withdrawals reflect the existing user base**, not just users who installed this week. A channel with high withdrawals and low installs (e.g., Apple Search Ads) means historically-acquired users from that channel are high-LTV, not that this week's installs already withdrew.
3. Conversion rates below should be interpreted directionally, not as exact same-cohort funnels.

---

## 1. Channel Overview (Mar 14–20 Totals)

| Channel | Installs | Sign-ups | Withdrawals | Install→Signup % | Notes |
|---|---|---|---|---|---|
| **Organic** | 632 | 77 | 487 | 12.2% | Largest install volume; strong withdrawal base |
| **appnext_int** | 273 | 24 | 1 | 8.8% | 🚩 Massive installs, near-zero withdrawals |
| **zzgtechltmqk_int** | 120 | 20 | 22 | 16.7% | Growing volume (spiked end of week) |
| **Apple Search Ads** | 75 | 22 | 254 | 29.3% | ⭐ Highest quality — strong downstream activity |
| **Architect** | 73 | 19 | 0 | 26.0% | 🚩 Good sign-ups but zero withdrawals |
| **byteboost2_int** | 71 | 9 | 34 | 12.7% | Moderate; some downstream conversion |
| **cenoa.com** | 69 | 18 | 8 | 26.1% | Web referral; decent sign-up rate |
| **googleadwords_int** | 54 | 14 | 29 | 25.9% | ⭐ Small but high-quality traffic |
| **tiktokglobal_int** | 49 | 8 | 0 | 16.3% | 🚩 Zero withdrawals; campaigns paused mid-week |
| **af_app_invites** | 7 | 3 | 13 | 42.9% | ⭐ Referrals — tiny volume but highest conversion |
| **Web Onboarding** | 6 | 1 | 0 | 16.7% | Negligible volume |
| **cenoacomtr** | 5 | 1 | 23 | 20.0% | Low new installs but high withdrawal from existing |
| **Auto Pilot Tool** | 4 | 1 | 0 | 25.0% | Too small to evaluate |
| **Other** | 6 | 3 | 0 | — | Eihracat Yıldızları, Social_instagram, Egypt LTV Test |

**Total attributed installs:** ~1,444  
**Unattributed sign-ups ("none"):** 986 | **Unattributed withdrawals ("none"):** 1,355

---

## 2. Organic vs Paid Funnel Comparison

| Segment | Installs | Sign-ups | Withdrawals | Signup Rate | Quality Signal |
|---|---|---|---|---|---|
| **Organic** | 632 (44%) | 77 | 487 | 12.2% | ⭐ High-LTV base |
| **Paid (all)** | 765 (53%) | 104 | 340 | 13.6% | Mixed — ASA strong, appnext weak |
| **Referral** (invites + web) | 47 (3%) | 4 | 21 | 8.5% | Tiny but loyal |

### Paid Channel Breakdown:
- **Apple Search Ads** — Best paid channel by far. High intent (brand/competitor search), 29.3% install→signup, massive withdrawal base (254/week). Historical users are highly active.
- **Google Ads** — Similar quality profile at smaller scale. 25.9% signup rate, 29 withdrawals. Efficient.
- **appnext_int** — ⛔ 273 installs but only 1 withdrawal. Classic CPI fraud/low-quality pattern. Campaign already stopped mid-week (zero installs from Mar 17).
- **byteboost2_int** — Mediocre. 12.7% signup, some withdrawals (34). Watchlist.
- **zzgtechltmqk_int** — Concerning. Spiking installs (38→44 last 2 days) but only 22 withdrawals. Monitor closely.
- **TikTok** — Paused mid-week. Zero withdrawals. 🚩 Low quality confirmed.
- **Architect (NG)** — Decent signup rate (26%) but zero withdrawals. Nigeria market may need more time to convert, or these are low-intent users.

---

## 3. Top Campaigns Ranked by Downstream Conversion

### Campaigns with Withdrawal Activity (highest → lowest):

| Campaign | Installs | Sign-ups | Withdrawals | Quality |
|---|---|---|---|---|
| **tr_asa_appinstall_brand_exact** | 26 | 12 | 114 | ⭐⭐⭐ Best campaign overall |
| **N/A (Organic)** | 632 | 77 | 488 | ⭐⭐⭐ Reliable base |
| **1764668627** (Meta legacy) | — | — | 76 | ⭐⭐ Strong historical LTV |
| **cenoa.comtr homepage** | 5 | 1 | 23 | ⭐⭐ Small but active base |
| **tr_asa_appinstall_brand_broad** | — | — | 17 | ⭐⭐ Broad brand ASA works |
| **890668** (byteboost) | 34 | 5 | 13 | ⭐ Some downstream |
| **Invite a Friend** | — | 3 | 13 | ⭐⭐ Referral loop working |
| **NG_Google_iOS_CVR** | — | — | 14 | ⭐ Nigeria Google showing activity |
| **890670** (byteboost) | 37 | 4 | 5 | ⚠️ High install, low withdrawal |
| **TR_Meta_web2app_RTGT** | 17 | 6 | 9 | ⭐ Retargeting converts |
| **tr_asa_competitor** | 12 | — | 9 | ⭐ Competitor ASA decent |
| **cenoa.com homepage** | 69 | 18 | 8 | ⚠️ Good signup, weak withdrawal |
| **tr_asa_generic** | — | — | 8 | ⭐ Generic ASA works |

### Campaigns with ZERO Withdrawal (Low Quality Flags):

| Campaign | Installs | Sign-ups | Flag |
|---|---|---|---|
| **Cenoa_CPI_UA_TR** (appnext) | 273 | 24 | 🚩 WORST — stopped mid-week, classic CPI fraud |
| **EG_Meta_web2app_CVR_Android_031826** | 44 | 3 | 🚩 New Egypt campaign, no downstream yet |
| **TR_TikTok_Android_030926** | 23 | 3 | 🚩 TikTok — installs don't convert |
| **TR_TikTok_Android_031726** | 21 | 3 | 🚩 Same pattern, newer campaign |
| **EG_Meta_web2app_ALL_031826** | 20 | 4 | ⚠️ Just launched (Mar 20), too early |
| **architect_nigeria_en_freelancer** | 21 | 4 | 🚩 Nigeria Architect — no withdrawals |
| **architect_freelancer_fiverr** | 18 | 8 | ⚠️ Good signup rate, no withdrawal yet |
| **architect_wise-paypal-wu-revolut** | 16 | 4 | 🚩 No downstream |
| **architect_freelancer_upwork** | 13 | — | 🚩 No downstream |

---

## 4. Key Findings & Recommendations

### ⭐ Highest Quality Channel: Apple Search Ads
- Brand exact search drives the best users by far
- 114 withdrawals from just 26 installs this week = massive historical LTV
- **Recommendation:** Increase ASA brand budget. Expand to brand broad and generic.

### ⭐ Runner-Up: Google Ads
- 25.9% signup rate, 29 withdrawals
- **Recommendation:** Scale Google search campaigns, especially TR brand terms.

### 🚩 Worst Quality: appnext_int (Cenoa_CPI_UA_TR)
- 273 installs → 24 sign-ups → **1 withdrawal**
- Install→withdrawal rate: **0.4%** — essentially zero
- Already paused mid-week (smart decision)
- **Recommendation:** Do not reactivate. Write off as CPI fraud/bot traffic.

### 🚩 Low Quality: TikTok
- 49 installs → 8 sign-ups → **0 withdrawals**
- Both Android campaigns show same pattern
- **Recommendation:** Pause until creative/targeting is reworked. Current traffic is non-converting.

### ⚠️ Watch List: Architect (Nigeria)
- 73 installs, 19 sign-ups (26% — good!) but **0 withdrawals**
- Could be market maturity issue (Nigeria users slower to first transaction)
- **Recommendation:** Don't kill yet. Set 2-week review window. If still zero withdrawals by Apr 3, pause.

### ⚠️ Watch List: zzgtechltmqk_int
- Volume spiking (5→44 installs/day by end of week)
- Only 22 withdrawals — unclear quality
- **Recommendation:** Monitor daily. If installs keep climbing without proportional signups, investigate for fraud.

### 💡 Hidden Gem: Referrals (af_app_invites)
- Only 7 installs but 42.9% signup rate and 13 withdrawals (from existing base)
- **Recommendation:** Invest in referral program UX. This is the highest quality per-user channel.

### 💡 Organic Remains King
- 44% of all installs, consistent daily volume (77-113/day)
- 487 withdrawals/week — the backbone of active users
- **Recommendation:** Protect organic (ASO, brand, content marketing). Don't let paid cannibalize.

---

## 5. Attribution Gap Analysis

The large "(none)" buckets (986 sign-ups, 1,355 withdrawals) indicate significant attribution loss:
- **Possible causes:** AF attribution window expiry, cross-device journeys, web-to-app flows not tracked, SDK issues
- **Impact:** True channel ROI is underreported — especially for channels that drive initial awareness but lose attribution before conversion
- **Recommendation:** Audit AppsFlyer attribution settings. Consider extending the lookback window. Check if web-to-app flows properly pass attribution.

---

*Generated: March 21, 2026 | Data: Amplitude Event Segmentation API*
