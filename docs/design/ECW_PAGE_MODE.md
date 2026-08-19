# ECW Page Mode

Page Mode is the default for ordinary social use: Home, Following, Balanced, custom feeds, threads, profiles, search, lists, notifications, and post detail.

## Structural order

1. **Identity/masthead:** product mark, current account context, and primary navigation.
2. **Navigation/utilities:** addressable section links, search, compose, and account/service utilities.
3. **Context/status:** active feed/provider/algorithm, stale/offline/error state, and relevant user controls.
4. **Primary content:** timeline, thread, profile, search result, or list.
5. **Secondary information:** provider provenance, labels, relationship state, explanation, or recovery action.
6. **Footer/escape:** settings, service details, legal/help, and a route back to the account context.

The exact shell may be responsive and platform-specific.  The information order must remain understandable when the sidebar becomes a bottom bar or a narrow view.

## Surface treatment

- Use one or a small number of strong framed surfaces rather than a cascade of soft floating cards.
- Use the blog's 74ch reading discipline for long explanations and thread text where practical; timelines may be wider to preserve media and interaction affordances.
- Use thin/dotted rules for separation and real structural borders for load-bearing grouping.
- Keep interaction copy in the Verdana-like UI voice, display titles in Georgia-like identity voice, and timestamps/provider/version details in Courier-like metadata.
- Keep links visibly link-like and preserve browser back/forward/new-tab behavior.
- Let the active control, selected feed, and current route be visible without relying on color alone.

## Social-specific rules

- Home identifies `Following`, `Balanced`, or the named custom/external feed and its provider/version.
- “Why this post?” is a compact, honest explanation of the actual candidate/ranking trace; it must not be decorative copy.
- More/Less controls remain attention preferences.  They must not look like follow/block relationship actions.
- A block or mute presentation identifies the actor and scope.  A community, labeler, or provider judgment is not presented as the user's durable relationship.
- Provider failure names the failing provider and any explicit fallback.  A substitute must not inherit the original provider's name.

## Responsive behavior

- At wide widths, simultaneous navigation and secondary context are allowed.
- At intermediate widths, collapse secondary context before hiding provenance or active-feed identity.
- At narrow widths, preserve the route title, active-feed identity, primary action, focus order, and 30px compact target floor.
- Avoid horizontal overflow from long handles, DIDs, provider URLs, and explanation text; wrap or provide a keyboard-focusable scrolling region.
- Do not use a fake desktop frame to signal “computer-native.”
