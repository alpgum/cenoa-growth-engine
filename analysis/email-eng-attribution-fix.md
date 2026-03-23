# Email Draft: Engineering — Attribution Fix

**To:** Engineering Team  
**From:** Marketing / Growth  
**Subject:** [P1] Web-to-App Attribution Gap — 81.8% of Signups Unattributed  

---

Hi team,

**Problem:** 81.8% of signups in Amplitude show `media_source = (none)`. Root cause: our landing page "Download" buttons link directly to the App Store / Play Store, which breaks the UTM→install chain. AppsFlyer tags these installs as Organic, and all downstream events (signup, KYC, deposit) lose attribution.

**Impact:** We can't measure which campaigns actually drive signups and activations. Budget decisions are based on broken data — strict last-click shows Meta at $125/signup when the modeled reality is closer to $8. We estimate $3K+/mo in misallocated spend from optimizing against incomplete numbers.

**Proposed solution:** Replace all direct store links with AppsFlyer OneLink URLs, implement deferred deep linking (SDK already integrated), and add a lightweight web-side UTM persistence layer. Full architecture, code samples, and QA test plan are in the attached spec.

**Ask:** Could you review the spec and provide a scope estimate? Our suggested phasing:

- **Phase 0** (2 days): Create OneLink template, replace store links — immediate signal recovery  
- **Full pipeline** (~3 weeks): Web session capture → deferred deep links → backend join → Amplitude property propagation

**Full spec:** `analysis/attribution-fix-spec.md`

Happy to walk through the spec together or answer any questions.

Thanks!
