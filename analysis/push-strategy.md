# Push Notification Strategy — Cenoa (Lifecycle + Templates)

**Scope:** Lifecycle push notifications aligned to the core funnel: **install → signup → KYC → deposit → withdraw**.

**Principle:** Push is a *nudge*, not a stressor. We optimize for **clarity + trust + next best action** and avoid anxiety-driven language.

---

## 1) Lifecycle stages aligned to the funnel

> Each stage has (a) *goal*, (b) *primary user friction*, (c) *push role*, (d) *success metric*.

### Stage A — Install → Signup (Activation)
- **Goal:** Turn installs into completed signups.
- **Friction:** App opened once; user unsure of value / busy.
- **Push role:** Remind benefits + one-tap deep link back to signup.
- **Success metric:** `signup_completed` per install (and push-assisted lift).

### Stage B — Signup → KYC start/submit/approve (Compliance activation)
- **Goal:** Move users to KYC completion.
- **Friction:** Document/selfie hassle, uncertainty about why KYC is needed.
- **Push role:** Explain *why* in 1 line, highlight “takes ~2 minutes”, offer help.
- **Success metric:** `kyc_submitted`, `kyc_approved` per signup.

### Stage C — KYC approved → First deposit (Value realization)
- **Goal:** First successful deposit.
- **Friction:** Choice overload (method), trust, fees/FX confusion.
- **Push role:** “You’re ready” confirmation + simplest path + reassurance.
- **Success metric:** `deposit_success` per `kyc_approved`.

### Stage D — Deposit → First “aha” action (Retention bridge)
- **Goal:** Users actually *use* the wallet (save, pay, transfer).
- **Friction:** Money sits idle; user hasn’t formed habit.
- **Push role:** Contextual: rate/fee transparency, reminders tied to intent.
- **Success metric:** repeat deposits, transfer/pay usage (if available).

### Stage E — Withdraw (Core value + trust loop)
- **Goal:** Make withdrawal feel fast, safe, and predictable.
- **Friction:** “Will it work?” anxiety; users want status updates.
- **Push role:** Status updates + confirmation + next best action (referrals / repeat behavior).
- **Success metric:** `withdrawal_success`, NPS/CSAT (if tracked), referral actions.

---

## 2) Push permission & onboarding strategy (when to ask)

- **Don’t ask on first launch.** Ask only after the user experiences value/intent.
- Best moments to prompt OS permission:
  1) After signup completion (“Want status updates for verification & transfers?”)
  2) When KYC starts (“Get notified when you’re approved.”)
  3) When a deposit/withdraw is initiated (“Get real-time status updates.”)
- **Copy rules for permission prompt:**
  - Be specific: “verification updates”, “deposit status”, “withdrawal status”.
  - Offer a clear benefit + control: “You can change this anytime in Settings.”

---

## 3) 12 push templates (title/body) with timing + trigger

**Formatting constraints:**
- Title: ~25–40 chars (varies by OS)
- Body: ~60–110 chars; 1 idea; 1 CTA
- Always include a **deep link** to the exact screen.

**Tokenization (optional):** `{first_name}`, `{amount}`, `{currency}`, `{minutes}`.

> Recommended implementation: use a campaign key like `lifecycle_<stage>_<purpose>_v1` to keep measurement clean.

| # | Funnel stage | Trigger (event/condition) | Timing | Title | Body | Deep link | Notes |
|---:|---|---|---|---|---|---|---|
| 1 | Install→Signup | `app_install` AND no `signup_completed` | +2h after install | Finish setting up Cenoa | Create your account in under 1 minute. | `app://signup/start` | Value-forward, no pressure |
| 2 | Install→Signup | No `signup_completed` | +24h after install | Your USD wallet is waiting | Pick up where you left off and unlock transfers. | `app://signup/resume` | Mention core benefit; avoid “miss out” |
| 3 | Signup→KYC | `signup_completed` AND no `kyc_started` | +1h after signup | Verify in ~2 minutes | KYC unlocks deposits & withdrawals. Start now. | `app://kyc/start` | Explain “why” briefly |
| 4 | Signup→KYC | `kyc_started` AND no `kyc_submitted` | +6h after KYC start | Need help finishing KYC? | Snap your ID + a quick selfie to complete verification. | `app://kyc/resume` | Helpful tone; offer support link if possible |
| 5 | KYC pending | `kyc_submitted` AND not approved | +12h after submit (if still pending) | KYC in review | We’ll notify you as soon as it’s approved. | `app://kyc/status` | Status reassurance; no timelines you can’t meet |
| 6 | KYC approved→Deposit | `kyc_approved` AND no `deposit_initiated` | +30m after approval | You’re approved ✅ | Add funds to start saving and sending in USD. | `app://deposit/methods` | First-deposit nudge |
| 7 | Deposit started | `deposit_initiated` AND no `deposit_success` | +2h after initiate | Deposit in progress | Tap to check status or try a different method. | `app://deposit/status` | Reduce support tickets via self-serve |
| 8 | First deposit success | First `deposit_success` | +5m after success | Deposit received | You can now send, save, or withdraw anytime. | `app://home` | “Aha” moment; reinforce control |
| 9 | Pre-withdraw assurance | `balance_available` AND user visited withdraw screen but no `withdrawal_initiated` | +24h after intent | Want to cash out? | Withdraw when you’re ready—see fees and ETA before confirming. | `app://withdraw/start` | Intent-based; avoids pushing withdrawals blindly |
| 10 | Withdrawal started | `withdrawal_initiated` | Instant | Withdrawal started | We’ll update you when it’s completed. | `app://withdraw/status` | Transactional, high-value |
| 11 | Special: post-withdraw referral | First `withdrawal_success` (or any) | +30m after completion | Invite a friend to Cenoa | Share your link—friends who join help you both grow. | `app://referrals` | **Required special**; keep wording neutral (no incentive claims unless true) |
| 12 | Special: “Get paid” reminders | User saved “payday” preference OR recurrent deposit pattern detected | 1–2 days before payday (local time) | Payday reminder | Get paid into Cenoa—share your account details in one tap. | `app://get-paid` | **Required special**; only if feature exists; otherwise link to deposit options |

**Implementation detail:** template #12 depends on having either:
- a user-set schedule (`payday_day_of_month`, `payday_weekday`) OR
- a heuristic cohort (“usually deposits every ~30 days”) with an opt-out.

---

## 4) Localization notes (TR / NG / EG / PK)

### Baseline localization rules (all countries)
- Keep the **meaning identical**, not word-for-word.
- Avoid idioms; keep sentences short.
- Currency formatting:
  - Use local currency symbol only when the amount is in that currency.
  - For USD: use `USD {amount}` (clear and unambiguous).
- Time formatting: prefer local conventions (TR: 24h; NG/PK often 12h; EG commonly 12h in consumer apps).
- Compliance terminology:
  - Explain KYC once, then use the short term.

### TR (Turkey) — Language: Turkish
- Tone: direct, reassuring, not overly casual.
- KYC: “Kimlik doğrulama” (avoid jargon).
- Example phrasing:
  - “Kimlik doğrulama 2 dk sürer”
  - “Para yatırma/çekme için gerekli”

### NG (Nigeria) — Language: English (and optional Pidgin variant later)
- Tone: friendly, clear; avoid slang in v1.
- Emphasize transparency: “fees & ETA shown before you confirm.”
- Watch-outs: avoid promises around FX rates or transfer speed.

### EG (Egypt) — Language: Arabic (Modern Standard / Egyptian-friendly)
- Keep Arabic short; avoid long formal clauses.
- KYC: “التحقق من الهوية”
- Numerals: consider Arabic-Indic digits only if already used in the app UI.
- RTL layout: keep placeholders `{amount}` tested in RTL.

### PK (Pakistan) — Language: Urdu (plus English fallback)
- Keep Urdu simple; avoid heavy Persianized vocabulary.
- KYC: “شناخت کی تصدیق”
- Sensitivities: avoid any implication of “interest/return” unless fully compliant/legal.

**Operational recommendation:**
- Ship **EN + TR** first if product supports; add **AR (EG)** and **UR (PK)** with professional translation + in-app QA.

---

## 5) Frequency caps, quiet hours, and safety rules

### Frequency caps (recommended starting point)
**Global caps (per user):**
- Max **2 lifecycle pushes / day** (excluding mandatory transactional updates)
- Max **5 lifecycle pushes / week**
- Minimum **6 hours** between non-transactional pushes

**Transactional pushes (status updates):**
- Allowed as-needed for `deposit_*` / `withdraw_*` / `kyc_*` status, but:
  - dedupe repeated states (don’t spam “in review”)
  - cap to **1 per state change**

**Stage caps (per funnel stage per user):**
- Install→Signup: max 2 nudges total (then stop)
- Signup→KYC: max 3 nudges total (then stop)
- KYC approved→Deposit: max 2 nudges total

### Quiet hours
- Default: **21:00–09:00 local time** (user timezone inferred from device)
- Exceptions: **critical transactional** updates (withdrawal completed) can pass quiet hours if policy allows; otherwise delay to 09:00.

### Safety & compliance rules (copy + segmentation)
**Avoid financial-anxiety phrasing.** Do NOT use:
- “Don’t lose money”, “Your money is at risk”, “Act now”, “Last chance”, “Urgent”
- Shame language: “You still haven’t…”, “Why didn’t you…”

**Use neutral, empowering phrasing:**
- “When you’re ready…”, “Tap to continue…”, “Check status…”, “You’re in control…”

**Sensitive segmentation guardrails:**
- If user experienced KYC rejection: use support/help content, not pressure.
- If user has 0 balance: don’t push withdrawals.
- If user disabled notifications: stop and rely on in-app banners/email.

---

## 6) Measurement plan (Amplitude)

### Event instrumentation (minimum viable)
Track the full push funnel with consistent naming and properties.

**Events (recommended):**
- `push_sent`
- `push_delivered` (if available)
- `push_opened`
- `push_clicked` (deep link tapped)
- `push_dismissed` (optional)
- Downstream: `signup_completed`, `kyc_started`, `kyc_submitted`, `kyc_approved`, `deposit_initiated`, `deposit_success`, `withdrawal_initiated`, `withdrawal_success`, `referral_link_shared`, `referral_signup_completed` (or equivalent)

**Core properties (attach to all push events):**
- `campaign_id` (e.g., `lifecycle_signup_nudge_v1`)
- `message_id` (unique per send)
- `stage` (install_signup / signup_kyc / kyc_deposit / withdraw / referrals)
- `variant` (A/B identifier)
- `country`, `language`
- `platform` (ios/android)
- `timezone`
- `permission_status` (authorized/provisional/denied)

### Metrics definitions
- **Open rate:** `push_opened / push_delivered` (or `/ push_sent` if delivered unavailable)
- **Click rate (deep link CTR):** `push_clicked / push_opened`
- **Push-to-action rate (primary):** downstream conversion within attribution window
  - Example: Signup push → `signup_completed` within **24h** of `push_opened`

### Attribution windows (starting defaults)
- Activation nudges (signup/KYC/deposit): **24h post-open** (plus a sensitivity check at 7d)
- Transactional status: measure **support deflection** (fewer “where is my money” tickets) if available
- Referral push: **72h post-open** to `referral_link_shared` and **14d** to `referral_signup_completed`

### Reporting views
In Amplitude, build:
1) **Lifecycle push funnel dashboard** (sent → opened → clicked → downstream event)
2) **Stage cohort**: users eligible for a push vs those who received it (holdout recommended)
3) **Geo/language breakdown**: TR/NG/EG/PK performance, plus OS differences

**Holdout best practice:** maintain a persistent **5–10% no-push control** per stage to quantify true incrementality.

---

## 7) A/B test plan for the top 3 pushes

> Focus on the biggest funnel drop-offs: **signup completion**, **KYC completion**, **first deposit**.

### Test 1 — Push #2 (Install→Signup, +24h)
- **Hypothesis:** Benefit-led copy beats reminder-led copy.
- **Audience:** installed but not signed up; exclude users who disabled notifications.
- **Variants:**
  - **A (Control):** “Your USD wallet is waiting”
  - **B:** “Open your USD wallet in 1 minute”
  - **C:** “Track deposits & withdrawals with instant updates”
- **Primary metric:** `signup_completed` within 24h of open
- **Secondary:** open rate, click rate
- **Guardrails:** uninstall rate, notification opt-out rate

### Test 2 — Push #4 (KYC started but not submitted, +6h)
- **Hypothesis:** “Help + reduce effort” message beats compliance framing.
- **Variants:**
  - **A (Control):** “Need help finishing KYC?” + generic steps
  - **B:** “Finish in 2 minutes” + reassurance (“Your data is protected” if true)
  - **C:** “Resume where you left off” + explicit CTA
- **Primary metric:** `kyc_submitted` within 24h of open
- **Guardrails:** `kyc_rejected` rate (if tracked), support contacts

### Test 3 — Push #6 (KYC approved→Deposit, +30m)
- **Hypothesis:** “You’re approved” + single next step beats broader benefit list.
- **Variants:**
  - **A (Control):** “Add funds to start saving and sending in USD.”
  - **B:** “Make your first deposit now (fees shown upfront).”
  - **C:** “Choose the easiest deposit method for you.”
- **Primary metric:** `deposit_success` within 72h
- **Guardrails:** deposit failure rate, refund/chargeback signals (if any)

**Experiment mechanics (all tests):**
- Randomize at **user-level**, persist assignment.
- Minimum runtime: **14 days** (weekday/weekend).
- Ensure caps still apply (avoid treatment over-sending).

---

## Appendix — Operational checklist

- [ ] Campaign keys, variants, and deep links defined
- [ ] Eligibility queries validated per stage
- [ ] Quiet hours per timezone implemented
- [ ] Global & stage frequency caps enforced server-side
- [ ] Amplitude events firing with required properties
- [ ] 5–10% holdout set per stage
- [ ] Localization QA on small devices + RTL (Arabic)
