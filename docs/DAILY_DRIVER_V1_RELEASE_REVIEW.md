# Daily Driver v1 Release Review (historical baseline)

> **Historical document.** This review predates the current radical-liberal
> acceptance pass and is retained for provenance only. Its counts, tree-status
> statement, and release verdict are superseded by
> `docs/RADLIB_CODEX_ACCEPTANCE_REVIEW.md`; they must not be used as current
> owner-acceptance evidence.

## Verdict

**DAILY_DRIVER_V1_RELEASE_READY**

Supported deployment is the existing social-app browser client against
compatible external ATProto services and the first-party PDS. AppViewLite is
retired and is not required or supported for the daily-driver path.

## Commands

```sh
cd upstream/social-app
pnpm install --frozen-lockfile
pnpm typecheck:web
EXPO_PUBLIC_ENV=production pnpm build-web
pnpm web
```

The production web artifact is `upstream/social-app/web-build`. The artifact metadata and entrypoint checksum are recorded in `artifacts/daily-driver-v1-release.json`.

## Severity

P0: 0. P1: 0. P2: 2. P3: 0.

P2 items are live public resolver probes skipped in this environment and migration repository/blob transfer remaining simulated/upstream-constrained. Neither is presented as live.

## Feature/capability summary

Core social, Association, Attention, Service, Identity, and Portable Personalization paths are fixture-tested through the existing client and regression suite. Migration is `SIMULATED`; identity endpoint update is `UNSUPPORTED-UPSTREAM`; public resolver probes are `SKIPPED_ENVIRONMENT`; native packaged Linux desktop is unimplemented. The supported Linux path is browser/PWA-style static web hosting, without adding a new desktop wrapper.

## Security and configuration

Production defaults use `EXPO_PUBLIC_ENV=production` and an explicitly
configured project AppView; the compatible `https://bsky.social` entryway is
limited to account login/handle availability. There is no implicit
`api.bsky.app` read provider. Localhost, fixture providers, and test
credentials are disabled by the machine-readable config fixture. No new
credential storage, diagnostic secret paths, or constitutional semantic changes
were introduced.

## Verification snapshot retained from the historical review

The historical snapshot recorded 74 root tests, 64 contract files, a clean
tree, and a passed client build. Those values are intentionally not restated
as current evidence. Current counts, dirty-tree status, and the current PDS
build result are maintained in `docs/RADLIB_CODEX_ACCEPTANCE_REVIEW.md`.
