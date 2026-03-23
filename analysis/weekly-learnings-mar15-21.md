# Weekly Learnings — Mar 15–21, 2026

**Sprint:** 1 (Performance Marketing Deep Dive)  
**Purpose:** Monday briefing — what we learned, what's broken, what to do next

---

## 1) 🔬 What we tested / investigated this week

- Full-stack funnel audit across 4 markets (TR, NG, EG, PK) using Amplitude, AppsFlyer, BigQuery, and Google Sheets
- Attribution model comparison: last-click vs data-driven vs first-click to understand where paid conversions are hiding
- Pre-KYC AI survey deep-dive in Nigeria & Egypt — traced why KYC completions are zero
- Channel-by-channel efficiency ranking on CPI, cost/signup, cost/active metrics
- Demand Gen retargeting campaign forensics (TR-Discovery-24.10.2025) — 5 months of spend with zero installs
- Meta campaign breakdown: W2A vs App Install vs LTV test performance across TR and EG
- Data quality monitoring: built automated checks for attribution gaps, missing properties, and pipeline completeness
- Built 26 scripts for repeatable data pulls, anomaly detection, campaign health checks, and weekly reporting

---

## 2) 📊 Key data findings (with numbers)

- **81.8% of sign-ups have no attribution** — 986 out of 1,206 sign-ups show as "(none)" in AppsFlyer source. Web→app handoff is fundamentally broken.
- **Correction factor ~6.9×** — strict last-click credits only 121 paid sign-ups; modeled paid-influenced estimate is ~830. Every channel-level CAC number is unreliable until this is fixed.
- **KYC is a catastrophe outside Turkey** — NG: 230 KYC starts → 0 submits. EG: 62 starts → 0 submits. Turkey has 95% of all KYC submits (170/179).
- **Pre-KYC AI survey rejects 67%** of applicants in NG/EG, and the 89 who ARE approved never see Bridgexyz (0 handoff — it's a bug).
- **Even Turkey KYC leaks 94%** — 3,025 users see the component, only 170 submit (5.6%). iOS is 3.8× worse than Android (2.4% vs 9.2%).
- **Demand Gen retargeting wasted ~$11,200 over 5 months** — 1,627 clicks/week, zero installs. Campaign was never flagged because nobody monitored campaign-level conversions.
- **meta_w2a Turkey: $3,536/active** — structural failure, not optimizable. Meanwhile meta_ltv_test Egypt: $68/active — proving Meta CAN work with the right campaign type.
- **Appnext is fraud/garbage** — 273 installs → 0 new actives. $893/active. Immediate pause.
- **Pmax is the best paid channel** — $19.18/new active, beating ASA ($22.66), Google Search ($25.48), and Meta ($82.21).
- **DAU dropped 46.1% WoW** — unexplained. Possibly seasonal (Ramadan/Nowruz) but not confirmed.
- **62.5% of sign-up events have no country/platform data** — 754/1,207 sign-ups in Amplitude have "(none)" for both properties.

---

## 3) 😮 What surprised us

- **The Pre-KYC survey handoff is completely broken** — 89 approved users in NG/EG literally cannot proceed. This isn't a conversion optimization problem, it's a bug shipping zero completions.
- **CAC numbers swing 42× depending on which doc you read** — $20.70 vs $208 vs $864 for "cost per active in Turkey," all from our own analyses. Different denominators, different time periods, no standard definitions.
- **A 5-month Demand Gen campaign was burning ~$560/week with zero installs** and nobody caught it. Engagement metrics (clicks, impressions) masked the complete absence of outcomes.
- **Referral channel has the best unit economics** ($30/active, 42.9% signup rate) but only drives 7 installs/week. Massively under-invested.
- **The entire "Nigeria is the growth engine" thesis is built on assumed LTV** — the LTV model uses placeholder guesses ($300-$5,000/mo withdrawal volume). No real backend data has been pulled. LTV ranges span 222× ($2.7 to $600/user).
- **4 scripts committed to git with hardcoded Amplitude API keys** in plaintext. Security incident waiting to happen.

---

## 4) ❌ What's broken and needs fixing

- **Bridgexyz KYC handoff in NG/EG** — approved users hit a dead end. Zero completions. Engineering bug, not a growth problem. (P0)
- **Web→app attribution** — 82% of sign-ups unattributed. OneLink + deferred deep linking + UTM persistence needed. Without this, all channel-level decisions are directional at best. (P0)
- **Amplitude property propagation** — 62.5% of sign-ups missing country/platform. Makes country-level analysis unreliable. (P0)
- **API credentials in git repo** — 4 scripts have hardcoded Amplitude keys. Need immediate rotation + refactor to use env files. (P0 security)
- **No standard metric definitions** — "active user," "CAC," "blended vs paid" mean different things in different docs. Created 42× variance in the same metric. (P1)
- **GA4 access blocked** — missing GA4_PROPERTY_ID prevents web funnel analysis. Web→app handoff is the #2 problem and we have zero web-side data. (P1)
- **BigQuery coverage gap** — daily_installs_campaign_tr table has only 6 days of data vs 21+ needed for trend analysis. (P1)
- **Looker Studio** — 4 Supermetrics connectors broken (Meta, TikTok organic, LinkedIn organic, IG organic). Dashboard unreliable. (P2)
- **19 analysis documents missing the attribution caveat** — readers could make wrong budget decisions based on uncaveated CAC numbers. (P1)

---

## 5) ✅ What's working well

- **Script-based data pipeline** — 26 scripts with JSON audit trails proved more reliable than connector-heavy dashboards. Repeatable, auditable, versionable.
- **Pmax channel performance** — $19.18/active, strong install-to-activation quality. Primary scale lever identified.
- **Apple Search Ads** — $22.66/active with high-intent users (75 installs → 254 withdrawals in attribution week). Solid intent anchor.
- **meta_ltv_test in Egypt** — $68/active and improving WoW. Proves Meta can work with right campaign type + market.
- **Turkey KYC retargeting (RTGT)** — only Meta W2A sub-campaign showing actual withdrawals (9 in attribution week). Small but real signal.
- **Anomaly detection + campaign health automation** — weekly alerts now catch dead campaigns, spend anomalies, and quality red flags automatically.
- **Sprint Mode / task queue discipline** — produced 70+ analysis docs, 26 scripts, and a functioning automation pipeline in a single sprint. Volume was impressive even if consistency needs work.

---

## 6) 🎯 Implications for next week

- **Fix KYC handoff first** — escalate the Bridgexyz bug to engineering. Until NG/EG users can complete KYC, scaling acquisition there is burning money. This unlocks the cheapest markets ($16/active in NG vs $864 in TR).
- **Rotate Amplitude API keys** — security fix, do it Monday morning.
- **Create a single metric definitions doc** — one page defining "new_active" vs "paid_active" vs "active," "blended CAC" vs "paid-attributed CAC," with exact event names and denominators. Every analysis must reference it.
- **Pause Demand Gen retargeting + Appnext + TikTok** — saves ~$1,350/week of zero-return spend. Reallocate to Pmax.
- **Design one incrementality test** — geo holdout for Meta in a Turkish city. Only way to resolve "does Meta drive organic?" which underlies half our attribution uncertainty.
- **Pull actual withdrawal volumes from backend** — replace LTV guesswork with real data. This single data point transforms unit economics from speculative to actionable.
- **Get GA4 property ID and run web funnel analysis** — the web→app handoff is problem #2 and we're flying blind on the web side.
- **Add attribution caveat to all 19 uncaveated docs** — or create a repo-wide ATTRIBUTION_WARNING.md template.
- **Investigate the 46% DAU drop** — determine if seasonal (Ramadan/Nowruz) or product issue. Matters for forecasting.

---

*Compiled: 2026-03-22 | Source: Sprint 1 audit, retrospective, and all analysis docs*
