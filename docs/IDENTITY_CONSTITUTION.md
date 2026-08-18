# Identity Constitution v1

Identity continuity belongs to the user and is represented by a DID. A handle is a human-readable, resolvable name; PDS hosting is storage; an AppView is an index/presentation service; profile presentation is not identity; reputation and moderation status are service-derived; portable personalization is private client state; credentials are issuer attestations; recovery is delegated authority with explicit scope.

## Authority boundaries

| Concern | Identity | Association | Attention | Service | Personalization |
|---|---|---|---|---|---|
| DID, keys, handle continuity | owns | observes | observes | resolves | references |
| follows/blocks/mutes | observes identity | owns | consumes | stores/indexes | does not own |
| ranking/feed allocation | observes | consumes | owns | provides candidates | supplies preferences |
| provider identity/succession | observes | observes | consumes | owns | stores selection |
| portable preferences | account-scoped identity binding | no authority | ranking input | never owns | owns export/privacy |

No service may silently convert delegated access into general account authority. Identity != handle != hosting provider != AppView != profile presentation != reputation != moderation.

## DID and handle

DID is the durable subject. Handles require bidirectional verification against DID documents and resolver evidence. DNS, PLC, DID:web, and cached results are resolution dependencies, not identity subjects. Mismatch, stale cache, resolver disagreement, and outage are visible and fail closed for writes; bounded cached state may support read-only presentation with an unresolved/mismatch indicator.

## Keys, sessions, and credentials

Account signing keys, DID document keys, service-auth keys, and provider release keys are separate authorities. Rotation/revocation invalidates affected grants; expiry, audience, lexical-method (`lxm`), replay, and revocation checks remain mandatory. Credentials are issuer/subject/claim/proof/expiry/revocation records, never universal reputation scores or recommendation inputs.

## Privacy and recovery

DID, handle, repository records, and service endpoints have protocol disclosure. Device/session metadata, recovery channels, provider selections, and personalization remain local or explicitly selected. Recovery providers are identifiable delegated authorities and must expose scope, purpose, duration, and revocation. Age/recovery attributes remain purpose-separated from attention systems.
