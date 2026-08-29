---
date: 2026-08-28
project: atproto
keywords: [oauth, provider-composition, plc, policy-portability, key-custody]
summary: "WorkPM implementation log for polycentric AT Protocol client boundaries"
---

# 2026-08-28 WorkPM activity log

## Objective

Implement the approved polycentric/user-sovereign client delta in the existing
AT Protocol fork: feature-scoped OAuth upgrades; provider composition across
read surfaces; verified PLC resolver plurality; portable policy controls;
user-held rotation-key custody; and adversarial multi-provider fixtures.

## Phase 1: repository and protocol reconciliation

- Confirmed the root contract-first repository and nested `upstream/social-app`
  client boundary.
- Preserved the deployment decision: `social.edriffles.us`,
  `pds.edriffles.us`, and `radlib.edriffles.us`; no new registrable domain.
- Reviewed current official OAuth, permissions, DID, cryptography, PLC replica,
  and recovery material before implementation.
- Confirmed that local tests cannot prove deployed credentials, independent
  operator control, Lexicon publication, or Relay/AppView ingestion.

## Phase 2: implementation decisions

- Split new OAuth requests into ordinary base scopes and explicit feature
  groups. Keep legacy transition scopes only as compatibility recognition for
  existing sessions.
- Make provider composition generic over surface and policy, retaining every
  observation and its status instead of returning an unlabelled winner.
- Keep PDS-owned writes, media/blob operations, and Spaces community authority
  explicit where no standard AppView read contract exists.
- Verify PLC histories cryptographically before selection; display operator
  declarations without treating them as proof of independent operation.
- Make policy portability versioned, credential-free, known-provider-only, and
  resettable.
- Make browser rotation keys non-extractable and require prior PLC
  authorization; leave native secure custody to the platform adapter.

## Phase 3: implementation evidence

Changed the nested client in these areas:

- `src/state/session/oauth-scopes.ts`, `oauth-session.ts`, `session-core.ts`,
  `index.tsx`, `session-data.ts`, `types.ts`
- `src/lib/provider-composition.ts`, `provider-composition.test.ts`
- `src/state/queries/provider-composition.ts` and profile, post, feed, search,
  labeler, and notification query boundaries
- `src/lib/plc-history.ts`, `plc-history.test.ts`, `plc-resolver.ts`,
  `plc-key-custody.ts`, `plc-key-custody.test.ts`
- `src/state/session/plc-resolvers.ts` and resolver tests
- `src/state/session/providers.ts` and provider tests
- `src/lib/personalization.ts`, `personalization.test.ts`, and persisted schema
- `src/screens/Settings/ServicesSettings.tsx` and
  `PersonalizationSettings.tsx`
- `src/screens/Settings/IdentitySovereigntySettings.tsx` — safe browser
  preparation of user-held PLC rotation custody, with explicit authorization
  limits

Added the root architecture record and authority-loop diagram:

- `docs/ANARCHISTIC_POLYCENTRIC_ARCHITECTURE_DECISION.md`
- `docs/flow-diagrams/polycentric-authority-loop.mmd`

## Verification status at log creation

| Check | Status | Evidence |
|---|---|---|
| Focused Jest suites | PASS | 7 suites, 57 tests |
| Full Jest suite | PASS | 103 suites, 984 tests, 21 snapshots; 28 existing todo tests |
| Web TypeScript check | PASS | `pnpm run typecheck:web` |
| Prettier on changed client files | PASS | formatted changed files |
| Root whitespace check | PASS | `git diff --check` in the nested client |
| Changed-file Oxlint | PASS | exact changed/new client file set |
| Full repository lint | FAIL | existing import-sort, unused-variable, TypeScript, and suppression-baseline violations outside this change |
| Web production build | PASS | `pnpm run build-web`; only bundle-size warnings |
| Root contract validation | PASS | `python3 scripts/validate_contract.py`; 125 files, 29 blocking rows, 6 feed cases |
| Credentialed disposable OAuth | BLOCKED | no disposable identity/invite/credential; no production credential used |
| Credentialed Spaces revocation | BLOCKED | no disposable credentialed environment available |
| Independent PLC operator evidence | NOT RUN | requires independently controlled deployment evidence |
| Relay/AppView external scan | NOT RUN | local fixture results do not prove external ingestion/privacy |

## Remaining work

Run the final deterministic verification cycle, repair root causes, reconcile
the blueprint with the implementation, and update this table with the actual
results. Do not commit, push, or deploy as part of this implementation turn.
