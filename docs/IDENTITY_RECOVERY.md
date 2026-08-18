# Identity Recovery v1

Recovery restores user control through explicitly scoped factors; it is not a new universal identity authority. User/device/session authority may authenticate or revoke grants. PDS operators, OAuth clients, recovery email, DNS, PLC, AppViews, feeds, and labelers have only their existing service or delegated scopes and cannot silently alter DID authority or portable personalization.

Supported runtime factors are represented by factor class (session, primary credential, OAuth grant, signing key, recovery key) without storing secrets. Each factor has purpose, expiry, revocation, and compromise implications. Social voting, reputation thresholds, and follower approval are explicitly unsupported.

Recovery transitions through challenge, factor verification, authority check, credential rotation, session revocation, identity/service revalidation, and final verification. Emergency lockdown revokes sessions, blocks writes, invalidates identity cache, and disables remembered service credentials while preserving portable preferences. Receipts contain no passwords, tokens, private keys, email contents, or raw device fingerprints.
