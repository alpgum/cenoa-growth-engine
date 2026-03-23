# Web → App Handoff Analysis (Attribution Repair)

**Problem statement:** Cenoa has a large **web → app attribution gap**. Web2App campaigns can drive intent on **cenoa.com**, but **install + downstream events** (sign-up, KYC, withdrawal) frequently show up as **Organic / (none)**.

**Why this matters:** When attribution breaks at the handoff, **paid looks unprofitable** and **“organic” looks inflated**. Current exports show this is material:
- **Unattributed sign-ups “(none)”**: **986 / 1,206 = 81.8%** (`analysis/attribution-comparison.md`)
- **Unattributed withdrawals “(none)”**: **1,355 / 2,226 = 60.9%** (`analysis/attribution-comparison.md`)
- **Web dominates sign-ups**: **754 / 1,207 = 62.5%**, but with **<1% downstream conversion** (15 deposits, 7 withdrawals) (`analysis/funnel-summary.md`)

This doc maps the current suspected journey, pinpoints where attribution is lost, and provides a concrete fix blueprint (AppsFlyer OneLink + deferred deep linking + server-side persistence + Amplitude propagation), plus QA + stop-gaps.

---

## 1) Current suspected user journey (paid → web → app)

Most failing journeys look like this:

1) **Paid ad click** (Meta/TikTok/Google)  
   → URL with `utm_*` + click IDs (`fbclid`, `gclid`, `wbraid/gbraid`, `ttclid`)

2) **cenoa.com landing page** (mobile web)  
   → user reads value prop / trust, then taps **“Download” / “Get the app”**

3) **App Store / Google Play**

4) **Install**

5) **First open**

6) **Sign-up** (and later: KYC / deposit / withdrawal)

### What we want (ideal state)
The **same acquisition context** should be recoverable across the chain:

`ad click` → `web session` → `store click` → `install attribution (AppsFlyer)` → `first open` → `signup` → `all downstream events`

In practice, we’re losing the trail between **(2) web** and **(4–6) app**.

---

## 2) Where attribution is currently lost (UTM, click-id, AppsFlyer params, deep links)

### Breakpoints (most likely)

| Step | What should persist | What often breaks | Symptom in current data |
|---|---|---|---|
| Ad click → LP | `utm_*`, click-id (`gclid/fbclid/ttclid`) | Redirects + Safari ITP; UTMs not stored first-party | GA4 sees campaign, but app install doesn’t |
| LP → App Store | A **measurement redirect** must happen (OneLink) | Using **direct store links** or “open in app store” without OneLink | Installs credited to **Organic** instead of paid |
| Store → Install | AppsFlyer match between click and install | No OneLink / no Smart Script; match fails (esp. iOS) | AppsFlyer install attributed incorrectly or as organic |
| Install → First open | Conversion data / deep link payload delivered | Deferred deep link not configured, or app doesn’t read & persist it | User opens app but has no acquisition properties |
| First open → Sign-up | Attribution fields applied to user + events | Sign-up is **backend/server event** without attribution context | **Sign-ups show (none)** even if install has source |
| Sign-up → Downstream events | Acquisition sticks to all events | Event pipeline drops properties; ID mapping issues | Withdrawals show (none) at high rates |

### The two distinct problems to separate
1) **Install attribution** is not reliably assigned (web→store→install mismatch).  
2) Even when installs are attributed, **downstream events are not carrying the AppsFlyer dimensions** (media source/campaign) → they collapse into **(none)**.

Both are visible in `analysis/attribution-funnel.md` caveats and the “(none)” dominance.

---

## 3) Concrete fix blueprint (recommended implementation)

### Overview: what “fixed” looks like
- Every web2app path uses **AppsFlyer OneLink** (not raw store URLs).
- OneLink is configured for **deferred deep linking**.
- Web captures `utm_*` + click IDs **first-party**, sends to backend, and passes a stable token through OneLink (`af_sub*` or deep link params).
- App reads conversion data on first open, sends it to backend, and Amplitude receives it as **user properties** + **event properties** on all key events.

Below is the concrete build plan.

---

### 3.1 AppsFlyer OneLink (the core bridge)

**Goal:** Turn `web click` into an attributed `install`, even when the app isn’t installed yet.

**Implementation checklist**
1) **Create OneLink template** (single template, multiple short links).
2) Use a **custom domain** if possible (trust + deliverability): e.g. `go.cenoa.com`.
3) Create **separate OneLinks** by channel + use case:
   - `meta_web2app_*`
   - `tiktok_web2app_*`
   - `google_web2app_*`
   - `organic_site_cta`
4) Replace all **“Download app”** links/buttons on cenoa.com with the relevant OneLink.
5) Ensure OneLink routes correctly:
   - App installed → open app via **universal link / app link**
   - App not installed → send to store → then **deferred deep link** on first open

**Parameters to pass (minimum viable)**
- UTMs: `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`
- Click IDs where available: `gclid`, `gbraid`, `wbraid`, `fbclid`, `ttclid`
- `lp_url` (landing page path) + `timestamp`
- A stable **web session token** (see 3.3) → `af_sub1=<web_session_id>`

**Important:** If you rely on OneLink without web-side capture/bridging, attribution can still be brittle (especially on iOS). Treat OneLink as necessary but not sufficient.

---

### 3.2 Deferred deep linking (make the click survive install)

**Goal:** If the app isn’t installed at click time, we still recover the click context after install.

**App requirements**
- On first open, call AppsFlyer’s conversion data callback (platform-specific) and extract:
  - `media_source`, `campaign`, `adset`, `ad`, etc.
  - any custom params you passed (e.g. `af_sub1` / deep link query string)
- Persist these values locally (first-launch only) and also send to backend.

**Deep link routing**
Use the deep link payload to route into the most relevant screen (this improves conversion and is also a QA signal):
- `.../invite?code=XXXX` → open referral flow
- `.../kyc` → open KYC entry
- `.../deposit` → open deposit

---

### 3.3 Persist UTM/click-id server-side and associate to the eventual user (closing the web-side gap)

**Goal:** Even if vendor matching fails, we can still join **web acquisition context → user**.

**Recommended design (robust + debuggable)**

1) **On landing page view** (server-side or client-side):
   - Create `web_session_id = uuid()`
   - Store it in a **first-party cookie** (and optionally localStorage) with a 7–30 day TTL.
   - Save a row in backend:

   ```
   web_session_id
   created_at
   landing_url
   referrer
   utm_source/medium/campaign/content/term
   click_ids (gclid/wbraid/gbraid/fbclid/ttclid)
   user_agent
   ip_country (if allowed)
   ```

2) **On “Get the app” click**:
   - Redirect the user through OneLink and attach `web_session_id`:

   ```
   https://go.cenoa.com/<shortlink>?af_sub1=<web_session_id>
   ```

3) **On app first open**:
   - Read AppsFlyer conversion data + `af_sub1`.
   - Send to backend: `web_session_id`, `appsflyer_id`, `advertising_id (if available)`, device metadata.

4) **On sign-up completed**:
   - Backend associates the signed-up `user_id` with:
     - the first-seen `web_session_id` (if present)
     - the first-seen AppsFlyer attribution payload
   - Freeze these as immutable “first-touch” acquisition fields:

   ```
   user.acq_first_utm_source
   user.acq_first_campaign
   user.acq_first_media_source
   user.acq_first_af_campaign
   user.acq_first_click_id
   user.acq_first_landing_page
   ```

**Why this matters for the current “(none)” issue**
If sign-up / withdrawals are tracked via backend events, they will default to **(none)** unless you explicitly join and attach acquisition properties. This server-side table is the canonical join.

---

### 3.4 Push attribution properties into Amplitude downstream events (make attribution “stick”)

**Goal:** Any event you care about (sign-up, KYC, virt_acc, new_active, deposit, withdrawal) must carry stable acquisition fields.

**Recommended Amplitude hygiene**
1) Set user properties once (first-touch):
   - `acq_first_source`, `acq_first_medium`, `acq_first_campaign`
   - `acq_first_media_source` (AppsFlyer)
   - `acq_first_af_campaign`
   - `acq_first_web_session_id`

2) Add event properties on key events (at least):
   - `Cenoa sign-up completed`
   - `KYC submit`
   - `VirtAcc created` / `New active`
   - `Deposit` / `Withdraw Completed`

3) Ensure identity alignment:
   - If events are client-side: confirm Amplitude user identity is set only after sign-up (`user_id`) but retains `device_id` continuity.
   - If events are server-side: ensure the backend can attach acquisition properties via the join table above.

**Success KPI (instrumentation quality):**
- `% of sign-ups with non-null acq_first_media_source` should rise from ~18% to **>70%** within 1–2 weeks (then keep pushing higher).
- `% of withdrawals with non-null media_source/campaign` should rise from ~39% to **>70%**.

---

## 4) QA plan (validate end-to-end)

### 4.1 Test matrix (minimum)
Run each test on:
- Android (Chrome)
- iOS (Safari)

And for channels:
- Meta (UTM + fbclid)
- Google (UTM + gclid/wbraid)
- TikTok (UTM + ttclid)

### 4.2 Test procedure (per test case)

1) **Prepare a test OneLink**
   - Include UTMs + a recognizable test campaign name:

   ```
   utm_source=meta&utm_medium=paid_social&utm_campaign=TEST_web2app_march
   ```

   - Include a synthetic click-id param if needed for QA visibility.

2) **Click from a clean state**
   - iOS: private browsing + ensure app is not installed (or delete it)
   - Android: incognito + ensure app is not installed (or clear Play Store/app data)

3) **Observe expected redirects**
   - Link → OneLink domain → App Store/Play Store

4) **Install and open**
   - Confirm the app opens to expected deep link route (if configured).

5) **Verify in AppsFlyer**
   - The install should appear under the correct **media source / campaign**.
   - Raw data should include `af_sub1` (web_session_id) and your UTM fields (where you mapped them).

6) **Verify in Amplitude**
   - For the new user/device:
     - user properties include `acq_first_*`
     - `sign-up completed` event includes `acq_first_media_source` and `acq_first_campaign`

7) **Regression check**
   - Repeat once with the app already installed to validate **direct deep link** behavior.

### 4.3 Expected payload (definition of done)
At minimum, the following should be queryable in Amplitude for the sign-up event:
- `acq_first_utm_source`
- `acq_first_utm_campaign`
- `acq_first_media_source` (AppsFlyer)
- `acq_first_af_campaign`
- `acq_first_web_session_id`

---

## 5) Stop-gap measurement options (while engineering fixes ship)

While the OneLink + persistence work is being implemented and stabilized, use these to reduce decision risk:

1) **Onboarding survey (in-app, post-signup)**
   - Question: “Where did you hear about Cenoa?”
   - Options mapped to channel taxonomy (Meta, TikTok, Google, Apple Search Ads, Friend, Other)
   - Treat as directional, but it helps re-allocate spend away from obvious waste.

2) **Promo codes / channel-specific referral codes**
   - Different code per channel or per country/campaign family.
   - Add to the web landing page (auto-filled) and the app onboarding.

3) **Geo holdouts / on-off tests**
   - Run controlled spend tests: pause spend in a geo for 3–7 days, compare lifts vs control geo.
   - Especially useful for Meta web2app where last-click reporting is unreliable.

4) **Blended CAC + activation proxy**
   - Use blended denominator (all new actives / virt_acc) until attribution improves.
   - Publish last-click alongside modeled assisted view (as in `analysis/attribution-comparison.md`).

---

## 6) Practical rollout plan (fastest path)

**Phase 0 (1–2 days): “Stop the bleeding”**
- Replace all cenoa.com app store links with OneLink.
- Create a single “generic” OneLink for website CTA so at least installs are captured.

**Phase 1 (3–7 days): “Make it deterministic”**
- Implement `web_session_id` capture + backend persistence.
- Pass token via `af_sub1`.
- Read conversion data + send to backend on first open.

**Phase 2 (1–2 weeks): “Make attribution stick”**
- Update Amplitude pipeline so all key events are enriched with first-touch acquisition fields.
- Add monitoring: % missing attribution by event type.

---

## Appendix: how this ties to existing findings
- The “(none)” dominance downstream is already documented in `analysis/attribution-funnel.md` and `analysis/attribution-comparison.md`.
- The web sign-up leak (754 web sign-ups with near-zero deposits/withdrawals) is highlighted in `analysis/funnel-summary.md` and is consistent with a broken web→app handoff.

*Generated: 2026-03-21. This is a best-effort technical blueprint; exact parameter names/macros should be finalized with the AppsFlyer dashboard + engineering implementation details.*


---

> ⚠️ **Attribution caveat:** Web campaigns (Meta/Google → cenoa.com → app store) may appear as "Organic" or "(none)" due to broken web→app attribution. Estimated correction factor: ~6.9×. See [attribution-reconciliation.md](attribution-reconciliation.md) for details.
