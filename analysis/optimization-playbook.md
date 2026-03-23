# Optimization Playbook (SOP)

**Project:** Cenoa Performance Marketing  
**Owner:** Growth / Performance  
**Last updated:** 2026-03-21  

This doc is the **operating system** for weekly optimization, budget reallocations, launches, and creative testing.

It consolidates learnings from:
- `analysis/meta-underperforming.md`
- `analysis/meta-budget-reallocation.md`
- `analysis/demand-gen-fix-plan.md`
- `analysis/bid-strategy-reco.md`
- `analysis/creative-scoring.md`
- `scripts/anomaly_detection.py` + `scripts/weekly_report.py` (weekly pulse)
- `analysis/channel-cac.md` + `analysis/budget-efficiency.md`

---

## 0) North Star + Rules of Engagement

### Optimize to downstream, not vanity
**Primary optimization KPI (portfolio):** **Cost / New Active** (Sheets) and/or **Cost / Paid Active**.  
**Secondary:** Cost / VirtAcc, KYC submit rate, install→signup, signup→KYC, KYC→VirtAcc, VirtAcc→New Active.

> **Never** scale a channel on CPI alone (Appnext is the canonical “cheap CPI trap”).

### Change management
- **One major change per lever per week** (budget / bid strategy / conversion action / creative). Avoid stacking changes that break attribution or reset learning.
- **Budget changes in 20% steps** (Google smart bidding + Meta learning stability). Larger changes often reset learning.

### Default guardrails (global)
- Any campaign with **meaningful spend and 0 tracked conversions** is treated as **broken until proven otherwise** (see Demand Gen case).
- Any channel with **high installs but near-zero downstream** is treated as **fraud / low-quality** until proven otherwise.

---

## 1) Definitions (so we don’t argue about metrics)

**Installs:** AppsFlyer attributed installs (or equivalent MMP).  
**Signups:** “Cenoa sign-up completed” (Amplitude).  
**KYC Submit:** “Bridgexyz KYC Component: Submit clicked” (Amplitude).  
**VirtAcc:** Virtual account opened (Sheets proxy; also track in-product event if available).  
**New Active:** Activation proxy in Sheets (aligned with spend; best weekly decision metric).  
**Withdrawals:** Withdrawal completed (Amplitude; can include older cohorts → not same-week CAC).  

**Important:** For weekly decisions, prefer **Sheets VirtAcc + New Active** because they’re aligned with spend tables; attribution exports often include older cohorts (withdrawals).

---

## 2) Weekly Optimization Checklist (Monday 09:00)

### 2.1 Run the Weekly Pulse (KPIs + anomalies)
**Goal:** detect structural breaks before we “optimize” the wrong thing.

**Inputs**
- `projects/cenoa-cortex/data.json` (weekly KPIs)
- `projects/cenoa-performance-marketing/data/weekly-report-latest.md`
- `projects/cenoa-performance-marketing/data/anomalies.json`

**Anomaly thresholds** (from `scripts/anomaly_detection.py`)
- `warning`: |Δ| ≥ 20%
- `critical`: |Δ| > 40%

**Checklist**
- [ ] Open the latest weekly pulse: `data/weekly-report-latest.md`
- [ ] Note week-over-week deltas for: installs, signups, KYC submit, withdrawals, DAU.
- [ ] Review anomalies and classify: measurement vs traffic vs product/funnel.
- [ ] If **KYC submit is 0 in a market** (e.g., NG/EG), treat it as a **hard blocker**: do not scale paid there until fixed.

### 2.2 Channel health scan (campaign-level)
**Goal:** catch “silent waste” (spend with no outcomes).

- [ ] For each channel: spend, installs, signups, VirtAcc, New Active (Sheets).
- [ ] Flag any campaign with:
  - [ ] spend > meaningful threshold (define per channel) **and** installs = 0
  - [ ] installs present but VirtAcc/New Active ~ 0
  - [ ] sudden CPA blowups (>1.5× last week) for 3+ days

**Known pattern:** Demand Gen retargeting can spend heavily while producing **0 tracked installs** if it’s optimizing to web clicks or re-engagement without install attribution.

### 2.3 Decide: STOP / HOLD / SCALE (portfolio)
Use `analysis/budget-efficiency.md` + `analysis/channel-cac.md` logic:

- **STOP / PAUSE**
  - Appnext: high installs, near-zero downstream → fraud/low-quality signature.
  - TikTok: installs with 0 withdrawals in attribution week; only keep if downstream improves.
  - Google Demand Gen retargeting: pause if installs=0 (see fix plan).
  - Meta TR Web2App prospecting: structural downstream failure (see Meta underperforming).

- **SCALE (primary levers)**
  - Google Pmax (best Cost/New Active)
  - Apple Search Ads (intent anchor; strong downstream)
  - Google Search (quality floor)

- **HOLD / CAP / TEST**
  - Meta: cap and treat as controlled experiment until attribution + downstream improves.
  - “Other” networks: keep only placements with verified VirtAcc/New Active.

### 2.4 Implement changes (with a changelog)
- [ ] Record changes in a weekly changelog (budget moves, creative swaps, bid strategy edits, conversion-action changes).
- [ ] Budget reallocation should be **budget-neutral** unless explicitly approved.

### 2.5 Mid-week check (Thu/Fri)
- [ ] Confirm changes took effect (spend pacing, conversion volume).
- [ ] Kill obvious losers early (e.g., broken tracking, CTR collapse, CPI spike).

---

## 3) Monthly Review Template (end of month)

> Copy/paste this section into a new monthly doc.

### 3.1 Budget pacing & mix
- Month: YYYY-MM
- Total performance spend vs plan: ____ / ____
- Spend share by channel (%): Meta __ / Google __ / ASA __ / Other __ / Referral __
- Spend share by geo (%): TR __ / NG __ / EG __ / Other __

### 3.2 Efficiency snapshot (downstream)
Use downstream metrics aligned to spend (Sheets).

| Channel | Spend | VirtAcc | New Active | Cost/VirtAcc | Cost/New Active | MoM trend | Decision |
|---|---:|---:|---:|---:|---:|---|---|
| Google Pmax | | | | | | | |
| Google Search | | | | | | | |
| Apple Search Ads | | | | | | | |
| Meta | | | | | | | |
| TikTok | | | | | | | |
| Appnext | | | | | | | |
| Other | | | | | | | |

### 3.3 Reallocation decisions (next month)
- Budget to cut (underperformers): ______________________________
- Budget to add (winners): ______________________________________
- Test budget reserve (% of total): ______ (recommended 5–10%)

**Rule:** reallocate from **DEAD/BLEEDING/FRAUD** to **HEALTHY** first (see Section 6).

### 3.4 Creative refresh plan
- TR: refresh cadence every 2–3 weeks
- NG/EG: refresh cadence every ~4 weeks (unless fatigue accelerates)

Checklist:
- [ ] Identify top 3 winning angles by market
- [ ] Identify fatigue risks (frequency, CTR decay, CPA creep)
- [ ] Build next month’s creative queue (min 15–20 TR, 10–12 NG, 10–12 EG)

### 3.5 Measurement + infra review
- [ ] Attribution gaps (unattributed “(none)” volumes)
- [ ] Web→app flows (deep links, OneLink, deferred deep links)
- [ ] Conversion action consistency across platforms
- [ ] Any “silent waste” campaigns (spend with no conversions)

---

## 4) Campaign Launch Checklist (measurement-first)

### 4.1 Conversion action audit (non-negotiable)
Before launch, verify:
- [ ] Primary conversion event is correct for the campaign type (install vs KYC_start etc.)
- [ ] “Primary” vs “Secondary/Observe” is configured correctly (avoid optimizing to web page views)
- [ ] Counting method is correct (e.g., installs counted as “One”)
- [ ] Pixel / SDK / MMP events are firing end-to-end

**Recommended defaults (from bid strategy reco):**
- App install campaigns (UAC/Meta App): primary = `af_app_install` / `first_open`
- Search generic (if enough volume): primary = `KYC_start`; else install
- Demand Gen (if used): must optimize to install + deep link; otherwise it becomes a click farm

### 4.2 UTMs + naming conventions
**UTM minimum:**
- `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term` (Search)

**Naming convention (suggested):**
`{COUNTRY}_{CHANNEL}_{OBJECTIVE}_{AUDIENCE}_{LANG}_{YYYYMMDD}`

Examples:
- `TR_Meta_AppInstall_Prospecting_TR_TR_20260321`
- `EG_Google_Search_Generic_AR_20260321`

### 4.3 Deep links & Web→App handoff
If the flow touches web at any point:
- [ ] Use AppsFlyer OneLink (or equivalent) with **deferred deep linking**
- [ ] Confirm user lands in the correct app screen post-install
- [ ] Confirm click IDs (fbclid, gclid) are preserved as much as possible
- [ ] Verify attribution window assumptions (click-through vs view-through)

### 4.4 Store / landing page alignment
- [ ] Message match: creative promise == landing/store headline
- [ ] Fast load, minimal steps
- [ ] App store page: screenshots + description aligned to the angle

### 4.5 Launch gates
- [ ] Budget cap set (avoid runaway spend)
- [ ] Tracking QA test conversions done (at least 1 real device)
- [ ] Monitoring plan: daily check for first 72 hours

---

## 5) Creative Testing SOP

### 5.1 The “3 variants” rule
Always run **3 creative variants simultaneously** per campaign/ad set.
- Variant A: control (best known performer)
- Variant B: iteration (same angle, new execution)
- Variant C: new angle (different hook)

### 5.2 Budget split (50/30/20)
- **50%** → proven winner (scale)
- **30%** → runner-up (maintain)
- **20%** → new test

### 5.3 Minimum data to judge (avoid noise)
Before killing for performance (except obvious broken cases), aim for:
- Impressions ≥ 5,000
- Clicks ≥ 50
- Installs ≥ 15
- Live time ≥ 3 days

### 5.4 Kill rules (fast + explicit)
Kill immediately if any are true:
- **CTR < 0.4%** after sufficient impressions (non-performing thumb stop)
- **CVR (click→install) < 4%** (creative/store mismatch)
- **CPA > 2× market benchmark** for 3+ days (waste)
- **Downstream is structurally dead** (installs but ~0 VirtAcc/New Active over a full week)

Weekly rotation rule (every Monday):
- Kill the lowest composite performer and replace with a new variant (keep 3 live).

### 5.5 Scoring (optional but recommended)
Use `analysis/creative-scoring.md` composite weights:
- CTR (15%)
- CVR click→install (20%)
- CPA (25%)
- Downstream quality (25%)
- Fatigue / decay (15%)

**Action matrix:**
- Score 8–10: scale + clone
- Score 6–7.9: maintain + iterate
- Score 4–5.9: on notice
- Score 2–3.9: kill within 7 days
- Score 1–1.9: kill immediately

---

## 6) Channel Evaluation Criteria (DEAD / BLEEDING / FRAUD / HEALTHY)

This is the shared language for decision-making.

### 6.1 HEALTHY ✅
**Definition:** efficient on downstream; scalable with controlled budget increases.

Signals:
- Stable or improving **Cost/New Active** vs last 2–4 weeks
- Reasonable install→signup and signup→KYC conversion
- No major attribution gaps specific to the channel

Default action:
- Scale budgets +20% weekly while maintaining CPA guardrails

### 6.2 BLEEDING 🩸
**Definition:** produces outcomes, but efficiency is deteriorating.

Signals:
- Cost/New Active trending worse for 2 consecutive weeks
- CPA spikes (>1.5×) for 5 consecutive days
- Creative fatigue (frequency up, CTR down, CPA up)

Default action:
- Cap spend, refresh creatives, adjust targeting, and/or tighten bid strategy
- Re-evaluate in 7 days

### 6.3 DEAD ☠️
**Definition:** structurally fails downstream or tracking is broken.

Signals:
- Spend + time but **0 installs** (or 0 primary conversion) → tracking/bidding misconfigured
- Installs exist but **near-zero VirtAcc/New Active** over 1–2 weeks

Canonical examples:
- Google Demand Gen retargeting showing **1,627 clicks and 0 installs** → pause + diagnose.
- Meta TR Web2App prospecting: high spend, terrible paid-active outcomes → structural web→app friction.

Default action:
- Pause immediately. Diagnose. Only relaunch with a clear measurement+conversion fix.

### 6.4 FRAUD / LOW-QUALITY 🚩
**Definition:** looks great on cheap CPI, fails completely downstream.

Signals:
- Very high installs with extremely low activation (VirtAcc/New Active/Withdrawals)
- Downstream rates inconsistent with organic + high-intent channels

Canonical example:
- Appnext: huge installs, near-zero New Active.

Default action:
- Pause 100% until proven otherwise.
- If re-tested, require strict downstream gates (Cost/New Active) before any scale.

---

## 7) Budget Reallocation SOP (weekly)

### 7.1 The method (simple, repeatable)
1. Rank channels by **Cost/New Active** (Sheets) and confidence.
2. Identify budget to cut from DEAD/BLEEDING/FRAUD.
3. Reallocate to the top 2–3 HEALTHY channels.
4. Implement in **20% increments** to protect algorithm learning.

### 7.2 Known decision from current learnings
From `meta-underperforming.md` + `meta-budget-reallocation.md`:
- **Pause / cut** Meta TR Web2App prospecting (keep RTGT capped if it shows real downstream)
- **Scale** Google Pmax + Apple Search Ads + Google Search

### 7.3 Revert protocol
If after reallocation:
- Total new actives/week drops below an agreed floor (e.g., < 100/wk) for 2 consecutive weeks,
  - partially revert (restore 50% of the cut budget),
  - and re-evaluate after another 2 weeks.

---

## 8) Bid Strategy SOP (Google-focused)

Use `analysis/bid-strategy-reco.md` as the source of truth. Core rules:
- **Pmax:** keep Maximize Conversions unless CPA drifts for 2+ weeks.
- **Search Brand / Generic:** use tCPA once you have conversion volume (30+/month).
- **Competitor low-volume:** manual CPC caps or very conservative tCPA.
- **Never** optimize app campaigns to web conversions.

Learning period rules:
- Don’t change bid strategy during “Learning” (7–14 days after edits).
- Don’t stack budget + conversion-action + bid-strategy changes in the same week.

---

## 9) Attribution Caveats (Web → App) + Mitigations

### 9.1 The problem
Web→App flows (Meta Web2App, landing page hops, app store handoffs) create **attribution leakage**:
- Click → web → store → install breaks identity chain
- Users switch browsers/apps; click IDs can be lost
- Post-install events happen outside optimization windows

Symptoms we’ve seen:
- Large downstream volumes falling into **“(none)” / unattributed** buckets
- Meta looking much worse than it might be due to missing linkage
- Web signups inflated (web form easier), but app activation weak

### 9.2 Mitigations (do these before trusting the numbers)
**Measurement fixes**
- Use AppsFlyer OneLink (or equivalent) with deferred deep linking
- Standardize UTMs and campaign naming across channels
- Ensure app installs + key in-app events are imported as conversion actions where needed

**Optimization fixes**
- Prefer **direct app install** objectives over Web2App when possible (fewer drop-offs)
- If running Web2App, treat it as an **upper-funnel experiment**, cap budget, and use longer evaluation windows

**Decision hygiene**
- When attribution is known-broken, base weekly budget moves on **aligned spend tables** (Sheets VirtAcc/New Active) + cohort sanity checks, not raw attribution exports.

---

## Appendix A — “Broken campaign” quick triage

If you see **spend + no conversions**:
1. Pause immediately.
2. Check conversion action assignment (is it optimizing to web visit?).
3. Check deep links / store flow / OneLink.
4. Check audience exclusions (retargeting may target existing installers).
5. Check invalid clicks/placements.

If you can’t explain the failure in 30 minutes → keep paused.


---

> ⚠️ **Attribution caveat:** Web campaigns (Meta/Google → cenoa.com → app store) may appear as "Organic" or "(none)" due to broken web→app attribution. Estimated correction factor: ~6.9×. See [attribution-reconciliation.md](attribution-reconciliation.md) for details.
