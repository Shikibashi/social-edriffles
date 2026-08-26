# Social at `social.edriffles.us`

Status: `SOCIAL_USER_FACING_CUTOVER_DEPLOYED / OAUTH_CLIENT_LIVE / EXTERNAL_SPACES_APPVIEW_BROWSER_AND_EXPIRY_GATES_PENDING`

The public product name is **Social**. The radical-liberal constitutional
implementation remains documented and machine-readable internally, but the
web product does not advertise that implementation as its brand. User-facing
feed provenance calls the feature **local curation**; protocol/profile IDs are
unchanged for compatibility.

## Current single-host topology

The user-facing public contract is `https://social.edriffles.us`. The existing
Pages project and tunnel-backed PDS remain implementation targets behind the
edge Worker. `https://radlib.edriffles.us` remains the configured PDS/OAuth
protocol authority, not the browser-facing web origin.

| Boundary | Verified value |
|---|---|
| Pages project | `social-edriffles` |
| User-facing public origin | `https://social.edriffles.us` |
| OAuth/PDS protocol origin | `https://radlib.edriffles.us` |
| Registrable domain | `edriffles.us` (the only domain in scope) |
| Edge Worker | `radlib-edriffles-edge-production` from `deploy/radlib-edge-proxy/wrangler.jsonc` |
| Web implementation target | `https://social-edriffles.pages.dev` (private implementation target) |
| PDS resource/implementation alias | `https://pds.edriffles.us` (existing owner-DID resource alias; not an OAuth issuer) |
| DNS/route status | Verified and deployed in the existing `edriffles.us` Cloudflare zone |
| Public HTTPS probes | Passed for health, DID, OAuth discovery, metadata, XRPC, headers, and post routing |

The site is a static client. It does not replace the account PDS, repository,
AppView, resolver, feed provider, labeler, or messaging service. Those service
boundaries remain visible in the client and are configured separately.

The public artifact does not contain an owner personalization profile.
New accounts start with a neutral `Discover`/local-curation profile, and all
personalization and selected-feed state is keyed by the signed-in account DID
on that device. The deployed build intentionally leaves
`EXPO_PUBLIC_DEFAULT_FEED_OWNER_DID` unset until a real neutral feed-generator
record and provider are registered. This fails closed rather than silently
using the owner's feed or Bluesky's operator feed; logged-out visitors see a
neutral empty starting feed and can sign in or add their own feeds.

## Build

From the repository root:

```sh
cd upstream/social-app
EXPO_PUBLIC_ENV=production \
EXPO_PUBLIC_BRAND_NAME=Social \
EXPO_PUBLIC_PUBLIC_WEB_ORIGIN=https://social.edriffles.us \
EXPO_PUBLIC_APPVIEW_SERVICE_DID=did:web:api.bsky.app \
EXPO_PUBLIC_APPVIEW_SERVICE_FRAGMENT=bsky_appview \
EXPO_PUBLIC_APPVIEW_DISPLAY_NAME='Public Bluesky AppView (explicit read provider)' \
EXPO_PUBLIC_PUBLIC_APPVIEW_URL=https://api.bsky.app \
EXPO_PUBLIC_ACCOUNT_SERVICE=https://social.edriffles.us \
EXPO_PUBLIC_SPACES_ALPHA_ENABLED=0 \
pnpm build-web
```

The static artifact is `upstream/social-app/web-build/`. It must be served at
the site root over HTTPS with an SPA fallback from unknown application routes
to `/index.html`. The post-build step also normalizes entrypoint asset URLs to
`/static/...`, which is required for direct visits to nested routes. The browser
uses the single public origin for account/PDS paths. The edge Worker routes
those paths to the PDS implementation target; AppView, resolver, feed, and
labeler services remain explicitly configured service boundaries.

## Re-deploying Pages

Cloudflare's direct-upload flow is the supported deployment path. From the
repository root, build the export and upload the resulting directory:

```sh
cd /var/home/tcs/Code/atproto/upstream/social-app
EXPO_PUBLIC_ENV=production \
EXPO_PUBLIC_BRAND_NAME=Social \
EXPO_PUBLIC_PUBLIC_WEB_ORIGIN=https://social.edriffles.us \
EXPO_PUBLIC_APPVIEW_SERVICE_DID=did:web:api.bsky.app \
EXPO_PUBLIC_APPVIEW_SERVICE_FRAGMENT=bsky_appview \
EXPO_PUBLIC_APPVIEW_DISPLAY_NAME='Public Bluesky AppView (explicit read provider)' \
EXPO_PUBLIC_PUBLIC_APPVIEW_URL=https://api.bsky.app \
EXPO_PUBLIC_ACCOUNT_SERVICE=https://social.edriffles.us \
EXPO_PUBLIC_SPACES_ALPHA_ENABLED=0 \
pnpm build-web

cd /var/home/tcs/Code/atproto
python3 scripts/validate_contract.py
python3 scripts/validate_oauth_spaces_receipts.py
sha256sum -c artifacts/oauth-spaces-manifest.sha256
test -z "$(git status --porcelain)" || { echo 'release requires a clean root checkout'; exit 1; }
test -z "$(git -C upstream/social-app status --porcelain)" || { echo 'release requires a clean social-app checkout'; exit 1; }
test -z "$(git -C upstream/atproto-pds status --porcelain)" || { echo 'release requires a clean PDS checkout'; exit 1; }
: "${CLOUDFLARE_API_TOKEN:?Provide a short-lived Pages deployment token through the CI secret store}"
npx --yes wrangler@4.125.0 pages deploy upstream/social-app/web-build \
    --project-name=social-edriffles \
    --branch=main \
    --commit-message='Deploy Social web client'
```

The Pages project remains the web implementation target. The public DNS route
must instead attach `social.edriffles.us` to the Worker in
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

## Pre-cutover deployment evidence

The earlier Pages and PDS receipts tested the pre-cutover two-host topology.
They are retained as historical evidence only and are marked
`historical-superseded` in the receipt bundle. They do not prove the new public
host.

The current cutover receipt records the live checks and the credential-safe
browser boundary:

- the Worker configuration passes `wrangler deploy --dry-run` and the Worker
  is deployed as `radlib-edriffles-edge-production`;
- the source metadata registers `https://social.edriffles.us/oauth/callback`
  and `us.edriffles.social:/oauth/callback`;
- the public route, PDS host binding, deployed header probes, and public post
  route pass;
- the owner-handle browser flow reaches the PDS password screen with the
  canonical HTTPS client ID; browser password entry is not run by policy;
- the Relay/AppView scan, fresh credentialed Spaces proof, and short-TTL
  expiry/replay walkthrough remain external gates.

The direct official Node OAuth protocol walkthrough passes against the public
configured OAuth/PDS origin using a disposable identity, including callback, refresh, and
revocation. No production credential was used. The immutable receipt and
blocker state are recorded in
`artifacts/receipts/radlib-edge-cutover-pending.json`,
`artifacts/receipts/local-oauth-spaces-acceptance.json`, and
`artifacts/oauth-spaces-manifest.json`.

### Current local scope fix

The current working tree builds and deploys an artifact containing the explicit
account and community Space read/write/manage scopes, the provider-owned
`prompt=create` signup option, browser OAuth callback initialization, the local
account Space Lexicon fixture, and strict validation for
`us.edriffles.radlib.private.post`. The corrected Pages upload is deployed at
`social.edriffles.us`; the failed token attempt remains preserved as historical
evidence in
`artifacts/receipts/cloudflare-deploy-attempt.json`, while the successful upload
is recorded as a pre-cutover historical receipt in
`artifacts/receipts/cloudflare-deploy-success-7c5fcd1c.json`.

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

- `Social` is the public brand and site name.
- `Discover`, `Following`, and custom feeds retain their ordinary social-app
  names.
- Local curation is optional, device-local ordering/filtering over candidates
  supplied by the selected provider.
- Direct likes remain ordinary `app.bsky.feed.like` records on the user's PDS.
  The client now updates direct post/quote views optimistically while that PDS
  write is pending, then reconciles with the server result.
- Internal namespace strings such as `org.radical-liberal.*` remain in
  compatibility-sensitive schemas and tests; they are not a product slogan.
