# Experience Contract: Plumbline editorial computer

## Source Mode

- Mode: product-derived
- Evidence: user-supplied Plumbline Design specification, current `DESIGN.md`, shared shell implementation, and existing Plumbline browser surface

## Product Facts

| Claim | Source | Captured at | Freshness/status | Allowed presentation |
|---|---|---|---|---|
| Plumbline is the product identity for the AT Protocol client | `DESIGN.md` and product specification | 2026-08-30 | current | Use in masthead, metadata, splash, and share surfaces |
| The canonical web origin is `https://plumblines.uk/` | `DESIGN.md` and runtime brand configuration | 2026-08-30 | current | Use for canonical links and deployment verification |
| The web shell already exposes provider-aware workbench context | `src/view/shell/desktop/RightNav.tsx` and `src/components/Layout/index.tsx` | 2026-08-30 | current | Preserve and make visually legible |

## Benchmark Sources

Not applicable — product-derived direction supplied by the product owner.

## Page Goal

- User result: understand the current social surface and operate it without confusing a provider with the network.
- Product result: make Plumbline's existing provider-aware shell feel coherent, editorial, and trustworthy.
- Observable success: a user can identify the current surface, navigate, inspect the selected provider/rule, and continue ordinary social actions.

## Audience and Tasks

- Primary user and situation: an AT Protocol user reading, posting, and moving among independent services in a desktop browser, with a mobile fallback.
- Highest-priority tasks: navigate to a surface, read the document stream, perform the surface's primary action, and inspect or change its source when needed.
- Start and completion: start at the canonical web origin; completion is a successful readable surface or an explicit recovery action.
- Main anxieties: unclear ownership, stale or missing provider data, lost authorization, and UI states that hide whether an action completed.

## Header and Navigation

- Order: Plumbline mark and wordmark, current account or sign-in context, global navigator, document stream, then inspector.
- Desktop navigation: fixed left navigator with labeled routes and the Plumbline selection marker.
- Mobile alternative: existing bottom navigation and compact brand treatment; inspector is deferred below the primary task.

## Core Message

- Promise: Plumbline keeps the user oriented among people, records, and services.
- Explanation: the document stream is ordinary and calm; provider and rule details appear progressively in the inspector.
- Evidence: source, rule, and control fields already supplied by the existing workbench inspector.
- Next understanding: a default provider is a replaceable source, not an invisible authority.

## Content Integrity

| Content item | Classification | Evidence | Presentation rule |
|---|---|---|---|
| Plumbline wordmark and plumb-bob mark | verified | local brand component and public SVG asset | Use without Bluesky branding; preserve accessible label |
| Provider, rule, and control text | verified | existing route-aware inspector context | Show only claims supported by the current route and data |
| Feed posts, profile records, counts, and timestamps | verified | live records returned by configured providers | Never invent values; preserve existing loading and error states |

## Section Order

1. Shell identity and navigator: establish the user agent and current route.
2. Document stream: keep the primary social task readable and addressable.
3. Inspector: explain provider, rule, and available control without interrupting the task.
4. Secondary services and trends: provide optional exploration after the selected object is understandable.

## CTA Strategy

- Primary: preserve each screen's existing action, including `New post`, navigation links, feed selection, and record inspection.
- Secondary: use provider/service links only where the existing route supplies a real destination.
- Repetition: retain existing placement and show context-sensitive controls in the inspector rather than adding new competing CTAs.
- Completion and failure feedback: keep existing toasts, loading, empty, error, and permission messages; style them as readable document notices.

## Trust Strategy

- Anxiety points: authorization, provider failure, stale reads, moderation effects, and identity ownership.
- Evidence before anxiety: show source, rule, action, and real record addresses where already available.
- Source/date/verification: use live provider labels and existing protocol metadata; do not synthesize verification.
- Without evidence: omit a reason or claim rather than fabricate one.

## Asset Provenance

| Asset | Source | Local path | License/trademark/attribution | Modification allowed | Status/fallback |
|---|---|---|---|---|---|
| Plumbline mark | project-owned product asset | `upstream/social-app/assets/plumbline/plumbline-mark.svg` and `src/view/icons/PlumblineBrandMark.tsx` | project brand asset | limited to product rendering | verified; SVG/React mark fallback |
| Georgia/Verdana/Courier New-like font roles | platform font stacks | `src/ecw.css` and `web/index.html` | system font availability | no font files added | verified fallback stack |

## Desktop Structure

- Reference viewport: 1440 × 900 CSS pixels.
- First viewport: fixed navigator at left, centered document stream with structural rules, fixed inspector at right.
- Grid and hierarchy: Plumbline masthead above account identity; navigation rows below; stream owns the visual weight; inspector is a narrow annotation apparatus.
- Scroll and density: central content scrolls normally; supporting rails remain compact and do not turn the stream into cards.

## Mobile Transformations

| Desktop element | Operation | Mobile result | Reason |
|---|---|---|---|
| Inspector | defer | available after the primary stream or through service context | preserve reading and action width |
| Navigator | replace | existing bottom navigation and drawer paths | preserve route access within touch width |
| Masthead descriptor | compress | mark plus short Plumbline label | preserve identity without consuming the stream |
| Provider details | collapse | concise source/rule notice with deeper service destination | keep infrastructure legible without crowding the task |
| Document rules and metadata | retain | full-width stream with compact dividers | preserve addressability and scanability |

## States

| State | Trigger | User sees | Available action | Recovery |
|---|---|---|---|---|
| loading | provider or route data pending | structured shell with a calm loading surface | wait or use existing navigation | resolve when data arrives |
| empty | provider returns no records | explicit empty explanation | use the existing action or navigate elsewhere | change provider or retry where supported |
| error | provider or route fails | readable error notice with known source and recovery | retry, go back, or inspect services | preserve route and browser history |
| success | data is available | readable stream, actions, and inspectable context | continue the primary task or inspect source | no additional ceremony |

## Performance Budget

- First-screen assets: local mark, existing CSS, shell component, and current route data.
- Deferred assets: non-selected provider details, secondary trends, and below-fold media.
- Font/image/motion budget: use existing system stacks and local mark; no new remote font, texture, or decorative animation.
- Low-end fallback: keep structural borders and text hierarchy when effects or nonessential media are unavailable.

## Accessibility Contract

- Document/landmark/heading order: navigation, main document stream, inspector summary, then secondary links; keep real headings and landmark roles.
- Keyboard/focus/Escape: retain browser links, keyboard navigation, visible focus, and existing dialog escape behavior.
- Labels/errors/live state: preserve accessible labels and existing error/empty text; do not encode meaning by color alone.
- Contrast/color/touch: navy text on paper, dark-on-light and light-on-dark theme pairs, square controls, and at least 30px interactive targets.
- Reduced motion: the layout remains fully usable with transitions removed.

## Adopt

- Adopt the user-supplied editorial computer direction, ECW's workbench layout, and browser-native hypertext.

## Adapt

- Adapt the existing ALF/React Native shell with web tokens and shared data attributes so the redesign remains cross-platform-safe and does not duplicate route or provider logic.

## Avoid

- Avoid new provider abstractions, new feed semantics, new permission requests, decorative gradients, and any claim that a visual change proves runtime interoperability.

## Prompt Contract

GOAL — Make the shared Plumbline web shell read as an editorial computer while preserving social behavior.
AUDIENCE — AT Protocol users reading and acting across user-selected services.
TASK — Navigate, read, act, and inspect the source/rule of the current surface.
FLOW — Masthead and navigator → document stream → inspector → optional services.
HEADER — Plumbline mark, wordmark, open-web descriptor, account context.
MESSAGE — The client is a user agent with inspectable service boundaries.
FACTS — Use only current local brand, route, provider, and record facts.
CONTENT_INTEGRITY — Do not invent counts, reasons, providers, or verification.
SECTION_ORDER — Identity, navigation, stream, inspector, secondary services.
CTA — Preserve current route actions and make service controls ordinary.
TRUST — Put provider, rule, and control evidence next to the surface that needs it.
ASSETS — Use the local Plumbline mark and platform font stacks.
LAYOUT — Navigator | document stream | inspector.
RESPONSIVE — Defer inspector, then replace navigator with existing mobile navigation.
STATES — Preserve loading, empty, error, permission, and success behavior.
PERFORMANCE — No new remote assets or decorative motion.
ACCESSIBILITY — Real landmarks, focus, labels, contrast, target sizes, reduced motion.
PRESERVE — Routes, provider composition, OAuth, posting, engagement, profiles, and Spaces.
EXCLUDE — Bluesky web branding, generic SaaS cards, political cosplay, gradients, and fake infrastructure claims.
SUCCESS — The surface is readable, addressable, inspectable, and usable at desktop and mobile widths.

## Success Checks

- Can a user explain the current route, primary action, and provider boundary within the first view?
- Are source/rule/control claims tied to actual route data rather than invented copy?
- Do loading, empty, error, and success surfaces retain a clear recovery path?
- Does mobile preserve the primary stream before secondary infrastructure detail?
- Do contrast, focus, target size, reduced motion, and forced-colors behavior remain usable?
