# Identity Migration Runtime

| State | Retry | Rollback | Intervention |
|---|---|---|---|
| validating_destination | retry validation | none | destination correction |
| transferring_repository/blobs | resume idempotently | source remains authoritative | repair missing data |
| updating_identity | fail closed | protocol-dependent | verify DID document |
| activating_destination | retry/continue forward | not assumed | operator verification |
| revoking_old_authority | retry | no restoration assumed | inspect grants |
| verifying | retry with fresh resolver | no | resolve discrepancy |
| complete | no-op/idempotent | protocol-dependent | none |
| terminal_failure | no automatic retry | no | explicit recovery |

Receipts persist migration id, DID, source/destination PDS, state, simulation marker, preference restoration, and old-authority retirement. Production transfer APIs are only invoked when discovered and supported; this fork does not invent endpoints.
