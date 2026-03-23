# Lookalike & Audience Targeting Recommendations

**Date:** March 21, 2026  
**Source data:** country-breakdown.md, feature-engagement.md, attribution-funnel.md  
**Purpose:** Define seed audiences, lookalike expansion, and platform-specific targeting for Meta, Google, and Apple Search Ads.

---

## 1. Meta Custom Audiences & Lookalikes

### Seed Audiences (ranked by value)

| # | Seed | Description | Size (weekly events) | Markets |
|---|------|-------------|---------------------:|---------|
| 1 | **Withdrawers** | Users who completed ≥1 withdrawal — highest-LTV action | TR 1,177 · NG 778 · EG 23 | TR, NG |
| 2 | **KYC Completers** | Users who submitted KYC (Bridge KYC Submit) | TR 170 (95% of total) | TR only |
| 3 | **Depositors** | Users who completed a deposit | TR 961 · NG 448 · EG 22 | TR, NG |
| 4 | **Website Visitors** | cenoa.com sessions (GA4) | ~6,317 sessions/week | All |

**Why this ranking:**
- Withdrawers are the ultimate value signal — they've moved real money out, indicating active usage and trust.
- KYC completers show high intent; currently TR-dominated (95%), so usable only in Turkey.
- Depositors are mid-funnel — they've put money in but may not have transacted yet.
- Website visitors are top-of-funnel but provide broad reach for prospecting.

### Lookalike Expansion Strategy

| Seed | 1% LAL (Precision) | 3% LAL (Balanced) | 5% LAL (Reach) | Notes |
|------|--------------------|--------------------|-----------------|-------|
| Withdrawers (TR) | Start here — highest quality | Scale after 1% saturates | Test in parallel for cost comparison | Primary prospecting engine |
| Withdrawers (NG) | Start here | Scale phase 2 | Broader reach for awareness | NG deposit-first behavior — pair with deposit CTA |
| KYC Completers (TR) | Test alongside Withdrawer LAL | Backup expansion | Skip — too diluted | TR-only; good for web2app retarget flows |
| Depositors (TR+NG) | Secondary seed | Good for scale | Use for broad awareness | Overlap with Withdrawers ~60-70% — use as incremental |
| Website Visitors | Broad prospecting | Main reach driver | Skip — too generic | Exclude existing app users from this seed |

**Recommended launch order:**
1. Withdrawers 1% (TR) + Withdrawers 1% (NG) — highest expected ROAS
2. KYC Completers 1% (TR) — incremental TR reach
3. Depositors 3% (TR+NG) — scale phase
4. Website Visitors 3% (All markets) — awareness/top-of-funnel

### Custom Audiences for Retargeting

| Audience | Definition | Use Case |
|----------|-----------|----------|
| Installed, No Sign-up | AF Install event, no "Cenoa sign-up completed" within 7d | Re-engagement push — 69% of installers don't sign up |
| Signed Up, No KYC | Sign-up completed, no KYC Submit within 14d | KYC nudge campaign |
| KYC Complete, No Deposit | KYC submitted, no Deposit Completed within 14d | Deposit incentive (TR only for now) |
| Depositors, No Withdrawal | Deposit completed, no Withdrawal Completed within 30d | Activation/usage campaign |
| Lapsed Users (30d) | Any activity >30 days ago, no activity since | Win-back campaign |

---

## 2. Google Ads — Audience Signals & Custom Intent

### Performance Max Audience Signals

**Competitor Keywords (Custom Segments):**
- "payoneer", "payoneer login", "payoneer withdrawal"
- "wise transfer", "wise business account", "transferwise"
- "paypal freelancer", "paypal receive payment"
- "revolut", "revolut USD account"
- "western union online"

**In-Market Segments:**
- Financial Services → Payment Services
- Financial Services → Banking Services → Online Banking
- Business Services → Freelance & Gig Work Platforms
- Financial Services → Currency Exchange & Money Transfer

**Affinity Segments:**
- Technophiles
- Business Professionals
- Avid Investors
- Aspiring Entrepreneurs

**Life Events:**
- Starting a new job (correlates with freelancer onboarding)

### Custom Intent Audiences (Search & Display)

| Audience Name | Keywords | Markets |
|---------------|----------|---------|
| Freelancer Payments | "freelancer payment", "get paid as freelancer", "freelance income", "receive USD payment" | TR, NG, EG |
| USD Banking | "USD bank account", "dollar account", "usd hesabı" (TR), "dollar savings account" | TR, NG, EG |
| Competitor Seekers | "payoneer alternative", "wise alternative", "paypal alternative for freelancers" | TR, NG |
| Remittance | "send money to Turkey", "send money to Nigeria", "international money transfer" | All |
| Crypto-Adjacent | "USDC", "stablecoin", "crypto withdrawal to bank" | TR, NG |

### Google Ads Remarketing Lists

- App Installers (via Firebase/AF) — exclude from prospecting
- Website visitors (cenoa.com, 30d) — RLSA for search, Display retarget
- Cart/funnel abandoners (started sign-up but didn't complete)

---

## 3. Apple Search Ads

### Keyword Strategy by Match Type

#### Brand (Exact + Broad)
| Keyword | Match | Priority | Notes |
|---------|-------|----------|-------|
| "cenoa" | Exact | 🔴 Must-win | Best campaign overall — 114 withdrawals from 26 installs (historical LTV) |
| "cenoa app" | Exact | 🔴 Must-win | Capture full brand queries |
| "cenoa" | Broad | 🟡 Scale | Already running — 17 withdrawals/week |

**Current performance:** Brand exact is the single best campaign across all channels (tr_asa_appinstall_brand_exact → 114 withdrawals). Protect and scale budget.

#### Competitor (Exact)
| Keyword | Match | Priority | Notes |
|---------|-------|----------|-------|
| "payoneer" | Exact | 🔴 High | Direct competitor for freelancer payments |
| "wise" | Exact | 🔴 High | Money transfer competitor |
| "paypal" | Exact | 🟡 Medium | Broad audience, may have lower intent |
| "transferwise" | Exact | 🟡 Medium | Legacy Wise users |
| "revolut" | Exact | 🟡 Medium | Digital banking competitor |
| "western union" | Exact | 🟢 Test | Remittance corridor overlap |

**Current performance:** tr_asa_competitor → 9 withdrawals/week. Decent ROI — expand keyword list.

#### Generic (Broad + Exact)
| Keyword | Match | Priority | Notes |
|---------|-------|----------|-------|
| "freelancer bank" | Broad | 🟡 Medium | High intent, niche |
| "usd account" | Broad | 🟡 Medium | Core value prop |
| "freelance payment app" | Exact | 🟡 Medium | Long-tail, high intent |
| "receive money abroad" | Broad | 🟢 Test | Remittance angle |
| "dolar hesabı" (TR) | Exact | 🟡 Medium | Turkish-language generic |
| "freelancer ödeme" (TR) | Exact | 🟡 Medium | Turkish-language generic |

**Current performance:** tr_asa_generic → 8 withdrawals/week. Working — expand keyword coverage.

#### ASA Budget Allocation Recommendation
| Campaign Type | Current Share | Recommended Share | Rationale |
|---------------|--------------|-------------------|-----------|
| Brand Exact | ~35% | 40% | Highest LTV — protect at all costs |
| Brand Broad | ~15% | 15% | Discovery + defense |
| Competitor | ~25% | 25% | Good ROI, expand keywords |
| Generic | ~25% | 20% | Test more keywords, cull losers |

---

## 4. Country-Specific Targeting

### 🇹🇷 Turkey (TR) — Primary Market

**Profile:** Power users — heavy on Money Transfer (55%), Debit Card (61%), Get Paid (47%). KYC completion is 95% TR.

| Channel | Targeting Approach |
|---------|-------------------|
| **Meta** | Freelancer communities (Upwork TR, Fiverr TR), "yurt dışından para kazanma", tech/design interest groups |
| **Google** | Keywords: "freelancer ödeme", "dolar hesabı", "yurtdışı gelir", "Upwork para çekme", "Fiverr ödeme alma" |
| **ASA** | Already strongest market — scale brand + generic Turkish keywords |
| **Interest Targeting** | Upwork, Fiverr, Freelancer.com interests; Remote work; Digital nomad; Software development; Graphic design |
| **Demographics** | 22-40, urban (Istanbul, Ankara, Izmir), university-educated |

### 🇳🇬 Nigeria (NG) — High-Growth Market

**Profile:** Deposit-first behavior (45% of Deposit Tapped), strong Get Paid (35%). Lower Debit Card interest (20%).

| Channel | Targeting Approach |
|---------|-------------------|
| **Meta** | Tech freelancer communities, "earn in USD", remittance groups, Paystack/Flutterwave interest audiences |
| **Google** | Keywords: "receive USD in Nigeria", "freelancer payment Nigeria", "dollar account Nigeria", "how to withdraw USD" |
| **ASA** | Expand from TR — run competitor (Payoneer, Wise) and generic ("dollar account") |
| **Interest Targeting** | Tech Twitter/X communities, remote work, cryptocurrency interest, Andela/tech talent networks |
| **Demographics** | 20-35, urban (Lagos, Abuja, Port Harcourt), tech-savvy |

**Creative angle:** Lead with Deposit + Get Paid flows (highest engagement). Avoid card-centric messaging (low interest in NG).

### 🇪🇬 Egypt (EG) — Emerging Market

**Profile:** Card-curious (38% of feature engagement is Debit Card), weak Money Transfer (14%). Arabic-speaking.

| Channel | Targeting Approach |
|---------|-------------------|
| **Meta** | Arabic-language creatives, freelancer groups (Arabic), remote work communities, "العمل عن بعد" interest |
| **Google** | Keywords: "حساب دولار" (dollar account), "freelancer payment Egypt", "USD account Egypt", "remote work payment" |
| **ASA** | Start with competitor exact (Payoneer, Wise) — these are known brands for EG freelancers |
| **Interest Targeting** | Remote work, freelancing, Upwork Arabic, translation services, graphic design |
| **Demographics** | 22-35, urban (Cairo, Alexandria, Giza) |

**Creative angle:** Lead with Debit Card feature (highest EG interest at 38%). Arabic-language ads are mandatory.

**⚠️ Note:** EG campaigns just launched (Mar 18-20) — zero withdrawal data yet. Allow 2-3 weeks before evaluating LTV.

---

## 5. Exclusion Lists

### Universal Exclusions (Apply to ALL Campaigns)

| Exclusion | Source | Reason |
|-----------|--------|--------|
| **Existing App Installers** | AppsFlyer device list / Firebase audience | Don't pay to re-acquire existing users |
| **Existing Customers** (KYC completed) | CRM export → Meta/Google customer list | Already converted — use retargeting instead |
| **Withdrawers** (active users) | Amplitude cohort export | Already high-value — don't waste prospecting budget |
| **Fraud/Bot Installs** | appnext_int campaign users | 273 installs → 1 withdrawal — confirmed low quality |

### Platform-Specific Exclusions

| Platform | Exclusion | Implementation |
|----------|-----------|---------------|
| **Meta** | Custom Audience: all app events (180d) | Upload via Meta Events Manager / MMP integration |
| **Meta** | Exclude Lookalike overlap: when running multiple LALs, exclude narrower seeds from broader ones | Campaign-level exclusion |
| **Google** | Customer Match: email list of existing users | Upload hashed emails to Google Ads |
| **Google** | App Install exclusion (Firebase link) | Exclude "all app users" segment in PMax |
| **ASA** | Existing downloaders | Automatic in ASA — Apple excludes current installers by default |

### Negative Keywords (Google)

| Type | Keywords |
|------|----------|
| **Brand defense** | "cenoa scam", "cenoa review", "is cenoa safe" (route to brand campaign, not generic) |
| **Irrelevant** | "cenoa restaurant", "cenoa wine", "cenoa italy" |
| **Low intent** | "free money app", "earn money online free", "make money fast" |
| **Wrong product** | "cenoa stock", "cenoa crypto price", "cenoa token" |

---

## 6. Implementation Priorities

### Week 1 (Immediate)
1. ✅ Create Withdrawer seed audiences in Meta (TR + NG separately)
2. ✅ Launch Withdrawer 1% LAL campaigns (TR + NG)
3. ✅ Scale ASA brand exact budget (+30%)
4. ✅ Upload exclusion lists across all platforms

### Week 2
5. Create KYC Completer seed (TR only) → launch 1% LAL
6. Add competitor keywords to ASA (Payoneer, Wise, PayPal)
7. Set up Google PMax with audience signals (competitor keywords + in-market)
8. Launch Google Custom Intent campaigns (freelancer payments, USD banking)

### Week 3
9. Launch Depositor 3% LAL (TR + NG) for incremental scale
10. Start ASA campaigns in NG market (competitor + generic)
11. Launch EG-specific Meta campaigns with Arabic creatives + card-centric messaging
12. Website Visitor 3% LAL for broad awareness (all markets)

### Week 4 (Review & Optimize)
13. Evaluate all LAL tiers: compare 1% vs 3% CPA and downstream conversion
14. Prune underperforming ASA keywords (generic)
15. Scale winning LALs to 5% if 1-3% are saturating
16. Review EG campaign data (should have 2+ weeks of withdrawal data by now)

---

## 7. Expected Impact

| Metric | Current (Week of Mar 14) | Target (4 weeks out) | Driver |
|--------|------------------------:|---------------------:|--------|
| Paid Install Quality (signup rate) | 13.6% | 20%+ | Shift budget from CPI networks to LAL + ASA |
| Paid → Withdrawal Rate | ~5% blended | 12%+ | Withdrawer LAL seeds find similar high-value users |
| ASA Withdrawals/week | 254 | 350+ | Budget increase + keyword expansion |
| Google Withdrawals/week | 29 | 60+ | PMax + Custom Intent launch |
| CPA (blended paid) | Unknown | Track from Week 1 | Baseline needed — set up cost tracking |

---

*Generated: March 21, 2026 | Next review: March 28, 2026*
