import {
  fetchPostMetadata,
  parsePostRoute,
  renderPostMetadata,
} from './post-metadata.ts'

const PDS_EXACT_PATHS = new Set([
  '/oauth/authorize',
  '/oauth/authorize/redirect',
  '/oauth/jwks',
  '/oauth/par',
  '/oauth/revoke',
  '/oauth/token',
])

const OAUTH_PROVIDER_PATH_PREFIX = '/@atproto/oauth-provider/'
const CANONICAL_PUBLIC_HOST = 'social.edriffles.us'
const LEGACY_PUBLIC_HOST = 'radlib.edriffles.us'
const OAUTH_ISSUER_HOST = 'radlib.edriffles.us'
const LEGACY_PDS_HOST = 'pds.edriffles.us'
const CANONICAL_PUBLIC_ORIGIN = `https://${CANONICAL_PUBLIC_HOST}`
const OAUTH_ISSUER_ORIGIN = `https://${OAUTH_ISSUER_HOST}`
const LEGACY_PDS_ORIGIN = `https://${LEGACY_PDS_HOST}`
const DEFAULT_APPVIEW_ORIGIN = 'https://api.bsky.app'
const PUBLIC_PROTOCOL_HOSTS = new Set([
  CANONICAL_PUBLIC_HOST,
  OAUTH_ISSUER_HOST,
  LEGACY_PDS_HOST,
])

type ProtectedResourceMetadata = {
  resource: string
  authorization_servers: string[]
  scopes_supported: string[]
  bearer_methods_supported: string[]
  resource_documentation: string
}

type EdgeEnv = Env & {
  APPVIEW_ORIGIN?: string
}

/**
 * Select the public origin the upstream PDS should use for URL-bound auth.
 * OAuth issuer routes remain Radlib; account/PDS resource routes remain on the
 * owner's pds.edriffles.us endpoint.
 */
function upstreamPublicHost(incomingUrl: URL, env: Env): string {
  if (
    isPdsPath(incomingUrl.pathname) &&
    incomingUrl.hostname !== OAUTH_ISSUER_HOST &&
    incomingUrl.pathname !== '/.well-known/did.json'
  ) {
    return env.PDS_PUBLIC_HOST
  }
  return env.PUBLIC_HOST
}

/**
 * Keep the former public URL usable as a compatibility entry point while the
 * user-facing OAuth client and callback live on social.edriffles.us. Protocol
 * paths remain on radlib.edriffles.us because that is the configured PDS/OAuth
 * issuer; web paths redirect to the user-facing origin.
 */
export function redirectLegacyPublicHost(incomingUrl: URL): Response | undefined {
  if (incomingUrl.hostname !== LEGACY_PUBLIC_HOST) return
  if (isPdsPath(incomingUrl.pathname)) return

  const target = new URL(incomingUrl.toString())
  target.protocol = 'https:'
  target.hostname = CANONICAL_PUBLIC_HOST
  target.port = ''
  return Response.redirect(target, 308)
}

/**
 * The public contract is one origin. The SPA owns the root and callback, while
 * the PDS owns protocol and XRPC paths. Keep this list explicit so a new
 * browser route cannot accidentally expose the PDS or an OAuth endpoint.
 */
export function isPdsPath(pathname: string): boolean {
  if (
    pathname === '/xrpc' ||
    pathname.startsWith('/xrpc/') ||
    pathname === '/_health' ||
    pathname.startsWith('/_health/') ||
    pathname === '/.well-known' ||
    pathname.startsWith('/.well-known/')
  ) {
    return true
  }

  if (PDS_EXACT_PATHS.has(pathname)) return true

  // The authorization page is a PDS-owned UI. Its bundled assets and the
  // same-origin sign-in/consent API share this prefix; sending only
  // /oauth/* to the PDS would load the page shell but route its login POST to
  // the static web app.
  if (pathname.startsWith(OAUTH_PROVIDER_PATH_PREFIX)) return true

  return (
    pathname.startsWith('/oauth/') &&
    pathname !== '/oauth/callback' &&
    !pathname.startsWith('/oauth/callback/')
  )
}

/**
 * The owner's existing PLC DID still declares pds.edriffles.us as its PDS.
 * Keep that identity declaration usable while also allowing the user-facing
 * web origin to be used as a protocol alias. The authorization server remains
 * radlib.edriffles.us, the configured PDS OAuth issuer.
 */
export function protectedResourceMetadataForHost(
  hostname: string,
): ProtectedResourceMetadata | undefined {
  const normalizedHostname = hostname.toLowerCase()
  const resource =
    normalizedHostname === CANONICAL_PUBLIC_HOST
      ? CANONICAL_PUBLIC_ORIGIN
      : normalizedHostname === LEGACY_PDS_HOST
        ? LEGACY_PDS_ORIGIN
        : undefined

  if (!resource) return

  return {
    resource,
    authorization_servers: [OAUTH_ISSUER_ORIGIN],
    scopes_supported: [],
    bearer_methods_supported: ['header'],
    resource_documentation: 'https://atproto.com',
  }
}

function publicPdsProtectedResourceMetadata(
  incomingUrl: URL,
): Response | undefined {
  if (incomingUrl.pathname !== '/.well-known/oauth-protected-resource') {
    return
  }

  const metadata = protectedResourceMetadataForHost(incomingUrl.hostname)
  if (!metadata) return

  return new Response(
    JSON.stringify(metadata),
    {
      status: 200,
      headers: {
        'access-control-allow-headers': '*',
        'access-control-allow-method': '*',
        'access-control-allow-origin': '*',
        'cache-control': 'no-store',
        'content-type': 'application/json',
      },
    },
  )
}

/**
 * The configured OAuth issuer must explicitly list every public resource alias
 * that can return the issuer metadata. This lets an OAuth client validate the
 * resource-to-issuer relationship without changing the PDS issuer identity.
 */
async function proxyAuthorizationServerMetadata(
  request: Request,
  origin: string,
  incomingUrl: URL,
  publicHost: string,
): Promise<Response> {
  const response = await proxy(request, origin, incomingUrl, publicHost)
  if (response.status !== 200) return response

  const contentType = response.headers.get('content-type') ?? ''
  if (!contentType.includes('application/json')) return response

  const metadata = (await response.json()) as {
    protected_resources?: string[]
  }
  const protectedResources = new Set(metadata.protected_resources ?? [])
  protectedResources.add(CANONICAL_PUBLIC_ORIGIN)
  protectedResources.add(OAUTH_ISSUER_ORIGIN)
  protectedResources.add(LEGACY_PDS_ORIGIN)

  const headers = new Headers(response.headers)
  headers.delete('etag')
  headers.delete('content-length')
  headers.set('content-type', 'application/json')
  return new Response(
    JSON.stringify({
      ...metadata,
      protected_resources: [...protectedResources],
    }),
    {
      status: response.status,
      statusText: response.statusText,
      headers,
    },
  )
}

function buildUpstreamRequest(
  request: Request,
  incomingUrl: URL,
  origin: string,
  publicHost: string,
): Request {
  const upstreamUrl = new URL(origin)
  if (upstreamUrl.protocol !== 'https:') {
    throw new Error('Configured upstream origins must use HTTPS')
  }
  // Keep a small public health alias while using the PDS's actual XRPC health
  // route upstream.
  upstreamUrl.pathname =
    incomingUrl.pathname === '/_health'
      ? '/xrpc/_health'
      : incomingUrl.pathname
  upstreamUrl.search = incomingUrl.search

  const headers = new Headers(request.headers)
  // The upstream host is selected by fixed environment variables. Do not
  // forward a caller-controlled Host header; preserve the configured public
  // origin for trusted reverse-proxy-aware PDS deployments.
  headers.delete('host')
  if (!/^[a-z0-9.-]+$/i.test(publicHost)) {
    throw new Error('Configured public host is invalid')
  }
  headers.set('x-forwarded-host', publicHost)
  headers.set('x-forwarded-proto', incomingUrl.protocol.slice(0, -1))

  const init: RequestInit = {
    method: request.method,
    headers,
    redirect: 'manual',
  }
  if (request.method !== 'GET' && request.method !== 'HEAD') {
    init.body = request.body
  }

  return new Request(upstreamUrl, init)
}

async function proxy(
  request: Request,
  origin: string,
  incomingUrl: URL,
  publicHost: string,
): Promise<Response> {
  const upstream = await fetch(
    buildUpstreamRequest(request, incomingUrl, origin, publicHost),
  )
  // Cloudflare Workers expose the upgraded peer on the Response.webSocket
  // property. Re-wrapping a 101 response in a new Response drops that peer,
  // which makes the PDS firehose look offline to relays even though ordinary
  // HTTP/XRPC requests still work.
  if (request.headers.get('upgrade')?.toLowerCase() === 'websocket') {
    return upstream
  }
  return new Response(upstream.body, {
    status: upstream.status,
    statusText: upstream.statusText,
    headers: new Headers(upstream.headers),
  })
}

async function proxyPublicPostPage(
  request: Request,
  incomingUrl: URL,
  env: EdgeEnv,
): Promise<Response> {
  const response = await proxy(
    request,
    env.WEB_ORIGIN,
    incomingUrl,
    upstreamPublicHost(incomingUrl, env),
  )
  const contentType = response.headers.get('content-type') ?? ''
  if (!contentType.toLowerCase().includes('text/html')) return response

  const route = parsePostRoute(incomingUrl.pathname)
  if (!route) return response

  const metadata = await fetchPostMetadata(
    route,
    env.APPVIEW_ORIGIN ?? DEFAULT_APPVIEW_ORIGIN,
  )
  if (!metadata) return response

  const html = await response.text()
  const canonicalUrl = new URL(incomingUrl.toString())
  canonicalUrl.search = ''
  canonicalUrl.hash = ''

  const headers = new Headers(response.headers)
  headers.delete('content-encoding')
  headers.delete('content-length')
  headers.delete('etag')
  headers.set('cache-control', 'public, max-age=60, s-maxage=300')
  headers.set('content-type', 'text/html; charset=utf-8')

  return new Response(
    renderPostMetadata(html, metadata, canonicalUrl.toString()),
    {
      status: response.status,
      statusText: response.statusText,
      headers,
    },
  )
}

export default {
  async fetch(request: Request, env: EdgeEnv): Promise<Response> {
    const incomingUrl = new URL(request.url)

    const legacyRedirect = redirectLegacyPublicHost(incomingUrl)
    if (legacyRedirect) return legacyRedirect

    const legacyResourceMetadata = publicPdsProtectedResourceMetadata(incomingUrl)
    if (legacyResourceMetadata) return legacyResourceMetadata

    const origin = isPdsPath(incomingUrl.pathname)
      ? env.PDS_ORIGIN
      : env.WEB_ORIGIN

    try {
      if (
        incomingUrl.pathname === '/.well-known/oauth-authorization-server' &&
        PUBLIC_PROTOCOL_HOSTS.has(incomingUrl.hostname)
      ) {
        return await proxyAuthorizationServerMetadata(
          request,
          origin,
          incomingUrl,
          upstreamPublicHost(incomingUrl, env),
        )
      }
      if (
        request.method === 'GET' &&
        incomingUrl.hostname === CANONICAL_PUBLIC_HOST &&
        parsePostRoute(incomingUrl.pathname)
      ) {
        return await proxyPublicPostPage(request, incomingUrl, env)
      }
      return await proxy(
        request,
        origin,
        incomingUrl,
        upstreamPublicHost(incomingUrl, env),
      )
    } catch (error) {
      console.error(
        JSON.stringify({
          message: 'radlib upstream request failed',
          upstream: isPdsPath(incomingUrl.pathname) ? 'pds' : 'web',
          pathname: incomingUrl.pathname,
          error: error instanceof Error ? error.message : String(error),
        }),
      )
      return new Response('Upstream unavailable', {status: 502})
    }
  },
} satisfies ExportedHandler<EdgeEnv>
