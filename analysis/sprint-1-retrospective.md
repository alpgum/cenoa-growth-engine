# Sprint 1 Retrospective — Cenoa Performance Marketing (Agent)

**Sprint window:** 2026-03-21 (Sprint Mode kickoff)

**Scope (what Sprint 1 was trying to achieve):**
- Stand up a reliable *weekly performance operating system* (data pull → KPI surface → alerts → actions).
- Produce decision-grade analysis across **country / platform / channel** with explicit caveats where attribution is broken.
- Turn the work into reusable assets: scripts, cron wrappers, canonical docs.

---

## 1) What worked

### Sprint Mode execution
- **Queue discipline as a system:** `TASK_QUEUE.md` with explicit status, dependencies, and “skip if blocked” rules prevented dead ends from consuming the sprint.
- **Small, composable outputs:** Each task produced a concrete artifact (script, JSON export, analysis doc) that could be referenced downstream.

### Scripts + automation (high leverage)
- **Reusable Amplitude pulls** (`scripts/amplitude_*`) turned manual exploration into a repeatable pipeline.
- **Weekly pulse automation** shipped end-to-end:
  - KPI refresh + publish (via Cortex `data.json` convention)
  - **Anomaly detection** (`scripts/anomaly_detection.py` + `scripts/anomaly_alert_cron.sh`)
  - **Weekly report** (`scripts/weekly_report.py` + `scripts/weekly_report_cron.sh`) saved to `data/weekly-report-latest.md`
  - **Campaign health checks** (`scripts/campaign_health_check.py`) + alert wrapper (see `analysis/automation-setup.md`)
- **Telegram-friendly formatting** (HTML / concise bullets) reduced friction for “eyes-on” monitoring.

### KPI surface area (Cortex)
- **KPI banner design** (Cortex reading a canonical `data.json`) created a single “source of truth” for weekly reporting and automation.
- Separation of concerns worked well:
  - Cortex = presentation layer
  - `cenoa-performance-marketing/scripts` = computation layer
  - `cenoa-performance-marketing/data/*.json` = audit trail

### Analysis that drove decisions
- Funnel analyses across **global + TR/NG/EG/PK**, plus platform and attribution breakdowns, quickly identified the biggest leaks:
  - KYC submit collapse
  - web→app attribution leakage inflating “organic” and “(none)” buckets
  - market-specific activation issues (EG)

---

## 2) What didn’t

### Attribution gaps (web→app leakage)
- A structurally large **“(none)” / misattributed** bucket exists in downstream events (sign-up / withdrawal), especially for web-to-app flows.
- Net effect: **channel-level CAC and ROI are directionally useful but not decision-grade** until OneLink + UTM persistence closes the loop.

### Country/platform = “(none)” issues
- Significant portions of events show **country/platform as “(none)”** (often web, missing geo or missing property propagation).
- This breaks “country CAC” and “platform funnel” analyses unless the missingness is explicitly modeled and reported.

### Connector errors / Looker fragility
- **Supermetrics connector failures** (Meta, TikTok organic, LinkedIn organic, IG organic) reduced confidence in Looker Studio as a primary source.
- Broken connectors created a pattern of “dashboard looks empty → analysis stalls”. The sprint ended up leaning on **Amplitude/BigQuery/Sheets** as the canonical layer.

### Meta MCP access limits
- The Meta MCP path was **not reliably available to subagents**, blocking programmatic campaign-level insights (CPM, CTR, frequency, creative performance).
- Workarounds existed (browser UI / exports), but they’re slower and harder to operationalize.

---

## 3) Data quality issues found + fixes

### (A) Time window alignment / script correctness
**Issue:** Early Amplitude scripts initially produced mismatched totals due to date boundaries / query configuration.

**Fixes applied:**
- Added explicit date-range handling and re-ran pulls until numbers matched manual spot-checks.
- Persisted outputs (`data/amplitude-weekly-*.json`, `data/amplitude-country-*.json`, etc.) to create an auditable trail.

### (B) Definition mismatches across sources
**Issue:** “Active / virtual account / KYC” definitions differ between Sheets (CAC analysis) vs Amplitude events vs AppsFlyer views.

**Fixes applied:**
- Documented canonical event mapping and created analysis docs that state **exact event names and denominators**.
- Added “cross-check” logic/docs (e.g., `analysis/cac-crosscheck.md`) so inconsistencies are visible, not hidden.

### (C) Missing property propagation
**Issue:** AppsFlyer attribution does not consistently propagate to downstream Amplitude events; country/platform sometimes missing.

**Fixes applied (operational, not fully solved):**
- Every attribution analysis now includes an explicit **Attribution Gap Warning** and avoids over-confident budget recommendations.
- Proposed remediation path: **AppsFlyer OneLink + deferred deep linking + UTM handoff** (see `analysis/attribution-comparison.md`, `analysis/optimization-playbook.md`).

### (D) Tooling reliability
**Issue:** Looker dashboards depend on connectors that can silently fail.

**Fixes applied:**
- Treated Looker as “presentation / screenshot source”, not as canonical truth.
- Promoted BigQuery + Sheets + Amplitude exports into the canonical dataset used by scripts.

---

## 4) Process improvements for next sprint

### Better queue discipline
- Limit work-in-progress harder (even within “3 slots”). When a task depends on missing access (e.g., Meta), **skip early** and continue.
- Add a “Definition of Done” checklist per task:
  - artifact exists
  - referenced paths are committed
  - numbers cross-checked (at least 1 alternative source)

### Stronger cross-check habit (before publishing conclusions)
- For every funnel / CAC / ROI claim, require at least one of:
  - Sheets vs Amplitude cross-check
  - Amplitude vs BigQuery cross-check
  - last week vs prior week sanity check (distribution shifts)

### Make “data contracts” explicit
- Maintain a small “canonical metrics contract” doc:
  - event names
  - segmentation properties
  - fallback logic for missing country/platform
  - time zone convention

### Operationalize attribution repair as a dedicated track
- Treat attribution fixes (OneLink, UTM persistence, deep-link validation) as *Sprint 2 P0*, because they unlock higher confidence in every paid decision.

---

## 5) Top 10 learnings (Sprint 1)

1. **Automation beats dashboards.** Scripts + JSON audit trail were more reliable than connector-heavy Looker views.
2. **Attribution leakage is the #1 constraint** on budget decisions (Meta/TikTok/Google web flows miscredit to organic/(none)).
3. **Country/platform missingness is not noise**—it meaningfully distorts funnel rates unless explicitly handled.
4. **KYC submit is a catastrophic bottleneck**; improving KYC completion likely dominates most acquisition optimizations.
5. **Egypt’s funnel needs activation fixes** (cheap acquisition is meaningless if withdrawal/activation stays low).
6. **Nigeria shows “inverted funnel” artifacts** (likely existing users driving withdrawals) → cohorting matters.
7. **Campaign-level health heuristics are useful** (DEAD/BLEEDING/FRAUD) even before perfect attribution.
8. **WoW anomaly alerts reduce cognitive load**—you only investigate when something moves materially.
9. **Data definitions must be written down** (especially “active”), otherwise analysis becomes inconsistent across sources.
10. **Access constraints shape architecture.** When APIs aren’t available (Meta MCP), design for UI-export fallbacks and keep the system modular.

---

## 6) Suggested updates to agent knowledge (docs to reference)

### Add/refresh references in agent knowledge
- **Operating system & automation:**
  - `projects/cenoa-performance-marketing/analysis/automation-setup.md`
  - `projects/cenoa-performance-marketing/analysis/optimization-playbook.md`
- **Attribution caveats + remediation:**
  - `projects/cenoa-performance-marketing/analysis/attribution-funnel.md`
  - `projects/cenoa-performance-marketing/analysis/attribution-comparison.md`
  - `projects/cenoa-performance-marketing/analysis/cac-crosscheck.md`
- **Canonical sprint artifacts:**
  - `projects/cenoa-performance-marketing/TASK_QUEUE.md` (Sprint Mode rules + provenance)
  - `projects/cenoa-performance-marketing/analysis/MASTER_REPORT_v1.md` (source catalog + limitations)
- **Scripts to treat as canonical tools:**
  - `scripts/amplitude_weekly_pull.py`, `scripts/amplitude_country_breakdown.py`, `scripts/amplitude_platform_breakdown.py`, `scripts/amplitude_attribution.py`
  - `scripts/anomaly_detection.py`, `scripts/weekly_report.py`, `scripts/campaign_health_check.py`

### Knowledge update themes
- Always include an **Attribution Gap Warning** in any channel-level recommendation until OneLink + UTM persistence is verified.
- Standardize “active” and downstream funnel definitions across Sheets/Amplitude/AppsFlyer before publishing CAC-to-active claims.
- Prefer a **script-first data pipeline** with JSON outputs; dashboards are optional consumers.
