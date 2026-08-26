# Benchmark synthesis: Communities forum surface

## Source mode

`benchmark` — official Bulletin repository and source files, captured on
2026-08-26. The benchmark informs product principles and information
architecture; it is not a source of copied code, branding, or assets.

## Sources and evidence

| Source | Evidence captured | Use |
| --- | --- | --- |
| [Bulletin README](https://github.com/bluesky-social/bulletin/blob/main/README.md) | Bulletin is an example app built on ATProto Spaces; each user can create one board, followers can read, mutuals can post, and the owner can move or remove notes. | Adopt the distinct-place and local-permission model; adapt one-board into many communities. |
| [Bulletin components](https://github.com/bluesky-social/bulletin/tree/main/components) | The UI is organized around `BoardFinder`, `Composer`, `CreateBoardButton`, `ModerationButton`, and `SpatialBoard`. | Preserve contextual composition and local moderation as concepts; avoid the spatial canvas. |
| [Bulletin app routes](https://github.com/bluesky-social/bulletin/tree/main/app) | The app includes dedicated board and handle route surfaces rather than only a feed toggle. | Keep Communities as a navigable route with a selected community context. |
| [Bulletin `SpatialBoard.tsx`](https://github.com/bluesky-social/bulletin/blob/main/components/SpatialBoard.tsx) | The board renders movable notes, an empty state, and an in-board composer. | Explicitly avoid note rotation, drag-first interaction, and coordinate placement for this forum surface. |

## Missing evidence recorded

- The public Bulletin deployment was not used as an authenticated test target;
  the web capture could not safely open it in this environment.
- No independent mobile screenshot or mobile interaction trace was available
  from the reference. Mobile decisions below are therefore product-derived and
  will be verified on the local deployed Community route.
- No benchmark evidence supports member totals, reply totals, handles, or
  topic examples for the Radlib deployment. Those values are not copied into
  the product.

## Product Design Gate

- Exact Product Design plugin: `UNKNOWN` — no exact selector was available in
  the installed or available plugin listings.
- Adapter comparison: `NOT RUN`.
- Local implementation path: approved for this task using the repository's
  existing ALF and ECW systems.

## Adopt

- A community is a place a user navigates into.
- Composition is contextual to the current place.
- Permission and moderation are local to the place and expressed in plain
  language.

## Adapt

- Replace Bulletin's person-to-one-board model with person-to-many communities.
- Replace spatial notes with topic rows, a topic detail view, and reply grouping
  from the existing private-post `reply` field.
- Keep the existing Bluesky shell, account identity, and ALF controls rather
  than introducing a separate application chrome.

## Avoid

- Sticky-note rotation, corkboard decoration, drag-to-compose, and coordinate
  placement.
- Discord-style live-room chrome, subreddit-style public ranking language, or a
  timeline-only presentation.
- Claims of member totals or threaded data that the current Space read API did
  not return.
