# Service Boundaries

| Actor/service | Authority | Must not silently do |
|---|---|---|
| User/device | preferences, local ranking, blocks, selected labelers, provider choice | upload private behavioral history by default |
| PDS | identity and repo records | become an undisclosed personalization owner |
| AppView | records and public/network views it serves | impose unrelated viewer decisions |
| Feed generator | candidates and ordering within its feed | own the user's private preference model |
| Integrity service | bounded evidentiary weighting of coordinated engagement | create content judgments or moderation actions |
| Labeler/classifier | its own descriptive labels/scores | become universal authority |
| Operator/community | published rules within its jurisdiction | claim that an unspecified “platform” acted |

Unsupported features must present an explicit choice before another service receives the request. Provider changes must preserve DID, PDS, public graph, and portable explicit preferences.

## Deferred architecture
Local reranking, encrypted profile export/import, permissioned-data synchronization, signed candidate batches, advanced provenance, runtime attestation, and runnable provider selectors are future work—not PR-00/PR-01 behavior.
