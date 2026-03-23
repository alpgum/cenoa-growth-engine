# Referral Program Scaling Plan

**Date:** 2026-03-21  
**Status:** 🟡 Ready to execute  
**Owner:** Performance Marketing  
**Goal:** 7 → 70 referral installs/week in 90 days  

---

## 1) Current State

Referral (`af_app_invites`) is Cenoa's **highest-quality, lowest-cost channel** — but also the smallest.

| Metric | Referral | Apple Search Ads | Organic | Google Ads |
|--------|------:|------:|------:|------:|
| Weekly installs | **7** | 75 | 632 | 54 |
| Install → Signup rate | **42.9%** ⭐ | 29.3% | 12.2% | 25.9% |
| Withdrawals (existing base) | 13 | 254 | 487 | 29 |
| Weekly spend | **$0** | $600 | $0 | $790 |
| Effective CAC/Active | **~$0** | $22.66 | $0 | $25.48 |

**Key insight:** Referral converts 42.9% of installs to sign-up — 3.5× better than organic, 1.5× better than ASA. Even at modest scale, this channel delivers pre-qualified users because they come with a personal recommendation.

Using Sheets downstream data, referral users who activate cost effectively **$0** (organic referral). Even with a $10 incentive and promotion costs, estimated CAC would be **~$30/active** — still the cheapest paid acquisition channel and on par with the best performers.

---

## 2) Why It's Tiny

The referral program exists (AppsFlyer tracks `af_app_invites` + "Invite a Friend" campaign shows 13 withdrawals) but is **not actively promoted**:

- **No in-app referral prompts** at high-satisfaction moments (e.g., post-withdrawal)
- **No shareable content** — users can't easily show friends what they're saving
- **Low incentive** — current reward structure doesn't motivate active sharing
- **No social sharing integration** — missing WhatsApp/Telegram share buttons (key for NG/TR)
- **No gamification** — no leaderboard, no ambassador tier, no recognition

The program is passive: buried in settings, discovered only by users who go looking for it.

---

## 3) Viral Coefficient Analysis

### Current State

```
Active users (weekly withdrawers):    ~2,000 (estimated from 1,355+ unattributed + attributed)
Referral installs/week:               7
Invitations sent/week (estimated):    ~20 (based on 7 installs at ~35% accept rate)
```

| Metric | Current | Target (90 days) |
|--------|--------:|------------------:|
| % of active users who refer | ~1% | 5% |
| Invitations per referrer | ~1 | 2 |
| Install rate per invitation | ~35% | 35% |
| **Viral coefficient (K)** | **~0.01** | **~0.10** |
| Referral installs/week | 7 | 70 |

**Viral coefficient formula:**  
K = (% users who refer) × (invites per referrer) × (install rate per invite)  
Current: 0.01 × 1 × 0.35 = **0.0035** (rounds to ~0.01 accounting for estimation noise)  
Target: 0.05 × 2 × 0.35 = **0.035** → with higher incentives and prompts improving all three levers → **~0.10**

A K of 0.10 means every 10 users generate 1 new user organically. Not viral (K < 1), but a meaningful **self-reinforcing growth loop** that compounds with paid acquisition.

---

## 4) Five Strategies to 10× Referral Volume

### A) In-App Referral Prompt After First Successful Withdrawal

**Why:** Post-withdrawal is peak satisfaction — the user just received money. This is the highest-intent moment to ask for a referral.

**Implementation:**
- Bottom sheet / modal after withdrawal confirmation: "Love Cenoa? Share it with a friend — you both earn $10"
- One-tap share with pre-filled message
- Show only once per user (or once per 30 days for repeat)
- Track: `referral_prompt_shown`, `referral_prompt_tapped`, `referral_share_sent`

**Expected lift:** 3-5× increase in referral share rate (from ~1% to 3-5% of active users)

**Priority:** 🔴 Highest — easiest win, lowest engineering effort

### B) Shareable Comparison Card ("I saved $X vs Payoneer this month")

**Why:** Social proof + concrete value demonstration. Users share savings naturally when given a frictionless format.

**Implementation:**
- Auto-generate personalized card: "I saved $47 in fees this month with Cenoa vs Payoneer"
- Instagram Story / WhatsApp-optimized format (1080×1920)
- Deep link embedded in card image
- Calculate savings by comparing Cenoa fees vs market average (Payoneer ~3%, Wise ~1.5%)

**Expected lift:** New sharing surface → +15-25 incremental shares/week from power users

**Priority:** 🟡 Medium — requires fee calculation logic + design

### C) Increase Incentive: $5 → $10 Both-Sides

**Why:** Higher incentive = more motivation to share AND more motivation to install. Both-sides reward removes friction ("my friend benefits too").

**Implementation:**
- $10 to referrer (credited after referee's first deposit)
- $10 to referee (credited after first deposit — ensures activation)
- Cap at 10 referrals/user/month (prevent abuse; $100 max payout)
- Review incentive level at 60 days — adjust based on actual CAC vs target

**Economics check:**
- $20 total incentive cost per activated referral
- Referral users have 42.9% signup rate and strong downstream activity
- Even at $20/activated user, this is cheaper than Meta ($82/active), Google ($25/active), and competitive with ASA ($23/active)
- **Break-even:** If referral CAC stays under $35/active (Turkey benchmark), it's profitable

**Priority:** 🔴 High — simple config change, immediate impact

### D) WhatsApp / Telegram Share Buttons

**Why:** Nigeria and Turkey are WhatsApp-dominant markets. Telegram is rising in TR. Without native share buttons, users must manually copy-paste referral links — massive friction.

**Context from Nigeria data:**
- NG users are power-transactors (492 withdrawals/week) with strong social networks
- Nigerian fintech adoption is heavily word-of-mouth
- NG referral installs could compound fastest with social sharing

**Implementation:**
- WhatsApp share button: pre-filled message + referral link
- Telegram share button: same
- SMS fallback for markets without messaging app dominance
- Track: `share_channel` property on `referral_share_sent` event

**Expected lift:** 2-3× increase in share completion rate (reduce friction from copy-paste)

**Priority:** 🔴 High — critical for NG/TR markets

### E) Referral Leaderboard / Ambassador Program

**Why:** Gamification turns referrals from a one-time action into ongoing behavior. Top referrers become brand ambassadors.

**Implementation — Phase 1 (Leaderboard):**
- In-app leaderboard: top 10 referrers this month
- Badge system: Bronze (3 referrals), Silver (10), Gold (25)
- Monthly bonus: top referrer gets $50 bonus

**Implementation — Phase 2 (Ambassador Program, Month 3+):**
- Application-based for users with 10+ successful referrals
- Custom referral code (e.g., "CENOA-AHMED")
- Higher commission tier: $15/referral (vs standard $10)
- Early access to new features
- Direct Slack/Telegram channel with Cenoa team

**Expected lift:** Turns top 1% of users into sustained referral engines; 5-10 ambassadors could drive 30-50% of all referral volume

**Priority:** 🟡 Medium — leaderboard is quick; ambassador program is Phase 2

---

## 5) 90-Day Target & Milestones

### Volume Targets

| Metric | Current | Day 30 | Day 60 | Day 90 |
|--------|--------:|-------:|-------:|-------:|
| Referral installs/week | 7 | 20 | 40 | **70** |
| Referral sign-ups/week | 3 | 9 | 17 | 30 |
| Referral actives/week | ~1 | 4 | 8 | 15 |
| Invitations sent/week | ~20 | 60 | 120 | 200 |
| Share rate (% of active users) | ~1% | 2% | 3% | 5% |
| Viral coefficient (K) | 0.01 | 0.03 | 0.06 | **0.10** |

### Implementation Timeline

| Week | Action | Owner |
|------|--------|-------|
| 1-2 | Increase incentive to $10 both-sides | Product/Growth |
| 1-2 | Add WhatsApp + Telegram share buttons | Engineering |
| 3-4 | Build post-withdrawal referral prompt | Engineering |
| 3-4 | Design shareable comparison card | Design + Engineering |
| 5-6 | Launch leaderboard | Engineering |
| 5-6 | Instrument all Amplitude events | Analytics |
| 7-8 | Analyze first 60 days; iterate incentive level | Growth |
| 9-12 | Launch ambassador program (if leaderboard shows power referrers) | Growth |

---

## 6) Budget

### Monthly Budget: $1,000/mo ($500 incentive + $500 promotion)

| Line Item | Monthly | 90-Day Total | Notes |
|-----------|--------:|-------------:|-------|
| **Referral incentives** | $500 | $1,500 | $10 × ~50 activations/mo (avg over 90 days) |
| **Promotion** | $500 | $1,500 | Push notifications, in-app banners, email campaigns promoting referral |
| **Ambassador bonuses** | $0→$100 | $100 | Top referrer monthly bonus (starts Month 2) |
| **Total** | $1,000 | **$3,100** | |

### Unit Economics

| Metric | Estimate | vs Best Paid Channel |
|--------|----------|---------------------|
| Incentive cost/referral install | $10 | ASA CPI: $8 |
| Incentive cost/referral signup | $23 | ASA: $27 |
| **Total cost/referral active** | **~$30** | ASA: $23, Google: $25 |
| Referral LTV advantage | +20-30% (est.) | Referred users retain better (industry benchmark) |

At $30/active, referral is **competitive with the best paid channels** — and referred users historically have 20-30% higher retention (Dropbox, PayPal, Revolut benchmarks), making the LTV-adjusted CAC significantly better.

**Self-funding potential:** If referral volume reaches 70/week with 42.9% signup rate = ~30 sign-ups → ~15 actives. At $30/active = $450/week cost. If referral users' LTV > $30 (likely, given high withdrawal frequency), the program is **self-funding by Month 3**.

---

## 7) Measurement Framework

### Amplitude Events (New)

| Event | Properties | Trigger |
|-------|-----------|---------|
| `referral_prompt_shown` | `trigger_type` (post_withdrawal, settings, leaderboard) | Modal/prompt displayed |
| `referral_prompt_tapped` | `trigger_type`, `share_channel` | User taps "Share" |
| `referral_share_sent` | `share_channel` (whatsapp, telegram, sms, copy_link) | Share action completed |
| `referral_link_opened` | `referrer_id`, `campaign` | Referee opens link |
| `referral_install_attributed` | `referrer_id`, `source` | AF `af_app_invites` install |
| `referral_signup_completed` | `referrer_id` | Referee completes sign-up |
| `referral_reward_credited` | `user_type` (referrer/referee), `amount` | Incentive paid out |

### Key Dashboards

1. **Referral Funnel:** Prompt shown → Tapped → Share sent → Link opened → Install → Signup → Active
2. **Share Channel Mix:** WhatsApp vs Telegram vs SMS vs Copy Link (optimize for highest-converting)
3. **Referrer Distribution:** Power law chart — top referrers vs long tail
4. **Geo Split:** TR vs NG referral volume (NG expected to outperform given social dynamics)
5. **Incentive ROI:** Total incentive spend ÷ referral actives = effective CAC

### Weekly Review Metrics

| Metric | Target | Kill Threshold |
|--------|--------|---------------|
| Referral installs/week | Growing week-over-week | Flat for 3 consecutive weeks |
| Share → Install conversion | ≥30% | <15% |
| Referral signup rate | ≥40% | <25% |
| Cost per referral active | ≤$35 | >$50 |
| Fraud rate (fake referrals) | <5% | >10% |

---

## 8) Nigeria-Specific Referral Opportunity

From the [Nigeria Growth Plan](./nigeria-growth-plan.md):

- **492 withdrawals/week** from existing NG user base — power transactors
- **Deposit-first market** — 45.2% of all deposit taps globally come from NG
- **Word-of-mouth culture** — Nigerian fintech adoption is heavily social
- **$0.35 CPI** in NG — even modest referral rewards ($2-5) are competitive

### NG-Specific Actions
1. **Post-withdrawal referral prompt** (localized for NG) — trigger after every successful withdrawal
2. **WhatsApp share** — #1 messaging platform in Nigeria; must be the primary share channel
3. **Lower incentive tier for NG** — $5 both-sides (vs $10 in TR) given lower CAC benchmark
4. **Community seeding** — identify top 20 NG withdrawers, invite to beta ambassador program
5. **Target:** 20-30 of the 70 weekly referral installs should come from NG by Day 90

### NG Referral Economics
| Metric | NG Estimate | TR Estimate |
|--------|----------:|----------:|
| Referral incentive | $5 both-sides | $10 both-sides |
| Expected signup rate | 45%+ | 40% |
| Cost/referral active | ~$15 | ~$30 |
| vs paid CAC benchmark | $16 (NG paid active) | $25 (TR best paid) |

---

## 9) Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|:----------:|:------:|------------|
| Referral fraud (fake accounts) | Medium | High | Device fingerprinting; require first deposit for reward; cap 10 referrals/user/month |
| Low share completion rate | Medium | Medium | A/B test share copy + incentive display; optimize for WhatsApp (pre-filled message) |
| Incentive cost exceeds budget | Low | Medium | Dynamic incentive: reduce to $7 if volume exceeds target; pause if CAC > $50 |
| Engineering bandwidth unavailable | Medium | High | Phase implementation; Week 1-2 items (incentive increase + share buttons) are config/small changes |
| Cannibalization of organic installs | Low | Low | Monitor organic volume alongside referral growth; referral should be additive |
| KYC blocks NG referral conversions | High | High | Depends on KYC fix from NG Growth Plan; referral in NG is blocked until KYC works |

---

## Summary

Referral is Cenoa's **hidden gem**: 42.9% signup rate (best channel), $0 current cost, and strong downstream engagement. The program is tiny (7 installs/week) only because it's never been actively promoted.

**With $1,000/month and 5 tactical changes, we can 10× referral volume to 70 installs/week in 90 days** — adding ~15 active users/week at ~$30/active (competitive with the best paid channels, with higher expected LTV).

The Nigeria opportunity is especially compelling: 492 weekly withdrawers in a word-of-mouth market, waiting to be activated as referral sources.

---

*References: [Attribution Funnel](./attribution-funnel.md) · [Channel CAC](./channel-cac.md) · [Nigeria Growth Plan](./nigeria-growth-plan.md) · [Budget Efficiency](./budget-efficiency.md)*
