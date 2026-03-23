# Feature Engagement by Country

**Period:** March 14–20, 2026  
**Source:** Amplitude (event totals, grouped by country)

---

## Summary Table

| Feature | Total | #1 Country | #2 Country | #3 Country |
|---------|------:|------------|------------|------------|
| Get Paid Opened | 6,872 | TR 3,223 (46.9%) | NG 2,415 (35.1%) | EG 607 (8.8%) |
| Money Transfer Clicked | 5,853 | TR 3,227 (55.1%) | NG 1,855 (31.7%) | EG 240 (4.1%) |
| Debit Card Tab Visited | 5,599 | TR 3,394 (60.6%) | NG 1,095 (19.6%) | EG 657 (11.7%) |
| Deposit Tapped | 2,619 | NG 1,185 (45.2%) | TR 987 (37.7%) | EG 224 (8.6%) |
| Financial Assistant Opened | 0 | — | — | — |

---

## Key Findings

### 1. Turkey (TR) — Power User Market
- **Dominates** Money Transfer (55.1%), Debit Card (60.6%), and Get Paid (46.9%)
- Turkey leads in 3 of 4 active features — users are heavily engaged with payments and card features
- Relatively lower share on Deposit (37.7%) — second to Nigeria

### 2. Nigeria (NG) — Deposit-First Market
- **Only market where Deposit leads** — NG is #1 for Deposit Tapped (45.2%) while being #2 everywhere else
- Strong Get Paid engagement (35.1%) suggests active earning/receiving flows
- Lower Debit Card engagement (19.6%) — card may be less relevant or available
- Nigeria has the most balanced feature usage across the board

### 3. Egypt (EG) — Card-Curious, Transfer-Light
- **Highest Debit Card share** relative to other features (11.7% of Debit Card vs 4.1% of Money Transfer)
- Egyptian users explore the card tab disproportionately more than they use transfer features
- Moderate Get Paid (8.8%) and Deposit (8.6%) — consistent ~8-9% baseline
- Money Transfer is notably low (4.1%) — potential friction or lack of supported corridors

### 4. Financial Assistant — Zero Usage
- No events recorded for "Financial Assistant Opened" during the period
- Either: not yet launched, renamed, or gated behind a flag

---

## Feature-by-Feature Breakdown

### Get Paid Opened (6,872 total)
The most-used feature. TR and NG together account for 82% of usage.

| Country | Count | % |
|---------|------:|--:|
| Turkey | 3,223 | 46.9% |
| Nigeria | 2,415 | 35.1% |
| Egypt | 607 | 8.8% |
| Ghana | 103 | 1.5% |
| Pakistan | 75 | 1.1% |

### Money Transfer Clicked on Homepage (5,853 total)
Turkey-heavy. Hungary appears at #5 (66 events) — unusual; worth investigating if organic or test traffic.

| Country | Count | % |
|---------|------:|--:|
| Turkey | 3,227 | 55.1% |
| Nigeria | 1,855 | 31.7% |
| Egypt | 240 | 4.1% |
| United States | 88 | 1.5% |
| Hungary | 66 | 1.1% |

### Deposit Tapped on Homepage (2,619 total)
The only feature where Nigeria leads Turkey. Deposit is critical for NG users.

| Country | Count | % |
|---------|------:|--:|
| Nigeria | 1,185 | 45.2% |
| Turkey | 987 | 37.7% |
| Egypt | 224 | 8.6% |
| Germany | 39 | 1.5% |
| United States | 20 | 0.8% |

### Debit Card Tab Visited (5,599 total)
Turkey's strongest feature (60.6%). Egypt has a notable 11.7% share — highest relative engagement for EG.

| Country | Count | % |
|---------|------:|--:|
| Turkey | 3,394 | 60.6% |
| Nigeria | 1,095 | 19.6% |
| Egypt | 657 | 11.7% |
| Pakistan | 51 | 0.9% |
| Germany | 45 | 0.8% |

---

## TR vs NG vs EG — Feature Mix Comparison

Normalized view (each country's events as % of their own total):

| Feature | TR (10,831 total) | NG (6,550 total) | EG (1,728 total) |
|---------|--:|--:|--:|
| Get Paid | 29.8% | 36.9% | 35.1% |
| Money Transfer | 29.8% | 28.3% | 13.9% |
| Deposit | 9.1% | 18.1% | 13.0% |
| Debit Card | 31.3% | 16.7% | 38.0% |

**Takeaways:**
- **TR** splits evenly between Get Paid, Money Transfer, and Debit Card (~30% each). Deposit is an afterthought (9.1%).
- **NG** is the most balanced market but indexes high on Deposit (18.1%) and Get Paid (36.9%). Card is lowest priority.
- **EG** is card-dominant (38.0%) with weak Money Transfer (13.9%). Users browse the card feature more than they transact.

---

## Recommendations

1. **Nigeria:** Double down on Deposit UX — it's the #1 action. Ensure deposit corridors are smooth and well-promoted.
2. **Turkey:** Card and Transfer are the engagement engines. Focus retention campaigns around these.
3. **Egypt:** Investigate why Money Transfer is low (4.1% share). High card interest (11.7%) suggests demand exists — may need better onboarding or corridor support.
4. **Financial Assistant:** Confirm feature status. If launched, check event naming in Amplitude.
5. **Hungary anomaly:** 66 Money Transfer clicks from Hungary is disproportionate — verify if it's organic, VPN, or test traffic.
