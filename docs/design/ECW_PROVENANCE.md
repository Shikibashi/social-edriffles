# ECW Current Provenance

**Status:** Pass A source audit; `OWNER_ACCEPTANCE_PENDING` remains the only acceptance state.

## Source ledger

| Source | Ref/commit | Audit paths | Classification |
| --- | --- | --- | --- |
| `ideologynormativesorter` | `main` / `1820d8d19478677b1b169996814e5a6f1f005ccd` | `src/styles/ecw-tokens.css`, `src/index.css`, `src/App.css`, `src/components/SiteShell.tsx`, `src/ecwTokens.test.ts` | Current living Workbench/data reference |
| `idoldle` | `main` / `33ee4c8fea1e402a16c25bced25756992a05fe0f` | `src/ecw-tokens.css`, `src/index.css`, `src/webpage.css`, `src/components/GameHeader.tsx`, `src/components/HUD.tsx`, `src/lib/ecwTokens.test.ts` | Current living application/control reference |
| `edriffles-blog` | `master` / `a3a1e430b4009de3c035da7b4341adf1635e2452` | `src/styles/global.css`, `src/components/Header.astro`, `src/components/HeaderLink.astro`, `src/layouts/BlogPost.astro`, `src/assets/edriffles-emblem.png` | Current living Page Mode/public identity reference |
| Historical Web99 package | local ZIP, SHA-256 `a59dab80e6f682f7be4411941c4eae5087985f9949cf24647374b108d468d623` | `tokens/`, `guidelines/`, `components/`, `styles.css`, `_ds_manifest.json` | Historical reference; never a current override |

The sorter checkout on disk was behind its remote `main`, so the audit used a detached temporary worktree at the current remote SHA.  The local Idoldle checkout was already at current `main`.  The blog audit used a detached temporary worktree at fetched `origin/master`; its local feature branch was not altered.

## What was observed

### Shared across living products

- `Georgia`/serif display identity, `Verdana`/sans UI content, and `Courier New`/monospace system metadata are intentionally ordered stacks with resilient fallbacks.
- Dark palette starts at `#050719`/`#070a2e`, with `#12144b` panels, `#0b0d38` recessed surfaces, `#1c1e67` raised surfaces, pale lavender text, cyan links, pink hover/marker accents, and yellow focus/status accents.
- Light palette starts at `#d6d9e8`/`#c7ccdf`, with warm `#f4f3eb` panels, `#e1e3ee` recessed surfaces, white raised surfaces, navy text, blue links, purple visited/accent states, and darkened semantic status text.
- 32px grid/backdrop, explicit borders, square geometry, hard shadows, underlined links, and two-tone focus are recurrent design choices.
- Density, theme, contrast, motion, language, and reduced-transparency are separate axes.  Density changes control geometry, not text legibility.

### Product-specific material that is not copied wholesale

- The blog's 1060px editorial shell and 74ch reading column belong to Page Mode, not every social screen.
- Idoldle's framed game/HUD chrome is appropriate to a game and not a universal fake browser window.
- Sorter's large data panes, compass plots, and research status surfaces are Workbench patterns, not mandatory social-feed cards.
- Existing ATProto/Bluesky identity marks remain the network product's marks.  The Edriffles emblem is provenance for the design language, not a replacement for network identity.

## Reconciliations and decisions

| Question | Living-source tension | Current resolution |
| --- | --- | --- |
| Semantic naming | Blog uses `bg/panel/ink`; sorter uses `canvas/workspace/surface/text`; Idoldle has compatibility aliases. | Use structured semantic roles in the client. Keep legacy aliases only at the token boundary, never in new component rules. |
| Dark purple | Blog and sorter use `#9c68ff` for a purple/selection role; Idoldle uses the contrast-reviewed `#b189ff` for purple and `#7787e8` for selection. | Split the roles. Use `#b189ff` for dark accent/identity text where contrast is required; keep selection as its own filled role (`#7787e8` dark, `#2c2a86` light). Do not use purple as a generic text color. |
| Light muted text | Blog's palette comment records `#5e6480`; sorter/Idoldle use darker contrast-corrected muted values (`#4f5570`/`#4d5372`). | Use `#4d5372` as the canonical light muted role for new client UI. Record the blog value as an observed legacy difference, not a silent correction. |
| Status colors | Blog has simple hue tokens; sorter/Idoldle split status text, accent fill, border, and on-accent text. | Use the quartet model. A saturated accent fill never supplies its own text contrast claim. |
| Default density | Sorter defaults compact; Idoldle defaults comfortable; the blog is compact in reading rhythm. | Expose Automatic/Compact/Comfortable. Keep social content readable by default; make compact an explicit user choice and retain the 30px target floor. |
| Theme resolution | Blog uses `prefers-color-scheme`; sorter/Idoldle use a prepaint `data-theme` resolver with system fallback. | Preserve the client’s existing `ALF_THEME` storage and `theme--light`/`theme--dark`/`theme--dim` prepaint classes; system is the initial fallback and an explicit user choice remains stable. |
| Geometry | Blog is a single framed page; Idoldle has game-specific framing; sorter has workbench panels. | Use Page Mode for social content and Workbench Mode for provider/identity/settings surfaces. No fake browser window. |
| Emblem | Blog's current 256px emblem and favicons are current public identity assets; the ZIP contains an older SVG mark. | Treat the blog assets as current Edriffles provenance. Keep the ATProto network mark in the client and apply the ECW geometry/typography around it. |

## Change-control rule

If a visual change would alter a relationship mutation, a provider decision, a ranking outcome, a service boundary, or portable state, it is outside this design pass and must be reviewed as a behavioral change.  The client pass is allowed to expose those distinctions more accurately; it is not allowed to collapse them.
