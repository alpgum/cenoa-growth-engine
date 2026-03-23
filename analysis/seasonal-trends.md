# Seasonal Trends (12+ months) — Performance + Funnel Seasonality

Scope: use the **already-parsed Google Sheets exports** to identify seasonality across spend → installs → signups → virt acc / new active, then translate into a practical **2026 ramp/hold calendar** (with **Ramadan** implications for EG/NG/PK).

## Data used (from parsed JSON)

1) `data/sheets-cac-analysis.json`
- **Turkey monthly (2025-01 → 2025-12)**: `cost`, `sign_up`, `virt_acc`, `new_active`, plus cost-per metrics.
- Early **2026 (TR Jan–Feb)** continuation.
- Some **weekly 2026** multi-country breakdowns (TR/EG/NG; PK mostly absent in weekly exports).

2) `data/sheets-trafik-canavari.json` (TR Only tab)
- **Turkey monthly (2025-01 → 2025-12)**: installs, signups, new active, conversion rates (install→signup, signup→new active) and spend lines (All Spend, Google, Meta, etc.).
- Contains multiple partial-week columns (May/Jun/Oct/Dec). For seasonality we use the **full-month columns** only.

3) `data/sheets-budget-tracking.json`
- **Realized cost** by country for **Jan 2026** and **Feb 2026** (TR/EG/NG) + March 2026 budget plan (TR/EG/NG/PK).

---

## 1) Monthly patterns (Spend, Installs, Signups, Virt Acc, New Active)

### 1.1 Turkey — monthly performance summary (2025)
Source: `sheets-cac-analysis.json → sum_turkey.months_2025`

| Month | Cost | Signups | Virt acc | New active | Cost / signup | Cost / virt acc | Cost / new active |
|---|---:|---:|---:|---:|---:|---:|---:|
| Jan | 35,805 | 2,451 | 1,154 | 239 | 15 | 31 | 150 |
| Feb | 52,458 | 2,745 | 1,183 | 375 | 19 | 44 | 140 |
| Mar | 36,997 | 2,568 | 1,247 | 402 | 14 | 30 | 92 |
| Apr | 9,266 | 1,687 | 854 | 369 | 5 | 11 | 25 |
| May | 33,630 | 3,589 | 1,178 | 368 | 9 | 29 | 91 |
| Jun | 38,405 | 2,689 | 744 | 329 | 14 | 52 | 117 |
| Jul | 33,322 | 1,805 | 646 | 283 | 18 | 52 | 118 |
| Aug | 37,391 | 3,092 | 749 | 227 | 12 | 50 | 165 |
| Sep | 35,839 | 2,357 | 687 | 283 | 15 | 52 | 127 |
| Oct | 29,556 | 1,566 | 550 | 242 | 19 | 54 | 122 |
| Nov | 26,850 | 1,500 | 628 | 221 | 18 | 43 | 121 |
| Dec | 23,312 | 1,719 | 754 | 271 | 14 | 31 | 86 |

**Peaks / troughs (TR, 2025):**
- **Spend peak:** Feb ($52.5k). **Spend trough:** Apr ($9.3k).
- **Signup peak:** May (3,589). **Signup trough:** Nov (1,500).
- **Virt acc peak:** Mar (1,247). **Virt acc trough:** Oct (550).
- **New active peak:** Mar (402). **New active trough:** Nov (221).
- **Best cost/new active (CPA):** Apr ($25) — *outlier-low spend month but strong activation yield.*
- **Worst cost/new active:** Aug ($165) — *high volume month but weak activation.*

**Quarter view (TR, 2025):**
- **Q1:** highest spend and strong new act (1,016). Auctions likely competitive.
- **Q2:** comparable new act (1,066) with **much lower spend** (driven by Apr). Most “efficient” quarter on paper.
- **Q3:** **installs surge** (see below) but new act drops (793) → *quality problem / intent mismatch.*
- **Q4:** lower spend; conversion improves; Dec CPA improves materially.


### 1.2 Turkey — traffic/funnel shape (installs → signups → new active)
Source: `sheets-trafik-canavari.json → TR Only`

| Month | All spend | Installs | Signups | New active | Install→Signup | Signup→Active |
|---|---:|---:|---:|---:|---:|---:|
| Jan | $35,805 | 3,100 | 2,300 | 238 | 73% | 10% |
| Feb | $52,458 | 3,300 | 2,400 | 375 | 73% | 16% |
| Mar | $36,997 | 3,400 | 2,200 | 399 | 66% | 18% |
| Apr | $9,266 | 2,000 | 1,400 | 367 | 69% | 26% |
| May | $33,630 | 5,173 | 3,295 | 367 | 64% | 11% |
| Jun | $38,405 | 6,225 | 2,595 | 328 | 42% | 13% |
| Jul | $33,322 | 4,593 | 1,739 | 283 | 38% | 16% |
| Aug | $37,391 | 7,270 | 3,015 | 227 | 41% | 8% |
| Sep | $35,839 | 4,810 | 2,290 | 283 | 48% | 12% |
| Oct | $29,556 | 2,127 | 1,508 | 242 | 71% | 16% |
| Nov | $26,851 | 2,140 | 1,510 | 221 | 71% | 15% |
| Dec | $23,118 | 2,549 | 1,647 | 271 | 65% | 16% |

**Key pattern: Summer = volume, not value (TR).**
- **Installs peak:** Aug (7,270) and Jun (6,225), but install→signup collapses to **38–42%** (vs 66–73% in Q1/Q4).
- **Signup→new active is worst in Aug (8%)**, matching Aug’s worst CPA in the CAC table.
- **Q4 (Oct–Nov)** shows **high-intent quality** (install→signup 71%) but low volume.

**Interpretation:**
- Treat **Jun–Aug** as a season where broader reach can inflate installs, but downstream quality (signup + activation) requires tighter targeting, stronger qualification messaging, and/or better onboarding.


### 1.3 Early 2026 (limited months)
Source: `sheets-cac-analysis.json → sum_turkey.months_2026`

| Month | Cost | Signups | Virt acc | New active | Cost / new active |
|---|---:|---:|---:|---:|---:|
| Jan 2026 | 27,088 | 2,751 | 900 | 226 | 120 |
| Feb 2026 | 25,811 | 1,721 | 580 | 124 | 208 |

Notes:
- Feb 2026 shows a **sharp activation efficiency drop** vs Jan 2026 (CPA 208 vs 120) *in this TR summary.*
- Budget Tracking’s Feb 2026 tab also notes funnel metrics were not fully populated (“#DIV/0!”), so treat Feb funnel efficiency as **low-confidence**.

---

## 2) Holiday effects + Ramadan impact (incl. EG/NG/PK)

### 2.1 What the 2025 Turkey data suggests (seasonal windows)
We can’t causally attribute with 100% confidence (no explicit holiday flags in the sheet), but the pattern is strong enough to be operational:

- **Ramadan 2025** was expected **Feb 28 → Mar 29, 2025** (moon-sighting dependent). This overlaps **late Feb + Mar**.
  - In the data: Mar has **peak new act (402)** and strong CPA (92).
  - **Apr** shows a *massive spend drop* but **best activation conversion** (signup→active 26%) and best CPA (25). This is consistent with a mix of (a) spend pause and/or (b) post-Ramadan behavioral shift.

- **Summer (Jun–Aug)**
  - Installs spike, but intent/quality drops materially (install→signup down to 38–42%; signup→active down to 8% in Aug).
  - Operational implication: **avoid scaling purely on CPI** in Jun–Aug; optimize on **virt acc / new active** (or at least signup quality proxies).

- **Back-to-routine (Sep)**
  - Volumes normalize; CPA improves vs Aug (165 → 127).

- **Q4 (Oct–Dec)**
  - Lower volume but higher “intent density” (install→signup 71% in Oct–Nov).
  - Dec shows improved CPA (86) and better virt acc count (754) vs Oct/Nov.


### 2.2 Ramadan 2026: timing + expected impact (EG/NG/PK)
Ramadan 2026 is expected to begin around **Tue Feb 17, 2026** and end around **Wed Mar 18–Thu Mar 19, 2026** (moon-sighting dependent). This matters most for **EG + PK**, and partially for **NG** (especially Northern states).

**Observed spend ramp into Feb 2026 (from Budget Tracking realized cost):**
- TR total: **$26.2k (Jan)** → **$35.4k (Feb)**
- EG total: **$4.7k (Jan)** → **$9.9k (Feb)**
- NG total: **$4.6k (Jan)** → **$12.2k (Feb)**

This suggests the team already tends to **ramp budgets in Feb**, which in 2026 overlaps with **pre-Ramadan + early Ramadan**.

**Practical Ramadan effects to plan for (EG/PK, partially NG):**
- **Daily rhythm shift:** lower daytime response; spikes after **iftar** and late evening.
  - Action: use **dayparting** (heavier evening budget) and refresh creative cadence faster in the last 10 nights.
- **Auction dynamics:** CPMs/CPAs can rise as many advertisers increase spend.
  - Action: enter Ramadan with **validated creatives** and strong intent campaigns (Search/PMax), not just broad prospecting.
- **Message resonance:** financial products can win with “stress reduction” and “control” framing.
  - Examples: salary/remittance timing, budgeting, fees transparency, safety/trust, family support ahead of Eid.


### 2.3 Other holiday windows (useful heuristics)
- **Eid al-Fitr (end of Ramadan):** conversion can swing both ways (travel + family time vs gifting/spend). Plan **pre-Eid push** + **post-Eid recovery**.
- **Eid al-Adha:** similar but typically later in the year; test “travel/home + exchange + safety” narratives.
- **Black Friday / year-end:** often increases competition across fintech; in TR data Q4 quality improves but volume is lower.

---

## 3) How seasonality should change budgeting + creative messaging

### Budgeting rules of thumb (based on the observed 2025 TR pattern)
1) **Don’t scale summer on installs/CPI.**
   - Jun–Aug: installs rise but conversion falls; guardrails must be **virt acc / new active** (or signup quality proxies).

2) **Keep an always-on “intent core” year-round.**
   - Search/PMax + ASA usually capture higher intent; Q4 shows this strongly (install→signup 71%).

3) **Use Feb/Mar as a “competition-heavy” period (esp. with Ramadan in 2026).**
   - Plan higher creative/testing budget in late Jan/early Feb so you’re not iterating in the most expensive weeks.

4) **Exploit efficiency windows (Apr-like behavior), but validate it’s real.**
   - Apr 2025 is unusually efficient; replicate by testing **tighter targeting + clearer qualification** rather than assuming the month is inherently cheap.


### Creative messaging shifts by season
- **Q1 (Jan–Mar):** “New year, reset, control money” + product education + trust.
- **Ramadan (EG/PK/NG segments):** “Peace of mind” + family support + fees transparency + availability when you need it (night-time usage).
- **Summer (Jun–Aug):** qualify harder (who it’s for) + reduce low-intent traffic; focus on “travel, cards, FX safety” if relevant.
- **Back-to-routine (Sep):** “get organized” + “salary / payments” + “save on fees”.
- **Q4:** “trust + proof” (testimonials, authority, comparisons) + “fast setup” + “clear pricing”.

---

## 4) Practical 2026 planning (what to ramp vs hold)

Because we only have full 12-month seasonality for **TR (2025)**, the calendar below is:
- **Data-led for TR** (observed seasonality), and
- **Ramadan-led for EG/PK/NG** (timing-driven), using Jan–Feb 2026 realized spend as supporting evidence.

### 2026 month-by-month actions (high-level)

**Legend:** Ramp = scale budgets if unit metrics hold. Hold = keep baseline, focus on efficiency/learning.

- **Jan:** Ramp (TR) — strong install→signup, good baseline demand. Prepare Ramadan creative/test plan (EG/PK).
- **Feb:** Ramp carefully (TR/EG/NG) — competition + **Ramadan starts ~Feb 17**.
  - Split: **pre-Ramadan (1–16)** ramp; **early Ramadan** monitor CPA and shift to evenings.
- **Mar:** Hold-to-Ramp depending on week (EG/PK/NG) — Ramadan continues until ~Mar 18/19; expect evening spikes; plan Eid window.
- **Apr:** Ramp (TR) if efficiency repeats; otherwise treat as “post-peak optimization month”.
- **May:** Ramp (TR) — highest signups month in 2025.
- **Jun:** Hold (TR) — installs rise but quality drops; scale only if activation guardrails are met.
- **Jul:** Hold (TR) — weakest install→signup month; focus on channel mix, onboarding, qualification.
- **Aug:** Hold / constrain (TR) — worst CPA; use for creative testing, not aggressive scaling.
- **Sep:** Ramp (TR) — back-to-routine; CPA improves vs Aug.
- **Oct:** Hold (TR) — high intent but lower volume; optimize search/ASA, tighten retargeting.
- **Nov:** Hold (TR) — similar to Oct; test BF/holiday angles selectively.
- **Dec:** Ramp (TR) — CPA improves; good time for year-end trust + “fast setup” messaging.

### Budget guardrails by season (recommended)
- **Jun–Aug:** require stable **cost/virt acc** and **cost/new active** before increasing budgets.
- **Ramadan weeks:** require stable **night-time CVR** + maintain creative freshness (shorter fatigue cycles).
- **Q4:** protect intent channels; scale prospecting only if it does not dilute install→signup.

---

## 5) Data quality notes / assumptions

1) **Market coverage:**
- Full 12-month seasonality is available for **Turkey 2025**.
- EG/NG/PK do **not** have 12-month monthly series in these exports; EG/NG appear in **Jan–Feb 2026 realized costs** and **weekly March 2026** snapshots.

2) **Month completeness:**
- `trafik-canavari` includes multiple partial-week columns; this analysis uses only **full-month columns** for 2025.

3) **Metric consistency across sheets:**
- TR spend in `trafik-canavari` (All Spend) matches TR monthly cost in `cac-analysis` for 2025, which is a good consistency check.
- Some 2026 tabs note missing/invalid cost-per calculations (“#DIV/0!”), so **Feb 2026 funnel efficiency** is treated as **directional**.

4) **Causality:**
- Holidays/Ramadan effects are presented as **operational hypotheses** supported by timing + directional shifts, not as statistically causal claims.

---

## Appendix — Quick takeaways

- **TR:** Feb is the biggest spend month; May is the biggest signup month; Aug is the biggest install month **but worst activation month**.
- **Don’t scale summer on CPI.** Summer volume is “cheap installs, expensive activations”.
- **Ramadan 2026 (Feb 17 → Mar 18/19):** plan for evening spikes + higher competition, especially EG/PK (and NG segments).
- **2026 ramps:** Jan, May, Sep, Dec (TR); Feb–Mar require Ramadan-aware execution (EG/PK/NG).