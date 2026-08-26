# Social/Radlib edge route

This Worker serves the user-facing Social web client at
`https://social.edriffles.us` and preserves `radlib.edriffles.us` as the
configured OAuth/PDS protocol authority. `edriffles.us` remains the only
registrable domain in this topology.

Web paths on `https://radlib.edriffles.us` are retained as a compatibility entry
point and permanently redirect to Social while preserving the path and query
string. Radlib protocol paths remain available for the configured PDS/OAuth
issuer.

## Routing contract

| Public path | Upstream | Reason |
| --- | --- | --- |
| `/`, static assets, SPA routes, `/oauth/callback`, and `/oauth-client-metadata.json` | Cloudflare Pages | Web client and registered browser callback |
| `/.well-known/*`, `/xrpc/*`, `/_health`, `/oauth/*` except `/oauth/callback`, and `/@atproto/oauth-provider/*` | PDS | DID, OAuth provider page/assets, sign-in/consent API, PAR, token, revocation, and AT Protocol APIs |
| Web paths on `radlib.edriffles.us` | Worker redirect | Compatibility URL to `social.edriffles.us` |

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

With the current Wrangler release, `deploy --dry-run` is the bundle and
configuration gate used for this Worker. The production Worker is deployed
with the `radlib.edriffles.us`, `social.edriffles.us`, and
`pds.edriffles.us` routes in the existing `edriffles.us` zone.

The deployed `pds.edriffles.us` route is an identity-resource compatibility
bridge because the owner's existing PLC DID still names that host. Its
protected-resource metadata points to the canonical
`radlib.edriffles.us` authorization server; it is not a second OAuth issuer.

## PDS cutover requirements

The disposable PDS behind the selected tunnel/origin is configured with:

```text
PDS_HOSTNAME=radlib.edriffles.us
PDS_SERVICE_DID=did:web:radlib.edriffles.us
PDS_PUBLIC_URL_ALIASES=https://pds.edriffles.us
```

The reverse-proxy path must preserve the public host as a trusted
`X-Forwarded-Host` value. The Worker sets the Radlib host for OAuth issuer
requests and the `pds.edriffles.us` host for PDS resource requests, then
removes the caller's `Host` header. Keep the old PDS origin private or
restricted to the trusted tunnel path; a publicly writable forwarded-host
header would defeat the PDS host-binding check.

The public health, DID, OAuth discovery, metadata, XRPC, header, and post-route
probes pass across the user-facing `https://social.edriffles.us` route and the
protocol `https://radlib.edriffles.us` route. Credentialed Spaces,
Relay/AppView, browser-password, and short-TTL expiry/replay receipts remain
required before any production-ready claim.
