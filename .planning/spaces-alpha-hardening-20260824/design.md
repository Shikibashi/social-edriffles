---
type: design
title: "Spaces alpha hardening and interoperability"
description: "Harden protected access grants, publish the community Space type, and enforce private response cache headers without deploying alpha infrastructure."
status: draft
mode: workpacks
updated: "2026-08-23"
authority: "Pinned PDS/client revisions, existing contract tests, read-only production probes, and official ATProto Spaces/Permissioned Data guidance reviewed 2026-08-23."
---

# Spaces alpha hardening and interoperability

## Outcome

The fork has an implementation-ready, dependency-linked path for the three immediate safety/interoperability gaps found in the Spaces alpha audit:

1. protected follow/access grants fail closed when remote block state is incomplete or unavailable, while still recognizing blocks beyond the first page;
2. `org.radlib.community` is a resolvable `type: "space"` Lexicon with an explicit collection contract and scoped-permission fixtures;
3. every private XRPC success and error response is `private, no-store` and varies on the authorization mechanisms it accepts.

The work is followed by a documentation/release gate that keeps the alpha/no-E2EE boundary and residual credential limitation visible. No production deployment, account mutation, Cloudflare mutation, or real-data migration is part of this plan.

## Current evidence

- The focused PDS suite passed 109 tests and the focused client suite passed 16 tests. Contract validation passed (113 files, 29 blocking rows, 6 feed cases); upstream pin checks report both submodules current.
- `upstream/atproto-pds/packages/pds/src/api/org/radlib/private/index.ts` currently checks remote blocks with `limit=100`, does not follow a cursor, and returns `false` on resolver, fetch, status, or parse failure. The happy-path remote-PDS block test passes, but the helper is not fail-safe.
- `org.radlib.community` is a URI constant in `packages/pds/src/permissioned-data/store.ts`, not a checked-in `type: "space"` Lexicon. Existing alpha tests prove the provider can materialize collections from a declared test type.
- `privateAuth` reapplies private headers around authorization; `privateControlAuth` does not reapply them after its service-auth fallback. The live unauthenticated `listCommunities` response observed `cache-control: private`, while `getSpace` observed `private, no-store`; Cloudflare reported `DYNAMIC`.
- Official references: [Spaces alpha](https://atproto.com/blog/atproto-spaces-alpha), [Permissioned Data proposal](https://github.com/bluesky-social/proposals/blob/main/0016-permissioned-data/README.md), and [block implementation guidance](https://atproto.com/blog/block-implementation).

UNVERIFIED until implementation: the exact externally deployed Lexicon-authority publishing path for the production authority DID, and whether the production service will remain alpha/test-only after these changes.

## Design

### Workpack order

- **WP-001 — fail-closed remote block checks:** introduce a tri-state internal lookup (`blocked`, `not blocked`, `unknown`) with cursor pagination, repeated-cursor detection, and bounded timeout/page budget. Protected access-grant callers treat `unknown` as no grant and never convert it into a successful approval. Existing community-ban policy remains separate.
- **WP-002 — private response headers:** after WP-001 because both own the same PDS API file, centralize header application across service-auth fallback, local authorization success, and all failures. Preserve the current JSON response contract.
- **WP-003 — community Space Lexicon:** add the authority-owned `org.radlib.community` space declaration with key `any`, human-readable name, and `org.radlib.private.post` as the initial declared collection; regenerate the PDS Lexicon barrel and add provider scope-materialization/undeclared-collection tests. Do not add a new client provider-selector or OAuth UX in this cycle.
- **WP-004 — alpha documentation/release gate:** after the code workpacks, update the existing Spaces alignment docs with the no-production/no-E2EE boundary, delayed credential revocation, the anti-block failure behavior, and required live header probes.

All workpacks remain `draft` because this turn authorizes planning files only. Test cases are specified before implementation; test materialization and source edits require a separate implementation authorization.

## Interfaces and boundaries

- PDS policy boundary: `upstream/atproto-pds/packages/pds/src/api/org/radlib/private/index.ts` owns protected-account access grants and response headers.
- PDS protocol boundary: `upstream/atproto-pds/lexicons` plus generated `packages/pds/src/lexicons` owns the Space declaration; standard `com.atproto.space.*` remains the permissioned data plane.
- Test authority: focused PDS tests, root contract validation, and read-only HTTP probes. No browser credentials or private storage are part of the evidence.
- Client boundary: current DPoP Space transport remains unchanged. Private AppView/search/notification/moderation-reader services are excluded from this plan.
- Deployment boundary: no Docker, PDS, Pages, DNS, Cloudflare, account, or production writes.

## Decisions and alternatives

- Keep block lookup fail-closed only for protected access-grant decisions. Do not globally reinterpret every ordinary block lookup, and do not conflate a bilateral block with a community-local ban.
- Use a bounded pagination loop with an explicit `unknown` result instead of unbounded remote work. This preserves availability under normal conditions and prevents an outage from becoming an authorization grant.
- Publish the Space type in the PDS Lexicon source and test authority resolution before changing client OAuth/provider behavior. A broad client scope redesign is deferred because the pinned fork currently uses direct DPoP Space transport and project instructions defer provider selectors.
- Normalize headers at the PDS auth boundary rather than adding a Cloudflare rule first. The PDS must be safe if the edge configuration changes; Cloudflare remains a verification target, not the authorization layer.
- Hardest cut: private AppView/search/notifications/moderation readers. They are valuable product work, but adding them now would expand this security/interoperability patch into a new service architecture without an approved authority or deployment design.

## Risks and recovery

- Remote block pagination can add latency; the fixed deadline/page budget and generic fail-closed error are mandatory. Stop if the implementation cannot distinguish a complete negative lookup from an unknown lookup.
- A wrong Space Lexicon collection set can overgrant OAuth. Stop if the declaration cannot be resolved by the configured Lexicon authority or if an undeclared collection is accepted by the provider tests.
- Header tests must cover both 401 and 200 paths; `cf-cache-status: DYNAMIC` alone is not acceptance. Stop before deployment if any private XRPC response lacks `private, no-store`.
- Alpha credential removal remains delayed for already-issued credentials. Do not claim immediate revocation or add stateful revocation without a separate protocol/product decision.
- Rollback is limited to reverting the isolated workpack commits before deployment. No live rollback or data repair is authorized by this plan.

## Non-goals

- No production deployment or migration away from the Spaces alpha.
- No E2EE implementation claim.
- No private AppView, private search index, notification delivery, or admitted moderation-reader service.
- No new community membership policy, invite-token policy, or UI redesign.
- No client provider selector or broad OAuth-consent redesign.
- No destructive data operation, Cloudflare account mutation, or inspection of credentials/browser storage.
