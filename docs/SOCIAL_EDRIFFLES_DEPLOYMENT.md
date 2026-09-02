# Plumbline at `plumblines.uk`

Status: `SOURCE_CONFIGURED / PAGES_DEPLOYMENT_PENDING / EXTERNAL_APPVIEW_EXPIRY_AND_PLC_INDEPENDENCE_GATES_PENDING`

The public product name is **Plumbline**. The radical-liberal constitutional
implementation remains documented and machine-readable internally; Plumbline
expresses it through explicit providers, provenance, ranking choice,
identity/exit, and association boundaries rather than through a political
brand claim. Existing protocol/profile identifiers remain unchanged for
compatibility.

## Current single-host topology

The user-facing public contract is `https://plumblines.uk`. The existing Pages
project and PDS remain implementation targets behind the edge Worker. The
canonical public web, OAuth, PDS, DID, and XRPC paths share the Plumbline host;
the `edriffles.us` hosts remain technical implementation and compatibility
boundaries, not browser-facing product identity.

| Boundary | Verified value |
|---|---|
| Pages project | `social-edriffles` |
| User-facing public origin | `https://plumblines.uk` |
| Public OAuth/PDS origin | `https://plumblines.uk` |
| Registrable domains | `plumblines.uk` for the public product; `edriffles.us` for existing PDS, Spaces, and implementation boundaries |
| Edge Worker | `radlib-edriffles-edge-production` from `deploy/radlib-edge-proxy/wrangler.jsonc` |
| Web implementation target | `https://social-edriffles.pages.dev` (private implementation target) |
| PDS implementation target | `https://pds.edriffles.us` (behind the public route; not a browser-facing product origin) |
| DNS/route status | `deploy/radlib-edge-proxy/wrangler.jsonc` binds the Plumbline custom domain and legacy compatibility routes |
| Public HTTPS probes | Re-run after each Pages upload; historical receipts do not prove this source revision |

The site is a static client. It does not replace the account PDS, repository,
AppView, resolver, feed provider, labeler, or messaging service. Those service
boundaries remain visible in the client and are configured separately.

The public artifact does not contain an owner personalization profile. New
accounts keep personalization and selected-feed state under their own account
DID on that device. A production build refuses to complete without an explicit
`EXPO_PUBLIC_DEFAULT_FEED_OWNER_DID` and `EXPO_PUBLIC_DEFAULT_FEED_RKEY`; the
release owner must review those public provider values as a neutral default,
not substitute an owner's personal feed or silently switch to an unrelated
operator's feed.

## Build

From the repository root:

```sh
cd upstream/social-app
EXPO_PUBLIC_ENV=production \
EXPO_PUBLIC_BRAND_NAME=Plumbline \
EXPO_PUBLIC_PUBLIC_WEB_ORIGIN=https://plumblines.uk \
EXPO_PUBLIC_ACCOUNT_SERVICE=https://plumblines.uk \
pnpm build-web
```

The deployment environment must additionally provide the explicit public
AppView identity and endpoint, the reviewed default-feed owner DID/rkey, and
the two acknowledged Spaces-alpha flags when the Community Board is enabled.
They are public configuration, not credentials, but must come from the
deployment's reviewed configuration store rather than from a developer's
personal shell. The production build fails closed if its public origin,
account-service origin, or default feed identity is missing or incorrect.

The static artifact is `upstream/social-app/web-build/`. It must be served at
the site root over HTTPS with an SPA fallback from unknown application routes
to `/index.html`. The post-build step also normalizes entrypoint asset URLs to
`/static/...`, which is required for direct visits to nested routes. The
production browser uses `plumblines.uk` for account and handle resolution,
while the OAuth metadata and callback remain on that same canonical origin.
The edge Worker routes its public PDS protocol paths to the PDS implementation
target; AppView, resolver, feed, and labeler services remain explicitly
configured service boundaries.

The two Spaces settings are intentionally required for this deployment: the
first activates the Space-backed community board and the second explicitly
acknowledges the alpha protocol in the production web bundle. This is an
operational alpha opt-in and does not waive the remaining Spaces credential,
revocation, interoperability, or production-readiness limitations.

The revocation-enabled PDS source also requires
`PDS_SPACE_CREDENTIAL_REVOCATION_ENABLED=1` in the disposable or separately
controlled staging PDS environment. It must not be enabled by changing the web
bundle alone; the PDS migration and source-built image must be deployed and
probed together.

## Re-deploying Pages

Cloudflare's direct-upload flow is the supported deployment path. From the
repository root, build the export and upload the resulting directory:

```sh
cd /var/home/tcs/Code/atproto/upstream/social-app
EXPO_PUBLIC_ENV=production \
EXPO_PUBLIC_BRAND_NAME=Plumbline \
EXPO_PUBLIC_PUBLIC_WEB_ORIGIN=https://plumblines.uk \
EXPO_PUBLIC_ACCOUNT_SERVICE=https://plumblines.uk \
pnpm build-web

cd /var/home/tcs/Code/atproto
python3 scripts/validate_contract.py
python3 scripts/validate_oauth_spaces_receipts.py
sha256sum -c artifacts/oauth-spaces-manifest.sha256
test -z "$(git status --porcelain)" || { echo 'release requires a clean root checkout'; exit 1; }
test -z "$(git -C upstream/social-app status --porcelain)" || { echo 'release requires a clean social-app checkout'; exit 1; }
test -z "$(git -C upstream/atproto-pds status --porcelain)" || { echo 'release requires a clean PDS checkout'; exit 1; }
: "${CLOUDFLARE_API_TOKEN:?Provide a short-lived Pages deployment token through the CI secret store}"
pnpm dlx wrangler@4.125.0 pages deploy upstream/social-app/web-build \
    --project-name=social-edriffles \
    --branch=main \
    --commit-message='Deploy Plumbline web client'
```

The Pages project remains the web implementation target. The public DNS route
must instead attach `plumblines.uk` to the Worker in
`deploy/radlib-edge-proxy/wrangler.jsonc`; the Worker then routes the SPA and
callback to Pages and PDS protocol paths to the PDS. Do not publish the
implementation target URLs as OAuth metadata, DID service endpoints, or
browser-facing account-service defaults.

Do not put PDS passwords, OAuth client secrets, service-auth secrets, or
recovery material in the web build environment. Do not extract tokens from a
local Wrangler cache or paste them into shell history. Supply only a short-lived
Pages deployment token through the CI secret store or an equivalent secret
manager, and revoke it after the upload.

Cloudflare Pages references: [Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/)
and [custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/).

## Current deployment evidence

Earlier Pages and PDS receipts tested pre-Plumbline source revisions or older
host topologies. They are historical evidence only and must not be used to
claim this release's public behavior.

Before marking a Plumbline upload current, bind the returned Pages deployment
URL and source commit in a credential-free receipt, then probe the returned URL
and `https://plumblines.uk/` for the Plumbline title, OAuth metadata, direct
post route, and public headers. A disposable-account OAuth walkthrough and a
Spaces revocation check remain separate, credential-gated acceptance lanes;
the Relay/AppView scan, short-TTL expiry/replay walkthrough, and independent
PLC-operator evidence remain external gates.

### Current release binding

The source builds an artifact containing the explicit account and community
Space read/write/manage scopes, the provider-owned `prompt=create` signup
option, browser OAuth callback initialization, the local account Space Lexicon
fixture, and strict validation for `us.edriffles.radlib.private.post`. The
source callback metadata binds `https://plumblines.uk/oauth/callback` and
`uk.plumblines:/oauth/callback`. A deployment receipt must record the specific
source and artifact digests after each upload; older successful uploads remain
historical evidence.

## Local fallback and start-on-login

Cloudflare Pages is the primary public host. A separate local fallback is also
configured outside the repository so the owner can run the same static export
on this machine without changing the public DNS record:

```sh
systemctl --user status social-edriffles-static.service cloudflared-social-edriffles.service
systemctl --user enable --now social-edriffles-static.service cloudflared-social-edriffles.service
```

The static fallback listens on `127.0.0.1:19008`. The dedicated tunnel is
`0da96e92-3e10-4632-ac82-d463e0f901de`, configured in
`~/.cloudflared/social-edriffles.yml`, and is enabled under the user's default
target. It is a rollback path only while Pages is primary; the existing
`idoldle` tunnel was not modified. Tunnel credentials remain outside the
repository at `~/.cloudflared/` and must never be committed.

The local development URL remains `http://127.0.0.1:19006/`; it is separate
from both the public Pages origin and the port-19008 static fallback.

## Product boundary

- `Plumbline` is the public brand and site name. The web descriptor is
  `Social client for the open web`.
- `Discover`, `Following`, and custom feeds retain their ordinary social-app
  names.
- Local curation is optional, device-local ordering/filtering over candidates
  supplied by the selected provider.
- Direct likes remain ordinary `app.bsky.feed.like` records on the user's PDS.
  The client now updates direct post/quote views optimistically while that PDS
  write is pending, then reconciles with the server result.
- Internal namespace strings such as `org.radical-liberal.*` remain in
  compatibility-sensitive schemas and tests; they are not a product slogan.
