# Social at `social.edriffles.us`

Status: `CLOUDFLARE_PAGES_ACTIVE`

The public product name is **Social**. The radical-liberal constitutional
implementation remains documented and machine-readable internally, but the
web product does not advertise that implementation as its brand. User-facing
feed provenance calls the feature **local curation**; protocol/profile IDs are
unchanged for compatibility.

## Verified Cloudflare deployment

The production web export is deployed to the Cloudflare Pages project
`social-edriffles`.

| Boundary | Verified value |
|---|---|
| Pages project | `social-edriffles` |
| Pages deployment | `https://99d240b7.social-edriffles.pages.dev` |
| Custom domain | `https://social.edriffles.us` |
| DNS | `social.edriffles.us CNAME social-edriffles.pages.dev` |
| Pages custom-domain status | `active` (verification and validation active) |
| Root HTTPS probe | HTTP `200`; `server: cloudflare` |
| SPA deep-route probe | `/settings/personalization` HTTP `200`; root-relative assets load on a direct visit |
| Metadata probe | title/application name `Social`; description `A user-controlled social network client.` |

The site is a static client. It does not replace the account PDS, repository,
AppView, resolver, feed provider, labeler, or messaging service. Those service
boundaries remain visible in the client and are configured separately.

The production artifact does not contain an owner personalization profile.
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
EXPO_PUBLIC_ACCOUNT_SERVICE=https://bsky.social \
pnpm build-web
```

The static artifact is `upstream/social-app/web-build/`. It must be served at
the site root over HTTPS with an SPA fallback from unknown application routes
to `/index.html`. The post-build step also normalizes entrypoint asset URLs to
`/static/...`, which is required for direct visits to nested routes. The browser
continues to talk directly to the configured
PDS, AppView, resolver, feed, and labeler services; the hosting site is not a
new service authority.

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
EXPO_PUBLIC_ACCOUNT_SERVICE=https://bsky.social \
pnpm build-web

cd /var/home/tcs/Code/atproto
set +x
cloudflare_token="$(python3 - <<'PY'
import pathlib, tomllib
print(tomllib.loads((pathlib.Path.home()/'.config/.wrangler/config/default.toml').read_text())['oauth_token'])
PY
)"
CLOUDFLARE_API_TOKEN="$cloudflare_token" \
  npx --yes wrangler@latest pages deploy upstream/social-app/web-build \
    --project-name=social-edriffles \
    --branch=main \
    --commit-message='Deploy Social web client' \
    --commit-dirty
unset cloudflare_token CLOUDFLARE_API_TOKEN
```

The Cloudflare Pages custom domain must remain attached to the project and the
`social` DNS record must continue to point to `social-edriffles.pages.dev`.
Cloudflare provisions TLS and serves extensionless application routes through
the static SPA fallback. If the Pages control plane ever reports a stale domain
state, check the DNS target first, then re-verify the custom domain in Pages;
do not silently route the public hostname to a different provider.

Do not put PDS passwords, OAuth client secrets, service-auth secrets, or
recovery material in the web build environment. The token extraction above
reads Wrangler's local OAuth cache without printing it; use an appropriate
short-lived deployment token in CI instead.

Cloudflare Pages references: [Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/)
and [custom domains](https://developers.cloudflare.com/pages/configuration/custom-domains/).

## Latest deployment verification

On 2026-08-19, the production export was uploaded through the authorized
Cloudflare MCP to deployment `99d240b7-66fa-40d8-a176-fec18bbc1b25`.
Cloudflare reported the production deployment stage as `success`; the custom
hostname cache was then purged by hostname so previously cached SPA shells did
not mask the new export.

Verified externally on both the custom hostname and deployment hostname:

- `/settings/personalization` returns HTTP `200`;
- its shell references `/static/js/main.f757c6d4.js` rather than a route-relative
  asset path;
- the emitted bundle contains the generic curation-term controls;
- retired owner-specific weight labels and bundled political term-pack labels
  are absent;
- the signed-in in-app browser loaded the direct settings URL and rendered
  `Feed customization & data`, `Add a term to prioritize`, and `Add term`.

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
from both the production Pages origin and the port-19008 static fallback.

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
