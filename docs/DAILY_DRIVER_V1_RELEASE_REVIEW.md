# Daily Driver v1 Release Review

## Verdict

**DAILY_DRIVER_V1_RELEASE_READY**

Supported deployment is the existing social-app browser client against compatible external ATProto services. AppViewLite is optional self-hosted infrastructure, not required for the daily-driver path.

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

Production defaults use `EXPO_PUBLIC_ENV=production`, `https://bsky.social`, and `https://api.bsky.app`; localhost, fixture providers, and test credentials are disabled by the machine-readable config fixture. No new credential storage, diagnostic secret paths, or constitutional semantic changes were introduced.

## Verification

Root: 74 passed, 2 skipped. Contract validation: 64 files passed. Social-app web typecheck: passed. Production web build: passed. Diff check: passed. Parent and submodule trees are clean. The real external-account smoke path is `SKIPPED_ENVIRONMENT`; fixture and build evidence are retained separately.
