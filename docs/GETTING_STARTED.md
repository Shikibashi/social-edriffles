# Getting Started

```sh
cd upstream/social-app
corepack enable
pnpm install
pnpm web
```

Open the local Expo web URL and sign in through the existing account flow. For a production-like static bundle use `EXPO_PUBLIC_ENV=production pnpm build-web`; the output is generated under the social-app web export directory. Configure only documented environment inputs; do not place tokens or passwords in `.env` files.

For the governed first-party PDS, install the pinned submodule dependencies and
build it with the policy enabled:

```sh
cd upstream/atproto-pds
npm exec --yes --package=pnpm@11.11.0 -- pnpm install --frozen-lockfile --ignore-scripts
PDS_RADLIB_MODERATION_WRITE_POLICY=deny-create-update \
  npm exec --yes --package=pnpm@11.11.0 -- pnpm --filter @atproto/pds build
```

The first-party `services/pds` entrypoint also fails closed unless that exact
setting is present. Its Docker image supplies the governed value by default;
the reusable `@atproto/pds` package keeps its upstream-compatible `standard`
default when embedded by another service.

The PDS still requires the normal official environment for database,
blobstore, PLC, signing-key, and session secrets. Retired providers are not
part of the launch path and cannot substitute for this PDS.

The root contract gate is `python3 scripts/validate_contract.py` and the root regression suite is `python3 -m unittest discover -s tests -p 'test_*.py'`.
