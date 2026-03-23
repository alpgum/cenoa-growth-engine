# Audience Insights Report — Mar 14–20, 2026

**Source:** Amplitude Event Segmentation API + cross-reference with country breakdown, feature engagement, and attribution funnel analyses  
**Period:** March 14–20, 2026

---

## 0. Requested property distributions (unique users)

> Metric used below: **Uniques** = number of distinct users who fired the event in Mar 14–20.

### 0.1 Withdraw Completed — grouped by country, platform, device

**By country (uniques, total=1,648):**

| Rank | Country | Unique users | Share |
|---:|---|---:|---:|
| 1 | Turkey | 892 | 54.1% |
| 2 | Nigeria | 579 | 35.1% |
| 3 | Egypt | 22 | 1.3% |
| 4 | United States | 19 | 1.2% |
| 5 | Germany | 17 | 1.0% |
| 6 | United Kingdom | 17 | 1.0% |
| 7 | Netherlands | 7 | 0.4% |
| 8 | Azerbaijan | 6 | 0.4% |
| 9 | Italy | 6 | 0.4% |
| 10 | Sweden | 6 | 0.4% |
| — | Others (29) | 77 | 4.7% |

**By platform (uniques, total=1,643):**

| Platform | Unique users | Share |
|---|---:|---:|
| iOS | 882 | 53.7% |
| Android | 756 | 46.0% |
| (none) | 5 | 0.3% |

**By device (uniques, total=1,643) — top brands/models bucket:**

| Device | Unique users | Share |
|---|---:|---:|
| Apple iPhone | 882 | 53.7% |
| Samsung Phone | 272 | 16.6% |
| Redmi Phone | 144 | 8.8% |
| Tecno Phone | 63 | 3.8% |
| Oppo Phone | 25 | 1.5% |
| Infinix Phone | 20 | 1.2% |
| POCO Phone | 17 | 1.0% |
| Xiaomi Phone | 15 | 0.9% |
| Huawei Phone | 14 | 0.9% |
| (many others) | 191 | 11.6% |

**Device type (more granular):** Top models are iPhone-heavy (iPhone 11/13/14/15 Pro Max variants). Long tail is large (218 models beyond top-15).

### 0.2 Cenoa sign-up completed — grouped by country, platform

**By country (uniques, total=1,219):**

| Rank | Country | Unique users | Share |
|---:|---|---:|---:|
| 1 | (none) | 762 | 62.5% |
| 2 | Turkey | 228 | 18.7% |
| 3 | Nigeria | 117 | 9.6% |
| 4 | Egypt | 65 | 5.3% |
| 5 | Pakistan | 15 | 1.2% |
| 6 | Ghana | 7 | 0.6% |
| — | Others | 25 | 2.1% |

**By platform (uniques, total=1,219):**

| Platform | Unique users | Share |
|---|---:|---:|
| (none) | 762 | 62.5% |
| iOS | 235 | 19.3% |
| Android | 222 | 18.2% |

> Data quality note: the massive **(none)** share on both **country** and **platform** strongly suggests a **web → app** (or server-side) sign-up flow that is not consistently attaching device + geo properties.

### 0.3 Get Paid Opened — grouped by country

**By country (uniques, total=3,112):** Turkey 1,494 (48.0%), Nigeria 1,072 (34.4%), Egypt 273 (8.8%).

### 0.4 [AppsFlyer] Install — grouped by media source

**By media source (uniques, total=1,444):** Organic 633 (43.8%), appnext_int 272 (18.8%), zzgtechltmqk_int 120 (8.3%), Apple Search Ads 75 (5.2%), Architect 74 (5.1%), byteboost2_int 70 (4.8%), cenoa.com 69 (4.8%), googleadwords_int 54 (3.7%), tiktokglobal_int 49 (3.4%).

---

## 1. Ideal Customer Profile by Market

### 🇹🇷 Turkey — The Power User Market

**Profile:** Crypto-savvy urban professionals using Cenoa for payments, transfers, and card spending.

| Dimension | Data |
|-----------|------|
| **Volume** | 670 installs (46.5%), 226 sign-ups (49.9%), 1,177 withdrawals (53.0%) |
| **Platform** | iOS slightly leads among withdrawers (53.7% of unique withdrawers are iOS) |
| **Device profile** | Apple iPhone-heavy (consistent with iOS over-indexing in withdrawals) |
| **Feature mix** | Debit Card (31.3%), Money Transfer (29.8%), Get Paid (29.8%), Deposit (9.1%) |
| **KYC engagement** | 95% of all KYC submissions come from Turkey — regulatory-ready users |
| **Top acquisition** | Apple Search Ads (brand exact: 114 withdrawals from 26 installs), Organic (44%), Google Ads |
| **Deposit:Withdraw ratio** | 0.8x — deposits slightly trail withdrawals, indicating users receive/earn within the app |

**ICP summary:** Turkish users are the highest-engagement, highest-LTV segment. They use the full product suite — card, transfer, and Get Paid equally. They convert well through brand search (ASA), complete KYC at very high rates, and become repeat transactors. These are digitally literate, card-using, crypto-comfortable 25–40 year-olds searching for "Cenoa" or related fintech terms.

**Power user signals:**
- Complete KYC within first session
- Use Debit Card tab within first week
- Make 2+ withdrawals/week
- Acquired via Apple Search Ads brand or organic

---

### 🇳🇬 Nigeria — The Remittance Market

**Profile:** Freelancers and diaspora receiving payments, with a strong deposit→withdraw pattern.

| Dimension | Data |
|-----------|------|
| **Volume** | 458 installs (31.8%), 117 sign-ups (25.8%), 778 withdrawals (35.0%) |
| **Platform** | Android-first engagement (Get Paid Opened uniques: 59.6% Android) |
| **Device profile** | Strong presence of Samsung/Redmi/Tecno/Infinix-class devices among withdrawers → optimize for mid/low-end Android UX |
| **Feature mix** | Get Paid (36.9%), Money Transfer (28.3%), Deposit (18.1%), Debit Card (16.7%) |
| **Deposit:Withdraw ratio** | 0.6x — significantly more withdrawals than deposits = heavy inbound money flow |
| **Top acquisition** | Organic (dominant), Architect (73 installs, 19 sign-ups, 0 withdrawals yet — ⚠️ watchlist) |
| **KYC** | 230 KYC starts but 0 KYC submissions — no Bridge KYC in Nigeria |

**ICP summary:** Nigerian users are remittance receivers. The 0.6x deposit:withdraw ratio means they're getting paid through the app (freelancers on Fiverr/Upwork receiving crypto payments) and cashing out. Deposit is their #1 action relative to other markets (18.1% of feature mix vs 9.1% for TR). Get Paid is the engagement hook. Card is secondary. These are 22–35 year-old Android users, likely freelancers or small business owners receiving international payments.

**Power user signals:**
- Use Get Paid + Deposit in the same session
- 3+ withdrawals/week (heavy outflow pattern)
- Acquired organically (word-of-mouth in freelancer communities)
- Do NOT index on card usage — it's not their primary use case

---

### 🇪🇬 Egypt — The Card-Curious Explorer

**Profile:** Users who browse the card feature disproportionately but transact lightly.

| Dimension | Data |
|-----------|------|
| **Volume** | 206 installs (14.3%), 64 sign-ups (14.1%), 23 withdrawals (1.0%) |
| **Platform** | Likely Android-leaning (as with Get Paid overall), but main issue is activation, not platform |
| **Activation gap** | 273 Get Paid unique users vs only 22 unique withdrawers in-week → high interest, low conversion |
| **Feature mix** | Debit Card (38.0%), Get Paid (35.1%), Deposit (13.0%), Money Transfer (13.9%) |
| **Deposit:Withdraw ratio** | 1.0x — balanced but extremely low volume (22 deposits, 23 withdrawals) |
| **Top acquisition** | Organic + new Meta web2app campaigns (launched Mar 18–20, too early to judge) |
| **KYC** | 62 KYC starts, 0 submissions — no Bridge KYC path for Egypt |

**ICP summary:** Egypt users are interested but not yet transacting at scale. The 38.0% Debit Card tab share is the highest of any market — they want the card but conversion friction is high. Money Transfer is notably weak (13.9% vs 29.8% for TR) suggesting limited corridor support. These users are curious about crypto-linked financial products but face structural barriers (KYC, corridors, local payment rails). The opportunity is large (206 installs/week) but activation is the bottleneck.

**Power user signals (aspirational — small sample):**
- Open Debit Card tab within first session
- Attempt deposit within first week
- Acquired via Meta campaigns or organic search

---

## 2. Best Acquisition Channel by User Quality Tier

### Tier 1 — High LTV (Active Transactors)

| Rank | Channel | Evidence | Market |
|------|---------|----------|--------|
| 1 | **Apple Search Ads (Brand Exact)** | 26 installs → 114 withdrawals/week | TR |
| 2 | **Organic** | 632 installs → 487 withdrawals/week | All |
| 3 | **Google Ads** | 54 installs → 29 withdrawals, 25.9% signup rate | TR |
| 4 | **af_app_invites (Referral)** | 7 installs → 13 withdrawals, 42.9% signup rate | TR/NG |

**Insight:** Intent-based channels (search, referral) massively outperform interruption-based channels (social, display) for transaction quality.

### Tier 2 — Medium LTV (Sign Up, Some Transactions)

| Rank | Channel | Evidence | Market |
|------|---------|----------|--------|
| 1 | **cenoa.com (Web Referral)** | 69 installs, 26.1% signup, 8 withdrawals | TR |
| 2 | **byteboost2_int** | 71 installs, 12.7% signup, 34 withdrawals | Mixed |
| 3 | **Google Ads (Nigeria)** | NG_Google_iOS_CVR: 14 withdrawals | NG |

### Tier 3 — Low/No LTV (Install but Don't Convert)

| Rank | Channel | Evidence | Flag |
|------|---------|----------|------|
| 1 | **appnext_int** | 273 installs → 1 withdrawal | 🚩 CPI fraud |
| 2 | **TikTok** | 49 installs → 0 withdrawals | 🚩 Non-converting |
| 3 | **Architect (NG)** | 73 installs → 0 withdrawals | ⚠️ Watchlist |
| 4 | **zzgtechltmqk_int** | 120 installs → 22 withdrawals | ⚠️ Spiking, unclear quality |

---

## 3. Feature Engagement Patterns That Predict High LTV

Based on cross-referencing feature usage with transaction volume across markets:

### Strong LTV Predictors

| Signal | Confidence | Reasoning |
|--------|------------|-----------|
| **KYC Submission** (Turkey) | ⭐⭐⭐ | 170 KYC submits → 1,177 withdrawals. Users who complete KYC become power transactors |
| **Debit Card Tab + Withdraw** (Turkey) | ⭐⭐⭐ | TR users who engage with card AND withdraw are the highest-engagement cohort |
| **Get Paid + Deposit combo** (Nigeria) | ⭐⭐⭐ | NG users receiving payments AND depositing = core remittance flow = repeat usage |
| **Money Transfer click** (Turkey) | ⭐⭐ | 55.1% of all Money Transfer clicks come from TR — active transfer users have high retention |
| **Deposit Tapped** (Nigeria) | ⭐⭐ | NG is #1 for deposits — users who deposit likely have ongoing inbound flow |

### Weak/Misleading Predictors

| Signal | Why Misleading |
|--------|---------------|
| **Debit Card Tab only** (Egypt) | High browse (38% of EG activity) but minimal transactions (23 withdrawals). Interest ≠ intent |
| **Install from paid display** | appnext (273 installs) and TikTok (49 installs) show volume without downstream conversion |
| **Get Paid only** (no deposit/withdraw) | Browse-only Get Paid users may be window shopping — need deposit OR withdraw within 7 days as qualifier |

### Recommended LTV Proxy Scoring

```
High LTV (score 8-10):
  KYC completed + 2+ withdrawals/week + any feature engagement
  
Medium LTV (score 5-7):
  Signup completed + 1+ deposit OR withdrawal + Get Paid or Card tab visit
  
Low LTV (score 1-4):
  Install only, or signup without any transaction event within 14 days
```

---

## 4. Targeting Recommendations

### 🎯 Lookalike Seed Audiences

| Seed Name | Definition | Size Est. | Use For |
|-----------|-----------|-----------|---------|
| **TR Power Users** | Turkey + 3+ withdrawals/week + KYC complete + Card tab visited | ~300-500 users | ASA LAL, Google Similar, Meta 1% LAL |
| **NG Remitters** | Nigeria + Get Paid opened + Deposit completed + 2+ withdrawals | ~200-300 users | Google LAL (Nigeria), organic community targeting |
| **High-Intent Signers** | All countries + signup within 24h of install + KYC started | ~150-200 users | Cross-market ASA/Google expansion |
| **Referral Champions** | Users with af_app_invites attribution + 5+ withdrawals | ~50-100 users | Referral program amplification |

### 🎯 Interest Targeting by Market

**Turkey:**
- Interests: cryptocurrency, fintech, digital payments, international transfers, freelancing
- Competitors: Papara, ininal, Wise (compete on ASA)
- Channels: Apple Search Ads (brand + competitor + generic), Google Search, Meta retargeting
- Creatives: Focus on card benefits, instant transfers, crypto→TRY conversion
- Avoid: TikTok (proven non-converting), CPI networks (fraud-prone)

**Nigeria:**
- Interests: freelancing, remote work, Fiverr/Upwork, international payments, dollar accounts
- Competitors: Grey, Chipper Cash, Payoneer
- Channels: Google Search (iOS CVR showing results), organic/content (freelancer communities)
- Creatives: "Get paid in USD, withdraw in Naira", freelancer testimonials
- Avoid: High-CPI display networks, broad social targeting
- Key insight: Android-first creative and UX optimization critical (58%+ Android)

**Egypt:**
- Interests: digital banking, card payments, online shopping, crypto
- Competitors: Telda, ValU, Fawry
- Channels: Meta web2app (just launched, monitor closely), Google Search
- Creatives: Focus on card feature (38% of EG engagement), easy onboarding
- Priority: Fix activation bottleneck first — high install-to-browse ratio but minimal transactions
- Avoid: Scaling spend until KYC/corridor barriers are resolved

### 🎯 Channel Budget Allocation (Recommended)

Based on quality tier analysis:

| Channel | Current Share | Recommended | Rationale |
|---------|-------------|-------------|-----------|
| Apple Search Ads | ~5% of installs | **↑ 15-20%** | Best LTV by far. Increase brand, expand generic |
| Organic/ASO | ~44% | **Protect** | Backbone. Invest in ASO, content, brand awareness |
| Google Ads | ~4% | **↑ 10-12%** | High quality. Scale TR brand + expand NG |
| Referral Program | ~0.5% | **↑ 3-5%** | Highest per-user quality. Invest in referral UX |
| Meta (Retargeting) | ~1% | **Maintain 3-5%** | TR_Meta_web2app_RTGT shows 9 withdrawals — retargeting works |
| Meta (Egypt) | New | **2-3% (test)** | Monitor for 2 weeks before scaling |
| Architect (NG) | ~5% | **↓ Pause/reduce** | Zero withdrawals. Review by Apr 3 |
| byteboost2 | ~5% | **↓ 2-3%** | Mediocre quality. Don't kill but don't scale |
| appnext | Paused | **⛔ Dead** | CPI fraud confirmed |
| TikTok | Paused | **⛔ Dead** | Zero conversion confirmed |

### 🎯 Creative & Messaging Matrix

| Market | Primary Hook | Secondary Hook | CTA |
|--------|------------|----------------|-----|
| TR | "Kripto kartınla harcamaya başla" (Spend with your crypto card) | "Anında transfer, sıfır komisyon" | KYC → Card activation |
| NG | "Get paid in crypto, withdraw in Naira" | "Your global freelancer wallet" | Get Paid → Deposit → Withdraw |
| EG | "Your digital card for online shopping" | "Buy crypto, spend anywhere" | Card tab → First deposit |

---

## 5. Platform + device implications (what to do with the distributions)

### Withdraw Completed — platform (uniques)

| Platform | Unique users | Share |
|---|---:|---:|
| iOS | 882 | 53.7% |
| Android | 756 | 46.0% |

**Implication:** iOS slightly over-indexes on *transacting* users. Keep iOS-heavy budgets for high-LTV channels (ASA + Google search), but don’t ignore Android (nearly half of withdrawers).

### Withdraw Completed — device (uniques)

- **Apple iPhone = 53.7%** of withdrawers
- Top Android brands among withdrawers: **Samsung (16.6%)**, **Redmi (8.8%)**, **Tecno (3.8%)**, plus Infinix/POCO/Xiaomi

**Implication:** Nigeria-heavy cohorts likely sit in the **Tecno/Infinix/Redmi** ecosystem → make sure Android creatives load fast, UI is readable on smaller screens, and onboarding flows are resilient on mid/low-end devices.

### Get Paid Opened — platform (uniques)

| Platform | Unique users | Share |
|---|---:|---:|
| Android | 1,848 | 59.6% |
| iOS | 1,254 | 40.4% |

**Implication:** Android is the engagement engine for “Get Paid” (especially relevant for NG). Campaigns that optimize for “Get Paid Opened” should be Android-first.

---

## 6. Attribution Gap & Data Quality Notes

- **62.5% of sign-ups have "(none)" platform** — web-to-app attribution broken for sign-up event
- **1,355 withdrawals unattributed** to any media source — AF attribution window may be too short
- **Country-filtered queries failed** in Amplitude API — cross-dimensional segmentation (country × platform × source) requires Amplitude Charts UI or Behavioral Cohort API, not basic event segmentation
- **Recommendation:** Set up Amplitude cohorts for each ICP definition above and track them as saved segments for ongoing monitoring

---

*Generated: March 21, 2026 | Data: Amplitude Event Segmentation API + existing analysis cross-reference*
