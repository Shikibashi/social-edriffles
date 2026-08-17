# Live Characterization Boundary

The isolated AppViewLite instance was started from the pinned submodule with an empty database and firehose/PLC ingestion disabled. The live root redirect and `com.atproto.server.describeServer` endpoint both respond successfully.

A/B/C record seeding is not complete. AppViewLite's `/api/CreateBlock` write endpoint requires an authenticated AppViewLite/PDS session; an unauthenticated fixture request returns HTTP 500 and does not create data. The static A/B/C matrix remains authoritative for contract shape, while live viewer-specific assertions are deliberately not claimed.

Do not replace the static matrix with guessed live expectations. Complete this phase only after providing one of:

- a disposable local PDS with A/B/C signed records;
- a signed CAR fixture import for A/B/C; or
- an authenticated AppViewLite session whose write operations can be isolated to a disposable database.

The existing live tests cover server reachability only and skip unless `APPVIEWLITE_URL` is set.
## Disposable PDS research

The official `bluesky-social/atproto` development environment provides a disposable PDS stack with seeded `alice.test`, `bob.test`, and `carla.test` accounts (`hunter2`). It requires Docker and starts PDS, PLC, AppView, Redis, and Postgres. The stack was built and started locally; its seeded AppView was reachable on port 2584.

AppViewLite's firehose client previously could not ingest that stack because FishyFlip forced `wss://` and dropped the PDS port. That compatibility defect is fixed in the pinned local FishyFlip fork. The disposable stack now runs with a `ws://` DID override and AppViewLite connects successfully; no live A/B/C assertions are claimed yet.
## Firehose compatibility fix

AppViewLite depends on FishyFlip 4.3.0, whose websocket client hard-coded `wss://` and discarded local ports. The fork now tracks a pinned FishyFlip submodule with scheme/port-preserving websocket construction and uses project references from AppViewLite. The solution compiles with 0 errors and 8 existing warnings when invoked with `-p:SignAssembly=false`; the environment's OpenSSL rejects the upstream strong-name signing digest, so signing metadata remains unchanged.
The disposable stack was rerun successfully after rebuilding the upstream dev environment's generated lexicons, OAuth assets, and Node 22 native `better-sqlite3` binding. AppViewLite connected to `ws://127.0.0.1:2583/` and indexed seeded records. DID-based profile lookup for `did:plc:xbyl3r5sn4aktwat4b7a2vjd` returned HTTP 200. Handle-based requests still require local `.test` resolver support, so viewer-specific block assertions remain unclaimed.
The first live feed request exposed an AppViewLite read-lock crash when enriching an AT URI whose DID had not yet been serialized. `TryGetAtObject` now uses the read-safe serializer and skips unknown mappings instead of fail-fast; the service remains alive and profile requests continue returning HTTP 200.
For the disposable `.test` stack, DID overrides intentionally omit handle aliases. This prevents AppViewLite from launching public-DNS verification tasks for non-resolvable `.test` names; live checks use the seeded DIDs directly.
A fresh disposable run seeded signed A/B/C profiles, posts, an A→B follow, and an A→B block. AppViewLite ingested the firehose and returned HTTP 200 for profiles, author feeds, post threads, notifications, and follows. `app.bsky.graph.getBlocks` returns HTTP 200 with B, and viewer states now report A→B as `blocking`, B→A as `blockedBy`, and C as neither. The complete evidence is recorded in `artifacts/live-ab-c-characterization.json`; static fixtures remain unchanged and underlying post-filter semantics are not changed.
