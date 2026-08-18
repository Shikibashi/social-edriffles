# Radical-Liberal Codex Acceptance Review

## Automated state

`RADLIB_CODEX_ACCEPTANCE_READY_FOR_OWNER`

This is an automated handoff state, not owner approval. `OWNER_ACCEPTANCE_PENDING` remains the final owner state. No owner-result cell in the checklist has been filled.

P0: **0**
P1: **0**
P2: **6**
P3: **1**

The P0/P1 gate is clear after bounded repairs. Remaining P2/P3 entries are capability breadth, upstream, environment, or scope questions rather than known local violations of the stated owner intent.

## Scope and inspected revisions

The review used the checked-out fork and all current submodules. No upstream rebase or moving-branch fetch was performed.

| Tree | Inspected revision | Pin/candidate meaning |
|---|---|---|
| Parent fork | `51d637a40d1782ae52b49f87000dec7cafc4c416a` before this review's parent-doc changes | Current parent checkout at inspection start |
| `upstream/social-app` | `c38bfe515a9d52d2b9969c8ead64eced5f8d33ee` | Reviewed radical-liberal candidate after the repair commit |
| `upstream/AppViewLite` | `ab3ac9ec20e234746d6978f74567bae67b53137e` | Current AppViewLite submodule |
| `upstream/FishyFlip` | `da2c08aa19475eb2c732933d213a374f03a8e549` | Current FishyFlip submodule |
| Declared protocol baselines | AppViewLite `75f78e8e098c05f52821e836832205050c0f539e`; social-app `1f5c698165c922e707833809902ee959e9824f00` | Unchanged in `upstream-pins.json` |

`artifacts/upstream-baseline.json` now binds the reviewed local candidate SHA for the read-only checkout gate. This records candidate provenance; it is not an upstream rebase. `python3 scripts/check_upstream.py --fast` reports all three current trees `CURRENT`.

## Product run and evidence boundary

The strongest available production-like web run was the actual `upstream/social-app` web app, launched with:

```sh
cd /var/home/tcs/Code/atproto/upstream/social-app
pnpm install --frozen-lockfile
pnpm web -- --port 8081
```

The Expo web wrapper exposed the compiled app at `http://127.0.0.1:19006/`. A real authenticated browser session rendered the following without relying on source text alone:

- Home / Following with real posts.
- Saved/custom feed selection and the real Science custom feed.
- Services settings showing the account PDS separately from the Bluesky AppView.
- Personalization settings showing Discovery, Variety, Freshness, Exploration, Quiet Metrics, export, reset, and import controls.
- Following-feed settings showing local reranking controls.
- Following provenance: `Following / chronological (version not declared) · Bluesky AppView`, provider DID, `Manifest: unverified`, chronological objective, local-preferences privacy scope, and health-unknown state.
- Science-feed provenance: provider-supplied ranking, Bluesky AppView DID, feed-owner DID, unverified manifest, and undeclared provider objective.

No live account follow, unfollow, block, mute, More-like-this, Less-like-this, provider mutation, export, reset, import, or recovery mutation was made. Those behavior-changing cases are deterministic-test or owner-walkthrough cases below. This is intentional evidence scoping, not a claim that all owner actions were live-executed.

The exact owner launch command is in `docs/OWNER_ACCEPTANCE_CHECKLIST.md`.

## Principle-to-implementation map

| Principle | Runtime implementation | User-facing surface | Verification |
|---|---|---|---|
| Individual sovereignty / identity | `upstream/social-app/src/lib/identity-runtime.ts`, `src/state/session/session-core.ts`, recovery state | Identity, sessions, recovery/lockdown settings | `src/lib/identity-runtime.test.ts`, `src/lib/identity-recovery.test.ts`, session tests |
| Pairwise freedom of nonassociation | Pinned AppViewLite relationship core and viewer-relative state; no new local suppression layer | Profile/block controls and public presentation | `tests/test_appviewlite_characterization.py`, `tests/test_live_block_presentation.py`, live A/B/C artifacts |
| Third-party independence | No local fork-wide block filter added to C's public presentation | Threads, author feeds, quotes, search, Home | `docs/LIVE_BLOCK_PRESENTATION_MATRIX.md`, live-block observations |
| Freedom of association | `src/components/PostControls/PostMenu/PostMenuItems.tsx`, `src/state/feed-feedback.tsx` | Follow, unfollow, block, mute, More/Less menus | `src/lib/feed-sovereignty/profile.test.ts`, social Jest suite, A/B/C fixtures |
| Attention sovereignty | `src/lib/feed-sovereignty/profile.ts`, `src/view/com/posts/PostFeed.tsx` | Following, local reranking, discovery controls, custom feeds | `src/lib/feed-sovereignty/profile.test.ts`, feed wiring tests, live browser smoke |
| Algorithm marketplace | `src/lib/balanced.ts` and provider registry in `src/state/session/providers.ts` | Following/custom feeds are live; Balanced remains library-only in this candidate | `src/lib/balanced.test.ts`, provider tests, owner checklist |
| Explicit preference dominance | Durable local post/topic/author preferences in `src/lib/personalization.ts` and `src/state/preferences/local-feed.tsx`; explicit tier weight `2.5` and URI > author > topic precedence | More/Less post controls and personalization settings | `src/lib/feed-sovereignty/profile.test.ts`, `src/lib/personalization.test.ts` |
| Controlled serendipity | `explorationLevel` and `explorationFloorForLevel()` in `src/lib/feed-sovereignty/profile.ts`; explicit avoids are excluded from exploration | Low/Default/High discovery setting | deterministic low/default/high composition tests |
| Attention transparency | `src/lib/attention-ui.ts`, `src/components/FeedProvenanceCard.tsx`, `src/view/com/feeds/FeedPage.tsx`, `src/screens/CustomFeed/index.tsx` | Provider/feed/owner/manifest/objective/privacy/health card and Why-this-post trace | `src/lib/attention-ui.test.ts`, profile trace tests, live provenance smoke |
| Polycentric services / explicit fallback | `src/state/session/providers.ts`, `clients.ts`, `session-core.ts`, `index.tsx`, `react-query.tsx`, `persisted-query-storage.ts` | Services settings and named provider errors | provider, session, client, and persisted-storage tests |
| Portable personalization | `src/lib/personalization.ts`, `src/state/preferences/local-feed.tsx`, `src/screens/Settings/PersonalizationSettings.tsx` | Inspect/export/reset/import | personalization tests and root secret audit |
| Privacy minimization | Export allowlists, credential-like key/value rejection, local-only More/Less | Personalization export/import controls | `src/lib/personalization.test.ts` |
| Institutional anti-reification | Actual PDS/AppView/provider/feed-owner identities and named failures | Services and provenance surfaces | provider tests, attention UI tests, live browser smoke |
| Political neutrality | No political/demographic quota or classifier in the constitutional ranking path | No ideological selector is forced; user-selected topics/feeds remain possible | targeted static audit and root neutrality tests |

## Findings by severity

### P0 — none

No credential leakage, hidden durable association mutation, local pairwise-block violation, political quota/classifier enforcement, or silent materially different-provider substitution remains in the reviewed path.

### P1 — none after repair

The independent review identified and the candidate repaired these P1 defects:

1. A remembered “Bluesky” fallback could override later provider choice while the UI showed another provider. The fallback is now made into the visible persisted selection and normal selection clears the remembered fallback.
2. Local-feed enablement could race the personalization event and undo the toggle. The enablement key is written before the event-emitting profile save.
3. “Less like this” could be selected but appear as a positive Why-this-post reason. Avoided posts now have explicit negative wording and are not selected as exploration slots.
4. Provider switching could race old persisted query writes. Cache invalidation now closes the old generation before the new persister can write.
5. More/Less could send third-party interaction events and showed success before durable local save. More/Less is local-only and the toast follows the save result.

Additional repaired defects include the wrong sign for the Balanced harassment-risk term, missing explicit preference influence in the ranker, disconnected discovery levels, synthetic Why-this-post explanations, stale provider routing, and credential-like values accepted in exportable service fields.

### P2 — six remaining tensions or environment limits

- **P2-01 — Marketplace breadth:** the provider registry and selection path are real and tested, but the current live environment exposed only the built-in Bluesky AppView. No alternate external feed provider was live for a user walkthrough.
- **P2-02 — Balanced activation:** `src/lib/balanced.ts` is a deterministic, tested ranking library. It is not currently wired as a live Home selector. This is an honest capability gap, not a fake live claim; the owner must decide whether the current product scope is sufficient.
- **P2-03 — Local ranking scope:** local reranking is page-local and currently wired to the Following/local-feed path. It does not establish a universal replacement for every provider algorithm.
- **P2-04 — Provider explanation depth:** provider-supplied ranking reasons, manifests, and versions are not available from the observed feed responses. The UI now says version not declared and manifest unverified rather than fabricating precision.
- **P2-05 — Failure coverage breadth:** AppView switching has a named health probe and deterministic failure tests. Resolver and labeler failure were not induced in the live browser, and `/xrpc/_health` is a provider capability assumption rather than a universal protocol guarantee.
- **P2-06 — Quiet Metrics scope:** Quiet Metrics currently changes post action-count prominence. It does not claim to hide every metric in every screen; that scope must remain visible to the owner.

### P3 — one residual prototype limitation

- **P3-01 — Familiarity/advanced controls:** familiarity is declared in the feed preference model but is not independently scored in the local ranker. This is retained as an explicit limitation; no political or demographic proxy was added to compensate.

Meaningful identity migration remains explicitly upstream-limited/qualified in the existing identity contracts. It is not presented as a completed migration capability and is an owner judgment question rather than a hidden local failure.

## Pairwise block acceptance: Alice / Bob / Charlie

The canonical disposable A/B/C characterization was rerun from the existing observations and tests. It covers profiles, relationship state, threads, replies, quotes, author feeds, search, notifications, and direct post-block probes. The exact evidence is in `artifacts/live-block-presentation-observations.json` and `docs/LIVE_BLOCK_PRESENTATION_MATRIX.md`.

| Effect | Classification | Evidence/result |
|---|---|---|
| A's block and inverse relationship fields for A/B | `PAIRWISE` | Viewer-relative `blocking` / `blockedBy` state and AppViewLite pairwise relationship core |
| A/B profile interaction and block-list state | `PAIRWISE` | A sees the block relationship; C does not inherit A's relationship state |
| A/B direct notifications after probe writes | `PAIRWISE` | No opposite-party direct notification was observed for A or B |
| PDS acceptance of post-block B reply, mention, and follow writes | `COLLATERAL-BUT-UPSTREAM-REQUIRED` | The PDS accepted the records; this is an upstream/protocol write-vs-presentation boundary, not a local fork claim |
| C profile presentation | `PAIRWISE` | C retained independent viewer state |
| C threads/replies | `COLLATERAL-BUT-UPSTREAM-REQUIRED` | C retained public roots/replies in the pinned AppViewLite run; reference presentation may apply viewer-relative transformations |
| C quotes/search/author feed | `COLLATERAL-BUT-UPSTREAM-REQUIRED` | Public A/B quote, search, and author-feed records remained available; no local collateral suppression was observed |
| C Home/timeline | `COLLATERAL-BUT-UPSTREAM-REQUIRED` | Fixture-specific timeline behavior retained C's explicit A/B posts; anonymous timeline HTTP 500 remains unsupported |
| Stable repost hydration | `UNSUPPORTED` | The tested AppViewLite surface did not expose a stable hydrated repost item |
| Permissioned-data and some thread-v2 surfaces | `UNTESTED` | No faithful disposable fixture existed |

No avoidable local collateral behavior was found, so no block-presentation patch was applied. The PDS accepting a direct record is not misreported as client-level authorization.

## Explicit preference precedence

The repaired deterministic rule is:

1. URI-specific explicit preference, if present.
2. Explicit author preference, if present.
3. Explicit topic preference, if present.
4. Inferred topic interest, social/network signal, passive engagement, freshness, and exploration.

Explicit preference is represented as a separate trace field and contributes at weight `2.5`; `prefer` is positive and `avoid` is negative. Candidate ordering sorts by explicit tier before the remaining score. A strong explicit negative therefore materially lowers a matching candidate despite repeated-view/inferred-positive signals. The same fixture proves an explicit positive raises the matching candidate. More/Less state is local and does not enter the association interaction allowlist.

## Controlled serendipity

`explorationFloorForLevel()` maps Low, Default, and High to increasing bounded exploration floors. The deterministic composition fixture verifies that High produces more unfamiliar candidates than Default, and Default more than Low. Candidates with an explicit negative preference are excluded from exploration selection; the explicit negative remains authoritative at every discovery level. No ideological, partisan, demographic, or cultural quota participates in this path.

The live settings screen rendered the three discovery-related controls. The full effect is proven by deterministic ranking tests, not by mutating the authenticated owner account.

## Why-this-post fidelity

The previous implementation generated a synthetic display reason from incomplete fields. The current local path records the actual `LocalRankingTrace` and maps only selected candidates' recorded reasons into `PostFeedItem`. Reasons include followed account, near social graph, explicit preference, inferred interest, freshness, exploration setting, integrity adjustment, seen suppression, and the local-settings fallback only when no stronger recorded reason exists. An avoided candidate is not described as “more like this”; if it is displayed, it says it was shown despite the Less-like-this preference.

The trace does not expose confidential anti-abuse signals. Provider-supplied reasons remain unavailable and the provenance card reports that absence rather than inventing a reason. This is why provider explanation depth remains P2.

## Algorithm and provider choice

| Choice | Actual current behavior | Persistence/isolation result |
|---|---|---|
| Following | Real chronological feed path; live browser rendered posts and the provenance card identified Bluesky AppView | Local preference/reranking choice is separate from identity and PDS |
| Balanced | Real tested library/manifest in `src/lib/balanced.ts`; not a live Home selector in this candidate | No claim of live marketplace breadth is made |
| Saved/custom feed | Real provider-supplied custom Science feed rendered in the browser | Feed/provider identity is displayed; switching is reversible where providers exist |
| External feed provider | Conditional registry/selection code exists and is tested; no alternate provider was registered in the current live environment | Fixture-only/conditional capability, not live owner proof |
| AppView selection | Persisted selection, explicit endpoint-scoped service auth, pre-switch probe, visible error, and cache-generation invalidation | PDS URL is retained; DID, PDS, associations, recovery, and unrelated personalization are not rewritten in tests |

The old hidden request-time fallback was removed. A remembered fallback is surfaced as the selected provider, and “Use Bluesky and remember this choice” is explicit. Normal selection can replace it.

## Provider failure and fallback

`probeAppViewProvider()` validates an HTTPS endpoint and names the provider on network, redirect, timeout, or HTTP failure. `buildAppviewClient()` uses only the selected provider's endpoint, DID, and fragment; it does not substitute `api.bsky.app` behind the caller's back. Session switching retains the account PDS route, and old persisted query writes cannot repopulate a new provider's cache.

Deterministic tests cover unsafe endpoints, probe failure/success, visible remembered fallback, clearing fallback on replacement, PDS route retention, service-auth audience/proxy identity, and persistence-generation races. The live browser did not induce a destructive account/provider failure. Resolver and labeler failure remain owner-checklist cases and P2 coverage limits.

## Political content neutrality

**PASS.** The targeted audit searched the constitutional ranking path (`src/lib/balanced.ts`, `src/lib/experimental-attention.ts`, `src/lib/feed-sovereignty/profile.ts`, local-feed state, and personalization controls) for left/right, party, demographic, ideological, quota, and political enforcement terms. The only relevant result in the ranking-path set is an audit/metadata statement in `experimental-attention.ts` explicitly describing optional exposure diversity without compulsory ideological balancing. `constructiveness` exists as an allowlisted personalization field and test fixture, not as a mandatory ranking classifier or quota.

There is no constitutional default path enforcing left/right balance, party balance, demographic quotas, ideological quotas, a political-quality classifier, a mandatory constructiveness classifier, or political diversity floors. User-selected topic and feed choices remain outside that prohibition.

## Institutional attribution

The repair adds or preserves specific attribution where it matters:

- Services identifies the account host as **PDS** and the read service as **AppView**.
- Feed provenance identifies the actual AppView provider DID and feed owner DID when supplied.
- Provider failures name the failing AppView provider.
- PDS writes remain described as account-host behavior, not generic “platform” behavior.
- Unverified manifests and undeclared versions are labeled as such.

Resolver and labeler actor-specific failure walkthroughs were not live-run; the owner checklist keeps them explicit rather than marking them complete.

## Defaults and friction classification

| Area | Classification | Reason |
|---|---|---|
| Default Home/Following | `ACCEPTABLE` | Useful chronological default, visible and replaceable where the current feed registry permits |
| Following accessibility | `GOOD` | First-class path and local reranking control |
| Balanced accessibility | `RADLIB-TENSION` | Tested library but not currently a live selector |
| Custom feed accessibility | `GOOD` | Real saved/custom feed path rendered in the live browser |
| Alternate AppView/provider choice | `RADLIB-TENSION` | Selection code is real, but current environment has only the built-in provider |
| PDS/AppView separation | `GOOD` | Separate settings identity and session/client routing |
| Resolver selection | `ACCEPTABLE` | Distinct resolution responsibility, but no comparable live resolver marketplace was available |
| Labeler behavior | `ACCEPTABLE` | Labeler authority is separate and scoped; live failure attribution remains untested |
| Personalization | `GOOD` | Inspectable, resettable, exportable/importable, credential-free, and local for More/Less |
| Discovery | `GOOD` | Low/Default/High controls materially change deterministic composition |
| Freshness/variety/familiarity | `ACCEPTABLE` | Some controls are model fields or future/partial integrations; current scope is documented |
| Quiet Metrics | `ACCEPTABLE` | Real post-control behavior with intentionally limited surface scope |

## Portable Personalization

The deterministic round trip is `export → inspect → reset → import`. Export validation is fail-closed and rejects credential-like keys as well as credential-like values in service fields. Tests cover explicit post preferences, service-field rejection, encryption/import validation, reset separation, and round-trip restoration. No account credentials, service-auth material, recovery secrets, or private-key material are accepted into the portable export schema.

The live browser opened the personalization surfaces but did not copy or reset the authenticated owner's data. The owner checklist requests the final manual inspect/reset/import walkthrough.

## Radical-liberal red team

| Criticism | Classification | Evidence |
|---|---|---|
| “The official AppView is effectively mandatory.” | `PARTIALLY SUPPORTED` | It is the only provider visible in the current live environment, but the registry, selection, endpoint validation, and persistence path are real and tested |
| “Feed replacement is fake or inaccessible.” | `PARTIALLY SUPPORTED` | Following and custom feeds are real; Balanced is library-only and no alternate external provider was live |
| “The PDS silently controls service selection.” | `NOT SUPPORTED` | `pdsUrl` is retained separately; AppView selection uses the explicit provider and PDS client routes account-host calls |
| “A block grants broad authority over Charlie.” | `NOT SUPPORTED` for avoidable local collateral | A/B/C fixtures retain C's public profile, threads, quotes, author-feed and search records; remaining transformations are upstream/reference-policy boundaries |
| “The labeler is a central moderator.” | `PARTIALLY SUPPORTED` | Labeler authority is separate and scoped in the client/contracts, but a live multi-labeler failure/choice walkthrough remains untested |
| “Explicit preferences do not affect ranking.” | `NOT SUPPORTED` after repair | Deterministic positive/negative precedence tests and local trace prove effect |
| “Personalization cannot leave the provider.” | `NOT SUPPORTED` | Local credential-free export/import/reset path exists and is tested |
| “The operator can silently change the algorithm.” | `PARTIALLY SUPPORTED` | Local ranking is disclosed; provider versions/manifests are often undeclared, which is shown as unknown rather than falsely precise |
| “Why-this-post is decorative.” | `NOT SUPPORTED` for local ranking; `PARTIALLY SUPPORTED` for provider ranking | Local explanations come from the actual trace; provider reason data is not available |
| “Recovery resets unrelated choices.” | `NOT SUPPORTED` by state-isolation tests | Recovery/session state and personalization/provider state are stored and switched separately |
| “A configuration store is a hidden master authority.” | `NOT SUPPORTED` by current code/tests | PDS, AppView, feed, labeler, identity, association, and personalization state have separate boundaries; marketplace breadth remains a P2 question |

## Fixes implemented

- Made More/Less durable local preferences and removed their remote interaction path.
- Implemented deterministic explicit-over-inferred ranking with traceable reasons.
- Corrected explicit negative reason wording and avoided exploration mislabeling.
- Wired Low/Default/High discovery to actual candidate composition.
- Corrected the Balanced risk sign and added explicit preference override weighting.
- Added Quiet Metrics behavior to post interaction-count surfaces.
- Added selected-provider provenance and truthful unknown version/manifest/health labels.
- Removed hidden provider fallback and made remembered fallback visible and replaceable.
- Retained the PDS route across AppView changes and invalidated old provider query generations safely.
- Added provider endpoint validation/probes and named errors.
- Validated portable personalization before encryption/import and rejected credential-like service fields/values.
- Updated stale root characterization gates to test preserved contracts and the reviewed candidate rather than pre-repair source text.

## Tests and gates

| Gate | Result |
|---|---|
| Nested social Jest | `69` suites passed; `810` tests passed; `28` todo; `21` snapshots passed |
| Nested web typecheck | `pnpm typecheck:web` passed |
| Production web build | `EXPO_PUBLIC_ENV=production pnpm build-web` exited `0`; webpack emitted existing size/module warnings but completed `post-web-build.js` |
| Root contract validation | `python3 scripts/validate_contract.py` passed: `95 files, 29 blocking rows, 6 feed cases` |
| Root pytest | `81 passed, 2 skipped` |
| Upstream checkout gate | `python3 scripts/check_upstream.py --fast` passed with all current trees `CURRENT` |
| Diff checks | Nested and parent `git diff --check` clean at final review |

The root tests changed in this review are `tests/test_attention_constitution.py`, `tests/test_feed_prototype_audit.py`, `tests/test_social_app_wiring.py`, and the current-candidate pointer in `artifacts/upstream-baseline.json`. The constitutional principles and declared upstream pins were not weakened or rebased.

## Remaining owner-judgment questions

1. Is a tested but library-only Balanced profile sufficient for this acceptance, or must it be wired as a live Home choice?
2. Is conditional provider-registry support sufficient for meaningful exit when the current deployment exposes only Bluesky AppView?
3. What alternate feed/AppView/provider should the owner use for a live switching walkthrough?
4. Does the current page-local Following reranker meet the desired algorithm-marketplace breadth?
5. Is the current Quiet Metrics surface scope acceptable?
6. Should resolver and labeler providers receive the same live replacement/failure walkthrough as AppView?
7. Are provider-supplied undeclared versions/manifests acceptable when the UI accurately says unknown/unverified?
8. Does the owner accept upstream-limited identity migration and the documented unsupported capabilities?
9. Does the owner accept the current defaults and friction classification?

## Handoff

- Owner checklist: `docs/OWNER_ACCEPTANCE_CHECKLIST.md`
- Existing contract/constitutional documents remain authoritative; this report records actual candidate behavior and its limits.
- Final automated state: `RADLIB_CODEX_ACCEPTANCE_READY_FOR_OWNER`; owner state remains `OWNER_ACCEPTANCE_PENDING`.
