# Iteration 04: Home apparatus reduction

## Scope

Direction A refinement only. This iteration changes the shared desktop Home Page Mode hierarchy; it does not alter feed data, provider selection, OAuth grants, posting, reactions, profile editing, or Spaces behavior.

## Baseline

At a public, unsigned local desktop render (`1280 × 720`), the pre-iteration Home screen spent its first viewport on framing rather than reading:

- Masthead: 132 px.
- Edition header: 111 px.
- Feed tabs: 59 px.
- Source summary and its detail control: 63 px.
- First post: 448 px below the viewport top.
- The collapsed Home margin still contained a reference shelf, search, secondary links, and legal links.

## Change

- Reduced the page masthead from 132 px to 112 px while preserving the wordmark, descriptor, and motto.
- Replaced self-describing header scaffolding with the edition title and a small publication-context line.
- Removed the repeated compact feed-name echo from the provenance cue; details still retain the full feed identity and provider data.
- Reduced the desktop edition header, tabs, and compact provenance treatment at the shared Page Mode boundary.
- Made the quiet Home margin progressive: it now offers **Inspect current edition** first. Opening it reveals the contextual provider/reference apparatus; closing it restores the reading-first state.
- Restyled the collapsed margin as a marginal reference rule instead of a bordered utility card.
- Reduced the signed-out Index account prompt to its explicit account actions. The inherited acquisition headline is absent in desktop Page Mode, while **Create account**, **Sign in**, and language selection remain visible and keyboard-accessible.
- Changed the signed-out Page Mode account controls from rounded application buttons to compact square controls, scoped only to the editorial composition.

## Local validation

Fresh browser inspection of the rebuilt local bundle at `127.0.0.1:4176` found:

- Masthead: 112 px.
- Edition header: 78.7 px.
- Feed tabs: 53 px.
- Compact source cue: 24 px; source-details control: 24 px.
- First post: 302.7 px below the viewport top, about 145 px higher than the baseline.
- Central reading measure: 760 px.
- Horizontal overflow: none (`scrollWidth` 1265 px at a 1280 px viewport).
- The Home margin initially exposes only `Edition context` and `Inspect current edition`.
- Opening and closing the inspector toggles the full context apparatus correctly.
- The visible compact provenance string begins with accountable source and state information, not a redundant feed title.
- The signed-out navigation has no visible generic engagement headline; its three retained controls expose semantic button/combobox roles, accessible labels, focusability, and zero border radius.
- The contextual inspector opener and provenance-details control are semantic, labelled, focusable buttons.

Static checks passed after the implementation:

- `pnpm typecheck:web`
- `pnpm lint`
- `git diff --check`
- `pnpm build-web` (with pre-existing bundle-size warnings only)

The targeted review also checked the changed surface against the current Web Interface Guidelines: controls use buttons/roles with labels, a skip link remains present, the main screen retains an `h1`, and the changed CSS introduces neither `transition: all` nor an outline removal.

## Critique

The Home screen now gets to social reading materially sooner and treats provenance as a user-invoked explanatory surface rather than a permanent dashboard rail. The Index behaves more like a publication index: it supplies navigation and account access, without a generic social-network callout competing with the reading surface. The reading stream remains wide enough for media and replies without increasing prose line length.

This is not evidence for authenticated flows, post mutations, OAuth, or narrow/mobile rendering. Those code paths were not changed in this iteration and remain outside this local public-page review. The current browser connector also did not provide a fresh mobile viewport for this iteration.

## Next visual questions

1. Test the same progressive margin behavior on signed-in feed and thread flows without obscuring reply or composer affordances.
2. Review the medium and narrow recompositions with a real mobile viewport before changing mobile Page Mode.
3. Continue replacing any remaining inherited application-shell labels only where they reduce comprehension rather than add useful orientation.
