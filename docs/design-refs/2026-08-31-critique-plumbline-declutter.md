# Render critique: Plumbline shell decluttering

## Review target

- Local production web export from `upstream/social-app`.
- Reference browser review at approximately 1265 CSS pixels wide.
- Review states: logged-out collapsed context and expanded optional context.

## Before

The desktop shell presented the stream between a full Navigator and a busy
right rail. The rail simultaneously showed the selected-surface Inspector,
search, available feeds, progress guidance, live-event content, and trends.
The stream also showed its feed authority summary beside a nested provider
composition summary. Each item was useful, but the first viewport offered too
many competing entry points and made the optional services look like a second
work surface.

## After

- The stream remains the dominant document surface.
- The selected-surface Inspector remains first in the right rail.
- Search remains immediately available.
- Feed lists, progress guidance, live events, and trends are behind one
  accessible `More context` disclosure and are not mounted while collapsed.
- The feed surface keeps one concise authority summary; provider comparison
  remains available through its existing inspection control.
- The right rail scrolls independently when optional context is expanded.

## Browser evidence

The local collapsed-state accessibility snapshot reported:

- `Show more context` present with no translation IDs;
- secondary context and discovery regions absent;
- feed actions `Reply`, `Repost or quote post`, and `Like` present;
- the feed and selected-surface summaries remained readable.

After activation, the snapshot reported `Hide more context` and the optional
discovery region with its existing sources. The rendered desktop review showed
the closed state as a compact Inspector/Search/context stack and the expanded
state as a contained secondary panel rather than a competing dashboard.

## Remaining review boundary

The local browser review does not prove production deployment or authenticated
provider behavior. Mobile navigation remains owned by the existing
`isMobile` shell path; the code and breakpoint contract were preserved, but a
separate physical mobile viewport was not available in the in-app browser
connector during this review.
