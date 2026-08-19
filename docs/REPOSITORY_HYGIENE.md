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

Submodule paths were repaired to root-relative entries in `.gitmodules` and
verified with `git submodule update --init --recursive`:

- `upstream/social-app` — `c38bfe515a9d52d2b9969c8ead64eced5f8d33ee`
- `upstream/atproto-pds` — `760fb12a080c87cdfd0dae42ae833bad8bc20886`

AppViewLite and FishyFlip are retired. Their existing dirty nested checkouts
are preserved as local archives outside the parent repository's dependency
graph and are not launchable or testable through the supported workflow.

Workflow state and generated caches are ignored by the project `.gitignore`.
