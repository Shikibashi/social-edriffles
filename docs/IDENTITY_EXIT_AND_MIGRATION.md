# Identity Exit and Migration v1

The exit invariant is: a user changing hosting retains the same DID and the portable state required to participate wherever ATProto permits.

A migration sequence is explicit: authenticate source, export/transfer repository records and blobs, establish destination, update DID service/PDS declaration through protocol-supported mechanisms, resolve and verify the same DID, restore portable personalization, reauthorize clients, and explicitly switch AppView/provider services. Old sessions and service grants are expired or revoked according to scope. Partial, unavailable, malicious, stale, or disagreeing authorities fail closed for writes and remain read-only where cached evidence is safe.

The repository's deterministic harness distinguishes simulated transitions from live protocol migration. It verifies DID continuity, portable preference restoration, service separability, and credential non-export. Production migration and resolver integration remain separately scoped implementation work where upstream support is unavailable.
