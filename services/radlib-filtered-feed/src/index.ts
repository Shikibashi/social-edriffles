import {createRadlibFeedServer} from './server.ts'
import {normalizePolicy} from './policy.ts'

const port = Number.parseInt(process.env.RADLIB_FILTERED_FEED_PORT ?? '19070', 10)
const did = process.env.RADLIB_FILTERED_FEED_DID ?? 'did:web:localhost'
const feedUri = process.env.RADLIB_FILTERED_FEED_URI ?? `at://${did}/app.bsky.feed.generator/radlib-filtered-following`
const storePath = process.env.RADLIB_FILTERED_FEED_SQLITE ?? './radlib-filtered-feed.sqlite'
const serviceEndpoint = process.env.RADLIB_FILTERED_FEED_ENDPOINT
const configuredTerms = (process.env.RADLIB_CONTENT_FILTER_TERMS ?? '')
  .split(',')
  .map(term => term.trim())
  .filter(Boolean)

const service = createRadlibFeedServer({
  did,
  feedUri,
  serviceEndpoint,
  serviceFragment: process.env.RADLIB_FILTERED_FEED_SERVICE_FRAGMENT,
  storePath,
  ingestionConfigured: process.env.RADLIB_FILTERED_FEED_INGESTION === 'configured',
  ingestToken: process.env.RADLIB_FILTERED_FEED_INGEST_TOKEN,
  auth: {
    acceptUnsignedDevJwt: process.env.RADLIB_DEV_ACCEPT_UNSIGNED_VIEWER_JWT === '1',
  },
  policy: normalizePolicy({
    enabled: process.env.RADLIB_CONTENT_FILTER_ENABLED === '1',
    algorithm: process.env.RADLIB_CONTENT_FILTER_ALGORITHM === 'strict' ? 'strict' : 'contextual',
    customTerms: configuredTerms,
  }),
})

service.server.listen(port, () => {
  process.stdout.write(`radlib-filtered-feed listening on http://127.0.0.1:${port}\n`)
})

function shutdown() {
  service.server.close(() => {
    service.store.close()
    process.exit(0)
  })
}

process.on('SIGINT', shutdown)
process.on('SIGTERM', shutdown)
