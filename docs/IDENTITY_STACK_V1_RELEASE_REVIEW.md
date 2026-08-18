# Identity Stack v1 Ultra Review

## Verdict

**IDENTITY_STACK_V1_REVIEW_BLOCKED**

The audit found unresolved P1 implementation gaps. Frozen constitutional documents remain intact, but the runtime/UI evidence does not support a truthful release-ready claim.

## Frozen inventory

| Stage | Parent | social-app | Evidence |
|---|---|---|---|
| Constitution | `8c91911` | `8c91911` | `artifacts/identity-constitution-v1-test-report.json` |
| Runtime | `765ecf2` | `d64e8b06` | `artifacts/identity-runtime-v1-test-report.json` |
| Recovery | `043e01b` | `af3e60e17` | `artifacts/identity-recovery-v1-test-report.json` |
| Sovereignty UI | `33f2a01` | `63ad20349` | `artifacts/identity-sovereignty-ui-v1-test-report.json` |

## P1 findings

1. **UI uses fabricated runtime state.** `upstream/social-app/src/screens/Settings/IdentitySovereigntySettings.tsx:5` hard-codes `Current account DID`, `verified`, `idle`, and `simulated` rather than consuming the resolver, migration, and recovery runtime. It can display verified identity without evidence and exposes no real session/recovery/lockdown controls. This violates UI truthfulness and is a release-blocking capability misrepresentation.
2. **Resolver endpoint is not hardened.** `upstream/social-app/src/lib/identity-runtime.ts:6` accepts and returns arbitrary endpoint strings, including loopback/private schemes, without scheme, redirect, size, or private-address validation. Any consumer that follows the endpoint can inherit SSRF/endpoint-confusion risk. The documented security contract is not enforced.
3. **Stale cache is not authorization-safe.** `IdentityCache.get` returns `stale-cache` resolutions through the same resolution API and no sensitive-operation freshness guard exists. Migration, recovery, provider-switch, and lockdown invalidation are not wired to this cache. A caller can accidentally use stale PDS authority for a sensitive action.

## P2/P3 findings

- P2: resolver fallback stops at the first syntactically successful mismatched result instead of retaining provider disagreement provenance and trying configured alternatives.
- P2: migration/recovery receipts are represented by types but lack tamper verification and durable persistence in runtime code.
- P2: live public resolver probes and live disposable migration are skipped/unavailable; current reports correctly mark simulation but cannot upgrade evidence.
- P3: UI screen is a dense one-line component and accessibility automation is documented rather than live-tested.

## Capability matrix

| Migration stage | Class | Reason |
|---|---|---|
| destination validation | FIXTURE-TESTED | typed state machine only |
| repository transfer | SIMULATED | no safe upstream disposable transfer API wired |
| blob transfer | SIMULATED | no safe upstream disposable transfer API wired |
| identity update | UNSUPPORTED-UPSTREAM | no production mutation exercised |
| activation/old authority retirement | FIXTURE-TESTED | receipt/state characterization |
| verification | FIXTURE-TESTED | deterministic harness |

Live resolver probes: `SKIPPED_ENVIRONMENT` (no safe public probe was run). Live migration: `UNSUPPORTED-UPSTREAM` / not safe to mutate a real account.

## Cross-constitution result

Existing root regressions pass for Association, Service, Portable Personalization, Candidate/Balanced, and Attention. No frozen semantic changes were found. The findings are in the new runtime/UI layer and must be fixed before a release-ready re-audit.

## Required remediation

- Bind UI to actual account/resolver/runtime/recovery state and make high-stakes controls operational or explicitly unavailable.
- Validate endpoint scheme/host, redirects, response bounds, and private-address policy before use.
- Separate display stale state from authorization: require fresh resolution for sensitive operations and wire invalidation across migration, recovery, provider switching, and lockdown.
- Add durable, tamper-verifiable receipts and provider disagreement handling.
