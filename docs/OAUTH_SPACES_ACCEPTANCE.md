# OAuth and Spaces acceptance

This is the repository-native, secret-free acceptance lane for the OAuth and
Spaces migration. It keeps local disposable-provider evidence separate from
external production gates. No credential, refresh token, password, DPoP key,
or authorization header belongs in a receipt.

## Run the local lane

```sh
cd upstream/social-app
pnpm exec jest src/state/session/__tests__/oauth-login-input-test.ts \
  src/state/session/__tests__/oauth-scopes-test.ts \
  src/state/session/__tests__/oauth-session-test.ts \
  src/lib/atproto/spaces/client.test.ts \
  src/lib/atproto/spaces/credential.test.ts \
  src/lib/atproto/spaces/sync.test.ts \
  src/env/common.test.ts --runInBand
pnpm typecheck:web

cd ../atproto-pds
pnpm --config.pm-on-fail=ignore --filter @atproto/pds test:sqlite -- \
  --runInBand tests/space-scope.test.ts tests/space/auth.test.ts \
  tests/radlib-spaces.test.ts

cd ../..
python3 scripts/validate_contract.py
python3 scripts/validate_oauth_spaces_receipts.py
```

The local PDS suites create ephemeral identities and DPoP-bound Space
credentials. They prove scope/credential parsing, issuance checks, replay and
key binding, strict `us.edriffles.radlib.private.post` validation, cleanup, private
repo/sequencer boundaries, and the alpha behavior in which an already-issued
credential remains usable until expiry after membership removal.

The credentialed disposable PDS OAuth protocol walkthrough passes through
authorization-page load, sign-in, consent, callback, forced refresh, and
revocation using the official Node OAuth client against the public canonical
origin. The browser UI lane reaches the PDS password screen with the owner
handle and a canonical HTTPS client ID; password entry is intentionally not run
under the browser safety policy. The acceptance bundle must never substitute a
production credential.

## Receipt and scan contract

`artifacts/receipts/local-oauth-spaces-acceptance.json` records the disposable
local test results. `artifacts/receipts/local-private-canary-scan.json` defines
the canary proof: a private record must be absent from the public repo CAR and
public sequencer, absent from a controlled AppView result, and never copied to
the receipt. `artifacts/receipts/cloudflare-deploy-attempt.json` records the
earlier failed deployment attempt without exposing the rejected token,
`artifacts/receipts/cloudflare-deploy-success.json` preserves the prior
successful deployment, and
`artifacts/receipts/cloudflare-deploy-success-7c5fcd1c.json` records the
current deployment, CSP, header probes, OAuth metadata, and complete
Space-URI validation. The current PDS image
(`sha256:8473b0ba089930f9ad61773c27f9efb65a5c238e2e666794a8ef9e0bf86b062a`)
and public DID discovery, including rejection on an unrelated Host header, are
recorded in `artifacts/receipts/pds-deploy-success-8473b0ba.json`; the prior
`cloudflare-deploy-success-2816da7c.json`,
`cloudflare-deploy-success-236dff2c.json`,
`cloudflare-deploy-success-31e7cbac.json`,
`cloudflare-deploy-success-51d0ffc0.json` and
`cloudflare-deploy-success-7e4ac417.json`, and
`cloudflare-deploy-success-eee550b3.json` receipts are retained as historical
evidence.

The current disposable PDS test lane records the local resolver authority used
to make the `us.edriffles.radlib.*` declarations available to OAuth. The live
`_lexicon.radlib.edriffles.us` TXT record is now independently verified by
multiple DNS resolvers, and the checked-in schema repository supplies the
corresponding declarations. `edriffles.us` remains the only registrable domain;
no `radlib.org` authority is required or claimed.

`python3 scripts/validate_oauth_spaces_receipts.py` verifies every receipt hash,
the manifest sidecar, the current source and web artifact digests, the
secret-free key policy, and the fact that authority and unavailable external
credentials remain explicit non-passes.

The canonical user-facing web/client origin is `https://social.edriffles.us`.
The edge Worker maps its public web, callback, account/PDS, and XRPC paths onto
the existing Pages and PDS implementation targets. The configured OAuth/PDS
protocol origin remains `https://radlib.edriffles.us`, so the owner DID's
`pds.edriffles.us` resource compatibility document points to that issuer. It
is not a second issuer or a second domain. Public route, metadata, and DNS
authority evidence is recorded in the current cutover and authority receipts;
Spaces/AppView/expiry evidence remains open.
