# Service Authentication: Current State

Date: 2026-08-17.

## Social-app routing

The pinned social-app fork (`bde69aa15102640b0e898653a505191acc4951a9`) currently builds three clients over one `PasswordSession` in `src/state/session/session-core.ts`:

- `buildAppviewClient(agent)` in `src/state/session/clients.ts` sets `service: BLUESKY_PROXY_HEADER`.
- `buildPdsClient(agent)` sets no service, so repo/server/identity calls stay on the account host.
- `buildChatClient(agent)` sets `service: CHAT_PROXY_SERVICE`.
- `getPublicAppviewClient()` is a process-wide unauthenticated public client using `PUBLIC_BSKY_SERVICE`.
- `routeSessionToPds()` pins the stored PDS URL while preserving the session's auth and refresh behavior.

`BLUESKY_PROXY_HEADER` is `${BLUESKY_PROXY_DID}#bsky_appview`, with `BLUESKY_PROXY_DID` defaulting to `did:web:api.bsky.app`. `PUBLIC_BSKY_SERVICE` is `https://public.api.bsky.app`. The service value causes `@atproto/lex` to emit `atproto-proxy`; it does not itself provide a provider registry or provider-switching model.

PDS writes are independent: `buildPdsClient` has no proxy service and `createLexClient` record helpers force `service: null`. Sessions and account records are persisted through `src/state/persisted/schema.ts` and `src/state/session/index.tsx`; no persisted AppView provider selection exists.

## AppViewLite authenticated request flow

The pinned AppViewLite fork (`45d6a0c913de53ae3397e12d5f30b41805961af3`) handles `/xrpc` bearer requests in `src/AppViewLite.Web/Program.cs`, `TryGetSessionCookie`:

1. Reads `Authorization: Bearer ...`.
2. Calls `JwtSecurityTokenHandler.ReadJwtToken`.
3. Reads `sub`, or falls back to `iss`, as the viewer DID.
4. Checks only that the selected string passes `BlueskyEnrichedApis.IsValidDid`.
5. Stores the unverified bearer string in `SessionIdWithUnverifiedDid`.

`BlueskyEnrichedApis.TryGetSessionFromCookie` and `AppViewLiteUserContext.TryGetAppViewLiteSession` in `src/AppViewLite/AppViewLiteSession.cs` compare the raw bearer string against a stored PDS `AccessJwt` or an AppViewLite cookie token. There is no cryptographic service-auth verification at this boundary.

The current implementation therefore:

| Requirement | Current state |
|---|---|
| Raw PDS access JWT accepted | Yes, when it matches the stored PDS session token or reaches a request path that derives identity from it |
| JWT signature verified | No |
| DID authorized signing key verified | No |
| `iss`/`sub` issuer consistency | No; `sub` or `iss` is selected heuristically |
| `aud` validated | No |
| endpoint-specific `lxm` validated | No |
| `exp` validated | No at the bearer boundary |
| `iat` sanity validated | No |
| `jti` replay protection | No |
| service DID/audience bound | No |
| password/app password forwarded | The AppViewLite login UI accepts credentials for its own login flow; the social-app proxy path does not intentionally send passwords, but the raw PDS access token remains bearer material |

The `com.atproto.server.getServiceAuth` compatibility endpoint in `src/AppViewLite.Web/ApiCompat/ComAtprotoServer.cs` is currently `NotImplementedException`, so the service-auth issuance/verification handshake is not available. This is a security blocker, not evidence that a token-shaped bearer is safe.

## Boundary decision

Do not enable alternate-AppView authenticated routing until service-auth issuance, DID-bound signature verification, audience/lxm/expiry/replay checks, provider identity, and explicit switching are implemented together. A proxy DID header alone is routing metadata; it is not authentication.
