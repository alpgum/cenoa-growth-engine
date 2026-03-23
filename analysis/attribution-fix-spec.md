# Attribution Fix — Engineering Implementation Spec

**Owner:** Engineering  
**Status:** Ready for implementation  
**Priority:** Critical  
**Created:** 2026-03-22

---

## Problem

81.8% of sign-up events in Amplitude have no attribution (`media_source = (none)`).  
60.9% of withdrawal events have the same issue.

**Root cause:** Users click a paid ad → land on cenoa.com → tap "Download" → go to App Store/Play Store → install → sign up. The app store link is a **direct store URL**, not an AppsFlyer OneLink. Attribution is lost at the web→store transition. The install is tagged as "Organic" by AppsFlyer, and downstream events inherit nothing.

**Impact:** Paid channels look 6–8× worse than reality. Budget decisions are based on broken data.

---

## Architecture Overview

```
Ad Click (utm_source, fbclid, gclid, ttclid)
  │
  ▼
cenoa.com landing page
  │  ← [1] Capture UTMs + click IDs → cookie + backend
  │  ← [2] Generate web_session_id → cookie + backend
  │
  ▼
"Download" button click
  │  ← [3] Build OneLink URL with af_sub1=web_session_id, af_sub2=utm_source, af_sub3=utm_campaign
  │
  ▼
AppsFlyer OneLink redirect → App Store / Play Store
  │
  ▼
Install + First Open
  │  ← [4] Read deferred deep link payload (AppsFlyer SDK)
  │  ← [5] Send web_session_id + AF attribution to backend
  │
  ▼
Sign-up
  │  ← [6] Backend joins user_id ↔ web_session_id ↔ AF attribution
  │  ← [7] Set Amplitude user properties (first-touch)
  │
  ▼
All downstream events (KYC, deposit, withdrawal)
     ← [8] Amplitude user properties propagate automatically
```

---

## 1. AppsFlyer OneLink Setup

### 1.1 Create OneLink Template

In AppsFlyer dashboard → OneLink Management:

- **Template name:** `cenoa_web2app`
- **Subdomain:** `go.cenoa.com` (configure CNAME in DNS)
- **iOS redirect:** App Store (existing app ID)
- **Android redirect:** Play Store (existing package name)
- **Fallback:** App store page

### 1.2 Configure Parameters

Every OneLink URL must carry these parameters:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `pid` | Channel identifier (e.g., `meta_web2app`) | AppsFlyer media source |
| `c` | Campaign name from UTM | AppsFlyer campaign |
| `af_sub1` | `web_session_id` (UUID, from cookie) | Links web session → app install |
| `af_sub2` | `utm_source` value | Backup: raw UTM source |
| `af_sub3` | `utm_campaign` value | Backup: raw UTM campaign |
| `af_sub4` | `utm_medium` value | Backup: raw UTM medium |
| `af_sub5` | Click ID (`gclid` / `fbclid` / `ttclid`) | Backup: raw click identifier |
| `is_retargeting` | `false` | New user acquisition |
| `af_dp` | Deep link URI (optional) | Post-install routing |

### 1.3 Replace All Store Links

Find every `<a>` tag on cenoa.com that links to:
- `https://apps.apple.com/app/cenoa/...`
- `https://play.google.com/store/apps/details?id=...`

Replace with dynamically generated OneLink URLs (see Section 3 for URL construction).

**Scope:**
- Homepage hero CTA
- Header/nav "Download" button
- Footer app store badges
- Any in-page "Get the app" buttons
- Blog/content CTAs (if any)

---

## 2. Deferred Deep Linking (App-Side)

### 2.1 On First App Open

The AppsFlyer SDK provides a deferred deep link callback. Implement it on both platforms:

**iOS (Swift):**
```swift
func onConversionDataSuccess(_ conversionInfo: [AnyHashable: Any]) {
    let isFirstLaunch = conversionInfo["is_first_launch"] as? Bool ?? false
    guard isFirstLaunch else { return }

    let webSessionId = conversionInfo["af_sub1"] as? String
    let mediaSource = conversionInfo["media_source"] as? String
    let campaign = conversionInfo["campaign"] as? String
    let utmSource = conversionInfo["af_sub2"] as? String
    let utmCampaign = conversionInfo["af_sub3"] as? String
    let utmMedium = conversionInfo["af_sub4"] as? String
    let clickId = conversionInfo["af_sub5"] as? String

    // Store locally
    AttributionStore.save(
        webSessionId: webSessionId,
        mediaSource: mediaSource,
        campaign: campaign,
        utmSource: utmSource,
        utmCampaign: utmCampaign,
        utmMedium: utmMedium,
        clickId: clickId
    )

    // Send to backend
    API.reportAttribution(params: AttributionStore.current)
}
```

**Android (Kotlin):**
```kotlin
override fun onConversionDataSuccess(conversionData: MutableMap<String, Any>?) {
    val isFirstLaunch = conversionData?.get("is_first_launch") as? Boolean ?: false
    if (!isFirstLaunch) return

    val attribution = Attribution(
        webSessionId = conversionData?.get("af_sub1") as? String,
        mediaSource = conversionData?.get("media_source") as? String,
        campaign = conversionData?.get("campaign") as? String,
        utmSource = conversionData?.get("af_sub2") as? String,
        utmCampaign = conversionData?.get("af_sub3") as? String,
        utmMedium = conversionData?.get("af_sub4") as? String,
        clickId = conversionData?.get("af_sub5") as? String,
    )

    AttributionStore.save(attribution)
    api.reportAttribution(attribution)
}
```

### 2.2 Persist Locally

Store attribution in `SharedPreferences` (Android) / `UserDefaults` (iOS). This data is immutable once written (first-touch only). Never overwrite on subsequent opens.

### 2.3 Send to Backend

**Endpoint:** `POST /api/v1/attribution/app-open`

```json
{
  "appsflyer_id": "1234567890123-1234567",
  "web_session_id": "550e8400-e29b-41d4-a716-446655440000",
  "media_source": "meta_web2app",
  "campaign": "tr_signup_march",
  "utm_source": "meta",
  "utm_campaign": "tr_signup_march",
  "utm_medium": "paid_social",
  "click_id": "fbclid_abc123",
  "platform": "ios",
  "app_version": "2.1.0",
  "device_id": "amplitude_device_id"
}
```

---

## 3. Web UTM Persistence (Server-Side + Client-Side)

### 3.1 On Landing Page Load

When a user lands on any cenoa.com page:

```javascript
// Client-side: runs on every page load
(function() {
  const params = new URLSearchParams(window.location.search);

  const utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
  const clickIdKeys = ['gclid', 'gbraid', 'wbraid', 'fbclid', 'ttclid'];

  // Only capture if UTMs or click IDs are present in the URL
  const hasAttribution = [...utmKeys, ...clickIdKeys].some(k => params.has(k));
  if (!hasAttribution) return;

  // Generate or retrieve web_session_id
  let sessionId = getCookie('cenoa_wsid');
  if (!sessionId) {
    sessionId = crypto.randomUUID();
    setCookie('cenoa_wsid', sessionId, 30); // 30-day expiry
  }

  // Build attribution object
  const attribution = { web_session_id: sessionId };
  utmKeys.forEach(k => { if (params.get(k)) attribution[k] = params.get(k); });
  clickIdKeys.forEach(k => { if (params.get(k)) attribution[k] = params.get(k); });
  attribution.landing_url = window.location.pathname;
  attribution.referrer = document.referrer;
  attribution.timestamp = new Date().toISOString();

  // Store in localStorage (backup)
  localStorage.setItem('cenoa_attribution', JSON.stringify(attribution));

  // Send to backend
  fetch('/api/v1/attribution/web-session', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(attribution)
  });
})();
```

### 3.2 Backend: Store Web Session

**Endpoint:** `POST /api/v1/attribution/web-session`

**Schema (new table: `web_attribution_sessions`):**

```sql
CREATE TABLE web_attribution_sessions (
  web_session_id  UUID PRIMARY KEY,
  created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
  landing_url     TEXT,
  referrer        TEXT,
  utm_source      VARCHAR(255),
  utm_medium      VARCHAR(255),
  utm_campaign    VARCHAR(255),
  utm_content     VARCHAR(255),
  utm_term        VARCHAR(255),
  gclid           VARCHAR(255),
  gbraid          VARCHAR(255),
  wbraid          VARCHAR(255),
  fbclid          VARCHAR(255),
  ttclid          VARCHAR(255),
  user_agent      TEXT,
  ip_country      VARCHAR(2)
);

CREATE INDEX idx_was_created ON web_attribution_sessions(created_at);
```

### 3.3 Build OneLink URL on CTA Click

When user clicks "Download the app":

```javascript
function buildOneLinkUrl() {
  const attr = JSON.parse(localStorage.getItem('cenoa_attribution') || '{}');
  const sessionId = getCookie('cenoa_wsid') || '';

  const base = 'https://go.cenoa.com/web2app'; // OneLink short URL

  const params = new URLSearchParams({
    pid: mapToPid(attr.utm_source, attr.utm_medium), // e.g., "meta_web2app"
    c: attr.utm_campaign || '',
    af_sub1: sessionId,
    af_sub2: attr.utm_source || '',
    af_sub3: attr.utm_campaign || '',
    af_sub4: attr.utm_medium || '',
    af_sub5: attr.gclid || attr.fbclid || attr.ttclid || '',
  });

  return `${base}?${params.toString()}`;
}

// Map utm_source + utm_medium → AppsFlyer pid
function mapToPid(source, medium) {
  if (source === 'google' && medium === 'cpc') return 'google_web2app';
  if (source === 'meta' || source === 'facebook') return 'meta_web2app';
  if (source === 'tiktok') return 'tiktok_web2app';
  return 'website_organic';
}
```

---

## 4. Amplitude Property Propagation

### 4.1 Set User Properties on Sign-Up

When a user completes sign-up, the backend must:

1. Look up the user's `web_session_id` (from the app-open attribution report)
2. Join with `web_attribution_sessions` table
3. Merge with AppsFlyer conversion data
4. Set Amplitude user properties

**Backend logic (on sign-up complete):**

```python
def on_signup_complete(user_id, appsflyer_id, web_session_id):
    # 1. Get web attribution
    web_attr = db.query(
        "SELECT * FROM web_attribution_sessions WHERE web_session_id = %s",
        web_session_id
    )

    # 2. Get AppsFlyer attribution (from app-open report, stored earlier)
    af_attr = db.query(
        "SELECT * FROM app_attribution WHERE appsflyer_id = %s",
        appsflyer_id
    )

    # 3. Build first-touch attribution (prefer AF, fallback to web)
    first_touch = {
        "attributed_source": af_attr.media_source or web_attr.utm_source,
        "attributed_campaign": af_attr.campaign or web_attr.utm_campaign,
        "attributed_medium": af_attr.utm_medium or web_attr.utm_medium,
        "attributed_click_id": web_attr.gclid or web_attr.fbclid or web_attr.ttclid,
        "attributed_landing_page": web_attr.landing_url,
        "attributed_web_session_id": web_session_id,
        "attributed_af_media_source": af_attr.media_source,
        "attributed_af_campaign": af_attr.campaign,
    }

    # 4. Save to user record (immutable first-touch)
    db.execute(
        "UPDATE users SET first_touch_attribution = %s WHERE id = %s",
        json.dumps(first_touch), user_id
    )

    # 5. Set Amplitude user properties
    amplitude.identify(user_id, user_properties={
        "$set_once": {  # $set_once = never overwrite
            "attributed_source": first_touch["attributed_source"],
            "attributed_campaign": first_touch["attributed_campaign"],
            "attributed_medium": first_touch["attributed_medium"],
            "attributed_click_id": first_touch["attributed_click_id"],
            "attributed_landing_page": first_touch["attributed_landing_page"],
            "attributed_web_session_id": first_touch["attributed_web_session_id"],
        }
    })
```

### 4.2 Ensure Properties Propagate to All Downstream Events

Amplitude user properties are automatically included in all subsequent events for that user. **No additional work needed per event** — as long as user properties are set before/at sign-up.

**Verify** that these events carry the user properties:
- `Cenoa sign-up completed`
- `KYC submit`
- `VirtAcc created`
- `New active`
- `Deposit`
- `Withdraw Completed`

### 4.3 Backfill (Optional)

For users who signed up before this fix ships, you can backfill from AppsFlyer raw data exports:

```python
# Backfill from AppsFlyer installs export
for row in appsflyer_installs_export:
    if row.media_source and row.media_source != "organic":
        amplitude.identify(row.customer_user_id, user_properties={
            "$set_once": {
                "attributed_source": row.media_source,
                "attributed_campaign": row.campaign,
            }
        })
```

---

## 5. QA Test Plan

### 5.1 Test Matrix

| # | Channel | Platform | Path | Expected `attributed_source` |
|---|---------|----------|------|------------------------------|
| 1 | Meta | iOS (Safari) | Ad → cenoa.com → Download → Install → Sign-up | `meta_web2app` |
| 2 | Meta | Android (Chrome) | Ad → cenoa.com → Download → Install → Sign-up | `meta_web2app` |
| 3 | Google | iOS (Safari) | Ad → cenoa.com → Download → Install → Sign-up | `google_web2app` |
| 4 | Google | Android (Chrome) | Ad → cenoa.com → Download → Install → Sign-up | `google_web2app` |
| 5 | TikTok | iOS (Safari) | Ad → cenoa.com → Download → Install → Sign-up | `tiktok_web2app` |
| 6 | TikTok | Android (Chrome) | Ad → cenoa.com → Download → Install → Sign-up | `tiktok_web2app` |
| 7 | Direct | iOS (Safari) | cenoa.com (no UTMs) → Download → Install → Sign-up | `website_organic` |
| 8 | Direct | Android (Chrome) | cenoa.com (no UTMs) → Download → Install → Sign-up | `website_organic` |
| 9 | Meta | iOS | Direct app install (no web) → Sign-up | `Meta Ads` (standard AF) |
| 10 | Meta | Android | Direct app install (no web) → Sign-up | `Meta Ads` (standard AF) |

### 5.2 Test Procedure (per test case)

**Pre-conditions:**
- App is NOT installed on test device
- iOS: use Private Browsing / clear Safari cookies
- Android: use Incognito / clear Chrome cookies

**Steps:**

1. **Click the test link** (OneLink with test UTMs):
   ```
   https://go.cenoa.com/web2app?pid=meta_web2app&c=TEST_qa_march&af_sub1=test-session-001&af_sub2=meta&af_sub3=TEST_qa_march&af_sub4=paid_social
   ```

2. **Verify cenoa.com** (if link routes through LP):
   - Check browser cookie: `cenoa_wsid` exists
   - Check localStorage: `cenoa_attribution` has correct UTMs

3. **Click "Download"** on cenoa.com:
   - Verify redirect goes through OneLink (not direct store URL)

4. **Install the app** from store

5. **Open the app**:
   - Check AppsFlyer debug logs: conversion data callback fires
   - Verify `af_sub1` (web_session_id) is present in payload

6. **Complete sign-up**

7. **Verify in AppsFlyer dashboard:**
   - Install appears under `media_source = meta_web2app`
   - Campaign = `TEST_qa_march`

8. **Verify in backend:**
   - `web_attribution_sessions` row exists for the session ID
   - `users.first_touch_attribution` is populated

9. **Verify in Amplitude:**
   - User profile has `attributed_source = meta_web2app`
   - `Cenoa sign-up completed` event has user property `attributed_campaign = TEST_qa_march`

### 5.3 Expected Properties at Each Funnel Step

| Funnel Step | Where to Check | Expected Properties |
|-------------|----------------|---------------------|
| Web landing | Backend DB (`web_attribution_sessions`) | `web_session_id`, `utm_source`, `utm_campaign`, `utm_medium`, click IDs |
| App install | AppsFlyer dashboard | `media_source`, `campaign`, `af_sub1` (web_session_id) |
| App first open | App logs + backend (`app_attribution`) | `appsflyer_id`, `web_session_id`, `media_source`, `campaign` |
| Sign-up | Backend (`users.first_touch_attribution`) | `attributed_source`, `attributed_campaign`, `attributed_medium` |
| Sign-up event | Amplitude | User property: `attributed_source`, `attributed_campaign` |
| KYC / Deposit / Withdrawal | Amplitude | Same user properties auto-propagate |

### 5.4 Pass Criteria

- All 10 test cases in matrix pass
- `attributed_source` is non-null and correct at sign-up for all web2app paths
- Properties visible on downstream events in Amplitude (spot-check KYC + withdrawal)
- No regression on direct app-install attribution (tests 9–10)

---

## 6. Success Metrics

| Metric | Current | Target (2 weeks post-launch) |
|--------|---------|------------------------------|
| Sign-ups with `attributed_source != (none)` | 18.2% | >70% |
| Withdrawals with `attributed_source != (none)` | 39.1% | >70% |
| Web2app installs attributed to correct paid source | ~0% | >80% |

---

## 7. Rollout Plan

| Phase | Timeline | Scope |
|-------|----------|-------|
| **Phase 0** | Days 1–2 | Create OneLink template. Replace all cenoa.com store links with a single generic OneLink. Immediate signal recovery. |
| **Phase 1** | Days 3–7 | Implement `web_session_id` capture on cenoa.com. Build `web_attribution_sessions` table. Pass `af_sub1` through OneLink. Read conversion data on first app open. |
| **Phase 2** | Days 8–14 | Backend join logic (web session ↔ app open ↔ sign-up). Set Amplitude user properties with `$set_once`. Run full QA matrix. |
| **Phase 3** | Days 15–21 | Monitor attribution fill rates. Backfill historical users from AF exports. Tune and iterate. |

---

## 8. Dependencies & Pre-requisites

- [ ] AppsFlyer dashboard access (OneLink management)
- [ ] DNS access to configure `go.cenoa.com` CNAME
- [ ] cenoa.com codebase access (frontend JS changes)
- [ ] Backend API capacity (2 new endpoints)
- [ ] New DB table (`web_attribution_sessions`)
- [ ] AppsFlyer SDK already integrated in iOS + Android apps
- [ ] Amplitude SDK already integrated (server-side `identify` capability)

---

*Generated: 2026-03-22. This spec is copy-paste actionable. All code samples are pseudocode — adapt to your actual stack.*
