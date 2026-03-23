# Competitor Ad Monitoring (Payoneer / Wise / Deel)

Goal: spot **new hooks, offers, landing-page patterns, and geo focus** before they show up in our performance metrics.

This doc is intentionally **tool-first + repeatable** (weekly cadence), with a lightweight baseline scan.

---

## 1) What we monitor (signals)
Track these for every competitor ad you log:
- **Hook/angle** (first 1–2 seconds / first line)
- **Offer** (pricing, promos, free account, cashback, etc.)
- **ICP** (freelancers, remote workers, SMBs, creators)
- **Geo/language** (TR / NG / EG / PK; English vs local language)
- **Format** (UGC talking head, animation, testimonial, comparison, product demo)
- **CTA** (Open account, Get paid, Receive USD, Send money)
- **Landing page** (domain + key above-the-fold claims + friction)
- **Compliance positioning** (banking partners, regulation, trust badges)

---

## 2) Primary tools (no credentials needed)

### 2.1 Meta Ad Library (Facebook/Instagram)
Use keyword search (works even when advertiser pages vary):
- Payoneer search: 
  - https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=US&q=payoneer&search_type=keyword_unordered
- Wise search:
  - https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=US&q=wise&search_type=keyword_unordered
- Deel search:
  - https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=US&q=deel&search_type=keyword_unordered

**Tip:** Switch `country=` to target markets when you run the weekly scan (TR/NG/EG/PK). Meta allows country filtering inside the UI too.

### 2.2 Google Ads Transparency Center (Search/Display/YouTube)
- Home: https://adstransparency.google.com/

Search by advertiser / website name:
- Payoneer, Wise, Deel

Filter suggestions:
- **Region**: TR / NG / EG / PK
- **Format**: Video vs Image vs Text
- **Date range**: last 7 days / 30 days

---

## 3) Weekly workflow (15–25 minutes)

### Monday routine
1) **Meta Ad Library:** 5 minutes per competitor
   - capture 3–5 representative ads (or biggest new angle)
2) **Ads Transparency Center:** 5 minutes per competitor
   - capture 3–5 ads (especially YouTube/video hooks)
3) Log everything into the template below
4) Summarize changes:
   - “New hook(s) noticed”, “New offer(s)”, “New geo push”, “New format”, “New trust claim”

### Output artifacts
- Update this file (append a new weekly entry)
- Optionally: add a 5-bullet “Competitor moves” section into weekly report

---

## 4) Logging template (copy/paste)

**Week of:** YYYY-MM-DD

### Payoneer
- Ad 1: [Platform] [Geo] — Hook: "…" | Offer: … | Format: … | CTA: … | Landing: … | Notes: …
- Ad 2: …

### Wise
- Ad 1: …

### Deel
- Ad 1: …

### Summary (what changed vs last week)
- New hooks:
- New offers:
- Geo shifts:
- Format shifts:
- Implications for Cenoa:

---

## 5) Baseline scan (initial snapshot)
This is a **baseline checklist** to align what we expect to see in competitors’ ads. When you do the first real scan in Meta/Google UI, fill the next section with concrete examples.

### Common competitor angles to watch for
- **Payoneer**: “Get paid globally”, “Business account”, “Freelancer payments”, “Request a payment”
- **Wise**: “Transparent fees”, “Best exchange rate”, “International transfers”, “Multi-currency account”
- **Deel**: “Get paid as a contractor”, “Global payroll”, “Compliance”, “Withdraw in local currency”

### What we should compare against in our creatives
- **Cost claim clarity** ("% fee" vs "save $X")
- **Trust badge density above fold**
- **Time-to-value** (“open in 3 minutes”, “get paid today”)
- **Local-language execution** (especially EG Arabic dialect)

---

## Weekly Log

---

**Week of:** 2026-03-22

### Payoneer (~31 active ads on Meta from @Payoneer page)
- Ad 1: [Meta] [Global/EN] — Hook: "Markets don't take breaks" | Offer: Stablecoin waitlist (early access) | Format: Static+link | CTA: Sign Up | Landing: payoneer.com/stablecoin/ | Notes: 🔥 **Major new angle** — stablecoin 24/7 payments
- Ad 2: [Meta] [LATAM/ES] — Hook: "Los mercados no se detienen" | Offer: Stablecoin waitlist | Format: Static+link | CTA: Sign Up | Landing: payoneer.com/es/stablecoin/ | Notes: Same campaign localized to Spanish (5 ad variants)
- Ad 3: [Meta] [APAC/VI] — Hook: "D2C sellers losing profits" | Offer: Whitepaper download | Format: Lead gen | CTA: Download | Landing: pages.payoneer.com/vi/hidden-cost-after-checkout/ | Notes: B2B checkout product, $72B stat hook
- Ad 4: [Meta] [Brazil/PT] — Hook: "Domestic market is huge but international is bigger" | Offer: Account signup | Format: Video (19s) | CTA: Learn more | Landing: payoneer.com/pt/ | Notes: Short video, local language support emphasis
- Ad 5: [Meta] [APAC/VI] — Hook: "$72B hidden costs" | Offer: Whitepaper | Format: Lead gen | CTA: Download | Landing: same | Notes: A/B headline test on same campaign

### Wise (reconstructed from campaign intelligence + Ads of the World)
- Ad 1: [TV/CTV/YouTube] [US+Canada] — Hook: "Absurd scenarios of bad financial decisions" | Offer: Registration | Format: :30 TV spots (comedy) | CTA: Get Wise | Landing: wise.com | Notes: "Be Smart and Get Wise" campaign by Little Big Engine. Premium media buy (NFL, SNL, Emmys). Running Aug 2025–ongoing
- Ad 2: [OOH] [US metros] — Hook: "Calm the Chaos" | Offer: Business accounts | Format: Murals / street | CTA: Sign up | Landing: wise.com/business | Notes: First US B2B campaign. Guerrilla marketing DNA
- Ad 3: [Instagram/TikTok] [Global] — Hook: "Hard to save money?" | Offer: Jars by Wise | Format: Reels/short video | CTA: Try Jars | Landing: wise.com | Notes: Gen Z/Millennial savings anxiety
- Ad 4: [Meta+Google] [Global] — Hook: "See the real cost" | Offer: Rate comparison | Format: Static comparison | CTA: Compare and send | Landing: wise.com/compare | Notes: Always-on transparency creative
- Ad 5: [YouTube] [Global] — Hook: "How to use Wise" | Offer: Free account | Format: Tutorial video (5min) | CTA: Try Wise | Landing: wise.com | Notes: Bottom-funnel educational content

### Summary (what changed vs last week)
- New hooks: **Payoneer stablecoin "24/7 money movement"** — directly overlaps Cenoa's value prop
- New offers: Stablecoin early access waitlist (Payoneer), Jars savings feature (Wise)
- Geo shifts: Payoneer heavy on APAC (Vietnam) + LATAM (Brazil, Spanish); Wise doubling down US/Canada
- Format shifts: Payoneer using lead gen whitepapers (B2B); Wise investing in TV/CTV (upper funnel)
- Implications for Cenoa: **Must accelerate stablecoin savings messaging before Payoneer captures narrative. TR/NG/EG remains uncontested territory. UGC + social-native is our differentiated format lane.**

Full analysis: [competitor-scan-mar22.md](./competitor-scan-mar22.md)

---

## 6) Important caveat: web→app attribution gap
Because **paid web→app flows can show up as “organic/(none)” installs**, competitor monitoring should be treated as **leading indicator** rather than something you can always validate via attribution dashboards.

Mitigation ideas while attribution is imperfect:
- Track **landing pages + UTMs** we use per creative
- Use **promo codes** per channel when possible
- Add a short **onboarding survey**: “How did you hear about Cenoa?”
