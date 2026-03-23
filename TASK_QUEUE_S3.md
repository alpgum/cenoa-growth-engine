# Cenoa Growth Engine — Sprint 3 Task Queue

> Sprint started: 2026-03-23 00:15 TRT
> Previous: Sprint 2A (30 tasks) + Sprint 2B (20 tasks) — ALL DONE
> Focus: Dashboard polish, data accuracy, marketing execution, reporting automation
> Goal: Monday morning meeting ready — real numbers, clear decisions, country clarity

---

## A) DASHBOARD FINE-TUNE (10 tasks)

### [S3-001] PENDING — Verify all 14 Cortex widgets render correctly with real data
Brief: Open cenoa-cortex/index.html in browser. Systematically test every section: exec summary KPIs, budget pacing gauge, trend history charts, campaign table, channel performance cards, CAC vs target bars, country breakdown, KYC mini funnels, platform split donut, weekly tests, weekly learnings, weekly agenda, attribution quality meter, and doc grid. Screenshot any blank/broken widgets. Log broken ones in analysis/cortex-widget-audit.md with exact section IDs and failure modes.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-001] Cortex widget render audit"

### [S3-002] PENDING — Add "Last Updated" timestamp to Cortex header
Brief: Add a visible "Data as of: Mar 22, 2026 23:45 TRT" timestamp in the Cortex header bar (right side, next to existing header-right element). Read timestamp from data.json field `lastUpdated`. If field missing, show "⚠️ No timestamp". Auto-format to human-readable "MMM DD, YYYY HH:MM TRT".
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S3-002] Last updated timestamp in header"

### [S3-003] PENDING — Add date range selector (This Week / MTD / Last 30d / Custom)
Brief: Add a pill-style date range selector below the exec summary. Options: "This Week", "MTD", "Last 30d", "Custom". On selection, filter data.json arrays by date range and re-render KPIs, charts, tables. Store selection in localStorage. Default to "This Week". Use vanilla JS, no dependencies.
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S3-003] Date range selector"

### [S3-004] PENDING — Improve chart labels, tooltips, and number formatting
Brief: Audit all Chart.js charts (trend history, CAC bars, donut). Ensure: (1) Y-axis has $ or # prefix, (2) tooltips show full label + formatted number + WoW delta, (3) large numbers use K/M shorthand (e.g., $1.2K), (4) CAC values show 2 decimal places, (5) percentages show 1 decimal. Fix any clipped labels on mobile.
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S3-004] Chart labels and tooltips polish"

### [S3-005] PENDING — Mobile responsiveness pass (test 375px / 768px breakpoints)
Brief: Test Cortex at iPhone SE (375px) and iPad (768px) widths. Fix: (1) exec KPI cards stack to 1-col on mobile, (2) campaign table horizontal scrolls, (3) chart containers don't overflow, (4) doc grid goes to 1-col, (5) header brand text truncates gracefully, (6) action chips wrap properly. Add media queries where missing.
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S3-005] Mobile responsiveness fixes"

### [S3-006] PENDING — Add print/export CSS and PDF button
Brief: Add a "📄 Export PDF" button in the header. On click, trigger window.print(). Add @media print CSS: hide nav, search, filters; force white background; ensure charts render (use Chart.js beforePrint plugin to resize). Page-break-before on major sections. Test that printed PDF is readable.
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S3-006] Print/export PDF capability"

### [S3-007] PENDING — Replace all hardcoded numbers with data.json references
Brief: Grep index.html for any remaining hardcoded numbers (dollar amounts, percentages, counts) that should come from data.json. Specifically check: exec summary status line, KPI values, budget pacing numbers, campaign table rows. Map each to a data.json field. Update renderDashboard() to populate them dynamically. Document mappings in a comment block at top of JS.
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S3-007] Remove hardcoded data, use data.json"

### [S3-008] PENDING — Add loading states and error handling for data.json fetch
Brief: Currently if data.json fails to load, the dashboard shows nothing with no explanation. Add: (1) skeleton loading animation while fetching, (2) error state with "⚠️ Failed to load data. Last cached version: [date]" message, (3) retry button, (4) fallback to localStorage cached data.json if fetch fails.
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S3-008] Loading states and error handling"

### [S3-009] PENDING — Fix campaign table sorting and add column sort toggles
Brief: Campaign table should be sortable by clicking column headers. Add click handlers to: Spend, Installs, CPI, TRUE CAC, WoW Δ columns. Toggle asc/desc. Add sort indicator arrow (▲/▼). Default sort: TRUE CAC ascending (cheapest first). Persist sort preference in localStorage.
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S3-009] Campaign table column sorting"

### [S3-010] PENDING — Add country flag + color coding to country breakdown section
Brief: Country breakdown section should have flag emojis (🇹🇷 TR, 🇳🇬 NG, 🇪🇬 EG, 🇵🇰 PK) and consistent color coding (TR=blue, NG=green, EG=amber, PK=purple) across all widgets that show country data: breakdown cards, KYC funnels, CAC bars. Update CSS variables and JS rendering.
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S3-010] Country flags and color coding"

---

## B) DATA ACCURACY (5 tasks)

### [S3-011] PENDING — Validate Cortex KPI numbers against Amplitude API response
Brief: Run kpi_auto_update.py, capture raw Amplitude API responses. Compare every number in data.json against raw API output. Check: total installs, signups, KYC submits, virtual accounts, new actives — globally and per country. Document any discrepancies in analysis/data-validation-s3.md. Fix any mismatches in the script.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-011] KPI validation vs Amplitude API"

### [S3-012] PENDING — Cross-check spend totals: data.json vs Sheets vs campaign reports
Brief: Pull spend from 3 sources: (1) data.json current values, (2) Sheets CAC Analysis raw data, (3) campaign-performance-weekly-mar15-21.md reported spend. Compare per-channel spend. Flag any >5% discrepancy. Document in analysis/spend-crosscheck-s3.md. Update data pipeline if Sheets is the source of truth.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-012] Spend cross-check 3 sources"

### [S3-013] PENDING — Fix double-counting risk in channel attribution
Brief: The "Other | TR" Amplitude bucket (~157 installs) contains Meta, Google App, and uncategorized traffic. Current pipeline splits this using prior-week ratios — verify this doesn't double-count with separately tagged Meta/Google campaigns. Cross-reference Amplitude utm_source with channel mapping in scripts/. Fix any overlap. Document methodology in analysis/attribution-methodology-s3.md.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-013] Fix channel attribution double-counting"

### [S3-014] PENDING — Standardize all date ranges to ISO weeks (Mon-Sun)
Brief: Audit all scripts and data files. Ensure consistent date ranges: (1) weekly = Monday 00:00 UTC to Sunday 23:59 UTC, (2) MTD = 1st of month 00:00 to current day 23:59, (3) daily = 00:00-23:59 UTC. Fix any scripts using TRT midnight vs UTC midnight inconsistency. Update kpi_auto_update.py, weekly_channel_country.py, and any other date-parameterized scripts.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-014] Standardize date ranges to ISO weeks"

### [S3-015] PENDING — End-to-end pipeline test: raw API → data.json → dashboard renders
Brief: Run the full pipeline from scratch: (1) kpi_auto_update.py, (2) copy data.json to cenoa-cortex, (3) open index.html, (4) verify every widget shows correct data matching the API pull. Automate this as scripts/e2e_test.sh that runs pipeline + outputs a checklist of pass/fail per widget. Run it and fix any failures.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-015] E2E pipeline test script"

---

## C) MARKETING EXECUTION (10 tasks)

### [S3-016] PENDING — Campaign pause execution checklist (Demand Gen + Appnext + dead campaigns)
Brief: Create a step-by-step checklist to pause: Google Demand Gen (TR), Appnext (TR), Twitter/X Ads (TR), Onboarding Meta Test (TR), Meta Combined (EG) if still above $200 CAC. Per campaign: platform login steps, what to click, screenshot confirmation, budget to reallocate, where to reallocate. Save to analysis/campaign-pause-checklist.md.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-016] Campaign pause execution checklist"

### [S3-017] PENDING — Pmax scaling implementation plan ($500 → $1,500/week)
Brief: Google Pmax (TR) has best blended performance. Create a scaling plan: current daily budget, target daily budget (3x), ramp schedule (20% increments every 3 days), asset group review, audience signals to add, conversion action verification (optimize for virtual_account_opened not install). Include rollback criteria if CPI rises >30%. Save to analysis/pmax-scaling-plan.md.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-017] Pmax scaling implementation plan"

### [S3-018] PENDING — ASA expansion implementation (EG scale + NG pilot)
Brief: Apple Search Ads (TR) at $26 CAC is best performer. Apple Ads (EG) at $16 CAC has tiny $33/week spend. Plan: (1) EG budget increase from $5/day to $25/day, (2) add asa-keyword-expansion.md keywords, (3) NG pilot: $10/day on top freelancer/payment keywords, (4) competitor brand terms test. Include bid strategy and match type recommendations. Save to analysis/asa-expansion-plan.md.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-018] ASA expansion implementation plan"

### [S3-019] PENDING — Meta retargeting optimization spec
Brief: Meta (EG) spending $1,449/week with $483 CAC is catastrophic. Create optimization spec: (1) pause all prospecting campaigns above $150 CAC, (2) shift budget to retargeting: website visitors, app installers who didn't sign up, KYC dropoffs, (3) lookalike audiences from top 10% LTV users, (4) creative refresh with Arabic content from arabic-lp-content-spec.md. Include audience size estimates and budget split. Save to analysis/meta-rtgt-optimization-spec.md.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-019] Meta retargeting optimization spec"

### [S3-020] PENDING — Nigeria Google Search pilot plan
Brief: NG Google Search at $229/week and $76 CAC (was $13 prior week — volatility due to small volume). Create a structured pilot: (1) keyword themes from nigeria-growth-plan.md, (2) daily budget $15, (3) exact match + phrase match only, (4) negative keyword list from negative-keywords-audit.md, (5) landing page: English, NG-specific benefits, (6) 2-week test with weekly checkpoints. Success = CAC < $50. Save to analysis/ng-search-pilot-plan.md.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-020] Nigeria Google Search pilot plan"

### [S3-021] PENDING — Draft email to Eng: KYC bug in NG/EG (0 KYC shown events)
Brief: Write a concise, actionable email to Engineering team about the KYC bug. Reference kyc-escalation-brief.md data. Include: (1) Bug description — NG and EG show 0 "kyc_shown" events despite having kyc_start events, (2) Impact — can't measure KYC conversion, estimated $X waste, (3) Hypothesis — event not firing or wrong event name, (4) Ask — investigate by Wed Mar 25, provide event schema. Save to analysis/email-eng-kyc-bug.md.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-021] Email draft: Eng KYC bug"

### [S3-022] PENDING — Draft email to Eng: Attribution fix (web-to-app gap)
Brief: Write email to Engineering about web-to-app attribution gap. Reference attribution-fix-spec.md. Include: (1) Problem — 50%+ signups show "(none)" attribution, (2) Root cause — LP → App Store breaks UTM chain, (3) Solution — AppsFlyer OneLink + deferred deep links, (4) Scope estimate request, (5) Impact — $3K+/month wasted on unmeasurable campaigns. Save to analysis/email-eng-attribution-fix.md.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-022] Email draft: Eng attribution fix"

### [S3-023] PENDING — Creative brief finalization (TR + EG + NG)
Brief: Consolidate creative-refresh-brief-mar22.md + creative-scoring.md + competitive positioning into a final creative brief. Per market: (1) TR — Papara/Wise comparison angle, freelancer income story, (2) EG — Arabic, bank access pain point, receive international payments, (3) NG — USD earnings, quick withdrawal. Include format specs (1080x1080, 9:16 video, carousel), CTA text, 3 headline variants each. Save to analysis/creative-brief-final.md.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-023] Final creative brief TR/EG/NG"

### [S3-024] PENDING — Turkish LP A/B test implementation spec
Brief: Turn tr-lp-ab-variants.md copy variants into an implementation spec. Include: (1) Current LP URL and screenshot, (2) Variant A: benefit-first headline, (3) Variant B: comparison-first (vs Papara), (4) Variant C: social-proof-first, (5) Traffic split (25/25/25/25 with control), (6) Tool recommendation (Google Optimize / VWO / manual), (7) Success metric: LP→Install conversion rate, (8) Sample size calculation, (9) Expected test duration: 2 weeks. Save to analysis/lp-ab-test-implementation.md.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-024] LP A/B test implementation spec"

### [S3-025] PENDING — Weekly review meeting template
Brief: Create a reusable weekly marketing review template. Sections: (1) KPI Scorecard (spend, installs, signups, CAC — actual vs target), (2) Channel Health (traffic light per campaign), (3) Test Results (what ran, what we learned), (4) Budget Pacing (over/under by channel), (5) This Week's Actions (P0/P1/P2), (6) Blockers & Asks, (7) Next Week Preview. Format: markdown, Notion-friendly, can be filled in 15 min. Save to analysis/weekly-review-template.md.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-025] Weekly review meeting template"

---

## D) REPORTING (5 tasks)

### [S3-026] PENDING — Monday briefing auto-send via Telegram
Brief: Create scripts/monday_briefing_telegram.py that: (1) runs kpi_auto_update.py to refresh data, (2) generates a Telegram-formatted briefing (bullet points, no tables, emoji headers), (3) includes: KPI snapshot, top 3 winners, top 3 to-kill, budget pacing %, this week's #1 priority. Keep under 4096 chars (Telegram limit). Test output to stdout first. Document how to wire to OpenClaw cron for Monday 09:00 TRT.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-026] Monday briefing Telegram auto-send"

### [S3-027] PENDING — Weekly PDF export script
Brief: Create scripts/weekly_pdf_export.py (or .sh using wkhtmltopdf/puppeteer) that: (1) opens cenoa-cortex/index.html, (2) triggers print CSS, (3) saves as PDF to reports/weekly-YYYY-MM-DD.pdf. Include all dashboard sections. Test that charts render in PDF (not blank). Add to Monday pipeline after data refresh.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-027] Weekly PDF export script"

### [S3-028] PENDING — March month-end report preparation
Brief: Create analysis/march-month-end-report.md template. Pre-fill with: (1) March budget $50K plan vs actual spend, (2) March KPI targets vs actuals (installs, signups, new_actives, CAC), (3) Channel performance summary with recommendations carried forward, (4) Key learnings (KYC bug, attribution gap, Appnext fraud, Demand Gen waste), (5) April budget recommendation, (6) April priority channels. Mark data fields as [TBD - fill Mar 31] where final numbers needed.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-028] March month-end report template"

### [S3-029] PENDING — Sprint 3 report page (cenoa-cortex)
Brief: Create sprint-3-report.html in cenoa-cortex following Sprint 1/2 report format. Include: Sprint 3 objectives, task completion tracker (30 tasks), key deliverables (dashboard polish, data accuracy, execution plans), dashboard before/after screenshots, pipeline reliability metrics, what's next for Sprint 4. Add navigation link in index.html. Light theme matching main dashboard.
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S3-029] Sprint 3 report page"

### [S3-030] PENDING — Stakeholder update email template
Brief: Create a reusable stakeholder update email template for weekly/biweekly sends. Sections: (1) TL;DR (3 bullets max), (2) Spend & ROI snapshot (1 table), (3) What's Working (top 2 campaigns), (4) What We're Fixing (top 2 issues), (5) Decisions Needed (if any), (6) Next Week Preview. Tone: executive, data-driven, no jargon. Max 300 words. Include placeholder variables for dynamic fill. Save to analysis/stakeholder-email-template.md.
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S3-030] Stakeholder update email template"

---

## Summary

| Category | Tasks | IDs |
|----------|------:|-----|
| A) Dashboard Fine-Tune | 10 | S3-001 → S3-010 |
| B) Data Accuracy | 5 | S3-011 → S3-015 |
| C) Marketing Execution | 10 | S3-016 → S3-025 |
| D) Reporting | 5 | S3-026 → S3-030 |
| **Total** | **30** | |

All tasks: Status **PENDING**

### Priority Order (suggested)
1. **S3-001** (widget audit) → know what's broken before fixing
2. **S3-011–S3-015** (data accuracy) → numbers must be right before Monday
3. **S3-007** (remove hardcoded data) → dashboard shows real data
4. **S3-002** (timestamp) → quick win, shows data freshness
5. **S3-016** (pause checklist) → stop bleeding $2K+/week on dead campaigns
6. **S3-026** (Telegram briefing) → automate Monday morning flow
7. **S3-017–S3-020** (scaling/optimization plans) → growth execution
8. **S3-021–S3-022** (Eng emails) → unblock KYC and attribution fixes
9. **S3-003–S3-010** (remaining dashboard polish)
10. **S3-023–S3-030** (remaining execution + reporting)
