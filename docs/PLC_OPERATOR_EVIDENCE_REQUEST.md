# PLC Operator Evidence Request

This document is the handoff package for a genuinely independent PLC mirror or
resolver operator. It is an evidence request, not a declaration that Radlib
controls or operates the external service. A second endpoint operated by
Radlib, or by the same person or organization as an existing endpoint, is not
eligible for this gate.

## Research result

The current ecosystem includes several useful read-replica patterns:

- `https://plc.wtf` is live and identifies itself as an Allegedly mirror in
  wrap mode. Its public service is useful for comparison, but it does not
  publish the signed Ed25519 operator statement required by this project.
- `https://didplc.directory` is live and identifies itself as a `go-didplc`
  read replica operated from `vayumandala.com`. Its DID histories can be
  fetched and verified, but its published operator key is not Ed25519 and it
  does not publish the required signed statement, tombstone evidence, or
  disagreement receipt.
- `https://plcbundle.atscan.net` is a documented bundle-mirror project, but it
  was not reachable from the current probe and therefore is not evidence for
  this gate.

The [official PLC read-replica guidance](https://atproto.com/blog/plc-replicas)
requires replicas to retain independently queryable data and audit operation
hashes, signatures, and timestamp constraints. The gate below additionally
requires operator evidence so that cryptographic correctness is not confused
with independent control.

## Required external package

The operator should publish a secret-free JSON receipt over HTTPS, then give
the URL and the source/deployment binding to the Radlib release reviewer. The
receipt must use the existing format:

```text
us.edriffles.radlib.external-plc-independence/1
```

The receipt must contain two operator records:

1. the primary PLC operator;
2. the independent mirror or resolver operator.

Each record needs:

- a stable operator identifier;
- a distinct service DID;
- a distinct HTTPS endpoint origin;
- a base64url-encoded 32-byte Ed25519 public key;
- independently verifiable control evidence, such as a signed deployment
  record, a public service control document, or an auditor report that binds the
  operator to the endpoint and key.

The two operators must differ in `operatorId`, `serviceDid`, `publicKey`, and
endpoint origin. Domain ownership alone is not enough if both endpoints are
controlled by the same actor.

## Signed DID-history statement

The mirror operator must sign a canonical statement with the Ed25519 key
published in its operator record. The current verifier canonicalizes the JSON
as UTF-8 using sorted keys, no insignificant whitespace, and no ASCII escaping:

```python
json.dumps(
    signed_statement,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
```

The receipt records the SHA-256 digest of those bytes and the unpadded
base64url signature. The signed statement must bind at least:

- the exact `did:plc` under test;
- the verified history digest;
- the operation count;
- genesis-derived DID verification;
- previous-CID verification;
- rotation-signature verification;
- terminal tombstone-rule verification;
- rejection of stale, malformed, and invalid-signature fixtures;
- the fact that resolver disagreement was made visible.

The validator checks the Ed25519 signature itself. A boolean field saying
`signatureVerified: true` without a matching cryptographic signature is not
accepted.

## Tombstone evidence

Provide a real terminal tombstone fixture or a signed URL to one. The fixture
must contain a history whose final entry is `plc_tombstone`; the primary and
mirror histories must be fetched from their own endpoints and verified against
the active rotation key, previous CID, and terminal-position rule. A normal
non-tombstoned DID history does not prove this behavior.

The local probe can verify a supplied DID against both endpoints:

```sh
python3 scripts/verify_plc_mirror_candidate.py \
  --primary https://plc.directory \
  --mirror https://mirror.example \
  --operator-did-url https://mirror.example/.well-known/operator.json \
  --tombstone-did did:plc:terminalfixturexxxxxxxx
```

Replace the example values with the operator's actual endpoint and a real
`did:plc` that is demonstrably tombstoned. The command emits blocked evidence
until the separate signed operator receipt is supplied.

## Disagreement and reconciliation evidence

Provide a real observation in which independently queried resolver results
differ, for example because the mirror is intentionally stale during a
controlled update window. The receipt must include:

- the DID or resolution subject;
- the primary result digest and provenance;
- the mirror result digest and provenance;
- timestamps and endpoint origins;
- the user-visible reconciliation outcome.

The client must expose the disagreement rather than silently treating one
endpoint as universally authoritative. The mirror operator must include the
disagreement fact in the signed statement.

The probe supports this controlled comparison when both endpoints expose the
same DID history API:

```sh
python3 scripts/verify_plc_mirror_candidate.py \
  --primary https://plc.directory \
  --mirror https://mirror.example \
  --operator-did-url https://mirror.example/.well-known/operator.json \
  --disagreement-did did:plc:comparisonfixturexxxxxxxx \
  --reconciliation 'show both claims; prefer the verified newer history after review'
```

`visibleResolverDisagreement` is true only when the live histories actually
differ and a non-empty reconciliation outcome is supplied. It is never set by
the presence of a second URL alone.

## Review commands

After receiving the operator package, run the schema and signature validator:

```sh
python3 scripts/validate_external_gate_receipts.py /path/to/external-plc-independence.json
```

Then run the live history probe against the operator's published endpoints and
compare its history digest, operation count, tombstone result, and disagreement
evidence with the signed statement. Finally, bind the reviewed receipt to the
staging manifest and rerun:

```sh
python3 scripts/validate_external_gate_manifest.py
python3 scripts/validate_contract.py
```

Do not change `status` to a pass, replace the operator key, or sign the
statement locally. If the operator cannot publish the signed package, the
correct result remains `PLC_OPERATOR_INDEPENDENCE_NOT_PROVEN`.
