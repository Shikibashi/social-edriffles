# Edriffles Computer Web — Current Reconciled Language

**Status:** Pass A complete; this document is the visual contract for the ATProto client pass.  It is not an owner acceptance decision.

## Scope and source precedence

The current ECW language is reconstructed from the living `main`/`master` heads of:

| Product | Current source | What it establishes |
| --- | --- | --- |
| `ideologynormativesorter` | `1820d8d19478677b1b169996814e5a6f1f005ccd` | Workbench density, semantic token roles, data surfaces, accessibility constraints |
| `idoldle` | `33ee4c8fea1e402a16c25bced25756992a05fe0f` | Application controls, display preferences, responsive/keyboard behavior, high-personality product chrome |
| `edriffles-blog` | `a3a1e430b4009de3c035da7b4341adf1635e2452` | Page Mode, editorial reading width, masthead/navigation rhythm, current public-facing palette |

The package at `/var/home/tcs/Downloads/Edriffles Web 99 Design System.zip` has SHA-256 `a59dab80e6f682f7be4411941c4eae5087985f9949cf24647374b108d468d623`.  It is a historical reference only.  Its component names and concrete values are useful for provenance, but do not override the living products.

## The current family resemblance

ECW is a modern web interface with a late-1990s/early-2000s computer-native lineage:

- **Three typographic voices:** Georgia-like display/identity, Verdana-like UI/content, and Courier-like system/metadata.
- **Visible structure:** square or nearly square surfaces, real borders, dotted rules for decoration, and small hard offset shadows.
- **Explicit hypertext:** links look like links, navigation is addressable, and actions use real buttons or links rather than clickable decoration.
- **State is visible:** active feed/provider, loading/empty/stale/denied/offline states, selected controls, and service provenance are written into the interface.
- **Compact but not cramped:** compact is a selectable density, not a 10–11px text treatment.  Action targets keep the ECW 30px compact floor; comfortable mode expands controls without changing the text scale.
- **Accessible personality:** two-tone focus rings, forced-colors survival, semantic HTML where the web path permits it, keyboard alternatives for direct manipulation, and no color-only state.
- **Modern implementation:** no fake operating-system chrome, fixed 800×600 assumptions, CRT effects, or broken browser navigation.

## Product modes

### Page Mode

Home/feed, thread, profile, search, lists, and post views use a readable page shell: identity/masthead, navigation and utilities, context/status, primary content, secondary information, and footer.  Page Mode uses the blog's calm reading rhythm and surface hierarchy.  It does not copy the blog masthead or pretend the social app is an editorial site.

### Workbench Mode

Services, identity, personalization, moderation, diagnostics, and advanced settings use an explicit workbench treatment: a named control area, navigator or section list, main workspace, inspector/details, and a status/provenance line.  Panels may be dense and simultaneous, but each important authority and recovery action remains discoverable.  Workbench Mode is a layout pattern, not a new source of authority.

## ATProto application translation

The client may adopt ECW appearance and information architecture while retaining the fork's existing product behavior.  In particular, this pass does not change:

- direct block, mute, follow, list, or moderation semantics;
- provider authority, fallback, feed selection, ranking, More/Less, or Balanced behavior;
- DID, PDS, AppView, resolver, labeler, session, recovery, or personalization data behavior;
- Candidate Protocol or any existing constitutional contract.

The client already exposes a `Dim` theme.  Because the living ECW sources
establish a dark role grammar rather than a separate named Dim palette, the
client uses a documented low-contrast dark extension for that existing choice;
it is not presented as a new Edriffles source token.

The visual translation should make those existing actors and choices easier to see.  It must not make an AppView look like a PDS, a feed provider look like the platform, or a user preference look like a durable relationship.

## Acceptance test for the language

An implementation conforms when a user can identify what is content, what is a control, who supplied a result, what state is active, and how to change or recover it—while the interface plausibly belongs to the same continuously improved computer/web family as the three living products.
