# Viewer-Sovereignty Architecture

Status: implemented in the current fork; owner acceptance remains
`OWNER_ACCEPTANCE_PENDING`.

Audited bases:

- root contract checkout: `519a66e25389380935b2b008221135da57796408`;
- first-party PDS/AppView source: `760fb12a080c87cdfd0dae42ae833bad8bc20886`;
- social-app source: `c38bfe515a9d52d2b9969c8ead64eced5f8d33ee`.

The first-party read service in this repository is the forked
`upstream/atproto-pds/packages/bsky` package (`@atproto/bsky`, `BskyAppView`).
AppViewLite and FishyFlip are retired and are not runtime dependencies. The
client does not silently substitute `api.bsky.app` or another stock AppView.

## Authority layers

The fork keeps these questions separate:

```text
public record exists
    -> selected AppView can serve it
    -> viewer chooses local presentation
    -> viewer may or may not be authorized to interact
    -> author may curate their own preferred conversation
```

### Public read policy — TECHNICAL / INTEROPERABILITY

The selected AppView is an explicit provider record with a DID, service
fragment, endpoint, health path, and enabled state. Authenticated XRPC reads
use a PDS-issued service-auth token whose audience is that provider DID and
whose `atproto-proxy` value names that provider. Public reads use the same
configured AppView URL without an authenticated session. Repository writes,
identity operations, CAR operations, and recovery remain on the account PDS.

Implementation:

- `upstream/social-app/src/env/common.ts` — neutral AppView and labeler
  configuration;
- `upstream/social-app/src/state/session/providers.ts` — provider identity,
  validation, health, selection, and explicit fallback registry;
- `upstream/social-app/src/state/session/clients.ts` — PDS/AppView client
  separation and service-auth routing;
- `upstream/social-app/src/lib/api/feed/custom.ts` — configured public AppView
  for logged-out custom-feed reads;
- `upstream/atproto-pds/packages/bsky/src/index.ts` — first-party AppView
  server implementation.

If the configured provider is unavailable, the UI names that provider and
offers only a provider explicitly registered by the user/operator. There is no
request-time substitution that preserves the failed provider's name.

The account entryway (`EXPO_PUBLIC_ACCOUNT_SERVICE`, defaulting to the
compatible `bsky.social` entryway) is used only for login and handle
availability. It is not the AppView read authority.

### Interaction policy — NORMATIVE / PRODUCT POLICY

Direct blocks are individually authored relationship boundaries. A current
viewer-authored direct block can restrict that viewer's direct interaction and
the fork's ordinary local presentation of the blocked actor. An incoming
external direct block remains a hard interaction boundary where the protocol
requires it. Neither direction grants an unrelated viewer universal authority
over a public record.

`app.bsky.graph.listblock` remains a standard readable compatibility record but
is behaviorally inert in the first-party policy path. List mutes remain private
attention state. This preserves standard records and CAR compatibility without
turning a mutable list into thousands of durable direct blocks.

### Author curation policy — PRODUCT POLICY / NORMATIVE

`app.bsky.feed.threadgate.hiddenReplies` and threadgate rule violations remain
indexed metadata. They can affect an author's preferred conversation view,
notifications, and reply authorization. They do not erase an independently
published public reply from the fork's public-reference graph.

The social-app default is `Everyone's replies` (`threadCurationView: all`).
`Author's curation` is an explicit local view and may honor the author's
hidden-reply request. A hidden public reply is annotated as author curation,
not represented as universally deleted. Descendants remain in the public graph
and deleted, suspended, taken-down, or nonexistent records remain unavailable.

The PDS/AppView implementation is in
`upstream/atproto-pds/packages/bsky/src/views/index.ts` and the aggregate/index
path in `packages/bsky/src/data-plane/server/indexing/plugins/post.ts`.
The client preference and mode split is in:

- `upstream/social-app/src/state/queries/preferences/useThreadPreferences.ts`;
- `upstream/social-app/src/state/queries/usePostThread/index.ts`;
- `upstream/social-app/src/screens/PostThread/components/HeaderDropdown.tsx`;
- `upstream/social-app/src/screens/Settings/ThreadPreferences.tsx`.

### Quote and postgate policy — PRODUCT POLICY / INTEROPERABILITY

`app.bsky.feed.postgate.detachedEmbeddingUris` is an advisory author request
for the fork's public-read presentation. It does not delete or detach a public
quote relationship for unrelated viewers. The normal public embedded post is
retained while the source remains available. Deletion, takedown, suspension,
missing bytes, and direct viewer interaction boundaries remain authoritative.

The implementation is in `Views.recordEmbed()` and its postgate callers in
`upstream/atproto-pds/packages/bsky/src/views/index.ts`; regression coverage is
in `upstream/atproto-pds/packages/bsky/tests/postgates.test.ts` and quotes
tests.

### Viewer moderation policy — PRODUCT POLICY / PRIVACY

Ordinary labelers provide information and recommendations. The client keeps
label provenance and applies the viewer's Show/Warn/Hide preference. The
viewer-sovereign adapter is centralized in
`upstream/social-app/src/lib/moderation.ts` and is used by the client
moderation call sites.

The adapter may make an ordinary custom label that stock behavior marked
`no-override` viewer-configurable. It does not weaken system/takedown labels,
adult-safety boundaries, direct blocks, service-unavailable states, deleted
records, or infrastructure restrictions. An unavailable record cannot be
created by choosing Show.

Global labelers are empty unless `EXPO_PUBLIC_DEFAULT_LABELER_DIDS` explicitly
configures them. Account-selected labelers remain supported, and provenance is
preserved in all three ordinary presentation modes.

### Infrastructure availability — SECURITY / INTEROPERABILITY

The fork does not represent a service refusal as a normal moderation label.
PDS/AppView failures, deletion, suspension, takedown, malware/security
enforcement, unavailable blobs, and legal hosting restrictions remain
unavailable. The client reports the actual failing service and does not claim
that a local preference bypassed it.

### Identity and privacy limitations — SECURITY / PRIVACY

Changing a handle on a `did:plc` identity requires acknowledgement that the
handle rename does not create a new identity and that PLC history may retain
prior handles and PDS locations. A genuinely separate pseudonym requires a
separate account/DID. A PDS move, a handle rename, or a did:web handle does not
promise cryptographic unlinkability. Browser, network, operator, reused
content, and behavioral metadata may still correlate accounts.

The warning and acknowledgement gate are implemented in
`upstream/social-app/src/screens/Settings/components/ChangeHandleDialog.tsx`.

Handle and URI resolution is now a separate read capability from feed/profile
AppView selection. `upstream/social-app/src/state/queries/resolve-uri.ts`
collects claims from every enabled identity-capable provider through public
clients, validates the DID-method PDS endpoint, and applies the local
agreement/preference policy. Disagreement and unavailable resolvers remain
visible evidence; they are not silently converted into a canonical DID. The
decision record and flow are in
[`docs/ANARCHISTIC_PROVIDER_COMPOSITION_DECISION.md`](ANARCHISTIC_PROVIDER_COMPOSITION_DECISION.md)
and
[`docs/flow-diagrams/provider-claim-reconciliation.mmd`](flow-diagrams/provider-claim-reconciliation.mmd).

## Standard records and compatibility

The fork retains standard records and wire formats for:

- `app.bsky.graph.block`, list, listitem, listblock, and list mute records;
- `app.bsky.feed.threadgate` and `app.bsky.feed.postgate`;
- ordinary ATProto moderation labels;
- public repository/CAR export and import.

The fork-specific behavior is a service/client policy layer over those records,
not a replacement Lexicon dialect. Raw records remain available for standard
clients and reindexing. This is an INTEROPERABILITY decision, not a claim that
ATProto itself requires the normative policy.

## Rebase guardrails — TECHNICAL / SECURITY

Before accepting upstream changes, audit these symbols and follow their data
flow to a behavioral sink:

```sh
rg -n 'viewerBlockExists|blockedBy|blockingByList|blockedByList|listblock|hiddenReplies|violatesThreadGate|detachedEmbeddingUris|noOverride|no-override|BLOCK_BEHAVIOR' \
  upstream/atproto-pds/packages upstream/social-app/src
```

Compatibility occurrences are allowed. Flag any new use that makes an
unrelated actor's block/list, an author curation signal, a labeler judgment, or
a postgate request an unconditional public-read predicate. Keep the explicit
names `viewerHidesActor`, `viewerIsBlockedByActor`, `interactionBlocked`,
`serviceContentUnavailable`, and `viewerLabelPreference` at policy boundaries.

## Phase verdicts

These are automated implementation verdicts, not owner acceptance:

| Phase | Automated result | Evidence boundary |
|---|---|---|
| Independent AppView routing | PASS | Client routing/provider tests; a current-fork live AppView deployment still needs the owner walkthrough. |
| Viewer-sovereign labels | PASS | 11 focused moderation/provider tests; service-unavailable remains separate. |
| Hidden replies | PASS | Public/author-curated PDS thread tests and client mode split. |
| Quote detachment | PASS | Postgate/quote regression tests retain available public embeds. |
| Threadgate model | PASS | Rule and descendant tests retain public references and preserve notification gating. |
| DID privacy UX | PASS | Typechecked warning/acknowledgement path; owner should exercise both DID methods. |
| Block regression | PASS | Existing directional A/B/C suites remain green. |
| Listblock regression | PASS | Existing inert-listblock and list-mute suites remain green. |

The overall product remains `RADLIB_CODEX_ACCEPTANCE_BLOCKED` until the
remaining live/provider and owner checks are completed. It is not
`OWNER_ACCEPTANCE_PASSED`.
