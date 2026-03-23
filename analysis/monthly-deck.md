# Monthly Executive Deck — February 2026

Generated: `2026-03-21 04:57 TRT`

## Exec summary
- **KYC is the single biggest funnel killer.** 94.2% of users who start KYC never submit — and outside Turkey, KYC completion is literally zero (BridgeXYZ doesn't render for NG/EG/PK).
- **Turkey carries the business.** 95% of KYC submits, 57% of withdrawals, and the only market with a functioning end-to-end funnel.
- **Nigeria and Egypt are blocked goldmines.** Together they represent 46% of installs and show strong feature engagement, but zero new-user activation due to the KYC hard block.
- **iOS converts 3.8× worse than Android at KYC** (2.4% vs 9.2% Shown→Submit), and 62% of sign-ups come from web with almost no downstream conversion.
- **Channel quality varies wildly.** Apple Search Ads delivers 254 withdrawals from 75 installs; appnext delivers 1 withdrawal from 273 installs. Budget reallocation is the fastest ROI lever after KYC.

### Most recent KPI pulse (weekly snapshot)
- 📲 Installs: 1,453 (▼36.1%)
- 📝 Signups: 1,219 (▼27.0%)
- ✅ KYC Submit: 185 (▼39.7%)
- 💳 Withdrawals: 2,236 (▬ flat)
- 👤 DAU avg: 3,075

## KPI snapshot + deltas
### Turkey unit economics — February 2026 vs January 2026
| Metric | February 2026 | January 2026 | Δ |
|---|---|---|---|
| Spend (TR) | $25,811 | $27,088 | -4.7% |
| Signups (TR) | 1,721 | 2,751 | -37.4% |
| Virtual accounts (TR) | 580 | 900 | -35.6% |
| New active (TR) | 124 | 226 | -45.1% |
| CAC / Signup (TR) | $15.00 | $9.85 | 52.3% |
| CAC / Virtual acct (TR) | $44.50 | $30.10 | 47.8% |
| CAC / New active (TR) | $208.15 | $119.86 | 73.7% |

Global realized spend (budget tracking) for **February 2026**: **$57,570**

## Funnel + KYC issues
Primary constraint: **KYC** (conversion + availability across markets).
References: analysis/funnel-summary.md

## CAC & budget efficiency
### Low-quality flags (latest weekly)
- **TikTok** — installs>=20 and withdrawals==0
- **Appnext** — cheap CPI + near-zero downstream (new_active=0; withdrawals<=1)

### Suggested reallocation (weekly proxy)
- Pause: `Appnext, TikTok`
- Reallocate weekly USD to:
  - Pmax: $500
  - Google Search: $200
  - Apple Search Ads: $88

### Budget pacing (context)
- Month: `2026-03`
- Status: **OVERSPENDING** (pace 159.7%)
- Expected spend: **$33,871** | Est. actual: **$54,082**
- Note: Extrapolated from TR weekly cost ($9756/wk) scaled to all geos. 21 days elapsed. ⚠️ Real-time pacing needs fresh Sheets or ad-platform API pull.

## Attribution caveat
- Spend sources are mixed (finance budget tracking vs marketing-attributed spend).
- Deposits/withdrawals are cross-cohort in current reporting (include returning users).
- Large attribution loss in AppsFlyer/Amplitude join; treat channel ROI as directional.

## Market plans
- Turkey 90D Plan: `analysis/turkey-90d-plan.md`
- Nigeria Growth Plan: `analysis/nigeria-growth-plan.md`
- Egypt Scaling Plan: `analysis/egypt-scaling-plan.md`
- Pakistan Prelaunch Plan: `analysis/pakistan-prelaunch-plan.md`
- Multi Market Expansion Playbook: `analysis/multi-market-expansion-playbook.md`

## Next month action plan
- **P0 / Acquisition** — Cap budgets — overspending monthly pace
  - Why: Spend pace at ~159.7% of expected (expected $33,871 vs est. actual $54,082).
  - Impact: Avoid exceeding monthly budget; force reallocation to highest-quality channels.
- **P0 / Data** — Diagnose DAU WoW anomaly (↓46.0%)
  - Why: DAU changed ↓46.0% vs last week (5677.7 → 3065.0).
  - Impact: Identify root cause and unblock recovery within 24h (tracking, spend, funnel, outages).
- **P0 / Product** — Diagnose KYC Submit WoW anomaly (↓41.7%)
  - Why: KYC Submit changed ↓41.7% vs last week (307 → 179).
  - Impact: Identify root cause and unblock recovery within 24h (tracking, spend, funnel, outages).
- **P0 / Acquisition** — Pause & audit appnext (fraud pattern)
  - Why: 1779 installs, 349 signups but only 47 virt_acc (2.6%) — suspicious downstream
  - Impact: Reduce low-quality traffic and protect downstream conversion.
- **P0 / Acquisition** — Pause twitter_ads (DEAD spend)
  - Why: $183 spent, 1 installs but 0 signups & 0 activations
  - Impact: Stop wasted spend and reallocate budget to healthy channels.
- **P0 / Acquisition** — Pause & audit appnext_dsp (fraud pattern)
  - Why: 113 installs but only 2 signups (1.8% conversion) — fraud pattern
  - Impact: Reduce low-quality traffic and protect downstream conversion.
- **P1 / Acquisition** — Diagnose Installs WoW anomaly (↓36.3%)
  - Why: Installs changed ↓36.3% vs last week (2274 → 1448).
  - Impact: Identify root cause and unblock recovery within 24h (tracking, spend, funnel, outages).
- **P1 / Product** — Diagnose Virtual Account Opened WoW anomaly (↓31.3%)
  - Why: Virtual Account Opened changed ↓31.3% vs last week (632 → 434).
  - Impact: Identify root cause and unblock recovery within 24h (tracking, spend, funnel, outages).
- **P0 / Product** — Escalate EG KYC blocked (0 submits)
  - Why: EG shows 206 installs / 64 signups but 0 KYC submits in country breakdown.
  - Impact: Unblock onboarding; recover KYC conversion in a priority geo.
- **P0 / Product** — Escalate NG KYC blocked (0 submits)
  - Why: NG shows 458 installs / 117 signups but 0 KYC submits in country breakdown.
  - Impact: Unblock onboarding; recover KYC conversion in a priority geo.

---

## Gamma instructions
- Paste this markdown into Gamma → *Create from text*.
- Or use `data/monthly-deck.json` as a structured outline.
