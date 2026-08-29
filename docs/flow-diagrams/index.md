# Flow diagrams

These diagrams describe bounded Radlib community behavior and the approved
Spaces-alpha upstream maintenance workflow.

| Diagram | Purpose |
| --- | --- |
| [community-directory-cleanup.mmd](community-directory-cleanup.mmd) | Enumerate, identify, confirm, and safely delete communities owned by the authenticated viewer. |
| [provider-claim-reconciliation.mmd](provider-claim-reconciliation.mmd) | Query identity-capable providers without credentials, retain claims and failures, and apply an explicit local reconciliation policy. |
| [polycentric-authority-loop.mmd](polycentric-authority-loop.mmd) | Select providers by capability, preserve attributable claims, reconcile disagreement with user-owned policy, upgrade OAuth grants explicitly, and keep identity custody behind protocol authority. |
| [external-gate-remediation.mmd](external-gate-remediation.mmd) | Disposable OAuth expiry, controlled Relay/AppView canaries, and independent PLC evidence before external gate promotion. |
| [spaces-alpha-upstream-sync.mmd](spaces-alpha-upstream-sync.mmd) | Merge the live PDS/client upstream tips into the existing Spaces integration branches, preserve unrelated parent changes, update pins only after local gates pass, and stop before push or default-branch changes. |

The deletion path is owner-scoped. A community that is merely visible to the
viewer is never a deletion target. If one deletion fails, the client stops and
reports the exact completed and remaining targets.

Identity resolution is capability-scoped rather than inherited from the feed
AppView selection. New providers start with public-read only; a provider can
participate in identity resolution only after an explicit local grant. A
registered provider can propose a claim but cannot become the DID authority by
position, and the default policy does not select a partial or disputed result.
