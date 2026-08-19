# ECW Workbench Mode

Workbench Mode is for Services, Identity, Sessions/Recovery, Personalization, Moderation, Diagnostics, and advanced attention controls.  It makes many relevant facts visible at once without turning ordinary reading into an administration console.

## Regions

- **Command/context bar:** title, current account, route, and reversible actions.
- **Navigator:** stable links for service domains or settings sections.
- **Workspace:** the selected provider, identity, personalization, or policy surface.
- **Inspector/details:** actor, scope, version, source, timestamps, and recovery/reset actions.
- **Status/output line:** concise state such as `PDS available`, `AppView unavailable`, `import queued`, or `last sync`; this is not automatically a live region.

The regions may become stacked sections on small screens.  Every pane has a named heading and a non-drag alternative for resizing/reordering where those behaviors exist.

## Service and authority presentation

Provider identity is a first-class field, not a decorative badge.  Use explicit labels:

| Fact | Preferred presentation |
| --- | --- |
| Account repository | `PDS: host/name` |
| Read model | `AppView: host/name` |
| Feed | `Feed provider: name`, algorithm/version |
| Search | `Search provider: name` |
| Resolution | `Resolver: name` |
| Moderation judgment | `Labeler: name`, label/policy |
| Community surface | community name, jurisdiction, provider |
| Private messaging | messaging provider/room scope |

If a service is unavailable, keep the actor name attached to the error and expose only an explicit, provenance-preserving fallback.  Never use “the platform” when a specific provider made the decision.

## Identity and recovery

Identity surfaces lead with DID/handle state, PDS/AppView distinction, sessions, recovery authority, and migration status.  Recovery and lockdown controls name what they affect and what they do not affect.  Resetting personalization must not look like deleting identity; changing an AppView must not look like changing a PDS.

## Personalization and attention

Workbench controls expose inspect/reset/export/import, active feed/provider/algorithm, discovery/freshness/variety controls, explicit More/Less state, and explanation/provenance settings.  Preference controls are visibly separate from follows, mutes, blocks, and other durable association records.

## Density, contrast, and recovery

- Compact mode increases simultaneity while retaining the 30px target floor.
- Comfortable mode adds whitespace without changing the type scale.
- Increased contrast strengthens text/borders/focus and preserves the same layout.
- Destructive or consequential changes prefer a reachable undo path; confirmation names the object and consequence when undo is not possible.
- Empty, stale, denied, offline, and error states state what exists, what is unavailable, and what the user can do next.
