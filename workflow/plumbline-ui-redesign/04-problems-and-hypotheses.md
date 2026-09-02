# Problems and hypotheses

## Diagnosis method

The current render, DOM snapshot, source inventory, and existing design documents were compared. The screenshot is treated as evidence of composition, not as a complete specification. Each hypothesis below has a proposed falsification test; successful compilation or a more historical color palette is not sufficient evidence.

## H1 — Branding is subordinate to application chrome

**Observed evidence:** The current page has a masthead, but the account card, navigation labels, and social-app controls still establish the first visual hierarchy. The page identity is not carried by the masthead alone.

**Hypothesis:** A full-width masthead with wordmark, descriptor, motto, rules, and clear section entry will make the publication identity recognizable before the user notices ordinary social controls.

**Test:** Blind comparison of the first viewport at wide and medium desktop, with color removed. Ask participants to identify the product type and current section before interacting. Reject if the result is still described as a generic social client with a themed rail.

## H2 — The UI exposes implementation vocabulary

**Observed evidence:** `Index`, `CURRENT EDITION / SECTION`, `MODE`, provenance rows, and `Workbench inspector` appear as stacked chrome. Current implementation terms are useful to engineers but not all are useful as dominant user-facing headings.

**Hypothesis:** Editorial labels such as a section title, edition line, byline, source cue, and marginal note will improve orientation without hiding provider accountability.

**Test:** Inventory all visible headings and classify each as user task language, provider/provenance language, or implementation vocabulary. No implementation vocabulary may dominate the initial stream viewport; source/provider fields must remain reachable in one explicit action.

## H3 — The three regions have insufficient role differentiation

**Observed evidence:** The current left rail, center route, and right rail have similar visual weight and repeated borders/controls. The center is not sufficiently dominant.

**Hypothesis:** A publication index, a dominant document stream, and a contextual marginal apparatus will be understood as different roles when their typography, density, and interaction grammar differ.

**Test:** Selection task: find the active section, read one post, and inspect why it appears. Measure first correct target, pane switching, and mistaken attempts to use the Inspector as navigation. The stream must remain the primary visual and keyboard reading order.

## H4 — Typography is too homogeneous

**Observed evidence:** Existing Page Mode rules add serif headings but much of the layout still uses common UI treatment. Monospace metadata is used as an identity cue in places where it is not infrastructure.

**Hypothesis:** Explicit task-based type roles will make publication hierarchy legible: display serif for masthead/section/marginal titles, sans for content and controls, monospace only for actual identifiers/endpoints/records.

**Test:** Grayscale screenshot review plus DOM/style audit. Remove color and icon assets; section, byline, body, source, and technical metadata must remain distinguishable. Flag any monospace field that is not an identifier, endpoint, version, timestamp, AT URI, or provider ID.

## H5 — The Inspector is dashboard-like

**Observed evidence:** The right rail is less boxed than older versions, but it still presents persistent source/rule/control blocks, optional tools, search, and context utilities regardless of the selected object.

**Hypothesis:** A selection-linked marginal note with definition-like fields and progressive expansion will provide better accountability with less competition for attention.

**Test:** Compare no-selection, feed-selection, post-selection, label-selection, and service-selection states. The Inspector must either explain the selected object or collapse into a lightweight context cue. The user must reach technical detail in one or two predictable steps.

## H6 — The document stream does not yet feel like a document

**Observed evidence:** Feed posts are flatter, but status rows, tabs, nested embeds, and action controls still create repeated component boundaries. Thread/provenance markers appear as several independent decorations.

**Hypothesis:** A continuous publication stream with bylines, a single ancestry/provenance spine, printer-like separators, integrated figures, and compact action lines will improve reading continuity.

**Test:** Compare scroll traversal and visual segmentation. Posts must read as entries in one document rather than isolated cards; quote/media boundaries remain understandable without rounded containers. Action controls remain keyboard and screen-reader discoverable.

## H7 — Historical identity is being carried by beige

**Observed evidence:** The current palette communicates the intended period association more strongly than the structure does.

**Hypothesis:** The masthead, type hierarchy, rules, measure, bylines, document flow, and plumb-line geometry will remain recognizably Plumbline in grayscale.

**Test:** Generate a grayscale render at wide desktop, standard desktop, and narrow mode. Remove logo/wordmark in a second review. Reject if identity collapses into “generic social app with borders.”

## H8 — Desktop space is underused and the stream is still cramped

**Observed evidence:** The central measure is near 760px, but the surrounding shell spends substantial space on persistent utility structures and stacked status controls. The browser connector did not yet verify true target viewport sizes.

**Hypothesis:** A wide application canvas can support simultaneous index and marginal context while preserving a moderate reading measure; at smaller widths, side apparatus should yield before prose measure does.

**Test:** Capture true 1440x900, 1280x720, and 1024x768 renders with a browser that honors viewport changes. Record stream character measure, visible posts, scroll position, and side-rail state. Reject any layout that expands ordinary post prose beyond a readable measure or hides the active section.

## Cross-cutting risks

| Risk | Why it matters | Guardrail |
|---|---|---|
| Removing too much chrome | Users may lose action discoverability or route orientation | Keep explicit links, buttons, labels, focus states, and a short path to advanced surfaces |
| Showing too much provenance | Accountability can become a reading burden | Typed, task-relevant summary first; deeper evidence on demand |
| Persistent three-pane commitment | The Inspector may consume space without helping reading | Treat Inspector visibility as a state, not a constitutional layout requirement |
| Decorative plumb geometry | Repeated markers can become visual noise | One spine per relevant document/ancestry context; markers must encode a relationship |
| False transparency | A source label may be mistaken for proof or correctness | Separate provider/source, explanation, evidence/status, and user control |
| Responsive shrinkage | Desktop composition can become unusable on mobile | Define explicit mobile transformations and test with actual viewport/device behavior |
