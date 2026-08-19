import {DatabaseSync} from 'node:sqlite'
import type {FeedCandidate} from './types.ts'

export type FeedStoreOptions = {
  maxPosts?: number
  ttlMs?: number
  now?: () => Date
}

export class FeedStore {
  private db: DatabaseSync
  private maxPosts: number
  private ttlMs: number
  private now: () => Date

  constructor(path = ':memory:', options: FeedStoreOptions = {}) {
    this.db = new DatabaseSync(path)
    this.maxPosts = options.maxPosts ?? 50_000
    this.ttlMs = options.ttlMs ?? 48 * 60 * 60 * 1000
    this.now = options.now ?? (() => new Date())
    this.init()
  }

  close() {
    this.db.close()
  }

  upsertPost(candidate: FeedCandidate) {
    this.db.prepare(`
      INSERT INTO posts (uri, cid, author_did, text, created_at, indexed_at, provider_reason, labels_json, deleted)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
      ON CONFLICT(uri) DO UPDATE SET
        cid = excluded.cid,
        author_did = excluded.author_did,
        text = excluded.text,
        created_at = excluded.created_at,
        indexed_at = excluded.indexed_at,
        provider_reason = excluded.provider_reason,
        labels_json = excluded.labels_json,
        deleted = 0
    `).run(
      candidate.uri,
      candidate.cid ?? null,
      candidate.authorDid,
      candidate.text,
      candidate.createdAt,
      candidate.indexedAt,
      candidate.providerReason ?? null,
      JSON.stringify(candidate.labels ?? []),
    )
    this.prune()
  }

  deletePost(uri: string) {
    this.db.prepare(`
      INSERT INTO posts (uri, author_did, text, created_at, indexed_at, deleted)
      VALUES (?, 'did:radlib:deleted', '', ?, ?, 1)
      ON CONFLICT(uri) DO UPDATE SET deleted = 1, indexed_at = excluded.indexed_at
    `).run(uri, this.now().toISOString(), this.now().toISOString())
    this.prune()
  }

  listCandidates(): FeedCandidate[] {
    const rows = this.db.prepare(`
      SELECT uri, cid, author_did, text, created_at, indexed_at, provider_reason, labels_json
      FROM posts
      WHERE deleted = 0
      ORDER BY indexed_at DESC, uri ASC
      LIMIT ?
    `).all(this.maxPosts) as Array<Record<string, unknown>>

    return rows.map(row => ({
      uri: String(row.uri),
      cid: row.cid ? String(row.cid) : undefined,
      authorDid: String(row.author_did) as FeedCandidate['authorDid'],
      text: String(row.text),
      createdAt: String(row.created_at),
      indexedAt: String(row.indexed_at),
      providerReason: row.provider_reason ? String(row.provider_reason) : undefined,
      labels: parseLabels(row.labels_json),
    }))
  }

  countCachedPosts(): number {
    const row = this.db.prepare('SELECT COUNT(*) AS count FROM posts WHERE deleted = 0').get() as {count: number}
    return row.count
  }

  checkHealth(): 'ok' | 'unavailable' {
    try {
      this.db.prepare('SELECT 1').get()
      return 'ok'
    } catch {
      return 'unavailable'
    }
  }

  private init() {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS posts (
        uri TEXT PRIMARY KEY,
        cid TEXT,
        author_did TEXT NOT NULL,
        text TEXT NOT NULL,
        created_at TEXT NOT NULL,
        indexed_at TEXT NOT NULL,
        provider_reason TEXT,
        labels_json TEXT NOT NULL DEFAULT '[]',
        deleted INTEGER NOT NULL DEFAULT 0
      );
      CREATE INDEX IF NOT EXISTS posts_active_indexed_at_idx ON posts (deleted, indexed_at DESC);
      CREATE INDEX IF NOT EXISTS posts_author_idx ON posts (author_did);
    `)
  }

  private prune() {
    const cutoff = new Date(this.now().getTime() - this.ttlMs).toISOString()
    this.db.prepare('DELETE FROM posts WHERE indexed_at < ?').run(cutoff)
    this.db.prepare(`
      DELETE FROM posts
      WHERE uri NOT IN (
        SELECT uri FROM posts ORDER BY indexed_at DESC, uri ASC LIMIT ?
      )
    `).run(this.maxPosts)
  }
}

function parseLabels(value: unknown): FeedCandidate['labels'] {
  if (typeof value !== 'string') return []
  try {
    const parsed = JSON.parse(value)
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}
