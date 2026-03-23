# Nigeria Google Search Pilot Plan

**Created:** 2026-03-23  
**Sprint:** 068  
**Status:** 📋 Ready to launch (demand-only pilot — KYC broken)  
**Owner:** Performance Marketing  
**Depends on:** [nigeria-growth-plan.md](nigeria-growth-plan.md), [negative-keywords-audit.md](negative-keywords-audit.md)

---

## 1. Current State

Nigeria Search is live but underinvested and volatile:

| Metric | Value | Notes |
|--------|------:|-------|
| Weekly spend | **$229** | Mar 9–15 |
| CAC (Cost/Virtual Account) | **$76** | Volatile — tiny sample, wide confidence interval |
| CPI (paid) | $0.35 | Cheapest market by far |
| KYC completions | **0** | NG KYC flow is broken (AI survey 70% reject + Bridgexyz handoff bug) |
| Organic installs | ~200/wk | Strong baseline even without paid |

**The $76 CAC is directionally interesting but statistically meaningless.** At $229/week the sample is too small for any reliable read. We need a structured pilot with controlled variables to determine whether NG Search can produce efficient, scalable acquisition.

---

## 2. Pilot Design

### Parameters

| Parameter | Value |
|-----------|-------|
| **Daily budget** | $15/day ($105/week) |
| **Duration** | 2 weeks (14 days) |
| **Total budget** | $210 |
| **Match types** | Exact match + Phrase match only |
| **Bid strategy** | Manual CPC |
| **Max CPC cap** | $0.30 |
| **Conversion action** | `virtual_account_opened` |
| **Campaign type** | Search (App Install or Search + deep link) |
| **Geo target** | Nigeria only |
| **Language** | English |
| **Device** | Mobile only (app install context) |

### Why This Budget

- $15/day is the minimum for directional signal at $0.30 CPC → ~50 clicks/day → ~700 clicks over 2 weeks
- At a conservative 5% install rate → ~35 installs → enough to measure CPI and early funnel
- Low enough to limit downside ($210 total) while proving or disproving demand

---

## 3. Keywords

Four high-intent keyword themes targeting Nigerian freelancers and cross-border workers actively seeking USD payment solutions:

### Exact Match
```
[receive USD Nigeria]
[freelancer payment Nigeria]
[dollar account Nigeria]
[upwork payment Nigeria]
```

### Phrase Match
```
"receive USD Nigeria"
"freelancer payment Nigeria"
"dollar account Nigeria"
"upwork payment Nigeria"
```

### Why These Keywords

| Keyword | Intent Signal |
|---------|--------------|
| `receive USD Nigeria` | Direct product-market fit — Cenoa's core use case |
| `freelancer payment Nigeria` | Matches NG's deposit-first behavior (45% of global deposit taps) |
| `dollar account Nigeria` | High commercial intent — seeking a product, not information |
| `upwork payment Nigeria` | Platform-specific pain point — Upwork → Naira conversion friction |

### Keywords NOT Included (Phase 1)

- Broad match of any kind (too noisy for pilot)
- Competitor terms (Payoneer, Wise — proven low ROI in TR, skip for now)
- Generic terms ("send money Nigeria", "money transfer") — too broad, low intent
- Crypto-adjacent terms — wrong audience

---

## 4. Negative Keywords

Full negative keyword list from the [negative-keywords-audit.md](negative-keywords-audit.md), adapted for NG:

### Account-Level Negatives (Apply from Shared Lists)

#### Employment & Career (13 keywords)
```
job, jobs, career, kariyer, iş ilanı, iş ilanları, salary, maaş, hiring, işe alım, çalışan, intern, staj
```

#### Customer Support (12 keywords)
```
login, giriş, şifre, password, müşteri hizmetleri, customer service, support, destek, şikayet, complaint, hesap silme, delete account
```

#### Investor & Financial (10 keywords)
```
stock, hisse, investor, yatırımcı, IPO, halka arz, valuation, değerleme, funding, sermaye
```

#### Crypto & Trading (14 keywords)
```
crypto, kripto, bitcoin, ethereum, forex, trading, borsa, coin, token, NFT, mining, madencilik, staking, DeFi
```

#### Lending & Credit (10 keywords)
```
loan, kredi, credit card, kredi kartı, mortgage, ipotek, faiz oranı, interest rate, borç, debt
```

#### Insurance & Unrelated Finance (5 keywords)
```
sigorta, insurance, emeklilik, pension, retirement
```

#### Legal & Regulatory (7 keywords)
```
lawsuit, dava, yasal mı, legal, regulation, düzenleme, TCMB
```

#### Academic & Research (5 keywords)
```
nedir, tez, thesis, araştırma, research
```

### Campaign-Level Negatives (NG Pilot Specific)

#### Competitor Brands (12 keywords — broad match)
```
payoneer, wise, transferwise, remitly, western union, moneygram, papara, ininal, tosla, revolut, N26, bunq
```

#### Low-Intent / Navigational (6 keywords)
```
app store, play store, indir, download, ücretsiz, free
```

#### NG-Specific Additions (8 keywords)
```
CBN, naira exchange rate, black market, parallel market, bureau de change, BDC, aboki, forex bureau
```

**Total negatives: ~102 keywords/phrases**

---

## 5. Bidding & Budget Rules

| Rule | Setting | Rationale |
|------|---------|-----------|
| **Bid strategy** | Manual CPC | Full control during pilot — no algorithmic learning on tiny data |
| **Max CPC** | $0.30 | NG Search CPCs are typically $0.05–0.25; cap prevents outlier clicks |
| **Daily budget** | $15 | Hard cap, no overspend |
| **Ad scheduling** | All hours (monitor, adjust in week 2 if patterns emerge) |
| **Bid adjustments** | None initially — too little data for device/location/time modifiers |

### Budget Pacing

| Week | Daily Budget | Cumulative Spend | Action |
|------|------------:|------------------:|--------|
| Week 1 (Days 1–7) | $15 | $105 | Observe — no changes |
| Week 2 (Days 8–14) | $15 | $210 | Optimize: pause low-CTR keywords, adjust bids |

**Do NOT touch anything in Week 1.** Let data accumulate. The temptation to optimize on Day 3 is strong and wrong — 3 days of $15/day is not a sample.

---

## 6. Success Criteria & Decision Framework

### Primary Metric: Cost per Virtual Account Opened (CAC)

| CAC Result | Decision | Next Step |
|:----------:|:--------:|-----------|
| **< $50** | ✅ **Scale** | Increase to $30/day, add phrase match expansion, move to Phase 1 of nigeria-growth-plan.md ($1,000/mo) |
| **$50 – $100** | 🟡 **Optimize** | Keep $15/day, test new keywords, tighten negatives, review search terms report, run 2 more weeks |
| **> $100** | 🔴 **Pause** | Stop NG Search spend, reallocate to Pmax TR or EG Generic, revisit after KYC fix |

### Secondary Metrics (Directional)

| Metric | Target | Red Flag |
|--------|--------|----------|
| CPC | < $0.20 | > $0.30 (hitting cap consistently) |
| CTR | > 3% | < 1% (keyword mismatch) |
| Install rate (click → install) | > 5% | < 2% (landing page or store listing issue) |
| CPI | < $5 | > $10 |

### Minimum Data Thresholds

Don't make any scaling decisions until:
- ≥ 500 clicks
- ≥ 25 installs
- ≥ 5 virtual accounts opened (conversion events)

If after 2 weeks you have < 5 conversions, extend the pilot 1 more week before deciding.

---

## 7. KYC Dependency & What This Pilot Actually Proves

### ⚠️ Critical Context: NG KYC Is Broken

| KYC Stage | Status | Impact |
|-----------|--------|--------|
| Pre-KYC AI Survey | 🔴 70% rejection rate | Only 30% of users pass |
| Bridgexyz Handoff | 🔴 Bug — 0% reach KYC | Even approved users never see KYC |
| KYC Completion | 🔴 0 completions/week | No users can fully verify |

### What This Pilot Proves (Demand Only)

This is a **demand validation pilot**, not a full-funnel acquisition test:

1. **Can we acquire clicks at < $0.30 CPC?** → Proves Search inventory exists at viable prices
2. **Can we drive installs at < $5 CPI?** → Proves ad-to-install conversion works
3. **Can we get virtual account opens at < $50 CAC?** → Proves top-of-funnel intent quality
4. **What search terms do Nigerian users actually use?** → Search Terms Report = free keyword research

### What This Pilot Does NOT Prove

- KYC completion rates (blocked by bug)
- Deposit/withdrawal behavior of paid users (need KYC first)
- True Cost per Paid Active user (need full funnel)
- Long-term retention or LTV

### Interpretation Guide

| Pilot Result | + KYC Fixed | Strategic Implication |
|:------------:|:-----------:|----------------------|
| CAC < $50 | KYC fix deployed | 🚀 Immediate scale — NG becomes primary growth market |
| CAC < $50 | KYC still broken | 📋 Proven demand, budget pre-approved, deploy day KYC ships |
| CAC > $100 | KYC fix deployed | 🔄 Rely on organic (200/wk free) + referral program instead |
| CAC > $100 | KYC still broken | ⏸️ Pause all NG paid, focus entirely on TR + EG |

---

## 8. Implementation Checklist

### Pre-Launch (Day 0)

- [ ] Create campaign: `NG Search Pilot — Freelancer Intent`
- [ ] Add 4 exact match keywords + 4 phrase match keywords
- [ ] Apply account-level negative keyword lists (Universal + Fintech = 76 keywords)
- [ ] Add campaign-level negatives (competitor brands + low-intent + NG-specific = 26 keywords)
- [ ] Set manual CPC at $0.20 initial bid, $0.30 max
- [ ] Set daily budget $15
- [ ] Set geo: Nigeria only, language: English, device: mobile
- [ ] Set conversion action: `virtual_account_opened`
- [ ] Create 2–3 ad variations (focus: "Get paid in USD", "Dollar account for freelancers", "Receive USD payments")
- [ ] Verify tracking: AppsFlyer attribution for Google Ads NG → install → virtual account opened

### Week 1 Review (Day 7)

- [ ] Pull Search Terms Report — review actual queries triggering ads
- [ ] Add any new negative keywords discovered
- [ ] Check: Are we spending the full $15/day? (If not, increase bids or add keywords)
- [ ] Check: CPC within range? CTR acceptable?
- [ ] **Do not optimize keywords or bids yet**

### Week 2 Review (Day 14) — Decision Point

- [ ] Pull full 14-day performance data
- [ ] Calculate: CPC, CPI, CAC (virtual account opened)
- [ ] Pull Search Terms Report — full 2-week view
- [ ] Apply decision framework (Scale / Optimize / Pause)
- [ ] Document findings in `ng-search-pilot-results.md`

---

## 9. Ad Copy Suggestions

### Headline Options (30 char max)
```
Get Paid in USD — Nigeria
Dollar Account for Freelancers
Receive USD Payments Fast
Upwork Pay → Your USD Account
USD Account — No Hidden Fees
```

### Description Options (90 char max)
```
Open a free USD account. Receive freelancer payments from Upwork, Fiverr & more. Download now.
Get paid in dollars. Fast, secure transfers to your Nigerian bank account. Try Cenoa free.
Freelancers: stop losing money on conversion fees. Receive USD directly with Cenoa.
```

### Best Practices for NG
- Lead with USD/dollar — it's the #1 pain point
- Mention specific platforms (Upwork, Fiverr) — builds relevance
- "Free" is a strong CTA in price-sensitive markets
- Avoid mentioning crypto/blockchain — triggers wrong audience

---

*This pilot runs independently of KYC status. It proves demand at the top of the funnel. Scale decisions depend on both pilot CAC results AND KYC fix deployment.*
