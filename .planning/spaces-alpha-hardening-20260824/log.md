# Planning log

## 2026-08-23

- Initialized `workpacks` bundle.

## 2026-08-23

- Applied the required less-but-better cut before decomposition.
- Kept four deliverables: fail-closed block lookup, private XRPC headers, the community Space Lexicon, and the alpha documentation/release gate.
- Deferred private AppView/search/notifications/moderation-reader infrastructure because it requires a separate service architecture and deployment authority.
- Kept all workpacks in `draft`: this cycle authorizes planning artifacts, not source/test edits or deployment.
- Independent review passed: four required workpack headings are present; WP-001/WP-002 shared-path ownership is serialized; WP-003 is independent; WP-004 gates all predecessors; no dependency or hierarchy cycle exists; optional service architecture is excluded.
- Implementation-ready validation was intentionally not promoted to `ready`: the new red tests have not been materialized because source/test edits were not authorized in this planning turn.

## 2026-08-23 implementation wave

- User authorized Copernicus execution. Implemented Wave 1 only: WP-001 and WP-003; no deployment or production mutation was performed.
- Test-first red evidence: the new tests failed against the baseline with first-page-only block handling, fail-open remote lookup errors, and unresolved `org.radlib.community`.
- WP-001 completed: remote block checks now paginate with cursor-loop/page/deadline bounds, validate response shape, share a five-second deadline across both directions, and map incomplete verification to `NotAuthorized` before access grants.
- WP-003 completed: added the tracked `org.radlib.community` Space Lexicon source and dev authority fixture; generated PDS outputs resolve `Radlib Community` with only `org.radlib.private.post` declared.
- Verification evidence: PDS type-check builds for `@atproto/pds` and `@atproto/dev-env`; focused tests 12/12 passed; six-suite Space regression 146/146 passed; Lexicon code generation completed.
- WP-002 private response-header normalization and WP-004 alpha documentation/release gate remain draft and intentionally unimplemented in this wave.

## 2026-08-23 Wave 2 implementation and release gate

- User authorized the next Copernicus wave. Materialized WP-002's real HTTP header matrix first; the baseline red result reproduced the service-auth fallback failure with `Cache-Control: private`.
- WP-002 source implementation is complete locally: private control auth reapplies `private, no-store` and `Authorization, DPoP` variation across service-auth success, fallback authorization success, and both failure paths. The local header suite passes 2/2.
- WP-004 documentation gate is complete: all three Spaces documents now state alpha/no-E2EE limits, delayed credential revocation, Lexicon/authority status, fail-closed block bounds, header evidence, exact checks, and deferred services.
- Regression evidence: seven PDS suites pass with 149 tests; root Python contract tests pass 91 tests with 5 skips; formatter, ESLint, contract validation, upstream pin check, and Copernicus workpack validation pass.
- Read-only external evidence remains a release blocker: `https://pds.edriffles.us/xrpc/org.radlib.private.listCommunities?limit=50` still returns `Cache-Control: private` while `cf-cache-status: DYNAMIC`. No deployment or credentialed probe was performed; the source fix must be deployed and re-probed under separate production authorization.

## 2026-08-23 deployment wave

- Committed and pushed PDS hardening as `2a119ba5f15a349d0db63fe46d1d3c854dfb9760` and root metadata/docs as `1d89267`.
- Built `codex/atproto-pds-spaces-alpha:test` from the committed checkout and recreated only the PDS container; persistent volume `codex_spaces_alpha_test_data` remained mounted.
- Container health, `describeServer`, and the active `cloudflared-atproto-pds.service` check passed.
- Deployed unauthorized probes for `listCommunities` and `getSpace` now return `Cache-Control: private, no-store` and `Vary: Authorization, DPoP, Accept-Encoding` through `pds.edriffles.us`.
- No credentialed deployed probe was run; local real-HTTP tests cover authorized and unauthorized paths without exposing production credentials.
