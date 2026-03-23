# Cross-channel attribution reconciliation (AppsFlyer × Amplitude × GA4 × Sheets)

**Generated:** 2026-03-21  
**Primary time window (attribution export):** 2026-03-14 → 2026-03-20 (7d)  
**Goal:** reconcile how much *paid* volume we should expect vs what we currently *observe* in last-click attribution, quantify the gap, and define how we make decisions until instrumentation is fixed.

**Inputs (existing docs / data):**
- `analysis/attribution-comparison.md`
- `analysis/channel-cac.md`
- `analysis/cac-crosscheck.md`
- `analysis/web-to-app-handoff.md`
- `data/attribution-breakdown-20260320.json` (Amplitude segmentation by AppsFlyer source)
- `data/sheets-budget-tracking.json` (realized spend + GA-based web paid/organic split note)

---

## 1) What each system is good for / bad for

### AppsFlyer (mobile attribution / install measurement)
**Good for**
- Install attribution (media source, campaign/adset/ad) when the click→install chain is intact.
- Deterministic mobile identifiers / install reattribution logic (within privacy limits).
- Auditable last-click records for UA performance.

**Bad for (in our current setup)**
- **Web → app** paths that use direct store links (or lose click params) will show as **Organic** at install time.
- Even when installs are attributed, **downstream events** (signup/withdrawal) can become **(none)** if the attribution payload isn’t propagated into the event pipeline.

### Amplitude (product events + segmentation)
**Good for**
- Canonical product event counts (sign-up completed, withdrawal completed, etc.).
- Funnel / cohort analysis and “truth” about what users did.
- Can segment events by AppsFlyer dimensions *if* those properties exist on the user/event.

**Bad for (in our current setup)**
- If acquisition properties are missing at signup time, Amplitude segmentation collapses into **(none)**.
- Doesn’t solve install attribution by itself; it depends on correct source properties being set.

### GA4 (web analytics)
**Good for**
- Web session attribution (UTMs/campaigns) and on-site behavior.
- Measuring **landing page performance** and **CTA clicks** (if instrumented), and estimating what share of web traffic is paid.
- Debugging the *pre-store* part of web2app.

**Bad for (in our current setup)**
- It cannot natively join a web session to a later mobile install/signup unless we implement a bridging mechanism (OneLink + deferred deep links + server-side persistence).
- Current GA4 deep-dive is **blocked** (see `analysis/ga4-web-traffic.md`: missing `GA4_PROPERTY_ID`).

### Sheets (Budget Tracking + CAC analysis exports)
**Good for**
- Closest-to-finance view of spend (realized cost) and planning.
- Operational “activation proxies” (virtAcc / new_active) used for weekly optimization.

**Bad for**
- Denominators are often not aligned with product analytics definitions (see `analysis/cac-crosscheck.md`: virtAcc/new_active mismatch across tabs).
- Can embed assumptions (e.g., GA-based paid share) that must be made explicit.

---

## 2) The hard fact: downstream attribution is missing for most conversions

From `data/attribution-breakdown-20260320.json` (Mar 14–20, 2026):

- **Sign-ups total (Amplitude event):** 1,206
  - **(none):** 986 (**81.8%**)
  - **Organic:** 77 (6.4%)
  - **Attributed paid buckets (sum of paid sources in the export):** 121 (10.0%)

- **Withdrawals total (Amplitude event):** 2,226
  - **(none):** 1,355 (**60.9%**)
  - **Organic:** 487 (21.9%)
  - **Attributed non-organic non-none:** 384 (17.2%)

Interpretation:
- For **sign-ups**, last-click attribution is effectively “missing” for ~82% of volume.
- For **withdrawals**, it is still missing for ~61% (and withdrawals are especially cohort-mixed, so don’t use them as a clean CAC denominator for the week).

---

## 3) Reconciliation: expected vs observed paid volume (sign-ups)

We need one reconciliation lens that combines:
- **Spend** (Sheets proxy)
- **Observed paid-attributed sign-ups** (AppsFlyer→Amplitude source view)
- **Unattributed sign-ups** as the “gap pool” we need to re-assign probabilistically until measurement is fixed

### 3.1 Observed (strict last-click) paid sign-ups
From `analysis/channel-cac.md` (week proxy spend + Mar 14–20 outcomes):
- **Paid spend proxy (weekly):** **$6,714**
- **Paid sign-ups credited in strict last-click source view:** **121**
- Implied **cost / paid-attributed signup:** **$55.5**

This is the *lower bound* view.

### 3.2 Modeled “paid-influenced” sign-ups (stop-gap, until web→app is fixed)

We treat the unattributed pool as “paid-influenced” at some share **p** (because web2app loses attribution), and we also allow some organic to be paid-influenced (brand/search/returning users).

**Base assumptions (aligned with `analysis/attribution-comparison.md`):**
- **p = 70%** of “(none)” sign-ups are paid-influenced
- **25%** of Organic sign-ups are paid-influenced

Then:
- Paid-influenced from “(none)” = 0.70 × 986 = **690.2**
- Paid-influenced from Organic = 0.25 × 77 = **19.3**
- Add observed paid-attributed sign-ups = **121**

➡️ **Estimated paid-influenced sign-ups (base): ~830**
- Implied **cost / paid-influenced signup:** $6,714 / 830 ≈ **$8.1**

### 3.3 Sensitivity + correction factor
Define a correction factor:

> **Paid sign-up correction factor = (estimated paid-influenced sign-ups) / (paid-attributed sign-ups in last-click)**

- **Low case:** p=50% → paid-influenced ≈ 633 → factor **5.2×**
- **Base case:** p=70% → paid-influenced ≈ 830 → factor **6.9×**
- **High case:** p=90% → paid-influenced ≈ 1,027 → factor **8.5×**

**Recommendation (until fixed):**
- Publish last-click paid sign-ups (121) **and** a modeled paid-influenced range (**633–1,027**) to prevent over-reacting to broken last-click.
- For *decisioning*, use the **base factor ~6.9×** as the default adjustment for “paid volume undercount” (revisit weekly as instrumentation improves).

---

## 4) Reconciliation table (bullets): channel expected vs observed paid sign-ups

This table answers: *“Given spend, how many paid sign-ups should we expect vs what we observe in last-click?”*

**Inputs**
- Observed sign-ups by paid bucket (from `analysis/channel-cac.md`, strict last-click):
  - Google Search: 7
  - Pmax: 7
  - Apple Search Ads (ASA): 22
  - Appnext: 24
  - TikTok: 8
  - Meta: 22
  - Other: 31
  - **Total observed paid:** 121
- Gap pool to redistribute (base case):
  - “(none)” paid-influenced: 690.2
  - Organic paid-influenced: 19.3
  - **Total gap pool:** 709.5
- Redistribution rule (from `analysis/attribution-comparison.md`):
  - Redistribute the gap pool across **web2app-leak-prone channels** proportional to spend share, excluding ASA + Appnext.
  - Channels used for redistribution: **Meta, TikTok, Google Search, Pmax, Other**.

### Base-case expected sign-ups (modeled)
- **Meta**
  - Spend: $2,754
  - Observed paid sign-ups: 22
  - Expected add-back from gap pool: ~345
  - **Expected paid-influenced sign-ups:** ~367  
  - Gap vs observed: **+345**

- **Google Search**
  - Spend: $790
  - Observed: 7
  - Expected add-back: ~99
  - **Expected:** ~106
  - Gap: **+99**

- **Pmax**
  - Spend: $805.5
  - Observed: 7
  - Expected add-back: ~101
  - **Expected:** ~108
  - Gap: **+101**

- **Other**
  - Spend: $976.5
  - Observed: 31
  - Expected add-back: ~122
  - **Expected:** ~153
  - Gap: **+122**

- **TikTok**
  - Spend: $341
  - Observed: 8
  - Expected add-back: ~43
  - **Expected:** ~51
  - Gap: **+43**

- **Apple Search Ads (ASA)** *(excluded from redistribution)*
  - Spend: $600.5
  - Observed: 22
  - **Expected:** 22 (as last-click baseline)

- **Appnext** *(excluded from redistribution)*
  - Spend: $446.5
  - Observed: 24
  - **Expected:** 24 (as last-click baseline)

**Check:** expected paid-influenced total ≈ 830 (matches section 3).

What this means:
- Under strict last-click, Meta looks like **$125/sign-up** (2,754/22). Under the modeled view, it’s closer to **~$7.5/sign-up** (2,754/367) — a *massive* swing driven by attribution loss.
- The same “unfairly penalized” pattern applies to Google web flows and Pmax.

---

## 5) Recommendations: decision framework while attribution is broken

Treat each system as answering a different question, and do not force a single “source of truth” until the web→app pipeline is repaired.

### 5.1 Use 3 lenses, explicitly
1) **Finance lens (Sheets realized spend):** “What did we actually pay?”
2) **Product lens (Amplitude totals):** “How many sign-ups / actives happened?”
3) **Attribution lens (AppsFlyer/Amplitude source):** “How are conversions distributed across channels *when measurable*?”

### 5.2 Default operating rules
- **Budget changes** should be driven by:
  - blended efficiency metrics (e.g., cost per virtAcc / new_active from Sheets),
  - plus controlled tests (geo holdouts / on-off tests),
  - **not** by strict last-click CAC when “(none)” is 80%+.

- **Reporting** should always publish:
  - last-click results (audit trail),
  - share of unattributed conversions (measurement health KPI),
  - and a modeled paid-influenced range (clearly labeled).

- **Channel-level calls**
  - Keep ASA optimization decisions closer to last-click (it’s more direct, less web2app leakage).
  - Treat Meta/TikTok web2app as **under-attributed**; require incrementality evidence before cutting hard.
  - Treat low-CPI networks (e.g., Appnext-like) as **guilty until proven** via downstream activation (Sheets) and fraud checks.

### 5.3 “Stop-gap” measurement (while engineering ships)
(Also listed in `analysis/web-to-app-handoff.md`)
- Post-signup onboarding survey (“where did you hear about us?”)
- Channel-specific promo codes / referral codes
- Geo holdouts / on-off tests (esp. Meta web2app)

---

## 6) Concrete fix plan (references): OneLink + deferred deep links + persistence

This reconciliation will remain a model until we fix the pipeline. The engineering blueprint is already written:

- **Primary fix doc:** `analysis/web-to-app-handoff.md`
  - **AppsFlyer OneLink** for *all* web2app CTAs (replace direct store links)
  - **Deferred deep linking** so click context survives install
  - Create `web_session_id` on web, store UTMs + click-ids first-party, and pass via `af_sub1`
  - On first open: send AppsFlyer conversion payload + `af_sub1` to backend
  - On sign-up: join user_id to the acquisition record and freeze first-touch properties

- **Reporting/modeling context:** `analysis/attribution-comparison.md`
  - Keep last-click as audit trail, but use assisted/DDA proxy for budgeting

**Definition of done (quality KPIs)**
- `% of sign-ups with non-null acquisition media source` improves from **~18%** (100%-81.8%) to **>70%**.
- `% of withdrawals with non-null media source` improves from **~39%** (100%-60.9%) to **>70%**.

---

## Appendix: raw numbers referenced (Mar 14–20, 2026)

From `data/attribution-breakdown-20260320.json`:
- Installs (AppsFlyer) total: **1,444**
- Sign-ups (Amplitude) total: **1,206**
  - (none): **986**
  - Organic: **77**
- Withdrawals (Amplitude) total: **2,226**
  - (none): **1,355**
  - Organic: **487**

From `analysis/channel-cac.md`:
- Paid spend proxy (weekly): **$6,714**
- Paid-attributed sign-ups (strict last-click buckets): **121**

From `data/sheets-budget-tracking.json` (Jan CAC tab note):
- Website traffic split assumption: **paid 88% / organic 12%** (GA-based), applied to web/organic install allocation in that sheet.
