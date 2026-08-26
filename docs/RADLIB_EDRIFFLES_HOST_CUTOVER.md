# Social user-facing host and Radlib protocol authority

Status: `SOCIAL_USER_FACING_CUTOVER_DEPLOYED / OAUTH_CLIENT_LIVE / EXTERNAL_SPACES_APPVIEW_AND_EXPIRY_GATES_PENDING`

The canonical user-facing web and OAuth client origin for this fork is:

```text
https://social.edriffles.us
```

`edriffles.us` remains the only registrable domain. No second domain is part of
this design. The configured PDS/OAuth protocol authority remains
`https://radlib.edriffles.us`; this preserves the existing `did:web` service
identity and Radlib namespace while the browser-facing site lives at Social.

The former public Radlib web URL is retained as a compatibility entry point.
The edge Worker redirects its web paths to `https://social.edriffles.us`,
preserving paths and query strings. Radlib protocol paths remain available for
the configured PDS/OAuth issuer; this is not a second registrable domain.

## Naming contract

The public hostname and the AT Protocol namespace are deliberately different
strings because AT Protocol NSIDs use reverse-DNS order:

| Purpose | Value |
|---|---|
| User-facing web/client origin | `https://social.edriffles.us` |
| OAuth/PDS protocol origin | `https://radlib.edriffles.us` |
| `did:web` service host | `radlib.edriffles.us` |
| Lexicon/NSID authority | `us.edriffles.radlib` |
| Fork Lexicons | `us.edriffles.radlib.*` |
| Browser OAuth metadata/callback | `https://social.edriffles.us/oauth-client-metadata.json` / `https://social.edriffles.us/oauth/callback` |
| Native OAuth callback scheme | `us.edriffles.social:/oauth/callback` |
| DNS Lexicon authority record | `_lexicon.radlib.edriffles.us` |

`us.edriffles.radlib` is an NSID authority, not a hostname. The repository
must not invent an `edriffles.radlib` hostname or claim a separate registrable
domain.

## Single-host routing

`deploy/radlib-edge-proxy/` contains the Cloudflare Worker cutover:

- web root, static assets, SPA routes, `/oauth/callback`, and
  `/oauth-client-metadata.json` go to the existing Pages implementation target;
- `/.well-known/*`, `/xrpc/*`, `/_health`, and OAuth provider routes other than
  the browser callback go to the PDS implementation target;
- the Worker removes the caller-controlled `Host` header and sets the fixed
  PDS `X-Forwarded-Host` to `radlib.edriffles.us`;
- web paths on `radlib.edriffles.us` redirect permanently to the user-facing
  `social.edriffles.us` origin, while protocol paths continue to serve the
  configured OAuth/PDS issuer;
- the user-facing Social origin can proxy account/PDS paths to the same PDS
  implementation target without changing its protocol identity;
- the deployed disposable PDS is configured with
  `PDS_HOSTNAME=radlib.edriffles.us` and
  `PDS_SERVICE_DID=did:web:radlib.edriffles.us`.

The owner's existing PLC DID still declares `pds.edriffles.us` as its PDS
resource. The Worker serves standards-valid protected-resource metadata at
that existing alias and points it to the canonical `radlib.edriffles.us`
authorization server. This is a migration compatibility bridge, not a second
OAuth issuer or a second registrable domain; the owner-controlled PLC service
endpoint can be changed later when that identity authority is available.

The upstream URLs in the Worker configuration are implementation targets only.
They must not appear in public OAuth metadata, the public DID service endpoint,
or the browser-facing account-service default.

## Local validation

Run from the repository root:

```sh
npx --yes wrangler@latest types --config deploy/radlib-edge-proxy/wrangler.jsonc
npx --yes wrangler@latest deploy --dry-run --config deploy/radlib-edge-proxy/wrangler.jsonc --env production
python3 scripts/validate_contract.py
python3 scripts/validate_oauth_spaces_receipts.py
```

The dry run validates the Worker bundle and configuration. The current live
deployment and public probes are recorded in the cutover receipt; they do not
replace credentialed Spaces, AppView, or short-TTL expiry/replay evidence.

## External completion sequence

1. The `radlib.edriffles.us`, `social.edriffles.us`, and existing
   `pds.edriffles.us` routes are deployed in the `edriffles.us` Cloudflare zone.
2. The disposable PDS hostname and `did:web` service DID are configured, and
   the public health, DID, OAuth, metadata, and XRPC probes pass.
3. The `us.edriffles.radlib.*` authority is independently verified through the
   `_lexicon.radlib.edriffles.us` TXT record and the checked-in schema
   repository.
4. The official disposable Node OAuth flow passes discovery, PAR, PKCE S256,
   DPoP, callback, refresh, and revocation. The browser handoff reaches the
   PDS password UI; password entry remains intentionally unrun in the browser
   lane.
5. Run the controlled Relay/AppView canary scan and record whether the public
   AppView response is a privacy pass rather than an HTTP 403 inconclusive
   result.
6. Run the credentialed Spaces removal test and retain the explicit
   already-issued-credential behavior as either an accepted alpha limitation or
   a remediated revocation result.

The release manifest remains blocked only by the external Spaces, AppView,
browser-credential, and expiry/replay gates. The pre-cutover Pages and PDS
receipts are retained as historical evidence and are not reclassified as
evidence for the Social user-facing origin.
