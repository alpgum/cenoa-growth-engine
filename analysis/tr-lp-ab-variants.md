# Turkish Landing Page A/B Test — Hero Variants

**Sprint:** 063  
**Ticket:** S2B-014  
**Date:** 2026-03-22  
**Owner:** Growth / Performance Marketing  
**Status:** Ready for implementation  
**Target:** cenoa.com Turkish visitors (TR geo)

---

## Test Overview

Three hero section variants targeting Turkish freelancers and remote workers. Each variant tests a different psychological hook as the primary conversion lever.

- **Baseline CTA rate:** 14.72% (cenoa.com homepage, Mar 14–20)
- **Target CTA rate:** 17–20%
- **Traffic split:** 33/33/34 (equal distribution, no control — all three are new)

---

## Variant A: Benefit-First (Fayda Odaklı)

### Hypothesis
Turkish freelancers primarily care about *what they get*, not who they're switching from. Leading with a tangible, personal benefit ("your own US account") creates immediate relevance and reduces cognitive load. This mirrors Wise's successful "The international account" approach — simple, benefit-driven, zero competitor mentions.

### Hero Copy

**Headline:**  
`Kendi ABD Hesabın, 3 Dakikada Hazır`

**Subheadline:**  
`Dünyanın her yerinden ödeme al. Ücretler %1'in altında — geri kalanı senin.`

**CTA Button:**  
`Ücretsiz Hesap Aç`

**3 Bullets:**  
- 💰 **%1'in altında toplam ücret** — gizli kesinti yok, gördüğün fiyat son fiyat  
- ⚡ **3 dakikada hesap aç** — KYC doğrulaması dahil, aynı gün ödeme almaya başla  
- 🔒 **Stripe + Lead Bank altyapısı** — Amazon ve Shopify'ın kullandığı ödeme altyapısıyla güvende

### Why It Might Win
- Removes comparison fatigue — user doesn't need to know Payoneer to understand value
- "3 dakikada" is a concrete speed anchor that creates urgency
- "Ücretsiz" in CTA eliminates price anxiety (biggest barrier in TR fintech adoption)
- Works for both Payoneer-aware AND unaware audiences (broader net)

---

## Variant B: Comparison-First — Tasarruf Odaklı (vs Payoneer/Wise)

### Hypothesis
A significant portion of Turkish freelancer traffic arrives with existing Payoneer/Wise frustration (search intent: "payoneer alternatif", "payoneer komisyon"). Leading with a direct savings comparison activates loss aversion — the most powerful conversion trigger in behavioral economics. The Egypt Architect LP test showed 27% cheaper CTA cost with localized, specific messaging.

### Hero Copy

**Headline:**  
`Payoneer'a Yılda 756$ Ödemeyi Bırak`

**Subheadline:**  
`Aynı USD hesap, %70 daha düşük ücret. Freelancer'lar için tasarlandı — geçiş 3 dakika.`

**CTA Button:**  
`Ne Kadar Tasarruf Edeceğini Gör`

**3 Bullets:**  
- 📉 **Payoneer: toplam ~%3 kesinti** (alma ücreti + kur farkı) → **Cenoa: <%1 hepsi dahil**  
- 💵 **Aylık 3.000$ kazanan freelancer yılda 756$ tasarruf eder** — yeni ekipman veya tatil parası  
- 🚀 **Payoneer hesabını kapat*ma*** — Cenoa'yı dene, farkı gör, sonra karar ver

### Why It Might Win
- "$756/yıl" is a concrete, painful number — Turkish freelancers earning in USD are hyper-cost-sensitive
- Loss aversion framing ("ödemeyi bırak") is 2x more motivating than equivalent gain framing
- "Ne Kadar Tasarruf Edeceğini Gör" CTA implies personalization, increasing click curiosity
- "Kapatma" bullet reduces switching anxiety — the #1 objection for Payoneer users
- Directly captures "payoneer alternatif" search intent (strong SEO/SEM alignment)

---

## Variant C: Social Proof-First (Sosyal Kanıt Odaklı)

### Hypothesis
Turkish users exhibit high uncertainty avoidance (Hofstede cultural dimension: Turkey scores 85/100 on Uncertainty Avoidance). Social proof — especially from peers in the same country — is the #1 trust signal. Leading with user count + a relatable testimonial reduces the "is this legit?" barrier that kills fintech conversion in Turkey. Fintech studies show social proof above the fold lifts conversion 10–15%.

### Hero Copy

**Headline:**  
`500.000+ Profesyonel Cenoa'yı Tercih Etti`

**Subheadline:**  
`"Payoneer'dan geçtim, yıllık 900$ tasarruf ediyorum." — Elif, İstanbul'da freelance yazılımcı`

**CTA Button:**  
`Sen de Katıl — Ücretsiz Başla`

**3 Bullets:**  
- 🌍 **35+ ülkeden 500.000+ kullanıcı** — Türkiye'den binlerce freelancer aktif  
- ⭐ **App Store'da 4.8 puan** — gerçek kullanıcılardan 2.300+ değerlendirme  
- 🏦 **Stripe & Lead Bank güvencesi** — paranız FDIC sigortalı bir ABD bankasında

### Why It Might Win
- Turkey's high uncertainty avoidance means "others trust it" > "it's cheap"
- Named testimonial with city (İstanbul) creates geographic proximity and relatability
- "Sen de Katıl" leverages bandwagon effect — implies joining a movement, not just signing up
- App Store rating is a verifiable, third-party trust signal (user can check instantly)
- Combines three trust layers: peer count + named testimonial + institutional backing

---

## GA4 Measurement Setup

### Event Schema

All events fire via GTM (Google Tag Manager) dataLayer push.

#### 1. Variant Impression Event

```javascript
// Fire once per session when hero section enters viewport
dataLayer.push({
  event: 'lp_variant_impression',
  test_id: 'TR_LP_AB_2026Q1',
  variant_id: 'A' | 'B' | 'C',
  page_path: window.location.pathname,
  traffic_source: document.referrer || 'direct',
  device_type: /Mobile|Android|iPhone/.test(navigator.userAgent) ? 'mobile' : 'desktop',
  geo: 'TR',
  language: 'tr',
  timestamp: new Date().toISOString()
});
```

#### 2. CTA Click Event

```javascript
// Fire on primary CTA button click
dataLayer.push({
  event: 'cta_click',
  test_id: 'TR_LP_AB_2026Q1',
  variant_id: 'A' | 'B' | 'C',
  cta_text: 'Ücretsiz Hesap Aç' | 'Ne Kadar Tasarruf Edeceğini Gör' | 'Sen de Katıl — Ücretsiz Başla',
  cta_position: 'hero_above_fold',
  page_path: window.location.pathname,
  session_id: ga4_session_id // from GA4 cookie
});
```

#### 3. Supporting Events

| Event Name | Trigger | Parameters |
|---|---|---|
| `hero_scroll_past` | User scrolls past hero section | `variant_id`, `time_on_hero_ms` |
| `bullet_hover` | User hovers on a bullet point >1s | `variant_id`, `bullet_index` |
| `app_store_redirect` | Device-detected redirect fires | `variant_id`, `store` (ios/android) |
| `bounce_from_hero` | Session ends without scroll or CTA | `variant_id`, `time_to_bounce_ms` |

### GA4 Custom Dimensions

| Dimension | Scope | Value |
|---|---|---|
| `test_variant` | Session | A / B / C |
| `test_id` | Session | TR_LP_AB_2026Q1 |
| `variant_impression_time` | Event | ISO timestamp |

### Amplitude Attribution (Post-Install)

Pass `utm_content=variant_A|B|C` in the app store redirect URL. Map to Amplitude user property `lp_variant` on first app open for full-funnel attribution through signup → KYC → first deposit.

---

## Statistical Requirements

### Sample Size Calculation

| Parameter | Value | Source |
|---|---|---|
| **Baseline conversion rate** | 14.72% | GA4, Mar 14–20, 2026 |
| **Minimum Detectable Effect (MDE)** | 2.28 pp (→ 17.0%) | Business target: meaningful CTA lift |
| **Statistical significance** | 95% (α = 0.05) | Industry standard |
| **Bonferroni correction** | α/3 = 0.0167 per variant | 3-way comparison adjustment |
| **Statistical power** | 80% (β = 0.20) | Standard |
| **Tails** | Two-tailed | Conservative — detect improvement or degradation |

### Required Sample

Using Bonferroni-corrected α = 0.0167:

| Metric | Value |
|---|---|
| **Sample per variant** | ~4,200 visitors |
| **Total sample (3 variants)** | ~12,600 visitors |
| **Current weekly TR traffic (est.)** | ~2,500 sessions (homepage) |
| **Minimum test duration** | 5 weeks (to reach sample) |
| **Hard minimum** | 2 full weeks (day-of-week + weekend effects) |
| **Recommended duration** | 5–6 weeks |

### Guardrails

- **Stop test early if:** Any variant's bounce rate exceeds 75% for 3+ consecutive days (guardrail alert)
- **Don't peek before:** 2 weeks minimum / 1,500 visitors per variant
- **Winner threshold:** p < 0.0167 (Bonferroni-corrected) AND practically significant (≥1.5pp lift)
- **If no winner at 6 weeks:** Declare inconclusive, pick directional winner for next iteration

### Power Note
With ~2,500 weekly TR homepage sessions, 5 weeks = ~12,500 sessions total. If TR traffic is lower than estimated, consider:
1. Boosting paid TR traffic during test period
2. Reducing to 2 variants (A vs B) to reach significance faster (~3,500/variant)

---

## Expected Winner Prediction

### Prediction: **Variant B (Comparison-First) wins** — 55% confidence

### Reasoning

1. **Search intent alignment:** A large portion of Turkish cenoa.com traffic likely arrives from "payoneer alternatif" or "payoneer komisyon" queries. Variant B directly mirrors this intent — the headline answers what they're already thinking.

2. **Egypt precedent:** The Architect LP test in Egypt showed 27% cheaper CTA cost with localized, specific messaging. Variant B is the most specific — it names the competitor, quantifies savings, and localizes for the Turkish freelancer persona.

3. **Loss aversion > benefit framing:** Behavioral economics consistently shows that "stop losing $756" outperforms "save money" by 1.5–2x in click-through. Turkish freelancers earning in USD are acutely aware of fee erosion due to lira depreciation making every dollar more valuable.

4. **CTA curiosity gap:** "Ne Kadar Tasarruf Edeceğini Gör" creates a personalization hook — the user wants to calculate their own savings, driving higher intent clicks.

### Runner-up: Variant C (Social Proof) — 30% confidence
Turkey's high uncertainty avoidance could make social proof the deciding factor, especially for users who *don't* arrive with competitive intent. If organic/direct traffic dominates over search, Variant C could outperform.

### Underdog: Variant A (Benefit-First) — 15% confidence
Clean and universal, but may lack the emotional punch needed to disrupt the default behavior (staying with current provider or bouncing). Best as a long-term winner if Cenoa moves away from competitor-based positioning.

### Segment-Level Predictions

| Segment | Predicted Winner | Reasoning |
|---|---|---|
| SEM traffic ("payoneer alternatif") | **Variant B** | Direct intent match |
| Organic/direct visitors | **Variant C** | Trust-first for cold traffic |
| Mobile users | **Variant A** | Shorter copy, faster scan |
| Returning visitors | **Variant B** | Already aware, need push to act |

---

## Implementation Notes for Developer

### 1. Variant Assignment Logic

```javascript
// Assign variant on first pageview, persist in session storage + GA4
function assignVariant() {
  const stored = sessionStorage.getItem('tr_lp_variant');
  if (stored) return stored;
  
  const rand = Math.random();
  let variant;
  if (rand < 0.333) variant = 'A';
  else if (rand < 0.666) variant = 'B';
  else variant = 'C';
  
  sessionStorage.setItem('tr_lp_variant', variant);
  return variant;
}
```

### 2. Content Swap Method

- **Recommended:** Server-side rendering based on cookie/session (no flash of unstyled content)
- **Alternative:** Client-side swap via JS — hide hero on load, swap content, reveal (add `opacity: 0` → `1` transition to prevent FOUC)
- **Do NOT** use `display: none` toggling — causes CLS (Cumulative Layout Shift) penalty

### 3. Webflow Implementation

If using Webflow:
- Create 3 hero section components: `hero-variant-a`, `hero-variant-b`, `hero-variant-c`
- Use Webflow's custom code embed to run assignment logic in `<head>`
- Apply `data-variant="A|B|C"` to `<body>`, use CSS to show/hide correct hero
- Ensure all 3 hero sections have identical dimensions to prevent layout shift

### 4. CTA Routing

```javascript
// Single CTA button → device-aware app store redirect
document.querySelector('.hero-cta').addEventListener('click', () => {
  const variant = sessionStorage.getItem('tr_lp_variant');
  const isIOS = /iPhone|iPad|iPod/.test(navigator.userAgent);
  const storeUrl = isIOS 
    ? 'https://apps.apple.com/app/cenoa/id...' 
    : 'https://play.google.com/store/apps/details?id=...';
  
  // Append variant for attribution
  const url = new URL(storeUrl);
  url.searchParams.set('utm_content', `variant_${variant}`);
  url.searchParams.set('utm_campaign', 'TR_LP_AB_2026Q1');
  
  // Fire GA4 event before redirect
  dataLayer.push({
    event: 'cta_click',
    variant_id: variant,
    cta_position: 'hero_above_fold'
  });
  
  setTimeout(() => window.location.href = url.toString(), 150);
});
```

### 5. Geo-Targeting

- Show variants **only to TR-geo visitors** (detect via Cloudflare `CF-IPCountry` header or MaxMind)
- Non-TR visitors see current default homepage (no test contamination)
- Log geo-detection method in `lp_variant_impression` event for debugging

### 6. QA Checklist

- [ ] All 3 variants render correctly on mobile (375px) and desktop (1440px)
- [ ] CTA buttons have identical size/placement across variants (isolate copy effect)
- [ ] Turkish characters (ş, ç, ö, ü, ğ, ı, İ) render correctly in all fonts
- [ ] No layout shift when variant loads (CLS < 0.1)
- [ ] GA4 events fire correctly for each variant (test with GA4 DebugView)
- [ ] Session persistence works (same variant on page refresh/return)
- [ ] UTM parameters carry through to app store redirect
- [ ] Variant B savings calculator link works (if implementing inline calculator)
- [ ] Testimonial in Variant C has user consent documentation on file

### 7. Accessibility

- All CTA buttons: `role="button"`, proper `aria-label` in Turkish
- Bullet icons: decorative only, use `aria-hidden="true"`
- Color contrast: CTA button meets WCAG AA (4.5:1 minimum)
- Headline hierarchy: `<h1>` for headline, `<p>` for subheadline

---

## Timeline

| Phase | Duration | Deliverable |
|---|---|---|
| **Dev implementation** | 3–4 days | All 3 variants built + QA'd |
| **GTM setup** | 1 day | Events configured + tested in DebugView |
| **Soft launch (5% traffic)** | 2 days | Verify events fire, no bugs |
| **Full launch (100% TR traffic)** | 5–6 weeks | Test runs to statistical significance |
| **Analysis + decision** | 2–3 days | Winner declared, losing variants archived |

**Estimated start:** Sprint 064 (Week of Mar 30)  
**Estimated winner call:** Mid-May 2026

---

*Cross-references:*
- *[LP CTA Optimization Brief](./lp-cta-optimization.md) — baseline data + test framework*
- *[Competitive Positioning](./competitive-positioning.md) — messaging pillars*
- *[Cenoa vs Payoneer Comparison](./cenoa-vs-payoneer-comparison.md) — fee data*
- *[A/B Test Framework](./ab-test-framework.md) — statistical methodology*

*Created: 2026-03-22 | S2B-014*
