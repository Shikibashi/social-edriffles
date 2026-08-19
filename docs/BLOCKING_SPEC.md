# Blocking Specification

## Contract boundary

The characterization suite records historical behavior from a former pinned
read-provider implementation; it is not a runtime dependency and is not by
itself the desired fork policy. The reviewed candidate adds a first-party
official PDS and a direct-block/list-mute policy. Direct blocks remain
unchanged. `app.bsky.graph.listblock` remains readable raw compatibility data,
but is behaviorally inert for local and incoming interpretation. It is not a
block, an attention filter, or an interaction gate. See
`docs/MODERATION_LIST_POLICY.md` for the normative fork contract and the
report for tested-versus-untested boundaries.

## Three-account matrix
For each scenario, fixtures distinguish:

- **A:** blocker;
- **B:** blocked account;
- **C:** unrelated viewer.

Each row records whether content is visible, whether direct interaction is permitted, and the observed reason/context.

## Required surfaces
The matrix covers posts, threads, profiles, follows, replies, mentions,
notifications, quotes, feeds, block-list views, blocked-by views, and the
direct-interaction surfaces retained in the historical fixture. The initial
fixture uses the surfaces enumerated in `tests/fixtures/blocking-matrix.json`;
future provider refreshes must add newly discovered surfaces rather than
silently dropping rows.

## Separation rule
A characterization assertion must not be rewritten as a constitutional rule. Constitutional requirements live in `CONSTITUTION.md`; observed rows live in the fixture.

## Listblock data-plane rule

The AppView may continue indexing `list_block` rows and repository/CAR import
continues to accept the standard Lexicon. Effective relationship and block
existence queries exclude those rows; listblock-specific compatibility RPCs
return empty/no-block answers; hydration never populates `blockingByList` or
`blockedByList` from them. This applies to profiles, threads, replies,
mentions, notifications, quotes, author feeds, timelines, list feeds, search,
suggestions, embeds, and chat eligibility. Only `list_mute` can supply
delegated attention filtering, and only an individual `app.bsky.graph.block`
can supply a hard relationship.
