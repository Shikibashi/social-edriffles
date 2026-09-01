# Render critique: Plumbline Page Mode editorial reconstruction

## Review target

- Date: 2026-09-01
- Surface: `https://plumblines.uk/`
- Browser: ChatGPT in-app browser, read-only logged-out desktop inspection
- Baseline title: `Following — Plumbline`
- Baseline status: rejected by product-owner instruction and source inspection

## Rejected baseline findings

The current shell cannot pass the canonical Plumbline test as rendered:

1. Product identity is confined to the left rail instead of establishing a
   publication masthead across the page.
2. The core feed is explicitly mounted in `workbench` mode and visibly labels
   itself `DOCUMENT STREAM`; the left rail visibly labels itself `WORKSPACE`.
3. The central reading surface is constrained to a 600-pixel column while the
   surrounding application shell consumes visual attention.
4. The inspector appears as a bordered, shadowed dashboard card rather than
   marginal reference apparatus.
5. The page reads as a social application with ECW tokens rather than a serious
   periodical that became interactive software.

This is not accepted as a partially successful Plumbline direction. More
decoration, a new palette, or a smaller logo cannot correct it.

## Required reconstruction test

Reject the resulting render if a reviewer can reasonably summarize it as:

```text
Bluesky with an ECW or retro stylesheet
```

Accept only when the first desktop viewport immediately communicates:

- editorial publication;
- Plumbline identity;
- continuous document flow;
- marginal provenance;
- display-serif hierarchy;
- structural plumb-line geometry.

## Review method after implementation

1. Inspect the local production build in a new ChatGPT in-app browser tab at
   wide desktop, compact desktop, and mobile widths without signing in or
   mutating social state.
2. Confirm no horizontal overflow, clipped masthead, or desktop rail leaks into
   mobile reading width.
3. Confirm the navigator remains legible until the layout actually transitions
   to the existing mobile navigation.
4. Confirm source, rule, and control still expose actual route-derived content.
5. Conduct a grayscale structural pass: hide brass mentally and verify that type
   roles, horizontal rules, column hierarchy, alignment, and marker shape still
   distinguish masthead, index, stream, and margin.
6. Check keyboard focus and semantic landmarks by DOM inspection; visual rails
   must not replace accessible text.

## Non-goals

- This critique does not certify a login, post, like, repost, reply, quote,
  profile edit, Spaces, or OAuth mutation in a live account.
- It does not claim a visual marker verifies an account or source.
- It does not replace existing provider, protocol, or behavioral validation.
