# Identity Recovery Failure Matrix

Expired/replayed/duplicate challenges, wrong account/factor, stale sessions, stolen OAuth refresh, old-key replay, malicious/unavailable PDS, resolver staleness, handle takeover, interrupted recovery, tampered receipt, authority expansion, and secret leakage all fail closed. Safe retries resume the durable state machine; post-identity-update rollback is not assumed; human intervention is required where protocol custody prevents recovery.

# Identity Session and Key Lifecycle

Sessions are opaque identifiers with creation/last-use metadata, authorization type, scope, and revocation state. Lockdown revokes all sessions, blocks writes, invalidates identity cache, and requires fresh verification. Repository, DID operation, recovery, OAuth, service-auth, and provider release keys remain separate; stale/revoked material cannot authorize new sensitive operations.
