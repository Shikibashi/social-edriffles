import test from 'node:test'
import assert from 'node:assert/strict'
import {once} from 'node:events'
import {createRadlibFeedServer} from '../src/server.ts'
import {FeedStore} from '../src/store.ts'
import {extractViewerDidFromAuthorization} from '../src/auth.ts'

test('auth extraction fails closed without a verifier or dev mode', async () => {
  await assert.rejects(
    () => extractViewerDidFromAuthorization(`Bearer ${jwt('did:plc:viewer')}`),
    /verification is not configured/,
  )
})

test('auth extraction accepts unsigned JWT only in explicit dev mode', async () => {
  const did = await extractViewerDidFromAuthorization(`Bearer ${jwt('did:plc:viewer')}`, {
    acceptUnsignedDevJwt: true,
    now: new Date('2026-08-18T12:00:00.000Z'),
  })
  assert.equal(did, 'did:plc:viewer')
})

test('getFeedSkeleton is standard-shaped, authenticated, filtered, and paginated', async () => {
  const store = new FeedStore(':memory:')
  store.upsertPost({
    uri: 'at://did:plc:a/app.bsky.feed.post/one',
    authorDid: 'did:plc:a',
    text: 'ordinary hello',
    createdAt: '2026-08-18T12:00:00.000Z',
    indexedAt: '2026-08-18T12:00:00.000Z',
  })
  store.upsertPost({
    uri: 'at://did:plc:b/app.bsky.feed.post/two',
    authorDid: 'did:plc:b',
    text: 'communists organize here',
    createdAt: '2026-08-18T12:00:00.000Z',
    indexedAt: '2026-08-18T12:01:00.000Z',
  })

  const service = createRadlibFeedServer({
    did: 'did:web:feed.local',
    feedUri: 'at://did:web:feed.local/app.bsky.feed.generator/radlib',
    store,
    ingestionConfigured: true,
    auth: {
      acceptUnsignedDevJwt: true,
      now: new Date('2026-08-18T12:00:00.000Z'),
    },
    policy: {enabled: true},
  })
  service.server.listen(0)
  await once(service.server, 'listening')
  const base = address(service.server)

  const response = await fetch(`${base}/xrpc/app.bsky.feed.getFeedSkeleton?feed=${encodeURIComponent('at://did:web:feed.local/app.bsky.feed.generator/radlib')}&limit=1`, {
    headers: {authorization: `Bearer ${jwt('did:plc:viewer')}`},
  })
  const body = await response.json()

  assert.equal(response.status, 200)
  assert.deepEqual(body.feed, [{post: 'at://did:plc:a/app.bsky.feed.post/one'}])
  assert.equal(typeof body.feedContext, 'string')
  service.server.close()
  store.close()
})

test('getFeedSkeleton fails explicitly when provider cache and ingestion are unavailable', async () => {
  const service = createRadlibFeedServer({
    did: 'did:web:feed.local',
    feedUri: 'at://did:web:feed.local/app.bsky.feed.generator/radlib',
    store: new FeedStore(':memory:'),
    auth: {
      acceptUnsignedDevJwt: true,
      now: new Date('2026-08-18T12:00:00.000Z'),
    },
  })
  service.server.listen(0)
  await once(service.server, 'listening')

  const response = await fetch(`${address(service.server)}/xrpc/app.bsky.feed.getFeedSkeleton?feed=${encodeURIComponent('at://did:web:feed.local/app.bsky.feed.generator/radlib')}`, {
    headers: {authorization: `Bearer ${jwt('did:plc:viewer')}`},
  })
  const body = await response.json()
  assert.equal(response.status, 503)
  assert.equal(body.error, 'ProviderUnavailable')

  service.server.close()
  service.store.close()
})

test('getFeedSkeleton preserves auth error codes and cursor bounds', async () => {
  const store = new FeedStore(':memory:')
  store.upsertPost({
    uri: 'at://did:plc:a/app.bsky.feed.post/one',
    authorDid: 'did:plc:a',
    text: 'ordinary hello',
    createdAt: '2026-08-18T12:00:00.000Z',
    indexedAt: '2026-08-18T12:00:00.000Z',
  })
  const service = createRadlibFeedServer({
    did: 'did:web:feed.local',
    feedUri: 'at://did:web:feed.local/app.bsky.feed.generator/radlib',
    store,
    ingestionConfigured: true,
    auth: {
      acceptUnsignedDevJwt: true,
      now: new Date('2026-08-18T12:00:00.000Z'),
    },
  })
  service.server.listen(0)
  await once(service.server, 'listening')

  const noAuth = await fetch(`${address(service.server)}/xrpc/app.bsky.feed.getFeedSkeleton?feed=${encodeURIComponent('at://did:web:feed.local/app.bsky.feed.generator/radlib')}`)
  assert.equal(noAuth.status, 401)
  assert.equal((await noAuth.json()).error, 'AuthenticationRequired')

  const badCursor = await fetch(`${address(service.server)}/xrpc/app.bsky.feed.getFeedSkeleton?feed=${encodeURIComponent('at://did:web:feed.local/app.bsky.feed.generator/radlib')}&cursor=${'x'.repeat(513)}`, {
    headers: {authorization: `Bearer ${jwt('did:plc:viewer')}`},
  })
  assert.equal(badCursor.status, 400)

  service.server.close()
  store.close()
})

test('getFeedSkeleton applies selected labeler hide from request context', async () => {
  const store = new FeedStore(':memory:')
  store.upsertPost({
    uri: 'at://did:plc:a/app.bsky.feed.post/hidden',
    authorDid: 'did:plc:a',
    text: 'ordinary hidden',
    createdAt: '2026-08-18T12:00:00.000Z',
    indexedAt: '2026-08-18T12:01:00.000Z',
    labels: [{src: 'did:plc:labeler', val: 'hide-pol'}],
  })
  store.upsertPost({
    uri: 'at://did:plc:b/app.bsky.feed.post/visible',
    authorDid: 'did:plc:b',
    text: 'ordinary visible',
    createdAt: '2026-08-18T12:00:00.000Z',
    indexedAt: '2026-08-18T12:00:00.000Z',
  })
  const service = createRadlibFeedServer({
    did: 'did:web:feed.local',
    feedUri: 'at://did:web:feed.local/app.bsky.feed.generator/radlib',
    store,
    ingestionConfigured: true,
    auth: {acceptUnsignedDevJwt: true},
    viewerContext: () => ({
      viewerDid: 'did:plc:viewer',
      hiddenLabels: [{src: 'did:plc:labeler', val: 'hide-pol'}],
    }),
  })
  service.server.listen(0)
  await once(service.server, 'listening')

  const response = await fetch(`${address(service.server)}/xrpc/app.bsky.feed.getFeedSkeleton?feed=${encodeURIComponent('at://did:web:feed.local/app.bsky.feed.generator/radlib')}`, {
    headers: {authorization: `Bearer ${jwt('did:plc:viewer')}`},
  })
  const body = await response.json()
  assert.deepEqual(body.feed, [{post: 'at://did:plc:b/app.bsky.feed.post/visible'}])

  service.server.close()
  store.close()
})

test('health is explicit when firehose ingestion is absent', async () => {
  const service = createRadlibFeedServer({
    did: 'did:web:feed.local',
    feedUri: 'at://did:web:feed.local/app.bsky.feed.generator/radlib',
    store: new FeedStore(':memory:'),
  })
  service.server.listen(0)
  await once(service.server, 'listening')

  const response = await fetch(`${address(service.server)}/health`)
  const body = await response.json()
  assert.equal(response.status, 200)
  assert.equal(body.status, 'unavailable')
  assert.match(body.message, /subscribeRepos ingestion is not configured/)

  service.server.close()
  service.store.close()
})

test('standard health and DID surfaces identify the feed provider', async () => {
  const service = createRadlibFeedServer({
    did: 'did:web:feed.local',
    feedUri: 'at://did:web:feed.local/app.bsky.feed.generator/radlib',
    serviceEndpoint: 'https://feed.example',
    serviceFragment: 'bsky_feed',
    ingestionConfigured: true,
    store: new FeedStore(':memory:'),
  })
  service.server.listen(0)
  await once(service.server, 'listening')

  const health = await fetch(`${address(service.server)}/xrpc/_health`)
  assert.equal(health.status, 200)
  assert.equal((await health.json()).status, 'ok')

  const did = await fetch(`${address(service.server)}/.well-known/did.json`)
  assert.deepEqual(await did.json(), {
    '@context': ['https://www.w3.org/ns/did/v1'],
    id: 'did:web:feed.local',
    service: [{
      id: '#bsky_feed',
      type: 'BskyFeedGenerator',
      serviceEndpoint: 'https://feed.example',
    }],
  })

  service.server.close()
  service.store.close()
})

test('HTTP feed requests do not accept private ranking or filter headers', async () => {
  const store = new FeedStore(':memory:')
  store.upsertPost({
    uri: 'at://did:plc:a/app.bsky.feed.post/ordinary',
    authorDid: 'did:plc:a',
    text: 'ordinary visible',
    createdAt: '2026-08-18T12:00:00.000Z',
    indexedAt: '2026-08-18T12:00:00.000Z',
  })
  const service = createRadlibFeedServer({
    did: 'did:web:feed.local',
    feedUri: 'at://did:web:feed.local/app.bsky.feed.generator/radlib',
    store,
    ingestionConfigured: true,
    auth: {acceptUnsignedDevJwt: true},
  })
  service.server.listen(0)
  await once(service.server, 'listening')

  const response = await fetch(
    `${address(service.server)}/xrpc/app.bsky.feed.getFeedSkeleton?feed=${encodeURIComponent('at://did:web:feed.local/app.bsky.feed.generator/radlib')}`,
    {
      headers: {
        authorization: `Bearer ${jwt('did:plc:viewer')}`,
        'x-radlib-more-terms': 'ordinary',
        'x-radlib-less-terms': 'ordinary',
        'x-radlib-blocked-authors': 'did:plc:a',
      },
    },
  )
  const body = await response.json()
  assert.deepEqual(body.feed, [
    {post: 'at://did:plc:a/app.bsky.feed.post/ordinary'},
  ])

  service.server.close()
  service.store.close()
})

test('describe endpoint exposes provenance without private policy profile values', async () => {
  const service = createRadlibFeedServer({
    did: 'did:web:feed.local',
    feedUri: 'at://did:web:feed.local/app.bsky.feed.generator/radlib',
    store: new FeedStore(':memory:'),
    policy: {enabled: true, customTerms: ['private phrase']},
  })
  service.server.listen(0)
  await once(service.server, 'listening')

  const response = await fetch(`${address(service.server)}/xrpc/app.bsky.feed.describeFeedGenerator`)
  const body = await response.json()
  assert.equal(body.did, 'did:web:feed.local')
  assert.equal(body.feeds[0].uri, 'at://did:web:feed.local/app.bsky.feed.generator/radlib')
  assert.equal(JSON.stringify(body).includes('private phrase'), false)

  service.server.close()
  service.store.close()
})

test('decoded ingestion endpoint is disabled unless explicitly tokenized', async () => {
  const service = createRadlibFeedServer({
    did: 'did:web:feed.local',
    feedUri: 'at://did:web:feed.local/app.bsky.feed.generator/radlib',
    store: new FeedStore(':memory:'),
  })
  service.server.listen(0)
  await once(service.server, 'listening')

  const response = await fetch(`${address(service.server)}/radlib/ingest/decoded`, {method: 'POST'})
  const body = await response.json()
  assert.equal(response.status, 503)
  assert.equal(body.error, 'IngestionDisabled')

  service.server.close()
  service.store.close()
})

function jwt(did: string) {
  const header = Buffer.from(JSON.stringify({alg: 'none', typ: 'JWT'})).toString('base64url')
  const payload = Buffer.from(JSON.stringify({
    sub: did,
    // Keep the fixture valid independently of the wall clock used to run CI.
    exp: Math.floor(new Date('2027-08-19T12:00:00.000Z').getTime() / 1000),
  })).toString('base64url')
  return `${header}.${payload}.`
}

function address(server: import('node:http').Server) {
  const addr = server.address()
  assert.equal(typeof addr, 'object')
  assert.ok(addr)
  return `http://127.0.0.1:${addr.port}`
}
