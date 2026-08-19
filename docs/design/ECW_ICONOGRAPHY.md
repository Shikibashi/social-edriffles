# ECW Current Iconography

## Source of truth

The current Edriffles public emblem is `edriffles-blog/src/assets/edriffles-emblem.png` (256×256 RGBA), rendered by `Header.astro` at 64px desktop and a smaller responsive size.  Current blog favicons are the 16px, 32px, ICO, and 180px assets in `public/`.  The ZIP's `assets/logo-mark.svg` is historical and is not copied into the ATProto client.

The ATProto client retains its existing network/product mark.  ECW is a shared design language, not a reason to misidentify a Bluesky/ATProto service as Edriffles.  Shared treatment comes from geometry, color roles, typography, and state visibility.

## Icon grammar

### Action scale

- Use monochrome, crisp silhouettes at 16px or 22px with `currentColor`.
- Give every icon a minimum 30px compact target (24px is the absolute accessibility floor; ECW's compact floor is higher).
- Pair icon state with text or an accessible name.  Do not encode state by hue alone.
- Use familiar action metaphors for follow, mute, block, search, settings, refresh, external provider, and navigation.
- Use the existing icon library where possible; do not add a decorative icon font or encode institutional authority in a glyph.

### Object scale

- Product marks, avatars, service marks, and provider badges may be 32/48/64px with two or three controlled layers and a small hard shadow.
- Use a product/service mark only when it identifies the actual actor: user, PDS, AppView, feed provider, resolver, labeler, or operator.
- Preserve user-supplied avatar and media identity; ECW frames it but does not recolor it into authority.

### Status and authority

Use the familiar `✓`, `!`, `×`, and `i` glyph family alongside text for success, warning, error, and information.  Provenance labels should be textual (`PDS`, `AppView`, provider name, labeler name) and may have a small neutral icon.  A generic platform logo must not be used for a provider-specific failure or judgment.

## Prohibited shortcuts

- No political, partisan, demographic, religious, or cultural imagery in default navigation or ranking controls.
- No dollar/coin or “market” icon that implies a mandatory ideological marketplace; algorithm choice is represented as a neutral service/provider selection.
- No fake browser buttons, OS title bars, CRT scanlines, or pixel-art decoration in ordinary social screens.
- No icon-only moderation decisions without an accessible label and an explicit actor/policy description.
