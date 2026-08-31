# Plumbline seam refinement implementation log

## Scope

This batch implements a narrow visual and interaction correction in the
existing Plumbline shell. It does not change OAuth scopes, PDS behavior,
provider selection algorithms, record formats, or protocol authority.

## Research basis

- The AT Protocol OAuth and permission specifications treat authorization as a
  declared, feature-scoped capability; the UI therefore keeps the selected
  surface separate from optional provider controls.
- The AT Protocol label model treats labels as attributable claims; the
  existing moderation and provenance components remain the source of that
  distinction.
- WCAG 2.2 and the current web interface guidance reinforce visible focus,
  semantic headings/regions, usable targets, stable layout, and resilient
  text overflow behavior.

## Changes

| Surface | Change | Authority effect |
| --- | --- | --- |
| Home document stream | Names the active pinned feed in the heading and bounds long names | Makes the selected feed legible without changing feed ownership |
| Account context | Removes hover-driven avatar movement and keeps a square, ruled account block | Keeps actor identity stable and distinct from product identity |
| Right rail | Labels optional read and discovery sections, explains their non-authoritative role, and gives them separate structural surfaces | Prevents convenience sources from reading as the selected surface's sovereign answer |
| Preview routing | Preserves SPA fallback for dotted application routes while keeping missing asset extensions as 404s | Keeps handles and other addressable resources working without masking broken assets |
| Design records | Adds a route/seam sitemap and this implementation log | Makes the design boundary inspectable and forkable |

## Intentionally unchanged

The implementation reuses the existing `Layout`, ALF, provider-composition,
provenance, services, identity, moderation, and route systems. No new provider
registry, reconciliation engine, permission grant, fallback, or protocol
endpoint was introduced.

## Verification record

- `pnpm exec prettier --check` on the changed TypeScript, JSX, and CSS files:
  **PASS**.
- `pnpm exec oxlint --quiet` on the changed TypeScript and JSX files:
  **PASS**.
- `pnpm intl:compile`: **PASS**. The new inspector labels are present in the
  compiled English catalog.
- `pnpm typecheck:web`: **PASS**.
- `python3 scripts/validate_contract.py` from the repository root: **PASS**;
  144 files, 29 blocking rows, and 6 feed cases.
- Production web export with the canonical Plumbline environment variables:
  **PASS**. The build completed with existing bundle-size warnings and copied
  the Plumbline metadata, icon assets, and headers into `web-build`.
- Local browser review of the built artifact at `127.0.0.1:19008`: **PASS**.
  At 1440x900 the document stream, provider inspector, optional-read label,
  optional-discovery label, provenance affordances, and post actions were
  present. At 390x844 the mobile shell loaded with the desktop inspector
  deferred and post actions still present.
- Static-preview route assertions: **PASS**. The corrected server returns the
  SPA for `/profile/edriffles.us`, returns 404 for a missing `.js` asset, and
  serves an existing JavaScript asset normally.
- `pnpm typecheck:ios` and `pnpm typecheck:android`: **FAIL** on existing
  session-test/session-type and shared `Logomark` typing errors outside the
  files changed by this batch. They remain unresolved and are not relabeled as
  a Plumbline UI pass.
- Hosted `https://plumblines.uk`: **PASS**. Wrangler 4.125.0 uploaded the
  current `web-build` export to the production `social-edriffles` Pages
  project as deployment `9311eb0f`
  (`https://9311eb0f.social-edriffles.pages.dev`). Read-only HTTPS probes
  returned 200 for the immutable deployment, the canonical host, the OAuth
  metadata document, the Plumbline SVG mark, and the dotted profile route.
  The deployed metadata is bound to `https://plumblines.uk` and its HTTPS
  callback. The ChatGPT in-app browser rendered the canonical Plumbline
  masthead, document stream, provider provenance, inspector, feed controls,
  and posts without an application error. No authenticated or social write
  action was performed.
