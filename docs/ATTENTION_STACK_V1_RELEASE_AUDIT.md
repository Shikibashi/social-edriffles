# Attention Stack v1 Hostile Release Audit

Date: 2026-08-18
Decision: `ATTENTION_STACK_V1_REVIEW_BLOCKED`

## Evidence executed

- `python3 scripts/validate_contract.py`: passed, 16 files / 29 blocking rows / 6 feed cases.
- `python3 -m unittest discover -s tests -p 'test_*.py'`: 58 passed, 2 skipped.
- `git diff --check`: passed.
- social-app focused suites previously recorded: personalization 5, feed security 3, candidate protocol 3, Balanced 3, UI 7, experimental modules 2; web typecheck passed.
- Release artifact paths: `artifacts/*-test-report.json`.

## Frozen SHA inventory

- Service/security parent baseline: `12f80ec`.
- Candidate Protocol parent: `45c9353` with social implementation `dc8daa01` lineage.
- Balanced parent: `1d34144`, social implementation `dc8daa01`.
- Attention Sovereignty UI parent: `235195e`, social implementation `f66b7be`.
- Experimental modules parent: `5acba74`, social implementation `e3f9aa2e`.
- AppViewLite baseline: `ab3ac9e`.

No unexplained tracked working-tree drift was found. The frozen contracts and validator remain present; this audit does not silently rewrite them.

## Findings

### P1 — Release exit path is not end-to-end runnable

The repository contains typed contracts, client-local ranking, settings surfaces, and characterization fixtures, but no single runnable scenario exercising PDS A → AppView X → provider/algorithm switching → AppView switch → PDS B migration/import. Existing AGENTS.md explicitly defers runnable pairwise semantics, production resolver integration, and migration workflows. This prevents proving the strongest required exit test.

Evidence: `AGENTS.md` deferred-work section; `docs/SERVICE_BOUNDARIES.md`; `docs/CANDIDATE_PROTOCOL_V1.md`; absence of an integrated exit harness.

Remediation: add a focused disposable multi-service harness and replayable migration fixture before release.

### P1 — Attention-surface coverage is contractual, not implemented

The audit surface includes timeline, feeds, search, account recommendations, feed discovery, trending, notifications, Starter Packs, and social-proof metrics. Current changes implement provenance/controls models and a settings screen, but do not integrate provenance and Why-this-post into every listed surface. This is a contract gap, not a test gap.

Evidence: `upstream/social-app/src/components/FeedProvenanceCard.tsx` is a reusable component without broad surface integration; `docs/ATTENTION_SOVEREIGNTY_UI_V1.md`; route/settings inventory.

Remediation: inventory each surface with explicit integration or constitutional future-work status and add user-visible entry points where promised.

### P1 — Experimental modules do not independently implement required objectives

`rankExperimental` modifies a few feature defaults and delegates to Balanced. It does not implement independent measurable constructive/bridging/longform/news objectives, hard-constraint preservation for High Serendipity, source/story clustering for News, or independent evaluation metrics. The manifests accurately say experimental, but the implementation is a selector shim rather than five independently evaluated algorithms.

Evidence: `upstream/social-app/src/lib/experimental-attention.ts`; `tests/fixtures/experimental-attention-v1.json` contains scenario names and metric labels but no measured result matrix.

Remediation: either narrow the product contract to explicit experimental presets backed by Balanced, or implement and evaluate each objective independently before release.

### P2 — Cross-runtime deterministic replay is not proven

Tests run in the social-app Jest environment and root Python fixtures. There is no cross-platform/cross-runtime replay artifact comparing serialized outputs across supported runtimes.

Evidence: `artifacts/experimental-attention-v1-test-report.json`; no platform comparison artifact.

Remediation: add canonical serialized replay outputs and compare them under pinned runtimes.

### P2 — Accessibility proof is structural only

Accessibility labels, header semantics, and live-region fields are present, but no live screen-reader/keyboard automation transcript or screenshot artifact was produced for the changed UI.

Evidence: `upstream/social-app/src/components/FeedProvenanceCard.tsx`; `artifacts/attention-sovereignty-ui-test-report.json`.

Remediation: run supported client accessibility automation and retain transcript/artifact.

## Positive controls verified

- Provider output remains declarative and provider credentials are not part of personalization exports.
- Candidate signing/expiry/replay and hydration contracts have focused tests and fixtures.
- Balanced ranking is local, deterministic for identical inputs, and emits traces.
- Provider health/fallback concepts are represented as visible states.
- Public Why-this-post model marks confidential integrity signals omitted.
- Portable personalization export/import/reset remains account-scoped.

## Release decision

P1 findings remain open. The attention stack is **not release ready**. Required remediation is an end-to-end exit harness, complete surface integration inventory/implementation, and honest independent experimental-module evaluation or contract narrowing.

ATTENTION_STACK_V1_REVIEW_BLOCKED
