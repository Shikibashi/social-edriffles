# Association Constitution

## Frozen principles

1. An individual block governs the bilateral relationship between the blocker and blocked account.
2. Direct interaction restrictions remain strong: block state must not be weakened by third-party presentation policy.
3. Unrelated viewers do not inherit another user's personal block preference. Public A/B records remain available to C when they otherwise exist and service policy permits them.
4. Public visibility never overrides deletion, takedown, account suspension, privacy, permissioned-data rules, threadgates, postgates, legal restrictions, or interaction authorization.
5. Individual ATProto block records are the canonical durable nonassociation primitive.
6. Continuously delegated block-list mutation is not a normal product primitive. Bulk mute may remain local and reversible; a future one-time block import would require explicit review.
7. Existing `app.bsky.graph.block`, `app.bsky.graph.listblock`, list, and list-item records remain interoperable. Compatibility does not require exposing continuous mass-block delegation as first-class UX.

## Moderation-list interpretation

For a governed local account, a moderation list is an attention input only when
the user subscribes through **Mute list**. A `listblock` record itself is inert
compatibility data in this fork, including when authored by a remote actor. The
client exposes **Mute list** and **Review accounts**. Review creates ordinary
individual block records only for the DIDs the user explicitly selects. The PDS
policy and migration ordering are specified in
`docs/MODERATION_LIST_POLICY.md`.

## Characterization evidence

The live A/B/C presentation matrix is in `docs/LIVE_BLOCK_PRESENTATION_MATRIX.md`. Safety-boundary evidence is in `artifacts/live-block-presentation-observations.json`.

- C retained public A/B thread roots and replies, author-feed records, ordinary search results, and quote search results.
- C's explicit following timeline retained public A/B posts. A and B timelines were empty in the fixture after their relationship state changed; this is recorded, not generalized beyond the fixture.
- Deleted records returned `RecordNotFound`/HTTP 404 for A, B, C, and anonymous callers.
- PDS record takedown removed record retrieval. PDS account takedown rejected login with `AccountTakedown`; AppView account-state refresh produced a placeholder profile and an empty author feed, preserving service-level removal.
- Threadgate omitted a probe reply that violated the gate. Postgate quote detachment left the quote record while removing the embedded view; detachment is not deletion.
- Existing list and list-item/listblock records remain indexed and readable as
  raw compatibility data. The first-party AppView does not expose effective
  `blockingByList`; the client exposes list mute and explicit member review,
  never continuous list blocking.
- Permissioned/private-data behavior was not simulated and remains explicitly untested.

## Decision boundary

The pairwise block architecture remains frozen for the already-characterized
presentation surfaces. Account takedown now refreshes from the PDS before
profile lookup, yielding a placeholder profile and empty author feed rather
than resurrecting public content. Listblock is explicitly inert in the
first-party data plane; permissioned-data support remains an interoperability
boundary and neither justifies weakening bilateral direct-block semantics.
