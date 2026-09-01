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
| Production export after entrypoint change | NOT ACCEPTED | An agent-started export compiled actively but its terminal completion was not captured; it is not counted as a passing production-build result. |

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

### Fresh verification

| Check | Status | Evidence |
|---|---|---|
| Focused Oxlint | PASS | `pnpm exec oxlint --quiet` on the changed shell, header, layout, and breakpoint files exited `0`. |
| Web TypeScript | PASS | `pnpm typecheck:web` exited `0`. |
| Web export | PASS | `pnpm build-web` completed with the generated `main.272ed937.js` and CSS output; Webpack reported only existing asset-size warnings. |
| Local rendered desktop layout | PASS | Fresh in-app-browser render at `http://127.0.0.1:4176/`, viewport `1198×1318`: masthead `1183×132`, grid `190px 640px 220px`, central stream `640px`, no horizontal overflow, and main wrapper `1186px` high. |
| Rendered visual direction | PASS | Screenshot visibly shows the full masthead, `Index`, editorial `Following` heading, continuous post rules/provenance line, and marginal notes; it is not reasonably describable as Bluesky with an ECW/retro stylesheet. |
| Grayscale resilience | PASS | Computed token contrast after luminance conversion: text/workspace `13.41:1`, text/surface `14.82:1`, secondary/workspace `8.58:1`, muted/surface `5.36:1`. |
| Root contract | PASS | `python3 scripts/validate_contract.py` validated `144` files, `29` blocking rows, and `6` feed cases. |
| Deep local route smoke | BLOCKED | The connected in-app browser rejected the first nested local route with `ERR_BLOCKED_BY_CLIENT`; no route failure was relabeled as a UI pass. |

The visual acceptance claim is limited to the fresh local Page Mode render above.
Hosted deployment and credentialed provider behavior remain separate gates and
were not changed or inferred by this visual pass.
