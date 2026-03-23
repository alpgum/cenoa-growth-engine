# Access Inventory — Cenoa Performance Marketing

> Last updated: 2026-03-21
> Sprint: [010]

## ✅ Working

### Amplitude (Product Analytics)
- **MCP:** Connected for Claude Code ACP sessions
- **REST API:** API_KEY + SECRET_KEY confirmed working (basic auth)
- **Credentials:** `~/.openclaw/credentials/amplitude.env`
- **Confirmed endpoints:** Dashboard REST API, Export API, Taxonomy API, User Activity
- **Data pulled:** Weekly metrics, country breakdown, platform breakdown, attribution data

### BigQuery
- **Project:** `cenoa-marketingdatawarehouse`
- **Service account:** `openclaw-bq-writer@cenoa-marketingdatawarehouse.iam.gserviceaccount.com`
- **Credentials:** `~/.openclaw/credentials/cenoa-marketingdatawarehouse-82b8600e66d6.json`
- **Dataset:** `marketing_appsflyer` (2 tables — AppsFlyer attribution data)
- **Access level:** Writer (can read + write)

### GA4 (Google Analytics 4)
- **Service account:** Same as BigQuery (`openclaw-bq-writer@...`)
- **Access level:** Viewer on GA4 property
- **Use:** Sessions, events, conversions, traffic sources via GA4 Data API

### Google Sheets (3 sheets)
- **Credentials:** Same service account as BigQuery
- **Sheets:**
  1. `1H27QF84Nm02nAhXebP6zWgEG7pwu_UTwcliO_c4mKmM` — Budget tracking
  2. `1VTZQbRD0gZAABLvgjwlymAx0sQ7vcvMUySsWzLhnFKk` — CAC analysis
  3. `1d743wipSvWEfwwXCmy2J73yCAMNYa-hCb-nTvNf3yHc` — Trafik Canavarı (traffic data)

### Looker Studio (Embed)
- **URL:** `https://lookerstudio.google.com/embed/reporting/1e81a948-62f8-42d9-9c6c-31aab4dd60c6`
- **Access:** Embed working, viewable via browser tool
- **Use:** Visual dashboards, screenshots for reporting

### AppsFlyer Pull API
- **Credentials:** `~/.openclaw/credentials/appsflyer.env`
- **Status:** Token stored, endpoint validation pending

---

## 🟡 Partially Working

### Meta Ads
- **MCP:** Configured in OpenClaw but **NOT exposed to subagents**
- **Workaround 1:** Run Meta Ads queries in main session where MCP is available
- **Workaround 2:** Use browser tool to access Meta Ads Manager UI
- **Workaround 3:** Export CSV manually from Meta Ads Manager
- **TODO:** Investigate exposing MCP to subagents or building a direct API integration

### AppsFlyer Attribution
- **Status:** Token received, connection + app list still pending
- **Data available via:** BigQuery (`marketing_appsflyer` dataset) as alternative

---

## ❌ Not Working

### Looker Studio — Supermetrics Connectors
- **Issue:** 4 connectors broken (likely expired auth or license issue)
- **Impact:** Dashboard data may be stale for connector-dependent charts
- **Workaround:** Pull raw data directly from BigQuery/Sheets/Amplitude instead
- **Fix needed:** Re-authenticate Supermetrics connectors or renew license

---

## Data Access Summary

| Source | Direct API | BigQuery | Sheets | Looker | Notes |
|--------|-----------|----------|--------|--------|-------|
| Amplitude | ✅ REST + MCP | — | — | — | Full product analytics |
| GA4 | ✅ Data API | — | — | ❌ connector | Service account viewer |
| Meta Ads | 🟡 MCP only | — | — | ❌ connector | Main session only |
| AppsFlyer | 🟡 Pull API | ✅ 2 tables | — | ❌ connector | BQ is reliable path |
| Budget/CAC | — | — | ✅ 3 sheets | — | Manual data |
| Google Ads | — | — | — | ❌ connector | No direct access yet |

---

## Recommended Data Pipeline

1. **Product metrics:** Amplitude REST API or MCP
2. **Attribution:** BigQuery `marketing_appsflyer` dataset (most reliable)
3. **GA4 traffic:** GA4 Data API via service account
4. **Budget/spend:** Google Sheets API
5. **Meta Ads:** Main session MCP or browser export
6. **Visual dashboards:** Looker Studio embed via browser screenshot
