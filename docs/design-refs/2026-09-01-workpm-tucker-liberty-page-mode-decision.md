# WorkPM decision record: Tucker's Liberty visual direction

## Research finding

The useful precedent is structural, not ornamental. The preserved run of
Benjamin Tucker's `Liberty` is a compact periodical organized around a strong
title treatment, issue/section hierarchy, titled columns, short editorial
items, and deliberate rules. The first-issue transcription describes the
heading as original, vigorous, simple, and restrained; the archive presents
the run as numbered issues with dates and a navigable index. Sources:

- https://www.libertarian-labyrinth.org/periodicals/liberty-1881-1908/
- https://usa.anarchistlibraries.net/library/benjamin-tucker-liberty-vol-i-no-1

This pass uses those observable publication behaviors only. It does not copy
period artwork, historical copy, political symbols, or antique textures.

## Residual concentration in the rejected render

The prior render still made the upstream social application the visual host:
the masthead was a branded strip, the center was a tabbed application column,
the feed provider appeared in the primary title block, and navigation and
inspector surfaces retained equal dashboard weight. The result was still
readable as a social app with a themed stylesheet.

## Decision

Rebuild the shared desktop Page Mode around a publication frame:

```text
publication masthead
index / navigator | editorial document | marginal reference
```

The central document owns the visual measure and reading rhythm. The index is
quiet orientation apparatus. The margin is a typographic note field, not a
card rail. Provider and rule details move out of the headline hierarchy and
remain available as attributable marginal context. The route's actual title
remains the section title; no generic `WORKSPACE` or `DOCUMENT STREAM` label
is allowed to dominate ordinary Page Mode.

## Impact analysis

| Boundary | Change | Preserved contract |
| --- | --- | --- |
| Shared web shell | Give Page Mode a publication frame and semantic landmarks | route stack, auth gates, browser history, mobile navigation |
| Page Mode header | Use masthead, issue line, section title, and rules | feed selection, feed creator/provider facts, existing tabs and handlers |
| Feed rows | Flatten raised containers into continuous document entries | post renderers, media, links, replies, likes, reposts, quotes, errors |
| Navigator | Use index-like grouped links and one structural selection line | real links, counts, compose, account switcher, accessibility |
| Inspector | Render provenance as marginal definitions and notes | source, rule, control, optional-source controls and destinations |
| Workbench routes | Keep stronger panels and controls outside Page Mode | Services, Identity, Moderation, Diagnostics, authorization and policy |

## Acceptance criteria

- At wide desktop, the first viewport reads as a publication before ordinary
  social-app chrome: full wordmark, rules, section title, document flow, and
  marginal reference are immediately visible.
- The reading surface is the largest useful track, with deliberate width and
  readable measure rather than a narrow centered application column.
- No Page Mode inspector group is enclosed in a dashboard card solely for
  grouping; rules, type, and definition-like spacing carry the structure.
- The feed has no floating post-card treatment. Its entries share one paper
  plane, printer-like separators, integrated media, and a continuous
  provenance rail.
- The hierarchy remains legible after colors are converted to grayscale using
  type family, scale, weight, rules, alignment, spacing, and marker geometry.
- Page Mode contains no dominant `WORKSPACE` or `DOCUMENT STREAM` heading.
- Mobile collapses the masthead, navigator, and margin without desktop rail
  leakage or horizontal overflow.
- Existing behavior and accessibility semantics remain unchanged outside the
  visual/information-architecture boundary.

## Implementation evidence

The shared Page Mode boundary now renders `PlumblinePageMasthead` above the
desktop composition. The web layout uses a dominant 760px editorial track
between an index rail and a marginal reference rail at wide widths, collapses
the rails at narrower breakpoints, and keeps the tab row internally scrollable
on mobile. Page Mode headings use the section title and publication metadata;
the old generic workspace/document-stream labels are absent. Feed entries are
flat rows with rules, a continuous provenance rail, and diamond reference
markers. Workbench routes retain their existing stronger panel treatment.

The built artifact was inspected at 1280px, 1024px, and 390px widths. The
checks recorded no page-level horizontal overflow, no generic Page Mode
headings, 31 rendered feed entries, a serif masthead/section/marginal-note
hierarchy, card-free feed rows and inspector notes, and no browser console
errors. The remaining media-legibility gradient is an existing content
overlay, not a page-level decoration. These results are local render/build
evidence; they do not assert a new production deployment or provider-side
behavior.

## Rejection rule

After implementation, reject the pass if a reviewer can still reasonably
describe the result as “Bluesky with an ECW or retro stylesheet.” A title,
palette, or icon change alone is not evidence of conformance.
