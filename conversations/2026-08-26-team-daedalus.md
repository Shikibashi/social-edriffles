# Daedalus activity log: community directory cleanup

## Phase 1 — research and proposal

- Scope: make the community directory scrollable, reduce directory noise, and handle the request to delete selected communities.
- Evidence: `listCommunities` accepts a cursor and returns up to 100 records; the client was loading only one page and rendering a horizontal strip. The Radlib private API exposes `leaveCommunity` but no `deleteCommunity` operation.
- Decision: continue with the uncommitted client draft for all-page loading, a vertical directory, search, and explicit filters. Do not call generic `com.atproto.simplespace.deleteSpace` because it would not remove the Radlib `private_space` metadata and could leave the directory inconsistent.
- Safety gate: exact community URI/name and owner authorization are required before destructive deletion. Deletion must have a Radlib contract, metadata cascade, Space cleanup, and tests before it is exposed.

## Phase 2 — approved safety contract

- User decision: approved Option 1 — delete every community owned by the authenticated user and start from scratch. This does not authorize deletion of communities owned by other DIDs.
- Confirmation boundary: the client must enumerate all pages, display the exact owner-scoped target count and identities, and require a separate final confirmation before issuing any delete call. Missing ownership data is never treated as ownership.
- Failure behavior: delete targets one at a time, stop on the first failure, and report completed and remaining targets so a partial cleanup is recoverable and auditable.
- Protocol behavior: a non-public community must clean up its associated Standard Space before the Radlib metadata cascade; public communities only need Radlib metadata cleanup. Generic `deleteSpace` remains unsuitable as a standalone client operation.

## Proposals

1. Recommended: add a Radlib owner-only `deleteCommunity` contract with confirmation, metadata cascade, protocol cleanup, and a client directory action; keep the current community protected until an explicit target is chosen.
2. Lower-risk: ship only the paginated, searchable, filterable directory and use existing leave behavior; defer actual deletion until a dedicated contract is approved.
3. Lowest implementation effort: add a client-only hidden list; this reduces local noise but does not delete data and does not change server visibility.

## Phase 5 — implementation and deployment

- Implemented and tested the owner-only `us.edriffles.radlib.private.deleteCommunity` procedure in PDS commit `678464128`; it validates the authenticated owner, cleans associated Standard Space state when present, and cascades Radlib control-plane rows without erasing member repositories.
- Implemented the all-pages directory, search/filter controls, explicit target review, final confirmation, stop-on-first-failure behavior, and OAuth `manage=delete` scope in social-app commit `da99b770d`.
- Verification: PDS Radlib suite 13 tests passed; store cascade tests passed; social OAuth scope suite 4 tests passed; web typecheck and focused Oxlint passed; root contract validation passed; the PDS image/container is healthy; public Social and PDS describe-server checks returned HTTP 200; unauthenticated delete returned HTTP 401; public metadata contains the delete scope.
- Deployment: Pages uploaded the built artifact as `https://9f4bb653.social-edriffles.pages.dev`, with the configured user-facing origin remaining `https://social.edriffles.us`. Qdrant was not restarted or modified.
