# Polycentric provider composition — iteration 1

**Status:** implemented locally; release and owner acceptance remain separate
gates.

**Scope:** identity and handle resolution. This is the first bounded slice of
the broader `social-edriffles` authority-reduction loop. It does not claim that
the whole client is decentralized or that multiple endpoints are independent
merely because they are numerous.

## 1. Residual authority concentration discovered

The client already had an explicit, replaceable AppView registry, but
`useResolveDidQuery` and `useResolveUriQuery` routed handle resolution through
the single AppView selected for the account. The existing identity runtime was
also not connected to that user-facing query. A selected AppView could therefore
become the invisible answer to an identity question even though identity is a
separate authority domain.

Two other concentrations remain visible and are intentionally not hidden by
this slice: the OAuth login path still requests a broad compatibility bundle,
and DID-document resolution still needs a method-specific resolver path rather
than a user-configurable set of independent PLC replicas.

## 2. Why it matters

An AppView is an index/read provider, not the owner of a DID or handle. A stale,
malicious, unavailable, or merely incomplete read provider should not silently
decide which DID a handle denotes. Sending a signed-in PDS token to every
candidate provider would replace one concentration with ambient authority, so
identity resolution must use public clients and keep account-PDS credentials on
the account host.

## 3. Existing ecosystem precedent

The design follows protocol boundaries that already exist rather than creating a
private identity protocol:

- The [AT Protocol OAuth specification](https://atproto.com/specs/oauth) makes
  the DID canonical, requires discovery and issuer/PDS binding, and requires
  DPoP, PAR, PKCE, exact redirects, and state handling.
- The [permissions specification](https://atproto.com/specs/permission)
  separates `repo`, `rpc`, `blob`, `identity`, and `account` permissions and
  constrains RPC permissions by lexicon method and audience.
- The [DID specification](https://atproto.com/specs/did) treats `did:plc` and
  `did:web` documents as the identity-method records, with handles as aliases
  that must verify bidirectionally.
- The [Labels specification](https://atproto.com/specs/label) treats labels
  as attributable metadata from an issuer, which is the same claim-versus-
  viewer-policy separation used here.
- [Cirrus](https://github.com/ascorbic/cirrus) separates Worker routing,
  Durable Object repository state, and R2 blobs; [Blacksky's rsky
  implementation](https://github.com/blacksky-algorithms/rsky) separates
  identity, OAuth, PDS, relay, feed generation, labeler, and Spaces crates.
  Blacksky's [AppView fork](https://github.com/blacksky-algorithms/atproto)
  also separates firehose/indexing, datastore, dataplane, AppView, and search.
- [`str4d/plc`](https://github.com/str4d/plc) is a useful user-held PLC key
  management precedent, but it is not treated as proof that this client has
  integrated recovery-key custody.

These projects demonstrate replaceable service boundaries and protocol
compatibility. They do not, by themselves, make a provider user-sovereign.

## 4. Chosen architectural change

The existing AppView registry now carries a declared capability set. The
identity query selects all enabled providers that declare
`identity-resolution`, rather than inheriting the feed/profile AppView choice.
Each provider is adapted to the existing identity-runtime contract and queried
concurrently through an unauthenticated public client. DID-method resolution
supplies the PDS endpoint needed to validate each claim; it does not grant that
PDS or AppView ownership of the identity.

The identity runtime now returns every usable claim, the resolver IDs that were
unavailable, an evidence status, and a policy-selected claim when one is
allowed. The default persisted policy is `require-agreement`. The Services
screen exposes explicit local alternatives: `first-verified` and
`prefer-provider`. Those alternatives preserve `disagreement` or
`resolver-unavailable` status, so selection is not mislabeled as consensus.

Legacy provider records without capabilities are normalized to `public-read`
only. Identity resolution is an explicit opt-in, so old registrations and new
providers do not silently gain a new authority. The Services screen exposes
that capability as a separate revocable choice. No session or PDS access token
is sent to a resolver merely because it is registered.

## 5. Authority before versus after

| Question | Before iteration 1 | After iteration 1 |
| --- | --- | --- |
| Which service resolves a handle? | The one account-selected AppView | Every enabled identity-capable provider |
| How are results represented? | One DID or one provider error | Attributable claims with provider ID, DID, endpoint, timestamp, and unavailable-provider list |
| What happens on disagreement? | No disagreement channel in the user-facing query | Default fail-closed error with the disputed claims attached |
| Who chooses an allowed partial result? | Implicit first network path | An explicit local policy owned by the user/device |
| Who can participate in identity resolution? | The selected AppView by inheritance | Only providers explicitly granted the capability on this device |
| What credentials cross the boundary? | Existing signed-in reads may use AppView service-auth | Identity resolver fan-out uses public clients; account-PDS tokens are not minted for resolver fan-out |
| Does an AppView become DID authority? | It could be the hidden answer for this query | It can propose a claim only; the client records evidence and policy separately |

If all configured providers are controlled by the same operator, the system has
not achieved independent authority. The capability registry and provenance
still make that fact inspectable, but actual plural authority requires users to
register providers operated under meaningfully different control.

## 6. Interoperability and security tradeoffs

- A handle lookup can make more than one public request, increasing latency,
  bandwidth, and the number of services that see the queried handle. This is an
  explicit consequence of choosing plural resolution; no account credential is
  added to those requests.
- The default agreement policy can temporarily block a lookup when one resolver
  is stale or offline. The explicit partial-result policies provide an exit for
  a user who accepts that risk, while retaining the evidence status.
- Provider claims are not cryptographic proof of a DID history. The adapter
  uses the existing DID-method PDS endpoint resolution and rejects unsafe
  endpoints; independent PLC replicas, signed-history comparison, and
  resolver-specific trust policy remain future work.
- The change keeps standard AT Protocol DIDs, handles, AppView XRPC, and PDS
  routing. It does not weaken OAuth, service-auth audience checks, DPoP, label
  boundaries, block semantics, abuse controls, or protocol records.
- Adding a provider is not a hidden fallback. Provider capability, policy,
  unavailable state, and disagreement remain local and inspectable.

## 7. Implementation evidence

- `upstream/social-app/src/lib/identity-runtime.ts` collects all resolver
  claims, validates DID/endpoint shape, detects mismatched or divergent claims,
  and applies the explicit local policy.
- `upstream/social-app/src/state/session/providers.ts` owns capability
  declarations, legacy normalization, and persisted identity policy validation.
- `upstream/social-app/src/state/persisted/schema.ts` persists the compatible
  capability and policy fields without making old provider records invalid.
- `upstream/social-app/src/state/queries/resolve-uri.ts` wires public
  identity-capable AppViews into the claim runtime and preserves provider/policy
  composition in the React Query key.
- `upstream/social-app/src/screens/Settings/ServicesSettings.tsx` exposes the
  policy choice and explains that it does not transfer identity ownership.
- `docs/flow-diagrams/provider-claim-reconciliation.mmd` describes the normal,
  unavailable, disagreement, and explicit-policy paths.

## 8. Tests proving the new boundary

The focused tests cover:

- two providers agreeing while both claims and provenance are retained;
- divergent DID/PDS claims failing closed under the default policy;
- an explicit preferred-provider policy selecting a claim without erasing the
  disagreement status;
- an unavailable provider being recorded and requiring an explicit partial
  result policy;
- capability filtering that excludes a public-read-only provider from identity
  resolution while normalizing a legacy provider;
- persistence and validation of a preferred identity resolver.
- identity capability opt-in and revocation, including safe reset of a policy
  that preferred a provider whose capability was removed.

The local verification record for this iteration is:

| Check | Status | Evidence |
| --- | --- | --- |
| Identity runtime and provider tests | PASS | 21 tests in the focused Jest run |
| Web TypeScript check | PASS | `pnpm run typecheck:web` |
| Targeted Oxlint | PASS | Changed client files |
| Root contract validator | PASS | `python3 scripts/validate_contract.py` — 125 files, 29 blocking rows, 6 feed cases |
| Production-shaped web build | PASS | `pnpm run build-web`; export completed with existing bundle-size warnings |
| Full client test suite | FAIL (baseline environment) | 290 passed; 7 existing session snapshot failures because `.env.local` selects `pds.edriffles.us` while snapshots expect the older web-origin service |
| iOS/Android typecheck | FAIL (baseline) | Existing `SessionData`/installed `@atproto/lex-password-session` incompatibilities and `Logomark` style error; no changed-file error |
| Full client lint/format | FAIL (baseline) | Existing import-sort, unused-variable, type-rule, suppression, and 33 formatting findings; changed files pass targeted checks |
| Deployment | NOT RUN | No deployment is claimed from this iteration; full repository gates remain unresolved |

## 9. Iteration 2 — user-visible provider evidence

The first implementation left successful composed reads as the selected API
value in most screens. That was compatible, but it made the provider seam
visible only on selected feed surfaces or when a read failed. Iteration 2 keeps
the existing selected-value contract and carries the complete composition
alongside it for progressive inspection.

### Authority before versus after

| Surface | Before iteration 2 | After iteration 2 |
| --- | --- | --- |
| Profile | Selected profile view without source evidence | Profile view plus expandable provider observations and reconciliation policy |
| Thread | Selected thread without source evidence | Thread view plus the same evidence; PDS fallback clears AppView evidence |
| Search | Selected page without source evidence | Each loaded page retains its search-provider composition |
| Notifications | Selected page without source evidence | Each fetched page retains notification-provider composition; unread cache remains explicitly cache-backed |
| Label service | Selected labeler metadata without source evidence | Label-service metadata carries its composed provider observations |
| Provider failure | Error text could hide the cause of disagreement | Fail-closed errors retain the composition for inspection where the boundary exposes it |

### Implementation evidence

- `upstream/social-app/src/components/ProviderCompositionProvenance.tsx` is a
  shared progressive inspector for status, policy, selected providers,
  declared operator IDs, endpoints, freshness, verification, and errors. It
  states that declared operator identity is not proof of independent control.
- `upstream/social-app/src/state/queries/profile.ts` and
  `upstream/social-app/src/state/queries/usePostThread/` retain composition
  only when the displayed value came from the composed AppView boundary.
  Account-PDS fallback values do not inherit stale AppView provenance.
- `upstream/social-app/src/state/queries/search-posts-v2.ts`,
  `notifications/feed.ts`, and `labeler.ts` retain composition at their
  existing query/page boundaries; no parallel cache or provider registry was
  introduced.
- `upstream/social-app/src/view/screens/Profile.tsx`,
  `screens/PostThread/index.tsx`, `screens/Search/SearchResults.tsx`,
  `view/com/notifications/NotificationFeed.tsx`, and
  `screens/Profile/Sections/Labels.tsx` expose the seam progressively.

### Verification evidence

| Check | Status | Evidence |
| --- | --- | --- |
| Profile/thread/provider/identity focused tests | PASS | 8 suites, 52 tests |
| Search/notification/provider focused tests | PASS | 5 suites, 61 tests |
| Label-service/provider focused tests | PASS | 4 suites, 28 tests |
| Web TypeScript check | PASS | `pnpm run typecheck:web` |
| Changed-file Oxlint | PASS | New and modified client files |
| Changed-file Prettier and whitespace | PASS | `pnpm exec prettier --check`; `git diff --check` |
| Deployment | PASS | Wrangler Pages deployment completed at `https://7361cb4b.social-edriffles.pages.dev`; canonical `https://plumblines.uk/` serves the Plumbline bundle and the credential-free public-contract probe passes without writes |

This iteration improves contestability without claiming that the selected
provider is independently operated, cryptographically authoritative for every
view, or current in an eventually consistent network. Media remains an
account-PDS boundary and communities remain a Spaces/Radlib boundary; neither
is falsely routed through the generic AppView composition layer.

## 10. Iteration 3 — canonical Plumbline share URLs and thread provenance

The next UI pass closed a remaining product-identity leak at the shared-link
boundary. Internal profile, post, feed, list, embed, hashtag, topic, and search
links now resolve against the runtime Plumbline origin rather than defaulting to
`bsky.app`. Absolute external HTTP(S) links remain unchanged. The thread view
also retains the existing feed-row `Why this post?` inspector when a post is
opened from a feed, and the Moderation & Reach web link now points to
`plumblines.uk`.

### Implementation and verification evidence

- `upstream/social-app/src/lib/strings/url-helpers.ts` uses the existing
  runtime-origin resolver for internal share paths and preserves external
  HTTP(S) URLs.
- `upstream/social-app/src/screens/Hashtag.tsx`, `Topic.tsx`, and
  `Search/Shell.tsx` use the shared helper; no ATProto lexicon or provider
  endpoint was renamed.
- The client commit is `dca8068f2` and is pushed to
  `fork/codex/spaces-alpha-integration`.
- URL-helper and attention tests pass (8 tests total); targeted Oxlint,
  Prettier, whitespace, and `pnpm run typecheck:web` pass.
- `pnpm run build-web` completed with the existing bundle-size warnings, and
  Wrangler deployed the exact export at
  `https://7361cb4b.social-edriffles.pages.dev`.
- The live public-contract probe passed at `2026-08-30T08:16:45Z` with
  `credentialsUsed: false` and `writesPerformed: false`; the hosted shell
  serves the Plumbline title, mark, and `main.5bcabf4f.js` bundle.

This iteration changes presentation and share authority only. It does not make
the public AppView authoritative, prove independent PLC operators, or close the
credentialed OAuth expiry/replay and private Relay/AppView canary gates.

## 11. Iteration 4 — canonical chat links and app-icon identity

The current UI batch extends the canonical Plumbline boundary into chat invite
links and native app-icon settings. New copied invite links and chat reply
previews use the runtime Plumbline origin. The URL helper accepts both exact
Plumbline and reference `bsky.app` application origins for post, feed, list,
starter-pack, RSS, and chat-path recognition, preserving interoperability while
rejecting lookalike hosts. App-icon settings now labels the internal set as
“Plumbline variants” and “Plumbline Classic”; technical package and asset IDs
remain unchanged.

### Implementation and verification evidence

- Client commit `250a3cf40` was pushed to
  `fork/codex/spaces-alpha-integration`.
- URL-helper tests pass 4/4; targeted Oxlint, Prettier, whitespace checks, and
  `pnpm run typecheck:web` pass.
- `pnpm run build-web` completed with the existing bundle-size warnings and
  produced the Plumbline title, mark, metadata, and canonical share-origin
  export.
- The deployment step will use the exact generated `web-build` output; no
  account credentials or write operations are part of this UI verification.

This is a presentation and link-boundary change. It does not rename ATProto
protocol namespaces, external service identifiers, or the provider provenance
shown when Bluesky is the actual external service.

## 12. Iteration 5 — canonical profile invites and starter-pack links

The client now applies the runtime Plumbline origin to profile invite QR and
share output as well as starter-pack share links. The display and copy paths
share one canonical generator, while existing reference `bsky.app` links
remain parseable for interoperability. This removes another user-facing
product-identity redirect without changing ATProto record or provider
identifiers.

### Implementation and verification evidence

- `upstream/social-app/src/features/inviteFriends/urls.ts` uses
  `getRuntimePublicWebOrigin()` for new profile share output.
- `upstream/social-app/src/lib/routes/links.ts` uses the same runtime-origin
  boundary for starter-pack links.
- Focused invite and route-link suites pass 13/13 tests; targeted Oxlint,
  Prettier, whitespace checks, and `pnpm run typecheck:web` pass.
- `pnpm run build-web` completed with the existing bundle-size warnings. The
  generated `web-build` is the artifact intended for the next Pages deploy;
  live deployment evidence is recorded only after Wrangler and the public
  contract probe run.

This iteration changes only user-facing share destinations. It does not make
the web client, a bundled provider, or a starter-pack AppView authoritative
over the underlying ATProto records.

## 13. Iteration 6 — canonical quote, draft, chat, and RSS paths

The internal post-link generators now use the shared runtime-origin helper.
Quote composition, draft restoration, embedded-post chat previews, and
relative RSS opening stay on Plumbline for new internal links. Canonical RSS
URLs are classified as internal alongside legacy `bsky.app` URLs, so the
change does not turn a supported reference link into an external destination.

### Implementation and verification evidence

- `upstream/social-app/src/state/shell/composer/index.tsx` and
  `upstream/social-app/src/view/com/composer/state/composer.ts` use the
  runtime helper for quote precaching and quote embed URLs.
- `upstream/social-app/src/view/com/composer/drafts/state/api.ts` uses the
  runtime helper when restoring persisted quote embeds.
- `upstream/social-app/src/components/dms/getMessageInfo.ts` and
  `upstream/social-app/src/lib/hooks/useOpenLink.ts` use the same boundary for
  embedded post previews and relative RSS paths.
- `upstream/social-app/src/lib/strings/url-helpers.ts` removes the obsolete
  internal Bsky-origin generators and recognizes canonical Plumbline RSS.
- The focused URL and route suites pass 17/17 tests; targeted Oxlint,
  Prettier, whitespace checks, and `pnpm run typecheck:web` pass.
- Client commit `fd5b65112` was pushed to
  `fork/codex/spaces-alpha-integration`, and Wrangler deployed the exact
  export at `https://61288ec7.social-edriffles.pages.dev`. The canonical
  shell and preview serve the Plumbline title, mark, and
  `main.16493acb.js`; the live public-contract probe passed at
  `2026-08-30T08:50:12Z` with no credentials and no writes.

This is a destination and classification change only. ATProto collection
names, external provider URLs, account-PDS writes, and legacy reference-link
compatibility remain unchanged.

## 14. Iteration 7 — inspectable account-PDS profile media

The owner-profile path already kept the account PDS authoritative for avatar
and banner blob references, but that authority was not visible in the UI. The
client now carries typed media provenance beside the owner profile, retains
the direct `com.atproto.sync.getBlob` delivery path, and exposes a progressive
profile inspector for the PDS endpoint, record owner, protocol method, and
blob CIDs. This makes the existing boundary contestable without inventing a
second media authority or promoting a CDN URL to record ownership.

### Implementation and verification evidence

- `upstream/social-app/src/lib/api/account-profile.ts` owns CID extraction,
  safe HTTP(S) PDS-origin normalization, direct blob URL derivation, and
  `AccountProfileMediaProvenance`.
- `upstream/social-app/src/components/MediaDeliveryProvenance.tsx` and
  `upstream/social-app/src/view/screens/Profile.tsx` expose the source only
  when owner-PDS media evidence exists. The expanded view states that an
  AppView or CDN can be a cached delivery view but cannot replace the account
  profile record.
- `upstream/social-app/src/lib/api/account-profile.test.ts` passes all 6
  focused tests, including valid provenance and missing-endpoint/blob refusal.
  Web TypeScript, targeted Oxlint, Prettier, and whitespace checks pass.
- Client commit `0774e978e` is pushed to
  `fork/codex/spaces-alpha-integration`; the root gitlink is advanced only
  after this client commit is integrated below.
- Wrangler deployed the exact export at
  `https://22c77414.social-edriffles.pages.dev`; the preview and canonical
  `https://plumblines.uk/` serve the Plumbline title, mark, and
  `main.40c760a2.js` bundle.
- The credential-free public-contract probe passed at
  `2026-08-30T09:06:34.065473Z` with no credentials and no writes. The
  connected ChatGPT in-app browser loaded the canonical public shell, feed
  content, media, and provenance controls; it was not used for signed-in
  mutations.

The slice does not claim general media-provider plurality. Non-owner profile
media remains the existing public AppView/CDN view until a safe, verified PDS
endpoint can be derived without sending account credentials to public readers.

## 15. Iteration 8 — make provider substitution reachable from evidence

The provider-composition inspector already made source, disagreement, and
limitations visible, but it stopped at explanation. This iteration adds a
progressive `Change read provider` action to the expanded inspector. The
action routes to the existing Services workbench, where the user can select
capabilities, reconciliation, and provider configuration. It does not create
a second provider-settings store or silently change the active provider.

### Implementation and verification evidence

- `upstream/social-app/src/components/ProviderCompositionProvenance.tsx`
  adds the accessible action and keeps it inside the expanded evidence view.
  It uses the existing `ServicesSettings` route and provider-composition
  policy.
- Web TypeScript, targeted Oxlint, Prettier, whitespace validation, and the
  production web export pass. The bundle retains the Plumbline title, icon,
  and public-origin configuration.
- Client commit `30e165ef3` was pushed to
  `fork/codex/spaces-alpha-integration`.
- Wrangler deployed the exact export at
  `https://95255e0f.social-edriffles.pages.dev`; the preview and canonical
  `https://plumblines.uk/` return HTTP 200, the Plumbline title, and
  `main.12405af4.js`.
- The credential-free ChatGPT in-app-browser smoke check loaded the canonical
  shell, populated public feed content, and exposed the existing provenance
  control. No credentials were read and no mutation was performed.

This is a reachability improvement at the existing policy boundary. It does
not claim that every surface has an independent provider available, or that
the canonical public smoke check proves signed-in provider mutation behavior.

## 16. Iteration 9 — route provider changes to the relevant workbench section

The provider-change affordance now carries an explicit typed destination into
Services. Provider evidence and feed/provider error recovery open the
Providers section directly; identity evidence opens the Identity section.
Community and custom-feed provider controls use the same route contract. This
reduces the gap between explaining a provider boundary and giving the user a
real replacement path without adding surface-specific settings stores.

### Implementation and verification evidence

- `upstream/social-app/src/lib/routes/types.ts` defines the optional
  `ServicesSettingsSection` route parameter, and
  `upstream/social-app/src/screens/Settings/ServicesSettings.tsx` honors it
  while preserving the normal overview default.
- Provider composition, feed, custom-feed, post-feed-error, and community
  controls pass the relevant `providers` or `identity` section explicitly.
- Web TypeScript, targeted Oxlint, Prettier, whitespace validation, focused
  provider/identity/OAuth/PLC tests (33 tests), and the production web export
  pass.
- Client commit `fdfd0213d` was pushed to
  `fork/codex/spaces-alpha-integration`.
- Wrangler deployed the exact export at
  `https://b6788290.social-edriffles.pages.dev`; the preview and canonical
  `https://plumblines.uk/` return HTTP 200, the Plumbline title, and
  `main.93da2ac9.js`.
- The credential-free ChatGPT in-app-browser smoke check loaded the canonical
  shell, populated feed tabs, and loaded a public profile without an error.
  No credentials were read and no mutation was performed.

The browser smoke check does not claim that an authenticated provider switch
was performed. It verifies the deployed route shell; authenticated selection
remains guarded by the existing session and provider availability checks.

## 17. Iteration 10 — make identity exit utilities first-class

The Identity & recovery workbench now exposes the existing exit utilities at
the same boundary as DID, PDS, recovery, and session state. It reuses the
repository/chat export dialog and links to the existing portable policy backup
controls rather than introducing duplicate state or a second exporter. The
migration status remains honest: an unavailable upstream migration API is not
presented as a completed migration workflow.

### Implementation and verification evidence

- `upstream/social-app/src/screens/Settings/IdentitySovereigntySettings.tsx`
  adds an Exit utilities group with repository/chat export and a route to
  portable policy backup, import, and reset controls.
- The existing CAR / JSONL exporter remains the implementation boundary and
  keeps credentials excluded; the existing Personalization workbench remains
  the policy backup boundary.
- Client commits `688a0e2d0` and `7ff0c06fe` were pushed to
  `fork/codex/spaces-alpha-integration`.
- Targeted Oxlint, Prettier, whitespace validation, web TypeScript, and the
  focused provider/identity/PLC-custody/OAuth suite pass (33 tests).
- Wrangler deployed the exact export at
  `https://d7bbfe2a.social-edriffles.pages.dev`; the preview and canonical
  `https://plumblines.uk/` return HTTP 200, the Plumbline title, and
  `main.0e1bc6c1.js`.
- The credential-free ChatGPT in-app-browser smoke check loaded the canonical
  shell with Plumbline branding and feed tabs and without an error state. No
  credentials were read and no mutation was performed.

This makes export and portable policy controls directly discoverable from the
identity boundary. It does not claim that an authenticated export was run in
the browser or that PDS migration is available when the upstream API is not.

## 18. Iteration 11 — carry provider provenance into post inspection

The feed query already retained provider provenance, composition status, and
the limits of declared operator identity, but the evidence stopped at the
feed-level workbench. This iteration carries that typed metadata with each
feed slice and transient post source so the post's `Why this post?` inspector
can identify the read provider(s), endpoint, service DID, declared operator,
composition status, and whether independent control has actually been proven.

### Implementation and verification evidence

- `upstream/social-app/src/state/queries/post-feed.ts` attaches page-level
  provider metadata to each `FeedPostSlice`; `PostFeed` and `PostFeedItem`
  preserve it for the rendered post and the post-thread transition.
- `upstream/social-app/src/components/Post/PostProvenance.tsx` and
  `upstream/social-app/src/lib/attention-ui.ts` expose bounded provider
  identifiers and endpoints, composition status, and the explicit
  `independent control not proven` limitation. The data remains inspectable
  and does not promote a provider merely because it was selected.
- `upstream/social-app/src/state/unstable-post-source.tsx` and
  `upstream/social-app/src/screens/PostThread/components/ThreadItemAnchor.tsx`
  preserve the same evidence when a user opens a post detail view.
- The focused attention/provider/identity/PLC/OAuth suite passes (39 tests),
  targeted Oxlint and Prettier pass, web TypeScript passes, and the production
  web export contains the new post-inspector labels.
- Client commit `586491ade` was pushed to
  `fork/codex/spaces-alpha-integration`.
- Wrangler deployed the exact export at
  `https://91b75138.social-edriffles.pages.dev`; the preview and canonical
  `https://plumblines.uk/` return HTTP 200, the Plumbline title, and
  `main.d4df7bec.js`.
- The credential-free ChatGPT in-app-browser smoke check loaded the canonical
  shell with the Plumbline title, feed tabs, and post-provenance affordance,
  with no error state. No credentials were read and no mutation was performed.

This closes a provenance visibility gap in the client UI. It does not prove
authenticated provider switching, independent operator control, or the
external Relay/AppView and short-TTL OAuth gates.

## 19. Iteration 12 — make policy ownership explicit in settings

The settings UI previously sent users directly to provider-owned policy URLs
from the About and Privacy & Security screens. That made the browser destination
look like an implicit Plumbline policy and left the source boundary unclear.
This iteration routes those actions through the existing local support screens,
which identify the hosting provider as the policy owner before exposing the
external document. Takedown, community-guideline, and copyright copy now uses
the same source-explicit language.

### Implementation and verification evidence

- `upstream/social-app/src/screens/Settings/AboutSettings.tsx` now exposes
  `Provider Terms of Service` and `Provider Privacy Policy` through the
  existing `/support/tos` and `/support/privacy` routes.
- `upstream/social-app/src/screens/Settings/PrivacyAndSecuritySettings.tsx`
  now labels its policy link as the hosting provider's privacy policy and uses
  the same internal support route. `Takendown.tsx`, `CommunityGuidelines.tsx`,
  and `CopyrightPolicy.tsx` explicitly identify provider ownership without
  inventing a Plumbline legal policy.
- The focused attention/provider/identity/PLC/OAuth suite passes (39 tests),
  targeted Oxlint and Prettier pass, web TypeScript passes, and the web export
  completes with only the existing bundle-size warnings.
- Client commit `4f87b2880` was pushed to
  `fork/codex/spaces-alpha-integration`.
- Wrangler deployed the exact export at
  `https://b41a65f2.social-edriffles.pages.dev`; the preview and canonical
  `https://plumblines.uk/` return HTTP 200 and the export uses
  `main.94d5b092.js`.
- The credential-free ChatGPT in-app-browser smoke check verified the
  Plumbline home shell, the provider-labelled About links, and the provider
  privacy support route without an error state. No credentials were read and
  no mutation was performed.

This reduces a user-facing authority ambiguity. It does not change the
hosting provider's legal documents, establish independent policy authority, or
close the external Relay/AppView, short-TTL OAuth, or PLC-operator gates.

## 20. Iteration 13 — make provider ownership visible on support and identity entry points

The previous policy-link work did not cover every user-facing entry point. The
support screen still described the help destination as if Plumbline itself
owned the support relationship, the age-gate linked directly to an unlabeled
provider document, and the custom-handle flow used an unsourced “Learn more”
label. This iteration keeps the existing provider destinations but makes their
ownership explicit and keeps the links addressable through the existing
Plumbline support routes where appropriate.

### Implementation and verification evidence

- `upstream/social-app/src/view/screens/Support.tsx` now identifies the
  hosting provider's support form while preserving the external help-desk
  destination.
- `upstream/social-app/src/components/dialogs/BirthDateSettings.tsx` now
  routes the age-gate policy link through `/support/tos` and labels it as the
  hosting provider's Terms of Service.
- `upstream/social-app/src/screens/Settings/components/ChangeHandleDialog.tsx`
  now labels the existing provider domain-handle article as the hosting
  provider's domain-handle guide; the external provider URL remains intact.
- `upstream/social-app/src/locale/locales/en/messages.po` was regenerated and
  the compiled English catalog was rebuilt. The live route previously exposed
  the generated message ID `kfpVmS`; the post-build browser probe now shows the
  complete English support sentence and no message ID.
- Targeted `git diff --check`, Prettier, and Oxlint pass. The focused OAuth,
  provider-composition, attention, and account-profile suites pass (40 tests).
  The production web export completes with only the existing bundle-size
  warnings.
- Client commits `4a6bab405` and `4f9d54fd6` were pushed to
  `fork/codex/spaces-alpha-integration`.
- Wrangler deployed the corrected export at
  `https://d6bbc7bf.social-edriffles.pages.dev`; the canonical
  `https://plumblines.uk/` browser check verified the provider-labelled
  support copy, provider terms/privacy labels, `Following — Plumbline` home
  title, `/plumbline-mark.svg` favicon, and no visible error state. No
  credentials were read and no mutation was performed.

This makes three remaining provider-owned destinations inspectable without
pretending they are Plumbline-operated services. It does not change provider
policy, establish independent operator control, or close the external
Relay/AppView, short-TTL OAuth, or PLC-operator gates.

## 21. Remaining concentrations worth attacking next

1. **OAuth ambient grant (highest value):** split the compatibility scope bundle
   into feature-scoped permission requests and an explicit reauthorization or
   upgrade path. Do not remove scopes without preserving posting, likes,
   profile edits, chat, and Spaces behavior.
2. **One AppView per other read surface:** extend the same capability/claims
   model to profiles, threads, feeds, search, notifications, media, and
   communities, while measuring cost and avoiding PDS service-auth fan-out.
3. **Resolver plurality:** add independently operated resolver configurations,
   cryptographic DID-document/history verification, signed receipts, and
   disagreement UI. A list of PLC URLs controlled by one operator would not
   satisfy this goal.
4. **Portable policy exit:** export/import/reset provider capabilities,
   reconciliation policies, and local attention/moderation policy without
   exporting secrets or changing DID/PDS identity.
5. **User-held identity recovery:** integrate hardware-backed or separately
   controlled PLC rotation/recovery workflows only where current protocol APIs
   support safe custody and recovery; keep the PDS as host, not identity
   continuity authority.
6. **Operator and community jurisdiction:** keep legitimate refusal-to-host,
   abuse prevention, and private Space ACL authority narrow and attributable;
   do not convert any of them into universal public-visibility authority.
