# Repository Hygiene

The project is now a standalone Git root:

```text
/var/home/tcs/Code/atproto/.git
```

The accidental home-directory repository metadata was preserved at:

```text
/tmp/atproto-git-backup
```

History was rewritten with `git-filter-repo --path-rename 'Code/atproto/:'` so project paths are root-relative. The migration preserved all 15 project commits by subject and order; rewritten commit IDs differ because paths changed. The standalone history currently ends at the migration commit and contains no unrelated home-directory files.

Submodule paths were repaired to root-relative entries in `.gitmodules` and verified with `git submodule update --init --recursive`:

- `upstream/AppViewLite` — `73f3c2408fc5c744b14da78ce6d4427ddc1d69da`
- `upstream/social-app` — `bde69aa15102640b0e898653a505191acc4951a9`
- `upstream/FishyFlip` — `da2c08aa19475eb2c732933d213a374f03a8e549`

Workflow state and generated caches are ignored by the project `.gitignore`.
