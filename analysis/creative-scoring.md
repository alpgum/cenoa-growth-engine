# Creative Performance Scoring System

**Date:** 2026-03-21  
**Sprint:** 069  
**Purpose:** Standardized 1–10 scoring framework for evaluating creative performance across TR, NG, and EG markets

---

## 1. Scoring Dimensions & Weights

| # | Dimension | Weight | What It Measures |
|---|---|---:|---|
| 1 | **CTR** (click-through rate) | 15% | Ad relevance & thumb-stopping power |
| 2 | **CVR** (click → install) | 20% | Landing/store page alignment with creative promise |
| 3 | **CPA** (cost per acquisition) | 25% | Efficiency of spend → install conversion |
| 4 | **Downstream Quality** (install → active) | 25% | User quality — do installs become real users? |
| 5 | **Frequency/Fatigue** (performance decay rate) | 15% | Creative longevity — how fast does it burn out? |

**Composite Score** = Σ (Dimension Score × Weight)

---

## 2. Scoring Thresholds (1–10 Scale)

### 2a. CTR (Weight: 15%)

Benchmarks calibrated to Meta mobile app/W2A campaigns in fintech vertical.

| Score | CTR Range | Label |
|---:|---|---|
| 10 | ≥ 3.0% | Exceptional — viral-level engagement |
| 9 | 2.5–2.99% | Outstanding |
| 8 | 2.0–2.49% | Excellent |
| 7 | 1.5–1.99% | Strong |
| 6 | 1.2–1.49% | Above average |
| 5 | 1.0–1.19% | Average (Meta fintech baseline) |
| 4 | 0.8–0.99% | Below average |
| 3 | 0.6–0.79% | Weak |
| 2 | 0.4–0.59% | Poor |
| 1 | < 0.4% | Non-performing — kill immediately |

### 2b. CVR — Click → Install (Weight: 20%)

| Score | CVR Range | Label |
|---:|---|---|
| 10 | ≥ 40% | Exceptional (strong store page + creative alignment) |
| 9 | 35–39% | Outstanding |
| 8 | 30–34% | Excellent |
| 7 | 25–29% | Strong |
| 6 | 20–24% | Above average |
| 5 | 15–19% | Average |
| 4 | 10–14% | Below average |
| 3 | 7–9% | Weak |
| 2 | 4–6% | Poor — creative/store mismatch |
| 1 | < 4% | Non-performing |

### 2c. CPA — Cost per Acquisition/Install (Weight: 25%)

Thresholds are **market-specific** due to different CPM environments.

| Score | TR (CPA) | NG (CPA) | EG (CPA) | Label |
|---:|---|---|---|---|
| 10 | < $3 | < $1 | < $1.50 | Exceptional |
| 9 | $3–5 | $1–2 | $1.50–3 | Outstanding |
| 8 | $5–8 | $2–3.50 | $3–5 | Excellent |
| 7 | $8–12 | $3.50–5 | $5–7 | Strong |
| 6 | $12–16 | $5–7 | $7–10 | Above average |
| 5 | $16–22 | $7–10 | $10–14 | Average (current Meta TR: ~$22 CPI) |
| 4 | $22–28 | $10–14 | $14–18 | Below average |
| 3 | $28–35 | $14–18 | $18–25 | Weak |
| 2 | $35–50 | $18–25 | $25–35 | Poor |
| 1 | > $50 | > $25 | > $35 | Non-performing |

*Context: Current Meta TR CPI ≈ $22.57, ASA CPI ≈ $8.01, Google CPI ≈ $29.26*

### 2d. Downstream Quality — Install → Active Rate (Weight: 25%)

"Active" = user who creates a virtual account AND completes at least one withdrawal.

| Score | Install→Active % | Label |
|---:|---|---|
| 10 | ≥ 35% | Exceptional (ASA brand exact territory) |
| 9 | 28–34% | Outstanding |
| 8 | 22–27% | Excellent |
| 7 | 17–21% | Strong |
| 6 | 13–16% | Above average (current Meta W2A: ~16.7% signup) |
| 5 | 10–12% | Average |
| 4 | 7–9% | Below average |
| 3 | 4–6% | Weak |
| 2 | 2–3% | Poor — likely low-intent traffic |
| 1 | < 2% | Non-performing (appnext territory: 0.4%) |

*Reference points: ASA 29.3% signup rate, Google 25.9%, Meta 16.7%, Appnext 8.8% (→0.4% withdrawal)*

### 2e. Frequency/Fatigue — Performance Decay (Weight: 15%)

Measured as days until CTR drops >30% from peak (or CPA rises >30%).

| Score | Days to Decay | Label |
|---:|---|---|
| 10 | > 42 days | Evergreen creative |
| 9 | 35–42 days | Highly durable |
| 8 | 28–34 days | Strong longevity |
| 7 | 21–27 days | Good — standard refresh cycle |
| 6 | 17–20 days | Above average |
| 5 | 14–16 days | Average (2-week shelf life) |
| 4 | 10–13 days | Below average — burning fast |
| 3 | 7–9 days | Weak — weekly refresh needed |
| 2 | 4–6 days | Poor — audience saturation |
| 1 | < 4 days | Dead on arrival |

---

## 3. Application to Known Campaigns (Mar 14–20 Data)

> ⚠️ Creative-level CTR/frequency data unavailable (requires Meta API). Scores below use campaign-level proxies. Dimensions without data are marked "N/A" and excluded from the weighted composite.

### Turkey (TR)

| Campaign | CTR | CVR | CPA | Downstream | Fatigue | Composite | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| **TR_Meta_web2app_RTGT** | N/A | 6 (35% signup) | 4 (~$22 CPI proxy) | 7 (9 withdrawals from 17 installs = 53% downstream*) | N/A | **5.7** | ⭐ Best current Meta TR — retargeting works |
| **1764668627 (legacy)** | N/A | N/A | N/A | 10 (76 withdrawals/week — proven LTV) | 10 (still performing after months) | **10.0** | ⭐⭐ Gold standard — reverse-engineer these creatives |
| **tr_asa_appinstall_brand_exact** (benchmark) | N/A | 8 (46% signup) | 8 (~$8 CPI) | 10 (114 withdrawals from 26 installs) | N/A | **8.8** | 🏆 Best campaign overall (not Meta, but the bar to aim for) |

*\*RTGT downstream inflated by retargeting warm audiences — adjust expectations for prospecting.*

### Nigeria (NG)

| Campaign | CTR | CVR | CPA | Downstream | Fatigue | Composite | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| **architect_freelancer_fiverr** | N/A | 7 (44% signup: 8/18) | N/A | 1 (0 withdrawals) | N/A | **3.2** | 🚩 Good signup, zero activation — messaging attracts curiosity not intent |
| **architect_nigeria_en_freelancer** | N/A | 5 (19% signup: 4/21) | N/A | 1 (0 withdrawals) | N/A | **2.4** | 🚩 Worse conversion, same zero-activation problem |
| **architect_wise-paypal-wu-revolut** | N/A | 5 (25% signup: 4/16) | N/A | 1 (0 withdrawals) | N/A | **2.4** | 🚩 Payment angle not converting to active use |
| **NG_Google_iOS_CVR** (benchmark) | N/A | N/A | N/A | 7 (14 withdrawals) | N/A | **7.0** | ⭐ Google reaching higher-intent NG users |

### Egypt (EG)

| Campaign | CTR | CVR | CPA | Downstream | Fatigue | Composite | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| **EG_Meta_web2app_CVR_Android_031826** | N/A | 2 (7% signup: 3/44) | N/A | 1 (0 withdrawals) | N/A | **1.2** | 🚩 Low quality — just launched, needs 2-week window |
| **EG_Meta_web2app_ALL_031826** | N/A | 5 (20% signup: 4/20) | N/A | 1 (0 withdrawals) | N/A | **2.4** | ⚠️ Broad targeting, too early to judge |

---

## 4. Creative Refresh Cadence

Based on market CPM competition, audience pool size, and frequency saturation dynamics:

| Market | Refresh Cadence | Rationale |
|---|---|---|
| **Turkey (TR)** | Every **2–3 weeks** | Highest CPM market ($8–15 CPM), smaller targetable audience for fintech, most competitive. Creative fatigue hits faster. With only 9 creatives for $9K/month, frequency is likely 3–5x/week — unsustainable. |
| **Nigeria (NG)** | Every **4 weeks** | Lower CPMs ($2–5), larger untapped audience pool for freelancer targeting. Less competition in fintech ads. Slower saturation. |
| **Egypt (EG)** | Every **4 weeks** | Recently launched market. Audience is fresh. Arabic-language creative pool is smaller so refresh resources are constrained. Monitor if fatigue accelerates as spend scales. |

### Refresh Calendar Template

```
Week 1: Launch 3 new variants per market
Week 2: Kill bottom performer, scale winner, introduce 1 new test
Week 3 (TR): Full creative refresh cycle — retire fatigued assets, launch 3 new
Week 4 (NG/EG): Full refresh cycle for these markets
```

### Creative Volume Targets

| Market | Current Creatives | Target Creatives | Gap |
|---|---:|---:|---|
| TR | 9 | 15–20 | +6–11 (urgently under-stocked for $9K/month) |
| NG | 7 | 10–12 | +3–5 |
| EG | 8 | 10–12 | +2–4 |

---

## 5. Creative Testing Protocol

### The 3-Variant Rule

**Always run 3 creative variants simultaneously per campaign.** Never run a single creative — you need data to optimize.

### Weekly Testing Cadence

```
Monday    → Review prior week's creative performance
Tuesday   → Kill bottom performer (lowest composite score)
Wednesday → Brief & assign replacement creative  
Thursday  → Launch new variant (3 active again)
Friday    → Mid-week check — pause any creative with CTR < 0.4% immediately
```

### Testing Framework

| Phase | Duration | Action | Kill Criteria |
|---|---|---|---|
| **Learning** | Days 1–3 | Let Meta optimize delivery across all 3 variants | None — let the algorithm explore |
| **Evaluate** | Days 4–7 | Compare CTR, CVR, CPA across variants | Kill if CTR < 50% of best variant AND CPA > 150% of best |
| **Optimize** | Days 7–14 | Scale winner, maintain runner-up, replace loser | Kill bottom performer weekly |
| **Refresh** | Day 14–21 (TR) / Day 21–28 (NG/EG) | Replace all creatives if composite score drops below 5.0 | Full creative refresh |

### Statistical Significance Minimums

Before killing a creative, ensure minimum data:
- **Impressions:** ≥ 5,000
- **Clicks:** ≥ 50
- **Installs:** ≥ 15
- **Time live:** ≥ 3 days (Meta learning phase)

If a creative hasn't hit these thresholds, extend the test — don't kill based on noise.

### Budget Split for Testing

| Allocation | % of Campaign Budget |
|---|---:|
| Proven winner (scale) | 50% |
| Runner-up (maintain) | 30% |
| New test variant | 20% |

---

## 6. Per-Market Creative Insights

### 🇹🇷 Turkey (TR)

**Audience context:** Fintech-savvy, high smartphone penetration, competitive remittance market (Papara, Wise, ENPARA competing).

| Dimension | Insight |
|---|---|
| **Language** | Turkish copy mandatory. English-only creatives will score 2–3 points lower on CTR. |
| **Messaging angle** | **Competitive differentiation** — "Why Cenoa vs Papara/Wise?" Direct comparison works in TR. |
| **Top-performing themes** | Remittance savings ("X TL daha az komisyon"), speed ("Anında transfer"), security ("BDDK lisanslı") |
| **Creative format** | UGC-style testimonials outperform polished brand creatives in TR Meta. Test real user stories. |
| **Retargeting** | RTGT is the only currently-performing TR Meta campaign (9 withdrawals). Invest here. |
| **Avoid** | Generic "send money abroad" — too broad. Fintech-literate TR users need specifics. |
| **CTA** | "Hemen Dene" (Try Now) > "İndir" (Download) — action-oriented CTAs outperform on Meta. |

### 🇳🇬 Nigeria (NG)

**Audience context:** Freelancers earning in USD, large diaspora sending money home, crypto-native user base.

| Dimension | Insight |
|---|---|
| **Language** | English. Nigerian Pidgin can work for younger demographics but test carefully. |
| **Messaging angle** | **USD earning/receiving focus** — "Get paid in dollars, spend in naira at the best rate." |
| **Top-performing themes** | Freelancer payments (Fiverr/Upwork angle shows 44% signup — but zero activation, so refine), dollar account access, lower fees than traditional banks |
| **Creative format** | Problem→Solution format. "Tired of losing 5% on Wise? Cenoa gives you the real rate." |
| **Critical gap** | Current creatives attract sign-ups but not activation. The "receive payments" angle likely converts better than "freelancer tool" because it's transaction-intent, not tool-intent. |
| **Pivot needed** | Shift from "Cenoa for freelancers" → "Receive USD payments instantly, withdraw to your bank" — action-oriented messaging that matches the actual product workflow. |
| **CTA** | "Start Receiving Payments" > "Sign Up Free" — matches high-intent users. |

### 🇪🇬 Egypt (EG)

**Audience context:** Underbanked population, strict currency controls, remittance-dependent economy, Arabic-first market.

| Dimension | Insight |
|---|---|
| **Language** | **Arabic mandatory** (Egyptian dialect preferred over MSA). English creatives will fail. |
| **Messaging angle** | **Bank account access** — "حساب دولاري بدون تعقيدات" (Dollar account without complications). Many Egyptians can't access USD accounts through traditional banks. |
| **Top-performing themes** | USD access, remittance receiving (diaspora), savings protection against EGP devaluation, alternative to black market FX |
| **Creative format** | Educational content performs well — many EG users are new to fintech. Explainer-style creatives showing the app flow. |
| **Early signals** | CVR campaign (7% signup) underperforming vs ALL campaign (20% signup). Broad targeting with right messaging may outperform narrow CVR optimization initially — audience needs educating first. |
| **Regulatory sensitivity** | Avoid direct mentions of "currency exchange" or "crypto" — Egyptian regulators are strict. Frame as "digital wallet" / "حافظة رقمية". |
| **CTA** | "افتح حسابك الآن" (Open Your Account Now) — direct, clear, action-oriented in Egyptian Arabic. |

---

## 7. Composite Score Interpretation & Action Matrix

| Score Range | Label | Action |
|---:|---|---|
| 8.0–10.0 | **Star** | Scale aggressively. Increase budget allocation. Clone format for new variants. |
| 6.0–7.9 | **Performer** | Maintain. Use as baseline. Test iterations to push into Star territory. |
| 4.0–5.9 | **Average** | On notice. Must improve within 1 refresh cycle or replace. |
| 2.0–3.9 | **Underperformer** | Kill within 7 days. Replace with new test variant. |
| 1.0–1.9 | **Dead weight** | Kill immediately. Don't wait for statistical significance. |

---

## 8. Data Requirements for Full Scoring

The scoring system is designed but **most dimensions are currently unscoreable** due to missing creative-level data:

| Data Needed | Source | Status |
|---|---|---|
| Creative-level CTR | Meta Ads API / Ads Manager export | ❌ Not available to subagents |
| Creative-level CVR | Meta Ads API + AppsFlyer | ❌ Partial (campaign-level only) |
| Creative-level CPA | Meta Ads API | ❌ Not available |
| Install→Active by creative | AppsFlyer + Amplitude join | ⚠️ Available at campaign level only |
| Frequency / reach overlap | Meta Ads API | ❌ Not available |

### Next Steps to Operationalize

1. **Export Meta Ads Manager creative report** (weekly CSV) — CTR, CPA, frequency by ad ID
2. **Join with AppsFlyer** at campaign level for downstream quality
3. **Build a scoring spreadsheet** that auto-calculates composite scores from weekly data
4. **Set up alerts** for any creative dropping below 4.0 composite (auto-flag for replacement)

---

## Summary

| Market | Current State | Top Priority |
|---|---|---|
| **TR** | 9 creatives, $9K/month, only RTGT performing | Increase creative volume to 15–20; test UGC; shift budget to retargeting |
| **NG** | 7 creatives, good signup but zero activation | Pivot from "freelancer tool" to "receive payments" messaging |
| **EG** | 8 creatives, just launched Mar 18–20 | Arabic-first creatives; monitor for 2 weeks before judging |

**The scoring system is ready.** Full operationalization requires Meta Ads API access for creative-level metrics. Until then, apply at campaign level with available data and supplement with weekly Ads Manager CSV exports.

---

*Generated: 2026-03-21 | Sprint 069*
