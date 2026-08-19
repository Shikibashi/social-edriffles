import type {DecodedSubscribeReposEvent, FeedCandidate} from './types.ts'
import type {FeedStore} from './store.ts'
import {isDid} from './policy.ts'

const POST_COLLECTION = 'app.bsky.feed.post'

export type IngestionResult = {
  indexed: number
  deleted: number
  ignored: number
}

export class IngestionBoundaryError extends Error {
  code = 'IngestionBoundaryError'
}

export function ingestDecodedSubscribeReposEvent(
  store: FeedStore,
  event: DecodedSubscribeReposEvent,
  indexedAt = new Date(),
): IngestionResult {
  if (!isDid(event.repo)) throw new IngestionBoundaryError('subscribeRepos event repo is not a valid DID')
  if (!Array.isArray(event.ops)) throw new IngestionBoundaryError('subscribeRepos event ops must be an array')

  const result: IngestionResult = {indexed: 0, deleted: 0, ignored: 0}
  for (const op of event.ops) {
    const parsed = parsePath(event.repo, op.path)
    if (!parsed) {
      result.ignored += 1
      continue
    }

    if (op.action === 'delete') {
      store.deletePost(parsed.uri)
      result.deleted += 1
      continue
    }

    if (op.action !== 'create' && op.action !== 'update') {
      result.ignored += 1
      continue
    }

    const record = normalizePostRecord(op.record)
    if (!record) {
      result.ignored += 1
      continue
    }

    store.upsertPost({
      uri: parsed.uri,
      cid: op.cid,
      authorDid: event.repo,
      text: record.text,
      createdAt: record.createdAt,
      indexedAt: indexedAt.toISOString(),
      providerReason: 'subscribeRepos:indexed-post',
      labels: record.labels,
    })
    result.indexed += 1
  }
  return result
}

export function createSubscribeReposBoundary(store: FeedStore) {
  return {
    protocol: 'com.atproto.sync.subscribeRepos',
    mode: 'decoded-event-boundary',
    ingestDecodedEvent(event: DecodedSubscribeReposEvent) {
      return ingestDecodedSubscribeReposEvent(store, event)
    },
  }
}

function parsePath(repo: string, path: string): {rkey: string; uri: string} | undefined {
  const prefix = `${POST_COLLECTION}/`
  if (!path.startsWith(prefix)) return undefined
  const rkey = path.slice(prefix.length)
  if (!rkey || rkey.includes('/')) return undefined
  return {
    rkey,
    uri: `at://${repo}/${POST_COLLECTION}/${rkey}`,
  }
}

function normalizePostRecord(record: unknown): Pick<FeedCandidate, 'text' | 'createdAt' | 'labels'> | undefined {
  if (!record || typeof record !== 'object') return undefined
  const value = record as Record<string, unknown>
  if (value.$type !== POST_COLLECTION) return undefined
  if (typeof value.text !== 'string') return undefined
  const createdAt = typeof value.createdAt === 'string' ? value.createdAt : new Date(0).toISOString()
  const labels = Array.isArray(value.labels) ? value.labels as FeedCandidate['labels'] : []
  return {
    text: value.text,
    createdAt,
    labels,
  }
}
