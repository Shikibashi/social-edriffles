# Daily Driver v1 Feature Matrix

| Area | Status |
|---|---|
| Web launch/auth/profile/timeline/thread/search | FIXTURE-TESTED / existing client path |
| Association pairwise controls | FIXTURE-TESTED |
| Following/Balanced/feeds/provider choice | FIXTURE-TESTED |
| Service identity/fallback | FIXTURE-TESTED |
| Identity provenance/recovery UI | FIXTURE-TESTED; live resolver environment-dependent |
| Portable Personalization | FIXTURE-TESTED |
| Repository/blob migration | SIMULATED |
| Identity endpoint update | UNSUPPORTED-UPSTREAM |
| Public resolver probe | SKIPPED_ENVIRONMENT |
| Native packaged Linux desktop | UNIMPLEMENTED |

Claims remain qualified where live external infrastructure was not exercised.

# Troubleshooting

- **Cannot start:** verify Node/pnpm versions, run `pnpm install --frozen-lockfile`, and check `EXPO_PUBLIC_ENV`.
- **Authentication fails:** identify whether the PDS, resolver, OAuth callback, or network is failing; retry only after confirming the configured origin.
- **AppView/feed unavailable:** inspect the named provider and use explicit Services selection; no silent identity-authority substitution occurs.
- **Identity stale/unresolved:** retry fresh verification; stale display state never authorizes sensitive writes.
- **Build failure:** run `pnpm typecheck:web`, inspect the first error, and avoid copying local absolute paths into configuration.
