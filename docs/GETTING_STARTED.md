# Getting Started

```sh
cd upstream/social-app
corepack enable
pnpm install
pnpm web
```

Open the local Expo web URL and sign in through the existing account flow. For a production-like static bundle use `EXPO_PUBLIC_ENV=production pnpm build-web`; the output is generated under the social-app web export directory. Configure only documented environment inputs; do not place tokens or passwords in `.env` files.

The root contract gate is `python3 scripts/validate_contract.py` and the root regression suite is `python3 -m unittest discover -s tests -p 'test_*.py'`.
