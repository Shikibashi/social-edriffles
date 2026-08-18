# Upstream Patch Surface

High-risk social-app surfaces are `src/lib/identity-runtime.ts` (resolver/cache/auth authority) and `src/screens/Settings/IdentitySovereigntySettings.tsx` (settings integration). They are protected by focused identity tests and root contracts. Medium-risk surfaces are the dedicated personalization, candidate, feed-security, attention, service-provider, and experimental modules. Root fixtures/scripts are low-risk release tooling.

AppViewLite and FishyFlip currently have no local source delta in this integration tree; they remain pinned optional/dependency repositories. Churn classification is `LOCAL_HISTORY`; no remote fetch is performed by the checker. A clean Git merge is not semantic proof: map changed surfaces to identity, association, attention, service, personalization, deployment, and root gates before accepting updates.
