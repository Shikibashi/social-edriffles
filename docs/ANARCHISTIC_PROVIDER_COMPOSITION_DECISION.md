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

## 21. Iteration 14 — distinguish the account service from the repository PDS

The Services and Identity workbenches previously used the active account's
generic `service` value as a fallback for the repository host. For hosted
OAuth sessions that value can identify the login or account-entryway service,
not the PDS that stores the user's repository. This iteration aligns both
workbenches with the session-state contract: login authority and repository
hosting are separate rows, and an unavailable DID-backed PDS is shown as
unknown rather than inferred.

### Implementation and verification evidence

- `upstream/social-app/src/screens/Settings/ServicesSettings.tsx` now labels
  the generic service as `Account service (login)` and adds a separate
  `Repository PDS` row sourced only from `currentAccount.pdsUrl`. Missing
  DID-backed PDS state is rendered as `Not available from the DID-backed
  session state`.
- `upstream/social-app/src/screens/Settings/IdentitySovereigntySettings.tsx`
  now labels the PDS as `Repository PDS (from DID document)` and the generic
  service as `Session login service`; it no longer presents the login service
  as the PDS.
- Existing `upstream/social-app/src/state/session/session-data.ts` behavior
  and session-core coverage continue to prove that `pdsUrl` does not fall back
  to the login service. Targeted Prettier, Oxlint, and `git diff --check` pass;
  the focused session and identity suite passes (43 tests).
- Client commit `fc0898981` was pushed to
  `fork/codex/spaces-alpha-integration`.
- The generated web export contains `main.05652ee9.js` and Wrangler deployed
  it at `https://3096c3e8.social-edriffles.pages.dev`. The credential-free
  ChatGPT in-app-browser check of the canonical Plumbline deployment verified
  `Services — Plumbline`, the separate account-service and repository-PDS
  labels, the explicit unavailable PDS state, `Identity sovereignty —
  Plumbline`, and the separate identity labels. The home route remained
  `Following — Plumbline` with no visible error. No credentials were read and
  no mutation was performed.

This removes a user-facing authority conflation without claiming that the
client can discover a PDS when the DID-backed session state does not provide
one. It does not establish independent operators, close the external
Relay/AppView or short-TTL OAuth gates, or prove authenticated write flows.

## 22. Iteration 15 — recover the repository PDS during browser OAuth initialization

The deployed browser callback path could authenticate through the Plumbline
OAuth entryway while leaving the repository PDS absent from the persisted
account snapshot when the identity response omitted `didDoc`. This made the
login service look like the only account authority and left later requests
without an explicit repository route. The existing DID-backed resolver is now
used as the recovery boundary, with the resolved endpoint retained across
refresh and persisted-session reconstruction.

### Implementation and verification evidence

- `upstream/social-app/src/state/session/oauth-session.ts` resolves a missing
  repository PDS from the authenticated DID and keeps the endpoint available
  to the session adapter across token rotation. `plumblines.uk` remains the
  OAuth issuer/account service; `pds.edriffles.us` remains the DID-declared
  repository host.
- The omitted-`didDoc` regression fixture and the focused OAuth,
  PDS-resolution, and session suite pass (23 tests). Targeted Oxlint,
  Prettier, web TypeScript, and the production web export pass; the export
  reports only the existing bundle-size warnings.
- The exact export was deployed at
  `https://e6660482.social-edriffles.pages.dev`. The credential-free
  in-app-browser probe showed the separate account service and repository PDS
  rows, a loaded post feed, the owner profile, and PDS-backed media
  provenance. No credentials were read and no authenticated mutation was
  performed.

This removes a concrete session-routing concentration without making the PDS
the OAuth authorization server by assumption. It does not close the external
Relay/AppView, short-TTL OAuth, or independent PLC-operator gates.

## 23. Iteration 16 — make the service authority map inspectable

The Services workbench already exposed provider registration and policy
controls, but the overview required users to infer the relationship between
identity, hosting, read providers, authorization, moderation, media, and
communities from separate rows and sections. This iteration adds a compact
capability map to the existing overview. It keeps the current session and
provider registry as the sources of truth; it does not add a new service or
make the bundled AppView authoritative.

### Implementation and verification evidence

- `upstream/social-app/src/screens/Settings/ServicesSettings.tsx` now presents
  an explicit capability map for Identity, Personal Data Server, AppView
  reads, Feeds, Moderation & Reach, Search, Notifications, Authorization,
  Media, Communities, and Exit & backups. Each row identifies the current
  source, state, explanation, and an `Inspect` action into the existing
  workbench section.
- Boundary-owned media and community services remain labeled as such instead
  of being exposed as AppView choices. Provider names and endpoints are still
  rendered as inspectable values, and no account credential is moved across a
  provider boundary by this UI change.
- The map keeps a wide table-like layout only at the wide-tablet breakpoint;
  narrower workspaces stack source and state details so the Inspector does not
  make the primary service surface unreadable.
- Targeted Prettier, Oxlint, and web TypeScript checks pass. The production web
  export completes with the existing bundle-size warnings and was deployed to
  `https://177916bd.social-edriffles.pages.dev` behind the canonical
  `https://plumblines.uk` host. The credential-free in-app-browser check found
  all eleven rows, no error state, and a working Identity inspection action.

This makes the service seams legible in one place while preserving the existing
authority boundaries. It does not establish independent operator control,
close the external Relay/AppView or short-TTL OAuth gates, or prove
credentialed write behavior.

## 23. Iteration 17 — route service inspection to the owning boundary

The capability map made service seams visible, but several `Inspect` actions
still opened a generic Services section even when the capability had an
existing authority-owned settings surface. This iteration keeps the map as
the entry point while routing each action to the screen that can actually
explain or change that boundary.

### Implementation and verification evidence

- `upstream/social-app/src/screens/Settings/ServicesSettings.tsx` now gives
  each row an explicit workbench destination. Provider-backed identity,
  AppView, feed, search, notification, and authorization rows remain in the
  Services workbench; Moderation & Reach opens moderation settings, Media
  opens Content & Media, Communities opens private Spaces settings, and
  Personal Data Server plus Exit & backups open Identity sovereignty.
- The destination is modeled as a typed Services-section or route target, so
  adding a capability row cannot silently turn its inspection action into a
  generic provider redirect.
- Prettier, Oxlint, web TypeScript, and the production web export pass. The
  export was deployed to `https://8ef923ad.social-edriffles.pages.dev` behind
  `https://plumblines.uk`. The credential-free ChatGPT in-app-browser check
  exercised all five route-backed actions, confirmed the expected URLs and
  titles, found no error state, and returned to the Services overview.

This makes the authority map actionable without adding a second settings
system or changing provider selection, PDS routing, OAuth grants, or account
data. It does not establish independent operators, close the external
Relay/AppView or short-TTL OAuth gates, or prove credentialed write behavior.

## 24. Remaining concentrations worth attacking next

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

## 25. Iteration 18 — persistent feed authority summary

The feed surface previously exposed its provider and ordering model only after
the user opened `Show feed details`. That made the ordinary timeline look
more authoritative than the underlying composed read actually was: a user
could see posts without seeing which feed and provider supplied the current
candidate set. The existing provenance inspector remains the detailed seam;
this iteration adds a compact summary beside it rather than creating a second
feed-state model.

### Authority before versus after

| Surface | Before iteration 18 | After iteration 18 |
| --- | --- | --- |
| Active feed context | Provider and ordering hidden behind an expansion | Feed name, ordering model, and source provider visible in the ordinary view |
| Provider substitution | Available from expanded details | Still available from the same existing inspector and Services route |
| Protocol evidence | Detailed feed/provider IDs remained inspectable | Detailed IDs remain inspectable; the summary does not imply verification or operator independence |

### Implementation and verification evidence

- `upstream/social-app/src/components/FeedProvenanceCard.tsx` now renders a
  compact, accessible `feed-provenance-summary` with the active feed name,
  algorithm/order label, and source provider. The existing expanded details
  retain provider DIDs, observations, health, privacy, feed URI, and
  change-provider controls.
- The summary uses the existing theme contrast token and Plumbline's vertical
  rule grammar. The disclosure control now has an explicit border while
  preserving its existing state and browser-visible interaction.
- The feed still receives candidates from the configured provider boundary;
  this UI change does not make a provider authoritative, add a hidden
  fallback, or move account credentials across services.

### Verification

| Check | Status | Evidence |
| --- | --- | --- |
| Feed attention model tests | PASS | `upstream/social-app/src/lib/attention-ui.test.ts` — 6 tests |
| Targeted Prettier | PASS | `pnpm exec prettier --check src/components/FeedProvenanceCard.tsx` |
| Targeted Oxlint | PASS | `pnpm exec oxlint --quiet src/components/FeedProvenanceCard.tsx` |
| Web TypeScript | PASS | `pnpm run typecheck:web` |
| Production-shaped web export | PASS | `pnpm run build-web`; export completed with the existing bundle-size warnings |
| Deployed browser verification | PASS | Wrangler deployment `https://4d5949ec.social-edriffles.pages.dev`; canonical `https://plumblines.uk/?deployment=4d5949ec` loaded in the ChatGPT in-app browser with 4 summaries, 1 feed-details control, 96 like controls, 32 reply controls, 32 repost/quote controls, and no application error |

This iteration improves ordinary-view legibility of feed authority without
claiming provider independence, cryptographic feed manifests, or completion
of the external OAuth/Relay/AppView/PLC gates.

## 26. Iteration 19 — delegated OAuth authority inspector

The client already had a feature-scoped OAuth ledger and upgrade path, but the
Authorization workbench reduced that state to permission counts. That hid the
institutional boundary that matters to the user: which feature is delegated,
for what purpose, to which resource, and whether the current grant is native,
legacy-compatible, or still absent.

### Authority before versus after

| Surface | Before iteration 19 | After iteration 19 |
| --- | --- | --- |
| OAuth grant explanation | Feature rows showed counts or an upgrade action | Each feature can expose purpose, authority, resource, audiences, requested scopes, granted scopes, and missing scopes |
| Revocation | Session revocation existed elsewhere in account settings | Authorization explains that revocation is whole-session and exposes the existing session logout action without claiming per-feature revocation |
| Spaces upgrade path | Missing Spaces access redirected to the provider selector | Community composer/read gates open the Authorization workbench directly |

### Implementation evidence

- `upstream/social-app/src/state/session/oauth-scopes.ts` now derives
  presentation metadata from the existing scope ledger. It does not add a
  second permission model or include access tokens, refresh tokens, keys, or
  cookies.
- `upstream/social-app/src/components/AuthorizationProvenance.tsx` adds a
  progressive disclosure inspector to the existing Services Authorization
  section. The ordinary view remains compact; the expanded view identifies the
  account, recorded OAuth service, account PDS, feature purpose, authority,
  audience, exact scope strings, upgrade action, and whole-session revocation
  boundary.
- `upstream/social-app/src/screens/Settings/ServicesSettings.tsx` reuses the
  existing upgrade and logout APIs. No write path was silently changed, so
  posting, likes, profile edits, chat, and Spaces retain their current
  compatibility behavior while the delegated authority becomes inspectable.
- `upstream/social-app/src/screens/CommunityBoardScreen.tsx` now routes missing
  Spaces permission prompts to Authorization rather than Providers.

### Verification

| Check | Status | Evidence |
| --- | --- | --- |
| OAuth permission contract | PASS | `src/state/session/__tests__/oauth-scopes-test.ts` — 11 tests |
| Targeted Prettier | PASS | All five touched TypeScript/TSX files |
| Targeted Oxlint | PASS | All five touched TypeScript/TSX files |
| Web TypeScript | PASS | `pnpm run typecheck:web` |
| Production-shaped web export | PASS | `pnpm run build-web`; completed with existing bundle-size warnings |
| Repository contract validation | PASS | `python3 scripts/validate_contract.py` — 144 files, 29 blocking rows, 6 feed cases |
| Client commit and fork push | PASS | `168a70986 ui: expose delegated oauth authority`; pushed to `https://github.com/Shikibashi/social-app` branch `codex/spaces-alpha-integration` |
| Hosted anonymous/home check | PASS | Wrangler Pages deployment `https://53c2d93b.social-edriffles.pages.dev`; canonical `https://plumblines.uk/?deployment=53c2d93b` rendered Plumbline branding, feed posts, and no application error in the in-app browser |
| Hosted Authorization workbench check | PASS | `https://plumblines.uk/settings/services?section=authorization&deployment=53c2d93b` exposed and expanded delegated authority, requested scopes, feature upgrades, and whole-session revocation text without an application error |

This iteration makes delegated authority legible and keeps revocation claims
honest. It does not yet enforce action-level scope preflight at every write
caller, prove credentialed browser mutations, or close the external
Relay/AppView, short-TTL OAuth, and independent-PLC gates.

## 27. Iteration 20 — enforce feature-scoped OAuth at action boundaries

The Authorization workbench made OAuth delegation inspectable, but the
important mutation callers could still proceed directly to a PDS or service
client. That left a residual ambient-authority path: a user could be shown a
missing feature grant while an action still reached the transport boundary,
and optimistic UI could be updated before consent had completed.

### Authority before versus after

| Boundary | Before iteration 20 | After iteration 20 |
| --- | --- | --- |
| Posts, likes, reposts, and deletes | Mutation callers relied on the captured client and provider rejection | Posting is checked before optimistic state or the PDS call; a missing OAuth grant opens the existing feature upgrade and stops the attempt |
| Profile edits and media uploads | Profile writes/uploads could begin without a feature preflight | Profile-editing is checked before any write; media is checked before avatar, banner, or post-media work |
| Chat and Spaces | Chat optimistic messages/reactions and Spaces controls had no shared action gate | Chat mutations and Spaces control/private-record actions check their feature grant before state changes or writes |
| Compatibility | A new parallel authorization model would risk legacy sessions | Password sessions, non-OAuth sessions, native grants, and documented legacy compatibility remain allowed; new requests still use the existing granular scope ledger |

### Implementation evidence

- `upstream/social-app/src/state/session/oauth-authority.ts` is a pure
  decision/error boundary. It distinguishes OAuth feature absence from token
  expiry or revocation, which remain transport/session concerns.
- `upstream/social-app/src/state/session/oauth-feature-gate.ts` reuses
  `upgradeOAuthFeature`, requests only the missing feature, deduplicates
  simultaneous prompts per feature, and returns control without authorizing a
  pending write.
- Posting, likes, reposts, profile editing, community/Spaces controls, and
  private record actions call the gate before optimistic updates, uploads, or
  PDS/service writes. Chat sends now report whether a message was accepted, so
  a stopped consent attempt cannot trigger send metrics or scroll behavior.
- The provider-owned OAuth implementation remains responsible for PAR, PKCE,
  DPoP, refresh, state, and credential storage. This change only narrows the
  client-side delegation boundary.

### Verification

| Check | Status | Evidence |
| --- | --- | --- |
| OAuth authority contract | PASS | `src/state/session/__tests__/oauth-authority-test.ts` plus `oauth-scopes-test.ts` — 15 tests |
| Targeted Prettier | PASS | All touched TypeScript/TSX files |
| Targeted Oxlint | PASS | All touched TypeScript/TSX files |
| Web TypeScript | PASS | `pnpm run typecheck:web` |
| Diff hygiene | PASS | `git diff --check`; the existing `oxlint-suppressions.json` newline-only change remains unstaged |

This iteration removes the ambient write path for the principal social,
profile, chat, media, and Spaces actions without claiming that every settings
mutation has been converted. Remaining work includes other optional chat
administration/preferences callers, credentialed browser mutation evidence,
and the external Relay/AppView, short-TTL OAuth, and independent-PLC gates.

### Hosted release evidence

| Check | Status | Evidence |
| --- | --- | --- |
| Production-shaped export from the pushed client revision | PASS | `pnpm run build-web`; deployment input was built from nested client revision `d1f8c0d52` |
| Canonical Plumbline home | PASS | `https://plumblines.uk/?deployment=68880dc6`; read-only ChatGPT in-app-browser inspection found title `Following — Plumbline`, posts, and no application error |
| Plumbline browser asset | PASS | The published document advertises `/plumbline-mark.svg` as its favicon; the deployment preserves the Plumbline title and visual shell |
| Delegated-authority inspector | PASS | `https://plumblines.uk/settings/services?section=authorization&deployment=68880dc6`; the inspector expanded with feature authority, upgrade controls, and the whole-session revocation boundary |
| Credentialed mutation walkthrough | NOT RUN | No browser credential or social mutation was used during this release check; this is not evidence that a live account posted, liked, reposted, edited a profile, or sent chat |

## 28. Iteration 21 — make authority seams visible and addressable

The provider composition boundary already retained observations and local
reconciliation choices, but several ordinary read surfaces made that evidence
available only after an inspection click. The Services workbench likewise kept
section selection in local state even though its route already accepted a
section parameter.

The client now shows a compact Source / Rule / State summary from the existing
composition result before the detailed inspector, uses readable labels for
the four existing reconciliation modes, and updates the Services route
parameter whenever a workbench section is selected. The change is a UI and
navigation extension, not a new provider registry or authority model.

### Authority before versus after

| Boundary | Before iteration 21 | After iteration 21 |
| --- | --- | --- |
| Public read provenance | Provider participation and state were hidden until expansion on several surfaces. | Source names, local rule, and observed state are visible before expansion; observations and independence caveats remain inspectable. |
| Policy language | Internal mode identifiers could be exposed to ordinary users. | Existing modes are presented as `Require agreement`, `Use first verified result`, `Merge attributable results`, or an explicit provider preference. |
| Service inspection | A selected section could be lost on refresh or could not be copied as a stable URL. | Section selection updates the existing `ServicesSettings` route parameter and remains deep-linkable. |

### Existing ecosystem precedent

The change follows the web's addressable-resource model and the AT Protocol
client pattern of keeping service selection and provider metadata explicit.
It does not treat URL addressability, a provider label, or a declared operator
ID as proof of independent control.

### Interoperability and security tradeoffs

The summary is derived only from observations already returned by the generic
composition contract. No endpoint, token, service-auth material, or private
read is added to the UI. Updating a route parameter improves browser history
and refresh behavior while leaving account writes on the account PDS and the
existing OAuth boundary.

### Implementation evidence and remaining concentrations

- `upstream/social-app/src/components/ProviderCompositionProvenance.tsx`
  exposes the compact seam and retains the detailed source observations.
- `upstream/social-app/src/screens/Settings/ServicesSettings.tsx` makes the
  existing workbench section parameter authoritative for navigation state.
- The bundled default read provider remains a convenience default, and the
  external Relay/AppView privacy, short-TTL OAuth, and independent PLC operator
  gates remain open.

### Verification

| Check | Status | Evidence |
| --- | --- | --- |
| Provider composition tests | PASS | `src/lib/provider-composition.test.ts` — 18 tests; no selection or verification semantics changed |
| Client formatting, lint, and typecheck | PASS | Prettier and Oxlint passed for the changed files; `pnpm run typecheck:web` passed |
| Production-shaped web export | PASS | `pnpm run build-web`; existing bundle-size warnings only |
| Nested client push | PASS | `c89cf049b docs: record live authority ui verification` pushed to `fork/codex/spaces-alpha-integration`; source fix is `5dea1ea00` |
| Root push | PASS | `c78ce37 docs: bind live authority ui evidence` pushed to `origin/codex/spaces-alpha-integration` |
| Canonical public browser check | PASS | `https://plumblines.uk/profile/davidwilliampippy.bsky.social?deployment=fdd04899` rendered Plumbline branding and literal `Source:`, `Rule:`, and `State:` labels without application errors or Lingui ID artifacts |
| Services authenticated browser check | NOT RUN | The in-app browser session was logged out; no credential was supplied, so the authenticated workbench content and signed-in mutation paths remain unverified |

## 29. Iteration 22 — align authority summaries across read surfaces

The compact Source / Rule / State seam introduced for composed provider reads
was not yet shared by feed provenance, identity resolution, or profile-media
provenance. Identity evidence also retained the reconciliation policy only in
the query key and resolver call, which made the rule harder for a screen to
show beside the claims it governed.

### Authority before versus after

| Boundary | Before iteration 22 | After iteration 22 |
| --- | --- | --- |
| Feed provenance | Feed name and provider appeared in a bespoke summary with no explicit rule or state. | The existing feed algorithm/objective, provider, health, and composition state are shown through the shared Source / Rule / State summary. |
| Identity resolution | Resolver evidence was available after expansion, while the selected policy was not carried in the result. | Resolver sources and unavailable providers are visible before expansion, and the result carries the user-owned reconciliation policy into the inspector. |
| Profile media | The account-PDS delivery seam was hidden until expansion. | The ordinary profile view identifies the account PDS as record authority while retaining CID and delivery details behind the inspector. |

### Implementation evidence

- `upstream/social-app/src/components/PlumblineAuthoritySummary.tsx` is a
  presentation-only seam. It consumes source, rule, and state already produced
  by the existing provider or record boundary; it does not select a provider
  or mint access.
- `upstream/social-app/src/components/FeedProvenanceCard.tsx`,
  `upstream/social-app/src/components/IdentityResolutionProvenance.tsx`,
  `upstream/social-app/src/components/MediaDeliveryProvenance.tsx`, and
  `upstream/social-app/src/components/ProviderCompositionProvenance.tsx` use
  the same compact layout while retaining their detailed inspectors.
- `upstream/social-app/src/lib/identity-runtime.ts` and
  `upstream/social-app/src/state/queries/resolve-uri.ts` carry the existing
  `IdentityResolutionPolicy` through direct, resolved, invalid, and cached
  claim results. No resolver is promoted to a universal authority.

### Interoperability and security tradeoffs

The change is additive to the `IdentityClaimsResult` shape and preserves the
existing fail-closed disagreement behavior. Source text may include provider
IDs when no display name is available, which is intentionally attributable
rather than silently replaced with a generic network label. The profile-media
summary identifies the account PDS as the record authority but does not claim
that its CDN or AppView delivery path is independently authoritative.

### Verification

| Check | Status | Evidence |
| --- | --- | --- |
| Resolver/provider behavior | PASS | `upstream/social-app/src/lib/provider-composition.test.ts`, `attention-ui.test.ts`, and `identity-runtime.test.ts` — 3 suites, 34 tests |
| Targeted formatting and lint | PASS | Prettier and Oxlint passed for all changed TypeScript/TSX files |
| Web TypeScript | PASS | `pnpm run typecheck:web` |
| Production-shaped web export | PASS | `pnpm run build-web`; completed with existing bundle-size warnings |
| Public browser verification | PASS | Wrangler deployment `https://f01fb7c9.social-edriffles.pages.dev`; canonical `https://plumblines.uk/?deployment=f01fb7c9` rendered `Following — Plumbline` with four feed Source / Rule / State summaries and no page alerts; the profile route rendered identity and profile-provider summaries, posts, and Plumbline favicon links |

This iteration improves disclosure at an existing boundary. It does not
claim authenticated write verification, independent PLC operator control, or
closure of the external Relay/AppView and short-TTL OAuth gates.

## 30. Iteration 23 — make user-held PLC recovery authority registrable

The identity screen could prepare a non-exportable browser key, but key
generation alone did not give that key any PLC authority. The missing boundary
was an explicit, user-triggered path from a prepared key to a PDS-signed PLC
operation that includes the key in the DID document.

### Residual concentration and why it matters

The account PDS still controls the initial PLC operation and the bootstrap
email authorization. Without a registration path, the user-held key was only
local custody metadata and could not support later recovery or rotation. This
was a real concentration of authority, not a presentation problem.

### Ecosystem precedent and chosen change

The implementation follows the protocol's account-recovery and migration
model: the PDS requests an authorization code, returns recommended DID
credentials, signs an updated operation, and accepts a signed operation at the
standard identity endpoint. The client uses the smallest currently supported
scope for these APIs, `identity:*`, only when the user activates registration.
See [Account Recovery](https://atproto.com/guides/account-recovery), [Account
Migration](https://atproto.com/guides/account-migration), and [ATProto
Permissions](https://atproto.com/specs/permission).

The identity workbench now:

- exposes `identity-recovery` as a separate OAuth feature rather than treating
  the legacy generic grant as sufficient;
- requests the PDS email authorization code only after the user asks to
  register a key;
- preserves existing PDS rotation keys while adding the user-held key with
  explicit duplicate and five-key-limit validation;
- validates the returned PLC operation shape before it reaches the submit
  boundary; and
- checks verified resolver claims after submission, showing resolver
  disagreement or missing evidence instead of inferring registration.

### Authority before versus after

| Boundary | Before iteration 23 | After iteration 23 |
| --- | --- | --- |
| Browser key | A non-exportable key could be prepared, but preparation granted no network authority. | The key remains non-exportable and inert until the user explicitly authorizes registration. |
| Bootstrap registration | Only the account PDS could be used through an implicit broad session boundary. | The PDS still performs the email-authorized bootstrap, but the client asks for the separate `identity:*` grant only for this feature and makes the requested operation visible. |
| Ongoing identity evidence | Local metadata could be mistaken for recovery readiness. | Registration is reported only from verified PLC resolver claims; unavailable or disagreeing resolvers remain visible. |

This does not claim that the client has completed every migration, recovery,
lockdown, or native secure-key workflow. It also does not claim operator
independence for the configured resolvers.

### Interoperability and security tradeoffs

`identity:*` is intentionally high-impact and remains opt-in. It is not added
to the ordinary login grant, and the identity screen does not persist the
one-time email code. The PDS remains the authorization and account-state
boundary for the initial registration; the browser only holds the generated
private key and submits the standard signed operation. Resolver propagation
may lag, so the UI separates submitted state from verified directory evidence.

### Implementation evidence

- `upstream/social-app/src/state/session/oauth-scopes.ts` adds the
  feature-scoped identity grant and prevents `transition:generic` from
  satisfying it.
- `upstream/social-app/src/screens/Settings/IdentitySovereigntySettings.tsx`
  wires the opt-in request, credential merge, PDS sign/submit flow,
  account-switch token clearing, and resolver-evidence status.
- `upstream/social-app/src/lib/plc-key-custody.ts` owns key-set preservation,
  duplicate handling, and the maximum-key invariant.
- `upstream/social-app/src/lib/plc-history.ts` validates the signed operation
  before submission.

### Verification

| Check | Status | Evidence |
| --- | --- | --- |
| Focused identity/OAuth/PLC tests | PASS | 6 suites, 51 tests, including scope isolation, PLC history parsing, custody authorization, and the five-key limit |
| Targeted formatting and lint | PASS | Prettier and Oxlint passed for all changed files |
| Web TypeScript | PASS | `pnpm run typecheck:web` |
| Android TypeScript | FAIL | Existing unrelated fixture/type errors in session, provider, post, route, and `Logomark.tsx` checks; no changed identity/OAuth diagnostic |
| Full repository Oxlint | FAIL | Existing unrelated import-sort, unused-variable, and Spaces diagnostics; no changed identity/OAuth diagnostic |
| Contract validator | PASS | `python3 scripts/validate_contract.py` — 144 files, 29 blocking rows, 6 feed cases |
| Authenticated browser registration | NOT RUN | No credentialed browser session or disposable identity was available |
| Production-shaped web export | PASS | `pnpm run build-web`; compiled with existing bundle-size warnings and generated the deployed `web-build` export |
| Deployed browser UI | PASS | Wrangler deployment `https://4f0f137f.social-edriffles.pages.dev`; canonical `https://plumblines.uk/?deployment=4f0f137f` rendered `Following — Plumbline`, posts, four provenance summaries, Plumbline icon links, and no page alerts; `/settings/identity-sovereignty` rendered the current identity/PDS workbench with no alerts |

The next remaining concentrations are the PDS-controlled bootstrap email,
the unresolved external PLC operator-independence gate, and the still-open
Relay/AppView and short-TTL OAuth evidence gates.
