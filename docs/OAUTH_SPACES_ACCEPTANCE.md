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
repo/sequencer boundaries, and the fork-owned immediate-revocation extension:
an already-issued credential in the `us.edriffles.radlib.*` namespace is rejected
after membership removal on both the authority PDS and a member PDS. Standard
Space credentials remain interoperable when the extension is disabled or when
the Space type is outside the fork-owned namespace.

The credentialed disposable PDS OAuth protocol walkthrough passes through
authorization-page load, sign-in, consent, callback, profile read, restore,
and cleanup using the official Node OAuth client against the public canonical
origin. The isolated browser lane entered only a freshly created disposable
account credential and observed the callback before the web client returned to
its home route. The acceptance bundle must never substitute a production
credential.

## Receipt and scan contract

`artifacts/receipts/local-oauth-spaces-acceptance.json` records the disposable
local test results. `artifacts/receipts/local-private-canary-scan.json` defines
the canary proof: a private record must be absent from the public repo CAR and
public sequencer, absent from a controlled AppView result, and never copied to
the receipt. `artifacts/receipts/cloudflare-deploy-attempt.json` records the
earlier failed deployment attempt without exposing the rejected token,
`artifacts/receipts/cloudflare-deploy-success.json` preserves the prior
successful deployment, and
`artifacts/receipts/cloudflare-deploy-success-7c5fcd1c.json` is retained as
historical deployment evidence. The current PDS image
(`sha256:3d4c971691f205fdd7afd8050681669eb0a563495c334531f801bd0ebe6dc348`)
and its source binding are recorded in `artifacts/deployment-current.json`; the
prior `artifacts/receipts/pds-deploy-success-8473b0ba.json` remains historical
evidence for its public DID discovery and unrelated-Host rejection. The prior
`cloudflare-deploy-success-2816da7c.json`,
`cloudflare-deploy-success-236dff2c.json`,
`cloudflare-deploy-success-31e7cbac.json`,
`cloudflare-deploy-success-51d0ffc0.json` and
`cloudflare-deploy-success-7e4ac417.json`, and
`cloudflare-deploy-success-eee550b3.json` receipts are retained as historical
evidence.

The current disposable PDS test lane records the local resolver authority used
to make the `us.edriffles.radlib.*` declarations available to OAuth. The live
`_lexicon.radlib.edriffles.us` TXT record is verified by three DNS resolvers,
and the checked-in schema repository supplies the corresponding declarations.
DNS and repository resolution do not prove independent operation by themselves;
that operator-independence gate remains explicit. `edriffles.us` remains the
only registrable domain; no `radlib.org` authority is required or claimed.

`python3 scripts/validate_oauth_spaces_receipts.py` verifies every receipt hash,
the manifest sidecar, the current source and web artifact digests, the
secret-free key policy, and the fact that authority and unavailable external
credentials remain explicit non-passes.

The canonical user-facing web/client origin is `https://plumblines.uk`. The
edge Worker maps its public web, callback, account/PDS, and XRPC paths onto the
existing Pages and PDS implementation targets. The public OAuth/PDS and
`did:web` authority is Plumbline; `pds.edriffles.us` remains a technical
implementation/resource boundary and the existing
`us.edriffles.radlib.*` namespace remains protocol-compatible infrastructure.
Older route, metadata, and DNS receipts are historical evidence only. A fresh
credential-free public probe must bind the Pages upload and Plumbline public
route to the current source revision. The remaining open gates are the
external Relay/AppView scan, short-TTL expiry/replay walkthrough, and proof of
independent PLC-operator control.
