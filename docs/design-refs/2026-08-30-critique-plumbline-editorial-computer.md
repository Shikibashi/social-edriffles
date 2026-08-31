# Plumbline visual correction critique

## Review target

- Date: 2026-08-30
- Surface: `https://plumblines.uk/`
- Review viewport: 1198 x 1318 CSS pixels in the ChatGPT in-app browser
- Direction: locked Plumbline / ECW `Seamful Hypertext Workbench`
- Effect budget: zero decorative effects; structure and hierarchy must carry the identity

## What the rendered surface actually communicates

The deployed surface has the Plumbline palette, rules, provenance copy, and a shared
mark, but the composition still communicates an upstream Bluesky-style application:

1. The primary desktop review width collapses the Navigator to an icon-only rail while
   leaving the Inspector visible. That makes the client identity and route vocabulary
   secondary at exactly the width where the three-pane workbench should be legible.
2. The home header still renders the upstream logo component. This is a direct brand
   mismatch even though the surrounding shell has Plumbline tokens.
3. The main feed remains the visually dominant surface, but the header does not name it
   as a document stream or give it a clear current-workspace hierarchy.
4. The right column contains a useful Inspector, but the following feed list and
   trending block visually read as a generic recommendation rail rather than optional
   tools beneath a selected-object explanation.
5. The signed-in account identity in the full Navigator is not a stable, always-visible
   account context; the existing hover-first presentation is optimized for the old
   compact shell rather than an inspectable workbench.

## Bounded correction

Change the shared shell boundary rather than layering more decoration onto the old
composition:

- retain a labeled Navigator until the viewport can no longer fit the three-pane
  workbench;
- use a less aggressive mid-width center shift so the labeled Navigator, 600px stream,
  and Inspector occupy distinct columns;
- replace the upstream home logo with the Plumbline mark and an explicit document-stream
  heading;
- keep account identity visible in the labeled Navigator;
- give the Inspector and its secondary tools separate structural sections and surfaces.

## Acceptance evidence

The correction is complete only after browser renders show:

- 1198px: labeled Navigator, Plumbline home header, continuous document stream, and
  Inspector without horizontal overflow;
- 1440px: the same hierarchy with the full desktop spacing;
- 390px: mobile navigation and primary actions remain usable, with no desktop-only rail
  leaking into the mobile surface;
- no upstream logo component or upstream brand wordmark is rendered by the shell;
- existing route actions and content semantics remain intact.
