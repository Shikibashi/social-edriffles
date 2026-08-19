import {spawn} from 'node:child_process'
import {existsSync, rmSync, writeFileSync} from 'node:fs'
import {tmpdir} from 'node:os'
import {join, resolve} from 'node:path'

const root = resolve(new URL('..', import.meta.url).pathname)
const port = 19171
const base = `http://127.0.0.1:${port}`
const did = 'did:web:radlib-feed.local'
const feedUri = `at://${did}/app.bsky.feed.generator/radlib-filtered-following`
const token = 'radlib-live-walkthrough-token'
const dbPath = join(tmpdir(), `radlib-filtered-feed-${process.pid}.sqlite`)

const results = {
  command: 'node scripts/radlib_live_filtered_feed_walkthrough.mjs',
  provider: {did, feedUri, endpoint: base},
  healthy: false,
  indexed: undefined,
  filteredFeed: undefined,
  provenance: undefined,
  unavailable: undefined,
}

let child
try {
  child = await start({
    RADLIB_FILTERED_FEED_DID: did,
    RADLIB_FILTERED_FEED_URI: feedUri,
    RADLIB_FILTERED_FEED_ENDPOINT: base,
    RADLIB_FILTERED_FEED_PORT: String(port),
    RADLIB_FILTERED_FEED_SQLITE: dbPath,
    RADLIB_FILTERED_FEED_INGESTION: 'configured',
    RADLIB_FILTERED_FEED_INGEST_TOKEN: token,
    RADLIB_CONTENT_FILTER_ENABLED: '1',
    RADLIB_CONTENT_FILTER_TERMS: 'local-only phrase',
    RADLIB_DEV_ACCEPT_UNSIGNED_VIEWER_JWT: '1',
  })

  const health = await get('/xrpc/_health')
  assert(health.status === 200 && health.body.status === 'ok', 'configured provider is healthy')
  results.healthy = true

  const ingest = await post('/radlib/ingest/decoded', {
    repo: 'did:plc:feed-walkthrough',
    ops: [
      op('neutral', 'ordinary market and technology notes'),
      op('local-only', 'a local-only phrase should be filtered'),
      op('web-app', 'a progressive web app release'),
    ],
  }, {'x-radlib-ingest-token': token})
  assert(ingest.status === 200 && ingest.body.indexed === 3, 'decoded subscribeRepos events are indexed')
  results.indexed = ingest.body

  const feed = await get(`/xrpc/app.bsky.feed.getFeedSkeleton?feed=${encodeURIComponent(feedUri)}&limit=10`, {
    authorization: `Bearer ${unsignedJwt('did:plc:viewer')}`,
  })
  const posts = feed.body.feed.map(item => item.post)
  assert(feed.status === 200, 'feed skeleton is available')
  assert(posts.some(uri => uri.endsWith('/neutral')), 'neutral candidate remains visible')
  assert(posts.some(uri => uri.endsWith('/web-app')), 'contextual false-positive protection remains visible')
  assert(!posts.some(uri => uri.endsWith('/local-only')), 'explicit provider term is filtered')
  results.filteredFeed = posts

  const provenance = await get('/radlib/provenance')
  assert(provenance.status === 200, 'provenance endpoint is available')
  results.provenance = provenance.body
} finally {
  await stop(child)
  child = undefined
}

try {
  child = await start({
    RADLIB_FILTERED_FEED_DID: did,
    RADLIB_FILTERED_FEED_URI: feedUri,
    RADLIB_FILTERED_FEED_ENDPOINT: base,
    RADLIB_FILTERED_FEED_PORT: String(port),
    RADLIB_FILTERED_FEED_SQLITE: `${dbPath}.unavailable`,
    RADLIB_DEV_ACCEPT_UNSIGNED_VIEWER_JWT: '1',
  })

  const health = await get('/xrpc/_health')
  const ready = await get('/ready')
  const feed = await get(`/xrpc/app.bsky.feed.getFeedSkeleton?feed=${encodeURIComponent(feedUri)}`, {
    authorization: `Bearer ${unsignedJwt('did:plc:viewer')}`,
  })
  assert(health.status === 503 && health.body.status === 'unavailable', 'health identifies missing ingestion')
  assert(ready.status === 503, 'readiness fails closed')
  assert(feed.status === 503 && feed.body.error === 'ProviderUnavailable', 'feed failure is explicit instead of a different-provider fallback')
  results.unavailable = {
    health: health.body,
    readinessStatus: ready.status,
    feedStatus: feed.status,
    feedError: feed.body.error,
  }
} finally {
  await stop(child)
  for (const path of [dbPath, `${dbPath}-wal`, `${dbPath}-shm`, `${dbPath}.unavailable`, `${dbPath}.unavailable-wal`, `${dbPath}.unavailable-shm`]) {
    if (existsSync(path)) rmSync(path, {force: true})
  }
}

writeFileSync(
  join(root, 'artifacts/radlib-live-filtered-feed-walkthrough.json'),
  `${JSON.stringify(results, null, 2)}\n`,
)
process.stdout.write(`${JSON.stringify(results, null, 2)}\n`)

function op(rkey, text) {
  return {
    action: 'create',
    path: `app.bsky.feed.post/${rkey}`,
    cid: `bafy${'a'.repeat(50)}`,
    record: {
      $type: 'app.bsky.feed.post',
      text,
      createdAt: '2026-08-18T12:00:00.000Z',
    },
  }
}

function unsignedJwt(sub) {
  const encode = value => Buffer.from(JSON.stringify(value)).toString('base64url')
  return `${encode({alg: 'none', typ: 'JWT'})}.${encode({sub, iat: 1, exp: 4_000_000_000})}.`
}

async function start(extraEnv) {
  const processHandle = spawn(process.execPath, ['services/radlib-filtered-feed/src/index.ts'], {
    cwd: root,
    env: {...process.env, ...extraEnv},
    stdio: ['ignore', 'pipe', 'pipe'],
  })
  let output = ''
  processHandle.stdout.on('data', chunk => {
    output += String(chunk)
  })
  processHandle.stderr.on('data', chunk => {
    output += String(chunk)
  })
  const deadline = Date.now() + 10_000
  while (Date.now() < deadline) {
    try {
      await fetch(`${base}/health`)
      return processHandle
    } catch {
      if (processHandle.exitCode !== null) {
        throw new Error(`filtered feed exited before readiness: ${output}`)
      }
      await new Promise(resolveWait => setTimeout(resolveWait, 100))
    }
  }
  throw new Error(`timed out waiting for filtered feed: ${output}`)
}

async function stop(processHandle) {
  if (!processHandle || processHandle.exitCode !== null) return
  processHandle.kill('SIGTERM')
  await new Promise((resolveExit, rejectExit) => {
    const timer = setTimeout(() => {
      processHandle.kill('SIGKILL')
      rejectExit(new Error('filtered feed did not stop after SIGTERM'))
    }, 5_000)
    processHandle.once('exit', () => {
      clearTimeout(timer)
      resolveExit()
    })
  })
}

async function get(path, headers = {}) {
  const response = await fetch(`${base}${path}`, {headers})
  return {status: response.status, body: await response.json()}
}

async function post(path, body, headers = {}) {
  const response = await fetch(`${base}${path}`, {
    method: 'POST',
    headers: {'content-type': 'application/json', ...headers},
    body: JSON.stringify(body),
  })
  return {status: response.status, body: await response.json()}
}

function assert(condition, message) {
  if (!condition) throw new Error(message)
}
