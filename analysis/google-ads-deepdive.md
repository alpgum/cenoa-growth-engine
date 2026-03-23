# Google Ads Campaign Deep-Dive

**Period:** Jan 2025 – Mar 2026  
**Sources:** Sheets (Trafik Canavarı, CaC Analysis, Budget Tracking), BigQuery (AppsFlyer), Amplitude attribution  
**Generated:** 2026-03-21

---

## 1. All Google Ads Campaigns — Spend, Installs, CPI

### A. Active Campaigns (from AppsFlyer / BigQuery, late Feb–early Mar 2026)

| Campaign | Market | Type | Weekly Spend (proxy) | Installs/wk | CPI | Notes |
|---|---|---|---:|---:|---:|---|
| **Google // Cenoa // Pmax // TR // E-ihracat // Architect // KYC_Start** | TR | Pmax | ~$806 | 27 | ~$30 | Primary Pmax campaign |
| **Google // Cenoa // Search // TR // Pure Brand** | TR | Search | ~$790 | 27 | ~$29 | Brand search — high intent |
| **Cenoa // Search // TR // Freelancer // Platform** | TR | Search | incl. above | — | — | Freelancer vertical |
| **TR-Discovery-24.10.2025** | TR | Demand Gen | unknown | 0 (attributed) | — | 🚩 1,627 clicks, 0 installs |
| **Google App Android (Sheets ref)** | TR | App Install | ~$1,400/wk | 45 act. | ~$31 CPA | Largest Google spend line |
| **EG Generic (egypt_en_architect_googleads)** | EG | Search | ~$500-700/wk | ~15-20 | ~$325 CPI est. | Best EG CPI |
| **TR Rakipler Payoneer** | TR | Search (competitor) | ~$200-300/wk | <1/wk | $938–$1,047 | 🚩 Extremely high CPI |
| **NG_Google_iOS_CVR** | NG | Search/CVR | minimal | ~5-10 | ~$27 | Cheap Nigeria traffic |

### B. Historical Google Spend (from Trafik Canavarı, monthly USD)

| Month | Google Spend | Total Spend | Google % | Blended CPI |
|---|---:|---:|---:|---:|
| Jan 2025 | $28,739 | $35,805 | 80% | $12 |
| Feb 2025 | $22,000 | $52,458 | 42% | $16 |
| Mar 2025 | $26,000 | $36,997 | 70% | $11 |
| May 2025 | $5,286 | $33,630 | 16% | $7 |
| Jun 2025 | $22,520 | $38,405 | 59% | $6 |
| Sep 2025 | $17,800 | $35,839 | 50% | $7 |
| Dec 2025 | $9,505 | $23,118 | 41% | $9 |
| Jan 2026 | ~$10,000 | $26,235 | 38% | — |
| Feb 2026 | ~$12,000 | $35,435 | 34% | — |

**Trend:** Google's share of total spend has declined from 80% → 34% as Meta, ASA, and ad networks expanded. However Google remains the most reliable channel for quality.

### C. January 2026 CAC Benchmark (Budget Tracking Sheet)

| Channel | Cost | Virtual Accounts | Cost/VirtAcc |
|---|---:|---:|---:|
| **Google (adjusted)** | $9,302 | 179 | **$52.10** |
| Apple Search Ads | $2,370 | 66 | $35.90 |
| Meta | $9,215 | 93 | $99.10 |
| Referral | $860 | 73 | $11.80 |

---

## 2. Pmax vs Search — Performance Comparison

### The Big Picture (from Sheets CaC Analysis)

| Metric | Pmax | Search | Combined |
|---|---|---|---|
| Weekly spend (proxy) | ~$806 | ~$790 | ~$1,596 |
| Weekly installs | 27 | 27 | 54 |
| CPI | ~$30 | ~$29 | ~$30 |
| Virtual accounts/wk | 87 | 124 | 211 |
| New active/wk | 42 | 31 | 73 |
| **Cost/VirtAcc** | **$9.26** | **$6.37** | **$7.56** |
| **Cost/New Active** | **$19.18** | **$25.48** | **$21.86** |

### CTA Cost Comparison (Sheets "Google Detailed" tab reference, from task brief)

| Campaign Type | Cost/CTA Range | Interpretation |
|---|---|---|
| **Pmax** | ₺3–27 per CTA | Ultra-efficient top-of-funnel; broad reach, algorithm-optimized |
| **Search** | ₺100–1,500 per CTA | High-intent but expensive clicks; brand/competitor terms |

### Analysis

**Pmax advantages:**
- 10–50× cheaper per click-to-action vs Search
- Higher new active rate (42 vs 31 per week) despite similar spend
- Algorithm finds conversion-likely users across Google surfaces (YouTube, Display, Discover, Search, Maps)

**Search advantages:**
- More virtual accounts per $ (124 vs 87 weekly → $6.37 vs $9.26 Cost/VirtAcc)
- Higher downstream quality — Search users come with intent ("Cenoa", "döviz hesabı", competitor terms)
- Withdrawals: 14 vs 15 (parity), but Search's withdrawal users likely have higher ATV

**Verdict:** Both are efficient. Pmax wins on activation volume, Search wins on account quality. **Run both.**

---

## 3. Campaign-Level Funnel (where data allows)

### TR Google (all types combined, Mar 14-20 attribution week)

| Stage | Count | Conv % |
|---|---:|---:|
| Installs | 54 | — |
| Sign-ups | 14 | 25.9% |
| Withdrawals | 29 | 53.7% (of signups) |

**Note:** 25.9% install→signup is the **second-best paid channel** (after ASA at 29.3%). 29 withdrawals includes historical cohort users — Google-acquired users are high-LTV.

### By Campaign Type (proxy split)

| Campaign | Installs | Signups | Withdrawals | Install→Signup |
|---|---:|---:|---:|---:|
| Pmax (KYC_Start) | ~27 | ~7 | ~15 | ~26% |
| Search (Brand) | ~27 | ~7 | ~14 | ~26% |

### Full Funnel Proxy (Jan 2026, Budget Tracking Sheet)

| Stage | Google | % of prior |
|---|---:|---:|
| Installs | 1,712 | — |
| KYC Start | 608 | 35.5% |
| Virtual Account | 179 | 29.4% |
| **Install → VirtAcc** | — | **10.5%** |

Compare: Meta had 1,251 installs → 93 VirtAcc (7.4%), ASA had 423 → 66 (15.6%).

---

## 4. TR Demand Gen Retargeting Anomaly

### The Problem

| Metric | Value |
|---|---|
| Campaign | TR-Discovery-24.10.2025 |
| Type | Demand Gen (Retargeting) |
| Clicks | 1,627 |
| Installs (attributed) | **0** |
| Status | Active since Oct 2025 |

### Root Cause Analysis

1. **Retargeting = existing users.** Demand Gen retargeting targets users who already visited the website or engaged with ads. These users likely already have the app installed → no new "install" event fires.

2. **Attribution mismatch.** AppsFlyer counts installs, not re-engagements. If a user clicks a retargeting ad and opens the existing app, it's a "re-attribution" or "re-engagement" — invisible in install-based reporting.

3. **Web-to-app gap.** If the Demand Gen campaign drives users to a landing page (web) and they don't click through to the app store, there's no install to attribute — even if the web visit was valuable.

4. **Possible click fraud/inflation.** 1,627 clicks with zero measurable outcome deserves scrutiny. Check Google Ads click quality reports for invalid traffic percentage.

### What We're Missing

The campaign may be driving:
- Web conversions (sign-ups via web flow) → check Google Ads conversion tracking
- App re-opens (not tracked as installs)
- Assisted conversions (first-touch awareness, last-touch attributed elsewhere)

### Recommendation

| Action | Priority |
|---|---|
| **Pause immediately** | 🔴 HIGH |
| Check Google Ads conversion tracking — are web conversions counted? | This week |
| Pull Google Ads "All conversions" report for this campaign | This week |
| If no web conversions either → kill permanently | Next 7 days |
| If web conversions exist → reconfigure as web-CPA campaign with proper tracking | Next 14 days |

**Spend being burned with zero measured outcome = unacceptable.** Even if there's a measurement gap, the default action is pause until proven otherwise.

---

## 5. TR Rakipler Payoneer — Worth Continuing?

### Performance Data

| Metric | Value |
|---|---|
| Campaign type | Search — Competitor targeting (Payoneer keywords) |
| CPI range | ₺938–₺1,047 (~$26-29 USD) |
| Volume | <1 install/week |
| Quality signal | Unknown (too few installs to measure funnel) |

### Analysis

**Arguments for keeping:**
- Competitor conquest is strategically valuable — users searching Payoneer are high-intent fintech users
- CPI of ~$27 USD is not terrible in absolute terms (close to ASA brand broad)
- Even 1 install/week at high LTV could justify the spend

**Arguments for killing:**
- ₺938-1,047 CPI in TRY is ~30-35× the Pmax CPI of ₺27
- Volume is negligible — doesn't move the needle
- Budget better allocated to campaigns that produce volume AND quality
- Competitor terms often attract curiosity clicks, not switching intent

### Verdict: **Scale down to monitoring budget or kill**

| Action | Detail |
|---|---|
| **Option A (preferred):** Reduce to ₺500/month monitor budget | Keep keyword coverage, limit waste |
| **Option B:** Kill and reallocate to Pmax | Better volume/CPI ratio |
| **Do NOT scale** | At current CPI, scaling would be burning money |

If keeping at monitoring level, add negative keywords aggressively (e.g., "Payoneer login", "Payoneer customer service") to filter out non-switching intent.

---

## 6. EG Generic — Best CPI at ₺325, Scaling Strategy

### Current Performance

| Metric | Value |
|---|---|
| Campaign | egypt_en_architect_googleads (EG Generic) |
| Market | Egypt |
| CPI (est.) | ~₺325 (~$9 USD) |
| Quality | NG_Google_iOS_CVR showed 14 withdrawals — EG Google has downstream signal |
| Country CPI comparison | EG overall: $8/VirtAcc vs TR: $35/VirtAcc (4.4× cheaper) |

### Why EG Generic Works

1. **Low competition:** Fewer advertisers bidding on fintech keywords in Egypt → cheaper CPCs
2. **English targeting:** "egypt_en" captures expat/freelancer audience — high-value segment
3. **Cross-border demand:** Egypt has strong remittance + freelancer economy → natural product-market fit

### Scaling Playbook

| Phase | Action | Budget | Timeline |
|---|---|---|---|
| **Phase 1: Validate** | Confirm install→KYC→active funnel (currently blocked by Bridgexyz KYC issue in EG) | Current | Now |
| **Phase 2: Expand keywords** | Add Arabic keywords (مصرف, تحويل أموال, حساب بالدولار) | +$500/wk | After KYC fix |
| **Phase 3: Launch Pmax EG** | Replicate TR Pmax success in Egypt market | +$1,000/wk | Month 2 |
| **Phase 4: Scale winners** | Double budget on campaigns with CPA < $20/active | 2× current | Month 3 |

### Risks

- ⚠️ **KYC blocker:** EG currently shows 0 KYC in weekly report (Bridgexyz blocked). Scaling installs without a working KYC flow = waste.
- ⚠️ **LTV unknown:** Cheap installs don't guarantee revenue. Need 30-day LTV data before aggressive scaling.

**Action:** Fix KYC first, then scale. Don't pour budget into a broken funnel.

---

## 7. Recommendations — Kill / Scale / Optimize

### 🟢 SCALE (increase budget)

| Campaign | Current Spend | Action | Target Spend | Rationale |
|---|---|---|---|---|
| **Pmax TR (E-ihracat/KYC_Start)** | ~$806/wk | **+50%** | $1,200/wk | Best activation efficiency ($19/active); Pmax auto-optimizes to budget |
| **Search TR (Pure Brand)** | ~$790/wk | **+30%** | $1,030/wk | Highest downstream quality; protect brand terms from competitors |
| **Google App Android** | ~$1,400/wk | **Hold + optimize** | $1,400/wk | Already largest line; optimize bids before scaling further |
| **EG Generic** | ~$500-700/wk | **+100% after KYC fix** | $1,200/wk | Best CPI in portfolio; needs working funnel first |
| **NG Google iOS** | minimal | **Test at $300/wk** | $300/wk | $27/VirtAcc — cheapest market; validate LTV |

### 🔴 KILL (stop immediately)

| Campaign | Current Spend | Issue | Savings |
|---|---|---|---|
| **TR Demand Gen (Discovery)** | unknown | 1,627 clicks, 0 installs — zero measured outcome | Immediate |
| **TR Rakipler Payoneer** | ~$200-300/wk | ₺938-1,047 CPI, <1 install/week | ~$1,000/mo |

### 🟡 OPTIMIZE (keep but fix)

| Campaign | Issue | Fix |
|---|---|---|
| **Pmax + Search combined** | Can't separate in AppsFlyer attribution | Tag campaigns distinctly in AF; use UTM params |
| **All Google campaigns** | Attribution loss — large "(none)" bucket in downstream events | Audit AppsFlyer SDK integration; ensure AF attribution carries to sign-up/KYC events |
| **Google App Android** | $31 CPA vs Pmax $19 — investigate why App campaigns are 63% more expensive | Review targeting overlap; may be bidding against own Pmax |

### 📊 Summary Budget Reallocation

| From | To | Amount/wk |
|---|---|---|
| Demand Gen retargeting | Pmax TR scale-up | ~$400 |
| Rakipler Payoneer | Search Brand + EG Generic | ~$250 |
| TikTok (from channel-cac reco) | Google App Android optimization | ~$340 |
| **Net reallocation** | | **~$990/wk → high-performing Google campaigns** |

### 🎯 KPI Targets (next 30 days)

| Metric | Current | Target |
|---|---|---|
| Google blended CPI (TR) | ~$29 | <$25 (with Pmax scale-up) |
| Google Cost/Active (TR) | ~$20-25 | <$20 |
| Google share of total spend | ~34% | 40-45% (shift budget from underperformers) |
| EG Google CPI | ~$9 | Maintain <$12 while scaling |
| Attribution coverage | ~60% | >80% (fix AF propagation) |

---

## Appendix: Data Confidence Notes

| Data Point | Source | Confidence | Gap |
|---|---|---|---|
| Campaign list | BigQuery (AppsFlyer) | ✅ High | Only Feb 25–Mar 2 window |
| Spend by campaign | Sheets (Budget Tracking) | ⚠️ Medium | Weekly averages, not campaign-level |
| Install→Signup funnel | Amplitude | ✅ High | One-week snapshot (Mar 14-20) |
| Signup→KYC→Active | Sheets (CaC Analysis) | ⚠️ Medium | Different time windows than attribution |
| Pmax vs Search split | Sheets proxy | ⚠️ Low | AppsFlyer doesn't distinguish — spend-share split |
| EG/NG campaign detail | Sparse | ❌ Low | Limited campaign-level data for non-TR markets |

**Key measurement fix needed:** Separate Pmax vs Search in AppsFlyer attribution to enable accurate per-campaign-type optimization.

---

*Analysis: Sprint 044 | Data: Sheets + BigQuery + Amplitude | 2026-03-21*


---

> ⚠️ **Attribution caveat:** Web campaigns (Meta/Google → cenoa.com → app store) may appear as "Organic" or "(none)" due to broken web→app attribution. Estimated correction factor: ~6.9×. See [attribution-reconciliation.md](attribution-reconciliation.md) for details.
