# Radical-Liberal Moderation-List Audit

Status: implemented in the first-party PDS/client path; owner acceptance
remains `OWNER_ACCEPTANCE_PENDING`.

## Authority map

| Contract | Implementation | User-facing surface | Evidence |
|---|---|---|---|
| Individual direct block is hard | `upstream/social-app/src/state/queries/profile.ts`; standard `app.bsky.graph.block` | profile block and review dialog | client tests and A/B/C fixture |
| Individual mute is private attention | standard client mute mutation | profile/list controls | social-app tests |
| Moderation-list mute is delegated attention | `state/queries/list.ts`, `SubscribeMenu.tsx` | “Mute list” | provider boundary test |
| Review list members is explicit | `ReviewListMembersDialog.tsx` and `useDirectBlockMutation` | “Review accounts” | moderation-list policy tests |
| Local listblock CREATE/UPDATE is denied | `packages/pds/src/repo/moderation-policy.ts`, `repo/prepare.ts`, create/put/apply APIs | explicit policy error | PDS tests and bypass guard |
| First-party PDS launch is governed | `services/pds/index.ts` requires `PDS_RADLIB_MODERATION_WRITE_POLICY=deny-create-update` | ungoverned service refuses to start | service-entrypoint refusal check and configured real-PDS test |
| Legacy listblock import stays interoperable | `repo/radlib-migration.ts`, `repo/importRepo.ts` | migration status/activation gate | import/migration tests and live walkthrough |
| Local and incoming listblock records are behaviorally inert | `packages/bsky/src/data-plane/server/routes/{relationships,blocks}.ts`, `hydration/*`, `views/index.ts`, `getListBlocks.ts` | no relationship, block-existence, profile, feed, thread, search, notification, embed, or chat effect | `tests/views/block-lists.test.ts` 6/6, listblock thread regressions 2/2, list-mute regression 22/22, broader 10-file run 229/229 |
| Provider private-mute proof is signed | `repo/radlib-attestation.ts`, `us.edriffles.radlib.moderation.*` XRPC routes | provider capability/provenance | live PDS/CAR/provider walkthrough |
| External incoming listblock remains inert in this fork | raw record/index compatibility only | no relationship fields or hard-boundary handling | inert-listblock fixture; direct external blocks remain separate |

## Normative split

The wire format remains standard ATProto. The fork policy is:

1. direct blocks are individually authored durable boundaries;
2. list subscriptions are private attention tools;
3. review actions create ordinary individual block records only for selected
   members;
4. local governed listblock CREATE/UPDATE is rejected;
5. DELETE remains available for legacy cleanup;
6. CAR import inventories legacy listblocks before activation;
7. an incoming external direct block remains hard for interaction, while an
   external listblock is inert;
8. list membership changes never create new direct blocks.

These are `NORMATIVE / PRODUCT POLICY` choices, not ATProto requirements.
Keeping the Lexicon, repository format, CAR import, and direct block record is
`INTEROPERABILITY`.

## Migration ordering

```text
discover → create private mute → verify mute → obtain provider attestation
→ delete source with CID/CAS → verify deletion → write secret-free receipt
```

Mute failure leaves the source record. Delete failure leaves the verified mute.
Retries are idempotent and direct-block deltas remain zero unless the user
explicitly selected review blocks. Receipts hold counts and hashed source
identifiers, not a plaintext moderation graph or credentials.

## Provider boundary

The first-party PDS owns identity, repository writes, CAR import/export, sync,
and account state. The client selects AppView/feed/labeler/resolver providers
explicitly and displays their identity and health separately. AppViewLite and
FishyFlip are retired; they are not active implementations of relationship
semantics, auth, import, or provider attestation.

## Threat-model coverage

- alternate clients and `applyWrites` hit the same PDS policy boundary;
- standards-compliant CAR import is accepted into a visible migration state;
- mutable list membership changes attention only and create zero blocks;
- an external actor's direct hard boundary is not softened into local
  preference, and an external listblock cannot create a boundary;
- direct block behavior remains upstream-compatible;
- a malicious provider can supply a signed claim but cannot fabricate a PDS
  direct block or silently mutate association state;
- the private provider state is not copied into migration receipts or exports.

## Remaining scope

The exact custom-client live bypass walkthrough and populated alternate
provider/resolver/labeler failure walkthrough are owner-facing checks. They
are not replaced by a former provider's historical build or local experiment.
