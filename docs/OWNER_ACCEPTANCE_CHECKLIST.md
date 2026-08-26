# Owner Acceptance Checklist

**State:** `OWNER_ACCEPTANCE_PENDING` — automated evidence is populated for
owner review. Owner-result fields are not completed by Codex and this remains
a checklist, not a global acceptance verdict.

## Exact local launch command

```sh
cd /var/home/tcs/Code/atproto/upstream/social-app && \
EXPO_PUBLIC_ENV=development \
EXPO_PUBLIC_APPVIEW_SERVICE_DID=did:plc:dw4kbjf5mn7nhenabiqpkyh3 \
EXPO_PUBLIC_APPVIEW_SERVICE_FRAGMENT=bsky_appview \
EXPO_PUBLIC_PUBLIC_APPVIEW_URL=http://127.0.0.1:2584 \
EXPO_PUBLIC_ALLOW_INSECURE_LOCAL_APPVIEW=1 \
EXPO_PUBLIC_DEFAULT_LABELER_DIDS= \
EXPO_PUBLIC_ACCOUNT_SERVICE=http://127.0.0.1:2583 \
EXPO_PUBLIC_DEFAULT_FEED_OWNER_DID=did:plc:tgdhu5j5on7rokehpgyzcben \
EXPO_PUBLIC_DEFAULT_FEED_RKEY=social-discover \
pnpm install --frozen-lockfile && pnpm web -- --port 8081
```

Start the pinned first-party PDS/AppView fixture first when doing an integrated
walkthrough; its AppView service DID must match
`EXPO_PUBLIC_APPVIEW_SERVICE_DID`. The command uses Metro port 8081; Expo
Webpack serves the browser at `http://127.0.0.1:19006/`. The old `19007` tab is
the native/Metro endpoint, not the rendered web timeline. Use another free
Metro port only when necessary. This command deliberately does not route
public reads to `api.bsky.app`.

For the real owner account `edriffles.us`, use the same command with the
account-entryway line changed to:

```sh
EXPO_PUBLIC_ACCOUNT_SERVICE=https://bsky.social
```

That real-account variant still requires a provider that indexes the remote
account. The disposable local AppView does not. For a live browser smoke test
of the real account's authenticated reads, use this explicit provider variant
(it is not the fork's first-party AppView and does not prove the neutral
Discover provider):

```sh
cd /var/home/tcs/Code/atproto/upstream/social-app && \
EXPO_PUBLIC_ENV=development \
EXPO_PUBLIC_APPVIEW_SERVICE_DID=did:web:api.bsky.app \
EXPO_PUBLIC_APPVIEW_SERVICE_FRAGMENT=bsky_appview \
EXPO_PUBLIC_APPVIEW_DISPLAY_NAME='Public Bluesky AppView (explicit read provider)' \
EXPO_PUBLIC_PUBLIC_APPVIEW_URL=https://api.bsky.app \
EXPO_PUBLIC_DEFAULT_LABELER_DIDS= \
EXPO_PUBLIC_ACCOUNT_SERVICE=https://bsky.social \
pnpm web -- --port 8081
```

This explicit provider resolves `edriffles.us` through the declared remote PDS
and can serve the account's standard authenticated reads. It must remain
visibly attributed as `Public Bluesky AppView`; it is not an implicit fallback
and is not an owner acceptance result for the fork's own AppView.

The localhost PDS is a disposable `.test`/`.example` fixture and is not the
owner's PDS. The login flow resolves the handle, follows its DID document to
the declared PDS, and keeps the selected AppView as a separate read service.
The current local AppView remains a seeded fixture and must not be described as
the owner's live timeline until it has indexed that account.

The two `EXPO_PUBLIC_DEFAULT_FEED_*` values above identify the current seeded
local fixture only. `Discover` is registered by
`packages/dev-env/src/mock/index.ts` as a neutral second feed-generator record;
`Following` remains the chronological path. If the dev environment is
recreated and generates a new Alice DID, replace the owner DID with that
fixture's feed owner; do not reuse this DID as a production identity.

For the first-party PDS policy/build check, use the PDS-declared pnpm 11.11.0
toolchain (the focused policy/migration tests and full TypeScript build passed;
this does not provision a live database). On the validation host the pinned
binary was invoked with:

```sh
cd /var/home/tcs/Code/atproto/upstream/atproto-pds && \
PATH=/tmp/codex-pnpm-11.11.0/node_modules/.bin:$PATH \
  pnpm --filter @atproto/pds build
```

For the live PDS/CAR/provider migration walkthrough:

```sh
cd /var/home/tcs/Code/atproto && \
node scripts/radlib_live_provider_walkthrough.mjs
```

Results below distinguish verified live behavior, deterministic/fixture evidence, and capabilities that still need a live owner walkthrough.

| # | ACTION | EXPECTED BEHAVIOR | PRINCIPLE | AUTOMATED STATE (PASS / FAIL / NEEDS CHANGE; OWNER CONFIRMATION PENDING) | OWNER NOTES |
|---:|---|---|---|---|---|
| 1 | Launch the client with the command above | The ordinary social client opens without architecture ceremony or an invented identity state | Usable defaults; individual sovereignty | PASS | Rendered web app verified at `http://127.0.0.1:19006/`; `19007` is the native/Metro endpoint. Real posts rendered with no React refresh error overlay. |
| 2 | Open Home | The active feed, provider, algorithm/version, and provenance state are identifiable; an enabled local curation overlay is identified separately from the provider | Attention transparency | PASS (local build) | The source-bound production web artifact is deployed at `https://social.edriffles.us`; `radlib.edriffles.us` remains the configured protocol/OAuth authority. |
| 3 | Select Following | A chronological/following view is available and remains first-class | Attention sovereignty | PASS | The local fixture has a pinned `Following` timeline beside neutral `Discover`; Following reports `Following / chronological` and `Chronological access`, while the custom feed has separate provider provenance. |
| 4 | Select Balanced | If Balanced is presented as a product choice, it is a real selectable ranking mode with a distinct identity; otherwise its current library-only status is plainly disclosed | Algorithm marketplace; honest capability | PASS | Balanced is a real persisted opt-in local algorithm for the Following feed only. The provenance card now says `Balanced local algorithm (Following only)`, and the card links directly to ranking/provider replacement controls. No mandatory “Radical Liberal Algorithm” is presented. Owner may still decide whether a broader marketplace is desired. |
| 5 | Select a saved/custom feed | The selected feed and its owner/provider are visible and switching is reversible | Polycentric services | PASS | The local fixture registers and renders neutral `Discover` as a real feed-generator record beside Following. The historical `Kpop GGs` and `Headphones` feeds are not part of the current local default/pinned set. |
| 6 | Inspect the provenance card | Provider DID, feed owner when known, version/manifest status, objective, and privacy scope are not fabricated | Institutional anti-reification; attention transparency | PASS | Live card identifies `Public Bluesky AppView (explicit read provider)`, DID `did:web:api.bsky.app`, the `for-you` feed owner/URI, `Manifest: unverified`, the actual local-curation objective, and device-local privacy scope. The disposable local fixture still identifies its own fixture AppView and feed owner when that launch command is used. |
| 7 | Open Why this post? on a locally ranked post | The explanation names only ranking signals present in the actual trace, including a local curation branch only when it contributed | Attention transparency | PASS | `rankLocallyWithTrace` and explanation-fidelity tests pass; local reasons consume the selected trace and curation reasons are attached only to scored candidates. |
| 8 | Open Why this post? on a provider-ranked post | Missing provider trace data is disclosed; the client does not invent a local reason | Truthful attribution | PASS | Candidate reason metadata is validated before rendering. A public `label`, `reason`, or `explanation` is attributed as `From feed provider`; scores and unknown fields are omitted, and no provider reason means no fabricated post-level “Why this post?” claim. Provider-ranked live data without a reason remains an owner walkthrough. |
| 9 | Choose the ↑ segment in the grouped More/Less control below a post, or choose More like this from the menu | The local explicit positive preference is persisted and visibly acknowledged; the arrow is an attention control, not a public vote record | Explicit preferences outrank inference | PASS | Live browser showed the stable accessible `Show more like this` toggle in the outlined pair; persistence and ranking-effect tests pass. |
| 10 | Choose the ↓ segment in the grouped More/Less control below a post, or choose Less like this from the menu | The local explicit negative preference is persisted, reversible by choosing ↓ again, and is not a block, mute, follow, or remote interaction | Freedom of association; explicit control | PASS | Live browser showed the stable accessible `Show less like this` toggle in the outlined pair; toggle-off and persistence tests pass. |
| 11 | Compare association state before and after More/Less | Follows, blocks, mutes, and other durable relationship records are unchanged | Separation of attention and association | PASS | Local preference and interaction allowlist tests establish state separation. |
| 12 | Run the explicit-negative preference fixture | A strong explicit negative materially lowers a candidate despite passive/inferred positive signals | Explicit preferences outrank passive inference | PASS | Deterministic URI/author/topic precedence and negative-ranking tests pass. |
| 13 | Run the explicit-positive preference fixture | A strong explicit positive materially raises a matching candidate under the documented rule | Explicit preferences outrank passive inference | PASS | Deterministic positive-ranking test passes under explicit tier weight `2.5`. |
| 14 | Set discovery/exploration to Low | The exploratory/unfamiliar composition decreases, while explicit Less constraints still apply | Controlled serendipity | PASS | Low/default/high candidate-composition tests pass and avoided candidates are excluded from exploration. |
| 15 | Set discovery/exploration to Default | The default exploration level is bounded and understandable | Limited/reversible defaults | PASS | Default is an explicit setting level and is covered by deterministic composition tests. |
| 16 | Set discovery/exploration to High | Exploratory composition increases without ideological balancing or quota behavior | Controlled serendipity; political neutrality | PASS | High increases exploration in fixtures; targeted neutrality audit found no constitutional quota. |
| 17 | Combine High discovery with Less Topic X | Exploration does not override an explicit negative preference | Explicit authority; controlled serendipity | PASS | Explicit avoids are excluded from exploration selection and remain negative in ranking traces. |
| 18 | In Feed customization & data, adjust the six attention controls, switch chronological Following/local reranking and Following/Balanced, then inspect local curation controls | Each value is persisted locally and affects the matching ranking path; chronological Following remains available; curation reply inclusion, author cap, branch weights, custom terms, and custom authors change only local attention behavior and create no relationship/provider writes | Attention sovereignty; political neutrality; explicit user control; freedom of association | PASS | Live settings rendered 10% stepper controls for discovery, familiarity, freshness, variety, conversation activity, and exploration; real Following/Balanced radio controls; local curation reply/author/branch/exclusion controls. Deterministic ranking and curation tests pass. |
| 19 | Open Feed customization & data and toggle Hide public post metrics | Public likes, reposts, and reply counts are hidden by default; the setting restores them only when the user explicitly chooses to show them, without changing records or ranking authority | Attention sovereignty; privacy | PASS | Default is now hidden for logged-in and logged-out post views; old unconfigured local state migrates to hidden; the settings toggle remains reversible. |
| 20 | Compare concentration/author-variety fixture | Structural diversity controls bound concentration without political or demographic outcome quotas | Structural diversity; political neutrality | PASS | Balanced/diversity fixtures pass; no ideological or demographic output quota is enforced. |
| 21 | Follow a user, then unfollow | Only deliberate user actions create and reverse the relationship | Freedom of association | PASS | Association fixtures and the ordinary profile mutation path cover deliberate follow/unfollow writes. Codex did not mutate the owner account; an owner may repeat this harmless reversible check. |
| 22 | Run Alice blocks Bob | Alice/Bob direct interaction is severed or bounded according to the supported protocol surfaces | Pairwise freedom of nonassociation | PASS | Canonical A/B/C fixture and generic client/PDS relationship tests pass; the result is not coupled to a retired read provider. |
| 23 | View Bob as Charlie | Alice's block does not silently become Charlie's universal authority | Third-party independence | PASS | Charlie retained independent profile/viewer state in the canonical fixture. |
| 24 | As Charlie, inspect threads and replies containing Alice/Bob | Public records remain available where the upstream service permits them; provider tombstones caused by Alice/Bob are automatically hydrated so Charlie sees the parent author and text; any upstream-required collateral is identified | Pairwise nonassociation | PASS | Live thread check showed the parent post and reply text with no `Post blocked` tombstone; a viewer-authored direct block remains hard, while list-only and incoming block state is read-through for public context and still constrains interaction. |
| 25 | As Charlie, inspect quotes, author feeds, search, and Home | No avoidable local fork behavior suppresses Charlie's independent view; blocked quote cards are automatically hydrated when the block is between other actors | Third-party independence | PASS | Live `19006` route shows `1 quote`, renders `writerofdragons.bsky.social`, and shows the Edriffles target text automatically with no `Post blocked`/`No quotes yet`. Public fallback now rechecks each recovered author through authenticated relationship state, so incoming/list-only records read through while a viewer-authored direct block remains hidden. |
| 26 | Unblock and mute/unmute Bob | Each action is distinct, reversible, and accurately labeled | Freedom of association | PASS | Direct unblock and mute/unmute remain separate ordinary relationship/attention mutations with regression coverage. Codex did not mutate the owner account; an owner may repeat this reversible check. |
| 27 | Open Services settings | PDS, AppView, feed provider, labeler, and resolver are shown as distinct actors when known | Polycentric services | PASS (deployed) | The source-bound artifact is live at `https://social.edriffles.us/settings/services`; the Worker route and PDS public-host configuration are deployed. The UI identifies the account PDS separately from `Public Bluesky AppView (explicit read provider)` and does not fabricate separate labeler/resolver providers. |
| 28 | Inspect account host and AppView | PDS writes/identity and AppView reads are visibly separated | Institutional anti-reification | PASS | Live settings and session/client tests show separate PDS route and AppView provider. |
| 29 | Register/select an alternate AppView or feed provider where available | Selection is real, persisted, and uses the selected endpoint rather than a hidden default | Meaningful exit; algorithm marketplace | PASS | Services now exposes an explicit `Add a read provider` AppView form. HTTPS, DID, health, persistence, selection, and “Use it now” are real; selecting it does not replace the PDS or identity. A populated authenticated alternate remains an owner walkthrough. |
| 30 | Switch back to the prior provider | Switching back is possible and does not rewrite identity or relationship records | Reversible defaults | PASS | Provider selection and switch-back are persisted and covered by the provider isolation tests; no PDS, DID, relationship, recovery, or personalization state is rewritten. An owner may repeat the live switch. |
| 31 | Compare state across provider switching | DID, PDS, follows, blocks, recovery state, and unrelated personalization remain stable | Service separation | PASS | PDS-route retention, session isolation, and provider-cache tests pass. |
| 32 | Simulate a feed-provider failure | The failing provider is named; a materially different provider is not silently impersonated | Explicit fallback | PASS | The filtered-provider fixture returns explicit 503 `ProviderUnavailable`; the client names the selected provider and does not substitute a materially different feed. An owner-selected live outage can be repeated without changing the automated result. |
| 33 | Simulate an AppView failure | Unaffected PDS functionality remains available where practical and the failure names the AppView | Polycentric services; explicit fallback | PASS | Named probe errors, explicit fallback, PDS separation, and cache-generation tests pass. The live configured read service is now named `Public Bluesky AppView (explicit read provider)`; no live failure was induced on the owner's account. |
| 34 | Simulate resolver and labeler failures | The resolver/labeler actor and unsupported scope are named; no generic “platform” authority is invented | Institutional anti-reification | PASS | `ServiceBoundaryError` and injected-503 fixtures attribute resolver/labeler-directory failure to the named service and do not echo arbitrary upstream text. Authenticated live injection is optional owner verification, not an untested implementation path. |
| 35 | Exercise remembered fallback | Any remembered fallback is also visible as the active choice and can be replaced or cancelled | Explicit delegated authority | PASS | Remembered fallback is persisted as visible selection and cleared by normal replacement; tests pass. |
| 36 | Open Identity settings | DID, handle, PDS, and verification state are not conflated | Individual sovereignty | PASS | Identity settings now performs a read-only DID-document PDS resolution and separately displays DID, handle, stored PDS, resolver result, selected AppView, migration, and recovery capability. A live owner walkthrough remains optional. |
| 37 | Inspect active sessions | Session authority, expiry, and revocation are understandable | Explicit delegated authority | PASS | Identity & recovery now shows the current session, local access-credential expiry, authority PDS, and explicit local sign-out controls. It does not claim server-wide session inventory or revocation, and it never displays a credential. |
| 38 | Open recovery/lockdown | Recovery capabilities and unsupported migration/identity-update boundaries are described honestly | Meaningful exit; recovery sovereignty | PASS | Identity & recovery now displays live DID/PDS resolution plus explicit migration, recovery, and lockdown capability states. Unsupported server-wide recovery/lockdown and migration claims are stated as unavailable rather than implied. |
| 39 | Inspect personalization | Learned, explicit, ephemeral, service state, attention weights, explicit interests/authors, inferred-interest opt-out, filter packs, and the opt-in curation profile are inspectable with clear scope | Portable personalization | PASS | Live Personalization settings rendered the full attention/customization surface plus reset/export/import controls; ranking policy and curation state remain local explicit preference state. |
| 40 | Export personalization and inspect the JSON | Format/version/provenance and any chosen curation weights/exclusions are present, while credentials or recovery material are absent | Privacy/data minimization | PASS | Deterministic export validation includes the supported curation state and secret exclusion. The owner export was not copied from the live account by Codex; the local export action remains available for owner inspection. |
| 41 | Search the export/schema for secret-bearing fields and values | No passwords, tokens, service-auth material, recovery secrets, or private keys are exported | Credential exclusion | PASS | Schema/value rejection tests and root artifact secret audit pass. |
| 42 | Reset personalization | Reset clears the intended local state without deleting identity, follows, blocks, or recovery state | Cross-domain isolation | PASS | Reset isolation tests prove only this client’s local personalization is cleared. Codex did not reset the owner’s live state; the destructive live action remains owner-controlled. |
| 43 | Import the saved export | Explicit preferences and supported settings round-trip; malformed or foreign data fails closed | Portability; fail-closed validation | PASS | Round-trip and malformed/foreign-input fail-closed tests pass. Codex did not import into the owner account; the owner controls that live mutation. |
| 44 | Search constitutional ranking code/configuration and inspect the curation profile | No mandatory left/right, party, ideological, demographic, political-quality, or constructiveness quota enforces outcomes; ideological terms exist only in the explicitly selected local profile | Political content neutrality | PASS | Targeted static audit and root neutrality tests pass; `constructiveness` is schema-only, not ranking enforcement. The curation terms are opt-in additive/exclusion configuration, not default constitutional ranking. |
| 45 | Review defaults and friction | Important controls are discoverably replaceable without putting every advanced control on Home | Limited/reversible defaults | PASS | Following remains the chronological fallback; provenance details now provide direct `Change ranking` and `Change provider` actions, while advanced personalization remains in its labeled settings screen. No advanced control is required on Home. |
| 46 | Attempt the red-team criticism | The owner can distinguish actual centralized authority from documented or upstream-limited capability, with evidence for each claim | Radical-liberal allocation of authority | PASS | The red-team matrix is documented with exact code, fixture, live, and upstream evidence. |
| 47 | Inspect the first-party PDS policy manifest and build the PDS | `app.bsky.graph.listblock` CREATE/UPDATE is rejected only when the governed PDS policy is explicitly enabled; raw records remain interoperable, but listblock data is inert in all effective relationship/block views; direct blocks and deletes remain available | Polycentric services; interoperability | PASS | Official PDS base is pinned at `760fb12a080c87cdfd0dae42ae833bad8bc20886`; policy/build and the final 10-file/229-test inert-listblock regression pass. Deployment activation remains an explicit owner/infrastructure decision. |
| 48 | From a custom client, try listblock CREATE/UPDATE, `applyWrites`, DELETE, direct block, CAR import, and listblock-specific reads | Governed CREATE/UPDATE are rejected, DELETE/direct block remain available, CAR import accepts raw historical records, listblock reads/relationship RPCs return empty/no-block answers, and list mute remains the only delegated attention path | Meaningful exit; explicit delegated authority | PASS | The deterministic PDS suite proves the complete data-plane result, including raw `getRecord` readability, empty listblock subscription/listblock RPCs, no relationship/block-existence fields, public recovery surfaces, direct-block regression, and list-mute filtering. Exact custom-client/live CAR repetition remains owner-controlled. |
| 49 | Inspect a legacy-import migration receipt and retry after mute/delete failure | Receipt contains counts and hashed source identifiers only; mute-before-delete ordering is preserved and retries do not create extra direct blocks | Privacy; freedom of association | PASS | Live receipt ended `clean` with one discovered/one converted/one deleted/zero remaining; deterministic retry tests still pass and no direct-block delta is introduced. |
| 50 | Review the service topology and confirm the retired provider is not the account host | Identity, repository writes, sync, and import belong to the first-party PDS; retired read providers cannot silently impersonate the PDS | Polycentric services; institutional anti-reification | PASS | First-party PDS/CAR/provider walkthrough passed. AppViewLite is retired and outside the tracked/configured graph. The live public site explicitly labels `api.bsky.app` as a read provider; no first-party AppView or neutral Discover is claimed merely because the public provider is selected. |

### Permissioned accounts and communities

| # | ACTION | EXPECTED BEHAVIOR | PRINCIPLE | AUTOMATED STATE (PASS / FAIL / NEEDS CHANGE; OWNER CONFIRMATION PENDING) | OWNER NOTES |
|---:|---|---|---|---|---|
| 51 | Enable the four permissioned-data flags on a disposable PDS and open Privacy & Security | The PDS creates a separate private store; the client reports the feature state without claiming that ordinary public composer writes are private | Privacy boundary; honest capability | PASS | The private store/policy tests pass. Privacy & Security now explicitly reports when the permissioned account space is available on the selected PDS and continues to state that ordinary public composer posts are not silently private. |
| 52 | Enable Protected account, then inspect the public profile shell and existing public posts | DID, handle, profile shell, and old public posts remain public; protected mode does not retroactively privatize already-published data | Identity portability; historical-content rule | PASS | Store semantics pass, the public profile/posts remain on the ordinary public path, and the owner’s own profile now shows a `Protected account` marker when the PDS reports that state. |
| 53 | Request, approve, deny, cancel, remove, and re-request protected access as two disposable accounts | Follow requests are separate from public follows; current approval is required for private-space reads | Voluntary association; explicit delegated authority | PASS | `/settings/protected-access` now exposes request/cancel and owner approve/deny/remove controls through the directional `us.edriffles.radlib.private.getFollowState` API. PDS tests cover requester/target visibility and the full state-transition boundary; no public follow record is created. |
| 54 | Select “Save as a private text post” in the composer on a protected account, then attempt public `createRecord`, `putRecord`, `applyWrites`, and CAR import | The private post is sent only through `us.edriffles.radlib.private.putRecord`; it never becomes `app.bsky.feed.post`; public repository/firehose/CAR paths reject private writes | Privacy/data minimization; interoperability | PASS | The intentionally text-only private composer uses `us.edriffles.radlib.private.putRecord`; public writes and CAR import reject the private namespace. Media/private-viewer UI is outside this text-only capability and remains explicitly described rather than silently implied. |
| 55 | Retrieve the protected record and private blob as owner, approved follower, non-follower, and revoked follower | Only current authorized viewers receive body/bytes; unauthorized responses do not reveal CID, body, or blob metadata; revoked access fails closed | Viewer-aware authorization; revocation | PASS | `/settings/private-spaces` now provides owner-authorized record/blob lookup. Store and XRPC tests cover owner, approved, non-follower, and revoked reads, fail-closed metadata/body access, and private blob bytes. This does not claim a private AppView or private media composer. |
| 56 | Direct-block an approved follower, then retry private record/blob retrieval | The block overrides stale approval immediately at the PDS private read boundary | Individual hard boundary | PASS | PDS private record/blob handlers recheck current direct blocks at read time and the private-store/API tests cover stale-approval revocation. No live owner-account block was created by Codex. |
| 57 | Create public, restricted, invite-only, and private communities | Visibility and discovery rules are explicit; private/invite-only metadata is not returned to non-members | Polycentric community authority; privacy | PASS | `/settings/private-spaces` now exposes public, restricted, invite-only, and private community creation plus join/leave controls. Store tests cover visibility ACLs and invite-only metadata isolation; the surface is explicitly PDS-local and does not claim a public community directory. |
| 58 | Redeem a one-use invite concurrently, then revoke it and try again | At most the configured number of members are admitted; revoked/expired secrets do not work; raw secrets are not stored | Security; explicit delegated authority | PASS | Atomic conditional redemption, hash-only storage, expiration, and revocation are covered by private-store tests. Owner may repeat against a disposable PDS. |
| 59 | Ban, unban, leave, and re-request community membership | Bans and leave state immediately stop private reads/writes; unban does not silently restore membership | Community-local governance; revocation | PASS | Local store tests cover ban read revocation and unban-to-removed semantics; owner UI exercise remains pending. |
| 60 | Inspect the private database, public CAR/export, public sync, Relay/AppView, logs, and caches after private writes | Private bodies/blobs/CIDs are absent from public data paths and sensitive values are not logged or globally cached | Hard privacy boundary | NEEDS CHANGE | Local PDS/CAR/sequencer and private-response checks pass, but the current controlled AppView target is unavailable and the external AppView probe returned HTTP 403 (`INCONCLUSIVE_APPVIEW_403`). The prior TestNetwork/AppView claim is historical evidence and is not a current privacy pass. Do not treat this item as complete until a controlled Relay/AppView scan receipt is available. |
| 61 | Open login, Home, Settings, Notifications, Messages, and Account > Birthday after rebuilding the client; search the runtime for age-assurance UI | No age-assurance provider, redirect, region/device gate, no-access screen, feed banner, chat restriction, or age-derived moderation override appears; ordinary birthdate/account metadata still works. Standard ATProto age-assurance protocol definitions remain only for interoperability and are not invoked by this client. | Usable defaults; individual sovereignty; interoperability | PASS | Client feature directories/runtime wiring and the web IPCC age-geolocation surface were removed; `tests/test_client_age_assurance_removed.py` passed 3/3, full client Jest passed 85 suites/901 tests, web/iOS typechecks passed, and the production export completed. Fresh browser owner confirmation remains pending. |
| 62 | Enter `edriffles.us` on the sign-in screen with the real-account launch configuration | The fixture PDS is not used for the owner handle; the handle resolves to `did:plc:3ijrhre2q5e4tt2f4ph2sneo`, the DID-declared PDS is `https://pds.edriffles.us`, and the password is sent only after normal hosting-provider resolution/confirmation. | Identity sovereignty; PDS/service separation; privacy | PASS (handoff; credential pending) | The deployed flow resolves the owner handle through the user-facing `social.edriffles.us` account entryway, confirms `pds.edriffles.us`, and reaches the real PDS password screen with the HTTPS Social client. Browser password entry remains owner-controlled; no production credential was entered by Codex. |
| 63 | Open a post directly or open its quotes/likes view and press Like | The heart and local count change immediately, a pending state is truthful while the PDS write is in flight, and the final state reconciles with the PDS result | Attention responsiveness; service separation | PASS | Direct `['post', uri]` cache coverage was added and tested. Durable writes still use the account PDS; no local fake like record is treated as confirmed. |
| 64 | Inspect the browser title, logged-out navigation label, feed provenance, and Feed customization & data settings | The public product is branded `Social`; the UI says `local curation`; it does not present the constitutional project name as a political slogan | Political neutrality; institutional anti-reification | PASS | `EXPO_PUBLIC_BRAND_NAME` defaults to `Social`; visible copy is neutralized. Internal compatibility IDs remain intentionally unchanged. |
| 65 | Build the web artifact with the command in `docs/SOCIAL_EDRIFFLES_DEPLOYMENT.md` | The artifact is a static SPA whose title/metadata use `Social`, whose user-facing origin is `https://social.edriffles.us`, whose deep routes load root-relative assets, and whose protocol providers remain separately configured | Polycentric services; meaningful exit | PASS | The production Webpack export includes the neutral metadata, direct-route asset fix, accurate public-provider label, CSP allowances, complete Space URI validation, callback recovery, and Radlib OAuth scope enforcement. The deployed artifact is bound into the current Social user-facing cutover receipt; browser password entry remains owner-controlled. |
| 66 | Resolve `social.edriffles.us` and open it over HTTPS after DNS/hosting setup | DNS points to the selected static host, TLS is valid, SPA fallback works on a direct nested-route visit, and login redirects are registered for this exact origin | Deployment honesty; identity/provider separation | PASS (deployment; credential pending) | `social.edriffles.us` resolves over HTTPS. The Worker route, Pages upload, PDS public-host configuration, public header/metadata probes, and Radlib web compatibility redirect pass. The owner-handle browser handoff reaches the PDS password screen; entering the owner password remains owner-controlled. |
| 67 | Enable a protected account, add private text posts, and open `Private feed` as the owner, an approved viewer, and a revoked/non-member viewer | The feed is returned by the hosting PDS only; the provider DID is visible; each request re-checks authorization; revoked/non-member viewers receive no private body or metadata; public AppView, Relay, and CAR remain uninvolved | Viewer-authorized attention; service separation; privacy | PASS | `us.edriffles.radlib.private.getFeed` is a PDS-local, ACL-checked feed of `us.edriffles.radlib.private.post` records. The client exposes `/private-feed`, labels the PDS provider, and keeps the query root out of persisted React Query state. API/store tests cover the boundary; owner live walkthrough remains pending. |
| 68 | Create a private-sync grant for one target PDS/actor, pull directly, retry with the wrong target, revoke it, and pull again | The capability is hash-stored, collection-scoped, expires within 30 days, only the named PDS/actor can use it, revocation is enforced at the source, and no public Relay/CAR/AppView event is created | Explicit delegated authority; meaningful exit; privacy | PASS | `us.edriffles.radlib.private.createSyncGrant`, `syncPull`, and `revokeSyncGrant` implement direct PDS-to-PDS capability pulls. The source checks target binding, expiry, collection, and revocation on every pull; no persistent public-repository replica is created. Disposable tests start separate source/target PDS identities, cover scope, wrong target, expiry bounds, revocation, private-feed hydration, and public CAR exclusion. |

## Historical live site verification snapshot — 2026-08-19

The live authenticated walkthrough was performed against
`https://social.edriffles.us` after Cloudflare Pages deployment
`6b00d319-8b1f-4410-86e0-b01d8fa5b179`:

- `Settings > Services` showed the account PDS
  `https://yellowfoot.us-west.host.bsky.network/` and separately showed
  `Public Bluesky AppView (explicit read provider)` with DID
  `did:web:api.bsky.app` and endpoint `https://api.bsky.app`.
- Home showed `For You`, the selected provider, and the local overlay as
  separate provenance fields. The live feed owner was
  `did:plc:3guzzweuqraryl3rdkimjamk`, with feed URI ending in
  `/app.bsky.feed.generator/for-you`.
- The live provenance card stated `Manifest: unverified`, named the actual
  objective, and stated that custom filter/curation state remains on-device;
  no first-party AppView or neutral Discover deployment was inferred from
  this public-provider walkthrough.
- The cache-busting query was used only to force the browser to fetch the
  newly deployed static bundle; it did not change account, social-graph, or
  personalization state.

This is automated evidence for owner review. It does not fill owner-result
fields, perform destructive reset/import actions, or change the required
`OWNER_ACCEPTANCE_PENDING` state.

## Historical latest live verification snapshot — 2026-08-19

The corrected 2026-08-19 bundle was Cloudflare Pages deployment
`7d6c7dcb-17fd-4932-8f1b-e5dc429d22f8`, with the custom-host alias
`https://social.edriffles.us` and deployment stage `success`.

- The browser loaded `main.d563bed3.js` from a cache-busted custom-host URL.
- `/settings/protected-access` has the visible title `Protected access`; its
  browser document title is no longer an opaque localization ID.
- `/settings/private-spaces` has the visible title `Private spaces &
  communities`; its browser document title is no longer an opaque localization
  ID.
- `/settings/privacy-and-security` visibly lists both new settings destinations
  with their real labels.
- `/settings/identity-sovereignty` still distinguishes the DID, account PDS,
  AppView, session authority, and honest unavailable recovery/migration state.
- `/settings/personalization` remains account/device-local and exposes generic
  user-added terms rather than owner-specific built-in topic weights.

This is automated evidence only. It does not fill owner-result fields or
change `OWNER_ACCEPTANCE_PENDING`.

The overall state remains `OWNER_ACCEPTANCE_PENDING` because this assessment records several explicitly unexecuted live owner walkthroughs and does not constitute a global acceptance verdict.
