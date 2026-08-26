# Brief: Communities forum surface

## Request

Turn the existing Communities board from a sticky-note presentation into a
classic forum embedded in Bluesky. Use Bulletin as inspiration for the feeling
of entering a distinct ATProto/Spaces place, but do not copy its spatial note
board or its one-board-per-person product model.

## Product direction

The mental model is:

```text
ordinary Bluesky identity
  -> enter a community space
  -> read local topics
  -> open a topic and its replies
  -> start a topic or reply in that context
```

The target hierarchy is `person -> many communities -> threads -> posts`.
Community-local membership, access, content, and moderation remain the source
of truth. A dedicated community authority DID and authority transfer remain
future protocol work.

## Scope

- Redesign the existing `CommunityBoard` route and preserve its current
  community discovery, creation, membership, invite, leave, and private Space
  record transport.
- Present top-level private-post records as forum topics and records carrying a
  supported `reply.root.uri` reference as replies. Computed reply counts must be
  derived from the records actually read.
- Add local `Threads`, `Latest`, `Members`, and `About` views without creating a
  second route or a second data plane.
- Keep the public origin at `https://social.edriffles.us` and the PDS at
  `https://pds.edriffles.us`. `radlib.org` and a separate registrable domain
  are out of scope.

## Non-goals

- No new registrable domain, DNS authority, production credential, Qdrant
  change, Relay/AppView behavior, or PDS protocol migration.
- No fabricated member directory or public social graph.
- No replacement of the existing private Space transport with public
  `app.bsky.feed.post` records.
