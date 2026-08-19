# Algorithm customization research

**Date:** 2026-08-19
**Scope:** neutral defaults and explicit local curation controls in the Social web client

## Finding

The strongest common pattern is layered control rather than a single opaque
algorithm setting:

1. A user chooses the source/feed (for example, a following timeline or a
   community/custom feed).
2. The user can give direct, reversible feedback on a post or source.
3. Topic and author preferences are explicit controls, separate from passive
   inference.
4. Advanced controls affect the recommendation surface they describe, not
   durable social relationships or unrelated surfaces.
5. The product provides reset, history, and explanation paths so the user can
   understand and undo personalization.

## Primary-source observations

- Bluesky describes custom feeds as algorithmic feed generators that users can
  choose as timelines. A feed provider can host multiple algorithms, and each
  feed is identified by a repository record rather than being presented as a
  single mandatory platform algorithm: [Bluesky custom feeds](https://docs.bsky.app/docs/tutorials/custom-feeds)
  and [Bluesky custom-feed starter template](https://docs.bsky.app/docs/starter-templates/custom-feeds).
- Mastodon separates the home timeline from list timelines. Lists are user-made
  subsets of the home timeline, while its home-timeline API describes followed
  accounts and followed hashtags as the input: [Mastodon live feeds and lists](https://docs.joinmastodon.org/user/network/)
  and [Mastodon timelines API](https://docs.joinmastodon.org/methods/timelines/).
- YouTube exposes reversible recommendation feedback such as “Not interested,”
  “Don't recommend channel,” clearing feedback, topic controls, and history
  controls. Its documentation also explains that watch/search activity and
  explicit feedback influence recommendations: [YouTube manage recommendations](https://support.google.com/youtube/answer/6342839?hl=en)
  and [YouTube recommendation controls](https://support.google.com/youtube/answer/16533387?hl=en).
- Meta documents direct “Show more” and “Show less” feedback, Favorites,
  unfollow, snooze, and feed-preference controls. These controls are attached
  to the feed or post rather than silently changing a durable relationship:
  [Facebook feed customization](https://about.fb.com/news/2022/10/new-ways-to-customize-your-facebook-feed/)
  and [Facebook News Feed controls](https://about.fb.com/news/2015/07/updated-controls-for-news-feed/).
- Instagram documents Following and Favorites views, plus Not Interested and
  keyword controls for recommendation surfaces: [Instagram feed controls](https://about.fb.com/news/2022/08/testing-ways-to-control-what-you-see-on-instagram/)
  and [Instagram Following and Favorites](https://about.fb.com/news/2022/03/two-new-ways-to-control-what-you-see-on-instagram/).
- TikTok exposes topic sliders in settings and from a “Why this video” path,
  explicitly says those topic preferences apply to For You rather than
  Following/profile/inbox, and warns that changes can take time to affect the
  feed: [TikTok Manage topics](https://support.tiktok.com/en/account-and-privacy/account-privacy-settings/manage-topics)
  and [TikTok recommendation controls](https://support.tiktok.com/en/using-tiktok/exploring-videos/how-tiktok-recommends-content).
- Mastodon’s filter model is also useful as a scope reference: users choose
  contexts such as home, notifications, public timelines, conversations, and
  account views, and filters can be reversible or expiring: [Mastodon filters](https://docs.joinmastodon.org/user/moderating/).

## Design decisions for this fork

### Neutral bootstrap

New accounts start with no positive local curation terms and no built-in topic
taxonomy. The client ships no owner-specific curation vocabulary.

### Explicit terms only

The user adds a positive term under **Local curation terms · explicit terms
only**. The ranking path performs whole-term matching against only those terms
stored in the current account's local state. It does not expand a term into a
bundled topic list, infer synonyms, or activate hidden branch controls.

Old `branchWeights` fields remain accepted as inert compatibility data when an
older profile is imported. New profiles do not contain them, the settings UI
does not render them, and the scorer ignores them.

### Separate positive topics and exclusions

Positive curation topics and negative exclusions are different operations.
The UI therefore has separate inputs and labels:

- **Add a topic or curation term**: a local ordering preference.
- **Exclude a topic or term from local curation**: an ordering exclusion.

Neither operation creates a follow, block, mute, listblock, label, or public
social-graph record. Hard content filters remain separately labeled and scoped.

The content-filter path follows the same rule: legacy `termPacks` and strict
mode fields are import-compatible but inert. Only custom terms entered by the
current account can create a local hard content exclusion.

### Scope and authority

Local curation only reorders candidates supplied by the selected feed. The
Following/chronological option remains available, and explicit post/author
preferences retain higher authority than passive inference. This follows the
documented distinction between TikTok’s For You topic controls and its
Following/profile/inbox surfaces, while retaining ATProto’s user-selected feed
provider model.

### What this does not do

Local curation is not a political quota, ideological balancing rule, or
mandatory recommendation objective. It does not ship a default topic outcome,
political term list, or account-specific vocabulary. Users can choose any
custom term, and a term affects only their local ranking state.

## Regression contract

The deterministic tests cover:

- neutral curation with legacy compatibility fields produces no branch matches;
- arbitrary explicit terms get bounded local ordering weight without taxonomy
  expansion;
- legacy content-pack fields do not filter posts; custom terms do;
- old state without `curationTerms` remains importable;
- positive terms and exclusions persist as separate fields;
- the settings screen renders only generic term and exclusion controls.

## Settings-entry usability and accessibility follow-up

The first live comparison exposed a deployment/UI mismatch: the public bundle
still showed the retired topic-weight controls, and its old “Add curation term”
action wrote to the exclusion list. The current client replaces that ambiguous
two-row interaction with a labeled entry row: a visible instruction, a bounded
text field, an adjacent rectangular **Add term** button, Enter-to-submit, and a
polite confirmation message. The button is disabled while the field is empty,
and the saved term appears immediately as a removable account-local item.

This follows the Edriffles Computer Web contract in
[`docs/design/ECW_CURRENT.md`](design/ECW_CURRENT.md) and
[`docs/design/ECW_TOKENS.md`](design/ECW_TOKENS.md): real buttons, visible
structure, compact-but-not-cramped controls, keyboard alternatives, and
two-tone focus that survives forced-colors mode. The input is kept at the
workbench hit-size floor and the status text is exposed as a polite live
region.

The accessibility decisions are grounded in the primary W3C guidance:

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) requires a programmatically
  determinable name/role/value for controls, sets a 24×24 CSS-pixel minimum
  target-size baseline, and defines status-message exposure.
- [WAI forms guidance](https://www.w3.org/WAI/tutorials/forms/) calls for
  labels or instructions for inputs and simple, short forms.
- [WAI-ARIA APG Button Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/button/)
  requires an accessible button name and documents Enter/Space activation;
  this UI keeps the action as a real button and gives the field a keyboard
  submit path rather than relying on pointer-only interaction.

The source-level and rendered checks now cover the generic field/button pair,
empty-state disabling, button submission, Enter submission, account-local
removal, and the confirmation message. The public deployment remains a
separate operational issue until the Cloudflare Pages credentials/route are
available; the local checkout is the verified implementation.
