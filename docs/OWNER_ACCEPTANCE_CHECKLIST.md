# Owner Acceptance Checklist

**State:** `OWNER_ACCEPTANCE_PENDING` — the owner must complete the result columns. Automated tests and this review do not constitute owner approval.

## Exact local launch command

```sh
cd /var/home/tcs/Code/atproto/upstream/social-app && pnpm install --frozen-lockfile && pnpm web
```

The validation run used the same app with `pnpm web -- --port 8081` because another development process already occupied the default port. Use a separate port only when necessary.

For every row, the owner should write exactly one of `PASS`, `FAIL`, or `NEEDS CHANGE` in the Owner result column and record evidence or questions in Owner notes. Leave no automated result in these columns before the owner walkthrough.

| # | ACTION | EXPECTED BEHAVIOR | PRINCIPLE | OWNER RESULT (PASS / FAIL / NEEDS CHANGE) | OWNER NOTES |
|---:|---|---|---|---|---|
| 1 | Launch the client with the command above | The ordinary social client opens without architecture ceremony or an invented identity state | Usable defaults; individual sovereignty | | |
| 2 | Open Home | The active feed, provider, algorithm/version, and provenance state are identifiable | Attention transparency | | |
| 3 | Select Following | A chronological/following view is available and remains first-class | Attention sovereignty | | |
| 4 | Select Balanced | If Balanced is presented as a product choice, it is a real selectable ranking mode with a distinct identity; otherwise its current library-only status is plainly disclosed | Algorithm marketplace; honest capability | | |
| 5 | Select a saved/custom feed | The selected feed and its owner/provider are visible and switching is reversible | Polycentric services | | |
| 6 | Inspect the provenance card | Provider DID, feed owner when known, version/manifest status, objective, and privacy scope are not fabricated | Institutional anti-reification; attention transparency | | |
| 7 | Open Why this post? on a locally ranked post | The explanation names only ranking signals present in the actual trace | Attention transparency | | |
| 8 | Open Why this post? on a provider-ranked post | Missing provider trace data is disclosed; the client does not invent a local reason | Truthful attribution | | |
| 9 | Choose More like this | The local explicit preference is persisted and visibly acknowledged | Explicit preferences outrank inference | | |
| 10 | Choose Less like this | The local explicit negative preference is persisted, reversible, and is not a block, mute, follow, or remote interaction | Freedom of association; explicit control | | |
| 11 | Compare association state before and after More/Less | Follows, blocks, mutes, and other durable relationship records are unchanged | Separation of attention and association | | |
| 12 | Run the explicit-negative preference fixture | A strong explicit negative materially lowers a candidate despite passive/inferred positive signals | Explicit preferences outrank passive inference | | |
| 13 | Run the explicit-positive preference fixture | A strong explicit positive materially raises a matching candidate under the documented rule | Explicit preferences outrank passive inference | | |
| 14 | Set discovery/exploration to Low | The exploratory/unfamiliar composition decreases, while explicit Less constraints still apply | Controlled serendipity | | |
| 15 | Set discovery/exploration to Default | The default exploration level is bounded and understandable | Limited/reversible defaults | | |
| 16 | Set discovery/exploration to High | Exploratory composition increases without ideological balancing or quota behavior | Controlled serendipity; political neutrality | | |
| 17 | Combine High discovery with Less Topic X | Exploration does not override an explicit negative preference | Explicit authority; controlled serendipity | | |
| 18 | Change freshness and variety controls where shown | The controls either change output or clearly state their current scope; they are not decorative | Attention sovereignty | | |
| 19 | Toggle Quiet Metrics | Counts/prominence change without changing the underlying records or ranking authority | Attention sovereignty; privacy | | |
| 20 | Compare concentration/author-variety fixture | Structural diversity controls bound concentration without political or demographic outcome quotas | Structural diversity; political neutrality | | |
| 21 | Follow a user, then unfollow | Only deliberate user actions create and reverse the relationship | Freedom of association | | |
| 22 | Run Alice blocks Bob | Alice/Bob direct interaction is severed or bounded according to the supported protocol surfaces | Pairwise freedom of nonassociation | | |
| 23 | View Bob as Charlie | Alice's block does not silently become Charlie's universal authority | Third-party independence | | |
| 24 | As Charlie, inspect threads and replies containing Alice/Bob | Public records remain available where the upstream service permits them; any upstream-required collateral is identified | Pairwise nonassociation | | |
| 25 | As Charlie, inspect quotes, author feeds, search, and Home | No avoidable local fork behavior suppresses Charlie's independent view | Third-party independence | | |
| 26 | Unblock and mute/unmute Bob | Each action is distinct, reversible, and accurately labeled | Freedom of association | | |
| 27 | Open Services settings | PDS, AppView, feed provider, labeler, and resolver are shown as distinct actors when known | Polycentric services | | |
| 28 | Inspect account host and AppView | PDS writes/identity and AppView reads are visibly separated | Institutional anti-reification | | |
| 29 | Register/select an alternate AppView or feed provider where available | Selection is real, persisted, and uses the selected endpoint rather than a hidden default | Meaningful exit; algorithm marketplace | | |
| 30 | Switch back to the prior provider | Switching back is possible and does not rewrite identity or relationship records | Reversible defaults | | |
| 31 | Compare state across provider switching | DID, PDS, follows, blocks, recovery state, and unrelated personalization remain stable | Service separation | | |
| 32 | Simulate a feed-provider failure | The failing provider is named; a materially different provider is not silently impersonated | Explicit fallback | | |
| 33 | Simulate an AppView failure | Unaffected PDS functionality remains available where practical and the failure names the AppView | Polycentric services; explicit fallback | | |
| 34 | Simulate resolver and labeler failures | The resolver/labeler actor and unsupported scope are named; no generic “platform” authority is invented | Institutional anti-reification | | |
| 35 | Exercise remembered fallback | Any remembered fallback is also visible as the active choice and can be replaced or cancelled | Explicit delegated authority | | |
| 36 | Open Identity settings | DID, handle, PDS, and verification state are not conflated | Individual sovereignty | | |
| 37 | Inspect active sessions | Session authority, expiry, and revocation are understandable | Explicit delegated authority | | |
| 38 | Open recovery/lockdown | Recovery capabilities and unsupported migration/identity-update boundaries are described honestly | Meaningful exit; recovery sovereignty | | |
| 39 | Inspect personalization | Learned, explicit, ephemeral, and service state are inspectable with clear scope | Portable personalization | | |
| 40 | Export personalization and inspect the JSON | Format/version/provenance are present and credentials or recovery material are absent | Privacy/data minimization | | |
| 41 | Search the export/schema for secret-bearing fields and values | No passwords, tokens, service-auth material, recovery secrets, or private keys are exported | Credential exclusion | | |
| 42 | Reset personalization | Reset clears the intended local state without deleting identity, follows, blocks, or recovery state | Cross-domain isolation | | |
| 43 | Import the saved export | Explicit preferences and supported settings round-trip; malformed or foreign data fails closed | Portability; fail-closed validation | | |
| 44 | Search constitutional ranking code/configuration | No mandatory left/right, party, ideological, demographic, political-quality, or constructiveness quota enforces outcomes | Political content neutrality | | |
| 45 | Review defaults and friction | Important controls are discoverably replaceable without putting every advanced control on Home | Limited/reversible defaults | | |
| 46 | Attempt the red-team criticism | The owner can distinguish actual centralized authority from documented or upstream-limited capability, with evidence for each claim | Radical-liberal allocation of authority | | |

The automated review remains `OWNER_ACCEPTANCE_PENDING`; owner result cells above are intentionally blank.
