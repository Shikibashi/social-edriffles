# Implementation log: Communities forum surface

## Gate record

- Date: 2026-08-26
- Reference mode: benchmark
- Product Design plugin gate: `UNKNOWN`; exact selector was not present in the
  installed/available plugin listings.
- Adapter comparison: `NOT RUN`.
- Reference desktop evidence: official repository/source capture available.
- Reference mobile evidence: unavailable; local deployed mobile render is the
  verification source.
- Direction variants: not rendered. The user-provided direction explicitly
  selected Bulletin's place model plus forum IA, so variant renders would add
  exploration without resolving a live decision.

## Decisions

- Keep the existing `CommunityBoard` route and current PDS/Space queries.
- Treat top-level private-post records as topics and group records with a
  matching `reply.root.uri` as replies. This makes the UI forum-like while the
  current backend remains unchanged.
- Show a transparent Members tab instead of inventing a member directory or
  total that the current API does not provide.
- Use runtime ALF theme roles rather than hard-coded light-only colors so the
  redesign follows existing ECW dark, dim, contrast, forced-color, and reduced-
  motion behavior.

## Planned verification

1. Validate the Experience Contract with the bundled validator.
2. Run focused social-app type/tests and the root contract validator.
3. Build the production web bundle with the existing `social.edriffles.us`
   environment and deploy to Pages.
4. Verify the live route in the ChatGPT desktop in-app browser at desktop and
   narrow widths without entering credentials.
5. Commit only reviewed source/design changes; keep automatic conversation and
   memory logs unstaged.

## Known boundary

The current Space control API does not return a member directory or public
profile metadata for fanout writer DIDs. The implementation must keep those
limitations visible rather than implying the forum has richer data than the
transport supplied.
