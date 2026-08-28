# Flow diagrams

These diagrams describe bounded Radlib community behavior and the approved
Spaces-alpha upstream maintenance workflow.

| Diagram | Purpose |
| --- | --- |
| [community-directory-cleanup.mmd](community-directory-cleanup.mmd) | Enumerate, identify, confirm, and safely delete communities owned by the authenticated viewer. |
| [spaces-alpha-upstream-sync.mmd](spaces-alpha-upstream-sync.mmd) | Merge the live PDS/client upstream tips into the existing Spaces integration branches, preserve unrelated parent changes, update pins only after local gates pass, and stop before push or default-branch changes. |

The deletion path is owner-scoped. A community that is merely visible to the
viewer is never a deletion target. If one deletion fails, the client stops and
reports the exact completed and remaining targets.
