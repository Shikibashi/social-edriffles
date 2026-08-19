# AppViewLite Retirement

Status: `RETIRED` as of 2026-08-18.

AppViewLite is no longer an active, tracked, configured, built, or supported
provider for this fork. The parent repository removes its submodule and pin,
removes the FishyFlip submodule that existed only for that provider, and keeps
the client provider registry generic rather than replacing one mandatory
provider with another.

## Replacement topology

- The first-party `upstream/atproto-pds` checkout owns DID sessions,
  repository writes, CAR import/export, sync, and the moderation-list write
  policy.
- The social-app client uses an explicitly selected AppView, feed generator,
  labeler, and resolver. Provider identity, endpoint, health, and failure are
  shown independently of the PDS.
- `services/radlib-filtered-feed` remains an optional provider lane for local
  filtering/ranking. It is not an AppView replacement or an account host.

This is a service-boundary migration, not a protocol fork: standard ATProto
records, DIDs, repositories, CARs, and external provider semantics remain the
interoperability boundary.

## Preserved local work

The former nested checkout contained uncommitted user changes. It was not
deleted. It is preserved locally as a retired archive so those changes remain
recoverable, but it is no longer represented by a parent Git submodule and is
not part of any supported command, test, build, or runtime configuration.
The same treatment applies to the former FishyFlip checkout. No current
result may be described as a live AppViewLite result.

## Verification contract

The retirement is complete when all of the following hold:

1. `.gitmodules` and `upstream-pins.json` contain no retired provider entry.
2. `git ls-files upstream/AppViewLite upstream/FishyFlip` is empty.
3. No active client, PDS, service, test, fixture, launch command, or current
   acceptance artifact selects the retired provider.
4. The generic provider tests pass and the first-party PDS build/tests pass.
5. Historical evidence, where retained, is explicitly labeled retired and is
   not used as current acceptance evidence.

The exact checked-out SHAs of the supported upstreams are recorded in
`upstream-pins.json` and `artifacts/upstream-baseline.json`.
