# Identity Runtime v1

The runtime uses replaceable resolver providers, deterministic provider order, provenance, and bounded caching. Supported input methods are `did:plc`, `did:web`, and handles. Handle resolution is verified bidirectionally against the DID document. Results distinguish verified, mismatched, invalid, unavailable, stale-cache, and revocation states.

Positive results cache for five minutes; negative results cache for thirty seconds; stale-while-error display is bounded to one hour and never authorizes sensitive writes. Cache invalidation is explicit on identity transitions. Resolver output is untrusted data and is not itself an authorization grant.

Migration is represented by an idempotent durable state machine: destination validation, preparation, repository/blob transfer, identity update, activation, old-authority revocation, verification, and completion. The current harness is simulated where upstream migration APIs are unavailable; receipts mark this explicitly. Invalid transitions fail closed, interrupted work is recoverable where protocol semantics permit, and terminal identity updates are not pretended reversible.
