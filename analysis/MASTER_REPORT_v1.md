# Cenoa Performance Marketing — Master Report v1

**Prepared:** March 21, 2026  
**Analysis period:** March 14–20, 2026 (with 6-month historical context)  
**Data sources:** Amplitude, AppsFlyer, Google Sheets (Budget Tracking, CAC Analysis, Trafik Canavarı), BigQuery  
**Confidence tier:** Medium — see Appendix for caveats

---

## 1. Executive Summary

Cenoa's performance marketing engine is **structurally broken outside Turkey** and **inefficiently allocated within Turkey**. Three issues account for the majority of lost value:

1. **KYC is blocked for 54% of installs.** Nigeria, Egypt, and Pakistan — representing 687 of 1,445 weekly installs — have **zero KYC completions**. The BridgeXYZ identity widget never renders for non-Turkish documents. Every dollar spent acquiring users in these markets currently yields zero activated accounts.

2. **iOS converts 3.8× worse than Android at KYC.** iOS shows a 2.4% KYC Shown→Submit rate vs Android's 9.2%. Given iOS users generate 53% of all withdrawals, this gap represents significant unrealized revenue.

3. **$787/week is spent on channels with near-zero downstream conversion.** Appnext (273 installs → 1 withdrawal) and TikTok (49 installs → 0 withdrawals) should be paused immediately, with budget redirected to Apple Search Ads and Google.

**The single highest-ROI action is fixing KYC for Nigeria.** At Turkey's 11% KYC completion rate, Nigeria's existing funnel volume would yield ~50–100 additional KYC submits per week — nearly doubling total activations. Nigeria's sheet-derived CAC is $2/virtual account vs Turkey's $35.

**Unit economics are early-stage and assumption-heavy.** Turkey's base-case LTV/CAC ratio is 0.08× — deeply unprofitable under current assumptions. Nigeria (if KYC is fixed) shows 1.8× at base case. However, LTV inputs are parameterized; finance-confirmed margins and cohort retention data are needed to make these actionable.

**Key numbers this week:**

| Metric | Value | WoW | Status |
|---|---:|---:|---|
| Installs | 1,445 | -36.5% | 📉 |
| Sign-ups | 1,207 | -27.8% | 📉 |
| KYC Submits | 179 | -41.7% | 🚨 |
| Withdrawals | 2,227 | +0.6% | ✅ Stable base |
| KYC Started→Submit | 5.8% | — | 🚨 94% dropout |
| Unattributed withdrawals | 61% | — | ⚠️ Measurement gap |

---

## 2. Business Context

**Cenoa** is a freelancer banking platform operating across four markets: Turkey, Nigeria, Egypt, and Pakistan. The product offers multi-currency accounts, money transfers, debit cards, and deposit/withdrawal rails — targeting freelancers and remote workers who earn in foreign currencies.

**Market positioning by volume (Mar 14–20):**

| Market | Installs | % of Total | KYC Submits | Withdrawals | Role |
|---|---:|---:|---:|---:|---|
| Turkey | 670 | 46% | 170 (95%) | 1,260 (57%) | Revenue engine |
| Nigeria | 458 | 32% | 0 | 492 (22%) | Blocked goldmine |
| Egypt | 206 | 14% | 0 | 23 (1%) | Early-stage test |
| Pakistan | 23 | 2% | 0 | 0 | Pre-launch |

Turkey is the only market with a functioning end-to-end funnel. Nigeria shows the strongest latent demand signal — 492 weekly withdrawals from legacy users despite zero new activations. Egypt has the cheapest CAC ($8/virtual account vs Turkey's $35) but an equally blocked funnel.

**Feature engagement reveals market character:**
- **Turkey:** Balanced power users — Card (31%), Transfer (30%), Get Paid (30%)
- **Nigeria:** Deposit-first — only market where Deposit Tapped leads (45% of feature mix)
- **Egypt:** Card-curious — Debit Card is 38% of feature mix, Transfer only 14%

---

## 3. Data Infrastructure

### What We Connected

| Source | Coverage | Use |
|---|---|---|
| **Amplitude** (Event Segmentation API) | Real-time events, country/platform segments | Funnel analysis, KYC dropout, feature engagement |
| **AppsFlyer** (via BigQuery + Amplitude) | Install attribution, media source, campaigns | Channel performance, CPI, attribution |
| **Google Sheets** (3 sheets via API) | Budget tracking, CAC analysis, traffic data | Spend, historical CAC, channel benchmarks |
| **BigQuery** (marketing_appsflyer dataset) | Raw AppsFlyer data, 2 tables | Campaign-level queries, cross-channel joins |
| **Looker Studio** (embed) | Visual dashboards | Reporting screenshots (4 connectors broken) |

### What's Missing (Priority Order)

| Gap | Impact | Resolution |
|---|---|---|
| **Withdrawal volume ($)** per user/country | Cannot compute real LTV — model is 100% parameterized | Backend data export or Amplitude revenue events |
| **True cohort retention** (D1/D7/D30) | Retention proxy is crude (DAU/cumulative signups) | Amplitude Retention API or BigQuery cohort SQL |
| **Net margin per transaction** | LTV assumptions range 0.3%–1.0% take rate | Finance-confirmed unit margin by rail/corridor |
| **Meta Ads API** | No campaign-level CTR, CPM, frequency, creative performance | MCP access or direct API credentials |
| **KYC error telemetry** | Cannot diagnose exact failure point for non-TR users | Instrument `kyc_error_type`, `kyc_provider_response` events |
| **Unified metric definitions** | "Virtual account" differs 3.6× across sheets | Single source-of-truth table: month × country × channel × spend × outcomes |

---

## 4. Funnel Analysis

### 4.1 Global Funnel (Mar 14–20)

```
Install (1,445)
  └─→ Sign-up (1,207) ............ 83.5% ✅ Strong
        └─→ KYC Started (3,098) .. includes returning users
              └─→ KYC Shown (3,139)
                    └─→ KYC Submit (179) .. 5.7% of Shown 🚨
                          └─→ Deposit (1,546) ¹
                                └─→ Withdrawal (2,227) ¹
```
¹ Deposits/withdrawals include returning users; not cohort-pure.

**The funnel cliff is at KYC.** Install→Sign-up (83.5%) is healthy. But of every 100 installs, ~84 sign up, ~12 start KYC, and **fewer than 1 submits KYC**. The 94.2% KYC dropout rate is the defining constraint.

### 4.2 The Two KYC Problems

| Problem | Scope | Root Cause | Severity |
|---|---|---|---|
| **Non-TR countries can't KYC** | NG, EG, PK, GH | BridgeXYZ widget never renders — provider/jurisdiction block | 🚨 Critical |
| **TR KYC has 94% dropout** | Turkey | UX friction in Shown→Submit (5.6% conversion) | ⚠️ High |

**Evidence:** `Bridgexyz KYC Component Shown` = 0 for Nigeria (230 KYC starts), Egypt (62), Pakistan (17), and Ghana (22). KYC Submit events exist in only 7 countries — all with European/supported ID documents.

### 4.3 Country Highlights

**Turkey** — The only functioning market. KYC Started→Submit = 11.1% (2× global average). 95% of all KYC completions. Install→Signup appears low (33.7%) but 754 "(none)" country sign-ups obscure the real rate (likely 50–60%).

**Nigeria** — Strongest latent demand. 458 installs, 492 withdrawals from legacy users, highest Deposit Tapped engagement (45%). If KYC were fixed at Turkey's 11% rate on Nigeria's ~600 KYC starts, expect +50–100 submits/week.

**Egypt** — Cheapest acquisition. $8/virtual account vs Turkey's $35. Sign-up→KYC Start rate is 96.9% — users try to KYC almost immediately. KYC follow-up messaging test showed 450% better conversion; Architect LP showed 27% cheaper CTA clicks.

**Pakistan** — Too small to evaluate (23 installs). KYC blocked. Do not allocate budget until KYC support is confirmed.

### 4.4 Platform Funnel

| Metric | Android | iOS | Web |
|---|---:|---:|---:|
| Installs | 1,275 (88%) | 170 (12%) | — |
| Sign-ups | 221 (18%) | 232 (19%) | 754 (63%) |
| KYC Submit | 140 (78%) | 39 (22%) | 0 |
| Withdrawals | 1,033 (46%) | 1,187 (53%) | 7 (<1%) |
| **KYC Shown→Submit** | **9.2%** | **2.4%** 🚨 | — |

**Three platform issues:**
1. **iOS KYC gap (3.8×):** Possible submit button occlusion, webview issue, or instrumentation failure
2. **Web sign-up leak:** 754 web sign-ups → 15 deposits (2.0%) — massive handoff failure
3. **iOS paradox:** 12% of installs but 53% of withdrawals — iOS users are the highest-value segment, yet KYC conversion is worst

---

## 5. Unit Economics

### 5.1 CAC by Country (Mar 9–15, 2026 — Sheets)

| Country | CPI | $/Sign-up | $/Virtual Account | $/Paid Active |
|---|---:|---:|---:|---:|
| **Nigeria** | $0.35 | $0.79 | $2 | $16 |
| **Egypt** | $3.60 | $6.89 | $8 | $64 |
| **Turkey** | $2.61 | $6.63 | $35 | $864 |

⚠️ **Nigeria and Egypt CAC is only meaningful if KYC is fixed.** Current incremental LTV for newly acquired NG/EG users ≈ $0.

### 5.2 Turkey Blended CAC Trend (6 months)

| Month | Spend | New Actives | $/Active | Trend |
|---|---:|---:|---:|---|
| 2025-09 | $35,839 | 283 | $127 | — |
| 2025-10 | $29,556 | 242 | $122 | Flat |
| 2025-11 | $26,850 | 221 | $122 | Flat |
| **2025-12** | **$23,312** | **271** | **$86** | **🏆 Best** |
| 2026-01 | $27,088 | 226 | $120 | Regressed |
| **2026-02** | **$25,811** | **124** | **$208** | **📉 Worst** |

Dec 2025 was the efficiency peak — lowest spend AND best CAC. Feb 2026 collapse was driven by poor downstream conversion (signup→active at 7.2% vs Dec's 15.8%), not spend level.

### 5.3 Diminishing Returns (Turkey)

The data shows a clear saturation threshold at **~$27K–$30K/month** for Turkey:
- Below $30K: each $1K generates ~10 marginal actives (~$100/marginal active)
- Above $30K: each $1K generates ~5–6 marginal actives (~$170–225/marginal active)
- **meta_w2a consumed $10.6K in Jan (39% of budget) with only 3 actives** — the single biggest efficiency drain

### 5.4 LTV Model (Parameterized — Base Case)

| Country | Monthly Vol/User | FX Margin | Lifetime | LTV/Active |
|---|---:|---:|---:|---:|
| Turkey | $2,000 | 0.60% | 6 mo | **$72** |
| Nigeria | $800 | 0.60% | 6 mo | **$29** |
| Egypt | $600 | 0.60% | 6 mo | **$22** |

⚠️ These are assumption-driven. Real withdrawal volumes, margins, and retention curves are needed.

### 5.5 LTV/CAC Ratios

| Country | CAC ($/Active) | Base LTV | LTV/CAC | Payback | Viable? |
|---|---:|---:|---:|---:|---|
| Turkey | $864 | $72 | **0.08×** | 72 months | ❌ Not at current CAC |
| Nigeria | $16 | $29 | **1.8×** | 3.3 months | ✅ If KYC fixed |
| Egypt | $64 | $22 | **0.34×** | 17.8 months | ⚠️ Borderline |

**Turkey's $864/active is an outlier** driven by a specific weekly snapshot. The 6-month average (~$86–$127/active) gives LTV/CAC of 0.6–0.8× at base case — still below 1×, indicating the need for either margin improvement or CAC reduction.

---

## 6. Channel Performance

### 6.1 Scorecard (Scale / Optimize / Kill)

| Channel | Spend/wk | Installs | $/Active (Sheets) | Withdrawals | Verdict |
|---|---:|---:|---:|---:|---|
| **Apple Search Ads** | $601 | 75 | $22.66 | 254 | 🟢 **SCALE** |
| **Google Pmax** | $806 | 27 | $19.18 | 15 | 🟢 **SCALE** |
| **Google Search** | $790 | 27 | $25.48 | 14 | 🟢 **SCALE** |
| **Referral** | $0 | 7 | $0 | 13 | 🟢 **INVEST** |
| **Organic** | $0 | 632 | — | 487 | 🟢 **PROTECT** (ASO) |
| **Meta** | $2,754 | 122 | $82.21 | 22 | 🟡 **FIX MEASUREMENT** |
| **Architect (NG)** | ~$0 | 73 | — | 0 | 🟡 **WATCH** (2-wk gate) |
| **TikTok** | $341 | 49 | $28.42 | 0 | 🔴 **PAUSE** |
| **Appnext** | $447 | 273 | $893 | 1 | 🔴 **KILL** |

### 6.2 Reallocation Plan

**Free up:** Appnext ($447/wk) + TikTok ($341/wk) = **$788/wk**

**Redistribute:**
- +$500/wk → Google Pmax (best activation efficiency)
- +$200/wk → Google Search (high-intent protection)
- +$88/wk → Apple Search Ads (incremental intent)

### 6.3 Google Ads Deep-Dive

- **Pmax** is the best activation channel: $19/active, algorithm-optimized across surfaces
- **Search (Brand)** delivers highest downstream quality: $6.37/virtual account
- **Demand Gen retargeting** (TR-Discovery): 1,627 clicks, 0 installs — **pause immediately**
- **Competitor (Payoneer):** ₺938–1,047 CPI, <1 install/week — **kill or reduce to monitoring budget**

### 6.4 Meta Ads Assessment

Meta is the 3rd largest paid channel (~$9K/month Turkey) but delivers the worst cost/active ($82 vs Google's $19–25). However, legacy Meta campaigns show 76 withdrawals/week — the channel CAN work. The core issue is **measurement**: with 60%+ downstream conversions unattributed, Meta's true ROI is unknown. Fix attribution before deciding to scale or cut.

---

## 7. Critical Issues

### Issue 1: KYC Block for Non-Turkish Markets 🚨

**Impact:** 54% of installs (NG + EG + PK) cannot complete onboarding. All acquisition spend in these markets yields zero new activated users.

**Root cause:** BridgeXYZ KYC Component Shown = 0 for all non-TR countries. The eligibility/routing layer blocks the widget from rendering.

**Evidence:** KYC Submit events exist in only 7 countries, all with European/supported ID documents. Zero exceptions across the full analysis week.

**Resolution path:**
1. Confirm BridgeXYZ jurisdiction/document support
2. If unsupported: add alternative provider (Smile Identity for NG, local providers for EG)
3. If technical issue: reproduce on fresh device with real non-TR ID, capture error telemetry

### Issue 2: iOS KYC Gap (3.8× Worse Than Android) ⚠️

**Impact:** iOS generates 53% of withdrawals but has 2.4% KYC Shown→Submit vs Android's 9.2%.

**Hypotheses (ranked):**
1. Submit button occlusion (keyboard, webview viewport)
2. BridgeXYZ SDK rendering issue in iOS WebView
3. Event instrumentation failure (Submit click not firing on iOS)
4. Camera/document capture permission flow breaking

**Resolution:** QA the full KYC flow on iOS devices (multiple models); check event parity in Amplitude.

### Issue 3: Attribution Gap (61% Unattributed) ⚠️

**Impact:** 61% of withdrawals and 82% of sign-ups have no channel attribution. Channel ROI calculations are directional at best.

**Likely causes:**
- AppsFlyer attribution window expiry
- Web-to-app flows losing tracking (754 web sign-ups)
- Cross-device journeys not captured
- Meta Web2App handoff losing attribution at app store redirect

**Resolution:** Audit AF settings, implement deferred deep linking, extend lookback windows, cross-reference Meta CAPI with AF data.

---

## 8. 90-Day Action Plan

### Week 1–2: Emergency Fixes

| # | Action | Owner | KPI Gate |
|---|---|---|---|
| 1 | **KYC incident triage:** Confirm BridgeXYZ support for NG/EG documents. Reproduce KYC flow on real devices. | Product/Eng | KYC Shown > 0 for NG |
| 2 | **iOS KYC investigation:** QA submit flow on iOS; check event instrumentation parity | Eng/QA | iOS Shown→Submit > 5% |
| 3 | **Pause Appnext + TikTok; reallocate $788/wk to Google + ASA** | Growth | Immediate |
| 4 | **Pause Google Demand Gen retargeting** (0 installs from 1,627 clicks) | Growth | Immediate |
| 5 | **Cap NG/EG spend** to small test budgets until KYC is non-zero | Growth | KYC Submit > 0 |

### Week 3–4: Measurement & Quick Wins

| # | Action | Owner | KPI Gate |
|---|---|---|---|
| 6 | **Attribution repair sprint:** Audit AF settings, fix web-to-app deep linking, extend lookback | Growth/Eng | Unattributed sign-ups < 50% |
| 7 | **Roll out KYC follow-up messaging** (450% CVR lift proven in Egypt test) | Lifecycle | KYC submit rate +20% |
| 8 | **Launch geo-gating dashboard:** Daily KYC submit by country + alert if any drops to zero | Data | Operational |
| 9 | **Scale Google Pmax to $1,300/wk** and Search to $1,000/wk | Growth | Cost/Active < $25 |
| 10 | **Increase ASA to $700/wk;** expand to competitor + generic keywords | Growth | CPI < $12 |

### Month 2: Scale Unlocked Markets

| # | Action | Owner | KPI Gate |
|---|---|---|---|
| 11 | **If KYC fixed for NG:** Ramp Nigeria spend to $1–2K/month on Google Search | Growth | KYC Submit/Install > 5% |
| 12 | **If KYC fixed for EG:** Scale Egypt to $4–6K/month; use Architect LP + Arabic creatives | Growth | $/Active < $80 |
| 13 | **Meta attribution audit complete:** Decide scale or cut based on true ROI data | Growth | Cost/Active clarity |
| 14 | **Invest in referral program UX** — highest quality per-user channel (42.9% signup rate) | Product | Referral installs > 50/wk |
| 15 | **Turkey budget ceiling at $30K/month** until signup→active conversion improves | Growth | $/Active < $120 |

### Month 3: Optimize & Prove Unit Economics

| # | Action | Owner | KPI Gate |
|---|---|---|---|
| 16 | **Pull real LTV data:** withdrawal volumes, unique transacting users, cohort retention | Data/Finance | Replace parameterized model |
| 17 | **Build canonical fact table:** month × country × channel × spend × signups × virtacc × active | Data | Single source of truth |
| 18 | **If NG/EG scaling:** Validate LTV/CAC > 1.0× with real data before exceeding $5K/month | Finance | LTV/CAC > 1.0× |
| 19 | **Creative refresh for Meta:** Target 15–20 creatives per market to combat fatigue | Creative | CPM and CTR stable |
| 20 | **Set up true D1/D7/D30 retention** via Amplitude Retention API or BigQuery cohort SQL | Data | Retention dashboard live |

---

## 9. Appendix: Data Confidence Notes

| Data Point | Confidence | Caveat |
|---|---|---|
| Install & sign-up volumes (Amplitude) | 🟢 High | Small source variance (<5%) |
| KYC event breakdown by country/platform | 🟢 High | Event-level, confirmed across full week |
| KYC = 0 for NG/EG/PK (systemic) | 🟢 High | No single-day exceptions |
| Feature engagement by country | 🟢 High | Consistent with user base distribution |
| Install→Sign-up conversion | 🟡 Medium | 754 "(none)" sign-ups inflate global rate |
| Deposit/Withdrawal volumes | 🟡 Medium | Cross-cohort; includes returning users |
| iOS vs Android KYC gap | 🟡 Medium | Could be real UX issue OR instrumentation gap |
| Channel CAC (Sheets) | 🟡 Medium | Spend and outcomes from different weeks; definitions vary across tabs |
| Country CAC (NG/EG sheet) | 🟡 Medium | Attractive on paper but blocked by KYC = 0 |
| Channel withdrawal attribution | 🟠 Low-Med | 61% unattributed; channel ROI is directional |
| LTV model | 🟠 Low | Fully parameterized — no observed volumes or margins |
| Retention metrics | 🟠 Low | DAU/cumulative signups is crude proxy; avg 50.5% |
| "Virtual account" definition | 🔴 Very Low | 3.6× spread across three sheet sources for same month |

### Known Instrumentation Issues
1. **KYC Shown > KYC Started** (3,139 vs 3,098) — event ordering inconsistency
2. **KYC Updated >> KYC Submit** (1,480 vs 179) — Updated is backend-driven, not a funnel step
3. **754 sign-ups with "(none)" country** — country property not set for web flows
4. **AppsFlyer attribution not propagating** to downstream Amplitude events for most users

### Metric Reconciliation Warning
The CAC Analysis sheet, Budget Tracking sheet, and Amplitude show different numbers for the same metrics. Feb 2026 Turkey spend differs by $9.6K (37%) between sheets. Virtual account counts differ 3.6× for Jan 2026. **A canonical fact table is needed before any metric can be treated as "high confidence."**

---

*This report synthesizes 20+ analysis files produced during Sprint 040–050. All recommendations are data-backed but subject to the confidence levels noted above. The next version should incorporate real LTV data, resolved KYC blocking, and unified metric definitions.*


---

> ⚠️ **Attribution caveat:** Web campaigns (Meta/Google → cenoa.com → app store) may appear as "Organic" or "(none)" due to broken web→app attribution. Estimated correction factor: ~6.9×. See [attribution-reconciliation.md](attribution-reconciliation.md) for details.
