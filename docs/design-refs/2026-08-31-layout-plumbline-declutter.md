# Layout blueprint: Plumbline shell decluttering

## Canonical desktop frame

```text
┌────────────────┬──────────────────────────────────────┬───────────────────┐
│ PLUMBLINE      │ DOCUMENT STREAM                      │ INSPECTOR         │
│ account        │ current feed                         │ selected surface   │
│ NAVIGATOR      │ one concise source/rule summary      │ source             │
│ route rows     │ composer / posts / actions           │ rule               │
│                │ ───────────────────────────────────  │ control            │
│                │ next document                        │ Search             │
│                │                                      │ More context ▸     │
└────────────────┴──────────────────────────────────────┴───────────────────┘
```

## Information hierarchy

1. The stream is the only primary work surface.
2. The Inspector explains the selected route or object.
3. Search remains a global, immediately available read tool.
4. Feed lists, progress guidance, live events, trends, and other replaceable
   sources sit inside one optional context boundary.
5. Provider comparison remains available from the stream’s inspection control,
   but its summary is not repeated beside the feed summary.

## Implementation boundary

- `RightNav.tsx` owns the optional-context disclosure because it already owns
  the fixed desktop right rail and its secondary tools.
- `FeedProvenanceCard.tsx` owns the feed boundary; it suppresses only the
  nested provider-composition summary and leaves its inspection action intact.
- `ProviderCompositionProvenance.tsx` keeps its default summary behavior for
  profiles and other surfaces; no cross-surface contract changes.
- `ecw.css` styles the new disclosure and the scrollable expanded rail using
  existing tokens.

## Responsive transformations

- At desktop widths, keep the labeled Navigator and selected-surface Inspector.
- At intermediate widths, the existing layout breakpoint still controls the
  compact Navigator and Inspector visibility; the optional context remains
  closed by default.
- At mobile widths, the existing bottom navigation and route screens remain the
  owner of navigation; no desktop right rail is introduced.
- When optional content is expanded, the right rail scrolls independently so it
  cannot force page-wide horizontal overflow.

## Design-plan direction record

The 2026-08-30 Plumbline direction remains canonical. This delta does not
generate alternate brand directions because the product owner’s direction is
locked and the evidence identifies a hierarchy problem within that direction.
The delta is reviewed through before/after desktop browser renders and a
responsive ownership check for the existing mobile shell. A physical mobile
viewport remains a follow-up review because the available in-app connector did
not expose viewport resizing.
