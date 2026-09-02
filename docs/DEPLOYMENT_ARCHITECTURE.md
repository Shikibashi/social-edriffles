# Deployment Architecture

The Daily Driver web artifact is a static Expo web SPA. The build entrypoint is `upstream/social-app/package.json` script `build-web`; output is `upstream/social-app/web-build`. The host serves immutable hashed assets and an HTML shell. Unknown application routes must fall back to `/index.html`; static files and protocol metadata must remain direct files.

The browser talks directly to configured ATProto services (first-party PDS,
selected AppView, resolver, feeds, labelers, and OAuth endpoints). The
first-party deployment uses the pinned official PDS base with
`PDS_RADLIB_MODERATION_WRITE_POLICY=deny-create-update`; the retired AppViewLite
service is not part of the deployment graph and cannot replace the PDS.
No application server is required for the static client deployment. Build-time
public variables include `EXPO_PUBLIC_ENV`, `EXPO_PUBLIC_RELEASE_VERSION`,
`EXPO_PUBLIC_APPVIEW_SERVICE_DID`, `EXPO_PUBLIC_APPVIEW_SERVICE_FRAGMENT`,
and `EXPO_PUBLIC_PUBLIC_APPVIEW_URL`; secrets must never be public build
variables. Production binds
`EXPO_PUBLIC_ACCOUNT_SERVICE=https://plumblines.uk` for login and handle
resolution; this is not a public-read provider. The edge Worker forwards the
public account/PDS paths to `pds.edriffles.us` as an implementation target, so
that hostname must not be substituted into browser metadata or build defaults.
OAuth requires the canonical `https://plumblines.uk` origin and its registered
web and reverse-domain callbacks.
