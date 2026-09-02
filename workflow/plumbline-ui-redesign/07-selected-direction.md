# Selected direction and decision record

## Status

**Approved: Direction A — Publication Ledger with Marginal Edition.**

The user selected Direction A after the research and structural comparison. The representative vertical slice is implemented on the existing Page Mode composition points; Direction B remains a fallback only if later task evidence shows that the persistent marginal context harms comprehension or discoverability.

## Decision record

### Decision: start with Publication Ledger Page Mode

**Problem:** The current UI has the right nouns but still gives a shared social-app shell more visual authority than the publication document.

**Evidence:** The live DOM and source tree show a route stack surrounded by persistent left/right app rails. The baseline render shows a masthead plus three adjacent panels, stacked feed controls, and a right utility dashboard. `00-current-state.md` and `01-ui-inventory.md` record the concrete component hierarchy.

**Research:** Overview/detail and coordinated-view research supports differentiated, synchronized views rather than undifferentiated panes. Zotero and Thunderbird show selected-object context; Vector and screen-reading literature constrain the central measure; *Liberty* supplies masthead/rule/editorial hierarchy principles; progressive-disclosure research supports a short path from summary to technical detail.

**Alternatives considered:**

- Direction B, Reader's Folio: strongest document continuity and the most direct challenge to permanent Inspector assumptions, but weaker desktop discoverability and simultaneous provider context.
- Direction C, Correspondence Desk: strongest register/selection model, but it changes the ordinary social-feed task into a mail/database-like selection workflow and has the highest implementation risk.

**Why selected:** Direction A balances publication identity, continuous social reading, provider/provenance comprehension, desktop simultaneity, responsive collapse, and behavioral preservation. Its central design constraint is that the Index and Inspector must remain subordinate apparatus, not equivalent columns.

**Known tradeoff:** A persistent Index and populated marginal note can recreate application chrome. The implementation must therefore make the Inspector contextual, keep the Stream visually dominant, use role-specific typography, and hide empty utility structures.

**How validated:**

1. Implemented the representative public vertical slice: masthead, Index, edition/section heading, document stream, media post, compact source cue, contextual Marginal note, and responsive recomposition.
2. Captured local renders at 1440x900, 1280x720, 1024x768, and 390x844. A grayscale derivative of the wide render remains legible and structurally distinct without color.
3. The focused web typecheck, affected-file lint, Prettier check, production configuration gate, strict web export, and overflow/geometry browser probes pass. The browser probe confirms marker visibility and the 760px reading surface at wide and standard breakpoints.
4. The in-app browser connector does not expose color-scheme emulation, so a real user-controlled dark-mode render is **NOT VERIFIED** in this iteration. Authenticated selection synchronization and action mutation walkthroughs are also outside the available unauthenticated fixture and remain **NOT VERIFIED**.
5. The independent adversarial reviewer was started but did not return a final report within two bounded waits. The local review therefore records the remaining risks explicitly rather than treating the missing response as approval.

## Implementation boundary

Change first:

- Page Mode shell grid and region semantics;
- full-width masthead relationship to the composition;
- Index presentation;
- section/edition header and feed navigation hierarchy;
- contextual Inspector states;
- feed-entry document rhythm and one plumb/provenance spine;
- Page Mode CSS/token consolidation;
- responsive Page Mode states.

Preserve initially:

- route/auth stack and browser history;
- feed queries and provider composition;
- feed/post provenance data and truthful status;
- post action mutations and accessibility labels;
- embeds/media/link behavior;
- Workbench Services, Identity, Moderation, authorization, migration, and diagnostics;
- real links, AT URIs, DIDs, and expert inspection paths.

## Explicit rejection criteria

Reject the implementation if any of the following remain true in the representative slice:

- the primary viewport is dominated by `WORKSPACE`, `DOCUMENT STREAM`, or other implementation vocabulary;
- the Inspector is a static stack of dashboard boxes when nothing is selected;
- posts still read as floating cards or repeated nested application panels;
- ordinary post prose is widened beyond a deliberate reading measure or narrowed by side apparatus;
- provider/source/rule explanation is either absent or dumped into the default stream;
- grayscale removal makes the layout indistinguishable from a generic social feed;
- the result can fairly be summarized as “Bluesky with an ECW/retro stylesheet.”

## Approval gate

The research phase and Direction A selection gate are complete. The current source implements the first vertical slice; production deployment, commit/push, and authenticated live verification remain separate authorized steps.

## Decision traceability after implementation

### Decision: keep the document measure at 760px while using wide space for apparatus

**Problem:** A full-width feed creates unreadably long lines, while the earlier shell wasted desktop width around a cramped center.

**Evidence:** The rendered 1440px and 1280px probes report a 760px central surface with the Index and Marginal note beside it; the 1024px probe hides the marginal pane and preserves the same central measure; the 390px probe has no horizontal overflow.

**Research:** Overview/detail and text-reading research support simultaneous context around a deliberately bounded reading measure rather than widening the prose itself.

**Alternatives considered:** Keep the former narrow centered column; widen the stream to fill the desktop; or permanently stack all context below the stream.

**Why selected:** It improves simultaneous context without sacrificing scanning and preserves a stable reading surface across the desktop breakpoints.

**Known tradeoff:** The unauthenticated 1024px state still uses the existing bottom account-action bar in place of the compact Index because the shell's logged-out breakpoint owns that CTA behavior. An authenticated compact-Index render must be checked before release.

**How validated:** Browser geometry probes and saved wide, standard, medium, narrow, and grayscale artifacts under `workflow/plumbline-ui-redesign/iterations/01-publication-ledger/`.

### Decision: restore plumb-line markers at the final Page Mode boundary

**Problem:** An older HomeScreen simplification hid the document marker, provenance marker, and feed-item pseudo-elements, so the stream did not visibly express ancestry or provenance.

**Evidence:** Before the correction, the live DOM reported `display: none` for the two markers and no visible pseudo-elements; after the correction, the same selectors report `display: flex`/`block` and populated pseudo-elements at both wide and narrow widths.

**Research:** Seamful design and provenance-interface research support revealing infrastructure seams when they provide agency, while keeping the marker geometry subordinate to the document.

**Alternatives considered:** Leave the stream flat; add decorative icons beside each post; or expose raw protocol metadata inline.

**Why selected:** A single restrained line and reference point communicates ancestry without adding another panel or flooding the default view with protocol text.

**Known tradeoff:** The marker contrast must remain strong enough for grayscale and low-vision users without becoming a competing column. The current version is a candidate for adversarial visual review, not a permanent contrast exemption.

**How validated:** Computed-style browser probes plus saved screenshots; contrast and reduced-motion rules remain inherited from the existing ECW boundary.

### Decision: make Home context progressive and keep public navigation visible

**Problem:** A permanently populated Home Inspector competed with the document stream, while logged-out medium and public states could turn the Index into an account invitation rather than navigation.

**Evidence:** The independent review identified the route-driven Home margin, the public sign-up-only Index, and the medium/mobile context gap as release risks. The second-pass DOM and captures show an `Edition context` summary on Home, a public `Reading` Index, a compact Index at 1024px, and a single-column mobile state.

**Research:** Progressive disclosure and overview/detail research support keeping a lightweight summary available while making deeper context an explicit transition. Mature document applications keep navigation independent from account prompts and use selection-linked detail when detail is needed.

**Alternatives considered:** Keep the full Inspector always open; hide all context on Home; or add a new global mobile drawer before validating the existing post-level provenance disclosure.

**Why selected:** The collapsed Home state reduces repeated metadata without removing the user's route to explanation. Public navigation remains useful before sign-in, and the medium layout preserves the publication index without squeezing the reading surface.

**Known tradeoff:** Home context is currently a route-level edition summary, not a fully selection-linked object inspector; mobile relies on the existing `Why this post?` disclosure. These boundaries are explicit **NOT VERIFIED** items for authenticated and task-based testing rather than claims of completeness.

**How validated:** Clean English second-pass screenshots at 1440x900, 1280x720, 1024x768, and 390x844; grayscale derivative; DOM probes for context labels, no overflow, 760px desktop measure, mobile bottom-bar clearance, and English catalog output. The selected route link also emits `aria-current="page"` after a shared navigation correction.
