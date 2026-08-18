# Identity Session and Key Lifecycle

Sessions are opaque identifiers with creation/last-use metadata, authorization type, scope, and revocation state. Lockdown revokes all sessions, blocks writes, invalidates identity cache, and requires fresh verification. Repository, DID operation, recovery, OAuth, service-auth, and provider release keys remain separate; stale/revoked material cannot authorize new sensitive operations.
