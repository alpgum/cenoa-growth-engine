# [067] Budget Allocation Model — ROI-Based ($50K/mo)

**Generated:** 2026-03-21  
**Sprint:** 067  
**Inputs:** country-cac.md, channel-cac.md, ltv-cac-ratio.md, marginal-cac.md, budget-efficiency.md, meta-budget-reallocation.md  
**Budget envelope:** $50,000/month total performance marketing

---

## 1. Current Allocation vs Recommended

### Current state (Feb–Mar 2026 run-rate)

| Country | Monthly Spend | % of Total | Channels | $/Paid Active | LTV/CAC (Base) |
|---|---:|---:|---|---:|---:|
| TR | ~$35,400 | 71% | Meta, Pmax, Search, ASA, TikTok, Appnext | $208 (Feb) / $864 (Mar 9-15) | 0.08× |
| EG | ~$9,900 | 20% | Meta W2A | $64–$107 | 0.34× |
| NG | ~$4,700 | 9% | Google Search | $16 | 1.80× |
| **Total** | **$50,000** | **100%** | | | |

### Recommended allocation (post-KYC fix for NG/EG)

| Country | Monthly Spend | % of Total | Primary Channels | Expected $/Active | LTV/CAC (Base) |
|---|---:|---:|---|---:|---:|
| TR | $28,000 | 56% | Pmax, ASA, Search, Meta RTGT | $100–$130 | 0.08× |
| NG | $12,000 | 24% | Google Search, Pmax, Meta test | $20–$40 | 1.80× |
| EG | $8,000 | 16% | Meta LTV, Google Search | $50–$80 | 0.34× |
| Reserve | $2,000 | 4% | New channel tests | — | — |
| **Total** | **$50,000** | **100%** | | | |

> ⚠️ The recommended allocation is **only valid after KYC submit is non-zero** in NG/EG. Until then, Scenario A applies.

---

## 2. Channel Allocation Within Each Country

### Turkey ($28K–$40K depending on scenario)

| Channel | Allocation % | Monthly Budget | Expected $/Active | Rationale |
|---|---:|---:|---:|---|
| Google Pmax | 30% | $8,400–$12,000 | $19 | Best cost/active; ML-optimized; primary scale lever |
| Apple Search Ads | 20% | $5,600–$8,000 | $23 | Highest-intent users; strong downstream signal |
| Google Search | 18% | $5,040–$7,200 | $25 | Reliable quality; high-intent queries |
| Meta RTGT only | 9% | $2,400 | $67 | Proven retargeting; warm audience |
| Other (Spaze/selective) | 8% | $2,240–$3,200 | $31 | Keep only verified placements |
| Referral/Affiliate | 10% | $2,800–$4,000 | $30 est. | Organic-adjacent; high-quality users |
| Channel tests | 5% | $1,400–$2,000 | — | New channel experimentation |

**Killed/Paused in TR:**
- ❌ Meta W2A non-RTGT ($1,124–$3,536/active — consistently terrible)
- ❌ Appnext (fraud pattern: huge installs, 0 downstream)
- ❌ TikTok (0 withdrawals in attribution)

### Nigeria ($2K–$12K depending on scenario)

| Channel | Allocation % | Monthly Budget | Expected $/Active | Rationale |
|---|---:|---:|---:|---|
| Google Search | 50% | $1,000–$6,000 | $16–$30 | Only proven channel; scale carefully |
| Google Pmax | 30% | $600–$3,600 | $20–$35 est. | ML-optimized; test alongside Search |
| Meta prospecting | 20% | $400–$2,400 | $25–$50 est. | Test creative/audience in market |

### Egypt ($4K–$8K depending on scenario)

| Channel | Allocation % | Monthly Budget | Expected $/Active | Rationale |
|---|---:|---:|---:|---|
| Meta LTV test | 35% | $1,400–$2,800 | $54 (proven 1 wk) | Best early signal from Meta LTV campaign |
| Google Search | 30% | $1,200–$2,400 | $30–$60 est. | Intent-based; test market |
| Google Pmax | 25% | $1,000–$2,000 | $35–$70 est. | Scale candidate |
| ASA | 10% | $400–$800 | TBD | Small test in Egypt App Store |

---

## 3. Three Scenarios

### Scenario A: Status Quo (all to TR, NG/EG in test mode)

**Assumption:** KYC remains broken for NG/EG. All real budget stays in Turkey.

| Country | Monthly Spend | Channel Mix |
|---|---:|---|
| TR | $45,000 | Pmax $13.5K, ASA $9K, Search $8.1K, Meta RTGT $2.4K, Other $4K, Referral $4.5K, Tests $3.5K |
| NG | $2,000 | Google Search only (KYC validation budget) |
| EG | $3,000 | Meta LTV + Search (KYC validation budget) |

**Expected outcomes (monthly):**

| Metric | TR | NG | EG | Total |
|---|---:|---:|---:|---:|
| Installs | 5,500–7,000 | 2,800–4,000 | 600–1,000 | 8,900–12,000 |
| Signups | 2,200–2,800 | 1,200–1,800 | 300–500 | 3,700–5,100 |
| KYC submits | 600–700 | **0** | **0** | 600–700 |
| New actives | 300–350 | **~0** (no KYC) | **~0** (no KYC) | 300–350 |
| Blended $/active | $129–$150 | — | — | **$129–$150** |

**Pros:**
- Only market with functioning KYC → real users
- Channel reallocation (killing Meta W2A, Appnext, TikTok) improves TR efficiency vs historical
- Pmax/ASA scaling should bring $/active down from Feb's $208

**Cons:**
- TR diminishing returns kick in hard above $30K (see marginal CAC analysis)
- Extra $15K above the $30K threshold yields only ~75-90 marginal actives at $170–$225/marginal active
- Total actives ceiling of ~350/mo at this budget level
- LTV/CAC of 0.08× (base) means TR is **unit-economics negative** in every scenario except High LTV

---

### Scenario B: KYC Fixed → Measured Reallocation (recommended)

**Assumption:** KYC submit becomes functional in NG/EG. Gradual 30% shift from TR.

| Country | Monthly Spend | Channel Mix |
|---|---:|---|
| TR | $28,000 | Pmax $8.4K, ASA $5.6K, Search $5K, Meta RTGT $2.4K, Other $2.2K, Referral $2.8K, Tests $1.6K |
| NG | $12,000 | Search $6K, Pmax $3.6K, Meta $2.4K |
| EG | $8,000 | Meta LTV $2.8K, Search $2.4K, Pmax $2K, ASA $0.8K |
| Reserve | $2,000 | New channel tests |

**Expected outcomes (monthly):**

| Metric | TR | NG | EG | Total |
|---|---:|---:|---:|---:|
| Installs | 4,000–5,200 | 12,000–18,000 | 1,600–2,800 | 17,600–26,000 |
| Signups | 1,600–2,100 | 5,400–8,100 | 800–1,400 | 7,800–11,600 |
| KYC submits | 450–550 | 400–800* | 100–250* | 950–1,600 |
| New actives | 220–280 | 300–600* | 100–160* | 620–1,040 |
| $/active | $100–$127 | $20–$40* | $50–$80* | **$48–$81** |

*NG/EG estimates assume KYC completion rates reach 30–50% of TR's rate initially.

**Pros:**
- NG at $20–$40/active with base LTV/CAC of 1.80× → **only market that's unit-economics positive**
- 2–3× more total actives than Scenario A on same budget
- Blended $/active drops 40–65% vs status quo
- TR stays within efficient spend band ($27–$30K threshold)

**Cons:**
- Dependent on KYC fix (timeline unknown)
- NG/EG activation rates are estimates — could be worse than modeled
- Need 4–6 weeks of data post-KYC fix to validate
- NG's $16/active at $230 spend may not hold at $12K (diminishing returns untested)

---

### Scenario C: Aggressive NG/EG Ramp

**Assumption:** KYC works perfectly. Aggressive 50%+ shift to NG/EG within 8 weeks.

| Country | Monthly Spend | Channel Mix |
|---|---:|---|
| TR | $18,000 | Pmax $5.4K, ASA $3.6K, Search $3.2K, Meta RTGT $2.4K, Other $1.4K, Referral $2K |
| NG | $18,000 | Search $7.2K, Pmax $5.4K, Meta $3.6K, Other $1.8K |
| EG | $12,000 | Meta LTV $4.2K, Search $3.6K, Pmax $3K, ASA $1.2K |
| Reserve | $2,000 | New channel tests |

**Expected outcomes (monthly):**

| Metric | TR | NG | EG | Total |
|---|---:|---:|---:|---:|
| Installs | 2,800–3,600 | 18,000–25,000 | 2,400–4,000 | 23,200–32,600 |
| Signups | 1,100–1,400 | 8,100–11,200 | 1,200–2,000 | 10,400–14,600 |
| KYC submits | 300–400 | 600–1,200* | 150–350* | 1,050–1,950 |
| New actives | 150–200 | 450–900* | 150–250* | 750–1,350 |
| $/active | $90–$120 | $20–$40* | $48–$80* | **$37–$67** |

*Aggressive estimates — assumes NG/EG reach 50–70% of TR's conversion rates.

**Pros:**
- Maximum volume play: potentially 750–1,350 actives/mo (2.5–4× Scenario A)
- Lowest blended CAC ($37–$67)
- NG could become 50%+ of all active user growth
- TR at $18K stays well within efficient zone

**Cons:**
- **High risk:** NG/EG CAC at scale is completely untested
- TR dropping to $18K means losing ~100 actives vs Scenario B
- NG diminishing returns are unknown — $16/active may 3× at $18K spend
- EG KYC completion historically near-zero; $12K is aggressive
- If NG/EG CAC doubles at scale, effective budget waste of $10–15K/mo
- Requires dedicated campaign management capacity for 3 markets

---

## 4. Scenario Comparison Summary

| Metric | A: Status Quo | B: Measured (rec.) | C: Aggressive |
|---|---:|---:|---:|
| TR spend | $45,000 | $28,000 | $18,000 |
| NG spend | $2,000 | $12,000 | $18,000 |
| EG spend | $3,000 | $8,000 | $12,000 |
| Total installs | 8,900–12,000 | 17,600–26,000 | 23,200–32,600 |
| Total signups | 3,700–5,100 | 7,800–11,600 | 10,400–14,600 |
| **Total new actives** | **300–350** | **620–1,040** | **750–1,350** |
| **Blended $/active** | **$129–$150** | **$48–$81** | **$37–$67** |
| Risk level | Low (known) | Medium | High |
| KYC dependency | None | Yes | Yes |
| LTV/CAC positive? | No (TR only 0.08×) | Partially (NG 1.80×) | Partially (NG 1.80×) |

---

## 5. Critical Caveat: Web→App Attribution & "Organic" Decline

> ⚠️ **When paid spend is paused or reduced in a market, "organic" installs/signups may decline simultaneously.**

### Why this happens

Cenoa uses a **web-to-app (W2A) flow** where:
1. User clicks a paid ad → lands on web (cenoa.com)
2. Web page redirects to App Store / Play Store
3. User installs the app

In this flow, **AppsFlyer may attribute the install to "organic"** rather than the paid source because:
- The redirect breaks the click→install attribution chain
- Deep linking / deferred deep links may not fire correctly
- iOS ATT (App Tracking Transparency) blocks attribution for ~60% of iOS users

### What this means for budget decisions

- **If you pause Meta W2A campaigns in Turkey:** you may see organic installs drop 20–40% in the following weeks. This does NOT mean organic users disappeared — it means the attribution bridge broke.
- **The "organic" bucket (632 installs/wk, 77 signups/wk)** likely contains **significant paid-driven installs** that lost attribution.
- **Unattributed downstream (986 signups, 1,355 withdrawals/wk)** almost certainly includes Meta + other paid channel users who went through the W2A flow.

### Impact on this model

- **Scenario A (status quo):** Organic numbers may be inflated by paid spillover. If you cut TR Meta completely, "organic" will likely drop, making true blended CAC worse than modeled.
- **Scenarios B & C:** When ramping NG/EG, initial "organic" in those markets may rise as W2A attribution leaks — don't mistake this for true organic growth.
- **Guardrail:** When evaluating any channel pause, track **total installs (paid + organic + unattributed)** as the real metric, not just attributed paid installs.

### Recommended measurement approach
1. Run **holdout tests** (pause campaigns for 72h in one geo, measure total install decline)
2. Use **incrementality testing** (Meta Conversion Lift or geo-based experiments)
3. Fix **AppsFlyer OneLink** deep linking for W2A campaigns to recover attribution
4. Compare **total installs per $1K spent** rather than only attributed installs

---

## 6. Recommendation: Execute Scenario B with Staged Gates

### Phase 1: Channel cleanup in TR (Weeks 1–2, immediate)
- Pause Meta W2A non-RTGT, Appnext, TikTok in Turkey
- Reallocate freed ~$7,600/mo to Pmax (+$3,600), ASA (+$2,400), Search (+$1,600)
- Keep NG/EG in test mode ($2K and $3K respectively)
- **Expected impact:** TR actives stay flat or improve; blended TR $/active drops from $208 → $100–$130

### Phase 2: KYC validation (Weeks 3–6)
- Monitor KYC submit clicked for NG/EG in Amplitude daily
- When KYC submit > 0 for 5 consecutive days → trigger Phase 3
- If KYC not fixed by Week 6 → stay in Scenario A, escalate KYC as P0

### Phase 3: Measured NG/EG ramp (Weeks 7–10)
- Increase NG from $2K → $6K/mo (3× step)
- Increase EG from $3K → $5K/mo (1.7× step)
- Decrease TR from $45K → $37K/mo
- **Gate:** NG $/active must stay < $50; EG $/active must stay < $100

### Phase 4: Full Scenario B (Weeks 11–14)
- If Phase 3 validates: move to full Scenario B allocation
- TR: $28K, NG: $12K, EG: $8K, Reserve: $2K
- **Gate:** Total actives must exceed 500/mo (vs Scenario A's 300–350)

### Escalation to Scenario C
- Only consider after 8+ weeks of Scenario B data
- Requires: NG $/active < $30 at $12K spend AND EG $/active < $60 at $8K spend
- Board approval for aggressive geo shift (brand/regulatory implications)

---

## 7. Guardrails

### Hard stops (revert immediately)

| Signal | Threshold | Action |
|---|---|---|
| Total actives < 250/mo | Below Scenario A floor | Revert all budget to TR |
| NG $/active > $80 | 5× current level | Pause NG scaling, cap at test budget |
| EG $/active > $120 | Near TR levels | Pause EG scaling |
| TR "organic" drops > 40% | After Meta pause | Re-enable Meta prospecting at 50% of old budget |
| Pmax CPA doubles | $/active > $38 for 5+ days | Cap Pmax at pre-increase level |

### Weekly monitoring checklist

- [ ] Total installs by country (paid + organic + unattributed)
- [ ] KYC submit clicked by country (Amplitude)
- [ ] $/active by channel × country
- [ ] Organic install trend (watch for attribution leakage signal)
- [ ] Marginal $/active (week-over-week spend vs outcome delta)

### Monthly review

- Recalculate LTV/CAC by country with fresh cohort data
- Compare modeled vs actual actives for each scenario phase
- Adjust allocation ±10% based on observed marginal efficiency
- Re-evaluate channel mix within each country

---

## 8. Key Assumptions & Risks

| Assumption | Confidence | If Wrong |
|---|---|---|
| TR diminishing returns above $30K/mo | High (14-month data) | Scenario A worse than modeled |
| NG $16/active holds at moderate scale | Low (only $230 sample) | NG costs 3–5× more; reduce allocation |
| EG $54–$64/active at $5–8K spend | Medium (1-week signal) | EG costs more; shift budget to NG |
| KYC can be fixed for NG/EG | Unknown (product dependency) | Stuck in Scenario A indefinitely |
| Meta W2A drives hidden organic | High (attribution analysis) | Organic more resilient to Meta cuts |
| LTV model accuracy | Medium (scenario-based) | Unit economics better or worse than modeled |

---

## 9. Bottom Line

**Today:** Cenoa spends $50K/mo and gets ~300–350 new active users. Turkey is the only functioning market, and it's deeply unit-economics negative (LTV/CAC 0.08× base case). Over-spending above TR's $30K diminishing returns threshold wastes $10–15K/mo.

**With channel cleanup alone (Phase 1):** Same $50K budget → better channel mix → ~350–400 actives at ~$125/active. Immediate, no dependencies.

**With KYC fix + Scenario B:** Same $50K budget → 620–1,040 actives at $48–$81/active. Nigeria becomes the growth engine with **the only positive unit economics** (LTV/CAC 1.80× base). This is the play.

**The unlock isn't more budget — it's KYC in NG/EG + better channel allocation in TR.**

---

*Generated: 2026-03-21 | Sprint 067*  
*Dependencies: [028] LTV/CAC, [029] Budget Efficiency, [043] Marginal CAC, [045] Meta Analysis, [058] Meta Reallocation*


---

> ⚠️ **Attribution caveat:** Web campaigns (Meta/Google → cenoa.com → app store) may appear as "Organic" or "(none)" due to broken web→app attribution. Estimated correction factor: ~6.9×. See [attribution-reconciliation.md](attribution-reconciliation.md) for details.
