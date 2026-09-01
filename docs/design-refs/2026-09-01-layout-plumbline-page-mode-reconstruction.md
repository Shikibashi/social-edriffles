# Layout Blueprint: Plumbline Page Mode editorial reconstruction

## Canonical desktop frame

Reference frame: 1440 by 900 CSS pixels.

```text
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│  PLUMBLINE  ·  SOCIAL CLIENT FOR THE OPEN WEB  ·  ALIGN · INSPECT · UNDERSTAND                │
├───────────────────────┬───────────────────────────────────────────────┬───────────────────────┤
│ INDEX                 │ FOLLOWING                                     │ MARGINAL NOTE         │
│ ───────────────────   │ CURRENT EDITION                               │ ───────────────────   │
│ Home                  │ ───────────────────────────────────────────   │ Following             │
│ Communities           │ │ author · handle · time                     │ Source                │
│ Explore               │ │ post content and integrated media           │ Rule                  │
│ Notifications         │ │ actions                                     │ Control               │
│ Chat                  │ │                                              │ Inspect providers     │
│                       │ │──────────────────────────────────────────    │                       │
│ READING               │ │ next document                               │ ADJACENT SOURCES      │
│ Feeds                 │ │                                              │ search and optional   │
│ Lists                 │ │                                              │ context on request    │
│ Saved                 │ │                                              │                       │
│                       │ │                                              │                       │
│ SERVICES              │ │                                              │                       │
│ Account               │ │                                              │                       │
└───────────────────────┴───────────────────────────────────────────────┴───────────────────────┘
```

## Composition rules

### Masthead

- Owns the full desktop width and begins the visual hierarchy.
- Contains the full PLUMBLINE wordmark, a restrained descriptor, horizontal
  rules, the motto, and one structurally meaningful plumb-line marker.
- Is not a substitute for route navigation or a duplicated social action.
- Is visually useful in grayscale through display type, rule weight, placement,
  and spacing.

### Index / Navigator

- Begins below the masthead on desktop and reads like a compact publication
  index, not a product-logo shelf.
- Uses index, reading, services, and account section labels.
- Uses a continuous vertical selection line and bob as the active-route marker.
- Maintains account context, real links, counts, and existing compose behavior.
- De-emphasizes background surfaces and shadows so the stream retains authority.

### Editorial document stream

- Has the broadest useful desktop measure and a reading-focused section title.
- Uses a display-serif title and a concise utility eyebrow such as `CURRENT
  EDITION`; it must not call itself a workspace or a document stream.
- Presents post entries as one continuous document, never a collection of
  floating cards.
- Uses a slim non-interactive provenance rail, post or thread ancestry lines,
  compact author metadata, integrated media, and printer-like separators.
- Keeps route-owned headers, actions, loading, empty, and error content in their
  existing relative flow.

### Marginal Inspector

- Begins below the masthead and aligns to the document stream rather than
  competing with it.
- Uses `MARGINAL NOTE` as a quiet utility label, then a display-serif route
  title, followed by source, rule, and control details.
- Treats details as a readable definition list, not separate dashboard cards.
- Uses horizontal rules for internal separation and defers optional adjacent
  sources until a user asks for them.
- Retains the existing route-aware attribution and real service destination.

## Page and Workbench allocation

| Surface | Mode | Reason |
|---|---|---|
| Home, profile, post thread, custom feed, topic, tag, community board | Page | primary reading, writing, conversation, and association surfaces |
| Feed, list, saved-record views, notification reading | Page where their existing route layout supports it | document or collection reading surface |
| Services, Identity, Moderation and Reach, diagnostics, authorization, policy, backups, advanced settings | Workbench | configuration, inspection, and explicit capability control |
| Messages and chat split view | existing specialized mode | preserve constrained messaging behavior and authorization boundaries |

## Breakpoint contract

| Range | Layout behavior |
|---|---|
| wide desktop | masthead, labeled index, broad stream, and marginal inspector coexist |
| compact desktop or tablet | preserve the stream first; compact or defer the marginal context before replacing the labeled index |
| mobile | compress masthead, replace desktop index with existing mobile navigation, retain route heading and stream, defer marginal context |

## Semantics and interaction

- Product masthead is a labelled banner; navigator is navigation; stream is main;
  marginal context is complementary.
- The visual provenance rail is `aria-hidden`; actual source, rule, and control
  remain readable text.
- The composition does not change links, action handlers, OAuth grants, provider
  selection, moderation rules, association scope, or recovery controls.
- Existing test IDs remain stable. New IDs identify the masthead and Page Mode
  visual boundary only.
