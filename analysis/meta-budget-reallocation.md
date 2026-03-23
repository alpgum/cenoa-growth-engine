# Meta Ads Budget Reallocation Plan

**Date:** 2026-03-21  
**Sprint:** 058  
**Status:** Actionable — ready for execution  
**Dependencies:** [045] Meta Ads Analysis, [029] Budget Efficiency, Channel CAC Scorecard

---

## 1. Current Meta Spend Allocation

### Monthly spend (Turkey, from Trafik Canavarı)

| Period | Meta Spend/mo | % of Total Perf | Trend |
|---|---:|---:|---|
| May 2025 | $18,886 | 73.7% | Peak |
| Jun 2025 | $7,660 | 23.5% | Sharp cut |
| Sep 2025 | $5,700 | 22.5% | Stable |
| Dec 2025 | $4,497 | 26.6% | Declining |
| Mar 2026 (proxy) | ~$11,016 | ~40% | Rebounded |

### Weekly breakdown by campaign type (Mar 14–20 proxy)

| Campaign / Bucket | Spend/wk (est.) | Installs | Sign-ups | Withdrawals | Cost/Active |
|---|---:|---:|---:|---:|---:|
| TR_Meta_web2app (CVR+broad) | ~$1,400 | 61 | 10 | 4 | ~$350 |
| TR_Meta_web2app_RTGT | ~$600 | 17 | 6 | 9 | ~$67 |
| EG_Meta_web2app (CVR+ALL) | ~$500 | 64 | 7 | 0 | ∞ (new) |
| Other Meta fragments | ~$254 | 41 | 9 | 9 | ~$28 |
| **Total Meta** | **$2,754/wk** | **122** | **22** | **22** | **$82/active** |

**Monthly run-rate:** ~$11,016/mo across all Meta campaigns.

---

## 2. What to Pause — and Why

### Immediate pause candidates

| Campaign | Weekly Spend (est.) | Monthly Freed | Reason |
|---|---:|---:|---|
| **TR_Meta_web2app (non-RTGT)** | ~$1,400 | **~$5,600** | $350/active — 18× worse than Pmax ($19). Low sign-up rate (16.4%). Structural W2A friction makes this unscalable. |
| **EG_Meta_web2app (both)** | ~$500 | **~$2,000** | Launched Mar 18-20. 64 installs, 0 withdrawals after 3 days. Give 10 more days; if 0 withdrawals by Apr 3 → pause. |

### Keep running

| Campaign | Weekly Spend (est.) | Reason |
|---|---:|---|
| **TR_Meta_web2app_RTGT** | ~$600 | Only Meta campaign with proven downstream (9 withdrawals/wk). ~$67/active is still expensive but retargeting has structural advantages — warm audience, higher intent. |
| **Other Meta fragments** | ~$254 | Includes legacy campaign 1764668627 generating 76 withdrawals/wk from historical cohorts. Don't touch. |

### Summary of freed budget

| Action | Timing | Budget Freed/mo |
|---|---|---:|
| Pause TR non-RTGT prospecting | Week 1 (immediate) | **$5,600** |
| Pause EG campaigns (if still 0 withdrawals) | Week 2 (Apr 3) | **$2,000** |
| **Total freed** | By end of Week 2 | **$7,600/mo** |

**Remaining Meta budget:** ~$3,400/mo (RTGT $2,400 + legacy/fragments $1,000)

---

## 3. Where to Reallocate — Expected Impact

Reallocation targets chosen by **Cost/New Active** ranking:

| Channel | Current Spend/mo | Add | New Spend/mo | Current Cost/Active | Expected New Actives from Added Budget |
|---|---:|---:|---:|---:|---:|
| **Google Pmax** | $3,222 | **+$3,600** | $6,822 | $19.18 | ~188 |
| **Apple Search Ads** | $2,402 | **+$2,400** | $4,802 | $22.66 | ~106 |
| **Google Search** | $3,160 | **+$1,600** | $4,760 | $25.48 | ~63 |
| **Total reallocated** | | **$7,600** | | | **~357 new actives** |

### Comparison: What that same $7,600 was producing on Meta

- Meta $7,600/mo → ~92 new actives (at $82.21/active)
- Reallocated $7,600/mo → **~357 new actives** (blended ~$21.28/active)
- **Net gain: ~265 additional active users/month (+288%)**

### Channel-specific rationale

**Google Pmax (+$3,600/mo) — Primary scale lever**
- Best cost/active at $19.18 — 4.3× more efficient than Meta
- ML-optimized across Search, Display, YouTube, Discover
- Already proven with 42 new actives/wk on only $805/wk
- Risk: diminishing returns at scale; monitor CPA weekly

**Apple Search Ads (+$2,400/mo) — Intent anchor**
- $22.66/active with strongest downstream signal (254 withdrawals/wk)
- High-intent users actively searching App Store
- Currently underspent at $600/wk — significant headroom
- Expand: brand exact → competitor → generic keywords

**Google Search (+$1,600/mo) — Quality floor**
- $25.48/active, reliable quality
- Captures high-intent "send money" / "Cenoa" queries
- Moderate headroom; don't over-scale (impression share already decent)

---

## 4. Phased Execution Plan

### Week 1: Pause (Mar 24–28)

| Day | Action | Owner |
|---|---|---|
| Mon Mar 24 | Pause TR_Meta_web2app non-RTGT campaigns in Meta Ads Manager | Furkan |
| Mon Mar 24 | Screenshot current Meta campaign states + last 7-day metrics for baseline | Furkan |
| Mon Mar 24 | Set up daily spend alerts on remaining Meta campaigns (RTGT + legacy) | Furkan |
| Tue Mar 25 | Confirm paused campaigns show $0 spend in Meta dashboard | Alp/Furkan |
| Fri Mar 28 | Week 1 checkpoint: Meta daily spend should be ~$120/day (down from ~$390) | Alp |

**Budget freed Week 1:** ~$1,400/wk → $5,600/mo

### Week 2: Reallocate (Mar 31 – Apr 4)

| Day | Action | Owner |
|---|---|---|
| Mon Mar 31 | Increase Google Pmax daily budget by ~$120/day ($900/wk added) | Alp |
| Mon Mar 31 | Increase ASA campaign budgets by ~$80/day ($600/wk added) | Alp |
| Tue Apr 1 | Increase Google Search budgets by ~$55/day ($400/wk added) | Alp |
| Thu Apr 3 | Evaluate EG Meta campaigns — if 0 withdrawals in 14 days → pause | Furkan |
| Fri Apr 4 | Verify all channels spending at new target levels | Alp |

**If EG paused:** additional ~$500/wk freed → add to Pmax ($300) + ASA ($200)

### Week 3: Measure (Apr 7–11)

| Day | Action | Owner |
|---|---|---|
| Mon Apr 7 | Pull 7-day post-reallocation metrics for all channels | Alp/Lucas |
| Mon Apr 7 | Compare: new actives/wk, cost/active, install volume | Lucas |
| Wed Apr 9 | Check Meta RTGT performance — still delivering 9+ withdrawals/wk? | Furkan |
| Fri Apr 11 | Go/No-Go decision: continue reallocation or revert (see guardrails below) | Alp |

---

## 5. Expected Outcome (4-week projection)

| Metric | Before (current) | After (projected) | Delta |
|---|---:|---:|---|
| Total paid spend/mo | ~$11,016 | ~$11,016 | $0 (budget-neutral) |
| Meta spend/mo | ~$11,016 | ~$3,400 | -$7,600 (-69%) |
| Google (Pmax+Search) spend/mo | ~$6,382 | ~$11,582 | +$5,200 |
| ASA spend/mo | ~$2,402 | ~$4,802 | +$2,400 |
| New actives/mo (Meta portion) | ~136 | ~41 (RTGT+legacy) | -95 |
| New actives/mo (Google+ASA portion) | ~396 | ~753 | +357 |
| **Net new actives/mo** | **~532** | **~794** | **+262 (+49%)** |
| **Blended cost/active** | **~$20.70** | **~$13.87** | **-33%** |

---

## 6. Guardrails — What to Watch, When to Revert

### Red flags (trigger immediate review)

| Signal | Threshold | Action |
|---|---|---|
| Google Pmax CPA doubles | Cost/active > $38 for 5 consecutive days | Cap Pmax budget at pre-increase level |
| ASA CPA spikes | Cost/active > $45 for 5 consecutive days | Reduce ASA back to $600/wk |
| Total new actives drop | < 100/wk (vs current ~133/wk) | Partial Meta reactivation |
| RTGT performance degrades | < 5 withdrawals/wk for 2 consecutive weeks | Investigate creative fatigue; refresh creatives |
| Install quality drops (any channel) | Install→Signup rate < 10% | Pause offending campaign |

### Yellow flags (monitor closely)

| Signal | Threshold | Action |
|---|---|---|
| Google Search impression share drops | < 50% on brand terms | Increase Search budget from Pmax allocation |
| ASA hits budget cap daily | 100% budget utilization for 3+ days | Raise budget incrementally (+20%) |
| Organic installs decline | < 500/wk (vs current 632) | Check if Meta awareness driving organic; consider re-enabling prospecting |

### Revert protocol

If **total new actives/week drops below 100** for 2 consecutive weeks post-reallocation:

1. Re-enable TR_Meta_web2app at 50% of previous budget ($700/wk)
2. Reduce Pmax increase by $700/wk
3. Run for 2 more weeks to compare
4. If Meta still underperforms → permanent cut; if actives recover → Meta has brand-awareness lift effect

### Attribution dependency

> ⚠️ The $82/active Meta figure may be inflated due to attribution leakage (60%+ unattributed downstream). If/when AppsFlyer W2A attribution is fixed and Meta's true cost/active drops below $40, reconsider scaling Meta back up.

---

## 7. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Pmax diminishing returns at scale** | Medium | Wasted budget, rising CPA | Daily CPA monitoring; cap at 2× current if CPA doubles |
| **ASA keyword saturation** | Low-Medium | Can't spend incremental budget | Expand to competitor + generic keywords; test new ad groups |
| **Meta brand awareness halo effect** | Medium | Organic installs decline when Meta paused | Monitor organic closely; Week 3 checkpoint |
| **Attribution improves → Meta was actually good** | Low-Medium | Missed opportunity | Keep RTGT running as signal; re-evaluate after attribution fix |
| **Team execution lag** | Low | Slow to implement changes | Clear owner + date for each action item |

---

## Summary

**The play:** Cut $7,600/mo from underperforming Meta prospecting campaigns, keep $3,400/mo in proven Meta retargeting + legacy, and reallocate to Google Pmax ($3,600), ASA ($2,400), and Google Search ($1,600).

**Expected result:** +262 new active users/month (+49%) at 33% lower blended cost/active — all budget-neutral.

**Key caveat:** Meta's attribution is broken. If fixing AppsFlyer W2A tracking reveals Meta's true cost/active is <$40, revisit this plan. Until then, the data says reallocate.

---

*Generated: 2026-03-21 | Sprint 058*


---

> ⚠️ **Attribution caveat:** Web campaigns (Meta/Google → cenoa.com → app store) may appear as "Organic" or "(none)" due to broken web→app attribution. Estimated correction factor: ~6.9×. See [attribution-reconciliation.md](attribution-reconciliation.md) for details.
