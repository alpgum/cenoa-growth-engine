# March 2026 Month-End Report — Cenoa Performance Marketing

**Status:** DRAFT — Pre-filled with data through Mar 22. Final numbers marked [TBD - fill Mar 31].  
**Prepared:** 2026-03-23  
**Period:** March 1–31, 2026  
**Budget envelope:** $50,000  
**Data sources:** Google Sheets (spend/funnel through Mar 15), Amplitude (events through Mar 21), AppsFlyer (attribution), BigQuery  

---

## 1. Executive Summary

- **March media spend will land ~$27–30K against a $50K plan** — a ~$20K underspend driven by unstarted channels (PK, Affiliate, Influencer, Reddit, LinkedIn) and intentional pauses on fraud/waste channels. [TBD - fill Mar 31: final spend number]
- **Blended TRUE CAC (cost/new_active) = $33.67 through Mar 15** — headline looks strong vs the $48–$81 target, but contaminated by returning-user withdrawals and 82% attribution gap. Steady-state TR CAC is likely $80–$150.
- **$9.4K/month in waste identified and flagged for pause:** Appnext (fraud), Meta W2A TR prospecting ($3,536/active), Demand Gen retargeting (5 months, 0 installs), Twitter ($183 CPI, 0 downstream).
- **Growth Engine infrastructure built from scratch:** 26 reusable scripts, automated anomaly detection, campaign health checks, weekly reporting pipeline, and canonical metric definitions — replacing unreliable Looker/connector stack.
- **Critical blockers remain:** KYC handoff broken in NG/EG (0 submits), web→app attribution broken (82% unattributed), GA4 access incomplete. These must be fixed before April scaling.

---

## 2. March Budget: $50K Plan vs Actual Spend

### By Country

| Country | Plan ($) | % of Plan | Actual (est. 21d) | Projected EOM | Pacing % | Status |
|---------|----------:|----------:|---------:|--------:|----------:|--------|
| TR | $23,000 | 46.0% | $11,527 | [TBD - fill Mar 31] | 50.1% | 🟡 Under |
| EG | $8,500 | 17.0% | $6,919 | [TBD - fill Mar 31] | 81.4% | 🔴 Over (Meta 3.3×) |
| PK | $6,000 | 12.0% | $0 | $0 | 0.0% | ⚫ Not launched |
| NG | $2,200 | 4.4% | $427 | [TBD - fill Mar 31] | 19.4% | 🔴 Severely under |
| Subs + Buffer | $10,300 | 20.6% | ~$2,689 | [TBD - fill Mar 31] | — | — |
| **Total** | **$50,000** | **100%** | **~$21,562** | **[TBD - fill Mar 31]** | **~43%** | **🟡 Underspent** |

### By Channel — Turkey ($23K plan)

| Channel | Plan (Mo) | Actual (est. 21d) | Pacing % | Status |
|---------|----------:|---------:|----------:|--------|
| Google Pmax/Search/W2A | $3,750 | $2,305 | 61.5% | 🟡 Slightly under |
| Meta (W2A + RTGT + test) | $750 | $1,742 | 232.3% | 🔴 Over 2.3× |
| Apple Search Ads | $2,800 | $1,587 | 56.7% | 🟡 Under |
| TikTok (W2A + app) | $1,200 | $994 | 82.8% | ✅ On pace |
| Spaze + Appnext | $4,500 | $3,776 | 83.9% | ✅ On pace (quality issues) |
| Twitter | $1,000 | $260 | 26.0% | 🔴 Severely under |
| Affiliate / RAF / CRM | $3,000 | $0 | 0.0% | ⚫ Not started |
| Influencer / Other | $4,500 | $0 | 0.0% | ⚫ Not started |
| Reddit / LinkedIn | $1,500 | $0 | 0.0% | ⚫ Not started |

### By Channel — Egypt ($8.5K plan)

| Channel | Plan (Mo) | Actual (est. 21d) | Pacing % | Status |
|---------|----------:|---------:|----------:|--------|
| Google Pmax | $1,500 | $1,553 | 103.6% | ✅ On pace |
| Meta (get_paid + LTV) | $1,500 | $4,875 | 325.0% | 🔴🔴 3.3× over |
| Apple Search Ads | $500 | $70 | 14.0% | 🔴 Severely under |
| TikTok / AdNetworks / Affiliate | $5,000 | $0 | 0.0% | ⚫ Not started |

**Key takeaway:** ~$20K of the $50K budget is allocated to channels that never launched (PK entirely, plus Affiliate/Influencer/Reddit/LinkedIn in TR, TikTok/AdNetworks in EG). Meta EG massively overspent its allocation. Effective media spend will be ~55–60% of envelope.

---

## 3. March KPI Targets vs Actuals

### Country-Level Funnel (Mar 1–15 hard data)

| Metric | TR | NG | EG | Total | Monthly Target | Achievement % |
|--------|---:|---:|---:|------:|-------:|---------:|
| Spend | $7,824 | $230 | $5,549 | $13,603 | $50,000 | 27.2% (15d) |
| Installs | 3,289 | 1,445 | 1,252 | 5,986 | [TBD - fill Mar 31] | — |
| Sign-ups | 1,176 | 614 | 703 | 2,493 | [TBD - fill Mar 31] | — |
| Virtual Accounts | 776 | 260 | 217 | 1,253 | [TBD - fill Mar 31] | — |
| New Active (1st withdrawal) | 292 | 31 | 81 | 404 | [TBD - fill Mar 31] | — |
| Paid Active (repeat usage) | 22 | 23 | 62 | 107 | [TBD - fill Mar 31] | — |

### TRUE CAC vs Targets

| Country | TRUE CAC (Actual) | Target Range | Status | Notes |
|---------|---:|---:|--------|-------|
| TR | $26.79 | $100–$130 | ⚠️ Looks good — caveats apply | Under-pacing + returning-user contamination inflate efficiency |
| NG | $7.42 | $20–$40 | ⚠️ Low spend ($230), unreliable | Mostly organic; KYC broken |
| EG | $68.51 | $50–$80 | 🟡 Within range | Meta 3.3× over budget driving this |
| **Blended** | **$33.67** | **$48–$81** | **✅ Below target** | **Directional only — see caveats** |

### TRUE CAC Caveats (Critical)

- **Returning-user contamination:** "Withdraw Completed" includes existing users, not just March acquisitions. W3 had 568 TR withdrawals vs ~208 new virtual accounts.
- **Attribution gap:** 82% of sign-ups have "(none)" source. Channel-level CAC is not calculable.
- **Under-pacing effect:** Lower spend = cherry-picking highest-intent users. CAC will rise at scale.
- **Estimated steady-state TR CAC: $80–$150/new_active** (not $26.79).

### Weekly Trajectory (W2 → W3)

| Metric | W2 (Mar 8–14) | W3 (Mar 15–21) | WoW Δ |
|--------|---:|---:|---:|
| Installs | 2,274 | 1,445 | ▼ 36.5% |
| Sign-ups | 1,672 | 1,207 | ▼ 27.8% |
| KYC submits | 307 | 179 | ▼ 41.7% |
| Avg DAU | 5,680 | 3,060 | ▼ 46.1% |

> ⚠️ Sharp W3 decline across all top-of-funnel metrics. Likely seasonal (Ramadan/Nowruz) and/or creative fatigue. Needs investigation. [TBD - fill Mar 31: W4–W5 data to confirm trend]

---

## 4. Channel Performance Summary

### 🟢 Winners — Scale

| Channel | Country | Cost/Active | Why It Works | Action Taken / Recommended |
|---------|---------|---:|---|---|
| **Google Pmax** | TR | $19.18 | Best cost/active in portfolio; ML-optimized across surfaces | +50% budget increase recommended |
| **Apple Search Ads (Brand)** | TR | $22.66 | Highest-intent users; 114 withdrawals from 26 installs (cohort LTV proof) | Scale to $5K/mo |
| **Google Search** | TR | $25.48 | 49% sign-up rate; strong intent capture | +$200/wk recommended |
| **Meta LTV Test** | EG | $68 | Improving WoW ($174→$68); only Meta campaign that works | Scale to $2K/wk |
| **Referral** | All | ~$30 | Best unit economics; 42.9% signup rate; highly active cohorts | Increase incentives +50% |

### 🔴 Losers — Paused/Killed

| Channel | Country | Cost/Active | Why It Failed | Action Taken |
|---------|---------|---:|---|---|
| **Appnext** | Multi | ∞ (0–1 active from 1,779 installs) | Install fraud — bot farms | Flagged for immediate pause; fraud claim filed |
| **Meta W2A Prospecting** | TR | $3,536 (Jan) → ∞ (Feb) | Structural W2A failure; attribution collapse | Kill all prospecting; keep RTGT at $500/wk |
| **Demand Gen Retargeting** | TR | ∞ (0 installs, 5 months) | Retargeting app users; wrong conversion action | Kill immediately; ~$11.2K wasted total |
| **Twitter Ads** | TR | $183 CPI, 0 downstream | Dead channel for app installs | Killed permanently |
| **Onboarding Meta Test** | TR | $33.67 CPI, 0 active | Tiny budget, terrible efficiency | Paused |

### 🟡 Watch List

| Channel | Country | Issue | Deadline |
|---------|---------|-------|----------|
| TikTok (all variants) | TR | 0 withdrawals in attribution; cheap CPI but no downstream proof | Mar 28 — pause if still 0 |
| Meta Get Paid | EG | Week 1 excellent ($96), Week 2 collapsed ($637) | Creative refresh or reallocate to LTV test |
| EG Meta W2A (new) | EG | Launched Mar 18–20; too early to judge | Apr 3 deadline |
| NG Google Search Architect | NG | Good sign-ups, zero activation; KYC broken | Post-KYC fix only |

### Budget Impact of Pauses

| Action | Monthly Savings |
|--------|---:|
| Pause Appnext | +$880/mo |
| Pause Meta W2A TR prospecting | +$6,000/mo |
| Pause Demand Gen | +$2,240/mo |
| Pause Twitter | +$183/mo |
| **Total freed** | **~$9,400/mo** |

**Recommended reallocation:** Pmax +$1,600/mo, ASA +$1,200/mo, Search +$800/mo, Meta LTV EG +$2,400/mo, Referral +$300/mo, NG Google (post-KYC) +$3,100/mo.

---

## 5. Key Learnings

### 5.1 KYC Bug (P0)
- **Nigeria:** 230 KYC starts → 0 submits. Pre-KYC AI survey approves 33% of users, but the 89 approved users hit a dead end — Bridgexyz handoff is broken (bug, not optimization).
- **Egypt:** 62 KYC starts → 0 submits. Same bug.
- **Turkey:** Only market with functioning KYC (170/179 submits globally), but even TR leaks 94% — 3,025 see the component, 170 submit. iOS is 3.8× worse than Android.
- **Impact:** Scaling NG/EG acquisition is literally burning money until this ships.

### 5.2 Attribution Gap (P0)
- 81.8% of sign-ups have no source attribution (986/1,206). Web→app handoff (ad → cenoa.com → App Store) breaks the chain.
- Correction factor estimated at ~6.9× (last-click credits 121 paid sign-ups; modeled estimate is ~830).
- **Impact:** Channel-level CAC is unreliable. Cannot make confident budget decisions. Need OneLink + deferred deep linking + UTM persistence.

### 5.3 Appnext Fraud
- 1,779 installs at $0.50 CPI → only 47 virtual accounts (2.6% conversion) → 0–1 new active users.
- DSP variant: 113 installs, 2 sign-ups, 0 active.
- Classic bot farm pattern: high volume, zero downstream.
- **Impact:** ~$893 wasted in 15 days. Fraud claim submitted. Added to permanent exclusion list.

### 5.4 Demand Gen Waste
- TR-Discovery campaign running since Oct 2025: 1,627 clicks/week, **zero installs over 5 months**.
- Estimated total waste: $5,600–$11,200.
- Was never flagged because engagement metrics (clicks, impressions) looked healthy; nobody monitored conversion outcomes.
- **Impact:** Instituted campaign health check automation — "high spend + 0 conversions" now triggers alerts.

### 5.5 Budget Overspend (EG Meta)
- Egypt Meta planned at $1,500/mo; actual tracking to $8K+ by month-end (5.3×).
- "Get paid" and "LTV" test campaigns ran without budget caps.
- Meta LTV test EG is producing at $68/active (acceptable), but budget discipline was violated.
- **Impact:** Formal budget caps now enforced per channel; weekly pacing alerts active.

### 5.6 CAC Definition Chaos
- CAC numbers swing 42× depending on the document: $20.70 vs $208 vs $864 for "cost per active in Turkey."
- Different denominators (virtual account vs new_active vs paid_active), different time periods, no standard definitions.
- **Impact:** Created `metric-definitions.md` as canonical source. All analysis now references standardized event names and denominators.

---

## 6. Growth Engine Infrastructure Built

### Scripts & Automation (26 scripts committed)

| Category | Scripts | Function |
|----------|---------|----------|
| **Data pulls** | `amplitude_weekly_pull.py`, `amplitude_country_breakdown.py`, `amplitude_platform_breakdown.py`, `amplitude_attribution.py` | Repeatable Amplitude data extraction with JSON audit trails |
| **Anomaly detection** | `anomaly_detection.py` + `anomaly_alert_cron.sh` | WoW anomaly alerts for spend, installs, sign-ups, KYC; reduces cognitive load |
| **Campaign health** | `campaign_health_check.py` | Automated DEAD/BLEEDING/FRAUD classification; catches Demand Gen-style waste |
| **Reporting** | `weekly_report.py` + `weekly_report_cron.sh` | Auto-generate weekly markdown reports with Telegram formatting |
| **Budget monitoring** | Sheets API integration | Real-time budget vs actual pacing by country and channel |

### Dashboards & Surfaces

| Surface | Status | Notes |
|---------|--------|-------|
| KPI banner (Cortex `data.json`) | ✅ Live | Single source of truth for weekly KPIs |
| Looker Studio embed | 🟡 Partial | 4 Supermetrics connectors broken; use for visuals only, not data |
| Script-based pipeline | ✅ Primary | JSON outputs → analysis docs → decision flow |

### Analysis Assets

- **70+ analysis documents** covering funnel, attribution, CAC, channel efficiency, budget pacing, market deep-dives
- **Canonical references:** `metric-definitions.md`, `ATTRIBUTION_WARNING.md`, `budget-allocation-model.md`, `marginal-cac-curves.md`
- **TASK_QUEUE.md** sprint system with explicit status tracking, dependencies, and skip rules

---

## 7. April Budget Recommendation

Based on marginal CAC curves and the budget allocation model, recommended April allocation:

### Scenario A: KYC Still Broken in NG/EG (Conservative)

| Country | April Budget | % | Primary Channels | Expected $/Active |
|---------|---:|---:|---|---:|
| TR | $40,000 | 80% | Pmax $12K, ASA $5.2K, Search $6.4K, Meta RTGT $2.4K, Spaze $3.2K, Referral $4K, Tests $2K, Other $4.8K | $100–$130 |
| EG | $6,000 | 12% | Meta LTV $2.8K, Google Pmax $2K, Search $1.2K | $50–$80 |
| NG | $2,000 | 4% | Google Search $1K, Google Pmax $600, Meta test $400 | $20–$40 (unproven) |
| Reserve | $2,000 | 4% | New channel tests | — |
| **Total** | **$50,000** | **100%** | | |

### Scenario B: KYC Fixed in NG/EG (Aggressive)

| Country | April Budget | % | Primary Channels | Expected $/Active |
|---------|---:|---:|---|---:|
| TR | $28,000 | 56% | Pmax $8.4K, ASA $5.6K, Search $5K, Meta RTGT $2.4K, Spaze $2.2K, Referral $2.8K, Tests $1.6K | $100–$130 |
| NG | $12,000 | 24% | Google Search $6K, Pmax $3.6K, Meta test $2.4K | $20–$40 |
| EG | $8,000 | 16% | Meta LTV $2.8K, Google Search $2.4K, Pmax $2K, ASA $800 | $50–$80 |
| Reserve | $2,000 | 4% | New channel tests | — |
| **Total** | **$50,000** | **100%** | | |

### Marginal CAC Curve Guidance (TR Channels)

| Channel | Current Spend/mo | Sweet Spot Ceiling | Recommended April | Headroom |
|---------|---:|---:|---:|---:|
| Google Pmax | $3,489 | $51,000 | $8,400–$12,000 | 14.6× (massive) |
| Apple Search Ads | $2,602 | $5,200 | $5,200 | 2.0× (near ceiling) |
| Google Search | $3,423 | $6,400 | $5,000–$6,400 | 1.9× (near ceiling) |

> **Pmax is the scaling workhorse.** α = 0.25 means gentle CAC degradation — marginal CAC stays under $50 up to ~$51K/mo. ASA and Search are near their efficient ceilings; optimize bids before increasing budget.

---

## 8. April Priority Channels

### 🟢 Scale (Proven)

| Priority | Channel | Country | April Budget | Rationale |
|----------|---------|---------|---:|---|
| 1 | **Google Pmax** | TR | $8.4K–$12K | Best cost/active ($19.18); most scaling headroom (14.6×); ML-optimized |
| 2 | **Apple Search Ads** | TR | $5.2K | Highest-intent users; expand to generic + broad match; near efficient ceiling |
| 3 | **Google Search** | TR | $5K–$6.4K | Reliable quality at $25.48/active; near ceiling — optimize bids first |
| 4 | **Meta LTV Test** | EG | $2.8K | Only Meta campaign that works ($68/active, improving); primary EG lever |

### 🟡 Expand (Test → Scale)

| Priority | Channel | Country | April Budget | Rationale |
|----------|---------|---------|---:|---|
| 5 | **NG Google Search** | NG | $3K–$6K | Best blended CAC ($7.42) but KYC-blocked; scale immediately post-KYC fix |
| 6 | **NG Google Pmax** | NG | $600–$3.6K | ML-optimized complement to Search; test alongside |
| 7 | **Referral Program** | All | $2.8K–$4K | Best unit economics (~$30/active); increase incentives +50%; in-app prompts |

### 🔴 Meta Retargeting Only (TR)

- **Keep:** Meta RTGT at $2.4K/mo cap — only Meta W2A sub-campaign showing real withdrawals (9/wk attributed).
- **Kill:** All Meta W2A prospecting in TR. Do not reactivate until web→app attribution is fixed end-to-end.
- **Test:** Meta App Install (iOS) in TR at small budget ($1K/mo) — 65% sign-up rate, 32 new active; warrants further testing.

---

## 9. Risks & Dependencies

### 🔴 P0 — Must Fix for April Success

| Risk | Impact | Owner | Status |
|------|--------|-------|--------|
| **KYC handoff broken (NG/EG)** | $14K–$20K of April budget targets markets where users literally cannot complete KYC. Scaling = burning money. | Engineering (Bridgexyz integration) | 🔴 Open — 0 submits in NG/EG |
| **Web→App attribution broken** | 82% of sign-ups unattributed. Channel-level budget decisions are directional guesses, not data-driven. All CAC numbers carry ±50% uncertainty. | Product/Engineering (OneLink + deferred deep links + UTM) | 🔴 Open |
| **GA4 access incomplete** | Web funnel analysis blocked. Can't measure cenoa.com → App Store handoff — the exact point where attribution breaks. | Marketing Ops (GA4 property ID + service account access) | 🟡 Partial — service account added, property ID needed |

### 🟡 P1 — Should Fix

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Amplitude property gaps** | 62.5% of sign-ups missing country/platform. Country-level analysis unreliable. | Escalate to product; add property propagation to user events |
| **Looker connectors broken** | 4 Supermetrics connectors down (Meta, TikTok organic, LinkedIn organic, IG organic). Dashboard unreliable for stakeholder reporting. | Use script pipeline as primary; fix Looker connectors as P2 |
| **API credentials in git** | 4 scripts committed with hardcoded Amplitude API keys. Security incident risk. | Rotate keys Monday; refactor to env files |
| **DAU drop unexplained** | 46.1% WoW decline in W3. Could be seasonal (Ramadan) or product issue. Affects forecasting. | [TBD - fill Mar 31: confirm trend in W4–W5] |

### 🟢 Dependencies Met

| Dependency | Status |
|------------|--------|
| BigQuery access | ✅ Working — AppsFlyer data queryable |
| Google Sheets API | ✅ 3 sheets accessible — budget, CAC, traffic data |
| Amplitude API | ✅ REST API confirmed working |
| Automation pipeline | ✅ 26 scripts operational; anomaly + health check crons ready |

---

## Appendix: Final March Numbers (Fill Mar 31)

> **Instructions:** Update these fields with final data on March 31.

| Metric | Final Value | Notes |
|--------|-------------|-------|
| Total March media spend | [TBD - fill Mar 31] | |
| TR total spend | [TBD - fill Mar 31] | |
| EG total spend | [TBD - fill Mar 31] | |
| NG total spend | [TBD - fill Mar 31] | |
| Total installs (March) | [TBD - fill Mar 31] | |
| Total sign-ups (March) | [TBD - fill Mar 31] | |
| Total new active (March) | [TBD - fill Mar 31] | |
| Total paid active (March) | [TBD - fill Mar 31] | |
| Blended TRUE CAC (March) | [TBD - fill Mar 31] | |
| TR TRUE CAC (March) | [TBD - fill Mar 31] | |
| EG TRUE CAC (March) | [TBD - fill Mar 31] | |
| NG TRUE CAC (March) | [TBD - fill Mar 31] | |
| W4 installs | [TBD - fill Mar 31] | Confirm W3 decline trend |
| W4 DAU | [TBD - fill Mar 31] | Confirm 46% drop trend |
| Channels paused (confirmed) | [TBD - fill Mar 31] | Appnext, Demand Gen, Meta W2A TR, Twitter |
| KYC fix shipped? | [TBD - fill Mar 31] | Determines April Scenario A vs B |
| Attribution fix shipped? | [TBD - fill Mar 31] | OneLink + UTM persistence |

---

*Generated: 2026-03-23 | Sprint S3-028*  
*Sources: march-mtd-budget-vs-actual.md, march-mtd-cac-tracking.md, campaign-commentary-mar22.md, weekly-learnings-mar15-21.md, sprint-1-retrospective.md, budget-allocation-model.md, marginal-cac-curves.md*
