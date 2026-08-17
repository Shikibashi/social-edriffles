# Provider Failure and Unsupported Endpoint Matrix

| Condition | Behavior | Credential boundary | User choice |
|---|---|---|---|
| Valid selected provider | Request uses its HTTPS endpoint and DID-bound service-auth token | PDS token stays on PDS minting call | None |
| Invalid custom DID | Registration rejects the provider | No request issued | Cancel registration |
| HTTP, localhost, private-IP, credentials, query, or fragment endpoint | Registration rejects the provider | No request issued | Cancel registration |
| Provider timeout (15 seconds) | Request fails; no provider substitution | No raw PDS token forwarded | Cancel, use Bluesky once, or always use Bluesky for the feature |
| Redirect response | `redirect: error` rejects the request | No redirected credential forwarding | Cancel or explicit Bluesky choice |
| Service-auth issuance failure | Request fails before AppView call | PDS access token is used only against PDS | Cancel or explicit Bluesky choice |
| Wrong DID/audience/lxm/signature/replay | AppView rejects request | No raw PDS token accepted | Cancel or explicit Bluesky choice |
| Unsupported feature | No automatic provider change | PDS writes remain independent | Use Bluesky once, always use Bluesky for feature, or cancel |

There is no implicit fallback to `api.bsky.app` after provider selection. The Services screen displays the selected provider DID and endpoint and makes fallback choices explicit. Persisted provider choices are account-DID scoped; the one-time choice does not overwrite the selection.
