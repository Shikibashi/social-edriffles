# Plumbline edge route

This Worker serves the user-facing Plumbline web client and OAuth/PDS protocol
authority at `https://plumblines.uk`. The former `social.edriffles.us` and
`radlib.edriffles.us` hosts remain compatibility aliases during the cutover;
the PDS/account service is served at the canonical root route and retains
`pds.edriffles.us` as an existing identity-resource alias.

Web paths on `https://social.edriffles.us` and `https://radlib.edriffles.us` are
retained as compatibility entry points and permanently redirect to Plumbline
while preserving the path and query string. Protocol paths on the canonical
host are proxied to the PDS/OAuth issuer.

## Routing contract

| Public path | Upstream | Reason |
| --- | --- | --- |
| `/`, static assets, SPA routes, `/oauth/callback`, and `/oauth-client-metadata.json` | Cloudflare Pages | Web client and registered browser callback |
| `/.well-known/*`, `/xrpc/*`, `/_health`, `/oauth/*` except `/oauth/callback`, and `/@atproto/oauth-provider/*` | PDS | DID, OAuth provider page/assets, sign-in/consent API, PAR, token, revocation, and AT Protocol APIs |
| Web paths on `social.edriffles.us` and `radlib.edriffles.us` | Worker redirect | Compatibility URLs to `plumblines.uk` |

For canonical Social post routes (`/profile/:handleOrDID/post/:rkey`), the
Worker resolves the public post through `APPVIEW_ORIGIN` and enriches the Pages
HTML shell with Plumbline-branded Open Graph and Twitter-card metadata. This is
the metadata contract used by chat clients and link unfurlers: author, post
text, post media, timestamp, likes, replies, and reposts are exposed for public
posts. AppView failures leave the normal SPA shell intact, so a provider outage
does not turn a working web route into a 5xx response. Author-authenticated and
sensitive-labeled posts intentionally receive only the minimal/private preview
metadata used by the existing bskyweb implementation.

The two upstream URLs in `wrangler.jsonc` are implementation targets only. They
must not appear in the OAuth client metadata or in the public DID service
document after cutover. No secret, token, credential, or Cloudflare API key is
stored in this configuration.

## Validate and deploy

From the repository root:

```sh
npx --yes wrangler@latest types --config deploy/radlib-edge-proxy/wrangler.jsonc
npx --yes wrangler@latest deploy --dry-run --config deploy/radlib-edge-proxy/wrangler.jsonc --env production
npx --yes wrangler@latest deploy --config deploy/radlib-edge-proxy/wrangler.jsonc --env production
```

The focused metadata regression tests run without project dependencies:

```sh
node --experimental-strip-types --test deploy/radlib-edge-proxy/src/post-metadata.test.ts
```

With the current Wrangler release, `deploy --dry-run` is the bundle and
configuration gate used for this Worker. The production Worker is deployed
with the `radlib.edriffles.us`, `social.edriffles.us`, and `pds.edriffles.us`
routes in the existing `edriffles.us` zone, plus the `plumblines.uk` custom
domain in the separately controlled `plumblines.uk` zone.

The deployed `pds.edriffles.us` route is an identity-resource compatibility
bridge because the owner's existing PLC DID still names that host. Its
protected-resource metadata points to the canonical
`plumblines.uk` authorization server; it is not a second OAuth issuer.

## PDS cutover requirements

The disposable PDS behind the selected tunnel/origin is configured with:

```text
PDS_HOSTNAME=plumblines.uk
PDS_SERVICE_DID=did:web:plumblines.uk
PDS_PUBLIC_URL_ALIASES=https://pds.edriffles.us,https://radlib.edriffles.us
```

The reverse-proxy path must preserve the public resource host as a trusted
`X-Forwarded-Host` value. The Worker preserves each known protocol alias (in
particular `pds.edriffles.us`) for PDS requests, then removes the caller's
`Host` header. This is required for OAuth DPoP: the PDS reconstructs the URL
from the forwarded host, and that URL must match the host signed by the client.
Keep the old PDS origin private or restricted to the trusted tunnel path; a
publicly writable forwarded-host header would defeat the PDS host-binding
check. Every protocol alias exposed by the Worker must also be listed in the
PDS's `PDS_PUBLIC_URL_ALIASES` configuration.

The public health, DID, OAuth discovery, metadata, XRPC, header, and post-route
probes must pass across the user-facing and protocol `https://plumblines.uk`
route and the compatibility `https://pds.edriffles.us` route. Credentialed Spaces,
Relay/AppView, browser-password, and short-TTL expiry/replay receipts remain
required before any production-ready claim.
