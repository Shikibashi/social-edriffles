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
