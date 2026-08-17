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

`upstream/social-app/src/lib/feed-sovereignty/profile.ts` provides local candidate scoring, author caps, exploration floors, explicit portable profile JSON, and AES-GCM/PBKDF2 encrypted backup using platform cryptography. Its focused Jest suite covers author caps, exploration, profile round-trip, and encryption.

## Baseline verification

- `upstream/social-app/src/state/preferences/local-feed.tsx` persists an opt-in local-reranking toggle and explicit preferences on-device. Following-feed settings expose the toggle; feed rendering applies local slice reranking and displays deterministic “Why this post?” reasons.
- Social-app `pnpm intl:compile && pnpm typecheck:web` passes.
- Focused feed Jest suite and root audit suite pass; the repository Python suite passes 21 tests with 2 live-endpoint skips.
- AppViewLite builds with the isolated .NET 10 SDK and `-p:SignAssembly=false`, with 8 existing compiler warnings and 0 errors.
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
| Portable personalization | Plaintext profile export/import plus encrypted export | Decrypt/import, strict schema limits, provenance |
| Hostile providers/requester privacy | Local-only toggle and AsyncStorage | Candidate omission audits, privacy-preserving telemetry, no-fallback enforcement |
| On-device reranking | Opt-in per-page prototype | Wider candidate retrieval and faithful trace |
| Sybil/integrity separation | `integrityWeight` field only | Provider-supplied integrity evidence and non-moderation boundary |
| Attention governance | Following-only prototype | Search, recommendations, trending, notifications, social proof |
| Service manifests/succession | Constitutional documentation only | Signed manifests, succession protocol, exit tests |
| Accessibility and pace | Existing client conventions | Explicit feed pace controls and verification |
| Emergency powers | Documentation intent only | Narrow, auditable, expiry-bound operational tests |

Balanced v1 is not implemented or claimed.
