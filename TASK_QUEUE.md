# Cenoa Performance Marketing — Sprint Mode Task Queue

> Sprint started: 2026-03-21 01:06 TRT
> Slots: 3 auto
> Rule: dependency'li task'lar önce, workaround yoksa skip & next

---

## PENDING

### [001] ⏭️ SKIPPED — Meta Ads MCP test (MCP not available to subagents, will use browser/API workaround)
Brief: Run Meta Ads MCP `list_ad_accounts`, save account IDs to `projects/cenoa-performance-marketing/data/meta-accounts.json`. Test `read_ads` with one simple query (last 7 days spend). Write results.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[001] Meta Ads MCP test — accounts + spend" 2>/dev/null; true

### [002] ✅ DONE — BigQuery full dataset exploration
Brief: Using service account at `~/.openclaw/credentials/cenoa-marketingdatawarehouse-82b8600e66d6.json`, query BigQuery `cenoa-marketingdatawarehouse.marketing_appsflyer.*`. Get schema of both tables, row counts, date ranges, all unique campaigns, countries, platforms. Save to `projects/cenoa-performance-marketing/data/bigquery-inventory.md`.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[002] BigQuery dataset exploration" 2>/dev/null; true

### [003] ✅ DONE — Google Sheets parse — CaC Analysis (all tabs)
Brief: Using Google Sheets API or export CSV, read sheet `1d743wipSvWEfwwXCmy2J73yCAMNYa-hCb-nTvNf3yHc`. Parse all tabs (Sum, 2026 Channel ALL, 2025 Channels TR, channel mapping, tr mart proj). Save structured data to `projects/cenoa-performance-marketing/data/sheets-cac-analysis.json` and human-readable summary to `projects/cenoa-performance-marketing/data/sheets-cac-analysis.md`.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[003] Sheets CaC Analysis parsed" 2>/dev/null; true

### [004] ✅ DONE — Google Sheets parse — Budget Tracking (key tabs)
Brief: Read sheet `1VTZQbRD0gZAABLvgjwlymAx0sQ7vcvMUySsWzLhnFKk`. Focus on tabs: Budget Distribution 2026, Realized Cost Jan/Feb, march 26 budget, Jan Cac, Performance Budget, Subscriptions. Save to `projects/cenoa-performance-marketing/data/sheets-budget-tracking.json` + `.md` summary.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[004] Sheets Budget Tracking parsed" 2>/dev/null; true

### [005] ✅ DONE — Google Sheets parse — dikkat trafik canavarı (Meta + Google tabs)
Brief: Read sheet `1H27QF84Nm02nAhXebP6zWgEG7pwu_UTwcliO_c4mKmM`. Focus on: Furkan Meta Ads Plan, Google Detailed, Weekly google, Egypt LTV Test, LP tests. Save to `projects/cenoa-performance-marketing/data/sheets-trafik-canavari.json` + `.md`.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[005] Sheets trafik canavari parsed" 2>/dev/null; true

### [006] ✅ DONE — Amplitude weekly KPI pull script (reusable) ⚠️ numbers off, needs date/metric fix
Brief: Create `projects/cenoa-performance-marketing/scripts/amplitude_weekly_pull.py`. Source creds from `~/.openclaw/credentials/amplitude.env`. Pull last 2 weeks: installs, signups, KYC submit, withdrawals, deposits, DAU. Output JSON to `data/amplitude-weekly-{date}.json`. Include WoW delta calculation. Make it reusable (date range as arg).
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[006] Amplitude weekly pull script" 2>/dev/null; true

### [007] ✅ DONE — Amplitude country breakdown script ⚠️ same date/totals issue as [006]
Brief: Create `projects/cenoa-performance-marketing/scripts/amplitude_country_breakdown.py`. For each core funnel event, pull by country (TR, NG, EG, PK, Other). Output to `data/amplitude-country-{date}.json`. Include percentage splits.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[007] Amplitude country breakdown script" 2>/dev/null; true

### [008] ✅ DONE — Amplitude platform breakdown script ⚠️ iOS-only installs, (none) signup issue
Brief: Create `projects/cenoa-performance-marketing/scripts/amplitude_platform_breakdown.py`. Core funnel events by platform (iOS, Android, Web/none). Output to `data/amplitude-platform-{date}.json`.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[008] Amplitude platform breakdown script" 2>/dev/null; true

### [009] ✅ DONE — Amplitude attribution breakdown script
Brief: Create `projects/cenoa-performance-marketing/scripts/amplitude_attribution.py`. Funnel events by `gp:[AppsFlyer] media source` and `gp:[AppsFlyer] campaign`. Output to `data/amplitude-attribution-{date}.json`.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[009] Amplitude attribution breakdown script" 2>/dev/null; true

### [010] ✅ DONE — Credentials & access inventory update
Brief: Update `~/.openclaw/workspace/TOOLS.md` and `~/.openclaw/workspace/CAPABILITIES.md` with all confirmed access: Amplitude (API+Secret), GA4 (service account), Meta Ads (MCP), BigQuery (service account), Google Sheets (3 IDs), Looker (embed). Note what works and what doesn't. Update `projects/cenoa-performance-marketing/data/access-inventory.md`.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[010] Access inventory updated" 2>/dev/null; true

### [011] ✅ DONE — Fix & run amplitude scripts — all numbers verified ✅
Brief: Run the script from [006] for Mar 14-20 and Mar 7-13. Save outputs. Verify numbers match what we pulled manually earlier (installs 1422, signups 1189, etc).
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[011] Weekly KPI data pulled and verified" 2>/dev/null; true

### [012] ✅ DONE — Country breakdown + analysis (TR dominates KYC, NG zero KYC submit, EG drops)
Brief: Run [007] script. Verify TR/NG/EG/PK splits. Save outputs.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[012] Country breakdown data pulled" 2>/dev/null; true

### [013] ✅ DONE — Platform funnel (Android 88% install, iOS wins monetization, web→app leak)
Brief: Run [008] script. iOS vs Android vs Web. Save outputs.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[013] Platform breakdown data pulled" 2>/dev/null; true

### [014] ✅ DONE — Attribution funnel (appnext fraud, TikTok zero conversion, ASA best quality)
Brief: Run [009] script. Organic vs paid vs referral. Save outputs.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[014] Attribution data pulled" 2>/dev/null; true

### [015] ✅ DONE — Global funnel (KYC 94% dropout, NG+EG KYC BLOCKED = 0 submit)
Brief: Using data from [011-014], create `projects/cenoa-performance-marketing/analysis/global-funnel.md`. Full funnel: Install(1422) → Signup(1189) → KYC Submit(177) → Deposit(1543) → Withdrawal(2207). Calculate conversion rates between each step. Identify bottlenecks. Include WoW comparison.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[015] Global funnel analysis" 2>/dev/null; true

### [016] ✅ DONE — Turkey funnel (KYC 6.6%, Pmax best channel, cut TikTok/Appnext)
Brief: Using country data from [012], create `analysis/turkey-funnel.md`. TR-specific funnel with conversion rates, comparison to global. Include BigQuery campaign data if available from [002].
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[016] Turkey funnel analysis" 2>/dev/null; true

### [017] ✅ DONE — Nigeria funnel (inverted funnel, 0 Bridge KYC submit, ultra-cheap CAC)
Brief: Same as [016] but for Nigeria. `analysis/nigeria-funnel.md`.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[017] Nigeria funnel analysis" 2>/dev/null; true

### [018] ✅ DONE — Egypt funnel + activation gap analysis
Brief: EG funnel + deep-dive into why installs don't convert to withdrawals. `analysis/egypt-funnel-activation-gap.md`. Compare EG KYC rate vs TR/NG. Hypothesize causes (regulatory? UX? Arabic content?).
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[018] Egypt funnel + activation gap" 2>/dev/null; true

### [019] ✅ DONE — Pakistan funnel analysis
Brief: PK funnel. Very low volume (23 installs). `analysis/pakistan-funnel.md`. Assess if pre-launch or underinvestment.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[019] Pakistan funnel analysis" 2>/dev/null; true

### [020] ✅ DONE — KYC dropout deep-dive (NG/EG Bridgexyz shown=0; TR shown→submit 5.6%; iOS 2.4% vs Android 9.2%)
Brief: `analysis/kyc-dropout-deepdive.md`. Map every KYC event: KYC Started(3071) → Bridgexyz KYC Component Shown(2235) → Submit clicked(177). 92% dropout. Break down by country, platform. Find where exactly users drop.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[020] KYC dropout deep-dive" 2>/dev/null; true

### [021] Platform funnel comparison (iOS vs Android vs Web)
Brief: `analysis/platform-funnel.md`. Full funnel by platform. Which platform converts best? Where does each platform drop off?
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[021] Platform funnel comparison" 2>/dev/null; true

### [022] Attribution funnel (Organic vs Google vs Meta vs Referral)
Brief: `analysis/attribution-funnel.md`. Which channel brings highest quality users? Organic vs paid funnel completion rates.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[022] Attribution funnel analysis" 2>/dev/null; true

### [023] ✅ DONE — Blended CAC calculation (monthly, last 6 months)
Brief: Using Sheets data [003-004] + Amplitude [011], calculate blended CAC monthly. `analysis/blended-cac.md`. Include trend chart data.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[023] Blended CAC calculation" 2>/dev/null; true

### [024] ✅ DONE — Channel CAC (Google vs Meta vs Organic)
Brief: `analysis/channel-cac.md`. Using campaign spend from Sheets + install/signup counts from Amplitude/BigQuery. Per-channel cost per install, per signup, per KYC, per active user.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[024] Channel CAC analysis" 2>/dev/null; true

### [025] ✅ DONE — Country CAC (TR vs NG vs EG)
Brief: `analysis/country-cac.md`. Spend allocation by country (from Sheets/BigQuery) vs signups by country (Amplitude). Which country is most efficient?
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[025] Country CAC analysis" 2>/dev/null; true

### [026] ✅ DONE — Historical CAC cross-check (definitions mismatch flagged; canonical method proposed)
Brief: Compare CaC Analysis sheet historical data with Amplitude-derived numbers. `analysis/cac-crosscheck.md`. Flag discrepancies. Determine which source is more reliable.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[026] Historical CAC cross-check" 2>/dev/null; true

### [027] ✅ DONE — LTV estimation model (scenario-based, assumptions explicit)
Brief: `analysis/ltv-model.md`. Estimate: avg monthly withdrawal volume × estimated FX margin × avg user lifetime (from retention data). If retention data not available, use industry benchmarks. Calculate per country.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[027] LTV estimation model" 2>/dev/null; true

### [028] ✅ DONE — LTV/CAC ratio by country (TR unprofitable at current CAC; NG best if KYC unlocks)
Brief: `analysis/ltv-cac-ratio.md`. Combine [025] + [027]. Which country has best unit economics? Include payback period estimate.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[028] LTV/CAC ratio by country" 2>/dev/null; true

### [029] ✅ DONE — Budget efficiency ranking
Brief: `analysis/budget-efficiency.md`. Rank all campaigns by efficiency: CPI, CPA (signup), CPA (KYC), CPA (active user). Flag worst performers. Recommend reallocations.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[029] Budget efficiency ranking" 2>/dev/null; true

### [030] ✅ DONE — Unit economics 1-page executive brief
Brief: `analysis/unit-economics-brief.md`. Single page: blended CAC, best/worst channel, best/worst country, LTV/CAC, payback, top 3 actions. Written for exec consumption.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[030] Unit economics executive brief" 2>/dev/null; true

### [031] ✅ DONE — KPI auto-update script (Amplitude → data.json → Cortex)
Brief: `scripts/kpi_auto_update.py` created; generates `projects/cenoa-cortex/data.json` with KPI values + WoW deltas/direction.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[031] KPI auto-update script" 2>/dev/null; true

### [032] ✅ DONE — Cortex dashboard — read data.json for KPI banner
Brief: Update `projects/cenoa-cortex/index.html`. Replace hardcoded KPI values with JS that fetches `data.json` on page load. Fallback to current values if fetch fails.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[032] KPI banner reads data.json" 2>/dev/null; true

### [033] 🟥 RETRY — Cortex — country breakdown widget (previous run produced no commit/deploy)
Brief: Add 4 country cards to Cortex (TR/NG/EG/PK) showing installs, signups, KYC, withdrawals per country. Read from data.json. Below KPI banner.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[033] Country breakdown widget" 2>/dev/null; true

### [034] Cortex — funnel visualization (Chart.js bar chart)
Brief: Add horizontal bar chart showing funnel: Install → Signup → KYC → Deposit → Withdrawal. Using Chart.js CDN. Read from data.json.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[034] Funnel visualization" 2>/dev/null; true

### [035] Cortex — campaign performance table
Brief: Add table showing top campaigns with spend, installs, CPI. Data from BigQuery or Sheets parse. Include in data.json.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[035] Campaign performance table" 2>/dev/null; true

### [036] Week-over-week comparison logic
Brief: In `scripts/kpi_auto_update.py`, add WoW comparison. For each KPI: this week vs last week → delta %. Store in data.json as `{direction: "up"|"down"|"neutral", delta: "+X%"}`.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[036] WoW comparison logic" 2>/dev/null; true

### [037] Anomaly detection script
Brief: Create `scripts/anomaly_detection.py`. If any KPI drops/rises >20% WoW, flag it. Output: list of anomalies with severity. Save to `data/anomalies.json`.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[037] Anomaly detection script" 2>/dev/null; true

### [038] Weekly report template (Telegram format)
Brief: Create `scripts/weekly_report.py`. Generates markdown report: KPIs, WoW deltas, country breakdown, top/bottom campaigns, anomalies, action items. Format for Telegram (no tables, bullet lists).
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[038] Weekly report template" 2>/dev/null; true

### [039] Retention analysis script (D1, D7, D30)
Brief: Create `scripts/amplitude_retention.py`. Query Amplitude retention API (if available) or compute from daily active data. By country. Save to `data/retention-{date}.json` + `analysis/retention.md`.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[039] Retention analysis" 2>/dev/null; true

### [040] Feature engagement by country
Brief: `analysis/feature-engagement.md`. Query Amplitude for Get Paid Opened, Money Transfer Clicked, Deposit Tapped — by country. Which features are used where?
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[040] Feature engagement by country" 2>/dev/null; true

### [041] Referral program analysis
Brief: `analysis/referral-analysis.md`. Find referral-related events in Amplitude (Recipient Sign-Up Completed, etc.). Volume, conversion, country split.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[041] Referral program analysis" 2>/dev/null; true

### [042] Funnel summary document (all findings)
Brief: `analysis/funnel-summary.md`. Combine [015]-[022] + [039]-[041] into one comprehensive funnel document. Executive-ready. Top insights, worst bottlenecks, recommended actions.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[042] Funnel summary document" 2>/dev/null; true

### [043] Marginal CAC analysis
Brief: `analysis/marginal-cac.md`. Using monthly budget data: for each $1K additional spend, how many additional signups? Diminishing returns curve. Optimal spend level per country.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[043] Marginal CAC analysis" 2>/dev/null; true

### [044] Google Ads campaign deep-dive from Looker data
Brief: `analysis/google-ads-deepdive.md`. Parse all campaign data visible in Looker (Main Traffic page). Campaign → installs → CPI → which to scale, which to kill. Include the Demand Gen 0-install anomaly.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[044] Google Ads campaign deep-dive" 2>/dev/null; true

### [045] Meta Ads campaign analysis (from MCP data)
Brief: Using data from [001], create `analysis/meta-ads-analysis.md`. Active campaigns, spend, performance, creative breakdown. Recommendations.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[045] Meta Ads campaign analysis" 2>/dev/null; true

### [046] Cortex — CAC trend chart (Chart.js)
Brief: Add monthly CAC bar chart to Cortex dashboard. Use historical data from Sheets + current from Amplitude. Chart.js.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[046] CAC trend chart" 2>/dev/null; true

### [047] Cortex — KYC dropout trend chart
Brief: Add weekly KYC dropout rate trend line to Cortex. Show KYC Started vs KYC Submit over time.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[047] KYC dropout trend chart" 2>/dev/null; true

### [048] Cortex — Action Items auto-section
Brief: Add "🎯 This Week's Actions" section to Cortex. Read from data.json action_items array. Auto-generated from anomaly detection + funnel bottlenecks.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-cortex && git add -A && git commit -m "[048] Action Items section" 2>/dev/null; true

### [049] A/B test framework document
Brief: `analysis/ab-test-framework.md`. Template: Hypothesis → Metric → Audience → Duration → Success criteria. Include 5 ready-to-run test ideas (KYC flow, LP CTA, onboarding, pricing page, referral incentive).
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[049] A/B test framework" 2>/dev/null; true

### [050] Performance marketing master report v1
Brief: `analysis/MASTER_REPORT_v1.md`. Comprehensive 5-page report combining all findings: data inventory, funnel analysis, unit economics, campaign performance, action plan. The "board deck" document.
Workspace: /Users/alperengumusdograyan/.openclaw/workspace
Commit: cd projects/cenoa-performance-marketing && git add -A && git commit -m "[050] Master report v1" 2>/dev/null; true
