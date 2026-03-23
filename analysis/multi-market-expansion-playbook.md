# Multi-Market Expansion Playbook (TR, NG, EG, PK)

**Created:** 2026-03-21  
**Owner:** Performance Marketing  
**Scope:** A repeatable, guardrail-driven way to launch + scale acquisition across multiple countries without burning budget into broken funnels.

---

## 0) The non-negotiables (applies to every market)

1) **No scaling without a working funnel.**
   - **Hard gate:** `KYC Submit > 0` (and preferably `KYC Approved > 0`) in the last 7 days.
2) **One tracking standard everywhere.**
   - Same **AppsFlyer OneLink**, UTM schema, campaign naming, and event properties.
3) **Budgets scale in phases, not vibes.**
   - $2K → $4K → $6K is the default ramp template.
4) **A market must earn the right to scale.**
   - Weekly gates: tracking health, KYC throughput, withdrawal success, CAC efficiency, and LTV/CAC.

---

## 1) KPI definitions (so we don’t argue later)

Use these consistently in dashboards, post-mortems, and gates:

- **CPI:** Spend / installs
- **$/Signup:** Spend / signups
- **KYC Start → Submit rate:** KYC submits / KYC starts
- **KYC Approval rate:** KYC approved / KYC submits
- **Cost/VirtAcc (paid):** Spend / paid-attributed virtual account creations (as in Sheets)
- **Cost/Paid Active (paid):** Spend / paid-attributed “paid_active” (as in Sheets)
- **Withdrawal success rate:** Successful withdrawals / withdrawal attempts *(if only “withdrawals” exists, treat as proxy and upgrade instrumentation)*
- **LTV/CAC:** (D30 or D60 gross margin / contribution) / CAC (pick one CAC definition and stick to it)

> Recommendation: pick **one “CAC”** for gates (usually **Cost/KYC Approved** or **Cost/First Deposit**) and compute it per market once KYC is functional.

---

## 2) Entry checklist per market (KYC readiness, localization, channel mix, CAC targets)

### 2.1 Turkey (TR) — “Benchmark / stable market”

**KYC readiness (must be true):**
- [ ] KYC submit + approval events firing (TR is the current baseline)
- [ ] KYC start → submit rate monitored weekly
- [ ] Withdrawal flows stable; customer support confirms no systemic failures

**Localization (P0):**
- Language: **Turkish**
- [ ] TR-specific LP copy (trust, fees, local transfer rails)
- [ ] App store assets localized (screenshots + description)

**Channel mix (default):**
- **Google Search / PMax** (high intent)
- **Apple Search Ads (ASA)** (category + competitor)
- **Meta**: primarily retargeting + selective prospecting tests

**CAC targets (starting targets; update after 2 weeks of current data):**
- **Cost/VirtAcc (paid): ≤ $40** *(baseline observed ~ $35 in Mar 9–15)*
- **Cost/Paid Active (paid): ≤ $900** *(baseline observed ~ $864 in Mar 9–15; definition-dependent)*
- Tripwire: if key CAC metric is **>1.5× target for 3 consecutive days**, pause the campaign group and diagnose.

---

### 2.2 Nigeria (NG) — “High potential / low CPI, currently funnel-blocked”

**KYC readiness (hard gate):**
- [ ] **KYC Submit > 0** in last 7 days *(currently 0 in recent weeks)*
- [ ] Pre-KYC survey approval rate tuned (target **≥60% approval**)
- [ ] KYC provider supports NG docs (e.g., NIN/BVN/passport) and the handoff renders correctly

**Localization (P0):**
- Language: **English** (Pidgin optional later)
- [ ] NG value props emphasize **USD access + transfers + reliability**
- [ ] Clear NG document guidance (what’s accepted, expected time)

**Channel mix (post-fix default):**
- **Google Search** first (intent capture; lower fraud risk)
- **Meta** only after funnel is proven (start with retargeting, then small prospecting)

**CAC targets (based on Mar 9–15 efficiency; only valid once KYC works):**
- **CPI:** ≤ $1.00 (Phase 1), ≤ $1.50 (Phase 2), ≤ $2.00 (Phase 3)
- **Cost/VirtAcc (paid): ≤ $5** *(baseline observed ~ $2)*
- **Cost/Paid Active (paid): ≤ $25** *(baseline observed ~ $16)*

**Kill rule (pre-fix):**
- If paid spend is running and **KYC Submit remains 0 after 14 days** → **pause all acquisition** (keep only minimal tracking validation spend).

---

### 2.3 Egypt (EG) — “Efficiency market, currently funnel-blocked + Arabic requirement”

**KYC readiness (hard gate):**
- [ ] **KYC Submit > 0** for **2 consecutive weeks**
- [ ] Pre-KYC survey approval rate improved (target **≥50% approval**)
- [ ] Bridgexyz (or provider) KYC component is actually shown to approved users

**Localization (P0/P1):**
- Language: **Arabic (RTL)**, English fallback acceptable short-term
- [ ] Arabic ad copy (Meta + Google), RTL-safe creatives
- [ ] Arabic LP (Architect LP localized) as **P1** once funnel works
- [ ] Arabic KYC follow-ups (push/email) because EG shows strong KYC intent

**Channel mix (post-fix default):**
- **Meta Web2App** primary (LP control + rapid creative iteration)
- Add **Google Search** in Phase 2 (Arabic keyword set)

**CAC targets (starting targets; update after 2 weeks post-fix):**
- **Cost/VirtAcc (paid): ≤ $12** *(baseline observed ~ $8 in Mar 9–15)*
- **Cost/Paid Active (paid): ≤ $80** *(baseline observed ~ $64 in Mar 9–15)*

**Kill rule:**
- If EG spend > $500/week and **KYC Submit = 0** → **pause** until fixed (this market burns quietly because top-of-funnel looks “good”).

---

### 2.4 Pakistan (PK) — “Pre-launch + waitlist leverage, KYC blocked”

**KYC readiness (hard gate):**
- [ ] Confirm provider supports PK documents (CNIC/NICOP/passport)
- [ ] Verify whether the pre-KYC survey/handoff issue also blocks PK
- [ ] **KYC Submit > 0** before any meaningful scaling

**Localization (P0):**
- Language: **English-first**, **Urdu ads** (expand later)
- [ ] App store listing: English + Urdu (P0)
- [ ] LP: English with optional Urdu toggle (P1)

**Channel mix (Phase 1):**
- **Waitlist → install** (CRM/email/push is the highest ROI lever)
- **Google Search** (English + Urdu ad copy)
- **ASA** (category + competitor)

**CAC targets (from PK pre-launch plan; directional until data exists):**
- **CPI (Google): < $3.00** (kill if > $5.00)
- **CPI (ASA): < $2.50** (kill if > $4.00)
- **KYC Submit:** must be **> 0 within 2 weeks** of paid tests, otherwise pause

---

## 3) Scaling gates (when a market earns the next budget phase)

Use these gates **per market**. Default rule: require gates to be met for **2 consecutive weeks** to ramp.

### Gate A — Tracking + attribution health
- [ ] AppsFlyer installs match channel platforms within acceptable variance (e.g., ±15%)
- [ ] OneLink deep links resolve correctly (web → app store/app)
- [ ] Events contain required properties (country, channel, campaign identifiers)

### Gate B — KYC throughput (hard)
- [ ] **KYC Submit > 0** (minimum)
- [ ] Target: **KYC Start → Submit ≥ 40%** once stable *(tune per market)*
- [ ] Target: **KYC Approval > 0** and approval rate not collapsing week-over-week

### Gate C — Money movement reliability (protect against “broken product” growth)
- [ ] **Withdrawal success rate ≥ 95%** *(or ≥90% if infrastructure is still stabilizing, but then do NOT scale aggressively)*
- [ ] Withdrawal time-to-complete within acceptable SLA (define with Ops/CS)

### Gate D — Unit economics
- [ ] Primary CAC metric at/under target (e.g., Cost/KYC Approved or Cost/First Deposit)
- [ ] **LTV/CAC ≥ 2.5** (early scale) and trending upward
- [ ] If LTV is not yet stable: require **payback ≤ 60–90 days** as proxy

### Gate E — Volume floor (avoid ramping on noise)
- [ ] Minimum weekly sample for decisions:
  - **≥200 installs/week** OR
  - **≥50 KYC submits/week** (better)

---

## 4) Budget phasing template ($2K → $4K → $6K)

### 4.1 Default phasing

| Phase | Monthly budget | Goal | Ramp condition (must hold 2 weeks) |
|---|---:|---|---|
| Phase 1 | $2,000 | Validate end-to-end funnel + baseline CAC | Gates A + B met; CAC within target band |
| Phase 2 | $4,000 | Add a second channel / expand audiences | Gates A–D met; no reliability regressions |
| Phase 3 | $6,000 | Scale winners + broaden reach | Stable CAC + KYC throughput; LTV/CAC ≥ 2.5 |

### 4.2 “When to ramp” rule of thumb
Ramp to the next phase **only when**:
- You have **at least 2 consecutive weeks** with:
  - KYC Submit > 0 (and not a one-off)
  - Withdrawal success rate above threshold
  - CAC at/under target (or improving)

### 4.3 Daily pacing guardrails
- Weekly cap = (monthly budget / 4)
- If by **Thu EOD** spend is **>120% of weekly cap** → reduce daily budgets immediately.
- Never increase budgets more than **+20–30% in a single day** (avoid resetting learning).

---

## 5) Localization requirements (language, LP, creatives, compliance)

### 5.1 Localization matrix

| Market | Language P0 | LP requirements | Creative requirements | Compliance / trust cues |
|---|---|---|---|---|
| TR | Turkish | TR LP variant; fast load; local trust | TR testimonials, local money movement, fees clarity | Consumer finance disclaimers; clear KYC steps |
| NG | English | NG doc guidance + “USD access” framing | Avoid overly “get rich” crypto framing; emphasize reliability | Explicit KYC eligibility + document list |
| EG | Arabic (RTL) | Arabic LP (P1); RTL layout; mobile-first | Arabic copy; culturally relevant visuals; Ramadan-ready | Avoid sensitive claims; strong security/trust blocks |
| PK | English + Urdu ads | English LP (P0), Urdu toggle (P1) | Urdu search ad copy; simple benefit-led creatives | Clear KYC doc eligibility; avoid prohibited claims |

### 5.2 Compliance checklist (every market)
- [ ] “No misleading financial promises” (returns, guaranteed profit, etc.)
- [ ] Clear fees disclosure (where required)
- [ ] Clear KYC requirements and supported documents
- [ ] Local sensitivity review (religious holidays, cultural norms)

---

## 6) Operational cadence (weekly reviews, anomaly checks, campaign health)

### Daily (15 minutes)
- Spend pacing vs caps (by channel)
- CPI / $/Signup / primary CAC metric (by market)
- Tracking sanity: sudden drops/spikes in installs, signups, KYC events

### Weekly (60–90 minutes, per market)
- Funnel review:
  - Install → Signup → KYC Start → KYC Submit → KYC Approved → First Deposit → Withdrawal success
- Creative health:
  - CTR, CVR, frequency, fatigue (esp. Meta)
- Channel health:
  - Search term quality, ASA keyword efficiency, Meta placement breakdown
- Decision log:
  - What changed last week, what we expect to happen, what we’ll do if it doesn’t

### Anomaly checks (must run before scaling)
- KYC Submit goes to **0** after being non-zero
- Withdrawal success rate drops below threshold
- Attribution shifts (e.g., sudden spike in “organic/(none)” or cross-channel mismatch)

---

## 7) Failure modes + kill switches (do not spend into a broken funnel)

### Failure mode A: Broken KYC (most common)
**Signals:** KYC starts exist, but KYC submit is 0 or collapses; approval rate tanks.
- **Kill switch:** If **KYC Submit = 0 for 7 days** in an active market → pause acquisition.
- **Exception:** Keep a tiny “tracking validation” campaign ($5–$20/day) to detect recovery.

### Failure mode B: Broken withdrawals / unreliable money movement
**Signals:** CS tickets spike; success rate below threshold; delays.
- **Kill switch:** If withdrawal success rate **<90%** for 48h → pause prospecting; keep only retargeting / brand defense.

### Failure mode C: Tracking drift (you’re flying blind)
**Signals:** Platform spend continues, but AppsFlyer installs/events drop, or OneLink breaks.
- **Kill switch:** If attribution mismatch persists **>24h** → freeze scaling; reduce budgets to minimum until fixed.

### Failure mode D: CAC inflation / diminishing returns
**Signals:** CAC rises >1.5× target; frequency climbs; CTR/CVR falls.
- **Kill switch:** Pause the worst-performing campaign/adset group; refresh creative; tighten targeting; revert last big change.

### Failure mode E: Bad unit economics
**Signals:** LTV/CAC < 1.5 after enough cohorts; payback > 120 days.
- **Kill switch:** Stop scaling; shift budget to the best-performing market; treat the market as “R&D only” until product/retention improves.

---

## 8) Keeping attribution consistent (OneLink + UTMs + event properties)

### 8.1 OneLink standard (Web → App)
- Use **one global AppsFlyer OneLink** with country/language routing parameters.
- For every landing page CTA/button, use the same deep link pattern.

**Minimum parameters to preserve:**
- `af_channel`
- `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`
- `pid` / `c` / `af_adset` / `af_ad` equivalents (depending on channel)
- `lp_variant` (critical for LP testing)

### 8.2 Canonical UTM schema (never deviate)
- `utm_source`: meta | google | asa | tiktok | influencer | crm
- `utm_medium`: paid_social | paid_search | app_store | email | push
- `utm_campaign`: `country_objective_theme_phase` (e.g., `eg_kyc_usdaccess_p1`)
- `utm_content`: `creativeConcept_format_hook_v#`
- `utm_term`: keyword (search) OR audience bucket (paid social)

### 8.3 Required event properties (analytics)
Every funnel event should include:
- `country` (TR/NG/EG/PK)
- `language`
- `channel` (normalized)
- `campaign_id`, `adset_id`, `ad_id` (when available)
- `creative_id` / `asset_id`
- `lp_variant`
- `kyc_provider`

### 8.4 Naming conventions (so reporting isn’t chaos)
- Campaign names must start with **country code**.
- Adset names must include **audience type** (prospecting/retargeting/lookalike).
- Creative names must include **concept + format + version**.

### 8.5 Reconciliation workflow (weekly)
- AppsFlyer vs platform spend/install deltas by channel
- Amplitude funnel counts vs AppsFlyer postbacks for key events
- Update a single source-of-truth table (BigQuery/Sheets) for:
  - market → channel → campaign → LP variant → primary CAC → KYC throughput

---

## Appendix A — Market quick-start summary

- **TR:** Use as baseline; keep scaling disciplined; focus on intent channels + LP/creative iteration.
- **NG:** Do not scale until KYC works; once fixed, it can be the lowest-cost growth engine.
- **EG:** Similar to NG but requires Arabic + RTL; post-fix it should be a strong efficiency market.
- **PK:** Pre-launch; leverage waitlist + Search/ASA; KYC submit is the gating event.

## References (existing docs)
- `analysis/country-cac.md` (TR/NG/EG benchmarks)
- `analysis/nigeria-growth-plan.md`
- `analysis/egypt-scaling-plan.md`
- `analysis/pakistan-prelaunch-plan.md`
- `analysis/turkey-90d-plan.md`


---

> ⚠️ **Attribution caveat:** Web campaigns (Meta/Google → cenoa.com → app store) may appear as "Organic" or "(none)" due to broken web→app attribution. Estimated correction factor: ~6.9×. See [attribution-reconciliation.md](attribution-reconciliation.md) for details.
