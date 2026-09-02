# Iteration 02 critique: Contextual Ledger

## Scope

This iteration rechecks the Direction A vertical slice after moving the Home Marginal note to an explicit collapsed context state, restoring public Index navigation, preserving the medium compact Index, reserving mobile bottom-bar space, and rebuilding the English catalog. It uses the strict local production export served from the same checkout. It is local evidence, not a public deployment or authenticated interoperability result.

## What improved

- Home now opens with a quiet `Edition context` summary rather than a permanent dashboard-like Marginal note. The full context remains one explicit action away, while non-Home routes retain their contextual Inspector.
- Logged-out Page Mode exposes a real public Index (`Reading`, `Home`, `Explore`, and `Communities`) before the account invitation, so the left apparatus remains navigation rather than becoming only a sign-up panel.
- The medium layout retains a compact Index rail and removes the permanent marginal pane. The central document measure remains 760px; the existing logged-out account actions stay in the bottom bar.
- The mobile layout recomposes to one document column with a compact Plumbline lockup. The main content reserves bottom-bar space: at 390x844 the bottom bar begins at y=782 and the last feed entry can be scrolled to y=673.55, leaving 108.45px of clearance.
- The English catalog was regenerated after the source changes. The saved renders now show `Edition context`, `Inspect current edition`, `Reference shelf`, and `More context` instead of untranslated message identifiers.
- The four saved renders remain free of horizontal overflow. The wide/standard views keep the Index, document, and context apparatus distinct; the medium view demotes context; the narrow view removes both side regions. The grayscale derivative retains the masthead, rules, document flow, and plumb-line structure.
- The shared Index link now exposes `aria-current="page"` for the current route, making the selected editorial marker addressable in the DOM as well as visible.

## What regressed or remains risky

- The contextual Home note is still a route-level summary rather than a fully selection-linked Inspector. The representative public fixture does not select a post, feed, account, or label, so selection-to-margin synchronization remains **NOT VERIFIED**.
- Mobile has an inline `Why this post?` provenance disclosure but no separate global Context drawer. This is an intentional use of the existing post-level disclosure boundary for the current vertical slice; a global contextual action should be added only if real mobile tasks show that the inline path is insufficient.
- The unauthenticated 1024px view still shows the existing account-action bottom bar. An authenticated compact-Index walkthrough is **NOT VERIFIED** because no disposable credential is available in this local browser pass.
- Posting, likes, reposts, quote posts, replies, profile editing, chat, Spaces, provider switching, and migration were not exercised by this unauthenticated visual pass. Existing behavior-owned code was not rewritten.
- A true dark-mode render remains **NOT VERIFIED** because the in-app browser connector does not expose color-scheme emulation and the application preference flow was not part of this local fixture.
- The static export still reports large JavaScript assets. That warning predates this visual boundary and remains a separate performance task.
- The local server is serving generated files from `web-build`; this does not prove that `plumblines.uk` has been deployed or that its cache has been invalidated.

## Research and design checks

| Check | Result | Evidence |
| --- | --- | --- |
| Context is progressive on Home | PASS for public summary state | `Edition context` region and explicit `Inspect current edition` action in the wide and standard captures |
| Public Index remains navigation | PASS | Logged-out DOM and renders contain `Reading`, `Home`, `Explore`, and `Communities` |
| Active navigation is addressable | PASS after source correction | Current link exposes `aria-current="page"`; marker remains visible |
| Medium responsive recomposition | PASS for unauthenticated state | 1024x768 capture retains compact Index, removes permanent margin, and shows no horizontal overflow |
| Mobile content is not occluded | PASS for measured fixture | Bottom-bar clearance probe reports 108.45px at document end |
| English localization | PASS | Rebuilt catalog and clean English labels in saved renders |
| Flat editorial stream | PASS for representative feed | No generic post card wrapper; ruled entries, bounded reading measure, integrated media, compact action row |
| Grayscale independence | PASS | Derived grayscale capture preserves hierarchy and geometry |
| Dark theme | NOT VERIFIED | No connector color-scheme emulation available |
| Authenticated behavior | NOT VERIFIED | No disposable credential in the local browser fixture |
| Public deployment | NOT VERIFIED | Local static server only |

## Next changes

1. Rebuild after the `aria-current` correction and repeat the four viewport probes against the resulting export.
2. Run the repository's focused web typecheck, lint, formatting, web export, and root contract validator against the final source.
3. If authenticated access becomes available, verify the 1024px compact Index, selected-object context, and action rows in a real session.
4. Treat public deployment, cache invalidation, dark-mode verification, and authenticated task walkthroughs as separate release gates.

## Release recommendation

**Hold this iteration locally until the final rebuild and repository gates complete.** The structural Direction A design is now materially improved and the second-pass evidence is clean, but this artifact does not establish authenticated behavior, dark mode, or public deployment.
