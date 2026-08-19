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
| 2 | Open Home | The active feed, provider, algorithm/version, and provenance state are identifiable; an enabled local curation overlay is identified separately from the provider | Attention transparency | PASS | Live `https://social.edriffles.us/?cachebust=af026399` rendered `For You` with `Algorithm: Filtered For You + local curation (version content-filter/1 + local-curation/1)`, separate `AppView: Public Bluesky AppView (explicit read provider)`, provider DID `did:web:api.bsky.app`, feed owner DID/URI, objective, and device-local privacy scope. The local fixture remains separately documented below. |
| 3 | Select Following | A chronological/following view is available and remains first-class | Attention sovereignty | PASS | The local fixture has a pinned `Following` timeline beside neutral `Discover`; Following reports `Following / chronological` and `Chronological access`, while the custom feed has separate provider provenance. |
| 4 | Select Balanced | If Balanced is presented as a product choice, it is a real selectable ranking mode with a distinct identity; otherwise its current library-only status is plainly disclosed | Algorithm marketplace; honest capability | NEEDS CHANGE | Balanced toggled false → true in the rendered browser, enabled local ranking atomically, showed `Algorithm: Balanced local algorithm (version org.radical-liberal.balanced/1)`, and restored the prior off state; owner judgment is still required on whether page-local ranking is sufficient marketplace breadth. |
| 5 | Select a saved/custom feed | The selected feed and its owner/provider are visible and switching is reversible | Polycentric services | PASS | The local fixture registers and renders neutral `Discover` as a real feed-generator record beside Following. The historical `Kpop GGs` and `Headphones` feeds are not part of the current local default/pinned set. |
| 6 | Inspect the provenance card | Provider DID, feed owner when known, version/manifest status, objective, and privacy scope are not fabricated | Institutional anti-reification; attention transparency | PASS | Live card identifies `Public Bluesky AppView (explicit read provider)`, DID `did:web:api.bsky.app`, the `for-you` feed owner/URI, `Manifest: unverified`, the actual local-curation objective, and device-local privacy scope. The disposable local fixture still identifies its own fixture AppView and feed owner when that launch command is used. |
| 7 | Open Why this post? on a locally ranked post | The explanation names only ranking signals present in the actual trace, including a local curation branch only when it contributed | Attention transparency | PASS | `rankLocallyWithTrace` and explanation-fidelity tests pass; local reasons consume the selected trace and curation reasons are attached only to scored candidates. |
| 8 | Open Why this post? on a provider-ranked post | Missing provider trace data is disclosed; the client does not invent a local reason | Truthful attribution | NEEDS CHANGE | Provider-supplied reason/manifest data was unavailable; the limitation is disclosed, but this live owner walkthrough was not completed. |
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
| 21 | Follow a user, then unfollow | Only deliberate user actions create and reverse the relationship | Freedom of association | NEEDS CHANGE | Association fixtures cover relationship semantics, but no mutation was made to the authenticated owner account. |
| 22 | Run Alice blocks Bob | Alice/Bob direct interaction is severed or bounded according to the supported protocol surfaces | Pairwise freedom of nonassociation | PASS | Canonical A/B/C fixture and generic client/PDS relationship tests pass; the result is not coupled to a retired read provider. |
| 23 | View Bob as Charlie | Alice's block does not silently become Charlie's universal authority | Third-party independence | PASS | Charlie retained independent profile/viewer state in the canonical fixture. |
| 24 | As Charlie, inspect threads and replies containing Alice/Bob | Public records remain available where the upstream service permits them; provider tombstones caused by Alice/Bob are automatically hydrated so Charlie sees the parent author and text; any upstream-required collateral is identified | Pairwise nonassociation | PASS | Live thread check showed the parent post and reply text with no `Post blocked` tombstone; a viewer-authored direct block remains hard, while list-only and incoming block state is read-through for public context and still constrains interaction. |
| 25 | As Charlie, inspect quotes, author feeds, search, and Home | No avoidable local fork behavior suppresses Charlie's independent view; blocked quote cards are automatically hydrated when the block is between other actors | Third-party independence | PASS | Live `19006` route shows `1 quote`, renders `writerofdragons.bsky.social`, and shows the Edriffles target text automatically with no `Post blocked`/`No quotes yet`. Public fallback now rechecks each recovered author through authenticated relationship state, so incoming/list-only records read through while a viewer-authored direct block remains hidden. |
| 26 | Unblock and mute/unmute Bob | Each action is distinct, reversible, and accurately labeled | Freedom of association | NEEDS CHANGE | Protocol/UI paths exist, but this live account mutation walkthrough was intentionally not performed. |
| 27 | Open Services settings | PDS, AppView, feed provider, labeler, and resolver are shown as distinct actors when known | Polycentric services | PASS | Live `https://social.edriffles.us/settings/services?cachebust=af026399` rendered the account PDS `https://yellowfoot.us-west.host.bsky.network/` separately from `Public Bluesky AppView (explicit read provider)` (`did:web:api.bsky.app · https://api.bsky.app`). The current UI does not claim separate configured labeler/resolver providers; the feed card separately identifies its feed owner/provider. |
| 28 | Inspect account host and AppView | PDS writes/identity and AppView reads are visibly separated | Institutional anti-reification | PASS | Live settings and session/client tests show separate PDS route and AppView provider. |
| 29 | Register/select an alternate AppView or feed provider where available | Selection is real, persisted, and uses the selected endpoint rather than a hidden default | Meaningful exit; algorithm marketplace | NEEDS CHANGE | Generic provider registration, validation, persistence, and probing are implemented. The retired AppViewLite instance is not an alternate-provider result; a populated authenticated alternate remains an owner walkthrough. |
| 30 | Switch back to the prior provider | Switching back is possible and does not rewrite identity or relationship records | Reversible defaults | NEEDS CHANGE | Switch-back behavior is tested with fixtures and the local provider probe is real; an authenticated alternate-provider switch-back was not performed. |
| 31 | Compare state across provider switching | DID, PDS, follows, blocks, recovery state, and unrelated personalization remain stable | Service separation | PASS | PDS-route retention, session isolation, and provider-cache tests pass. |
| 32 | Simulate a feed-provider failure | The failing provider is named; a materially different provider is not silently impersonated | Explicit fallback | NEEDS CHANGE | The standalone filtered provider live walkthrough returns explicit 503 `ProviderUnavailable` when ingestion is absent; an owner-selected feed-provider failure was not induced. |
| 33 | Simulate an AppView failure | Unaffected PDS functionality remains available where practical and the failure names the AppView | Polycentric services; explicit fallback | PASS | Named probe errors, explicit fallback, PDS separation, and cache-generation tests pass. The live configured read service is now named `Public Bluesky AppView (explicit read provider)`; no live failure was induced on the owner's account. |
| 34 | Simulate resolver and labeler failures | The resolver/labeler actor and unsupported scope are named; no generic “platform” authority is invented | Institutional anti-reification | NEEDS CHANGE | `ServiceBoundaryError` regression fixtures and an injected HTTP 503 fixture name the identity-resolver or labeler-directory AppView boundary without echoing arbitrary upstream text; authenticated live failure injection remains owner work. |
| 35 | Exercise remembered fallback | Any remembered fallback is also visible as the active choice and can be replaced or cancelled | Explicit delegated authority | PASS | Remembered fallback is persisted as visible selection and cleared by normal replacement; tests pass. |
| 36 | Open Identity settings | DID, handle, PDS, and verification state are not conflated | Individual sovereignty | NEEDS CHANGE | Identity separation is covered by code/tests, but the live owner walkthrough was not completed. |
| 37 | Inspect active sessions | Session authority, expiry, and revocation are understandable | Explicit delegated authority | NEEDS CHANGE | Session/recovery tests pass; no live session mutation or revocation walkthrough was performed. |
| 38 | Open recovery/lockdown | Recovery capabilities and unsupported migration/identity-update boundaries are described honestly | Meaningful exit; recovery sovereignty | NEEDS CHANGE | Recovery is qualified and tested, but migration remains upstream-limited and the live surface was not walked through. |
| 39 | Inspect personalization | Learned, explicit, ephemeral, service state, attention weights, explicit interests/authors, inferred-interest opt-out, filter packs, and the opt-in curation profile are inspectable with clear scope | Portable personalization | PASS | Live Personalization settings rendered the full attention/customization surface plus reset/export/import controls; ranking policy and curation state remain local explicit preference state. |
| 40 | Export personalization and inspect the JSON | Format/version/provenance and any chosen curation weights/exclusions are present, while credentials or recovery material are absent | Privacy/data minimization | NEEDS CHANGE | Deterministic export validation and curation round-trip pass, but the authenticated owner's export was not copied or inspected live. |
| 41 | Search the export/schema for secret-bearing fields and values | No passwords, tokens, service-auth material, recovery secrets, or private keys are exported | Credential exclusion | PASS | Schema/value rejection tests and root artifact secret audit pass. |
| 42 | Reset personalization | Reset clears the intended local state without deleting identity, follows, blocks, or recovery state | Cross-domain isolation | NEEDS CHANGE | Reset isolation is covered by tests; live reset was intentionally not performed on the owner account. |
| 43 | Import the saved export | Explicit preferences and supported settings round-trip; malformed or foreign data fails closed | Portability; fail-closed validation | NEEDS CHANGE | Round-trip and fail-closed tests pass; live import was not performed. |
| 44 | Search constitutional ranking code/configuration and inspect the curation profile | No mandatory left/right, party, ideological, demographic, political-quality, or constructiveness quota enforces outcomes; ideological terms exist only in the explicitly selected local profile | Political content neutrality | PASS | Targeted static audit and root neutrality tests pass; `constructiveness` is schema-only, not ranking enforcement. The curation terms are opt-in additive/exclusion configuration, not default constitutional ranking. |
| 45 | Review defaults and friction | Important controls are discoverably replaceable without putting every advanced control on Home | Limited/reversible defaults | NEEDS CHANGE | Following is the fallback Home selection when no explicit choice exists; custom feeds, personalization, and Balanced are discoverable in settings. Alternate-provider breadth remains an owner decision. |
| 46 | Attempt the red-team criticism | The owner can distinguish actual centralized authority from documented or upstream-limited capability, with evidence for each claim | Radical-liberal allocation of authority | PASS | The red-team matrix is documented with exact code, fixture, live, and upstream evidence. |
| 47 | Inspect the first-party PDS policy manifest and build the PDS | `app.bsky.graph.listblock` CREATE/UPDATE is rejected only when the governed PDS policy is explicitly enabled; raw records remain interoperable, but listblock data is inert in all effective relationship/block views; direct blocks and deletes remain available | Polycentric services; interoperability | NEEDS CHANGE | Official PDS base is pinned at `760fb12a080c87cdfd0dae42ae833bad8bc20886`; the bsky build and the final 10-file/229-test inert-listblock regression pass. Owner should confirm the deployed policy setting and manifest. |
| 48 | From a custom client, try listblock CREATE/UPDATE, `applyWrites`, DELETE, direct block, CAR import, and listblock-specific reads | Governed CREATE/UPDATE are rejected, DELETE/direct block remain available, CAR import accepts raw historical records, listblock reads/relationship RPCs return empty/no-block answers, and list mute remains the only delegated attention path | Meaningful exit; explicit delegated authority | NEEDS CHANGE | The deterministic PDS suite proves the data-plane result (raw `getRecord` readability, empty listblock subscription/listblock RPCs, no relationship/block-existence fields, public profile/feed/search/thread/quote access, direct-block regression, and list-mute filtering). The exact custom-client and live CAR walkthrough remain owner checks. |
| 49 | Inspect a legacy-import migration receipt and retry after mute/delete failure | Receipt contains counts and hashed source identifiers only; mute-before-delete ordering is preserved and retries do not create extra direct blocks | Privacy; freedom of association | PASS | Live receipt ended `clean` with one discovered/one converted/one deleted/zero remaining; deterministic retry tests still pass and no direct-block delta is introduced. |
| 50 | Review the service topology and confirm the retired provider is not the account host | Identity, repository writes, sync, and import belong to the first-party PDS; retired read providers cannot silently impersonate the PDS | Polycentric services; institutional anti-reification | NEEDS CHANGE | First-party PDS/CAR/provider walkthrough passed. AppViewLite is retired, removed from the tracked/configured graph, and preserved only as an unlaunchable local archive. The live public site uses an explicitly labelled `api.bsky.app` read provider; a separately deployed first-party AppView/neutral Discover is not yet live. |

### Permissioned accounts and communities

| # | ACTION | EXPECTED BEHAVIOR | PRINCIPLE | AUTOMATED STATE (PASS / FAIL / NEEDS CHANGE; OWNER CONFIRMATION PENDING) | OWNER NOTES |
|---:|---|---|---|---|---|
| 51 | Enable the four permissioned-data flags on a disposable PDS and open Privacy & Security | The PDS creates a separate private store; the client reports the feature state without claiming that ordinary public composer writes are private | Privacy boundary; honest capability | NEEDS CHANGE | Private store and protected-account policy are implemented; live flag-enabled client walkthrough remains pending. |
| 52 | Enable Protected account, then inspect the public profile shell and existing public posts | DID, handle, profile shell, and old public posts remain public; protected mode does not retroactively privatize already-published data | Identity portability; historical-content rule | NEEDS CHANGE | Store semantics are covered; profile marker and live profile walkthrough remain pending. |
| 53 | Request, approve, deny, cancel, remove, and re-request protected access as two disposable accounts | Follow requests are separate from public follows; current approval is required for private-space reads | Voluntary association; explicit delegated authority | NEEDS CHANGE | State transitions are tested in the private store; client follow-request UI is not complete. |
| 54 | Select “Save as a private text post” in the composer on a protected account, then attempt public `createRecord`, `putRecord`, `applyWrites`, and CAR import | The private post is sent only through `org.radlib.private.putRecord`; it never becomes `app.bsky.feed.post`; public repository/firehose/CAR paths reject private writes | Privacy/data minimization; interoperability | NEEDS CHANGE | Text-only private composer and namespace/prepare/import guards pass; private media, live multi-account read, and live CAR walkthrough remain pending. |
| 55 | Retrieve the protected record and private blob as owner, approved follower, non-follower, and revoked follower | Only current authorized viewers receive body/bytes; unauthorized responses do not reveal CID, body, or blob metadata; revoked access fails closed | Viewer-aware authorization; revocation | NEEDS CHANGE | Text-only private composer and store tests pass; private media composition, private AppView, and live multi-account retrieval remain incomplete. |
| 56 | Direct-block an approved follower, then retry private record/blob retrieval | The block overrides stale approval immediately at the PDS private read boundary | Individual hard boundary | NEEDS CHANGE | Owner-block lookup is implemented; an end-to-end live direct-block/private-read harness is still required. |
| 57 | Create public, restricted, invite-only, and private communities | Visibility and discovery rules are explicit; private/invite-only metadata is not returned to non-members | Polycentric community authority; privacy | NEEDS CHANGE | Local store and metadata ACL tests pass; community UI/directory is not complete. |
| 58 | Redeem a one-use invite concurrently, then revoke it and try again | At most the configured number of members are admitted; revoked/expired secrets do not work; raw secrets are not stored | Security; explicit delegated authority | PASS | Atomic conditional redemption, hash-only storage, expiration, and revocation are covered by private-store tests. Owner may repeat against a disposable PDS. |
| 59 | Ban, unban, leave, and re-request community membership | Bans and leave state immediately stop private reads/writes; unban does not silently restore membership | Community-local governance; revocation | PASS | Local store tests cover ban read revocation and unban-to-removed semantics; owner UI exercise remains pending. |
| 60 | Inspect the private database, public CAR/export, public sync, Relay/AppView, logs, and caches after private writes | Private bodies/blobs/CIDs are absent from public data paths and sensitive values are not logged or globally cached | Hard privacy boundary | NEEDS CHANGE | Separate storage and no-public-pipeline tests pass; multi-PDS/private-AppView/export/log audit remains incomplete. |
| 61 | Open login, Home, Settings, Notifications, Messages, and Account > Birthday after rebuilding the client; search the runtime for age-assurance UI | No age-assurance provider, redirect, region/device gate, no-access screen, feed banner, chat restriction, or age-derived moderation override appears; ordinary birthdate/account metadata still works. Standard ATProto age-assurance protocol definitions remain only for interoperability and are not invoked by this client. | Usable defaults; individual sovereignty; interoperability | PASS | Client feature directories/runtime wiring and the web IPCC age-geolocation surface were removed; `tests/test_client_age_assurance_removed.py` passed 3/3, full client Jest passed 83 suites/890 tests, web/iOS typechecks passed, and the production export completed. Fresh browser owner confirmation remains pending. |
| 62 | Enter `edriffles.us` on the sign-in screen with the real-account launch configuration | The fixture PDS is not used for the owner handle; the handle resolves to `did:plc:3ijrhre2q5e4tt2f4ph2sneo`, the DID-declared PDS is `https://yellowfoot.us-west.host.bsky.network`, and the password is sent only after normal hosting-provider resolution/confirmation. | Identity sovereignty; PDS/service separation; privacy | PASS | The local fixture PDS is `did:web:localhost` with only `.test`/`.example` domains, which caused the original failure. Login-time detection now uses the explicit account entryway rather than the selected AppView. Current web process uses `EXPO_PUBLIC_ACCOUNT_SERVICE=https://bsky.social`; owner must still perform the credentialed login. |
| 63 | Open a post directly or open its quotes/likes view and press Like | The heart and local count change immediately, a pending state is truthful while the PDS write is in flight, and the final state reconciles with the PDS result | Attention responsiveness; service separation | PASS | Direct `['post', uri]` cache coverage was added and tested. Durable writes still use the account PDS; no local fake like record is treated as confirmed. |
| 64 | Inspect the browser title, logged-out navigation label, feed provenance, and Feed customization & data settings | The public product is branded `Social`; the UI says `local curation`; it does not present the constitutional project name as a political slogan | Political neutrality; institutional anti-reification | PASS | `EXPO_PUBLIC_BRAND_NAME` defaults to `Social`; visible copy is neutralized. Internal compatibility IDs remain intentionally unchanged. |
| 65 | Build the web artifact with the command in `docs/SOCIAL_EDRIFFLES_DEPLOYMENT.md` | The artifact is a static SPA whose title/metadata use `Social`, whose canonical origin is `https://social.edriffles.us`, whose deep routes load root-relative assets, and whose protocol providers remain separately configured | Polycentric services; meaningful exit | PASS | Production Webpack export completed with the neutral metadata, direct-route asset fix, and accurate public-provider label. Cloudflare Pages deployment `af026399-700a-46de-a1e6-6040fd3914f8` is successful; exact build/login owner confirmation remains pending. |
| 66 | Resolve `social.edriffles.us` and open it over HTTPS after DNS/hosting setup | DNS points to the selected static host, TLS is valid, SPA fallback works on a direct nested-route visit, and login redirects are registered for this exact origin | Deployment honesty; identity/provider separation | PASS | Cloudflare Pages custom-domain status is active. The signed-in browser loaded `/settings/services?cachebust=af026399` and `/` over HTTPS after deployment `af026399-700a-46de-a1e6-6040fd3914f8`; owner must still exercise login and leave OWNER NOTES blank until personally verified. |

## Live site verification snapshot — 2026-08-19

The live authenticated walkthrough was performed against
`https://social.edriffles.us` after Cloudflare Pages deployment
`af026399-700a-46de-a1e6-6040fd3914f8`:

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

The overall state remains `OWNER_ACCEPTANCE_PENDING` because this assessment records several explicitly unexecuted live owner walkthroughs and does not constitute a global acceptance verdict.
