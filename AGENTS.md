# Project Instructions

## Scope
This fork is contract-first. PR-00/PR-01 documents and characterizes pinned upstream behavior; it does not change production blocking, client, feed-generator, or UI semantics.

## Upstream baselines
- First-party PDS: `bluesky-social/atproto` at commit `760fb12a080c87cdfd0dae42ae833bad8bc20886`.
- Client: `bluesky-social/social-app` at commit `1f5c698165c922e707833809902ee959e9824f00`.
- AppViewLite and FishyFlip are retired from this repository and are not supported runtime dependencies.
- Record source URLs and retrieval dates in `upstream-pins.json`.

## Verification
Run `python3 scripts/validate_contract.py` from the repository root. It validates required documents, pinned metadata, deterministic fixtures, and the A/B/C characterization matrix. Do not claim runtime provider tests until the selected provider source is vendored or wired into a focused test harness.

## Upstream maintenance
Never rebase against moving branch heads without updating `upstream-pins.json`, reviewing licenses, refreshing dated protocol references, and rerunning validation. Keep observed characterization fixtures separate from constitutional requirements.

## Deferred work
Runnable pairwise semantic changes, client UI/provider selectors, feed generators, custom candidate-batch protocols, advanced provenance/audits, permissioned-data sync, and runtime attestation require separate approved work.
