# Identity Recovery Authority Matrix

| Actor | Can recover/authenticate | Cannot do | Revocation | Compromise impact |
|---|---|---|---|---|
| User/current device | request recovery, revoke sessions | bypass identity verification | user lockdown | local account compromise |
| Authorized device/session | scoped authentication | become DID operation authority | session revoke | bounded grant theft |
| PDS operator | service-local account assistance | mint DID authority or portable state | service replacement | hosting compromise |
| OAuth client | declared endpoint scope | general account control | grant revocation | token theft |
| DNS/registrar | DID:web/handle evidence | alter did:plc subject | DNS correction | resolution compromise |
| AppView/feed/labeler | presentation/indexing | identity, association, or recovery control | provider switch | privacy/presentation impact |
| Recovery email/provider | deliver challenge | silently rotate DID keys | channel replacement | recovery-channel compromise |

No default social recovery or centralized reputation authority exists.
