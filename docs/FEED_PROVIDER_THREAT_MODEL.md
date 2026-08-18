# Feed Provider Threat Model

Independent feed generators and candidate providers are untrusted services. A provider may be malicious, compromised, impersonated, unavailable, slow, oversized, stale, or simply incorrect. Provider output is declarative data; it never carries executable behavior or authority to mutate relationships.

## Assets and boundaries

- User identity, PDS session, social graph, moderation state, and Portable Personalization remain outside provider authority.
- Feed candidates, cursors, reasons, manifests, and hydration requests are untrusted input.
- Provider endpoints are network boundaries subject to SSRF, redirect, DNS takeover, resource exhaustion, and denial-of-service threats.
- Signing and release/build credentials are separate concerns: service signing keys must not be treated as release keys.

## Threat matrix

| Threat | Control | Failure behavior |
|---|---|---|
| Impersonated provider/DID or lookalike | DID syntax, canonical HTTPS origin, manifest identity binding, explicit display | Identity failure; no provider request |
| Compromised signing key | Key separation, rotation, revocation, succession, rollback | Signature/revocation failure; circuit failure |
| Domain expiry/takeover | DID service endpoint revalidation and explicit manifest update | Identity failure; no silent substitution |
| Huge/ compressed response | Byte/decompression/candidate limits | Deterministic rejection |
| Slow/pathological cursor | Connect/read/total deadlines and cursor bounds | Timeout or stale-batch failure |
| Redirect/SSRF | HTTPS-only canonical origins, redirect error, private-host rejection | Request rejected |
| Malicious URI/CID/reason | Strict syntax and size validation; reasons treated as data | Candidate/batch rejected |
| Duplicate/replayed/stale batch | URI deduplication, bounded cursors/pages, freshness metadata where supplied | Batch rejected |
| Hydration disagreement | Compare requested candidate identity with hydrated record | Hydration-disagreement failure |
| Executable payload | JSON data-only schema; no dynamic evaluation or code loading | Field rejected |
| Relationship mutation attempt | Provider has read/order authority only | No mutation path |
| Provider outage/DoS | Backpressure, concurrency limit, circuit breaker, explicit fallback | Cached/chronological path or explicit user choice |

## Privacy and observability

Operational telemetry may aggregate health, latency, rejection category, and circuit state. It must not create permanent per-user feed traces by default. Diagnostic bundles are opt-in, bounded, and redact account identifiers, cursors, candidate histories, and personalization. The Attention Constitution's public/audit/confidential explanation scopes remain in force.
Candidate Protocol v1 remains a later protocol-design boundary; this document does not authorize a public candidate-batch protocol.
