# Spaces alignment acceptance

Status: `ALPHA-GATED / OWNER ACCEPTANCE PENDING`

Audited: 2026-08-23

This matrix records evidence from the fork's source-built test lane and the
current browser smoke check. It does not authorize production use of the alpha
PDS or claim E2EE.

## Matrix

| ID | Capability | Result | Evidence / remaining condition |
|---|---|---|---|
| A0 | Reviewed source pins match submodule gitlinks | `PASS` | Root pins and gitlinks match PDS `d906e959dabcd017b4a0fa840e755d3a5f5d77d8` and client `64f85eed85ee0eff36b177944349339a76051119`; `check_upstream.py --fast` is green. |
| A1 | Spaces is the only normal private record/blob/feed/sync transport | `PASS` | Control-mode store omits legacy payload tables; no active legacy content routes; client uses Space transport when alpha is enabled. |
| A2 | Radlib is policy/governance/discovery/moderation only | `PASS` | Control tables and routes contain policy state; private bodies and blob bytes remain in Spaces. |
| A3 | Protected account toggles without the legacy flag | `PASS` | Two-PDS PDS test deletes `PDS_LEGACY_RADLIB_PRIVATE_ENABLED` and exercises visibility plus Space write. |
| A4 | Protected block revokes access | `PASS` | Canonical graph block from a remote PDS is detected; membership is removed; fresh credential exchange fails. |
| A5 | Owner and remote member write from separate PDSes | `PASS` | `tests/radlib-spaces.test.ts` writes from two PDS repos and reads both through DPoP credentials. |
| A6 | Community reads all writers and pages | `PASS (fanout)` | Client exhausts `listRepos` and per-writer `listRecords`, preserves author provenance, and reports partial writers. Opaque aggregate UI cursor remains P2. |
| A7 | Revocation fails closed | `PASS FOR NEW CREDENTIALS` | Leave and ban remove membership and reject new credentials. Already-issued alpha credentials may survive until expiry. |
| A8 | Public transition preserves private history | `PASS` | Store test proves the account Space remains after protected → public. No automatic publication or destruction exists. |
| A9 | Private media/blob bytes stay off public paths | `PASS (local canary)` | Space `getBlob` succeeds; ordinary `sync.getBlob` rejects Space-only references; private/no-store headers are set. |
| A10 | Private sync/index is direct and rebuildable | `PASS (minimal)` | Cursor/sink abstraction reconciles `listRepoOps` and persists only positions. Server-side durable private AppView is future work. |
| A11 | Private notification transport does not leak | `PARTIAL` | Space register/unregister RPCs are generated and wrapped; no browser notification service or notification index is deployed. |
| A12 | Custom records use reviewed/generated Lexicons | `PASS WITH COMPATIBILITY NOTE` | PDS Lexicons are generated; the client generates the same Space source set after removing unsupported pinned-runtime format validators at the boundary. |
| A13 | Alpha Docker lane is isolated | `PASS (documented)` | `docs/SPACES_ALPHA_INTEGRATION.md` specifies disposable identities, loopback binding, separate volume, health, and describe-server checks. |
| A14 | Browser UI supports accepted paths | `PARTIAL (production auth recovery)` | Cloudflare Pages serves the new production bundle and the browser shell loads, but the current persisted production session still receives `InvalidToken` from the migrated PDS; the bundle now refreshes and retries body-less PDS reads, resolves a deep-linked board through its authority when local discovery is unavailable, and a fresh sign-in is still required to complete the live private-board check. |
| A15 | Owner accepts migration and residual alpha risk | `PENDING` | Requires an owner walkthrough on disposable data after A0-A14 evidence is reviewed. |

## Commands run

The final acceptance run must include:

```sh
python3 scripts/validate_contract.py
python3 -m unittest discover -s tests -p 'test_*.py'
pnpm --dir upstream/social-app run typecheck:web
pnpm --dir upstream/social-app exec jest \
  src/lib/atproto/spaces/fanout.test.ts \
  src/lib/atproto/spaces/sync.test.ts \
  src/lib/atproto/spaces/client.test.ts \
  src/lib/permissioned-data.test.ts --runInBand
NODE_OPTIONS=--experimental-vm-modules pnpm --dir upstream/atproto-pds \
  --config.pm-on-fail=ignore --filter @atproto/pds exec jest \
  tests/permissioned-data/store.test.ts tests/space/records.test.ts \
  tests/space/auth.test.ts tests/space/sync.test.ts \
  tests/space/simplespace.test.ts tests/radlib-spaces.test.ts --runInBand
```

The PDS package build uses direct TypeScript build validation in this checkout:

```sh
pnpm --dir upstream/atproto-pds --config.pm-on-fail=ignore \
  --filter @atproto/pds exec tsc --build tsconfig.build.json
```

The repository's nested `prebuild` script currently rejects pnpm 11.21 when
the package declares 11.11; that package-manager mismatch is tooling noise,
not a source build failure.

## Explicit blockers before production

- Spaces alpha schema/database compatibility is not a production contract.
- Existing alpha credentials are not immediately invalidated by membership
  removal.
- The private sync implementation is minimal and fanout-based.
- Browser notification sync, full community member management, aggregate feed
  pagination, and external Relay/AppView leak scans are not complete.
- The production-configured web bundle is now deployed to Cloudflare Pages;
  production private-board acceptance remains blocked by the current browser
  session's invalid PDS token until a fresh sign-in is performed.
- A human owner must accept the residual alpha risk and disposable-data policy.
