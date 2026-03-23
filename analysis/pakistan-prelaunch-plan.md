# Pakistan Pre-Launch Marketing Plan

**Date:** 2026-03-21  
**Status:** 🟡 Pre-Launch (Waitlist Active)  
**Sprint:** 062

---

## 1) Current State

| Metric | Value | Source |
|---|---|---|
| **Weekly installs** | 23 | Amplitude Mar 14–20 |
| **Install→Signup rate** | 65.2% (15/23) | Amplitude |
| **KYC Started** | 17 | Amplitude |
| **KYC Submit** | **0** | Amplitude |
| **Deposits / Withdrawals** | 0 / 0 | Amplitude |
| **Waitlist sessions** | ~2,291 | GA4/channel data |
| **March budget allocated** | $6,000 | Budget tracker |

**Summary:** Pakistan is pre-launch with meaningful waitlist interest (2,291 sessions) but negligible paid installs (23/wk). The 65% install→signup rate is healthy, but **KYC is completely blocked** — 17 users started KYC, 0 submitted. No deposits or withdrawals exist. This mirrors the Nigeria/Egypt KYC failure pattern exactly.

---

## 2) 🚨 KYC Readiness Check — BLOCKER

### Does Pakistan have the same Pre-KYC survey / handoff issue as NG/EG?

**Strong evidence says YES:**

| Signal | Nigeria/Egypt | Pakistan |
|---|---|---|
| KYC Started | 292/wk | 17/wk |
| KYC Submit | **0** | **0** |
| Deposits | Legacy only | 0 |
| Pattern | Pre-KYC AI survey → 67% rejection + 100% handoff failure | Unknown mechanism, same outcome |

**Required before any spend increase:**

1. **Confirm Bridgexyz supports Pakistani documents** (CNIC, NICOP, passport)
2. **Check if Pre-KYC AI survey is active for PK** — if yes, it's likely blocking users just like NG/EG
3. **Get at least 1 KYC submit** before scaling — this is the hard gate

> ⛔ **DO NOT scale budget past Phase 1 ($2K) until KYC Submit > 0 for Pakistan.**

---

## 3) Waitlist → Install Conversion Strategy

Pakistan's 2,291 waitlist sessions represent the **single biggest pre-launch asset**. Converting even 10-15% would deliver 230-340 installs — hitting the 100/wk target immediately.

### Launch Announcement Sequence

| Day | Action | Channel | Goal |
|---|---|---|---|
| D-7 | "Coming soon" teaser | Email + push to waitlist | Build anticipation |
| D-3 | Feature preview + early access CTA | Email | Drive pre-registration |
| D0 | **Launch email** — direct app download link | Email blast to full waitlist | Convert waitlist → install |
| D+1 | Push notification to non-openers | Push / SMS | Catch stragglers |
| D+3 | "X people already joined" social proof | Email + in-app | FOMO nudge |
| D+7 | Re-engagement for non-installers | Email | Second chance |

### Expected Conversion
- **Conservative (5%):** ~115 installs from waitlist
- **Moderate (10%):** ~229 installs
- **Optimistic (15%):** ~344 installs

### Requirements
- [ ] Confirm email/phone capture from waitlist signups
- [ ] Set up email sequence in CRM (Braze/equivalent)
- [ ] Prepare deep links for iOS + Android

---

## 4) Initial Channel Test Plan

### Phase 1: $2,000/month (Weeks 1–4)

| Channel | Budget | Rationale |
|---|---|---|
| **Google Search** | $1,200 | High-intent keywords: "send money Pakistan", "crypto Pakistan", "USDT PKR", "dollar account Pakistan" |
| **Apple Search Ads** | $500 | Brand + category terms; low-competition market |
| **Reserve** | $300 | Creative testing, retargeting |

**Google Search targeting:**
- Language: English + Urdu
- Geo: Pakistan (PK), major cities (Karachi, Lahore, Islamabad, Rawalpindi)
- Keywords (seed): `buy usdt pakistan`, `dollar account pakistan`, `send money abroad pakistan`, `crypto wallet pakistan`, `stablecoin pakistan`
- Match type: Phrase + Exact (no broad until data)

**ASA targeting:**
- Category: Finance
- Competitors: Binance, OKX, JazzCash, Easypaisa
- Brand defense: Cenoa variants

### Phase 1 KPIs

| Metric | Target | Kill threshold |
|---|---|---|
| CPI (Google) | < $3.00 | > $5.00 |
| CPI (ASA) | < $2.50 | > $4.00 |
| Install→Signup | > 50% | < 30% |
| KYC Submit | > 0 ⚠️ | = 0 after 2 weeks → pause all spend |

---

## 5) Localization Assessment

### Language landscape in Pakistan
- **Urdu:** National language, ~75% literacy
- **English:** Official language, widely used in tech/finance/urban
- **Regional:** Punjabi, Sindhi, Pashto (not needed for V1)

### Recommendation: **English-first, Urdu ads**

| Asset | Language | Priority |
|---|---|---|
| App Store listing | English + Urdu | P0 (before launch) |
| Google Search ads | English + Urdu ad copy | P0 |
| Landing page | English (Urdu toggle if possible) | P1 |
| In-app experience | English | P2 (Urdu localization post-validation) |
| Push/email nurture | English | P1 |

**Why not full Urdu first:** Urban, tech-savvy, crypto-curious audience in Pakistan is comfortable with English. Urdu ads will expand reach for Google Search but the product can launch English-only.

**Urdu ad copy examples (for Google):**
- "ڈالر اکاؤنٹ پاکستان میں — Cenoa" (Dollar account in Pakistan)
- "USDT خریدیں آسانی سے" (Buy USDT easily)

---

## 6) Budget Phasing

### Three-phase approach: $2K → $4K → $6K

```
Phase 1 ($2K)          Phase 2 ($4K)          Phase 3 ($6K)
Weeks 1–4              Weeks 5–8              Weeks 9–12
─────────────────      ─────────────────      ─────────────────
Gate: Launch ready     Gate: KYC Submit > 0   Gate: CPI < $3 &
+ KYC confirmed        + CPI < $4             KYC rate > 10%
                       
Google: $1,200         Google: $2,500         Google: $3,500
ASA: $500              ASA: $800              ASA: $1,000
Reserve: $300          Meta: $500             Meta: $1,000
                       Reserve: $200          Reserve: $500
```

### Phase gates (hard requirements)

| Phase | Gate-in criteria | Budget | Duration |
|---|---|---|---|
| **Phase 1** | App live in PK + KYC provider confirmed | $2,000/mo | 4 weeks |
| **Phase 2** | KYC Submit > 0 + CPI < $4 + Install→Signup > 40% | $4,000/mo | 4 weeks |
| **Phase 3** | CPI < $3 + KYC completion rate > 10% + first deposits | $6,000/mo | Ongoing |

### Kill switches
- **Immediate pause:** KYC Submit = 0 after 2 full weeks of spend
- **Budget reduction:** CPI > $5 for 2 consecutive weeks
- **Full stop:** No deposits after Phase 2 (8 weeks)

---

## 7) Target: 100 Installs/Week Within 30 Days of Launch

### How we get there

| Source | Week 1 | Week 2 | Week 3 | Week 4 |
|---|---:|---:|---:|---:|
| Waitlist conversion | 80 | 40 | 20 | 10 |
| Google Search | 15 | 25 | 35 | 45 |
| ASA | 5 | 10 | 15 | 20 |
| Organic (ASO lift) | 5 | 10 | 15 | 25 |
| **Total** | **105** | **85** | **85** | **100** |

**Week 1 spike** from waitlist conversion, then paid channels ramp to replace organic tailoff.

### CAC benchmarks (from comparable markets)

| Market | CPI (Jan) | CPI (Mar 9–15) |
|---|---|---|
| Nigeria | $0.67 | $0.35 |
| Egypt | $1.32 | $3.60 |
| Turkey | $6.19 | $2.61 |

**Pakistan estimate:** $1.50–$3.00 CPI (similar to Egypt, lower competition but smaller market).

---

## 8) Success Criteria — Go/No-Go Matrix

| Phase | Metric | 🟢 Go | 🟡 Adjust | 🔴 No-Go |
|---|---|---|---|---|
| **Phase 1** | KYC Submit | > 5/wk | 1–5/wk | 0 after 2 wks |
| | CPI | < $3 | $3–5 | > $5 |
| | Install→Signup | > 50% | 30–50% | < 30% |
| **Phase 2** | KYC completion rate | > 15% | 5–15% | < 5% |
| | First deposit | > 5 users | 1–5 users | 0 |
| | CPI trend | Decreasing | Flat | Increasing |
| **Phase 3** | Cost/Paid Active | < $50 | $50–100 | > $100 |
| | WoW install growth | > 10% | 0–10% | Negative |
| | Deposits/wk | > 20 | 5–20 | < 5 |

---

## Pre-Launch Checklist

- [ ] **KYC provider confirmation** — Bridgexyz supports PK documents (CNIC/passport)
- [ ] **Pre-KYC survey check** — Is AI survey active for PK? If yes, ensure handoff works
- [ ] **App Store readiness** — PK listing live on iOS + Android with Urdu keywords
- [ ] **Waitlist email capture** — Confirm we have contact info for waitlist users
- [ ] **Email sequence built** — 4-email launch sequence ready
- [ ] **Google Ads account** — PK campaigns created (paused until launch)
- [ ] **ASA campaigns** — PK keyword sets ready
- [ ] **Analytics events** — Country=PK segmentation confirmed in Amplitude
- [ ] **Payment rails** — PK deposit/withdrawal methods configured and tested
- [ ] **Legal/compliance** — PK regulatory requirements met

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| KYC blocked (same as NG/EG) | **High** | Critical | Don't scale until KYC Submit > 0 |
| Low waitlist-to-install conversion | Medium | High | Multi-touch email sequence + push |
| High CPI in PK | Medium | Medium | Start with high-intent Search; pause if CPI > $5 |
| Urdu content needed for scale | Medium | Medium | English-first launch, add Urdu in Phase 2 |
| Payment rails not ready | Medium | Critical | Confirm deposit/withdraw methods before launch |
| Regulatory changes | Low | Critical | Legal review before spend commitment |

---

## Summary

**Pakistan has real waitlist demand (2,291 sessions) but faces the same KYC blocker as Nigeria and Egypt.** The plan is:

1. **Fix KYC first** — confirm Bridgexyz supports PK, check if Pre-KYC survey is active
2. **Convert the waitlist** — this alone could deliver 100+ installs in week 1
3. **Phase budget carefully** — $2K → $4K → $6K with hard gates at each step
4. **Target 100 installs/wk** within 30 days, but only if KYC funnel is unblocked
5. **Kill fast** if KYC stays broken — don't repeat the NG/EG pattern of spending into a broken funnel

> **Bottom line:** Pakistan is a high-potential market (cheap installs, good signup rate, strong waitlist) but is **gated on KYC**. Solve KYC, then scale. Not the other way around.

---

*Created: Sprint 062, 2026-03-21*
