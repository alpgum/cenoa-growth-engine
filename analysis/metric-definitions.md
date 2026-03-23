# Canonical Metric Definitions

**Project:** Cenoa Performance Marketing
**Status:** Approved by Alp (March 2026)
**Reference:** See [data-dictionary.md](data-dictionary.md) for full implementation details, source-of-truth priorities, and caveats.

---

## ⚠️ Critical: CAC Terminology

There are **two distinct cost metrics** in use. Every report **must** specify which one it uses.

### Cost per Virtual Account Opened (NOT true CAC)

```
Cost per Virtual Account Opened = Total Spend / Virtual Account Opened (unique users)
```

- Often casually called "CAC" in funnel reports — **this is misleading**
- Measures cost to acquire a user who opens a virtual account
- Does NOT indicate the user is truly "active" (no transaction required)
- **Usage:** Funnel reports may show this metric but **must label it "Cost per Virtual Account Opened (not true CAC)"**

### Cost per New Active — TRUE CAC ✅

```
Cost per New Active (TRUE CAC) = Total Spend / New Active (unique users with first withdrawal)
```

- This is the **real Customer Acquisition Cost**
- "New Active" = user who completes their **first withdrawal** (the activation event)
- **Usage:** All exec reports, board decks, and strategic planning **must** use this definition
- This is the metric that matters for unit economics and LTV/CAC ratio

---

## Funnel Event Definitions

### Install
- **Definition:** First app install on a device, attributed by AppsFlyer (deduped per AppsFlyer rules)
- **Amplitude event:** `[AppsFlyer] Install`
- **Primary source:** BigQuery (AppsFlyer-derived) or AppsFlyer dashboard

### Signup
- **Definition:** User successfully creates an account (first-time signup completion)
- **Amplitude event:** `Cenoa sign-up completed`
- **Count method:** Unique users

### KYC Started
- **Definition:** User initiates the KYC process
- **Amplitude event:** `KYC Started`
- **Caveat:** Not cohort-pure — returning users can restart KYC. Do not compare directly to installs without cohorting.

### KYC Shown
- **Definition:** KYC provider UI component is rendered for the user
- **Amplitude event:** `Bridgexyz KYC Component Shown`
- **Caveat:** Can be 0 even when KYC Started > 0 if gating happens before the widget (observed in NG/EG).

### KYC Submit
- **Definition:** User clicks submit on the KYC provider component
- **Amplitude event:** `Bridgexyz KYC Component: Submit clicked`
- **Caveat:** Submit clicked ≠ approved. This is a submission attempt, not KYC approval.

### Virtual Account Opened
- **Definition:** User successfully opens/creates a virtual account (product milestone)
- **Amplitude event:** `Virtual account opened`
- **Count method:** Unique users

### Deposit
- **Definition:** A successful deposit transaction (money in)
- **Amplitude event:** `Deposit Completed`
- **Caveat:** Includes returning users — not a pure conversion step from same-period installs.

### Withdrawal
- **Definition:** A successful withdrawal transaction (money out)
- **Amplitude event:** `Withdraw Completed`
- **Caveat:** Strong returning-user contamination. Use cohorting for install→withdraw analysis.

### New Active
- **Definition:** A newly acquired user who completes their **first withdrawal** (activation event)
- **Measurement:** Unique users whose first successful withdrawal occurs within 30 days of signup
- **This is the denominator for TRUE CAC**
- **Caveat:** Legacy Sheets definitions (`new_active`, `paid_active`) disagree materially — do not mix without explicit mapping.

### DAU (Daily Active Users)
- **Definition:** Unique users who open the app on a given day
- **Source:** Amplitude (active users metric)
- **Caveat:** This is an engagement metric, not a funnel step. Do not use as a conversion denominator.

---

## Reporting Rules

1. **Every report must state which CAC definition it uses** — no ambiguity
2. **Exec reports** → Cost per New Active (TRUE CAC)
3. **Funnel reports** → May show Cost per Virtual Account Opened, but must label: *"Cost per Virtual Account Opened — not true CAC"*
4. **Conversion rates** → Always use unique users (not event totals)
5. **Channel breakdowns** → If >(30-40%) of signups/withdrawals are `(none)` source, label tables as *"directional only"*
6. **Spend numerator** → Label explicitly: `spend_realized` (Budget Tracking) vs `spend_attributed` (CAC Analysis)
