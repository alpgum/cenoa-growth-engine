# Platform Funnel Analysis — iOS vs Android vs Web

**Period:** 2026-03-14 → 2026-03-20  
**Source:** Amplitude Event Segmentation API (m=totals, group_by=platform)

---

## Raw Numbers by Platform

| Funnel Stage | Android | iOS | (none)¹ | Total |
|---|---:|---:|---:|---:|
| [AppsFlyer] Install | 1,275 | 170 | — | 1,445 |
| Application first opened | 1,473 | 485 | — | 1,958 |
| Cenoa sign-up completed | 221 | 232 | 754 | 1,207 |
| KYC Started | 1,717 | 1,333 | 48 | 3,098 |
| KYC Submit clicked | 140 | 39 | — | 179 |
| Deposit Completed | 718 | 813 | 15 | 1,546 |
| Withdraw Completed | 1,033 | 1,187 | 7 | 2,227 |

¹ **(none) = Web / unattributed platform.** Users who signed up or transacted without a detected mobile platform — most likely web-based flows.

---

## Platform Mix (% of Total)

| Funnel Stage | Android | iOS | Web/none |
|---|---:|---:|---:|
| Install | **88.2%** | 11.8% | — |
| App first opened | **75.2%** | 24.8% | — |
| Sign-up completed | 18.3% | 19.2% | **62.5%** |
| KYC Started | **55.4%** | 43.0% | 1.5% |
| KYC Submit | **78.2%** | 21.8% | — |
| Deposit Completed | 46.4% | **52.6%** | 1.0% |
| Withdraw Completed | 46.4% | **53.3%** | 0.3% |

---

## Key Findings

### 1. Top-of-Funnel: Android Dominates Installs (88%)

Android captures **7.5x more installs** than iOS (1,275 vs 170). This is consistent with paid media being heavily Android-weighted (likely cheaper CPIs in target markets). iOS installs are minimal — either budget isn't allocated or iOS campaigns aren't running at scale.

### 2. Web Owns Sign-Up (62.5%)

The biggest surprise: **754 of 1,207 sign-ups (62.5%) come from "(none)" platform** — almost certainly web-based sign-up flows. Mobile sign-ups are roughly equal (Android 221, iOS 232), meaning the web funnel is the primary sign-up channel, outperforming both mobile platforms combined.

### 3. iOS Converts Better at Monetization

Despite having far fewer installs, iOS users show **stronger monetization behavior**:
- **Deposits:** iOS 813 vs Android 718 (iOS leads by 13%)
- **Withdrawals:** iOS 1,187 vs Android 1,033 (iOS leads by 15%)

iOS users are higher-value — they deposit more and withdraw more.

### 4. KYC is a Massive Bottleneck

- **KYC Started → KYC Submit** conversion: only **5.8%** overall
  - Android: 140 / 1,717 = **8.2%**
  - iOS: 39 / 1,333 = **2.9%**
- This is the biggest drop-off in the entire funnel. KYC completion rate is catastrophically low on both platforms, but **iOS is 3x worse** than Android at KYC submission.

### 5. Funnel Numbers Don't Decrease Linearly

KYC Started (3,098) and Deposit/Withdraw numbers exceed sign-up (1,207). This means:
- KYC Started / Deposit / Withdraw include **returning users** from before the analysis window
- The funnel is not purely sequential within this 7-day slice
- Install → Sign-up is the only clean acquisition funnel; downstream events mix new + existing users

---

## Platform Drop-Off Analysis

### Android Funnel
| Step | Count | Drop-off from Previous |
|---|---:|---:|
| Install | 1,275 | — |
| App opened | 1,473 | +15.5% (returning users inflate) |
| Sign-up | 221 | **−85.0% from app opened** |
| KYC Submit | 140 | −36.7% from sign-up |

**Android bottleneck:** App opened → Sign-up (85% drop). Users open the app but don't sign up.

### iOS Funnel
| Step | Count | Drop-off from Previous |
|---|---:|---:|
| Install | 170 | — |
| App opened | 485 | +185% (heavy returning user base) |
| Sign-up | 232 | **−52.2% from app opened** |
| KYC Submit | 39 | −83.2% from sign-up |

**iOS bottleneck:** Sign-up → KYC Submit (83% drop). iOS users sign up but abandon KYC at alarming rates.

### Web (none)
| Step | Count |
|---|---:|
| Sign-up | 754 |
| KYC Started | 48 |
| Deposit | 15 |
| Withdraw | 7 |

**Web bottleneck:** Sign-up → KYC (93.6% drop). Web sign-ups almost never proceed to KYC — they may be redirected to download the app, or the web KYC flow is broken/nonexistent.

---

## iOS vs Android Parity Analysis

| Metric | Android | iOS | Parity Ratio (iOS/Android) |
|---|---:|---:|---:|
| Install volume | 1,275 | 170 | 0.13x ⚠️ |
| App opens | 1,473 | 485 | 0.33x |
| Sign-ups | 221 | 232 | **1.05x** ✅ |
| KYC Started | 1,717 | 1,333 | 0.78x |
| KYC Submit | 140 | 39 | 0.28x ⚠️ |
| Deposits | 718 | 813 | **1.13x** ✅ |
| Withdrawals | 1,033 | 1,187 | **1.15x** ✅ |

**Summary:** iOS has far less top-of-funnel volume but **outperforms Android at monetization** (deposits +13%, withdrawals +15%). The severe iOS KYC Submit gap (0.28x) needs investigation — possible UX issue with the BridgeXYZ KYC component on iOS.

---

## Web/None Platform — Quantifying the Gap

- **754 web sign-ups** = 62.5% of all sign-ups, making web the #1 sign-up channel
- But web → KYC conversion is only **6.4%** (48/754), vs mobile combined at ~680% (inflated by returning users)
- Web → Deposit: only **2.0%** (15/754)
- Web → Withdraw: only **0.9%** (7/754)

**The gap:** Web acquires users cheaply but **fails to convert them downstream**. The 754 web sign-ups generate only 15 deposits — a **2.0% conversion rate** vs mobile's much higher engagement.

**Hypothesis:** Web sign-ups likely need to download the app to proceed with KYC/transactions. The handoff from web → app is leaking users massively.

---

## Recommendations

1. **Fix KYC completion** — The 5.8% KYC Started → Submit rate is the #1 funnel killer. Investigate BridgeXYZ component UX, especially on iOS (2.9% rate).

2. **Invest more in iOS acquisition** — iOS users are 13-15% more valuable at monetization despite getting 7.5x less install budget. Even at higher CPIs, iOS LTV likely justifies the spend.

3. **Fix web → app handoff** — 754 web sign-ups are mostly wasted. Either build a complete web KYC/transaction flow, or create a seamless deep-link + onboarding for web-to-app transition.

4. **Improve Android sign-up conversion** — 85% drop from app open to sign-up suggests onboarding friction or the app is opened but the value prop isn't landing.

---

*Generated: 2026-03-21 | Data: Amplitude API | Analysis window: 7 days*
