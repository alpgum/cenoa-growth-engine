# CRM Lifecycle Email Strategy (Cenoa)

**Goal:** increase activation + monetization by moving users through the core lifecycle.

**Lifecycle (required):** new install → signup → KYC started → KYC submit → first deposit → first withdrawal → power user

**Key constraints from current funnel:**
- Install → Signup is strong (≈83%).
- KYC completion is the main bottleneck (KYC Started → KYC Submit clicked ≈5.8% overall; largely TR-only).
- Web/none platform produces most signups but converts poorly downstream; email + deep links should focus on web→app handoff.

> **Important assumption:** email address is reliably available starting at **Signup**. For the **New install** stage, emails only work if you collect email earlier (web lead, pre-signup step, "continue with email" before account creation). If not, replicate the same messaging via push/in-app.

---

## 1) Stage model: triggers, entry/exit, suppression

### Trigger events (Amplitude naming used in current analysis)
| Lifecycle stage | Entry condition (trigger) | Exit / suppression condition |
|---|---|---|
| New install | `[AppsFlyer] Install` (or `Application first opened`) **AND** email known | `Cenoa sign-up completed` |
| Signup | `Cenoa sign-up completed` | `KYC Started` (or `KYC Submit clicked`) |
| KYC started | `KYC Started` | `KYC Submit clicked` |
| KYC submit | `KYC Submit clicked` | `Deposit Completed` |
| First deposit | first-ever `Deposit Completed` | `Withdraw Completed` |
| First withdrawal | first-ever `Withdraw Completed` | Power user definition met |
| Power user | see definition below | churn / inactivity definition (optional) |

### Power user definition (pick one, then stick to it)
- **Behavioral:** ≥3 `Withdraw Completed` in last 30 days **OR** ≥2 `Deposit Completed` + ≥2 `Withdraw Completed` in last 30 days.
- **Cadence:** weekly active (any core event) ≥4 of last 6 weeks.
- **Value:** total withdrawal volume ≥$X within 30 days (requires amount property).

### Frequency caps (global)
- **Max 1 lifecycle email / day** per user.
- **Max 3 lifecycle emails / 7 days** per user.
- **Quiet hours:** local time 21:00–08:00.
- **Suppression:** as soon as user hits next stage, stop remaining emails in the prior stage.

---

## 2) Email sequences per stage (timing, subject lines, key message, CTA)

Below are **recommended default sequences**. Keep them short, punchy, and stage-specific; avoid “everything in one email.”

### A) Stage: New install (pre-signup)
**Audience:** installers/first-openers where email is known (web lead capture, incomplete signup with email).

| Email | Timing | Subject line (examples) | Key message (what to say) | Primary CTA |
|---:|---|---|---|---|
| A1 | +15 min from install/first open | “Your USD account is 2 minutes away” / “Finish setup in 2 minutes” | 1) What Cenoa does in one sentence (get paid globally → withdraw locally). 2) Set expectation: signup is quick. | **Complete sign up** (deep link to signup) |
| A2 | +24h if no signup | “Need help getting started?” / “Most freelancers start here” | 1) 3-step checklist: Sign up → Verify ID → Get paid/withdraw. 2) Offer help + support link. | **Continue setup** |
| A3 | +72h if no signup | “Don’t lose your progress” / “Your account is waiting” | 1) Light urgency. 2) Social proof (country-specific if possible). | **Open Cenoa** |

**Notes:** if you cannot collect email pre-signup, shift these to push notifications + in-app banners.

---

### B) Stage: Signup (no KYC started yet)
**Audience:** `Cenoa sign-up completed` users who have not triggered `KYC Started`.

| Email | Timing | Subject line (examples) | Key message | Primary CTA |
|---:|---|---|---|---|
| B1 | +10 min from signup | “Welcome — next step: verify your account” / “Get ready to receive USD” | 1) Welcome + promise. 2) Explain why KYC unlocks limits/withdrawals (trust + compliance). 3) “Takes ~5 minutes.” | **Start verification (KYC)** |
| B2 | +24h if no KYC started | “Verification takes 5 minutes (here’s what you’ll need)” | 1) Document checklist (country-specific). 2) Tips to avoid rejection (good lighting, exact name). | **Start KYC** |
| B3 | +72h if no KYC started | “Stuck? We can help you finish verification” | 1) Troubleshooting bullets. 2) Route to support if KYC provider coverage is an issue. | **Contact support / Retry KYC** |

---

### C) Stage: KYC started (not submitted)
**Audience:** `KYC Started` but no `KYC Submit clicked`.

| Email | Timing | Subject line (examples) | Key message | Primary CTA |
|---:|---|---|---|---|
| C1 | +1h after KYC start | “Finish verification to unlock withdrawals” / “You’re almost verified” | 1) Reinforce benefit (withdrawals, higher limits, faster support). 2) Re-open the exact step via deep link. | **Continue verification** |
| C2 | +24h | “Common verification issues (quick fixes)” | 1) Photo tips. 2) Name mismatch / expired ID / glare. 3) If country coverage limited: acknowledge + offer workaround path. | **Continue KYC** |
| C3 | +48h | “Can we help you get verified today?” | 1) Human help angle. 2) Provide support chat + FAQ. | **Get help** |

**Country nuance:** because KYC submit is near-zero in NG/EG right now, C3 should include a **country-detection fallback** (“If your documents aren’t supported yet, reply to this email / contact support; we’ll guide you”).

---

### D) Stage: KYC submit (no deposit yet)
**Audience:** `KYC Submit clicked` but no `Deposit Completed`.

| Email | Timing | Subject line (examples) | Key message | Primary CTA |
|---:|---|---|---|---|
| D1 | +15 min | “Verification received — next: add money” / “You’re verified. Fund your account” | 1) Confirm KYC submission/receipt. 2) Clear next action: make first deposit to enable use cases. 3) Safety/trust (regulated partners, security). | **Make a deposit** |
| D2 | +24h if no deposit | “Best first deposit method for your country” | 1) Country-specific rails and expected time/fees. 2) Small “start with $X” suggestion (if allowed). | **Deposit now** |
| D3 | +72h | “What you can do with Cenoa (in 3 examples)” | 1) Receive USD from clients. 2) Convert at good rates. 3) Withdraw to local bank/card. | **Fund your account** |

---

### E) Stage: First deposit (no withdrawal yet)
**Audience:** first-ever `Deposit Completed`, but no `Withdraw Completed`.

| Email | Timing | Subject line (examples) | Key message | Primary CTA |
|---:|---|---|---|---|
| E1 | +30 min after first deposit | “Deposit successful — withdraw your earnings” / “You’re ready to withdraw” | 1) Confirm deposit succeeded. 2) Show the simplest next step: withdraw to local bank/card. 3) Set expectation: typical processing times. | **Make first withdrawal** |
| E2 | +48h if no withdrawal | “How to withdraw (step-by-step)” | 1) Simple steps + screenshot/GIF placeholders. 2) Encourage first withdrawal as activation moment. | **Withdraw now** |
| E3 | +5 days | “Save money on every payout (fees comparison)” | 1) Re-state main economic benefit vs alternatives. 2) Provide comparison link/landing page. | **Withdraw with Cenoa** |

---

### F) Stage: First withdrawal (activation + referral moment)
**Audience:** first-ever `Withdraw Completed`.

| Email | Timing | Subject line (examples) | Key message | Primary CTA |
|---:|---|---|---|---|
| F1 | +15 min after first withdrawal | “Your withdrawal is complete” / “✅ Payout received” | 1) Celebrate success (this is the “aha”). 2) Set expectation for next withdrawals (faster, saved method). 3) Introduce next best action: set up recurring withdrawals or add another currency. | **Set up next withdrawal / Open app** |
| F2 (Referral) | +2–6 hours after F1 (same day) | “Invite a friend who gets paid in USD” / “Earn rewards when friends withdraw” | 1) Referral framing tied to freelancer reality. 2) Clear reward mechanics (keep generic if unknown): “You both get X after they complete Y.” 3) Emphasize share link/code. | **Invite friends (get referral link)** |
| F3 | +7 days | “Pro tips for faster payouts” / “Make Cenoa your payout hub” | 1) Power-user habits: saved beneficiaries, payout schedule, multi-currency. 2) Optional: card waitlist. | **Enable pro setup** |

**Referral moment rule:** do not ask for referral **before** first withdrawal. The emotional peak is right after the user proves value.

---

### G) Stage: Power user (retention, trust, expansion)
**Audience:** users meeting the power user definition.

| Email | Timing | Subject line (examples) | Key message | Primary CTA |
|---:|---|---|---|---|
| G1 | Upon entering power user cohort | “You’re a power user — unlock more” / “Thanks for trusting Cenoa” | 1) Gratitude + status. 2) Benefits: higher limits, priority support, early access. | **Explore advanced features** |
| G2 | 14 days later | “Lower fees, better FX: optimize your payouts” | 1) Best practices + settings. 2) Encourage consolidating more income sources. | **Set payout preferences** |
| G3 | Monthly (if still active) | “What’s new in Cenoa” | 1) Product updates. 2) Trust-building (security, partners). 3) Keep short. | **See updates** |

---

## 3) Country localization notes (TR / NG / EG / PK)

### Language recommendations
- **TR (Turkey):** Turkish by default. Optional bilingual TR+EN for high-income freelancer segment.
- **NG (Nigeria):** English default; keep copy simple, direct, benefit-led. Avoid heavy jargon.
- **EG (Egypt):** Arabic recommended for conversion; optionally English toggle for tech/freelancer segment.
- **PK (Pakistan):** English default; consider Urdu for broader reach in retention emails.

### Content localization (what actually changes)
| Country | Trust triggers | Offer framing | Operational notes |
|---|---|---|---|
| TR | compliance/KVKK, local rails, speed | “Cheaper than Payoneer/Wise” + fast withdrawals | KYC works best today; lean into “verify now.” |
| NG | reliability + support, “USD to local” clarity | “Get paid globally, withdraw locally” (avoid aggressive fee claims) | If KYC coverage is limited: proactively provide support workaround.
|
| EG | trust + legitimacy, clear steps | “Simple steps to receive USD” + peace-of-mind | Arabic UX matters; keep steps very explicit.
|
| PK | trust + clarity, minimize uncertainty | “Receive international payments, withdraw easily” | Consider longer education sequence; reduce pressure tone.

### Practical localization checklist
- Use **local examples** in 1 sentence (e.g., “clients in US/UK,” “monthly invoices,” “freelance platforms”).
- Localize **time/fees** only if numbers are accurate; otherwise keep qualitative.
- Translate CTAs as verbs, not nouns (e.g., TR: “Doğrulamayı Başlat”).
- Avoid deliverability issues with mixed scripts: if using Arabic, keep subject lines short and avoid excessive punctuation.

---

## 4) Primary CTA rules (so emails don’t get mushy)

- 1 email = **1 primary CTA**.
- The CTA must deep link into the exact screen:
  - Signup → `/signup`
  - KYC → `/kyc/start` or `/kyc/resume`
  - Deposit → `/deposit`
  - Withdrawal → `/withdraw`
  - Referral → `/referral`

Secondary links are allowed (FAQ / support), but visually de-emphasized.

---

## 5) Measurement plan (Amplitude): open/click + conversion events

### A) Minimum instrumentation
Track email exposure events in Amplitude (or pipe from your ESP → Amplitude):
- `Email Sent`
- `Email Delivered`
- `Email Opened`
- `Email Clicked`

**Required properties (all 4 events):**
- `email_id` (immutable)
- `stage` (install/signup/kyc_started/kyc_submit/first_deposit/first_withdrawal/power_user)
- `sequence` (A1, B2, etc.)
- `country`
- `language`
- `platform` (if known)
- `utm_campaign`, `utm_content`

### B) Primary conversion events per stage
| Stage email sequence | Success event to attribute | Secondary metrics |
|---|---|---|
| New install | `Cenoa sign-up completed` | time-to-signup, app open |
| Signup | `KYC Started` | `KYC Submit clicked` |
| KYC started | `KYC Submit clicked` | support contact rate, KYC error events (if instrumented) |
| KYC submit | `Deposit Completed` (first) | deposit method started, time-to-deposit |
| First deposit | `Withdraw Completed` (first) | withdrawal method add, time-to-withdraw |
| First withdrawal | `Referral Invite Sent` / `Referral Link Copied` (if exists) | referral clicks, next withdrawal |
| Power user | retention (WAU/MAU), volume | NPS/support tickets, churn |

### C) Attribution windows (practical defaults)
- **Open/click attribution:** 7-day rolling.
- **Stage conversion attribution:** 3-day window for “next step” actions (signup→KYC start; KYC submit→deposit), 7-day for first withdrawal.

### D) Dashboards to build in Amplitude
- Funnel: `Email Delivered` → `Email Clicked` → next-stage event.
- By country + language + platform.
- Holdout test: % of users suppressed from lifecycle emails to estimate incremental lift.

---

## 6) Deliverability + compliance basics

### Deliverability fundamentals
- Authenticate sending domain: **SPF + DKIM + DMARC** (at minimum DMARC p=none initially; later quarantine/reject).
- Use a **dedicated subdomain** for lifecycle (e.g., `mail.cenoa.com`).
- Warm up gradually (especially if you introduce Arabic/TR content).
- Keep image-to-text balanced; avoid link shorteners; use consistent from-name.
- List hygiene: suppress hard bounces; sunset policy for non-openers (e.g., no opens in 90 days → reduce cadence).

### Compliance (baseline)
- Every marketing email must include:
  - **Unsubscribe** link (one-click if possible)
  - physical address / company identity (per ESP defaults)
  - clear reason for receiving (“You’re receiving this because you created a Cenoa account…”)
- **Transactional vs marketing:** some emails (e.g., withdrawal confirmation) are transactional; still include preferences center when possible.
- Respect local regimes (high-level):
  - TR: KVKK consent + data processing disclosure.
  - NG: NDPR principles (consent/legitimate interest + opt-out).
  - EG/PK: follow best-practice consent + opt-out; maintain audit logs.

### User experience rules
- Don’t send lifecycle emails if the user is actively in-session (optionally suppress for 2 hours after app session).
- Avoid sending multiple reminders for the same stuck point without offering **help** (support link / troubleshooting).

---

## 7) Referral tie-in (post-withdrawal) — the “right moment”

**Why post-withdrawal:** the user has just experienced core value (money successfully moved). That’s peak trust + willingness to recommend.

### Recommended referral prompt design
- **In-app first:** show referral card immediately after withdrawal success screen.
- **Email second (F2):** 2–6 hours later, with the same deep link, to capture users who churned after cashout.

### Referral measurement (Amplitude)
Instrument at least:
- `Referral Screen Viewed`
- `Referral Link Copied`
- `Referral Invite Sent`
- `Referred User Signed Up`
- `Referral Reward Earned`

Build a cohort: “first-withdrawal users” → referral actions within 7 days.

---

## Implementation checklist (ops)
- [ ] Confirm when email is captured (pre-signup vs post-signup only)
- [ ] Define power user criteria + thresholds
- [ ] Confirm KYC coverage constraints by country; update C-sequence messaging
- [ ] Create deep links + UTM standard
- [ ] Set up Amplitude taxonomy for email events + referral events
- [ ] Launch with TR first (best KYC completion), then expand with localized variants for NG/EG/PK
