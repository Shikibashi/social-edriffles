# Runtime Slice Status

## Imported baselines

- `upstream/AppViewLite` is checked out at `75f78e8e098c05f52821e836832205050c0f539e`.
- `upstream/social-app` is checked out at `1f5c698165c922e707833809902ee959e9824f00`.

## Characterization

`tests/test_appviewlite_characterization.py` anchors the A/B/C matrix to real pinned AppViewLite source paths and verifies the pairwise relationship core considers direct and inverse relationships while preserving unrelated viewers. Runtime .NET endpoint tests remain pending because the current environment has no `dotnet` executable.

## Pairwise relationship boundary

AppViewLite's relationship core was explicitly named `UsersHavePairwiseBlockRelationshipCore`. It evaluates `(a,b)` and `(b,a)` for the requesting context and returns direct, inverse, mutual, or no relationship. This is a naming/contract clarification of the existing behavior, not a nuclear-block semantic rewrite.

## Local feed sovereignty

`upstream/social-app/src/lib/feed-sovereignty/profile.ts` provides local candidate scoring, author caps, exploration floors, explicit portable profile JSON, and AES-GCM/PBKDF2 encrypted backup using platform cryptography. Its focused Jest suite covers author caps, exploration, profile round-trip, and encryption.

## Baseline verification

- `upstream/social-app/src/state/preferences/local-feed.tsx` persists an opt-in local-reranking toggle and explicit preferences on-device. Following-feed settings expose the toggle; feed rendering applies local slice reranking and displays deterministic “Why this post?” reasons.
- Social-app dependencies install with `pnpm install --frozen-lockfile`.
- `pnpm typecheck:web` passes.
- Focused feed Jest suite passes (3 tests).
- Root contract and characterization suite passes (7 tests).
- AppViewLite baseline build passes with the isolated .NET 10 SDK (`/tmp/dotnet10/dotnet build upstream/AppViewLite/src/AppViewLite.slnx --no-restore`), with 8 existing compiler warnings and 0 errors.
