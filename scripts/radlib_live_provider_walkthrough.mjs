import { createServer } from 'node:http'
import { once } from 'node:events'
import { readFile } from 'node:fs/promises'
import { join } from 'node:path'

import { AtUri } from '../upstream/atproto-pds/packages/api/dist/index.js'
import { P256Keypair, sha256Hex } from '../upstream/atproto-pds/packages/crypto/dist/index.js'
import {
  TestNetworkNoAppView,
  TestPds,
  mockNetworkUtilities,
} from '../upstream/atproto-pds/packages/dev-env/dist/index.js'

const ATTESTATION_VERSION = 'radlib-list-mute-attestation/1'

const json = (value) => JSON.stringify(value, null, 2)

const errorShape = (error) => ({
  error: error?.error ?? error?.name ?? 'Error',
  message: error?.message ?? String(error),
})

const tryAction = async (action) => {
  try {
    await action()
    return { ok: true }
  } catch (error) {
    return { ok: false, ...errorShape(error) }
  }
}

const readBody = async (request) => {
  const chunks = []
  for await (const chunk of request) chunks.push(chunk)
  return JSON.parse(Buffer.concat(chunks).toString('utf8'))
}

const listen = async (server) => {
  server.listen(0, '127.0.0.1')
  await once(server, 'listening')
  return server.address().port
}

const close = async (server) => {
  if (!server) return
  server.close()
  await once(server, 'close')
}

const main = async () => {
  let network
  let targetPds
  let provider

  try {
    network = await TestNetworkNoAppView.create()
    const sourceAgent = network.pds.getAgent()
    const sourceAccount = await sourceAgent.createAccount({
      email: 'radwalksrc@test.com',
      handle: 'radwalksrc.test',
      password: 'radlib-walkthrough-pass',
    })
    const sourceDid = sourceAgent.assertDid
    let plcOperationToken
    network.pds.ctx.mailer.sendPlcOperation = async ({ token }) => {
      plcOperationToken = token
    }

    const list = await sourceAgent.api.app.bsky.graph.list.create(
      { repo: sourceDid },
      {
        name: 'Legacy moderation list',
        purpose: 'app.bsky.graph.defs#modlist',
        createdAt: new Date().toISOString(),
      },
    )
    const listUri = list.uri
    const listblock = await sourceAgent.com.atproto.repo.createRecord({
      repo: sourceDid,
      collection: 'app.bsky.graph.listblock',
      record: {
        $type: 'app.bsky.graph.listblock',
        subject: listUri,
        createdAt: new Date().toISOString(),
      },
    })
    const sourceCar = await sourceAgent.com.atproto.sync.getRepo({
      did: sourceDid,
    })

    const providerKey = await P256Keypair.create({ exportable: true })
    const providerDid = providerKey.did()
    const mutedLists = new Set([listUri])
    const providerRequests = []

    provider = createServer(async (request, response) => {
      if (
        request.method !== 'POST' ||
        request.url !== '/xrpc/us.edriffles.radlib.moderation.getListMuteAttestation'
      ) {
        response.writeHead(404).end()
        return
      }

      const input = await readBody(request)
      providerRequests.push({ ...input })
      if (!mutedLists.has(input.list)) {
        response.writeHead(400, { 'content-type': 'application/json' })
        response.end(JSON.stringify({ error: 'ListNotMuted' }))
        return
      }

      const issuedAt = new Date().toISOString()
      const payload = [
        ATTESTATION_VERSION,
        providerDid,
        sourceDid,
        input.listUriHash,
        issuedAt,
        input.nonce,
      ].join('\n')
      const signature = Buffer.from(
        await providerKey.sign(Buffer.from(payload, 'utf8')),
      )
        .toString('base64')
        .replaceAll('+', '-')
        .replaceAll('/', '_')
        .replaceAll('=', '')

      response.writeHead(200, { 'content-type': 'application/json' })
      response.end(
        JSON.stringify({
          attestation: {
            version: ATTESTATION_VERSION,
            subjectDid: sourceDid,
            listUriHash: input.listUriHash,
            providerDid,
            issuedAt,
            nonce: input.nonce,
            signature,
          },
        }),
      )
    })
    const providerPort = await listen(provider)
    const providerUrl = `http://127.0.0.1:${providerPort}`

    targetPds = await TestPds.create({
      didPlcUrl: network.plc.url,
      radlibModerationWritePolicy: 'deny-create-update',
      radlibMuteAttestationProviderDid: providerDid,
      radlibMuteAttestationProviderKey: providerDid,
    })
    mockNetworkUtilities(targetPds)
    const targetAgent = targetPds.getAgent()
    const targetServer = await targetAgent.api.com.atproto.server.describeServer()
    const serviceAuth = await sourceAgent.com.atproto.server.getServiceAuth({
      aud: targetServer.data.did,
      lxm: 'com.atproto.server.createAccount',
    })

    await targetAgent.api.com.atproto.server.createAccount(
      {
        did: sourceDid,
        email: 'radwalkdst@test.com',
        handle: 'radwalkdst.test',
        password: 'radlib-walkthrough-pass',
      },
      {
        headers: { authorization: `Bearer ${serviceAuth.data.token}` },
        encoding: 'application/json',
      },
    )
    await targetAgent.login({
      identifier: 'radwalkdst.test',
      password: 'radlib-walkthrough-pass',
    })

    await targetAgent.com.atproto.repo.importRepo(sourceCar.data, {
      encoding: 'application/vnd.ipld.car',
    })
    const statusAfterImport = await targetAgent.com.atproto.server.checkAccountStatus()
    const activationBefore = await tryAction(() =>
      targetAgent.com.atproto.server.activateAccount(),
    )

    const listUriHash = await sha256Hex(listUri)
    const nonce = 'radlib-live-walkthrough-001'
    const providerResponse = await fetch(
      `${providerUrl}/xrpc/us.edriffles.radlib.moderation.getListMuteAttestation`,
      {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          list: listUri,
          listUriHash,
          nonce,
        }),
      },
    )
    const providerBody = await providerResponse.json()
    if (!providerResponse.ok) {
      throw new Error(`provider attestation failed: ${json(providerBody)}`)
    }

    const recordResponse = await fetch(
      `${targetPds.url}/xrpc/us.edriffles.radlib.moderation.recordListMuteAttestation`,
      {
        method: 'POST',
        headers: {
          authorization: `Bearer ${targetAgent.session.accessJwt}`,
          'content-type': 'application/json',
        },
        body: JSON.stringify({ attestation: providerBody.attestation }),
      },
    )
    const recordBody = await recordResponse.json()
    if (!recordResponse.ok) {
      throw new Error(`PDS attestation recording failed: ${json(recordBody)}`)
    }

    const listblockUri = new AtUri(listblock.data.uri)
    await targetAgent.com.atproto.repo.deleteRecord({
      repo: sourceDid,
      collection: 'app.bsky.graph.listblock',
      rkey: listblockUri.rkey,
    })

    const recommendedDidCredentials =
      await targetAgent.com.atproto.identity.getRecommendedDidCredentials()
    await sourceAgent.com.atproto.identity.requestPlcOperationSignature()
    if (!plcOperationToken) {
      throw new Error('source PDS did not issue a PLC operation token')
    }
    const signedPlcOperation =
      await sourceAgent.com.atproto.identity.signPlcOperation({
        token: plcOperationToken,
        ...recommendedDidCredentials.data,
      })
    await targetAgent.com.atproto.identity.submitPlcOperation({
      operation: signedPlcOperation.data.operation,
    })

    const activationAfter = await tryAction(() =>
      targetAgent.com.atproto.server.activateAccount(),
    )
    const statusAfterActivation = await targetAgent.com.atproto.server.checkAccountStatus()
    const finalRepoStatus = await targetAgent.com.atproto.sync.getRepoStatus({
      did: sourceDid,
    })

    const journalHash = await sha256Hex(sourceDid)
    const journalPath = join(
      targetPds.ctx.cfg.actorStore.directory,
      'radlib-migrations',
      `${journalHash}.json`,
    )
    const receipt = JSON.parse(await readFile(journalPath, 'utf8'))

    console.log(
      json({
        result: 'PASS',
        sourcePds: network.pds.url,
        targetPds: targetPds.url,
        providerEndpoint: providerUrl,
        sourceDid,
        listUri,
        listblockUri: listblock.data.uri,
        listUriHash,
        sourceCarBytes: sourceCar.data.byteLength,
        statusAfterImport: statusAfterImport.data,
        activationBefore,
        provider: {
          url: providerUrl,
          did: providerDid,
          mutedListCount: mutedLists.size,
          requests: providerRequests,
          returnedAttestation: {
            version: providerBody.attestation.version,
            subjectDid: providerBody.attestation.subjectDid,
            listUriHash: providerBody.attestation.listUriHash,
            providerDid: providerBody.attestation.providerDid,
            nonce: providerBody.attestation.nonce,
            signatureBytes: Buffer.from(
              providerBody.attestation.signature.replaceAll('-', '+').replaceAll('_', '/'),
              'base64',
            ).length,
          },
        },
        pdsRecordAttestation: { status: recordResponse.status, body: recordBody },
        activationAfter,
        statusAfterActivation: statusAfterActivation.data,
        finalRepoStatus: finalRepoStatus.data,
        migrationReceipt: {
          status: receipt.status,
          listblocksDiscovered: receipt.listblocksDiscovered,
          convertedToPrivateMute: receipt.convertedToPrivateMute,
          deleted: receipt.deleted,
          remainingListblocks: receipt.remainingListblocks,
          attestationRequired: receipt.attestationRequired,
          attestedListUriHashes: receipt.attestedListUriHashes,
          sourceRecords: receipt.sourceRecords,
        },
      }),
    )
  } finally {
    await close(provider)
    await targetPds?.close()
    await network?.close()
  }
}

await main()
