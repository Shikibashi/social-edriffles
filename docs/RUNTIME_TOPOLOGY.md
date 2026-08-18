# Daily Driver Runtime Topology

The supported v1 path is the existing `upstream/social-app` web client against compatible external ATProto infrastructure. The client is required; PDS, AppView, feed providers, labelers, and resolver are remote services selected or discovered through existing client contracts. AppViewLite is optional self-hosted infrastructure, not required for ordinary use. FishyFlip is a development/library repository and is not required to launch the web client.

Required: Node 24.19+, pnpm 11.21+, social-app dependencies, browser. Optional: self-hosted AppViewLite/PDS/provider services. Development-only: e2e mock server, native build toolchains, fixture providers. Test-only: Jest fixtures and harnesses.
