# Reference UI and historical composition study

## Method

The references below were studied for interaction architecture and information hierarchy, not copied as visual skins. Official documentation, primary design papers, and historical source material were preferred. A reference observation is not a local usability test of Plumbline.

## Zotero 7: selected object plus metadata pane

Reference: [Zotero quick start](https://www.zotero.org/support/quick_start_guide) and [Zotero 7](https://www.zotero.org/blog/zotero-7/).

Observed architecture:

```text
collections / navigation | items / working list | selected item metadata
```

Useful pattern:

- The right pane is about the selected item, not a permanent dashboard of application status.
- Metadata is grouped into collapsible sections, so the default view can remain useful without exposing every field.
- The center list remains the working surface; selection links the panes.
- Density is configurable rather than presented as a moral choice.

Plumbline adaptation: the Inspector should be anchored to the selected route/post/feed/provider. It should not repeat the entire service model on every screen. Its summary can be visible, while deeper authority and protocol data are collapsible.

Avoid: copying Zotero's styling or assuming every social task needs a metadata pane.

## Thunderbird: separable, selection-linked panes

Reference: [Thunderbird mail display architecture](https://source-docs.thunderbird.net/en/latest/frontend/mail_display.html) and its [three-pane UI documentation](https://support.mozilla.org/en-US/kb/whats-new-thunderbird-115).

Observed architecture:

```text
folder/context | message list | selected message
```

Useful pattern:

- The panes have distinct jobs and can be reorganized or hidden.
- A selected object can be opened in a separate tab/window without losing the list context.
- The content pane is not forced to carry all navigation and metadata simultaneously.
- Wide, vertical, and single-pane modes are meaningful alternatives, not just resized versions of one grid.

Plumbline adaptation: Inspector visibility should be a real Page Mode choice. Opening a post/thread or context view should preserve the feed route and scroll position. Medium widths should be able to move the Inspector into an explicit overlay/drawer.

Avoid: making every route permanently three-pane when the task is reading a single document.

## Wikipedia Vector: bounded reading in a wide viewport

Reference: [Vector 2022 design documentation](https://www.mediawiki.org/wiki/Skin:Vector/2022/Design_documentation).

Observed architecture:

- The article measure is bounded for reading even on wide screens.
- Navigation and tools can remain available without expanding the prose to the full viewport.
- The page distinguishes reading surface from utility controls.

Plumbline adaptation: wide desktop should be used for simultaneous index and marginal context, not for 150-character post lines. The reading measure and total application width are separate constraints.

Avoid: copying Wikipedia's visual identity, typography, or content assumptions.

## Mature feed/news readers: document list and source context

The reference set includes long-lived feed-reader patterns documented by [Feedly's feed organization help](https://docs.feedly.com/article/84-organize-your-feeds) and [NetNewsWire's user documentation](https://netnewswire.com/help/).

Common architectural lessons:

- Source/section navigation is a list or collection model, not a row of marketing tabs.
- The reading surface supports keyboard traversal and preserves unread/position state.
- Source identity is present but subordinate to the item title/content.
- A reader can move between overview/list and selected article without losing orientation.

Plumbline adaptation: feed editions can be navigated as an index of sections. The active provider and ordering model can be a compact line beneath the section title, with full explanation in the margin.

Avoid: copying a feed reader's unread mechanics or assuming a social timeline is a set of articles.

## Historical *Liberty*: masthead, rules, and editorial seriousness

Reference archive: [Benjamin Tucker's *Liberty*, 1881–1908](https://archive.org/details/benjamin-tucker-liberty/1881-1908_BenjaminTucker_Liberty_01-01/mode/1up). The publication is also described as a biweekly newspaper in [the archive collection](https://archive.org/details/benjamin-tucker-liberty).

Composition principles extracted from the scans:

- The masthead establishes the publication before the reader enters any individual item.
- Horizontal rules carry hierarchy and rhythm; they do not need to enclose every group.
- Headlines, bylines, and body matter are differentiated by role and measure.
- Dense information is made navigable by alignment, repeated typographic structure, and section boundaries.
- The page feels authored and public without making the apparatus itself the subject.

Plumbline adaptation: use a genuine masthead, section/edition hierarchy, byline rhythm, printer-like separators, and a continuous document stream. The plumb-line can become a vertical editorial/provenance spine that aligns entries and selected references.

Avoid: antique paper effects, period ornament, newspaper-column mimicry, or decorative historical cosplay. The design must remain legible and recognizable in grayscale.

## Reference conclusions

| Reference lesson | Plumbline decision |
|---|---|
| Selected-object panes earn their space through selection | Inspector is contextual and may collapse when no useful object is selected |
| Wide applications need a bounded reading measure | Keep a moderate stream measure and spend extra width on index/margin/context |
| Long-lived readers use lists/sections rather than generic tab chrome | Treat editions as publication sections with a compact control line |
| Historical editorial authority comes from hierarchy and rules | Masthead, bylines, baselines, separators, and measure carry identity |
| Complex tools need explicit advanced surfaces | Keep Services, Identity, Moderation, and diagnostics in Workbench mode |
