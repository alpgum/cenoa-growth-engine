# LP A/B Test — Developer Implementation Spec

**Sprint:** 064  
**Ticket:** S3-024  
**Date:** 2026-03-23  
**Owner:** Growth / Performance Marketing  
**Status:** Ready for dev  
**Depends on:** [S2B-014] TR LP A/B Variants (tr-lp-ab-variants.md)

---

## 1. Current State — cenoa.com Hero Section

**URL:** https://www.cenoa.com/  
**Platform:** Webflow (custom code embeds supported)

### Current Hero (to become Control)

| Element | Current Copy |
|---|---|
| **Headline** | `Get paid globally— 10x cheaper than Payoneer` |
| **Subheadline** | `Open free US and EU accounts in 3 minutes — powered by Stripe, Lead Bank, and USDC (Circle).` |
| **Social proof line** | `Serving 500,000+ professionals from: +35 [countries]` |
| **Below-fold widget** | Fee comparison table (Cenoa $10 vs Payoneer $85 on $1,000) |
| **CTA** | App store links (implied — no single hero CTA button) |

> **Note:** The current hero is in English. All test variants are Turkish-only, served exclusively to TR-geo visitors. Non-TR visitors continue seeing the English default.

---

## 2. Test Variants (Control + 3 Treatments)

### Traffic Split: 25 / 25 / 25 / 25

| ID | Name | Hook | Headline |
|---|---|---|---|
| **control** | Current | English default | `Get paid globally— 10x cheaper than Payoneer` |
| **A** | Benefit-first | Personal benefit | `Kendi ABD Hesabın, 3 Dakikada Hazır` |
| **B** | Comparison-first | Loss aversion | `Payoneer'a Yılda 756$ Ödemeyi Bırak` |
| **C** | Social-proof | Trust / bandwagon | `500.000+ Profesyonel Cenoa'yı Tercih Etti` |

### Variant Copy Detail

#### Control (current hero — no changes)
Serve existing English hero as-is to 25% of TR traffic.

#### Variant A — Benefit-First

```
Headline:    Kendi ABD Hesabın, 3 Dakikada Hazır
Subheadline: Dünyanın her yerinden ödeme al. Ücretler %1'in altında — geri kalanı senin.
CTA:         Ücretsiz Hesap Aç

Bullets:
• 💰 %1'in altında toplam ücret — gizli kesinti yok, gördüğün fiyat son fiyat
• ⚡ 3 dakikada hesap aç — KYC doğrulaması dahil, aynı gün ödeme almaya başla
• 🔒 Stripe + Lead Bank altyapısı — Amazon ve Shopify'ın kullandığı ödeme altyapısıyla güvende
```

#### Variant B — Comparison-First

```
Headline:    Payoneer'a Yılda 756$ Ödemeyi Bırak
Subheadline: Aynı USD hesap, %70 daha düşük ücret. Freelancer'lar için tasarlandı — geçiş 3 dakika.
CTA:         Ne Kadar Tasarruf Edeceğini Gör

Bullets:
• 📉 Payoneer: toplam ~%3 kesinti (alma ücreti + kur farkı) → Cenoa: <%1 hepsi dahil
• 💵 Aylık 3.000$ kazanan freelancer yılda 756$ tasarruf eder — yeni ekipman veya tatil parası
• 🚀 Payoneer hesabını kapatma — Cenoa'yı dene, farkı gör, sonra karar ver
```

#### Variant C — Social Proof

```
Headline:    500.000+ Profesyonel Cenoa'yı Tercih Etti
Subheadline: "Payoneer'dan geçtim, yıllık 900$ tasarruf ediyorum." — Elif, İstanbul'da freelance yazılımcı
CTA:         Sen de Katıl — Ücretsiz Başla

Bullets:
• 🌍 35+ ülkeden 500.000+ kullanıcı — Türkiye'den binlerce freelancer aktif
• ⭐ App Store'da 4.8 puan — gerçek kullanıcılardan 2.300+ değerlendirme
• 🏦 Stripe & Lead Bank güvencesi — paranız FDIC sigortalı bir ABD bankasında
```

---

## 3. Variant Assignment — JavaScript Implementation

Google Optimize is sunset. Recommended approach: **lightweight custom JS** (no third-party tool dependency).

### Assignment Logic

```javascript
/**
 * TR LP A/B Test — Variant Assignment
 * Test ID: TR_LP_AB_2026Q1
 * 
 * Place in <head> BEFORE any hero rendering.
 * Runs only for TR-geo visitors (gated by geo check).
 */
(function () {
  var COOKIE_NAME = 'tr_lp_variant';
  var COOKIE_DAYS = 90; // persist assignment for test duration + buffer
  var VARIANTS = ['control', 'A', 'B', 'C'];

  // --- Read existing assignment from cookie ---
  function getCookie(name) {
    var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
  }

  // --- Write cookie ---
  function setCookie(name, value, days) {
    var d = new Date();
    d.setTime(d.getTime() + days * 86400000);
    document.cookie = name + '=' + value +
      ';expires=' + d.toUTCString() +
      ';path=/;SameSite=Lax;Secure';
  }

  // --- Deterministic assignment via FNV-1a hash of fingerprint ---
  // Using a simple hash instead of Math.random() for consistency
  // if cookies are cleared mid-session.
  function fnv1a(str) {
    var hash = 0x811c9dc5;
    for (var i = 0; i < str.length; i++) {
      hash ^= str.charCodeAt(i);
      hash = (hash * 0x01000193) >>> 0;
    }
    return hash;
  }

  function assignVariant() {
    var existing = getCookie(COOKIE_NAME);
    if (existing && VARIANTS.indexOf(existing) !== -1) {
      return existing;
    }

    // Generate a semi-stable fingerprint for assignment
    // (screen size + timezone + language + random salt for first-timers)
    var fp = [
      screen.width, screen.height, screen.colorDepth,
      new Date().getTimezoneOffset(),
      navigator.language,
      Math.random().toString(36).substr(2, 8)
    ].join('|');

    var hash = fnv1a(fp);
    var variant = VARIANTS[hash % 4];

    setCookie(COOKIE_NAME, variant, COOKIE_DAYS);
    return variant;
  }

  // --- Expose variant globally ---
  window.__TR_LP_VARIANT = assignVariant();

  // --- Set body attribute for CSS-based show/hide ---
  document.documentElement.setAttribute('data-lp-variant', window.__TR_LP_VARIANT);
})();
```

### Why Cookie (not sessionStorage)

- Persists across sessions — user sees same variant on return visits
- Readable server-side if SSR is added later
- Survives tab close / browser restart
- 90-day expiry covers full test duration

### Alternative: Hash-Based Assignment (if user IDs available)

If the visitor has a user_id (e.g., from a logged-in state or UTM parameter):

```javascript
// Deterministic: same user always sees same variant
var variant = VARIANTS[fnv1a(user_id) % 4];
```

Use cookie-based for anonymous visitors (majority of LP traffic).

---

## 4. Geo-Targeting (TR-only)

Variants are shown **only to Turkish-geo visitors**. All others see the current English hero unchanged.

### Option A — Cloudflare Header (Recommended)

```javascript
// In Webflow custom code or edge worker:
// Cloudflare sets CF-IPCountry header automatically
// Use a Cloudflare Worker to inject a JS variable:

// cloudflare-worker.js
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const response = await fetch(request);
  const country = request.headers.get('CF-IPCountry') || 'XX';
  
  // Inject country code into HTML <head>
  const html = await response.text();
  const injected = html.replace(
    '</head>',
    `<script>window.__GEO_COUNTRY="${country}";</script></head>`
  );
  
  return new Response(injected, {
    headers: response.headers
  });
}
```

### Option B — Client-Side Geo API (Fallback)

```javascript
// If Cloudflare Worker is not feasible:
fetch('https://ipapi.co/country/')
  .then(r => r.text())
  .then(country => {
    window.__GEO_COUNTRY = country.trim();
    if (country.trim() === 'TR') initABTest();
  });
```

### Gate Logic

```javascript
// Only initialize A/B test for TR visitors
if (window.__GEO_COUNTRY === 'TR') {
  // Run variant assignment + hero swap
  initABTest();
} else {
  // Show default English hero — do nothing
  document.documentElement.setAttribute('data-lp-variant', 'default');
}
```

---

## 5. Webflow Hero Swap Implementation

### Approach: CSS Show/Hide with `data-lp-variant`

Create all 4 hero sections in Webflow. Use CSS to show only the assigned variant.

#### HTML Structure (Webflow components)

```html
<section class="hero-section" data-variant="control">
  <!-- Current English hero — unchanged -->
</section>

<section class="hero-section" data-variant="A">
  <h1>Kendi ABD Hesabın, 3 Dakikada Hazır</h1>
  <p>Dünyanın her yerinden ödeme al. Ücretler %1'in altında — geri kalanı senin.</p>
  <a class="hero-cta" href="#" data-cta-text="Ücretsiz Hesap Aç">Ücretsiz Hesap Aç</a>
  <ul class="hero-bullets">
    <li>💰 <strong>%1'in altında toplam ücret</strong> — gizli kesinti yok, gördüğün fiyat son fiyat</li>
    <li>⚡ <strong>3 dakikada hesap aç</strong> — KYC doğrulaması dahil, aynı gün ödeme almaya başla</li>
    <li>🔒 <strong>Stripe + Lead Bank altyapısı</strong> — Amazon ve Shopify'ın kullandığı ödeme altyapısıyla güvende</li>
  </ul>
</section>

<section class="hero-section" data-variant="B">
  <h1>Payoneer'a Yılda 756$ Ödemeyi Bırak</h1>
  <p>Aynı USD hesap, %70 daha düşük ücret. Freelancer'lar için tasarlandı — geçiş 3 dakika.</p>
  <a class="hero-cta" href="#" data-cta-text="Ne Kadar Tasarruf Edeceğini Gör">Ne Kadar Tasarruf Edeceğini Gör</a>
  <ul class="hero-bullets">
    <li>📉 <strong>Payoneer: toplam ~%3 kesinti</strong> (alma ücreti + kur farkı) → <strong>Cenoa: &lt;%1 hepsi dahil</strong></li>
    <li>💵 <strong>Aylık 3.000$ kazanan freelancer yılda 756$ tasarruf eder</strong> — yeni ekipman veya tatil parası</li>
    <li>🚀 <strong>Payoneer hesabını kapatma</strong> — Cenoa'yı dene, farkı gör, sonra karar ver</li>
  </ul>
</section>

<section class="hero-section" data-variant="C">
  <h1>500.000+ Profesyonel Cenoa'yı Tercih Etti</h1>
  <p>"Payoneer'dan geçtim, yıllık 900$ tasarruf ediyorum." — Elif, İstanbul'da freelance yazılımcı</p>
  <a class="hero-cta" href="#" data-cta-text="Sen de Katıl — Ücretsiz Başla">Sen de Katıl — Ücretsiz Başla</a>
  <ul class="hero-bullets">
    <li>🌍 <strong>35+ ülkeden 500.000+ kullanıcı</strong> — Türkiye'den binlerce freelancer aktif</li>
    <li>⭐ <strong>App Store'da 4.8 puan</strong> — gerçek kullanıcılardan 2.300+ değerlendirme</li>
    <li>🏦 <strong>Stripe &amp; Lead Bank güvencesi</strong> — paranız FDIC sigortalı bir ABD bankasında</li>
  </ul>
</section>
```

#### CSS (Webflow Custom Code → `<head>`)

```css
/* Hide all hero variants by default — prevents FOUC */
.hero-section[data-variant] {
  display: none !important;
}

/* Show only the assigned variant */
[data-lp-variant="control"] .hero-section[data-variant="control"],
[data-lp-variant="A"] .hero-section[data-variant="A"],
[data-lp-variant="B"] .hero-section[data-variant="B"],
[data-lp-variant="C"] .hero-section[data-variant="C"],
[data-lp-variant="default"] .hero-section[data-variant="control"] {
  display: block !important;
}
```

> **Critical:** The variant assignment JS (Section 3) MUST run in `<head>` before DOM renders. This sets `data-lp-variant` on `<html>`, and CSS handles visibility with zero layout shift.

#### Layout Consistency

- All 4 hero sections MUST have **identical dimensions** (height, padding, CTA button size/position)
- CTA buttons: same size, same position, same color — only text changes
- Bullet section: same layout grid, same icon sizing
- Test copy changes only — not design changes

---

## 6. GA4 Event Tracking

### 6.1 Variant Impression Event

Fire **once per session** when the hero section enters the viewport.

```javascript
// Place after variant assignment in <head> or early <body>
(function () {
  var fired = false;

  function fireImpression() {
    if (fired) return;
    fired = true;

    var variant = window.__TR_LP_VARIANT;
    if (!variant || variant === 'default') return;

    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: 'lp_variant_impression',
      test_id: 'TR_LP_AB_2026Q1',
      variant_id: variant,
      page_path: window.location.pathname,
      traffic_source: document.referrer || 'direct',
      device_type: /Mobile|Android|iPhone/i.test(navigator.userAgent) ? 'mobile' : 'desktop',
      geo: 'TR',
      language: 'tr',
      timestamp: new Date().toISOString()
    });
  }

  // Fire on DOMContentLoaded (hero is above fold, always visible)
  if (document.readyState !== 'loading') {
    fireImpression();
  } else {
    document.addEventListener('DOMContentLoaded', fireImpression);
  }
})();
```

### 6.2 CTA Click Event

Fire on **every hero CTA button click**.

```javascript
// Delegate click handler for all hero CTAs
document.addEventListener('click', function (e) {
  var cta = e.target.closest('.hero-cta');
  if (!cta) return;

  var variant = window.__TR_LP_VARIANT;
  if (!variant || variant === 'default') return;

  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    event: 'cta_click',
    test_id: 'TR_LP_AB_2026Q1',
    variant_id: variant,
    cta_text: cta.getAttribute('data-cta-text') || cta.textContent.trim(),
    cta_position: 'hero_above_fold',
    page_path: window.location.pathname
  });
});
```

### 6.3 GTM Configuration

Create the following in Google Tag Manager:

| GTM Element | Type | Details |
|---|---|---|
| **Trigger:** `lp_variant_impression` | Custom Event | Event name = `lp_variant_impression` |
| **Trigger:** `cta_click` | Custom Event | Event name = `cta_click` |
| **Tag:** GA4 Impression | GA4 Event | Event = `lp_variant_impression`, params: `test_id`, `variant_id`, `device_type`, `geo` |
| **Tag:** GA4 CTA Click | GA4 Event | Event = `cta_click`, params: `test_id`, `variant_id`, `cta_text`, `cta_position` |
| **DL Variable:** `variant_id` | Data Layer Variable | Variable name = `variant_id` |
| **DL Variable:** `test_id` | Data Layer Variable | Variable name = `test_id` |
| **DL Variable:** `cta_text` | Data Layer Variable | Variable name = `cta_text` |
| **DL Variable:** `device_type` | Data Layer Variable | Variable name = `device_type` |

### 6.4 GA4 Custom Dimensions (Admin → Custom Definitions)

| Dimension Name | Scope | Event Parameter |
|---|---|---|
| `test_variant` | Session | `variant_id` |
| `test_id` | Session | `test_id` |
| `device_type` | Event | `device_type` |

### 6.5 Supporting Events (Optional — Nice to Have)

| Event | Trigger | Parameters |
|---|---|---|
| `hero_scroll_past` | IntersectionObserver: hero exits viewport | `variant_id`, `time_on_hero_ms` |
| `bounce_from_hero` | `beforeunload` without CTA click or scroll | `variant_id`, `time_to_bounce_ms` |

---

## 7. CTA → App Store Routing with Attribution

```javascript
// Attach to all .hero-cta buttons
document.addEventListener('click', function (e) {
  var cta = e.target.closest('.hero-cta');
  if (!cta) return;

  e.preventDefault();

  var variant = window.__TR_LP_VARIANT || 'unknown';
  var isIOS = /iPhone|iPad|iPod/i.test(navigator.userAgent);

  // Replace with actual store URLs
  var storeBase = isIOS
    ? 'https://apps.apple.com/app/cenoa/id1234567890'
    : 'https://play.google.com/store/apps/details?id=com.cenoa.app';

  var url = new URL(storeBase);
  url.searchParams.set('utm_source', 'website');
  url.searchParams.set('utm_medium', 'lp_ab_test');
  url.searchParams.set('utm_campaign', 'TR_LP_AB_2026Q1');
  url.searchParams.set('utm_content', 'variant_' + variant);

  // Fire GA4 event, then redirect after brief delay
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    event: 'cta_click',
    test_id: 'TR_LP_AB_2026Q1',
    variant_id: variant,
    cta_text: cta.getAttribute('data-cta-text') || cta.textContent.trim(),
    cta_position: 'hero_above_fold',
    page_path: window.location.pathname
  });

  // 150ms delay ensures GA4 event fires before navigation
  setTimeout(function () {
    window.location.href = url.toString();
  }, 150);
});
```

### Amplitude Post-Install Attribution

The `utm_content=variant_A|B|C|control` parameter carries through to app install. On first app open, map to Amplitude user property:

```
User Property: lp_variant → "A" | "B" | "C" | "control"
User Property: lp_test_id → "TR_LP_AB_2026Q1"
```

This enables full-funnel analysis: LP impression → CTA click → Install → Signup → KYC → First Deposit.

---

## 8. Statistical Design

| Parameter | Value |
|---|---|
| **Baseline conversion (LP → Install)** | 14.72% (GA4, Mar 14–20) |
| **Minimum Detectable Effect** | 2.28 pp (→ 17.0%) |
| **Significance level** | α = 0.05 |
| **Bonferroni correction** | α/3 = 0.0167 per comparison (3 treatments vs control) |
| **Power** | 80% |
| **Tails** | Two-tailed |
| **Sample per variant** | ~4,200 visitors |
| **Total sample (4 variants)** | ~16,800 visitors |
| **Current weekly TR traffic** | ~2,500 sessions |
| **Estimated duration** | 5–6 weeks (at 25% split = ~625/variant/week) |
| **Hard minimum** | 2 full weeks (day-of-week coverage) |

### Success Metric

**Primary:** LP → Install conversion rate (CTA click → app store → install)  
**Secondary:** CTA click-through rate (impression → CTA click)

### Guardrails

- **Stop early if:** Any variant bounce rate > 75% for 3+ consecutive days
- **No peeking before:** 2 weeks minimum AND 1,500 visitors per variant
- **Winner threshold:** p < 0.0167 (Bonferroni) AND ≥ 1.5pp practical lift
- **If no winner at 6 weeks:** Declare inconclusive, pick directional winner for iteration

---

## 9. Tool Options (A/B Testing Platform)

| Option | Pros | Cons | Recommendation |
|---|---|---|---|
| **Manual JS (this spec)** | Zero cost, full control, no third-party dependency | Manual analysis, no visual editor | ✅ **Recommended** |
| **VWO Lite** | Visual editor, built-in stats | Paid (~$99/mo), adds script weight | Consider if dev bandwidth is tight |
| **Optimizely Web** | Robust stats engine | Expensive (~$36k/yr), overkill | ❌ Not for this test |
| **Google Optimize** | Free, GA4 native | ❌ **Sunset Sept 2023** — unavailable | ❌ Dead |
| **PostHog** | Free tier, feature flags | Requires PostHog setup | Future option |

**Decision:** Use manual JS implementation (this spec). Simple 4-way split with cookie persistence. Analysis via GA4 + BigQuery.

---

## 10. QA Checklist — Pre-Launch

### Functional

- [ ] **Variant assignment works:** Refresh page 20+ times, verify ~25% distribution across 4 variants (check cookie values)
- [ ] **Cookie persists:** Assign variant → close browser → reopen → same variant shown
- [ ] **Geo gate works:** VPN to non-TR country → default English hero shown (no test)
- [ ] **Geo gate works:** VPN to Turkey → test variant shown
- [ ] **All 4 heroes render:** Force each variant via cookie override (`document.cookie = "tr_lp_variant=A"`) and verify

### Visual / Layout

- [ ] **Mobile (375px):** All 4 variants render correctly on iPhone SE / Android small screen
- [ ] **Desktop (1440px):** All 4 variants render correctly
- [ ] **Tablet (768px):** All 4 variants render correctly
- [ ] **No FOUC:** Hero loads without visible flash/swap (test on throttled 3G connection)
- [ ] **No CLS:** Cumulative Layout Shift < 0.1 (Chrome DevTools → Lighthouse)
- [ ] **Turkish characters:** ş, ç, ö, ü, ğ, ı, İ render correctly in all variants + all font weights
- [ ] **CTA button size:** Identical dimensions across all 4 variants (pixel-check)
- [ ] **Bullet alignment:** Consistent across variants

### Tracking

- [ ] **GA4 DebugView:** `lp_variant_impression` fires with correct `variant_id` on page load
- [ ] **GA4 DebugView:** `cta_click` fires with correct `variant_id` + `cta_text` on CTA click
- [ ] **No duplicate impressions:** Refresh page — only 1 impression event per session
- [ ] **UTM passthrough:** Click CTA → verify app store URL contains `utm_content=variant_X`
- [ ] **GTM Preview:** All tags fire in correct order (impression → click)
- [ ] **GA4 Realtime:** Events appear in GA4 Realtime report within 30 seconds

### Edge Cases

- [ ] **Cookie blocked:** If user blocks cookies, variant still assigned (falls back to random per-pageview)
- [ ] **Bot traffic:** Googlebot / crawlers → serve control variant (or no test) to avoid SEO issues
- [ ] **Multiple tabs:** Open 2 tabs simultaneously → same variant in both
- [ ] **Incognito mode:** New assignment on first visit, consistent within session
- [ ] **Page speed:** Measure LCP with test code vs without — delta should be < 100ms

### Legal / Compliance

- [ ] **Variant C testimonial:** Confirm "Elif, İstanbul'da freelance yazılımcı" has user consent on file
- [ ] **Savings claims:** Variant B "$756/year" calculation documented and defensible
- [ ] **App Store guidelines:** CTA redirects comply with Apple/Google linking policies

---

## 11. Rollout Plan

| Phase | Duration | Traffic | Deliverable |
|---|---|---|---|
| **Dev build** | 3–4 days | — | All 4 hero sections + JS + CSS |
| **GTM setup** | 1 day | — | Tags, triggers, variables configured |
| **QA** | 1–2 days | Internal only | Full checklist passed |
| **Soft launch** | 2 days | 5% TR traffic | Verify events fire, no errors in console |
| **Full launch** | 5–6 weeks | 100% TR traffic (25% × 4) | Test runs to significance |
| **Analysis** | 2–3 days | — | Winner declared |
| **Winner deploy** | 1 day | 100% TR traffic | Winning variant becomes permanent hero |

### Estimated Timeline

- **Dev start:** Sprint 064 (week of Mar 30)
- **Soft launch:** Apr 4–5
- **Full launch:** Apr 7
- **Expected winner call:** Mid-May 2026

---

## 12. Post-Test Analysis Plan

1. Export GA4 data via BigQuery: `lp_variant_impression` + `cta_click` events
2. Calculate per-variant: impressions, CTA clicks, CTR, installs (from Amplitude attribution)
3. Run chi-squared test with Bonferroni correction (α = 0.0167 per comparison)
4. Segment analysis: mobile vs desktop, SEM vs organic, new vs returning
5. Document in `tr-lp-ab-results.md`

### BigQuery Query Template

```sql
-- LP A/B Test Results
SELECT
  ep.value.string_value AS variant_id,
  COUNT(DISTINCT CASE WHEN event_name = 'lp_variant_impression' THEN user_pseudo_id END) AS impressions,
  COUNT(DISTINCT CASE WHEN event_name = 'cta_click' THEN user_pseudo_id END) AS cta_clicks,
  SAFE_DIVIDE(
    COUNT(DISTINCT CASE WHEN event_name = 'cta_click' THEN user_pseudo_id END),
    COUNT(DISTINCT CASE WHEN event_name = 'lp_variant_impression' THEN user_pseudo_id END)
  ) AS ctr
FROM `cenoa-marketingdatawarehouse.analytics_XXXXXXX.events_*`,
  UNNEST(event_params) AS ep
WHERE
  ep.key = 'variant_id'
  AND _TABLE_SUFFIX BETWEEN '20260407' AND '20260518'
  AND event_name IN ('lp_variant_impression', 'cta_click')
GROUP BY variant_id
ORDER BY ctr DESC;
```

---

## File Reference

| File | Description |
|---|---|
| `tr-lp-ab-variants.md` | Copy variants, hypotheses, predictions (S2B-014) |
| `lp-ab-test-implementation.md` | This file — developer implementation spec (S3-024) |
| `lp-cta-optimization.md` | Baseline data + test framework |
| `ab-test-framework.md` | Statistical methodology |

---

*Created: 2026-03-23 | S3-024*  
*Source: tr-lp-ab-variants.md (S2B-014)*
