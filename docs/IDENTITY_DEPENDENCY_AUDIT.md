# Identity Dependency Audit

| Dependency | Authority | Failure | Exit/replacement | User consequence |
|---|---|---|---|---|
| plc.directory/PLC replicas | DID method infrastructure | outage/disagreement/compromise | cached read-only state; resolver replacement where protocol permits | identity status unavailable or mismatch shown |
| DNS | DID:web/handle evidence | stale/tampered DNS | explicit re-resolution and certificate validation | handle unresolved/mismatch |
| Certificate authorities | HTTPS endpoint identity | revocation/compromise | alternate verified endpoint or fail closed | service unavailable |
| Relay/index infrastructure | propagation/presentation | lag/outage | alternate AppView/provider | stale/read-only presentation |
| OAuth metadata | authorization service | stale/invalid metadata | reauthorization with visible scope | grant denied |
| PDS discovery | hosting declaration | unavailable/malicious former PDS | destination declaration and explicit migration | writes blocked until verified |

Caches never silently override fresh conflicting evidence. Protocol-public identity data is distinguished from local sessions, recovery data, and personalization.
