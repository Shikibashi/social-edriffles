# Experience Contract: Plumbline shell decluttering

## Source Mode

- Mode: product-derived
- Evidence: `DESIGN.md`, the locked Plumbline experience contract, the live
  `plumblines.uk` shell review, and current implementation behavior

## Product Facts

| Claim | Source | Captured at | Freshness/status | Allowed presentation |
|---|---|---|---|---|
| Plumbline is the product identity and user-agent shell | `DESIGN.md` and local brand components | 2026-08-31 | current | Keep the mark and wordmark in the Navigator and responsive masthead |
| The document stream is the primary social task | locked Plumbline experience/layout contracts | 2026-08-31 | current | Give the stream the clearest hierarchy and largest uninterrupted region |
| Provider, rule, and control details are already implemented | `RightNav.tsx`, `FeedProvenanceCard.tsx`, and provider composition components | 2026-08-31 | current | Preserve them, but disclose secondary detail progressively |
| Existing routes and social actions own their data and behavior | current screen and navigation code | 2026-08-31 | current | Do not change route or protocol semantics in this visual refinement |

## Benchmark Sources

- GOV.UK Design System, [Styles and page structure](https://design-system.service.gov.uk/styles/): use a clear page hierarchy and spacing system rather than adding independent visual panels.
- GitHub Primer, [PageLayout](https://primer.style/product/components/page-layout/) and [PageLayout accessibility](https://primer.style/product/components/page-layout/accessibility/): keep header, main content, and pane roles distinct; minimize distractions in fixed panes and avoid overloading one region.
- IBM Carbon, [UI shell fixed side navigation](https://web-components.carbondesignsystem.com/?path=%2Fstory%2Fcomponents-ui-shell--fixed-side-nav): treat shell navigation as an orientation aid and secondary navigation as a separate layer.
- W3C, [WCAG 2.2 Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html): use responsive grid/flex reflow so narrower widths do not require two-dimensional page scrolling.

## Page Goal

- User result: read and act on the selected social surface without first
  parsing every available provider, feed, and discovery tool.
- Product result: make Plumbline’s existing seamful architecture legible through
  hierarchy instead of simultaneous panels.
- Observable success: the user can identify the stream, its selected source,
  the next primary action, and the location of optional tools within one view.

## Audience and Tasks

- Primary user and situation: a signed-in or logged-out AT Protocol user using a
  desktop browser, with a mobile fallback.
- Highest-priority tasks: read the current stream, select a feed, post or
  respond where authorized, and inspect the selected source when needed.
- Secondary tasks: search, change feeds, inspect provider composition, view
  trends, and use progress guidance.
- Main anxieties: too many competing panels, repeated provenance text, and
  uncertainty about whether a secondary source is authoritative.

## Header and Navigation

- Keep the existing Plumbline identity and labeled Navigator at its supported
  desktop widths.
- Keep the document-stream heading and feed tabs as the central surface header.
- Keep the selected-surface Inspector first in the right rail.
- Keep global search available without requiring the user to understand the
  optional-source model.

## Core Message

- Promise: Plumbline gives the user a readable stream first and inspectable
  service seams when they are useful.
- Explanation: the current feed and its concise source/rule state remain in the
  stream; provider comparisons, feed lists, guides, and discovery signals are
  available as optional context.
- Evidence: existing `testID`s, route-aware inspector text, and provider
  provenance controls.

## Content Integrity

| Content item | Classification | Evidence | Presentation rule |
|---|---|---|---|
| Current feed title and concise authority summary | verified | feed provenance state returned by the existing screen | Show once at the stream boundary |
| Provider observations and reconciliation details | verified | existing provider composition result | Keep behind the existing inspect-sources action |
| Search, feed list, progress, live-event, and trend tools | verified | existing right-rail components | Keep available behind `More context`; do not imply authority |
| `More context` disclosure state | hypothesis | new interaction decision for this declutter pass | Default closed and expose `aria-expanded`/accessibility state |

## Section Order

1. Stable identity and navigation.
2. Current document-stream heading and feed selection.
3. One concise feed authority summary and primary composer/content.
4. Selected-surface Inspector.
5. Global search and one `More context` disclosure for optional tools.
6. Footer links and language controls.

## CTA Strategy

- Primary: preserve the existing composer, feed tabs, retry controls, and
  post actions.
- Secondary: use `More context` as the single entry point for replaceable read
  and discovery tools.
- Repetition: remove only the nested duplicate provider summary in the feed
  provenance surface; deeper provider inspection remains available.
- Failure: retain all existing error and permission affordances in their owning
  screen; disclosure must not be required to understand a consequential error.

## Trust Strategy

- Show the selected feed source/rule once at the stream boundary.
- Preserve provider comparison, disagreement, outage, and independence text in
  the existing inspection path.
- Label optional tools as optional and non-authoritative; do not turn the
  disclosure into a hidden fallback.
- Make the collapsed state understandable from its label and accessible name.

## Asset Provenance

| Asset | Source | Local path | License/trademark/attribution | Modification allowed | Status/fallback |
|---|---|---|---|---|---|
| Plumbline mark | project-owned product asset | `upstream/social-app/assets/plumbline/plumbline-mark.svg` and `src/view/icons/PlumblineBrandMark.tsx` | project brand asset | existing rendering only | verified; no new assets |
| Typography | platform stacks | `upstream/social-app/src/ecw.css` and `web/index.html` | system font availability | no new remote fonts | verified fallback stack |

## Desktop Structure

- Reference viewport: 1440 × 900 CSS pixels.
- First viewport: labeled Navigator, centered document stream, compact selected
  surface Inspector, global search, and a closed `More context` disclosure.
- The right rail may scroll when expanded; it must not clip optional content or
  steal the stream’s reading width.
- The feed stream retains structural rules and post actions; no new card grid
  or decorative surface is introduced.

## Mobile Transformations

| Desktop element | Operation | Mobile result | Reason |
|---|---|---|---|
| Inspector | defer | existing mobile route context and service paths | preserve the primary stream width |
| Navigator | replace | existing bottom navigation/drawer | preserve route access within touch width |
| Optional context | collapse | remains available through the existing secondary paths | avoid stacking a second dashboard below the stream |
| Feed authority summary | compress | one concise source/rule notice with existing inspection action | retain provenance without crowding the task |
| Feed tabs | retain and reflow | horizontally scrollable, keyboard-reachable tab row | preserve feed selection and addressability |

## States

| State | Trigger | User sees | Available action | Recovery |
|---|---|---|---|---|
| loading | provider or route data pending | existing structured loading surface | wait or use existing navigation | resolve when data arrives |
| empty | provider returns no records | existing empty explanation | use the owning action or change surface | preserve current recovery |
| error | provider or route fails | existing readable error and recovery | retry, go back, or inspect services | no hidden error behind disclosure |
| success | data is available | stream, one concise source summary, and primary actions | continue reading/acting or expand context | inspect optional sources when needed |

## Performance Budget

- Add no remote assets, fonts, data providers, or polling.
- Keep optional components mounted only when the disclosure is open so their
  existing network/UI work is not foregrounded by default.
- Use existing CSS and ALF tokens; no decorative animation.
- Preserve existing `prefers-reduced-motion` and forced-colors behavior.

## Accessibility Contract

- Use a real button for the disclosure with an accessible name, hint, and
  expanded state.
- Preserve navigation, main content, inspector, headings, link targets, and
  visible focus.
- Keep existing target sizing and keyboard operation; the disclosure must not
  trap focus or alter browser Back/Forward behavior.
- Use hierarchy and text labels, not color alone, to distinguish the selected
  surface from optional sources.

## Adopt

- Adopt a single primary document surface with stable shell landmarks.
- Adopt progressive disclosure for optional tools and secondary provider detail.
- Adopt the benchmark emphasis on fixed-pane restraint, clear structure, and
  responsive reflow.

## Adapt

- Adapt the existing React Native web shell and provider-aware components.
- Use a local `More context` control instead of a new generic disclosure
  framework, because the project already has the necessary Pressable and
  accessibility conventions.
- Keep the Plumbline rules, square geometry, and brass marker unchanged.

## Avoid

- Avoid removing routes or provider controls.
- Avoid a second navigation system, a new provider registry, and a new policy
  layer.
- Avoid replacing the inspector with a generic recommendation rail.
- Avoid adding decorative cards, gradients, badges, or engagement prompts.

## Prompt Contract

GOAL — Make the shared Plumbline shell easier to scan without weakening its
provider-aware behavior.
TASK — Read the selected stream, perform its primary action, and inspect or
change its source when needed.
FACTS — Use current route, feed, provider, and account data only.
CONTENT_INTEGRITY — Preserve verified stream and provider facts; mark the new
disclosure as an interaction hypothesis until browser-reviewed.
ASSETS — Reuse the local Plumbline mark and existing system font stacks.
RESPONSIVE — Keep the stream primary, defer the Inspector, and collapse optional
context at narrow widths.
STATES — Preserve existing loading, empty, error, permission, and success
states.
SUCCESS — One primary stream is immediately understandable; optional tools are
discoverable but not competing; provider seams remain inspectable.

## Success Checks

- Can a user identify the active stream without reading two source panels?
- Is search still available while feeds, guides, and trends are deferred?
- Does expanding `More context` expose every previously visible optional tool?
- Does the disclosure retain accessible focus and expanded state?
- Do the stream, composer, post actions, routes, and mobile navigation remain
  available and unchanged?
- Does the shell remain usable at desktop and mobile widths without horizontal
  page overflow?
