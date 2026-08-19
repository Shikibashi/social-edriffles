export type Did = `did:${string}:${string}`

export type FeedAlgorithm = 'contextual' | 'strict'

/** Opaque legacy identifier; the provider does not ship or evaluate packs. */
export type TermPack = string

export type ContentFilterPolicy = {
  version: 1
  enabled: boolean
  algorithm: FeedAlgorithm
  termPacks: TermPack[]
  customTerms: string[]
  excludedAuthorDids: Did[]
  hardExclude: true
  actorTarget: 'all'
  semanticMode: 'rules-only'
}

export type FeedCandidate = {
  uri: string
  cid?: string
  authorDid: Did
  text: string
  createdAt: string
  indexedAt: string
  providerReason?: string
  labels?: Array<{
    src: Did
    val: string
  }>
}

export type ViewerPolicyContext = {
  viewerDid: Did
  blockedAuthorDids?: Did[]
  blockedByAuthorDids?: Did[]
  hiddenLabels?: Array<{
    src: Did
    val: string
  }>
  lessTerms?: string[]
  moreTerms?: string[]
  now?: Date
}

export type ExclusionCode =
  | 'relationship-hard-block'
  | 'incoming-hard-block'
  | 'selected-labeler-hide'
  | 'explicit-author-exclusion'
  | 'content-filter-hard-exclusion'

export type CandidateTrace = {
  uri: string
  included: boolean
  rankScore?: number
  rankSignals: string[]
  exclusion?: {
    code: ExclusionCode
    detail: string
  }
}

export type RankedFeedItem = {
  post: string
  trace: CandidateTrace
}

export type SubscribeReposOperation = {
  action: 'create' | 'update' | 'delete'
  path: string
  cid?: string
  record?: unknown
}

export type DecodedSubscribeReposEvent = {
  seq?: number
  repo: Did
  ops: SubscribeReposOperation[]
}

export type HealthState =
  | 'ok'
  | 'degraded'
  | 'unavailable'

export type ServiceHealth = {
  status: HealthState
  database: 'ok' | 'unavailable'
  ingestion: 'connected' | 'not_configured' | 'failed'
  cachedPosts: number
  message: string
}
