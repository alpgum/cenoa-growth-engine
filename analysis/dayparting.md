# Dayparting (Day-of-Week) Analysis — Amplitude

**Sprint:** 072  
**Created:** 2026-03-21  
**Source:** Amplitude Dashboard REST API → `/api/2/events/segmentation` (daily interval)  
**Date range:** 2026-02-19 → 2026-03-20 (30 days)  
**Events:** `[AppsFlyer] Install`, `Cenoa sign-up completed`, `Withdraw Completed`  
**Status:** ✅ Completed (weekday-level; hourly not available via this API)

---

## 1) Executive takeaways

### Installs (`[AppsFlyer] Install`)
- **Peak day:** **Tuesday** (avg **372.8/day**, **16.0%** share)
- **Strong day:** **Thursday** (avg **328.6/day**, **17.6%** share)
- **Softest day:** **Wednesday** (avg **281.0/day**, **12.0%** share)

### Sign-ups (`Cenoa sign-up completed`)
- **Peak day:** **Sunday** (avg **229.2/day**, **15.1%** share)
- **Strong days:** **Thursday / Friday** (avg **208.0 / 200.8 per day**, **17.1% / 16.5%** shares)
- **Softest day:** **Wednesday** (avg **180.2/day**, **11.9%** share)

### Withdrawals (`Withdraw Completed`)
- **Peak day:** **Tuesday** (avg **393.2/day**, **16.2%** share)
- **Strong days:** **Thursday / Friday** (avg **354.8 / 354.0 per day**, **18.2% / 18.2%** shares)
- **Weekend drop:** **Saturday** avg **231.2/day** and **Sunday** avg **173.8/day** (lowest)

> Note on the date window: this range contains **5 Thursdays and 5 Fridays** (other weekdays appear 4×). The tables below use **per-day averages** to normalize.

---

## 2) Weekday distribution (global)

| Weekday | Installs (avg) | Installs share | Sign-ups (avg) | Sign-ups share | Withdrawals (avg) | Withdrawals share |
|---|---:|---:|---:|---:|---:|---:|
| Mon | 288.5 | 12.4% | 191.0 | 12.6% | 376.0 | 15.5% |
| Tue | 372.8 | 16.0% | 207.2 | 13.6% | 393.2 | 16.2% |
| Wed | 281.0 | 12.0% | 180.2 | 11.9% | 372.8 | 15.3% |
| Thu | 328.6 | 17.6% | 208.0 | 17.1% | 354.8 | 18.2% |
| Fri | 298.0 | 15.9% | 200.8 | 16.5% | 354.0 | 18.2% |
| Sat | 302.2 | 12.9% | 201.8 | 13.3% | 231.2 | 9.5% |
| Sun | 308.2 | 13.2% | 229.2 | 15.1% | 173.8 | 7.1% |

---

## 3) Recommended ad scheduling (weekday bid adjustments)

This is **volume-based dayparting** (event counts), *not* CPA/ROAS-based dayparting. Use it as a first-pass schedule, then replace with **cost + conversion efficiency by weekday/hour** from ad platforms.

### Suggested weekday modifiers (starting point)

**Acquisition (optimize for installs / sign-ups):**
- **Tue:** +10–15% (install + withdrawal peak)
- **Thu:** +10% (install + sign-up strong)
- **Fri:** +0–5% (sign-up + withdrawal strong)
- **Wed:** -5–10% (softest day across installs + sign-ups)
- **Sun:** keep **0%** (sign-ups peak on Sunday; don’t blindly down-bid weekends)
- **Sat:** 0% initially (installs are not low; withdrawals are low)

**Finance/ops-style conversion campaigns (if any optimize closer to withdrawals):**
- Consider **down-weighting Sat/Sun** (-10% to -25%), *only after validating CPA/quality*.

### Practical implementation notes (platform constraints)
- **Google Search / Display:** weekday ad scheduling + bid modifiers are straightforward.
- **PMax:** ad scheduling control is limited; you’ll likely adjust via **budgets** and monitoring rather than strict schedules.
- **Google App campaigns (UAC):** dayparting controls are typically **not available**; use budget pacing, creative, geo splits.
- **Meta:** use delivery breakdowns to learn time-of-day/day-of-week efficiency; enforcement is less direct than Google’s schedule modifiers.

---

## 4) Country-specific patterns (top 5 by volume)

### `[AppsFlyer] Install` — Top 5 countries
| Country | 30d total | Share | Best weekday (avg) |
|---|---:|---:|---|
| Turkey | 5,311 | 56.8% | Tue (230.0/day) |
| Nigeria | 2,309 | 24.7% | Tue (88.8/day) |
| Egypt | 1,290 | 13.8% | Thu (48.6/day) |
| United States | 75 | 0.8% | Wed (3.5/day) |
| Ghana | 40 | 0.4% | Sat (2.2/day) |

### `Cenoa sign-up completed` — Top 5 countries
| Country | 30d total | Share | Best weekday (avg) |
|---|---:|---:|---|
| (none) | 3,779 | 62.1% | Sun (145.0/day) |
| Turkey | 1,220 | 20.1% | Sun (51.5/day) |
| Nigeria | 487 | 8.0% | Tue (22.2/day) |
| Egypt | 440 | 7.2% | Fri (18.4/day) |
| United States | 19 | 0.3% | Thu (1.2/day) |

**Important tracking note:** the large **(none)** bucket indicates **missing/unknown country** for most sign-up completed events (user property not set, or event not joined to geo). This limits country-specific dayparting confidence for sign-ups.

### `Withdraw Completed` — Top 5 countries
| Country | 30d total | Share | Best weekday (avg) |
|---|---:|---:|---|
| Turkey | 5,079 | 52.2% | Tue (235.2/day) |
| Nigeria | 3,461 | 35.6% | Fri (134.8/day) |
| United States | 261 | 2.7% | Tue (11.0/day) |
| South Africa | 110 | 1.1% | Tue (6.0/day) |
| Netherlands | 106 | 1.1% | Thu (6.4/day) |

---

## 5) Limitations + what needs Ads Console access

### Limitations (Amplitude API)
- The Dashboard REST **segmentation endpoint provides daily series** here; it doesn’t give a clean **hourly** distribution suitable for “hour-of-day” dayparting in this workflow.
- This analysis is **count-only**. It doesn’t include cost, CPA, ROAS, or impression-share dynamics.
- Country dayparting is partially blocked by **missing country attribution** for sign-up events ("(none)").

### What to pull from ad platforms (to finish true dayparting)

**Google Ads**
- Reports → **Day & hour** performance by campaign/ad group:
  - Spend, impressions, clicks, CPI/CPA, conversion rate
  - Split by **country** (TR/NG/EG) and by **campaign type** (Search vs PMax vs UAC)

**Meta Ads**
- Breakdown → **Time of day** / **Day of week** (where available):
  - Spend, CPM, CTR, installs, CPA
  - Compare prospecting vs retargeting

### Optional next-step (if we want true hourly from analytics)
- Use **Amplitude raw event export** (Export API) and compute hourly distributions offline (heavier + needs event-level data processing).

---

*Sprint 072 | Dayparting (weekday) | 2026-03-21*
