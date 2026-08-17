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

AppViewLite's firehose client previously could not ingest that stack because FishyFlip forced `wss://` and dropped the PDS port. That compatibility defect is fixed in the pinned local FishyFlip fork. Live ingestion still requires rerunning the disposable stack with a `ws://` DID override and handling `.test` login resolution; no live A/B/C assertions are claimed yet.
## Firehose compatibility fix

AppViewLite depends on FishyFlip 4.3.0, whose websocket client hard-coded `wss://` and discarded local ports. The fork now tracks a pinned FishyFlip submodule with scheme/port-preserving websocket construction and uses project references from AppViewLite. The solution compiles with 0 errors and 8 existing warnings when invoked with `-p:SignAssembly=false`; the environment's OpenSSL rejects the upstream strong-name signing digest, so signing metadata remains unchanged.
