# Constitutional Invariants

This fork is politically content-neutral. It allocates authority rather than deciding which viewpoints are worthy.

1. **Viewer sovereignty:** each viewer controls their information environment.
2. **Pairwise nonassociation:** a block governs the blocker/blocked relationship; it does not decide what unrelated viewer C sees.
3. **Direct boundaries:** supported direct follows, replies, mentions, notifications, chat, and other direct association are severed according to the observed AppView contract.
4. **Third-party independence:** unrelated viewers retain independent choice.
5. **Replaceability and exit:** PDS, AppView, feeds, labelers, and future providers remain separable; exit preserves identity and portable explicit preferences.
6. **Delegated authority:** OAuth and service powers are narrow, visible, and revocable.
7. **Polycentric moderation:** personal filtering, feed/community curation, labelers, and operator enforcement remain distinct powers.
8. **Transparent actors:** UI and documentation name the actual actor making a decision.
9. **Privacy defaults:** telemetry, tracking redirects, dwell/scroll/hover collection, and geolocation are disabled unless explicitly required.

PR-00/PR-01 records current behavior and does not change production semantics.
## Personalization boundary

10. **User-owned personalization:** explicit preferences and local learned personalization belong to the user, not the current AppView, feed provider, PDS host, or client instance.
11. **Inspectable and portable:** derived state remains resettable/exportable at an appropriate abstraction level; settings-only export excludes behavioral history.
12. **Provider independence:** changing AppView, feed provider, or PDS host does not inherently delete personalization or require retraining from zero.
13. **Data minimization:** passive dwell time and full behavioral histories are not collected or forwarded by default.
14. **Attention governance:** attention orderings remain user-controlled, replaceable, inspectable, and distinct from association, moderation, and service authority; see `docs/ATTENTION_CONSTITUTION.md`.
