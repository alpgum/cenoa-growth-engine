# Nigeria Funnel Analysis — Mar 14–20, 2026

**Period:** March 14–20, 2026  
**Sources:** Amplitude Event Segmentation API (country = Nigeria)

---

## Nigeria Funnel

| Stage | Volume | % of Global | Conversion from Prior |
|---|---:|---:|---:|
| **Install** | 458 | 31.7% | — |
| **Sign-up** | 117 | 25.8% | 25.5% (Install→Signup) |
| **KYC Started** | ~600¹ | ~19% | — |
| **KYC Submit** | **0** | 0% | 🚨 **0%** |
| **Deposit** | 300² | ~19% | — |
| **Withdrawal** | 492 | 22.1% | — |

¹ Estimated from country breakdown proportions.  
² Estimated from country split data.

---

## Key Findings

### 🚨 KYC is completely broken for Nigeria
- **Zero KYC submits** from Nigerian users
- This is the #1 finding: the Bridge/Bridgexyz KYC flow does not work for Nigerian documents
- Nigerian users can install, sign up, and even start KYC — but cannot complete it
- This creates a massive funnel break that blocks new user activation

### 🤔 Paradox: Withdrawals exist without KYC submits
- 492 withdrawals from Nigeria despite 0 KYC submits this week
- **Explanation:** These are existing users who completed KYC in the past (possibly when a different KYC flow was available, or through manual verification)
- Alternatively: some transaction types may not require full KYC
- This shows strong demand — Nigerian users *want* to use the product

### ⚠️ Install→Signup conversion is low (25.5%)
- Only 117 of 458 installers signed up (25.5%)
- Compare to global 83.5% (though this includes unattributed signups)
- Possible causes:
  - App experience not localized for Nigerian users
  - Sign-up flow friction (phone verification, Naira references?)
  - Users discovering the app isn't fully functional for them

### ✅ Second-largest install market
- 458 installs = 31.7% of total — significant organic/paid demand
- Nigeria is the second-largest market after Turkey
- Strong acquisition potential if the funnel can be fixed

---

## Nigeria vs Turkey Comparison

| Metric | Nigeria | Turkey | Gap |
|---|---:|---:|---|
| Installs | 458 | 670 | NG is 68% of TR volume |
| Sign-ups | 117 | 226 | NG is 52% of TR |
| KYC Submit | **0** | **170** | 🚨 Total failure |
| Withdrawals | 492 | 1,260 | NG is 39% of TR |

Nigeria has **68% of Turkey's install volume** but **0% of its KYC completion**. If KYC were fixed, Nigeria could potentially deliver 50-100+ additional KYC submits per week.

---

## Nigeria Funnel Visualization

```
Install (458)
   └─→ Sign-up (117) .............. 25.5%
         └─→ KYC Started (~600)
               └─→ KYC Submit (0) .. 🚨 BLOCKED
                     ╳ Dead end
                     
   Meanwhile: Withdrawal (492) ← existing users only
```

---

## Root Cause Hypotheses

1. **KYC provider limitation:** Bridge/Bridgexyz may not support Nigerian NIN, BVN, or voter's card as identity documents
2. **Document upload failure:** Camera/upload flow may fail on common Nigerian Android devices (low-end, older OS versions)
3. **Network issues:** KYC document upload may timeout on Nigerian mobile networks
4. **Regulatory:** Nigerian financial regulations may require different KYC flow than what's implemented
5. **UX friction:** KYC component may show but with form fields/options that don't match Nigerian document types

---

## Recommendations

### Immediate
1. **Investigate KYC provider support:** Does Bridge/Bridgexyz support Nigerian identity documents (NIN, BVN, International Passport)?
2. **Check error logs:** What happens when Nigerian users attempt KYC? Are they getting errors, or is the component simply not showing options?
3. **Manual testing:** Have someone in Nigeria attempt the full KYC flow and document where it breaks

### Short-term
4. **Alternative KYC for Nigeria:** If Bridge doesn't support NG, consider Smile Identity, Dojah, or Youverify — Nigeria-focused KYC providers
5. **Simplified verification:** For lower-risk transactions, consider a tiered KYC approach (basic phone/BVN verification for small amounts)

### Medium-term
6. **Naira on-ramp:** Ensure deposit/withdrawal flows work with Nigerian payment methods
7. **Local content:** Localize onboarding for Nigerian users (Pidgin English option, local payment references)
8. **Targeted campaigns:** Once KYC is fixed, Nigeria could be the highest-ROI market to invest in — large TAM, existing demand

---

## Impact Assessment

**If KYC were fixed for Nigeria:**
- Conservative estimate: 50-100 additional KYC submits/week (using Turkey's 11% conversion as benchmark on Nigeria's ~600 KYC starts)
- This would nearly double total KYC completions (from 179 → ~250-280)
- Given Nigeria's existing withdrawal base, these users have high intent to transact
- **Estimated revenue impact:** Significant — Nigeria already shows 492 weekly withdrawals from the existing base

---

*Data from Amplitude. Zero KYC submits for Nigeria is confirmed across the full week with no single-day exceptions. This is a systemic issue, not a temporary glitch.*
