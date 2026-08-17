# Service Constitution

## Status

The authenticated service-auth boundary and persisted provider-switching model are implemented in the pinned forks. The constitution remains subject to the remaining live A/B/C presentation regression and final quality-gate audit.

## Principles

1. The account host (PDS) and AppView are separate authorities.
2. Changing an AppView never requires changing the PDS or migrating account records.
3. Raw PDS access/refresh tokens, passwords, and app passwords never flow to an AppView.
4. Viewer identity is cryptographically authenticated with a DID-authorized service-auth key.
5. AppView identity is DID-bound and its endpoint/service fragment are validated together.
6. Provider changes are explicit, persisted per account/device, and visible to the user.
7. Unsupported features never silently change provider.
8. Provider failures cannot alter PDS account data or local personalization.
9. AppViews are replaceable services, not account hosts.
10. Users can exit to another provider or directly to their PDS without logout or migration.

## Required service-auth contract

Authenticated XRPC requests must use a verified service-auth JWT, not a raw PDS access JWT. Verification must bind issuer DID, authorized signing key and accepted algorithm, service audience, endpoint `lxm`, expiration, issued-at sanity, and replay policy (`jti`). Invalid signatures, DIDs, audiences, lexicons, timestamps, keys, and replays are rejected.

## Required provider record

```ts
interface AppViewProvider {
  id: string
  displayName: string
  serviceDid: string
  serviceFragment: string
  endpoint: string
  builtin: boolean
}
```

Built-ins are Bluesky AppView and the project AppView. Custom providers require validated DID/service resolution, HTTPS where applicable, bounded requests, safe redirects, and no arbitrary credential forwarding.

## Current gap

`docs/SERVICE_AUTH_CURRENT_STATE.md` records the verified bearer behavior and live HTTP evidence. Remaining closure requires the complete A/B/C presentation regression, provider failure/unsupported-endpoint tests, and final quality gates.
