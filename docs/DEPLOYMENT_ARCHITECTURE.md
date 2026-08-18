# Deployment Architecture

The Daily Driver web artifact is a static Expo web SPA. The build entrypoint is `upstream/social-app/package.json` script `build-web`; output is `upstream/social-app/web-build`. The host serves immutable hashed assets and an HTML shell. Unknown application routes must fall back to `/index.html`; static files and protocol metadata must remain direct files.

The browser talks directly to configured ATProto services (PDS, AppView, resolver, feeds, labelers, OAuth endpoints). No application server is required for the static deployment. Build-time public variables include `EXPO_PUBLIC_ENV`, `EXPO_PUBLIC_RELEASE_VERSION`, and `EXPO_PUBLIC_APPVIEW_ENDPOINT`; secrets must never be public build variables. OAuth requires an HTTPS canonical origin and registered redirect configuration.
