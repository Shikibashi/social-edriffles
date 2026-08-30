# Layout Blueprint: Plumbline editorial computer

## Canonical desktop frame

Reference frame: 1440 × 900 CSS pixels.

```text
┌────────────────┬──────────────────────────────────────┬───────────────────┐
│ PLUMBLINE      │ current route / document stream     │ INSPECTOR         │
│ mark + identity│ author · handle · time              │ selected surface   │
│                │ post content                         │ source            │
│ NAVIGATOR      │ metadata / actions                   │ rule              │
│ route rows     │ ───────────────────────────────────  │ control           │
│ account        │ next document                        │ service link      │
│                │                                      │                   │
└────────────────┴──────────────────────────────────────┴───────────────────┘
```

## Block anatomy

### Navigator

- fixed desktop rail aligned to the center column;
- Plumbline mark, wordmark, `SOCIAL CLIENT FOR THE OPEN WEB`, and quiet motto;
- current account identity remains distinct from product identity;
- labeled route rows use a vertical line and brass bob for selection;
- compose remains a normal square primary control.

### Document stream

- existing route content remains the data owner;
- the shared workbench screen supplies canvas and structural border framing;
- post/document rows use rules and compact metadata where the existing component
  exposes those elements;
- real links remain underlined/addressable;
- primary action and recovery state remain in the route's existing position.

### Inspector

- fixed right apparatus on desktop when the breakpoint supports it;
- a single selected-surface summary before optional search, feeds, trends, and
  footer links;
- labels are uppercase utility text; values remain readable and copyable;
- no rounded floating card treatment; border and rule communicate the seam;
- hidden/deferred before the document stream is narrowed below a useful reading
  width.

## Responsive transformations

1. At the existing tablet breakpoint, retain workbench context but reduce rail
   width and let the inspector defer.
2. At mobile width, use the existing bottom bar/drawer navigation and retain
   only the mark or compact wordmark in the primary shell.
3. Preserve the current route's heading, primary action, and document stream in
   that order.
4. Move source/rule/control detail below the task or into Services; never hide
   a consequential error behind a collapsed visual.

## State and semantics

- Root shell: `data-ecw-shell="true"`.
- Screen surface: `data-ecw-mode="workbench"` for workbench routes.
- Shared regions: `data-ecw-part="shell-brand"`, `left-nav`, `right-nav`, and
  `inspector` identify the style boundary without changing route semantics.
- Existing test IDs remain stable for browser and QA verification.

## Design-plan direction record

The product owner supplied a complete visual direction and exclusions. Three
alternate identity directions were not generated because alternate directions
would contradict the locked Plumbline brief rather than resolve uncertainty.
The implementation must still be reviewed with actual desktop and mobile
renders; a locked direction is not visual verification.
