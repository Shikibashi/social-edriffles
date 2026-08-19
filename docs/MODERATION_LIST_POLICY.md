# Moderation-list policy

Status: implemented in the reviewed candidate; owner acceptance remains
`OWNER_ACCEPTANCE_PENDING`.

This document separates protocol facts from fork policy. The fork keeps the
standard `app.bsky.graph.listblock` Lexicon and record shape. The radical-
liberal choice is how a governed actor's record is created and interpreted.

## Normative operation matrix

| Operation | Governed first-party PDS | Standard/remote semantics |
|---|---|---|
| Individual `app.bsky.graph.block` create/update/delete | Allowed; hard relationship | Standard hard relationship |
| Individual mute | Allowed; private attention state | Standard client/service behavior |
| Local `app.bsky.graph.listblock` create | Rejected with an explicit policy error | Accepted by standard services |
| Local `app.bsky.graph.listblock` update | Rejected with an explicit policy error | Accepted by standard services |
| Local `app.bsky.graph.listblock` delete | Allowed for legacy cleanup | Standard delete |
| Historical listblock in CAR import | Accepted and indexed; journaled as legacy | Accepted and indexed |
| Local legacy listblock interpretation | Inert compatibility data; no attention or block effect | Not applicable |
| Incoming external listblock against a local actor | Inert compatibility data; no incoming boundary effect | Standard remote services may interpret it differently |
| List membership change | Never creates direct blocks | Never creates direct blocks |

## Product behavior

The client offers two distinct actions for a moderation list:

- **Mute list** calls the private `app.bsky.graph.muteActorList` service and
  does not create a public listblock.
- **Review accounts** enumerates current members and lets the user explicitly
  select individual DIDs. Each selected account creates one ordinary
  `app.bsky.graph.block` record. Future list membership changes do not create
  blocks.

Legacy local listblocks remain readable long enough to migrate or clean up.
They are already behaviorally inert before migration. Migration is ordered as:
create private mute, verify private mute, obtain a signed claim from the
selected provider when attestation is configured, delete the public listblock
with CID/CAS protection, verify deletion, then write a receipt.
Mute/attestation failure leaves the source record. Delete failure leaves the
verified mute and is retryable. During this pre-activation window, the
governed PDS permits only the intended legacy-listblock deletion for the
deactivated imported account; ordinary repository writes remain blocked.

## Authority and compatibility tags

- **INTEROPERABILITY:** retain the upstream Lexicon, CAR format, direct block
  records, lists, list items, and raw local/external listblocks.
- **SECURITY / PRODUCT POLICY:** enforce the local create/update denial in the
  PDS `prepareCreate`/`prepareUpdate` boundary and every repository write API.
- **TECHNICAL / INTEROPERABILITY:** CAR import inventories listblocks before
  applying a commit and writes a receipt with hashed source identifiers.
- **SECURITY / INTEROPERABILITY:** when configured, the PDS verifies the
  provider's `did:key` signature, subject DID, list hash, provider identity,
  and freshness window before accepting an attestation. This proves a signed
  provider claim; it does not give the PDS access to the provider's private
  state.
- **PRODUCT POLICY / PRIVACY:** private list mutes are the delegated attention
  primitive; receipts do not contain a plaintext moderation graph or secrets.
- **NORMATIVE / PRODUCT POLICY:** durable hard relationships require explicit
  individual action; listblock records never supply hard or attention state in
  this fork.

These are fork choices, not requirements imposed by ATProto itself.

## PDS and AppView separation

The first-party PDS is a patched copy of the official `@atproto/pds` source at
the pinned revision in `upstream/atproto-pds`. It owns DID-authenticated
repository writes, CAR import, blobs, sync, and account state. AppViewLite is
retired and is not a selectable or mandatory read-side service. The client may
use another explicitly configured AppView/feed provider without changing the
PDS.

The PDS journal can reconcile a repository to `clean` once cleanup has removed
the public listblock records and, when configured, each imported list has a
verified provider attestation. Governed account activation may remain blocked
while the journal is non-clean, but this is an import/cleanup gate rather than
a visibility effect. The private mute is provider-side state, so the PDS does
not claim to inspect provider internals; it accepts only a signed claim from
the configured provider. The first-party client must perform the mute and
obtain that claim before deleting the public record.

## Configuration

Set this only on the first-party governed PDS:

```sh
PDS_RADLIB_MODERATION_WRITE_POLICY=deny-create-update
```

For a governed deployment that requires provider-side proof during CAR
migration, configure the provider DID/key and freshness window as well:

```sh
PDS_RADLIB_MUTE_ATTESTATION_PROVIDER_DID=did:web:provider.example
PDS_RADLIB_MUTE_ATTESTATION_PROVIDER_KEY=did:key:z...
PDS_RADLIB_MUTE_ATTESTATION_MAX_AGE_SECONDS=300
```

The provider key is public verification material. The provider's private
signing key stays in provider deployment configuration and is never placed in
the PDS receipt or personalization export. The provider implements
`org.radlib.moderation.getListMuteAttestation`; the PDS accepts the signed
result through `org.radlib.moderation.recordListMuteAttestation`.

The package default remains `standard` so embedding the official PDS code in a
non-governed interoperable service does not silently acquire fork policy.

The selected provider's private list-mute implementation is an attention
service, not a source of durable direct blocks. `listblock` is inert for local
and incoming external interpretation: it cannot hide public content, deny
interaction, alter notifications, or populate block relationships. Provider
identity and attestation configuration must be explicit and must never
silently fall back to a retired implementation.
