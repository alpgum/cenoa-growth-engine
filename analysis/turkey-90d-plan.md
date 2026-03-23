# Turkey Market Deepening — 90-Day Performance Plan (TR)

**Sprint:** [096]  
**Date:** 2026-03-21  
**Owner:** Performance Marketing / Growth  
**Scope:** Turkey acquisition + activation deepening (scale what already works; protect KYC engine)

## Why Turkey (context recap)
Turkey is currently the **only market with a functioning end-to-end funnel** and is the dominant driver of KYC, deposits, and withdrawals.

Baseline (Mar 14–20, 2026):
- **Installs (TR):** 670 (46% of global)
- **KYC submits (TR):** 170 (**95% of global**)
- **KYC started → submit (TR):** 11.1% (≈2× global)

Sources: `analysis/turkey-funnel.md`

---

## 1) 90-day objective + north-star metrics

### 90-day objective
**Grow Turkey net-new actives while keeping CAC disciplined, and increase “quality throughput” via KYC submits.**

This plan assumes:
- We **prioritize intent channels** (Google + ASA) as the scaling engine.
- **Meta runs RTGT only** (per budget reallocation) to harvest warm demand and reduce leakage.
- We pair spend scaling with **conversion action + LP/CTA audit** to avoid paying for misattributed/low-quality outcomes.

### North-star metrics (tracked weekly)
**Primary (the 3 that matter):**
1) **New Actives (TR)**  
   - Definition: “new_active” proxy from Sheets / Amplitude cohort (new users reaching activation threshold)  
2) **Blended CAC per New Active (TR)**  
   - Definition: TR paid spend ÷ TR new_actives (triangulate with Sheets + AppsFlyer)  
3) **KYC Submits (TR, new-user cohort)**  
   - Definition: count of `KYC Submit` within **D7 of install** (to de-noise existing users)

**Supporting (diagnostics):**
- Install → Signup rate (TR) (note: country attribution gap exists)
- KYC started → submit rate (TR)
- LP CTA click rate (GA4) and app-store redirect rate
- Store conversion rate (ASA: tap → install; Google: click → install)

### Baseline → targets (90 days)
Directional baseline values pulled from: `analysis/channel-cac.md`, `analysis/meta-budget-reallocation.md`, `analysis/turkey-funnel.md`.

| Metric | Baseline (proxy) | Day 30 target | Day 60 target | Day 90 target |
|---|---:|---:|---:|---:|
| **New actives / week (TR)** | ~130/wk | **~190/wk** | **~220/wk** | **~250/wk** |
| **Blended CAC / new active (TR)** | ~$20–$21 | **≤ $18** | **≤ $16** | **≤ $15** |
| **KYC submits / week (TR, D7 cohort)** | ~170/wk (raw) | **200/wk** | **230/wk** | **260/wk** |

**Important:** Attribution is currently leaky (large “(none)” bucket). These targets must be evaluated with a **blended view** (AppsFlyer + Amplitude + Sheets), not single-source ROAS.

---

## 2) Channel plan (Google, ASA, Meta RTGT-only)

### A) Google Ads (Pmax + Search + Brand)
Guiding principle: **scale what already has the best cost/new_active**, but keep a hard budget discipline + correct conversion actions.

**From Channel CAC:**
- Pmax cost/new_active ≈ **$19.18**
- Google Search cost/new_active ≈ **$25.48**

Sources: `analysis/channel-cac.md`

#### Campaign architecture (TR)
1) **Pmax TR (scale lever)**
   - Goal: efficient acquisition at volume
   - Bid strategy: **Maximize Conversions** (no target initially)
   - Primary conversion: `af_app_install` / `first_open`
   - Budget: phase up (see weekly budget plan)

2) **Search — Brand (protect + cap CPC inflation)**
   - Bid strategy: **tCPA**
   - Suggested tCPA: **₺500 (~$14)** with fallback to ₺700 if brand IS drops <90%
   - Primary conversion: `af_app_install`

3) **Search — Generic / Freelancer (incremental intent)**
   - Split into separate campaigns so bid + budgets can be controlled independently
   - Bid strategy: start Max Conversions → move to **tCPA** once ≥30 conversions/month
   - Primary conversion: `af_app_install` (option: move to KYC_start if enough volume)

4) **Competitor search (monitoring only)**
   - Keep minimal budget; use Manual CPC cap or aggressive tCPA
   - Kill if 0 installs for 30 days

**Bid strategy + conversion action checklist:**
- Audit that app campaigns optimize to **app install**, not web visits.
- Keep KYC_start / virtual_account_created as secondary (observation).

Source: `analysis/bid-strategy-reco.md`

---

### B) Apple Search Ads (ASA)
Role: **highest-intent anchor** and quality floor.

**From Channel CAC:** ASA shows strong intent with competitive cost/new_active (~$22.66) and very strong downstream signals.

Focus areas (TR):
- **Brand exact** (defend + harvest)
- **Competitor** (Wise / Papara / Payoneer keyword sets)
- **Generic** (get paid in USD, international payments, US bank account, IBAN, freelancer payments)

Execution:
- Expand keyword coverage weekly; isolate match types.
- Keep CPT/CPA ceilings by ad group.
- Align Product Page (screenshots + copy) with top creative angles (see creative plan).

---

### C) Meta Ads — RTGT only (per reallocation)
Role: **harvest warm demand** + recover drop-offs from web/app flows.

Rules:
- **RTGT only** (pause non-RTGT prospecting per reallocation plan).
- Audience: 7/14/30-day website visitors, engaged social, app engagers; exclude recent installers/active users.
- Optimize for app install (or downstream event only if volume allows).
- Enforce frequency caps + creative rotation to avoid fatigue.

Source: `analysis/meta-budget-reallocation.md`

---

## 3) Creative plan (cadence + angles vs Papara/Wise)

### Creative operating system (12 weeks)
- **Cadence:** ship **3 new concepts/week** (minimum) across Google assets, ASA screenshots, Meta RTGT creatives.
- **Format mix:**
  - Static (benefit + proof)
  - UGC-style short video (15–25s)
  - Comparison cards (fees saved vs Papara/Wise/Payoneer)
  - Screenshot-first (product clarity) for RTGT
- **Refresh rule:** if CTR drops >25% WoW or frequency >6 (RTGT), rotate.

### Winning angles to test (Turkey)
1) **“Global payments” vs local wallets (Papara)**
   - Claim: Papara is great locally; **Cenoa is for getting paid internationally** (US/EU account details, clients abroad).
   - Hook ideas:
     - “Client wants USD/EUR? Give them US bank details in 3 minutes.”
     - “Stop losing money to ‘receiving fees’.”

2) **“Real savings” vs Wise**
   - Emphasize concrete fee/FX savings + speed.
   - Hook ideas:
     - “Wise is good. But if you’re getting paid often, the fees add up. Here’s the difference.”
     - “Keep more of every invoice.”

3) **“10× cheaper than Payoneer” (use selectively)**
   - Keep as one lane (works for comparison intent) but do not make all messaging competitor-first.

4) **Trust + legitimacy (fintech anxiety)**
   - Lead Bank / Stripe / USDC (Circle) trust stack, but ensure legal wording is approved.
   - Hook: “Your money held with trusted partners — withdraw anytime.”

5) **Jobs-to-be-done: TR freelancer + e-commerce exporter**
   - “Get paid from Upwork / Shopify / Etsy / clients abroad” (only where compliant and accurate).

### Weekly creative checklist
- [ ] 1× Papara contrast concept
- [ ] 1× Wise savings concept
- [ ] 1× Trust + proof concept
- [ ] 1× Product clarity concept (screens)
- [ ] RTGT: 2 variants of “finish setup / complete KYC” nudges

---

## 4) Landing page + conversion action audit plan

### A) Landing page (LP) action plan (TR)
Goal: lift **CTA click rate** and reduce bounce, especially for paid traffic.

Current baseline (site-wide):
- CTA click rate: **14.72%**
- Bounce rate: **60.99%**

Source: `analysis/lp-cta-optimization.md`

**Plan (Weeks 1–6):**
1) **P0 — Speed + Core Web Vitals audit** (Week 1)
2) **P1 — Single, unmissable CTA button above fold** (Week 1–2)
   - Replace “choose-your-store” friction with **one CTA** → smart route to store
3) **P1 — Headline test (benefit-first vs comparison-first)** (Week 1–2)
4) **P2 — Trust row above fold** (Week 2–3)
5) **P2 — Social proof upgrade** (Week 2–3)

**TR-specific LP idea:** create a lightweight TR page focused on:
- “Get paid internationally”
- “US/EU account in minutes”
- “Save fees vs Wise/Payoneer”
- single CTA

### B) Conversion action audit (must-do before scaling)
Goal: ensure each channel is optimizing to the correct event and we aren’t paying for “web clicks that never become installs.”

Checklist (Week 1):
- [ ] Google Ads: confirm campaigns optimize to **`af_app_install` / `first_open`** (primary)
- [ ] Remove/disable web visit conversions as primary on app campaigns
- [ ] AppsFlyer: validate deep link routing and W2A attribution
- [ ] GA4: event mapping for `cta_click` → `app_store_redirect`

Source: `analysis/bid-strategy-reco.md`

---

## 5) Budget plan (weekly) + overspend caps

### Principles
- Scale budgets in **≤20% steps** to avoid resetting learning.
- Hard **weekly caps** with daily budgets = weekly/7.
- Reallocate only from underperformers → top 2 performers (Pmax, ASA).

### Weekly caps by channel (TR)
Numbers are built off existing recommendations and Meta reallocation logic; adjust after Week 2 measurement.

| Channel | Week 1–2 (stabilize + audit) | Week 3–6 (scale intent) | Week 7–12 (optimize + expand) |
|---|---:|---:|---:|
| **Google Pmax (TR)** | $1,200/wk | $1,500/wk | $1,700/wk (cap) |
| **Google Search (TR total)** | $1,030/wk (brand) + $300 (generic) | $1,200/wk | $1,300/wk |
| **Google UAC Android (TR)** | $1,400/wk (hold) | $1,400/wk | $1,500/wk (only if CPA stable) |
| **ASA (TR)** | $1,200/wk | $1,400/wk | $1,500/wk |
| **Meta RTGT (TR)** | $600/wk | $600/wk | $700/wk (only if quality holds) |
| **Referral incentives (TR)** | $250/wk | $250/wk | $300/wk |
| **Total (cap)** | **~$4,980/wk** | **~$5,750/wk** | **~$7,000/wk** |

### Overspend guardrails (non-negotiable)
- **Budget pacing:** if any channel spends **>120% of weekly cap** by Thu EOD → cut daily budgets immediately.
- **CPA tripwire:** if cost/new_active > **1.5× target** for **3 consecutive days** → pause that campaign group and investigate.
- **Learning period rule:** don’t change bid strategy + conversion action in separate weeks; batch changes.

---

## 6) Risks + guardrails (incl. attribution caveat)

### Key risks
1) **Attribution leakage (“(none)” dominates downstream)**
   - Risk: we under-credit channels (especially Meta/W2A) and misallocate.
   - Mitigation: use **blended reporting** (AppsFlyer + Amplitude + Sheets) and cohort-based KYC submits (D7).

2) **Diminishing returns (Pmax/ASA saturation)**
   - Risk: CPA rises as we scale.
   - Mitigation: scale in 20% steps; set hard caps; expand keyword sets and creative breadth.

3) **Meta halo effect on organic**
   - Risk: cutting prospecting reduces top-of-funnel awareness.
   - Mitigation: keep RTGT as signal; watch organic installs weekly; if organic drops >20% for 2 weeks, reconsider a small TOF test.

4) **Creative fatigue in RTGT**
   - Risk: frequency spikes; CTR and CVR drop.
   - Mitigation: strict refresh cadence; cap frequency; rotate offers/angles.

5) **KYC throughput constraints / UX friction**
   - Risk: scaling installs doesn’t convert if KYC stalls.
   - Mitigation: weekly KYC funnel review; prioritize KYC micro-fixes when drop-off rises.

### Guardrail dashboard (weekly)
- Spend vs caps (by channel)
- New actives/wk + blended CAC
- KYC submits (D7 cohort) and KYC started → submit rate
- Install → signup rate (watch for tracking shifts)
- Meta RTGT: frequency, CTR, cost/quality

---

## 90-day execution calendar (high level)

### Weeks 1–2: Stabilize + measurement
- Pause Meta prospecting (keep RTGT only) per reallocation.
- Conversion action audit (Google + AppsFlyer + GA4).
- Launch LP P0/P1 tests (speed + single CTA + headline).

### Weeks 3–6: Scale intent channels
- Increase Pmax + ASA budgets stepwise.
- Expand ASA keywords (brand → competitor → generic).
- Search: enforce tCPA brand; split out generic campaigns.
- Ship 3 new creative concepts/week.

### Weeks 7–12: Optimize + compound
- Promote winning LP variant; add trust + social proof above fold.
- Expand creative into 2–3 repeatable “series” (Papara, Wise, trust).
- Consider selective budget lift on UAC only if CPA stable.
- Keep RTGT healthy; widen warm audiences if quality holds.

---

## References (inputs used)
- `analysis/turkey-funnel.md`
- `analysis/channel-cac.md`
- `analysis/bid-strategy-reco.md`
- `analysis/meta-budget-reallocation.md`
- `analysis/lp-cta-optimization.md`
- `analysis/referral-scaling-plan.md`
