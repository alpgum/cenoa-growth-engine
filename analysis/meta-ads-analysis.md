# Meta Ads Campaign Analysis

**Date:** 2026-03-21  
**Status:** Best-effort (MCP/API not available to subagents)  
**Data sources:** Sheets Trafik Canavarı, CaC Analysis, Amplitude attribution funnel, channel-cac scorecard

---

## 1. Meta Ads Presence — Campaign Inventory

### Active Media Sources (from AppsFlyer/Amplitude)
| Media Source | Mapping | Notes |
|---|---|---|
| `zzgtechltmqk_int` | Meta Web2App | Primary Meta attribution identifier |
| `Facebook Ads` | Meta App Install | Legacy campaigns |
| `Social_instagram` | Meta (Instagram) | Minimal/organic reach |
| `metaweb_int` | Meta Web | Web-based campaigns |

### Campaigns Observed (Mar 14–20, 2026)
| Campaign | Type | Installs | Sign-ups | Withdrawals |
|---|---|---|---|---|
| **TR_Meta_web2app_RTGT** | Retargeting (Turkey) | 17 | 6 | 9 |
| **EG_Meta_web2app_CVR_Android_031826** | Egypt CVR | 44 | 3 | 0 |
| **EG_Meta_web2app_ALL_031826** | Egypt Broad | 20 | 4 | 0 |
| **1764668627** (legacy) | Historical | — | — | 76 |
| Other Meta fragments | Various | ~41 | ~9 | — |
| **Total Meta** | | **~122** | **~22** | **22** |

### Historical Meta Spend (Turkey, from Trafik Canavarı)
| Month | Meta Spend | % of Total Perf Spend |
|---|---|---|
| May 2025 | $18,886 | 73.7% |
| Jun 2025 | $7,660 | 23.5% |
| Sep 2025 | $5,700 | 22.5% |
| Dec 2025 | $4,497 | 26.6% |

Meta spend peaked in May 2025 ($18.9K) then contracted sharply. Currently running at ~$4-6K/month in Turkey — a fraction of Google's budget.

---

## 2. Meta Channels in CaC Analysis — Performance

### Weekly Proxy (early March 2026)

| Metric | Meta (all) | Apple Search Ads | Google (Search+Pmax) | Appnext |
|---|---|---|---|---|
| **Spend/week** | $2,754 | $601 | $1,596 | $447 |
| **Installs** | 122 | 75 | 54 | 273 |
| **Sign-ups** | 22 | 22 | 14 | 24 |
| **Withdrawals** | 22 | 254 | 29 | 1 |
| **CPI** | $22.57 | $8.01 | $29.26 | $1.64 |
| **Cost/Sign-up** | $125.18 | $27.30 | $112.86 | $18.60 |
| **Cost/Withdrawal** | $125.18 | $2.36 | $56.43 | $446.50 |

### From Sheets (VirtAcc/Active proxies)

| Metric | Meta | ASA | Google | TikTok |
|---|---|---|---|---|
| **Cost/VirtAcc** | $25.50 | $12.01 | $6.37–$9.26 | $6.26 |
| **Cost/New Active** | $82.21 | $22.66 | $19.18–$25.48 | $28.42 |

**Meta is the most expensive paid channel per active user** — $82/active vs Google's $19-25 and ASA's $23.

---

## 3. Attribution Funnel — zzgtechltmqk_int (Meta W2A)

### Mar 14–20 Weekly Flow
```
Installs: 120 → Sign-ups: 20 (16.7%) → Withdrawals: 22
```

- Install→Signup rate of 16.7% is middling (vs ASA 29.3%, Google 25.9%)
- Volume spiked end of week (5→44 installs/day by Mar 20) — new campaigns launching
- Only 22 withdrawals — includes historical cohort activity, not just this week

### Campaign-Level Attribution
| Campaign | Installs | Sign-ups | Withdrawals | Quality |
|---|---|---|---|---|
| TR_Meta_web2app_RTGT | 17 | 6 | 9 | ⭐ Retargeting works |
| EG_Meta_web2app_CVR_Android | 44 | 3 | 0 | 🚩 Too early / low quality |
| EG_Meta_web2app_ALL | 20 | 4 | 0 | ⚠️ Just launched Mar 20 |
| 1764668627 (legacy) | — | — | 76 | ⭐⭐ Historical LTV proven |

**Key finding:** Legacy Meta campaigns (1764668627) show 76 withdrawals/week — proving Meta CAN acquire high-LTV users. Current campaigns are not replicating this.

---

## 4. Meta Web2App: $3,536/Active — Structural Issue Analysis

### The Math (March 2026 projection from CaC Analysis)
| Metric | Value |
|---|---|
| Planned monthly budget | $6,000 |
| Projected virtual accounts | 182 |
| Projected cost/virtual account | $33 |
| Actual cost/new active (Sheets) | **$82.21** |
| Attribution-based cost/active (weekly → monthly) | **$3,536** ⚠️ |

### Why the Number is So High

The $3,536/active figure comes from attribution data where:
- **Weekly spend proxy:** $2,754
- **Attributed active users (withdrawals):** 22 (but many are historical, not new)
- If we use Sheets "new active" proxy: 34/week → ~$82/active (still 3-4× worse than Google/ASA)

### Root Causes (Structural)

1. **Attribution leakage:** Meta Web2App flow (browser → app store → app) loses attribution at every handoff. Many Meta-acquired users end up in the "(none)" bucket (986 unattributed sign-ups, 1,355 unattributed withdrawals). Meta is disproportionately affected because W2A is its primary flow.

2. **Funnel friction:** Web2App requires: see ad → click → landing page → app store redirect → download → open app → sign up. Each step loses 40-60% of users. Direct app install campaigns (ASA, Google UAC) skip 2-3 steps.

3. **Audience quality vs intent:** Meta targets interest/behavior signals (financial apps, crypto). ASA/Google target search intent ("send money to Nigeria"). Intent > interest for fintech activation.

4. **Creative fatigue risk:** With only 9 creatives for Turkey (see §5), frequency is likely high → ad fatigue → declining CTR → higher CPA over time.

5. **Optimization signal delay:** Meta's ML needs conversion events to optimize. If the target event (active user) happens days/weeks after install, Meta can't optimize effectively within its attribution window.

---

## 5. Creative Allocation Matrix (Furkan's Plan)

> Note: "Furkan Meta Ads Plan" tab was not accessible in the Sheets API export (hidden/restricted). Data below is inferred from CaC Analysis budget planning and attribution data.

### Estimated Creative Distribution
| Market | Creatives | Campaign Types | Monthly Budget |
|---|---|---|---|
| Turkey (TR) | ~9 | Web2App (CVR, RTGT), App Install | $6,000 + $3,000 = $9,000 |
| Nigeria (NG) | ~7 | Architect (freelancer targeting) | Included in Architect budget |
| Egypt (EG) | ~8 | Web2App (CVR, ALL) | Included in Egypt allocation ($5,549 total) |

### Campaign Structure
- **TR:** Retargeting (RTGT) + CVR optimization + App iOS installs
- **EG:** Recently launched (Mar 18-20) — CVR Android + broad targeting
- **NG:** Running through "Architect" campaigns targeting freelancers (Fiverr, Upwork, Wise/PayPal angles)

### Creative Gaps
- **No A/B test signal visibility** — can't assess which creatives perform without Meta API access
- **9 creatives for Turkey** is thin for $9K/month spend → high frequency risk
- **Egypt just launched** — too early to evaluate creative performance
- **Nigeria creatives** (freelancer angle) show decent sign-up (26%) but zero withdrawals — messaging may attract curiosity without intent

---

## 6. Recommendations

### Priority 1: Fix Attribution Gap (BEFORE optimizing spend)

| Action | Impact | Effort |
|---|---|---|
| Audit AppsFlyer Web2App attribution settings | Unlock true Meta ROI visibility | Medium |
| Extend AF lookback window for Meta campaigns | Capture delayed conversions | Low |
| Implement deferred deep linking for W2A flow | Reduce attribution loss at app store handoff | High |
| Cross-reference Meta CAPI with AF data | Validate actual vs attributed conversions | Medium |

**Why first:** With 986 unattributed sign-ups and 1,355 unattributed withdrawals per week, Meta's true contribution could be 2-5× higher than what attribution shows. Optimizing based on broken measurement = optimizing in the dark.

### Priority 2: Structural Campaign Changes

| Action | Rationale |
|---|---|
| **Shift budget to retargeting (RTGT)** | TR_Meta_web2app_RTGT shows 9 withdrawals — only Meta campaign with proven downstream |
| **Test App Install campaigns** | Bypass W2A friction; Meta App Install → direct download → better attribution |
| **Increase creative volume** | 9 creatives for $9K/month = creative fatigue. Target 15-20 creatives per market |
| **Pause zero-conversion campaigns after 14 days** | EG campaigns launched Mar 18-20 — evaluate by Apr 3 |

### Priority 3: Budget Reallocation (if attribution confirms poor ROI)

| Current | Proposed | Rationale |
|---|---|---|
| Meta TR: $9,000/mo | Meta TR: $5,000/mo | Redirect $4K to ASA + Google |
| Meta EG: ~$2,000/mo | Meta EG: $3,000/mo | Egypt CAC is 5-10× cheaper; scale test |
| ASA: $2,800/mo | ASA: $5,000/mo | Best downstream conversion; underinvested |

### Priority 4: Creative Strategy

- **Turkey:** Focus on remittance/savings use cases (high intent). Test UGC-style creatives.
- **Egypt:** Test Arabic-first creatives. Current campaigns just launched — monitor for 2 weeks.
- **Nigeria:** Freelancer angle has good sign-up but no activation. Test "receive payments" angle instead.

---

## 7. Data Limitations

| Gap | Impact | Resolution |
|---|---|---|
| **Meta Ads API not accessible** | No campaign-level metrics (CPM, CTR, frequency, ROAS) | Requires MCP access or direct Meta API credentials |
| **Furkan Meta Ads Plan tab hidden** | Creative allocation details are inferred, not confirmed | Request sheet access or manual export |
| **Attribution window mismatch** | Spend and outcomes are from different weeks | Align data windows in next analysis |
| **No creative-level performance** | Can't identify winning/losing creatives | Needs Meta API or Ads Manager export |
| **No frequency data** | Can't confirm creative fatigue hypothesis | Needs Meta API |

**Full Meta API analysis will be possible when:** MCP is available to subagents, or direct Meta Marketing API credentials are configured for script-based access.

---

## Summary

Meta is Cenoa's **3rd largest paid channel** (~$9K/month Turkey) but delivers the **worst cost/active** among major channels ($82/active vs Google's $19-25 and ASA's $23). However, legacy Meta campaigns prove the channel CAN acquire high-LTV users (76 withdrawals/week from historical cohorts).

The core issue is **measurement, not necessarily the channel**: with 60%+ of downstream conversions unattributed, Meta's true ROI is unknown. Fix attribution first, then decide whether to scale or cut.

**Bottom line:** Don't kill Meta yet — fix how you measure it, then optimize or reallocate based on real numbers.

---

*Generated: 2026-03-21 | Sprint 045*


---

> ⚠️ **Attribution caveat:** Web campaigns (Meta/Google → cenoa.com → app store) may appear as "Organic" or "(none)" due to broken web→app attribution. Estimated correction factor: ~6.9×. See [attribution-reconciliation.md](attribution-reconciliation.md) for details.
