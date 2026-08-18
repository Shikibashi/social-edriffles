# Balanced v1

Balanced v1 is a replaceable, local/client-side ranking algorithm under the Attention Constitution. It consumes validated Candidate Protocol v1 batches and Portable Personalization v1 preferences. It does not moderate, classify ideology, mutate relationships, or replace chronological access.

## Candidate-source policy

Pools are explicit and bounded: followed network, graph-near discovery, broader exploration, explicit-interest candidates, and new/low-exposure candidates. `composeCandidatePools` records source composition and applies per-source limits before ranking.

## Formula and bounds

For candidate `c`, all features are clamped to documented bounds:

```
score(c) =
  .20 freshness
+ .16 graphProximity
+ .06 log1p(engagementCount)/log1p(1,000,000)
+ .22 explicitInterest
+ .10 inferredInterest
+ .16 explicitFeedback
+ .10 novelty
+ .08 exploration
+ .08 integrity
- .18 harassmentAmplificationRisk
- authorConcentrationPenalty
- duplicateConcentrationPenalty
```

Explicit author/topic controls and More/Less interaction weights outrank inferred interests and generic features. Missing features are unknown and use bounded neutral defaults; they are not treated as negative evidence. Popularity is logarithmic and cannot dominate. Integrity and harassment amplification risk remain separate from moderation, authenticity, ideology, and viewpoint.

Author caps, duplicate suppression, popularity diminishing returns, exploration allocation, and concentration dampening are soft ranking penalties. Risk can incorporate rapid multi-account attention, quote/reply concentration, forwarding bursts, duplicate-account flooding, keyword/tag stuffing, interest bait, creator gaming, recommender SEO, and cheap Sybil volume when trustworthy features exist. Breaking-news bursts are evaluated as a separate regime and do not automatically imply coordinated manipulation.

## Explainability and determinism

Every result includes a structured trace with bounded features, weighted contributions, penalties, score, source category, and a faithful user-readable reason. The same validated batch, preference snapshot, algorithm manifest, and clock produces the same order; URI is the final deterministic tie-breaker.

Generic ATProto records remain eligible when sufficient metadata exists. Native short posts receive no structural privilege solely because they expose richer engagement telemetry.
