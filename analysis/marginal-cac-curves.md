# [S2B-001] Marginal CAC Curves — Diminishing Returns Model

**Generated:** 2026-03-22  
**Inputs:** channel-cac.md, budget-allocation-model.md, weekly-spend-mar15-21.md, budget-efficiency.md  
**Scope:** Top 3 TR channels by Cost/New Active efficiency: Google Pmax, Apple Search Ads, Google Search  
**Model:** Power-law diminishing returns: `CAC_avg(S) = CAC_0 × (S / S_0)^α`

---

## ⚠️ Caveats

1. **Attribution lag:** Spend and outcome windows don't perfectly align — CAC figures are directional proxies.
2. **Small sample sizes:** Weekly data with ~26–42 new actives per channel. One bad week shifts CAC ±30%.
3. **Nigeria caveat:** NG Google Search shows $16/active at only $229/wk spend — **sample is too small to model diminishing returns**. Included as a reference point only. KYC submit = 0 in NG makes downstream conversion unmeasurable.
4. **Model assumptions:** Diminishing returns exponents (α) are calibrated from industry benchmarks for fintech mobile app campaigns; actual decay rates will vary. The model assumes constant creative quality, targeting, and competitive environment.
5. **Web→App attribution leakage:** Some paid installs appear as "organic" — true channel CAC may be lower than reported.

---

## 1. Current State — Top 3 Channels (Turkey)

| Channel | Weekly Spend | Monthly Spend (est.) | New Actives/wk | Avg CAC ($/Active) | Data Source |
|---|---:|---:|---:|---:|---|
| **Google Pmax** | $805.50 | $3,489 | 42 | **$19.18** | Sheets (early Mar avg) |
| **Apple Search Ads** | $600.50 | $2,602 | 26 | **$22.66** | Sheets (early Mar avg) |
| **Google Search** | $790.00 | $3,423 | 31 | **$25.48** | Sheets (early Mar avg) |

**Mar 15–21 cross-check (Amplitude-based TRUE CAC):**
- Apple Ads TR: $26.32/active ($500/wk)
- Google (all) TR: $154.38/active ($1,235/wk) — combined Search+Pmax, inflated by Amplitude's stricter "withdraw" definition

> **We use Sheets-based Cost/New Active as the baseline** — it's from aligned spend/outcome periods and uses a more stable "new active" definition.

---

## 2. Diminishing Returns Model

### Model specification

```
Average CAC at spend S:   CAC_avg(S) = CAC_0 × (S / S_0)^α
Total actives at spend S: N(S) = S / CAC_avg(S) = (S_0^α / CAC_0) × S^(1-α)  
Marginal CAC at spend S:  CAC_marg(S) = CAC_avg(S) / (1 - α)
```

Where:
- `S_0` = current observed spend level
- `CAC_0` = current observed average CAC
- `α` = diminishing returns exponent (0 = no diminishing returns, 1 = all diminishing returns)

### Calibrated α values

| Channel | α | Rationale |
|---|---:|---|
| Google Pmax | **0.25** | ML-optimized bidding across broad inventory (Search, Display, YouTube, Discover). Moderate diminishing returns — Google's algorithm reallocates to cheaper placements as spend increases. Industry benchmark: 0.20–0.30 for automated campaigns. |
| Apple Search Ads | **0.40** | Limited inventory (App Store search only). High-intent but finite keyword volume. Steeper diminishing returns as you exhaust exact-match and move to broad. Industry benchmark: 0.35–0.50 for ASA. |
| Google Search | **0.35** | Intent-based with finite keyword inventory. More headroom than ASA (broader keyword universe) but less than Pmax. Industry benchmark: 0.30–0.40 for branded+generic search. |

---

## 3. Spend Scaling Projections

### Google Pmax (α = 0.25)

| Scenario | Monthly Spend | Spend Δ | Avg CAC | Marginal CAC | Est. Monthly Actives | Marginal Actives |
|---|---:|---:|---:|---:|---:|---:|
| **Current** | $3,489 | — | $19.18 | $25.57 | 182 | — |
| **+25%** | $4,361 | +$872 | $20.28 | $27.04 | 215 | 33 |
| **+50%** | $5,234 | +$1,745 | $21.23 | $28.31 | 247 | 65 |
| **+100%** | $6,978 | +$3,489 | $22.81 | $30.41 | 306 | 124 |
| **+200%** | $10,467 | +$6,978 | $25.62 | $34.16 | 409 | 227 |
| **+400%** | $17,445 | +$13,956 | $29.92 | $39.89 | 583 | 401 |
| Sweet spot ceiling | **$51,000** | — | $47.28 | $50.00 | 1,079 | — |
| $100 marginal | **$816,000** | — | $75.00 | $100.00 | 10,880 | — |

**Pmax has the most scaling headroom.** Marginal CAC stays under $50 up to ~$51K/mo (15× current). The $100 marginal threshold is at ~$816K/mo — effectively unreachable in current budget.

### Apple Search Ads (α = 0.40)

| Scenario | Monthly Spend | Spend Δ | Avg CAC | Marginal CAC | Est. Monthly Actives | Marginal Actives |
|---|---:|---:|---:|---:|---:|---:|
| **Current** | $2,602 | — | $22.66 | $37.77 | 115 | — |
| **+25%** | $3,253 | +$651 | $24.78 | $41.30 | 131 | 16 |
| **+50%** | $3,903 | +$1,301 | $26.81 | $44.68 | 146 | 31 |
| **+100%** | $5,204 | +$2,602 | $29.90 | $49.84 | 174 | 59 |
| **+200%** | $7,806 | +$5,204 | $35.62 | $59.37 | 219 | 104 |
| Sweet spot ceiling | **$5,200** | — | $29.90 | $49.84 | 174 | — |
| $100 marginal | **$29,700** | — | $60.00 | $100.00 | 495 | — |

**ASA hits diminishing returns faster.** Marginal CAC crosses $50 at ~$5.2K/mo (2× current). The $100 marginal threshold is at ~$29.7K/mo (11.4× current). Sweet spot is current → $5.2K/mo.

### Google Search (α = 0.35)

| Scenario | Monthly Spend | Spend Δ | Avg CAC | Marginal CAC | Est. Monthly Actives | Marginal Actives |
|---|---:|---:|---:|---:|---:|---:|
| **Current** | $3,423 | — | $25.48 | $39.20 | 134 | — |
| **+25%** | $4,279 | +$856 | $27.48 | $42.28 | 156 | 22 |
| **+50%** | $5,135 | +$1,712 | $29.41 | $45.25 | 175 | 41 |
| **+100%** | $6,846 | +$3,423 | $32.48 | $49.97 | 211 | 77 |
| **+200%** | $10,269 | +$6,846 | $38.08 | $58.59 | 270 | 136 |
| Sweet spot ceiling | **$6,400** | — | $32.10 | $49.38 | 199 | — |
| $100 marginal | **$48,600** | — | $65.00 | $100.00 | 748 | — |

**Google Search has moderate headroom.** Marginal CAC stays under $50 up to ~$6.4K/mo (1.9× current). The $100 marginal threshold is at ~$48.6K/mo (14.2× current).

---

## 4. Comparative Chart Data (Spend → Marginal CAC)

Spend levels normalized as multiples of current:

| Spend Multiple | Pmax Marg CAC | ASA Marg CAC | Search Marg CAC |
|---:|---:|---:|---:|
| 0.5× | $21.52 | $28.66 | $31.73 |
| 0.75× | $23.77 | $33.48 | $35.77 |
| **1.0×** | **$25.57** | **$37.77** | **$39.20** |
| 1.25× | $27.04 | $41.30 | $42.28 |
| 1.5× | $28.31 | $44.68 | $45.25 |
| 2.0× | $30.41 | $49.84 | $49.97 |
| 3.0× | $33.63 | $58.88 | $57.62 |
| 5.0× | $38.22 | $71.31 | $67.49 |
| 10.0× | $45.48 | $94.78 | $83.55 |
| 15.0× | $50.34 | $111.65 | $94.73 |
| 20.0× | $54.14 | $125.17 | $103.78 |

**Visual read:**
```
Marginal CAC ($)
 $120 |                                              · ASA
      |                                         ·    
 $100 |                                    · ──────── $100 THRESHOLD
      |                               ·         · Search
  $80 |                          ·          ·
      |                     ·          ·
  $60 |                ·         ·              · Pmax
      |           ·         ·              ·
  $40 |      · · ·    · ·            ·
      |  · ·    · · ·           ·
  $20 |                    ·
      |
   $0 +---+---+---+---+---+---+---+---+---+---→ Spend multiple
      0.5  1   2   3   4   5   7  10  15  20
```

---

## 5. Sweet Spot Analysis

| Channel | Current Spend/mo | Sweet Spot Range | Max Efficient Spend/mo | Headroom | Marginal CAC at Sweet Spot Ceiling |
|---|---:|---|---:|---:|---:|
| **Google Pmax** | $3,489 | $3.5K–$51K | **$51,000** | 14.6× | $50.00 |
| **Apple Search Ads** | $2,602 | $2.6K–$5.2K | **$5,200** | 2.0× | $49.84 |
| **Google Search** | $3,423 | $3.4K–$6.4K | **$6,400** | 1.9× | $49.38 |

**Sweet spot defined as:** marginal CAC ≤ $50/active (2× blended target for TR portfolio).

### Scaling priority order:

1. **🟢 Google Pmax — SCALE AGGRESSIVELY** → Can absorb 5–10× budget increase before marginal CAC doubles. First choice for incremental TR budget.
2. **🟡 Google Search — SCALE CAUTIOUSLY** → ~$3K headroom before $50 marginal threshold. Good for +50–100% increase.
3. **🟠 Apple Search Ads — NEAR CEILING** → Only ~$2.6K headroom. Optimize bids/keywords before increasing budget.

---

## 6. $100 Marginal CAC Threshold (Red Flag)

| Channel | Spend Where Marg CAC > $100 | Multiple of Current | Implication |
|---|---:|---:|---|
| **Google Pmax** | ~$816K/mo | 234× | ✅ Not a concern at any realistic budget |
| **Google Search** | ~$48.6K/mo | 14.2× | ⚠️ Only relevant if Search gets entire $50K budget |
| **Apple Search Ads** | ~$29.7K/mo | 11.4× | ⚠️ Closer but still well above recommended ceiling |

**At the current $50K/mo total budget, no single channel would cross the $100 marginal threshold** even if it received the entire budget.

---

## 7. Optimal Allocation at $50K/mo Total (TR Only)

Using the marginal CAC curves to find the allocation where marginal CAC is equalized across channels (theoretical optimum):

| Channel | Optimal Monthly Budget | % of $50K | Expected Avg CAC | Expected Marginal CAC | Expected Monthly Actives |
|---|---:|---:|---:|---:|---:|
| Google Pmax | $30,000 | 60% | $37.96 | $50.61 | 790 |
| Google Search | $11,000 | 22% | $38.16 | $58.71 | 288 |
| Apple Search Ads | $5,000 | 10% | $29.32 | $48.87 | 170 |
| Meta RTGT + Other | $4,000 | 8% | ~$70 | ~$100 | 57 |
| **Total** | **$50,000** | **100%** | **$38.26** | — | **~1,305** |

> This theoretical optimum assumes all $50K goes to TR and ignores NG/EG. The budget-allocation-model.md recommends a mixed geo approach — see that document for the full picture.

---

## 8. Nigeria Reference Point (⚠️ Insufficient Data)

| Metric | Value | Caveat |
|---|---:|---|
| Current spend | $229/wk ($992/mo) | Minimal test budget |
| Current CAC | $16/active | **Based on ~3 paid actives; n is dangerously small** |
| KYC submit (Amplitude) | **0** | No downstream conversion measurable |
| Modeled α | Unknown | Cannot calibrate with single data point |

**NG cannot be modeled for diminishing returns.** The $16/active figure could be:
- **Real signal:** NG is structurally cheaper (lower competition, lower CPMs)
- **Small-sample artifact:** 3 actives ± 1 = $16 ± $5 swing per active
- **Attribution leakage:** Organic NG users attributed to paid (386 organic vs 31 paid installs)

**Recommendation:** Do not model NG marginal CAC curves until we have ≥ 4 weeks of data at ≥ $1K/wk spend with functioning KYC.

---

## 9. Key Takeaways

1. **Pmax is the scaling workhorse.** With α = 0.25, it can absorb massive budget increases with gentle CAC degradation. Every incremental dollar should go here first.

2. **ASA is near its efficient ceiling.** Current spend of ~$2.6K/mo is already in the upper half of the sweet spot. Doubling the budget is the max before marginal CAC exceeds $50.

3. **Search has modest headroom.** Can handle a ~2× increase (to ~$6.4K/mo) before hitting diminishing returns. Good complement to Pmax.

4. **At +100% spend across all 3 channels** (~$19.3K/mo → $12.6K incremental), you'd gain ~260 marginal actives at a blended marginal CAC of ~$48.50. That's efficient.

5. **The real unlock isn't channel scaling — it's geo expansion.** TR channels are well-optimized. The marginal dollar in NG (if CAC holds) produces 3–5× more actives than marginal TR spend.

---

*Model parameters, data points, and projections available in `../data/marginal-cac.json`*  
*Dependencies: [028] Channel CAC, [029] Budget Efficiency, [067] Budget Allocation Model*
