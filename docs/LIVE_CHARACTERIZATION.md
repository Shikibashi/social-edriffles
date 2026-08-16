# Live Characterization Boundary

The isolated AppViewLite instance was started from the pinned submodule with an empty database and firehose/PLC ingestion disabled. The live root redirect and `com.atproto.server.describeServer` endpoint both respond successfully.

A/B/C record seeding is not complete. AppViewLite's `/api/CreateBlock` write endpoint requires an authenticated AppViewLite/PDS session; an unauthenticated fixture request returns HTTP 500 and does not create data. The current checkout has no local PDS credentials or signed repository CAR fixture. Therefore the static A/B/C matrix remains authoritative for contract shape, while live viewer-specific assertions are deliberately not claimed.

Do not replace the static matrix with guessed live expectations. Complete this phase only after providing one of:

- a disposable local PDS with A/B/C signed records;
- a signed CAR fixture import for A/B/C; or
- an authenticated AppViewLite session whose write operations can be isolated to a disposable database.

The existing live tests cover server reachability only and skip unless `APPVIEWLITE_URL` is set.
