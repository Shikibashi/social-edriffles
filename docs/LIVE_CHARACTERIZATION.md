# Historical Live Characterization Boundary

> Status: `HISTORICAL_RETIRED`. The former local read-provider experiment and
> its .NET dependency were removed from the supported repository graph. The
> evidence below is retained only to distinguish prior observation from current
> product behavior; it must not be cited as a current provider or acceptance
> result.

The current live walkthrough uses the first-party PDS for identity, repository
writes, CAR import, and migration state, plus the generic provider boundary in
the client. Current provider choice is explicit and provenance-bearing. The
static A/B/C fixture remains the contract source for surfaces not exercised by
the live PDS walkthrough.

The historical artifacts are `artifacts/live-ab-c-characterization.json` and
`artifacts/live-block-presentation-observations.json`. They describe the old
disposable run only. No current build, test, or launch command depends on the
retired provider or its former .NET support library.
