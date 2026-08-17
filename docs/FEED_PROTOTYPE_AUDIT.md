# Local Feed Prototype Audit

Status: audit of the existing opt-in prototype; this is not Balanced v1.

## Confirmed findings

| ID | Severity | Finding | Evidence |
|---|---|---|---|
| F-01 | P1 | `FeedPreferences.familiarity` is declared and persisted but never participates in `scoreCandidate`. | `upstream/social-app/src/lib/feed-sovereignty/profile.ts:1-8,37-46` |
| F-02 | P1 | Following integration hardcodes `networkRelevance: 0.5`. | `upstream/social-app/src/view/com/posts/PostFeed.tsx:443-449` |
| F-03 | P1 | Following integration hardcodes `integrityWeight: 1`. | `PostFeed.tsx:444-448` |
| F-04 | P1 | Following integration hardcodes `seen: false`; local action history is not consulted. | `PostFeed.tsx:447-448`; `src/state/userActionHistory.ts` |
| F-05 | P1 | Candidate topic is not populated by Following integration. | `PostFeed.tsx:436-449` constructs no `topic` field. |
| F-06 | P2 | Conversation activity is boolean (`replyCount ? 1 : 0`) rather than normalized. | `PostFeed.tsx:445,914` |
| F-07 | P1 | Reranking is applied independently to each fetched page. | `PostFeed.tsx:433-457` maps `data.pages` and calls `rerankLocally` per page. |
| F-08 | P1 | The exploration pool is therefore limited to each already-fetched page, not a wider-network candidate pool. | `PostFeed.tsx:435-457`; no retrieval expansion is present. |
| F-09 | P1 | “Why this post?” recomputes an approximate candidate and does not consume a ranking trace. | `PostFeed.tsx:907-920`; `profile.ts:95-103` |
| F-10 | P1 | Explanation uses `freshness: 0.5`, while ranking uses indexedAt-derived exponential freshness. | `PostFeed.tsx:439-443,909-917` |
| F-11 | P1 | Encrypted export has no decrypt/import workflow. | `profile.ts:105-120`; only plaintext `importPortableProfile` exists. |
| F-12 | P1 | Portable import validates schema and languages only; ranges, sizes, dates, topics, modules, and constitutional fields are not validated. | `profile.ts:87-93` |
| F-13 | P2 | UI exposes a single enabled toggle rather than two-level presets plus advanced controls. | `src/state/preferences/local-feed.tsx`; `src/view/com/feeds/FeedPage.tsx` |

## Regression coverage added by the existing prototype

The current Jest suite covers author caps, exploration floor, plaintext profile round-trip, encryption availability, and deterministic explanation output. It does not yet encode the defects above as corrected behavior; changing them belongs to a separate implementation slice.

## Scope decision

No scoring or UI redesign is made in this audit. The prototype remains opt-in and local-only. The next slice must first define a ranking-trace contract, retrieval boundary, validation limits, and decrypt/import threat model before changing behavior.
