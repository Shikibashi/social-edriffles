# Experience Contract: Plumbline Page Mode editorial reconstruction

## Source Mode

- Mode: product-derived
- Evidence: `docs/design/PLUMBLINE_DESIGN.md`, `DESIGN.md`, the 2026-09-01
  product-owner correction, shared shell source, and a rejected desktop render
  captured in the ChatGPT in-app browser.

## Product Facts

| Claim | Source | Captured at | Freshness/status | Allowed presentation |
|---|---|---|---|---|
| Plumbline is the public product identity | `DESIGN.md` and local brand components | 2026-09-01 | current | Full masthead, page title, and accessible brand label |
| Core read routes currently use the shared layout boundary | `src/components/Layout/index.tsx` and route screens | 2026-09-01 | current | Change Page Mode presentation without changing route behavior |
| Provider source, rule, and control strings are route-derived | `src/view/shell/desktop/RightNav.tsx` | 2026-09-01 | current | Preserve as marginal provenance only |
| Posting and engagement actions already belong to route content | existing route and feed components | 2026-09-01 | current | Preserve their actions, feedback, and recovery behavior |

## Page Goal

- User result: read the selected social surface as a coherent publication while
  retaining a quick path to inspect the source, rule, and available control.
- Product result: make Plumbline immediately communicate editorial publication,
  document flow, marginal provenance, and user-agent identity before generic
  social-app chrome.
- Observable success: a user can identify Plumbline, the current edition, the
  current section, and the responsible provider boundary without the stream
  becoming a narrow dashboard panel.

## Audience and Tasks

- Primary user and situation: a desktop AT Protocol user reading a feed,
  profile, thread, custom feed, topic, tag, or community in a browser.
- Highest-priority tasks: orient to the section, read posts and replies, open
  real links, use the existing social actions, and inspect the responsible
  service boundary only when useful.
- Start and completion: begin at an addressable route and complete a normal
  reading or social action with existing confirmation, error, and recovery
  semantics intact.
- Main anxieties: treating a provider as the network, losing the thread while
  reading, missing an applied rule, or losing ordinary browser behavior.

## Header and Navigation

- Desktop order: full-width Plumbline masthead, index-like Navigator, editorial
  document stream, then marginal Inspector.
- Masthead: full wordmark, restrained descriptor, horizontal rules, optional
  motto, and a plumb-line reference marker.
- Navigator: publication index labels, compact route rows, account context, and
  a visible selected-state line and bob.
- Mobile alternative: retain existing compact brand and bottom or drawer
  navigation; do not force the desktop masthead or marginal rail into the
  reading width.

## Core Message

- Promise: Plumbline is the user's reader and instrument, not a network-owned
  window.
- Explanation: the stream presents people and records as a readable document;
  the margin attributes the service, rule, and available replacement or control.
- Evidence: existing route-aware source, rule, and control values; existing
  provenance and provider-composition surfaces.
- Next understanding: a selected provider is a named, inspectable source rather
  than an invisible property of the network.

## Content Integrity

| Content item | Classification | Evidence | Presentation rule |
|---|---|---|---|
| Product name, descriptor, and motto | verified | local brand source and canonical design | Present as product identity, not a claim about a provider |
| Current section title | verified | route or configured feed title | Use the actual title; do not invent ordering claims |
| Source, rule, and control | verified | route-aware inspector context | Preserve attribution and wording from the current route |
| Post, profile, and community data | verified | existing configured provider queries | Preserve loading, empty, error, and recovery behavior |
| Grayscale hierarchy | prototype | shared typographic and rule treatment in this batch | Validate structurally before accepting the visual direction |

## Section Order

1. Plumbline masthead establishes the publication and its user-agent role.
2. Navigator exposes the index and account context.
3. Editorial section heading names the actual feed or route.
4. Continuous document stream presents posts, thread ancestry, media, and action
   lines.
5. Marginal inspector explains source, rule, and control.
6. Optional adjacent sources remain subordinate to the selected surface.

## CTA Strategy

- Primary: preserve current route actions such as New post, reply, like, repost,
  quote, share, feed selection, profile editing, and recovery actions.
- Secondary: preserve the existing real service destinations and inspection
  links; do not create a replacement authority workflow.
- Repetition: do not add competing masthead CTAs. The masthead orients; route
  content owns its existing actions.
- Completion and failure feedback: retain existing toasts, notices, and error
  actions with no semantic change.

## Trust Strategy

- Anxiety points: provider failure, stale reads, applied moderation, identity
  resolution, and authorization boundaries.
- Evidence before anxiety: show source, rule, and control in marginal form when
  the route supplies them.
- Source and verification: preserve existing provider and protocol provenance;
  do not turn a visual marker into a verification claim.
- Without evidence: use the existing unavailable or error presentation rather
  than fabricate an explanation.

## Asset Provenance

| Asset | Source | Local path | License/trademark/attribution | Modification allowed | Status/fallback |
|---|---|---|---|---|---|
| Plumbline mark | project-owned product asset | `upstream/social-app/assets/plumbline/plumbline-mark.svg` and `src/view/icons/PlumblineBrandMark.tsx` | project brand asset | existing rendering only | verified; React mark fallback |
| Display, UI, and metadata type stacks | existing platform font stacks | `upstream/social-app/src/ecw.css` | platform fonts and fallbacks | use existing stacks only | verified fallback stacks |
| Plumb-line marker | local geometry and brass token | `src/view/shell/PlumblineSelectionMarker.tsx` and shell styles | project implementation | extend structurally | verified visual primitive |

## Desktop Structure

- Reference viewport: 1440 by 900 CSS pixels.
- Frame: a full-width masthead above an asymmetric three-part composition.
- Navigator: approximately 220 to 240 pixels, visually quiet, publication-index
  density, and never equivalent in weight to the stream.
- Editorial stream: approximately 680 pixels with a readable text measure,
  stronger title hierarchy, and a document rather than card-stack grammar.
- Marginal inspector: approximately 230 to 250 pixels, aligned to the masthead
  and stream rules, using type and definition-like details before boxes.
- Rules: masthead rules, section rules, document separators, and marginal note
  rules form the grayscale structural system.

## Mobile Transformations

| Desktop element | Operation | Mobile result | Reason |
|---|---|---|---|
| Full masthead | compress | existing compact product identity | preserve reading height and identity |
| Navigator index | replace | existing bottom or drawer navigation | preserve usable route access |
| Marginal inspector | defer | existing route and Services paths retain details | preserve stream width before secondary context |
| Editorial stream | retain | full-width readable document flow | preserve primary reading and action task |
| Page heading | reorder | current route heading before stream | preserve orientation without desktop chrome |
| Vertical provenance line | compress | compact thread and post ancestry marker | preserve structure without consuming touch width |

## States

| State | Trigger | User sees | Available action | Recovery |
|---|---|---|---|---|
| loading | route data is pending | stable masthead, section structure, and existing loading content | wait or navigate | current provider query resolves |
| empty | selected provider has no records | existing empty explanation in editorial position | use existing action or change route | retry or select another source where supported |
| error | route or provider fails | existing readable error with source context | retry, go back, or inspect Services | preserve browser route and recovery path |
| success | records or route data resolves | named section, document stream, and marginal provenance | read, act, navigate, or inspect source | no extra ceremony |

## Performance Budget

- First screen: existing local mark, CSS, shell components, and existing route
  data only.
- Deferred: optional feeds, discovery sources, trending content, and below-fold
  media remain secondary to the current section.
- No new remote font, texture, illustration, animation library, or network
  request is permitted for this visual correction.
- Low-end fallback: typography, HTML or accessibility roles, rules, and static
  layout remain usable without decorative marker rendering.

## Accessibility Contract

- Landmark and heading order: product masthead, navigation index, main section,
  and complementary marginal context in document order.
- Keyboard and focus: preserve real links, existing buttons, visible focus, skip
  link behavior, and browser Back and Forward behavior.
- Labels and errors: retain all existing accessible labels and error text;
  product identity and decorative plumb geometry have appropriate labels or are
  hidden from assistive technology.
- Contrast and color: hierarchy must remain distinguishable through text scale,
  family, weight, borders, spacing, and marker shape without brass color.
- Reduced motion and forced colors: preserve existing global fallbacks; do not
  make a marker, shadow, or animation required to understand state.

## Prompt Contract

GOAL — Rebuild desktop Page Mode as a Plumbline publication and user-agent
surface, not as an upstream social shell with an ECW skin.
TASK — Orient, read, act, and inspect the attributable service boundary through
an asymmetric masthead, index, document stream, and margin.
FACTS — Use only local product identity, current route titles, route-derived
provider context, and existing record state.
CONTENT_INTEGRITY — Classify product copy and provider context correctly; never
invent an ordering, provider, moderation, verification, or social-action result.
ASSETS — Reuse the local Plumbline mark, existing plumb geometry, and platform
font stacks; add no remote asset.
RESPONSIVE — Compress the masthead, replace the index with existing mobile
navigation, defer margin detail, and retain the document stream.
STATES — Preserve loading, empty, error, and success behavior from the existing
route implementations.
SUCCESS — The first desktop view reads as editorial publication, Plumbline
identity, document flow, marginal provenance, and structural plumb geometry
before ordinary social-app chrome is noticed.

## Success Checks

- The masthead is visibly full-width and contains the PLUMBLINE wordmark,
  descriptor, rules, and motto before the desktop rails.
- `WORKSPACE` and `DOCUMENT STREAM` no longer dominate normal Page Mode.
- The central stream is wider and visually more authoritative than either rail.
- Inspector information is readable as marginal reference notes rather than a
  dashboard card.
- Posts form a continuous document with rules and a non-interactive provenance
  rail while their existing actions remain usable.
- The hierarchy remains intelligible in grayscale by typography, layout, rules,
  and shape.
- Services, Identity, Moderation and Reach, diagnostics, and advanced settings
  retain workbench presentation.
- Desktop and mobile preserve existing focus, route, social-action, provider,
  and recovery semantics.
