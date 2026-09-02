# Iteration 01 critique: Publication Ledger

## Scope

This iteration validates the Direction A vertical slice against the local production export, not the public deployment. The same source checkout was built with the production configuration gate enabled and served from the generated `web-build` directory. Screenshots were captured in the in-app browser at 1440x900, 1280x720, 1024x768, and 390x844.

## What improved

- The masthead now spans the page and establishes Plumbline before the social content begins.
- The central surface reads as a named edition (`Discover`) with secondary order/source language instead of `WORKSPACE` or `DOCUMENT STREAM` headings.
- The Index, document stream, and Marginal note have distinct visual roles. The stream keeps a 760px desktop measure while the side regions carry navigation and context.
- Feed entries are flat and ruled rather than floating cards. Media remains integrated into the entry, and the action line stays compact.
- The final Page Mode boundary restores the document marker, feed provenance marker, and feed-item plumb line that the earlier HomeScreen simplification hid.
- The narrow render retains a compact Plumbline wordmark, removes the side apparatus, keeps the edition tabs usable, and reports no horizontal overflow.
- The grayscale derivative retains the masthead hierarchy, section rules, document measure, marginal apparatus, and plumb-line geometry without relying on color.

## What regressed or remains risky

- The unauthenticated 1024px capture uses the existing bottom account-action bar instead of rendering the compact Index. This is a shell-level logged-out behavior; the authenticated medium-width state still needs a credentialed browser walkthrough.
- The restored reference line is intentionally quiet. It is visible in computed styles and at the document margin, but its contrast and persistence through long, nested media entries need an independent visual review at several scroll positions.
- The source export reports large JavaScript bundles. This is an existing release-performance warning surfaced during this build, not a reason to hide the new layout, but it should be handled separately.
- The current fixture is an unauthenticated public feed. Profile editing, posting, likes, reposts, quotes, chat, Spaces, provider switching, and selection-linked Inspector updates were not exercised here.

## Research and design checks

| Check | Result | Evidence |
| --- | --- | --- |
| H1 branding establishes the page | PASS | Full-width masthead in all desktop captures; compact lockup in narrow capture |
| H2 user-facing vocabulary | PASS for representative home view | Visible headings use `Index`, edition title, `Marginal note`; implementation vocabulary is not dominant |
| H3 differentiated regions | PASS at wide/standard; partial at medium logged-out | 1440/1280 retain Index + stream + margin; 1024 hides margin and uses account CTA |
| H4 typographic roles | PASS | Serif masthead/section/marginal titles; UI sans for controls; system face reserved for infrastructure cues |
| H5 non-dashboard Inspector | PASS | Marginal note uses rules and definition-like text without card boxes |
| H6 document stream | PASS with review pending | Flat ruled entries, integrated media, action row, restored marker geometry |
| H7 grayscale independence | PASS | `grayscale.png` remains structurally legible and editorial |
| H8 desktop space | PASS at wide/standard | Wide context is used for apparatus while prose stays bounded |
| Narrow overflow | PASS | Browser probe reports no horizontal overflow at 390px |
| Dark theme | NOT VERIFIED | Connector exposes viewport/visibility but not color-scheme emulation; the page remained in light mode |
| Authenticated task behavior | NOT VERIFIED | No disposable credential was available in this browser pass |

## Next changes

1. Obtain an independent adversarial review of the saved renders and explicitly resolve any remaining “Bluesky with a retro stylesheet” evidence.
2. Run a signed-in 1024px and mobile walkthrough to confirm the compact Index, selected-object Marginal note, and action rows preserve their behavioral contracts.
3. Verify a real dark-theme render through the application preference flow or a browser connector that supports color-scheme emulation.
4. If those checks pass, propagate the shared Page Mode boundary to the remaining Page Mode surfaces without changing Workbench composition.

## Release recommendation

**Do not deploy or merge from this artifact yet.** The representative local visual direction is materially improved and meets the structural Direction A target in the available unauthenticated render, but dark mode, authenticated behavior, independent adversarial review, and public deployment remain open verification gates.
