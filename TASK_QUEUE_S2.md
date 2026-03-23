# Cenoa Growth Engine — Sprint 2 Task Queue

> Sprint started: 2026-03-22 18:44 TRT
> Slots: 3 auto
> Context: Monday briefing prep + dashboard upgrade + weekly ops

---

## MONDAY BRIEFING PREP (P0 — must ship before Mon 10:00)

### [S2-001] PENDING — Last 7 days: channel × country install/signup/KYC/virt_acc/new_active
Brief: Pull Amplitude data (Mar 15-21 vs Mar 8-14). Break down by channel (Google Pmax, Google Search, Meta, ASA, Appnext, TikTok, Organic, Referral) AND by country (TR, NG, EG, PK). Include: installs, signups, KYC submit, virtual_account_opened, new_active (first withdrawal). WoW delta. Save to `data/weekly-channel-country-20260322.json` + human-readable `analysis/weekly-channel-country-mar15-21.md`.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S2-001] Weekly channel×country breakdown"

### [S2-002] PENDING — Last 7 days: spend by channel (from Sheets/BigQuery)
Brief: Pull latest spend data per channel for Mar 15-21. Cross-ref with Sheets budget tracking. Calculate CPI, cost/signup, cost/virt_acc, cost/new_active per channel. Save to `data/weekly-spend-20260322.json` + `analysis/weekly-spend-mar15-21.md`.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S2-002] Weekly spend by channel"

### [S2-003] PENDING — Last 7 days: platform breakdown (iOS vs Android vs Web)
Brief: Pull Amplitude data Mar 15-21 by platform for all funnel events. Include iOS/Android split for installs, signups, KYC, withdrawals. Note web→app attribution caveat. Save to `analysis/weekly-platform-mar15-21.md`.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S2-003] Weekly platform breakdown"

### [S2-004] PENDING — March MTD: budget plan vs actuals (channel-level spend + targets)
Brief: Compare March 2026 budget plan (from sheets-budget-tracking.json, $50K target) vs March to-date realized spend. Per-channel: planned vs actual spend, planned vs actual installs/virt_acc/new_active. Calculate pacing %, over/under per channel. Save to `analysis/march-mtd-budget-vs-actual.md` + `data/march-mtd-pacing.json`.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S2-004] March MTD budget vs actuals"

### [S2-005] PENDING — March MTD: CAC tracking vs targets
Brief: Calculate March MTD blended CAC (cost/new_active = TRUE CAC) and cost/virt_acc per channel and country. Compare with Sprint 1 targets and budget-allocation-model recommendations. Flag channels above target CAC. Save to `analysis/march-mtd-cac-tracking.md`.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S2-005] March MTD CAC tracking"

### [S2-006] PENDING — Last week's tests & learnings summary
Brief: Review Sprint 1 outputs + any campaign changes made. Document: what was tested (new campaigns, bid changes, creative tests, audience changes), what we learned (from data), what surprised us. Include KYC findings, attribution discovery, budget overspending. Save to `analysis/weekly-learnings-mar15-21.md`.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S2-006] Weekly learnings Mar 15-21"

### [S2-007] PENDING — This week's test plan (Mar 22-28)
Brief: Based on Sprint 1 recommendations + learnings, create this week's test plan. Include: campaigns to pause (Demand Gen, Appnext), campaigns to scale (Pmax, ASA), creative tests to run, LP tests, budget cap changes. Each test: hypothesis, metric, success criteria, timeline. Save to `analysis/weekly-test-plan-mar22-28.md`.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S2-007] Test plan Mar 22-28"

### [S2-008] PENDING — This week's agenda & priorities
Brief: Create the week's agenda based on all Sprint 1 insights + P0 actions. Structure: P0 (do today), P1 (do this week), P2 (start this week). Include: KYC escalation, budget cap enforcement, Demand Gen pause, attribution fix kickoff, creative refresh. Save to `analysis/weekly-agenda-mar22-28.md`.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S2-008] Weekly agenda Mar 22-28"

### [S2-009] PENDING — Monday briefing message (Telegram format)
Brief: Compile S2-001 through S2-008 into a single Monday briefing. Format: bullet-style, Telegram-friendly (no tables). Structure: KPI snapshot → channel performance → budget pacing → last week learnings → this week plan → agenda. Save to `data/monday-briefing-20260322.md` AND print to stdout.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S2-009] Monday briefing Mar 22"

---

## CORTEX DASHBOARD UPGRADE (P1 — ship by Mon EOD)

### [S2-010] PENDING — Cortex: Weekly channel performance widget
Brief: Add a new section to cenoa-cortex/index.html showing last 7 days performance per channel. Read from data.json (extend schema). Show: channel name, spend, installs, CPI, new_actives, true CAC, WoW trend arrow. Dark theme, compact cards.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S2-010] Channel performance widget"

### [S2-011] PENDING — Cortex: Budget pacing gauge
Brief: Add a visual budget pacing gauge to Cortex. Show: March target ($50K), MTD spend, pacing %, days remaining. Color: green (<100%), orange (100-120%), red (>120%). Read from data.json.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S2-011] Budget pacing gauge"

### [S2-012] PENDING — Cortex: This Week's Tests section
Brief: Add a "🧪 This Week's Tests" section to Cortex. Show active experiments: name, hypothesis, status (running/planned/completed), metric being tracked. Read from data.json.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S2-012] Tests tracker widget"

### [S2-013] PENDING — Cortex: Weekly Learnings carousel
Brief: Add "💡 What We Learned" section. Show 5-7 key learnings from the week as scrollable cards. Each: emoji + 1-line finding + impact. Read from data.json.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S2-013] Weekly learnings carousel"

### [S2-014] PENDING — Cortex: True CAC vs Target CAC comparison
Brief: Add a CAC tracking widget. Show per-channel: actual true CAC (cost/new_active) vs target CAC from budget-allocation-model. Green if below target, red if above. Bar chart style.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S2-014] CAC vs target widget"

### [S2-015] PENDING — Cortex: Platform split donut chart (iOS/Android)
Brief: Add a small donut chart showing iOS vs Android split for installs, signups, withdrawals. Use Chart.js. Read from data.json.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S2-015] Platform split donut"

### [S2-016] PENDING — Cortex: Campaign health status indicators
Brief: Add colored status dots next to each campaign in the campaign table. Green=HEALTHY, Orange=BLEEDING, Red=DEAD, Purple=FRAUD. Read from data.json (campaign-health data).
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S2-016] Campaign health indicators"

### [S2-017] PENDING — Cortex: Attribution quality meter
Brief: Add a small "Attribution Health" indicator. Show: % of signups with known attribution (vs (none)), trend. Orange/red when (none) > 50%. Explain web→app gap on hover/click.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S2-017] Attribution quality meter"

### [S2-018] PENDING — Cortex: KYC funnel per country (mini funnels)
Brief: Add mini funnel visualizations per country (TR/NG/EG/PK). Show: KYC Started → Shown → Submit with conversion rates. Highlight NG/EG broken state (0 shown). Small, compact.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S2-018] Country KYC mini funnels"

### [S2-019] PENDING — Cortex: Weekly agenda/priorities panel
Brief: Add "📋 This Week" section showing P0/P1/P2 priorities. Read from data.json. Checkmark style, clean.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S2-019] Weekly agenda panel"

### [S2-020] PENDING — data.json schema v2 (extend for all new widgets)
Brief: Extend kpi_auto_update.py to generate all new data fields needed by S2-010 through S2-019. New sections in data.json: channelPerformance[], budgetPacing{}, weeklyTests[], weeklyLearnings[], cacTracking[], platformSplit{}, campaignHealth[], attributionQuality{}, kycByCountry[], weeklyAgenda[]. Run and generate updated data.json.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S2-020] data.json schema v2"

---

## OPERATIONAL EXCELLENCE (P1-P2)

### [S2-021] PENDING — Run weekly automation pipeline end-to-end
Brief: Execute the full Monday pipeline manually: kpi_auto_update → anomaly_detection → campaign_health_check → budget_pacing → data_quality_monitor → weekly_actions → weekly_report. Verify each step works. Fix any errors. Save all outputs. Document any issues.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S2-021] Full pipeline test run"

### [S2-022] PENDING — Real withdrawal volume pull (LTV validation)
Brief: Pull actual withdrawal volumes and amounts from Amplitude (Withdraw Completed event with amount property if available). By country, by month (last 3 months). Validate/update LTV model. This was P0 from audit.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S2-022] Real withdrawal volume for LTV"

### [S2-023] PENDING — KYC escalation brief for Product/Eng
Brief: Create a 1-page brief for Product/Eng team about the KYC issues. Format: problem statement, data evidence, impact ($ and users), proposed fix, priority. Make it actionable — they should be able to start debugging Monday. Save to `analysis/kyc-escalation-brief.md`.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S2-023] KYC escalation brief"

### [S2-024] PENDING — Attribution fix implementation spec
Brief: Turn the web-to-app-handoff.md analysis into a technical implementation spec for Eng. Include: OneLink setup steps, deferred deep link code changes, UTM persistence requirements, Amplitude property propagation. Make it copy-paste actionable.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S2-024] Attribution fix implementation spec"

### [S2-025] PENDING — Demand Gen pause recommendation memo
Brief: 1-page memo recommending immediate Demand Gen pause. Include: spend to date, 0 installs, estimated waste, what to do with freed budget, diagnostic steps if we want to try relaunching later.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S2-025] Demand Gen pause memo"

### [S2-026] PENDING — Appnext fraud investigation summary
Brief: Compile fraud evidence for Appnext: high installs, near-zero downstream, suspicious patterns. Include recommendation (pause + request refund/credit). 1-page.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S2-026] Appnext fraud summary"

### [S2-027] PENDING — Weekly creative refresh brief
Brief: Based on creative-scoring.md, write a brief for the creative team: which creatives to refresh, which angles to test, per-market messaging guidance. Include TR (vs Papara/Wise), NG (receive payments), EG (Arabic, bank access).
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[S2-027] Creative refresh brief"

### [S2-028] PENDING — Cortex deploy (push all updates to Vercel)
Brief: After all Cortex updates are committed, push to GitHub → Vercel auto-deploys. Verify live site works. Test all new widgets. Screenshot key sections.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-cortex && git push

### [S2-029] PENDING — Sprint 1 report update (add new data)
Brief: Update sprint-1-report.html with any corrections from the audit P0 fixes (metric definitions, attribution caveats). Add a "Post-Audit Fixes" section.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[S2-029] Sprint report post-audit update"

### [S2-030] PENDING — Memory + daily log update
Brief: Update memory/2026-03-22.md with Sprint 2 progress. Update MEMORY.md if any new permanent rules/facts discovered. Clean up workspace notes.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: echo "memory update - no git commit needed"
