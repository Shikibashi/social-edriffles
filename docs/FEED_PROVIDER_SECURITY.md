# Feed Provider Security v1

This is the bounded security contract for untrusted feed generators and candidate providers. It hardens current custom-feed responses without changing ranking semantics or implementing Candidate Protocol v1.

Portable Personalization v1 remains client-owned and is never transmitted as a complete profile to a provider.
Provider payloads are declarative data only; executable content has no execution path.
## Provider identity and manifests

A provider manifest contains a canonical provider DID, HTTPS origin, algorithm name/version, manifest hash, and optional signing-key identifier. DID and endpoint are validated together. HTTP, credentials, ports, query/fragment endpoints, local/private hosts, revoked manifests, and malformed identifiers are rejected. Manifest identity is displayed canonically; lookalike labels do not establish authority.

Signing keys are separate from release/build keys. Rotation publishes a new key before use, revocation stops acceptance, offline recovery protects the root, and succession requires explicit DID/service-manifest control. Compromised manifests are rolled back to the last accepted version; domain expiry or takeover is treated as identity failure, not an automatic provider switch.

## Network limits

The client contract uses 3s connect, 10s read, and 15s total deadlines; 2MB response and 1MB compressed-response budgets; 100 candidates per page; 512-byte cursors; 20-page pagination bounds; two concurrent provider requests; HTTPS-only endpoints; redirect rejection; and private/local-host rejection. Production adapters should add decompression accounting, token-bucket backpressure, and circuit breakers before broad provider rollout.

## Candidate contract

Each hydrated candidate must have a valid AT URI and CID. Candidate counts, cursor characters/length, duplicate URIs, malformed records, malformed reason metadata, and non-finite/out-of-contract numeric values are rejected deterministically. Reasons are bounded strings/data only. No provider response is evaluated as code, loaded as a module, or allowed to mutate durable relationships.

## Failure behavior

| Failure | Required result |
|---|---|
| Timeout/slow response | Abort; classify timeout; preserve cached/chronological path or offer explicit fallback |
| Malformed response/candidate | Reject batch; do not partially apply it |
| Identity/signature/revocation failure | Reject provider; do not silently substitute |
| Stale/replayed batch or pathological cursor | Reject and restart only through bounded explicit pagination |
| Unavailable/circuit-open provider | No request while open; expose provider failure and explicit exit |
| Hydration disagreement | Reject disagreement; do not display a mismatched record |

Fallback remains visible and explicit under the Attention Constitution. Provider data cannot override moderation, association, PDS, or personalization authority.

## Remaining Candidate Protocol v1 work

Signed candidate-batch envelopes, replay freshness proofs, manifest signature verification against a production DID resolver, resolver-aware DNS rebinding defense, streaming decompression quotas, privacy-preserving health aggregation, and end-to-end hydration provenance remain reserved for Candidate Protocol v1.
