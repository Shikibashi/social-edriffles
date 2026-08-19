# ECW Current UI Owner Acceptance Checklist

**State:** `OWNER_ACCEPTANCE_PENDING`

This checklist is for the owner. It does not mark owner acceptance. For each
check, select exactly one owner result: `PASS`, `FAIL`, or `NEEDS CHANGE`, and
record concrete notes where useful.

## Launch

Run the exact command below from a shell. If the requested port is occupied,
use the port printed by Expo.

```sh
cd /var/home/tcs/Code/atproto/upstream/social-app
pnpm web -- --port 8081
```

Open the printed web URL while signed in to the available local fixture or
development account. Verify both light and dark themes, and test at wide,
intermediate, and narrow widths.

| ID | ACTION | EXPECTED BEHAVIOR | PRINCIPLE | AUTOMATED / IMPLEMENTATION EVIDENCE | OWNER RESULT | OWNER NOTES |
| --- | --- | --- | --- | --- | --- | --- |
| ECW-001 | Launch the client with the command above. | The app starts and the printed URL serves the client. | Production-like launch | `pnpm build-web` passed; dev server returned HTTP 200 on port 19007. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-002 | Open the client with no stored theme preference. | The initial theme follows the system preference without a white flash. | Limited defaults; accessibility | Prepaint resolver updated in `web/index.html` and `bskyweb/templates/base.html`. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-003 | Choose Light, Dark, and Dim in Appearance. | Each choice is visibly distinct, persists, and can be changed back. | User control | ALF themes are explicit ECW light/dark/dim themes; Dim has a distinct low-contrast palette. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-004 | Inspect the page at desktop width. | The canvas grid, framed surfaces, structural borders, and small hard shadows are coherent. | Current ECW visual language | `src/ecw.css` implements the web surface layer. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-005 | Resize to an intermediate width. | Secondary context collapses before active-feed identity or provenance disappears. | Responsive sovereignty | Page Mode CSS includes responsive behavior; visual owner check required. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-006 | Resize to a narrow/mobile width. | Route title, active-feed identity, primary action, focus order, and usable controls remain available without horizontal overflow. | Responsive accessibility | Page Mode contract; visual owner check required. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |

## Page Mode and ordinary attention

| ID | ACTION | EXPECTED BEHAVIOR | PRINCIPLE | AUTOMATED / IMPLEMENTATION EVIDENCE | OWNER RESULT | OWNER NOTES |
| --- | --- | --- | --- | --- | --- | --- |
| ECW-007 | Open Home and Following. | The screen reads as a content page, not a fake operating-system window, and Following remains easy to reach. | Attention sovereignty | Home uses the default `ecwMode="page"`. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-008 | Open Balanced. | Balanced is visibly a feed choice, not a mandatory platform objective. | User-controlled attention | Existing Balanced behavior was not changed in this pass. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-009 | Open a custom or external feed. | The named feed and provider remain visible and addressable. | Algorithm marketplace; provenance | Page Mode contract; existing feed behavior preserved. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-010 | Inspect the active feed/provider/version area. | The active feed, provider, and algorithm/version are distinguishable from the platform shell. | Institutional anti-reification | Existing service/attention surfaces preserved; owner visual confirmation required. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-011 | Use More like this. | It changes attention preference only and does not create a follow, mute, or block. | Explicit preference dominance; association freedom | Existing behavior preserved; no behavioral code was changed by ECW pass. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-012 | Use Less like this. | It changes attention preference only and does not create a follow, mute, or block. | Explicit preference dominance; association freedom | Existing behavior preserved; no behavioral code was changed by ECW pass. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-013 | Open Why this post? on a recommendation. | The explanation names only supported reasons and does not claim fabricated precision. | Attention transparency | Existing explanation behavior preserved; owner fidelity check required. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-014 | Change discovery/familiarity/freshness/variety controls where available. | Controls remain visibly separate from relationship actions and retain their state. | Controlled serendipity | Workbench mode applied to attention settings; behavior preserved. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-015 | Inspect Quiet Metrics or equivalent metric visibility control. | Metrics are optional and do not silently become the ranking objective. | Engagement is bounded input | Existing attention behavior preserved. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-016 | Visit a profile, thread, search result, and list. | These ordinary social surfaces share Page Mode rhythm without pretending to be editorial pages. | Current ECW; content neutrality | Page Mode is the default for `Layout.Screen`. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |

## Workbench Mode and authority visibility

| ID | ACTION | EXPECTED BEHAVIOR | PRINCIPLE | AUTOMATED / IMPLEMENTATION EVIDENCE | OWNER RESULT | OWNER NOTES |
| --- | --- | --- | --- | --- | --- | --- |
| ECW-017 | Open Settings. | Settings read as a named control workbench with clear sections and reversible choices. | Individual sovereignty | `Settings.tsx` uses `ecwMode="workbench"`. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-018 | Open Services. | PDS, AppView, feed provider, resolver, and labeler facts are distinguishable where shown. | Polycentric services | `ServicesSettings.tsx` uses Workbench Mode. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-019 | Open Identity sovereignty. | DID/handle, PDS, resolution, migration, recovery, and authority map are not collapsed into “the platform.” | Portable identity; anti-reification | `IdentitySovereigntySettings.tsx` uses Workbench Mode. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-020 | Open Personalization. | Inspect, reset, export, and import controls are visibly separate from identity and relationships. | Portable personalization | `PersonalizationSettings.tsx` uses Workbench Mode. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-021 | Open moderation settings and moderation lists. | Moderation actor, list, labeler, and local policy scope remain distinguishable. | Pluralistic moderation | Moderation screens use Workbench Mode. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-022 | Open diagnostics/debug moderation if enabled. | Diagnostic output is clearly diagnostic and does not look like a user relationship mutation. | Explicit delegated authority | `DebugMod.tsx` uses Workbench Mode. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-023 | Change an AppView or feed provider where the product exposes it. | The choice is visibly attributed to that provider and does not look like a PDS or identity change. | Service substitutability | No ECW behavior path changes provider state. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-024 | Trigger or inspect an unavailable provider state. | The error names the failing service and any fallback; it does not say vaguely that “the platform” failed. | Explicit fallback; institutional attribution | Existing behavior preserved; owner error-copy check required. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |

## Interaction, typography, and accessibility

| ID | ACTION | EXPECTED BEHAVIOR | PRINCIPLE | AUTOMATED / IMPLEMENTATION EVIDENCE | OWNER RESULT | OWNER NOTES |
| --- | --- | --- | --- | --- | --- | --- |
| ECW-025 | Inspect page titles and identity headings. | Display/identity text uses the Georgia-like voice without changing the actual product mark. | Current ECW; accurate attribution | Header title applies the resilient ECW display stack on web. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-026 | Inspect body controls and explanatory copy. | UI/content uses the Verdana-like stack and remains readable; compact does not mean tiny. | Accessibility; current ECW | ECW font roles and body/UI sizes are in `src/ecw.css`. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-027 | Inspect timestamps, provider IDs, and versions. | Metadata is visually distinguishable with the Courier-like system voice where implemented. | Provenance | ECW token contract defines the system role; owner visual check required. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-028 | Navigate with keyboard only. | Links and buttons are reachable in logical order and browser navigation remains normal. | Explicit association; accessibility | Real links/buttons remain unchanged; owner interaction check required. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-029 | Tab through controls in Light and Dark. | Every focused control has a visible two-tone inner/outer focus treatment. | Accessibility | `src/ecw.css` defines `:focus-visible` rings. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-030 | Enable forced colors/high contrast. | Structural boundaries and control identity remain visible without relying on hue alone. | Accessibility; state visibility | Forced-colors and increased-contrast rules are present in `src/ecw.css`. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-031 | Enable reduced motion. | Scrolling, transitions, and animations are reduced without losing task feedback. | Accessibility | Reduced-motion rules are present in `src/ecw.css`. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-032 | Inspect icon-only actions. | Each has an accessible name/tooltip and at least the compact target floor. | Iconography; accessibility | Icon grammar is documented; owner UI check required. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |

## Behavioral non-regression

| ID | ACTION | EXPECTED BEHAVIOR | PRINCIPLE | AUTOMATED / IMPLEMENTATION EVIDENCE | OWNER RESULT | OWNER NOTES |
| --- | --- | --- | --- | --- | --- | --- |
| ECW-033 | Follow and unfollow an account. | The ordinary individually authored association behavior is unchanged by the ECW files. | Freedom of association | ECW files change presentation only; separate dirty moderation work is present in the checkout. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-034 | Block and unblock an account. | Direct hard-block behavior is unchanged by the ECW files and remains distinct from More/Less. | Pairwise freedom of nonassociation | ECW files change presentation only; separate dirty moderation work is present in the checkout. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-035 | Mute/unmute an account or list. | Attention filtering remains distinct from a durable direct block. | Delegated attention | ECW files change presentation only; separate dirty moderation work is present in the checkout. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-036 | Switch theme, provider, or feed, then inspect identity and relationships. | DID, PDS, follows, blocks, recovery, and unrelated preferences do not change because of the ECW layer. | Cross-domain isolation | ECW files contain no provider/identity/ranking mutation; the checkout has separate dirty behavior changes. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-037 | Import/export/reset personalization. | Preference state round-trips without credentials, recovery secrets, or private keys. | Portable personalization; privacy | Existing personalization behavior preserved. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-038 | Inspect a provider failure and recover. | Unaffected functions remain available where practical and any fallback preserves provenance. | Explicit fallback | Existing service behavior preserved; owner integration check required. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-039 | Inspect political/topic controls and feeds. | User-selected topics/feeds remain available, but no mandatory ideological or demographic balancing is introduced by the visual layer. | Political neutrality | ECW pass contains no ranking or political classifier changes. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |
| ECW-040 | Compare the client with the three living Edriffles products. | It belongs to the current ECW family while retaining ATProto identity and product semantics; it does not copy fake browser/game chrome. | Provenance; accurate attribution | Pass A source ledger and reconciliation docs are complete. | ☐ PASS ☐ FAIL ☐ NEEDS CHANGE | |

## Automated gate record

These are evidence for the owner, not owner-result fields:

- `pnpm typecheck:web`: **PASS**.
- `pnpm test --runInBand src/alf/ecwThemes.test.ts`: **PASS** (4 tests).
- Combined ECW plus moderation migration Jest run: **PASS** (6 tests).
- `pnpm build-web`: **PASS WITH EXISTING WARNINGS** (reexport, optional `expo-router` module, and bundle-size warnings).
- Targeted oxlint for the ECW theme/layout files: **PASS**.
- Pass A JSON/Markdown artifact validation: **PASS**.
- Full repository typecheck: **PASS** across iOS, Android, and web.
- Full `pnpm lint`: **PASS**.
- Full `pnpm test --runInBand`: **PASS** (71 suites, 816 tests, 28 todos, 21 snapshots).
- The current client checkout also contains separate dirty moderation-list behavior changes; those are not owner-approved by this checklist.
- In-app browser screenshot/visual run: **UNVERIFIED** because the available browser rejected the localhost URL under its URL policy. The owner must perform the visual checks above.

Do not change the state to `OWNER_ACCEPTANCE_PASSED` until the owner has reviewed the checklist and explicitly records that judgment elsewhere.
