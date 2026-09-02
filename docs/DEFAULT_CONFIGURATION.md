# Default Configuration

Production defaults use `EXPO_PUBLIC_ENV=production` and the public account
entryway `EXPO_PUBLIC_ACCOUNT_SERVICE=https://plumblines.uk` only for login and
handle availability. The edge Worker routes that public path to the PDS
implementation target; it does not make the PDS implementation hostname a
browser default. Public reads require an explicitly configured
first-party AppView:
`EXPO_PUBLIC_APPVIEW_SERVICE_DID`,
`EXPO_PUBLIC_APPVIEW_SERVICE_FRAGMENT`, and
`EXPO_PUBLIC_PUBLIC_APPVIEW_URL`. An unset production AppView is an explicit
unavailable configuration; it never falls back to `api.bsky.app`.

A first-party deployment must replace the account-host/PDS configuration with
its own PDS and set `PDS_RADLIB_MODERATION_WRITE_POLICY=deny-create-update`;
AppViewLite is retired and is neither a required nor an implicit service.
Development defaults are selected only when `EXPO_PUBLIC_ENV` is absent or
explicitly `development`; e2e uses `EXPO_PUBLIC_ENV=e2e`. No production default
points at localhost, fixture providers, or retired services. AppView/feed/
provider switching remains explicit and provenance-bearing.

`EXPO_PUBLIC_RELEASE_VERSION` is optional and derives from package metadata when absent. Never put OAuth, refresh, session, or service-auth secrets in public build variables.
