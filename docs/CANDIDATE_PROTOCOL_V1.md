# Candidate Protocol v1

Candidate Protocol v1 is the provider-independent, declarative boundary between untrusted candidate providers and local/client ranking. It is ATProto-centered but intentionally leaves an extension point for future Lexicons and external protocols. It does not implement Balanced v1.

It is subordinate to the Attention Constitution and Feed Provider Security contract; provider batches propose candidates and never own attention policy.
## Batch schema

A batch contains `format`, `version`, unique `batchId`, `providerDid`, `serviceIdentity`, source `{id,type}`, manifest `{id,version,hash}`, ISO-8601 `generatedAt`/`expiresAt`, bounded cursor, explicit `privacyMode`, candidates, and signed `{keyId,algorithm,signature}` metadata. A candidate binds AT URI, CID, candidate timestamp, and hydration `{state,checkedAt}`. Hydration states are visible, deleted, labelled, access-restricted, or unavailable; hydration is current access/visibility state and must be rechecked before display.

Provider reason codes are advisory data. Local ranking reasons, audit traces, and confidential integrity evidence are separate layers and never replaced by provider claims.

## Canonical signing and replay

Canonical JSON recursively sorts object keys, preserves array order, rejects undefined/non-finite values, and uses canonical numeric fields. V1 signatures use ECDSA P-256/SHA-256 over the canonical unsigned batch. `keyId`, manifest version/hash, and provider identity bind provenance. Batches must not be expired, future-versioned, malformed, duplicated, or replayed; `ReplayGuard` rejects a reused `batchId` within its bounded window. Provider succession uses a new manifest/key identity and explicit acceptance rather than silent key substitution.

## Privacy modes

The schema explicitly supports:

- `public-cacheable`: no account identifier; suitable for shared caches.
- `anonymous`: no stable requester identifier.
- `pseudonymous`: rotating/non-account pseudonym where required.
- `cohort`: bounded cohort request without account identity.
- `stable-did`: strongest personalization-aware mode and highest requester exposure.

The current implementation validates and represents all five modes; transport adapters and privacy-preserving provider negotiation remain future integration work. Portable Personalization is never included in a batch.

## Determinism and extensibility

Canonical field ordering, canonical rank keys, URI tie-breaking, and stable serialization make replay cross-platform. Missing features are distinct from negative features. Unknown candidate record types may be retained as opaque data only when the enclosing version declares them optional; unknown required features reject the batch. Future community Lexicons and external feeds must define an adapter preserving the same identity, hydration, signing, and privacy boundary.

## Replay fixture

A reproducible replay consists of the signed batch, provider manifest, Portable Personalization snapshot at an allowed abstraction level, hydrated candidate features, and deterministic local ranking output. The fixture is test data only; no provider payload is executable.
