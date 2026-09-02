# Plumbline UI inventory

This inventory traces the real component boundaries before redesign. It distinguishes shared shell infrastructure, Page Mode composition, social behavior, and Workbench-only surfaces.

## Shell and layout

| Concern | Current owner | Current responsibility | Redesign boundary |
|---|---|---|---|
| Authenticated web shell | `upstream/social-app/src/view/shell/createNativeStackNavigatorWithAuth.tsx` | Mounts the route stack, masthead, left/bottom navigation, and right navigation | Keep route/auth behavior; make Page Mode composition explicit and avoid changing Workbench routes |
| Page/Workbench mode | `src/components/Layout/index.tsx`, `src/components/Layout/context.ts` | `Screen` and layout regions, center width, shell mode attributes | Establish publication Page Mode constraints here; preserve Workbench geometry |
| Breakpoints | `src/alf/breakpoints.ts` | `leftNavMinimal`, `rightNavVisible`, mobile/tablet thresholds | Replace mechanical hide/show with named responsive Page Mode states |
| Global Page Mode styling | `src/ecw.css` | Layout grid, headings, tabs, feed item overrides, quote/thread decoration overrides | Consolidate ad hoc overrides into one documented Page Mode layer |
| Brand/masthead | `src/view/shell/PlumblineShellBrand.tsx`, `src/lib/brand.ts` | Wordmark, descriptor, motto, symbol, masthead height | Keep brand contract; revise hierarchy and copy only after direction approval |

## Navigation and contextual surfaces

| Concern | Current owner | Current behavior | Redesign question |
|---|---|---|---|
| Desktop navigation rail | `src/view/shell/desktop/LeftNav.tsx` | Account card, labeled sections, icons, links, `New post` | Can it read as an index with publication sections rather than a generic app menu? |
| Right rail | `src/view/shell/desktop/RightNav.tsx` | Mounts `DesktopWorkbenchInspector`, optional tools, search, context/discovery, footer | Make it a selection-linked marginal apparatus; collapse it when it has no useful context |
| Mobile navigation | `src/view/shell/mobile/BottomBar.tsx` and related web shell components | Persistent bottom navigation on mobile web | Preserve touch targets while moving route/context actions into explicit drawers or sheets |
| Selection marker | `src/view/shell/PlumblineSelectionMarker.tsx` | Repeated selected-state line/bob treatment | Use one consistent active-index and provenance grammar, not many unrelated decorations |

## Home and feed composition

| Concern | Current owner | Current behavior | Redesign question |
|---|---|---|---|
| Home route | `src/view/screens/Home.tsx` and related home screen modules | Route container for feed tabs/composer/feed | Keep data and navigation; replace the Page Mode presentation wrapper |
| Feed heading | `src/view/com/home/HomeHeaderLayout.web.tsx` | `CURRENT EDITION / SECTION`, serif title, mode metadata, feed link, marker | Change visible vocabulary to publication hierarchy while preserving source/mode information on demand |
| Mobile feed heading | `src/view/com/home/HomeHeaderLayoutMobile.tsx` | Mobile-specific header path | Define a deliberate mobile edition header, not a desktop shrink |
| Feed tabs | Home feed tab components under `src/view/com/home/` | Horizontal tablist for Following, For You, custom feeds | Treat as edition navigation with keyboard/overflow support and less toolbar emphasis |
| Feed provenance | `src/components/FeedProvenanceCard.tsx` | Source/state summary and details toggle | Keep source truth; move routine status to a compact issue line and details to the margin |
| Feed item | `src/view/com/posts/PostFeedItem.tsx` | Post/repost wrappers, item layout, feed list identity | Make the list a continuous document while retaining item semantics and test IDs |
| Composer | `src/view/com/composer/` and Home composer modules | New-post entry point and authoring UI | Keep action and auth behavior; make it an editorial entry point rather than a floating app card |

## Posts, embeds, and actions

| Concern | Current owner | Current responsibility | Redesign boundary |
|---|---|---|---|
| Post action row | `src/components/PostControls/index.tsx`, `PostControlButton.tsx` | Reply, repost, like, vote, bookmark, share, menu | Preserve mutations and accessibility; reduce visual chrome in Page Mode only |
| Repost | `src/components/PostControls/RepostButton*.tsx` | Repost/un-repost behavior | Keep behavior, add typographic attribution in document flow |
| Post embeds | `src/components/Post/Embed/index.tsx` and subcomponents | Images, video, links, feeds, lists, quote posts, chats | Keep media and link semantics; define one integrated preview treatment instead of nested cards |
| External site previews | `src/components/Post/Embed/ExternalEmbed/`, `StandardSiteEmbed/` | External metadata and media presentation | Use publication-style figure/caption treatment where data exists; never fabricate provenance |
| Quote embeds | `src/components/Post/Embed/LazyQuoteEmbed.tsx`, related | Nested post/quote presentation | Remove redundant enclosure while preserving a clear quote boundary and source link |
| Thread route | Post-thread screen modules and `src/components/Post/PostProvenance.tsx` | Root post, replies, ancestry, provenance, actions | Use the same document rhythm as feed, with a persistent thread spine and contextual marginal notes |

## Provenance and authority surfaces

| Concern | Current owner | Current responsibility | Redesign question |
|---|---|---|---|
| Post provenance | `src/components/Post/PostProvenance.tsx` | Source/record context for a post | Which cue belongs in the byline, and which belongs in the Inspector? |
| Provider composition | `src/components/ProviderCompositionProvenance.tsx` | Provider agreement/disagreement and source identity | Keep disagreement explicit without making every post an audit readout |
| Identity resolution | `src/components/IdentityResolutionProvenance.tsx` | DID/handle resolution source and status | Show a compact status cue, with details on demand |
| Media delivery | `src/components/MediaDeliveryProvenance.tsx` | Media source/delivery information | Keep infrastructure metadata in technical detail, not ordinary copy |
| Authorization | `src/components/AuthorizationProvenance.tsx` | Permission/session explanation | Remain in Workbench/settings, surfaced contextually when an action requires authority |

## Workbench surfaces that must not inherit the Page Mode redesign wholesale

| Surface | Owner | Reason to preserve separate mode |
|---|---|---|
| Services | `src/screens/Settings/ServicesSettings.tsx` | Provider tables, health, replacement, and comparison are configuration work |
| Identity | `src/screens/Settings/IdentitySovereigntySettings.tsx` | Migration, recovery, export, and sessions require explicit account-management affordances |
| Moderation | `src/screens/Moderation*`, `src/screens/ModerationInteractionSettings/` | Layered assertions/rules/actions need inspectable controls and stronger state treatment |
| Authorization | Settings authorization surfaces | Permission scope, consent, and revocation require deliberate workflows |
| Diagnostics | diagnostics/provenance components and screens | Raw protocol details are expert content, not default stream content |

## Architectural conclusion

The smallest useful redesign boundary is the web Page Mode composition: shell grid, Page Mode masthead/section header, navigator presentation, inspector presentation, feed list rhythm, and their CSS contracts. The social data hooks, mutations, provider composition, auth, post controls, embeds, and Workbench screens should remain intact. This gives a high-value visual/information-architecture change without duplicating or rewriting protocol behavior.
