# Project Instructions

## Scope
This fork is contract-first. PR-00/PR-01 documents and characterizes pinned upstream behavior; it does not change production blocking, client, feed-generator, or UI semantics.

## Upstream baselines
- AppViewLite: `alnkesq/AppViewLite` at commit `75f78e8e098c05f52821e836832205050c0f539e`.
- Client: `bluesky-social/social-app` at commit `1f5c698165c922e707833809902ee959e9824f00`.
- Record source URLs and retrieval dates in `upstream-pins.json`.

## Verification
Run `python3 scripts/validate_contract.py` from the repository root. It validates required documents, pinned metadata, deterministic fixtures, and the A/B/C characterization matrix. Do not claim runtime AppView tests until the pinned upstream source is vendored or wired into a focused test harness.

## Upstream maintenance
Never rebase against moving branch heads without updating `upstream-pins.json`, reviewing licenses, refreshing dated protocol references, and rerunning validation. Keep observed characterization fixtures separate from constitutional requirements.

## Deferred work
Runnable pairwise semantic changes, client UI/provider selectors, feed generators, custom candidate-batch protocols, advanced provenance/audits, permissioned-data sync, and runtime attestation require separate approved work.
