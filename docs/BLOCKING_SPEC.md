# Blocking Specification

## Contract boundary
The characterization suite records the pinned AppViewLite behavior at commit `75f78e8e098c05f52821e836832205050c0f539e`; it is not a desired-future-behavior test. Production semantics remain unchanged in PR-00/PR-01.

## Three-account matrix
For each scenario, fixtures distinguish:

- **A:** blocker;
- **B:** blocked account;
- **C:** unrelated viewer.

Each row records whether content is visible, whether direct interaction is permitted, and the observed reason/context.

## Required surfaces
The matrix covers posts, threads, profiles, follows, replies, mentions, notifications, quotes, feeds, block-list views, blocked-by views, and every additional direct-interaction surface discovered in the pinned AppViewLite source. The initial fixture uses the surfaces enumerated in `tests/fixtures/blocking-matrix.json`; future upstream refreshes must add newly discovered surfaces rather than silently dropping rows.

## Separation rule
A characterization assertion must not be rewritten as a constitutional rule. Constitutional requirements live in `CONSTITUTION.md`; observed rows live in the fixture.
