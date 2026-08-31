# Implementation log: Plumbline shell decluttering

## Scope

This batch applies the approved decluttering delta to the existing Plumbline
shell. It does not change routes, provider contracts, OAuth, posting,
engagement, profiles, chat, Spaces, or the Plumbline visual tokens.

## Changes

| Area | Implementation |
|---|---|
| Desktop secondary context | `RightNav.tsx` now exposes a closed-by-default, keyboard-reachable `More context` button. Optional feeds, progress guidance, live events, and discovery sources mount only when opened. |
| Right-rail behavior | The desktop right rail uses its existing fixed layout with independent vertical overflow so expanded context cannot force page-wide scrolling. |
| Feed provenance | `FeedProvenanceCard.tsx` suppresses only the nested provider-composition summary. Its existing source inspection action and details remain available. |
| Provider component | `ProviderCompositionProvenance.tsx` adds an opt-in `showSummary` prop while preserving the existing default for every other surface. |
| Styling | `ecw.css` gives the optional panel and disclosure a restrained recessed surface and structural border using existing tokens. |
| Localization | New disclosure labels and accessibility text were extracted and compiled into the existing English catalog. |

## Design decisions

1. Preserve one primary document stream instead of removing useful features.
2. Keep consequential source/rule information visible at the stream boundary.
3. Defer replaceable and discovery-oriented tools behind one boundary.
4. Preserve provider inspection and the existing mobile shell rather than adding
   a second navigation or disclosure framework.

## Verification record

| Check | Result | Evidence |
|---|---|---|
| Experience Contract validator | PASS | `validate_experience_contract.py` accepted the decluttering contract. |
| Web TypeScript check | PASS | `pnpm typecheck:web` |
| Focused Oxlint | PASS | `pnpm exec oxlint --quiet` on the three changed TypeScript components |
| Prettier | PASS | Changed source, CSS, and decluttering design documents |
| Web export | PASS | `pnpm build-web` after catalog compilation |
| Local browser collapsed state | PASS | Accessible disclosure, no translation IDs, primary feed actions retained |
| Local browser expanded state | PASS | Optional discovery context appeared and the disclosure label changed to `Hide more context` |
| Contract validator | PASS | `python3 scripts/validate_contract.py` reported 144 files, 29 blocking rows, and 6 feed cases. |

## Boundary

The built artifact was verified locally before release. Git publication and
external deployment are separate release operations; this implementation log
does not substitute for deployed-URL verification.
