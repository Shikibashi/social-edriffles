# ECW Current UI Review

**Automated handoff state:** `ECW_CURRENT_UI_BLOCKED`

**Owner state:** `OWNER_ACCEPTANCE_PENDING`

This review covers the current Edriffles Computer Web design synchronization and
the visual application to the ATProto client. It does not approve the product,
change the radical-liberal constitutional behavior, or mark owner acceptance.
The checkout also contains an earlier, separate moderation-list implementation
in the same dirty client submodule. This report does not re-audit or claim that
those existing changes are visual-only; it isolates the ECW changes from them.

## Repository and source SHAs

| Area | Revision inspected | State |
| --- | --- | --- |
| Parent `/var/home/tcs/Code/atproto` | `519a66e25389380935b2b008221135da57796408` | Existing dirty fork work preserved |
| Client `upstream/social-app` | `c38bfe515a9d52d2b9969c8ead64eced5f8d33ee` | Existing dirty moderation work plus this UI pass |
| AppViewLite | retired | Existing nested checkout preserved as a local archive; not a supported dependency |
| PDS | `760fb12a080c87cdfd0dae42ae833bad8bc20886` | Existing dirty submodule |
| Living `ideologynormativesorter` main | `1820d8d19478677b1b169996814e5a6f1f005ccd` | Pass A source |
| Living `idoldle` main | `33ee4c8fea1e402a16c25bced25756992a05fe0f` | Pass A source |
| Living `edriffles-blog` master | `a3a1e430b4009de3c035da7b4341adf1635e2452` | Pass A source |
| Historical Web99 ZIP | `a59dab80e6f682f7be4411941c4eae5087985f9949cf24647374b108d468d623` SHA-256 | Reference only; not authoritative |

## Pass A result

Pass A is complete before the client pass. The following artifacts record the
source ledger, reconciled language, token decisions, iconography, and the Page
Mode/Workbench Mode split:

- `docs/design/ECW_CURRENT.md`
- `docs/design/ECW_PROVENANCE.md`
- `docs/design/ECW_TOKENS.md`
- `docs/design/ECW_ICONOGRAPHY.md`
- `docs/design/ECW_PAGE_MODE.md`
- `docs/design/ECW_WORKBENCH_MODE.md`
- `artifacts/ecw-source-provenance.json`
- `artifacts/ecw-token-diff.json`

The current language is the shared living vocabulary: Georgia-like display,
Verdana-like UI/content, Courier-like metadata, visible square structure,
32-pixel grid rhythm, hard shadows, explicit links, two-tone focus, resilient
contrast/forced-colors behavior, and compact controls that remain usable. The
old Web99 package was not used as a current token or component override.

## Principle-to-implementation map

| Principle | Current implementation | UI surface | Verification |
| --- | --- | --- | --- |
| Current semantic palette | `upstream/social-app/src/alf/themes.ts` and `src/lib/themes.ts` | Shared ALF/native palette plus deprecated `usePalette` compatibility bridge | `src/alf/ecwThemes.test.ts`; web typecheck |
| Page Mode | `src/components/Layout/index.tsx`, default `ecwMode="page"`, `src/ecw.css` | Home, feeds, profiles, threads, search, lists, posts | Static CSS emission; owner visual checks ECW-007–016 |
| Workbench Mode | `Layout.Screen ecwMode="workbench"` on settings, services, identity, personalization, moderation, attention, and diagnostics screens | Explicit service/identity/personalization/moderation work areas | Web typecheck; owner visual checks ECW-017–024 |
| Shell/canvas grammar | `src/view/shell/index.web.tsx`, `src/ecw.css` | Web shell grid, surfaces, structural boundaries | Built CSS contains ECW selectors; owner visual checks |
| Typography and interaction | `src/ecw.css`, `Layout/Header/index.tsx` | Body/UI/display/system roles, link states, focus rings, square controls | Targeted lint; owner checks ECW-025–032 |
| Prepaint theme continuity | `web/index.html`, `bskyweb/templates/base.html` | Initial system/light/dark/dim canvas before hydration | Source inspection and `curl` of running app |
| Behavioral preservation | No ranking, relationship, provider, identity, recovery, or personalization algorithm changes in the ECW files listed below | Existing home, moderation, service, identity, and personalization flows; earlier dirty moderation work remains in the checkout | Diff review of ECW files; owner checks ECW-033–039 |

## Client files changed for this pass

The design pass changed these client files. Existing unrelated dirty files in the
same submodule were preserved:

- `upstream/social-app/src/App.web.tsx`
- `upstream/social-app/src/ecw.css`
- `upstream/social-app/src/alf/themes.ts`
- `upstream/social-app/src/alf/ecwThemes.test.ts`
- `upstream/social-app/src/lib/themes.ts`
- `upstream/social-app/src/components/Layout/index.tsx`
- `upstream/social-app/src/components/Layout/Header/index.tsx`
- `upstream/social-app/src/view/shell/index.web.tsx`
- `upstream/social-app/src/screens/Settings/AppearanceSettings.tsx`
- `upstream/social-app/src/screens/Settings/ContentAndMediaSettings.tsx`
- `upstream/social-app/src/screens/Settings/FollowingFeedPreferences.tsx`
- `upstream/social-app/src/screens/Settings/IdentitySovereigntySettings.tsx`
- `upstream/social-app/src/screens/Settings/InterestsSettings.tsx`
- `upstream/social-app/src/screens/Settings/PersonalizationSettings.tsx`
- `upstream/social-app/src/screens/Settings/ServicesSettings.tsx`
- `upstream/social-app/src/screens/Settings/Settings.tsx`
- `upstream/social-app/src/screens/Moderation/index.tsx`
- `upstream/social-app/src/screens/Moderation/VerificationSettings.tsx`
- `upstream/social-app/src/screens/ModerationInteractionSettings/index.tsx`
- `upstream/social-app/src/view/screens/ModerationBlockedAccounts.tsx`
- `upstream/social-app/src/view/screens/ModerationModlists.tsx`
- `upstream/social-app/src/view/screens/ModerationMutedAccounts.tsx`
- `upstream/social-app/src/view/screens/DebugMod.tsx`
- `upstream/social-app/web/index.html`
- `upstream/social-app/bskyweb/templates/base.html`

The parent-level handoff files are `docs/ECW_OWNER_ACCEPTANCE_CHECKLIST.md`
and this report.

## Verification results

### Green checks

- `pnpm typecheck:web` passed after the final mode and palette changes.
- Full `pnpm typecheck` passed across iOS, Android, and web after repairing the
  fork's typed contract fixtures and validation helpers.
- `pnpm test --runInBand src/alf/ecwThemes.test.ts` passed: 4 tests.
- The combined focused run for ECW plus the existing moderation migration
  passed: 6 tests.
- Full `pnpm test --runInBand` passed: 71 suites, 816 tests, 28 todos, and 21
  snapshots.
- Full `pnpm lint` passed.
- Targeted oxlint for the ECW theme, layout, shell, and newly marked mode files
  passed after import normalization in the two already-dirty settings files.
- `pnpm build-web` passed. Webpack reported existing warnings about a missing
  `ContactAccessButtonProps` re-export, an optional `expo-router` module, and
  recommended bundle-size limits; these were not introduced by the ECW rules.
- `git diff --check` passed for the parent and client changes.
- Pass A JSON and Markdown artifacts validated.
- The running development server responded HTTP 200 on port 19007, and the
  emitted CSS contains the ECW variables plus `data-ecw-shell`,
  `data-ecw-region`, and `data-ecw-mode` selectors.
- Dark and Dim now use distinct low-contrast palettes, and broad control/link
  selectors are scoped under `#root` to reduce interference with unrelated
  document portals.

### Remaining verification limit

- The available Codex in-app browser rejected `http://localhost:19007` under
  its URL policy after the server launched. No screenshot or rendered visual
  verdict is claimed. The owner must perform ECW-001 through ECW-032 locally.

## Behavioral scope and non-changes

The ECW pass intentionally did not modify:

- direct block, mute, follow, list, or moderation semantics;
- provider authority, fallback, feed selection, ranking, More/Less, or Balanced;
- DID, PDS, AppView, resolver, labeler, session, recovery, or personalization
  data behavior;
- Candidate Protocol or constitutional contracts.

The legacy `usePalette` bridge was updated because it was a real visual path
still emitting old white/blue/green/red surfaces. It maps to the same ECW
semantic palette and does not alter action behavior.

The current client submodule also contains separate pre-existing dirty
moderation changes, including list-mute migration and review-created direct
blocks. Those are visible in the working tree and are not represented as ECW
changes here; they require their own behavioral acceptance review.

## Remaining owner questions

- Does the visual hierarchy remain readable at the owner's real desktop and
  mobile sizes, especially in Workbench Mode?
- Are any provider, feed, labeler, resolver, fallback, or “Why this post?”
  messages still too vague in the live fixture?
- Do compact mode, forced colors, reduced motion, and keyboard focus meet the
  owner's practical accessibility bar?
- Does the current density feel like contemporary ECW rather than a decorative
  skin over unrelated social UI?
- Should any additional service/diagnostic route receive Workbench Mode after
  the owner reviews the current screen inventory?

## Local launch and owner handoff

```sh
cd /var/home/tcs/Code/atproto/upstream/social-app
pnpm web -- --port 8081
```

Owner checklist: `docs/ECW_OWNER_ACCEPTANCE_CHECKLIST.md`.

## Personalization entry-row follow-up — 2026-08-19

The rendered public bundle was behind the checkout and still exposed retired
topic-weight controls. In the current client, the local curation editor now
uses a single labeled workbench row with a visible **Add term** button beside
the field. Empty input disables the action; Enter submits it; successful entry
announces confirmation and renders a removable account-local term. The same
entry-row treatment is used for curation exclusions, feed-filter terms, and
explicit interests.

This is the intended ECW/accessibility boundary: real buttons and inputs,
visible instructions, the 30px compact hit-size floor, two-tone focus, and a
keyboard path. The W3C baseline is documented in
[`docs/ALGORITHM_CUSTOMIZATION_RESEARCH.md`](ALGORITHM_CUSTOMIZATION_RESEARCH.md)
with links to WCAG 2.2, WAI Forms, and the ARIA Button Pattern.

Local browser verification confirmed both pointer submission and Enter
submission, then removed the disposable test terms. The live public site still
requires a fresh Pages deployment before it can show this repaired bundle.

The final state remains `OWNER_ACCEPTANCE_PENDING`. It must not be changed to
`OWNER_ACCEPTANCE_PASSED` by this automated review.
