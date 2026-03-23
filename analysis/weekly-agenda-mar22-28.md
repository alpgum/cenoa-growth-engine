# Weekly Agenda — Mar 22–28, 2026

**Sprint:** S2 | **Status:** Execute

---

## P0 — Do Monday (Mar 22)

| # | Action | Owner | Deadline | Dependency |
|---|--------|-------|----------|------------|
| 1 | **Pause Demand Gen, Appnext, TikTok W2A, Meta W2A non-RTGT** — frees ~$2,530/wk of zero-return spend | Acquisition | Mon EOD | None |
| 2 | **Send KYC escalation brief to Product/Eng** — NG/EG handoff bug (89 approved users → 0 reach Bridge UI) + iOS submit collapse (2.4% vs Android 9.2%) | Acquisition → Product | Mon EOD | KYC roadmap doc [095] ready |
| 3 | **Enforce March budget caps per channel** — reallocate freed spend to Pmax/ASA/EG scaling targets; confirm no channel exceeds monthly ceiling | Acquisition | Mon EOD | Pauses (#1) executed first |
| 4 | **Run full automation pipeline** (KPI → anomaly → health → actions → report) — validate Monday cron sequence per launch checklist | Data | Mon EOD | Amplitude + BQ creds verified |

---

## P1 — Do This Week

| # | Action | Owner | Deadline | Dependency |
|---|--------|-------|----------|------------|
| 5 | **Scale Pmax +50%** ($806 → $1,206/wk), **ASA +$500** ($600 → $1,100/wk), **EG Search +$200** ($500 → $700/wk) | Acquisition | Tue Mar 23 | Budget freed from pauses (#1) |
| 6 | **Launch creative tests** — TR-C1 UGC testimonial, TR-C2 CTA copy, NG-C1 messaging pivot, EG-C1 Arabic explainer | Acquisition | Mon–Wed | Creative assets ready (UGC video, Arabic copy) |
| 7 | **LP A/B test setup** — LP-A (single CTA) + LP-B (trust badges above fold); run PageSpeed first, fix LCP > 2.5s | Acquisition + Data | Wed Mar 24 | PageSpeed audit Mon; ~3,500 visitors/variant needed |
| 8 | **Bid strategy changes** — Brand TR → tCPA ₺500, Freelancer TR → breakout + tCPA ₺200, EG Generic → tCPA ₺350, Competitor → manual CPC ₺15-20 | Acquisition | Mon–Wed | Conversion action audit (verify `af_app_install` is primary) |
| 9 | **Attribution fix spec → Eng** — OneLink + deferred deep linking + UTM persistence + `web_session_id`; document in 1-pager for Eng handoff | Data → Product | Fri Mar 27 | Web→app handoff analysis [085] |

---

## P2 — Start This Week

| # | Action | Owner | Deadline | Dependency |
|---|--------|-------|----------|------------|
| 10 | **Appnext fraud credit request** — 273 installs → 0 actives, $893/active; compile evidence for credit/refund claim | Acquisition | Thu Mar 25 | Campaign paused (#1); fraud data documented |
| 11 | **Creative refresh brief to design team** — scope Week 2+ creatives: TR UGC variants, NG payment-intent series, EG Arabic education set | Acquisition | Fri Mar 27 | Week 1 creative test results (early signals) |
| 12 | **Weekly report automation dry-run** — run full cron chain manually per launch checklist §4; validate outputs, fix failures, document gaps | Data | Fri Mar 27 | All scripts + creds working (#4) |

---

**Weekly checkpoint:** Friday Mar 28 — review early test signals, kill underperformers, prep Week 2 scaling decisions.

*Expected net impact: +265 new actives/month at 33% lower blended CAC — budget-neutral.*
