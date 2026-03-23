# Weekly Platform Breakdown — Mar 15–21 vs Mar 8–14

> **Source:** Amplitude Segmentation API (uniques) · **Grouped by:** `platform` property  
> **Generated:** 2026-03-22

---

## 1. Platform Split Per Funnel Step

### Current Week (Mar 15–21)

| Funnel Step | iOS | Android | (none) | Total | iOS % | Android % | (none) % |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Install** | 177 | 1,192 | — | 1,369 | 12.9% | 87.1% | — |
| **Sign-up** | 246 | 211 | 766 | 1,223 | 20.1% | 17.3% | 62.6% |
| **KYC Submit** | 27 | 79 | — | 106 | 25.5% | 74.5% | — |
| **Virtual Account** | 192 | 152 | 18 | 362 | 53.0% | 42.0% | 5.0% |
| **Withdraw** | 846 | 766 | 5 | 1,617 | 52.3% | 47.4% | 0.3% |

### Previous Week (Mar 8–14)

| Funnel Step | iOS | Android | (none) | Total | iOS % | Android % | (none) % |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Install** | 241 | 1,996 | — | 2,237 | 10.8% | 89.2% | — |
| **Sign-up** | 295 | 303 | 1,011 | 1,609 | 18.3% | 18.8% | 62.8% |
| **KYC Submit** | 48 | 95 | — | 143 | 33.6% | 66.4% | — |
| **Virtual Account** | 289 | 256 | 15 | 560 | 51.6% | 45.7% | 2.7% |
| **Withdraw** | 924 | 772 | 8 | 1,704 | 54.2% | 45.3% | 0.5% |

### WoW Deltas

| Funnel Step | iOS Δ | Android Δ | Total Δ |
|---|---:|---:|---:|
| **Install** | -64 (−26.6%) | -804 (−40.3%) | -868 (−38.8%) |
| **Sign-up** | -49 (−16.6%) | -92 (−30.4%) | -386 (−24.0%) |
| **KYC Submit** | -21 (−43.8%) | -16 (−16.8%) | -37 (−25.9%) |
| **Virtual Account** | -97 (−33.6%) | -104 (−40.6%) | -198 (−35.4%) |
| **Withdraw** | -78 (−8.4%) | -6 (−0.8%) | -87 (−5.1%) |

> 📉 Broad decline across the funnel — install volume down ~39%, heaviest on Android (−40.3%). Withdraw held relatively steady (−5.1%) suggesting existing users still active.

---

## 2. iOS vs Android Conversion Rates at Each Step

### Install → Sign-up (known-platform only, excl. (none))

| Platform | Current | Previous | Δ |
|---|---:|---:|---:|
| **iOS** | 246 / 177 = **139.0%*** | 295 / 241 = **122.4%*** | — |
| **Android** | 211 / 1,192 = **17.7%** | 303 / 1,996 = **15.2%** | +2.5pp |

> *iOS signup > install because (none)-platform signups likely include iOS web signups. See attribution caveat §5.

### Sign-up → KYC Submit (known-platform only)

| Platform | Current | Previous | Δ |
|---|---:|---:|---:|
| **iOS** | 27 / 246 = **11.0%** | 48 / 295 = **16.3%** | −5.3pp ⚠️ |
| **Android** | 79 / 211 = **37.4%** | 95 / 303 = **31.4%** | +6.1pp ✅ |

### KYC Submit → Virtual Account Opened

| Platform | Current | Previous | Δ |
|---|---:|---:|---:|
| **iOS** | 192 / 27 = **711%*** | 289 / 48 = **602%*** | — |
| **Android** | 152 / 79 = **192.4%*** | 256 / 95 = **269.5%*** | — |

> *Virtual accounts opened >> KYC submits because virtual accounts include users who completed KYC in prior periods, plus some accounts open without full KYC. These are not same-cohort conversion rates.

### Virtual Account → Withdraw

| Platform | Current | Previous | Δ |
|---|---:|---:|---:|
| **iOS** | 846 / 192 = **440.6%*** | 924 / 289 = **319.7%*** | — |
| **Android** | 766 / 152 = **503.9%*** | 772 / 256 = **301.6%*** | — |

> *Withdraw users vastly outnumber new virtual account opens — these are repeat/existing users. Withdraw is a retention metric, not a new-user funnel step.

### Clean Install → KYC Submit Rate (best funnel proxy)

| Platform | Current | Previous | Δ |
|---|---:|---:|---:|
| **iOS** | 27 / 177 = **15.3%** | 48 / 241 = **19.9%** | −4.7pp ⚠️ |
| **Android** | 79 / 1,192 = **6.6%** | 95 / 1,996 = **4.8%** | +1.9pp ✅ |

---

## 3. Device Breakdown — Top Devices per Funnel Step (Current Week)

### Installs — Top 10 Devices

| # | Device | Installs |
|---|---|---:|
| 1 | (none) | 222 |
| 2 | Apple iPhone 11 | 21 |
| 3 | Redmi 14C | 19 |
| 4 | Infinix Smart 8 | 17 |
| 5 | Tecno Spark Go 2 | 16 |
| 6 | Redmi Note 11 Pro | 15 |
| 7 | Apple iPhone 13 | 14 |
| 8 | Apple iPhone 16 Pro Max | 14 |
| 9 | Redmi 15C | 14 |
| 10 | Redmi Note 14 Pro | 14 |

### Sign-ups — Top 10 Devices

| # | Device | Sign-ups |
|---|---|---:|
| 1 | (none) | 795 |
| 2 | Apple iPhone 12 | 33 |
| 3 | Apple iPhone 13 | 27 |
| 4 | Apple iPhone 16 Pro Max | 24 |
| 5 | Apple iPhone 14 Pro Max | 16 |
| 6 | Apple iPhone 11 | 13 |
| 7 | Apple iPhone 13 Pro Max | 13 |
| 8 | Apple iPhone 16 Pro | 13 |
| 9 | Apple iPhone 14 Pro | 11 |
| 10 | Apple iPhone 15 Pro Max | 11 |

> Sign-ups heavily skewed to iPhones in known-device segment. (none) dominates — these are web/deeplink signups without device attribution.

### KYC Submit — Top 10 Devices

| # | Device | KYC Submits |
|---|---|---:|
| 1 | (none) | 10 |
| 2 | Redmi Note 13 Pro 5G | 4 |
| 3 | Apple iPhone 14 Pro | 3 |
| 4 | Apple iPhone 14 Pro Max | 3 |
| 5 | Redmi Note 14 Pro | 3 |
| 6 | Samsung Galaxy A06 | 3 |
| 7 | Samsung Galaxy A26 5G | 3 |
| 8 | Tecno Spark 10 Pro | 3 |
| 9 | Apple iPhone 11 | 2 |
| 10 | Apple iPhone 12 | 2 |

### Withdrawals — Top 10 Devices

| # | Device | Withdrawals |
|---|---|---:|
| 1 | (none) | 111 |
| 2 | Apple iPhone 11 | 77 |
| 3 | Apple iPhone 14 Pro Max | 72 |
| 4 | Apple iPhone 13 | 71 |
| 5 | Apple iPhone 16 Pro Max | 60 |
| 6 | Apple iPhone 15 Pro Max | 53 |
| 7 | Apple iPhone 14 Pro | 46 |
| 8 | Apple iPhone 15 | 45 |
| 9 | Apple iPhone 13 Pro Max | 40 |
| 10 | Apple iPhone 17 Pro Max | 34 |

### Top 5 Device Brands — Installs (excl. (none))

| Brand | Installs | % of Known |
|---|---:|---:|
| **Samsung** | ~230 | 20.0% |
| **Apple** | ~177 | 15.4% |
| **Redmi/Xiaomi** | ~195 | 17.0% |
| **Tecno** | ~85 | 7.4% |
| **Infinix** | ~55 | 4.8% |

> Android install base is dominated by budget devices: Redmi, Tecno, Infinix, Samsung A-series. These are emerging-market devices (Turkey, Africa, South Asia).

---

## 4. KYC Submit Gap: iOS vs Android — Is It Improving?

### The Question: "iOS 2.4% vs Android 9.2% — is it improving?"

The referenced rates appear to come from an earlier period with different denominator logic. Here's the latest:

#### Sign-up → KYC Submit Rate

| Period | iOS | Android | Gap (Android − iOS) |
|---|---:|---:|---:|
| **Mar 8–14** | 16.3% | 31.4% | 15.1pp |
| **Mar 15–21** | 11.0% | 37.4% | 26.5pp |

**🔴 The gap is WIDENING, not closing.**

- iOS KYC rate dropped from 16.3% → 11.0% (−5.3pp)
- Android KYC rate improved from 31.4% → 37.4% (+6.1pp)
- Net gap expanded from 15.1pp → 26.5pp

#### Install → KYC Submit Rate

| Period | iOS | Android | Gap |
|---|---:|---:|---:|
| **Mar 8–14** | 19.9% | 4.8% | 15.2pp (iOS leads) |
| **Mar 15–21** | 15.3% | 6.6% | 8.6pp (iOS leads) |

> When measured from install, iOS still converts better (15.3% vs 6.6%), but the iOS rate is declining while Android improves. The gap is narrowing at the install level, widening at the signup level.

#### Root Cause Hypotheses

1. **iOS web signup issue:** iOS users may be signing up via web (landing in `(none)` platform) but then their KYC attempt is tracked under iOS — creating a denominator mismatch
2. **KYC UX on iOS:** Bridge KYC component may have rendering/camera issues on certain iOS versions
3. **Intent difference:** Android installs are campaign-driven (higher intent for KYC), iOS installs may include more organic/exploratory users
4. **Small iOS sample:** With only 27 iOS KYC submits, one week's movement may be noise

---

## 5. ⚠️ Attribution Caveats

### (none) Platform in Sign-ups

**62.6% of sign-ups (766/1,223) have `platform = (none)`.** This is the single biggest data quality issue in platform analysis.

**What (none) means:**
- Users who signed up via **web browser** (not the native app)
- Users who came through **deep links** that didn't carry platform attribution
- Users whose **Amplitude SDK** didn't fire the platform property at sign-up time
- Potentially **server-side events** triggered without client context

**Impact on analysis:**
- iOS and Android sign-up numbers are **understated** by ~60%+
- Conversion rates from sign-up → KYC are **inflated** for both platforms (denominator is too small)
- The true platform split at sign-up is unknown without resolving (none)
- If (none) users skew iOS (common for web-to-app flows), the iOS KYC gap is less severe than it appears

**Recommendation:**
1. Cross-reference with AppsFlyer's `media_source` to attribute (none) sign-ups
2. Ensure Amplitude `identify()` fires with platform on web sign-up flows
3. Consider using `device_type` presence as a proxy — sign-ups with known Apple devices = iOS

### Other Attribution Notes

- **Install data is AppsFlyer-sourced** (`[AppsFlyer] Install`) — different SDK than Amplitude native events
- **KYC Submit has 0 (none) platform** (in-app only) — this is expected since Bridge KYC component runs natively
- **Withdraw (none) is minimal** (5 users) — most withdrawals happen in-app with proper attribution
- **Virtual Account (none) = 18 users** — some accounts may be opened via API/backend processes

---

## Summary

| Signal | Status | Note |
|---|---|---|
| Install volume | 📉 −38.8% WoW | Both platforms down; Android hit hardest |
| Android dominance in installs | 87.1% | Budget device ecosystem (Redmi, Tecno, Infinix) |
| iOS dominance in withdrawals | 52.3% | Higher-value users, better retention |
| KYC gap (signup→KYC) | 🔴 Widening | iOS 11.0% vs Android 37.4% — gap grew +11pp WoW |
| (none) platform in signups | ⚠️ 62.6% | Critical attribution gap; masks true platform split |
| Withdraw resilience | ✅ −5.1% only | Existing user base stable despite acquisition dip |

---

*Analysis by Amplitude Segmentation API. Device model grouping unavailable (API limitation). Device data from `device_type` property.*

