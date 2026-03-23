# A/B Test Framework — Cenoa Performance Marketing

> Living document for structured experimentation across acquisition, activation, and retention.

---

## 1. Test Template Structure

Every test MUST follow this template before launch:

```
### Test: [Name]

**Hypothesis:**
"If we [change], then [metric] will [improve/decrease] by [X%]"

**Primary Metric:** The single metric that determines success/failure
**Guardrail Metrics:** Metrics that must NOT degrade (safety rails)

**Audience:**
- Traffic split: [X% control / Y% variant]
- Segment: [All users / New users / Geo / Platform]
- Exclusions: [Any excluded cohorts]

**Duration & Sample Size:**
- Minimum detectable effect (MDE): [X%]
- Baseline conversion rate: [X%]
- Required sample per variant: [N] (α=0.05, β=0.2 → 80% power)
- Estimated duration: [X days] at current traffic

**Success Criteria:**
- Statistical significance: p < 0.05 (two-tailed)
- Minimum runtime: 2 full weeks (capture weekday/weekend cycles)
- Practical significance: lift must exceed [X%] to justify implementation cost

**Decision Rules:**
- ✅ Ship if: primary metric improves at p<0.05 AND no guardrail degrades >5%
- ⏸️ Extend if: trending positive but p>0.05 after minimum duration
- ❌ Kill if: guardrail metric degrades >5% at p<0.10 OR primary metric negative at p<0.05
```

### Minimum Sample Size Formula

```
n = (Z_α/2 + Z_β)² × [p₁(1-p₁) + p₂(1-p₂)] / (p₂ - p₁)²

Where:
  Z_α/2 = 1.96 (for α = 0.05, two-tailed)
  Z_β   = 0.84 (for 80% power)
  p₁    = baseline conversion rate
  p₂    = expected conversion rate (baseline + MDE)
```

For quick estimation: use [Evan Miller's calculator](https://www.evanmiller.org/ab-testing/sample-size.html) or Amplitude's built-in experiment sizing.

---

## 2. Ready-to-Run Test Ideas

### Test A: KYC Flow Simplification

**Hypothesis:**
"If we reduce the KYC submission flow from 5 steps to 3 steps (combining document upload + selfie into a single screen, removing redundant confirmation step), then the KYC submit rate will improve from 5.8% to 7.5% (+29% relative lift)."

**Primary Metric:** KYC submit rate (users who complete KYC submission / users who start KYC)
**Guardrail Metrics:**
- KYC approval rate (must not drop — fewer steps shouldn't mean worse submissions)
- Document quality rejection rate (must not increase >10% relative)
- Fraud/fake document rate

**Audience:**
- Traffic split: 50% control / 50% variant
- Segment: All new users who reach KYC step (post-signup)
- Exclusions: Users who already completed KYC, re-verification flows

**Duration & Sample Size:**
- MDE: 1.7pp (5.8% → 7.5%)
- Baseline: 5.8%
- Required sample per variant: ~4,200 users
- Estimated duration: 3–4 weeks (depending on signup volume reaching KYC)

**Success Criteria:**
- p < 0.05, minimum 14 days runtime
- Practical significance: ≥1pp lift (absolute) justifies engineering effort
- KYC approval rate must not drop more than 2pp

**Amplitude Events to Track:**
| Event | Purpose |
|---|---|
| `kyc_flow_started` | Entry to funnel |
| `kyc_step_completed` (with step property) | Per-step progression |
| `kyc_document_uploaded` | Document submission |
| `kyc_selfie_captured` | Selfie step |
| `kyc_submitted` | Primary metric trigger |
| `kyc_approved` / `kyc_rejected` | Guardrail downstream |
| `kyc_flow_abandoned` (with step property) | Drop-off diagnosis |

**Risk Assessment:**
| Risk | Severity | Mitigation |
|---|---|---|
| Lower document quality from rushed flow | Medium | Monitor rejection rate daily; kill switch at +10% rejections |
| Compliance concern (fewer review screens) | High | Pre-clear simplified flow with compliance team before launch |
| Technical bugs in new flow | Medium | QA + 5% canary rollout for 48h before full 50/50 |

---

### Test B: Landing Page CTA Copy Test

**Hypothesis:**
"If we change the cenoa.com primary CTA from the current copy to a benefit-driven variant ('Start Saving in USD' vs generic 'Sign Up'), then the landing page conversion rate will improve from 14.72% to 17% (+15.5% relative lift)."

**Variants:**
- **Control:** Current CTA copy
- **Variant 1:** "Start Saving in USD" (benefit-driven)
- **Variant 2:** "Open Your Dollar Account — Free" (benefit + price anchor)
- **Variant 3:** "Join 50K+ Savers" (social proof)

**Primary Metric:** Landing page → App install / Signup click-through rate (14.72% baseline)
**Guardrail Metrics:**
- Signup completion rate (CTA may attract low-intent clicks)
- Cost per acquisition downstream (quality of traffic unchanged since organic)
- Bounce rate (ensure page still loads correctly)

**Audience:**
- Traffic split: 25% per variant (4-way test)
- Segment: All cenoa.com visitors (organic + paid)
- Exclusions: Returning users (cookie-based), bot traffic

**Duration & Sample Size:**
- MDE: 2.28pp (14.72% → 17%)
- Baseline: 14.72%
- Required sample per variant: ~3,500 visitors
- Total required: ~14,000 visitors
- Estimated duration: 1–2 weeks (depending on site traffic)

**Success Criteria:**
- p < 0.05 with Bonferroni correction (3 comparisons → p < 0.017 per variant)
- Minimum 7 days to capture day-of-week effects
- Winner must show ≥1.5pp absolute lift

**Amplitude Events to Track:**
| Event | Purpose |
|---|---|
| `landing_page_viewed` (with variant property) | Impression count |
| `cta_clicked` (with variant, position) | Primary metric |
| `app_store_redirect` | Downstream conversion |
| `signup_completed` (attributed to variant) | Quality guardrail |
| `page_scroll_depth` | Engagement secondary metric |

**Risk Assessment:**
| Risk | Severity | Mitigation |
|---|---|---|
| Clickbait CTA inflates clicks but lowers signup quality | Medium | Track full funnel through D7 activation |
| SEO impact from page changes | Low | CTA-only change, no structural/content changes |
| Sample pollution from returning visitors | Low | Cookie-based exclusion + first-visit filter in analysis |

---

### Test C: Onboarding Flow — Skip vs Mandatory KYC

**Hypothesis:**
"If we allow users to skip KYC during onboarding and explore the app first (with a persistent KYC prompt), then D7 activation rate will improve by 20% relative, while maintaining comparable D30 KYC completion rates."

**Variants:**
- **Control:** Current flow — KYC required before accessing main features
- **Variant:** KYC skippable — users can explore limited features (view rates, simulate transactions) with persistent "Complete KYC to unlock" nudges

**Primary Metric:** D7 activation rate (defined as: user completes at least 1 core action — deposit, trade, or send)
**Secondary Metric:** D30 KYC completion rate
**Guardrail Metrics:**
- Fraud rate (skip flow may attract bad actors exploring without verification)
- D30 retention (users who skip KYC may churn before completing it)
- Regulatory compliance (all transacting users MUST have KYC — enforce before any money movement)

**Audience:**
- Traffic split: 50% control / 50% variant
- Segment: New signups only
- Exclusions: Users from high-risk geos requiring upfront KYC (regulatory)

**Duration & Sample Size:**
- MDE: 20% relative lift on D7 activation
- Baseline D7 activation: estimate ~15% (needs validation from Amplitude)
- Required sample per variant: ~2,800 users
- Estimated duration: 4–5 weeks (need D30 readout)

**Success Criteria:**
- D7 activation: p < 0.05
- D30 KYC completion must be within 3pp of control (non-inferiority)
- Zero regulatory violations (hard guardrail — any transacting user without KYC = instant kill)

**Amplitude Events to Track:**
| Event | Purpose |
|---|---|
| `signup_completed` | Cohort entry |
| `kyc_prompt_shown` | Nudge frequency |
| `kyc_prompt_dismissed` / `kyc_prompt_accepted` | Skip behavior |
| `kyc_submitted` | KYC funnel |
| `first_deposit` / `first_trade` / `first_send` | Activation events |
| `app_opened` (daily) | Retention curve |
| `kyc_completed_day` (computed: days from signup to KYC) | KYC delay distribution |

**Risk Assessment:**
| Risk | Severity | Mitigation |
|---|---|---|
| Regulatory non-compliance | **Critical** | Hard block on ANY money movement without KYC; legal review before launch |
| Users never complete KYC (explore then churn) | High | Progressive nudge sequence (D1 soft, D3 stronger, D7 feature lock) |
| Fraud exploration without KYC | Medium | Rate-limit account creation; monitor suspicious patterns |
| Engineering complexity | Medium | Feature flags; phased rollout starting at 10% |

---

### Test D: Referral Incentive Amount

**Hypothesis:**
"If we increase the referral incentive from $5 to $10 per successful referral, then the referral conversion rate (invites sent → invitee signup) will improve by 40% relative, with a CAC still below our $25 target."

**Variants:**
- **Control:** $5 per successful referral (both referrer + invitee)
- **Variant 1:** $10 per successful referral (both sides)
- **Variant 2:** $20 per successful referral (both sides)

**Primary Metric:** Referral conversion rate (invited user completes signup + KYC / total invites sent)
**Secondary Metrics:**
- Invites sent per referrer
- Referral CAC (incentive cost / acquired user)
- Referred user D30 retention (quality check)

**Guardrail Metrics:**
- Fraud rate (fake accounts to claim referral bonus)
- Referral CAC must stay < $25
- LTV:CAC ratio of referred users ≥ 2:1

**Audience:**
- Traffic split: 33% per variant
- Segment: All active users with referral capability
- Exclusions: Users flagged for suspicious referral activity

**Duration & Sample Size:**
- MDE: 40% relative lift on referral conversion
- Baseline referral conversion: estimate ~8% (needs validation)
- Required sample per variant: ~1,500 referral invites
- Estimated duration: 3–4 weeks

**Success Criteria:**
- p < 0.05 with Bonferroni correction (p < 0.025 per comparison)
- Referral CAC must remain < $25 across all variants
- Minimum 14 days runtime
- Winner determined by highest conversion rate WHERE CAC < $25

**Amplitude Events to Track:**
| Event | Purpose |
|---|---|
| `referral_link_generated` | Intent to refer |
| `referral_invite_sent` (with channel: SMS/WhatsApp/link) | Invite volume |
| `referral_link_clicked` | Invitee interest |
| `referral_signup_completed` | Conversion step 1 |
| `referral_kyc_completed` | Conversion step 2 (triggers reward) |
| `referral_reward_claimed` | Payout tracking |
| `referral_fraud_flagged` | Guardrail |

**Risk Assessment:**
| Risk | Severity | Mitigation |
|---|---|---|
| Referral fraud (self-referrals, fake accounts) | **High** | Device fingerprinting; IP checks; delay reward payout 7 days |
| $20 variant blows up CAC | High | Daily CAC monitoring; auto-pause if CAC > $30 for 3 consecutive days |
| Low-quality referred users (only came for the bonus) | Medium | Track D30 retention + first transaction rate of referred cohort |
| Cannibalization of organic signups | Low | Compare total signup rate (not just referral) across periods |

---

### Test E: Push Notification Timing for KYC Completion

**Hypothesis:**
"If we send the KYC completion reminder push notification on D1 (24h after signup) instead of D3, then the KYC completion rate within 7 days will improve by 15% relative (from estimated 12% to 13.8%)."

**Variants:**
- **Control:** Current timing (D3 push notification)
- **Variant 1:** D1 push notification (24h after signup)
- **Variant 2:** D7 push notification (7 days after signup)
- **Variant 3:** Progressive sequence (D1 + D3 + D7, escalating urgency)

**Primary Metric:** KYC completion rate within 14 days of signup
**Secondary Metrics:**
- Push notification open rate per variant
- Time-to-KYC (median days from signup to KYC completion)
- Push opt-out rate

**Guardrail Metrics:**
- Push notification opt-out rate (must not increase >1pp)
- App uninstall rate within 7 days
- Overall notification engagement rate

**Audience:**
- Traffic split: 25% per variant (4-way)
- Segment: New signups who have NOT completed KYC and have push notifications enabled
- Exclusions: Users who completed KYC within first 4 hours (high-intent, don't need a nudge)

**Duration & Sample Size:**
- MDE: 1.8pp (12% → 13.8%)
- Baseline: 12% KYC completion within 14 days
- Required sample per variant: ~5,500 users
- Total: ~22,000 users
- Estimated duration: 5–6 weeks (need D14 readout for each cohort)

**Success Criteria:**
- p < 0.05 with Bonferroni correction (p < 0.017)
- Push opt-out rate must not increase >1pp vs control
- Minimum 21 days from first cohort entry (to capture D14 outcome)

**Amplitude Events to Track:**
| Event | Purpose |
|---|---|
| `push_notification_sent` (with variant, day_offset) | Delivery tracking |
| `push_notification_opened` (with variant) | Engagement |
| `push_notification_dismissed` | Non-engagement |
| `app_opened` (attributed to push) | Push-driven sessions |
| `kyc_flow_started` (within 1h of push open) | Push → KYC attribution |
| `kyc_submitted` | Primary outcome |
| `push_opt_out` | Guardrail |
| `app_uninstalled` | Guardrail |

**Risk Assessment:**
| Risk | Severity | Mitigation |
|---|---|---|
| D1 push feels spammy → opt-outs increase | Medium | Soft copy ("Ready when you are"); monitor opt-outs daily |
| Progressive sequence (Variant 3) causes notification fatigue | Medium | Cap at 3 total pushes; stop sequence once KYC started |
| D7 variant may miss the window entirely | Low | This is the hypothesis we're testing — acceptable risk |
| Platform differences (iOS vs Android push behavior) | Low | Segment analysis by platform in post-test |

---

## 3. Measurement Plan — Amplitude Event Taxonomy

### Required Amplitude Setup Per Test

| Requirement | Details |
|---|---|
| **User Property** | `experiment_variant_{test_id}` — assigned at bucketing time, immutable |
| **Event Property** | `experiment_id` on all relevant events during test |
| **Cohort** | Create Amplitude cohort per variant for retention/funnel analysis |
| **Dashboard** | Dedicated Amplitude dashboard per active test |

### Cross-Test Event Matrix

| Event | Test A | Test B | Test C | Test D | Test E |
|---|---|---|---|---|---|
| `signup_completed` | | ✓ | ✓ | ✓ | ✓ |
| `kyc_flow_started` | ✓ | | ✓ | | ✓ |
| `kyc_submitted` | ✓ | | ✓ | ✓ | ✓ |
| `kyc_approved` | ✓ | | ✓ | ✓ | |
| `landing_page_viewed` | | ✓ | | | |
| `cta_clicked` | | ✓ | | | |
| `first_deposit` | | | ✓ | | |
| `referral_invite_sent` | | | | ✓ | |
| `referral_signup_completed` | | | | ✓ | |
| `push_notification_sent` | | | | | ✓ |
| `push_notification_opened` | | | | | ✓ |
| `app_opened` | | | ✓ | | ✓ |

### Amplitude Configuration Checklist

- [ ] Create `experiment_variant` user property (string)
- [ ] Set up Feature Flag integration (Amplitude Experiment or custom)
- [ ] Build per-test funnel charts
- [ ] Configure retention analysis cohorts per variant
- [ ] Set up real-time guardrail metric alerts (Amplitude → Slack)
- [ ] Ensure event taxonomy is documented in Amplitude Data

---

## 4. Consolidated Risk Matrix

| Test | Highest Risk | Show-Stopper? | Pre-Launch Requirement |
|---|---|---|---|
| A — KYC Simplification | Compliance concern | ⚠️ Maybe | Compliance team sign-off |
| B — CTA Copy | Low risk overall | No | QA on all variants |
| C — Skip KYC | Regulatory non-compliance | 🛑 Yes | Legal review + hard transaction block |
| D — Referral Amount | Referral fraud | ⚠️ Maybe | Fraud detection rules in place |
| E — Push Timing | Notification fatigue | No | Opt-out monitoring dashboard |

### Recommended Launch Order

1. **Test B** (CTA Copy) — Lowest risk, fastest to implement, no backend changes
2. **Test E** (Push Timing) — Low risk, configuration change only
3. **Test A** (KYC Simplification) — Medium risk, needs compliance review
4. **Test D** (Referral Amount) — Needs fraud safeguards first
5. **Test C** (Skip KYC) — Highest risk, requires legal + engineering investment

### General Safeguards

- **No overlapping tests** on the same user journey (e.g., don't run Test A and Test C simultaneously)
- **Minimum 48h canary** at 5% traffic before scaling to full split
- **Daily check-ins** on guardrail metrics for first 5 days of each test
- **Kill switch** accessible to product + growth team (not just engineering)
- **Post-test report** due within 5 business days of test conclusion

---

*Last updated: 2026-03-21*
*Owner: Growth / Performance Marketing*
