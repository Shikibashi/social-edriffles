# Radical-Liberal Personal Content Filter Research

**Status:** research-informed implementation is now present in the client and
in the standalone service lane. Semantic advocacy classification remains
deferred; the current behavior is explicitly rules-only and opt-in.

> Implementation status update (2026-08-19): the bundled term-pack design
> described below is historical research, not the active product behavior.
> The client and filtered-feed service now keep legacy pack fields only for
> import compatibility and evaluate custom terms supplied by the current
> account/deployment. No political or owner-specific vocabulary is shipped by
> the production ranking/filtering path.

## Question

How can a user-selected feed preference reliably reduce posts about or
advocating communist, Marxist-authoritarian, authoritarian-left, or
progressive politics without turning the client into a mandatory political
moderator?

The answer must preserve the fork's political-neutrality rule: the filter is a
private attention preference chosen by the user. It is not a constitutional
ranking rule, a universal takedown, a direct block, or an assertion that a
classifier's political judgment is objective.

## Current implementation finding

The first production-quality rules-only slice is now implemented:

- `upstream/social-app/src/lib/feed-sovereignty/content-filter.ts` defines the
  versioned portable policy, Unicode-aware exact matching, contextual packs,
  strict standalone `progressive` mode, and hard-exclusion trace.
- `PostFeed` applies the local policy after hydration to all feed candidates;
  it does not mutate follows, blocks, mutes, or listblocks. A content-only
  policy filters without taking ownership of provider ordering.
- Explicit More/Less ranking signals are evaluated only for surviving
  candidates. A hard content exclusion cannot be resurrected by More.
- The policy remains disabled by default and strict standalone matching remains
  off by default. The settings UI labels the false-positive tradeoff and
  exposes custom terms and author DIDs.
- `services/radlib-filtered-feed/` provides a separate standard feed-skeleton
  service with bounded SQLite storage, contextual/strict algorithms, explicit
  health, and a decoded `subscribeRepos` ingestion boundary. It does not claim
  live firehose coverage until an operator supplies the connection and verifier.

The implementation still examines post text rather than inferring an author's
political identity. Semantic advocacy classification is intentionally deferred
to a local model adapter rather than silently approximated by lexical rules.

## What the protocol already provides

### 1. Standard personal word mutes

The standard `app.bsky.actor.defs#mutedWordsPref` schema supports a user-owned
list of muted words, targets (`content` or `tag`), an actor scope (`all` or
`exclude-following`), and expiration. This is the best interoperability layer
for exact phrase/term filtering, but it cannot reliably distinguish advocacy
from quotation, criticism, journalism, or historical discussion.

Source: [the official actor definitions](https://raw.githubusercontent.com/bluesky-social/atproto/main/lexicons/app/bsky/actor/defs.json),
especially `mutedWord` and `mutedWordsPref`.

### 2. User-selected labelers

ATProto labels are self-authenticated metadata with a source DID, subject URI,
and short label value. Clients can request selected labelers through
`atproto-accept-labelers`, and users can map a label to hide, warn, show, or
ignore. A private political-content labeler could therefore provide labels
without creating blocks or deleting records.

Sources: [ATProto moderation](https://atproto.com/guides/moderation/),
[the labels specification](https://atproto.com/specs/label), and
[Bluesky labels and moderation](https://bsky.network/docs/advanced-guides/moderation/).

This is appropriate only when the labeler is clearly identified, explicitly
selected, and treated as a delegated judgment provider. It must not be shown as
“the platform decided.”

### 3. User-selected feed generators

An ATProto feed generator can subscribe to `com.atproto.sync.subscribeRepos`,
index a candidate pool, apply its own algorithm, and return post-URI skeletons
through `app.bsky.feed.getFeedSkeleton`. It can host a dedicated personal
filter feed, but a per-user algorithm may receive an authenticated user JWT and
requires an explicit provider/privacy choice.

Source: the official [ATProto feed-generator starter kit](https://github.com/bluesky-social/feed-generator).

This is the correct long-term path for broad candidate coverage. The current
client overlay only filters hydrated posts already returned by the selected
feed; it cannot guarantee suppression outside that returned page.

## Research result: use four separate controls

The UI should not collapse four different decisions into one ideological
switch:

| Control | What it does | Authority | Recommended default |
|---|---|---|---|
| Hide terms | Exact normalized words/phrases and selected variants | User's local policy | Off until selected |
| Hide political advocacy | Local classifier hides high-confidence advocacy; uncertain/critical/reporting cases remain visible or warn | User's local policy + local model | Off until selected |
| Hide authors | Explicit DID or private list mute | User's deliberate association/attention action | Empty |
| Hide label | Maps a named labeler/category to hide/warn/ignore | User-delegated labeler policy | Unconfigured |

The user can therefore ask for “no mention of these words,” “no advocacy,”
“no posts from this author,” or “use this labeler's judgment” without the
system pretending those are the same operation.

## Recommended implementation

### Phase A — make exact filtering reliable

Create a versioned, portable `contentFilterPolicy` separate from ranking
weights:

```ts
type ContentFilterPolicy = {
  version: 1
  strictProgressive: boolean
  semanticMode: 'rules-only'
  enabled: boolean
  termPacks: Array<'communist-authoritarian' | 'progressive-politics'>
  customTerms: string[]
  actorTarget: 'all'
  excludedAuthorDids: string[]
  hardExclude: true
}
```

Use Unicode-aware normalization and explicit inflection/phrase entries rather
than unrestricted substring matching. The initial pack should cover, at
minimum:

- `communism`, `communist`, `communists`;
- `marxism`, `marxist`, `marxists`, `marxism-leninism`, and
  `marxist-leninist`;
- `maoism`/`maoist`, `trotskyism`/`trotskyist`;
- `authoritarian left`, `authoritarian leftist`, and
  `authoritarian socialism`;
- the existing contextual progressive-politics phrases;
- an explicitly labeled strict option for `progressive`/`progressives`, with a
  warning that it will catch non-political uses such as “progressive web app”
  and “progressive rock.”

`hardExclude` must outrank inferred interest, engagement, exploration, and a
generic More signal. If the user deliberately chooses both “show this post”
and a hard category exclusion, the UI must expose the conflict and require the
user to choose; it must not silently override the exclusion.

### Phase B — add semantic advocacy filtering locally

Lexical matching cannot answer whether a post supports, criticizes, quotes, or
reports on a political movement. Add a local classifier adapter with explicit
multi-label output:

```ts
type LocalContentJudgment = {
  category:
    | 'communist-authoritarian-advocacy'
    | 'marxist-authoritarian-advocacy'
    | 'progressive-politics-advocacy'
    | 'political-mention'
    | 'critique-or-reporting'
    | 'uncertain'
  confidence: number
  modelId: string
  modelVersion: string
}
```

Policy should be conservative:

- high-confidence advocacy → hide only when the user selected strict hide;
- medium confidence or missing context → warn/review;
- criticism, quotation, historical discussion, and uncertainty → keep visible
  by default;
- never infer that an author belongs to an ideology from one post;
- author-level suppression requires an explicit DID/list action or repeated
  high-confidence evidence followed by user confirmation.

This should run on-device or against a user-controlled local service whenever
possible. The provider should receive neither the user's full preference
profile nor classifier results unless the user explicitly selects a remote
provider.

The research supports this caution. Political stance detection is context
dependent, and annotation context affects noise and disagreement ([ConStance,
EMNLP 2017](https://aclanthology.org/D17-1116/); [Stance Detection with
Background Knowledge, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.972/)).
Political ideology in training data can also distort ordinary topic relevance
([Guo et al., COLING 2020](https://aclanthology.org/2020.coling-main.428/)).
Those findings argue for a user-controlled, calibrated filter—not a hidden
global ideology classifier.

### Phase C — broaden the candidate pool with a personal feed generator

After the local policy is deterministic and inspectable, implement a separate
feed generator for a broad firehose/indexed candidate pool. It should:

1. ingest repository events;
2. apply direct blocks, incoming hard boundaries, labeler policy, and the
   user's selected content filter;
3. rank remaining candidates with explicit preference precedence;
4. return a skeleton with provider identity, version, and truthful reason data;
5. preserve Following and ordinary custom feeds as alternatives.

This gives the user a real “Filtered Following” choice without claiming that
the filter controls search, profiles, or every other view. A self-hosted
instance is the strongest meaningful-exit option; a remote instance must be
named as a separate provider.

## Required regression tests

1. Default/disabled policy leaves Following unchanged.
2. Singular and plural term variants match; `progressive web` and
   `progressive rock` remain visible under the contextual pack.
3. Strict progressive mode is explicitly selected and visibly labeled.
4. Hard exclusions beat passive/inferred ranking and exploration.
5. A positive More preference cannot silently override a hard exclusion.
6. Explicit author exclusion changes attention only and creates no block.
7. Labeler hide/warn/ignore behavior is scoped to the selected labeler DID.
8. Classifier output is traceable by model/version/confidence and never shown
   as objective platform fact.
9. Quotation, criticism, reporting, and uncertain classifier fixtures do not
   get silently hard-hidden by the conservative default.
10. Export/import includes the policy but no credentials, recovery material,
    or private keys.
11. Following, search, profile, and custom feed behavior are tested
    separately; the policy's scope is never implied to be universal.

## Decision

The narrowest safe next implementation is **Phase A plus the conflict and
fidelity tests**. Phase B is needed for “advocacy” rather than mere word
filtering. Phase C is needed for broad, provider-independent coverage. None of
the phases should become a mandatory political rule or a durable relationship
mutation.

The current acceptance state therefore remains pending/blocked until the owner
decides whether they want term-only filtering, semantic advocacy filtering, or
both, and whether the classifier should run locally or through a selected
provider.
