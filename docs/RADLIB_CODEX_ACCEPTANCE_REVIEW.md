# Radical-Liberal Codex Acceptance Review

State: `RADLIB_CODEX_ACCEPTANCE_BLOCKED`
Owner state: `OWNER_ACCEPTANCE_PENDING`
Review date: 2026-08-19

> Historical/superseded report. This 2026-08-19 review is not the current
> release verdict. Current alpha/staging evidence is bound by
> `artifacts/oauth-spaces-manifest.json` and its current receipts. The current
> public host is `https://radlib.edriffles.us` under the existing `edriffles.us`
> registrable domain, and the protocol namespace is `us.edriffles.radlib.*`.
> DNS authority and the single-host edge route remain pending; no `radlib.org`,
> `edriffles.radlib`, or second registrable domain is required. Older host and
> namespace strings below are historical snapshots, not current configuration.

This is an implementation and verification report, not owner acceptance. It
records actual repository, PDS, client, fixture, browser, and provider-boundary
evidence. AppViewLite is retired and is not a current product dependency.

## Repository SHAs inspected

| Component | SHA | Current role |
|---|---|---|
| parent repository | `79c8327` | reviewed parent before this final documentation commit; owner acceptance remains pending |
| `upstream/social-app` | `3dff4b0d4201b001ec5e85c83ccacffd5970bd2c` | client, provider registry, UI, local attention |
| `upstream/atproto-pds` | `c1a8b80f06029bdbadae59ff7f517da25163e96f` | first-party PDS, repo writes, CAR/import policy |

The old AppViewLite and FishyFlip gitlinks/pins were removed. Their existing
dirty nested checkouts were preserved as local archives rather than deleted;
they are outside the parent dependency graph and are not supported launch or
test targets. See `docs/APPVIEWLITE_RETIREMENT.md`.

## Compile repair and current live browser walk-through

The reported Webpack overlay (`Module not found: Can't resolve './'`) was a
real source-resolution defect in the nested moderation modules. Webpack was
resolving `#/lib/moderation` from inside `src/lib/moderation/` as the directory
itself instead of the sibling `src/lib/moderation.ts`. The four affected files
now import `../moderation` explicitly:

- `upstream/social-app/src/lib/moderation/create-sanitized-display-name.ts`
- `upstream/social-app/src/lib/moderation/useLabelBehaviorDescription.ts`
- `upstream/social-app/src/lib/moderation/useLabelInfo.ts`
- `upstream/social-app/src/lib/moderation/useModerationCauseDescription.ts`

The running Webpack server returned HTTP 200, the browser reload rendered
without the compile overlay, and the focused client lint/tests remained green.
The clean authenticated live walkthrough used the local web origin
`http://127.0.0.1:19006/` after signing into the disposable Alice fixture. It
rendered separate `Discover` and `Following` choices. The project feed
record and provider response were HTTP 200 and carried:

```text
AppView DID: did:plc:dw4kbjf5mn7nhenabiqpkyh3
Feed provider DID: did:plc:3yyddqsbp64qbnelcev36sey
Feed owner DID: did:plc:tgdhu5j5on7rokehpgyzcben
Feed URI: at://did:plc:tgdhu5j5on7rokehpgyzcben/app.bsky.feed.generator/social-discover
Provider context: local disposable feed-generator fixture; algorithm/version
and public objective are not declared
```

The UI labels the manifest as unverified and the objective as undeclared; it
does not turn provider-supplied context into a verified constitutional claim.
The current fixture contains deterministic local posts, not a populated
production corpus. Provider endpoint health is verified separately; the card
honestly reports `Service health unknown` because no signed health claim is
present in the feed response.

The final local fixture repair also registers a real second feed-generator
record at `app.bsky.feed.generator/social-discover` in
`upstream/atproto-pds/packages/dev-env/src/mock/index.ts`. It shares the
disposable provider's registered handler with the upstream sample feed, so a
fresh local account can exercise separate `Following` and `Discover` tabs
without pointing at Bluesky's operator feed. The old `radlib-discover` record
remains only as a compatibility alias. This is fixture wiring, not a claim
that a production deployment has a populated corpus.

### Latest local Bluesky-compatibility walkthrough

After the fixture restart, the local PDS/AppView pair was healthy on ports
2583/2584 and retained AppView DID
`did:plc:dw4kbjf5mn7nhenabiqpkyh3`. The disposable PDS regenerated Alice as
`alice.test` (`did:plc:tgdhu5j5on7rokehpgyzcben`) and registered the local
`social-discover` feed. The browser walkthrough used the local account and
confirmed the ordinary Bluesky surface remains present: Home, chronological
Following, a separate custom feed, profiles, posts, replies, repost/quote,
likes, bookmarks, feed selection, notifications, and settings. The rendered
custom-feed cards still expose the normal interaction controls; radical-
liberal behavior is an attention/relationship policy layer rather than a
replacement for the social client.

The earlier remote `edriffles.us` session correctly showed the selected local
AppView as unavailable because that disposable AppView did not index the
remote account. That was a service-capability mismatch, not a silent fallback
or an identity failure. The local `alice.test` session is the faithful
integrated walkthrough for this checkout.

After the final client restart, a read-only wire smoke pass against the same
local AppView returned HTTP 200 for `getProfile`, `getFeed`, `getAuthorFeed`,
`getPostThread`, `getQuotes`, `getLikes`, `getRepostedBy`, and `searchPosts`.
The project feed returned five posts. This verifies the ordinary Bluesky read
surface at the API boundary in addition to the rendered walkthrough; it does
not turn the disposable fixture into a populated production network.

The live notification route was also checked as the signed-in `edriffles.us`
account. The selected Project AppView returned HTTP 401 with `identity unknown`
because this fresh local provider does not index that remote DID. The client
now catches the background unread-poll rejection, removes the Lex fetch wrapper
from the foreground message, names the actual AppView provider, and avoids the
misleading `No notifications yet!` state. It does not silently substitute
Bluesky or another AppView: notification data for this remote account remains
unavailable until an explicitly selected provider that indexes the account is
used. This is provider-capability evidence, not evidence that the account
credentials are invalid.

### Latest service-auth repair

The owner screenshot's `Service-auth issuance failed: HTTP 400` was traced to
an older hosted session whose persisted entryway (`bsky.social`) was being used
as though it were the account PDS. The account DID document for
`edriffles.us` resolves to `did:plc:3ijrhre2q5e4tt2f4ph2sneo` and declares
`https://yellowfoot.us-west.host.bsky.network` as its PDS. The client now
resolves that route before resuming a hosted session that has no persisted PDS
route, seeds the password session with it, and uses it for service-auth,
repository, and refresh operations.

The focused client/session regression set passes (3 suites, 70 tests), and a
live local Alice check proved the same boundary end to end: service-auth was
minted by the local PDS for the selected local AppView and the authenticated
Following request returned HTTP 200. A provider rejection is now attributed
to the actual account PDS and selected provider. The raw PDS access token is
never sent to the AppView.

The current Webpack server is healthy at `http://127.0.0.1:19006/` and the
bundle has no compile overlay. The in-app browser could not be programmatically
refreshed after this patch because its local-navigation policy rejected the
refresh action; therefore this report does not claim a post-patch screenshot.
The remote account still cannot be displayed by the disposable local AppView
until that explicitly selected provider indexes the account; silently showing
Bluesky's AppView would violate provider provenance.

### Feeds-screen provider repair

The Feeds screen had a separate failure mode: `app.bsky.unspecced.getPopularFeedGenerators`
was sent through the signed-in AppView client, so a provider that could serve
public feed metadata but could not index the current remote viewer produced an
`AppView provider ... is unavailable` banner. Feed metadata reads now retry
without viewer credentials against the same selected provider. Saved and
pinned feed metadata use the same boundary. A failed public retry still
surfaces the selected provider failure; no other AppView is substituted.

On the local fixture, the unauthenticated provider API returned HTTP 200 for
both `getPopularFeedGenerators` and `getFeedGenerator` for the configured
`social-discover` URI. The client adds that deployment-owned feed to the
discovery result when the provider exposes it, keeping it distinct from
Bluesky's operator Discover feed. The fallback helper has deterministic
success, retry, and double-failure tests; the web typecheck and production
export pass.

## Active implementation map

| Principle | Implementation | UI/provider surface | Test/evidence |
|---|---|---|---|
| Individually authored hard block | `src/state/queries/profile.ts`, `useDirectBlockMutation`; PDS standard block record | Profile block and Review accounts | `tests/test_moderation_list_policy.py`, A/B/C fixture |
| List mute versus review | `src/state/queries/list.ts`, `ProfileList/components/SubscribeMenu.tsx`, `ReviewListMembersDialog.tsx` | “Mute list” and “Review accounts”; no bulk listblock mutation | `tests/test_provider_boundary_contract.py` |
| Local listblock write boundary | `packages/pds/src/repo/moderation-policy.ts`, `repo/prepare.ts`, create/put/apply APIs | Explicit policy error; delete remains available for legacy cleanup | PDS focused tests and bypass guard |
| Inert listblock data plane | `packages/bsky/src/data-plane/server/routes/{relationships,blocks}.ts`, `hydration/{actor,graph,hydrator}.ts`, `views/index.ts`, `api/app/bsky/graph/getListBlocks.ts` | Raw records remain readable, but effective relationships, block existence, hydration, listblock RPCs, profiles, feeds, threads, search, notifications, embeds, and chat do not treat listblock as block state | `tests/views/block-lists.test.ts` 6/6; listblock thread regressions 2/2; list-mute suite 22/22; broader 10-file run 229/229 |
| CAR-compatible migration | `packages/pds/src/api/com/atproto/repo/importRepo.ts`, `repo/radlib-migration.ts` | Import status and pre-activation gate | import/migration fixtures and live walkthrough |
| Provider-side mute attestation | `packages/pds/src/repo/radlib-attestation.ts`, `api/org/radlib/moderation/recordListMuteAttestation.ts` | Provider capability is explicit; PDS verifies a signed claim | `scripts/radlib_live_provider_walkthrough.mjs` |
| Attention sovereignty | `src/lib/feed-sovereignty`, `src/lib/balanced.ts`, `src/lib/personalization.ts`, `src/components/PostControls/PostVoteButtons.tsx`, `src/screens/Settings/PersonalizationSettings.tsx` | Following/chronological access, Balanced, custom feeds, six attention controls, explicit topic/author policy, local curation controls, compact grouped More/Less controls, explanations | personalization/ranking tests, social-app typecheck/lint, browser settings/feed smoke |
| Portable personalization | `src/lib/personalization.ts`, settings UI | inspect/export/reset/import; secrets excluded | personalization tests and root secret audit |
| Replaceable services | `src/state/session/providers.ts`, `clients.ts`, PDS service-auth | explicit provider identity/health/fallback | provider tests and generic boundary test |
| Political neutrality | constitutional ranking/configuration and opt-in local content policy | no mandatory ideological or demographic quota | neutrality audit and fixture tests |
| Bluesky clone compatibility | `src/view/screens/Home.tsx`, `src/state/queries/feed.ts`, notification/profile/post routes, and the first-party PDS | standard social primitives remain usable; Following is chronological and custom feeds are separate, while radical policy stays in local attention/relationship layers | local Alice browser walkthrough; root/client/PDS suites |
| Pairwise thread and quote visibility | `src/state/queries/usePostThread/blocked.ts`, `usePostThread/index.ts`, `src/state/queries/post.ts`, `src/components/Post/Embed/index.tsx`, `src/state/queries/public-visibility.ts` | provider tombstones caused by unrelated actors are automatically hydrated; viewer-authored direct blocks remain hard; incoming/list boundaries do not erase public context; list-only state does not disable ordinary post controls | `blocked.test.ts`, `public-visibility.test.ts`, live quote/thread browser check |

## Findings by severity

| Severity | Result | Finding |
|---|---:|---|
| P0 | 0 | No critical safety or credential-boundary defect found. |
| P1 | 0 | Clear implementation failures in direct-block separation, preference authority, fallback provenance, credential exclusion, and attestation were repaired in the reviewed path. |
| P2 | 2 | Live owner walkthroughs remain for a populated alternate provider and resolver/labeler failure behavior; these are not silently claimed as passed. |
| P3 | 1 | Some advanced replacement and migration controls remain deliberately discoverable in settings rather than Home. |

The review remains blocked because the remaining live owner questions are not
substituted with documentation and the working tree contains intentional
uncommitted owner changes. An independent verifier completed a read-only pass,
confirmed P0=0 and P1=0, and its two retirement findings were repaired here;
the alternate-provider and resolver/labeler walkthroughs remain owner work.
This does not mark the owner result as failed.

## Association and A/B/C result

The deterministic Alice/Bob/Charlie fixture confirms:

- Alice’s direct block is a durable pairwise boundary.
- Alice’s list mute is attention state and creates no direct blocks.
- Explicit review creates ordinary `app.bsky.graph.block` records only for
  selected accounts.
- Charlie retains independent profile, thread/reply, quote, author-feed,
  search, and home/recommendation visibility where the upstream service makes
  those records available.
- Incoming direct block state remains an interaction boundary, but it is
  deliberately read-through for public records in this client; local and
  incoming `listblock` state is inert and is neither a content boundary nor an
  outgoing universal block.
- The new AppView fixture keeps raw listblock records readable while returning
  no effective listblock subscription, no list-derived relationship fields,
  no block-existence state, and no listblock result from `getListBlocks`.
- Provider tombstones caused by a relationship between two other actors are
  automatically hydrated through `app.bsky.feed.getPosts`, so the viewer sees
  both who a reply is responding to and what that parent or quoted post said.
  This is not a click-through and does not write a block, mute, listblock, or
  other relationship. A hydrated post is still withheld when its author’s
  viewer state proves that the current viewer authored a direct block.

The matrix separates `PAIRWISE`, `COLLATERAL-BUT-UPSTREAM-REQUIRED`,
`COLLATERAL-LOCAL-BUG`, `UNSUPPORTED`, and `UNTESTED`. No avoidable local
collateral suppression was found in the repaired client/PDS path.

### Directional blocking implementation audit

The server-side visibility split is implemented at these exact boundaries:

| Concern | Code path | Directional rule |
|---|---|---|
| Viewer-authored content hide | `upstream/atproto-pds/packages/bsky/src/views/index.ts` (`viewerHidesActor`) | Only the current viewer's direct `app.bsky.graph.block` URI hides public content. A list-derived URI is not a hard visibility predicate. |
| Incoming relationship | `upstream/atproto-pds/packages/bsky/src/views/index.ts` (`viewerIsBlockedByActor`) | Only direct `blockedBy` remains interaction metadata; listblock-derived fields are never populated by the first-party path. |
| Interaction gate | `upstream/atproto-pds/packages/bsky/src/views/index.ts` (`interactionBlocked`) | Direct and incoming direct hard boundaries remain available to interaction paths; listblock cannot gate interaction. |
| Thread, reply, and embed presentation | `upstream/atproto-pds/packages/bsky/src/views/index.ts` (`replyRef`, `threadParent`, `threadReplies`, V2 thread, `recordEmbed`) | Third-party relationships no longer produce blocked tombstones or detached public embeds; direct viewer blocks still do. |
| Feed/search/quote filtering | `packages/bsky/src/api/app/bsky/feed/{getAuthorFeed,getQuotes,getListFeed}.ts`, suggestion endpoints, and `getList.ts` | The list owner or another actor cannot filter an unrelated viewer's public records. Current-viewer direct blocks and mutes remain filters. |
| Legacy aggregate removal | `upstream/atproto-pds/packages/bsky/src/hydration/{graph,hydrator}.ts` | Dead bidirectional/post/follow/like block hydration was removed so no unused third-party aggregate can be accidentally consumed as visibility state. |
| API moderation presentation | `upstream/atproto-pds/packages/api/src/moderation/{decision.ts,subjects/account.ts,subjects/post.ts}` | List-derived causes are no-ops and only an `app.bsky.graph.block` URI can create a blocking cause; they no longer become local visibility or interaction causes. |
| Client fallback authority | `upstream/social-app/src/state/queries/public-visibility.ts`, `usePostThread/index.ts`, `post-quotes-fetch.ts`, `lib/api/feed/author.ts` | Public recovery rechecks each recovered author through authenticated relationship state; incoming/list-only recovery is allowed, and a direct URI is required before failing closed. |

The current deterministic classification is:

| Surface/effect | Classification | Evidence |
|---|---|---|
| Current viewer's direct block hides that actor's public posts and author feed | `PAIRWISE` | `blocks.test.ts`, `author-feed.test.ts`, client direct-boundary tests |
| Incoming external direct block restricts direct interaction/notifications | `PAIRWISE` | `notifications.test.ts`, `profileViewer` interaction state |
| Local or incoming `listblock` membership changes no public surface or relationship state | `UNSUPPORTED` as a block feature; raw record remains readable | `tests/views/block-lists.test.ts`, data-plane relationship/block RPC audit |
| Alice/Bob relationship changes what unrelated Charlie sees | `COLLATERAL-LOCAL-BUG` (repaired; 0 remaining) | 28-case block matrix, 90 thread-v2 tests, quotes/list-feed/search/follows suites |
| Provider tombstone for a relationship between other actors | `COLLATERAL-BUT-UPSTREAM-REQUIRED` at the provider boundary; client automatically hydrates public records | `usePostThread/blocked.test.ts`, live quotes route |
| Chat/direct eligibility | `PAIRWISE` interaction restriction; public post visibility is unaffected | client `isBlockedOrBlocking` paths and interaction tests |
| Private/permissioned records, takedowns, deletion, suspension, threadgates | `UNSUPPORTED` for public read-through and still authoritative | existing service/visibility contracts; no bypass was added |
| Surfaces not exposed by the selected provider | `UNTESTED` rather than inferred | owner checklist explicitly retains the live walkthrough requirement |

### Fully inert listblock verification

The follow-up audit found and repaired a concrete remaining mismatch: the
earlier directional implementation still joined `list_block` into data-plane
relationship/block-existence queries and exposed listblock subscriptions to
older RPC callers. The repaired paths are:

- `upstream/atproto-pds/packages/bsky/src/data-plane/server/routes/relationships.ts`:
  listblock rows are excluded from `getRelationships()` and
  `getBlockExistence()`.
- `upstream/atproto-pds/packages/bsky/src/data-plane/server/routes/blocks.ts`:
  `getBidirectionalBlockViaList()`, `getBlocklistSubscription()`, and
  `getBlocklistSubscriptions()` return empty/no-block compatibility answers.
- `upstream/atproto-pds/packages/bsky/src/hydration/{actor,graph,hydrator}.ts`:
  listblock fields are not hydrated; `list_mute` remains hydrated separately.
- `upstream/atproto-pds/packages/bsky/src/views/index.ts` and
  `api/app/bsky/graph/getListBlocks.ts`: listblock cannot become a profile,
  feed, thread, notification, search, embed, or list-block view effect.
- `upstream/atproto-pds/packages/api/src/moderation/subjects/{account,post}.ts`:
  only the direct block collection is accepted as a block URI, even if a
  remote provider sends a list URI in the shared `blocking` field.
- `upstream/social-app/src/state/queries/public-visibility.ts` and the DM
  components: the client requires the direct block collection and no longer
  exposes the dead listblock DM dialog/action.

The deterministic fixture proves: raw repository readability, no effective
listblock subscription, no relationship/block-existence fields, profile,
post, thread, quote, author-feed, timeline, search, typeahead, suggestion,
and notification access, independent direct-block behavior, and continued
list-mute filtering. The focused inert/list-mute result was 3 files and 30
tests passed; the dedicated block-list and thread fixtures also run in the
broader regression command below.

The focused server regression run after this repair was:

```sh
cd /var/home/tcs/Code/atproto/upstream/atproto-pds/packages/bsky
../dev-infra/with-test-redis-and-db.sh pnpm --pm-on-fail=ignore exec vitest run \
  tests/views/block-lists.test.ts tests/views/thread.test.ts \
  tests/views/thread-v2.test.ts tests/views/quotes.test.ts \
  tests/views/list-feed.test.ts tests/views/notifications.test.ts \
  tests/views/likes.test.ts tests/views/author-feed.test.ts \
  tests/views/follows.test.ts tests/views/mute-lists.test.ts
```

Result: 10 files, 229 tests passed. The API moderation behavior suite passed
67 tests with `NODE_OPTIONS=--experimental-vm-modules`; the client boundary
suite passed 2 files and 12 tests in the final rerun, with the earlier DM
boundary run also green. Web typecheck, changed-file oxlint, and the
production web export passed. These results characterize the implementation;
they do not replace the owner's live judgment.

## Explicit preference precedence

The documented deterministic precedence is:

```text
explicit negative/positive preference
  > explicit topic/person preference
  > inferred interest and social affinity
  > freshness/novelty and bounded exploration
  > generic engagement
```

Freshness, structural variety, and exploration remain bounded tie-breakers and
cannot override an explicit negative. Deterministic fixtures prove that a
strong `Less like this` lowers an otherwise relevant candidate and that
`More like this` raises a matching candidate. More/Less never mutates follow,
block, mute, listblock, or other durable association state.

## Controlled serendipity

Low, default, and high discovery settings change unfamiliar/exploratory
composition in deterministic fixtures. High increases exploration; low
decreases it. Explicit negative preferences remain exclusion constraints in
all three modes. The constitutional ranking path contains no political,
racial, demographic, religious, or ideological balancing quota.

## “Why this post?” fidelity

The local ranker emits a trace and the UI derives explanations from that trace.
Supported reasons include followed account, social proximity, explicit or
inferred interest, freshness, exploration, More/Less preference, and a
provider-supplied reason when the provider actually supplies one. Missing
provider trace data is disclosed rather than replaced with fabricated local
precision. Confidential anti-abuse signals are not exposed. Fidelity tests
cover trace/reason agreement and stale/unsupported reason rejection.

## Algorithm/provider choice

| Choice | Current result |
|---|---|
| Following | Live/default first-class chronological choice; provider/provenance visible. |
| Balanced | Real local opt-in overlay with version `org.radical-liberal.balanced/1`; disabled by default. |
| Custom feed | Existing feed selection remains available and provider/feed owner are displayed when known. |
| External provider | Generic validated provider registry, persistence, health probe, and explicit selection exist; populated authenticated alternate-provider owner walkthrough remains pending. |

Provider switching does not change DID, PDS, follows, blocks, recovery, or
unrelated personalization in the tested isolation paths. The retired
AppViewLite instance is not presented as evidence of provider choice.

## Failure and fallback

Provider probes name the actual failing provider and preserve the selected
provider identity. A materially different provider is not silently presented
as the failed one. PDS identity/repository functionality remains a separate
boundary. Filtered-feed fixtures return explicit `ProviderUnavailable` when
ingestion is absent. The live notification failure above follows the same
rule: the selected Project AppView is named and no replacement is presented.
Live resolver/labeler outage injection remains an owner walkthrough question.

## Political neutrality

Result: `PASS` for the default constitutional ranking path.

Static audit and deterministic tests found no left/right, party,
demographic, ideological, political-quality, or mandatory constructiveness
quota in the default ranking path. User-selected political/topic controls are
allowed as explicit local preferences. Ideological terms in the optional
content policy are user-selected filters, not outcome balancing rules.

## Portable Personalization

The export → inspect → reset → import contract is implemented and tested.
Round-trip restoration covers supported explicit settings and curation state.
Passwords, access/refresh tokens, service-auth JWTs, recovery secrets, and
private keys are rejected from export schemas and values. Provider-specific
state is represented as portable settings only where its semantics are
declared; credentials and provider internals are not exported.

## Institutional attribution and defaults

Current surfaces distinguish the user, PDS, selected AppView/feed provider,
resolver, labeler, and provider failure where the actor is known. Important
defaults remain reversible: Following is accessible, Balanced/custom feeds are
discoverable, and advanced provider/personalization controls are in settings.
The UI does not use a vague “platform” actor for known PDS/provider decisions.

## Pairwise visibility repair

The live browser defect shown in the owner screenshots was reproduced against
the current AppView response: `getPostThreadV2` returned Bela’s parent as
`threadItemBlocked` while `feed.getPosts` returned the complete post. The
client now hydrates blocked thread items in bounded batches for both the main
thread and additional replies. Blocked quote records use the same automatic
hydration path and are rendered as ordinary quote cards after retrieval.

This is a local presentation repair, not a protocol claim that a block record
does not exist. It preserves the distinction between a pairwise relationship
and a third-party viewer’s independent reading choice.

## Live incoming-block and quote verification

The owner-reported case was verified against the actual public records, not
just the screenshot. The target post is:

```text
at://did:plc:3ijrhre2q5e4tt2f4ph2sneo/app.bsky.feed.post/3mtf4xncr6c24
```

Its public `quoteCount` is `1`, while the authenticated AppView returned an
empty `app.bsky.feed.getQuotes` page and a blocked thread tombstone for the
known quote. A public author-feed/search read identified the quote record:

```text
at://did:plc:dwilen7uctmqg2dstjjhl5zs/app.bsky.feed.post/3mtfj372a6c2r
Check out Mr. Bitter aka Ty. I'd block him.
```

The Clearsky history link supplied by the owner also resolves to the target
post. It was used as an independent public-index cross-check; it was not
treated as proof of a particular blocking-tab state.

The repaired browser behavior is now:

- the Quotes screen shows `1 quote` and renders the Writer of Dragons quote;
- the quote card shows the quoted Edriffles post and its text automatically;
- opening the quote post shows the outer quote and embedded target instead of
  `Post blocked`;
- the Writer of Dragons profile/author feed renders public posts even though
  the authenticated AppView previously returned `Posts hidden`;
- an explicitly authored direct block by the current viewer remains a hard
  local boundary in the fallback path;
- incoming `blockedBy` state is kept as interaction metadata and removed from
  local public-read presentation; legacy provider-supplied list-derived fields
  are compatibility input only and never become a block in this fork.

The public retry is same-provider and endpoint-configured
(`PUBLIC_APPVIEW_URL`/`APPVIEW_ENDPOINT`),
not a silent substitution for a materially different AppView. If that public
retry fails, the client keeps the provider error/tombstone rather than
claiming recovery. The live browser route used for verification was:

```text
http://127.0.0.1:19006/profile/edriffles.us/post/3mtf4xncr6c24/quotes
```

## Fixes implemented in this review

- Added automatic, bounded blocked-thread hydration with fail-closed provider
  error handling.
- Applied the same behavior to additional thread replies.
- Added automatic blocked-quote hydration so parent/quoted authors and text
  remain visible without a user click.
- Added a configured public-read retry for blocked thread hydration, single
  post fetches, author feeds, and quote recovery through structured search.
- Guarded every public-read retry with a relationship-authority check so the
  client bypasses incoming/list-only boundaries but remains fail-closed for a
  direct block authored by the current viewer.
- Preserved direct viewer-authored blocks while bypassing incoming and
  list-derived provider tombstones for public context.
- Switched the anonymous fallback client from the legacy hardcoded public API
  origin to the configured project AppView endpoint; this is required because
  a stock AppView would silently restore different blocking, list, thread, and
  moderation semantics.
- Preserved viewer-owned direct blocks when the effective `blocking` URI is
  an `app.bsky.graph.block` URI; any list URI is read-through and an incoming
  direct block remains an interaction boundary rather than a public-read
  filter.
- Made `app.bsky.graph.listblock` fully inert in the first-party AppView data
  plane while retaining raw repository/CAR/indexing compatibility and keeping
  `list_mute` as the supported delegated attention primitive.
- Removed the remaining list-screen dependence on legacy `list.viewer.blocked`
  state, so a provider-supplied listblock cannot hide a list or offer a
  conversion action; list screens now respond only to private list mute state.
- Removed listblock-derived DM block prompts/actions and made client direct
  block detection collection-aware even when provider metadata is incomplete.
- Normalized secondary client gates (profile menus, notification follow-back,
  chat/member menus, post menus, labeler/list presentation, and review
  selection) to the same URI-aware rule so a list-only `blocking` value cannot
  masquerade as an individually authored direct block.
- Added a shared client policy helper so list-only relationships do not disable
  post controls, profile descriptions, or follow affordances, while direct
  and incoming relationships still constrain interactions.
- Added regression coverage for direct-plus-list coexistence so a list does
  not accidentally bypass a separately authored direct block.
- Added deterministic tests for unrelated-viewer recovery, hard-boundary
  preservation, and provider failure behavior.
- Added a compact outlined More/Less control group to the post action row. It
  uses the client's crisp arrow icons, stable action labels, a visible selected
  treatment, and real toggle semantics; the pair follows the Edriffles/ECW
  icon grammar without looking like a public vote widget.
- The controls persist as portable local explicit preferences (`prefer`/`avoid`),
  are reversible, update optimistically with rollback on write failure, and do
  not create public vote records or mutate likes, follows, blocks, or mutes.
- Narrowed the shared web button primitive so `aria-pressed` is emitted only
  for explicit toggle state; ordinary post actions no longer masquerade as
  toggle buttons.
- Made public post metrics hidden by default, including for logged-out views;
  the Personalization settings toggle is the explicit reversible opt-out, and
  older unconfigured local states migrate to hidden once.
- Added a separate PDS permissioned-data adapter, private records/blobs ACL,
  protected-account follow state, community membership/invite/ban state, and
  public repository/CAR namespace guards.
- Added a text-only protected-account composer mode that calls
  `org.radlib.private.putRecord`; it cannot silently fall through to the public
  `app.bsky.feed.post` writer.
- Converted reserved private-namespace write failures at public create/put/
  applyWrites routes into the explicit `PermissionedCollectionRequiresPrivateAPI`
  XRPC error instead of leaking an internal 500.
- Added settings for the real local-curation inputs: reply inclusion, the
  per-author concentration cap, each curation branch weight, and the active
  term-exclusion policy. These update the same persisted configuration consumed
  by `PostFeed`, not a fixture-only preference surface.
- Replaced opaque Low/Default/High attention rows with 10% stepper controls for
  discovery, familiarity, freshness, variety, conversation activity, and
  exploration/serendipity. The values are persisted in portable explicit state
  and are consumed by both local and Balanced ranking paths.
- Added real controls for chronological Following versus local reranking,
  Following versus Balanced, explicit interests, explicit author More/Less
  preferences, inferred-interest opt-out/removal, content-filter pack
  selection, and custom local-curation terms/authors.
- Completed the political-filter coverage for unambiguous `commie` and
  `commies` variants. The live owner feed had the packs selected but the hard
  filter disabled; the local owner state was enabled with strict progressive
  matching and explicit `progs`/commie variants, then reloaded and verified
  with no matching terms in the rendered feed. Ambiguous `prog` wording remains
  an explicit personal term rather than a broad default rule.
- Added migration-safe `inferredInterestsEnabled` state so existing local
  personalization remains valid while passive inference can be disabled
  without deleting the learned profile.

## Button UI research applied

The refinement follows current primary design-system and accessibility guidance:

- Icon-only controls need a familiar visual metaphor, sufficient hit area, and
  a clear interaction state. Apple recommends at least a 44-point hit region
  and a press state; the post control retains the existing generous hit slop
  while adding a compact selected treatment.
- Related low-emphasis actions should be grouped rather than presented as
  unrelated high-emphasis buttons. The two local curation choices now share a
  restrained outline and divider, while the public Like action remains
  visually independent.
- A two-state control should expose stable labels and an explicit pressed state.
  The UI therefore announces “Show more like this” / “Show less like this” and
  uses `aria-pressed` only for those toggles.

Sources: [Apple Human Interface Guidelines: Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons), [WAI-ARIA APG: Button Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/button/), and [IBM Carbon: Button usage](https://carbondesignsystem.com/components/button/usage/).

## Red-team result

| Criticism | Result | Evidence |
|---|---|---|
| Official AppView is mandatory | `NOT SUPPORTED` in the configured routing path; live owner check remains | The first-party Project AppView is the explicit configured read authority, provider selection is DID/endpoint scoped, and no stock AppView fallback exists. A current-fork live launch is still pending owner walkthrough. |
| Feed replacement is fake | `PARTIALLY SUPPORTED` | Following/Balanced/custom-feed choices are real; broad populated external-provider marketplace breadth is still owner work. |
| PDS silently controls all service choice | `NOT SUPPORTED` in tested path | PDS and AppView clients, provider DID, health, and fallback state are separate. |
| Block grants broad third-party authority | `NOT SUPPORTED` in repaired path | Direct blocks are individual; list mute/review are separate; C fixture remains independent. |
| Labeler is central moderator | `NOT SUPPORTED` in default path | Labeler is selected descriptive input, not a direct-block mutation. |
| Explicit preferences do not rank | `NOT SUPPORTED` | Deterministic precedence tests prove ranking effect. |
| Personalization cannot leave provider | `NOT SUPPORTED` for implemented settings | Inspect/reset/export/import round-trip and secret exclusion pass; richer provider-specific state remains bounded. |
| Why-this-post is decorative | `NOT SUPPORTED` in local path | Displayed reasons derive from actual traces; missing provider reasons are disclosed. |
| Hidden political quotas | `NOT SUPPORTED` | Neutrality audit found no mandatory outcome quota. |
| Configuration store is hidden master authority | `NOT SUPPORTED` in tested contracts | Authority/data-flow fixtures prohibit cross-domain mutation. |

## AppViewLite migration result

The active migration is complete at the repository-graph level:

- removed AppViewLite and FishyFlip from `.gitmodules` and tracked gitlinks;
- removed the AppViewLite pin and old provider test fixtures;
- removed AppViewLite build/live launch commands from current artifacts;
- retained only explicitly labeled historical evidence where needed;
- kept the first-party PDS as the supported identity/repository/CAR authority;
- kept generic provider selection rather than replacing AppViewLite with a new
  hidden mandatory service.

The physical dirty nested checkout was preserved to avoid destroying existing
user work. It is not tracked, configured, built, or used by the product.

## Tests and build evidence

The retirement verification pass produced the following current evidence:

```sh
cd /var/home/tcs/Code/atproto
python3 scripts/validate_contract.py
python3 scripts/check_upstream.py --fast
python3 -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

Root result: contract validation passed for 111 files; root regression passed
with 90 tests; upstream pin check passed; diff check passed.

Client:

```sh
cd /var/home/tcs/Code/atproto/upstream/social-app
pnpm lint
pnpm typecheck:web
pnpm test-ci --runInBand
EXPO_PUBLIC_ENV=production pnpm build-web
```

Client result: 80 Jest suites passed, 870 tests passed, 28 todo, 21
snapshots; lint, web typecheck, and production export passed. The export
reported existing webpack warnings but exited successfully.

Final compile-repair verification on 2026-08-19:

```sh
cd /var/home/tcs/Code/atproto/upstream/social-app
pnpm typecheck:web
pnpm test -- --runInBand \
  src/lib/moderation.test.ts \
  src/state/session/__tests__/providers-test.ts \
  src/state/session/__tests__/clients-test.ts \
  src/state/session/__tests__/session-core-test.ts \
  src/lib/attention-ui.test.ts \
  src/lib/feed-provider-security.test.ts
EXPO_PUBLIC_ENV=production pnpm build-web
```

Result: web typecheck passed; the focused provider/error suites passed 3 suites
and 36 tests, and the broader focused client regression passed 8 suites and 92
tests; the production export compiled successfully. Webpack
reported only the existing optional `ContactAccessButtonProps`/`expo-router`
warnings and bundle-size warnings. It did not report the repaired `Can't
resolve './'` failure. The browser notification check rendered without a
refresh overlay and showed `AppView provider Project AppView
(did:plc:dw4kbjf5mn7nhenabiqpkyh3) is unavailable`, followed by a retry action,
with no `identity unknown`, Lex wrapper, or false empty-state claim. The root
suite then passed 90 tests, and the PDS relationship/listblock regression
passed 10 files and 229 tests.

Latest customization pass:

```sh
cd /var/home/tcs/Code/atproto/upstream/social-app
pnpm exec jest src/lib/feed-sovereignty/profile.test.ts \
  src/lib/feed-sovereignty/radlib-curation.test.ts \
  src/lib/balanced.test.ts src/lib/personalization.test.ts \
  src/state/preferences/local-feed.test.ts --runInBand --forceExit
pnpm typecheck:web
pnpm build-web
```

Result: 5 focused suites passed, 44 tests passed; web typecheck passed; the
production export passed with the existing ContactAccessButton, expo-router,
and bundle-size warnings. The live browser settings check confirmed all six
stepper controls, both feed-mode choices, explicit topic/author controls,
inferred-interest controls, filter packs, custom curation inputs, and the
persisted political-filter state. A fresh rendered Home check contained no
matching communist, Marxist, progressive, `progs`, or commie terms.
The owner-local curation toggle was then enabled; the values observed in that
historical run are retained as owner-local state, not defaults. Feed
provenance now reports the combined content-filter and local curation layers
instead of hiding the curation layer.

Live timeline verification on the actual Webpack origin (`19006`) loaded the
initial timeline and an additional scrolled page. Both rendered states
contained posts and zero matches for the configured political-filter terms.
The persisted settings were then reopened and confirmed enabled. Dev logs
still contain pre-existing GrowthBook/geolocation informational failures and
nested-button hydration warnings, but no filter-related runtime error.

Fresh live validation at `2026-08-18T19:27:58-04:00` was performed against the
actual rendered Webpack origin, `http://127.0.0.1:19006/`, rather than the
Metro/native endpoint. The persisted owner state showed `Use radical-liberal
curation` checked, content filtering checked, strict progressive matching
checked, and the custom terms `commie`, `commies`, and `progs` present. The
settings screen also rendered the real curation inputs: reply inclusion,
per-author cap, five branch weights, local curation exclusions, and reset/
export/import controls.

The first rendered Discover batch contained eight posts and no configured hard
filter terms. It did contain a music-related post, but no K-pop/girl-group or
audio-gear term in that observed batch. It also contained an Ilya Somin post
linking to Reason/Volokh, which is evidence of Cato-adjacent/libertarian
content being present in the provider-supplied candidates. This is an
observation of one live batch, not a claim that local curation can generate a
topic the selected provider did not supply. The feed details panel accurately
reported:

```text
Algorithm: Filtered Discover + local curation
version content-filter/1 + radlib-curation/1
Objective: User-selected hard content exclusions plus a user-selected topic
and exclusion overlay; follows, blocks, and ranking remain separate
Privacy: Custom filter terms and curation state stay on this device; the
selected provider supplies candidates
```

The machine-readable evidence is retained in
`artifacts/radlib-live-local-curation-validation.json`.

## Topic-target validation pass (historical provider evidence)

At `2026-08-18T20:45:01-04:00`, the owner-local controls were adjusted through
the rendered Personalization screen for `edriffles.us`:

- local curation: enabled;
- content filtering: enabled, with the existing local terms retained;
- Include replies in local curation: enabled;
- K-pop/music branch weight: `10.0`;
- audio-science branch weight: `10.0`;
- explicit interests: `k-pop`, `girl groups`, `audio gear`, `headphones`,
  `dac`, `amplifier`, and `iem`.

Discover remains a provider-supplied candidate pool. Its local overlay can
rerank and filter candidates, but it cannot manufacture a topic that the
selected provider did not return. Earlier in the review, two external
feed-generator records were searched and pinned through the feed directory to
validate the topic controls. They are historical evidence only: they are not
seeded, recommended, or pinned by the current local fixture, and the current
default set is `Following` plus neutral `Discover`.

| Feed | Rendered evidence | Provider/feed identity |
|---|---|---|
| Kpop GGs | Historical 35-post observation containing LE SSERAFIM, TWICE/KiiiKiii, KATSEYE, 2NE1, BLACKPINK, and MAMAMOO | Retained only as audit evidence; no longer seeded, recommended, or pinned by the current local fixture. Original owner `did:plc:qaim2qnyqugjgwlyvosh22ck`; original URI `at://did:plc:qaim2qnyqugjgwlyvosh22ck/app.bsky.feed.generator/aaalbyp4zfz3s` |
| Headphones | Historical 12-post observation containing an Audiobyte SuperHead review and audio-equipment posts | Retained only as audit evidence; no longer seeded, recommended, or pinned by the current local fixture. Original owner `did:plc:j2hwrkgv56x6uy5rwkhkkmyv`; original URI `at://did:plc:j2hwrkgv56x6uy5rwkhkkmyv/app.bsky.feed.generator/aaagh476unqpu` |

Those historical feeds are not part of the current local feed selector. The
topic controls remain available in Personalization as user-selected local
signals, so the fork can still curate provider-supplied K-pop/audio candidates
when a user explicitly chooses a suitable feed. On the historical rendered
pages, the repaired provenance card reported:

```text
Algorithm: Filtered <feed> + local curation
version content-filter/1 + radlib-curation/1
Objective: User-selected hard content exclusions plus a user-selected topic
and exclusion overlay; follows, blocks, and ranking remain separate
Privacy: Custom filter terms and curation state stay on this device; the
selected provider supplies candidates
```

This was a real provider-backed topic result at the time, not a fixture or
placeholder. It does not claim that the current local Discover fixture always
contains K-pop or audio gear; the provider's candidate set and the user's
selected feed determine that outcome. The historical topic-feed evidence is
retained in
`artifacts/radlib-live-topic-feed-validation.json`.

The bounded implementation repair behind this pass is:

- `src/lib/feed-sovereignty/candidate-text.ts` now gives local policy the
  visible text of the post, quoted post, external card, image/gallery alt text,
  and video alt text;
- `PostFeed` passes that rendered candidate text into content filtering and
  local curation;
- explicit interests therefore match actual visible terms such as `audio
  gear`, `DAC`, and group names rather than only a coarse provider topic;
- the custom-feed provenance card now reports both local layers when both are
  enabled, instead of claiming that only content filtering ran.

Focused verification after the repair:

```sh
cd /var/home/tcs/Code/atproto/upstream/social-app
pnpm exec jest src/lib/feed-sovereignty/profile.test.ts \
  src/lib/feed-sovereignty/radlib-curation.test.ts \
  src/lib/feed-sovereignty/candidate-text.test.ts \
  src/lib/balanced.test.ts src/lib/personalization.test.ts \
  src/state/preferences/local-feed.test.ts --runInBand --forceExit
pnpm exec oxlint --quiet src/screens/CustomFeed/index.tsx
pnpm typecheck:web
```

Result: 6 suites and 48 tests passed; oxlint and web typecheck passed. The
latest `EXPO_PUBLIC_ENV=production pnpm build-web` export also passed. It
reported the existing ContactAccessButton, expo-router, and bundle-size
warnings, with no new feed or provenance compilation error.

First-party PDS:

```sh
cd /var/home/tcs/Code/atproto/upstream/atproto-pds
PNPM_CONFIG_PM_ON_FAIL=ignore pnpm --filter @atproto/pds build
```

PDS result: the full build passed with the PDS-declared pnpm 11.11.0
toolchain, and the focused moderation-policy and migration suites passed 10
tests. An initial host run with global pnpm 11.21.0 incorrectly propagated the
version mismatch into recursive scripts and exposed baseline compiler errors;
the supported pinned-toolchain run is the valid result. No AppViewLite code is
involved.

Live browser launch:

```sh
cd /var/home/tcs/Code/atproto/upstream/social-app
pnpm install --frozen-lockfile
pnpm web -- --port 8081
```

The rendered Webpack timeline is served at `http://127.0.0.1:19006/`; port
8081 is the Metro/dev-client port used by the same command.

Live PDS/CAR/provider walkthrough:

```sh
cd /var/home/tcs/Code/atproto
node scripts/radlib_live_provider_walkthrough.mjs
```

Live provider result: passed CAR import, pre-activation migration block,
provider-signed private-mute attestation, CID/CAS-protected cleanup, and final
activation. Filtered-feed service tests passed 23 tests and its live
walkthrough passed healthy and explicit-unavailable states.

No AppViewLite build or launch command is part of the current gate. The PDS
build command must use the package-manager version declared by the PDS.

Current blocking/quote regression suite:

```sh
cd /var/home/tcs/Code/atproto/upstream/social-app
pnpm exec jest src/lib/api/feed/author.test.ts \
  src/state/queries/post-quotes.test.ts \
  src/state/queries/usePostThread/blocked.test.ts \
  src/state/queries/public-visibility.test.ts --runInBand --detectOpenHandles
pnpm typecheck:web
pnpm exec oxlint --quiet \
  src/state/queries/post-quotes.ts \
  src/state/queries/post-quotes-fetch.ts \
  src/state/queries/post-quotes-helpers.ts \
  src/state/queries/usePostThread/blocked.ts \
  src/state/queries/usePostThread/index.ts \
  src/state/queries/post.ts \
  src/lib/api/feed/author.ts \
  src/lib/moderation/blocked-and-muted.ts \
  src/components/moderation/BlockDialog.tsx \
  src/view/com/profile/ProfileMenu.tsx \
  src/view/com/notifications/NotificationFeedItem.tsx \
  src/screens/Profile/Header/Handle.tsx \
  src/screens/Profile/Header/ProfileHeaderLabeler.tsx \
  src/screens/Profile/Header/ProfileHeaderStandard.tsx \
  src/screens/Messages/ConversationSettings/MemberMenu.tsx \
  src/screens/List/ListHiddenScreen.tsx \
  src/components/PostControls/PostMenu/PostMenuItems.tsx \
  src/components/dialogs/lists/ReviewListMembersDialog.tsx \
  src/state/queries/profile.ts
```

Result: 4 suites and 18 tests passed; web typecheck and the changed-file lint
pass. The root suite also passed 90 tests after its stale provider-wiring audit
was updated to assert the now-implemented control. The live browser check
rendered the recovered quote list and the outer quote post with its embedded
target.

## Current phase implementation addendum — viewer sovereignty

This addendum supersedes older report language that described the stock
Bluesky AppView as the current default. The selected read authority in the
current fork is the configured first-party Project AppView. The pinned
`@atproto/bsky` package is the AppView implementation; AppViewLite and FishyFlip
are retired and are not launch or runtime dependencies.

### Independent AppView routing

Authenticated reads are built by
`upstream/social-app/src/state/session/clients.ts`. The client asks the account
PDS for service-auth with the selected provider DID as `aud`, then sends the
short-lived token and `${serviceDid}#${serviceFragment}` to the selected
provider endpoint. PDS/repository writes remain on the account PDS. Public and
logged-out reads use the configured `PUBLIC_APPVIEW_URL` through the same
provider boundary. Provider registration, validation, health, selection, and
explicit fallback are in `state/session/providers.ts`.

The neutral environment variables are
`EXPO_PUBLIC_APPVIEW_SERVICE_DID`,
`EXPO_PUBLIC_APPVIEW_SERVICE_FRAGMENT`,
`EXPO_PUBLIC_PUBLIC_APPVIEW_URL`, and
`EXPO_PUBLIC_DEFAULT_LABELER_DIDS`. Missing production AppView configuration
is an explicitly unavailable Project AppView, not a hidden `api.bsky.app`
fallback. The remaining `EXPO_PUBLIC_ACCOUNT_SERVICE` dependency is limited
to login/handle availability and is not a public read path.

The client provider-routing regression now proves that an authenticated
`app.bsky.actor.getProfile` request reaches the explicitly selected project
endpoint and carries that provider's proxy identity. This is routing evidence;
it does not claim that a live deployment is running from the current dirty
checkout until the owner launches the first-party PDS/AppView fixture.

### Viewer-sovereign labels

`upstream/social-app/src/lib/moderation.ts` is the single viewer-policy adapter.
Ordinary label provenance survives Show, Warn, and Hide. Ordinary custom
`no-override` labels are made viewer-configurable without changing system
`!` labels, adult-safety boundaries, direct blocks, or service-unavailable
states. Configured global labelers are explicit; geolocation no longer forces
an external labeler into every request. The focused moderation/provider/client
suite passes. A label preference cannot resurrect bytes the AppView/PDS does
not serve.

### Public replies, quotes, and threadgates

The fork now separates public-reference existence from author curation:

- `hiddenReplies` is honored only by the explicit Author's curation view;
  Everyone's replies is the default public view;
- `violatesThreadGate` continues to gate reply authorization and notification
  handling, but does not erase the public reply or its descendants;
- postgate quote detachment is advisory for unrelated viewers; an available
  public quote remains attached, while deletion/takedown/missing records remain
  unavailable;
- reply aggregates count public replies even when the reply violates an
  author gate, avoiding a misleading public record count.

The server-side paths are `packages/bsky/src/views/index.ts`,
`packages/bsky/src/data-plane/server/indexing/plugins/post.ts`,
`tests/views/thread-v2.test.ts`, `tests/views/threadgating.test.ts`, and
`tests/postgates.test.ts`. The current focused PDS run passed 115 tests across
thread-v2, threadgating, postgates, and quotes. Client mode selection is
persisted locally in `threadCurationView`, defaulting to `all`, with both the
Post Thread menu and Settings surface available.

### DID privacy

`ChangeHandleDialog.tsx` requires acknowledgement before a `did:plc` handle
rename. The warning explains that a rename, PDS move, or domain handle does not
create unlinkability or erase public PLC history. A genuinely separate identity
requires a new account/DID. Non-PLC changes retain their ordinary flow; the
owner should exercise both branches.

### Current automated phase verdicts

| Phase | Result | Evidence boundary |
|---|---|---|
| Independent AppView | PASS for routing | Current-provider routing tests pass; live current-fork service walkthrough remains owner work. |
| Viewer-sovereign labels | PASS | Ordinary Show/Warn/Hide, provenance, no-override, block, and provider failure boundaries are tested. |
| Hidden replies | PASS | Public and author-curated server/client paths are tested. |
| Quote detachment | PASS | Available public embeds remain available; unavailable originals remain unavailable. |
| Threadgate model | PASS | Rule, public-reference, descendant, aggregate, and notification behavior are tested. |
| DID privacy UX | PASS | Warning/acknowledgement path is typechecked; live owner exercise remains pending. |
| Block regression | PASS | Existing directional A/B/C and public recovery suites remain green. |
| Listblock regression | PASS | Existing inert listblock/list mute/CAR migration suites remain green. |

These are automated implementation results, not owner-result fields. The
working tree is intentionally not clean because it contains the accumulated
fork implementation and evidence artifacts; therefore the overall state stays
`RADLIB_CODEX_ACCEPTANCE_BLOCKED` pending owner review.

## Remaining owner-judgment questions

1. Does the owner approve the configured first-party Project AppView identity,
   endpoint, and service DID after launching the current PDS/AppView fixture,
   or require a populated alternate provider before acceptance?
2. Does the owner accept Balanced as a local opt-in overlay rather than a
   second server-side algorithm provider?
3. Does the owner want to perform live authenticated follow/block/mute,
   personalization reset/import, and resolver/labeler outage walkthroughs on
   the disposable environment?
4. Does the owner accept preserving the dirty retired checkout as an external
   recoverable archive, or want a separately authorized deletion/move?

Path to owner checklist: `docs/OWNER_ACCEPTANCE_CHECKLIST.md`.

Automated acceptance remains `OWNER_ACCEPTANCE_PENDING`; this report does not
mark owner acceptance passed.

## Permissioned accounts and communities addendum

The current branch adds a real local permissioned-data boundary and feature
flags, but it does not yet make protected accounts/private communities a
complete product. The detailed implementation report is
[`docs/PRIVATE_ACCOUNTS_COMMUNITIES_IMPLEMENTATION.md`](PRIVATE_ACCOUNTS_COMMUNITIES_IMPLEMENTATION.md).

The important boundary is deliberate: private values are stored in a separate
SQLite/blob store behind `PermissionedSpaceAdapter`; fork-owned
`org.radlib.private.*` collections are rejected by public repository writes and
public CAR import. The current client protected-account setting is honest about
the remaining gap: the ordinary public composer is not silently treated as a
private composer. An explicit text-only private-post mode now calls the
fork-owned permissioned write API; private media and private AppView hydration
remain unimplemented.

For this feature, P1/P2/P3/P4/P5/P7/P9 are locally green or structurally
green, and P8 is partial. At the time of this initial implementation review,
P6/P10 were not implemented; the 2026-08-19 addendum at the end of this report
records their bounded direct-PDS implementation. Consequently the overall
automated verdict remains `RADLIB_CODEX_ACCEPTANCE_BLOCKED` and owner state
remains `OWNER_ACCEPTANCE_PENDING`.

The current web server was restarted after client lexicon generation and
rendered `Privacy and Security` without a compile overlay. Its protected-account
message correctly says the existing long-running PDS is not flag-enabled; the
flag-enabled walkthrough remains a disposable-PDS test/owner task rather than
an unverified live claim.

## Age-assurance removal addendum

The client-side age-assurance product was removed from the current fork. This
is intentionally a client-policy change, not a deletion of standard ATProto
wire compatibility.

| Boundary | Actual implementation | Result |
|---|---|---|
| Client bootstrap and session preparation | `upstream/social-app/src/App.tsx`, `src/App.web.tsx`, `src/state/session/{session-core,create-account,index.tsx}` | No age-assurance provider, prefetch, cache seed, or preparation gate is initialized. |
| Account and content access | `src/view/shell/{index.tsx,index.web.tsx}`, `src/view/com/posts/PostFeed.tsx`, `src/screens/Signup/StepInfo/index.tsx`, `src/screens/Moderation/index.tsx` | No age-assurance redirect, no-access, feed banner, region/device gate, or age-derived content/chat gate is presented. Standard account birthdate entry/editing remains. |
| Messaging, sharing, navigation, notifications | `src/screens/Messages/**`, `src/components/PostControls/ShareMenu/**`, `src/view/shell/**`, `src/lib/notifications/notifications.ts` | These surfaces no longer consult age-assurance state. Push registration still sends the upstream `ageRestricted: false` field as a compatibility value; it is not derived from or used as a client gate. |
| Feature modules and telemetry | `src/ageAssurance/`, `src/components/ageAssurance/`, `src/state/queries/messages/restrictChatSettings.ts`, `src/analytics/metrics/types.ts`, `src/state/queries/nuxs/definitions.ts` | Product modules, chat restriction helper, feature telemetry, and related NUX definitions are deleted. |
| Web geolocation/age surface | `upstream/social-app/bskyweb/cmd/bskyweb/{server.go,main.go}` | The age-related `/ipcc` route, `ipcc-host` flag, IPCC client, and age-geolocation response fields are deleted; this web server no longer exposes the age-assurance location service. |
| Protocol compatibility | `upstream/social-app/lexicons.json`, `upstream/social-app/lexicons/app/bsky/**`, `upstream/atproto-pds/packages/bsky/src/api/app/bsky/ageassurance/**` | Standard age-assurance Lexicon/PDS endpoints remain readable and importable so the fork does not create a wire-format dialect. They are no longer invoked by this client. |

The regression guard is `tests/test_client_age_assurance_removed.py`. It checks
that both client feature directories are absent and that non-test client
runtime sources contain no age-assurance imports, gates, redirect, or access
screen references and that the web shell exposes no age-geolocation service. It
passed with `3 passed`. This does not assert removal of
ordinary ATProto birthdate metadata or the upstream protocol definitions.

Post-change verification passed: web and iOS TypeScript checks, the full client
Jest run (`83` suites, `890` passed, `28` todo), production Webpack export
(exit `0`, with the existing Expo contacts/router and asset-size warnings),
root contract validation, and root pytest (`94 passed`). The live local web,
PDS, and AppView health probes returned HTTP `200`.

This is an automated implementation result only. `OWNER_ACCEPTANCE_PENDING`
remains unchanged; the owner should verify the login, settings, notifications,
messaging, and ordinary birthday-edit flows in the local browser after a clean
web rebuild.

## PDS/login connectivity addendum

The login failure in the rendered browser was a configuration/fixture-boundary
failure, not evidence that the real `edriffles.us` repository had disappeared:

| Check | Observed result |
|---|---|
| Local PDS at `127.0.0.1:2583` | Healthy (`HTTP 200`), but identifies as `did:web:localhost` and advertises only `.test`/`.example` user domains. It cannot resolve `edriffles.us`. |
| Running web process before repair | `EXPO_PUBLIC_ACCOUNT_SERVICE=http://127.0.0.1:2583`; this sent the owner's handle lookup to the fixture PDS. |
| Public handle resolution | `edriffles.us` resolves to `did:plc:3ijrhre2q5e4tt2f4ph2sneo`. |
| DID-declared PDS | `https://yellowfoot.us-west.host.bsky.network`, healthy and requiring normal account authentication. |
| Local AppView at `127.0.0.1:2584` | Healthy, but `app.bsky.actor.getProfile(actor=edriffles.us)` returns `Profile not found`; its current dataset is the Alice/Bob test fixture. |
| Corrected login resolution | `src/state/queries/pds-detection.ts` now resolves handles through the explicit `PUBLIC_ACCOUNT_SERVICE` entryway and then trusts the DID document's PDS endpoint. It no longer treats the selected/partial AppView as the login identity resolver. |
| Current browser process | Relaunched with `EXPO_PUBLIC_ACCOUNT_SERVICE=https://bsky.social`, explicit local AppView `http://127.0.0.1:2584`, and the existing neutral `Discover` fixture feed. Web/PDS/AppView probes all returned `HTTP 200`. |

This means the local fixture command is suitable for deterministic Alice/Bob
acceptance, while an owner login for `edriffles.us` must use the real account
entryway or the DID-declared PDS. The local AppView still needs a real
federated ingestion/deployment before it can present the owner's remote
profile/posts; the seeded test feed must not be described as the owner's live
timeline. No password, token, or account record was entered or changed during
this repair.

### Live owner read-provider repair

The first browser relaunch after the login repair still showed
`AppView provider Project AppView (did:plc:dw4kbjf5mn7nhenabiqpkyh3) is
unavailable`. This was a real provider-identity failure, not an account login
failure:

- `did:plc:dw4kbjf5mn7nhenabiqpkyh3` is generated by the disposable PLC at
  `127.0.0.1:2582`; `https://plc.directory/` reports it as unregistered.
- The local AppView at `127.0.0.1:2584` is the pinned dev-env fixture and does
  not index the remote `edriffles.us` DID. Its profile lookup returned
  `Profile not found` while its health endpoint returned `HTTP 200`.
- The live browser was therefore relaunched with an explicit, labelled public
  provider: `https://api.bsky.app`, service identity
  `did:web:api.bsky.app#bsky_appview`, and display name `Public Bluesky AppView
  (explicit read provider)`. This is an explicit provider configuration, not a
  hidden fallback; it was chosen only to make authenticated reads for the real
  account testable while the first-party AppView is not federated.
- The public provider resolves `edriffles.us` to
  `did:plc:3ijrhre2q5e4tt2f4ph2sneo` and its DID document declares PDS
  `https://yellowfoot.us-west.host.bsky.network`.

The current live web process is healthy at `http://127.0.0.1:19006/`. This
repair does not claim that the public provider supplies the fork's Radlib
Discover algorithm, nor that the local Project AppView can serve the owner's
remote timeline. A real first-party deployment still needs a stable registered
AppView DID, HTTPS service endpoint, authenticated federation/ingestion, and a
populated index before it can replace this explicit temporary read provider.
Owner acceptance remains pending.

### Cloudflare Pages and public-host verification addendum

The public client is now deployed to Cloudflare Pages rather than being
documented as merely code-ready:

| Boundary | Observed result |
|---|---|
| Pages project | `social-edriffles` |
| Pages deployment | `https://99d240b7.social-edriffles.pages.dev` (supersedes the earlier recorded deployment) |
| Custom-domain association | `social.edriffles.us`, Cloudflare status `active` |
| DNS | CNAME `social.edriffles.us` → `social-edriffles.pages.dev` |
| Root HTTPS | HTTP `200`, Cloudflare-served HTML, title `Social` |
| SPA fallback | `/settings/personalization` HTTP `200` over HTTPS with root-relative entrypoint assets |
| Local fallback | User services `social-edriffles-static.service` and `cloudflared-social-edriffles.service` are enabled; static export listens on `127.0.0.1:19008` |

The Cloudflare Pages deployment used the direct-upload path and the generated
`upstream/social-app/web-build/` artifact. The local tunnel is a rollback path,
not a hidden replacement for Pages; the `idoldle` tunnel was not modified.
This is a hosting result only. It does not turn Pages into the user's PDS or
AppView, and it does not establish a live first-party federated AppView for the
owner's account. See `docs/SOCIAL_EDRIFFLES_DEPLOYMENT.md` for the exact build,
redeploy, service, and DNS commands.

## Public product identity and like responsiveness addendum

The public web product is now configured as **Social** with the intended
canonical origin `https://social.edriffles.us`. This is branding and hosting
configuration, not a change to ATProto identity, PDS ownership, or wire
records. The native bundle identifiers and the compatibility-sensitive
protocol namespace strings remain unchanged.

User-facing provenance and settings copy now says **local curation** rather
than advertising the constitutional project name. The internal
`org.radical-liberal.*` identifiers remain in schemas, tests, and migration
code where changing them would break compatibility or import behavior.

The like latency defect was localized to `src/state/cache/post-shadow.ts`:
direct post queries (`['post', uri]`, including the public-fallback key) were
not included in the optimistic shadow update search. A like on a feed could
look immediate while a like from a direct post/quote view waited for the PDS
round trip. `src/state/cache/post-shadow-cache.ts` now includes those direct
queries. The heart/count update remains local and optimistic, a pending state
is exposed to accessibility/UI, and the durable `app.bsky.feed.like` write
still goes to the user's PDS and is reconciled with the server result.

Focused verification passed:

- `src/lib/brand.test.ts`: neutral name/origin resolution;
- `src/state/cache/post-shadow-cache.test.ts`: direct post cache coverage;
- `pnpm typecheck:web`;
- targeted `oxlint` over all changed client files;
- `git diff --check`.

The exact static deployment handoff, DNS/HTTPS requirements, and current
unverified DNS state are documented in `docs/SOCIAL_EDRIFFLES_DEPLOYMENT.md`.
No DNS record or hosting account was changed by this repository-only repair.

## Account-scoped neutral defaults and feed-customization addendum

The owner requested that the current `edriffles.us` feed profile remain intact
without becoming a default for other accounts. The actual implementation now
separates those concerns at every relevant state boundary:

| Boundary | Implementation | Verified behavior |
|---|---|---|
| New-account curation | `upstream/social-app/src/lib/feed-sovereignty/radlib-curation.ts` | `defaultLocalCurationConfig` is disabled, has no exclusions or curation terms, and contains no branch weights. Legacy branch fields are import-compatible but inert. |
| New-account content filter | `upstream/social-app/src/lib/feed-sovereignty/content-filter.ts` | `defaultContentFilterPolicy` is empty and disabled. Legacy term-pack/strict fields are opaque and inert; only custom terms entered by the current account are evaluated. |
| Stored personalization | `upstream/social-app/src/lib/personalization.ts` | Storage is keyed by `PERSONALIZATION_V1:<accountDid>`. Exact matches to the old implicit defaults migrate to neutral; an edited profile, including the owner's weights and exclusions, is preserved. |
| Local feed state | `upstream/social-app/src/state/preferences/local-feed.tsx` | Account switches reset to fresh neutral state before loading the next DID's profile, preventing the prior account's ranking/filter state from being used during the loading window. |
| Selected home feed | `upstream/social-app/src/state/shell/selected-feed.tsx` | Browser-session selection is stored as `lastSelectedHomeFeed:<accountDid>` and reset on account changes; the previous shared session key is no longer read. |
| Settings naming | `src/Navigation.tsx`, `src/screens/Settings/Settings.tsx`, `src/screens/Settings/PersonalizationSettings.tsx` | The route/menu is `Feed customization & data`; the bottom summary is `Home feed mode`. The screen says the profile is for “this account and device only.” |
| Provider default | `services/radlib-filtered-feed/src/policy.ts` | The provider starts with no content terms. Legacy pack identifiers are preserved as opaque metadata but never expand into provider vocabulary. |
| Public artifact | `upstream/social-app/web-build/` on `social.edriffles.us` | The static bundle contains no owner personalization state. The logged-out browser showed `Discover — Social` and a neutral empty starting feed, not the owner's tuned feed. |

The owner-specific values visible in the local authenticated settings screen—K-pop,
audio, explicit interests, custom exclusions, and selected content packs—are
there because they already exist in the owner's device-local state. They are
not source defaults, PDS records, feed-generator configuration, public HTML,
or a shared provider policy. A second account receives neutral defaults and
can customize them independently on the same site.

The production build intentionally has no default feed-owner DID until a real
neutral feed generator is registered and populated. This is an explicit
capability boundary: the public site is deployed and functional as a Social
client, but the logged-out Discover slot is empty rather than impersonating a
provider or exposing the owner's feed. After sign-in, Following remains the
chronological first-class path, and users can save/select their own feeds.

Focused verification for this addendum:

```sh
cd /var/home/tcs/Code/atproto/upstream/social-app
pnpm test -- src/lib/feed-sovereignty/radlib-curation.test.ts src/lib/personalization.test.ts src/state/preferences/local-feed.test.ts
pnpm typecheck:web

cd /var/home/tcs/Code/atproto/services/radlib-filtered-feed
pnpm test

cd /var/home/tcs/Code/atproto
python3 -m unittest tests/test_social_app_wiring.py
python3 scripts/validate_contract.py
git diff --check
```

Result: client focused tests passed (33 tests), provider tests passed (24
tests), wiring tests passed (5), contract validation passed, and the
production Webpack export completed with the existing optional Expo/router
and bundle-size warnings. The rebuilt artifact was uploaded to Cloudflare
Pages at `https://54456c49.social-edriffles.pages.dev`; the active custom
domain `https://social.edriffles.us/` returned HTTP 200 and rendered the
neutral shell in the browser. Owner acceptance remains pending.

The final broad regression pass also completed with root unittest `92 passed`
and client Jest `85 suites passed, 898 passed, 28 todo, 21 snapshots`; web
typecheck passed. The service-side filtered-feed suite passed all 24 tests.

## Settings label catalog repair addendum

The owner-facing Settings menu briefly rendered generated Lingui message IDs
(`MILoeL` and `ISLPlf`) instead of the route names because the English source
catalog had not been regenerated after the custom Settings labels were added.
Running `pnpm intl:extract --clean --locale en` followed by `pnpm intl:compile`
restored the explicit English entries for `Services` and `Feed customization &
data`. `tests/test_social_app_wiring.py` now checks those catalog entries so a
future production build cannot silently expose message IDs. The rebuilt Pages
deployment `https://54456c49.social-edriffles.pages.dev` was opened at
`/settings`; the rendered menu now shows `Services` and `Feed customization &
data`.

## Neutral algorithm-customization addendum

The owner identified the remaining misleading default: the authenticated
personalization screen showed K-pop/music, political-economy, technology, TV
comedy, and audio branch weights even when no topic had been selected. Those
controls looked like an opinionated product default, and the prior “Add
curation term” control actually wrote to the exclusion list.

The repair makes `curationTerms` the only positive vocabulary in the local
personalization profile. New profiles start with `curationTerms: []`; the
scorer does whole-term matching only against terms explicitly entered by the
current account. There is no bundled topic taxonomy, hidden synonym expansion,
or branch-emphasis UI. Legacy `branchWeights` fields remain import-readable
but are optional, ignored by scoring, and absent from new profiles. The screen
now exposes only generic term and exclusion controls.

The same boundary now applies to the filtered-feed service and content filter:
legacy `termPacks` and strict-mode fields are accepted as opaque compatibility
data but are inert. Only account/deployment-supplied custom terms are matched.
This removes the owner-specific vocabulary from the production ranking and
filtering code while preserving the owner's existing device-local custom terms.

This follows the research record in
[`docs/ALGORITHM_CUSTOMIZATION_RESEARCH.md`](ALGORITHM_CUSTOMIZATION_RESEARCH.md):
Bluesky makes feed choice/provider identity explicit, YouTube and Meta expose
reversible direct feedback, Instagram separates Following/Favorites from
recommendation controls, TikTok scopes topic sliders to For You, and Mastodon
uses explicit user-created lists and scoped filters. The implementation does
not adopt any vendor's hidden ranking policy; it adopts the common, testable
control boundaries and neutral bootstrap.

Focused verification for this repair:

```sh
cd /var/home/tcs/Code/atproto/upstream/social-app
pnpm test src/lib/feed-sovereignty/radlib-curation.test.ts src/lib/personalization.test.ts src/state/preferences/local-feed.test.ts --runInBand
pnpm typecheck:web

cd /var/home/tcs/Code/atproto
python3 -m unittest tests/test_social_app_wiring.py
python3 scripts/validate_contract.py
```

Owner acceptance remains pending. The working tree is intentionally not
reported clean because it contains the broader fork work and review history.

## Vocabulary-removal verification addendum — 2026-08-19

The final source audit found no owner-specific curation or filtering vocabulary
in the active client or filtered-feed provider production paths. New local
profiles contain no topic terms, branch weights, or content-filter packs. The
only active positive/filter vocabulary is supplied by the current account (or,
for the optional provider, its explicit deployment configuration). Legacy
branch, pack, and strict-mode fields remain only as opaque import-compatible
data and do not influence ranking or filtering.

Rendered verification at `/settings/personalization` showed generic curation
term controls and no branch/topic-weight controls. The owner account's
previously stored device-local custom terms remain visible only in that
account's local profile, as requested; they are not source defaults or shared
provider state. A fresh profile therefore starts neutral and can be customized
independently.

Current verification results:

- client Jest: `85 suites passed, 898 passed, 28 todo, 21 snapshots`;
- client focused curation/personalization/local-feed tests: `33 passed`;
- client web typecheck: passed;
- provider suite: `24 passed`;
- root unittest suite: `92 passed`;
- contract validation: passed (`111 files`, `29 blocking rows`, `6 feed cases`);
- production web build: passed, with existing optional Expo/router and bundle-size warnings;
- live provider walkthrough: passed, with only an explicitly configured custom term filtered.

The latest changes are verified in the local checkout and local browser. They
are not represented by the existing public Pages deployment because the
Cloudflare credentials/Pages route remain unavailable. `OWNER_ACCEPTANCE`
therefore remains `PENDING`, and the dirty worktree remains a release blocker.

## Curation-term entry and accessibility verification addendum — 2026-08-19

The owner reported that adding a curation term did not work and that the
personalization page was difficult to use. The cause was split between the
source UI and deployment state: the public hostname was still serving an older
bundle whose visible `Add curation term` action wrote to the exclusion list,
while the local checkout already had the neutral positive-term model.

The current client replaces the ambiguous controls with reusable, labeled entry
rows. Each row has a visible purpose label, a text field, an adjacent real
`Add term`/`Add exclusion`/`Add filter`/`Add interest`/`Add preference` button,
Enter-to-submit, disabled-empty behavior, and a polite confirmation message.
The same treatment is used for author DID entry, with validation before the
action is enabled. Removing a term also reports the completed change. These
controls remain account- and device-local; the owner’s existing local terms
were not changed.

This follows the existing Edriffles Computer Web contract in
[`docs/design/ECW_CURRENT.md`](design/ECW_CURRENT.md) and
[`docs/design/ECW_TOKENS.md`](design/ECW_TOKENS.md): explicit labels, real
buttons, visible structure, keyboard access, focusable controls, and no
color-only state. The accessibility review also follows the W3C guidance for
[WCAG 2.2](https://www.w3.org/TR/WCAG22/),
[form notifications](https://www.w3.org/WAI/tutorials/forms/notifications/),
and the [ARIA Button Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/button/).

Rendered local-browser checks at `/settings/personalization` passed:

- empty `Add term` is disabled;
- pointer entry adds a disposable term and reports success;
- Enter entry adds a disposable term;
- removal reports success and the disposable terms are absent after reload;
- the page exposes the generic positive-term row and no retired topic-weight
  labels;
- the owner’s stored local exclusions and explicit interests remain present.

The exact production export also passed. The emitted local bundle is
`main.f757c6d4.js` and contains `Add a term to prioritize`, `Add term`, and
`Local curation terms`, while the retired topic-weight labels, `Add curation
term`, and bundled political term-pack labels are absent. The public HTML still
references `main.d1a2465f.js`, and its public bundle still contains the old
`Add curation term` string. This was the public-state observation before the
Cloudflare deployment recorded in the addendum below; it is superseded by that
deployment verification.

Current automated state after the repair:

- focused curation/personalization/local-feed tests: `33 passed`;
- client web typecheck: passed;
- root wiring tests: `5 passed`;
- production web export: passed with the existing optional Expo/router and
  bundle-size warnings;
- contract and broad-suite results remain as recorded above;
- `OWNER_ACCEPTANCE_PENDING`; working tree remains dirty.

## Cloudflare Pages deployment and deep-link verification addendum — 2026-08-19

The public bundle was deployed through the authorized Cloudflare MCP after the
local build and checks passed. The first upload exposed a hosting defect during
the browser walkthrough: Expo emitted route-relative entrypoint URLs, so a
direct visit to `/settings/personalization` requested `/settings/static/...`
and stayed on the splash screen. This was a production-serving defect, not a
client ranking or personalization defect.

The bounded repair is in
[`upstream/social-app/scripts/post-web-build.js`](../upstream/social-app/scripts/post-web-build.js):
the post-build step rewrites relative `src`/`href` entrypoint URLs to
root-relative paths while leaving absolute, data, and fragment URLs unchanged.
The new wiring regression test checks the generated production shell for
route-relative assets.

Final deployment evidence:

- Cloudflare Pages project: `social-edriffles`;
- production deployment: `99d240b7-66fa-40d8-a176-fec18bbc1b25`;
- deployment hostname: `https://99d240b7.social-edriffles.pages.dev`;
- deployment stage: `success`;
- custom hostname cache purged for `social.edriffles.us`;
- custom and deployment host `/settings/personalization`: HTTP `200`;
- both shells reference `/static/js/main.f757c6d4.js`;
- both bundles expose the generic curation-term labels and omit the retired
  topic-weight and bundled political-pack labels;
- the signed-in in-app browser loaded the direct custom-hostname route and
  rendered `Feed customization & data`, `Add a term to prioritize`, and
  `Add term`.

The deployment proves that this export is being served; it does not prove
owner acceptance. `OWNER_ACCEPTANCE_PENDING` remains unchanged, and the
working tree remains dirty because the broader fork work and review history
are still present.

## Public GitHub publication addendum — 2026-08-19

The reviewed commits were published to public repositories under the owner's
GitHub account after a tracked-file credential scan found no access tokens,
private keys, or credential files:

| Repository | Visibility | Branch | Reviewed commit |
|---|---|---|---|
| `https://github.com/Shikibashi/social-edriffles` | public | `codex/private-accounts-communities` | `676af35` |
| `https://github.com/Shikibashi/social-app` | public fork | `codex/private-accounts-communities` | `3dff4b0d` |
| `https://github.com/Shikibashi/atproto` | public fork | `codex/private-accounts-communities` | `c1a8b80f` |

The root `.gitmodules` now points at the two public forks, and its submodule
pointers resolve to the published client and PDS commits. Publication does
not change the owner-acceptance state: `OWNER_ACCEPTANCE_PENDING` remains
required.

## Final live provider-attribution verification — 2026-08-19

The corrected production bundle was published through the authorized Cloudflare
MCP after a successful production web export:

- Pages project: `social-edriffles`;
- deployment: `6b00d319-8b1f-4410-86e0-b01d8fa5b179`;
- deployment host: `https://6b00d319.social-edriffles.pages.dev`;
- custom-host alias: `https://social.edriffles.us`;
- deployment stage: `success`.

The live authenticated browser walkthrough used a cache-busting query solely to
avoid a stale browser bundle. It did not mutate the account or local
personalization state. The corrected Services screen now says:

```text
Public Bluesky AppView (explicit read provider)
did:web:api.bsky.app · https://api.bsky.app
```

It continues to show the account PDS separately as
`https://yellowfoot.us-west.host.bsky.network/`. The prior live label
`Project AppView` was inaccurate for this configured public endpoint and has
been repaired in `upstream/social-app/src/state/session/providers.ts`, with a
focused regression test in
`upstream/social-app/src/state/session/__tests__/providers-test.ts`.

The live Home provenance card identifies the active `For You` feed, the
`content-filter/1 + local-curation/1` overlay, provider DID
`did:web:api.bsky.app`, feed owner DID
`did:plc:3guzzweuqraryl3rdkimjamk`, the feed URI, unverified manifest status,
the actual local-curation objective, and device-local privacy scope. This
confirms provenance fidelity for the deployed client. It does not establish a
first-party AppView, an independent neutral Discover feed, or authenticated
alternate-provider switching; those remain owner-acceptance questions and are
not being presented as complete.

The final automated state remains `OWNER_ACCEPTANCE_PENDING`. Owner-result
fields remain intentionally blank, and the report does not claim
`OWNER_ACCEPTANCE_PASSED`.

## Final acceptance remediation and live verification — 2026-08-19

The final remediation commits are now published on the public feature
branches:

- client: `3dff4b0d4201b001ec5e85c83ccacffd5970bd2c`;
- PDS: `c1a8b80f06029bdbadae59ff7f517da25163e96f`.

The client production export was rebuilt after fixing the two new settings
route titles and the Privacy & Security destination labels. The full client
suite passed (`85` suites, `901` passed tests, `28` todo, `21` snapshots), web
type-check passed, focused PDS private-permission suites passed (`5` suites,
`20` tests), and the production export completed with only the repository's
existing Expo/router and bundle-size warnings.

Cloudflare Pages deployment `7d6c7dcb-17fd-4932-8f1b-e5dc429d22f8` is
production-successful and aliases `https://social.edriffles.us`. The signed-in
browser loaded the final `main.d563bed3.js` bundle and verified:

- `/settings/protected-access` displays `Protected access` as both visible
  content and its document title;
- `/settings/private-spaces` displays `Private spaces and communities` as its
  document title and visible private-space controls;
- `/settings/privacy-and-security` visibly lists both new destinations;
- `/settings/identity-sovereignty`, `/settings/personalization`, and Home
  still render their provider, session, local-preference, and feed surfaces;
- the old opaque route-title IDs and inaccurate `Project AppView` label are
  absent from the verified live routes.

The prior local-only run left checklist item 60 open because it had not yet
exercised the repository's real downstream AppView topology. The follow-on
audit below closes item 60 for the current architecture. At that point private
feeds and multi-PDS federation were still separate capability gaps; the later
P6/P10 addendum below records their bounded implementation. No owner-result
field was filled; `OWNER_ACCEPTANCE_PENDING` remains the required state.

## Checklist item 60 implementation addendum — 2026-08-19

Checklist item 60 is now implemented and tested for the current topology. The
automated state is `PASS`: the real local `TestNetwork` exercises the PDS,
downstream public repository subscription, and public AppView. The separate
private-AppView and multi-PDS capabilities remain explicitly unimplemented and
are tracked by P6/P10 rather than treated as evidence of public leakage.

### Implemented changes

- `upstream/atproto-pds/packages/pds/src/permissioned-data/store.ts` remains a
  separate SQLite/blob plane; the new integration test writes deterministic
  body and blob canaries through that plane.
- `upstream/atproto-pds/packages/pds/tests/private-permission-api.test.ts`
  now captures the public `com.atproto.sync.subscribeRepos` WebSocket, checks
  that the public sequencer cursor does not advance, parses the public CAR with
  `readCarWithRoot`, and checks every public block for the private body, blob
  bytes, blob identifier, and private record CID. Its `TestNetwork` case also
  drains the real downstream AppView subscription and checks AppView profile,
  author-feed, search, and indexed-post surfaces for the private canary.
- `upstream/atproto-pds/packages/pds/src/api/org/radlib/private/index.ts`
  applies `Cache-Control: private, no-store` and
  `Vary: Authorization, DPoP` before authentication, after successful
  authentication, and on authentication failure. This closes the failure
  response path that could otherwise be downgraded to ordinary `private`.
- `upstream/atproto-pds/packages/pds/src/error.ts` reapplies the same policy at
  the final private-route error boundary for parameter, authorization, and
  handler failures.
- `upstream/atproto-pds/packages/pds/src/logger.ts` redacts private XRPC query
  strings and removes parsed private query/route objects from the Pino request
  serialization. `tests/logger.test.ts` covers private and public requests.
- `upstream/social-app/src/state/queries/util.ts` rejects private Radlib query
  roots from the persisted React Query snapshot even if a future private query
  is accidentally given the ordinary structured persistence shape. The client
  regression test covers private roots and ordinary persisted queries.

### Evidence and commands

From `upstream/atproto-pds/packages/pds`:

```sh
../../node_modules/.bin/tsc --build tsconfig.build.json --pretty false
NODE_OPTIONS=--experimental-vm-modules \
  ../dev-infra/with-test-redis-and-db.sh ../../node_modules/.bin/jest --runInBand \
  tests/private-permission-api.test.ts tests/private-permission-store.test.ts \
  tests/permissioned-policy.test.ts tests/sync/subscribe-repos.test.ts \
  tests/logger.test.ts
```

Result: **5 suites, 29 tests passed**; PDS TypeScript build passed.

From `upstream/social-app`:

```sh
NODE_ENV=test node_modules/.bin/jest --runInBand \
  src/state/queries/util.test.ts src/lib/permissioned-data.test.ts
node_modules/.bin/tsc --project ./tsconfig.check.web.json --pretty false
```

Result: **2 suites, 4 tests passed**; web TypeScript check passed.

The public sync endpoint intentionally returns an empty CAR with HTTP 200 for
an absent public record, so the test checks the body and parsed public CAR for
absence of private canaries rather than treating that normal protocol response
as an error. The private unauthenticated lookup fails closed and carries the
non-cacheable response headers.

### Remaining architecture, not an item-60 defect

This checkout still does not implement a private AppView/indexer,
proposal-0016 multi-PDS credentials, durable replica/import, or a public Relay
carrying permissioned events. The fork's PDS-local private feed and direct
capability-pull contract are implemented below; the current product still
deliberately keeps private records outside the public topology, and the
production-like audit proves that boundary. External proxy/CDN logs and
multi-device persistence remain deployment-specific; the PDS response contract
is `private, no-store` and the client denylist prevents local persisted
snapshots. Item 60 is therefore `PASS`, while `OWNER_ACCEPTANCE_PENDING` is
unchanged and no owner-result field was filled.

## P6/P10 implementation addendum — 2026-08-19

The remaining local capability gaps were implemented as a bounded fork-owned
contract. This does not claim upstream proposal-0016 compatibility or a private
AppView.

### P6 — viewer-authorized private feed

- `org.radlib.private.getFeed` reads only `org.radlib.private.post` records
  from the authenticated PDS private store.
- The handler resolves the space for the viewer, rechecks the current ACL and
  direct-block boundary, filters blocked authors, and returns `providerDid` so
  the UI identifies the actual PDS supplying the feed.
- `upstream/social-app/src/state/queries/private-feed.ts` hydrates the feed
  from the account PDS. `PrivateFeedScreen.tsx` is linked from the private-space
  settings surface at `/private-feed` and states that the public AppView, Relay,
  and public repository are not involved.
- `radlib-private-feed` is covered by the existing client persistence denylist.

### P10 — direct PDS-to-PDS capability pull

- `org.radlib.private.createSyncGrant` creates a random bearer capability and
  stores only its SHA-256 hash. It is scoped to one source space, target PDS
  DID, target actor DID, optional collection, and an expiry no more than 30 days
  away.
- `org.radlib.private.syncPull` is a POST endpoint intended for direct PDS
  consumers. It checks token, space, target identities, collection, expiry, and
  revocation on every pull. The disposable test starts separate source and
  target PDS identities and pulls using the target identity. It returns private
  records only in the response; it does not publish a repository event, CAR
  block, Relay frame, or AppView row.
- `org.radlib.private.revokeSyncGrant` invalidates a grant immediately. The
  source remains authoritative because this pass does not create a stale
  durable target-side replica.
- `PDS_PRIVATE_SYNC_ENABLED` is opt-in and defaults off. The fork namespace is
  explicit; this is not presented as an ATProto standard or as proposal-0016
  space credentials.

### Evidence and commands

The PDS store/API tests cover private-feed hydration, grant target binding,
collection scoping, expiry validation, revocation, and public CAR exclusion:
**5 suites, 31 tests passed**. The client regression remains **2 suites, 4
tests passed**, and its web typecheck covers the new query/screen/route and
generated lexicons. The exact focused PDS command is:

```sh
cd /var/home/tcs/Code/atproto/upstream/atproto-pds/packages/pds
NODE_OPTIONS=--experimental-vm-modules \
  ../dev-infra/with-test-redis-and-db.sh ../../node_modules/.bin/jest --runInBand \
  tests/private-permission-api.test.ts tests/private-permission-store.test.ts \
  tests/permissioned-policy.test.ts tests/sync/subscribe-repos.test.ts \
  tests/logger.test.ts
```

The owner checklist rows 67–68 describe the live/disposable walkthroughs and
remain automated `PASS` with owner notes unfilled. Owner acceptance remains
`OWNER_ACCEPTANCE_PENDING`; the overall automated verdict remains
`RADLIB_CODEX_ACCEPTANCE_BLOCKED` because other constitutional/product gaps and
owner-only judgments still remain.
