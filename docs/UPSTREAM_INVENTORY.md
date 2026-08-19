# Upstream Inventory

| Project | Local path | Relation | Pinned/current SHA | Remote |
|---|---|---|---|---|
| bluesky-social/social-app | `upstream/social-app` | direct fork | `c38bfe51` | `https://github.com/bluesky-social/social-app` |
| bluesky-social/atproto PDS | `upstream/atproto-pds` | direct fork | `760fb12a` | `https://github.com/bluesky-social/atproto` |

The canonical machine-readable baseline is `artifacts/upstream-baseline.json`. `python3 scripts/check_upstream.py --fast` is read-only and reports whether local trees match that baseline. AppViewLite and FishyFlip were retired from the tracked dependency graph; any preserved checkout is historical evidence only. Ordinary npm/pnpm packages are dependencies, not source forks, and are excluded from this inventory.
