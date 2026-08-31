# Plumbline progressive-surface audit

## Scope

This is a focused implementation record for ordinary read surfaces. It applies
the Plumbline progression without changing OAuth grants, provider selection,
records, routes, or social actions:

```text
ordinary reading -> concise source/state -> inspectable explanation -> Services/raw detail
```

The source of truth remains `DESIGN.md`. The audit also used the current web
interface guidance for visible labels, focusable disclosure controls, and
stable sticky/layout behavior.

## Findings and disposition

| Surface | Ordinary task | Finding | Change | Full detail remains visible when |
| --- | --- | --- | --- | --- |
| Feed stream | Read, switch feed, post | The provenance header rendered outside the constrained stream at desktop widths, then repeated its source/rule details before every task. | Put the header in the list boundary at every viewport and compress it to feed/source/state. | The user selects `Show feed details`, inspects sources, or opens feed settings. |
| Feed post | Read and act on a post | A `Why this post?` row appeared on every post even when it repeated the feed-level source and normal reader state. | Render it only for a public per-post reason, provider ranking explanation, or degraded/disputed reader state. | The post has a placement-specific fact; generic provider/feed provenance remains inspectable once at the feed boundary. |
| Profile | Read an account and its posts | Media and identity summaries led with two full source/rule/state blocks before the profile content. | Use compact source/state summaries while preserving their existing inspection controls. | The user opens profile-media or identity-resolution details; profile-read errors retain full summaries. |
| Thread, search, notifications, feeds directory | Complete a read task | Read provider summaries were correct but more verbose than the primary list/document. | Use compact source/state summaries during ordinary success states. | A provider error occurs, or the user selects the existing source inspection control. |
| Services, Identity & recovery, Moderation & Reach, OAuth prompts, Community authorization | Configure, authorize, or recover | These are workbench or blocking-decision surfaces, not ambient reading chrome. | Keep their full explanations visible. | Always, because the source/rule/control is the task itself. |

## Boundary

Compact presentation does not hide a provider, claim agreement that is not
available, or create a fallback. It removes only duplicated default prose.
Every compact line retains a text label, a non-color plumb-line marker, a
keyboard-reachable inspection action, and the same underlying source data.

## Acceptance checks

- The feed header belongs to the center document stream at desktop and mobile
  sizes, without horizontal page overflow.
- A normal chronological feed does not add a repetitive placement row to every
  post.
- An explicit per-post reason or non-agreement provider state still creates a
  `Why this post?` control.
- Profile, thread, search, notification, and feeds-directory source details
  are reachable without competing with their primary documents/lists.
- Error and Services workbench screens continue to expose full source/rule
  details before remediation.
