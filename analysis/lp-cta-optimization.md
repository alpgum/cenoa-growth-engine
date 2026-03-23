# Landing Page CTA Optimization Brief

**Sprint:** 063  
**Date:** 2026-03-21  
**Owner:** Growth / Performance Marketing  
**Status:** Ready for implementation

---

## 1. Current Performance Baseline

**Source:** GA4 + Looker (Mar 14–20, 2026)

| Metric | Value | Assessment |
|---|---:|---|
| **Total Sessions** | 6,317 | Weekly cenoa.com traffic |
| **CTA Click Rate** | 14.72% | ~930 CTA clicks/week |
| **Bounce Rate** | 60.99% | ⚠️ High — 6 in 10 visitors leave without interaction |
| **Avg Session Duration** | ~1:45 | Moderate engagement |

### Current CTA Copy (cenoa.com as of Mar 21)

- **Headline:** "Get paid globally — 10x cheaper than Payoneer"
- **Sub-headline:** "Open free US and EU accounts in 3 minutes — powered by Stripe, Lead Bank, and USDC (Circle)."
- **Primary CTA:** App store download buttons (no single text CTA button above fold)
- **Social proof:** "Serving 500,000+ professionals from 35+ countries"

---

## 2. Top Landing Pages Breakdown

**Source:** Looker Studio dashboard

| Landing Page | Sessions (est.) | CTA Rate | Bounce Rate | Notes |
|---|---:|---:|---:|---|
| `/pakistan-waitlist-v2` | ~1,800 | Higher than avg | Lower | Geo-specific, high intent |
| `/` (homepage) | ~2,500 | 14.72% (blended) | 60.99% | Main traffic driver |
| `/blog/accepted-proof` | ~600 | Lower | Higher | Content/SEO traffic, low purchase intent |

### Key Observations

1. **Pakistan waitlist page outperforms homepage** — geo-specific messaging + waitlist scarcity drives better engagement
2. **Homepage carries most volume** but has the highest optimization ceiling
3. **Blog traffic converts poorly** — needs separate CTA strategy (email capture vs app download)

---

## 3. Architect LP Insight: Egypt Tests

**Source:** Trafik Canavarı sheet (Architect LP results — referenced in sprint notes)

| Test | Market | Finding |
|---|---|---|
| Architect LP variant | Egypt | **27% cheaper CTA cost** vs standard LP |
| Standard LP | Egypt | Higher CPA, generic messaging |

### What Made Architect LP Work

- **Localized headline** addressing specific Egypt use case (USD savings)
- **Simplified page structure** — fewer sections, faster to scan
- **Single clear CTA** instead of multiple competing actions
- **Lesson:** Geo-specific, simplified pages with one clear action outperform generic global pages

---

## 4. Competitor LP Analysis

### Payoneer (payoneer.com)

| Element | Payoneer Approach | Cenoa Gap |
|---|---|---|
| **Headline** | "Get paid by international clients" — benefit-first, audience-specific | Cenoa's "10x cheaper" is comparison-first |
| **CTA** | "Register Now" — single prominent button above fold | Cenoa has app store buttons, less prominent |
| **Trust** | Visa/Mastercard logos, "Trusted by 5M+ businesses" prominently displayed | Cenoa has partner logos below fold |
| **Social Proof** | Customer count + specific use cases (freelancers, marketplaces) | Cenoa's "500K+ professionals" is above fold ✅ |
| **Calculator** | Interactive fee comparison tool | Cenoa has static comparison table ✅ |

### Wise (wise.com)

| Element | Wise Approach | Cenoa Gap |
|---|---|---|
| **Headline** | "The international account" — simple, clear | More concise than Cenoa |
| **CTA** | "Open an account" — single green button, impossible to miss | CTA clarity gap |
| **Trust** | FCA regulated, transparent fee breakdown, real exchange rate | Cenoa mentions partners but not regulation prominently |
| **UX** | Ultra-clean, minimal page — loads in <1s | Cenoa has more sections, longer scroll |
| **Speed** | Core Web Vitals optimized, AMP pages for key markets | Unknown for Cenoa |

### Key Competitor Takeaways

1. **Single, unmissable CTA button** (not app store badges)
2. **Benefit-first headlines** that answer "what's in it for me?"
3. **Trust signals above the fold** (not buried below)
4. **Minimalist design** — fewer distractions = higher conversion

---

## 5. Five Specific Changes to Test

### Test 5A: Headline — Benefit-First vs Feature-First

| Variant | Copy | Rationale |
|---|---|---|
| **Control** | "Get paid globally — 10x cheaper than Payoneer" | Current — comparison-based |
| **V1** | "Your US Bank Account, Ready in 3 Minutes" | Benefit + speed anchor |
| **V2** | "Get Paid from Anywhere. Keep More of Your Money." | Benefit-first, no competitor mention |

**Expected impact:** Headlines account for 40-60% of LP engagement decisions. A stronger benefit-first headline could lift CTA rate 1-2pp.

**Implementation:** Client-side A/B split via Google Optimize or Webflow variant pages.

---

### Test 5B: CTA Button Copy

| Variant | Copy | Psychology |
|---|---|---|
| **Control** | App store download buttons | Standard but passive — user must choose platform |
| **V1** | "Open Free Account" | Low friction, emphasizes free |
| **V2** | "Start Earning in USD" | Outcome-driven, aspirational |
| **V3** | "Get Your US Bank Account" | Specific, tangible benefit |

**Expected impact:** CTA button copy changes typically yield 5-15% relative lift. Moving from app store badges to a single action button removes decision friction.

**Implementation:** Single prominent button above fold → routes to app store based on device detection.

---

### Test 5C: Social Proof Above Fold

| Variant | Element | Placement |
|---|---|---|
| **Control** | "500,000+ professionals" counter (exists, small) | Below headline |
| **V1** | Testimonial card: "I saved $2,400/year switching from Payoneer" — Ali, Pakistan | Above fold, next to CTA |
| **V2** | Live counter: "12,847 accounts opened this month" | Animated, below headline |
| **V3** | Star rating: "⭐ 4.8 on App Store (2,300+ reviews)" | Next to CTA button |

**Expected impact:** Social proof above fold consistently lifts conversion 10-15% in fintech. Most impactful for new visitors from paid channels.

**Implementation:** Webflow component swap; testimonials from real users (get consent).

---

### Test 5D: Trust Signals Enhancement

| Current State | Proposed Addition |
|---|---|
| Stripe + Lead Bank mentioned in body copy | **Badge row above fold:** Lead Bank logo, Stripe Verified Partner, FDIC-insured callout, 256-bit encryption icon |
| Security not prominently featured | **"Your funds are held at Lead Bank, Member FDIC"** below CTA |
| No regulatory messaging | **"Licensed & Regulated"** with relevant compliance badges |

**Expected impact:** Trust is the #1 barrier for fintech first-time visitors. Adding visible trust signals typically reduces bounce rate 5-10% and lifts CTA rate 1-2pp.

**Implementation:** Design badge row component; legal review of claims before publishing.

---

### Test 5E: Page Speed & Core Web Vitals

| Metric | Target | Action |
|---|---|---|
| **LCP (Largest Contentful Paint)** | < 2.5s | Optimize hero image, lazy-load below-fold content |
| **FID (First Input Delay)** | < 100ms | Defer non-critical JS |
| **CLS (Cumulative Layout Shift)** | < 0.1 | Set explicit image dimensions, preload fonts |
| **Total page weight** | < 1MB | Compress images, remove unused CSS/JS |

**Expected impact:** Every 100ms of load time improvement = ~1% conversion gain. If current LCP is >4s, fixing to <2.5s could lift CTA rate 2-3%.

**Action required:** Run PageSpeed Insights on cenoa.com, establish baseline, fix critical issues before A/B tests (faster page = cleaner test results).

---

## 6. Measurement Plan

### GA4 Events to Track Per Test

| Event Name | Parameters | Purpose |
|---|---|---|
| `lp_variant_impression` | `variant_id`, `test_id`, `page_path`, `traffic_source` | Track which variant each user sees |
| `cta_click` | `variant_id`, `test_id`, `cta_text`, `cta_position` | Primary metric |
| `page_scroll_depth` | `variant_id`, `percent` (25/50/75/100) | Engagement depth |
| `app_store_redirect` | `variant_id`, `store` (ios/android), `source` | Post-CTA conversion |
| `time_on_page` | `variant_id`, `seconds_bucket` | Engagement quality |
| `bounce` | `variant_id`, `time_to_bounce` | Negative signal |

### Amplitude Events (Post-Install Attribution)

| Event Name | Purpose |
|---|---|
| `signup_completed` (with `lp_variant` user property) | Full-funnel attribution |
| `kyc_submitted` (attributed) | Quality signal — did the LP variant attract real users? |
| `first_deposit` (attributed) | Revenue attribution |

### Dashboard Requirements

- [ ] GA4 custom report: CTA rate by variant, by traffic source, by device
- [ ] Amplitude cohort: users from each LP variant → D7/D30 retention
- [ ] Daily Slack alert if any variant's bounce rate spikes >70%
- [ ] Weekly summary: variant performance vs control

### Statistical Rigor (from A/B Test Framework — Test B)

| Parameter | Value |
|---|---|
| Baseline CTA rate | 14.72% |
| MDE | 2.28pp (→ 17%) |
| Required sample per variant | ~3,500 visitors |
| Minimum runtime | 7 days (day-of-week effects) |
| Significance threshold | p < 0.05 (Bonferroni-corrected for multi-variant: p < 0.017) |
| Power | 80% |

---

## 7. Expected Impact

### Conservative Scenario (14.72% → 18%)

| Metric | Current | Target | Delta |
|---|---:|---:|---:|
| Weekly sessions | 6,317 | 6,317 | — |
| CTA rate | 14.72% | 18.0% | +3.28pp |
| Weekly CTAs | 930 | 1,137 | **+207 CTAs/week** |
| Monthly CTAs | 3,720 | 4,548 | **+828 CTAs/month** |

### Impact on Downstream Funnel

Assuming current install-to-signup rate (83.5%) and signup-to-active rate hold:

| Stage | Current Weekly | Projected Weekly | Delta |
|---|---:|---:|---:|
| CTA clicks | 930 | 1,137 | +207 |
| Installs (est. 70% of CTAs) | 651 | 796 | +145 |
| Signups (83.5%) | 544 | 665 | +121 |
| New Actives (est. ~7%) | 38 | 47 | +9 |

### Revenue Impact Estimate

At current CPA of ~$85/active user (Turkey), +9 organic actives/week = **$765/week in equivalent paid acquisition value** saved, or **~$3,060/month** in CAC efficiency.

### Optimistic Scenario (14.72% → 20%)

If multiple tests compound (headline + CTA button + trust signals):

| Metric | Value |
|---|---|
| Weekly CTAs | 1,263 |
| Delta vs current | +333 CTAs/week |
| Additional monthly actives | +60 |
| Monthly CAC equivalent saved | ~$5,100 |

---

## 8. Implementation Roadmap

| Priority | Test | Effort | Timeline | Risk |
|---|---|---|---|---|
| **P0** | 5E — Page Speed audit | 1 day | Week 1 | None — do before other tests |
| **P1** | 5B — CTA Button Copy | 2 days | Week 1-2 | Low |
| **P1** | 5A — Headline Test | 1 day | Week 1-2 | Low |
| **P2** | 5C — Social Proof | 3 days | Week 2-3 | Low (need testimonial consent) |
| **P2** | 5D — Trust Signals | 2 days | Week 2-3 | Medium (legal review needed) |

### Sequencing Notes

1. Fix page speed FIRST — it improves all subsequent tests' reliability
2. Run headline + CTA button tests simultaneously (different page sections, no interaction)
3. Social proof + trust signals as follow-up tests once winner from round 1 is established
4. Don't test more than 2 elements simultaneously to maintain clean attribution

---

## 9. Open Questions

- [ ] What is cenoa.com's current PageSpeed Insights score? (Run audit)
- [ ] Can we get 3-5 real user testimonials with consent for LP use?
- [ ] Is Webflow's built-in A/B testing sufficient, or do we need Google Optimize / VWO?
- [ ] What % of cenoa.com traffic is mobile vs desktop? (Affects CTA design)
- [ ] Can we implement device-based smart routing (single CTA → correct app store)?
- [ ] Legal review: Can we display "FDIC-insured" on the LP? (Lead Bank partnership terms)

---

*Cross-references:*
- *[Global Funnel Analysis](./global-funnel.md) — full funnel data*
- *[A/B Test Framework](./ab-test-framework.md) — Test B: LP CTA Copy Test*
- *[Trafik Canavarı](../data/sheets-trafik-canavari.md) — historical performance data*

*Last updated: 2026-03-21*
