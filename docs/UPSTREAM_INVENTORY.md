# Upstream Inventory

| Project | Local path | Relation | Pinned/current SHA | Remote |
|---|---|---|---|---|
| bluesky-social/social-app | `upstream/social-app` | direct fork | `946df3eb` | `https://github.com/bluesky-social/social-app` |
| alnkesq/AppViewLite | `upstream/AppViewLite` | pinned optional submodule | `ab3ac9e` | `https://github.com/alnkesq/AppViewLite` |
| DrasticActions/FishyFlip | `upstream/FishyFlip` | pinned dependency/submodule | `da2c08a` | `https://github.com/drasticactions/FishyFlip` |

The canonical machine-readable baseline is `artifacts/upstream-baseline.json`. `python3 scripts/check_upstream.py --fast` is read-only and reports whether local trees match that baseline. Ordinary npm/pnpm packages are dependencies, not source forks, and are excluded from this inventory.
