# Brief: Edriffles Computer Web identity refresh

## Intent

Replace upstream Bluesky product identity on the public web client with the
source-owned Edriffles identity while keeping the AT Protocol and hosting
provider facts accurate.

## In scope

- Browser favicon, Apple touch icon, pinned-tab icon, pre-JavaScript splash,
  reusable web logo components, OAuth client name, page metadata, and share
  cards.
- Logged-out web copy, server-rendered `bskyweb` titles, and Edriffles design
  provenance documentation.

## Out of scope

- AT Protocol lexicon names, account handles, PDS/AppView provider names, or
  the OAuth protocol implementation.
- Native app icon variants, mobile bundle identifiers, or upstream service
  infrastructure.
- New domains. The web origin remains `social.edriffles.us`; the PDS remains
  `pds.edriffles.us`.

## Success criteria

1. The web identity layer renders the Edriffles emblem and lowercase wordmark.
2. Generated metadata, favicons, pinned-tab icon, and share cards identify
   Edriffles and resolve on the existing public origin.
3. A repository scan finds no upstream Bluesky mark in the web identity paths.
4. Protocol/provider references remain technically truthful and tests/builds
   pass.
