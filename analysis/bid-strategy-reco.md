# Google Ads Bid Strategy Recommendations

**Sprint:** 068  
**Created:** 2026-03-21  
**Sources:** google-ads-deepdive.md, demand-gen-fix-plan.md, budget-efficiency.md, channel-cac.md  
**Status:** 📋 Ready for implementation

---

## 1. Current Campaign Types & Likely Bid Strategies

| Campaign | Type | Market | Est. Weekly Spend | Current Bid Strategy (likely) | CPI |
|---|---|---|---:|---|---:|
| Pmax TR E-ihracat KYC_Start | Performance Max | TR | ~$806 | Maximize Conversions | ~$30 |
| Search TR Pure Brand | Search | TR | ~$790 | Maximize Conversions or Enhanced CPC | ~$29 |
| Search TR Freelancer Platform | Search | TR | incl. above | Maximize Conversions or Enhanced CPC | — |
| TR-Discovery-24.10.2025 | Demand Gen (Retargeting) | TR | ~$560 | Maximize Clicks or Maximize Conversions (web) | ∞ (0 installs) |
| Google App Android | App Install (UAC) | TR | ~$1,400 | Target CPA (auto) | ~$31 |
| EG Generic (egypt_en_architect) | Search | EG | ~$500-700 | Maximize Conversions | ~$9 |
| TR Rakipler Payoneer | Search (Competitor) | TR | ~$200-300 | Maximize Conversions or Manual CPC | ~$27 USD |
| NG Google iOS CVR | Search/CVR | NG | minimal | Target CPA or Maximize Conversions | ~$27 |

**Note:** Exact bid strategies need confirmation in Google Ads console — these are inferred from campaign types and performance patterns.

---

## 2. Per Campaign Type Recommendations

### 2a. Performance Max (TR E-ihracat KYC_Start)

| Setting | Recommendation |
|---|---|
| **Bid Strategy** | **Keep: Maximize Conversions** |
| **Rationale** | Pmax is already the best-performing campaign on Cost/New Active ($19.18). Algorithm-driven bidding across all Google surfaces is working. |
| **Do NOT switch to tCPA yet** | Pmax needs volume headroom to auto-optimize. tCPA constrains the algorithm and can reduce reach. |
| **When to consider tCPA** | Only if CPA drifts above $35/install consistently for 2+ weeks |
| **Budget** | Scale to **$1,200/wk** (+50%) — Pmax auto-adjusts bids to budget |

### 2b. Search Brand (TR Pure Brand)

| Setting | Recommendation |
|---|---|
| **Bid Strategy** | **Switch to tCPA at ₺500 (~$14)** |
| **Rationale** | Brand search is high-intent, predictable volume. tCPA prevents overpaying for branded clicks while maintaining impression share. |
| **Current CPI** | ~₺1,015 (~$29) — tCPA at ₺500 is aggressive but achievable for brand terms |
| **Fallback** | If impression share drops below 90%, raise tCPA to ₺700 |
| **Conversion action** | Must be set to **app_install** (Firebase/AppsFlyer), NOT web visits |
| **Budget** | Scale to **$1,030/wk** (+30%) — protect brand from competitor bidding |

### 2c. Search Generic (TR Freelancer + EG)

| Campaign | Bid Strategy | tCPA Target | Rationale |
|---|---|---:|---|
| **EG Generic** | **tCPA** | **₺350 (~$10)** | Current CPI ~₺325 (~$9). Set tCPA slightly above to maintain volume while capping waste. EG has low competition = cheaper clicks. |
| **TR Freelancer** | **tCPA** | **₺200 (~$6)** | Freelancer vertical is niche with strong intent. Lower CPA target pushes algorithm to find best converters. |
| **TR Generic (if any)** | **tCPA** | **₺400 (~$11)** | Generic TR keywords are competitive; tCPA prevents runaway costs |

**EG scaling note:** Do NOT scale EG until KYC is fixed (Bridgexyz blocker — currently 0 KYC submits outside TR). Fix funnel first, then scale budget.

### 2d. Demand Gen (TR-Discovery-24.10.2025)

| Setting | Recommendation |
|---|---|
| **Bid Strategy** | **🔴 PAUSE IMMEDIATELY** |
| **Rationale** | 1,627 clicks, **0 installs** over 5 months. Estimated waste: ₺100K–200K+ (~$2,800–$5,600 total). |
| **Current spend** | ~₺19,620/week (~$560/wk) |
| **Action** | Pause → diagnose (see demand-gen-fix-plan.md) → kill or relaunch with fixed conversion actions |
| **If relaunched** | Must use Firebase app_install as primary conversion, narrow audience to 30-day high-intent visitors, exclude existing installers, budget cap at ₺5,000/wk, kill if CPI > ₺500 after 2 weeks |

### 2e. Competitor Campaigns (TR Rakipler Payoneer)

| Setting | Recommendation |
|---|---|
| **Bid Strategy** | **Manual CPC with cap, or tCPA at ₺600 (~$17)** |
| **Rationale** | CPI of ₺938–1,047 is 30–35× Pmax CPI. Volume is <1 install/week. Not scalable. |
| **Option A (preferred)** | **Manual CPC** with max CPC bid of ₺15-20. This prevents overpaying for competitor terms while maintaining keyword coverage. |
| **Option B** | **tCPA at ₺600** — aggressive target forces algorithm to only bid when conversion probability is high |
| **Budget** | **Reduce to ₺500/month** monitoring budget. Add negative keywords: "Payoneer login", "Payoneer customer service", "Payoneer support" |
| **Kill trigger** | If 0 installs after 30 days at monitoring budget → kill permanently, reallocate to Pmax |

### 2f. Google App Android (UAC)

| Setting | Recommendation |
|---|---|
| **Bid Strategy** | **tCPA at ₺1,050 (~$30)** |
| **Rationale** | Currently the largest Google spend line at ~$1,400/wk with ~$31 CPA. Setting tCPA at current level locks in performance while preventing drift. |
| **Optimize** | Investigate why App campaign CPA ($31) is 63% higher than Pmax ($19). Check for audience overlap / self-cannibalization. |
| **Budget** | Hold at **$1,400/wk** — optimize before scaling |

---

## 3. When to Use Each Bid Strategy

### tCPA (Target Cost Per Acquisition)

**Use when:**
- Campaign has a clear, measurable conversion event (app install, KYC start)
- Campaign generates **30+ conversions/month** (minimum for smart bidding learning)
- You know your target CPA and want to constrain spend
- Campaign is mature (2+ months of data)

**Best for:** Search Brand, Search Generic, Google App (UAC), mature competitor campaigns

**Pitfall:** Setting tCPA too low kills volume. Start at current CPA level, then reduce by 10–15% every 2 weeks.

### Maximize Conversions (no target)

**Use when:**
- Campaign is new or scaling up (need volume signal first)
- You trust the algorithm to find the right CPA
- Campaign has headroom to spend more (not budget-constrained)
- Pmax campaigns (algorithm needs freedom across surfaces)

**Best for:** Pmax, new campaign launches, campaigns in learning phase

**Pitfall:** Can overspend if budget is set too high. Always pair with a daily/weekly budget cap.

### Manual CPC

**Use when:**
- Campaign volume is too low for smart bidding (<30 conversions/month)
- You need tight cost control per click
- Competitor targeting where you want presence but not aggressive spending
- Testing new keywords before enabling smart bidding

**Best for:** Competitor campaigns, low-volume exploratory campaigns, new market tests (NG)

**Pitfall:** Requires ongoing manual management. Doesn't auto-optimize to conversions.

### Decision Matrix

| Monthly Conversions | Budget Flexibility | Recommended Strategy |
|---|---|---|
| 30+ | High | Maximize Conversions |
| 30+ | Constrained | tCPA |
| 10–30 | Any | tCPA (loose target) or Maximize Conversions with budget cap |
| <10 | Any | Manual CPC or Enhanced CPC |
| 0 | Any | **PAUSE** |

---

## 4. Conversion Action Audit

### Critical: Which Conversion Action Should Each Campaign Optimize For?

| Campaign Type | Primary Conversion Action | Why | Secondary (observation only) |
|---|---|---|---|
| **Pmax** | `first_open` (Firebase) or `af_app_install` (AppsFlyer) | Pmax needs high-volume signal. Install is the most frequent event → best for algorithm learning. | KYC_start, virtual_account_created |
| **Search Brand** | `af_app_install` (AppsFlyer) | Brand searchers are high-intent — optimize for the install, downstream will follow naturally. | KYC_start |
| **Search Generic** | `KYC_start` (if volume allows) or `af_app_install` | Generic users need stronger conversion signal. If KYC_start has 30+/month, use it. Otherwise fall back to install. | virtual_account_created |
| **Google App (UAC)** | `af_app_install` | UAC is built for install optimization. Don't fight it. | first_open, KYC_start |
| **Competitor** | `af_app_install` | Too few conversions for deeper events. Install is the only realistic target at current volumes. | — |
| **Demand Gen (if relaunched)** | `af_app_install` with deep link | **MUST** switch from current (likely web visit) to app install. This is probably why 0 installs are attributed. | — |

### Red Flags to Check in Google Ads Console

1. **Are campaigns optimizing for web conversions instead of app installs?** This is the most likely reason Demand Gen shows 0 installs — it's optimizing for landing page visits.
2. **Is the same conversion action used across all campaigns?** Inconsistent conversion actions cause Google's algorithm to optimize for different things per campaign.
3. **Are "All conversions" vs "Conversions" showing different numbers?** If "All conversions" >> "Conversions", there are conversion actions being tracked but not used for bidding — these might be the ones you actually care about.
4. **Is Firebase linked properly?** Ensure Firebase app events are imported as conversion actions in Google Ads and set as primary for relevant campaigns.

### Conversion Action Setup Checklist

- [ ] Verify `af_app_install` is imported as a conversion action in Google Ads
- [ ] Set `af_app_install` as **primary** conversion for all app-install campaigns
- [ ] Add `KYC_start` and `virtual_account_created` as **secondary** (observe, don't optimize)
- [ ] Remove any web-based conversion actions (page visits, form fills) from app campaigns
- [ ] Confirm Demand Gen campaign is NOT using a web conversion as primary goal
- [ ] Check that conversion counting is set to "One" (not "Every") for install events

---

## 5. Budget Cap Recommendations Per Campaign

### Weekly Budget Caps

| Campaign | Current Spend/wk | Recommended Cap/wk | Change | Rationale |
|---|---|---:|---|---|
| **Pmax TR** | ~$806 | **$1,200** | +49% | Best Cost/Active ($19.18). Scale lever #1. |
| **Search Brand TR** | ~$790 | **$1,030** | +30% | Protect brand + high downstream quality. |
| **Search Freelancer TR** | incl. above | **$300** (separate) | New | Break out for independent tCPA control. |
| **Google App Android** | ~$1,400 | **$1,400** (hold) | 0% | Optimize CPA before scaling. Fix overlap with Pmax first. |
| **EG Generic** | ~$500-700 | **$700** (hold) | 0% | Hold until KYC fix. Then scale to $1,200/wk. |
| **Demand Gen** | ~$560 | **$0** (paused) | -100% | Zero installs. Pause immediately. |
| **TR Rakipler Payoneer** | ~$200-300 | **$125** (~₺500/mo) | -60% | Monitoring budget only. |
| **NG Google iOS** | minimal | **$300** | New target | Cheap market test. Validate LTV. |

### Monthly Budget Summary

| Campaign | Monthly Cap |
|---|---:|
| Pmax TR | $5,200 |
| Search Brand TR | $4,460 |
| Search Freelancer TR | $1,300 |
| Google App Android | $6,060 |
| EG Generic | $3,030 (post KYC fix: $5,200) |
| Demand Gen | $0 |
| Competitor (Rakipler) | $540 |
| NG Google iOS | $1,300 |
| **Total Google** | **$21,890/mo** |

### Budget Guardrails

- **Daily cap = Weekly cap / 7** (prevents Google from front-loading spend)
- **If any campaign spends >120% of weekly cap**, reduce daily budget immediately
- **If CPA exceeds 1.5× target for 3 consecutive days**, pause and investigate before resuming
- **Monthly review:** Reallocate from underperformers to top 2 campaigns (Pmax + Search Brand)

---

## 6. Learning Period Considerations

### Smart Bidding Minimum Thresholds

| Bid Strategy | Min Conversions/Month | Min Conversions/Week | Why |
|---|---:|---:|---|
| Maximize Conversions | 15 | ~4 | Algorithm needs signal but no target to chase |
| tCPA | **30** | ~8 | Algorithm must learn CPA distribution to hit target |
| tROAS | **50** | ~13 | Revenue prediction needs more data points |
| Manual CPC | 0 | 0 | No algorithmic learning needed |

### Current Campaign Conversion Volume Assessment

| Campaign | Est. Monthly Conversions | Smart Bidding Eligible? | Recommendation |
|---|---:|---|---|
| **Pmax TR** | ~108 (27/wk × 4) | ✅ Yes | Maximize Conversions ✓ |
| **Search Brand TR** | ~108 (27/wk × 4) | ✅ Yes | tCPA eligible ✓ |
| **Google App Android** | ~180 (45/wk × 4) | ✅ Yes | tCPA eligible ✓ |
| **EG Generic** | ~60-80 | ✅ Yes | tCPA eligible ✓ |
| **Search Freelancer TR** | unknown (newly broken out) | ⚠️ Maybe | Start with Maximize Conversions, switch to tCPA after 30 conversions |
| **Competitor Payoneer** | ~2-4 | ❌ No | **Manual CPC only** |
| **NG Google iOS** | ~20-40 | ⚠️ Borderline | Enhanced CPC or Maximize Conversions |
| **Demand Gen** | 0 | ❌ No | Paused |

### Learning Period Rules

1. **Don't change bid strategy during learning** (first 7–14 days after any change). Google shows "Learning" status — let it complete.
2. **Don't change budgets by more than 20% at once** — large changes reset the learning period.
3. **Don't change conversion actions mid-flight** — this resets everything. Plan conversion action changes alongside bid strategy changes.
4. **Minimum 2-week evaluation window** after any bid strategy change before judging performance.
5. **Expect CPA volatility during learning** — CPA can spike 30–50% during the first week. This is normal. Don't panic-pause.

### Migration Sequence (to minimize disruption)

| Week | Action | Campaigns Affected |
|---|---|---|
| **Week 1** | Pause Demand Gen. Reduce Competitor to monitoring budget. | Demand Gen, Rakipler |
| **Week 1** | Audit conversion actions across all campaigns (Section 4 checklist) | All |
| **Week 2** | Switch Search Brand to tCPA ₺500. Search Freelancer to tCPA ₺200. | Search campaigns |
| **Week 2** | Increase Pmax budget to $1,200/wk (Maximize Conversions unchanged). | Pmax |
| **Week 3** | Switch EG Generic to tCPA ₺350. | EG Generic |
| **Week 3** | Switch Google App Android to tCPA ₺1,050. | UAC |
| **Week 4** | Evaluate all changes. Adjust tCPA targets based on 2-week data. | All |
| **Week 5–6** | Second round of tCPA adjustments (reduce by 10–15% if volume holds). | Search, UAC |

### Conversion Action Change Timing

- **Week 1** (with pauses): Audit and fix conversion actions BEFORE changing bid strategies
- Changing conversion actions resets learning → do it at the same time as bid strategy changes (Week 2)
- Never change conversion action and bid strategy on different weeks for the same campaign

---

## Summary: Quick-Reference Table

| Campaign | Bid Strategy | tCPA Target | Conv. Action | Weekly Budget | Action |
|---|---|---:|---|---:|---|
| Pmax TR | Maximize Conversions | — | af_app_install | $1,200 | Scale +50% |
| Search Brand TR | tCPA | ₺500 | af_app_install | $1,030 | Switch strategy + scale |
| Search Freelancer TR | tCPA | ₺200 | af_app_install | $300 | Break out + set tCPA |
| Google App Android | tCPA | ₺1,050 | af_app_install | $1,400 | Switch to tCPA, hold budget |
| EG Generic | tCPA | ₺350 | af_app_install | $700 → $1,200 | tCPA now, scale after KYC fix |
| Demand Gen | **PAUSED** | — | — | $0 | Pause immediately |
| Competitor (Rakipler) | Manual CPC (₺15-20 max) | — | af_app_install | $125 | Cut to monitoring |
| NG Google iOS | Maximize Conversions | — | af_app_install | $300 | Test budget |

---

*Sprint 068 | Bid Strategy Recommendations | 2026-03-21*
