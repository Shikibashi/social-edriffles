# Historical Block Presentation Matrix

> Status: `HISTORICAL_RETIRED`. This document records an earlier disposable
> read-provider experiment. It is not an active provider, dependency, launch
> target, or acceptance claim. Current service behavior is tested through the
> first-party PDS and generic explicitly selected providers.

Date: 2026-08-17. Former read-provider experiment: archived local revision
`8abe96490df889cc1c5d1a5b15eef8650d2ad2a7` (historical baseline only).

## Fixture

Disposable PDS: `http://127.0.0.1:2583`.
Former read provider: `http://127.0.0.1:61754`.

- A: `did:plc:ptfwt757i5syd7u63zlv6cca`
- B: `did:plc:4tmyiq3rpcjqhhf24xfvueqo`
- C: `did:plc:t3myuj4fumsmxgtcoxdr5lg5`
- A→B block record: `at://did:plc:ptfwt757i5syd7u63zlv6cca/app.bsky.graph.block/3mtb4vghltd2l`
- Fixture records and raw observations: `artifacts/live-block-presentation-observations.json` and `artifacts/live-block-presentation-surface-summary.json`.

All records were created before the final A→B block unless explicitly identified as a post-block interaction probe. No pre-block records were deleted.

## Matrix

| Surface | Record/context | Viewer A | Viewer B | Viewer C | Anonymous | Historical read-provider behavior | Current Bluesky-reference behavior | Target fork behavior | Production change required? |
|---|---|---|---|---|---|---|---|---|---|
| Profile | B profile | `blocking` URI | no block flags | neither | not tested here | Standard viewer state; A blocks B, B is blocked by A, C is unrelated | Standard viewer state; relationship is viewer-relative | Preserve standard viewer state | No further change |
| Basic profile | B in profile/list view | relationship fields available through profile conversion | same | same | not separately queried | Uses the same viewer-state conversion | Standard viewer state | Preserve standard viewer state | No further change |
| Detailed profile | B detailed profile | relationship fields available | same | same | not separately queried | Uses the same viewer-state conversion | Standard viewer state | Preserve standard viewer state | No further change |
| `getBlocks` | A's block list | B returned, HTTP 200 | unauthenticated list not applicable | not applicable | not applicable | Authenticated controller returns B with cursor support | Reference returns the viewer's block records | Preserve protocol-compatible list | Implemented locally; no new patch |
| Author feed | `getAuthorFeed(A/B)` | A and B author feeds both returned public records to A | same | C received both actors' public feed records | Anonymous received both | No collateral block suppression in actor-specific feeds | Reference applies viewer-aware filtering in feed presentation where block rules require it | A/B should lose direct association; C retains public records | Future policy decision; do not patch before broader review |
| Timeline/following | `getTimeline` | HTTP 200, empty in this fixture | HTTP 200, empty | HTTP 200 with explicit A/B boundary posts | HTTP 500 | Explicit follow-state fixture showed C retains both A/B posts; A/B were empty after relationship state changed; anonymous remains unsupported | Reference timeline presentation applies viewer block policy | C should retain A/B public records | No semantic patch; retain as fixture-specific behavior |
| Root thread | `AR`, `BR2` | Normal `threadViewPost` | Normal `threadViewPost` | Normal `threadViewPost` | Normal `threadViewPost` | A/B/C/anonymous all retained the public root | Reference may return `notFoundPost` for viewer-blocked anchors | A/B direct severance; C retains root | Future policy decision |
| Reply | `BR→AR`, `AR2→BR2` | Normal post views; replies retained | Normal post views; replies retained | Normal post views; replies retained | Normal post views; replies retained | No third-party suppression observed; C retains both reply chains | Reference presentation can emit `blockedPost` or omit third-party block-violating replies | C retains otherwise-public replies | Future policy decision |
| Quote | B quotes A1; A quotes B1 | Both quote records searchable/hydratable | same | both searchable/hydratable | both searchable/hydratable | Quote embeds hydrated as normal record views; no C collateral suppression observed | Reference applies viewer-relative block presentation to embedded authors | C retains public quote and may choose local display policy | Future policy decision |
| Repost | B reposts A1; A reposts B1 | No supported direct repost-thread representation; probe produced not-found placeholder | same | same | not tested separately | Repost records were written, but this AppView surface did not expose a stable hydrated repost item in the tested feeds/search | Reference exposes reposts through feed views with viewer-aware post presentation | C retains public reposts unless source post is unavailable | Need a dedicated supported repost/feed query fixture |
| Search | `searchPosts` ordinary/quotes; `searchActors` | HTTP 200; A/B results visible | same | same | ordinary/quote search HTTP 200 | Search returned A/B ordinary and quote records for every authenticated viewer and anonymous | Reference search presentation is viewer-aware for blocked subjects | C retains public search results | Future policy decision |
| Notifications | post-block reply/follow probes | HTTP 200; no B-originated direct notification observed | HTTP 200; no A-originated direct notification observed | HTTP 200; empty | HTTP 200 | Direct notification suppression held while PDS accepted the writes; C was unaffected | Reference suppresses direct blocked interactions and notifications | Preserve direct nonassociation; do not suppress C | No change to direct notification protection |

## Direct interaction probe

The disposable PDS accepted B's post-block reply, mention, and follow writes. This demonstrates that the PDS write surface does not enforce the relationship. The former read provider did not deliver corresponding direct notifications to A/B in the observed notification responses. This is not evidence that all direct interactions are blocked at every write surface; it is evidence to preserve the distinction between PDS record acceptance and read-provider presentation/enforcement.

## Reference comparison

The current Bluesky reference source describes block presentation in `packages/bsky/src/api/app/bsky/feed/getPostThread.ts` and `packages/bsky/src/views/index.ts`:

- viewer-blocked anchors can become `app.bsky.feed.defs#notFoundPost`;
- third-party block-violating thread nodes can become `app.bsky.feed.defs#blockedPost` or be omitted;
- profile viewer state remains relationship-relative (`blocking`, `blockedBy`);
- privileged/internal requests can opt into different third-party block handling.

The former read provider did not reproduce those presentation transformations in the tested thread/feed surfaces. This report characterizes that historical difference; it does not copy the reference policy into production.

## Decision

C retained otherwise-public A/B roots, replies, quote records, author-feed records, and search results in this fixture. No collateral third-party suppression was observed on those tested surfaces. Therefore no production presentation patch is justified by this run. A future policy patch, if approved, should target the exact presentation functions for thread replies, feed hydration, quote embeds, and repost hydration—not relationship indexing or standard viewer-state fields.

## Unsupported or incomplete

- No stable repost hydration surface was available in the former read-provider build.
- Anonymous timeline returned HTTP 500.
- Direct PDS write acceptance is not equivalent to client/AppView interaction authorization.
- Deletion, takedown, suspension, private/permissioned data, threadgates, postgates, legal restrictions, and list-block behavior were not altered or claimed.
## Association safety boundaries

These characterization-only safety probes are separate from relationship-state and third-party presentation claims.

| Boundary | Evidence | Result | Association implication |
|---|---|---|---|
| Explicit timeline | C followed A and B; A/B/C timeline queries were separate | C received both explicit A/B timeline posts; A/B were empty in this fixture; anonymous returned HTTP 500 | Do not infer timeline policy from author feeds; retain C's public records |
| Deletion | A post was deleted through `com.atproto.repo.deleteRecord` | A, B, C, and anonymous received 404 for record/thread retrieval | Viewer sovereignty never resurrects deleted records |
| Record takedown | PDS admin status update with a strong record reference | AppView returned `RecordNotFound` | Service removal dominates presentation |
| Account takedown | PDS admin account takedown | PDS login returned `AccountTakedown`; AppView refreshed state to a placeholder profile and empty author feed | Service removal dominates presentation |
| Threadgate | B root with restrictive threadgate and C reply probe | AppView omitted the reply from the thread | Visibility does not grant interaction authorization |
| Postgate | B postgate disallowing embeds and C quote | Quote remained, embedded record view was detached/empty | Quote detachment is not deletion |
| Permissioned data | Disposable stack probe | Unsupported/untested | Do not simulate public visibility |
| Listblock | C list, list item, and listblock records | Raw list/list-item/listblock records remain readable/indexed; effective `blockingByList` is not exposed and listblock is inert | Preserve raw records; offer list mute and explicit member review, never delegated hard blocking |

These results are recorded in `artifacts/live-block-presentation-observations.json`. No semantic presentation patch was applied.
