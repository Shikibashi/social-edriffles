# Next Runtime Slice Plan

Balanced v1 is explicitly out of scope. Execute in dependency order.

## A. Pairwise blocking semantics
- **Files/symbols:** `upstream/AppViewLite/src/AppViewLite/BlueskyRelationships.cs` relationship lookup; `src/AppViewLite.Web/ApiCompat/AppBskyGraph.cs`; live characterization tests.
- **Depends on:** completed live A/B/C matrix and pinned source review.
- **Tests:** authenticated A/B/C profiles, feeds, threads, notifications, blocks, inverse-block behavior; anonymous control.
- **Acceptance:** only the observed, approved bilateral semantics change; unrelated C behavior remains unchanged.
- **Rollback/security:** revert one AppViewLite submodule commit; prevent global content suppression and DID/handle leakage.

## B. AppView/service selection
- **Files/symbols:** social-app AppView client/provider configuration and service manifest types.
- **Depends on:** service manifest contract.
- **Tests:** explicit provider selection, unavailable provider, no silent fallback.
- **Acceptance:** provider identity and failure are visible; no implicit authority transfer.
- **Rollback/security:** feature flag removal; constrain service scopes and requester metadata.

## C. Standards-compliant AppView auth
- **Files/symbols:** AppView client auth/session boundary; FishyFlip/XRPC auth integration.
- **Depends on:** B and OAuth/service manifest review.
- **Tests:** token audience/scope/expiry, provider mismatch, logout, replay.
- **Acceptance:** least-privilege standards-compliant auth only.
- **Rollback/security:** disable provider; never widen token scopes as fallback.

## D. Portable personalization v1
- **Files/symbols:** `profile.ts` export/import/encryption; `local-feed.tsx` persistence.
- **Depends on:** audit F-11/F-12 and identity constitution.
- **Tests:** decrypt/import round-trip, wrong password, tampering, size/range/schema limits, version rejection.
- **Acceptance:** complete portable profile lifecycle with explicit provenance and no hidden telemetry.
- **Rollback/security:** retain local profile; reject malformed imports and erase temporary plaintext.

## E. Candidate retrieval
- **Files/symbols:** social-app Following feed query boundary and candidate model.
- **Depends on:** D and service selection.
- **Tests:** wider pool, pagination, omission audit, dedupe, blocked/muted content.
- **Acceptance:** retrieval scope is explicit and auditable before local ranking.
- **Rollback/security:** revert to chronological Following without silent substitute provider.

## F. Local reranking v2
- **Files/symbols:** `profile.ts` scoring and `PostFeed.tsx` integration.
- **Depends on:** E and ranking-trace schema.
- **Tests:** familiarity, normalized conversation activity, topics, seen state, author caps, exploration, deterministic ordering.
- **Acceptance:** rank across the declared candidate batch, not page-by-page.
- **Rollback/security:** opt-out returns original order; all sensitive signals remain on device.

## G. Faithful ranking traces
- **Files/symbols:** `Candidate`, scoring result, `explainCandidate`, “Why this post?” UI.
- **Depends on:** F.
- **Tests:** explanation equals exact trace; no stale freshness approximation; serialization stability.
- **Acceptance:** every displayed reason is trace-backed and omissions are distinguishable.
- **Rollback/security:** hide explanations rather than fabricate them.

## H. Integrity/Sybil pipeline
- **Files/symbols:** provider integrity evidence schema and local `integrityWeight` adapter.
- **Depends on:** C, E, G.
- **Tests:** correlated engagement discount, independent signals, moderation/content separation.
- **Acceptance:** integrity changes evidence weighting only; never labels or suppresses content by itself.
- **Rollback/security:** remove evidence input; audit provider provenance and privacy.

## I. Attention surfaces
- **Files/symbols:** search, account recommendations, trending, notifications, social-proof metric adapters.
- **Depends on:** G/H.
- **Tests:** privacy, pace/accessibility, omission audits, blocked/muted behavior across every surface.
- **Acceptance:** whole-stack attention governance with consistent explanations.
- **Rollback/security:** per-surface disablement; no engagement-only optimization.

## J. Feed marketplace/discovery
- **Files/symbols:** feed discovery UI, feed manifests, provider metadata.
- **Depends on:** B, G, H.
- **Tests:** manifest authenticity, policy display, provider replacement, hostile provider.
- **Acceptance:** users choose feeds knowingly; no silent fallback.
- **Rollback/security:** remove listing; revoke manifest without deleting user data.

## K. Manifests/provenance
- **Files/symbols:** service/feed manifest schema and verification library.
- **Depends on:** B/C/J.
- **Tests:** signatures, versioning, succession, provenance chain, expired/revoked manifest.
- **Acceptance:** origin, policy, model/version, and data use are inspectable.
- **Rollback/security:** reject unverifiable manifests.

## L. Exit/succession tests
- **Files/symbols:** export/import, provider migration, succession state machine.
- **Depends on:** D and K.
- **Tests:** migration without DID loss, provider death, emergency powers expiry, no data lock-in.
- **Acceptance:** credible exit preserves identity, PDS, public graph, and explicit preferences.
- **Rollback/security:** abort migration atomically; minimize retained copies and audit access.
