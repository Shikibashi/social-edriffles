# Structural design directions

These are three different information architectures, not palette variants. All preserve the existing social data, provider, authorization, moderation, identity, and browser-link behavior. Scores are design hypotheses on a 1–5 scale, not usability results.

## Direction A — Publication Ledger with Marginal Edition

### Wireframe

```text
+------------------------------------------------------------------------------+
|                         PLUMBLINE MASTHEAD                                   |
|             Social client for the open web · motto · rule                    |
+-------------------+--------------------------------------+------------------+
| INDEX / NAVIGATOR |       EDITORIAL DOCUMENT STREAM       | MARGINAL NOTE    |
|                   |  section title / edition / source    | selected object  |
| account           |  byline                              | why shown        |
| sections          |  post text                           | source/provider  |
| editions          |  figure / quote                       | rule/status      |
| reading           |  action line                          | control          |
| services          |  printer rule                         | details          |
+-------------------+--------------------------------------+------------------+
```

### Interaction model

- The Stream is the visual and keyboard primary surface.
- The Index is persistent on wide desktop and behaves like a publication index: sections, editions, reading collections, then explicit escape routes to Workbench.
- The Inspector is selection-linked. It shows a compact note when useful and can collapse when nothing is selected.
- Selecting a feed, post, provider, label, or service updates the Inspector without replacing the document route.
- `Why this?`, `What was omitted?` where grounded, and `What can I change?` are separate actions.

### Responsive behavior

- Wide: approximately `208px / minmax(0, 1fr) / 240px`; Stream retains a moderate reading measure inside the central region.
- Standard: compact Index plus Stream; Inspector becomes a contextual drawer or a narrow margin only when populated.
- Tablet: Stream with explicit Index and Context drawers.
- Mobile: compact masthead, Stream, bottom/edge controls for Index and Context; no permanent right dashboard.

### Provenance model

The source cue appears near the section or selected entry at summary level. Provider endpoint, DID, algorithm declaration, record, and reconciliation evidence are in the Inspector's progressive path. A stale or unavailable source is named as such.

### Strengths

- Closest to the required publication/index/document/margin model.
- Supports simultaneous orientation, reading, and explanation on wide screens.
- Keeps advanced authority operations in existing Workbench mode.
- Gives plumb-line geometry a structural home as one stream/ancestry spine plus selection markers.

### Weaknesses

- A persistent Index still costs horizontal space.
- A margin can become a dashboard if its selection contract is weak.
- Requires careful synchronization between route, selection, scroll, and drawer states.

### Research support and conflicts

Supported by overview/detail and coordinated-view literature, Zotero/Thunderbird selection-linked panes, Vector's bounded reading measure, and *Liberty*'s masthead/rule hierarchy. It conflicts with the temptation to expose every provider detail persistently; progressive disclosure and calm peripheral status constrain that impulse.

### Implementation cost

Medium. The current shell already has the three mounting points, so the main work is to establish role-specific Page Mode composition, remove stacked toolbar vocabulary, make the Inspector contextual, and consolidate CSS. Existing post/feed/provider components can be retained.

## Direction B — Reader's Folio with Context Drawer

### Wireframe

```text
+------------------------------------------------------------------------------+
|                         PLUMBLINE MASTHEAD                                   |
+------------------------------------------------------------------------------+
|  [Index]       FOLLOWING · CHRONOLOGICAL                 [Context]            |
|                                                                              |
|                  EDITORIAL DOCUMENT STREAM                                  |
|            byline                                                          |
|            text                                                            |
|            figure / quote                                                   |
|            actions                                                          |
|            rule                                                             |
|                                                                              |
+------------------------------------------------------------------------------+
```

### Interaction model

- The Stream owns nearly the full desktop canvas and behaves as a reader first.
- Index is hidden behind a persistent but quiet edge control or a keyboard shortcut; Context opens a right drawer only for a selected object.
- The default view has no permanent Inspector. A visible `Context` control and selected-state cue preserve discoverability.
- The current section and compact provider cue remain in the stream header so the page is not epistemically opaque.

### Responsive behavior

- Wide and standard use one bounded reading surface with generous surrounding margin/context space.
- Tablet and mobile use full-screen Stream plus labeled sheets for Index and Context.
- Workbench routes remain separately pane-based.

### Provenance model

The first line of the selected context drawer contains source/provider/rule/status. Deep technical detail is nested. When no post/feed is selected, the drawer is closed rather than filled with generic service widgets.

### Strengths

- Strongest reading continuity and clearest rejection of social-dashboard composition.
- Least risk of Inspector clutter or duplicated metadata.
- Best use of a narrow viewport without shrinking post text.

### Weaknesses

- Navigation and provider controls are less discoverable on desktop if the edge affordance is too quiet.
- Simultaneous source comparison is harder.
- The user may forget that context exists if selection and drawer affordances are weak.

### Research support and conflicts

Supported by focus/context distinctions, calm technology, bounded reading research, and the warning that three columns are not automatically better. It puts more weight on discoverability costs identified by progressive disclosure research and on explicit transitions from simple to powerful layers.

### Implementation cost

Medium-high. It needs a robust contextual drawer, focus/scroll preservation, selection affordances, and desktop navigation replacement rather than merely restyling the current rails.

## Direction C — Correspondence Desk with Register and Reading Pane

### Wireframe

```text
+------------------------------------------------------------------------------+
|                         PLUMBLINE MASTHEAD                                   |
+----------------------+----------------------------------+--------------------+
| INDEX / SECTIONS     | CORRESPONDENCE REGISTER          | READING / MARGIN   |
| editions             | author / excerpt / time          | selected post       |
| providers            | selected row                    | thread ancestry     |
|                      |                                | source/rule         |
|                      |                                | actions             |
+----------------------+----------------------------------+--------------------+
```

### Interaction model

- Home presents a publication register of entries; selecting one opens a larger reading pane.
- The register supplies overview/scanning; the reading pane supplies full post, media, thread, and actions.
- The Inspector is attached to the selected post in the reading pane, not to the whole application.
- Thread traversal is a correspondence workflow: moving through replies changes the selected reading object while preserving the register/route.

### Responsive behavior

- Wide: Index, register, reading pane/margin.
- Standard: register and reading pane; Index is a drawer.
- Mobile: register first, then selected post view with explicit Back to register; context is a sheet.

### Provenance model

The register has a compact source cue per entry only when needed; the reading pane's selected object gets the full marginal explanation. Provider disagreements can be compared for the selected entry without dumping every result into the register.

### Strengths

- Strongest overview/detail and thread-navigation story.
- Makes selection and source comparison concrete.
- Natural fit for correspondence, saved reading, and expert inspection.

### Weaknesses

- Breaks the continuous-feed expectation and adds a selection step to ordinary social reading.
- Can feel like an email client or database browser rather than a publication stream.
- More difficult to preserve quick social actions and mobile scan flow.

### Research support and conflicts

Supported by Thunderbird, Zotero, and overview/detail research. It conflicts with the publication's primary requirement that the Home feed read as a continuous document and with the user's expectation of immediate social feed traversal.

### Implementation cost

High. It requires a new register/selection reading architecture, route semantics, and substantial mobile behavior changes. Existing feed item renderers could be reused, but the shell and navigation contract would change materially.

## Comparative rubric

Scores are provisional design judgments grounded in the research and current code inventory. A higher score is better. They must be validated with renders and user tasks.

| Criterion | A: Ledger | B: Folio | C: Desk |
|---|---:|---:|---:|
| Reading continuity | 4 | 5 | 3 |
| Scanning/orientation | 5 | 3 | 5 |
| Source comprehension | 5 | 4 | 5 |
| Algorithm awareness | 5 | 4 | 5 |
| Provider control | 5 | 4 | 5 |
| Discoverability | 5 | 3 | 4 |
| Expert depth | 4 | 4 | 5 |
| Wide-screen use | 5 | 4 | 5 |
| Mobile recomposition | 4 | 5 | 3 |
| Accessibility/focus model | 4 | 4 | 3 |
| Plumbline editorial identity | 5 | 5 | 4 |
| Existing behavior preservation | 5 | 4 | 3 |
| Implementation risk (inverse) | 4 | 3 | 2 |
| **Total** | **60** | **52** | **52** |

## Recommendation

Direction A is the provisional recommendation because it best satisfies the required publication-first family resemblance while preserving existing behavior and the repository's Page Mode/Workbench boundary. Direction B is the principal alternative if usability testing shows the persistent Index or contextual margin still competes with reading. Direction C is a useful pattern for a future correspondence/reading workspace, not the default Home composition.

The recommendation is not final until a rendered representative slice and an adversarial review test the H1–H8 hypotheses.
