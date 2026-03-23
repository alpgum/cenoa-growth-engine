# Pmax Scaling Implementation Plan — $500 → $1,500/week

**Ticket:** S3-017  
**Created:** 2026-03-23  
**Sources:** marginal-cac-curves.md, bid-strategy-reco.md, campaign-commentary-mar22.md, lookalike-reco.md  
**Campaign:** Pmax TR E-ihracat KYC_Start  
**Status:** 📋 Ready for implementation

---

## 1. Current State

| Metric | Value | Source |
|---|---|---|
| Weekly spend | ~$500–$806/wk (avg ~$500 recent, $806 early-Mar peak) | Sheets |
| Avg CAC (Cost/New Active) | **$19.18** | Sheets (early Mar) |
| CPI | $8.22 | campaign-commentary |
| Sign-up rate | 29% | campaign-commentary |
| Weekly new actives | ~42 | marginal-cac-curves |
| Monthly new actives | ~182 | marginal-cac-curves |
| Bid strategy | Maximize Conversions | bid-strategy-reco (inferred) |
| Diminishing returns exponent (α) | 0.25 | marginal-cac-curves |
| Scaling headroom (to $50 marginal CAC) | **14.6×** current spend | marginal-cac-curves |

**Why Pmax is the #1 scale lever:** Lowest CAC in the entire portfolio. ML-optimized bidding across all Google surfaces (Search, Display, YouTube, Discover). α = 0.25 means gentlest diminishing returns of any channel — every incremental dollar here returns more actives than anywhere else.

---

## 2. Target

| Metric | Current | Target | Change |
|---|---:|---:|---|
| Weekly spend | ~$500 | **$1,500** | **3×** |
| Monthly spend | ~$2,170 | ~$6,500 | 3× |
| Expected avg CAC at target | $19.18 | **~$26** | +35% |
| Expected weekly new actives | ~26 | **~58** | +123% |
| Expected monthly new actives | ~113 | ~250 | +123% |
| Marginal CAC on incremental $1,000/wk | — | ~$31 | Well within $50 threshold |

> **At $1,500/wk, marginal CAC is ~$31** — still well under the $50 sweet-spot ceiling. We have further headroom beyond this target, but 3× is the right first step to validate the model.

---

## 3. Ramp Schedule (+20% Every 3 Days)

**Why +20% per step:** Google's smart bidding re-enters "Learning" if budget changes exceed ~20% at once. Smaller steps keep the algorithm in steady state, preventing CPA spikes.

| Day | Date (if starting Mon Mar 24) | Daily Budget | Weekly Run-Rate | Δ from Previous | Cumulative Δ |
|---:|---|---:|---:|---|---|
| **1** | Mon Mar 24 | $86 | **$600** | +20% from $500 | +20% |
| **4** | Thu Mar 27 | $103 | **$720** | +20% | +44% |
| **7** | Sun Mar 30 | $123 | **$864** | +20% | +73% |
| **10** | Wed Apr 2 | $148 | **$1,037** | +20% | +107% |
| **13** | Sat Apr 5 | $178 | **$1,244** | +20% | +149% |
| **16** | Tue Apr 8 | $213 | **$1,493** | +20% | +199% |
| **17** | Wed Apr 9 | $214 | **$1,500** | Final adjust | **3×** ✅ |

**Total ramp duration:** ~17 days (2.5 weeks)

### Step-by-Step Actions

1. **Day 1 (Mar 24):** Set daily budget to $86/day in Google Ads console
2. **Day 4 (Mar 27):** Increase to $103/day — check CPI hasn't spiked >30%
3. **Day 7 (Mar 30):** Increase to $123/day — first weekly CPA review
4. **Day 10 (Apr 2):** Increase to $148/day — cross 2× baseline
5. **Day 13 (Apr 5):** Increase to $178/day — second weekly CPA review
6. **Day 16 (Apr 8):** Increase to $213/day — approaching target
7. **Day 17 (Apr 9):** Fine-tune to $214/day ($1,500/wk) — hold here

> ⚠️ **Do NOT change bid strategy during ramp.** Keep "Maximize Conversions" throughout. Only consider tCPA if CAC drifts above $35 for 2+ consecutive weeks post-ramp (per bid-strategy-reco.md).

---

## 4. Asset Group Review Checklist

Before scaling, ensure asset quality supports higher impression volume:

### Creative Assets

- [ ] **Headlines:** Minimum 5 headlines (max 15). Include: value prop ("Get paid in USD"), feature ("Virtual IBAN"), social proof ("50K+ freelancers"), urgency/CTA ("Start free today")
- [ ] **Long headlines:** Minimum 1 (max 5). Test: "The Dollar Account Built for Turkish Freelancers"
- [ ] **Descriptions:** Minimum 2 (max 5). Cover different angles: payments, card, KYC speed, fees
- [ ] **Images:** Minimum 3 landscape + 3 square + 1 portrait. Mix of: app screenshots, lifestyle, feature callouts. Refresh any assets older than 60 days
- [ ] **Videos:** At least 1 YouTube video (landscape + portrait versions). Pmax heavily utilizes YouTube inventory — missing video = missing placements
- [ ] **Logo:** Both landscape and square versions uploaded
- [ ] **Final URL:** Verify links to correct app store listing or deep-linked landing page (not generic cenoa.com)

### Asset Performance Audit

- [ ] Check asset performance labels in Google Ads: replace any "Low" performing assets
- [ ] Remove assets with <1% CTR after 1,000+ impressions
- [ ] A/B test 2-3 new headline variants before ramp starts (give 7 days to collect data)
- [ ] Ensure Turkish-language assets for TR audience (not English-only)

### Landing Page / Store Listing

- [ ] App Store / Play Store listing is optimized (screenshots, description, ratings)
- [ ] No broken deep links
- [ ] Store listing reflects current value prop (matches ad messaging)

---

## 5. Audience Signals to Add

Source: lookalike-reco.md — audience signals guide Pmax's ML but don't restrict targeting.

### Custom Segments (Competitor Keywords)

Add these as audience signals in the Pmax asset group:

| Segment | Keywords |
|---|---|
| **Competitor seekers** | "payoneer", "payoneer login", "payoneer withdrawal", "wise transfer", "wise business account", "transferwise", "paypal freelancer", "paypal receive payment", "revolut", "revolut USD account" |
| **Freelancer payments** | "freelancer payment", "get paid as freelancer", "freelance income", "receive USD payment", "freelancer ödeme", "yurtdışı gelir" |
| **USD banking** | "USD bank account", "dollar account", "usd hesabı", "dolar hesabı" |

### In-Market Segments

- Financial Services → Payment Services
- Financial Services → Banking Services → Online Banking
- Business Services → Freelance & Gig Work Platforms
- Financial Services → Currency Exchange & Money Transfer

### Affinity Segments

- Technophiles
- Business Professionals
- Avid Investors
- Aspiring Entrepreneurs

### Customer Lists (First-Party Data)

- [ ] Upload **Withdrawer** list as a signal (highest-LTV users — Pmax finds similar)
- [ ] Upload **KYC Completers** list as secondary signal
- [ ] Upload **Website Visitor** list (cenoa.com, 30d, from GA4)
- [ ] **Exclude** existing app installers (Firebase audience) to avoid paying for re-acquisition

### Life Events

- Starting a new job (correlates with freelancer onboarding)

> **Implementation note:** Add all signals BEFORE the ramp starts (Day 0 prep). Signals are suggestions, not restrictions — Pmax can and will go beyond them, but they accelerate the learning phase and improve initial targeting at higher budgets.

---

## 6. Conversion Action Verification

### ✅ Required: Optimize for `virtual_account_opened`, NOT `install`

| Setting | Required Value | Why |
|---|---|---|
| **Primary conversion action** | `virtual_account_opened` (or `virtual_account_created`) | This is the "new active" event — the metric we actually optimize for. Optimizing for install inflates volume with low-quality users who never activate. |
| **Secondary (observe only)** | `af_app_install`, `first_open`, `KYC_start` | Track these for funnel analysis but don't optimize bids toward them |
| **Remove / demote** | Any web-based conversions (page visits, form fills) | These dilute the conversion signal |

### Verification Steps

- [ ] Open Google Ads → Campaign → Settings → Conversions
- [ ] Confirm `virtual_account_opened` (or equivalent Firebase/AF event) is set as **primary** conversion action
- [ ] If currently set to `af_app_install` or `first_open`: **change to `virtual_account_opened`**
- [ ] ⚠️ Changing conversion actions resets learning — do this on **Day 0** (before ramp starts), not mid-ramp
- [ ] Verify conversion counting is set to **"One"** (not "Every") — we want unique users, not repeat events
- [ ] Confirm conversion window: 30-day click-through, 1-day view-through (standard for app campaigns)

### Why This Matters for Scaling

At $500/wk, even optimizing for install works okay because volume is low and the algorithm finds decent users by default. At $1,500/wk, the algorithm needs to bid 3× as aggressively — if it's optimizing for installs, it'll buy cheap, low-quality installs to hit volume. Optimizing for `virtual_account_opened` forces it to find users who actually activate, even if CPI rises. **This is the single most important setting for a successful scale-up.**

> **⚠️ Critical timing:** If conversion action needs changing, do it at least 7 days before Day 1 of the ramp (i.e., by Mar 17 if ramp starts Mar 24). This gives the algorithm time to recalibrate before budget increases begin.

---

## 7. Rollback Criteria

### Automatic Rollback Triggers

| Trigger | Threshold | Action |
|---|---|---|
| **CPI spike** | CPI rises **>30% above baseline** ($10.69+) for **3 consecutive days** | Revert to previous budget step |
| **CAC spike** | Cost/New Active exceeds **$35** for 3 consecutive days | Revert to previous budget step |
| **Zero conversions** | 0 new actives for **2 consecutive days** at any budget level | Pause ramp, investigate, revert to last known-good |
| **Spend runaway** | Daily spend exceeds **150%** of set daily budget | Reduce daily budget immediately, investigate |
| **Learning failed** | Google shows "Learning (limited)" status for **>7 days** | Pause ramp at current level, wait for learning to complete |

### Rollback Procedure

1. **Revert budget** to the previous step's daily amount (e.g., if issue at $148/day → revert to $123/day)
2. **Do NOT** change bid strategy or conversion actions during rollback — only change budget
3. **Hold** at reverted level for minimum 5 days
4. **Diagnose:** Check for creative fatigue, competitive pressure (auction insights), or seasonal effects
5. **Resume ramp** only when CPI returns to within 15% of pre-spike level for 3+ consecutive days
6. **If 2 rollbacks occur:** Pause at current budget, conduct full campaign audit before any further scaling

### What "Baseline" Means

- **CPI baseline:** Rolling 7-day average CPI before the current budget step was applied
- **CAC baseline:** Rolling 7-day average Cost/New Active before the current step
- Recalculate baseline at each budget step — some CAC increase is expected and healthy

---

## 8. Expected Outcomes at $1,500/wk

### From Marginal CAC Model (α = 0.25)

| Metric | At $500/wk | At $1,500/wk | At $1,500/wk (conservative) |
|---|---:|---:|---:|
| Avg CAC | $19.18 | **$25.73** | $28.50 |
| Marginal CAC | $25.57 | **$34.31** | $38.00 |
| Weekly new actives | ~26 | **~58** | ~53 |
| Monthly new actives | ~113 | **~250** | ~228 |
| Incremental actives/wk | — | **+32** | +27 |
| Incremental cost/wk | — | **+$1,000** | +$1,000 |
| Marginal cost per incremental active | — | **~$31** | ~$37 |

### Scenario Analysis

| Scenario | Weekly Actives | Avg CAC | Probability | Notes |
|---|---:|---:|---|---|
| 🟢 **Bull case** (α < 0.25) | 65+ | $23 | 25% | Creative refresh + audience signals outperform model |
| 🟡 **Base case** (α = 0.25) | ~58 | $26 | 50% | Model-predicted outcome |
| 🟠 **Conservative** (α = 0.30) | ~53 | $28 | 20% | Slightly faster diminishing returns than modeled |
| 🔴 **Bear case** (α > 0.35) | <45 | $33+ | 5% | Significant competitive pressure or creative fatigue |

### Financial Impact (Monthly, Base Case)

| Line Item | Current | At Target | Delta |
|---|---:|---:|---:|
| Monthly Pmax spend | ~$2,170 | ~$6,500 | +$4,330 |
| Monthly new actives | ~113 | ~250 | +137 |
| Blended CAC | $19.18 | ~$26 | +$6.82 |
| **Cost per incremental active** | — | **~$31.60** | — |

> At $31.60 per incremental active, Pmax at $1,500/wk is still the most efficient marginal spend in the portfolio. For comparison: ASA marginal CAC at similar scale increase would be ~$42, and Google Search ~$39.

---

## 9. Monitoring Plan

### Daily Check (First 2 Weeks — Mar 24 to Apr 7)

**Owner:** Marketing lead  
**Time:** Every morning, 10:00 AM Istanbul time  
**Duration:** 5-10 minutes

| Check | Where | What to Look For |
|---|---|---|
| **Daily spend** | Google Ads → Campaign → Overview | Actual spend vs. set budget (should be within ±20%) |
| **CPI** | Google Ads → Campaign → Cost/Conv | Compare to rolling 7-day baseline |
| **Conversion volume** | Google Ads → Conversions column | Minimum 3 conversions/day expected at $86+/day |
| **Learning status** | Google Ads → Campaign status column | Should show "Eligible" not "Learning (limited)" |
| **Search terms** | Google Ads → Insights → Search Terms | Check for irrelevant queries consuming budget |
| **Auction insights** | Google Ads → Auction Insights | Monitor competitor overlap and impression share |

### Decision Points

| Day | Decision |
|---|---|
| **Day 3** | First budget increase ($86 → $103). Only proceed if CPI is within 30% of baseline and >0 conversions/day |
| **Day 7** | First weekly review. Calculate week 1 blended CPA. Compare to $19.18 baseline. Proceed if CPA < $28 |
| **Day 10** | Cross 2× spend threshold. Extra scrutiny on quality — check downstream sign-up rate (should be >25%) |
| **Day 14** | Two-week checkpoint. Full funnel review: installs → sign-ups → KYC → virtual_account → withdrawal. Decide: continue ramp / hold / rollback |
| **Day 17** | Ramp complete. Set final budget ($214/day). Monitor for 1 more week before declaring success |
| **Day 24** | One-week post-ramp. If CPA is stable at <$30, ramp is successful. Transition to weekly monitoring. |

### Weekly Monitoring (After Ramp Completes)

| Cadence | Check |
|---|---|
| **Weekly** | CPA trend, conversion volume, impression share, asset performance |
| **Bi-weekly** | Full funnel review (install → active → withdrawal), creative refresh assessment |
| **Monthly** | Marginal CAC vs. model prediction, budget reallocation review |

### Alerting

- Set up **Google Ads automated rules:**
  - Alert if daily spend > $300 (140% of target daily budget)
  - Alert if CPI > $15 (1.8× baseline) for any single day
  - Alert if conversions = 0 for any day with spend > $50

---

## 10. Pre-Launch Checklist (Complete Before Day 1)

### Must-Do (Blockers)

- [ ] **Conversion action:** Verify `virtual_account_opened` is primary (Section 6) — change 7+ days before ramp if needed
- [ ] **Asset review:** All asset groups pass quality check (Section 4) — replace any "Low" performing assets
- [ ] **Audience signals:** Add competitor keywords, in-market segments, and customer lists (Section 5)
- [ ] **Exclusion lists:** Upload existing app installers as exclusion audience
- [ ] **Budget calculation:** Confirm current daily budget in Google Ads matches ~$71/day ($500/wk)
- [ ] **Baseline snapshot:** Record current CPI, CPA, conversion volume, impression share (rolling 7-day)

### Should-Do (Improve Outcomes)

- [ ] Upload at least 1 video asset (landscape + portrait) for YouTube placements
- [ ] Add Turkish-language headline variants
- [ ] Set up Google Ads automated alert rules (Section 9)
- [ ] Create monitoring dashboard or spreadsheet for daily tracking
- [ ] Brief the team on the ramp schedule and rollback criteria

### Nice-to-Have

- [ ] A/B test 2-3 new creative variants (start 7 days before ramp)
- [ ] Review Auction Insights for competitive landscape changes
- [ ] Set up Looker Studio or Sheets auto-refresh for daily CPA tracking

---

## Appendix: Key References

| Document | Key Insight |
|---|---|
| marginal-cac-curves.md | Pmax α = 0.25, 14.6× headroom to $50 marginal CAC |
| bid-strategy-reco.md | Keep Maximize Conversions, scale to $1,200/wk (we're going to $1,500) |
| campaign-commentary-mar22.md | Pmax is #1 performer at $19.18/active, recommended for +50% scale |
| lookalike-reco.md | Withdrawer seeds, competitor keywords, in-market segments for audience signals |

---

*[S3-017] Pmax Scaling Plan | 2026-03-23*
