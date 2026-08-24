# Spaces alpha alignment audit

Status: `ALPHA-GATED / OWNER ACCEPTANCE PENDING`

Audited: 2026-08-23

This audit records the implementation state after the fork's Spaces migration
pass. It is intentionally not a production-readiness or E2EE claim. The alpha
PDS image and the fork's Spaces branch are disposable test infrastructure.

## Evidence set

| Component | Checkout | Role |
|---|---|---|
| Root fork | `codex/spaces-alpha-integration` | Pins, acceptance documents, and contract tests. |
| PDS submodule | `codex/spaces-alpha-integration` | Spaces alpha data plane plus Radlib policy/control routes. |
| Client submodule | `codex/spaces-alpha-integration` | Generated Spaces client adapter, multi-writer fanout, sync cursor boundary, private composer, and community board. |
| References | Retrieved 2026-08-23 | Official Spaces alpha, Proposal 0016, Bulletin, SecretSky, rsky, and HappyView. |

The exact baseline submodule SHAs are written to `upstream-pins.json` and
`artifacts/upstream-baseline.json`. The fork hardening source is committed as
PDS `2a119ba5f15a349d0db63fe46d1d3c854dfb9760` and recorded by the root
deployment commit; the root validator remains the final metadata gate.

## Current architecture

```text
Radlib policy / discovery / governance
        │  protected visibility, follow state, communities, invites, bans
        ▼
standard simplespace membership and Space credential exchange
        │  DPoP-bound credential
        ▼
Space records and blobs on every writer's own PDS repo
        ├── authority repo
        ├── member A repo
        └── member B repo
        ▼
viewer-authorized fanout or rebuildable cursor reconciliation
        ▼
private feed / Bulletin-style community board UI
```

Standard `com.atproto.space.*` and `com.atproto.simplespace.*` are the
authoritative content and access paths. Radlib's active store is constructed in
`mode: 'control'`, so it creates policy tables but not the legacy
`private_record`, `private_blob`, or `private_sync_grant` tables. The old
adapter methods remain isolated behind an explicitly selected `mode: 'legacy'`
for a future one-way migration lane; no active route or Spaces-mode client
calls them.

The UI now resolves a community authority through a narrowly-scoped service
auth call, exchanges a standard Space credential, enumerates all writer repos,
reads each writer from its own PDS endpoint, preserves the writer DID, and
shows a visible partial-read warning when a writer is unavailable.

## Implemented gates

| Gate | Result | Evidence |
|---|---|---|
| Spaces is the normal private content transport | `PASS` | PDS control mode has no legacy payload tables; Spaces-mode client has no legacy fallback; direct Space record/blob tests pass. |
| Radlib is policy/control only | `PASS` | Active routes cover visibility, follow state, community metadata, membership, invites, bans, and discovery. Private bodies/blobs are not stored in the control DB. |
| Protected account without legacy flag | `PASS` | `radlib-spaces.test.ts` deletes `PDS_LEGACY_RADLIB_PRIVATE_ENABLED` and writes/reads a Space record. |
| Protected block | `PASS` | Canonical `app.bsky.graph.block` from a remote PDS is detected across cursor pages; incomplete remote lookup fails closed, Space access is removed for confirmed blocks, and a fresh credential is rejected. |
| Community Space Lexicon | `PASS (local authority)` | `org.radlib.community` resolves as a `type: "space"` with only `org.radlib.private.post`; the OAuth scope test rejects an undeclared write. Live authority publication remains `PENDING`. |
| Private XRPC cache headers | `PASS (local HTTP + deployed unauthorized probe)` | Local unauthorized and authorized discovery/control responses and deployed unauthorized probes carry `private, no-store` plus `Authorization, DPoP` variation. A credentialed deployed probe was not run because no production token was used. |
| Multi-writer, multi-PDS community | `PASS` | Two PDSes, two DIDs, owner/member writes, repo enumeration, writer provenance, per-writer reads, and public-sequence canary. |
| Invite, hidden discovery, and ban | `PASS` | Private metadata is hidden before membership, invite access becomes visible after approval, and ban removes discovery and fresh credential access. |
| Private media | `PASS` | Space blob retrieval succeeds with a Space credential; ordinary `sync.getBlob` rejects a blob referenced only by a Space record; private/no-store headers are set. |
| Account lifecycle | `PASS` | Public transition preserves the account Space; the UI/docs do not silently publish or destroy private history. |
| Private sync boundary | `PASS (minimal)` | `listRepoOps` reconciliation persists only per-space/repo cursors and forwards operations to a rebuildable sink; no private bodies are persisted by the cursor store. |
| Generated Spaces client contract | `PASS WITH COMPATIBILITY NOTE` | Space Lexicon sources are generated from the matching PDS checkout; unsupported pinned-runtime `space-ref`/Space-record URI validators are deliberately unconstrained at the client boundary. |
| Browser UI | `PASS (smoke)` | Production community board renders the EDRIFFLES/Bulletin board, membership state, notes, writer provenance, private composer, and main compose affordance. Local static build loads on loopback. |

## Explicit alpha gaps

These are not hidden by the implementation:

1. A Space credential is self-contained in the pinned alpha protocol. Removing
   a member prevents new credential exchange, but an already-issued credential
   may remain usable until expiry. The acceptance tests call this out instead
   of claiming immediate revocation for old tokens.
2. The private fanout currently exhausts pages in one query. It has deterministic
   ordering and explicit partial errors, but does not yet expose one opaque
   aggregate continuation cursor to the UI.
3. The sync layer is a client-side cursor/reconciliation abstraction, not a
   server-side durable private AppView. Notifications are exposed as Space RPC
   wrappers; a browser is not registered as a notification service.
4. Community roles are stored as owner/member policy state. Admin/moderator
   workflows and a full member-management screen remain product work; the
   Space ACL is still the read/write authority.
5. Public AppView/search/feed/profile and external Relay scans are not used as
   private content sources. The local acceptance harness proves the public CAR
   and public repo sequencer canaries; a production AppView/Relay scan still
   requires a disposable two-PDS deployment lane.
6. The pinned client runtime cannot validate the alpha-specific Space URI
   formats, so generated client schemas leave those fields unconstrained. The
   PDS's generated schemas remain strict and authoritative.
7. The private-header fix is deployed to the local PDS container behind the
   `pds.edriffles.us` Cloudflare Tunnel. The post-deploy unauthorized probes
   for `listCommunities` and `getSpace` return `Cache-Control: private,
   no-store` and `Vary: Authorization, DPoP, Accept-Encoding`; `cf-cache-status:
   DYNAMIC` is recorded but is not used as the acceptance condition. A
   credentialed deployed probe remains unrun to avoid using production tokens.

## Research-derived decisions

- The official Spaces alpha model, not Bulletin, defines the content and
  credential boundary.
- Bulletin supplies the board interaction model: a focused board index, a
  visual pinboard, provenance, and owner-oriented membership affordances.
- SecretSky supplies the source-of-truth rule: a local index may be rebuilt but
  never grants authorization.
- rsky and HappyView support separating protocol hosting from indexing and
  viewer-aware reads.

References:

- [ATProto Spaces alpha](https://atproto.com/blog/atproto-spaces-alpha)
- [Permissioned Data proposal 0016](https://github.com/bluesky-social/proposals/blob/main/0016-permissioned-data/README.md)
- [Bulletin](https://github.com/bluesky-social/bulletin)
- [SecretSky](https://github.com/mmattbtw/secretsky)
- [rsky](https://github.com/blacksky-algorithms/rsky)
- [HappyView](https://github.com/gamesgamesgamesgamesgames/happyview)
