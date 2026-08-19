# Permissioned Accounts and Communities — Implementation Review

**Status:** `RADLIB_CODEX_ACCEPTANCE_BLOCKED`
**Owner state:** `OWNER_ACCEPTANCE_PENDING`
**Branch:** `codex/private-accounts-communities`
**Starting root SHA:** `519a66e25389380935b2b008221135da57796408`
**Pinned PDS base:** `760fb12a080c87cdfd0dae42ae833bad8bc20886`
**Client checkout:** `c38bfe515a9d52d2b9969c8ead64eced5f8d33ee`

This records the first secure local implementation boundary. It does not claim
that the evolving upstream Permissioned Data/Spaces protocol, multi-PDS
federation, or a permissioned AppView is complete.

## Architecture decision

The fork now has two deliberately separate data planes:

| Plane | Storage and transport | Visibility |
|---|---|---|
| Public ATProto | Existing ActorStore/repository, public CAR, sequencer, `subscribeRepos`, Relay/AppView | Ordinary public records and blobs |
| Radlib permissioned adapter | Separate SQLite database and `0700` directory containing `0600` private blob files | Authenticated, current ACL only |

The private adapter is `RadlibPrivateDataStore`, behind the
`PermissionedSpaceAdapter` interface. It is mounted only when
`PDS_PERMISSIONED_DATA_ENABLED=true`. It has no dependency on `ActorStore`,
the public repository, the public sequencer, CAR export, or `subscribeRepos`.
Private record collections are reserved to `org.radlib.private.*`; the shared
public `prepareCreate`, `prepareUpdate`, `createRecord`, `putRecord`, and
`applyWrites` boundaries reject that namespace even if the feature is later
disabled. Public CAR import rejects non-delete writes in that namespace.

This remains a local private store rather than a custom replacement for public
ATProto repositories. The upstream proposal is still explicitly evolving: see the
[Permissioned Data proposal](https://github.com/bluesky-social/proposals/tree/main/0016-permissioned-data)
and the [current upstream implementation PR](https://github.com/bluesky-social/atproto/pull/5187).

The adapter uses the PDS's existing bearer/OAuth/DPoP verification boundary for
viewer operations. For cross-PDS use, the fork adds its own explicit capability
contract: an owner creates a hash-stored, collection-scoped, expiring grant for
one target PDS and actor, and that target pulls directly from the source PDS.
This is deliberately not presented as proposal-0016 credentials or a Relay
protocol. The pull response is ephemeral; it is not written to the public
repository or a public AppView index.

## Implemented foundation

### Protected-account policy and ACL

- `public` and `protected` account policy is persisted in a private database.
- Protected accounts receive a private account space controlled by the DID.
- Follow-request states include `none`, `requested`, `approved`, `denied`,
  `revoked`, and `blocked`.
- Request, approve/deny, cancel, remove-follower, and block-preserving
  transitions are transactional at the SQLite boundary.
- Account-space reads require the owner or a current `approved` request.
- Public profile data remains in the ordinary public profile path; changing to
  protected does not retroactively privatize old public records.

### Permissioned records and blobs

- `org.radlib.private.putRecord` writes only fork-owned private collections.
- `org.radlib.private.getRecord` and `listRecords` re-evaluate the ACL on every
  request; failed authorization returns not-found behavior.
- `org.radlib.private.uploadBlob` writes outside the public blob store with
  `0600` file permissions and size/MIME limits.
- `org.radlib.private.getBlob` performs an authenticated current ACL check and
  sends `Cache-Control: private, no-store` and `X-Content-Type-Options: nosniff`.
- Direct blocks authored by the private-record owner are checked again at the
  PDS API read boundary, so an old approval row cannot keep serving a blocked
  viewer.
- The generic write API does not accept `app.bsky.feed.post` in the private
  store; the private post schema is `org.radlib.private.post`.

### Private feed and direct PDS synchronization

- `org.radlib.private.getFeed` is an explicit PDS-local private feed. It fixes
  the collection to `org.radlib.private.post`, checks the current viewer ACL,
  rechecks direct blocks, and returns the actual hosting PDS DID as provider
  provenance.
- The client exposes the feed at `/private-feed` from the private-spaces
  settings surface. Its React Query root is excluded from persisted snapshots;
  the screen does not route through the public AppView or a Relay.
- `org.radlib.private.createSyncGrant` issues a 256-bit random bearer
  capability whose SHA-256 hash is stored. The grant names one target PDS DID,
  one target actor DID, an optional private collection, and an expiry no more
  than 30 days away. The raw token is returned only at creation.
- `org.radlib.private.syncPull` is a direct POST capability endpoint. Every
  pull checks the token hash, space, target PDS, target actor, collection,
  expiry, and revocation before returning records. `revokeSyncGrant` makes
  subsequent pulls fail immediately.
- The protocol intentionally does not create a durable target-side copy in
  this pass. A target service can consume the pull response directly, and
  revocation is therefore authoritative at the source on every request. No
  private record enters public CAR, `subscribeRepos`, Relay, or public AppView.

### Communities

- `public`, `restricted`, `invite-only`, and `private` visibility are stored in
  the same permissioned substrate.
- Public communities allow authenticated reads; restricted communities expose
  metadata but require approved membership for content; invite-only/private
  spaces require an invitation.
- Join, approve/deny, leave, one-time/high-entropy invite creation, atomic
  redemption, revocation, and community-local ban/unban are implemented.
- Invite secrets are returned once and stored only as SHA-256 hashes. Invite
  redemption uses a conditional SQL update, so a one-use token cannot create
  multiple memberships under a race.
- Private/invite-only metadata is not returned by `getSpace` to a non-member.
- Ban state is checked on every read/write; a ban immediately removes current
  application authorization. Private moderation reasons remain in the private
  database and a compact audit row records the action.
- The MVP uses the creator DID as the community authority. A dedicated
  community authority DID, role hierarchy, transfer, and multi-space authority
  migration remain future work.

## Actual implementation paths

| Concern | Paths |
|---|---|
| Adapter contract and private store | `upstream/atproto-pds/packages/pds/src/permissioned-data/adapter.ts`, `store.ts` |
| Config and flags | `upstream/atproto-pds/packages/pds/src/config/env.ts`, `config.ts`, `example.env` |
| PDS lifecycle | `upstream/atproto-pds/packages/pds/src/context.ts`, `src/index.ts` |
| Private XRPC | `upstream/atproto-pds/packages/pds/src/api/org/radlib/private/index.ts` |
| Private Lexicons | `upstream/atproto-pds/lexicons/org/radlib/private/*.json` |
| Public write boundary | `src/repo/permissioned-policy.ts`, `src/repo/prepare.ts`, public repo write APIs |
| CAR boundary | `src/api/com/atproto/repo/importRepo.ts` |
| Client generated types | `upstream/social-app/lexicons/org/radlib/private/*.json`, generated `src/lexicons/org/radlib/private/*` |
| Client policy and private composer | `upstream/social-app/src/state/queries/protected-account.ts`, `src/screens/Settings/components/ProtectedAccountToggle.tsx`, `PrivacyAndSecuritySettings.tsx`, `src/lib/permissioned-data.ts`, `src/view/com/composer/Composer.tsx` |
| Store/API/privacy tests | `upstream/atproto-pds/packages/pds/tests/private-permission-store.test.ts`, `private-permission-api.test.ts`, `permissioned-policy.test.ts`; `upstream/social-app/src/lib/permissioned-data.test.ts` |

## Privacy gates

| Gate | Result | Evidence boundary |
|---|---|---|
| P1 protected plaintext absent from public repository export | PASS for the adapter | Separate DB/blob path plus a body/blob-canary test that parses the public CAR and checks every block; a permissioned export/migration path is not implemented. |
| P2 absent from public firehose/Relay/AppView | PASS for the production-like local topology | Private writes never call public repo/sequencer code; the focused API test captures `subscribeRepos`, drains the real downstream AppView subscription, and checks AppView feed/search/profile responses and its `post` table for the canary. No private AppView or multi-PDS federation is claimed. |
| P3 private blobs deny unauthorized access | PASS | Store ACL/blob test and private response headers. |
| P4 unauthorized direct lookup fails closed | PASS for private XRPC | `getRecord`/`getBlob` return not-found behavior; auth success and failure responses are `private, no-store` and vary on `Authorization, DPoP`; no public AppView private lookup exists. |
| P5 global public search has no private records | PASS structurally | No private records are indexed in public tables or public APIs; private search is not implemented. |
| P6 private feeds are viewer-authorized | PASS for PDS-local private feed | `org.radlib.private.getFeed` fixes the private-post collection, re-checks the current viewer ACL and direct block boundary, returns provider DID provenance, and is hydrated by the client `/private-feed` screen. This is intentionally not a public AppView/indexer. |
| P7 revocation blocks later access | PASS locally | Approved-follower revocation, community leave, and ban tests re-read after transition. |
| P8 blocking invalidates account-space access | PARTIAL | PDS owner-block lookup is applied to private API reads; end-to-end direct-block integration is not yet exercised in a live multi-account harness. |
| P9 hidden communities do not leak discovery metadata | PASS locally | `getSpaceForViewer` returns null to non-members for private/invite-only spaces; tests cover membership ACL. |
| P10 multi-PDS authorized federation without public Relay | PASS for the fork direct-pull contract | Owner-scoped `createSyncGrant`/`syncPull`/`revokeSyncGrant` provide direct PDS-to-PDS pulls without public Relay/CAR/AppView participation. The grant is hash-stored, target-PDS/actor-bound, collection-scoped, expiring, and checked on every pull. Proposal-0016 space credentials and durable replica/import semantics remain separate future interoperability work. |
| P11 logs and client persistence do not retain private values | PASS for local PDS/client paths | PDS request serialization redacts private URL/query/route identifiers; private React Query roots are excluded from persisted snapshots; private responses are explicitly `no-store`. External proxy/CDN logs and multi-device cache behavior remain deployment-specific and are constrained by that response contract. |

The feature is therefore **NO-GO for owner acceptance** as a complete private
social product. It is a real privacy boundary and useful PDS foundation, but
not yet the full protected-account/community product requested by the target
scenario.

## What is deliberately not claimed

- The current Bluesky public composer still writes ordinary public records.
  Protected-account users now have an explicit, text-only private-post mode in
  the composer. It calls `org.radlib.private.putRecord` and never calls the
  public post writer. Public composition remains an explicit separate mode.
- Private media composition, private thread/quote/repost/like semantics,
  private notifications, private search, and a viewer-aware private AppView
  are not complete.
- Proposal-0016 space credentials, DPoP-bound space credentials, durable
  permissioned replica/import, and a viewer-aware private AppView are not
  complete. The fork's direct capability-pull contract is implemented, but is
  intentionally a fork namespace rather than a claim of upstream protocol
  compatibility.
- Public community discovery is intentionally conservative. There is no global
  community index yet; `getSpace` is an authenticated local operation.
- E2EE is not provided. The adapter is authenticated access control with server
  plaintext, not end-to-end encryption.

These are implementation gaps, not claims that public ATProto services support
the fork's private protocol automatically.

## Commands and results

From `upstream/atproto-pds/packages/pds`:

```sh
./node_modules/.bin/lex build --clear --indexFile --lexicons ../../lexicons
../../node_modules/.bin/tsc --build tsconfig.build.json --pretty false
NODE_OPTIONS=--experimental-vm-modules \
  ../dev-infra/with-test-redis-and-db.sh ../../node_modules/.bin/jest --runInBand \
  tests/private-permission-api.test.ts tests/private-permission-store.test.ts \
  tests/permissioned-policy.test.ts tests/sync/subscribe-repos.test.ts \
  tests/logger.test.ts
NODE_OPTIONS=--experimental-vm-modules \
  ../../node_modules/.bin/jest --runInBand \
  tests/moderation-policy.test.ts tests/radlib-migration.test.ts
```

Latest private-boundary result after adapter hardening: **5 suites, 31 tests
passed** for the private API/store/policy, direct sync, public sync, and logger
redaction. The PDS TypeScript build passed. The client persistence/privacy
regression passed (**2 suites, 4 tests**) and the client web TypeScript check
passed. The production web export
also exited successfully, with the checkout's existing optional
`ContactAccessButtonProps` and `expo-router` resolution warnings plus normal
bundle-size warnings.

The exact local audit command is:

```sh
cd /var/home/tcs/Code/atproto/upstream/atproto-pds/packages/pds
NODE_OPTIONS=--experimental-vm-modules ../../node_modules/.bin/jest --runInBand \
  tests/private-permission-api.test.ts tests/private-permission-store.test.ts \
  tests/permissioned-policy.test.ts tests/sync/subscribe-repos.test.ts \
  tests/logger.test.ts

cd /var/home/tcs/Code/atproto/upstream/social-app
NODE_ENV=test node_modules/.bin/jest --runInBand \
  src/state/queries/util.test.ts src/lib/permissioned-data.test.ts
```

This closes the implemented PDS-local private-feed and direct-pull portions of
P6/P10 as well as the local PDS/client portion of checklist item 60. It does
not replace a proposal-0016 private AppView, durable cross-PDS replica/import,
external proxy/CDN cache, or multi-device cache harness.

The local web command remains the owner checklist command in
`docs/OWNER_ACCEPTANCE_CHECKLIST.md`. Enable the PDS foundation explicitly in
a disposable deployment with:

```sh
PDS_PERMISSIONED_DATA_ENABLED=true
PDS_PROTECTED_ACCOUNTS_ENABLED=true
PDS_COMMUNITIES_ENABLED=true
PDS_PRIVATE_COMMUNITIES_ENABLED=true
PDS_PERMISSIONED_DATA_DIRECTORY=data/permissioned
```

The live web process was restarted after regenerating the client lexicons and
then rechecked at `http://127.0.0.1:19006/settings/privacy-and-security`.
Webpack reported `web compiled with 2 warnings` (the existing optional
`expo-contacts` and Sentry router-store warnings); the rendered page had no
compile overlay and accurately reported that protected accounts are
unavailable because the long-running dev PDS is not currently flag-enabled.
The live first-party PDS (`2583`) and AppView (`2584`) remained running and
responded during this check. This is a server/browser verification, not a
flag-enabled private-account walkthrough.

Do not enable this in production until private-post composition, private
AppView authorization, migration, and the missing privacy gates are complete.

## Follow-up required before owner acceptance

1. Extend the text-only permissioned composer with private media through the
   private blob API, then add private thread/embed semantics.
2. Add protected profile/read states, follow-request UI, private thread/feed
   hydration, and viewer-partitioned caches.
3. Add private community UI, community feed, membership moderation, and
   hidden discovery/search behavior.
4. Vendor or wire the evolving Spaces implementation, including delegation,
   DPoP-bound credentials, direct sync, and two-PDS tests.
5. Add private export/import/migration and explicit credential regeneration.
6. Run the live owner checklist; do not change its owner-result fields by
   automation.
