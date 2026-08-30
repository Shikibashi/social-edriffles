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
