# Automation Setup

## Anomaly Alert (Telegram)

**Script:** `scripts/anomaly_alert_cron.sh`

### What it does
1. Runs `anomaly_detection.py` against `cenoa-cortex/data.json`
2. Checks `data/anomalies.json` for flagged KPIs (|deltaPct| ≥ 20%)
3. If anomalies found → outputs a Telegram-formatted alert to stdout
4. If no anomalies → exits silently (no message sent)

### Trigger
- **Frequency:** After each weekly data refresh (recommended: Monday morning)
- **Method:** OpenClaw cron pipes stdout to Telegram
- **Example cron:** `openclaw cron add --schedule "0 9 * * 1" --command "bash scripts/anomaly_alert_cron.sh" --channel telegram`

### Severity levels
| Level | Threshold | Icon |
|-------|-----------|------|
| Warning | ±20–40% | 🟡 |
| Critical | >±40% | 🔴 |

### Example alert message

```
🚨 Anomaly Alert — W12 2026
Threshold: ±20%  |  1 critical, 2 warning

🔴 CPI: 0.42 → 0.68 (↑61.9%)
🟡 D7 Retention: 18.2% → 14.1% (↓22.5%)
🟡 Install Volume: 12400 → 9800 (↓21.0%)

📊 Run weekly_report.py for full breakdown.
```

### Dependencies
- Python venv: `~/.openclaw/venv`
- Input: `projects/cenoa-cortex/data.json`
- Output: `projects/cenoa-performance-marketing/data/anomalies.json`

---

## Weekly Report (Telegram)

**Script:** `scripts/weekly_report_cron.sh`

### What it does
1. Sources the Python venv
2. Runs `weekly_actions.py` (best-effort) to write `data/weekly-actions.json`
3. Runs `weekly_report.py` which reads `cenoa-cortex/data.json`, `data/anomalies.json`, `data/weekly-actions.json`, and country breakdown data
4. Outputs a Telegram-formatted weekly pulse report to stdout
5. Saves a copy to `data/weekly-report-latest.md`

### Trigger
- **Schedule:** Monday 10:00 TRT (Europe/Istanbul)
- **Method:** OpenClaw cron pipes stdout to Telegram
- **Example cron:** `openclaw cron add --schedule "0 10 * * 1" --tz "Europe/Istanbul" --command "cd projects/cenoa-performance-marketing && bash scripts/weekly_report_cron.sh" --channel telegram`

### Dependencies
- **KPI cron must run first** — `weekly_kpi_cron.sh` runs at 09:00 TRT and updates `data.json` + deploys Cortex
- **Anomaly detection** — `anomaly_alert_cron.sh` runs at 09:00 and writes `data/anomalies.json`
- Python venv: `~/.openclaw/venv`
- Input: `projects/cenoa-cortex/data.json`, `data/anomalies.json`, `data/country-breakdown-*.json`
- Output: `data/weekly-report-latest.md` + stdout

### Execution order (Monday morning)
| Time (TRT) | Script | Purpose |
|------------|--------|---------|
| 09:00 | `weekly_kpi_cron.sh` | Pull KPIs from Amplitude, update data.json, deploy Cortex |
| 09:00 | `anomaly_alert_cron.sh` | Detect anomalies, write anomalies.json, alert if critical |
| 10:00 | `weekly_report_cron.sh` | Generate full weekly pulse report, send via Telegram |

### Manual test
```bash
cd ~/.openclaw/workspace/projects/cenoa-performance-marketing
./scripts/weekly_report_cron.sh
# Report prints to stdout; check data/weekly-report-latest.md for saved copy
```

---

## Weekly PDF Export (Cortex Dashboard Snapshot)

**Script:** `scripts/weekly_pdf_export.sh`

### What it does
- Exports the live `projects/cenoa-cortex/index.html` dashboard as a PDF snapshot.
- Saves to: `reports/weekly-YYYY-MM-DD.pdf`

### How it works
1. If `puppeteer` is installed → renders and saves a PDF automatically (best fidelity).
2. Else if Chrome/Chromium is available → uses `--headless --print-to-pdf` automatically.
3. Else → opens the dashboard in your default browser and prompts you to **Cmd+P → Save as PDF**.

### Manual run
```bash
cd ~/.openclaw/workspace/projects/cenoa-performance-marketing
bash scripts/weekly_pdf_export.sh
# Output: reports/weekly-YYYY-MM-DD.pdf
```

### Notes
- If your `cenoa-cortex` repo is not in the default sibling location, set `CORTEX_DIR`:
  `CORTEX_DIR=~/.openclaw/workspace/projects/cenoa-cortex bash scripts/weekly_pdf_export.sh`

---

## Weekly Actions (Auto-generated)

**Script:** `scripts/weekly_actions.py`

### What it does
1. Reads weekly KPI snapshot from `projects/cenoa-cortex/data.json`
2. Reads detected anomalies from `data/anomalies.json` (if present)
3. Reads campaign/channel health flags from `data/campaign-health.json` (if present)
4. Optionally reads `data/budget-pacing.json` + latest `data/country-breakdown-*.json`
5. Produces a ranked list of action items with:
   - **severity** (P0/P1/P2)
   - **owner** (Acquisition/Product/Data)
   - **why** + **expected impact**

### Output
- Writes: `data/weekly-actions.json`
- `weekly_report.py` includes the **top 8** actions when this file exists.

### Trigger
- No separate cron required: `scripts/weekly_report_cron.sh` runs `weekly_actions.py` first (best-effort).

### Manual test
```bash
cd ~/.openclaw/workspace/projects/cenoa-performance-marketing
source ~/.openclaw/venv/bin/activate
python3 scripts/weekly_actions.py
cat data/weekly-actions.json | head
```

---

## Dead Campaign Sweep (Telegram)

**Script:** `scripts/dead_campaign_sweep_cron.sh`

### What it does
1. Activates the Python venv (`~/.openclaw/venv`)
2. Runs `scripts/campaign_health_check.py` (writes `data/campaign-health.json`)
3. If any items are flagged as <b>DEAD</b> / <b>BLEEDING</b> / <b>FRAUD</b> → prints a Telegram HTML alert to stdout
4. If nothing is flagged → exits silently (no message sent)

### Trigger
- **Recommended schedule:** Monday **09:05 TRT** (Europe/Istanbul) — after KPI pull + anomaly detection
- **Example cron:** `openclaw cron add --schedule "5 9 * * 1" --tz "Europe/Istanbul" --command "cd projects/cenoa-performance-marketing && bash scripts/dead_campaign_sweep_cron.sh" --channel telegram`

### Manual test
```bash
cd ~/.openclaw/workspace/projects/cenoa-performance-marketing
./scripts/dead_campaign_sweep_cron.sh
# Prints ONLY if there are DEAD/BLEEDING/FRAUD flags.
# Always writes/refreshes: data/campaign-health.json
```

### Example alert output

```text
🚨 <b>Campaign Health Alert</b>
<i>Generated:</i> <code>2026-03-21T09:05:12</code>
<i>Avg CPI (paid):</i> <code>$1.42</code>

<b>Channels</b>
• <code>meta_web2app</code> — 💀 <b>DEAD</b>: $2754 spent, 0 installs
• <code>tiktok</code> — 🩸 <b>BLEEDING</b>: CPI $3.10 is 2.2× the average ($1.42)

<b>Campaigns</b>
• <code>TR iOS - ASA - Brand</code> — 🚨 <b>FRAUD</b>: 120 installs, 2 signups (1.7%) — fraud pattern

Next: check <code>campaign_health_check.py</code> output in <code>data/campaign-health.json</code>.
```

---

## Monthly Executive Deck (Gamma)

**Script:** `scripts/monthly_deck.py`

### What it does
1. Reads latest exported KPI/funnel/CAC artifacts in `data/` and `analysis/` (best-effort, offline-first)
2. Writes a structured deck outline to: `data/monthly-deck.json`
3. Writes a paste-ready narrative to: `analysis/monthly-deck.md`

### Trigger
- **Recommended schedule:** **1st of every month 10:15 TRT** (Europe/Istanbul)
- **Example cron:**
  `openclaw cron add --schedule "15 10 1 * *" --tz "Europe/Istanbul" --command "cd projects/cenoa-performance-marketing && source ~/.openclaw/venv/bin/activate && python3 scripts/monthly_deck.py"`

### Manual test
```bash
cd ~/.openclaw/workspace/projects/cenoa-performance-marketing
source ~/.openclaw/venv/bin/activate
# Defaults to previous calendar month
python3 scripts/monthly_deck.py

# Explicit month
python3 scripts/monthly_deck.py --month 2026-02

# Outputs:
# - data/monthly-deck.json
# - analysis/monthly-deck.md
```

### Gamma workflow (no API)
- Paste `analysis/monthly-deck.md` into Gamma → **Create from text**
- Or use `data/monthly-deck.json` as a structured outline and build slides manually

---

## Cortex Auto-Deploy Pipeline

**Script:** `scripts/auto_deploy_cortex.sh`

### How to run
```bash
cd ~/.openclaw/workspace/projects/cenoa-performance-marketing
bash scripts/auto_deploy_cortex.sh
```

### What it does
1. **KPI auto-update** — pulls latest data from Amplitude/BigQuery/Sheets, generates `data.json` in cenoa-cortex
2. **Anomaly detection** — flags KPIs with significant week-over-week changes
3. **Campaign health check** — identifies dead/bleeding/fraud campaigns
4. **Budget pacing** — checks spend vs. budget targets
5. **Data quality monitor** — validates data completeness and freshness
6. **Weekly actions** — generates prioritized action items from all signals
7. **Weekly report** — produces the full weekly pulse report
8. **Commit PM repo** — stages and commits all updated data/reports
9. **Deploy to Cortex** — commits updated `data.json` to cenoa-cortex and pushes (Vercel auto-deploys)

### Expected runtime
~2–3 minutes (depends on API response times from Amplitude, BigQuery, Google Sheets)

### Error handling
- Steps 1 and 7 are **required** (`set -e` will abort on failure)
- Steps 2–6 use `|| true` — failures are logged but don't block the pipeline
- Step 8 uses `|| true` — no-op if nothing changed
- Step 9 uses `|| true` — handles case where data.json is unchanged

### Trigger
- **Recommended:** Monday morning, single command for the full weekly refresh
- **Example cron:**
  `openclaw cron add --schedule "0 9 * * 1" --tz "Europe/Istanbul" --command "cd ~/.openclaw/workspace/projects/cenoa-performance-marketing && bash scripts/auto_deploy_cortex.sh" --channel telegram`
- This replaces the need to run individual cron jobs for KPI pull, anomaly detection, etc.

### Output
- Cortex dashboard: https://cenoa-cortex.vercel.app
- PM data artifacts in `data/` directory
- Weekly report in `data/weekly-report-latest.md`

---

## Weekly launchd Automation (macOS)

**Plist:** `~/Library/LaunchAgents/com.cenoa.growth-engine.weekly.plist`
**Script:** `scripts/auto_deploy_cortex.sh`

### Schedule
- **Every Monday at 09:00 TRT** (06:00 UTC)
- Uses macOS `launchd` (StartCalendarInterval: Weekday=1, Hour=6, Minute=0)

### What it runs
The full Cortex auto-deploy pipeline: KPI pull → anomaly detection → campaign health → budget pacing → data quality → weekly actions → weekly report → commit → deploy.

### Logs

```bash
# Stdout
cat /tmp/cenoa-growth-engine-weekly.log

# Stderr
cat /tmp/cenoa-growth-engine-weekly-err.log

# Tail live (during execution)
tail -f /tmp/cenoa-growth-engine-weekly.log
```

### How to disable / re-enable

```bash
# Disable (unload)
launchctl unload ~/Library/LaunchAgents/com.cenoa.growth-engine.weekly.plist

# Re-enable (load)
launchctl load ~/Library/LaunchAgents/com.cenoa.growth-engine.weekly.plist

# Check status
launchctl list | grep cenoa.growth
# Output: -  0  com.cenoa.growth-engine.weekly  (loaded, exit code 0)
```

### Notes
- The machine must be awake at 06:00 UTC for launchd to fire. If asleep, it runs on next wake.
- PATH includes `/opt/homebrew/bin` for Homebrew Python access.
- WorkingDirectory is set to `~/.openclaw/workspace`.
