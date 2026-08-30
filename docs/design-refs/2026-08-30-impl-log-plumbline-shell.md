# Implementation log: Plumbline shell alignment

## Gate record

- Date: 2026-08-30
- Source mode: delta against the approved Plumbline `DESIGN.md` and existing
  shell/brand implementation.
- Interface mode: Agent Workbench. The shell must preserve navigation context
  while making the current location and workbench identity legible.
- Product Design plugin gate: `UNKNOWN`; no exact Product Design selector was
  present in the installed or available plugin listings.
- Adapter: local implementation using the existing ALF and React Native
  primitives. No new visual dependency was added.
- Direction variants: not rendered. This is a bounded shell correction within
  an already approved visual direction; three page compositions would not
  change the decision.

## Contract applied

- Replace pill geometry on web desktop navigation and the compose control with
  the existing Plumbline one-pixel control radius.
- Make the selected route explicit through the existing route calculation,
  a theme-aware alignment line, and the Plumbline brass bob.
- Preserve browser links, keyboard focus, target sizing, hover treatment,
  reduced-motion behavior, and the existing native shell boundary.
- Keep the marker decorative and expose selection through the interactive
  control's `accessibilityState`.

## Implementation evidence

- `upstream/social-app/src/view/shell/PlumblineSelectionMarker.tsx` provides
  the shared line-and-bob geometry.
- `upstream/social-app/src/view/shell/desktop/LeftNav.tsx` applies the marker,
  selected state, square web geometry, and stable test IDs to route items.
- `upstream/social-app/src/view/shell/desktop/LeftNav.tsx` applies the same
  square web geometry to `ComposeBtn`.
- `upstream/social-app/src/lib/brand.ts` owns the Plumbline brass token, which
  is also used by `PlumblineBrandMark`.

## Verification record

The implementation checks and deployed browser inspection completed with:

- focused Oxlint and Prettier for the touched client files: PASS;
- `git diff --check`: PASS;
- web TypeScript check: PASS;
- focused brand test (`3` tests): PASS;
- production-shaped web export: PASS, with the repository's existing bundle-size
  warnings;
- Pages production deployment: PASS at
  `https://151da74a.social-edriffles.pages.dev`, source `e330ff0`;
- canonical HTTPS delivery: PASS; `https://plumblines.uk/` served the same
  `main.6f4a3b73.js` and `8049.9b433de2.js` entrypoints;
- deployed ChatGPT in-app browser desktop inspection: PASS; the existing
  session rendered `Following — Plumbline`, visible feed provenance, square
  `1px` navigation controls, one `plumbline-nav-marker-home` marker, 48px
  navigation targets, and no page alert;
- narrow-width browser inspection: NOT RUN; no browser viewport-resize control
  is exposed by the persistent in-app browser connector.

## Remaining boundary

This slice changes shell presentation and selected-state disclosure only. It
does not change PDS/AppView routing, OAuth grants, social mutations, provider
reconciliation, identity custody, or external Relay/AppView/PLC evidence.

## Iteration 25: horizontal tab alignment

The shared web tab bar now carries the Plumbline selection grammar used by
the desktop shell. The existing blue underline remains the selection contrast
cue, while a small brass diamond marks the selected tab. Each web tab exposes
`accessibilityState.selected` and `aria-selected`; the marker is decorative,
`aria-hidden`, pointer-transparent, and has a stable test ID.

This is a presentation-only change in
`upstream/social-app/src/view/com/pager/TabBar.web.tsx`. It does not alter
routes, browser links, provider selection, PDS/AppView behavior, OAuth, social
mutations, records, storage, or the native tab bar. It follows the existing
ECW tab component and Plumbline `DESIGN.md` alignment/brass rules instead of
introducing a parallel navigation abstraction.

Verification:

- focused Oxlint: PASS;
- Prettier and `git diff --check`: PASS;
- web TypeScript: PASS;
- production export: PASS, with existing bundle-size warnings;
- client commit `80b823b95`: pushed to the fork branch;
- production Pages deployment `d15a243a`: PASS;
- ChatGPT in-app browser Home route: PASS; one selected tab, explicit
  `aria-selected`, brass marker, no alert;
- ChatGPT in-app browser profile route: PASS; one selected tab, explicit
  `aria-selected`, brass marker, no alert.

The remaining external authority/evidence gates are unchanged.

## Iteration 26: contextual right-rail inspector

The desktop right rail now begins with a compact, route-aware Plumbline
Inspector. It identifies the current route, source category, rule, and
available control, then links to the existing feed or Services workbench.
This makes the Navigator → Workspace → Inspector model visible without
creating another provider registry, policy engine, or privileged AppView.

The feed shortcut links now expose selected state and stable
`plumbline-feed-*` test IDs. Their web controls and the More feeds control use
the existing square one-pixel Plumbline geometry; avatars and semantic
shapes retain their intended forms. New inspector copy was extracted and
compiled through the existing Lingui workflow after the first production
probe exposed untranslated message IDs.

Verification:

- focused Oxlint, Prettier, and `git diff --check`: PASS;
- web TypeScript: PASS;
- English catalog extraction and compilation: PASS;
- production web export: PASS, with existing bundle-size warnings;
- client commits `3c018fd02` and `5f836207a`: pushed to the fork branch;
- Pages deployment: PASS at
  `https://46c0c74f.social-edriffles.pages.dev`;
- logged-out deployment browser inspection: PASS; Sign in/Create account,
  readable inspector copy, selected Discover tab, Plumbline title, and no
  alerts;
- canonical Home: PASS; `Following — Plumbline`, inspector copy, selected
  tab marker, Plumbline favicon, and no alerts;
- canonical profile: PASS; profile inspector, selected Posts marker, loaded
  profile/PDS/CDN media, and no alerts;
- canonical post thread: PASS; post inspector and reply/repost/like controls,
  with no alerts;
- narrow viewport: NOT RUN because the persistent ChatGPT in-app browser
  connector does not expose viewport resizing.

This is a shell disclosure slice only. Provider selection, PDS/AppView
routing, OAuth, social mutations, records, storage, identity custody, and the
external Relay/AppView/PLC evidence gates are unchanged.

## Iteration 27: explicit Chat OAuth boundary

The Chat route no longer attempts Chat reads when the separate Chat OAuth
permission is absent. Status, unread-count, conversation-list,
request-inbox, and direct-conversation query hooks now share the existing
feature-scoped grant check. The main Chat and request-inbox screens show a
square, bordered Plumbline authorization panel with the feature name, an
explicit `Authorize this feature` action, and an `Open Services` path. Consent
is not opened automatically, and no grant was widened.

Verification:

- touched-file Oxlint: PASS;
- English catalog extraction and compilation: PASS;
- web TypeScript: PASS;
- OAuth authority and scope tests: PASS, 15 tests;
- production web export: PASS, with existing bundle-size warnings;
- client commit `9d1f6c6fc`: pushed to the fork branch;
- Pages deployment: PASS at
  `https://49ede667.social-edriffles.pages.dev`;
- logged-out deployment shell and Chat route: PASS, no alert or raw
  missing-scope error;
- canonical signed-in Chat and request-inbox routes: PASS, explicit
  authorization panel visible and no raw missing-scope error;
- repository-wide lint: FAIL (baseline) from unrelated existing diagnostics;
- Relay/AppView, short-TTL OAuth, and independent-PLC evidence gates remain
  unresolved.

## Iteration 28: explicit Communities OAuth boundary

The Communities surface now treats the Spaces permission as a real delegated
authority. Community directory and selected-community reads do not run while
an OAuth session lacks that grant. The directory shows the shared Plumbline
authorization panel with `Feature: Spaces`, disables `New community`, and
withholds the selected board until authorization is available. The shared
prompt now names the resource associated with each feature instead of always
referring to the Chat service.

Verification:

- touched-file Oxlint, Prettier, `git diff --check`, and web TypeScript: PASS;
- English catalog extraction/compile: PASS;
- production web export: PASS, with existing bundle-size warnings;
- client code commit `c82c4303b`: pushed to the fork branch;
- Pages deployment: PASS at
  `https://8aefbf18.social-edriffles.pages.dev`;
- logged-out deployment Communities route: PASS, no raw scope or community
  error;
- canonical signed-in Communities route: PASS; Spaces authorization panel,
  `Feature: Spaces`, `Open Services`, and disabled `New community` visible;
- old generic PDS authorization error: absent from the canonical route;
- repository-wide lint: FAIL (baseline) from unrelated existing diagnostics;
- Relay/AppView, short-TTL OAuth, and independent-PLC gates remain unresolved.

## Iteration 29: profile media provenance source links

The existing profile-media boundary now makes the authored record and its
delivery path explicit. The profile inspector localizes its authority summary,
exposes the account's `app.bsky.actor.profile/self` AT URI, and provides
browser-native links to the exact avatar and banner `com.atproto.sync.getBlob`
URLs derived from the record-owned CIDs. This extends the existing account-PDS
boundary; it does not add a second media-provider authority or change profile
records.

### Contract applied

- Treat the account PDS profile record as the authority for avatar/banner CIDs.
- Treat the PDS `getBlob` URL as a derived transport path, not as a second
  author of the media.
- Make the record address, endpoint, method, and CIDs selectable in the
  inspector.
- Preserve browser-native external links, accessible labels, URL normalization,
  and direct PDS media loading.
- Use the existing Plumbline brass token for the source-media alignment marker.

### Implementation evidence

- `upstream/social-app/src/lib/api/account-profile.ts` adds
  `recordUri` to the existing media provenance value and retains direct PDS
  blob URL derivation.
- `upstream/social-app/src/components/MediaDeliveryProvenance.tsx` adds the
  localized source summary, record URI, and accessible avatar/banner source
  links.
- `upstream/social-app/src/lib/api/account-profile.test.ts` covers the new
  record URI while preserving existing PDS-owned media and unsafe-endpoint
  cases.
- `upstream/social-app/src/locale/locales/en/messages.po` contains the
  extracted English strings.

### Verification record

- focused Oxlint, Prettier, and `git diff --check`: PASS;
- account-profile Jest suite: PASS, 6 tests;
- web TypeScript check: PASS;
- English catalog extraction/compile: PASS, 3321 source messages;
- production web export: PASS, with existing bundle-size warnings;
- client code commit `91f7e4314`: pushed to the fork branch;
- client decision record commits `2bd0816f0` and `68afc3735`: pushed to the
  fork branch;
- Pages deployment: PASS at `https://aad5cdf4.social-edriffles.pages.dev`,
  uploaded with Node `v24.19.0` after the host's Node `v26.7.0` path was
  rejected by the repository runtime requirement;
- ChatGPT in-app browser canonical profile inspection: PASS; the deployed
  page showed the authority summary, selectable AT URI, source links, and no
  alert;
- direct media load: PASS; the deployed avatar and banner PDS images reported
  complete with non-zero dimensions.

### Remaining boundary

This is a UI/provenance extension only. It does not establish an independent
media operator, change PDS/AppView routing, add OAuth authority, or close the
external Relay/AppView, short-TTL OAuth, and independent-PLC evidence gates.

## Iteration 30: inline Services workbench controls

The Services screen now exposes provider and policy changes in the workspace
instead of routing them through native alert menus. Provider rows open an
inspector with the service DID, HTTPS endpoint, declared capabilities, current
selection, and an explicit read-provider action. Per-surface capability rows,
reconciliation modes, explicit provider preferences, identity-resolution
policy, and PLC resolver state use the same inline, reversible interaction
grammar.

### Contract applied

- Keep the existing provider registry, local policy persistence, and probing
  functions as the only state-changing boundaries.
- Make source, rule, current state, and available replacement visible before a
  choice is applied.
- Keep PDS writes, account identity, and OAuth/session authority separate from
  read-provider selection.
- Preserve browser-visible selected states, selectable endpoint/DID values, and
  ordinary close/back paths.

### Implementation evidence

- `upstream/social-app/src/screens/Settings/ServicesSettings.tsx` adds the
  inline `WorkbenchActionPanel` and `ProviderSurfaceActionPanel` components.
- Provider, surface, reconciliation, identity, and resolver rows now open
  inspectable controls with explicit selected state and no hidden fallback.
- Nested client commits `246e3c5fd` (implementation) and `dba27a84f`
  (decision record) are pushed to
  `fork/codex/spaces-alpha-integration`.

### Verification record

- focused Oxlint, Prettier, and `git diff --check`: PASS;
- web TypeScript check: PASS;
- production web export: PASS, with existing bundle-size warnings;
- Pages deployment: PASS at
  `https://e8965e7d.social-edriffles.pages.dev`, uploaded with Node
  `v24.19.0`;
- ChatGPT in-app browser canonical Services provider inspection: PASS; the
  page showed the provider DID, HTTPS endpoint, capabilities, selected state,
  and explicit `Use for new reads` / `Configure surfaces` controls;
- browser surface configuration inspection: PASS; each runtime surface and
  its allow/remove state was visible;
- browser reconciliation and identity policy inspection: PASS; modes,
  provider preferences, selected state, and close controls were visible;
- logged-out disposable deployment route: PASS; the protected Services route
  returned the logged-out shell without exposing a raw error.

The nested client still has the pre-existing uncommitted
`oxlint-suppressions.json` newline-only change; it was not included. The PDS,
OAuth, external Relay/AppView, short-TTL OAuth, and independent-PLC operator
evidence gates remain unchanged and unresolved.

## Iteration 31: copyable AT URI in post provenance

### Intent

Keep post records browser-native and portable. The existing `Why this post?`
inspector showed the stable post record as selectable text, but did not offer a
direct action for carrying that address to another client, resolver, or
protocol tool.

### Change

`upstream/social-app/src/components/Post/PostProvenance.tsx` now renders an
accessible `Copy AT URI` action beside the post record when provenance details
are expanded. It uses the existing Expo clipboard and toast abstractions and
stops propagation so copying does not activate the surrounding post link.

### Authority boundary

The post URI remains sourced from the protocol-shaped post model. This change
does not add a resolver, AppView, or fallback provider, and it does not make a
provider authoritative. It only makes an already exposed record address
portable and directly actionable.

### Verification record

- touched-file Oxlint: PASS;
- touched-file Prettier and `git diff --check`: PASS;
- web TypeScript: PASS;
- catalog extraction/compile: PASS; `pnpm intl:extract && pnpm intl:compile`
  produced 3324 source messages;
- production export: PASS; `EXPO_PUBLIC_ENV=production pnpm build-web`, with
  existing bundle-size warnings;
- nested client code commit `e3d4ce3c0` and decision record commit `469314890`:
  PASS; both pushed to `fork/codex/spaces-alpha-integration`;
- Pages deployment: PASS at
  `https://470139e7.social-edriffles.pages.dev`, uploaded with Node `v24.19.0`;
- ChatGPT in-app-browser inspection: PASS at
  `https://plumblines.uk/?deployment=470139e7`; expanded post provenance showed
  the copy control and the read-only click retained the route without an alert.

## Iteration 32: moderation source-state summary

### Intent

Make the main Moderation & Reach screen answer the source and rule questions
before the user opens an individual labeler or moderation detail. The existing
screen already described the generic Source / Assertion / My rule / Client
action chain, but did not summarize the current label-source availability.

### Change

`upstream/social-app/src/screens/Moderation/index.tsx` now uses the shared
`PlumblineAuthoritySummary` to show configured label sources, their loading or
availability state, and the local rule that interprets label claims. It also
exposes a visible link to the existing Services provider workbench.

### Authority boundary

The summary reads the existing labeler query and preferences only. It does not
create a moderation provider, select a fallback, reinterpret labels, or change
the PDS/account write boundary. The detailed four-layer explanation remains
below the summary.

### Verification record

- touched-file Oxlint, Prettier, and web TypeScript: PASS;
- provider-composition and attention model tests: PASS, 24 tests;
- catalog extraction/compile: PASS, 3330 source messages;
- production web export: PASS, with existing bundle-size warnings;
- nested client implementation commit `f801b7099`: PASS; pushed to
  `fork/codex/spaces-alpha-integration`;
- Pages deployment: PASS at
  `https://67ef54e3.social-edriffles.pages.dev`, uploaded with Node `v24.19.0`;
- ChatGPT in-app-browser verification: PASS at
  `https://plumblines.uk/moderation?deployment=67ef54e3`; the summary,
  four-layer explanation, and Services link rendered without an alert, and the
  link reached `Services — Plumbline?section=providers`.

## Iteration 33: notification document-stream refinement

### Intent

Continue the Plumbline document-stream treatment through Notifications. The
provider composition and source disclosure were already present, so this
slice changes only the activity record renderer: unread state becomes a clear
semantic left boundary, and embedded feed/starter-pack records use square
geometry instead of floating rounded cards.

### Change

`upstream/social-app/src/view/com/notifications/NotificationFeedItem.tsx`
now adds the existing primary-color unread rule and removes rounded corners
from the two embedded record treatments. Existing links, actions, author
grouping, moderation, notification data, and provider provenance are
unchanged.

### Verification record

- touched-file Oxlint: PASS;
- touched-file Prettier and `git diff --check`: PASS;
- web TypeScript: PASS;
- production web export: PASS with Node `v24.19.0`; existing bundle-size
  warnings remain;
- root contract validator: PASS; 144 files, 29 blocking rows, 6 feed cases;
- client commit/push: PASS; `dbbe66fd8` pushed to
  `fork/codex/spaces-alpha-integration`;
- deployment/browser inspection: NOT RUN because this iteration requested a
  repository push and did not request a Pages deployment.

The nested client continues to contain the pre-existing newline-only change
in `oxlint-suppressions.json`; it is intentionally excluded. The external
Relay/AppView, short-TTL OAuth, and independent-PLC operator evidence gates
remain unresolved.

## Iteration 34: Chat document-workbench refinement

### Intent

Carry the Plumbline document-stream grammar into the existing Chat workbench
without changing message authorization, conversation queries, navigation, or
mutation behavior. Split-view conversations should read as a continuous list
of records, and unread state should have the same explicit alignment cue used
by the notification stream.

### Change

`upstream/social-app/src/screens/Messages/components/ChatListItem.tsx` now
removes the split-view row's floating rounded treatment and horizontal inset,
uses a contrast rule between conversation records, and adds the existing
primary-color left rule for unread conversations. The full-screen list and
native rendering paths retain their existing layout behavior.

`upstream/social-app/src/screens/Messages/ChatList.tsx` now uses the existing
square control geometry for the desktop and mobile Chat settings and New chat
icon actions. Labels, keyboard/focus behavior, OAuth gating, and button target
sizes are unchanged.

### Authority boundary

This is a presentation-only extension of the existing Chat surface. It does
not add a provider, alter the Chat OAuth grant, widen account authority, change
PDS or AppView routing, or introduce a second messaging state boundary.

### Verification record

- touched-file Prettier: PASS;
- changed-file Oxlint: PASS with the existing compiler immutability warning at
  `ChatList.tsx:365`;
- web TypeScript: PASS;
- focused provider, attention, and OAuth regression tests: PASS, 4 suites and
  39 tests;
- production web export: PASS with Node `v24.19.0`; the existing bundle-size
  warnings remain;
- nested client code commit/push: PASS; `c1b9f726d` pushed to
  `fork/codex/spaces-alpha-integration`;
- Pages deployment and ChatGPT in-app-browser inspection: NOT RUN; this
  iteration requested a source push and did not authorize a live deployment.

The nested client continues to contain the pre-existing newline-only change
in `oxlint-suppressions.json`, and the nested PDS remains dirty; neither is
included. The external Relay/AppView, short-TTL OAuth, and independent-PLC
operator evidence gates remain unresolved.

## Iteration 35: identity authority and exit-workbench entry point

### Intent

Make the Identity & recovery screen answer the authority questions at the
point where account portability, hosting, recovery, and sessions are managed.
The existing screen already exposes these controls, but it presented them as
a flat diagnostic list and left the read-provider replacement path implicit.

### Change

`upstream/social-app/src/screens/Settings/IdentitySovereigntySettings.tsx`
now places the shared `PlumblineAuthoritySummary` above the identity details.
The summary identifies the resolved PDS or DID resolver, states that the DID
identifies the account while the PDS hosts repository and sessions, and shows
the current resolution/migration state without inventing a successful result.

The same screen now has an explicit `Inspect or change read providers` action
that opens the existing Services provider workbench. The action keeps provider
selection a reversible local choice and makes the replacement path visible
without changing identity hosting or write authority.

### Authority boundary

The screen reuses the current resolver, session, migration, export, recovery,
and Services navigation boundaries. It does not add a provider, alter DID or
PDS authority, widen OAuth, change migration behavior, or claim that a local
resolver result proves independent operation.

### Verification record

- touched-file Prettier: PASS;
- changed-file Oxlint: PASS with the existing React compiler warnings in the
  identity screen;
- web TypeScript: PASS;
- focused provider, attention, and OAuth regression tests: PASS, 4 suites and
  39 tests;
- production web export: PASS with Node `v24.19.0`; the existing bundle-size
  warnings remain;
- nested client code commit/push: PASS; `010a3f15f` pushed to
  `fork/codex/spaces-alpha-integration`;
- Pages deployment and ChatGPT in-app-browser inspection: NOT RUN; this
  iteration requested implementation and source push, not live deployment.

The nested client continues to contain the pre-existing newline-only change
in `oxlint-suppressions.json`, and the nested PDS remains dirty; neither is
included. The external Relay/AppView, short-TTL OAuth, and independent-PLC
operator evidence gates remain unresolved.

## Iteration 36: live production Pages binding for the current Plumbline shell

### Deployment evidence

The verified web export from nested client commit `010a3f15f` was uploaded to
the `social-edriffles` Cloudflare Pages project as a Production deployment on
the `main` branch. The deployment identifier is
`23467a9d-1345-40c0-bd0e-e2c617632daf`, with preview URL
`https://23467a9d.social-edriffles.pages.dev`. The canonical
`https://plumblines.uk/` response now serves the same `main.0b646aa7.js`
asset as that deployment.

### Verification record

- production Pages upload: PASS; Wrangler reported the deployment as
  Production / `main`, source `010a3f1`;
- HTTPS response for the deployment URL: PASS, HTTP 200;
- HTTPS response for `https://plumblines.uk/`: PASS, HTTP 200, same current
  asset hash;
- required document headers remained present, including CSP,
  `frame-ancestors 'none'`, `X-Content-Type-Options: nosniff`, and the
  configured Permissions Policy;
- ChatGPT in-app-browser rendered inspection: NOT RUN; the in-app connector
  was unavailable in this runtime, while the generic Playwright connector
  could not initialize because its Chrome distribution was absent. HTTP
  delivery is not being treated as rendered browser evidence.

The nested client continues to contain the pre-existing newline-only change
in `oxlint-suppressions.json`, and the nested PDS remains dirty; neither is
included. The external Relay/AppView, short-TTL OAuth, and independent-PLC
operator evidence gates remain unresolved.

## Iteration 37: Search provider composition for People and Feeds

### Research and implementation

Post search already retained provider observations, but the People and Feeds
tabs still used an implicit AppView path and did not expose which provider
answered or failed. The current `app.bsky.actor.searchActors` Lexicon defines
an unauthenticated query with cursor pagination, while the existing
`composeAppViewProviderRead` boundary already supplies attributable provider
observations and reconciliation policy. The implementation reuses that
boundary rather than introducing a second provider registry.

Actor search now uses the public `profiles` composition surface, keeps its
page cursor and provider receipt through deduplication, and adds a focused
regression test. Popular feed search retains its existing account-scoped
provider boundary while preserving its composition receipt. The People and
Feeds result and error states now render the shared provider-provenance
inspector, including cleaned provider errors.

### Authority boundary

Public actor search does not fan out account credentials. Feed-generator
search keeps the existing account-scoped provider factory because that is the
current project contract. The change adds source visibility and preserves
pagination; it does not add write authority, alter OAuth grants, or make a
built-in AppView constitutionally authoritative.

### Verification record

- changed-file Oxlint: PASS;
- changed-file Prettier check: PASS;
- web TypeScript: PASS;
- focused regression tests: PASS, 5 suites and 25 tests;
- production web export: PASS with Node `v24.19.0`; existing bundle-size
  warnings remain;
- nested client commit: PASS; `4efa4f472` pushed to
  `fork/codex/spaces-alpha-integration`;
- Pages deployment: PASS; Production deployment
  `8263f873` at `https://8263f873.social-edriffles.pages.dev/`, source
  `4efa4f472`;
- HTTPS asset verification: PASS; both the deployment URL and
  `https://plumblines.uk/` returned HTTP 200 and served `main.9f8bf579.js`
  with the configured security headers;
- ChatGPT in-app-browser rendered inspection: NOT RUN; the in-app connector
  was unavailable in this runtime and the generic Playwright connector could
  not initialize because its Chrome distribution was absent.

The nested client still contains the pre-existing newline-only change in
`oxlint-suppressions.json`, and the nested PDS remains dirty; neither is
included. The external Relay/AppView, short-TTL OAuth, and independent-PLC
operator evidence gates remain unresolved.

## Iteration 39: Preserve community directory provenance during total outage

### Research and implementation

The community directory already composes the account PDS and a narrowly
scoped deep-linked community-authority PDS through the shared provider
composition boundary. A successful, partial, or disagreeing read rendered
source observations, but `ProviderCompositionError` evidence was discarded
by the screen when every source failed. That reduced a diagnosable outage to
an unattributed generic error.

`CommunityBoardScreen` now derives one directory-composition value from
either successful query data or the composition attached to the provider
error. The directory evidence panel is rendered for total outages as well as
usable results, includes the local reconciliation policy and the explicit
limit that operator independence is not proven, and offers a source refresh
action. The generic outage message now points at the source observations
instead of implying that the account PDS is the only authority.

### Authority boundary

This is a presentation and recovery change at the existing community
directory boundary. It does not add a provider, mint credentials, widen
OAuth, change Space membership or record authority, or convert multiple
endpoints into proof of independent operation. The local merge policy remains
visible and the source error details remain attributable.

### Verification record

- changed-file Prettier: PASS;
- changed-file Oxlint: PASS;
- community directory composition tests: PASS, 1 suite and 4 tests;
- web TypeScript: PASS;
- production web export: PASS with Node `v24.19.0`; existing bundle-size
  warnings remain;
- root contract validation: PASS, 144 files, 29 blocking rows, 6 feed cases;
- nested client commit/push: PASS; `838c0c871` pushed to
  `fork/codex/spaces-alpha-integration`;
- Pages deployment: PASS; Production deployment `0a2e4b2e` at
  `https://0a2e4b2e.social-edriffles.pages.dev`, source `838c0c871`;
- HTTPS delivery: PASS; the deployment URL and `https://plumblines.uk/`
  returned HTTP 200 and served `main.44bb89f5.js` with the configured
  security headers;
- ChatGPT in-app-browser rendered inspection: NOT RUN; the in-app connector
  remains unavailable in this runtime and the generic Playwright connector
  cannot initialize because its Chrome distribution is absent.

The nested client still contains the pre-existing newline-only change in
`oxlint-suppressions.json`, and the nested PDS remains dirty; neither is
included. The external Relay/AppView, short-TTL OAuth, and independent-PLC
operator evidence gates remain unresolved.

## Iteration 38: Explicit provider exit and local authority cleanup

### Research and implementation

The Services workbench already allowed a user to register a read provider,
change its declared capability surfaces, and change reconciliation policy, but
it did not provide a way to remove a custom provider. That left local provider
registration and dependent selections, fallbacks, and preferred-provider
policies behind after a user chose to leave the service. The implementation
extends the existing provider-store boundary rather than adding another
registry: `removeAppViewProvider` rejects unknown and bundled providers,
removes the custom registration, clears selections and per-account fallbacks
that point to it, resets affected `prefer-provider` policies to
`require-agreement`, and resets identity-resolution preference when necessary.

The Services inspector now exposes `Remove from device` for custom providers
with an explicit confirmation explaining that this is local registration
removal, not remote service deletion or a PDS change. The bundled provider
remains a named convenience default; its optional surfaces can still be
revoked or its policy reset. A focused store test proves dependent state
cleanup, default-provider selection after removal, and bundled-provider
rejection.

### Authority boundary

Before this change, a user could alter a provider's local capabilities but
could not fully exit the local registration, and stale local choices could
continue to influence future reads. After this change, the user can remove a
custom read provider and its local authority references in one inspectable
operation. The operation does not delete a remote provider, mutate identity or
PDS state, widen OAuth, fan out credentials, or change records. It also does
not silently remove the bundled convenience provider; that provider remains
explicitly identifiable and subject to surface and policy controls.

This is a genuine local exit boundary, not a second provider architecture.
The existing provider composition, Services workbench, policy reset, and
identity-resolution mechanisms remain the contracts used by the feature.

### Verification record

- changed-file Prettier check: PASS;
- changed-file Oxlint: PASS with the existing React compiler warnings in the
  settings effect;
- focused provider, OAuth, and provider-composition tests: PASS, 4 suites and
  48 tests;
- web TypeScript: PASS;
- production web export: PASS with Node `v24.19.0`; the existing bundle-size
  warnings remain;
- nested client commit/push: PASS; `7668c7105` pushed to
  `fork/codex/spaces-alpha-integration`;
- Pages deployment: PASS; Production deployment `37fd33cc` at
  `https://37fd33cc.social-edriffles.pages.dev/`, source `7668c7105`;
- HTTPS asset verification: PASS; both the deployment URL and
  `https://plumblines.uk/` returned HTTP 200 and served
  `main.9a50ce99.js` with the configured CSP, frame-ancestor restriction, and
  `X-Content-Type-Options: nosniff` header;
- ChatGPT in-app-browser rendered inspection: NOT RUN; the in-app connector
  was unavailable in this runtime and the generic Playwright connector could
  not initialize because its Chrome distribution was absent.

The nested client still contains the pre-existing newline-only change in
`oxlint-suppressions.json`, and the nested PDS remains dirty; neither is
included. The external Relay/AppView, short-TTL OAuth, and independent-PLC
operator evidence gates remain unresolved.

## Iteration 40: Expose provider claim comparison in the shared inspector

### Research and implementation

The shared provider inspector already displayed source observations, selected
providers, reconciliation policy, and declared operator identity, but it did
not summarize how many distinct values were actually compared. That made a
disagreement or partial outage harder to distinguish from a normal provider
selection without opening and counting the observations manually.

The existing composition result now exposes a typed claim summary derived from
the same usable observations and distinct result keys used by reconciliation.
The shared provenance inspector renders this as `Claims compared`, including
the number of responding providers and the number of observations that did not
provide a usable claim. Agreement, disagreement, total outage, stale, invalid,
and partial states remain attributable; no provider is promoted by the summary.

### Authority boundary

This is a diagnostic presentation improvement at the existing provider
composition boundary. The claim count is derived from returned values, not
operator position, and it does not prove that operators are independent. It
does not change provider selection, reconciliation policy, account
authorization, PDS writes, protocol records, or external service authority.

### Verification record

- changed-file Prettier check: PASS;
- changed-file Oxlint: PASS;
- focused provider-composition, query-composition, and actor-search tests:
  PASS, 3 suites and 21 tests;
- web TypeScript: PASS;
- production web export: PASS with Node `v24.19.0`; existing bundle-size
  warnings remain;
- root contract validation: PASS, 144 files, 29 blocking rows, 6 feed cases;
- nested client commit/push: PASS; `b9208b083` pushed to
  `fork/codex/spaces-alpha-integration`;
- Pages deployment: PASS; Production deployment `c31b81db` at
  `https://c31b81db.social-edriffles.pages.dev`, source `b9208b083`;
- HTTPS asset verification: PASS; the deployment URL and
  `https://plumblines.uk/` returned HTTP 200 and served
  `main.afda48f8.js` with the configured CSP, Permissions Policy,
  referrer policy, and `X-Content-Type-Options: nosniff` header;
- ChatGPT in-app-browser rendered inspection: NOT RUN; the in-app connector
  was unavailable in this runtime and the generic Playwright connector could
  not initialize because its Chrome distribution was absent.

The nested client still contains the pre-existing newline-only change in
`oxlint-suppressions.json`, and the nested PDS remains dirty; neither is
included. The external Relay/AppView, short-TTL OAuth, and independent-PLC
operator evidence gates remain unresolved.

### Follow-up correction and final verification

The first browser inspection of this iteration exposed a real localization
defect: the new label rendered as the Lingui message ID `YZ+A56` instead of
`Claims compared`. The English catalog was regenerated and compiled from the
current source. The tracked `.po` catalog now contains the source-of-truth
entry; the generated `messages.ts` remains ignored and is rebuilt as part of
the web export.

- focused source verification after the catalog correction: PASS; Prettier,
  Oxlint, 3 focused suites and 21 tests, and web TypeScript all passed;
- production web export after the catalog correction: PASS with Node
  `v24.19.0`; existing bundle-size warnings remain; generated asset
  `main.431b1078.js` contains the claim-summary strings;
- nested client catalog commit/push: PASS; `99a010698` pushed to
  `fork/codex/spaces-alpha-integration`;
- final Pages deployment: PASS; Production deployment `b4eff5b1` at
  `https://b4eff5b1.social-edriffles.pages.dev`, source `99a010698`;
- final HTTPS delivery: PASS; the deployment URL and
  `https://plumblines.uk/` returned HTTP 200 and served
  `main.431b1078.js` with the configured CSP, Permissions Policy,
  referrer policy, and `X-Content-Type-Options: nosniff` header;
- final ChatGPT in-app-browser inspection: PASS; after reload at
  `https://plumblines.uk/search` with the `edriffles.us` query, opening Search
  source details displayed `Claims compared: 1 claim from 1 responding
  provider`, the selected `project-appview`, the `api.bsky.app` endpoint, and
  the agreement state. No representational or account actions were taken.

The catalog correction commit still excludes the pre-existing newline-only
change in `oxlint-suppressions.json`. The external Relay/AppView, short-TTL
OAuth, and independent-PLC operator evidence gates remain unresolved.

## Iteration 41: Expose provider composition on direct custom-feed routes

### Research and implementation

The first feed-composition deployment retained complete provider observations
through feed API responses, feed-source metadata, paginated feed pages, and
the shared feed provenance card. A browser inspection of the actual direct
custom-feed route exposed one remaining integration gap: `CustomFeedScreen`
used its own `CustomFeedScreenInner` and did not pass `onFeedContext` or the
full composition result into `ActiveFeedProvenance`. As a result, the route
could show the selected provider and ranking rule but could not open the
existing provider-composition inspector.

The route now uses the existing feed-context callback contract and forwards
provider observations, composition status, operator independence, and the
complete composition result to `ActiveFeedProvenance`. This is a route wiring
correction, not a second provider architecture or a change to reconciliation
semantics.

### Authority boundary

Before this correction, direct custom-feed pages silently dropped provider
composition evidence at the screen boundary. After it, the same feed source
inspector is available on direct custom-feed routes, so selected-provider
claims, agreement state, responding-provider count, and operator-independence
metadata remain inspectable where the user is viewing the feed. The UI still
reports the source's declared verification state and does not convert an
unverified provider into an independent or authoritative source.

### Verification record

- changed-file Prettier check: PASS;
- changed-file Oxlint: PASS;
- focused provider, feed-composition, attention, and actor-search tests:
  PASS, 4 suites and 30 tests;
- web TypeScript: PASS;
- production web export: PASS; generated `main.e5dd1f39.js`; existing bundle
  size warnings remain for the main and supporting JavaScript assets;
- nested client follow-up commit/push: PASS; `1f5f3b4cf` pushed to
  `fork/codex/spaces-alpha-integration`;
- Pages deployment: PASS; deployment `c39ba8a0` at
  `https://c39ba8a0.social-edriffles.pages.dev`, source `1f5f3b4cf`;
- HTTPS delivery: PASS; both the deployment URL and
  `https://plumblines.uk/` returned HTTP 200 and referenced
  `static/js/main.e5dd1f39.js`;
- final ChatGPT in-app-browser inspection: PASS; after navigation to
  `https://plumblines.uk/profile/bsky.app/feed/with-friends`, the direct
  custom-feed route displayed `Show Popular With Friends source details`.
  Opening it displayed `Rule: Require agreement · State: agreement`,
  `Claims compared: 1 claim from 1 responding provider`, and the provider
  observation `Public AT Protocol AppView (external read provider) · ok ·
  unverified`, along with `Change read provider`. No representational or
  account actions were taken.

The nested client still contains the pre-existing newline-only change in
`oxlint-suppressions.json`; root memory/conversation updates and the nested
PDS worktree remain outside this change. The external Relay/AppView,
short-TTL OAuth, and independent-PLC operator evidence gates remain
unresolved.

## Iteration 42: Expose provider composition on the feed directory

### Research and implementation

The feed directory and its search mutation already queried the shared `feeds`
provider-composition boundary, but both UI-facing paths discarded the complete
composition result after selecting the response. The catalog now retains a
typed `providerComposition` on every paginated result, carries the same
composition into precached feed-source metadata, and returns the composition
alongside feed-directory search results. The existing provider inspector is
shown below the directory search control and uses the composition attached to
the active catalog or search state, including composition evidence recovered
from a fail-closed provider error.

The deployment-owned Discover feed fallback remains an explicit configured
feed inclusion. It is not represented as an independent provider claim, so the
directory does not overstate what the provider comparison established.

### Authority boundary

Before this change, the feed directory showed provider-backed feed choices but
did not let the user inspect which read provider answered, which reconciliation
rule selected the result, whether providers disagreed, or whether operator
independence was established. After this change, the same inspectable
provenance used by profiles, threads, custom feeds, search, notifications, and
labels is available on the directory catalog and directory search. Provider
selection remains user-configurable through Services; the UI does not promote
the bundled provider to an independent or universally authoritative source.

### Verification record

- changed-file Prettier check and Oxlint: PASS;
- focused provider, feed, feed-composition, attention, and actor-search tests:
  PASS, 6 suites and 34 tests;
- web TypeScript: PASS;
- production web export: PASS; generated `main.8a85d3c2.js`; existing
  bundle-size warnings remain for the main and supporting JavaScript assets;
- nested client commit/push: PASS; `fcab2827d` pushed to
  `fork/codex/spaces-alpha-integration`;
- Pages deployment: PASS; deployment `4288e538` at
  `https://4288e538.social-edriffles.pages.dev`, source `fcab2827d`;
- HTTPS delivery: PASS; both the deployment URL and
  `https://plumblines.uk/` returned HTTP 200 and referenced
  `static/js/main.8a85d3c2.js`;
- final ChatGPT in-app-browser inspection: PASS; `/feeds` displayed the
  `Popular feeds` source summary and opening it displayed the agreement rule,
  selected `project-appview`, `api.bsky.app`, the responding-provider count,
  endpoint, retrieval timestamp, and `Change read provider`. A read-only
  `science` directory search refreshed the feed results while retaining the
  same inspectable provider evidence. No representational or account actions
  were taken.

The nested client still contains the pre-existing newline-only change in
`oxlint-suppressions.json`; root memory/conversation updates and the nested PDS
worktree remain outside this change. The external Relay/AppView, short-TTL
OAuth, and independent-PLC operator evidence gates remain unresolved.

## Iteration 43: Localize shared Plumbline provenance inspectors

### Implementation

The shared authority summary, provider-composition inspector, and
identity-resolution inspector already formed the existing seam for source,
rule, state, claims, resolver, and operator evidence. This iteration routed
their user-facing labels, status text, policy text, diagnostic labels, and
plural counts through the existing Lingui runtime rather than creating a
parallel localization layer. English source-catalog entries were extracted
and compiled; non-English catalogs were not rewritten beyond this scoped
source update to avoid unrelated reference churn.

### Authority boundary

Before this correction, provider and identity provenance was structurally
inspectable but several status, policy, count, and diagnostic strings bypassed
the client translation boundary as raw English. After it, the same
inspectable evidence remains attributable and the shared seam can render
through the active locale. Protocol identifiers, provider IDs, endpoints,
claim values, and error payloads remain data; only their user-facing labels
are translated. The feed card, OAuth authorization workbench, and Services
settings still have separate localization debt and are intentionally a
follow-up slice.

### Verification record

- changed-file Prettier and scoped Oxlint: PASS;
- focused provider-composition and identity-runtime tests: PASS, 3 suites and
  30 tests;
- web TypeScript: PASS;
- full TypeScript: FAIL on existing iOS/session fixture and Logomark baseline
  errors; no errors in changed files;
- full Oxlint: FAIL on existing repository-wide import-sort/type-rule/
  suppression baseline; scoped changed-file Oxlint: PASS;
- Lingui extraction and compile: PASS;
- production web export with explicit Plumbline environment: PASS; generated
  `main.6e3bd572.js`; existing bundle-size warnings remain;
- nested client commit/push: PASS; `36acda698` pushed to
  `fork/codex/spaces-alpha-integration`;
- Pages deployment: PASS; deployment `c2e45e6c` at
  `https://c2e45e6c.social-edriffles.pages.dev`;
- HTTPS delivery: PASS; preview and canonical `https://plumblines.uk/`
  returned HTTP 200 and referenced `static/js/main.6e3bd572.js`; no localhost
  references appeared in fetched HTML;
- metadata contract: PASS; `https://plumblines.uk/oauth-client-metadata.json`
  returned Plumbline metadata with an HTTPS callback, authorization-code and
  refresh-token grants, and DPoP-bound access tokens;
- final ChatGPT in-app-browser inspection: PASS; the deployed home view
  rendered the Plumbline mark, posts, feed action controls, provider summary,
  and navigation without a visible application error. The feed directory
  source inspector exposed source, rule, state, reconciliation, claim
  comparison, provider observations, operator-independence status, retrieval
  time, and `Change read provider`. No representational or account actions
  were taken.

The nested client retains pre-existing `oxlint-suppressions.json`; root
memory/conversation updates and nested PDS worktree remain outside this
change. External Relay/AppView, short-TTL OAuth, and independent-PLC operator
evidence gates remain unresolved.

## Iteration 44: Localize feed and delegated OAuth provenance

### Implementation

The feed provenance card and delegated-authority inspector already used the
shared Plumbline provider and OAuth seams, but their visible labels and status
descriptions bypassed the translation boundary. This iteration added reusable
Lingui message descriptors for OAuth feature, authority, resource, purpose,
and grant-status labels, then routed feed algorithm, provider, health,
manifest, privacy, operator, and action labels through the active locale. The
protocol identifiers, endpoints, scopes, provider values, and account data
remain inspectable data rather than translated or rewritten identifiers.

### Authority boundary

Before this correction, the underlying source/rule/state evidence was
available but a language change could leave the feed and authorization seams
partly in English. After it, ordinary and expanded views retain the same
provider attribution, least-authority grant ledger, and explicit change/revoke
controls while rendering their interface language through the existing
Lingui runtime. No new provider, fallback, authorization mechanism, or
credential store was introduced.

### Verification record

- focused provider-composition, identity-runtime, and OAuth-scope tests:
  PASS, 4 suites and 41 tests;
- web TypeScript: PASS;
- scoped changed-file Prettier and Oxlint: PASS;
- Lingui extraction and compile: PASS; 3477 source messages after extraction;
- production web export with explicit Plumbline environment: PASS; generated
  `main.00141ab3.js`; the existing bundle-size warnings remain for the 4.15 MiB
  main asset, 3.72 MiB supporting asset, and 631 KiB chunk;
- nested client hook validation during commit: PASS; Oxlint and Prettier
  completed for all staged files;
- nested client commit/push: PASS; `d0ef85aff` pushed to
  `fork/codex/spaces-alpha-integration`;
- Pages deployment: PASS; deployment `1bdf84b9` at
  `https://1bdf84b9.social-edriffles.pages.dev`;
- HTTPS delivery: PASS; preview and canonical `https://plumblines.uk/`
  returned HTTP 200, served `static/js/main.00141ab3.js`, and contained no
  localhost references in fetched HTML;
- final ChatGPT in-app-browser inspection: PASS; the deployed home view
  rendered the Plumbline mark, posts, feed action controls, provider summary,
  and navigation without a visible application error. Expanded feed details
  displayed the algorithm, AppView provider, operator-independence state,
  manifest, privacy, health, and read-provider change control. The feed
  directory displayed its source summary; opening the source inspector
  displayed reconciliation, claims compared, provider observations,
  operator-independence status, retrieval time, and `Change read provider`.
  No representational or account actions were taken.

The nested client retains pre-existing `oxlint-suppressions.json`; root
memory/conversation updates and nested PDS worktree remain outside this
change. Full repository TypeScript and lint baselines still have the
previously recorded unrelated failures. External Relay/AppView, short-TTL
OAuth, and independent-PLC operator evidence gates remain unresolved.

## Iteration 48: Align Profile and Post Thread with the Plumbline workbench

### Implementation

The Profile and Post Thread routes already owned their respective object
inspection seams: profile media, identity resolution, composed profile reads,
thread provider observations, and the existing shell inspector. This iteration
declared both route boundaries as `ecwMode="workbench"`, applying the existing
ECW canvas, structural border, heading, and hit-target grammar without changing
queries, records, interaction mutations, OAuth, moderation, or provider
selection behavior.

### Authority boundary

The screen presentation now matches the architectural role of these routes:
they are inspectable object workspaces rather than anonymous page containers.
The existing inspector remains the place for source, rule, control, and
replaceability context; the existing provenance components remain the source
of profile, identity, media, and thread claims. The workbench attribute is
visual grammar only and grants no authority to Plumbline or to any provider.

### Verification record

- changed-file Prettier and scoped Oxlint: PASS;
- web TypeScript: PASS;
- focused provider-composition, identity-runtime, and OAuth-scope tests:
  PASS, 4 suites and 41 tests;
- `git diff --check`: PASS;
- production web export with explicit Plumbline environment: PASS; generated
  `main.8233a335.js`; existing bundle-size warnings remain for the 4.15 MiB
  main asset, 3.72 MiB supporting asset, and 631 KiB chunk;
- nested client hook validation during commit: PASS; Oxlint and Prettier
  completed for both staged route files;
- nested client commit/push: PASS; `4c9a75bb8` pushed to
  `fork/codex/spaces-alpha-integration`;
- Pages deployment: PASS; deployment `ba715aef` at
  `https://ba715aef.social-edriffles.pages.dev`;
- final ChatGPT in-app-browser inspection: PASS; the signed-in canonical
  Profile route rendered the profile header, posts, profile-media source,
  identity-resolution source/rule/state, Plumbline inspector, and workbench
  layout. The canonical Post Thread route rendered the thread, thread source
  summary, quote/like controls, inspector, and workbench layout. A separate
  preview-domain inspection was signed out and rendered Discover, provider
  provenance, `Why this post?`, post links, and public interaction controls
  without a visible application error. No account, provider, resolver,
  moderation, or content mutation was performed.

The nested client retains the pre-existing `oxlint-suppressions.json` change;
root memory/conversation updates and nested PDS worktree remain outside this
change. Full repository TypeScript and lint baselines still have the
previously recorded unrelated failures. External Relay/AppView, short-TTL
OAuth, and independent-PLC operator evidence gates remain unresolved.

## Iteration 47: Organize Identity & recovery as a Plumbline workbench

### Implementation

The existing Identity & recovery screen already owns the identity, repository
PDS, read-provider, migration, export, user-held PLC rotation-key, session, and
authority-map seams. This iteration preserved those operations and reorganized
the surface into explicit Identity and hosting, Migration and exit, Recovery
and rotation, Sessions and delegation, and Authority map sections. It added
structural section rules, localized the visible labels and action affordances,
and localized the resolver/recovery state summaries without changing provider,
credential, PDS, or PLC behavior.

### Authority boundary

The screen now presents identity continuity, hosting, portability, recovery,
and session control as separate inspectable domains. The DID remains the
identity reference, the PDS remains the repository/session host, the selected
AppView remains a replaceable read provider, local policy remains portable,
and the user-held rotation-key flow remains feature-scoped and explicitly
authorization-gated. Section rules and the brass marker are visual grammar
only; they grant no authority and do not imply a successful migration or
resolver claim.

### Verification record

- changed-file Prettier and scoped Oxlint: PASS;
- web TypeScript: PASS;
- focused provider-composition, identity-runtime, and OAuth-scope tests:
  PASS, 4 suites and 41 tests;
- `git diff --check`: PASS;
- Lingui extraction and compile: PASS; 3796 source messages after extraction;
  generated non-English catalog churn was excluded from the scoped commit;
- production web export with explicit Plumbline environment: PASS; generated
  `main.e1d8ee98.js`; the existing bundle-size warnings remain for the 4.14 MiB
  main asset, 3.72 MiB supporting asset, and 631 KiB chunk;
- nested client hook validation during commit: PASS; Oxlint and Prettier
  completed for all staged files;
- nested client commit/push: PASS; `dd0370919` pushed to
  `fork/codex/spaces-alpha-integration`;
- Pages deployment: PASS; deployment `86b96ca9` at
  `https://86b96ca9.social-edriffles.pages.dev`;
- final ChatGPT in-app-browser inspection: PASS; canonical
  `https://plumblines.uk/settings/identity-sovereignty` rendered the Identity
  & recovery workbench with the Plumbline authority summary, verified
  `https://pds.edriffles.us` resolver/PDS state, localized identity/hosting,
  migration/exit, recovery/rotation, sessions/delegation, and authority-map
  sections, plus the existing Services workbench and portable backup controls.
  The signed-in inspection used the existing session and performed no account,
  provider, recovery-key, export, or session mutation.

The nested client retains pre-existing `oxlint-suppressions.json`; root
memory/conversation updates and nested PDS worktree remain outside this
change. Full repository TypeScript and lint baselines still have the
previously recorded unrelated failures. External Relay/AppView, short-TTL
OAuth, and independent-PLC operator evidence gates remain unresolved.

## Iteration 46: Align Moderation & Reach with Plumbline grammar

### Implementation

The shared `PlumblineAuthoritySummary` already provided the source, rule, and
state seam used by feed, identity, media, and moderation surfaces. This
iteration added the existing Plumbline line-and-brass-bob alignment marker to
that shared component and tightened the Moderation & Reach workbench around
the existing moderation model. Its source-to-assertion-to-user-rule-to-client
action explanation now uses the active Lingui catalog, while moderation tools,
content filters, and labeler states use square bordered groups consistent with
the ECW workbench direction. Provider, label, preference, and authorization
behavior was not changed.

### Authority boundary

The UI now makes the moderation seam visually and verbally consistent with the
other Plumbline inspectors: the source remains an attributable assertion, the
user rule remains local and changeable, and the client action is not presented
as a network-wide deletion or universal authority. The brass marker is
decorative state/provenance grammar only; it grants no authority and carries no
moderation severity meaning. Existing service links and moderation controls
remain the replacement and revocation paths.

### Verification record

- changed-file Prettier and scoped Oxlint: PASS;
- web TypeScript: PASS;
- focused provider-composition, identity-runtime, and OAuth-scope tests:
  PASS, 4 suites and 41 tests;
- `git diff --check`: PASS;
- Lingui extraction and compile: PASS; 3712 source messages after extraction;
  generated non-English catalog churn was excluded from the scoped commit;
- production web export with explicit Plumbline environment: PASS; generated
  `main.f3b41bb9.js`; the existing bundle-size warnings remain for the 4.14 MiB
  main asset, 3.72 MiB supporting asset, and 631 KiB chunk;
- nested client hook validation during commit: PASS; Oxlint and Prettier
  completed for all staged files;
- nested client commit/push: PASS; `205e5c6c3` pushed to
  `fork/codex/spaces-alpha-integration`;
- Pages deployment: PASS; deployment `e1c34a6a` at
  `https://e1c34a6a.social-edriffles.pages.dev`;
- HTTPS delivery and branding inspection: PASS; the generated artifact
  contains the Plumbline title, favicon/mark, canonical OAuth metadata, and
  no local-origin references;
- final ChatGPT in-app-browser inspection: PASS; canonical
  `https://plumblines.uk/moderation` rendered the Moderation & Reach workbench,
  the brass alignment marker, the source/rule/state summary, the moderation
  authority chain, square tool/filter groups, label controls, navigation, and
  the existing inspector without a visible application error. The preview
  domain correctly remained signed out and exposed only public controls. No
  representational, account, provider, labeler, or preference mutation was
  performed.

The nested client retains pre-existing `oxlint-suppressions.json`; root
memory/conversation updates and nested PDS worktree remain outside this
change. Full repository TypeScript and lint baselines still have the
previously recorded unrelated failures. External Relay/AppView, short-TTL
OAuth, and independent-PLC operator evidence gates remain unresolved.

## Iteration 45: Localize the Services authority workbench

### Implementation

The Services workbench already provided the appropriate authority boundary for
provider registration, per-surface capabilities, local reconciliation, OAuth
feature upgrades, identity resolver participation, PLC resolver declarations,
and export/import/reset. This iteration routed that existing UI through the
Lingui source catalog. It added typed message descriptors for service sections,
provider surfaces and authority descriptions, reconciliation actions, resolver
actions, and the workbench inspector while preserving provider IDs, DIDs,
endpoints, protocol scopes, operator assertions, and server error payloads as
inspectable data. No provider, fallback, credential, or authorization
mechanism was added.

### Authority boundary

Before this correction, the Services workbench exposed the seams but left much
of the provider, policy, resolver, and authorization language outside the
active locale. After it, the same source, rule, current-state, user-control,
and replaceability evidence is localized without changing who can write,
resolve, reconcile, or revoke anything. The bundled provider remains a
convenience default and the UI continues to state that declarations do not
prove operator independence.

### Verification record

- focused provider-composition, identity-runtime, and OAuth-scope tests:
  PASS, 4 suites and 41 tests;
- changed-file Prettier and scoped Oxlint: PASS;
- web TypeScript: PASS;
- Lingui extraction and compile: PASS; 3705 source messages after extraction;
- production web export with explicit Plumbline environment: PASS; generated
  `main.e8a3a9a5.js`; existing bundle-size warnings remain for the 4.14 MiB
  main asset, 3.72 MiB supporting asset, and 631 KiB chunk;
- nested client hook validation during commit: PASS; Oxlint and Prettier
  completed for all staged files;
- nested client commit/push: PASS; `c53ba43ce` pushed to
  `fork/codex/spaces-alpha-integration`;
- Pages deployment: PASS; deployment `f93fe3ca` at
  `https://f93fe3ca.social-edriffles.pages.dev`;
- HTTPS delivery: PASS; preview and canonical `https://plumblines.uk/`
  returned HTTP 200, served `static/js/main.e8a3a9a5.js`, and contained no
  `127.0.0.1`, `localhost`, or `19006` references in fetched HTML;
- final ChatGPT in-app-browser inspection: PASS; the deployed Services view
  rendered Overview, Providers, Policies, Authorization, and PLC resolvers
  with localized source/rule/state/control text, provider surface controls,
  policy export/import/reset controls, OAuth upgrade status, and resolver
  declarations. The signed-in read-only inspection showed no visible
  application error. No representational, account, provider, or resolver
  mutation was performed.

The nested client retains pre-existing `oxlint-suppressions.json`; root
memory/conversation updates and nested PDS worktree remain outside this
change. Full repository TypeScript and lint baselines still have the
previously recorded unrelated failures. External Relay/AppView, short-TTL
OAuth, and independent-PLC operator evidence gates remain unresolved.
