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
