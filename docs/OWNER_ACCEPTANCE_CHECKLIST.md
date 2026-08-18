# Owner Acceptance Checklist

**State:** `OWNER_ACCEPTANCE_PENDING` — automated checks do not constitute owner approval.

Launch from the tested path:

```sh
cd upstream/social-app
pnpm install --frozen-lockfile
pnpm web
```

For each row mark `PASS`, `FAIL`, or `NEEDS CHANGE` and add owner notes.

| # | Action | Expected behavior | Principle | Result / owner notes |
|---:|---|---|---|---|
| 1 | Launch client | Ordinary social client opens without architecture ceremony | Usable defaults | |
| 2 | Open Home | Home identifies its active feed/provider | Attention transparency | |
| 3 | Select Following | Chronological/following alternative is discoverable | Attention sovereignty | |
| 4 | Select Balanced | Balanced is labeled as a distinct ranking mode | Algorithm choice | |
| 5 | Select a custom feed | Provider/feed identity is visible | Polycentric services | |
| 6 | Open Why this post | Explanation does not claim more precision than evidence | Transparency | |
| 7 | Choose More like this | Explicit preference is acknowledged | Explicit preference | |
| 8 | Choose Less like this | Preference is reversible and not a block/mute | Freedom of association | |
| 9 | Change familiarity/discovery | Exploration control is understandable | Serendipity | |
| 10 | Toggle Quiet Metrics | Counts/prominence change without breaking feed | Quiet social proof | |
| 11 | Follow a user | Explicit follow creates the relationship | Freedom of association | |
| 12 | Unfollow the user | Explicit unfollow reverses it | Reversible defaults | |
| 13 | Block Bob | Direct A/B interactions are bounded | Pairwise nonassociation | |
| 14 | View Bob as Charlie | Alice's block does not unnecessarily control Charlie | Third-party independence | |
| 15 | Unblock Bob | Unblock is discoverable and reversible | Pairwise freedom | |
| 16 | Mute a user | Mute is distinct from block and labeled | Freedom of association | |
| 17 | Subscribe to a labeler | Labeler scope and actor are visible | Delegated authority | |
| 18 | Inspect a label | Label is not presented as a block or identity deletion | Anti-reification | |
| 19 | Disable/change provider | Provider switching is practical, not decorative | Polycentric services | |
| 20 | Simulate provider failure | Failing actor is named; fallback is not impersonated | Explicit fallback | |
| 21 | Open Services settings | AppView, feed, labeler identities are distinct | No meta-authority | |
| 22 | Open Identity settings | DID and handle are not conflated | Individual sovereignty | |
| 23 | Inspect PDS and AppView | Hosting and presentation are separate institutions | Polycentric services | |
| 24 | Inspect sessions | Session authority and revocation are understandable | Delegated authority | |
| 25 | Open recovery/lockdown | Recovery power is described honestly | Honest recovery | |
| 26 | Inspect personalization | State is inspectable/resettable | User-owned personalization | |
| 27 | Export personalization | Export has version/provenance and no credentials | Portability/privacy | |
| 28 | Reset personalization | Reset does not delete follows/blocks/identity | Separation | |
| 29 | Import personalization | Intended preferences restore without credentials | Portability | |
| 30 | Change AppView | DID, PDS, associations, and preferences remain stable | Exit | |
| 31 | Change feed provider | Ranking/provider changes without identity mutation | Service separation | |
| 32 | Inspect defaults | Defaults are labeled and replaceable | Reversible defaults | |
| 33 | Find advanced controls | Sovereignty controls are discoverable without overwhelming Home | Usability/choice | |
| 34 | Trigger a PDS error | UI names PDS rather than “the platform” | Anti-reification | |
| 35 | Trigger a feed error | UI names feed provider and fallback state | Explicit fallback | |
| 36 | Review terminology | No vague monolithic institutional claims | Anti-reification | |
| 37 | Search settings for political quotas | No compulsory viewpoint/demographic balancing | Content neutrality | |
| 38 | Compare viral/small-author fixture | Raw engagement does not trivially monopolize Balanced | Structural diversity | |
| 39 | View familiar/discovery fixture | Exploration remains bounded and user-adjustable | Controlled serendipity | |
| 40 | Attempt sign-in/logout/re-auth | Session transitions are understandable and truthful | Identity sovereignty | |

Owner decision options after completing this checklist: `OWNER_ACCEPTANCE_PASSED`, `OWNER_ACCEPTANCE_FAILED`, or `NEEDS_CHANGE`. Do not infer a decision from automated test results.
