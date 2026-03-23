# [030] Unit Economics — 1‑page executive brief (Mar 14–20, 2026)

**Objective:** decide where to spend (channel + geo) given current funnel constraints, using CAC proxies + funnel reality check + directional LTV.

## Executive summary (tight)
- **Growth is currently bottlenecked by KYC, not acquisition.** Install→Signup is **83.5% (strong)**, but **KYC Started→Submit is 5.8%** (94% dropout) and WoW KYC submits are **-41.7%**.
- **KYC completion is effectively Turkey-only.** Mar 14–20: **TR KYC submit = 170**, **NG/EG = 0** despite meaningful installs/signups → **treat NG/EG as geo-gated until proven otherwise**.
- **Channel spend should follow “quality + measurability”.** **Apple Search Ads (ASA)** and **Google Search/PMax** are the safest scale levers; **Appnext** and **TikTok** are value-destructive under current activation.
- **Unit economics are impossible to “scale into” while KYC is broken for NG/EG.** Directional LTV may look fine in those geos on paper, but incremental LTV of newly acquired users is ~0 if they can’t complete KYC.
- **Measurement is still leaking (huge “unattributed”).** Treat channel CPA/CAC as directional until attribution gaps are fixed; however the **KYC-by-country pattern is too strong to ignore**.

---

## Top KPIs (this week, WoW)
From Amplitude (Mar 14–20 vs Mar 7–13):
- **Installs:** 1,445 (**-36.5%**)
- **Sign-ups:** 1,207 (**-27.8%**) | **Install→Signup:** **83.5%**
- **KYC started:** 3,098 (**-7.5%**)
- **KYC submits:** 179 (**-41.7%**) | **KYC Started→Submit:** **5.8%**
- **DAU (avg):** 3,060 (**-46.1%**)
- **Deposits:** 1,546 (**-5.8%**) *(not cohort-pure)*
- **Withdrawals:** 2,227 (**+0.6%**) *(existing base holding steady; monetization not collapsing)*

**Geo gating indicator (KYC submit clicked, Mar 14–20):** TR **170** vs NG **0** vs EG **0**.

---

## Biggest bottleneck: KYC completion + geo gating
**Problem:** Users are willing to sign up, but the KYC funnel is a “death zone”, and outside TR it appears non-functional.
- Global: **94.2%** abandon between **KYC Started → KYC Submit**.
- Country reality check: **NG/EG have near-zero KYC submit** even when they reach KYC started.

**Implication for unit economics:**
- **Scaling NG/EG spend now is negative expected value** (cheap CPI doesn’t matter if activation is blocked).
- **The highest ROI action is fixing KYC coverage / flow**, because it unlocks the entire paid funnel and makes low-CAC geos investable.

**Gating KPI (make this explicit):**
- **KYC submit rate by country** (per install and per signup) must be **>0 and stable** before scaling budgets outside TR.

---

## Best channels to scale (and stop list)
**Scale (now):**
1) **Apple Search Ads** — best “quality intent” signal in current data (very strong downstream proxies and outcome volume). Expand: brand exact/broad + competitor/generic.
2) **Google Search + PMax** — consistent quality; keep scaling *with better split + reporting*.

**Stop / keep paused (now):**
- **Appnext** — classic low-quality pattern: **273 installs → 1 withdrawal**; terrible activation in Sheets (Cost/New Active ≈ **$893**).
- **TikTok** — weak downstream: **49 installs → 0 withdrawals** in attribution week; treat as experimentation only after activation is fixed.

**Watchlist (run controlled tests only):**
- **Meta** — large spend but attribution loss is huge (“(none)” dominates). Don’t scale until (a) attribution is repaired and (b) creative/targeting iteration shows stable activation.
- **“Other” (Spaze/byteboost/website)** — keep only placements with verified virt_acc / new_active.

**Why this is the call:** channel CPA is noisy (spend/outcomes from different weeks), but the ranking by downstream efficiency is stable enough to act on.

---

## Country reallocation recommendation (with gating caveats)
**This week (while KYC is broken outside TR):**
- **Allocate incremental budget to Turkey** (only geo with functioning KYC submit).
- **NG/EG: hold to small “verification budgets” only** (enough to confirm KYC fixes + track submit events; do not chase cheap CPI).

**Once KYC is fixed (trigger: sustained non-zero KYC submit in NG/EG):**
- **Primary scale lever: Nigeria** (Sheet week Mar 9–15 suggests extremely low Cost/VirtAcc ≈ **$2** and Cost/Paid Active ≈ **$16**).
- **Secondary: Egypt** (Cost/VirtAcc ≈ **$8**, Cost/Paid Active ≈ **$64**).
- **Turkey remains the quality baseline**, but appears structurally more expensive on “paid active” in the sheet.

**Decision rule (simple):**
- Scale a country only if **KYC submit per install** clears a minimum threshold and **Cost per KYC submit / paid active** is trackable.

---

## LTV note (directional, parameterized)
From the first-pass LTV scenarios (per *active* user):
- **TR base LTV:** ~$72 (wide range $9–$600)
- **NG base LTV:** ~$28.8 (wide range $3.6–$240)
- **EG base LTV:** ~$21.6 (wide range $2.7–$180)

**Key constraint:** for NG/EG, **incremental LTV for newly acquired users is effectively ~0 until KYC works**, regardless of modeled LTV.

---

## Next 7 days action plan (5 bullets)
1) **KYC incident triage (48h):** validate Bridge/Bridgexyz doc + jurisdiction support for **NG + EG**; reproduce KYC flow end-to-end on fresh devices; identify exact fail step(s).
2) **Add “geo gating dashboard”:** daily report of **KYC submit clicked** and **KYC submit rate (per signup)** by country; alert if any country drops toward zero.
3) **Budget move (immediate):** reallocate spend from **Appnext + TikTok** into **ASA + Google Search/PMax** (TR-focused until KYC unlocks).
4) **Attribution repair sprint:** reduce “(none)” by fixing AppsFlyer ↔ Amplitude mapping / deep links / web2app flows; goal: materially lower unattributed signups/withdrawals.
5) **Prepare post-KYC scale plan:** define go/no-go thresholds + budgets for **NG/EG re-entry** (small ramp steps tied to KYC submit and paid-active conversion).
