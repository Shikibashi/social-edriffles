# Flow diagrams

These diagrams describe the community cleanup behavior implemented for the
Radlib community directory.

| Diagram | Purpose |
| --- | --- |
| [community-directory-cleanup.mmd](community-directory-cleanup.mmd) | Enumerate, identify, confirm, and safely delete communities owned by the authenticated viewer. |

The deletion path is owner-scoped. A community that is merely visible to the
viewer is never a deletion target. If one deletion fails, the client stops and
reports the exact completed and remaining targets.
