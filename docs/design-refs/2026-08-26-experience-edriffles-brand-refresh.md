# Experience contract: Edriffles Computer Web identity

## User promise

When a visitor opens `social.edriffles.us`, the page identifies itself as
Edriffles Computer Web immediately, before and after JavaScript loads. The
product presents itself as an independent AT Protocol client without implying
that Edriffles is the PDS or that the upstream network is the publisher of the
web client.

## Identity hierarchy

1. Edriffles emblem: the visual mark in browser chrome, splash, shell, dialogs,
   and server-rendered pages.
2. `edriffles` wordmark: the lowercase display name beside or below the mark.
3. `Computer Web`: the descriptor used in metadata and share-card identity.
4. AT Protocol, PDS, AppView, account handles, and `app.bsky.*`: technical
   context shown only where it describes a real protocol or service boundary.

## State coverage

| State | Identity surface | Required result |
| --- | --- | --- |
| Pre-JavaScript | Inline splash SVG | Edriffles mark, no Bluesky butterfly |
| Logged out | Auth splash and footer | Edriffles mark/wordmark and Edriffles links |
| Logged in | Header, bottom bar, dialogs, home shell | Reusable web mark resolves to Edriffles |
| Server rendered | `bskyweb` title, metadata, favicon, share card | Edriffles metadata on the existing origin |
| OAuth | Public client metadata and authorization handoff | Client name is Edriffles; provider names remain factual |

## Accessibility and trust

The emblem receives the product name as an accessible label. Wordmark text is
live text on web rather than an unlabeled decorative path. The detailed emblem
is not used as the only source of meaning in a control, and the identity pass
does not alter relationship, moderation, or provider behavior.
