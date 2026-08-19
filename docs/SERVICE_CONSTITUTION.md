# Service Constitution

## Status

The authenticated service-auth boundary and persisted provider-switching model
are implemented in the pinned forks. The first-party PDS is now the pinned
official `@atproto/pds` source under `upstream/atproto-pds`, with the governed
listblock write policy enabled explicitly by deployment configuration.
AppViewLite is retired and is not an account host or read-side deployment
option. The client remains compatible with explicitly selected AppView/feed
providers. The constitution remains subject to the imported-repository
activation gate and final owner walkthrough.

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
11. The PDS is the authority for DID-authenticated repository writes, CAR
    import/export, sync, and account state; an AppView cannot silently replace
    it.
12. A selected AppView may provide private list-mute state, but it must not be
    represented as PDS repository state or as universal moderation authority.

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
  enabled: boolean
}
```

The built-in provider is the configured first-party Project AppView. Its DID,
service fragment, and endpoint are explicit deployment configuration; missing
production configuration is unavailable rather than a hidden stock provider.
Custom providers require validated DID/service resolution, HTTPS where
applicable, bounded requests, safe redirects, and no arbitrary credential
forwarding. Retired providers are not registered or selectable.

## Current gap

`docs/SERVICE_AUTH_CURRENT_STATE.md` records the verified bearer behavior and live HTTP evidence. Remaining closure requires the complete A/B/C presentation regression, provider failure/unsupported-endpoint tests, and final quality gates.
