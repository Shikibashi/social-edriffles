import type {
  CandidateTrace,
  ContentFilterPolicy,
  Did,
  ExclusionCode,
  FeedCandidate,
  RankedFeedItem,
  ViewerPolicyContext,
} from './types.ts'

const DID_RE = /^did:[a-z0-9]+:[A-Za-z0-9._:%-]+$/

export const DEFAULT_CONTENT_FILTER_POLICY: ContentFilterPolicy = {
  version: 1,
  enabled: false,
  algorithm: 'contextual',
  // New viewers get a neutral provider policy. Legacy pack fields are accepted
  // for interoperability but do not carry any provider vocabulary.
  termPacks: [],
  customTerms: [],
  excludedAuthorDids: [],
  hardExclude: true,
  actorTarget: 'all',
  semanticMode: 'rules-only',
}

export function isDid(value: string): value is Did {
  return DID_RE.test(value)
}

export function normalizePolicy(input?: Partial<ContentFilterPolicy>): ContentFilterPolicy {
  const raw = {
    ...DEFAULT_CONTENT_FILTER_POLICY,
    ...(input ?? {}),
  }

  const requestedTermPacks = input?.termPacks ?? DEFAULT_CONTENT_FILTER_POLICY.termPacks
  const termPacks = uniqueStrings(requestedTermPacks).slice(0, 100)

  return {
    version: 1,
    enabled: Boolean(raw.enabled),
    algorithm: raw.algorithm === 'strict' ? 'strict' : 'contextual',
    termPacks: Array.from(new Set(termPacks)),
    customTerms: uniqueStrings(raw.customTerms).slice(0, 200),
    excludedAuthorDids: uniqueStrings(raw.excludedAuthorDids).filter(isDid).slice(0, 1000),
    hardExclude: true,
    actorTarget: 'all',
    semanticMode: 'rules-only',
  }
}

export function activeTerms(policy: ContentFilterPolicy): string[] {
  // Only terms explicitly supplied for this viewer are evaluated. This keeps
  // provider policy neutral and makes the provenance honest.
  return uniqueStrings(policy.customTerms.map(normalizeTerm).filter(Boolean))
}

export function evaluateCandidate(
  candidate: FeedCandidate,
  policyInput: ContentFilterPolicy,
  context: ViewerPolicyContext,
): CandidateTrace {
  const policy = normalizePolicy(policyInput)
  const rankSignals: string[] = []

  if (context.blockedAuthorDids?.includes(candidate.authorDid)) {
    return excludedTrace(candidate, 'relationship-hard-block', 'viewer directly blocks this author')
  }

  if (context.blockedByAuthorDids?.includes(candidate.authorDid)) {
    return excludedTrace(candidate, 'incoming-hard-block', 'candidate author blocks the viewer')
  }

  const hiddenLabel = findHiddenLabel(candidate, context)
  if (hiddenLabel) {
    return excludedTrace(
      candidate,
      'selected-labeler-hide',
      `selected labeler ${hiddenLabel.src} hides ${hiddenLabel.val}`,
    )
  }

  if (policy.enabled && policy.excludedAuthorDids.includes(candidate.authorDid)) {
    return excludedTrace(candidate, 'explicit-author-exclusion', `viewer excluded author ${candidate.authorDid}`)
  }

  if (policy.enabled) {
    const match = matchAnyTerm(candidate.text, activeTerms(policy))
    if (match) {
      return excludedTrace(candidate, 'content-filter-hard-exclusion', `matched policy term: ${match}`)
    }
  }

  const ageHours = ageInHours(candidate.createdAt, context.now ?? new Date())
  let score = Math.max(0, 100 - ageHours)
  rankSignals.push('freshness')

  if (candidate.providerReason) {
    score += 5
    rankSignals.push(`provider-reason:${safeReason(candidate.providerReason)}`)
  }

  const less = matchAnyTerm(candidate.text, context.lessTerms ?? [])
  if (less) {
    score -= 1000
    rankSignals.push(`explicit-less:${less}`)
  }

  const more = matchAnyTerm(candidate.text, context.moreTerms ?? [])
  if (more) {
    score += 25
    rankSignals.push(`explicit-more:${more}`)
  }

  return {
    uri: candidate.uri,
    included: true,
    rankScore: score,
    rankSignals,
  }
}

export function rankCandidates(
  candidates: FeedCandidate[],
  policyInput: ContentFilterPolicy,
  context: ViewerPolicyContext,
): RankedFeedItem[] {
  return candidates
    .map(candidate => ({
      post: candidate.uri,
      trace: evaluateCandidate(candidate, policyInput, context),
    }))
    .filter(item => item.trace.included)
    .sort((a, b) => {
      const scoreDelta = (b.trace.rankScore ?? 0) - (a.trace.rankScore ?? 0)
      if (scoreDelta !== 0) return scoreDelta
      return a.post.localeCompare(b.post)
    })
}

export function explainPolicy(policyInput: ContentFilterPolicy): Record<string, unknown> {
  const policy = normalizePolicy(policyInput)
  return {
    policyVersion: 'radlib-content-filter/1',
    enabled: policy.enabled,
    algorithm: policy.algorithm,
    semanticMode: policy.semanticMode,
    hardExcludePrecedence: [
      'protocol hard blocks',
      'selected labeler hide',
      'explicit author exclusion',
      'rules-first content filter',
      'explicit Less demotion',
      'provider/freshness ranking',
      'explicit More boost among survivors',
    ],
    termPacks: policy.termPacks,
    legacyTermPacksIgnored: policy.termPacks.length > 0,
    strictProgressiveStandaloneTerms: false,
  }
}

export function matchAnyTerm(text: string, terms: string[]): string | undefined {
  const normalized = normalizeText(text)
  for (const term of terms) {
    const normalizedTerm = normalizeTerm(term)
    if (!normalizedTerm) continue
    if (termMatches(normalized, normalizedTerm)) return normalizedTerm
  }
  return undefined
}

function excludedTrace(
  candidate: FeedCandidate,
  code: ExclusionCode,
  detail: string,
): CandidateTrace {
  return {
    uri: candidate.uri,
    included: false,
    rankSignals: [],
    exclusion: {code, detail},
  }
}

function findHiddenLabel(candidate: FeedCandidate, context: ViewerPolicyContext) {
  for (const label of candidate.labels ?? []) {
    if (context.hiddenLabels?.some(hidden => hidden.src === label.src && hidden.val === label.val)) {
      return label
    }
  }
  return undefined
}

function normalizeText(text: string): string {
  return text
    .normalize('NFKC')
    .toLocaleLowerCase('en-US')
    .replace(/[\u2018\u2019]/g, "'")
    .replace(/[‐‑‒–—−]/gu, ' ')
    .replace(/[^\p{Letter}\p{Number}'-]+/gu, ' ')
    .replace(/\s+/g, ' ')
    .trim()
}

function normalizeTerm(term: string): string {
  return normalizeText(term)
}

function termMatches(normalizedText: string, normalizedTerm: string): boolean {
  const escaped = normalizedTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  return new RegExp(`(^|[\\s])${escaped}($|[\\s])`, 'u').test(normalizedText)
}

function uniqueStrings(values: readonly string[]): string[] {
  return Array.from(new Set(values.map(value => value.trim()).filter(Boolean)))
}

function ageInHours(createdAt: string, now: Date): number {
  const created = Date.parse(createdAt)
  if (!Number.isFinite(created)) return 24 * 365
  return Math.max(0, (now.getTime() - created) / 3_600_000)
}

function safeReason(reason: string): string {
  return reason.replace(/[^\p{Letter}\p{Number}:_. -]+/gu, '').slice(0, 80)
}
