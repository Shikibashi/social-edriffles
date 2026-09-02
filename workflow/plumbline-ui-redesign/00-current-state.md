# Plumbline UI redesign: current state

## Capture

- Date: 2026-09-02
- Repository: `/var/home/tcs/Code/atproto`
- Root revision: `184f61b` (`chore(plumbline): point to flat thread view`), branch `master`
- Client revision: `3e4201479` (`fix(web): flatten post thread decoration`), branch `main`
- Live target inspected: [plumblines.uk](https://plumblines.uk/?olympus-audit=phase1)
- Local capture: `screenshots/current-live-desktop.png`; `screenshots/current-live-mobile.png`
- Capture method: Codex in-app browser DOM snapshot, runtime measurement, and screenshot. No cookies or local-storage contents were inspected.

The nested client and root repository were already dirty before this redesign pass. The root has unrelated changes in `.gitignore`, conversation/memory files, and the new workflow directory. The client has a pre-existing `oxlint-suppressions.json` change and an owned, uncommitted masthead-wording change in `src/lib/brand.test.ts`, `src/lib/brand.ts`, `src/screens/Settings/AboutSettings.tsx`, and `src/view/shell/PlumblineShellBrand.tsx`. These changes are not part of the redesign baseline and must not be staged incidentally.

## What is actually running

The live page is a real web render, not a static mock. At the time of capture it exposed:

- a full-width banner with `Plumbline`, `Social client for the open web`, and `Liberty the Mother of Order`;
- a left `Index` rail with account, sections, reading, services, account controls, and `New post`;
- a center route with `CURRENT EDITION / SECTION`, the active feed title, mode metadata, feed tabs, feed provenance, composer, and posts;
- a right complementary `Workbench inspector` headed `Marginal note`, with source/rule/control text, optional tools, search, and `More context`;
- real feed results and real post actions, rather than placeholder content.

The source hierarchy confirms that this is still the shared social-app shell with Plumbline/ECW overlays:

```text
createNativeStackNavigatorWithAuth
  ├─ PlumblinePageMasthead
  ├─ NativeStackView / route screen
  ├─ DesktopLeftNav or mobile BottomBarWeb
  └─ DesktopRightNav

HomeScreen
  └─ HomeHeaderLayoutDesktopAndTablet
       ├─ section heading
       ├─ feed tab bar
       └─ feed/post surfaces
```

The shared `Screen`/`Layout` system owns the Page Mode versus Workbench distinction. The feed item, post controls, embeds, and provenance components remain independently owned by their existing modules. This is useful: the redesign can change composition at the shell and Page Mode boundaries without replacing ATProto behavior.

## Measured baseline

The browser connector's viewport override did not change the actual page viewport. The runtime reported approximately `innerWidth=1198`, `innerHeight=1318`, `bodyWidth=1183`, and a central main rectangle of `left=196`, `width=771`. Therefore the requested 1440x900, 1280x720, 1024x768, and 390x844 target captures are not yet verified. This is a tool limitation, not evidence that responsive behavior passes.

The current page's declared layout intent is approximately `224px / 760px / 256px` in Page Mode, with responsive variants. The central reading measure is close to the intended 760px, but the total composition is still constrained by persistent application rails and stacked controls.

## Visual diagnosis

The current direction has improved several isolated details, but it still reads as a social application shell decorated with editorial tokens:

1. The masthead is present, but it does not yet establish the whole page as a publication. The rail account card and app navigation still carry much of the product identity.
2. `Index`, `CURRENT EDITION / SECTION`, `EDITIONS`, provenance summary, and the right `Workbench inspector` are all visible at once. The page explains its implementation layers before the reader has oriented to the publication content.
3. The center is a 760px route surface inside a three-region app frame. Tabs, status rows, and controls create a toolbar sequence above the document stream.
4. The inspector is less boxed than the historical version, but its persistent dashboard-like labels and utility blocks still compete with the stream.
5. Feed entries are flatter than the old card treatment, yet nested quote/link previews, action rows, and provenance markers still create repeated component boundaries.
6. The plumb-line geometry is visible, but multiple markers and rules currently read as an overlay system rather than as one continuous editorial/provenance spine.
7. The narrow capture did not demonstrate an intentional mobile composition because the connector remained at a desktop-like viewport. Mobile transformation is consequently an open validation item.

## Failed hypothesis to retire

The failed hypothesis was: “Keep the existing Bluesky-like application composition and make it Plumbline through masthead, serif type, square borders, and provenance markers.” The next implementation must begin from a publication/document composition and then attach social controls and service seams to it. A successful build must be rejected if an observer can reasonably summarize it as “Bluesky with an ECW/retro stylesheet.”

## Evidence boundary

This file records an engineering and visual baseline. It does not claim that a screenshot proves usability, accessibility, protocol correctness, or production readiness. Those claims require the validation work described in the later artifacts.
