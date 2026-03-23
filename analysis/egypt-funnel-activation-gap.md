# Egypt Funnel + Activation Gap Analysis — Mar 14–20, 2026

**Period:** March 14–20, 2026  
**Primary sources:** Amplitude Segmentation (country breakdown), Google Sheets (CAC Analysis, Trafik Canavarı export)  
**Created:** 2026-03-21

---

## Executive summary

- Egypt is a **high-volume acquisition market** (≈14% of installs) with **very cheap CAC** vs Turkey.
- Egypt shows **strong intent to complete KYC** (almost all signups start KYC).
- **CRITICAL:** Egypt has **0 KYC submissions** (same for Nigeria) → strongly suggests **BridgeXYZ KYC is unavailable/broken** for EG (or non-TR generally).
- Despite 0 KYC submits, Egypt shows **~23 deposits and ~23 withdrawals** in the same week → these events are likely **returning/legacy users** or a **non-KYC transaction path**.
- Immediate priority: **verify Bridge KYC country support + identify where EG KYC flow fails**, before scaling spend.

---

## 1) Egypt funnel

### A) Funnel snapshot (task brief / working numbers)

```
Install (197) → Signup (61) → KYC Start (?) → KYC Submit (0!) → Deposit (23) → Withdrawal (23)
```

### B) Amplitude event totals by country (Mar 14–20)

```
Install (206) → Signup (64) → KYC Started (62) → KYC Submit (0!) → Deposit (22) → Withdrawal (23)
```

Notes:
- Small deltas (197 vs 206, 61 vs 64, 22 vs 23) are likely due to **time window alignment**, **attribution gaps**, or **event definition differences**.
- Deposits/withdrawals are **not cohort-pure** (they include returning users).

**Derived intent signal (Amplitude):**
- Signup → KYC Started: **62 / 64 = 96.9%** (Egypt users try to KYC almost immediately).

---

## 2) CRITICAL: Zero KYC submissions from Egypt

Egypt has **KYC Started = 62** but **KYC Submit = 0**.

This does not look like “low conversion.” It looks like a **hard block**.

**Evidence from country breakdown:**
- The KYC submit event (“**Bridgexyz KYC Component: Submit clicked**”) occurred in only **7 countries** total:
  - Turkey (170), Germany (3), Spain (2), Georgia (1), Montenegro (1), Poland (1), Thailand (1)
- **Egypt and Nigeria are completely absent** from KYC submit, despite substantial installs and KYC starts.

**Most likely explanation:** BridgeXYZ KYC is **not available / not supported / broken** for Egyptian documents or Egypt jurisdiction.

---

## 3) Paradox: deposits + withdrawals exist despite 0 KYC submits

Same week signals:
- **0 KYC submits** (new-user KYC completion blocked)
- Yet **~22–23 deposits** and **23 withdrawals** attributed to Egypt

This likely means deposits/withdrawals are coming from:

1) **Legacy users** who completed KYC in the past (or under a different KYC provider)  
2) **Different transaction path** that doesn’t require KYC (e.g., on-chain crypto deposit/withdraw)  
3) **Country attribution mismatch** (VPN, travel, device locale)  
4) **KYC required only for some rails** (fiat rails KYC-gated, crypto not)

**What to check immediately (high signal, low effort):**
- Pull the **user list** behind those 23 Egypt withdrawals and answer:
  - When was the user created? (new vs old)
  - Do they have verified KYC status already?
  - Which deposit/withdraw methods did they use?

---

## 4) Egypt LTV test + LP test results (from Sheets)

> Limitation: The exported “Trafik Canavarı” file accessible here only contained a “TR Only” tab. The task brief references Egypt tabs (“Egypt LTV Test”, “LP tests”) that were not accessible in the export; below is captured from the task brief.

Key results to carry forward:
- **KYC follow-up messaging → 450% better CVR**
- **Architect landing page → 27% cheaper CTA**

Interpretation:
- These are strong demand/intent signals: **Egypt users respond to activation nudges and better landing pages**.
- That increases confidence that the **binding constraint is KYC availability/UX**, not lack of interest.

---

## 5) Egypt CAC is 5–10× cheaper than Turkey

From CAC Analysis (March 2026):

- **Egypt cost per virtual account:** **$8**  
- **Turkey cost per virtual account:** **$35**  
- Egypt is ~**4.4× cheaper** on this metric (and typically framed as 5–10× depending on segment/week).

Egypt spend context (1–15 March):
- Total spend: **$13,373**
- Egypt spend: **$5,549** (**41.5%**) → large budget share flowing into a funnel currently blocked at KYC.

Implication:
- If KYC is fixed, Egypt can be a **major efficiency lever** vs Turkey.

---

## 6) Egypt Meta campaigns performance (what we can infer)

We do not have a full Meta Ads export (CTR/CPC/CPA by campaign) in the currently provided files.

What we *can* state from the available data:
- Egypt is absorbing substantial budget (CAC sheet), and installs are **accelerating** during Mar 14–20.
- Daily Egypt installs (Amplitude export):
  - Mar 14: 21 | Mar 15: 12 | Mar 16: 16 | Mar 17: 17 | Mar 18: 26 | Mar 19: 51 | Mar 20: 63

**Interpretation:** acquisition is working (volume is rising), but **activation is blocked**.

Actionable next step: export Meta performance for Egypt (campaign/adset) to confirm whether the spike is due to **scaling a winning adset** or **broad spend**.

---

## 7) Hypotheses for the activation gap (ranked)

1) **KYC provider limitation (BridgeXYZ not supporting Egypt)**  
   - Best fits the pattern across Egypt + Nigeria.

2) **Regulatory/jurisdiction exclusion**  
   - Bridge (or internal policy) may restrict Egypt for compliance reasons.

3) **KYC UX failure for Arabic / transliteration / field formats**  
   - Could cause drop after “start”, especially if users hit validation errors.

4) **Technical failure (SDK / network / device-specific capture issues)**  
   - Upload timeouts, camera permission issues, OCR failures.

5) **Measurement gap (Submit click event not firing)**  
   - Less likely because we’d expect at least *some* non-TR countries to show up, but still worth verifying with logs.

---

## 8) Recommendations — urgent investigation + quick wins

### Immediate (today / this week)
1) **Confirm BridgeXYZ coverage for Egypt** (hard yes/no): supported documents, supported jurisdictions, expected failure modes.
2) **Run an in-market EG KYC attempt** (real device + Egyptian ID) and screen-record the flow.
3) **Instrument KYC failures** (client + server): emit events for `kyc_error_type`, `kyc_provider_response`, `step_failed` by country.
4) **Audit Egypt deposit/withdraw users** (the 23 withdrawers): are they legacy users? which rails? do they already have KYC?

### Quick wins (1–2 weeks)
5) If Bridge is not viable for EG: **add an alternative KYC provider** for Egypt (or route EG traffic to a supported flow).
6) Apply growth levers proven in the brief:
   - **Roll out KYC follow-up** (450% CVR lift) as a standard lifecycle sequence.
   - Use **Architect LP** as default for Egypt (27% cheaper CTA).
7) **Arabic localization pass** for onboarding + KYC (RTL, names, address, error copy).

### Budget policy
8) **Do not scale Egypt acquisition aggressively until KYC is unblocked**. Keep spend capped to:
   - maintain learning velocity,
   - validate follow-up/LP tests,
   - avoid burning budget into a blocked funnel.

---

## Open questions (to resolve fast)

- Is **KYC required** for *all* deposit/withdraw rails, or only fiat rails?
- Are the 23 Egypt withdrawals from **new users or returning users**?
- What exact screen / step do Egyptian users drop at in the Bridge KYC flow?

---

*Bottom line: Egypt is an efficiency goldmine on CAC, but currently a broken activation funnel due to KYC completion = 0. Fix KYC first, then scale.*
