# ECW Current Token Contract

These are the reconciled semantic roles for the ATProto client.  Values are intentionally traceable to the living products; component code should consume roles, not hard-code palette literals.

## Color roles

| Role | Dark | Light | Use |
| --- | --- | --- | --- |
| `canvas` | `#050719` | `#d6d9e8` | outer page/background grid |
| `workspace` | `#070a2e` | `#c7ccdf` | app workspace behind main surfaces |
| `surface` | `#12144b` | `#f4f3eb` | structural panels and content surfaces |
| `surface-recessed` | `#0b0d38` | `#e1e3ee` | context strips, secondary regions, inset areas |
| `surface-raised` | `#1c1e67` | `#ffffff` | selected/raised cards and dialogs |
| `surface-input` | `#02030d` | `#d4d6df` | fields and code-like input areas |
| `text` | `#f9f3ff` | `#11132d` | ordinary readable text |
| `text-secondary` | `#dfe6ff` | `#24274a` | supporting content |
| `text-muted` | `#aeb6e9` | `#4d5372` | metadata only; never the only state signal |
| `border-structural` | `#6675c8` | `#626a9c` | load-bearing boundaries |
| `border-strong` | `#7787e8` | `#383f78` | active/strong boundaries |
| `rule-decorative` | `#343960` | `#9da2bd` | dotted rules and non-semantic decoration |
| `link` | `#6ff4ff` | `#004fa3` | ordinary links |
| `link-visited` | `#c594ff` | `#65349a` | visited links where the platform exposes them |
| `accent` | `#b189ff` | `#5530a3` | identity/selected text accent where contrast allows |
| `selection` | `#7787e8` | `#2c2a86` | selected control fill; separate from focus |
| `selection-text` | `#050719` | `#ffffff` | text on selection fill |
| `focus-outer` | `#ffd45c` | `#522598` | outer focus ring |
| `focus-inner` | `#050719` | `#ffffff` | inner focus ring |
| `marker` | `#ff76d7` | `#a82378` | attention marker/hover accent, never color-only state |

Status roles are quartets: `status-{success,warning,error,info}-{text,accent,border,on-accent}`.  Text and borders are contrast-oriented; accent is a fill; on-accent is its foreground.  Do not substitute a single hue for the quartet.

Dim is a distinct low-contrast dark theme, not an alias for Dark.  Its
headline surface roles are `canvas #0b0d20`, `workspace #0e123a`, `surface
#171a4d`, `surface-recessed #131640`, `text #f1efff`, `text-secondary
#d2d8f4`, `text-muted #9da7d0`, `border-structural #5968ad`, and link
`#65dbe5`.  It retains the same role grammar and accessibility requirements
as Dark while making the user's theme choice observable.

## Typography

```css
--ecw-font-display: Georgia, "Noto Serif", "DejaVu Serif", "Times New Roman", "Liberation Serif", serif;
--ecw-font-ui: Verdana, "DejaVu Sans", Tahoma, "Noto Sans", Arial, "Liberation Sans", sans-serif;
--ecw-font-system: "Courier New", "Liberation Mono", "DejaVu Sans Mono", "Noto Sans Mono", monospace;
--ecw-font-size-body: 0.9375rem;
--ecw-font-size-ui: 0.875rem;
--ecw-font-size-meta: 0.8125rem;
--ecw-font-size-micro: 0.75rem;
--ecw-line-height-body: 1.5;
--ecw-line-height-ui: 1.4;
--ecw-line-height-meta: 1.35;
```

The client may use platform-native font stacks for native surfaces, but the web surface must preserve these three voices.  Per-language fallbacks are required for Japanese, Korean, Arabic, Hebrew, and other scripts without Verdana coverage.

## Geometry and preference axes

```css
--ecw-control-block: 1.875rem;       /* compact */
--ecw-field-block: 2rem;             /* compact */
--ecw-row-block: 1.875rem;           /* compact */
--ecw-toolbar-block: 2.25rem;        /* compact */
--ecw-control-padding-inline: 0.5rem;
--ecw-gap-control: 0.25rem;
--ecw-hit-min: 1.875rem;              /* 30 CSS px compact floor */
--ecw-space-panel: 0.75rem;
--ecw-space-layout: 1rem;
```

Comfortable mode uses the living Idoldle values: 2.75rem controls/fields, 2.5rem rows, 3rem toolbars, 0.75rem inline padding, 0.5rem control gaps, and 2.75rem hit targets.  Automatic may resolve from pointer capability, but an explicit user selection always wins.  Theme, density, contrast, motion, transparency, and language remain independent axes.

## Interaction rules

- Links are underlined and addressable; buttons are real buttons.
- Every focusable control receives a two-tone ring: inner outline plus outer ring.
- Decorative rules cannot be the only grouping/state indicator.
- Raised/recessed controls retain a real control border so their identity survives forced-colors mode.
- Icon-only controls have an accessible name, tooltip, and target floor.
- Dragging, where present, has a single-pointer or keyboard alternative.
- Persistent status strips are not live regions by default.  Dynamic announcements use the existing announcement mechanism only when a user needs them.
- User-facing error states identify the actual object/service, the problem, and the next available action.
