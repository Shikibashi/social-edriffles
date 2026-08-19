# Upstream Patch Surface

High-risk social-app surfaces are `src/lib/identity-runtime.ts` (resolver/cache/auth authority) and `src/screens/Settings/IdentitySovereigntySettings.tsx` (settings integration). They are protected by focused identity tests and root contracts. Medium-risk surfaces are the dedicated personalization, candidate, feed-security, attention, service-provider, and experimental modules. Root fixtures/scripts are low-risk release tooling.

The supported upstreams are social-app and the first-party atproto PDS. The
former AppViewLite/FishyFlip dependency pair was retired and is no longer a
patch surface. Churn classification is `LOCAL_HISTORY`; no remote fetch is
performed by the checker. A clean Git merge is not semantic proof: map changed
surfaces to identity, association, attention, service, personalization,
deployment, and root gates before accepting updates.
