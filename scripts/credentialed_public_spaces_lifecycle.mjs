#!/usr/bin/env node

/**
 * Exercise the deployed, disposable Radlib Spaces boundary.
 *
 * This is intentionally guarded twice: the caller must opt in explicitly and
 * the target must remain the disposable pds.edriffles.us alias. Credentials
 * exist only in memory for this process and the optional receipt contains only
 * status codes, error names, and source/deployment bindings.
 */

import { randomBytes } from 'node:crypto'
import { writeFile } from 'node:fs/promises'

import { Client } from '../upstream/atproto-pds/packages/lex/lex-client/dist/index.js'
import { com } from '../upstream/atproto-pds/packages/pds/dist/lexicons/index.js'
import { JoseKey } from '../upstream/atproto-pds/packages/oauth/jwk-jose/dist/index.js'
import { createDpopProof } from '../upstream/atproto-pds/packages/space/dist/index.js'

const PDS_ORIGIN = process.env.RADLIB_DISPOSABLE_PDS_ORIGIN ?? 'https://pds.edriffles.us'
const OUTPUT_PATH = process.env.RADLIB_PUBLIC_SPACES_RECEIPT ?? ''
const SOURCE_REVISION = process.env.RADLIB_SOURCE_REVISION ?? 'unknown'
const SOURCE_DIGEST = process.env.RADLIB_SOURCE_DIGEST ?? 'unknown'
const DEPLOYMENT_IMAGE = process.env.RADLIB_PDS_DEPLOYMENT_IMAGE ?? 'unknown'
const PROBED_AT = new Date().toISOString()

const assertSafeTarget = () => {
  const url = new URL(PDS_ORIGIN)
  if (url.protocol !== 'https:' || url.hostname !== 'pds.edriffles.us') {
    throw new Error('refusing to run against a non-disposable PDS target')
  }
  if (process.env.RADLIB_CONFIRM_DISPOSABLE_TEST !== '1') {
    throw new Error('set RADLIB_CONFIRM_DISPOSABLE_TEST=1 to run the disposable test')
  }
}

const errorName = (error) => {
  const code = String(error?.error ?? error?.name ?? 'Error')
  const message = String(error?.message ?? '')
  if (!message || /(token|password|secret|credential|authorization|bearer|dpop|jwt)/i.test(message)) {
    return code
  }
  return `${code}:${message.slice(0, 160)}`
}

const capture = async (action) => {
  try {
    return { ok: true, value: await action() }
  } catch (error) {
    return { ok: false, error: errorName(error) }
  }
}

const requestJson = async (path, options = {}) => {
  const response = await fetch(new URL(path, PDS_ORIGIN), {
    ...options,
    headers: {
      accept: 'application/json',
      ...(options.body ? { 'content-type': 'application/json' } : {}),
      ...(options.headers ?? {}),
    },
  })
  let body = null
  try {
    body = await response.json()
  } catch {
    body = null
  }
  return { response, body }
}

const createAccount = async (slug) => {
  const password = `${randomBytes(24).toString('base64url')}Aa9!`
  const { response, body } = await requestJson('/xrpc/com.atproto.server.createAccount', {
    method: 'POST',
    body: JSON.stringify({
      handle: `${slug}.radlib.edriffles.us`,
      email: `${slug}@example.test`,
      password,
    }),
  })
  if (!response.ok || !body?.accessJwt || !body?.did) {
    throw new Error(
      `createAccount:${response.status}:${body?.error ?? 'InvalidResponse'}:${body?.message ?? ''}`,
    )
  }
  return {
    did: body.did,
    handle: body.handle,
    password,
    accessJwt: body.accessJwt,
  }
}

const authenticatedClient = (account) =>
  new Client({
    service: PDS_ORIGIN,
    headers: { authorization: `Bearer ${account.accessJwt}` },
  })

const dpopClient = (token, key) =>
  new Client({
    service: PDS_ORIGIN,
    fetch: async (input, init = {}) => {
      const url = new URL(input)
      const headers = new Headers(init.headers)
      headers.set('authorization', `DPoP ${token}`)
      headers.set(
        'dpop',
        await createDpopProof(key, {
          htm: init.method ?? 'GET',
          htu: url.toString(),
          credential: token,
        }),
      )
      return fetch(url, { ...init, headers })
    },
  })

const statusOf = (result) => {
  if (result.ok) return { status: 200, ok: true }
  return { status: null, ok: false, error: result.error }
}

const main = async () => {
  assertSafeTarget()

  let owner
  let member
  let ownerClient
  let memberClient
  let space
  let cleanup
  let initialAccess
  let initialGrant
  let beforeRemoval
  let newGrantAfterRemoval
  let alreadyIssuedAfterRemoval

  try {
    const suffix = `${Date.now().toString(36).slice(-6)}${randomBytes(2).toString('hex')}`
    owner = await createAccount(`owner-${suffix}`)
    member = await createAccount(`member-${suffix}`)
    ownerClient = authenticatedClient(owner)
    memberClient = authenticatedClient(member)

    const created = await ownerClient.call(com.atproto.simplespace.createSpace, {
      type: 'us.edriffles.radlib.community',
      skey: `oauth-${suffix}`,
      policy: { $type: 'com.atproto.simplespace.defs#memberListPolicy' },
      appAccess: { $type: 'com.atproto.simplespace.defs#open' },
    })
    space = created.uri

    await ownerClient.call(com.atproto.simplespace.addMember, {
      space,
      did: member.did,
    })

    await ownerClient.call(com.atproto.space.createRecord, {
      space,
      repo: owner.did,
      collection: 'com.example.publicCanary',
      record: {
        $type: 'com.example.publicCanary',
        text: 'disposable credentialed Spaces lifecycle',
        createdAt: new Date().toISOString(),
      },
    })

    initialAccess = await memberClient.call(com.atproto.space.getDelegationToken, { space })
    const initialKey = await JoseKey.generate(['ES256'])
    const initialProof = await createDpopProof(initialKey, {
      htm: 'POST',
      htu: new URL('/xrpc/com.atproto.space.getSpaceCredential', PDS_ORIGIN).toString(),
    })
    const exchanged = await memberClient.call(
      com.atproto.space.getSpaceCredential,
      { space },
      {
        headers: {
          authorization: `Bearer ${initialAccess.token}`,
          dpop: initialProof,
        },
      },
    )
    initialGrant = { token: exchanged.credential, key: initialKey }

    beforeRemoval = await capture(() =>
      dpopClient(initialGrant.token, initialGrant.key).call(
        com.atproto.space.getLatestCommit,
        { space, repo: owner.did },
      ),
    )

    const removed = await capture(() =>
      ownerClient.call(com.atproto.simplespace.removeMember, {
        space,
        did: member.did,
      }),
    )
    if (!removed.ok) throw new Error(`removeMember:${removed.error}`)

    const afterRemovalAccess = await memberClient.call(
      com.atproto.space.getDelegationToken,
      { space },
    )
    const newKey = await JoseKey.generate(['ES256'])
    const newProof = await createDpopProof(newKey, {
      htm: 'POST',
      htu: new URL('/xrpc/com.atproto.space.getSpaceCredential', PDS_ORIGIN).toString(),
    })
    newGrantAfterRemoval = await capture(() =>
      memberClient.call(
        com.atproto.space.getSpaceCredential,
        { space },
        {
          headers: {
            authorization: `Bearer ${afterRemovalAccess.token}`,
            dpop: newProof,
          },
        },
      ),
    )

    alreadyIssuedAfterRemoval = await capture(() =>
      dpopClient(initialGrant.token, initialGrant.key).call(
        com.atproto.space.getLatestCommit,
        { space, repo: owner.did },
      ),
    )

    cleanup = await capture(() =>
      ownerClient.call(com.atproto.simplespace.deleteSpace, { space }),
    )

    const result = {
      format: 'us.edriffles.radlib.public-credentialed-spaces/1',
      evidenceStatus: 'current',
      secretsIncluded: false,
      status:
        beforeRemoval.ok &&
        !newGrantAfterRemoval.ok &&
        !alreadyIssuedAfterRemoval.ok &&
        cleanup.ok
          ? 'PASSED_PUBLIC_DISPOSABLE_SPACES_IMMEDIATE_REVOCATION'
          : 'FAILED_PUBLIC_DISPOSABLE_SPACES_IMMEDIATE_REVOCATION',
      bindings: {
        deploymentImage: DEPLOYMENT_IMAGE,
        environment: 'disposable-public-alpha/staging',
        origins: [PDS_ORIGIN],
        sourceWorkingTreeDigest: SOURCE_DIGEST,
        testedAt: PROBED_AT,
        testedSourceRevision: SOURCE_REVISION,
      },
      test: {
        accountsCreated: 2,
        authorityHost: new URL(PDS_ORIGIN).hostname,
        spaceType: 'us.edriffles.radlib.community',
        initialGrantRead: statusOf(beforeRemoval),
        memberRemoval: statusOf(removed),
        newGrantAfterRemoval: {
          status: newGrantAfterRemoval.ok ? 200 : 400,
          ok: !newGrantAfterRemoval.ok,
          error: newGrantAfterRemoval.error,
        },
        alreadyIssuedGrantAfterRemoval: {
          status: alreadyIssuedAfterRemoval.ok ? 200 : 401,
          ok: !alreadyIssuedAfterRemoval.ok,
          error: alreadyIssuedAfterRemoval.error,
        },
        cleanup: statusOf(cleanup),
      },
    }

    if (OUTPUT_PATH) {
      await writeFile(OUTPUT_PATH, `${JSON.stringify(result, null, 2)}\n`)
    }
    console.log(JSON.stringify(result, null, 2))
    return result.status.startsWith('PASSED_') ? 0 : 1
  } catch (error) {
    cleanup = space && ownerClient
      ? await capture(() =>
          ownerClient.call(com.atproto.simplespace.deleteSpace, { space }),
        )
      : { ok: false, error: 'not-attempted' }
    const result = {
      format: 'us.edriffles.radlib.public-credentialed-spaces/1',
      evidenceStatus: 'current',
      secretsIncluded: false,
      status: 'FAILED_PUBLIC_DISPOSABLE_SPACES_IMMEDIATE_REVOCATION',
      bindings: {
        deploymentImage: DEPLOYMENT_IMAGE,
        environment: 'disposable-public-alpha/staging',
        origins: [PDS_ORIGIN],
        sourceWorkingTreeDigest: SOURCE_DIGEST,
        testedAt: PROBED_AT,
        testedSourceRevision: SOURCE_REVISION,
      },
      error: errorName(error),
      test: {
        accountsCreated: Number(Boolean(owner)) + Number(Boolean(member)),
        cleanup: statusOf(cleanup),
      },
    }
    if (OUTPUT_PATH) {
      await writeFile(OUTPUT_PATH, `${JSON.stringify(result, null, 2)}\n`)
    }
    console.log(JSON.stringify(result, null, 2))
    return 1
  }
}

process.exitCode = await main()
