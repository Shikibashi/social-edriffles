# Radlib Filtered Feed Service

Status: first standalone service lane. This document describes only the new
`services/radlib-filtered-feed/` implementation. It does not claim live
network integration unless the operator supplies feed-generator identity,
viewer-JWT verification, and firehose ingestion.

## Scope

The service is a dependency-free TypeScript feed-generator skeleton for
`app.bsky.feed.getFeedSkeleton`. It provides a self-hosted, rules-first,
user-sovereign attention lane:

- bounded local persistence through Node 26 `node:sqlite`;
- a standard `GET /xrpc/app.bsky.feed.getFeedSkeleton` endpoint;
- `GET /xrpc/app.bsky.feed.describeFeedGenerator`;
- `GET /xrpc/_health` and `GET /.well-known/did.json` provider identity
  surfaces;
- `GET /radlib/provenance`, `GET /health`, and `GET /ready`;
- authenticated viewer DID extraction with fail-closed production behavior;
- a decoded `com.atproto.sync.subscribeRepos` ingestion boundary;
- explicit viewer/deployment term filtering with legacy algorithm metadata;
- hard exclusion precedence before ordinary ranking;
- explicit degraded/unavailable health states.

## Term policy

The service ships no content vocabulary. `termPacks` and the `contextual` /
`strict` algorithm labels remain accepted for older manifests, but they are
inert. Only explicit `customTerms` supplied by the deployment or viewer are
matched, using rules-only whole-term matching. There is no live semantic model,
no author ideology inference, and no claim that the service can distinguish
advocacy, criticism, quotation, or reporting.

The standalone process accepts deployment-local terms through the comma
separated `RADLIB_CONTENT_FILTER_TERMS` environment variable. An empty or
unset variable means no term filtering.

## Precedence

The implemented ordering is:

1. protocol hard blocks supplied to the request context;
2. incoming hard blocks supplied to the request context;
3. selected labeler hide;
4. explicit author exclusion;
5. rules-first hard content exclusion;
6. explicit Less demotion;
7. provider/freshness ranking;
8. explicit More boost among surviving candidates.

More cannot silently override a hard content exclusion.

## Launch

From the service directory:

```sh
cd /var/home/tcs/Code/atproto/services/radlib-filtered-feed
RADLIB_CONTENT_FILTER_ENABLED=1 RADLIB_DEV_ACCEPT_UNSIGNED_VIEWER_JWT=1 node src/index.ts
```

Production operators should not set `RADLIB_DEV_ACCEPT_UNSIGNED_VIEWER_JWT=1`.
They must provide a verifier through the service factory before accepting
viewer-scoped requests.

## Test

```sh
cd /var/home/tcs/Code/atproto/services/radlib-filtered-feed
npm test
```

Live decoded-ingestion and outage walkthrough:

```sh
cd /var/home/tcs/Code/atproto
node scripts/radlib_live_filtered_feed_walkthrough.mjs
```

The walkthrough indexes three deterministic posts, verifies contextual
filtering and provenance, then starts the service without ingestion and checks
that readiness and feed reads fail explicitly with `ProviderUnavailable`.

## Non-Claims

This lane does not edit the social-app client, PDS, or selected read provider. It does not
start a firehose connection by itself. The ingestion boundary accepts decoded
`subscribeRepos` commit events, and a production deployment still needs an
operator-supplied firehose/WebSocket decoder plus DID/JWT verification.
