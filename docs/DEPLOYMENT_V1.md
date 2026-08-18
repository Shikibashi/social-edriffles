# Deployment v1

Official target: static HTTPS hosting, compatible with Cloudflare Pages or any equivalent static host. Core application code is vendor-neutral. Build and validate from a clean pinned SHA:

```sh
cd upstream/social-app
pnpm install --frozen-lockfile
EXPO_PUBLIC_ENV=production pnpm build-web
```

Publish `web-build/` atomically. Configure SPA fallback for non-file routes, preserve `/manifest.json` and hashed assets, apply `deploy/static-headers`, and retain the previous immutable deployment for rollback. Staging uses a distinct origin and `EXPO_PUBLIC_ENV=staging`; production uses a distinct origin and `production`. No hosting credentials are stored in the repository. External provider deployment is `READY-BUT-NOT-EXECUTED` when credentials are unavailable.

Production acceptance requires the artifact checksum, source SHA, environment, deployment ID, headers, route smoke, and post-deploy receipt to match.
