# ATProto Spaces authority model

Status: `IMPLEMENTED CONTROL/CONTENT BOUNDARY; ALPHA GAPS REMAIN`

Audited: 2026-08-23

This document defines which system is authoritative for each datum. Spaces are
an alpha access-control and repository protocol, not end-to-end encryption.

## Authority map

| Datum | Canonical authority | Radlib/UI role |
|---|---|---|
| Private record body, CID, rkey, revision | Writer's Space repo on the writer PDS | Fetch through a fresh viewer-authorized Space credential. |
| Private blob bytes | Writer PDS blob store, referenced by a Space record | Render through `com.atproto.space.getBlob`; ordinary sync blob access is blocked for Space-only references. |
| Space authority, policy, members, writer set | `com.atproto.simplespace.*` and `com.atproto.space.*` | Request policy transitions; never substitute a local membership row for the Space ACL. |
| DPoP key/credential exchange | Standard Spaces credential flow | Keep the key in the client session; issue writer-PDS clients with the same DPoP-bound credential. |
| Protected/public preference | Radlib control database | Choose whether future account writes use a protected Space; public history stays public. |
| Follow request and approval | Radlib control database plus Space member transition | A successful approval must add the Space member; revoke/block removes the member. |
| Community name/description/visibility | Radlib authority database | Discover metadata only when the viewer may discover it. |
| Invite token, role, ban, audit record | Radlib authority database | Drive Space membership transitions; does not itself grant record reads. |
| Derived feed/index/cursor | Rebuildable private sync layer | Cache position/provenance only; every private body read is re-authorized against Spaces. |

## Read/write invariant

```text
UI/app
  -> service-auth to the Radlib authority for policy calls only
  -> DPoP-bound Space credential
  -> authority listRepos
  -> writer-PDS listRecords/getRecord/getBlob
```

The public relay, public AppView, public search, public feeds, and ordinary
public repository export are outside this path. Space writes are stored in the
writer's own permissioned repo and do not advance the ordinary public repo
sequencer.

## Multi-writer community read

The client fanout in `src/lib/atproto/spaces/fanout.ts`:

1. exchanges a Space credential;
2. exhausts all `listRepos` pages;
3. opens the same credential-bound client at each writer's resolved PDS;
4. exhausts each writer's `listRecords` pages;
5. preserves the returned writer DID;
6. sorts by `createdAt DESC, repo DID ASC, rkey ASC, CID ASC`;
7. returns explicit per-writer errors and `complete: false` on partial reads.

This is deliberately a bounded alpha implementation. A future private AppView
can replace synchronous fanout with the cursor/reconciliation interface in
`src/lib/atproto/spaces/sync.ts`, but that index cannot become an authorization
authority.

## Control-plane service auth

When the viewer's PDS differs from the Space authority PDS, the client mints a
short-lived `com.atproto.server.getServiceAuth` token with:

- `aud` equal to the Space authority DID; and
- `lxm` equal to the specific Radlib control method.

The fork accepts that token only on Radlib control routes and checks the
audience against the Space URI authority. Ordinary repo, blob, sync, and Space
methods never accept this token as a content credential.

## Lifecycle and revocation

- Public → protected creates/ensures the account Space and routes new private
  posts through it. Existing public posts are not migrated automatically.
- Protected → public changes future account policy but preserves the old Space
  and its private history. Any future destruction or selected publication must
  be a separate explicit operation.
- Leave, revoke, block, and ban remove Space membership before committing the
  Radlib state transition. New credential exchange then fails closed.
- The pinned alpha credential is self-contained; an already-issued credential
  may survive until expiry. This is an explicit acceptance gap, not a hidden
  claim of immediate token revocation.

## Legacy classification

| Surface | Disposition |
|---|---|
| Radlib visibility/follow/community policy | Keep as control plane. |
| Radlib list/create/join/leave/invite/ban/discovery | Keep as product semantics; Space ACL remains the content gate. |
| Radlib put/get/list/delete record transport | No active route or Spaces-mode client caller; legacy adapter is quarantined. |
| Radlib upload/get blob transport | No active route or Spaces-mode client caller; Space blob APIs are canonical. |
| Radlib feed/sync-grant transport | No active route or Spaces-mode client caller; cursor reconciliation is the replacement boundary. |
| `org.radlib.private.post` | Keep as a fork Lexicon collection, but only as a record stored inside a Space repo. |

The PDS control route constructs `RadlibPrivateDataStore` with
`mode: 'control'`. The legacy tables are only created when a future migration
adapter explicitly selects `mode: 'legacy'`.

## Security invariants

Private record and blob bytes must not enter public CAR export, public repo
sequencer events, Relay/Jetstream, public AppView responses, logs, or persisted
browser caches. The focused PDS harness covers public CAR, public sequencer,
ordinary sync blob, Space blob, cross-PDS, block, invite, ban, and discovery
canaries. A disposable external Relay/AppView scan remains a deployment-lane
acceptance task.
