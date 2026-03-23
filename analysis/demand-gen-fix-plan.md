# Demand Gen Retargeting Fix Plan

**Campaign:** TR-Discovery-24.10.2025  
**Type:** Demand Gen (Retargeting)  
**Created:** 2026-03-21  
**Sprint:** 059  
**Status:** 🔴 PAUSE IMMEDIATELY

---

## 1. Current State

| Metric | Value |
|---|---|
| Period | Mar 14–20, 2026 |
| Clicks | 1,627 |
| Installs (AppsFlyer attributed) | **0** |
| Spend (period) | ₺19,620 (~$560) |
| Cost per Install | **∞** (division by zero) |
| Campaign age | ~5 months (since Oct 24, 2025) |
| Estimated total waste (5 months) | ₺100K–200K+ (~$2,800–$5,600) |

**Context:** During the same week, Google Pmax delivered 27 installs at ~$30 CPI and Search delivered 27 installs at ~$29 CPI. This campaign delivered zero with comparable spend velocity.

---

## 2. Likely Root Causes

### 2a. Retargeting existing app users (HIGH probability)
Demand Gen retargeting targets users who previously visited the website or engaged with ads. These users likely **already installed the app** — no new install event fires. The campaign is spending money to re-engage people who are already in the funnel. AppsFlyer counts installs, not re-engagements, so the campaign appears to produce nothing.

### 2b. Wrong conversion action configured (HIGH probability)
The campaign may be optimizing toward a **web conversion** (e.g., page visit, form submission) rather than an **app install conversion action**. If Google Ads is tracking "website visits" as conversions, it will happily optimize for clicks that never reach the app store. Check:
- Which conversion action is assigned to this campaign?
- Is it a Google Ads web tag firing on landing page load?
- Is the Firebase/AppsFlyer app install event linked as the primary conversion?

### 2c. Attribution chain broken (MEDIUM probability)
Even if some users do install after clicking, the attribution may be lost:
- **Landing page → App Store → Install** has a redirect hop that breaks the AppsFlyer click-through attribution window
- Deep links may not be configured, so users land on a generic web page and manually search the app store
- Google Ads click ID (GCLID) may not be passed through to the app store listing → AppsFlyer can't attribute

### 2d. Audience too broad (MEDIUM probability)
If the retargeting audience is "all website visitors" with no recency or intent filters:
- Includes users who bounced in 2 seconds
- Includes users who already completed KYC and are active
- Includes bot traffic / accidental visitors
- No exclusion of existing app installers

### 2e. Click fraud / invalid traffic (LOW-MEDIUM probability)
1,627 clicks with zero downstream outcome is suspicious. Demand Gen surfaces (YouTube, Discover, Gmail) are known for accidental clicks on mobile, especially on interstitial/feed ads. Could be:
- Accidental taps on mobile feed ads
- Invalid traffic not yet filtered by Google
- Bot impressions on partner sites

---

## 3. Diagnostic Steps (Check in Google Ads Console)

### Immediate (Day 1 — before pausing or after pause)

| # | What to Check | Where in Google Ads |
|---|---|---|
| 1 | **Conversion action assignment** | Campaign → Settings → Goals → Which conversion actions? Look for "App installs" vs web conversions |
| 2 | **All conversions report** | Campaign → Columns → Modify → Add "All conversions" + "View-through conversions" → Does this campaign show ANY conversions at all? |
| 3 | **Landing page destination** | Campaign → Ads → Click any ad → Where does it land? App store? Web page? Deep link? |
| 4 | **Audience definition** | Campaign → Audiences → What segments? "All visitors"? "Visitors last 540 days"? Any exclusions? |
| 5 | **Invalid click rate** | Campaign → Columns → Add "Invalid clicks" + "Invalid click rate" |
| 6 | **Placement report** | Campaign → Placements → Where are ads showing? YouTube? Gmail? Partner sites? |

### Within 48 Hours

| # | What to Check | How |
|---|---|---|
| 7 | **AppsFlyer re-engagement report** | AppsFlyer → Retargeting dashboard → Filter by Google Ads → Any re-engagements or re-attributions? |
| 8 | **Google Ads assisted conversions** | Google Ads → Attribution → Model comparison → Does this campaign assist conversions attributed to other campaigns? |
| 9 | **Web analytics for landing page** | GA4 → Landing pages → Filter by campaign UTM → Bounce rate, time on page, next action |
| 10 | **Audience overlap with existing installers** | Google Ads → Audience Manager → Check if retargeting list overlaps with app installer exclusion list |

---

## 4. Fix Options

### Option A: Pause Immediately (RECOMMENDED — do this NOW)

| Detail | Value |
|---|---|
| Action | Pause campaign in Google Ads console |
| Timeline | Today |
| Savings | ~₺19,620/week (~$560/week, ~$2,240/month) |
| Risk | Zero — campaign produces nothing measurable |
| Reversibility | Can re-enable anytime |

**This is the default action.** Zero installs = zero reason to keep spending. Pause first, diagnose second.

### Option B: Fix Conversion + Narrow Audience + Relaunch

If diagnostics reveal the campaign has potential (e.g., it was driving web conversions or re-engagements that weren't tracked):

| Step | Action | Timeline |
|---|---|---|
| 1 | Switch primary conversion to **Firebase app_install** or **AppsFlyer in-app event** | Day 1–2 |
| 2 | Add audience exclusions: exclude existing app installers (upload AppsFlyer device list or use Firebase audience) | Day 2–3 |
| 3 | Narrow retargeting audience to **high-intent web visitors only**: visited pricing page, started signup, or spent >60s on site | Day 2–3 |
| 4 | Add recency filter: only visitors from **last 30 days** (not 540-day stale audiences) | Day 2–3 |
| 5 | Set up proper deep links so ad click → app store → install attribution works | Day 3–5 |
| 6 | Relaunch with ₺5,000/week budget (75% reduction from current) | Day 7 |
| 7 | Monitor for 2 weeks — if CPI > ₺500 (~$14), kill permanently | Day 7–21 |

**Prerequisites:**
- Confirm conversion action is tracking app installs
- Confirm deep link / deferred deep link flow works end-to-end
- Exclude existing installers from audience

### Option C: Convert to App Install Campaign

Instead of trying to fix Demand Gen retargeting, redirect the budget to a proven format:

| Detail | Value |
|---|---|
| Action | Create new **Google App Campaign (UAC)** targeting TR |
| Budget | ₺10,000/week (half of current Demand Gen waste) |
| Conversion goal | App installs (Firebase/AppsFlyer) |
| Expected CPI | ₺200–400 based on existing Google App Android performance |
| Expected installs | 25–50/week at ₺10K budget |

**Advantage:** Google App Campaigns are purpose-built for installs. They automatically optimize across Search, Play Store, YouTube, Display, and Discover — same surfaces as Demand Gen but with install-optimized bidding.

**Note:** An existing "Google App Android" campaign already runs at ~$1,400/wk (~₺49K). Adding ₺10K would be a ~20% scale-up of an already-proven format. Consider simply increasing that campaign's budget instead of creating a new one.

---

## 5. Expected Impact

### If Option A (Pause Only)
| Metric | Impact |
|---|---|
| Weekly savings | ₺19,620 (~$560) |
| Monthly savings | ~₺78,480 (~$2,240) |
| Install impact | Zero (campaign produces 0 installs) |
| CPI impact on portfolio | Improves — removes ∞ CPI drag from blended metrics |
| Freed budget reallocation | → Pmax (+₺14K) which produces installs at ₺1,050 CPI |

### If Option B (Fix + Relaunch)
| Metric | Optimistic | Conservative |
|---|---|---|
| Relaunched budget | ₺5,000/wk | ₺5,000/wk |
| Expected installs | 10–15/wk | 3–5/wk |
| Expected CPI | ₺333–500 | ₺1,000–1,667 |
| Net savings vs current | ₺14,620/wk | ₺14,620/wk |
| Verdict | Worth running | Kill if CPI > ₺500 |

### If Option C (Convert to App Campaign)
| Metric | Expected |
|---|---|
| Budget | ₺10,000/wk (₺9,620 saved vs current) |
| Expected installs | 25–50/wk |
| Expected CPI | ₺200–400 |
| Net new installs vs current | +25–50 (from zero) |
| Budget savings reallocated | ₺9,620/wk → Pmax or Search |

### Portfolio-Level Impact (any option)

Current Google blended CPI includes this campaign's spend dragging the average up. Removing ₺19,620 of waste:

| Metric | Before | After (Option A) |
|---|---|---|
| Google weekly spend (TR) | ~₺56,000 | ~₺36,380 |
| Google weekly installs (TR) | 54 | 54 (unchanged) |
| Google blended CPI (TR) | ~₺1,037 | ~₺674 (35% improvement) |
| Freed budget → Pmax | — | +₺19,620 → ~19 more installs at ₺1,050 CPI |
| New total installs | 54 | ~73 (+35%) |

---

## 6. Timeline

| Day | Action | Owner | Status |
|---|---|---|---|
| **Day 0 (Now)** | **Pause campaign** in Google Ads | Alp / Growth | 🔴 Do immediately |
| Day 1 | Run diagnostics (steps 1–6 from Section 3) | Alp / Growth | ⏳ |
| Day 1 | Pull "All conversions" report for campaign lifetime | Alp / Growth | ⏳ |
| Day 2 | Check AppsFlyer retargeting dashboard | Alp / Growth | ⏳ |
| Day 2 | Check Google Ads assisted conversions | Alp / Growth | ⏳ |
| Day 3 | **Decision point:** Kill permanently OR fix + relaunch | Alp | ⏳ |
| Day 3–5 | If relaunching: fix conversion actions, audiences, deep links | Growth | ⏳ |
| Day 7 | Relaunch with ₺5K/wk budget (if viable) OR reallocate to Pmax | Growth | ⏳ |
| Day 7–21 | Monitor relaunch: kill if CPI > ₺500 after 2 weeks | Growth | ⏳ |
| Day 21 | **Final verdict:** Scale, maintain, or permanently kill | Alp | ⏳ |

### Decision Tree

```
PAUSE NOW
    │
    ├── Diagnostics show ZERO value (no web conversions, no re-engagements, no assisted conversions)
    │       → KILL permanently
    │       → Reallocate 100% of budget to Pmax
    │
    ├── Diagnostics show SOME value (web conversions exist, or re-engagements tracked)
    │       → Fix conversion action + audience exclusions
    │       → Relaunch at ₺5K/wk with 2-week trial
    │           ├── CPI < ₺500 → KEEP, optimize further
    │           └── CPI > ₺500 → KILL, reallocate to Pmax
    │
    └── Diagnostics show campaign was assisting other campaigns (attribution assist)
            → Consider keeping at ₺2K/wk as awareness layer
            → Only if assisted conversion value > spend
```

---

## Appendix: Why This Wasn't Caught Earlier

This campaign has been running since **October 24, 2025** — approximately 5 months. At ~₺19,620/week, the estimated total waste is **₺392,400 (~$11,200)** if the spend rate was consistent.

**Why it wasn't flagged:**
1. Campaign-level install attribution wasn't being monitored weekly
2. Demand Gen campaigns often report "engagement" metrics (clicks, impressions) that look healthy — 1,627 clicks/week appears active
3. Spend was likely buried in aggregate "Google Ads" line items in budget reports
4. No automated alert for "high spend + zero conversions" campaigns

**Prevention going forward:**
- Weekly automated check: any campaign with spend > ₺5,000 and 0 installs → auto-alert
- Monthly campaign-level ROI review (not just channel-level)
- Set up Google Ads automated rules: pause any campaign with spend > ₺10,000 and conversions = 0 in 7 days

---

*Sprint 059 | Fix Plan | 2026-03-21*


---

> ⚠️ **Attribution caveat:** Web campaigns (Meta/Google → cenoa.com → app store) may appear as "Organic" or "(none)" due to broken web→app attribution. Estimated correction factor: ~6.9×. See [attribution-reconciliation.md](attribution-reconciliation.md) for details.
