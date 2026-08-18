# Runtime Slice Status

## Imported baselines

- `upstream/AppViewLite` is checked out at `73f3c2408fc5c744b14da78ce6d4427ddc1d69da`.
- `upstream/social-app` is checked out at `bde69aa15102640b0e898653a505191acc4951a9`.
- `upstream/FishyFlip` is checked out at `da2c08aa19475eb2c732933d213a374f03a8e549`.

## Characterization

`tests/test_appviewlite_characterization.py` anchors the A/B/C matrix to real pinned AppViewLite source paths and verifies the pairwise relationship core considers direct and inverse relationships while preserving unrelated viewers. A disposable signed-record run now verifies firehose ingestion and several HTTP 200 endpoints; block-list and viewer-specific block assertions remain incomplete because the pinned block controller is unimplemented and the live viewer state did not expose A→B.

## Pairwise relationship boundary

AppViewLite's relationship core was explicitly named `UsersHavePairwiseBlockRelationshipCore`. It evaluates `(a,b)` and `(b,a)` for the requesting context and returns direct, inverse, mutual, or no relationship. This is a naming/contract clarification of the existing behavior, not a nuclear-block semantic rewrite.

## Local feed sovereignty

`upstream/social-app/src/lib/feed-sovereignty/profile.ts` provides local candidate scoring, author caps, exploration floors, and deterministic “Why this post?” reasons. Portable personalization state is now defined in `upstream/social-app/src/lib/personalization.ts`, with account-scoped storage, settings/profile/archive exports, strict validation, and authenticated encrypted backup.

## Attention Constitution

`docs/ATTENTION_CONSTITUTION.md` governs the full attention surface, including feeds, search, recommendations, trending, directories, Starter Packs, notifications, social-proof metrics, provider transparency, concentration controls, delegated authority, emergency changes, accessibility, and pace sovereignty. It is an architectural contract; Balanced v1 remains deferred.

## Baseline verification

- Social-app typecheck and focused personalization/session Jest suites pass.
- Root contract and Python audit suites pass.
- AppViewLite Release build passes with 0 errors and existing warnings.
- A clean current upstream checkout completed codegen and `pnpm build` with the pinned Node 24 runtime family; `make run-dev-env` reached `Dev environment is ready` after rebuilding the native SQLite binding.
## Research reconciliation: four constitutional domains

The existing constitutional intent maps into four non-duplicating domains:

- **Identity Constitution** — DID/PDS continuity, portable explicit preferences, credible exit, privacy-preserving observability, supply-chain security, and account recovery.
- **Association Constitution** — bilateral blocks, private mutes, reviewed one-time imports only, no delegated continuous block-list mutation, follows/lists, harassment boundaries, and direct-interaction severance.
- **Attention Constitution** — on-device reranking, whole-stack attention governance across feeds/search/recommendations/trending/notifications/social proof, explanation fidelity, candidate omission audits, accessibility and user-controlled pace, and `harassmentAmplificationRisk`.
- **Service Constitution** — manifests, provenance, provider succession, standards-compliant auth, no silent fallback, replaceable services, integrity/Sybil separation from moderation/content judgment, emergency powers, and credible exit.

### Research-to-code gap matrix

| Research requirement | Current code/status | Gap |
|---|---|---|
| Portable personalization | Account-scoped v1 settings/profile/archive state with strict validation and encrypted backup | Automatic synchronization and secure deletion remain deferred |
| Hostile providers/requester privacy | Service Constitution provider boundary and explicit selection | Candidate omission audits and privacy-preserving telemetry remain deferred |
| On-device reranking | Existing local candidate scoring and caps | Broader candidate retrieval and provider trace integration |
| Sybil/integrity separation | Constitution separates integrity, moderation, trust, and ranking utility | Provider-supplied integrity evidence remains deferred |
| Attention governance | Attention Constitution and machine-checkable surface contract | Runtime enforcement and Balanced v1 remain deferred |
| Service manifests/succession | Service Constitution and provider identity records | Signed manifest succession protocol remains deferred |
| Accessibility and pace | Constitutional requirements documented | Explicit runtime pace controls and verification remain deferred |
| Emergency powers | Bounded incident/expiry/rollback requirements documented | Operational emergency tooling remains deferred |

Balanced v1 is not implemented or claimed.
