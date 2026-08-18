# Default Configuration

Production defaults use `EXPO_PUBLIC_ENV=production`, `DEFAULT_SERVICE=https://bsky.social`, and `APPVIEW_ENDPOINT=https://api.bsky.app` from the existing client constants. Development defaults are selected only when `EXPO_PUBLIC_ENV` is absent or explicitly `development`; e2e uses `EXPO_PUBLIC_ENV=e2e`. No production default points at localhost, fixture providers, or test credentials. AppView/feed/provider switching remains explicit and provenance-bearing.

`EXPO_PUBLIC_RELEASE_VERSION` is optional and derives from package metadata when absent. Never put OAuth, refresh, session, or service-auth secrets in public build variables.
