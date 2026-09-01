# Plumbline shared-component audit

## Scope

This audit covers the built public web artifact in the in-app browser at
`390 × 844` and `1440 × 900`. It checks the shared Page Mode shell,
document-stream controls, progressive disclosure, deep links, and the public
thread surface. It does not authenticate, request OAuth authority, inspect a
session, or perform a social write.

## Corrections

| Boundary | Correction | Reason |
| --- | --- | --- |
| Feed, post, identity, media, and provider provenance | Use a 30px minimum action area for progressive toggles and their deferred actions. | Details become available only when the reader asks; the control must remain an ordinary accessible action without enlarging the default document stream. |
| Signed-out welcome dialog | Replace the bespoke inline sign-in pressable with the standard small button. | The previous text-only action rendered below the design system's minimum control height. |
| Grouped chat system updates | Give the disclosure row a 30px visible minimum in addition to native hit-slop. | Native hit-slop does not make the web control visibly or reliably large enough. |
| Static web shell | Remove the stale `/static/style.css` request from `web/index.html`. | `src/style.css` is already included in Expo's hashed CSS bundle; no separate file is emitted. |
| Public and deferred typeaheads | Attach `aria-controls` only while the matching Sift listbox is mounted. | A collapsed combobox must not reference a popup that does not exist yet. This applies to full search, desktop search, advanced search, signup handle suggestions, and composer autocomplete. |
| Shared web select and menu triggers | Attach Radix `aria-controls` only while the portalled content is open. | Radix unmounts the controlled content while closed, so the relationship must follow the real mounted state rather than an anticipated state. |

## Verification

- The public route matrix passed on both target viewports for `/`, search,
  feeds, lists, saved, profile, thread, quotes, community, moderation,
  Services, identity/recovery, messages, and notifications.
- Every checked route had one `main`/`role="main"` landmark and one `h1`, with
  no horizontal page overflow, alert state, stale stylesheet link, or visible
  button below 30px.
- The feed details control measured 30px before and after expansion. Its
  expanded `aria-controls` reference resolved to a labelled region.
- Search typeaheads and the desktop shell search now have no `aria-controls`
  reference while collapsed and a live, matching listbox reference while open.
  The source-only advanced-search, signup-handle, composer, shared select, and
  shared menu variants received the same mounted-state contract and passed
  format, lint, type, and build verification. This follows the [W3C combobox guidance](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/), which requires the popup relationship only while the popup is visible.
- The public mobile thread rendered four reply actions; replies remained
  visible in the initial document stream.
- Public profile and thread media rendered without broken image elements, and
  the built document exposes Plumbline favicon, browser-icon, and pinned-tab
  icon links.
- The final rebuilt artifact passed all 28 route/viewport checks: 14 public
  routes at `390 × 844` and the same 14 routes at `1440 × 900`. Each check
  required one main landmark, no horizontal overflow, no visible error copy,
  no alert state, no dangling `aria-controls`, and no visible button below
  30px.
- The final in-app-browser diagnostic log was empty.
- The production web export completed. Webpack retained its existing large
  entrypoint warning (about 7.92 MiB combined), which is a performance
  follow-up rather than a failed artifact check.
- The chat disclosure change is source-, format-, lint-, type-, and
  production-build-verified. It is not live-verified because the audit did
  not sign in.

## Boundary

The public route checks establish layout, navigation, and read-surface
behavior only. OAuth authorization, authenticated chat, Spaces, profile
editing, and write actions require a separately authorized credentialed test
session and remain outside this audit.

The production Jest suite was not green: it stopped on an existing URL-helper
expectation that expects `https://bsky.app` but receives
`https://bsky.app/`. The affected test/helper paths were not modified by this
audit, so this result is recorded separately rather than being hidden or
treated as a UI pass.

## Login rendering and OAuth preflight

The mobile sign-in report exposed two shared dark-theme contrast failures,
rather than evidence of a malformed OAuth client request:

- A focused shared `TextField` used a pale primary fill under light input text:
  `1.04:1` in dark and `1.03:1` in dim. The source now uses `primary_950` for
  dark and dim focused fields, raising those pairs to `8.67:1` and `8.72:1`.
- The same failure existed after an invalid identifier: the pale
  `negative_25` error fill could conceal the entered value in dark and dim
  themes. Error and error-hover fields now use `negative_950` outside light
  mode, and the shared ECW contrast test covers that state.
- A solid primary Button used light text over a pale primary fill: `1.65:1` in
  dark and `1.81:1` in dim. Active primary, negative, and subtle Button
  variants now select an accessible foreground/background pair for each theme.
  The checked active states, including hover states, are all at least `4.5:1`.

The anonymous local production bundle was also checked in the in-app browser:
the ordinary Sign in control reached `Sign in — Plumbline`, exposed an enabled
username/DID field, and exposed an enabled Continue with OAuth action. No
identifier, OAuth authorization request, PAR request, callback, session, or
social write was performed. The source fix passed the focused Jest contrast
test, format check, lint, web typecheck, diff check, and production build.

Cloudflare Pages production deployment `6f742034` now serves the rebuilt
`main.aea4d8a1.js` artifact on both its immutable deployment host and the
canonical `https://plumblines.uk` route. A read-only in-app-browser check
hydrated the canonical feed with one main landmark, one H1, no alert state, and
no horizontal overflow. A public post thread also loaded without an error state
and exposed six Reply controls plus the deferred `Show more replies` action.
The check used an already-existing browser session but did not enter an
identifier, request OAuth authority, authorize a client, or perform a social
write.

Public, read-only OAuth preflight remains healthy: Plumbline's client metadata,
PDS OAuth-server metadata, server description, and handle-resolution endpoints
return the expected public protocol data. No credential, authorization request,
PAR request, callback, session, or social write was performed in this audit;
end-to-end credentialed sign-in therefore remains not run.
