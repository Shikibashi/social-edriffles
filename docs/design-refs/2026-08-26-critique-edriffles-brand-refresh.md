# Critique: Edriffles Computer Web identity

## Static review

- The source emblem reads clearly at 256px and remains recognizable at the
  32px/48px shell sizes because its outer square border stays intact.
- The light and dark share cards preserve the existing ECW palette and have a
  clear mark-to-wordmark hierarchy at 1200x630.
- The wordmark is live web text, so it follows the active text color and has a
  meaningful accessible label rather than relying on a provider-specific SVG
  path.

## Risks and mitigations

- Detailed nautical linework can compress at very small sizes. The mark is
  paired with the `edriffles` name in lockups and is not used as an icon-only
  product explanation.
- Existing protocol/provider copy still contains Bluesky names where those
  names identify the actual network or service. That is intentional attribution,
  not a missed product-mark replacement.
- Native upstream app icons remain unchanged in this web-only pass. A future
  native rebrand must replace the full trademarked asset set together.

## Verification status

Source inspection and generated-asset inspection completed. Automated web build,
focused tests, and repository validation are the required next checks. In-app
browser screenshot review is not claimed unless the browser automation runtime
is available.
