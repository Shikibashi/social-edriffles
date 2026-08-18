# Self-hosting Web

Build the static artifact with the documented `pnpm build-web` command and serve `web-build/` from any HTTPS static host. Configure the host's SPA fallback and headers; no proprietary hosting API is required. Set the canonical public origin and register its OAuth redirect with the selected authentication service. Keep PDS/AppView/feed/resolver settings in the existing application configuration rather than coupling them to the hosting provider.
