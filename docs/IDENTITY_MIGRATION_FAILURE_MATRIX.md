# Identity Migration Failure Matrix

- destination disappears: recoverable failure; retry destination validation
- repository/blob transfer interrupted: resume from durable state
- identity update succeeds then activation fails: fail closed; verify current DID service
- stale resolver returns former PDS: cached read-only only; sensitive writes denied
- old PDS refuses cooperation: human intervention; do not claim rollback
- process crash between transitions: resume from receipt state
- user cancels before identity update: safe abort
- post-update cancellation: continue-forward verification; reversal is not assumed
- replayed old service authorization: reject by expiry/audience/revocation
