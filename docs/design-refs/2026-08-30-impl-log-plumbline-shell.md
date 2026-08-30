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
