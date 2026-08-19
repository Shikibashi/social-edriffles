import test from 'node:test'
import assert from 'node:assert/strict'
import {FeedStore} from '../src/store.ts'
import {ingestDecodedSubscribeReposEvent} from '../src/ingest.ts'

test('SQLite store persists, bounds, prunes, and deletes posts', () => {
  const store = new FeedStore(':memory:', {
    maxPosts: 2,
    ttlMs: 60_000,
    now: () => new Date('2026-08-18T12:00:00.000Z'),
  })

  store.upsertPost(post('old', '2026-08-18T11:58:00.000Z'))
  store.upsertPost(post('one', '2026-08-18T11:59:00.000Z'))
  store.upsertPost(post('two', '2026-08-18T12:00:00.000Z'))

  assert.deepEqual(store.listCandidates().map(candidate => candidate.uri), [
    'at://did:plc:a/app.bsky.feed.post/two',
    'at://did:plc:a/app.bsky.feed.post/one',
  ])

  store.deletePost('at://did:plc:a/app.bsky.feed.post/two')
  assert.equal(store.countCachedPosts(), 1)
  store.close()
})

test('decoded subscribeRepos boundary indexes posts and ignores other records', () => {
  const store = new FeedStore(':memory:')
  const result = ingestDecodedSubscribeReposEvent(store, {
    repo: 'did:plc:alice',
    ops: [{
      action: 'create',
      path: 'app.bsky.feed.post/abc',
      cid: 'bafy-post',
      record: {
        $type: 'app.bsky.feed.post',
        text: 'hello network',
        createdAt: '2026-08-18T12:00:00.000Z',
      },
    }, {
      action: 'create',
      path: 'app.bsky.graph.follow/abc',
      record: {$type: 'app.bsky.graph.follow'},
    }],
  }, new Date('2026-08-18T12:01:00.000Z'))

  assert.deepEqual(result, {indexed: 1, deleted: 0, ignored: 1})
  assert.equal(store.listCandidates()[0]?.uri, 'at://did:plc:alice/app.bsky.feed.post/abc')
  store.close()
})

test('decoded subscribeRepos boundary handles delete operations', () => {
  const store = new FeedStore(':memory:')
  ingestDecodedSubscribeReposEvent(store, {
    repo: 'did:plc:alice',
    ops: [{
      action: 'create',
      path: 'app.bsky.feed.post/abc',
      record: {
        $type: 'app.bsky.feed.post',
        text: 'hello',
        createdAt: '2026-08-18T12:00:00.000Z',
      },
    }],
  })
  ingestDecodedSubscribeReposEvent(store, {
    repo: 'did:plc:alice',
    ops: [{
      action: 'delete',
      path: 'app.bsky.feed.post/abc',
    }],
  })

  assert.equal(store.countCachedPosts(), 0)
  store.close()
})

function post(rkey: string, indexedAt: string) {
  return {
    uri: `at://did:plc:a/app.bsky.feed.post/${rkey}`,
    authorDid: 'did:plc:a' as const,
    text: rkey,
    createdAt: indexedAt,
    indexedAt,
  }
}
