# Upstream Rebase Playbook

1. Confirm clean parent and submodule trees: `git status --short` and `git submodule status`.
2. Record the known-good `artifacts/upstream-baseline.json`.
3. Inspect history/remotes without mutation: `python3 scripts/check_upstream.py --fast`.
4. Fetch upstream only in a disposable clone/worktree when network is available; never force-push or rewrite the canonical branch.
5. Predict textual overlap with Git's read-only merge/range tools in a disposable worktree. Classify semantic overlap by the patch-surface map even when Git merges cleanly.
6. Apply the update on a disposable branch, regenerate generated files from their source, and inspect characterization fixtures before changing expectations.
7. Run the FAST gate: `python3 scripts/check_upstream.py --fast && python3 -m unittest tests/test_upstream_hardening.py tests/test_constitutional_stack_integration.py tests/test_deployment_v1.py`.
8. Run the FULL gate: `python3 scripts/validate_contract.py && python3 -m unittest discover -s tests -p 'test_*.py'`; for social-app changes also run `pnpm typecheck:web` and `EXPO_PUBLIC_ENV=production pnpm build-web`.
9. Review identity/association/attention/service/personalization/deployment fixtures and write a rebase receipt. Update the baseline only after review and clean gates.
10. Roll back by discarding the disposable branch/worktree and restoring the previous pinned SHA; never revert remote user/account state.

Upstream metadata is untrusted input. The checker uses argument arrays, does not execute commit messages or branch names, and does not fetch or mutate trees.
