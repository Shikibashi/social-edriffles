# Deployment Troubleshooting

- Bundle fails to load: verify HTTPS, `/index.html`, hashed asset paths, and SPA fallback.
- Route refresh returns 404: configure fallback only for application routes, not static assets.
- OAuth callback fails: verify canonical origin and registered HTTPS redirect; do not weaken state/PKCE checks.
- CSP blocks boot: compare required PDS/AppView/resolver/feed/labeler/OAuth destinations with `deploy/static-headers`.
- API unavailable after successful boot: identify the named remote actor; this is not automatically a hosting outage.
- Rollback: select the previous immutable deployment and verify its recorded checksum.
