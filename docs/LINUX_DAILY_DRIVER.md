# Linux Daily Driver

The lowest-maintenance supported Linux path is the browser web client: install Node 24.19+ and pnpm 11.21+, run `pnpm install --frozen-lockfile`, then `pnpm web` for development or deploy the output from `EXPO_PUBLIC_ENV=production pnpm build-web` to a static HTTPS host. A packaged desktop binary is not part of v1. OAuth redirects must target the configured HTTPS deployment origin. Browser storage follows the existing social-app session model; do not treat it as an encrypted credential vault.
