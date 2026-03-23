# Cenoa Growth Engine — Sprint 2B Task Queue

> Sprint started: 2026-03-22 22:20 TRT
> Slots: 3 auto
> Previous: Sprint 2A (30 tasks) — ALL DONE

---

## GROWTH EXECUTION (P0)

### [S2B-001] PENDING — Marginal CAC curves (diminishing returns model)
Brief: For top 3 channels (Pmax, ASA, Google Search), model what happens to CPI/CAC as spend increases 25%/50%/100%. Use existing data to plot marginal cost curves. Flag spend levels where returns diminish. Create analysis/marginal-cac-curves.md + data/marginal-cac.json.

### [S2B-002] PENDING — Retention curve analysis (D1/D7/D14/D30)
Brief: Pull Amplitude retention data for last 90 days. Calculate D1/D7/D14/D30 retention by country and platform. Compare TR vs NG vs EG. Create analysis/retention-curves.md.

### [S2B-003] PENDING — Organic growth strategy (SEO + content + referral combined)
Brief: Combine SEO content plan + referral scaling plan + social boost plan into unified organic strategy. Prioritize by expected impact. Create analysis/organic-growth-strategy.md.

### [S2B-004] PENDING — ASA keyword expansion research
Brief: Research Apple Search Ads keywords beyond current set. Include competitor brand terms, category terms, long-tail freelancer terms. Estimate search volume where possible. Create analysis/asa-keyword-expansion.md.

### [S2B-005] PENDING — Google Search negative keywords audit
Brief: Review current Google Search campaigns. Identify wasted spend on irrelevant queries (if search term data available from Sheets/BigQuery). Propose negative keyword list. Create analysis/negative-keywords-audit.md.

## DATA INFRASTRUCTURE (P1)

### [S2B-006] PENDING — Amplitude funnel API implementation
Brief: Create a reusable script that uses Amplitude Funnel API (not just Segmentation) to get true funnel conversion rates with strict ordering. Pull: Install → Signup → KYC Start → KYC Submit → Virt Acc → Withdraw. By country. scripts/amplitude_funnel.py + data/funnel-api-20260322.json.

### [S2B-007] PENDING — Weekly data refresh automation (launchd)
Brief: Create a launchd plist that runs the full Monday pipeline (kpi_auto_update → anomaly → health → pacing → quality → actions → report) every Monday at 09:00 TRT. Document in analysis/automation-setup.md. Create the plist at ~/Library/LaunchAgents/com.cenoa.growth-engine.weekly.plist.

### [S2B-008] PENDING — Cortex data.json auto-deploy pipeline
Brief: After kpi_auto_update.py runs, auto-commit data.json to cenoa-cortex repo and push to GitHub (→ Vercel auto-deploys). Create scripts/auto_deploy_cortex.sh that: runs kpi_auto_update, copies data.json to cenoa-cortex, git add/commit/push. Make it the single command for Monday refresh.

### [S2B-009] PENDING — Historical data backfill (last 12 weeks)
Brief: Run weekly_channel_country.py for each of the last 12 weeks to build historical trend data. Save each week to data/weekly-channel-country-YYYYMMDD.json. Create analysis/12-week-trends.md with trend charts data.

### [S2B-010] PENDING — Sheets auto-sync script
Brief: Create scripts/sheets_sync.py that pulls latest data from all 3 Google Sheets (CaC Analysis, Budget Tracking, Trafik Canavarı) and saves to data/ directory. This removes manual dependency. Include in Monday pipeline.

## COMPETITIVE & MARKET (P1)

### [S2B-011] PENDING — First competitor ad scan (Meta Ad Library + Google Transparency)
Brief: Use browser tool to scan Meta Ad Library for Payoneer + Wise active ads. Screenshot or describe top 5 ads per competitor. Log in competitor-monitoring.md under "Week of 2026-03-22" section. Note creative formats, hooks, CTAs, geo targeting.

### [S2B-012] PENDING — Payoneer pricing comparison page content
Brief: Create detailed Cenoa vs Payoneer comparison content. Research current Payoneer fees (from their website). Build comparison data: withdrawal fees, FX markup, monthly fees, transfer speed, account opening time. Save to analysis/cenoa-vs-payoneer-comparison.md. This feeds into LP + ad creative.

### [S2B-013] PENDING — Arabic landing page content spec
Brief: Create content spec for an Arabic (Egyptian dialect) landing page. Include: headline, subheadline, 3 benefit bullets, CTA, trust signals, FAQ. All in Arabic. Reference competitive-positioning.md for messaging framework. Save to analysis/arabic-lp-content-spec.md.

### [S2B-014] PENDING — Turkish LP A/B test copy variants
Brief: Write 3 headline + CTA variants for cenoa.com Turkish LP test. Based on lp-cta-optimization.md recommendations. Include: benefit-first, comparison-first, social-proof-first variants. Save to analysis/tr-lp-ab-variants.md.

## REPORTING & VISIBILITY (P2)

### [S2B-015] PENDING — Cortex: historical trend charts (12-week sparklines)
Brief: Extend Cortex index.html to show 12-week trend lines for key KPIs (installs, signups, new_actives, CAC). Read from data.json history array if populated, otherwise hardcode last 4 weeks. Use Chart.js line charts.

### [S2B-016] PENDING — Cortex: country deep-dive pages (TR/NG/EG/PK)
Brief: Create 4 separate HTML pages (country-tr.html, country-ng.html, etc.) linked from main Cortex dashboard. Each shows: country funnel, channel mix, CAC, KYC status, growth plan summary. Dark theme matching main dashboard.

### [S2B-017] PENDING — Weekly email/Telegram report template polish
Brief: Review weekly_report.py output. Improve formatting, add more context per metric, include "vs target" comparisons, add mini ASCII charts if possible. Make it genuinely useful to read on a phone.

### [S2B-018] PENDING — Sprint 2 report page (like Sprint 1)
Brief: Create sprint-2-report.html in cenoa-cortex. Same dark theme. Show: Sprint 2 task completion, key deliverables, new dashboard widgets, Monday briefing readiness, what's next. Add nav link in index.html.

### [S2B-019] PENDING — Growth Engine README.md
Brief: Create a proper README.md for the cenoa-performance-marketing repo. Explain: what this is, how to run scripts, what data sources are needed, credential setup, Monday pipeline, Cortex dashboard. Make it onboarding-friendly.

### [S2B-020] PENDING — Growth Engine architecture diagram
Brief: Create a visual architecture diagram (HTML/SVG) showing: data sources → scripts → data.json → Cortex dashboard → alerts/reports. Include all automation flows. Save as architecture.html in cenoa-cortex or as section in README.
