# Weekly Spend by Channel — Mar 15-21, 2026

**Report Date:** March 22, 2026
**CAC Definition:** Cost per New Active (TRUE CAC) = Spend / New Actives (first withdrawal)
**Spend Source:** Sheets CAC Analysis — Mar 9-15 actuals used as proxy (Mar 15-21 not yet populated)
**Funnel Source:** Amplitude — actual Mar 15-21

---

## ⚠️ Attribution Caveat

> **Spend is estimated.** The Sheets weekly breakdown for Mar 15-21 is not yet available. We use the Mar 9-15 Sheets actuals as the best-effort proxy, assuming roughly constant weekly pacing. Actual spend may differ by ±15-25%.
>
> **Amplitude "new_active" = Withdraw Completed**, which includes returning users. This inflates the denominator vs. Sheets' "first-time new active" definition. TRUE CAC numbers here are therefore **more optimistic than reality** — treat as directional.
>
> **Channel attribution is incomplete.** The "Other | TR" Amplitude bucket (~157 installs, ~32 signups) contains Meta, Google App, and other campaigns not separately tagged. We split them using Mar 9-15 proportions where possible. Virtual account and new active data from Amplitude is at country level only — channel splits are estimated from prior-week Sheets ratios.

---

## 1. Estimated Spend per Channel (Mar 15-21)

| Country | Channel | Est. Spend ($) |
|---------|---------|---------------:|
| **TR** | Google (Search + Web2App + App) | 1,235 |
| **TR** | Spaze | 900 |
| **TR** | Appnext | 645 |
| **TR** | Apple Ads | 500 |
| **TR** | Meta Web2App | 485 |
| **TR** | TikTok (Web2App + App) | 364 |
| **TR** | Onboarding Meta Test | 101 |
| **TR** | Twitter Ads | 90 |
| | **Turkey Subtotal** | **4,320** |
| **EG** | Meta (Get Paid + LTV tests) | 1,449 |
| **EG** | Google Search | 116 |
| **EG** | Apple Ads | 33 |
| | **Egypt Subtotal** | **1,598** |
| **NG** | Google Search | 229 |
| | **Nigeria Subtotal** | **229** |
| | **GRAND TOTAL** | **6,147** |

*Pakistan: $0 paid spend in this period.*

---

## 2. Cross-Reference: Amplitude Funnel (Mar 15-21 Actual)

### Installs (paid channels only)

| Channel | TR | EG | NG | Other | Total |
|---------|---:|---:|---:|------:|------:|
| Appnext | 163 | – | – | 1 | 164 |
| Other (Meta/Google App/etc.) | 157 | 124 | 24 | 14 | 319 |
| ASA (Apple Ads) | 51 | 17 | – | 11 | 79 |
| TikTok | 42 | – | – | 1 | 43 |
| Google Search | 22 | 0 | 31 | 2 | 55 |
| **Paid Total** | **435** | **141** | **55** | **29** | **660** |

### Signups (paid channels only)

| Channel | TR | EG | NG | Other | Total |
|---------|---:|---:|---:|------:|------:|
| Other (Meta/Google App/etc.) | 32 | 17 | 3 | 2 | 54 |
| ASA (Apple Ads) | 17 | 7 | – | 3 | 27 |
| Appnext | 16 | – | – | – | 16 |
| TikTok | 7 | – | – | – | 7 |
| Google Search | 6 | 1 | 3 | – | 10 |
| Referral | 2 | – | 1 | – | 3 |
| **Paid Total** | **80** | **25** | **7** | **5** | **117** |

### Virtual Accounts & New Actives (country level only from Amplitude)

| Country | Virtual Accounts | New Actives (Withdraw) |
|---------|------------------:|-----------------------:|
| TR | 208 | 568 |
| NG | 76 | 343 |
| EG | 22 | 19 |
| Other | 49 | 98 |
| **Total** | **355** | **1,028** |

*Note: These totals include organic + paid. Paid-only share estimated below.*

---

## 3. Channel Efficiency (Estimated)

Using Mar 9-15 Sheets proportions to allocate country-level virt_acc/new_active to channels:

### Turkey

| Channel | Spend | Installs | Signups | Est. Virt Acc | Est. New Active | CPI | $/Signup | $/Virt Acc | TRUE CAC |
|---------|------:|--------:|--------:|--------------:|----------------:|----:|---------:|-----------:|---------:|
| Apple Ads | $500 | 51 | 17 | ~45 | ~19 | $9.80 | $29.41 | $11.11 | **$26.32** |
| Spaze | $900 | 77 | 12 | ~30 | ~13 | $11.69 | $75.00 | $30.00 | **$69.23** |
| Google (all) | $1,235 | 56 | 8 | ~24 | ~8 | $22.05 | $154.38 | $51.46 | **$154.38** |
| TikTok (all) | $364 | 42 | 7 | ~14 | ~2 | $8.67 | $52.00 | $26.00 | **$182.00** |
| Meta W2A | $485 | 45 | 7 | ~11 | ~2 | $10.78 | $69.29 | $44.09 | **$242.50** |
| Appnext | $645 | 163 | 16 | ~5 | 0 | $3.96 | $40.31 | $129.00 | **∞** 🚩 |
| Meta Test | $101 | 1 | 0 | 0 | 0 | $101.00 | – | – | **∞** 🚩 |
| Twitter | $90 | 0 | 0 | 0 | 0 | – | – | – | – |
| **TR Total** | **$4,320** | **435** | **80** | ~**129** | ~**44** | **$9.93** | **$54.00** | **$33.49** | **$98.18** |

### Egypt

| Channel | Spend | Installs | Signups | Est. Virt Acc | Est. New Active | CPI | $/Signup | TRUE CAC |
|---------|------:|--------:|--------:|--------------:|----------------:|----:|---------:|---------:|
| Apple Ads | $33 | 17 | 7 | ~2 | ~2 | $1.94 | $4.71 | **$16.50** |
| Google Search | $116 | 0 | 1 | ~1 | ~1 | – | $116.00 | **$116.00** |
| Meta (combined) | $1,449 | 124 | 17 | ~8 | ~3 | $11.69 | $85.24 | **$483.00** |
| **EG Total** | **$1,598** | **141** | **25** | ~**11** | ~**6** | **$11.33** | **$63.92** | **$266.33** |

### Nigeria

| Channel | Spend | Installs | Signups | Est. Virt Acc | Est. New Active | CPI | $/Signup | TRUE CAC |
|---------|------:|--------:|--------:|--------------:|----------------:|----:|---------:|---------:|
| Google Search | $229 | 31 | 3 | ~10 | ~3 | $7.39 | $76.33 | **$76.33** |

---

## 4. TRUE CAC Ranking (Best → Worst)

| Rank | Channel | Country | TRUE CAC | Weekly Spend |
|-----:|---------|---------|----------:|-------------:|
| 1 | Apple Ads | EG | **$16.50** | $33 |
| 2 | Apple Ads | TR | **$26.32** | $500 |
| 3 | Spaze | TR | **$69.23** | $900 |
| 4 | Google Search | NG | **$76.33** | $229 |
| 5 | Google Search | EG | **$116.00** | $116 |
| 6 | Google (all) | TR | **$154.38** | $1,235 |
| 7 | TikTok | TR | **$182.00** | $364 |
| 8 | Meta W2A | TR | **$242.50** | $485 |
| 9 | Meta (tests) | EG | **$483.00** | $1,449 |

**Overall blended TRUE CAC (all paid): ~$6,147 / ~53 est. new actives ≈ $116**

---

## 5. 🚩 Flagged Channels (Spend > $100 with 0 New Actives)

| Channel | Spend | Installs | Issue |
|---------|------:|--------:|-------|
| **Appnext (TR)** | $645 | 163 | ⚠️ High install volume but near-zero downstream conversion. Mar 9-15 showed identical pattern (853 installs → 0 new_actives). Likely bot/low-quality traffic. |
| **Onboarding Meta Test (TR)** | $101 | 1 | ⚠️ Negligible scale. Test campaign not producing meaningful volume. |

---

## 6. Key Takeaways

1. **Apple Ads is the TRUE CAC champion** across both TR ($26) and EG ($17) — efficient but low-spend. Scaling opportunity?
2. **Spaze (TR) at $69 TRUE CAC** is solid for a DSP channel — warrants continued investment.
3. **Appnext is burning $645/week with zero activations** — recommend immediate pause or dramatic creative/targeting refresh.
4. **Meta campaigns underperform on activation** — high CPIs and the worst TRUE CAC in both TR and EG. The "get paid" and "LTV" test campaigns in Egypt ($1,449 combined) are expensive relative to ~3 new actives.
5. **Google is mid-tier** — decent virt_acc cost but TRUE CAC of $154 in TR suggests the users it acquires are slower to activate.
6. **Nigeria is efficient at $76 TRUE CAC** from minimal spend — but nearly all volume is organic (386 organic installs vs 31 paid).

---

*Data files: `data/weekly-spend-20260322.json` (structured), `data/weekly-channel-country-20260322.json` (Amplitude raw)*
