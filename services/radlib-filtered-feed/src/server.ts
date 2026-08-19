import http, {type IncomingMessage, type ServerResponse} from 'node:http'
import {URL} from 'node:url'
import {extractViewerDidFromAuthorization, type AuthOptions} from './auth.ts'
import {explainPolicy, normalizePolicy, rankCandidates} from './policy.ts'
import {FeedStore} from './store.ts'
import {ingestDecodedSubscribeReposEvent} from './ingest.ts'
import type {ContentFilterPolicy, ServiceHealth, ViewerPolicyContext} from './types.ts'

export type RadlibFeedServerOptions = {
  did: string
  feedUri: string
  serviceEndpoint?: string
  serviceFragment?: string
  displayName?: string
  description?: string
  policy?: Partial<ContentFilterPolicy>
  store?: FeedStore
  storePath?: string
  auth?: AuthOptions
  /**
   * Resolve protocol/delegated boundaries on the provider side. Private
   * custom terms and More/Less ranking preferences are never request headers.
   */
  viewerContext?: (
    viewerDid: ViewerPolicyContext['viewerDid'],
  ) => Promise<ViewerPolicyContext> | ViewerPolicyContext
  ingestToken?: string
  ingestionConfigured?: boolean
}

export type RadlibFeedServer = {
  server: http.Server
  store: FeedStore
  health: () => ServiceHealth
}

const VERSION = 'radlib-filtered-feed/0.1.0'
const MAX_LIMIT = 100
const MAX_CURSOR_BYTES = 512

export function createRadlibFeedServer(options: RadlibFeedServerOptions): RadlibFeedServer {
  const store = options.store ?? new FeedStore(options.storePath ?? ':memory:')
  const policy = normalizePolicy(options.policy)
  const ingestionConfigured = Boolean(options.ingestionConfigured)

  const server = http.createServer(async (req, res) => {
    try {
      const url = new URL(req.url ?? '/', 'http://localhost')

      if (req.method === 'GET' && url.pathname === '/health') {
        return sendJson(res, 200, health())
      }

      if (req.method === 'GET' && url.pathname === '/xrpc/_health') {
        const state = health()
        return sendJson(res, state.status === 'unavailable' ? 503 : 200, state)
      }

      if (req.method === 'GET' && url.pathname === '/.well-known/did.json') {
        return sendJson(res, 200, didDocument(options, req))
      }

      if (req.method === 'GET' && url.pathname === '/ready') {
        const state = health()
        return sendJson(res, state.status === 'unavailable' ? 503 : 200, state)
      }

      if (req.method === 'GET' && url.pathname === '/radlib/provenance') {
        return sendJson(res, 200, provenance(options, policy, health()))
      }

      if (req.method === 'GET' && url.pathname === '/xrpc/app.bsky.feed.describeFeedGenerator') {
        return sendJson(res, 200, describeFeedGenerator(options, policy))
      }

      if (req.method === 'GET' && url.pathname === '/xrpc/app.bsky.feed.getFeedSkeleton') {
        return await getFeedSkeleton(req, res, url, options, policy, store, health())
      }

      if (req.method === 'POST' && url.pathname === '/radlib/ingest/decoded') {
        return await ingestDecoded(req, res, options, store)
      }

      return sendError(res, 404, 'NotFound', 'endpoint not found')
    } catch (err) {
      const status = typeof (err as {status?: unknown}).status === 'number' ? (err as {status: number}).status : 500
      const code = typeof (err as {code?: unknown}).code === 'string' ? (err as {code: string}).code : undefined
      const message = err instanceof Error ? err.message : 'unexpected error'
      return sendError(res, status, code ?? (status === 500 ? 'InternalServerError' : 'InvalidRequest'), message)
    }
  })

  function health(): ServiceHealth {
    const database = store.checkHealth()
    const cachedPosts = store.countCachedPosts()
    if (database === 'unavailable') {
      return {
        status: 'unavailable',
        database,
        ingestion: ingestionConfigured ? 'failed' : 'not_configured',
        cachedPosts,
        message: 'local SQLite persistence is unavailable',
      }
    }
    if (!ingestionConfigured && cachedPosts === 0) {
      return {
        status: 'unavailable',
        database,
        ingestion: 'not_configured',
        cachedPosts,
        message: 'subscribeRepos ingestion is not configured and no local cache is available',
      }
    }
    if (!ingestionConfigured) {
      return {
        status: 'degraded',
        database,
        ingestion: 'not_configured',
        cachedPosts,
        message: 'serving bounded local cache; subscribeRepos ingestion is not configured',
      }
    }
    return {
      status: 'ok',
      database,
      ingestion: 'connected',
      cachedPosts,
      message: 'service is ready',
    }
  }

  return {server, store, health}
}

async function getFeedSkeleton(
  req: IncomingMessage,
  res: ServerResponse,
  url: URL,
  options: RadlibFeedServerOptions,
  policy: ContentFilterPolicy,
  store: FeedStore,
  health: ServiceHealth,
) {
  const requestedFeed = url.searchParams.get('feed')
  if (requestedFeed !== options.feedUri) {
    return sendError(res, 400, 'InvalidRequest', 'requested feed is not served by this provider')
  }

  if (health.status === 'unavailable') {
    return sendError(res, 503, 'ProviderUnavailable', health.message)
  }

  const viewerDid = await extractViewerDidFromAuthorization(req.headers.authorization, options.auth)
  const limit = boundedLimit(url.searchParams.get('limit'))
  const offset = decodeCursor(url.searchParams.get('cursor'))
  const context = await viewerContextForRequest(options, viewerDid)
  const ranked = rankCandidates(store.listCandidates(), policy, context)
  const page = ranked.slice(offset, offset + limit)
  const nextOffset = offset + page.length
  const cursor = nextOffset < ranked.length ? encodeCursor(nextOffset) : undefined

  res.setHeader('x-radlib-provider-status', health.status)
  res.setHeader('x-radlib-algorithm', policy.algorithm)
  return sendJson(res, 200, {
    feed: page.map(item => ({post: item.post})),
    cursor,
    feedContext: JSON.stringify({
      provider: options.did,
      algorithm: policy.algorithm,
      version: VERSION,
      policyVersion: 'radlib-content-filter/1',
      rulesOnly: true,
    }),
  })
}

async function ingestDecoded(
  req: IncomingMessage,
  res: ServerResponse,
  options: RadlibFeedServerOptions,
  store: FeedStore,
) {
  if (!options.ingestToken) {
    return sendError(res, 503, 'IngestionDisabled', 'decoded ingestion endpoint is disabled')
  }
  if (req.headers['x-radlib-ingest-token'] !== options.ingestToken) {
    return sendError(res, 401, 'AuthenticationRequired', 'decoded ingestion token is required')
  }

  const body = await readJson(req)
  const result = ingestDecodedSubscribeReposEvent(store, body)
  return sendJson(res, 200, result)
}

function describeFeedGenerator(options: RadlibFeedServerOptions, policy: ContentFilterPolicy) {
  return {
    did: options.did,
    feeds: [{
      uri: options.feedUri,
      displayName: options.displayName ?? 'Radlib Filtered Feed',
      description: options.description ?? 'Rules-first self-hosted filtered feed generator.',
    }],
    links: {},
    radlib: provenance(options, policy, undefined),
  }
}

function provenance(
  options: RadlibFeedServerOptions,
  policy: ContentFilterPolicy,
  health: ServiceHealth | undefined,
) {
  return {
    service: VERSION,
    providerDid: options.did,
    feedUri: options.feedUri,
    algorithm: policy.algorithm,
    algorithmVersion: 'rules-first/1',
    scope: 'app.bsky.feed.getFeedSkeleton only',
    policy: explainPolicy(policy),
    persistence: {
      engine: 'node:sqlite',
      boundedLocalCache: true,
    },
    ingestion: {
      boundary: 'com.atproto.sync.subscribeRepos decoded commit events',
      liveFirehose: 'not claimed unless configured externally',
    },
    serviceEndpoint: options.serviceEndpoint,
    serviceFragment: options.serviceFragment ?? 'bsky_feed',
    health,
  }
}

function didDocument(options: RadlibFeedServerOptions, req: IncomingMessage) {
  const endpoint =
    options.serviceEndpoint ??
    `http://${req.headers.host ?? '127.0.0.1'}`
  const fragment = options.serviceFragment ?? 'bsky_feed'
  return {
    '@context': ['https://www.w3.org/ns/did/v1'],
    id: options.did,
    service: [
      {
        id: `#${fragment}`,
        type: 'BskyFeedGenerator',
        serviceEndpoint: endpoint,
      },
    ],
  }
}

async function viewerContextForRequest(
  options: RadlibFeedServerOptions,
  viewerDid: ViewerPolicyContext['viewerDid'],
): Promise<ViewerPolicyContext> {
  const resolved = options.viewerContext
    ? await options.viewerContext(viewerDid)
    : undefined
  return {
    viewerDid,
    // Only provider-resolved boundaries are accepted here. Client-local
    // custom terms, More/Less, and labeler policy do not cross this boundary.
    blockedAuthorDids: resolved?.blockedAuthorDids,
    blockedByAuthorDids: resolved?.blockedByAuthorDids,
    hiddenLabels: resolved?.hiddenLabels,
  }
}

function boundedLimit(value: string | null): number {
  const parsed = value ? Number.parseInt(value, 10) : 50
  if (!Number.isFinite(parsed) || parsed < 1) return 50
  return Math.min(parsed, MAX_LIMIT)
}

function encodeCursor(offset: number): string {
  return Buffer.from(JSON.stringify({v: 1, o: offset}), 'utf8').toString('base64url')
}

function decodeCursor(cursor: string | null): number {
  if (!cursor) return 0
  if (Buffer.byteLength(cursor, 'utf8') > MAX_CURSOR_BYTES) {
    const error = new Error('provider cursor is invalid or too large')
    ;(error as {status?: number}).status = 400
    throw error
  }
  try {
    const decoded = JSON.parse(Buffer.from(cursor, 'base64url').toString('utf8')) as {v?: unknown; o?: unknown}
    if (decoded.v !== 1 || typeof decoded.o !== 'number' || decoded.o < 0 || !Number.isInteger(decoded.o)) {
      throw new Error('invalid cursor payload')
    }
    return decoded.o
  } catch {
    const error = new Error('provider cursor is invalid or too large')
    ;(error as {status?: number}).status = 400
    throw error
  }
}

function sendJson(res: ServerResponse, status: number, value: unknown) {
  res.statusCode = status
  res.setHeader('content-type', 'application/json; charset=utf-8')
  res.end(JSON.stringify(value))
}

function sendError(res: ServerResponse, status: number, error: string, message: string) {
  return sendJson(res, status, {error, message})
}

async function readJson(req: IncomingMessage) {
  const chunks: Buffer[] = []
  for await (const chunk of req) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk))
    if (Buffer.concat(chunks).byteLength > 1_000_000) {
      const error = new Error('request body exceeds 1MB limit')
      ;(error as {status?: number}).status = 413
      throw error
    }
  }
  return JSON.parse(Buffer.concat(chunks).toString('utf8'))
}
