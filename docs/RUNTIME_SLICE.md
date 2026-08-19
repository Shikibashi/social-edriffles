# Runtime Slice Status

## Imported baselines

- `upstream/social-app` is checked out at `c38bfe515a9d52d2b9969c8ead64eced5f8d33ee`.
- `upstream/atproto-pds` is checked out at `760fb12a080c87cdfd0dae42ae833bad8bc20886`.
- AppViewLite and FishyFlip are retired and are not imported baselines.

## Characterization

The root A/B/C fixtures and client/PDS moderation tests anchor pairwise
relationship behavior without coupling the contract to a specific read
provider. A disposable signed-record run verifies the first-party PDS/CAR/
provider migration boundary; provider-specific relationship presentation still
requires the owner’s selected-provider walkthrough.

## Pairwise relationship boundary

The active contract evaluates `(a,b)` and `(b,a)` in the viewer context and
keeps direct blocks, incoming external hard boundaries, and local attention
filters distinct. It is implemented at the client/PDS policy boundary and is
not tied to a fork-specific AppView.

## Local feed sovereignty

`upstream/social-app/src/lib/feed-sovereignty/profile.ts` provides local candidate scoring, author caps, exploration floors, and deterministic “Why this post?” reasons. Portable personalization state is now defined in `upstream/social-app/src/lib/personalization.ts`, with account-scoped storage, settings/profile/archive exports, strict validation, and authenticated encrypted backup.

## Attention Constitution

`docs/ATTENTION_CONSTITUTION.md` governs the full attention surface, including feeds, search, recommendations, trending, directories, Starter Packs, notifications, social-proof metrics, provider transparency, concentration controls, delegated authority, emergency changes, accessibility, and pace sovereignty. It is an architectural contract; Balanced v1 remains deferred.

## Baseline verification

- Social-app typecheck and focused personalization/session Jest suites pass.
- Root contract and Python audit suites pass.
- First-party PDS build and focused migration/attestation tests pass.
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
