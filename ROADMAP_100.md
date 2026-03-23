# Cenoa Performance Marketing — 100-Task Roadmap

> **Amaç:** Lucas'ı (ve agent ekibini) Cenoa'yı büyütebilir ve reklam platformlarını yönetebilir hale getirmek.
> **Date:** 2026-03-21
> **Hedef:** 100 task tamamlandığında, marketing operasyonlarının %80'i otonom çalışır.

---

## ACCESS GAP'LER (Önce Bunları Çöz!)

| # | Platform | Mevcut Durum | Gerekli Aksiyon | Blocker |
|---|---|---|---|---|
| A | **Amplitude** | ✅ API Key + Secret Key | Çalışıyor | — |
| B | **GA4** | ❌ Doğrudan API erişimi yok | GCP service account'a GA4 property erişimi ver | Alp: GA4 Admin → Service Account ekle |
| C | **Google Ads** | ❌ API erişimi yok (sadece Looker'da) | Google Ads API developer token + OAuth | Alp: Ads Manager'dan developer token al |
| D | **Meta Ads** | ✅ MCP bağlı (Metacog OAuth) | Çalışıyor — test et | — |
| E | **BigQuery** | ✅ Service account var | `cenoa-marketingdatawarehouse` projesi | — |
| F | **AppsFlyer** | ❌ Direkt API yok (Amplitude üzerinden) | Pull API key gerekirse | Düşük öncelik |
| G | **Google Sheets** | ✅ OAuth (rclone token'ı ile veya Sheets API) | 3 sheet ID var | — |
| H | **Looker Studio** | ✅ Embed açık | 4 kırık Supermetrics connector | Alp: Supermetrics düzelt veya bypass |
| I | **Twitter/X Ads** | ❓ Kısmen Looker'da | API erişimi gerekebilir | Düşük öncelik |

### Alp'ten Gereken Aksiyonlar:
1. **GA4:** `alperen@cenoa.com` → GA4 Admin → Property Settings → Service Account (`openclaw-bq-writer@cenoa-marketingdatawarehouse.iam.gserviceaccount.com`) ekle → "Viewer" rolü ver
2. **Google Ads:** Developer token başvurusu (veya MCC hesaptan API erişimi)
3. **Looker:** 4 kırık Supermetrics connector'ı fix (veya "gerek yok bypass ediyoruz" de)

---

## ROADMAP OVERVIEW

```
Phase 0: ACCESS & SETUP ────────── Task 1-10
Phase 1: DATA INGESTION ─────────── Task 11-25
Phase 2: FUNNEL & SEGMENTATION ──── Task 26-40
Phase 3: CAC & UNIT ECONOMICS ───── Task 41-50
Phase 4: DASHBOARD & REPORTING ──── Task 51-65
Phase 5: CAMPAIGN MANAGEMENT ────── Task 66-80
Phase 6: OPTIMIZATION ENGINE ────── Task 81-90
Phase 7: AUTONOMOUS OPS ─────────── Task 91-100
```

---

## PART 1: TASK 1-50 (Foundation → Economics)

### Phase 0: ACCESS & SETUP (Task 1-10)

| # | Task | Depends | Owner |
|---|---|---|---|
| 1 | ✅ Amplitude API bağlantısı (Key + Secret) | — | Data Lead |
| 2 | ✅ Amplitude event taxonomy (507 event → 20 actionable) | 1 | Data Lead |
| 3 | ✅ Looker ↔ Amplitude cross-reference | 2 | Data Lead |
| 4 | ✅ Meta Ads MCP bağlantı testi — `list_ad_accounts` çalıştır, account ID al | — | Growth Manager |
| 5 | GA4 API erişimi — service account'a GA4 property viewer rolü ver | Alp aksiyonu | Data Lead |
| 6 | Google Ads API — developer token + OAuth setup | Alp aksiyonu | Data Lead |
| 7 | BigQuery — mevcut dataset'leri keşfet (`cenoa-marketingdatawarehouse`) | — | Data Lead |
| 8 | Google Sheets API — 3 sheet'i programatik okuyabilir hale getir | — | Data Lead |
| 9 | AppsFlyer — Amplitude üzerinden erişim yeterli mi kontrol et | 2 | Data Lead |
| 10 | Credentials inventory dosyası güncelle (`TOOLS.md` + `CAPABILITIES.md`) | 4-9 | Lucas |

### Phase 1: DATA INGESTION (Task 11-25)

| # | Task | Depends | Owner |
|---|---|---|---|
| 11 | Amplitude haftalık KPI pull script (installs, signups, KYC, withdrawals) | 1 | Data Lead |
| 12 | Amplitude ülke bazlı breakdown script (TR/NG/EG/PK) | 11 | Data Lead |
| 13 | Amplitude platform bazlı breakdown (iOS/Android/Web) | 11 | Data Lead |
| 14 | Amplitude attribution breakdown (organic/paid/media source) | 11 | Data Lead |
| 15 | Meta Ads — tüm aktif kampanyaları çek (MCP: `list_ad_accounts` → `read_ads`) | 4 | Growth Manager |
| 16 | Meta Ads — kampanya bazlı spend/impressions/clicks/conversions | 15 | Growth Manager |
| 17 | Meta Ads — ülke bazlı ad performance | 16 | Growth Manager |
| 18 | Meta Ads — creative bazlı performance (hangi ad en iyi?) | 16 | Growth Manager |
| 19 | Google Ads — Looker'daki campaign data'yı parse et (mevcut) | — | Data Lead |
| 20 | Google Ads — kampanya bazlı CPI hesapla (Looker verisinden) | 19 | Growth Manager |
| 21 | Google Sheets — "dikkat trafik canavarı" parse: Meta Ads Plan tab'ı | 8 | Data Lead |
| 22 | Google Sheets — "Budget Tracking" parse: aylık realized costs | 8 | Data Lead |
| 23 | Google Sheets — "CaC Analysis" parse: Turkey historical CAC | 8 | Data Lead |
| 24 | GA4 — web traffic by source/medium/campaign (API veya Looker'dan) | 5 | Data Lead |
| 25 | Tüm data kaynaklarını birleştiren `data-inventory.md` yaz | 11-24 | Data Lead |

### Phase 2: FUNNEL & SEGMENTATION (Task 26-40)

| # | Task | Depends | Owner |
|---|---|---|---|
| 26 | Global funnel: Install → Signup → KYC → Deposit → Withdrawal (haftalık) | 11 | Growth Manager |
| 27 | Turkey funnel (aynı metrikler, TR only) | 12 | Growth Manager |
| 28 | Nigeria funnel (NG only) | 12 | Growth Manager |
| 29 | Egypt funnel (EG only) — activation gap analizi | 12 | Growth Manager |
| 30 | Pakistan funnel (PK only) — neden düşük? | 12 | Growth Manager |
| 31 | Platform funnel: iOS vs Android vs Web | 13 | Growth Manager |
| 32 | Attribution funnel: Organic vs Google Ads vs Meta vs Referral | 14 | Growth Manager |
| 33 | KYC dropout deep-dive: KYC Started → Submit → Updated (step-by-step) | 2 | Growth Manager |
| 34 | KYC dropout ülke karşılaştırması (TR vs NG vs EG) | 33, 12 | Growth Manager |
| 35 | Retention analizi: Day 1, Day 7, Day 30 retention by country | 11 | Data Lead |
| 36 | Cohort analizi: hangi ay signup edenler en iyi retain oluyor? | 35 | Data Lead |
| 37 | Feature engagement: "Get Paid" vs "Transfer" vs "Deposit" usage by country | 2 | Data Lead |
| 38 | Web → App conversion: web signup sonrası app install oranı | 24, 11 | Data Lead |
| 39 | Referral program analizi: kaç referral signup, conversion rate | 2 | Growth Manager |
| 40 | Funnel summary raporu: tüm 26-39 findings tek doküman | 26-39 | Growth Manager |

### Phase 3: CAC & UNIT ECONOMICS (Task 41-50)

| # | Task | Depends | Owner |
|---|---|---|---|
| 41 | Blended CAC hesaplama: total ad spend / total signups (aylık) | 22, 11 | Growth Manager |
| 42 | Channel CAC: Google Ads CAC vs Meta Ads CAC vs Organic | 19, 16, 14 | Growth Manager |
| 43 | Country CAC: TR CAC vs NG CAC vs EG CAC | 42, 12 | Growth Manager |
| 44 | Google Sheets historical CAC'ı Amplitude data ile cross-check | 23, 11 | Data Lead |
| 45 | LTV tahmini: avg withdrawal volume × FX margin × avg lifetime months | 11, 35 | Growth Manager |
| 46 | LTV/CAC ratio by country | 43, 45 | Growth Manager |
| 47 | Payback period: kaç ayda CAC geri dönüyor? | 45, 43 | Growth Manager |
| 48 | Marginal CAC analizi: her $1K ek spend ne kadar ek signup getiriyor? | 22 | Growth Manager |
| 49 | Budget efficiency skoru: her kampanyanın "bang for buck" ranking'i | 42 | Growth Manager |
| 50 | Unit economics summary: 1-page exec brief | 41-49 | Chief of Staff |

---

## PART 2: TASK 51-100 (Dashboard → Autonomous Ops)

### Phase 4: DASHBOARD & REPORTING (Task 51-65)

| # | Task | Depends | Owner |
|---|---|---|---|
| 51 | ✅ Cortex Weekly Pulse KPI banner (manual data) | 11 | Web Ops |
| 52 | KPI auto-update script: Amplitude → data.json → git push → Vercel | 11 | Data Lead |
| 53 | Ülke kartları widget: TR/NG/EG/PK ayrı ayrı mini-dashboard | 12 | Web Ops |
| 54 | Funnel visualization: sankey diagram veya step chart (Chart.js) | 26 | Web Ops |
| 55 | CAC trend chart: aylık bar chart (Google Sheets data + Amplitude) | 41 | Web Ops |
| 56 | Campaign performance tablo: aktif kampanyalar + spend + CPI | 19, 16 | Web Ops |
| 57 | Week-over-week comparison logic (otomatik delta hesaplama) | 52 | Data Lead |
| 58 | Anomaly detection: %20+ düşüş/çıkışta alert | 57 | Data Lead |
| 59 | Anomaly → Telegram alert (OpenClaw cron job) | 58 | Lucas |
| 60 | Haftalık Pazartesi raporu: auto-generated, Telegram'a gönder | 52, 57 | Growth Manager |
| 61 | Aylık executive summary: 1-page PDF (Gamma ile) | 50, 60 | Chief of Staff |
| 62 | Cortex dashboard'a "Last 4 Weeks" trend sparkline'ları ekle | 52 | Web Ops |
| 63 | Campaign alert: herhangi bir kampanya $0 spend'e düşerse uyar | 16, 19 | Data Lead |
| 64 | KYC dropout rate haftalık trend chart | 33 | Web Ops |
| 65 | Cortex'e "Action Items" section ekle (auto-generated) | 58 | Web Ops |

### Phase 5: CAMPAIGN MANAGEMENT (Task 66-80)

| # | Task | Depends | Owner |
|---|---|---|---|
| 66 | Meta Ads — aktif kampanya inventory çıkar (hangi ülke, hangi objective) | 15 | Growth Manager |
| 67 | Meta Ads — underperforming campaign tespiti (high CPA, low ROAS) | 16 | Growth Manager |
| 68 | Meta Ads — budget reallocation önerisi (winning → losing) | 67 | Growth Manager |
| 69 | Meta Ads — creative rotation önerisi (hangi ad stale, hangisi fresh?) | 18 | Growth Manager |
| 70 | Google Ads — Demand Gen retargeting kampanya fix (0 install problemi) | 19 | Growth Manager |
| 71 | Google Ads — TR Rakipler Payoneer kampanya optimize (₺938 CPI!) | 19 | Growth Manager |
| 72 | Google Ads — EG Generic kampanyayı scale et (en iyi CPI ₺325) | 19 | Growth Manager |
| 73 | A/B test framework oluştur: hypothesis → test → measure → learn | — | Growth Manager |
| 74 | Landing page A/B test: cenoa.com ana sayfa CTA testi | 73, 24 | Content Writer |
| 75 | KYC flow A/B test plan: dropout azaltma deneyleri | 33, 73 | Growth Manager |
| 76 | Egypt-specific kampanya planla (Arabic creative + localized LP) | 29 | Growth Manager |
| 77 | Pakistan pre-launch kampanya planla (waitlist → install) | 30 | Growth Manager |
| 78 | Referral program kampanya: mevcut kullanıcılardan viral loop | 39 | Growth Manager |
| 79 | Content marketing plan: SEO blog → organic install pipeline | — | SEO + Content |
| 80 | Social media paid boost plan: hangi organic post'lar boost'lanmalı | — | Social Media |

### Phase 6: OPTIMIZATION ENGINE (Task 81-90)

| # | Task | Depends | Owner |
|---|---|---|---|
| 81 | Budget allocation model: ülke × kanal matris, ROI-based dağılım | 46, 49 | Growth Manager |
| 82 | Automated bid strategy önerisi (Google Ads: tCPA vs Maximize) | 70 | Growth Manager |
| 83 | Creative performance scoring: her ad creative'e 1-10 skor | 18, 69 | Growth Manager |
| 84 | Audience insight raporu: en iyi perform eden demografi/ilgi alanı | 17 | Growth Manager |
| 85 | Lookalike audience önerisi (Meta): best converters'a benzeyen) | 84 | Growth Manager |
| 86 | Dayparting analizi: hangi saat/gün en iyi install oranı | 11 | Data Lead |
| 87 | Seasonal trend analizi: aylık/haftalık pattern'lar | 22, 11 | Data Lead |
| 88 | Competitor ad monitoring: Payoneer/Wise ad library check (haftalık) | — | Growth Manager |
| 89 | Attribution model karşılaştırması: last-click vs data-driven | 14, 32 | Data Lead |
| 90 | Optimization playbook: tüm 81-89 findings → reusable SOP | 81-89 | Growth Manager |

### Phase 7: AUTONOMOUS OPS (Task 91-100)

| # | Task | Depends | Owner |
|---|---|---|---|
| 91 | Weekly KPI auto-pull + auto-publish cron job | 52, 60 | Lucas |
| 92 | Anomaly detection → auto-Telegram alert cron | 58, 59 | Lucas |
| 93 | Campaign health check cron: haftalık "dead campaign" sweep | 63 | Lucas |
| 94 | Budget pacing alert: aylık bütçenin %X'i harcanmışsa uyar | 22 | Lucas |
| 95 | Meta Ads auto-pause: CPA > threshold olan ad set'leri durdur (onay ile) | 67, 68 | Growth Manager |
| 96 | Auto-generated weekly action items (data → "şunu yap" listesi) | 65, 60 | Growth Manager |
| 97 | Monthly board deck auto-generation (Gamma) | 61 | Chief of Staff |
| 98 | Agent self-improvement: her hafta "ne öğrendik?" retrospective | — | Lucas |
| 99 | Cortex SaaS'a taşınabilecek modülleri dokümante et | — | Lucas |
| 100 | **"Cenoa Marketing Autopilot" v1.0 launch** — tüm sistem otonom | 91-99 | Team |

---

## Milestone'lar

| Task | Milestone | Expected |
|---|---|---|
| 10 | 🔑 All APIs connected | Hafta 1 |
| 25 | 📊 All data flowing | Hafta 1-2 |
| 40 | 🔬 Full funnel visibility | Hafta 2 |
| 50 | 💰 Unit economics clear | Hafta 2-3 |
| 65 | 📈 Auto-reporting live | Hafta 3 |
| 80 | 🎯 Campaign management active | Hafta 4 |
| 90 | 🧠 Optimization engine running | Hafta 5 |
| 100 | 🤖 Marketing Autopilot v1.0 | Hafta 6 |
