# Apple Search Ads — Keyword Expansion Plan

**Created:** March 22, 2026  
**Sprint:** 068  
**Sources:** bid-strategy-reco.md, competitive-positioning.md, seo-content-plan.md, ASA industry benchmarks  
**Markets:** TR (primary), EG, NG  
**Status:** 📋 Ready for implementation

---

## 1. Current State Assessment

### Likely Current ASA Keywords
Cenoa is likely running brand-only or minimal ASA campaigns:
- `cenoa` (brand — exact match)
- `cenoa app` (brand — exact match)
- Possibly a small discovery campaign (broad match, Search Match enabled)

### ASA Benchmark Context (Finance/Payments Category)
| Metric | US Benchmark | TR/EG/NG Est. |
|---|---|---|
| **CPI (Finance — Banking/Payments)** | $5.00–$15.00 | $1.50–$6.00 |
| **CPT (Cost Per Tap)** | $2.00–$5.00 | $0.50–$2.00 |
| **TTR (Tap-Through Rate)** | 2%–5% | 3%–7% (less competition) |
| **CR (Conversion Rate)** | 20%–40% | 25%–50% |

TR/EG/NG markets are significantly cheaper than US for ASA due to lower auction competition in the fintech/payments category. This is a major opportunity.

---

## 2. Keyword Expansion — Full Taxonomy

### Group A: Brand Keywords (20% of budget)

**Purpose:** Defend brand searches, capture high-intent users. Cheapest CPI, highest CR.

| Keyword | Match Type | Volume Tier | Est. CPI (TR) | Priority |
|---|---|---|---|---|
| `cenoa` | Exact | Low | $0.30–$0.80 | 🔴 Must-have |
| `cenoa app` | Exact | Low | $0.30–$0.80 | 🔴 Must-have |
| `cenoa uygulama` | Exact | Low | $0.20–$0.50 | 🔴 Must-have |
| `cenoa review` | Exact | Low | $0.30–$0.80 | 🟡 Medium |
| `cenoa hesap` | Exact | Low | $0.20–$0.50 | 🟡 Medium |
| `cenoa nedir` | Exact | Low | $0.20–$0.50 | 🟡 Medium |

**Bid Strategy:**
- **Aggressive exact match** — bid high to maintain 95%+ impression share
- Max CPT bid: $1.50 (TR), $2.00 (EG/NG)
- CPI target: <$1.00
- These keywords have highest CR (~50–70%) since users already know the brand
- Run as separate "Brand Defense" campaign

**Negative keywords:** None needed — brand terms are precise.

---

### Group B: Competitor Brand Keywords (30% of budget)

**Purpose:** Intercept users searching for competitor apps. Higher CPI but captures switcher intent.

#### B1: Direct Competitor Terms (Payments/Remittance)

| Keyword | Match Type | Volume Tier | Est. CPI (TR) | Priority |
|---|---|---|---|---|
| `payoneer` | Exact | High | $3.00–$8.00 | 🔴 Must-have |
| `payoneer app` | Exact | High | $3.00–$8.00 | 🔴 Must-have |
| `payoneer alternative` | Exact | Medium | $2.00–$5.00 | 🔴 Must-have |
| `payoneer alternatif` | Exact | Medium | $1.50–$4.00 | 🔴 Must-have |
| `wise` | Exact | High | $3.00–$7.00 | 🔴 Must-have |
| `wise app` | Exact | High | $3.00–$7.00 | 🔴 Must-have |
| `transferwise` | Exact | Medium | $2.50–$6.00 | 🟡 Medium |
| `wise transfer` | Exact | Medium | $2.00–$5.00 | 🟡 Medium |
| `paypal` | Exact | Very High | $5.00–$12.00 | ⚠️ Test only |
| `paypal alternatif` | Exact | Medium | $2.00–$5.00 | 🟡 Medium |
| `deel` | Exact | Medium | $2.00–$5.00 | 🟡 Medium |
| `deel app` | Exact | Medium | $2.00–$5.00 | 🟢 Nice-to-have |
| `remitly` | Exact | Medium | $2.00–$5.00 | 🟡 Medium |
| `xoom` | Exact | Low–Medium | $1.50–$4.00 | 🟢 Nice-to-have |
| `grey.co` | Exact | Low | $1.00–$3.00 | 🟡 Medium (NG) |

#### B2: Competitor Comparison Terms

| Keyword | Match Type | Volume Tier | Est. CPI | Priority |
|---|---|---|---|---|
| `payoneer vs wise` | Exact | Medium | $2.00–$5.00 | 🟡 Medium |
| `payoneer veya wise` | Exact | Low | $1.00–$3.00 | 🟢 Nice-to-have |
| `wise vs paypal` | Exact | Medium | $2.50–$6.00 | 🟢 Nice-to-have |
| `best payoneer alternative` | Broad | Low–Medium | $2.00–$5.00 | 🟡 Medium |
| `payoneer yerine` | Exact | Low | $1.00–$3.00 | 🟡 Medium |

**Bid Strategy:**
- **Moderate exact match** — control spend per keyword tightly
- Max CPT bid: $3.00 (TR), $4.00 (EG/NG for payoneer/wise)
- CPI target: <$6.00 (TR), <$8.00 (EG/NG)
- Lower CR expected (~15–30%) — users have competitor intent, not Cenoa intent
- Run separate "Competitor Conquest" campaign per tier:
  - Tier 1 (payoneer, wise): Higher bids, always-on
  - Tier 2 (paypal, deel, remitly, xoom): Lower bids, test-and-learn
- **PayPal warning:** Very high volume but extremely broad intent. Start with $50/week cap and evaluate. Most PayPal searchers want the PayPal app specifically — low CR expected.

**Negative keywords for competitor campaigns:**
- `payoneer login` / `payoneer giriş`
- `payoneer support` / `payoneer destek`
- `payoneer customer service`
- `wise login` / `wise giriş`
- `paypal login` / `paypal şifremi unuttum`
- `deel login` / `deel sign in`
- `remitly tracking` / `remitly order status`

---

### Group C: Category Keywords (30% of budget)

**Purpose:** Capture users searching for a solution, not a specific brand. Best volume-to-intent ratio.

#### C1: Core Category Terms

| Keyword | Match Type | Volume Tier | Est. CPI (TR) | Priority |
|---|---|---|---|---|
| `money transfer` | Broad | Very High | $3.00–$8.00 | 🟡 Medium |
| `para transferi` | Exact | High | $2.00–$5.00 | 🔴 Must-have |
| `uluslararası para transferi` | Exact | Medium | $1.50–$4.00 | 🔴 Must-have |
| `international payments` | Broad | High | $3.00–$7.00 | 🟡 Medium |
| `send money abroad` | Exact | Medium | $2.00–$5.00 | 🟡 Medium |
| `yurtdışına para gönderme` | Exact | Medium | $1.50–$4.00 | 🔴 Must-have |
| `döviz transferi` | Exact | Medium | $1.50–$4.00 | 🟡 Medium |

#### C2: USD Account / Banking Terms

| Keyword | Match Type | Volume Tier | Est. CPI (TR) | Priority |
|---|---|---|---|---|
| `usd account` | Exact | Medium | $2.00–$5.00 | 🔴 Must-have |
| `dolar hesabı` | Exact | Medium | $1.50–$4.00 | 🔴 Must-have |
| `us bank account` | Exact | Medium | $2.50–$6.00 | 🔴 Must-have |
| `virtual bank account` | Broad | Medium | $2.00–$5.00 | 🟡 Medium |
| `sanal banka hesabı` | Exact | Low–Medium | $1.00–$3.00 | 🟡 Medium |
| `amerikan banka hesabı` | Exact | Low–Medium | $1.00–$3.00 | 🔴 Must-have |
| `ABD banka hesabı` | Exact | Low–Medium | $1.00–$3.00 | 🔴 Must-have |

#### C3: Freelancer / Creator Economy Terms

| Keyword | Match Type | Volume Tier | Est. CPI (TR) | Priority |
|---|---|---|---|---|
| `freelancer bank` | Exact | Low–Medium | $1.50–$4.00 | 🔴 Must-have |
| `freelancer banka hesabı` | Exact | Low | $1.00–$3.00 | 🔴 Must-have |
| `freelancer ödeme` | Exact | Low–Medium | $1.00–$3.00 | 🔴 Must-have |
| `freelance payment` | Broad | Medium | $2.00–$5.00 | 🟡 Medium |
| `get paid internationally` | Broad | Low–Medium | $2.00–$5.00 | 🟡 Medium |
| `receive usd` | Exact | Low | $1.50–$4.00 | 🔴 Must-have |
| `dolar almak` | Exact | Low | $1.00–$3.00 | 🟡 Medium |
| `e-ihracat ödeme` | Exact | Low | $0.80–$2.50 | 🔴 Must-have |

**Bid Strategy:**
- **Exact match for Turkish terms** (lower competition, higher relevance)
- **Broad match for English terms** with aggressive negative keyword mining
- Max CPT bid: $2.50 (TR), $3.50 (EG/NG)
- CPI target: <$5.00 (TR), <$7.00 (EG/NG)
- Run as "Category — Generic" campaign with ad groups:
  - AG1: Money Transfer / Payments
  - AG2: USD Account / Banking
  - AG3: Freelancer / Creator
- Use Search Match = OFF (control keywords manually)
- Run a parallel **Discovery campaign** (broad match + Search Match ON, low budget $30/week) to find new category terms

---

### Group D: Long-Tail / Platform-Specific Keywords (20% of budget)

**Purpose:** Highly specific intent keywords. Lower volume but excellent CR and lower CPT.

#### D1: Freelance Platform Payment Terms

| Keyword | Match Type | Volume Tier | Est. CPI (TR) | Priority |
|---|---|---|---|---|
| `upwork payment` | Exact | Medium | $1.50–$4.00 | 🔴 Must-have |
| `upwork ödeme` | Exact | Low–Medium | $1.00–$3.00 | 🔴 Must-have |
| `upwork withdrawal` | Exact | Low–Medium | $1.50–$4.00 | 🔴 Must-have |
| `upwork para çekme` | Exact | Low | $0.80–$2.50 | 🟡 Medium |
| `fiverr payment` | Exact | Medium | $1.50–$4.00 | 🔴 Must-have |
| `fiverr ödeme` | Exact | Low–Medium | $1.00–$3.00 | 🔴 Must-have |
| `fiverr withdrawal` | Exact | Low–Medium | $1.50–$4.00 | 🔴 Must-have |
| `fiverr para çekme` | Exact | Low | $0.80–$2.50 | 🟡 Medium |
| `freelancer bank account` | Exact | Low | $1.50–$4.00 | 🟡 Medium |
| `receive usd turkey` | Exact | Low | $1.00–$3.00 | 🟡 Medium |
| `upwork türkiye` | Exact | Low | $0.80–$2.50 | 🟡 Medium |
| `fiverr türkiye` | Exact | Low | $0.80–$2.50 | 🟡 Medium |

#### D2: Corridor-Specific Terms

| Keyword | Match Type | Volume Tier | Est. CPI | Priority | Market |
|---|---|---|---|---|---|
| `send money to turkey` | Exact | Medium | $2.00–$5.00 | 🟡 Medium | TR |
| `türkiye'ye para gönderme` | Exact | Low–Medium | $1.00–$3.00 | 🟡 Medium | TR |
| `send money to nigeria` | Exact | Medium | $2.00–$5.00 | 🟡 Medium | NG |
| `send money to egypt` | Exact | Medium | $2.00–$5.00 | 🟡 Medium | EG |
| `nigeria money transfer` | Exact | Medium | $2.00–$4.00 | 🟡 Medium | NG |
| `egypt money transfer` | Exact | Low–Medium | $1.50–$4.00 | 🟡 Medium | EG |

#### D3: Country-Specific Local Language Terms

**Turkey (Turkish)**

| Keyword | Match Type | Volume Tier | Est. CPI | Priority |
|---|---|---|---|---|
| `ABD banka hesabı` | Exact | Low | $0.80–$2.00 | 🔴 Must-have |
| `amerika banka hesabı` | Exact | Low | $0.80–$2.00 | 🔴 Must-have |
| `yurtdışından para alma` | Exact | Low–Medium | $1.00–$3.00 | 🔴 Must-have |
| `dolar hesabı açma` | Exact | Low | $0.80–$2.50 | 🔴 Must-have |
| `freelancer dolar hesabı` | Exact | Low | $0.50–$1.50 | 🔴 Must-have |
| `ucuz döviz transferi` | Exact | Low | $0.80–$2.00 | 🟡 Medium |
| `e-ihracat hesabı` | Exact | Low | $0.50–$1.50 | 🟡 Medium |
| `yurtdışı freelance ödeme` | Exact | Low | $0.50–$1.50 | 🔴 Must-have |

**Egypt (Arabic)**

| Keyword | Match Type | Volume Tier | Est. CPI | Priority |
|---|---|---|---|---|
| `حساب بنكي أمريكي` (US bank account) | Exact | Low | $0.50–$2.00 | 🔴 Must-have |
| `تحويل أموال` (money transfer) | Exact | Medium | $1.00–$3.00 | 🟡 Medium |
| `استلام دولار` (receive dollars) | Exact | Low | $0.50–$2.00 | 🔴 Must-have |
| `حساب دولار` (dollar account) | Exact | Low | $0.50–$2.00 | 🔴 Must-have |
| `فريلانسر مصر` (freelancer Egypt) | Exact | Low | $0.30–$1.50 | 🟡 Medium |
| `بديل بايونير` (Payoneer alternative) | Exact | Low | $0.50–$2.00 | 🔴 Must-have |
| `سحب أموال أبورك` (withdraw money Upwork) | Exact | Low | $0.30–$1.50 | 🟡 Medium |

**Nigeria (English — local context)**

| Keyword | Match Type | Volume Tier | Est. CPI | Priority |
|---|---|---|---|---|
| `receive dollars nigeria` | Exact | Low | $0.50–$2.00 | 🔴 Must-have |
| `usd account nigeria` | Exact | Low | $0.80–$2.50 | 🔴 Must-have |
| `freelancer payment nigeria` | Exact | Low | $0.50–$2.00 | 🟡 Medium |
| `domiciliary account alternative` | Exact | Low | $0.50–$2.00 | 🟢 Nice-to-have |
| `payoneer alternative nigeria` | Exact | Low | $0.50–$2.00 | 🔴 Must-have |

**Bid Strategy:**
- **Exact match only** — long-tail terms need precision
- Max CPT bid: $1.50 (TR), $2.00 (EG/NG)
- CPI target: <$3.00 (TR), <$4.00 (EG/NG)
- These keywords have the **highest signal-to-noise ratio** — users searching "upwork ödeme" or "ABD banka hesabı" are extremely high-intent
- Run as "Long-Tail — Platform" and "Long-Tail — Local" campaigns
- Review weekly, pause any keyword with CR < 10% after 100 impressions

---

## 3. Search Volume Tier Definitions

| Tier | Estimated Monthly Searches (App Store) | Notes |
|---|---|---|
| **Very High** | 50,000+ | Generic English terms (paypal, money transfer). High competition. |
| **High** | 10,000–50,000 | Competitor brands (payoneer, wise), popular category terms |
| **Medium** | 2,000–10,000 | Specific category terms, platform names, Turkish generic |
| **Low–Medium** | 500–2,000 | Turkish-specific, Arabic, long-tail English |
| **Low** | <500 | Very specific long-tail, local language niche terms |

**Note:** App Store search volumes are significantly lower than web search volumes. A "high" App Store keyword may have 10x lower volume than its Google Search equivalent. Estimates are directional — use ASA's keyword popularity score (1–100) to validate after campaign launch.

---

## 4. Campaign Architecture

### Recommended ASA Campaign Structure

```
📱 ASA Account
├── 🟢 Campaign 1: Brand Defense (TR)
│   └── AG: cenoa, cenoa app, cenoa uygulama, cenoa hesap
│
├── 🔵 Campaign 2: Competitor Conquest — Tier 1 (TR)
│   ├── AG: Payoneer (payoneer, payoneer app, payoneer alternatif)
│   ├── AG: Wise (wise, wise app, transferwise, wise transfer)
│   └── AG: Comparison (payoneer vs wise, payoneer yerine)
│
├── 🔵 Campaign 3: Competitor Conquest — Tier 2 (TR)
│   ├── AG: PayPal (paypal, paypal alternatif)
│   ├── AG: Others (deel, remitly, xoom)
│   └── [Low budget, test mode]
│
├── 🟡 Campaign 4: Category — Generic (TR)
│   ├── AG: Money Transfer (para transferi, uluslararası, döviz)
│   ├── AG: USD Account (dolar hesabı, ABD banka hesabı, amerikan banka)
│   └── AG: Freelancer (freelancer banka, freelancer ödeme, e-ihracat)
│
├── 🟠 Campaign 5: Long-Tail — Platforms (TR)
│   ├── AG: Upwork (upwork payment, upwork ödeme, upwork para çekme)
│   └── AG: Fiverr (fiverr payment, fiverr ödeme, fiverr para çekme)
│
├── 🟠 Campaign 6: Long-Tail — Local Turkish
│   └── AG: (yurtdışından para alma, dolar hesabı açma, freelancer dolar hesabı)
│
├── 🔍 Campaign 7: Discovery (TR)
│   └── AG: Search Match ON + Broad match seed terms (low budget)
│
├── 🇪🇬 Campaign 8: Egypt (EG)
│   ├── AG: Competitor (payoneer, wise, بديل بايونير)
│   ├── AG: Category (حساب بنكي أمريكي, استلام دولار, تحويل أموال)
│   └── AG: Long-tail (سحب أموال أبورك, فريلانسر مصر)
│
└── 🇳🇬 Campaign 9: Nigeria (NG)
    ├── AG: Competitor (payoneer, wise, payoneer alternative nigeria)
    ├── AG: Category (receive dollars nigeria, usd account nigeria)
    └── AG: Long-tail (freelancer payment nigeria)
```

---

## 5. Budget Allocation

### Monthly Budget: $2,000 (starting — scale based on results)

| Group | % of Budget | Monthly $ | Weekly $ | Rationale |
|---|---|---|---|---|
| **A: Brand** | 20% | $400 | $100 | Defend brand. Cheapest CPI. |
| **B: Competitor** | 30% | $600 | $150 | Intercept switchers. Highest strategic value. |
| **C: Category** | 30% | $600 | $150 | Capture solution-seekers. Best volume potential. |
| **D: Long-Tail** | 20% | $400 | $100 | Highest intent / lowest CPI. |

### Market Split (within each group)

| Market | % | Rationale |
|---|---|---|
| **TR** | 70% | Primary market, highest organic base, most keywords |
| **EG** | 15% | Growing market, ⚠️ blocked by KYC issue (hold until fixed) |
| **NG** | 15% | Growing market, cheap CPIs |

### Scaling Rules
- **If CPI < target for 2 consecutive weeks:** Increase campaign budget by 20%
- **If CPI > 1.5× target for 1 week:** Reduce budget by 30%, review keywords
- **Monthly rebalance:** Move budget from underperformers to top 3 keywords by CPI
- **Scale ceiling (Month 1):** $2,000 → $3,000 max. Don't over-scale before data.

---

## 6. Bid Strategy Per Keyword Group

| Group | Bid Type | CPT Cap | CPI Target | Daily Budget Cap | Notes |
|---|---|---|---|---|---|
| **Brand** | Manual CPT (aggressive) | $1.50 | <$1.00 | $15 | Maximize impression share. Bid to win. |
| **Competitor T1** | Manual CPT (moderate) | $3.00 | <$6.00 | $15 | Payoneer + Wise only. Watch CR closely. |
| **Competitor T2** | Manual CPT (conservative) | $2.00 | <$8.00 | $7 | PayPal, Deel, Remitly — test mode. |
| **Category** | Manual CPT (moderate) | $2.50 | <$5.00 | $20 | Highest volume potential. Mine negatives aggressively. |
| **Long-Tail** | Manual CPT (moderate) | $1.50 | <$3.00 | $15 | Best CPI expected. Exact match only. |
| **Discovery** | Auto (Search Match) | $1.00 | <$5.00 | $5 | Find new terms. Move winners to exact match campaigns. |

### Why Manual CPT (not CPA goal)
- ASA in TR/EG/NG markets has **insufficient conversion data** for CPA Goal bidding to work well
- Manual CPT gives tighter cost control during the learning phase
- Switch to **CPA Goal** after 50+ installs per campaign (typically 4–8 weeks)
- Exception: Brand campaign can stay on Manual CPT permanently (predictable, low volume)

---

## 7. Custom Product Pages (CPP) Recommendations

ASA allows Custom Product Pages per ad group — use different screenshots/descriptions per keyword intent.

| Keyword Group | CPP Theme | Primary Message | Key Screenshots |
|---|---|---|---|
| **Brand** | Default App Store listing | Standard Cenoa value prop | Default |
| **Competitor (Payoneer/Wise)** | "Switch & Save" | "Fees under 1% — why freelancers switch from Payoneer" | Fee comparison, 3-min signup |
| **Category (USD Account)** | "Your USD Account" | "Get a US bank account in 3 minutes" | Account setup flow, USD balance |
| **Freelancer/Platform** | "Freelancer Payments" | "Upwork/Fiverr earnings — keep more, pay less fees" | Platform integration, withdrawal flow |
| **Local Turkish** | "Türk Freelancerlar İçin" | "ABD banka hesabınızı 3 dakikada açın" | Turkish screenshots, TRY withdrawal |
| **Egypt Arabic** | "للفريلانسرز في مصر" | "افتح حساب دولار أمريكي في دقائق" | Arabic screenshots, EGP context |

**Impact:** CPPs typically improve CR by 15–30%, which directly reduces CPI.

---

## 8. Keyword Discovery & Optimization Cadence

### Weekly (first 4 weeks)
- [ ] Review Search Terms report — add converting search terms as exact match
- [ ] Add non-converting/irrelevant terms as negative keywords
- [ ] Check impression share for brand terms (target 95%+)
- [ ] Pause keywords with 200+ impressions and 0 installs

### Bi-weekly (ongoing)
- [ ] Adjust CPT bids based on CPI performance vs targets
- [ ] Move top discovery terms to exact match in appropriate campaign
- [ ] Review competitor campaign CR — pause keywords with CR < 10%
- [ ] Test new long-tail keywords from SEO content plan keyword gaps

### Monthly
- [ ] Rebalance budget across groups based on CPI and volume
- [ ] Add new competitor/category keywords from market research
- [ ] Review CPP performance — A/B test new variants
- [ ] Evaluate readiness for CPA Goal bidding (50+ installs threshold)
- [ ] Cross-reference with Google Ads keyword performance (bid-strategy-reco.md)

---

## 9. Expected Outcomes (Month 1–3)

### Conservative Estimates

| Month | Budget | Est. Installs | Avg. CPI | Best Performing Group |
|---|---:|---:|---|---|
| **Month 1** | $2,000 | 400–600 | $3.50–$5.00 | Brand + Long-Tail |
| **Month 2** | $2,500 | 600–900 | $2.80–$4.00 | Category + Long-Tail |
| **Month 3** | $3,000 | 900–1,200 | $2.50–$3.30 | Category (optimized) |

### CPI Target by Group (Month 3 steady-state)

| Group | Target CPI | Expected CR | Volume Share |
|---|---|---|---|
| Brand | $0.50–$1.00 | 50–70% | 10% of installs |
| Competitor | $4.00–$6.00 | 15–25% | 20% of installs |
| Category | $2.50–$4.00 | 25–40% | 40% of installs |
| Long-Tail | $1.50–$3.00 | 30–50% | 30% of installs |

### Comparison to Google Ads Performance
- Current Google Ads CPI (TR): ~$27–$31 (Search/UAC)
- Current Google Ads CPI (EG): ~$9
- **ASA target CPI: $2.50–$5.00** → potential **6–10x cheaper** than Google Search
- ASA users are at the app store, ready to install → higher CR, lower funnel friction

---

## 10. Risk Factors & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| **PayPal keyword waste** | Very high volume, very low CR → budget drain | Start with $50/week cap, kill if CR < 5% after 2 weeks |
| **Competitor brand pushback** | Competitors may bid on "cenoa" in retaliation | Brand Defense campaign already recommended; monitor weekly |
| **EG market KYC blocker** | Installs from EG can't complete KYC | Hold EG budget until Bridgexyz fix (per bid-strategy-reco.md) |
| **Low App Store search volume in TR** | Turkish-language App Store searches may be low | Compensate with broader category terms in English |
| **Arabic keyword quality** | Arabic morphology = many spelling variants | Use broad match for Arabic with aggressive negative mining |
| **Seasonal volatility** | Freelancer payments spike Q4 (holiday season) | Reserve 20% budget increase capacity for Q4 |

---

## 11. Integration with Existing Campaigns

### Alignment with Google Ads (bid-strategy-reco.md)
- Google "TR Rakipler Payoneer" campaign has CPI ~$27 → **move competitor conquest budget to ASA** where CPI will be 5–10x lower
- Google Demand Gen is paused (0 installs) → reallocate some of that $560/week to ASA testing
- Google Pmax remains best Google channel ($19 CPI) — ASA complements, doesn't replace

### Alignment with SEO Content Plan
- SEO articles targeting "payoneer alternative", "upwork payment methods", "fiverr withdrawal" will boost App Store search volume for these terms
- As SEO content ranks, users searching these topics may also search in App Store → organic ASO + paid ASA flywheel
- Share keyword performance data between SEO and ASA teams monthly

### Alignment with Competitive Positioning
- Use competitive-positioning.md messaging in Custom Product Pages
- CPP for competitor keywords should mirror LP copy: "<1% fees, 3-min signup, Stripe + Lead Bank"
- Track whether ASA competitor keyword users convert at different rates than Google competitor keyword users

---

## Appendix: Full Keyword Count Summary

| Group | Keywords (Exact) | Keywords (Broad) | Total |
|---|---:|---:|---:|
| A: Brand | 6 | 0 | 6 |
| B: Competitor | 18 | 2 | 20 |
| C: Category | 20 | 3 | 23 |
| D: Long-Tail (Platforms) | 12 | 0 | 12 |
| D: Long-Tail (Local TR) | 8 | 0 | 8 |
| D: Long-Tail (EG Arabic) | 7 | 0 | 7 |
| D: Long-Tail (NG English) | 5 | 0 | 5 |
| Discovery | 0 | Search Match | — |
| **Total** | **76** | **5 + Search Match** | **81** |

---

*Sprint 068 | ASA Keyword Expansion Plan | 2026-03-22*
