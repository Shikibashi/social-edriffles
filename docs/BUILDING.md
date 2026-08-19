# Building

Requirements are Node `>=24.19.0` and pnpm `11.21.0` as declared by `upstream/social-app/package.json`.

```sh
cd upstream/social-app
pnpm install --frozen-lockfile
pnpm typecheck:web
pnpm test-ci --runInBand
EXPO_PUBLIC_ENV=production pnpm build-web
```

`pnpm web` is the development launcher. `pnpm build-web` is the supported web artifact command. Native EAS builds require platform credentials/toolchains and are not part of the Linux Daily Driver path. Retired read-provider source is not built by this repository.

For an integrated local browser walkthrough, start the pinned first-party
PDS/AppView fixture separately and run the client with an explicit Project
AppView configuration. The owner checklist contains the exact command and
requires the configured AppView service DID to match the DID printed by the
fixture. The client must not be launched with an implicit stock AppView URL.
