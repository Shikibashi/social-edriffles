# Personalization Data Policy (v1)

Personalization is client-owned local state. AppViews and feed providers receive request parameters and records needed for a feed request, never the complete local profile.

| Signal | Source | Local? | Sent remotely? | Retention | Export level | Reset |
|---|---|---:|---:|---|---|---|
| requestMore/requestLess | Explicit user action | Yes | No | Until deleted | settings (explicit preference) | feed preferences / delete |
| likes, reposts, replies, follows | Account records and local interpretation | No raw local history | Only normal ATProto action/request | Provider/PDS policy | never as raw history | delete local profile does not delete records |
| clicks, impressions, seen | Client feed interaction | Yes | No | Ephemeral/optional archive | archive only | learned/delete |
| passive dwell time | Not collected in v1 | No | No | None | None | None |
| topics | Explicit or locally inferred | Yes | No complete profile | Profile until reset | settings if explicit; profile if inferred | learned or feed reset |
| author/source affinity | Local inference | Yes | No | Profile until reset | profile | learned/delete |
| embeddings | Not collected by v1 | No | No | None | None | None |
| candidate history | Local dedupe window | Yes | No | Ephemeral; archive optional | archive | learned/delete |
| ranking traces | Local diagnostics | Yes | No | Ephemeral; archive optional | archive | learned/delete |

Explicit feedback has higher authority than inferred engagement. Negative `requestLess` feedback remains local. Exports reject credential-like fields and never contain OAuth, access, refresh, service-auth tokens, passwords, or app passwords.

## Portability levels

- **settings**: explicit preferences, presets, interests, quiet mode, and compatible service selections; no behavioral history.
- **profile**: settings plus derived topics, author/source/language affinities, interaction weights, and exploration history; no raw interaction log.
- **archive**: profile plus bounded local continuity state (seen/dedupe/pagination/traces). This is an advanced backup, not ordinary preference export.

## Storage and deletion

The mobile/web client stores account-scoped state under AsyncStorage keys prefixed `PERSONALIZATION_V1:<account DID>`. AsyncStorage persistence is not represented as cryptographic secure deletion; platform backups, snapshots, browser/device eviction, and filesystem remnants may retain data. Delete removes the current key and learned state; it cannot promise erasure from backups. Provider switching changes service configuration only and does not remove this state.
