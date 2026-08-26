# Implementation log: Edriffles Computer Web identity

## Changes

- Set the default product and OAuth client name to `Edriffles`.
- Added the source-owned emblem component and web-only branches for mark,
  wordmark, and mark-with-type components.
- Replaced web metadata, prepaint splash, logged-out footer copy, server shell
  titles, canonical/share-card URLs, and static browser assets.
- Added explicit post-build copying for root web icons, share cards, and the
  server-rendered shell.
- Updated `DESIGN.md`, ECW iconography/provenance, deployment instructions, and
  owner acceptance language.

## Boundaries preserved

- `social.edriffles.us` and `pds.edriffles.us` remain the only product/PDS
  origins in scope.
- OAuth, AT Protocol namespaces, PDS/AppView names, and account handles were
  not renamed or behaviorally changed.
- Qdrant, production credentials, native app infrastructure, and unrelated
  worktree changes were not touched.

## Verification record

The exact companion emblem/favicon hashes are recorded in
`upstream/social-app/assets/edriffles/README.md`. Build and test results are
added after the implementation checks complete.
