# Apple Search Ads — Expansion Plan

**Created:** March 23, 2026  
**Sprint:** 068  
**Status:** 📋 Ready for implementation  
**Markets:** EG (scale), NG (pilot), TR (expansion)

---

## 1. Current State

| Campaign | Weekly Spend | CPI | Actives/wk | TRUE CAC | Health |
|----------|-------------|-----|-----------|----------|--------|
| **ASA TR** | $500 | $9.80 | 19 | **$26** | 🟢 Best-in-class |
| **ASA EG** | $33 | $1.94 | 2 | **$16** | 🟢 Lowest CAC in portfolio |

ASA is the top-performing paid channel across all markets. TR delivers consistent $26 CAC (stable WoW). EG shows $16 CAC on tiny spend — the signal is strong but needs volume to validate.

**Why expand now:**
- ASA TR and EG are the only two 🟢 campaigns in the entire portfolio
- 8 of 12 campaigns are flagged 🔴 Kill — budget needs to shift to what works
- ASA CPIs ($2–$10) are 5–10× cheaper than Google Search ($22+ CPI) and Meta ($11+ CPI with no activations)
- Expanding ASA from $533/wk to $710/wk is a modest +33% increase with high-confidence ROI

---

## 2. Egypt — Scale Plan

### Budget
| | Current | Target | Delta |
|---|---------|--------|-------|
| Daily | $5 | $25 | +$20/day |
| Weekly | $33 | $175 | +$142/wk |

Ramp schedule: $5→$10 (Week 1), $10→$15 (Week 2), $15→$25 (Week 3+). Don't jump to $25 on day 1 — let the algorithm learn.

### Keywords — Top 20 (Competitor + Category)

**Competitor (10 keywords)**

| # | Keyword | Match | Lang | Est. CPI |
|---|---------|-------|------|----------|
| 1 | `payoneer` | Exact | EN | $2–$5 |
| 2 | `payoneer app` | Exact | EN | $2–$5 |
| 3 | `payoneer alternative` | Exact | EN | $1.50–$4 |
| 4 | `بديل بايونير` (Payoneer alternative) | Exact | AR | $0.50–$2 |
| 5 | `wise` | Exact | EN | $2–$5 |
| 6 | `wise app` | Exact | EN | $2–$5 |
| 7 | `paypal` | Exact | EN | $3–$8 |
| 8 | `grey.co` | Exact | EN | $1–$3 |
| 9 | `payoneer vs wise` | Exact | EN | $2–$5 |
| 10 | `best payoneer alternative` | Broad | EN | $2–$5 |

**Category (10 keywords)**

| # | Keyword | Match | Lang | Est. CPI |
|---|---------|-------|------|----------|
| 11 | `حساب بنكي أمريكي` (US bank account) | Exact | AR | $0.50–$2 |
| 12 | `استلام دولار` (receive dollars) | Exact | AR | $0.50–$2 |
| 13 | `حساب دولار` (dollar account) | Exact | AR | $0.50–$2 |
| 14 | `تحويل أموال` (money transfer) | Exact | AR | $1–$3 |
| 15 | `فريلانسر مصر` (freelancer Egypt) | Exact | AR | $0.30–$1.50 |
| 16 | `سحب أموال أبورك` (withdraw Upwork) | Exact | AR | $0.30–$1.50 |
| 17 | `receive usd` | Exact | EN | $1.50–$4 |
| 18 | `usd account` | Exact | EN | $2–$5 |
| 19 | `freelancer payment` | Broad | EN | $2–$5 |
| 20 | `send money to egypt` | Exact | EN | $2–$5 |

**Plus:** 1 Search Match discovery ad group ($3/day cap) to mine new Arabic terms.

### Match Type Strategy
- **Exact match** for all known keywords (control spend)
- **Search Match ON** in a separate discovery ad group at $3/day
- **Broad match** only for `best payoneer alternative` and `freelancer payment` to capture variants
- Mine Search Match weekly → promote winners to exact match

### Creative
- Current: default App Store listing
- **When Arabic LP is ready:** link Custom Product Page with Arabic screenshots + "افتح حساب دولار أمريكي في دقائق" messaging
- Until then: English default listing (still works — most EG freelancers read English)

### Campaign Structure
```
🇪🇬 ASA Egypt — Expanded
├── AG: Competitor (keywords 1–10) — $12/day
├── AG: Category Arabic (keywords 11–16) — $6/day
├── AG: Category English (keywords 17–20) — $4/day
└── AG: Discovery (Search Match ON) — $3/day
```

---

## 3. Nigeria — Pilot

### Budget
| | Target |
|---|--------|
| Daily | $10 |
| Weekly | $70 |
| Test duration | 2 weeks |

### Keywords (English)

| # | Keyword | Match | Est. CPI |
|---|---------|-------|----------|
| 1 | `receive usd` | Exact | $1.50–$4 |
| 2 | `receive dollars nigeria` | Exact | $0.50–$2 |
| 3 | `freelancer payment` | Exact | $2–$5 |
| 4 | `freelancer payment nigeria` | Exact | $0.50–$2 |
| 5 | `dollar account` | Exact | $2–$5 |
| 6 | `usd account nigeria` | Exact | $0.80–$2.50 |
| 7 | `payoneer alternative` | Exact | $2–$5 |
| 8 | `payoneer alternative nigeria` | Exact | $0.50–$2 |
| 9 | `payoneer` | Exact | $2–$5 |
| 10 | `wise` | Exact | $2–$5 |

**Plus:** Search Match discovery ad group ($2/day cap).

### Success Criteria
| Metric | Target | Kill Threshold |
|--------|--------|----------------|
| TRUE CAC | **< $50** | > $75 after 2 weeks |
| Installs | > 20 in 2 weeks | < 5 |
| Install → Active rate | > 5% | < 2% |

### Campaign Structure
```
🇳🇬 ASA Nigeria — Pilot
├── AG: Core (keywords 1–6) — $5/day
├── AG: Competitor (keywords 7–10) — $3/day
└── AG: Discovery (Search Match ON) — $2/day
```

### Decision Framework (End of Week 2)
- **CAC < $30:** Scale to $20/day, add more keywords from expansion list
- **CAC $30–$50:** Maintain $10/day, optimize keywords, run 2 more weeks
- **CAC $50–$75:** Cut to $5/day, narrow to top 3 keywords only
- **CAC > $75 or < 5 installs:** Kill. Reallocate to EG.

---

## 4. Turkey — Expansion

### Budget
Maintain **$500/wk** — no increase. Shift allocation from brand to competitor conquest.

### Current vs. New Allocation

| Ad Group | Current Share (est.) | New Share | Weekly $ |
|----------|---------------------|-----------|---------|
| Brand (cenoa, cenoa app) | ~60% | 20% | $100 |
| Competitor Tier 1 | ~10% | 35% | $175 |
| Category | ~20% | 25% | $125 |
| Long-Tail / Discovery | ~10% | 20% | $100 |

### New Competitor Keywords to Add

| Keyword | Match | Est. CPI | Priority |
|---------|-------|----------|----------|
| `payoneer` | Exact | $3–$8 | 🔴 Must |
| `payoneer alternatif` | Exact | $1.50–$4 | 🔴 Must |
| `payoneer app` | Exact | $3–$8 | 🔴 Must |
| `wise` | Exact | $3–$7 | 🔴 Must |
| `wise app` | Exact | $3–$7 | 🔴 Must |
| `transferwise` | Exact | $2.50–$6 | 🟡 Test |
| `payoneer vs wise` | Exact | $2–$5 | 🟡 Test |
| `payoneer yerine` | Exact | $1–$3 | 🟡 Test |

### Negative Keywords (add immediately)
- `payoneer login`, `payoneer giriş`, `payoneer support`, `payoneer destek`
- `wise login`, `wise giriş`, `wise hesap`
- Any `[competitor] login/support/customer service` variants

### Rationale
Google "TR Rakipler Payoneer" campaign has ~$27 CPI. ASA competitor keywords should deliver $3–$8 CPI — a 3–9× improvement for the same intent.

---

## 5. Bid Strategy Per Group

| Group | Market | Bid Type | Max CPT | CPI Target | CAC Target | Daily Cap |
|-------|--------|----------|---------|------------|------------|-----------|
| **Brand** | TR | Manual CPT (aggressive) | $1.50 | <$1 | <$10 | $15 |
| **Competitor T1** | TR | Manual CPT (moderate) | $3.00 | <$6 | <$35 | $25 |
| **Competitor T1** | EG | Manual CPT (moderate) | $4.00 | <$5 | <$25 | $12 |
| **Competitor** | NG | Manual CPT (conservative) | $3.00 | <$5 | <$40 | $3 |
| **Category** | TR | Manual CPT (moderate) | $2.50 | <$5 | <$30 | $18 |
| **Category (Arabic)** | EG | Manual CPT (moderate) | $2.00 | <$3 | <$20 | $6 |
| **Category (English)** | EG | Manual CPT (moderate) | $3.50 | <$5 | <$30 | $4 |
| **Core** | NG | Manual CPT (moderate) | $2.50 | <$4 | <$35 | $5 |
| **Long-Tail** | TR | Manual CPT (moderate) | $1.50 | <$3 | <$20 | $14 |
| **Discovery** | All | Auto (Search Match) | $1.00 | <$5 | — | $3–$5 |

**Why Manual CPT everywhere:**
- Insufficient conversion volume in TR/EG/NG for CPA Goal bidding
- Manual CPT gives tighter spend control during scale-up
- Switch to CPA Goal per campaign after 50+ installs (4–8 weeks for EG/NG)

**Bid adjustment rules:**
- Keyword CPI > 1.5× target for 7 days → reduce CPT bid by 20%
- Keyword CPI < 0.5× target for 7 days → increase CPT bid by 15% (capture more volume)
- Keyword with 200+ impressions and 0 installs → pause
- Keyword with CR > 40% → increase bid to max CPT cap

---

## 6. Expected Outcomes

### Weekly Projections (Steady State — Week 4+)

| Market | Spend/wk | Est. Installs | Est. Actives | Target CAC | Current Actives |
|--------|----------|---------------|-------------|------------|-----------------|
| **TR** | $500 | 55–65 | **21** (+2 from competitor conquest) | $24 | 19 |
| **EG** | $175 | 60–90 | **10** (+8 from scale) | $18 | 2 |
| **NG** | $70 | 15–25 | **3** (new market) | $23 | 0 |
| **Total** | **$745** | 130–180 | **34** | $22 avg | 21 |

### Incremental Impact
| Metric | Current | Projected | Delta |
|--------|---------|-----------|-------|
| ASA weekly spend | $533 | $745 | +$212 (+40%) |
| ASA weekly actives | 21 | 34 | +13 (+62%) |
| ASA blended CAC | $25 | $22 | -$3 (-12%) |

### Breakdown of New Actives
- **EG +8/wk:** 5× budget increase on a $16 CAC channel. Even if CAC doubles to $32 during scale, still the #1 channel. Conservative estimate assumes some efficiency loss.
- **NG +3/wk:** New market pilot at $70/wk. If NG mirrors EG economics (cheap App Store, low competition), $23 CAC is achievable. If not, we kill at week 2.
- **TR +2/wk:** Competitor conquest keywords tap new user intent currently going to Payoneer/Wise. 19→21 actives is modest because we're reallocating budget, not adding.

### Risk-Adjusted Scenarios

| Scenario | EG Actives | NG Actives | TR Actives | Total | CAC |
|----------|-----------|-----------|-----------|-------|-----|
| 🟢 Bull | 12 | 5 | 23 | 40 | $19 |
| 🟡 Base | 10 | 3 | 21 | 34 | $22 |
| 🔴 Bear | 5 | 1 | 19 | 25 | $30 |

---

## 7. Implementation Checklist

### Week 1 (Immediate)
- [ ] EG: Increase daily budget $5 → $10
- [ ] EG: Add competitor keywords (1–10) in new ad group
- [ ] EG: Add Arabic category keywords (11–16) in new ad group
- [ ] EG: Enable Search Match discovery ad group ($3/day)
- [ ] TR: Add competitor keywords (payoneer, wise, payoneer alternatif, wise app)
- [ ] TR: Add negative keywords for competitor login/support terms
- [ ] TR: Shift brand budget from 60% → 20% of $500
- [ ] NG: Create new campaign with Core + Competitor ad groups
- [ ] NG: Set daily budget $10, Search Match discovery at $2/day

### Week 2
- [ ] EG: Increase budget $10 → $15/day
- [ ] Review all Search Match terms — promote/negate
- [ ] Check NG pilot: any installs? Any active signals?

### Week 3
- [ ] EG: Increase budget $15 → $25/day (full target)
- [ ] NG: Mid-pilot review — on track for CAC < $50?
- [ ] TR competitor keywords: first CPI/CR read — adjust bids

### Week 4 (Decision Point)
- [ ] NG: Go/No-Go decision based on 2-week data
- [ ] EG: Full performance review at $25/day — CAC still < $30?
- [ ] TR: Competitor keyword performance vs. category — rebalance
- [ ] All markets: First monthly budget rebalance

### Ongoing (Weekly)
- [ ] Mine Search Match reports for new exact-match candidates
- [ ] Add negative keywords from irrelevant search terms
- [ ] Check brand impression share (target 95%+ in TR)
- [ ] Compare ASA CAC vs. other channels — inform portfolio allocation

---

## 8. Dependencies & Blockers

| Dependency | Status | Impact |
|------------|--------|--------|
| EG KYC (Bridgexyz) | ⚠️ Partially blocked | Install-to-active rate may be lower until fixed. Budget scale is still worth it at $16 CAC. |
| Arabic LP / Custom Product Page | 🔲 Not started | EG CR will improve 15–30% once Arabic CPP is live. Launch without it, add later. |
| NG App Store listing | ✅ Live | English listing works for NG. No localization needed. |
| ASA account access | ✅ Active | TR and EG campaigns already running. NG requires new campaign creation. |

---

*Sprint 068 | ASA Expansion Plan | 2026-03-23*
