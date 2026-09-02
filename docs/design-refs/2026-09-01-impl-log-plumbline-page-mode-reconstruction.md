# Implementation Log: Plumbline Page Mode and local OAuth bootstrap

## Scope

This batch continues the approved Plumbline Page Mode reconstruction and repairs
the local browser OAuth bootstrap without changing hosted OAuth metadata,
production credentials, provider authority, or social-feature behavior.

## Local OAuth repair

### Problem

AT Protocol's browser loopback exception uses an IP-loopback callback. A local
developer could begin at a `localhost` page, creating browser OAuth state in
the `localhost` IndexedDB namespace, and later receive the callback at
`127.0.0.1`. Those are distinct browser origins, so the callback could not
find the pending transaction.

### Change

- `index.web.ts` now evaluates a development-only `localhost` to `127.0.0.1`
  route normalization before it evaluates `App` or mounts the session provider.
  Query parameters, path, and hash are retained.
- The ordinary app module is not evaluated while that replacement navigation is
  pending, preventing an OAuth client from writing state under the wrong
  origin.
- `getDevelopmentLoopbackOAuthConfig()` builds a local-only client ID under the
  AT Protocol loopback exception: client ID hostname `localhost`, declared
  bootstrap and callback redirects on `127.0.0.1`.
- `pnpm web:local` starts the repeatable local server at port `19006` without
  attempting to launch a desktop browser.
- `docs/build.md` documents the supported local URL and why a generic static
  server cannot serve an OAuth callback route.

## Evidence

| Check | Status | Evidence |
|---|---|---|
| Local OAuth unit/session tests | PASS | `20` tests in `2` suites passed: `oauth-scopes-test.ts` and `oauth-session-test.ts`. |
| Web typecheck | PASS | `pnpm typecheck:web` exited `0`. |
| Focused lint | PASS | `pnpm exec oxlint --quiet` on bootstrap, OAuth, breakpoint, and test files exited `0`. |
| Focused formatting | PASS | Prettier reported all matched files formatted. |
| Local dev compilation | PASS | `pnpm web:local` compiled successfully. |
| Local route handling | PASS | `127.0.0.1:19006` returned `200` for `/`, `/oauth/callback`, a profile/post route, and `/community`. |
| Root contract | PASS | `python3 scripts/validate_contract.py` validated `144` files, `29` blocking rows, and `6` feed cases. |
| Credentialed local authorization | NOT RUN | No user or production credential was entered. The ChatGPT in-app browser connector blocks loopback navigation in this environment, so a real provider consent/callback cannot be claimed here. |
| Production export after entrypoint change | PASS | A tracked `EXPO_PUBLIC_ENV=production pnpm build-web` exited `0`; it regenerated the web bundle and copied Plumbline OAuth metadata, marks, and icons into both delivery outputs. Webpack reported only bundle-size warnings. |

## Safe local walkthrough

```sh
cd /var/home/tcs/Code/atproto/upstream/social-app
pnpm web:local
```

Open `http://127.0.0.1:19006/`. If a local profile, post, or community address
is opened using `localhost`, the bootstrap changes it to the equivalent
`127.0.0.1` address before the sign-in screen can initiate OAuth.

## Page Mode verification boundary

The ongoing Page Mode reconstruction remains separately documented by the
brief, critique, experience contract, layout, and sitemap in this directory.
Wide-desktop and mobile local renders were inspected earlier in the workstream.
The follow-up compact desktop breakpoint correction has static source and
typecheck evidence, but a fresh loopback in-app-browser screenshot is blocked
by the connector's local-URL policy. It must not be presented as visually
accepted until it is rendered in an allowed browser environment.

## Structural Page Mode implementation

This pass replaces the former fixed-rail, centered application shell with the
Page Mode composition required by `docs/design/PLUMBLINE_DESIGN.md`:

```text
full-width masthead
        ↓
Index / Navigator | Editorial document stream | Marginal inspector
```

### Decision record

| Item | Finding and decision |
|---|---|
| Residual concentration | Page Mode previously routed the visual hierarchy through a narrow centered feed and two fixed rails, making the product identity and provider context subordinate to generic application chrome. |
| Why it matters | The layout obscured the user's reading surface and made the client look like a social-network shell with a stylesheet rather than an inspectable user agent. |
| Ecosystem/design precedent | The accepted Plumbline design extends ECW with publication hierarchy, progressive seamfulness, provenance, and marginal inspection while preserving the existing ATProto feed/action components. |
| Architectural change | `createNativeStackNavigatorWithAuth` now places `PlumblinePageMasthead` in document flow and wraps the existing routed main view, desktop index, and inspector in one responsive CSS grid. |
| Authority before / after | Before: fixed navigation and a centered content column visually implied the shell owned the session. After: the masthead identifies the client, the index names navigation, the stream owns the page, and the inspector attributes source/rule/control without changing provider behavior. |
| Tradeoffs | Page Mode has a larger masthead and uses deliberate desktop width; Workbench routes retain their existing behavior and stronger configuration treatment. Existing feed controls, media, actions, and accessibility semantics remain in their source components. |

### Implementation evidence

- `PlumblinePageMasthead` is full width, carries the `PLUMBLINE` wordmark,
  descriptor, motto, rules, and a structural brass plumb marker.
- Page Mode uses a responsive `Index / stream / marginal` grid with the
  central stream as the dominant track. The old centered border is hidden on
  desktop so it cannot create a second, misaligned frame.
- Feed rows are flat document entries with printer-like separators, a
  continuous vertical provenance rail, square integrated media, and the
  existing compact action line.
- `Following` is presented as an `EDITION` with `CHRONOLOGICAL` metadata;
  the inspector uses serif titles, definition-style source/rule/control notes,
  and rules instead of dashboard cards.
- The actual wrapper uses `#plumbline-main-content` and is constrained to at
  least the viewport height below the masthead; this prevents the grid item
  from collapsing while the native stack's routed content remains positioned.

### Auth-gated entry treatment

Signed-out deep links are part of the same publication rather than a separate
marketing or provider-owned splash screen. `SplashScreen.web.tsx` therefore
uses the existing Page Mode masthead and an editorial entry document. Before
the unchanged create-account and sign-in controls, it states that the account
host remains the write and identity authority. On narrow screens the masthead
is intentionally replaced by the compact document identity rather than being
stacked above the controls. This is a visual and explanatory boundary only:
it does not add a provider, alter OAuth scopes, or change either entry flow.

### Direct post provenance

A thread route can identify a stable AT record even when its originating feed
and placement evidence are unavailable. The anchor therefore exposes a
`Post provenance` disclosure in that case, with the copyable AT URI and an
explicit statement that no public placement reason is available. `Why this
post?` remains reserved for actual local or provider-supplied placement
evidence; the interface does not promote generic read provenance into a
ranking explanation.

### Community reference color

The Community Board remains a Page Mode association surface, but its
non-semantic accent now uses ALF's theme-aware yellow role as the readable
Plumbline brass/reference companion. The exact brass mark remains structural;
the theme role is used for editorial metadata, conflict state, and references
because it maintains at least `4.5:1` contrast on the light, dark, and dim
editorial surfaces. This replaces the prior generic pink accent without
changing community authority, membership, or private-data behavior.

### Services capability table semantics

The Services capability map is substantively tabular: each row names a
capability, its source, state, and inspection action. Its prior generic
`summary` role hid that relationship from assistive technology and omitted
headers when the visual layout compacted. It now keeps the existing visual
matrix but declares table, row, column-header, and cell relationships; compact
layouts retain the same headers as visually hidden text. This is an
accessibility and information-architecture correction only: provider choice,
reconciliation, authorization, and PDS boundaries remain unchanged.

### Association authority summaries

Protected access and private-space controls are Workbench surfaces, so they
now use the same source/rule/state summary already used by Identity,
Moderation, and Services. Protected access identifies the protected account's
PDS as the source of a directional personal request and explicitly separates
that relationship from public follows and AppView policy. Private spaces
identify the selected PDS transport for authorized reads while keeping a
community's declared membership authority separate from AppView or
network-wide policy. The displayed state comes from the existing request or
protected-account query; the summaries add no authority, scope, membership,
or transport behavior.

### Quality-gate repair boundary

The current upstream checkout had accumulated strict-type and lint drift in
legacy password-session tests, generated lexicon fixtures, and import ordering.
The repair keeps OAuth persistence broad enough for OAuth-backed accounts while
using a strict password-session conversion only in the shared test-fixture
layer. It also updates the old share-URL expectation to the existing
Plumbline-origin resolver contract and applies mechanical import sorting. No
production provider, PDS, identity, ranking, moderation, association, or OAuth
consent behavior changes as part of that gate repair.

### Fresh verification

| Check | Status | Evidence |
|---|---|---|
| Focused Oxlint | PASS | `pnpm exec oxlint --quiet` on the changed shell, header, layout, and breakpoint files exited `0`. |
| Web TypeScript | PASS | `pnpm typecheck:web` exited `0`. |
| Web export | PASS | Tracked `EXPO_PUBLIC_ENV=production pnpm build-web` completed with generated `main.8ab357ea.js` and CSS output; Webpack reported only bundle-size warnings. |
| Local rendered desktop layout | PASS | Fresh in-app-browser render at `http://127.0.0.1:4176/`, viewport `1198×1318`: masthead `1183×132`, grid `190px 640px 220px`, central stream `640px`, no horizontal overflow, and main wrapper `1186px` high. |
| Rendered visual direction | PASS | Screenshot visibly shows the full masthead, `Index`, editorial `Following` heading, continuous post rules/provenance line, and marginal notes; it is not reasonably describable as Bluesky with an ECW/retro stylesheet. |
| Grayscale resilience | PASS | Computed token contrast after luminance conversion: text/workspace `13.41:1`, text/surface `14.82:1`, secondary/workspace `8.58:1`, muted/surface `5.36:1`. |
| Root contract | PASS | `python3 scripts/validate_contract.py` validated `144` files, `29` blocking rows, and `6` feed cases. |
| Deep local route smoke | BLOCKED | The connected in-app browser rejected the first nested local route with `ERR_BLOCKED_BY_CLIENT`; no route failure was relabeled as a UI pass. |

The visual acceptance claim is limited to the fresh local Page Mode render above.
Hosted deployment and credentialed provider behavior remain separate gates and
were not changed or inferred by this visual pass.

### Acceptance evidence map

This map makes the implementation reviewable against section 35 of
`PLUMBLINE_DESIGN.md`. It records implementation and local evidence only; it
does not replace the pending owner acceptance checklist or authenticate a real
account.

| Design criterion | Implementation and evidence | Review boundary |
|---|---|---|
| Home / feed | Page Mode supplies the active feed, ordering, source/rule/control inspector, Navigator, and continuous document stream. Public desktop and narrow renders were inspected. | Feed mutation and signed-in provider selection were not exercised. |
| Post | `Why this post?` remains tied to actual placement evidence; direct record reads expose `Post provenance`, an AT URI, and the absence of a public placement reason. Focused attention tests pass. | Provider-supplied recommendation evidence was not authenticated live. |
| Services | Workbench distinguishes PDS, AppView, feed provider, labeler, and configuration state in an accessible capability table. Provider-composition and service-boundary tests pass. | Changing a live provider requires an authenticated owner review. |
| Moderation | Existing source/assertion/rule/action boundaries remain intact; moderation and list-block regression tests pass. | Account-specific moderation mutations were not executed. |
| Identity | Existing handle, DID, host, recovery, migration, and export mechanisms remain reachable through Workbench surfaces; identity sovereignty tests pass. | Export/migration with a real account is not verified. |
| Association | Protected access and private spaces now state their distinct PDS, community, and provider authority boundaries; permissioned-data and Spaces tests pass. | Protected request and membership mutations are not verified. |
| Branding | Build output has `Plumbline`, `plumblines.uk`, canonical OAuth metadata, and the full icon/mark set while reference Bluesky/provider names remain infrastructure-specific. | Hosted deployment DNS and production edge behavior are not verified. |
| Visual identity and accessibility | Editorial tokens, Georgia/Verdana/Courier roles, Page Mode, responsive Navigator/stream/Inspector composition, focus, forced-colors, and reduced-motion rules have source/test evidence; public desktop and narrow screens were rendered. | Owner visual, keyboard, forced-colors, and signed-in Workbench acceptance remain pending. |

### Continuation verification

| Check | Status | Evidence |
|---|---|---|
| Focused Plumbline regression suite | PASS | `pnpm test --runInBand` passed `8` suites / `38` tests covering permissioned-data transport, Spaces, provider composition, OAuth scopes, identity, and moderation. The direct-post provenance and ECW contrast tests also passed in their focused runs. |
| Changed-file lint | PASS | `pnpm exec oxlint --quiet` on the Page Mode, Workbench, provenance, and test files exited `0`. |
| Web TypeScript | PASS | `pnpm typecheck:web` exited `0` after the Workbench association summary changes. |
| Production web export | PASS | A tracked `EXPO_PUBLIC_ENV=production pnpm build-web` exited `0`; it copied Plumbline metadata and icon assets into both web outputs. Webpack emitted only the existing asset-size warnings. |
| Public rendered desktop and narrow routes | PASS | Credential-free local renders showed the editorial Home frame, direct-post `Post provenance` control, narrow stream-first Home, and the narrow signed-out account-entry document. |
| Root contract | PASS | `python3 scripts/validate_contract.py` validated `144` files, `29` blocking rows, and `6` feed cases. |
| Broad typecheck, lint, and full Jest | PASS | `pnpm typecheck` passed iOS, Android, and web; `pnpm lint` passed without new suppressions; `pnpm test --runInBand` passed `116` suites / `1,060` tests (`28` todos, `21` snapshots). The repair was limited to strict test-fixture conversion, stale test expectations, and mechanical lint cleanup; it did not alter production authority or attention behavior. |
| Authenticated Workbench actions and real provider consent | NOT VERIFIED | No account or credential was used. Protected-access mutations, private-space membership, export/migration actions, and OAuth consent remain intentionally unexercised in this local review. |
