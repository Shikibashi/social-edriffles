# Daily Driver Runtime Topology

The supported radical-liberal topology is:

```text
social-app client
       ├── first-party PDS (identity, auth, repository writes, CAR import)
       └── explicitly selected AppView/feed/labeler/resolver providers
```

The first-party PDS is the pinned official `@atproto/pds` base under
`upstream/atproto-pds`, with the governed listblock write policy enabled by
configuration. AppViewLite and FishyFlip are retired and are not runtime
dependencies. The client uses the explicitly selected AppView/feed/labeler/
resolver providers; none is the authority for identity or repository writes.

Required for the client: Node 24.19+, pnpm 11.21+, social-app dependencies,
and a browser. Required for the first-party PDS: Node 22+, pnpm 11.11+,
configured database/blobstore/identity secrets, and the explicit
`PDS_RADLIB_MODERATION_WRITE_POLICY=deny-create-update` setting. Optional:
another AppView/feed/labeler/resolver provider. Development-only: e2e mock
server, native build toolchains, and fixture providers. Test-only: Jest
fixtures and harnesses. A retired provider checkout may remain as local
historical evidence, but is not a supported launch target.
