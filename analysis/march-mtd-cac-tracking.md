# March 2026 MTD — CAC Tracking vs Targets

**Generated:** 2026-03-22  
**Period:** March 1–21, 2026 (21/31 days = 67.7% elapsed)  
**Hard data:** Through Mar 15 (Sheets); Mar 16–21 estimated via W2 daily run-rate  
**Definitions:** See [metric-definitions.md](metric-definitions.md) — TRUE CAC = cost per new_active (first withdrawal)

---

## 1. March MTD TRUE CAC by Country — Actual vs Target

TRUE CAC = Total Spend ÷ New Active (unique users with first withdrawal)

| Country | Spend (15d) | New Active | TRUE CAC (Actual) | Target (Budget Model) | vs Target | Status |
|---------|------------:|-----------:|-------------------:|----------------------:|----------:|--------|
| TR | $7,824 | 292 | **$26.79** | $100–$130 | ✅ 74–79% below | Well below target |
| NG | $230 | 31 | **$7.42** | $20–$40 | ✅ 63–81% below | Well below target |
| EG | $5,549 | 81 | **$68.51** | $50–$80 | 🟡 Within range | At target |
| **Total** | **$13,603** | **404** | **$33.67** | $48–$81 | ✅ Below target | Efficient |

> **Reading:** TR and NG TRUE CAC look exceptionally strong vs targets. EG sits within the $50–$80 target band. Blended $33.67 is well below the Scenario B target of $48–$81.

### Why TR TRUE CAC Looks So Good — Handle With Care

TR's $26.79/new_active is suspiciously low vs the budget model's $100–$130 target. Likely causes:

1. **Returning-user contamination in "Withdraw Completed":** The withdrawal event captures ALL users who withdraw, not just newly acquired ones. Amplitude's weekly data shows 568 withdrawals in W3 alone — far exceeding the ~100 new users that week could have produced. Many are returning/existing users.
2. **Under-pacing spend:** TR is only at 50.1% of budget ($11.5K est. vs $23K plan). Lower spend → cherry-picking highest-intent users → lower CAC. This won't hold at scale.
3. **Attribution leakage:** 43.7% of installs and 81.7% of signups are unattributed — the spend denominator may be undercounting (some "organic" users were paid-driven).

**True steady-state TR CAC is likely $80–$150/new_active**, not $26.79.

---

## 2. March MTD Cost per Virtual Account Opened by Country

⚠️ **This is NOT true CAC** — virtual account opened does not equal an active user.

| Country | Spend (15d) | Virt Acc Opened | Cost / Virt Acc | vs TRUE CAC |
|---------|------------:|----------------:|----------------:|-------------|
| TR | $7,824 | 776 | **$10.08** | 2.7× cheaper (vanity) |
| NG | $230 | 260 | **$0.88** | 8.4× cheaper (vanity) |
| EG | $5,549 | 217 | **$25.57** | 2.7× cheaper (vanity) |
| **Total** | **$13,603** | **1,253** | **$10.86** | 3.1× cheaper (vanity) |

> **Why this matters:** The March budget projections tab uses "new_accounts" (≈ virt_acc) with a $37.21 target CPA. By that softer metric, TR looks amazing at $10.08. But virt_acc → new_active conversion is only **37.6% in TR**, **12.0% in NG**, and **37.3% in EG**. Most virtual account holders never transact.

---

## 3. TRUE CAC by Country Deep-Dive

### 🇹🇷 Turkey — $26.79/new_active

| Metric | Value |
|--------|------:|
| Spend (15d) | $7,824 |
| Installs | 3,289 |
| Signups | 1,176 |
| Virtual Accounts | 776 |
| New Active (first withdrawal) | 292 |
| **TRUE CAC** | **$26.79** |
| Install → New Active rate | 8.9% |
| Budget model target | $100–$130 |

**Channel-level spend (15d):**

| Channel | Spend (15d) | Est. 21d | Pacing % | Budget Model Expected $/Active |
|---------|------------:|---------:|---------:|-------------------------------:|
| Google Pmax/Search | $1,636 | $2,305 | 61.5% | $19–$25 |
| Meta (W2A + RTGT) | $1,327 | $1,742 | 232.3% | $67 (RTGT only) |
| Apple Search Ads | $1,159 | $1,587 | 56.7% | $23 |
| TikTok | $682 | $994 | 82.8% | ❌ Paused (budget model) |
| Spaze + Appnext | $2,663 | $3,776 | 83.9% | $31 (Spaze only; Appnext ❌) |
| Twitter | $183 | $260 | 26.0% | Not in model |

> ⚠️ Channel-level new_active attribution is unavailable (81.7% of signups are "(none)" source). Channel TRUE CAC cannot be calculated — only country-level blended.

### 🇳🇬 Nigeria — $7.42/new_active

| Metric | Value |
|--------|------:|
| Spend (15d) | $230 |
| Installs | 1,445 |
| Signups | 614 |
| Virtual Accounts | 260 |
| New Active | 31 |
| **TRUE CAC** | **$7.42** |
| Install → New Active rate | 2.1% |
| Budget model target | $20–$40 |

**Active channels:** Google Search only ($230 — over-pacing vs $310/mo plan at 137.7%)

> ⚠️ **Extremely low spend inflates efficiency.** At $230 total spend with 1,445 installs, most installs are organic (386 organic in W3 alone). The paid budget is a tiny fraction of total funnel. Real paid CAC is likely higher — NG Google Search is essentially a seed that catalyzes organic discovery.

### 🇪🇬 Egypt — $68.51/new_active

| Metric | Value |
|--------|------:|
| Spend (15d) | $5,549 |
| Installs | 1,252 |
| Signups | 703 |
| Virtual Accounts | 217 |
| New Active | 81 |
| **TRUE CAC** | **$68.51** |
| Install → New Active rate | 6.5% |
| Budget model target | $50–$80 |

**Channel-level spend (15d):**

| Channel | Spend (15d) | Est. 21d | Pacing % |
|---------|------------:|---------:|---------:|
| Google Pmax | $1,210 | $1,553 | 103.6% |
| Meta (get_paid + LTV) | $4,181 | $4,875 | 325.0% |
| Apple Search Ads | $42 | $70 | 14.0% |

> EG sits within the $50–$80 target band, but Meta is 3.3× over budget. If Meta's share of new_active is proportional to its spend share (75%), Meta EG TRUE CAC ≈ $68 — which is within range but teetering at the upper bound.

---

## 4. Trend: March vs February

### Paid Active CAC (cost per repeat-usage user)

| Country | Feb CAC (paid_active) | Mar MTD CAC (paid_active) | Trend |
|---------|----------------------:|-------------------------:|-------|
| TR | $208 | $355.64 | 🔴 **+71% worsening** |
| EG | ~$64–$107 | $89.50 | 🟡 Within Feb range |
| NG | ~$16 | $10.00 | ✅ Improving |

### New Active CAC (TRUE CAC)

| Country | Feb Blended $/Active | Mar MTD TRUE CAC | Trend |
|---------|---------------------:|-----------------:|-------|
| TR | ~$100–$130 (model target) | $26.79 | ⚠️ Looks improved but see caveats |
| EG | ~$50–$80 (model target) | $68.51 | 🟡 Within range |
| NG | ~$16 (at $230 spend) | $7.42 | ⚠️ Low spend, unreliable trend |

### Weekly Trajectory (W2 → W3, from Amplitude)

| Metric | W2 (Mar 8–14) | W3 (Mar 15–21) | WoW Δ |
|--------|---------------:|----------------:|------:|
| Total installs | 2,274 | 1,445 | ▼ 36.5% |
| Total signups | 1,672 | 1,207 | ▼ 27.8% |
| KYC submits | 307 | 179 | ▼ 41.7% |
| Withdrawals | 2,213 | 2,227 | ▲ 0.6% (flat) |
| Virtual accounts (TR) | 372 | 208 | ▼ 44.1% |

**Interpretation:** Top-of-funnel is deteriorating sharply (installs/signups down 28–37% WoW), but withdrawals are flat — suggesting existing user base is stable while new user acquisition is slowing. If spend stays constant but installs decline, **CAC will worsen in the coming weeks.**

---

## 5. Channels Above Target CAC → Action Needed

| Channel | Country | Issue | Estimated Efficiency | Target | Action |
|---------|---------|-------|---------------------|--------|--------|
| **Meta W2A (non-RTGT)** | TR | Budget model flags $1,124–$3,536/active | Catastrophic | ❌ Kill | **Pause immediately** — already recommended in budget model |
| **Appnext** | TR | 1,779 installs → 0–1 new_active (15d) | ∞ (no conversions) | ❌ Kill | **Pause immediately** — fraud pattern confirmed |
| **TikTok** | TR | 0 withdrawals in attribution | ∞ (no conversions) | ❌ Kill | **Pause** — budget model recommends stopping |
| **Meta** | EG | 3.3× over budget at $4,875 est. 21d | ~$68/new_active | $50–$80 | 🟡 **Cap at plan** — near upper bound of target; overspend creates risk |
| **Twitter** | TR | $260 est. spend, unknown downstream | Unmeasurable | N/A | 🟡 **Evaluate or pause** — too small to matter, no attribution signal |

### Total waste estimate (channels that should be paused):
- Appnext TR: ~$2,663 (15d) → $0 in new_active
- TikTok TR: ~$682 (15d) → $0 in attributed withdrawals  
- Meta W2A non-RTGT TR: portion of $1,327 → catastrophic CAC
- **~$3,500–$4,000 recoverable in remaining 10 days**

---

## 6. Channels Below Target CAC → Candidates for Scaling

| Channel | Country | TRUE CAC (est.) | Target | Headroom | Scale Recommendation |
|---------|---------|----------------:|-------:|---------:|---------------------|
| **Google Search** | NG | ~$7.42 blended | $20–$40 | 2.7–5.4× | 🟢 **Scale aggressively** — increase from $310/mo to $3K–$6K. Best CAC in portfolio. |
| **Google Pmax/Search** | TR | ~$19–$25 (model) | $100–$130 | 4–7× | 🟢 **Absorb freed budget** from paused channels. Can take +$3,600/mo per model. |
| **Apple Search Ads** | TR | ~$23 (model) | $100–$130 | 4–6× | 🟢 **Scale up** — high-intent users, can absorb +$2,400/mo. Currently 56.7% of plan. |
| **Google Pmax** | EG | Part of $68.51 blend | $50–$80 | Moderate | 🟡 **Maintain** — on pace at 103.6%, reasonable efficiency. |
| **Meta RTGT** | TR | ~$67 (model) | $100–$130 | 1.5–2× | 🟡 **Maintain** — retargeting proven; don't scale prospecting. |

### Reallocation opportunity (remaining 10 days):

| From | To | Amount | Expected Impact |
|------|----|---------:|----------------|
| Appnext TR (pause) | Google Pmax TR | +$800 | ~32–42 additional new_active |
| TikTok TR (pause) | ASA TR | +$300 | ~12–15 additional new_active |
| Meta W2A non-RTGT TR (pause) | NG Google Search | +$500 | ~25–67 additional new_active |
| EG Meta overspend (cap) | EG Google Pmax | +$500 | Diversify EG away from single channel |
| **Total reallocation** | | **~$2,100** | **~70–125 additional new_active** |

---

## 7. ⚠️ Attribution Caveats

### Why these numbers are directional, not precise

1. **Web-to-App attribution gap:** Cenoa's W2A flow (ad → cenoa.com → app store) breaks the attribution chain. AppsFlyer may classify paid-driven installs as "Organic." In W3, **632 of 1,445 installs (43.7%) are "Organic"** and **986 of 1,207 signups (81.7%) have "(none)" attribution.**

2. **Withdrawal ≠ new user:** The "Withdraw Completed" event includes returning users. W3 shows 568 TR withdrawals but only ~208 new virtual accounts — many withdrawals are from the existing user base, not March acquisitions. This inflates the new_active count and makes TRUE CAC appear lower than reality.

3. **Channel-level CAC is not calculable:** With 81.7% of signups unattributed, assigning new_active to specific channels is unreliable. Channel TRUE CAC figures from the budget model are estimates based on attributed install volume, not direct measurement.

4. **Spend estimation for days 16–21:** Hard spend data ends at Mar 15. Days 16–21 use W2 daily run-rates. Given W3's sharp install decline (−36.5% WoW), actual efficiency may differ materially.

5. **NG's $7.42 CAC is misleading at $230 spend:** With only $230 in paid spend driving 1,445 installs, the vast majority of NG activity is organic. The paid channel is a catalyst, not the primary driver. Scaling 10× will likely raise CAC significantly (diminishing returns untested).

6. **Estimated correction factor:** Attribution reconciliation suggests a ~6.9× correction factor for web campaigns. If applied, true paid-driven volume is higher and blended CAC is lower — but channel-level allocation remains impossible without better attribution infrastructure.

### What to trust vs what to question

| Metric | Reliability | Why |
|--------|-------------|-----|
| Country-level spend | ✅ High | Direct from Sheets (hard data through Mar 15) |
| Total installs/signups | ✅ High | Amplitude event counts are reliable |
| Country-level new_active | 🟡 Medium | Withdrawal events include returning users |
| TRUE CAC (country) | 🟡 Directional | Numerator solid, denominator contaminated |
| Channel-level TRUE CAC | 🔴 Low | 81.7% of signups unattributed |
| NG efficiency at scale | 🔴 Speculative | Only $230 sample size |

---

## Summary

| | TR | NG | EG | Total |
|---|---:|---:|---:|---:|
| **TRUE CAC (actual)** | $26.79 | $7.42 | $68.51 | $33.67 |
| **Target (budget model)** | $100–$130 | $20–$40 | $50–$80 | $48–$81 |
| **Cost / Virt Acc (NOT CAC)** | $10.08 | $0.88 | $25.57 | $10.86 |
| **vs Feb trend** | ⚠️ Looks better, caveats apply | ⚠️ Low spend | 🟡 Within range | — |
| **Action** | Pause waste channels, scale Pmax/ASA | Scale Google Search | Cap Meta overspend | Reallocate ~$2.1K |

**Bottom line:** Headline TRUE CAC numbers look strong vs targets, but the data has significant contamination (returning-user withdrawals, attribution gaps, estimation). The actionable insight isn't the CAC number itself — it's which channels to kill (Appnext, TikTok, Meta W2A non-RTGT) and which to scale (NG Google Search, TR Pmax/ASA). Reallocating ~$2.1K from waste channels in the remaining 10 days could yield 70–125 additional new_active users.

---

*Generated: 2026-03-22 | Sprint S2-005*  
*Dependencies: march-mtd-budget-vs-actual.md, march-mtd-pacing.json, weekly-channel-country-20260322.json, budget-allocation-model.md, metric-definitions.md*
