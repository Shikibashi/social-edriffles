# Spaces Alpha Integration

Status: `ALPHA_OPT_IN` on `codex/spaces-alpha-integration`.

This branch uses the upstream ATProto `permissioned-data` branch as the PDS
base and carries the fork's protected-account/community policy above the
standard Spaces data plane. The integration is deliberately opt-in: it is a
characterized implementation slice, not a production activation or owner
acceptance receipt.

## Pinned sources

| Component | Base | Reviewed checkout | Role |
|---|---|---|---|
| PDS | `bluesky-social/atproto` `permissioned-data` at `89deb9fac20e56fa2a262fe9746ed52bc1095ba` | `upstream/atproto-pds` at `5f413a8e50433c685c95c9d7209387a903b1d2f3` | Spaces protocol, DPoP credentials, ActorStore data plane, and fork product control API |
| Client | `bluesky-social/social-app` at `1f5c698165c922e707833809902ee959e9824f00` | `upstream/social-app` at `5a86dcd989d45a62c2586fd421579ee5c9c05eb5` | Opt-in standard Space record/blob adapter with legacy fallback |

The machine-readable copies are `upstream-pins.json` and
`artifacts/upstream-baseline.json`. The root checkout and both submodule
checkouts are local branch state; nothing in this change authorizes a push,
deployment, or moving-head rebase.

## Boundary

The standard Spaces APIs own private transport and repository data:

- `com.atproto.space.*` for Space-scoped records, blobs, credentials, and
  repository discovery;
- `com.atproto.simplespace.*` for Space creation, policy, and membership;
- the PDS `@atproto/space` implementation for DPoP-bound credentials and
  Space synchronization primitives.

`org.radlib.private.*` remains only for the higher-level protected-account and
community control plane: visibility, follow approval/revocation, community
metadata, invites, membership policy, and bans. Its SQLite state is policy
state, not the authority for new Space records or blobs. The old custom
record/blob/feed/sync transport is not mounted as a second active data plane;
existing legacy tables are retained for a non-destructive migration path.

## Feature gates

PDS deployments using this slice must explicitly set:

```text
PDS_SPACES_ALPHA_ENABLED=true
PDS_LEGACY_RADLIB_PRIVATE_ENABLED=true
PDS_PROTECTED_ACCOUNTS_ENABLED=true
PDS_COMMUNITIES_ENABLED=true
```

The client defaults to the standard Space adapter only when
`EXPO_PUBLIC_SPACES_ALPHA_ENABLED=1`. Otherwise
`EXPO_PUBLIC_LEGACY_RADLIB_PRIVATE_ENABLED` controls the old client adapter,
and setting it to `0` fails closed. On the PDS, the legacy flag enables only
the preserved `org.radlib.private.*` product-control compatibility API. It
does not restore the removed custom record/blob/feed/sync endpoints; those
remain replaced by standard Spaces.

## Evidence and open gates

Verified in this checkout:

- root contract and pinned-tree checks, after metadata update;
- social-app web typecheck;
- focused social-app permissioned-data and Spaces RPC unit tests;
- PDS code generation/build and the existing focused Spaces test files, when
  the local dependency checkout permits them.

Not established by this branch:

- native Hermes/Metro WebCrypto compatibility;
- a client CAR/sync consumer or incremental multi-PDS UI path;
- Radlib-specific multi-PDS acceptance across separate PDS processes;
- immediate invalidation of already-issued Space credentials after membership
  removal;
- production fielding, deployment, or owner acceptance.

These are explicit follow-up gates. They must not be inferred from a passing
typecheck, fixture, or local PDS build.
