import type {Did} from './types.ts'
import {isDid} from './policy.ts'

export type VerifiedViewer = {
  did: Did
  issuer?: string
  audience?: string | string[]
}

export type ViewerJwtVerifier = (jwt: string) => Promise<VerifiedViewer> | VerifiedViewer

export type AuthOptions = {
  verifier?: ViewerJwtVerifier
  acceptUnsignedDevJwt?: boolean
  now?: Date
}

export class AuthError extends Error {
  status = 401
  code = 'AuthenticationRequired'
}

export async function extractViewerDidFromAuthorization(
  authorization: string | undefined,
  options: AuthOptions = {},
): Promise<Did> {
  if (!authorization?.startsWith('Bearer ')) {
    throw new AuthError('viewer authorization bearer token is required')
  }

  const token = authorization.slice('Bearer '.length).trim()
  if (!token) throw new AuthError('viewer authorization bearer token is empty')

  if (options.verifier) {
    const verified = await options.verifier(token)
    if (!isDid(verified.did)) throw new AuthError('verified viewer DID is invalid')
    return verified.did
  }

  if (!options.acceptUnsignedDevJwt) {
    throw new AuthError('viewer JWT signature verification is not configured')
  }

  const payload = decodeJwtPayload(token)
  const did = payload.sub ?? payload.iss
  if (typeof did !== 'string' || !isDid(did)) {
    throw new AuthError('viewer JWT does not contain a valid DID subject')
  }

  assertTimeClaims(payload, options.now ?? new Date())
  return did
}

function decodeJwtPayload(token: string): Record<string, unknown> {
  const parts = token.split('.')
  if (parts.length < 2) throw new AuthError('viewer JWT is malformed')

  try {
    return JSON.parse(Buffer.from(parts[1], 'base64url').toString('utf8')) as Record<string, unknown>
  } catch {
    throw new AuthError('viewer JWT payload is malformed')
  }
}

function assertTimeClaims(payload: Record<string, unknown>, now: Date) {
  const nowSeconds = Math.floor(now.getTime() / 1000)
  if (typeof payload.exp === 'number' && payload.exp <= nowSeconds) {
    throw new AuthError('viewer JWT is expired')
  }
  if (typeof payload.nbf === 'number' && payload.nbf > nowSeconds) {
    throw new AuthError('viewer JWT is not active yet')
  }
}
