# Sprint 1 Independent Audit — Performance Marketing

**Auditor:** Independent review (automated)  
**Date:** 2026-03-22  
**Scope:** All 70+ analysis documents, 26 scripts, 40+ data files, and Cortex dashboard  
**Method:** Full cross-document read, number reconciliation, logic consistency check, script code review

---

## Overall Grade: B-

**Justification:** Sprint 1 produced an impressive volume of work — 70+ analysis documents, 26 scripts, and a functioning automation pipeline — in what appears to be a single-day sprint. The core strategic insight (KYC is the binding constraint, not acquisition) is correct and well-supported. Attribution gap discovery and the ~6.9× correction factor are valuable. However, the sprint suffers from **significant internal number inconsistencies** across documents, **metric definition confusion** that makes it unclear which "CAC" or "active" is being discussed at any given time, **19 analysis docs missing the attribution caveat** despite it being the most important finding, and **4 scripts with hardcoded API credentials** committed to the repo. The work is directionally sound but not yet decision-grade.

---

## Top 10 Issues Found (Ranked by Severity)

### 1. 🔴 CRITICAL: Hardcoded API Credentials in 4 Scripts
**Severity: Critical (Security)**

Four scripts have Amplitude API keys and secret keys hardcoded in plaintext:
- `scripts/attribution_funnel.py` (lines 9-10)
- `scripts/country_breakdown.py` (lines 8-9)
- `scripts/feature_engagement.py` (lines 8-9)
- `scripts/platform_funnel.py` (lines 9-10)

API Key: `1adec44d0d2d73321b08f4de26441ebd`  
Secret Key: `3a48a09cb7b7ef5ec8379b0a83e24696`

Meanwhile, other scripts (`amplitude_weekly_pull.py`, `kpi_auto_update.py`, etc.) correctly load credentials from `~/.openclaw/credentials/amplitude.env`. This inconsistency suggests the hardcoded scripts were written quickly without following the established pattern. **These credentials are in a git repo.**

**Fix:** Immediately rotate the Amplitude API key, refactor all 4 scripts to use `load_credentials()`, add a `.gitignore` rule or pre-commit hook.

---

### 2. 🔴 CRITICAL: Wildly Inconsistent "Active User" / CAC Numbers Across Documents

The same metric ("new actives" or "cost per active") shows dramatically different values depending on which document you read:

| Document | Metric | Value | Denominator Definition |
|---|---|---|---|
| `blended-cac.md` | TR $/Active (Feb 2026) | **$208** | "new_active" from Sheets Sum |
| `country-cac.md` | TR Cost/Paid Active (Mar 9-15) | **$864** | "paid_active" from Sheets CAC Analysis |
| `channel-cac.md` | Meta Cost/New Active | **$82.21** | "New Active" from Sheets weekly |
| `meta-budget-reallocation.md` | Blended cost/active (all channels) | **$20.70** | Sum of New Active across all channels |
| `turkey-90d-plan.md` | Baseline blended CAC/new active (TR) | **$20-$21** | References meta-budget-reallocation |
| `budget-allocation-model.md` | TR $/Paid Active (Feb) | **$208** | Consistent with blended-cac |
| `budget-allocation-model.md` | Scenario A blended $/active | **$129-$150** | Forward projection |
| `marginal-cac.md` | Feb 2026 $/Active | **$208** | Matches blended-cac |

The **$20.70 vs $208 vs $864** spread for what sounds like "cost per active user in Turkey" is a 42× range. This stems from different denominator definitions (new_active vs paid_active vs total_active), different time periods, and different spend numerators. But the documents do not consistently flag which definition they're using.

**Impact:** A reader going from `turkey-90d-plan.md` (baseline "$20-21") to `budget-allocation-model.md` (baseline "$208") would reasonably conclude the analyses are contradictory. The meta-budget-reallocation doc's "$20.70 blended" appears to use Sheets "New Active" which includes organic, making it misleading as a "cost per active" for paid channels.

**Fix:** Create a single definitions document. Every CAC claim must specify: (1) numerator source, (2) denominator event name, (3) paid-only vs blended, (4) time period.

---

### 3. 🟠 HIGH: 19 Analysis Documents Missing Attribution Caveat

The sprint's most important finding is that web→app attribution is broken (~6.9× correction factor, 82% of signups unattributed). Yet **19 of ~70 analysis documents** make no mention of attribution issues, unattributed data, or the "(none)" bucket:

- `bid-strategy-reco.md` — Makes channel bid strategy recommendations without noting attribution uncertainty
- `country-cac.md` — Computes country CAC without noting that channel-level attribution is broken (though it does note KYC gating)
- `ltv-cac-ratio.md` — Computes LTV/CAC ratios without noting that CAC numbers may be off by 6.9×
- `ltv-model.md` — No mention that LTV model inputs may be distorted by attribution
- `egypt-scaling-plan.md` — Recommends scaling budgets without attribution caveat
- `nigeria-growth-plan.md` — Same issue
- `creative-scoring.md`, `competitive-positioning.md`, `seasonal-trends.md`, `retention.md`, `ios-android-ux-gap.md`, `ga4-web-traffic.md`, `global-funnel.md`, `country-breakdown.md`, `bq-campaign-trends-30d.md`, `feature-engagement.md`, `pakistan-prelaunch-plan.md`, `pre-kyc-survey-investigation.md`, `automation-setup.md`

**Impact:** Someone reading `ltv-cac-ratio.md` sees TR LTV/CAC = 0.08× (terrible) but doesn't see the caveat that CAC may be overstated because attribution is broken. Similarly, `bid-strategy-reco.md` makes optimization recommendations based on potentially miscredited conversions.

**Fix:** Add a standard attribution caveat header to all channel/CAC/ROI analysis documents. Consider a template.

---

### 4. 🟠 HIGH: Budget Math Inconsistencies Across Documents

| Check | budget-allocation-model | meta-budget-reallocation | turkey-90d-plan | Consistent? |
|---|---|---|---|---|
| Total budget | $50K/mo | Implies ~$27.5K/mo TR total (doesn't address full $50K) | ~$5K-$7K/wk TR (~$21K-$30K/mo) | ❌ Partial overlap |
| TR allocation (Scenario B) | $28K/mo | N/A (focuses on Meta realloc) | $4,980-$7,000/wk ($21.6K-$30.3K/mo) | ⚠️ Close but not aligned |
| Meta freed budget | $4,400-$7,000/mo | $7,600/mo | Keep RTGT at $600/wk ($2.6K/mo) | ❌ Different numbers |
| Pmax target | $8.4K-$12K/mo | +$3,600/mo on current $3.2K = $6.8K | $1,200-$1,700/wk ($5.2-$7.4K/mo) | ⚠️ Different ranges |

The three documents that recommend budget changes propose **different specific numbers** for the same channels. A reader/operator following `meta-budget-reallocation.md` would set different budgets than one following `budget-allocation-model.md` or `turkey-90d-plan.md`.

**Fix:** Designate ONE document as the canonical budget plan. Others should reference it, not propose their own allocations.

---

### 5. 🟠 HIGH: meta-budget-reallocation Claims 532 Baseline Actives/mo vs 300-350 in budget-allocation-model

`meta-budget-reallocation.md` Section 5 projects:
- **Current baseline: ~532 net new actives/mo** at $20.70 blended cost/active
- **After reallocation: ~794 net new actives/mo**

`budget-allocation-model.md` Scenario A projects:
- **Current baseline: 300-350 new actives/mo** at $129-$150 blended
- **After channel cleanup: 350-400 actives/mo**

These are the same company, same budget, same time period. The **532 vs 300-350 gap (52-77% difference)** is because meta-budget-reallocation uses Sheets "New Active" (which includes organic-attributed users and may double-count), while budget-allocation-model uses a more conservative definition. Neither document explicitly reconciles with the other.

**Fix:** Cross-reference and explain the gap. If the 532 number uses a broader denominator, say so explicitly.

---

### 6. 🟡 MEDIUM: LTV Model Is Entirely Assumption-Based (No Real Data)

`ltv-model.md` clearly states it's parameterized with placeholder assumptions:
- FX margin: 0.30%-1.00% (placeholder)
- Monthly withdrawal volume per user: $300-$5,000 (guess)
- Lifetime: 3-12 months (guess)

This produces LTV ranges of $2.7 to $600 per user — a **222× spread**. Yet downstream documents (`ltv-cac-ratio.md`, `budget-allocation-model.md`, `unit-economics-brief.md`) cite the "Base" LTV scenario as if it has analytical backing:
- "NG LTV/CAC = 1.80×" → This is the **only market that looks unit-economics positive**, and it's built on a guess that Nigerian users withdraw $800/mo at 0.6% margin for 6 months.

The entire "Nigeria is the growth engine" thesis rests on assumed LTV that hasn't been validated with a single real data point.

**Fix:** Flag all LTV-dependent conclusions as "contingent on LTV validation." Prioritize pulling actual withdrawal volumes from the backend in Sprint 2.

---

### 7. 🟡 MEDIUM: Pre-KYC Survey Findings — "67% Rejection" vs KYC Deepdive Consistency

`pre-kyc-survey-investigation.md` claims:
- NG: 70% rejection rate (158/226 evaluated)
- EG: 63% rejection rate (36/57 evaluated)
- Combined: 67% rejection
- **0 Bridgexyz handoff** despite 89 approvals

`kyc-dropout-deepdive.md` independently found:
- NG: KYC Started=230, Shown=0, Submit=0
- EG: KYC Started=62, Shown=0, Submit=0

**These are consistent** ✅ — the KYC deepdive sees the same pattern (0 Shown) but didn't yet know the Pre-KYC survey was the gating mechanism. The pre-KYC investigation adds the crucial detail of WHY (survey rejection + handoff bug).

However, `kyc-dropout-deepdive.md` lists 3 possible explanations for the 0 Shown (provider gating, different KYC provider, instrumentation gap) but doesn't reference the pre-KYC survey at all. This suggests the two analyses were done independently without cross-referencing.

**Minor inconsistency:** KYC deepdive says NG KYC Started=230, pre-KYC investigation says NG KYC Started=230. ✅ Match. But pre-KYC says "292 users starting KYC" (NG+EG total), while KYC deepdive shows NG(230)+EG(62)=292. ✅ Match.

**Fix:** Cross-link the two documents. The pre-KYC investigation effectively answers the questions raised in the KYC deepdive.

---

### 8. 🟡 MEDIUM: Cortex Dashboard Numbers Don't Exactly Match Analysis Docs

| Metric | Cortex data.json | funnel-summary.md | channel-cac.md | Δ |
|---|---|---|---|---|
| Installs | 1,453 | 1,445 | 1,444 (sum of channels) | 0.6% spread |
| Signups | 1,219 | 1,207 | 1,206 | 1.1% spread |
| KYC Submits | 185 | 179 | N/A | 3.3% spread |
| Withdrawals | 2,236 | 2,227 | 2,226 | 0.4% spread |
| DAU | 3,074.6 | 3,060 | N/A | 0.5% spread |

The differences are small (0.4-3.3%) and likely due to different pull times or API query parameters. But they erode confidence when you're trying to validate claims across documents. The KYC submits discrepancy (185 vs 179 = 6 events) is the most notable.

**Fix:** Use a single canonical data pull as the source for all analysis docs. Pin the pull timestamp.

---

### 9. 🟡 MEDIUM: Scripts Without Error Handling

Several scripts have **zero error handling patterns** (no try/except, no sys.exit, no input validation):

| Script | Error Handling | Risk |
|---|---|---|
| `analyze_country.py` | 0 patterns | Crashes on missing/malformed JSON |
| `attribution_funnel.py` | 0 patterns | Crashes on API failure, no retry |
| `campaign_health_check.py` | 0 patterns | Crashes on missing input files |
| `country_breakdown.py` | 0 patterns | Crashes on API failure |
| `feature_engagement.py` | 0 patterns | Crashes on API failure |
| `platform_funnel.py` | 0 patterns | Crashes on API failure |

These are the same scripts that have hardcoded credentials. They appear to be "quick and dirty" pull scripts written for one-time use but now sitting in the repo alongside production-quality scripts like `weekly_report.py` (25 error-handling patterns) and `kpi_auto_update.py` (11 patterns).

**Fix:** Either (a) move one-time scripts to a `scripts/adhoc/` directory with a README, or (b) add basic error handling (file existence checks, API response validation, graceful failures).

---

### 10. 🟢 LOW-MEDIUM: Logical Tension — "Pause Meta" vs "Scale Meta Egypt"

Multiple documents recommend pausing Meta spending:
- `channel-cac.md`: Meta is on "Watchlist" 
- `budget-efficiency.md`: "Keep Meta capped / under test"
- `meta-underperforming.md`: "Pause meta_w2a Turkey immediately"
- `meta-budget-reallocation.md`: "Cut $7,600/mo from Meta"

But simultaneously:
- `budget-allocation-model.md` Scenario B: "Meta test $2,400/mo" for Nigeria
- `meta-underperforming.md`: "Scale meta_ltv_test (Egypt) to $2,000/wk" ⭐⭐
- `egypt-scaling-plan.md`: Meta LTV test is the star performer

This is **not actually a contradiction** — the nuance is "pause Meta W2A prospecting in Turkey, keep Meta retargeting, and scale the specific Meta LTV test campaign in Egypt." But it requires careful reading. A busy executive scanning headlines could easily misread "Pause Meta" as a blanket recommendation.

**Fix:** Add a "Meta Decision Matrix" summary: which Meta campaigns to pause, keep, and scale — in one table, one place.

---

## Data Consistency Check

### Key Numbers Across Documents

| Metric | channel-cac | budget-efficiency | meta-underperforming | blended-cac | Cortex | Consistent? |
|---|---|---|---|---|---|---|
| Meta spend/wk | $2,754 | $2,754 | $2,754 | N/A (monthly) | N/A | ✅ |
| Meta CPI | $22.57 | $22.57 | N/A | N/A | N/A | ✅ |
| Meta Cost/Signup | $125.18 | $125.18 | N/A | N/A | N/A | ✅ |
| Meta Cost/New Active | $82.21 | $82.21 | $82/active | N/A | N/A | ✅ |
| Pmax Cost/New Active | $19.18 | $19.18 | N/A | N/A | N/A | ✅ |
| ASA Cost/New Active | $22.66 | $22.66 | N/A | N/A | N/A | ✅ |
| Total installs (wk) | 1,444 (sum) | Same | N/A | N/A | 1,453 | ⚠️ ~0.6% |
| TR $/Active (Feb) | N/A | N/A | N/A | $208 | N/A | N/A |
| TR $/Paid Active (Mar 9-15) | N/A | N/A | N/A | N/A | N/A | N/A |
| NG Cost/Paid Active | N/A | $16 | N/A | N/A | N/A | ✅ vs country-cac |
| Unattributed signups | 986/1,206 (82%) | N/A | N/A | N/A | N/A | ✅ vs attribution-reconciliation |
| KYC Submit TR | N/A | N/A | N/A | N/A | 185 | ⚠️ vs funnel-summary (179) |

**Channel-level numbers are consistent** across channel-cac, budget-efficiency, and meta-underperforming (they all reference the same source data). The inconsistencies emerge at the "blended CAC" and "total actives" level due to different metric definitions.

---

## Logical Contradictions

### 1. Budget-neutral reallocation math doesn't add up globally

`meta-budget-reallocation.md` claims the reallocation is "budget-neutral" ($11,016 → $11,016). But `budget-allocation-model.md` works with a $50K total budget and allocates differently. The meta-budget-reallocation focuses only on Meta's portion without reconciling with the full $50K envelope.

This isn't technically a contradiction (it's a scope difference) but it means two documents give different operational guidance for the same budget.

### 2. Turkey 90-day plan baseline vs reality

`turkey-90d-plan.md` uses "$20-$21 blended CAC/new active" as the baseline, which comes from `meta-budget-reallocation.md`'s all-channel Sheets-based calculation. But `blended-cac.md` shows the TR blended CAC as $86-$208 depending on month. The $20 figure appears to use a denominator that includes organic/unattributed actives in the denominator but only paid spend in the numerator — which is misleading.

---

## Missing Caveat Alerts

**19 documents lack attribution gap warnings.** Most critical omissions:

| Document | Why caveat matters |
|---|---|
| `bid-strategy-reco.md` | Recommends optimizing to specific conversion events without noting those events may be misattributed |
| `ltv-cac-ratio.md` | Computes ratios using CAC that may be 6.9× overstated |
| `country-cac.md` | Core CAC reference doc — should lead with attribution warning |
| `egypt-scaling-plan.md` | Recommends budget decisions based on CAC numbers affected by attribution |
| `nigeria-growth-plan.md` | Same |
| `creative-scoring.md` | Evaluates creative performance using potentially misattributed conversions |

---

## Script Quality Assessment

| Script | Verdict |
|---|---|
| `amplitude_attribution.py` | ⚠️ Minimal error handling; uses env file for creds |
| `amplitude_country_breakdown.py` | ✅ Clean, proper cred loading, adequate error handling |
| `amplitude_kyc_deepdive.py` | ✅ Good structure, retry logic, proper cred loading |
| `amplitude_platform_breakdown.py` | ✅ Clean, mirrors country_breakdown pattern |
| `amplitude_retention.py` | ✅ Good error handling, uses requests library |
| `amplitude_weekly_pull.py` | ⚠️ Minimal error handling but uses env file |
| `analyze_country.py` | ❌ No error handling, crashes on missing file, hardcoded relative paths |
| `anomaly_detection.py` | ⚠️ Minimal but functional; argparse is good |
| `attribution_funnel.py` | 🔴 Hardcoded API keys, no error handling |
| `bq_campaign_trends_30d.py` | ⚠️ Minimal error handling but well-structured |
| `budget_pacing.py` | ✅ Good file checking, clear output |
| `campaign_health_check.py` | ❌ No error handling, crashes on missing input files |
| `country_breakdown.py` | 🔴 Hardcoded API keys, no error handling |
| `data_quality_monitor.py` | ✅ Best script in the set — comprehensive error handling, clear structure |
| `feature_engagement.py` | 🔴 Hardcoded API keys, no error handling |
| `ga4_web_traffic_deepdive.py` | ✅ Good error handling, env var-based config |
| `kpi_auto_update.py` | ✅ Well-built, proper cred loading, retries, dry-run support |
| `monthly_deck.py` | ✅ Robust error handling, offline-first design |
| `platform_funnel.py` | 🔴 Hardcoded API keys, no error handling |
| `weekly_actions.py` | ✅ Good structure, handles missing inputs gracefully |
| `weekly_report.py` | ✅ Best-in-class: 25 error-handling patterns, clean output |
| `anomaly_alert_cron.sh` | ✅ Uses set -euo pipefail, proper error handling |
| `dead_campaign_sweep_cron.sh` | ✅ Good cron wrapper pattern |
| `weekly_kpi_cron.sh` | ✅ Well-structured, date handling, logging |
| `weekly_report_cron.sh` | ✅ Clean, checks dependencies |

**Summary:** 4 scripts are security risks (hardcoded keys). ~6 scripts lack basic error handling. The cron wrappers and production scripts are well-built. There's a clear quality split between "quick pull" scripts and "production" scripts.

---

## Gaps & Blind Spots

### What Should Have Been Analyzed But Wasn't

1. **Actual withdrawal volumes ($)** — The LTV model uses guesses ($300-$5,000/mo). This data likely exists in the backend. Without it, the entire unit economics analysis is speculative.

2. **Cohort retention curves** — `retention.md` acknowledges it uses crude DAU/signup proxies. True D1/D7/D30 retention by channel and country was never computed despite being critical for LTV.

3. **Creative performance analysis** — `creative-scoring.md` exists but there's no actual creative-level data (CTR, CVR, frequency by ad creative). Meta MCP access was blocked, but no workaround (CSV export, browser screenshots) was attempted for creative analysis.

4. **Incrementality / holdout tests** — Multiple documents recommend geo holdouts and incrementality testing, but none were designed or executed. This is the only way to resolve the "does Meta drive organic?" question.

5. **Revenue per user by channel** — No document computes revenue-per-user segmented by acquisition channel. This would directly answer which channels produce the most valuable users.

6. **Referral program deep-dive** — `referral-scaling-plan.md` exists but the analysis is thin. Referral shows the best unit economics (42.9% signup rate, $30/active) but only 7 installs/week. What's blocking scale?

7. **KYC error telemetry** — The KYC deepdive identifies the problem but no one instrumented or pulled the actual error logs between "Pre-KYC Approved" and "Bridgexyz Shown." This is product engineering work but the analysis team could have pushed harder.

8. **Competitor pricing analysis** — `competitive-positioning.md` exists but doesn't include actual fee comparisons. Claims like "10× cheaper than Payoneer" in the creative plan are unsubstantiated with data.

9. **Seasonality decomposition** — `seasonal-trends.md` exists but the DAU drop of -46.1% WoW isn't adequately explained. Is this Ramadan? Nowruz? Random variance? This matters for forecasting.

10. **Web funnel analytics** — GA4 deepdive was blocked by missing `GA4_PROPERTY_ID`. The web→app handoff analysis identifies the problem conceptually but has no actual GA4 data to quantify drop-offs at each step.

---

## Recommendations for Sprint 2

### P0 (Do First)

1. **Rotate Amplitude API credentials immediately** — they're in plaintext in the git repo.

2. **Create a metric definitions document** — One page that defines: "new_active" vs "paid_active" vs "active user," "blended CAC" vs "paid-attributed CAC," and which Sheets tab / Amplitude event / AppsFlyer field each maps to. Every analysis doc must reference it.

3. **Pull actual withdrawal volumes from backend** — Replace LTV model guesswork with real numbers. This single data point transforms the entire unit economics analysis from speculative to actionable.

4. **Add attribution caveat to all 19 uncaveated documents** — Or create a repo-wide `ATTRIBUTION_WARNING.md` that is referenced.

### P1 (High Priority)

5. **Designate one canonical budget plan** — Consolidate budget-allocation-model, meta-budget-reallocation, and turkey-90d-plan into a single "Budget Decision" document. Others can provide supporting analysis but should not propose independent allocations.

6. **Run one incrementality test** — Design a geo holdout for Meta in one Turkish city. This would resolve the "does Meta drive organic?" question that underlies half the analysis uncertainty.

7. **Fix GA4 access** — Get the property ID and run the web funnel analysis. The web→app handoff is the second biggest problem after KYC, and we have zero data on it.

8. **Compute true cohort retention** — Use Amplitude's cohort/retention API or BigQuery to get D1/D7/D30 by channel and country. This replaces the crude DAU/signup proxy currently in use.

### P2 (Important)

9. **Standardize script quality** — Move adhoc pull scripts to `scripts/adhoc/`, add basic error handling, and remove all hardcoded credentials.

10. **Cross-link related analyses** — The pre-KYC investigation and KYC deepdive were done independently. Several other doc pairs have similar cross-referencing gaps. A simple "See also:" footer would help.

11. **Reconcile Cortex dashboard numbers with analysis docs** — Pin a single data pull timestamp and make all docs reference the same source numbers. Even 0.5-3% discrepancies erode trust.

12. **Track the DAU cliff** — -46.1% WoW DAU decline is mentioned but not explained. If this is seasonal (Ramadan/Nowruz), document it. If it's a product issue, escalate.

---

*Generated: 2026-03-22 | Independent Audit*
