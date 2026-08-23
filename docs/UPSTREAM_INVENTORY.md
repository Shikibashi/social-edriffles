# Upstream Inventory

| Project | Local path | Relation | Pinned/current SHA | Remote |
|---|---|---|---|---|
| bluesky-social/social-app | `upstream/social-app` | merged fork main + radical-liberal branch + opt-in Spaces adapter | `4ede0504` | `https://github.com/Shikibashi/social-app` |
| bluesky-social/atproto PDS | `upstream/atproto-pds` | `permissioned-data` base + Spaces product integration | `d906e959` | `https://github.com/Shikibashi/atproto` |

The canonical machine-readable baseline is `artifacts/upstream-baseline.json`. The `baseSha` fields retain the upstream provenance; `forkSha` and `upstream-pins.json` `checkoutCommit` fields identify the reviewed local feature commits. `python3 scripts/check_upstream.py --fast` is read-only and reports whether local trees match those commits. AppViewLite and FishyFlip were retired from the tracked dependency graph; any preserved checkout is historical evidence only. Ordinary npm/pnpm packages are dependencies, not source forks, and are excluded from this inventory. The Spaces base is an explicitly pinned alpha branch, not a moving `main` head.
