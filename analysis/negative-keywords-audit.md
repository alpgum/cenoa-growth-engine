# Google Search Negative Keywords Audit

**Created:** 2026-03-22  
**Sprint:** 068  
**Sources:** google-ads-deepdive.md, bid-strategy-reco.md, demand-gen-fix-plan.md, sheets-trafik-canavari.json  
**Status:** 📋 Ready for implementation

---

## Executive Summary

Cenoa's Google Ads account currently runs **6+ active campaigns** across Search (Brand, Generic, Competitor), Pmax, Demand Gen, and App Install — spending ~$3,500–4,000/week. Without a structured negative keyword strategy, an estimated **15–25% of Search campaign spend** is likely wasted on irrelevant queries. That's **$400–$800/month** in recoverable budget across Search campaigns alone (Brand + Generic + Competitor spend ~$1,300–1,900/wk).

This audit provides a ready-to-implement negative keyword list, organized by theme, with campaign-level and account-level implementation guidance.

---

## 1. Likely Wasted Search Terms by Campaign Type

### 1a. Brand Campaigns (Search TR Pure Brand — ~$790/wk)

Brand campaigns targeting "Cenoa" and variants are vulnerable to:

| Waste Category | Example Queries | Why It's Waste |
|---|---|---|
| **Misspellings hitting unrelated brands** | "cenoa ceramics", "cenoa restaurant", "cenoa italy" | Cenoa is also a place name (Genoa/Italy) and various business names |
| **Support/login queries from existing users** | "cenoa login", "cenoa app giriş", "cenoa müşteri hizmetleri" | Existing users don't need acquisition spend |
| **HR/career queries** | "cenoa iş ilanları", "cenoa kariyer", "cenoa maaş" | Job seekers, not potential customers |
| **Investor/stock queries** | "cenoa yatırım", "cenoa hisse", "cenoa stock" | Investor research, not user acquisition |
| **News/review queries** | "cenoa şikayet", "cenoa dolandırıcı mı", "cenoa güvenilir mi" | These may convert organically — paying for them is waste if organic ranks well |
| **App store navigation** | "cenoa app store", "cenoa play store", "cenoa indir" | Users will find the app organically; paying for navigational queries is low-value |

**Estimated waste:** 10–15% of brand spend (~$80–120/wk, ~$350–500/mo)

### 1b. Generic Campaigns (TR Freelancer + EG Generic — ~$500–1,000/wk)

Generic campaigns targeting "freelancer platform", "döviz hesabı", "e-ihracat" etc. attract:

| Waste Category | Example Queries | Why It's Waste |
|---|---|---|
| **Informational-only queries** | "freelancer nedir", "e-ihracat nasıl yapılır", "döviz hesabı nedir" | Top-of-funnel info seekers with no intent to sign up |
| **How-to/tutorial queries** | "freelancer nasıl para kazanılır", "upwork nasıl kullanılır" | Content consumption, not product evaluation |
| **Unrelated verticals** | "freelancer web developer", "freelancer graphic designer iş ilanı" | Looking for freelancers to hire, not a fintech platform |
| **Free/cheap seekers** | "ücretsiz döviz hesabı", "bedava swift", "free international transfer" | May convert but often low-LTV users |
| **Academic/research** | "e-ihracat tez", "döviz kuru araştırma", "freelance ekonomi" | Students/researchers, not customers |
| **Government/regulatory** | "e-ihracat teşvik", "döviz hesabı yasal mı", "TCMB döviz" | Looking for regulations, not products |

**Estimated waste:** 20–30% of generic spend (~$100–300/wk, ~$450–1,300/mo)

### 1c. Competitor Campaigns (TR Rakipler Payoneer — ~$200–300/wk)

Already the worst-performing campaign (CPI: ₺938–1,047, <1 install/week). Waste sources:

| Waste Category | Example Queries | Why It's Waste |
|---|---|---|
| **Competitor support queries** | "payoneer login", "payoneer müşteri hizmetleri", "payoneer support" | Users need help with their existing Payoneer account — zero switching intent |
| **Competitor account management** | "payoneer hesap silme", "payoneer şifre değiştirme", "payoneer verification" | Active users managing their account |
| **Competitor + unrelated modifiers** | "payoneer mastercard", "payoneer atm", "wise debit card" | Product feature queries for their current provider |
| **Competitor pricing/fees** | "payoneer komisyon oranları", "wise transfer ücreti" | May have some switching intent, but usually just comparison shopping |
| **Competitor careers** | "payoneer jobs", "wise kariyer" | Job seekers at competitor companies |

**Estimated waste:** 40–60% of competitor spend (~$80–180/wk, ~$350–780/mo)

> **Note:** The bid-strategy-reco.md already recommends cutting competitor campaign to ₺500/mo monitoring budget. Negative keywords are critical if keeping even this minimal spend.

---

## 2. Recommended Negative Keyword List (75+ keywords)

### 2a. Universal Negatives (Apply to ALL campaigns)

These should be added at **account level** (negative keyword list shared across all campaigns).

#### Employment & Career (13 keywords)
```
job
jobs
career
kariyer
iş ilanı
iş ilanları
salary
maaş
hiring
işe alım
çalışan
intern
staj
```

#### Customer Support (12 keywords)
```
login
giriş
şifre
password
müşteri hizmetleri
customer service
support
destek
şikayet
complaint
hesap silme
delete account
```

#### Investor & Financial (10 keywords)
```
stock
hisse
investor
yatırımcı
IPO
halka arz
valuation
değerleme
funding
sermaye
```

#### Legal & Regulatory (7 keywords)
```
lawsuit
dava
yasal mı
legal
regulation
düzenleme
TCMB
```

#### Academic & Research (5 keywords)
```
nedir
tez
thesis
araştırma
research
```

**Total universal: 47 keywords**

### 2b. Fintech-Specific Negatives (Apply to ALL campaigns)

Add at **account level** — Cenoa is a cross-border payment/e-ihracat platform, NOT crypto/trading/lending.

#### Crypto & Trading (14 keywords)
```
crypto
kripto
bitcoin
ethereum
forex
trading
borsa
coin
token
NFT
mining
madencilik
staking
DeFi
```

#### Lending & Credit (10 keywords)
```
loan
kredi
credit card
kredi kartı
mortgage
ipotek
faiz oranı
interest rate
borç
debt
```

#### Insurance & Unrelated Finance (5 keywords)
```
sigorta
insurance
emeklilik
pension
retirement
```

**Total fintech: 29 keywords**

### 2c. Competitor-Specific Negatives for Generic Campaigns

Apply at **campaign level** on Generic and Brand campaigns only (NOT on Competitor campaigns, obviously).

#### Competitor Brand Terms to Exclude from Generic/Brand (12 keywords)
```
payoneer
wise
transferwise
remitly
western union
moneygram
papara
ininal
tosla
revolut
N26
bunq
```

#### Competitor + Support Modifiers for Competitor Campaigns (8 phrases)
Add as **phrase match negatives** to the Competitor campaign:
```
"payoneer login"
"payoneer giriş"
"payoneer support"
"payoneer destek"
"payoneer müşteri hizmetleri"
"payoneer hesap silme"
"payoneer şifre"
"payoneer verification"
```

And equivalents for Wise if running Wise competitor terms:
```
"wise login"
"wise giriş"  
"wise support"
"wise destek"
"wise müşteri hizmetleri"
"wise hesap silme"
```

**Total competitor: 26 keywords/phrases**

### 2d. Geo Negatives (If Running Broad Match or Broad Geo)

Cenoa currently operates in TR, EG, NG. If campaigns target broader regions or use broad match:

#### Countries NOT Served (add as exact/phrase match)
```
india
hindistan
pakistan
bangladesh
philippines
filipinler
indonesia
endonezya
vietnam
iran
iraq
irak
syria
suriye
russia
rusya
china
çin
```

**Total geo: 18 keywords**

### 2e. Low-Intent / Navigational Negatives (6 keywords)
```
app store
play store
indir
download
ücretsiz
free
```

---

### Complete Negative Keyword Summary

| Category | Count | Level |
|---|---:|---|
| Universal (employment, support, investor, legal, academic) | 47 | Account |
| Fintech-specific (crypto, lending, insurance) | 29 | Account |
| Competitor-specific for generic campaigns | 26 | Campaign |
| Geo negatives | 18 | Account or Campaign |
| Low-intent / navigational | 6 | Campaign |
| **Total** | **126** | |

---

## 3. Implementation Guide

### Step 1: Create Shared Negative Keyword Lists (Account Level)

Google Ads allows **shared negative keyword lists** that apply across multiple campaigns. This is the most efficient approach.

**In Google Ads Console:**
1. Go to **Tools & Settings → Shared Library → Negative Keyword Lists**
2. Create **3 lists:**

| List Name | Keywords | Apply To |
|---|---|---|
| `[NEG] Universal - All Campaigns` | Universal (47) + Fintech (29) = 76 keywords | All Search & Pmax campaigns |
| `[NEG] Competitor Brands - Generic Only` | Competitor brand terms (12) | Generic campaigns only (NOT competitor campaigns) |
| `[NEG] Geo - Unserved Countries` | Geo negatives (18) | All campaigns with broad geo targeting |

### Step 2: Add Campaign-Level Negatives

For campaign-specific negatives that shouldn't apply everywhere:

| Campaign | Add These Negatives | Match Type |
|---|---|---|
| **TR Rakipler Payoneer** | Competitor + support phrases (14 phrases) | Phrase match |
| **TR Pure Brand** | Low-intent navigational (6) | Exact/phrase match |
| **TR Freelancer / EG Generic** | Competitor brands (12) + low-intent (6) | Phrase/exact match |

### Step 3: Match Type Strategy

| Negative Match Type | When to Use | Example |
|---|---|---|
| **Broad match negative** (default) | Block a concept entirely | `crypto` blocks "crypto wallet", "buy crypto", etc. |
| **Phrase match negative** | Block specific phrases while allowing the word in other contexts | `"payoneer login"` blocks that phrase but allows "payoneer alternative" |
| **Exact match negative** | Block only that exact query | `[nedir]` blocks "nedir" but allows "cenoa nedir" |

**Recommendation:** Use **broad match** for most negatives (employment, crypto, lending, insurance). Use **phrase match** for competitor + support modifiers. Use **exact match** sparingly for Turkish terms that could appear in valid queries.

### Step 4: Pmax Considerations

⚠️ **Performance Max campaigns have limited negative keyword support.** As of 2026:
- You can add account-level negative keyword lists that apply to Pmax
- Campaign-level negatives for Pmax require contacting Google Ads support or using the API
- Pmax negative keywords only affect the Search component (not Display, YouTube, Discover)

**Action:** Add the account-level shared lists — they will automatically apply to Pmax's Search inventory.

---

## 4. Estimated Waste Reduction

### Current Estimated Waste

| Campaign Type | Weekly Spend | Est. Waste % | Est. Waste $/wk | Est. Waste $/mo |
|---|---:|---:|---:|---:|
| Search Brand (TR) | $790 | 10–15% | $79–119 | $340–510 |
| Search Generic (TR + EG) | $500–1,000 | 20–30% | $100–300 | $430–1,300 |
| Search Competitor (TR) | $200–300 | 40–60% | $80–180 | $345–780 |
| **Total Search waste** | | | **$259–599/wk** | **$1,115–2,590/mo** |

### Expected Recovery After Implementation

Negative keywords typically recover **50–70% of identifiable waste** (some wasted clicks come from queries that are hard to predict or block proactively).

| Scenario | Monthly Waste Recovered | Annual Impact |
|---|---:|---:|
| Conservative (50% of low estimate) | **$558/mo** | **$6,690/yr** |
| Expected (60% of mid estimate) | **$1,110/mo** | **$13,320/yr** |
| Optimistic (70% of high estimate) | **$1,813/mo** | **$21,756/yr** |

### Where the Savings Go

Recovered budget should be reallocated to top performers:

| Reallocation Target | Why | Expected Incremental Installs |
|---|---|---|
| **Pmax TR (+$500/mo)** | Best Cost/Active at $19.18 | ~16 installs/mo |
| **EG Generic (+$300/mo)** | Best CPI at ~$9 (post KYC fix) | ~33 installs/mo |
| **Search Brand (+$300/mo)** | Highest downstream quality | ~10 installs/mo |

**Net impact:** Same total budget, ~40–60 additional installs/month from waste elimination + reallocation.

### Indirect Benefits

- **Improved Quality Score:** Fewer irrelevant clicks → higher CTR → better Ad Rank → lower CPC over time
- **Cleaner conversion data:** Smart bidding algorithms learn from better signal when junk clicks are removed
- **More accurate CPA:** Removes noise from campaign metrics, enabling better optimization decisions

---

## 5. Review Cadence: Weekly Search Term Report

### Weekly Ritual (Every Monday, 15 minutes)

| Step | Action | Where |
|---|---|---|
| 1 | Pull **Search Terms Report** for last 7 days | Google Ads → Campaigns → Keywords → Search Terms |
| 2 | Sort by **Cost (highest first)** | Look for high-spend, zero-conversion terms |
| 3 | Sort by **Impressions (highest first)** | Look for high-impression, low-CTR terms (irrelevant matches) |
| 4 | Flag any query with **spend > ₺50 and 0 conversions** | These are your immediate negative keyword candidates |
| 5 | Add new negatives to the appropriate shared list | Account-level for universal, campaign-level for specific |
| 6 | Log findings in a running doc | Track patterns over time to identify new negative themes |

### Monthly Deep Dive (First Monday of each month, 30 minutes)

| Step | Action |
|---|---|
| 1 | Pull Search Terms Report for **full month** |
| 2 | Export to spreadsheet for analysis |
| 3 | Group queries by theme — identify new waste patterns |
| 4 | Check if any negative keywords are **blocking valid queries** (compare impression share before/after) |
| 5 | Review negative keyword lists for outdated entries |
| 6 | Cross-reference with **Auction Insights** — new competitors appearing? Add to exclusion list for generic campaigns |

### Quarterly Audit (Every 3 months, 1 hour)

| Step | Action |
|---|---|
| 1 | Full negative keyword list review across all campaigns |
| 2 | Check for conflicts (negative keywords blocking intended keywords) |
| 3 | Review match type strategy — are broad match negatives too aggressive? |
| 4 | Benchmark waste % vs 3 months ago — are we trending down? |
| 5 | Update this document with new findings and keyword additions |

### Automated Alerts (Set up in Google Ads)

Create these automated rules in Google Ads → Tools → Rules:

| Rule | Trigger | Action |
|---|---|---|
| **High-spend zero-conversion alert** | Any search term with spend > ₺200 and conversions = 0 in 7 days | Email alert |
| **New search term spike** | Any new search term with >50 impressions in 1 day | Email alert (weekly digest) |
| **CTR drop alert** | Campaign CTR drops >20% week-over-week | Email alert |

---

## 6. Priority Implementation Timeline

| Day | Action | Time Required |
|---|---|---|
| **Day 1** | Create 3 shared negative keyword lists in Google Ads | 30 min |
| **Day 1** | Add all 76 account-level negatives (Universal + Fintech) | 20 min |
| **Day 1** | Apply lists to all campaigns | 10 min |
| **Day 2** | Add campaign-level negatives (competitor phrases, low-intent) | 20 min |
| **Day 2** | Add geo negatives if broad targeting is confirmed | 10 min |
| **Day 3** | Pull first Search Terms Report — validate no valid queries are blocked | 15 min |
| **Day 7** | First weekly review — add any new negatives found | 15 min |
| **Day 14** | Check impression share and CPA changes post-implementation | 15 min |
| **Day 30** | First monthly deep dive with full month of post-implementation data | 30 min |

### Quick Wins (Do These First)

1. ✅ Add `crypto`, `bitcoin`, `forex`, `trading` to all campaigns (likely the single biggest waste source for a fintech brand)
2. ✅ Add `login`, `giriş`, `şifre`, `password` to all campaigns (existing user queries)
3. ✅ Add `"payoneer login"`, `"payoneer support"` as phrase match to competitor campaign
4. ✅ Add `job`, `kariyer`, `iş ilanı` to all campaigns

These 4 actions alone likely capture 40–50% of total recoverable waste.

---

## Appendix: Turkish Language Considerations

Many queries will be in Turkish. Key translations for common negative themes:

| English | Turkish | Notes |
|---|---|---|
| job | iş | Also means "work" — use phrase match `"iş ilanı"` to be safe |
| career | kariyer | Safe as broad negative |
| salary | maaş | Safe as broad negative |
| login | giriş | Also means "entrance" — use phrase match if concerned |
| complaint | şikayet | Common on şikayetvar.com — these users are upset, not prospects |
| free | ücretsiz / bedava | May block valid queries like "ücretsiz hesap aç" — use carefully |
| how to | nasıl | Very common in Turkish — use as phrase match only, e.g., `"nasıl yapılır"` |
| what is | nedir | Informational — consider exact match `[nedir]` to avoid blocking "cenoa nedir" |

### Negative Keyword Conflicts to Watch

| Negative | Could Block | Solution |
|---|---|---|
| `free` / `ücretsiz` | "Cenoa free account" / "cenoa ücretsiz hesap" | Use phrase match `"ücretsiz transfer"` instead of broad |
| `nedir` | "cenoa nedir" (valid brand query) | Add as exact `[nedir]` only in generic campaigns, not brand |
| `iş` | "e-ihracat işlemleri" (valid generic query) | Use phrase match `"iş ilanı"` and `"iş başvurusu"` instead |
| `giriş` | "cenoa giriş" (navigational, low value but not zero) | Add only to generic campaigns; keep off brand if brand impression share matters |

---

*Sprint 068 | Negative Keywords Audit | 2026-03-22*
