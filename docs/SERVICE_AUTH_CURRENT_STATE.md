# Service Authentication: Current State

Date: 2026-08-17.

## Social-app routing

The pinned social-app fork (`56b346e49`) currently builds three clients over one `PasswordSession` in `src/state/session/session-core.ts`:

- `buildAppviewClient(agent)` mints an endpoint-scoped service-auth token from the account PDS and sends it to the configured AppView endpoint.
- `buildPdsClient(agent)` sets no service, so repo/server/identity calls stay on the account host.
- `buildChatClient(agent)` sets `service: CHAT_PROXY_SERVICE`.
- `getPublicAppviewClient()` is a process-wide unauthenticated public client using `PUBLIC_BSKY_SERVICE`.
- `routeSessionToPds()` pins the stored PDS URL while preserving the session's auth and refresh behavior.
- The configured AppView endpoint defaults to `https://api.bsky.app`; `BLUESKY_PROXY_DID` supplies the service-auth audience and `atproto-proxy` service identity.

PDS writes are independent: `buildPdsClient` has no proxy service and `createLexClient` record helpers force `service: null`. Sessions and account records are persisted through `src/state/persisted/schema.ts` and `src/state/session/index.tsx`; no persisted AppView provider selection exists.

## AppViewLite authenticated request flow

The pinned AppViewLite fork (`f0ef9be`) now verifies `/xrpc` bearer requests in middleware before session construction:
1. The social-app client requests `com.atproto.server.getServiceAuth` from the account PDS for the exact AppView DID and XRPC method.
2. It sends only the short-lived service-auth JWT to the AppView.
3. AppViewLite verifies the JWT signature against the issuer DID document, validates claims and replay nonce, and creates a read-only viewer session.
4. A raw PDS access JWT is rejected.

`BlueskyEnrichedApis.TryGetSessionFromCookie` remains the cookie-only path. Authenticated XRPC bearer requests are verified by middleware before session construction; raw bearer strings are no longer compared against stored PDS `AccessJwt` values.

The current implementation therefore:

| Requirement | Current state |
|---|---|
| Raw PDS access JWT accepted | No; rejected at the AppView middleware boundary |
| JWT signature verified | Yes, ES256K secp256k1 |
| DID authorized signing key verified | Yes, via issuer DID document `#atproto` |
| `iss`/`sub` issuer consistency | `iss` is required and must be a valid DID |
| `aud` validated | Yes, exact configured AppView service DID |
| endpoint-specific `lxm` validated | Yes, exact XRPC method path |
| `exp` validated | Yes, with bounded clock skew |
| `iat` sanity validated | Yes |
| `jti` replay protection | Yes, in-memory until token expiry |
| service DID/audience bound | Yes for the configured AppView service |
| password/app password forwarded | No; PDS access token is used only for PDS-side service-auth minting |

The AppViewLite `com.atproto.server.getServiceAuth` compatibility endpoint in `src/AppViewLite.Web/ApiCompat/ComAtprotoServer.cs` remains `NotImplementedException` by design: service-auth tokens are minted by the account PDS, not by the AppView. The social-app client calls the account PDS endpoint directly before each AppView request.

## Boundary decision

The authenticated boundary is now enforced for AppView XRPC requests in `upstream/AppViewLite/src/AppViewLite.Web/Program.cs`: raw bearer access JWTs are rejected, while verified service-auth JWTs create read-only AppView sessions. `ServiceAuthVerifier` validates ES256K, issuer DID/key, audience, endpoint `lxm`, `exp`, `iat`, `jti` replay, and DID-document resolution. The social-app session client mints an endpoint-scoped service-auth token through the PDS before each AppView request and sends only that token to the AppView endpoint. Live local evidence: a fresh PDS-issued ES256K token returned HTTP 200 for `app.bsky.feed.getTimeline`; the raw PDS access JWT returned HTTP 500 and was not accepted.
