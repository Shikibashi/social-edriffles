# AT Protocol best-practices gate

Status: `ALPHA-ONLY / PLUMBLINE PUBLIC HOST CONFIGURED / EXTERNAL GATES PENDING`

This gate records what the fork can prove locally and what remains an
external protocol or deployment obligation. Passing local tests does not
authorize production use of the Spaces alpha.

## Required before production consideration

- Keep the primary sign-in path on the official ATProto OAuth profile:
  DID/PDS authority verification, authorization-server discovery, PAR,
  authorization code flow, PKCE S256, state validation, DPoP, canonical HTTPS
  client metadata, refresh, revocation, and explicit scopes. The local Expo
  adapter owns OAuth tokens and keys; the app persists only an identity
  snapshot and PDS route.
- Keep `com.atproto.space.*` and `com.atproto.simplespace.*` behind an explicit
  alpha feature/deployment gate. The official Spaces announcement says the
  alpha may break and must not be used for production code.
- The client keeps the alpha path fail-closed unless a production build sets
  both `EXPO_PUBLIC_SPACES_ALPHA_ENABLED=1` and the separate
  `EXPO_PUBLIC_SPACES_ALPHA_PRODUCTION_ENABLED=1` acknowledgement. This is an
  explicit operational opt-in for the web community board, not a claim that
  the Spaces alpha is production-ready.
- The disposable credentialed OAuth protocol flow and deployed HTTPS/header
  probes pass on the canonical origin. The deployed credentialed Spaces
  removal test rejects both new and already-issued fork-owned credentials
  after member removal. An external Relay/AppView leak scan and the short-TTL
  expiry/replay walkthrough remain open. Never use production credentials for
  acceptance testing.
- Use the single owner-approved user-facing origin `https://plumblines.uk`.
  The edge route sends the web client and callback to Pages and sends the
  public PDS, OAuth, DID, and XRPC paths to the PDS implementation target.
  The public OAuth issuer and `did:web` service host are Plumbline; the
  `edriffles.us` PDS and Spaces hosts retain their existing technical roles.
  A fresh deployment must verify HTTPS, callback and metadata origin binding,
  cookie/header isolation, PDS host binding, and the configured custom-domain
  route. Historical cutover receipts do not prove a new source revision.

## Namespace and host cutover

The user-facing public and protocol host is `plumblines.uk`; the standards-
derived AT Protocol namespace remains `us.edriffles.radlib.*`. That namespace
and the `edriffles.us` PDS/Spaces infrastructure are compatibility-sensitive
technical boundaries, not public-product branding. If DNS Lexicon authority is
published, its existing record remains at `_lexicon.radlib.edriffles.us`.

The checked-in Lexicons and the live `_lexicon.radlib.edriffles.us` TXT record
are independently resolved through multiple DNS resolvers. The authority
receipt records this as current evidence. No `radlib.org` purchase or second
registrable domain is part of the contract.

## Local implementation guarantees

- The production source no longer imports or constructs
  `@atproto/lex-password-session`; the package remains only as a test fixture
  dependency. Web, iOS, and Android typechecks pass. Browser OAuth callback
  initialization, the OAuth scope fix, and the signup prompt are configured
  for `plumblines.uk`, with the edge Worker retaining the configured PDS
  implementation route. The current source binds the browser-facing account
  entryway to the public host; its deployed OAuth/PDS behavior must be
  re-probed after each Pages upload.
- The client metadata source is HTTPS-shaped, JSON-typed, accepted by the
  official ATProto metadata parser, and served publicly at the canonical
  origin. It registers the web callback at
  `https://plumblines.uk/oauth/callback` and the native reverse-domain callback
  `uk.plumblines:/oauth/callback`.
- The Space client validates Space references, DIDs, NSIDs, record keys, and
  returned repo-operation shapes before they reach application code.
- Sync cursor storage contains only positions and durable status. It records
  `synchronized`, `in-progress`, `desynchronized`, `authorization-revoked`,
  and `recoverable-error` states; it never stores private record bodies or
  blob bytes.
- Rebuildable indexes remain non-authoritative. A cached record does not grant
  access; reads still require a fresh viewer-authorized Space credential.

## Explicit alpha limitations

Standard upstream Space credentials may remain usable until expiry after
membership removal. The deployed fork-owned `us.edriffles.radlib.*` extension
adds an authority-status check and rejects both new and already-issued
credentials after removal. Aggregate multi-writer pagination, a server-side
private AppView, browser notification delivery, and full external
interoperability coverage remain deferred. These are blockers to production
claims, not hidden fallbacks.

The current local acceptance, canary receipt contract, and deployed single-host
cutover are recorded in
`artifacts/receipts/local-oauth-spaces-acceptance.json`,
`artifacts/receipts/local-private-canary-scan.json`,
`artifacts/receipts/authority-decision.json`,
`artifacts/receipts/radlib-edge-cutover-pending.json`, and
`artifacts/oauth-spaces-manifest.json`. The earlier Pages and PDS deployment
receipts remain marked historical because they tested the pre-cutover
topology.

The earlier `artifacts/receipts/oauth-migration.json` is historical protocol
evidence from a prior deployment and is not the current source-migration or
deployment verdict. The current source and cutover binding are recorded in
`artifacts/receipts/radlib-edge-cutover-pending.json` and
`artifacts/oauth-spaces-manifest.json`.

References: [AT Protocol OAuth](https://atproto.com/specs/oauth),
[Lexicon](https://atproto.com/specs/lexicon),
[Sync](https://atproto.com/specs/sync),
[Spaces Alpha](https://atproto.com/blog/atproto-spaces-alpha), and
[Going to production](https://atproto.com/guides/going-to-production).
