# AppView Service Identity

## Identity contract

An AppView provider is identified by a DID plus service fragment. The service-auth audience is the provider DID (or DID service reference), and the `atproto-proxy` value is `${serviceDid}#${serviceFragment}`. The endpoint is routing metadata only; it is not an authority for account writes.

## Current deployment

The pinned social-app default provider is Bluesky's public AppView:

- DID: `did:web:api.bsky.app`
- service fragment: `bsky_appview`
- endpoint: `https://api.bsky.app`

A project AppView deployment MUST set `APPVIEWLITE_SERVICE_DID` to its own stable `did:web` or `did:plc` identity and publish a DID document whose service entry points at the deployment. The verifier rejects tokens whose audience does not match that configured identity. No production public project DID is claimed by this repository.

## DID document requirements

The issuer account DID document must publish the `#atproto` verification method used to sign service-auth JWTs. The AppView DID document must publish the selected service endpoint and fragment. DID:web deployments require HTTPS and domain control; DID:PLC deployments require PLC operation control.

## Rotation and recovery

Rotate the issuer `#atproto` key by publishing the new DID document before issuing tokens with it; retain the old key until all short-lived tokens expire. Rotate a provider endpoint by updating its DID service entry and the persisted provider record explicitly. Recovery requires control of the DID method (DNS/web origin for DID:web or PLC operation keys for DID:PLC); an endpoint change alone does not transfer service identity.

## UI and diagnostics

The Services screen displays the selected provider display name and verified service DID. Provider records retain the endpoint and service fragment, while PDS account host and writes remain separate. Custom records are accepted only after DID syntax and HTTPS/SSRF validation.
