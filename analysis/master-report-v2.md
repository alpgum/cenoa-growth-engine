# Cenoa Performance Marketing — Master Report v2 (Sprint 001–098)

Prepared: 2026-03-21

Primary analysis window: 2026-03-14 → 2026-03-20 (WoW vs 2026-03-07 → 2026-03-13)

Sources connected: Amplitude, AppsFlyer (via BigQuery + Amplitude properties), Google Sheets (Budget Tracking + CAC Analysis + Trafik Canavarı), BigQuery.

Confidence note (plain-English): funnel + KYC findings are **high confidence** (event-level). Channel ROI is **directional** because downstream attribution is missing for most conversions.

Key “source of truth” references:
- Funnel + KYC: `analysis/funnel-summary.md`
- KPI deltas: `analysis/global-funnel.md`
- Budget efficiency: `analysis/budget-efficiency.md`, `analysis/channel-cac.md`
- Attribution gap + stop-gap correction: `analysis/attribution-reconciliation.md`
- Web→app fix blueprint: `analysis/web-to-app-handoff.md`
- Market strategy: `analysis/turkey-90d-plan.md`, `analysis/multi-market-expansion-playbook.md`
- Automation system: `analysis/automation-setup.md`, `analysis/data-quality-monitoring.md`

---

## 1) Executive summary (10 bullets)

1) **KYC is the bottleneck**: of ~3,098 KYC starts, only **179** submit (≈**5.8%**) → 94% dropout. (`analysis/global-funnel.md`, `analysis/kyc-dropout-deepdive.md`)

2) **Outside Turkey, KYC is effectively dead**: Nigeria + Egypt + Pakistan produce **687 / 1,445 installs (48%)** but **0 KYC submits** in the week. (`analysis/funnel-summary.md`)

3) **Root cause in NG/EG is not “low intent”**: users start KYC, hit a **Pre‑KYC AI survey**, get rejected at ~**67%**, and even the **approved** users never see BridgeXYZ (handoff bug). (`analysis/pre-kyc-survey-investigation.md`)

4) **iOS KYC is broken (or under-instrumented)**: BridgeXYZ shown→submit is **2.4% on iOS vs 9.2% on Android** (≈3.8× gap). (`analysis/ios-android-ux-gap.md`, `analysis/kyc-dropout-deepdive.md`)

5) **Web sign-ups dominate but don’t convert**: **~62.5%** of sign-ups are “web/none” and produce near-zero deposits/withdrawals → a web→app handoff failure. (`analysis/funnel-summary.md`, `analysis/web-to-app-handoff.md`)

6) **Budget is misallocated to low-quality sources**: Appnext is a CPI trap (273 installs → 1 withdrawal; Sheets new_active=0) and should stay paused; TikTok has 0 withdrawals in the attribution week. (`analysis/channel-cac.md`, `analysis/budget-efficiency.md`)

7) **Best activation efficiency channels (current proxy)**: Google Pmax, ASA, and Google Search are the top tier on cost/new_active; Meta is expensive on downstream until measurement is fixed. (`analysis/channel-cac.md`)

8) **Attribution is not decision‑grade**: sign-ups are **~82% “(none)”** and withdrawals **~61% “(none)”** → last-click CAC heavily undercounts paid. (`analysis/attribution-reconciliation.md`)

9) **Stop‑gap: use a correction factor for paid volume undercount**: base estimate implies paid‑influenced sign-ups are ~**6.9×** higher than last-click paid sign-ups until web→app is fixed. (`analysis/attribution-reconciliation.md`)

10) **The growth unlock sequence is clear**: (1) fix NG/EG KYC gates + handoff, (2) fix iOS KYC submit, (3) repair web→app attribution + property propagation, then (4) scale TR and re-open NG/EG with hard gates. (`analysis/multi-market-expansion-playbook.md`)

---

## 2) KPI snapshot + key deltas (WoW)

Global KPIs (Mar 14–20 vs Mar 7–13):
- Installs: **1,445** (WoW **-36.5%**)
- Sign-ups: **1,207** (WoW **-27.8%**)
- KYC submits: **179** (WoW **-41.7%**)  ← the “throughput” collapse
- Deposits (event totals; cohort-mixed): **1,546** (WoW **-5.8%**)
- Withdrawals (event totals; cohort-mixed): **2,227** (WoW **+0.6%**)  ← base is resilient
- DAU (avg): **3,060** (WoW **-46.1%**)  ← investigate if real or instrumentation

Country snapshot (same week; key reality check):
- Turkey: installs **670**, KYC submits **170** (≈**95%** of global KYC submits)
- Nigeria: installs **458**, KYC submits **0**
- Egypt: installs **206**, KYC submits **0**
- Pakistan: installs **23**, KYC submits **0**

Primary KPI interpretation:
- The business is **not supply-constrained by sign-up** (install→signup ≈ 83.5%).
- The system is **throughput-constrained by KYC**, plus a major **web→app leakage**.

References:
- KPI deltas: `analysis/global-funnel.md`
- Definitive breakdown: `analysis/funnel-summary.md`

---

## 3) Funnel + KYC root causes (pre‑survey + handoff bug + iOS gap)

### 3.1 The funnel cliff (global)

Funnel shape (cohort notes: KYC/deposit/withdrawal events are totals and include returning users; KYC submit is still the best “new user throughput” proxy we have):

- Install → Sign-up: healthy
- Sign-up → KYC submit: major drop
- KYC started → KYC submit: catastrophic drop (≈5.8%)

Reference: `analysis/global-funnel.md`

### 3.2 Root cause A — Pre‑KYC AI survey blocks NG/EG volume

Observed flow in NG/EG:
- KYC Started (NG 230, EG 62)
- Pre‑KYC evaluated (NG 226, EG 57)
- Approved (NG 68, EG 21) vs Rejected (NG 158, EG 36)

What this means:
- The AI survey rejects about **2 out of 3** applicants (volume killer).
- Even if everything else worked, only ~30–37% of starters would reach KYC provider UI.

Reference: `analysis/pre-kyc-survey-investigation.md`

### 3.3 Root cause B — Pre‑KYC “approved” → BridgeXYZ handoff is broken (hard bug)

Critical bug signature:
- NG+EG had **89 “approved”** evaluations, but **0 BridgeXYZ component shown** and **0 submits**.

This is not “market fit” and not “messaging”. It’s a routing/rendering/integration failure.

Reference: `analysis/pre-kyc-survey-investigation.md` and `analysis/kyc-dropout-deepdive.md`

### 3.4 Root cause C — iOS KYC shown→submit collapse

Symptom:
- Android BridgeXYZ shown→submit ≈ **9.2%**
- iOS BridgeXYZ shown→submit ≈ **2.4%**

Most likely explanations (ranked):
- iOS UI/UX blocker (CTA hidden/keyboard overlay/validation dead-end)
- iOS event instrumentation gap (submit happens but not tracked)
- WKWebView/session/upload issues inside Bridge flow

Reference: `analysis/ios-android-ux-gap.md`

### 3.5 Structural root cause D — web→app handoff leak (and it contaminates attribution)

What we see:
- Web/none sign-ups are ~**62.5%** of sign-ups.
- But web produces near-zero downstream events (tiny deposits/withdrawals).

This produces two harms at once:
- Conversion harm (wasted sign-up volume)
- Measurement harm (paid looks like “organic/(none)”)

Reference: `analysis/web-to-app-handoff.md`

---

## 4) Budget efficiency (best/worst channels)

Important framing:
- Use **Sheets downstream proxies** (virt_acc / new_active) for budget efficiency ranking because spend and outcomes are aligned there.
- Use AppsFlyer/Amplitude source buckets mainly for quality red flags (e.g., “installs with zero downstream”).

### 4.1 Best channels (activation efficiency; cost per new_active)

Top tier (scale once funnel + measurement basics are stable):
- **Google Pmax**: cost/new_active ≈ **$19.18**
- **Apple Search Ads (ASA)**: cost/new_active ≈ **$22.66**
- **Google Search**: cost/new_active ≈ **$25.48**

References: `analysis/channel-cac.md`, `analysis/budget-efficiency.md`

### 4.2 Worst channels (budget waste)

Must-pause / keep paused:
- **Appnext**: Sheets new_active = 0 → cost/new_active ≈ **$893**; attribution week shows 273 installs → 1 withdrawal (classic low-quality signature)
- **TikTok**: attribution week shows 49 installs → 0 withdrawals; Sheets cost/new_active ≈ $28.42 but quality signal is weak → do not scale until KYC/paid-active improves

Watchlist (do not scale based on last-click; fix measurement first):
- **Meta**: Sheets cost/new_active ≈ **$82.21** and attribution is heavily missing; true performance is unknowable until web→app + property propagation are repaired.

Reference: `analysis/budget-efficiency.md`

### 4.3 Immediate reallocation (weekly)

Free up:
- Appnext ($446.5/wk) + TikTok ($341.0/wk) ≈ **$787.5/wk**

Suggested move:
- +$500/wk → Google Pmax
- +$200/wk → Google Search
- +$87.5/wk → Apple Search Ads

Reference: `analysis/budget-efficiency.md`

---

## 5) Attribution reality ("(none)" share + correction factor) + fix plan

### 5.1 Current reality: attribution is missing for most downstream conversions

From the attribution export (Mar 14–20):
- Sign-ups: **~81.8%** are “(none)” (986 / 1,206)
- Withdrawals: **~60.9%** are “(none)” (1,355 / 2,226)

This is why strict last-click makes channels (especially Meta/Web2App) look much worse than they likely are.

Reference: `analysis/attribution-reconciliation.md`

### 5.2 Stop‑gap decisioning: apply a correction factor (until fixed)

Modeled paid‑influenced sign-ups (base case) imply:
- Paid sign-up undercount factor ≈ **6.9×** (sensitivity roughly **5.2× to 8.5×**)

Operating rule until instrumentation is repaired:
- Report both:
  - last-click paid sign-ups (audit trail)
  - modeled paid‑influenced range (decision support)

Reference: `analysis/attribution-reconciliation.md`

### 5.3 Fix plan: make web→app and downstream attribution “stick”

Implementation blueprint (do these in order):

1) **AppsFlyer OneLink everywhere on web CTAs**
   - Replace direct store links with OneLink short links

2) **Deferred deep linking configured and verified**
   - App reads conversion payload on first open
   - App persists first-touch acquisition fields

3) **Server-side persistence bridge**
   - Create a `web_session_id`
   - Store UTMs + click IDs first-party
   - Pass `web_session_id` through OneLink (e.g., `af_sub1`)
   - Join `web_session_id` ↔ user_id at sign-up

4) **Propagate acquisition properties into Amplitude**
   - Set user properties once (first-touch)
   - Attach to key events (signup, KYC submit, virt_acc/new_active, deposit/withdraw)

Success KPI:
- % sign-ups with non-null media_source/campaign should rise from ~18% to **>70%**

Reference: `analysis/web-to-app-handoff.md`

---

## 6) Market strategy

### 6.1 Turkey: 90-day plan (scale intent, protect throughput)

Turkey is the current “benchmark market” because it’s the only end-to-end functioning funnel.

TR 90-day priorities:
- Scale intent channels (Google Pmax + Search + ASA)
- Keep Meta primarily RTGT (until attribution is repaired)
- Pair spend scaling with conversion action audit + LP CTA improvements

Targets (directional; must be tracked with blended measurement):
- Grow weekly new actives while reducing blended CAC per new active
- Increase TR KYC submits (preferably D7-from-install cohort)

Reference: `analysis/turkey-90d-plan.md`

### 6.2 NG/EG/PK: gates + expansion playbook

Non-negotiable gates before scaling any non-TR market:
- **KYC Submit > 0** (and ideally KYC Approved > 0) in last 7 days
- Tracking standard parity (OneLink + naming + event properties)
- Budget ramp in phases (2K → 4K → 6K/month) only after 2 weeks of passing gates

Market-specific strategy:
- Nigeria: high potential, currently blocked; post-fix start with Google Search (lower fraud risk) and add Meta later
- Egypt: requires Arabic + RTL; start Meta Web2App once KYC works, add Google Search in phase 2
- Pakistan: pre-launch; use waitlist/CRM, confirm KYC doc support before meaningful spend

Reference: `analysis/multi-market-expansion-playbook.md`

---

## 7) Automation system (cron scripts + data quality monitor + weekly actions)

The system exists to make this sprint sustainable: weekly KPI pull, anomaly alerts, campaign health sweeps, and a weekly actions list.

### 7.1 Cron pipeline (recommended Monday schedule)

- 09:00 TRT — KPI pull + Cortex data refresh
  - `scripts/weekly_kpi_cron.sh`
  - writes/updates: `projects/cenoa-cortex/data.json`

- 09:00 TRT — anomaly detection + alert
  - `scripts/anomaly_alert_cron.sh`
  - writes: `projects/cenoa-performance-marketing/data/anomalies.json`

- 09:05 TRT — dead campaign sweep + alert
  - `scripts/dead_campaign_sweep_cron.sh`
  - writes: `projects/cenoa-performance-marketing/data/campaign-health.json`

- 10:00 TRT — weekly report + top actions
  - `scripts/weekly_report_cron.sh`
  - runs `scripts/weekly_actions.py`
  - saves: `data/weekly-report-latest.md`, `data/weekly-actions.json`

Reference: `analysis/automation-setup.md`

### 7.2 Data quality monitoring (stop flying blind)

Current critical failures to keep front-and-center:
- Signup events missing country/platform at extreme rates ("(none)" share > 60%)
- Organic installs share suspiciously high given paid spend (paid→organic loss)
- BigQuery daily table coverage incomplete

Reference: `analysis/data-quality-monitoring.md`

---

## 8) Top 15 actions (prioritized)

P0 = unblock growth now. P1 = increase ROI/decision quality. P2 = scale + systematize.

### P0 — this week

1) **Fix NG/EG: Pre‑KYC approved → BridgeXYZ shown handoff** (must produce Bridge “shown” > 0)
   - Reference: `analysis/pre-kyc-survey-investigation.md`

2) **Tune or bypass the Pre‑KYC AI survey threshold in NG/EG**
   - Target approval rate: move toward **≥50–60%** while monitoring fraud

3) **iOS KYC submit debugging + fix (or instrumentation parity fix)**
   - Target: iOS shown→submit moves toward Android levels
   - Reference: `analysis/ios-android-ux-gap.md`

4) **Web→app handoff: replace all store links with AppsFlyer OneLink**
   - This is the highest leverage “tracking + conversion” fix
   - Reference: `analysis/web-to-app-handoff.md`

5) **Pause/keep paused Appnext; pause TikTok until quality gate improves**
   - Reference: `analysis/budget-efficiency.md`

6) **Reallocate ~$787.5/wk into Pmax + Search + ASA**
   - Reference: `analysis/budget-efficiency.md`

### P1 — next 2–3 weeks

7) **Instrument provider-agnostic KYC step events + error telemetry**
   - Add `kyc_error_type`, `kyc_provider_response`, `kyc_step`, `submit_attempted/success/failed`

8) **Repair attribution propagation into downstream events** (Amplitude user + event properties)
   - Target: signups with non-null media_source >70%

9) **Build a canonical fact table** (month × country × channel × spend × key outcomes)
   - Resolves “virt_acc/new_active” definition drift between sheets
   - Reference: `analysis/cac-crosscheck.md`, `analysis/attribution-reconciliation.md`

10) **TR: conversion action audit in Google + LP CTA improvements**
   - Ensure app campaigns optimize to app events, not web visits
   - Reference: `analysis/turkey-90d-plan.md`

11) **Roll out KYC follow-up messaging (proven in EG tests)**
   - Reference: `analysis/funnel-summary.md` (proven lever callout)

### P2 — 30–90 days

12) **NG/EG relaunch with hard gates + phased budgets**
   - Reference: `analysis/multi-market-expansion-playbook.md`

13) **TR: creative operating system (3 new concepts/week) + fatigue controls**
   - Reference: `analysis/turkey-90d-plan.md`

14) **Weekly operations OS**
   - Use weekly report + anomalies + campaign health sweep as the ritual
   - Reference: `analysis/automation-setup.md`

15) **Replace parameterized LTV with observed revenue + cohort retention**
   - Pull withdrawal volumes and margins; compute real D30/D60 gross margin and LTV/CAC
   - Reference: `analysis/ltv-model.md`, `analysis/ltv-cac-ratio.md`

---

## 9) Appendix — the most important docs (links)

Funnel + KYC (read first):
- `analysis/funnel-summary.md`
- `analysis/global-funnel.md`
- `analysis/kyc-dropout-deepdive.md`
- `analysis/pre-kyc-survey-investigation.md`
- `analysis/ios-android-ux-gap.md`
- `analysis/web-to-app-handoff.md`

Attribution + measurement:
- `analysis/attribution-funnel.md`
- `analysis/attribution-reconciliation.md`
- `analysis/attribution-comparison.md`
- `analysis/data-quality-monitoring.md`

Budget + unit economics:
- `analysis/budget-efficiency.md`
- `analysis/channel-cac.md`
- `analysis/blended-cac.md`
- `analysis/unit-economics-brief.md`
- `analysis/ltv-model.md`
- `analysis/ltv-cac-ratio.md`

Market plans:
- `analysis/turkey-90d-plan.md`
- `analysis/nigeria-growth-plan.md`
- `analysis/egypt-scaling-plan.md`
- `analysis/pakistan-prelaunch-plan.md`
- `analysis/multi-market-expansion-playbook.md`

Automation / operating system:
- `analysis/automation-setup.md`
- `analysis/perf-marketing-team-os.md`
- `scripts/weekly_kpi_cron.sh`
- `scripts/anomaly_alert_cron.sh`
- `scripts/dead_campaign_sweep_cron.sh`
- `scripts/weekly_report_cron.sh`
- `scripts/data_quality_monitor.py`

---

Endnotes / constraints recap:
- Most “KYC counts” and platform comparisons are event totals, not unique users. Where it matters (KYC submit, Bridge shown), the directional conclusions still hold.
- Withdrawals/deposits are cohort-mixed; do not treat weekly withdrawals as “new user ROI.”
- Until OneLink + downstream property propagation is fixed, treat strict last-click CAC as a **lower bound**, and use blended metrics + controlled tests for budget decisions.
