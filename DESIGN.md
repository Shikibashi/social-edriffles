---
version: 1
source: ECW token contract and Communities forum brief
updated: 2026-08-26
direction: editorial-forum-workbench
tokens:
  color:
    canvas: {oklch: 'oklch(0.87 0.03 270)', fallback: '#d6d9e8'}
    workspace: {oklch: 'oklch(0.82 0.04 270)', fallback: '#c7ccdf'}
    surface: {oklch: 'oklch(0.96 0.01 100)', fallback: '#f4f3eb'}
    surface-recessed: {oklch: 'oklch(0.90 0.03 270)', fallback: '#e1e3ee'}
    surface-raised: {oklch: 'oklch(1 0 0)', fallback: '#ffffff'}
    ink: {oklch: 'oklch(0.20 0.04 285)', fallback: '#11132d'}
    ink-secondary: {oklch: 'oklch(0.31 0.05 285)', fallback: '#24274a'}
    ink-muted: {oklch: 'oklch(0.47 0.05 285)', fallback: '#4d5372'}
    border: {oklch: 'oklch(0.54 0.08 285)', fallback: '#626a9c'}
    border-strong: {oklch: 'oklch(0.39 0.13 285)', fallback: '#383f78'}
    action: {oklch: 'oklch(0.39 0.16 285)', fallback: '#004fa3'}
    accent: {oklch: 'oklch(0.36 0.20 305)', fallback: '#5530a3'}
    marker: {oklch: 'oklch(0.49 0.19 345)', fallback: '#a82378'}
  typography:
    display: "Georgia, 'Noto Serif', 'DejaVu Serif', 'Times New Roman', serif"
    ui: "Verdana, 'DejaVu Sans', Tahoma, 'Noto Sans', Arial, sans-serif"
    system: "'Courier New', 'Liberation Mono', 'DejaVu Sans Mono', monospace"
    body-size: '0.9375rem'
    ui-size: '0.875rem'
    meta-size: '0.8125rem'
    micro-size: '0.75rem'
  geometry:
    control-min: '30px'
    row-min: '48px'
    layout-gap: '16px'
    control-radius: '1px'
---

# Communities design source

Communities is an editorial forum workbench inside the existing Bluesky shell. It
should feel like entering a named place with its own membership, topics, and
moderation rules. The screen is intentionally denser than a public feed, but it
does not become an administration console.

## Direction

- Use classic forum information architecture: community header, local tabs,
  topic rows, and a topic detail view.
- Preserve the existing ECW visual language: paper-like light surfaces, a
  quiet grid workspace, serif display type, system metadata type, square
  controls, structural borders, and a two-tone focus treatment.
- Keep one dominant neutral surface system with the existing blue/purple action
  accents. Do not use a new gradient, decorative hero, sticky-note rotation, or
  background effect.
- Use the ALF theme palette at runtime so light, dark, dim, forced-colors, and
  high-contrast modes retain readable surfaces and text.

## Interaction principles

- The community is the context. The primary composer action always names the
  selected community and writes through the existing private Space transport.
- Authorization is explained in ordinary language: Public, Members, Invite
  required, Joined, or Owner. Protocol identifiers remain secondary details.
- Every topic row is a real button with a keyboard path and a visible selected
  state. Links remain addressable and underlined according to ECW rules.
- Counts are only shown when computed from records available to the client. The
  client must not invent member totals, reply totals, handles, or timestamps.
- Loading, partial-read, empty, authorization, and retry states explain what is
  known and what action is available.

## Responsive rule

Desktop keeps the forum hierarchy in the Bluesky center column. Mobile keeps the
community context, tab strip, topic title, and primary action in that order;
secondary metadata and technical identifiers move below the content or into the
About tab. No desktop-only multi-pane interaction is required for the first
implementation.

## Motion and effects

The effect budget is zero decorative effects and one lightweight state
transition budget. Use existing button hover/focus treatment and short
opacity/transform transitions only where the platform already supplies them.
Respect `prefers-reduced-motion`; the feature remains fully usable with motion
removed.
