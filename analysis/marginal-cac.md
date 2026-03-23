# [043] Marginal CAC Analysis

**Generated:** 2026-03-21  
**Scope:** Turkey (14-month time series) + Egypt/Nigeria (early-stage)  
**Key question:** Where do diminishing returns kick in?

---

## 1) Turkey — Spend vs Outcomes (Sep 2025 → Feb 2026)

```
Month     | Spend    | Signups | Virt Acc | Active | $/Active
----------|----------|---------|----------|--------|--------
2025-09   | $35,839  | 2,357   |   687    |  283   | $127
2025-10   | $29,556  | 1,566   |   550    |  242   | $122
2025-11   | $26,850  | 1,500   |   628    |  221   | $122
2025-12   | $23,312  | 1,719   |   754    |  271   | $ 86  ← BEST
2026-01   | $27,088  | 2,751   |   900    |  226   | $120
2026-02   | $25,811  | 1,721   |   580    |  124   | $208  ← WORST
```

**Visual trend ($/Active):**
```
$208 |                                              ●
     |
$150 |
$127 | ●
$122 |     ● ●                               ●
     |
$ 86 |              ●
     +----+----+----+----+----+----
      Sep  Oct  Nov  Dec  Jan  Feb
```

**Key observation:** Dec 2025 is the clear efficiency peak — lowest spend AND best CAC. Feb 2026 collapse is driven by poor downstream conversion (signups → active), not spend level alone.

---

## 2) Marginal Efficiency: What Does Each Extra $1K Buy?

### Month-over-month deltas (focus period)

| Transition | Δ Spend | Δ Signups | Δ Virt Acc | Δ Active | Verdict |
|---|---:|---:|---:|---:|---|
| Sep → Oct | –$6,283 | –791 | –137 | –41 | Proportional cut, ~flat efficiency |
| Oct → Nov | –$2,706 | –66 | +78 | –21 | Small cut, virt acc improved |
| **Nov → Dec** | **–$3,538** | **+219** | **+126** | **+50** | **🏆 Cut spend, got MORE output** |
| Dec → Jan | +$3,776 | +1,032 | +146 | –45 | Extra $ bought signups, NOT actives |
| Jan → Feb | –$1,277 | –1,030 | –320 | –102 | Collapse (seasonal + mix) |

### The Nov → Dec signal is critical

Cutting $3.5K in spend **increased** all three metrics. This means Nov's marginal $3.5K was *destroying value* — likely wasted on poor-converting channels (meta_w2a at $274/virt_acc in Nov).

### Dec → Jan: top-of-funnel inflation

Adding $3.8K bought 1,032 extra signups ($3.66/marginal signup — great!) but produced **45 fewer actives**. The extra spend inflated vanity metrics without converting downstream. Classic sign of diminishing returns in action.

---

## 3) Diminishing Returns: Spend Bands

### Full 14-month analysis

| Spend Band | Months | Avg Spend | Avg Active | Avg $/Active | Median $/Active |
|---|---:|---:|---:|---:|---:|
| < $15K | 1 | $9,266 | 369 | $25 | $25 |
| $23K–$30K | 5 | $26,523 | 217 | $132 | $122 |
| $33K–$38K | 7 | $35,841 | 304 | $123 | $118 |
| > $50K | 1 | $52,458 | 375 | $140 | $140 |

### What the data says

```
Actives
  400 |  ●                                       ●
      |              ●
  350 |                    ●
      |        ●          ●
  300 |                 ●
      |  ...●..●.........
  250 |           ●              ●
      |                               ●  ●
  200 |                                        ●
      +------+--------+---------+--------+------
       $9K   $23K    $30K     $37K    $52K
                      Spend →
```

**The curve flattens aggressively above $30K:**
- Going from $9K → $27K (+$18K) adds ~0 net actives (Apr's 369 vs Jan's 226) — but Apr had massive organic tailwinds, so the real floor is likely ~220-270 actives at $23-27K
- Going from $27K → $36K (+$9K avg) adds ~87 actives at **~$103 marginal** — acceptable
- Going from $36K → $52K (+$16K) adds only ~71 actives at **~$225 marginal** — clear over-saturation

### Diminishing returns threshold: **~$27K–$30K/month** for Turkey

Below this, each $1K generates ~10 marginal actives (~$100/marginal active).  
Above this, each $1K generates ~5-6 marginal actives (~$170-225/marginal active).

---

## 4) The Apr 2025 Anomaly vs Feb 2026 Worst Case

| | Apr 2025 | Feb 2026 | Gap |
|---|---|---|---|
| Spend | $9,266 | $25,811 | 2.8× more |
| Signups | 1,687 | 1,721 | ~same |
| Actives | 369 | 124 | **3× fewer** |
| $/Active | **$25** | **$208** | 8.3× worse |

**Why Apr was magical:**
- Ultra-low spend = only the most efficient channels active
- Likely strong organic/viral wave (1,687 signups on $9K suggests heavy organic contribution)
- Downstream conversion was excellent (22% signup→active vs Feb's 7.2%)

**Why Feb collapsed:**
- Conversion funnel degraded (7.2% signup→active is the worst in the dataset)
- Channel mix issues: meta_w2a still absorbing budget despite $3,500+/active in Jan
- Possible seasonal effect (post-holiday slump)

**Lesson:** The 8× CAC difference isn't primarily about spend level — it's about **funnel conversion rate**. Even at $9K, if Feb's conversion held, you'd get $75/active (good but not $25).

---

## 5) Country-Level Spend Recommendations

### 🇹🇷 Turkey

| Scenario | Monthly Budget | Expected $/Active | Expected Actives |
|---|---:|---:|---:|
| **Efficiency-first** | $23K–$27K | $86–$120 | 220–270 |
| **Balanced growth** | $27K–$33K | $110–$130 | 250–320 |
| **Max volume** | $33K–$38K | $118–$140 | 280–350 |
| ❌ Over-saturation | > $40K | > $140 | Diminishing hard |

**Recommendation: $25K–$30K/month** with aggressive channel reallocation:
- ✅ **Scale:** Apple Ads ($59-$157/active), Referral/Affiliate ($30/active), PMax Search ($153-$169/active)  
- ⚠️ **Cap:** Meta app ($213/active) — keep under $1K/mo
- ❌ **Kill/Pause:** meta_w2a ($1,124–$3,536/active — consistently terrible)
- 🧪 **Test:** Spaze DSP ($180/active but small sample), TikTok app (needs volume test)

**Channel reallocation alone could save $5K-$10K/month** while maintaining output. meta_w2a consumed $10.6K in Jan (39% of budget!) with only 3 actives.

### 🇪🇬 Egypt

| Metric | Current (Mar 1-15) | Recommendation |
|---|---|---|
| Spend | $5,549 / 2wk | **$4K–$6K/month** |
| $/Active | $107 | Target: < $80 |
| Best channels | Meta LTV test, Google Search | Scale these first |

Egypt is early-stage. Keep spend modest until cost/active stabilizes below $80. The Meta LTV test ($812 → 15 actives = $54/active in one week) looks promising.

### 🇳🇬 Nigeria

| Metric | Current (Mar 1-15) | Recommendation |
|---|---|---|
| Spend | $230 / 2wk | **$1K–$2K/month** |
| $/Active | $16 | Suspiciously good — verify attribution |
| Best channels | Google Search (only channel) | Test 1-2 more |

⚠️ Nigeria's $16/active on $230 spend needs verification. At this level, organic spillover likely dominates. Test with $1-2K/month on Google Search before scaling. If $/active stays < $30 at $2K, consider scaling to $5K.

---

## 6) Action Items

1. **Immediately reallocate Turkey budget away from meta_w2a** — this channel burns $4-10K/month with consistently terrible conversion. Redirect to Apple Ads + Referral/Affiliate.

2. **Set Turkey ceiling at $30K/month** until funnel conversion improves. Current conversion (signup→active) is at historic lows.

3. **Investigate Feb 2026 conversion collapse** — 7.2% signup→active is anomalous. Check: onboarding changes, KYC friction, product issues, attribution gaps.

4. **Don't chase the Apr 2025 benchmark of $25/active** — it was an organic-dominated anomaly. Realistic paid-only target: **$86–$100/active** (Dec 2025 benchmark).

5. **Egypt/Nigeria: stay in test mode** ($4-6K and $1-2K respectively). Scale only on proven cost/active thresholds.

---

## Files
- Machine-readable: `data/marginal-cac.json`
- Depends on: `data/sheets-cac-analysis.json`, `analysis/blended-cac.md`


---

> ⚠️ **Attribution caveat:** Web campaigns (Meta/Google → cenoa.com → app store) may appear as "Organic" or "(none)" due to broken web→app attribution. Estimated correction factor: ~6.9×. See [attribution-reconciliation.md](attribution-reconciliation.md) for details.
