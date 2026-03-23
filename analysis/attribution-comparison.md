# Attribution model comparison — why channel CAC swings (and how to fix it)

**Context:** Cenoa’s reporting currently has a large **web → app attribution gap**. Paid channels (especially **Meta Web2App / TikTok Web2App / Google web flows**) can create demand on the web, but the **install + downstream events** often show up as **Organic** or **(none)** in AppsFlyer/Amplitude exports.

This doc explains attribution models in plain terms, then shows (with current data) how **CAC / cost-per-active** changes depending on the model, and what we should do for **budgeting vs reporting**.

**Related analyses:**
- `analysis/attribution-funnel.md` (shows the “(none)” dominance downstream)
- `analysis/channel-cac.md` (spend proxy vs attributed outcomes)
- `analysis/cac-crosscheck.md` (why Sheet vs product analytics denominators disagree)

**Data sources (current):**
- `data/attribution-breakdown-20260320.json` (Amplitude segmentation by AppsFlyer source)
- `data/channel-cac.json` (compiled spend proxy + attributed outcomes + sheet activation proxies)
- `data/sheets-cac-analysis.json` (sheet exports used for weekly avg activation proxies)

---

## 0) Current problem in one chart-worthy stat

From `attribution-breakdown-20260320.json` (Mar 14–20, 2026):

- **Sign-ups with missing attribution “(none)”**: **986 / 1,206 = 81.8%**
- **Withdrawals with missing attribution “(none)”**: **1,355 / 2,226 = 60.9%**

So if we use a strict last-click view, most downstream value is **unassigned**, and paid looks far worse than it really is.

---

## 1) Attribution models (simple definitions)

### Last-click attribution (a.k.a. last-touch)
- **Gives 100% credit to the last known touchpoint** before conversion.
- In mobile measurement, this often means: *“the channel that got credit for the install”* gets credit for later events too.
- **Pro:** simple, audit-friendly.
- **Con:** with **web→app leakage**, paid often fails to “stick” to later events → lots of **(none)** / “organic”.

### First-click attribution (a.k.a. first-touch)
- **Gives 100% credit to the first touchpoint** that introduced the user.
- **Pro:** better for measuring **demand creation** (upper funnel).
- **Con:** can over-credit awareness channels and under-credit intent channels (e.g., ASA brand) if you don’t have true path data.

### Data-driven attribution (DDA)
- **Splits credit across touchpoints** based on observed patterns (or a proxy rule if you don’t have the full path data).
- **Pro:** closest to how marketing actually works (assists matter).
- **Con:** requires reliable capture of multi-touch journeys; otherwise you’re doing a “best-effort” proxy.

---

## 2) Demonstration with *current* data: CAC swings by attribution model

### 2.1 Inputs (what we know)
From `data/channel-cac.json` (Mar 14–20 outcomes + spend proxy):

- **Paid spend proxy (weekly):** **$6,714**
- **Paid sign-ups attributed in last-click AppsFlyer view:** **121**
- **Unattributed sign-ups (“(none)”):** **986**
- **Organic sign-ups:** **77**

We also need a definition of “active”. We don’t have **new_active by AppsFlyer source** in the attribution export, so we do a best-effort estimate:

- Use **activation rates** from Sheets weekly averages (early March) per bucket:
  - `activation_rate_bucket = sheet_new_active / sheet_signups`
- Then estimate:
  - `estimated_new_active_bucket = attributed_signups_bucket × activation_rate_bucket`

This is imperfect, but it’s directionally useful for *“how attribution changes cost-per-active.”*

### 2.2 Assumptions (explicit)
Because we **don’t** have web-to-app path-level attribution yet, we need assumptions to move “(none)” back into paid.

**Base case (used below):**
- **70% of unattributed sign-ups** are actually **paid-influenced** (web→app journeys losing attribution)
- **25% of organic sign-ups** are **paid-influenced** (paid creates demand; user later converts via “organic”)
- Redistribute those “paid-influenced” sign-ups across **Meta / TikTok / Google Search / Pmax / Other** proportional to their **paid spend share** (excluding ASA + Appnext, which are less likely to be the web→app leakage sources).

### 2.3 Results: paid CAC under 3 attribution models

> Interpretation: this is not “the truth”, it’s **how your CAC changes** when attribution moves from strict last-click to assisted / data-driven.

| Model | Paid sign-ups credited | Cost / sign-up | Paid *estimated* new actives | Cost / new active |
|---|---:|---:|---:|---:|
| **Last-click (strict AppsFlyer)** | 121.0 | **$55.5** | 28.7 | **$233.6** |
| **Data-driven (proxy = 50% LC + 50% FC)** | 475.7 | **$14.1** | 100.8 | **$66.6** |
| **First-click (paid-influenced)** | 830.4 | **$8.1** | 173.0 | **$38.8** |

#### Sanity check: why the last-click numbers look absurd
Under strict last-click, Meta shows **22 sign-ups** credited (in AppsFlyer source view) on **$2,754** proxy weekly spend → **$125/sign-up**.

But **81.8% of sign-ups are “(none)”**. If many of those are web→app paid journeys, strict last-click will systematically under-credit paid.

### 2.4 Sensitivity (how much of “(none)” is actually paid?)
Holding organic-influenced-by-paid at **25%**, the paid **cost/new active** moves a lot:

| Assumption: share of “(none)” sign-ups that are paid-influenced | DDA proxy cost/new active | First-click cost/new active |
|---:|---:|---:|
| 50% | $83.1 | $50.5 |
| **70% (base)** | **$66.6** | **$38.8** |
| 90% | $55.5 | $31.5 |

**Takeaway:** budget decisions based on strict last-click will push us toward the wrong conclusion (e.g., “Meta is broken”) even when paid is actually driving a big chunk of conversions that are currently unlabeled.

---

## 3) Recommendation for Cenoa (budgeting vs reporting)

### A) Use for **budgeting / channel optimization**
**Use a data-driven / assisted view (not strict last-click).**

Pragmatic approach until measurement is fixed:
1) Use **activation-based efficiency** (e.g., cost per *new active* / cost per *virt_acc*) from Sheets / internal ops views for day-to-day optimization.
2) Use a **DDA proxy** in reporting (like the one above) as a *second lens* to avoid killing channels that are suffering from attribution loss.
3) Validate big budget moves with **incrementality tests** (geo holdouts / on-off tests) where possible.

**Why:** budgeting needs to approximate *incremental impact*. Last-click under the current leakage regime mostly measures *“who happened to get the last measurable tag.”*

### B) Use for **exec reporting / finance narratives**
**Keep last-click AppsFlyer as the audit trail**, but always publish it **alongside**:
- **Blended CAC** (total paid spend / total activations)
- **Share of unattributed downstream events** (a KPI by itself)
- A **DDA/assisted estimate** (clearly labeled as modeled)

**Why:** exec reporting needs consistency and traceability. Last-click provides that, but it must be contextualized or it will cause wrong strategic calls.

---

## 4) Measurement plan to reduce uncertainty (fix the web→app gap)

### 4.1 Implement AppsFlyer OneLink + deferred deep linking (core)
Goal: web clicks reliably become attributed app installs, even if the app isn’t installed yet.

**Checklist:**
- Create **OneLink** for every web2app campaign (Meta, TikTok, Google).
- Ensure **deferred deep linking** works (click → install → first open routes correctly).
- Pass and persist at minimum:
  - `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`
  - click IDs: `gclid` / `gbraid` / `wbraid`, `fbclid`, `ttclid` (as applicable)
  - landing page + timestamp

### 4.2 Capture web UTMs in product + persist to backend
Even if attribution vendors fail, the product stack should retain the acquisition context.

- On web: store UTMs/click-ids in **first-party cookie/localStorage**.
- On signup / phone verify / key step: send them to backend and save to a **user acquisition table**.
- In app: on first open, read deferred deep link payload and attach to user profile.

### 4.3 Make attribution “stick” to downstream events (Amplitude hygiene)
The current export shows attribution sticks to installs but not consistently to signups/withdrawals.

- Ensure AppsFlyer media source + campaign are written as **user properties** (or event properties) at install/first open.
- Ensure the signup/virt_acc/new_active events carry those properties (or are joinable by user_id).
- Create a QA metric:
  - **% of events with missing media source** by event type (install, signup, virt_acc, new_active, withdrawal)
  - Alert if it breaches a threshold.

---

## 5) What can go wrong (failure modes)

1) **“Organic looks amazing” but it’s actually paid**
   - Web→app leakage makes paid conversions appear organic → you underinvest in paid growth.

2) **You kill the wrong channel**
   - Strict last-click can make Meta/TikTok look unprofitable while they are actually feeding assisted conversions.
   - Result: you cut spend, then overall sign-ups drop, and you can’t explain why.

3) **You over-credit high-intent channels (especially ASA brand)**
   - If a user sees Meta, then later searches brand and installs via ASA, last-click makes ASA look like the hero.
   - Result: you move budget to ASA, hit ceiling fast, and lose top-of-funnel growth.

4) **You chase low CPI fraud (Appnext-style)**
   - Low CPI can look great in install-based metrics while producing near-zero actives.
   - Without an activation metric, you scale garbage.

5) **Double-counting and “too-good-to-be-true” CAC**
   - If you combine platform-reported conversions with last-click vendor reporting without deduping, CAC will look artificially low.

6) **Attribution windows / privacy changes distort trends**
   - iOS privacy, reattribution windows, and SKAN constraints can shift credit without real performance change.

---

## Appendix: quick formulas used in this doc

- **Cost per sign-up (paid total)** = `total_paid_spend / signups_credited_to_paid`
- **Activation rate proxy (bucket)** = `sheet_new_active / sheet_signups`
- **Estimated new actives (bucket)** = `signups_credited_to_bucket × activation_rate_bucket`
- **Cost per new active (paid total)** = `total_paid_spend / Σ estimated_new_actives`

---

*Generated: 2026-03-21. Best-effort modeling based on current exports; use primarily to avoid wrong budget decisions until OneLink + UTM persistence closes the attribution gap.*


---

> ⚠️ **Attribution caveat:** Web campaigns (Meta/Google → cenoa.com → app store) may appear as "Organic" or "(none)" due to broken web→app attribution. Estimated correction factor: ~6.9×. See [attribution-reconciliation.md](attribution-reconciliation.md) for details.
