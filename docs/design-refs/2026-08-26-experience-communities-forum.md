# Experience Contract: Communities forum surface

## Source Mode

- Mode: benchmark
- Evidence: `2026-08-26-brief-communities-forum.md`,
  `2026-08-26-benchmark-communities-forum.md`, the user-provided Bulletin
  direction, and the current `CommunityBoardScreen`/private-post lexicon.

## Product Facts

| Claim | Source | Captured at | Freshness/status | Allowed presentation |
|---|---|---|---|---|
| Bulletin uses an ATProto Spaces-backed board with local read/write and owner moderation rules. | Official Bulletin README and source | 2026-08-26 | current benchmark | Use as design precedent, not as Radlib runtime behavior. |
| Radlib communities expose public, restricted, invite-only, and private visibility through the current PDS control API. | `upstream/atproto-pds/packages/pds/src/api/us/edriffles/radlib/private/index.ts` | 2026-08-26 | current repository evidence | Show the returned visibility in plain language. |
| Private community records are read through the existing Space credential and fanout reader. | `upstream/social-app/src/lib/atproto/spaces/fanout.ts` and `src/lib/permissioned-data.ts` | 2026-08-26 | current repository evidence | Keep the existing transport; do not route through public AppView. |
| The private-post schema permits an unknown `reply` value, so reply grouping can be computed when references are present. | `upstream/social-app/lexicons/us/edriffles/radlib/private/post.json` | 2026-08-26 | current repository evidence | Show only replies actually present in the authorized read result. |
| The current client does not expose a member directory or a trusted member total. | Current lexicons and screen API usage | 2026-08-26 | current limitation | Keep the Members tab transparent about this limitation; never invent a count. |

## Benchmark Sources

- [Bulletin repository](https://github.com/bluesky-social/bulletin) — product
  model and README claims.
- [Bulletin components](https://github.com/bluesky-social/bulletin/tree/main/components)
  — contextual composer and moderation surface names.
- [Bulletin app routes](https://github.com/bluesky-social/bulletin/tree/main/app)
  — dedicated board route precedent.
- Mobile reference capture: unavailable; verify the local route at a narrow
  viewport during implementation.

## Page Goal

- User result: enter a chosen community, understand its access state, scan
  topics, open a topic, and start a topic or reply without losing context.
- Product result: make the existing Space-backed community behavior legible as a
  forum without changing its data boundary.
- Observable success: a signed-in user can identify the community, select a
  topic, see its authorized replies, and submit a contextual private record or
  receive a specific recoverable error.

## Audience and Tasks

- Primary user and situation: a signed-in Bluesky identity visiting one of the
  communities visible to the account.
- Highest-priority task: read and participate in the selected community.
- Start and completion: start on `/community`, choose a community if needed,
  open a topic or `New topic`, and finish when the topic/reply appears after the
  private Space query refreshes.
- Anxiety/friction/failure: unclear privacy boundary, stale access state,
  invite requirements, partial fanout reads, and the possibility that an empty
  result is actually an authorization or transport failure.

## Header and Navigation

- Order: global `Communities` title, compact community switcher, selected
  community identity, local tabs, primary action.
- Desktop navigation: a compact switcher remains above the selected forum in
  the existing Bluesky center column; topic rows and selected topic detail are
  stacked for reliable keyboard and narrow-column behavior.
- Mobile alternative: the switcher scrolls horizontally, the community header
  precedes the tab strip, and topic detail replaces the topic list with an
  explicit `Back to topics` action.

## Core Message

- Promise: `A place for this community's conversations.`
- Explanation: topics and replies stay in the selected community and follow its
  access rules.
- Evidence: returned community name/description/visibility, actual topic and
  reply records, and explicit partial-read/error messaging.
- Next understanding: `New topic` writes here, not to the public feed.

## Content Integrity

| Content item | Classification | Evidence | Presentation rule |
|---|---|---|---|
| Community name, description, visibility | verified | Current PDS `getSpace`/`listCommunities` response | Render returned values; use neutral fallback labels when absent. |
| Topic title and body excerpt | verified | Authorized private-post record text | Derive from text; do not use sample forum copy. |
| Reply count | verified | Count of authorized records with matching `reply.root.uri` | Show the computed count only. |
| Member count and member directory | placeholder | Not exposed by current client contract | Do not show a number; explain the alpha limitation in Members. |
| Handle/avatar for a private record author | placeholder | Fanout result provides repo DID, not profile metadata | Show a shortened DID; do not fabricate a handle or avatar. |
| Bulletin branding or imagery | avoid | External benchmark only | No external asset is copied into the product. |

## Section Order

1. Community switcher: choose the place before reading its content.
2. Community header: establish name, description, access, and current topic
   count.
3. Local tabs: switch between topics, latest activity, membership guidance,
   and community details.
4. Forum content: scan topic rows or latest activity, then open one topic.
5. Contextual composer: start a topic or reply while the selected community is
   visible.
6. Recovery and moderation controls: keep access actions, partial-read notices,
   and owner controls close to the relevant community context.

## CTA Strategy

- Primary: `New topic` — opens the contextual composer for the selected
  community in the Threads view and stays visible in the community header.
- Secondary: `Reply` in topic detail; `Join`, `Leave`, `Refresh`, and `Create a
  community` appear only when their current state makes them relevant.
- Repetition: show `New topic` once in the selected community header and once in
  the empty Threads state; do not repeat it on every topic row.
- Completion/failure: announce `Topic posted` or `Reply posted` in the status
  line after invalidation; show the object, service, and recovery action in
  errors.

## Trust Strategy

- Anxiety points: whether content is public, whether access is current, and
  whether an empty/partial result is complete.
- Immediate evidence: plain-language visibility/access chips, the line that
  posting stays in this community, and a persistent partial-read notice when
  fanout errors occur.
- Source/date/verifiability: community metadata and record timestamps come
  from the PDS response; technical Space/DID details stay in About.
- Without evidence: omit member totals, profile claims, and reply totals that
  are not computable from the authorized result.

## Asset Provenance

| Asset | Source | Local path | License/trademark/attribution | Modification allowed | Status/fallback |
|---|---|---|---|---|---|
| UI icons | Existing social-app icon package | `upstream/social-app/src/components/icons` | Existing project asset policy | Existing use only | verified; no new asset |
| Typeface | Existing ECW/ALF platform stacks | `upstream/social-app/src/ecw.css` and `src/alf` | Existing project styling | No new font distribution | verified; platform fallback |
| Bulletin screenshots/logo | None | None | Not used | n/a | omitted |

## Desktop Structure

- Viewport: 1440 × 900 reference; actual content remains inside the existing
  Bluesky center column.
- First viewport: page title, community switcher, selected community header,
  tabs, first topic rows, and the `New topic` action.
- Grid/panes/hierarchy: one structured forum column with a recessed switcher,
  a bordered community header, a tab rule, then dense topic rows. A selected
  topic replaces the list in the same column to preserve route simplicity.
- Scroll flow/density: 48px minimum topic rows, compact metadata, and no
  decorative cards; detail view expands body/replies vertically.

## Mobile Transformations

| Desktop element | Operation | Mobile result | Reason |
|---|---|---|---|
| Community switcher | compress | Horizontal scroll of compact community links | Preserve place switching without a tall directory before content. |
| Header stats | compress | Two-line access/topic summary | Keep community identity readable at phone width. |
| Local tab strip | retain | Horizontally scrollable tab controls with selected state | Preserve the forum IA and keyboard/touch access. |
| Topic list and selected topic | replace | Topic list view or full-width detail view with `Back to topics` | Focus reading and avoid a cramped split pane. |
| Technical Space/DID details | defer | About tab below human-readable policy | Keep protocol detail available without leading with jargon. |
| Composer controls | reorder | Context line, field, then full-width action | Reduce thumb travel and make destination explicit. |

## States

| State | Trigger | User sees | Available action | Recovery |
|---|---|---|---|---|
| loading | Community or Space query pending | Contextual `Reading communities`/`Loading topics` text and stable layout | Wait; refresh after an error | Query resolves without changing route. |
| empty | Complete authorized read with no records | `No topics yet` and an invitation to start one | `New topic` | Post then refresh the current community. |
| error | Control or Space read fails | Named community/service, concise problem, and `Refresh` | Refresh or return to community switcher | Preserve non-empty metadata rather than showing a false empty state. |
| success | Topic/reply write returns and query invalidates | Topic/reply confirmation in status line and updated list | Open the created conversation context | Keep user in the selected community. |
| partial | Some authorized writer repos fail | Explicit incomplete-read warning | Retry | Never describe the visible records as complete. |
| permission | Join/invite/leave or record access is denied | Plain-language access state and next action | Join/request, enter invite, leave, or contact owner | Server remains authoritative. |

## Performance Budget

- First-screen assets: existing ALF, icons, and text only.
- Deferred assets: no images or external fonts; profile enrichment is not added.
- Font/image/video/motion budget: no new font, image, video, or animation
  dependency; existing control transitions only.
- Slow-device/network fallback: keep server data as the only source, render
  stable contextual loading copy, and retain retry/partial states.

## Accessibility Contract

- Document/landmark/heading order: `Communities` header, community heading,
  tablist, selected tab content, topic headings, composer heading, status/error.
- Keyboard/focus/Escape: real buttons/links, visible ECW focus ring, logical
  tab order, and no pointer-only topic interaction.
- Labels/errors/status: every action has an accessible label; invite and post
  fields have labels; dynamic write status is exposed through the existing
  status line and error alerts.
- Contrast/non-color/touch targets: use theme text/border roles and at least
  the existing 30px control floor; selected tabs use text and fill/border, not
  color alone.
- Reduced motion: no required animation; existing transitions collapse under
  the app's reduced-motion rule.

## Adopt

- Bulletin's distinct-place model, contextual composer, and local moderation
  concepts.

## Adapt

- Forum IA, many communities per person, computed thread grouping, and the
  existing Bluesky/ECW shell.

## Avoid

- Spatial sticky notes, public-feed semantics, unsupported member/reply claims,
  and new authority/domain assumptions.

## Prompt Contract

GOAL — Make a selected community feel like a coherent private forum inside Bluesky.
AUDIENCE — Signed-in Bluesky identities with visible community access.
TASK — Choose a community, scan topics, open one, start a topic or reply.
FLOW — Community switcher -> header/access -> tabs -> topic list/detail -> composer.
HEADER — Existing Communities shell plus selected community name and access.
MESSAGE — Conversations stay in this community and follow its rules.
FACTS — Render only returned community metadata and authorized record data.
CONTENT_INTEGRITY — Computed counts; no invented members, handles, or replies.
SECTION_ORDER — Switcher, header, tabs, forum content, composer, recovery.
CTA — New topic, with Reply in detail and stateful access actions.
TRUST — Plain-language visibility, provider-aware errors, and partial-read warnings.
ASSETS — Existing ALF/ECW/icons only; no external benchmark assets.
LAYOUT — Dense bordered forum column in the existing center shell.
RESPONSIVE — Compress switcher, retain tabs, replace list/detail on mobile.
STATES — Loading, empty, error, success, partial, permission.
PERFORMANCE — Text-first, no new media/font/dependency/motion budget.
ACCESSIBILITY — Semantic headings, tablist, real controls, focus, labels, contrast.
PRESERVE — Existing Space/PDS queries, membership, creation, and private write path.
EXCLUDE — New domain, public feed records, fake member totals, and protocol migration.
SUCCESS — A user can read and participate while understanding where the record goes.

## Success Checks

- Can a user explain the community's purpose and primary action within 5 seconds?
- Are every count, author label, timestamp, and reply relationship sourced from
  current data or omitted?
- Do loading, empty, error, partial, and permission states prevent false
  conclusions?
- Does mobile preserve the forum task order rather than simply shrinking the
  desktop arrangement?
- Do the existing theme, focus, forced-colors, and reduced-motion rules remain
  valid?
