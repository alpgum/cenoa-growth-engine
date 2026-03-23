# Pakistan Funnel Analysis — Mar 14–20, 2026

**Period:** March 14–20, 2026  
**Sources:** Amplitude Segmentation API (country breakdown)

---

## Pakistan Funnel (This Week)

| Stage | Volume | % of Global | Conversion from Prior |
|---|---:|---:|---:|
| **Install** | 23 | 1.6% (of 1,440) | — |
| **Sign-up** | 15 | 3.3% (of 453 attributed) | **65.2%** (Install→Signup) |
| **KYC Started** | 17 | 0.6% (of 3,050) | — ¹ |
| **KYC Submit** | **0** | 0% (of 179) | 🚨 **0.0%** (KYC Started→Submit) |
| **Deposit** | 0 | 0% (of 1,531) | — |
| **Withdrawal** | 0 | 0% (of 2,220) | — |

¹ KYC Started includes returning users; still, the volume is tiny.

---

## Interpretation

Pakistan volume is extremely low (23 installs/week). This looks like one of:

1. **Pre-launch / low investment market** (no meaningful paid spend)
2. **Geo exposure via organic spillover** (users finding the app incidentally)
3. **Tracking artifact** (few users attributed to PK, many might be (none))

However, **the KYC completion outcome is unambiguous:**

- 17 KYC Started
- 0 KYC Submit

So even at low volume, the funnel is **blocked at KYC**, consistent with Nigeria and Egypt.

---

## Key Takeaways

### ✅ Install→Signup conversion is decent (65%)
- Suggests initial onboarding might be acceptable for users who do install

### 🚨 KYC is a hard stop
- If Pakistan were to be scaled, KYC must support Pakistani CNIC / passport flows

### ❌ No deposits or withdrawals
- Either the user base is too small, or the product is unusable without KYC

---

## Recommendations

1. **Do not allocate budget to Pakistan yet** — too low signal and KYC is blocked
2. **Confirm KYC provider support for Pakistan** (CNIC, passport) before any scaling tests
3. If Pakistan is a strategic market:
   - Run a small controlled acquisition test only after KYC is confirmed working
   - Add PK-specific localization and payment rails validation

---

## What success looks like

At minimum, Pakistan should show **non-zero KYC submits**. Even 1–2 submits/week would confirm the funnel is unblocked.

---

*Pakistan is currently a low-priority market from a performance marketing perspective until KYC support is confirmed.*
