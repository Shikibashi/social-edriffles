# WorkPM activity log: Spaces alpha upstream synchronization

## Phase 1: research and proposal

- Created: 2026-08-27T06:44:47-04:00
- Project: `/var/home/tcs/Code/atproto`
- Branch: `codex/spaces-alpha-integration`
- Workflow: native WorkPM; read-only delegation was bounded and then closed after timeout, followed by sequential fallback.
- Domain dictionary: `docs/domain-dictionary.md` found and loaded. Terms retained: Community, Directory, Owned community, Protocol Space, Metadata cascade, Start from scratch.

### Repository evidence

- Parent checkout is dirty in root scripts, tests, memory/conversation artifacts, and `.sb_config.json`; preserve all of it. Nested `upstream/atproto-pds` and `upstream/social-app` checkouts are clean.
- Live read-only refs: atproto `permissioned-data-alpha`=`4c33457afe96ad2e5d2fe6bd975f094cd6f67328`, `permissioned-data`=`5fbc9a0076a40799c22a13e0bac7e6fba6ec785f`; social-app `main`=`c4c999ff4f8f6bf42e752a1b0d39718a6330b68b`.
- Fork refs remain PDS `codex/spaces-alpha-integration`=`37f823c7e0e81eae8589c7ebed30fc38dfc0326a` and client `codex/spaces-alpha-integration`=`31d7c8b083ddac2c44dc156f29081712211581c1`.
- PDS merge-base is `89deb9f...`; the live alpha branch has 10 commits outside the fork side and the fork has 22 outside the alpha side. Read-only `git merge-tree --write-tree` predicts no conflicts; upstream changes are four build/publish workflow files.
- Client merge-base is `c19fec3...`; the live upstream has 42 commits outside the fork side and the fork has 49 outside the upstream side. Read-only merge prediction reports 15 conflicts, including package manifests/lockfile, login/session clients, feed rendering, moderation/settings UI, and translation files.
- Baseline checks against the current pins pass: `python3 scripts/check_upstream.py --fast`, `python3 scripts/validate_contract.py` (125 files, 29 blocking rows, 6 feed cases), and root/nested `git diff --check`.

### Proposal scores

| Option | Fit | Risk | Effort | Summary |
|---|---:|---:|---:|---|
| A. Merge upstream into both existing Spaces branches in disposable worktrees, then update parent pins | 5 | 3 | 3 | Preserves history; PDS is predicted clean; client has 15 explicit conflicts to resolve and verify. Recommended. |
| B. Rebase both Spaces branches onto the live upstream tips | 4 | 2 | 5 | Linear history, but rewrites the fork branch and makes 49 client commits cross a large moving conflict surface. |
| C. Stage a new synchronized candidate worktree/branch; update the PDS lane first and defer the client/root baseline until acceptance | 4 | 5 | 4 | Best containment for the dirty parent and client churn, but leaves the maintained baseline split until a later promotion. |

### Decision gate

No branch, pin, default branch, remote branch, or production deployment has been changed. Await user selection of A, B, or C before Phase 2 blueprint and implementation.

## Phase 2: approved flow blueprint

- User selected Option A on 2026-08-27.
- Blueprint: `docs/flow-diagrams/spaces-alpha-upstream-sync.mmd`; the diagram records disposable study worktrees, PDS merge, client conflict resolution, generated-file refresh, boundary review, pin update, verification gates, and the no-push/default-branch authorization gate.
- Mermaid CLI (`mmdc`) is not installed. Structural inspection and `git diff --check` passed; rendered Mermaid verification was not run.

## Phase 3: impact analysis

- PDS merge-base `89deb9f...`: live `permissioned-data-alpha` had 10 alpha-only commits and the fork had 22 fork-only commits; read-only merge prediction reported no conflicts and the final merge changed four upstream workflow/changeset files.
- Client merge-base `c19fec3...`: live `main` had 42 upstream-only commits and the fork had 49 fork-only commits; read-only merge prediction reported 15 conflicts. Resolutions covered package/lock metadata, login/session OAuth behavior, moderation/settings, feed rendering, translation extraction, and fork-specific compatibility.
- The standard Spaces data plane and the `us.edriffles.radlib.private.*` product policy/control plane remain separate. No old custom private transport was reactivated.

## Phase 4: implementation and verification

- PDS local merge: `9c3d92f04335d624a79acbbf5f346130f00ffbdd`, parents fork `37f823c7...` and alpha `4c33457...`.
- Client local merge: `8cc2f7c63809e37d3df1089963d89d379471fdab`, parents fork `31d7c8b...` and upstream `c4c999ff...`.
- Updated active machine-readable pins, contract assertions, Spaces integration documentation, inventory, and the latest local synchronization receipt.
- PASS: client typecheck; 4 focused Spaces Jest suites / 15 tests; production web build with asset-size warnings; PDS focused Spaces/Radlib suites (149 passed, 1 todo); PDS TypeScript build; root fast pin check; root contract validation; root Python suite (91 tests, 5 skipped); root/nested diff checks.
- Parent root dirty changes and untracked user files were preserved. No push, default-branch change, remote branch update, or production deployment occurred.

## Phase 5: reconciliation

- The executed work follows the approved blueprint through `LocalDone`: both nested fork branches now contain local upstream merge commits, active pins match the exact checkout SHAs, and all required local gates pass.
- The process stops at the local-only authorization boundary. Owner acceptance, production activation, external authority publication, disposable-provider credential evidence, and other documented alpha gates remain pending.
