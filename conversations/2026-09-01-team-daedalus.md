---
date: 2026-09-01
project: atproto
keywords: [plumbline, services, inspector, flexbox, workpm]
summary: "WorkPM follow-up for compact explanatory Services inspectors"
---

# 2026-09-01 WorkPM activity log

## Objective

Continue the active Plumbline goal after the deployed editorial release by
auditing a remaining workbench surface against the canonical design language
and repairing the next root-level defect without changing authority,
credentials, provider registration, or user data.

## Findings

- The live `Services → Policies` workbench rendered its page-owned Inspector
  as a tall, mostly empty column. Its source, rule, user-control, and state
  fields were distributed over the full height of the adjacent workspace.
- The cause was local and deterministic: `SettingsList.ItemText` owns
  `flex: 1` for ordinary horizontal list rows. The Services Inspector reused
  that primitive as direct children of a vertically stretched column.
- React Native's Flexbox model distributes positive flex values on the main
  axis. The component therefore required an explicit compact-detail boundary,
  not a provider or OAuth change.
- The polycentric-authority decision record still named the retired
  `social.edriffles.us` web host even though deployed OAuth client metadata
  names `plumblines.uk`. The record needed a precise domain correction without
  renaming the deliberately separate `pds.edriffles.us` or
  `radlib.edriffles.us` services.

## Decision

- Add `ServiceInspectorDetail` in
  `upstream/social-app/src/screens/Settings/ServicesSettings.tsx`.
- The detail primitive keeps the existing semantic text, theme, and
  accessibility structure while setting `flex: 0` for its label and value.
- Mark the Inspector `self_start` so it retains its own content height instead
  of stretching to the full workspace column.

## Verification

| Check | Status | Evidence |
| --- | --- | --- |
| Live defect observation | PASS | The deployed Policies Inspector measured 800px high; each of its eight direct text children had `flex: 1` and a 86px height. |
| Source whitespace check | PASS | `git diff --check` in `upstream/social-app`. |
| Prettier | PASS | `pnpm exec prettier --check src/screens/Settings/ServicesSettings.tsx`. |
| Web TypeScript | PASS | `pnpm typecheck:web`. |
| Production web build | PASS | `EXPO_PUBLIC_ENV=production pnpm build-web`; bundle-size warnings only. |
| Core sovereignty regression fixtures | PASS | 6 suites, 47 tests across provider composition, PLC history/key custody, portable policy, and recovery. |
| Local logged-out route smoke check | PASS | Built SPA loaded on an ephemeral local server with one H1, no alert state, and no horizontal overflow. |
| Canonical-domain record check | PASS | Client metadata uses `https://plumblines.uk/oauth-client-metadata.json`; the decision record now distinguishes the Plumbline public origin from the PDS and Spaces service hosts. |
| Deployed public-feed read check | PASS | The current canonical deployment loaded actual posts in the in-app browser with one main landmark, one H1, no alert state, and no horizontal page overflow. This observes the prior deployment, not the unshipped compact-Inspector change. |
| Authenticated local inspector rendering | NOT RUN | The temporary local origin correctly had no production browser session. No credential, OAuth request, session data, or social write was used. |
| Deployed visual confirmation of this follow-up | NOT RUN | This local follow-up has not been committed, pushed, or deployed. |

## Boundary

This change is presentation-only. It does not alter OAuth scope requests,
identity recovery, PLC verification, provider policy, AppView behavior, Spaces,
chat, PDS writes, or external release evidence.
