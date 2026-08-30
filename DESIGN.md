---
version: 2
source: Plumbline product-design specification and ECW token contract
updated: 2026-08-30
direction: seamful-hypertext-workbench
brand:
  name: Plumbline
  descriptor: AT Protocol client
  origin: https://plumblines.uk
  emblem: upstream/social-app/assets/plumbline/plumbline-mark.svg
tokens:
  color:
    canvas: {oklch: 'oklch(0.87 0.01 250)', fallback: '#d5d8de'}
    workspace: {oklch: 'oklch(0.92 0.01 95)', fallback: '#ebe9e2'}
    surface: {oklch: 'oklch(0.97 0.01 95)', fallback: '#f6f4ef'}
    surface-recessed: {oklch: 'oklch(0.89 0.01 250)', fallback: '#e2e5e8'}
    surface-raised: {oklch: 'oklch(0.99 0.01 95)', fallback: '#fbfaf6'}
    ink: {oklch: 'oklch(0.22 0.04 255)', fallback: '#151f3a'}
    ink-secondary: {oklch: 'oklch(0.34 0.04 255)', fallback: '#334058'}
    ink-muted: {oklch: 'oklch(0.48 0.04 255)', fallback: '#596579'}
    border: {oklch: 'oklch(0.60 0.03 255)', fallback: '#8b95a3'}
    border-strong: {oklch: 'oklch(0.28 0.05 255)', fallback: '#151f3a'}
    action: {oklch: 'oklch(0.48 0.16 255)', fallback: '#2666cc'}
    accent: {oklch: 'oklch(0.45 0.18 300)', fallback: '#684cc6'}
    marker: {oklch: 'oklch(0.68 0.12 85)', fallback: '#b79a5a'}
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
  signature:
    motif: vertical plumb line terminating in a pointed geometric bob
    identity-accent: aged brass only; never a semantic status color
---

# Plumbline design source

Plumbline is the editorial branch of Edriffles Computer Web for this AT Protocol
client. Its interface direction is **Seamful Hypertext Workbench**: a serious
publication that became interactive software. ECW remains the underlying
visual, interaction, accessibility, responsive, and browser-behavior system;
this file fixes the additional Plumbline product language.

The client is an agent of the user, not a window owned by the network operator.
That principle is expressed through visible provenance, narrow delegation,
replaceable providers, ordinary exit actions, and addressable browser-native
objects. It is not expressed through political decoration or slogans.

## Brand identity

- Use the Plumbline plumb-bob mark from
  `upstream/social-app/assets/plumbline/plumbline-mark.svg` for the web mark.
- Use the `plumbline` wordmark in web identity surfaces, metadata, splash
  screens, and share cards.
- Keep AT Protocol facts, `app.bsky.*` record namespaces, hosting-provider
  names, and account handles technically accurate. They are interoperability
  and service references, not the product identity.
- Do not mix the Bluesky mark into the Plumbline web shell. Protocol names and
  record namespaces remain visible when they explain interoperability.

## Plumbline test

Whenever an actor, service, rule, algorithm, or configuration changes the
experience, the interface should make these questions answerable at the right
level of disclosure:

1. What happened?
2. Who or what caused it?
3. According to whose rule?
4. What can I change?
5. Can I substitute, revoke, appeal, export, or leave?

Ordinary views stay calm. The inspector and service workbench progressively
expose provider, rule, record, permission, and recovery details when they give
the user more agency.

## Direction

- Use a restrained editorial computer interface: warm paper surfaces, dark
  navy ink, cool-gray workspace framing, aged-brass identity markers, strong
  rules, disciplined columns, and compact document density.
- Prefer `NAVIGATOR | DOCUMENT STREAM | INSPECTOR` on desktop. The inspector is
  an apparatus for explaining the selected object, not a recommendation rail.
- Keep the central stream as a continuous document stream with horizontal rules
  and compact metadata rather than a stack of floating cards.
- Use a vertical plumb line and pointed bob for selected navigation, thread
  ancestry, provenance chains, pane divisions, and unread boundaries. Do not
  repeat literal illustrations as decoration.
- Use Georgia-like editorial serif for the Plumbline wordmark and major
  headings, Verdana-like interface sans for UI and post copy, and Courier
  New-like monospace for DIDs, AT URIs, endpoints, and diagnostics.
- Avoid gradients, glass, giant cards, generic SaaS panels, fake operating
  systems, newspaper or Victorian cosplay, black-and-red political imagery,
  Web3 aesthetics, and protocol-debugger presentation in the default view.
- Use the ALF theme palette at runtime so light, dark, dim, forced-colors, and
  high-contrast modes retain readable surfaces and text.

## Contestable services and provenance

- A provider is a source for a capability, not the capability itself. Label
  providers as defaults and preserve source information for consequential data.
- Feed surfaces should be able to identify the feed, ordering model, provider,
  and applicable moderation sources when that information is available.
- Moderation follows `source -> assertion or label -> user rule -> client
  action`. Network takedown, hosting refusal, AppView absence, third-party
  claims, blocks, and local presentation rules remain distinct.
- Authorization is delegated authority. Ask for the minimum capability,
  explain feature-scoped upgrades, show active sessions and permissions, and
  make revocation, export, backup, migration, and provider change ordinary
  account-management commands.
- Preserve real links, browser Back/Forward, open-in-new-tab, text selection,
  copyable AT addresses, and progressively disclosed record inspection.

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

Desktop keeps the three-part workbench aligned around the center document
stream. As width decreases, collapse or move the Inspector before damaging the
stream, then collapse the Navigator into the existing mobile navigation. Mobile
retains the current context, primary action, and content before secondary
provider metadata. Do not turn desktop columns into an undifferentiated stack.

## Interface states and accessibility

- Loading, empty, partial, permission, stale-provider, unavailable-provider,
  and error states say what is known and what the user can do next.
- Use real headings and landmarks, keyboard-reachable controls, visible focus,
  labels connected to errors, target sizes of at least 30px, and a non-color
  indicator for selected and moderated states.
- Keep the effect budget at zero decorative effects and one lightweight state
  transition budget. Respect `prefers-reduced-motion` and forced-colors.
- Do not invent counts, reasons, provider explanations, or verification claims
  that the underlying data cannot substantiate.

## Motion and effects

The effect budget is zero decorative effects and one lightweight state
transition budget. Use existing button hover/focus treatment and short
opacity/transform transitions only where the platform already supplies them.
Respect `prefers-reduced-motion`; the feature remains fully usable with motion
removed.
