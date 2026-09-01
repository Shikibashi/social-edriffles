# Polycentric Authority Decision Record

Date: 2026-08-28
Updated: 2026-09-01
Scope: Plumbline client and its AT Protocol integration
Canonical domains: `plumblines.uk` (public client and OAuth),
`pds.edriffles.us` (PDS), and `radlib.edriffles.us` (project and Spaces
authority)

## Decision

Treat every provider as a replaceable, attributable participant in a user-owned
policy rather than as a constitutional authority. The client may use a bundled
provider as a convenience default, but it must retain the provider identity,
surface, result, verification state, freshness, error state, and disagreement
when composing reads. A provider's hostname, position in the stack, or declared
operator ID is not evidence that it independently controls the service.

No new registrable domain is required or introduced. `plumblines.uk` is the
public client and OAuth origin; the established PDS and Spaces authorities
remain under `edriffles.us` as distinct technical services.

## Residual concentrations discovered

1. A single AppView was previously the implicit read authority for identity,
   profiles, threads, feeds, search, notifications, labels, media, and
   communities. That made an outage, stale index, moderation choice, or silent
   provider disagreement look like a canonical user-visible fact.
2. OAuth requests mixed a broad compatibility transition grant with unrelated
   feature permissions. That created ambient authority and made it difficult to
   inspect or revoke one capability without reauthorizing everything.
3. PLC resolution had a primary resolver path without a client-level record of
   competing resolver claims or cryptographic history verification.
4. Local attention, moderation, provider, and reconciliation state did not have
   one validated portable export/import/reset boundary.
5. PLC rotation-key custody was not a first-class user-held workflow.
6. The PDS remains authoritative for the user's own records and writes, while
   Spaces remains authoritative for its existing permissioned-data operations.
   Media and communities do not gain a fabricated AppView authority merely
   because they appear in the provider-surface registry.
7. A fork-owned Space credential was valid for its JWT lifetime after member
   removal in the upstream alpha path. That concentrated revocation authority
   in token expiry rather than the Space authority's current membership state.

These concentrations matter because routing convenience can silently become
jurisdiction. They are reduced only where the protocol supplies a verifiable
boundary; adding another service under the same operator would not count as
dispersing authority.

## Ecosystem precedent used

- The [AT Protocol OAuth specification](https://atproto.com/specs/oauth) and
  [permission specification](https://atproto.com/specs/permission) provide
  PAR, PKCE S256, DPoP, issuer/DID binding, refresh handling, scoped `repo:`,
  `rpc:`, `blob:`, `account:`, and `identity:` grants, and service audiences.
- The [scope builder guide](https://atproto.com/guides/scope-builder) supports
  progressively narrowing permissions by collection, action, `lxm`, and
  `aud`, which is the basis for feature-scoped upgrades here.
- The [DID specification](https://atproto.com/specs/did),
  [cryptography specification](https://atproto.com/specs/cryptography), and
  [PLC implementation](https://github.com/did-method-plc/did-method-plc)
  define the signed history and key material that the client verifies rather
  than trusting a resolver response.
- [PLC read replicas](https://atproto.com/blog/plc-replicas) establish that
  independently operated read replicas are a protocol-compatible deployment
  pattern. Operational independence remains an external fact and is not
  inferred from a client configuration field.
- The [account recovery guide](https://atproto.com/guides/account-recovery)
  establishes the recovery/rotation boundary used by the user-held key
  custody implementation.
- [Cirrus](https://cirrus.earth/) demonstrates a small, directly operated
  single-user PDS on Workers, Durable Objects, and R2. Its current changelog
  also documents endpoint-enforced granular OAuth permission sets and a
  transitional compatibility shim. That precedent supports keeping the
  client/PDS boundary protocol-compatible without treating a large shared
  AppView as mandatory, while its beta and migration warnings argue against
  claiming that a new PDS implementation is automatically safer.
- [str4d/plc](https://github.com/str4d/plc) is a focused Rust key-management
  tool that exposes rotation-key inspection, audit validation, and a planned
  YubiKey backup-key workflow. It supports the custody direction here, but its
  work-in-progress status and the protocol's authorized-rotation boundary are
  why this client prepares a non-exportable key without claiming that key
  generation alone grants recovery authority.
- [Blacksky's AT Protocol fork](https://github.com/blacksky-algorithms/atproto)
  and [rsky](https://github.com/blacksky-algorithms/rsky) demonstrate that
  firehose/indexing, dataplane, AppView, feed generation, label delivery, PDS,
  and relay functions can be separately implemented and operated. Their
  community-post and indexing-specific components are treated as precedent for
  service decomposition, not as a portable authority over another PDS's
  records. A current independent labeler example, [atproto-fact-labeler](https://github.com/DracoBlue/atproto-fact-labeler),
  likewise shows signed label claims and retryable delivery as separate from
  the user's local moderation policy.

## Chosen changes

### Feature-scoped OAuth

New authorization requests use `atproto` plus ordinary posting, profile
editing, social-graph, and audience-scoped AppView RPC grants. Chat, Spaces,
media, and notifications are separate feature groups. Existing transition
grants remain recognized only for compatibility with already-authorized
sessions; new requests do not request them. Reauthorization computes only the
missing feature scopes and merges them with the existing grant, preserving
posting, likes, profile editing, chat, and Spaces sessions.

### Provider composition

The composition boundary covers identity resolution, profiles, threads, feeds,
search, notifications, labels, media, and communities. Each query can fan out
to the selected providers and retain attributable observations. User-owned
per-surface policies select one of:

- require agreement;
- first verified result;
- explicit provider preference; or
- explicit merge of attributable results when the query supplies a
  domain-specific merge function.

Stale, unavailable, invalid, blocked, revoked, and malicious-looking claims are
retained as observations but are not silently promoted to a winner. A merge
policy without an explicit domain merge function returns the claims without a
selected value, so an implementation cannot accidentally discard a provider or
combine incompatible cursors. The bundled AppView has no special
reconciliation privilege. The current PDS and Spaces paths remain explicit
write/authority boundaries where no compatible AppView read contract exists.

### Resolver plurality and verification

The client supports the compatibility PLC Directory plus user-registered public
HTTPS mirrors/resolvers. Each audit history is checked for the PLC genesis DID
derivation, previous CIDs, active rotation-key signatures, and terminal
tombstone rules before selection. Agreement, disagreement, partial failure,
unavailability, and tombstoning are visible in the result. Operator IDs are
disclosures only; the client does not claim that two endpoints are genuinely
independent without deployment/operator evidence.

### Portable policy and exit

Provider capabilities, per-surface reconciliation policies, identity provider
preferences, attention policy, moderation policy, and portable personalization
can be exported/imported through validated versioned data. Exports omit
endpoints, credentials, tokens, and service-auth material. Imports can modify
only already-registered providers, and reset operations revoke optional provider
surface capabilities without deleting the identity account. Attention and
moderation can be reset independently or together.

### User-held recovery and rotation

The browser/WebCrypto path creates a non-extractable P-256 rotation key,
exports only its public `did:key` form, stores the private `CryptoKey` in an
IndexedDB-backed key store, signs a canonical PLC operation only when the key
is already authorized by the supplied PLC history, and submits through the
standard `com.atproto.identity.submitPlcOperation` endpoint. The Identity and
recovery screen exposes preparation of that custody boundary for `did:plc`
accounts and explains the remaining authorization step. Native clients must
provide a platform secure-key implementation; no private key export or
automatic recovery authority is added.

## Authority before versus after

| Boundary | Before | After |
|---|---|---|
| Public reads | One implicit AppView winner | Per-surface provider fanout, provenance, freshness, and user policy |
| OAuth | Broad compatibility grant mixed with features | Feature-scoped base grant plus progressive reauthorization |
| Identity resolution | Primary resolver result | Multiple claims with signed PLC-history verification and disagreement |
| Policy portability | Local settings without one policy boundary | Validated export/import/reset for providers and user policy |
| PLC rotation | Server-mediated path only | User-held non-exportable key path where secure custody exists |
| Own writes | Could be confused with public index state | PDS remains the authoritative record source; AppView lag is explicit |
| Media/communities | Risk of implied AppView authority | Surface is configurable, but runtime authority remains explicit PDS/Spaces |

## Interoperability and security tradeoffs

Provider composition adds concurrent requests, latency, cache coordination, and
privacy exposure to multiple operators. It therefore defaults to conservative
selection, keeps the provider set explicit, does not send credentials to public
providers, and treats unsigned AppView responses as unverified. Merge and
provider preference require a visible local policy. Public AppView responses
are not cryptographic proof of repository state; the PDS remains authoritative
for owned records.

Resolver disagreement can temporarily make identity routing unavailable rather
than silently selecting a potentially stale or malicious history. The PLC
verifier currently targets canonical v0.3 audit-operation shapes; legacy PLC
history normalization remains a compatibility item for a later bounded change.
The user-held key path provides custody and signing primitives, not a promise
that a PDS will accept an operation or that a client can bypass protocol
recovery rules.

The implementation preserves AT Protocol APIs and official OAuth machinery.
It does not invent a private cross-provider write protocol, weaken block
boundaries, bypass labeler claims, or treat local policy as a universal command
to other actors. For `us.edriffles.radlib.*` Spaces, the PDS now adds an
opt-in status check at credential use time; the standard signed JWT and DPoP
wire format remain unchanged, and ordinary Space types keep the upstream path.

### External evidence batches

The three remaining external gates are implemented as separate, fail-closed
evidence boundaries. A disposable PDS can opt into a short access-token
lifetime through `PDS_OAUTH_TOKEN_MAX_AGE_MS`; the guarded browser probe then
tests expiry, refresh rotation, stale-access rejection, and authorization-code
replay with two disposable identities. A controlled Relay/AppView scan receipt
requires public-control and private-canary observations plus capture, storage,
and log access. An independent PLC receipt requires distinct operator
identities and endpoints, a signed DID-history statement, cryptographic
verification, and visible resolver disagreement. Synthetic fixtures exercise
these validators but remain explicitly non-evidence and cannot clear the
manifest blockers.

## Implementation evidence

- `upstream/social-app/src/lib/provider-composition.ts` — generic attributable
  provider fanout and reconciliation boundary.
- `upstream/social-app/src/state/queries/provider-composition.ts` — AppView
  provider adapter with endpoint-scoped client factories.
- `upstream/social-app/src/state/queries/{profile,post,feed,search-posts-v2,labeler}.ts`
  and `upstream/social-app/src/state/queries/notifications/` — composition at
  the existing query boundaries while preserving PDS-owned writes.
- `upstream/social-app/src/state/session/oauth-scopes.ts` and
  `oauth-session.ts` — feature scopes and progressive upgrades.
- `upstream/social-app/src/lib/plc-history.ts`, `plc-resolver.ts`, and
  `src/state/session/plc-resolvers.ts` — signed-history verification and
  resolver claims.
- `upstream/social-app/src/lib/plc-key-custody.ts` — user-held key boundary.
- `upstream/social-app/src/lib/personalization.ts` and
  `src/state/persisted/schema.ts` — portable policy state and reset semantics.
- `upstream/social-app/src/screens/Settings/ServicesSettings.tsx` and
  `PersonalizationSettings.tsx` — user-visible capability, resolver, policy,
  export/import, and reset controls.
- `upstream/social-app/src/screens/Settings/IdentitySovereigntySettings.tsx` —
  user-visible non-exportable PLC custody preparation and explicit
  authorization limitation.
- `upstream/atproto-pds/packages/pds/src/actor-store/space/` and
  `packages/pds/src/auth-verifier.ts` — durable fork-owned credential status,
  fail-closed authority checks, and member-removal revocation.
- `scripts/verify_social_edriffles_live.py` — credential-free live endpoint
  probe plus cryptographic verification through the checked-in PLC verifier.
- `scripts/refresh_oauth_spaces_evidence.py` — reproducible current-receipt
  and release-manifest binding without rewriting historical evidence.
- `scripts/validate_external_gate_receipts.py` and
  `tests/test_external_gate_receipts.py` — fail-closed external canary,
  short-TTL OAuth, PLC operator, provenance, and signature contracts.
- `docs/EXTERNAL_GATE_REMEDIATION.md` and
  `docs/flow-diagrams/external-gate-remediation.mmd` — operator runbook and
  evidence-promotion boundary for the three external gates.
- `artifacts/deployment-current.json` — source, Pages, Worker, PDS image,
  route, domain, and environment identifiers for the deployed release.
- `docs/flow-diagrams/polycentric-authority-loop.mmd` — runtime authority loop.

## Verification evidence

The focused deterministic suite currently passes: 13 Jest suites and 74 tests,
covering OAuth feature scopes, provider policies and portability, all declared
provider surfaces, stale/malicious/partial/revoked/block/labeler/migration
fixtures, PLC signed-history tampering, resolver disagreement, user-held key
custody, and Spaces client/credential/sync paths. The full Jest suite also
passes: 103 suites, 984 tests, and 21 snapshots. The PDS TypeScript build and
test projects pass, and the focused PDS authorization/Spaces/header suite
passes: 3 suites and 48 tests. The edge metadata-cache regression suite passes
8 tests. `pnpm run typecheck:web`, the changed-file Oxlint check, the web
production build, root whitespace validation, and root contract validation all
pass. The full repository lint command remains red on pre-existing import-sort,
unused-variable, TypeScript, and suppression-baseline violations outside this
change; the activity log records that distinction rather than treating a
targeted lint pass as a repository-wide pass.

The fresh credentialed disposable-identity OAuth walkthrough and deployed
Spaces revocation walkthrough now pass in the current release receipts. The
live PLC audit history itself verifies cryptographically through the checked-in
client verifier. No production credentials are used. Genuinely independent PLC
operator evidence and an external Relay/AppView privacy scan remain unproven;
the short-TTL expiry/replay walkthrough is also still open. Those remaining
operator, privacy, and expiry gates stay external rather than being relabeled
as local PASS results.

## Remaining concentrations worth attacking next

1. The PDS and its deployment operator still control hosting availability and
   acceptance of writes; credible migration and operator exit need live
   credentialed tests and documented export/restore procedures.
2. Public AppViews and relays can lag, omit, or refuse records; independently
   operated deployed providers and signed/verifiable result paths should be
   added only with actual operator evidence.
3. The compatibility PLC Directory remains the default resolver and legacy PLC
   history normalization is not yet implemented. Configured resolver entries
   expose declared operator identity, but that declaration is not proof of
   independent operation.
4. Deployed OAuth metadata, credentialed Spaces revocation behavior, and
   Relay/AppView scans remain environment gates. DNS and checked-in authority
   resolution for `us.edriffles.radlib.*` now pass; the client cannot
   manufacture independent-operator or deployment receipts.
