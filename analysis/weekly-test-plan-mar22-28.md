# Weekly Test Plan — Mar 22–28, 2026

**Sprint:** S2 | **Owner:** Alp / Growth | **Status:** Execute

---

## 1) 🛑 Campaigns to PAUSE

| Campaign | Market | Weekly Spend | Reasoning |
|---|---|---:|---|
| **TR-Discovery-24.10.2025 (Demand Gen)** | TR | ~$560 | 5 months running, **0 installs**, ~$11.2K total waste. CPI = ∞. Engagement metrics masked zero outcomes. |
| **Appnext** | Multi | ~$220 | 273 installs → 0 new actives. $893/active. Fraud/junk traffic pattern. |
| **TikTok W2A** | TR | ~$350 | No measurable downstream conversions. W2A attribution chain broken same as Meta W2A. |
| **TR_Meta_web2app (non-RTGT prospecting)** | TR | ~$1,400 | $350/active — 18× worse than Pmax. Structural W2A friction. |

**Total freed:** ~$2,530/week (~$10,120/month). Redirect to scaling targets below.

---

## 2) 📈 Campaigns to SCALE

| Campaign | Market | Current Spend/wk | Change | New Spend/wk |
|---|---|---:|---|---:|
| **Google Pmax** | TR | $806 | **+$400/wk (+50%)** | $1,206 |
| **Apple Search Ads** | TR | $600 | **+$500/wk** | $1,100 |
| **Google Search (EG Generic)** | EG | $500 | **+$200/wk** | $700 |
| **Google Search Brand TR** | TR | $790 | Hold (switch to tCPA first) | $790 |

**Rationale:** Pmax = $19/active (best channel). ASA = $23/active + strongest downstream (254 withdrawals/wk). EG Generic = $9 CPI, cheapest market.

**Guardrail:** If Pmax CPA > $38 for 5 days → cap at pre-increase level. If ASA CPA > $45 → revert.

---

## 3) 🎨 Creative Tests to Launch

### 🇹🇷 Turkey
- **Test TR-C1:** UGC testimonial video (real user showing Cenoa transfer flow) vs current polished brand creative
  - *Hypothesis:* UGC drives 20%+ higher CTR in TR fintech (lower ad resistance)
  - *Success:* CTR ≥ 1.5%, CPA ≤ $25
  - *Timeline:* Launch Mon Mar 24, evaluate Day 7
  - *Kill:* CTR < 0.8% after 5K impressions OR CPA > $40 after 50 clicks
- **Test TR-C2:** CTA copy "Hemen Dene" (Try Now) vs "İndir" (Download) on RTGT campaign
  - *Hypothesis:* Action-oriented CTA lifts install CVR by 10%+
  - *Kill:* CVR < control after 3 days + 50 clicks

### 🇳🇬 Nigeria
- **Test NG-C1:** Messaging pivot — "Receive USD Payments Instantly" vs current "Cenoa for Freelancers"
  - *Hypothesis:* Transaction-intent copy drives activations (current: 44% signup, 0% activation)
  - *Success:* ≥ 1 withdrawal within 14 days from cohort
  - *Kill:* Signup rate drops below 20% AND 0 activations after 14 days

### 🇪🇬 Egypt
- **Test EG-C1:** Arabic-first explainer creative (educational app walkthrough) vs English variant
  - *Hypothesis:* Egyptian dialect copy lifts signup rate from 7% → 15%+
  - *Success:* Signup CVR ≥ 15%
  - *Kill:* CVR < 10% after 5K impressions
- **Note:** EG campaigns launched Mar 18 — give full 14-day window before judging. If 0 withdrawals by Apr 3 → pause.

---

## 4) 🔗 Landing Page Tests

### Test LP-A: CTA Button Copy A/B
- **Control:** App Store download buttons (current)
- **Variant:** Single "Open Free Account" button (device-detected routing)
- *Hypothesis:* Single CTA removes platform-choice friction, lifts CTA rate from 14.7% → 17%+
- *Success:* +2.3pp CTA rate (p < 0.05)
- *Sample needed:* ~3,500 visitors/variant (~1 week at current traffic)
- *Kill:* CTA rate drops below 13% after 3,500 visitors

### Test LP-B: Trust Badges Above Fold
- **Control:** Partner logos below fold (current)
- **Variant:** Badge row above fold — Lead Bank logo, "FDIC-insured", Stripe Verified, 256-bit encryption icon
- *Hypothesis:* Trust signals reduce bounce rate 5–10% and lift CTA rate 1–2pp
- *Success:* Bounce rate < 56% AND CTA rate ≥ 16%
- *Kill:* No improvement after 7 days + 3,500 visitors

### Pre-requisite: Run PageSpeed Insights on cenoa.com Monday — fix any LCP > 2.5s before launching A/B tests.

---

## 5) 💰 Bid Strategy Changes

| Campaign | Current Strategy | New Strategy | tCPA Target | When |
|---|---|---|---:|---|
| **Search Brand TR** | Max Conversions | **tCPA** | ₺500 (~$14) | Mon Mar 24 |
| **Search Freelancer TR** | (bundled) | **Break out + tCPA** | ₺200 (~$6) | Tue Mar 25 |
| **EG Generic** | Max Conversions | **tCPA** | ₺350 (~$10) | Mon Mar 24 |
| **Google App Android** | tCPA (auto) | **tCPA (explicit)** | ₺1,050 (~$30) | Wed Mar 26 |
| **Pmax TR** | Max Conversions | **Keep as-is** | — | — |
| **Competitor (Rakipler)** | Max Conv / Manual | **Manual CPC ₺15-20 cap** | — | Mon Mar 24, cut budget to ₺500/mo |

**Conversion action audit (Week 1 prerequisite):** Verify all campaigns use `af_app_install` as primary conversion — not web visits. This is likely why Demand Gen showed 0 installs.

**Learning period rule:** No further bid changes for 14 days after switch. Expect CPA volatility Week 1.

---

## 6) 📊 Test Summary Matrix

| Test ID | Hypothesis | Success Metric | Timeline | Kill Criteria |
|---|---|---|---|---|
| TR-C1 | UGC > polished brand | CTR ≥ 1.5%, CPA ≤ $25 | 7 days | CTR < 0.8% @ 5K imp |
| TR-C2 | "Hemen Dene" > "İndir" | CVR +10% vs control | 7 days | CVR < control @ 50 clicks |
| NG-C1 | Payment intent > freelancer | ≥ 1 withdrawal in cohort | 14 days | Signup < 20% + 0 activ @ 14d |
| EG-C1 | Arabic > English | Signup CVR ≥ 15% | 14 days | CVR < 10% @ 5K imp |
| LP-A | Single CTA > app badges | CTA rate +2.3pp | 7 days | CTA rate < 13% @ 3.5K visitors |
| LP-B | Trust badges above fold | Bounce < 56%, CTA ≥ 16% | 7 days | No improvement @ 3.5K visitors |
| Bid-1 | tCPA caps waste on Search | CPA stays within 120% of target | 14 days | CPA > 150% target for 5 days |

**Weekly checkpoint:** Friday Mar 28 — review early signals, kill underperformers, prepare Week 2 scaling decisions.

---

*Expected net impact of pauses + reallocation: +265 new actives/month at 33% lower blended CAC — budget-neutral.*

*Generated: 2026-03-22 | S2-007*
