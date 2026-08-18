# Attention Constitution v1

**Status:** Frozen as an architectural contract. This document governs systems that allocate, order, prioritize, suppress, or pace user attention. It does not change the frozen Association Constitution, Service Constitution, or Portable Personalization v1.

## 1. Scope and surface classification

| Surface | Constitutional classification | Default authority | Chronological/reversible path |
|---|---|---|---|
| Home/following feed | Attention ordering | User-selected feed and local preferences | Following/chronological remains available |
| Custom/external/experimental feed | Delegated ordering | Named feed provider under explicit selection | Switch/remove feed; chronological where meaningful |
| Account recommendations | Discovery ordering | Client/provider proposal | Dismiss/refresh; no durable action without user confirmation |
| Search ranking | Retrieval ordering | Search provider proposal | Query results remain inspectable; provider visible |
| Trending | Popularity/discovery ordering | Named service proposal | Not an authenticity or moderation verdict |
| Feed directories and Starter Pack discovery | Discovery ordering | Directory/pack publisher proposal | User chooses whether to subscribe |
| Notifications | Attention priority | Client and notification service | Chronological/activity views remain available where supported |
| Likes/reposts/follower counts | Social-proof presentation | Service-provided metrics | Metrics are not trust, authenticity, moderation, or ranking truth |
| Future recommendation surfaces | Attention ordering | Must be classified before release | Must provide an exit and authority declaration |

An attention surface may propose an ordering or visibility allocation; it may not silently perform a durable interpersonal action, alter moderation state, or impersonate user authority.

## 2. Core principles

1. **User attention authority:** the user controls what is shown, at what pace, and through which provider.
2. **Proposal, not ownership:** services propose orderings; no provider owns the user's attention model.
3. **Replaceability:** algorithms, providers, and client implementations are replaceable without DID, PDS, graph, or Portable Personalization migration.
4. **Chronological access:** meaningful chronological/following access remains available.
5. **Inspectable actors:** algorithm/provider identity, service DID, version, and objective are visible.
6. **Explicit objectives:** ranking objectives and material changes are named; raw engagement alone is not a sufficient default objective.
7. **Portable personalization:** Portable Personalization v1 remains client-owned, exportable, resettable, and unchanged by provider choice.
8. **User over inference:** explicit More/Less, interests, and controls override inferred interests and engagement signals.
9. **Revocable delegation:** delegated attention authority is narrow, visible, revocable, and cannot grant PDS write authority.
10. **Deliberate durable actions:** follows, likes, reposts, replies, blocks, subscriptions, and other durable association changes require deliberate user action.
11. **Moderation separation:** attention ordering, personal filtering, labeler decisions, operator enforcement, and moderation status are separate authorities.
12. **Conceptual separation:** authenticity, trustworthiness, ranking utility, moderation status, and reputation are distinct and must not be presented as interchangeable.

## 3. Algorithmic competition

- **Following/chronological** is the baseline exit and must not be hidden behind a provider's ranking.
- **Balanced** is a future named algorithm profile, not implemented or implied by this v1 constitution. It must declare objective, version, and controls before release.
- **External and experimental feeds** are separately named providers/algorithms. Material objective changes require explicit opt-in or re-selection.
- **Directories and user-created rankers** may propose feeds, but directory inclusion is not endorsement and user subscription is not durable social action.
- Feed switching changes attention ordering only; it does not change identity, PDS, graph, moderation authority, or local personalization state.

## 4. Transparency and explanation scopes

Every selected ordering exposes: provider name, provider DID/service identity, algorithm name, algorithm version, manifest/version hash when available, and ranking objective. A material algorithm change increments the declared version or manifest hash.

“Why this post?” must be derived from the actual ranking trace, using comprehensible factors such as chronological recency, explicit interest, selected feed rule, exploration slot, or duplicate suppression. It must not claim a factor that did not affect placement.

- **Public scope:** bounded, user-readable objective and factor categories; never disclose private profiles, anti-abuse thresholds, or another person's private data.
- **Audit scope:** authorized review may inspect signed manifests, deterministic traces, policy versions, and aggregate outcome evidence sufficient to reproduce a decision.
- **Confidential scope:** anti-abuse secrets, private safety signals, rate limits, and abuse-detection evidence may remain confidential; confidentiality cannot be used to invent a false public explanation.

## 5. User control and personalization

More/Less feedback, explicit interests, inferred-interest inspection/removal, discovery/variety/freshness controls, local-first personalization, and Quiet Metrics are user controls. Quiet Metrics suppress social-proof counts and attention pressure without asserting that the underlying metric is false.

Feed and provider switches are explicit. Portable Personalization v1 settings/profile/archive exports, imports, resets, and encrypted backups remain valid across switching. Reset learned state preserves explicit settings; deleting personalization does not delete social graph records. A provider receives only request data required for its service, not the complete local profile.

## 6. Concentration and dogpile controls

Author caps, duplicate suppression, diminishing popularity returns, exploration budgets, concentration-of-attention detection, and harassment/dogpile amplification controls are constitutionally permitted ranking/allocation constraints. They must be explainable at the appropriate scope, avoid viewpoint quotas, and remain distinct from moderation or authenticity judgments. A control may reduce amplification without declaring content false or impermissible.

## 7. Accessibility and pace sovereignty

Attention surfaces SHOULD support manual refresh, pause-new-posts, finite-page or no-infinite-scroll modes, reduced motion, reduced-information modes, keyboard navigation, screen-reader semantics, autoplay controls, and user-controlled refresh pace. Accessibility settings must not silently alter durable account or interpersonal state.

## 8. Delegated attention authority

| Operation | Authority class | Boundaries |
|---|---|---|
| One-shot recommendation/advice | Advisory | No persistence or durable mutation without confirmation |
| Continuous feed/ranking subscription | Delegated policy | Named provider, explicit selection, revocable, provider-visible |
| Local reversible filter/reranker | Local user policy | Account/device scoped, inspectable, resettable/exportable |
| Like/follow/repost/reply/block/subscription | Durable account mutation | Deliberate confirmation and PDS/account authority; never implied by ranking |

## 9. Emergency authority

Emergency attention changes require an incident identifier, named operator, bounded scope and duration, explicit start time, audit entry, expiry, rollback path, and after-action documentation. Emergency authority cannot mutate identity, PDS records, blocks, or moderation status merely by changing ordering. Expired emergency policies stop applying automatically.

## 10. Governance and change classes

- **Implementation patch:** no user-visible objective or authority change; ordinary review and tests.
- **Algorithm minor revision:** material ordering behavior within the declared objective; increments algorithm version/manifest and requires user-visible notice where practical.
- **Constitutional-major revision:** changes authority boundaries, transparency guarantees, durable-action rules, moderation separation, or exits; requires a new constitutional version and explicit project approval.
- **User-consent-triggering change:** new provider delegation, new remote signal, new durable action, materially changed objective, or reduced exit/control; requires explicit user choice and cannot be silently enabled.

Attention controls allocate exposure; they do not decide whose viewpoint is worthy. Association and Service Constitution boundaries remain authoritative.
