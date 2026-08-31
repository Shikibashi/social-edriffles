# Design brief: Plumbline shell decluttering

## Status

Bounded refinement of the existing Plumbline / ECW **Seamful Hypertext
Workbench** direction. This is a hierarchy and progressive-disclosure change,
not a brand or route redesign.

## Problem

The live desktop shell presents the document stream between a full Navigator
and an Inspector that is followed immediately by search, the complete feed
list, progress guidance, live-event content, and trending topics. The home
surface also presents a feed summary and a second provider-composition summary
at the same visual level. The result is useful information, but too many
simultaneous starting points compete with reading and posting.

## Intent

Make the document stream the unambiguous first task. Keep the selected surface
and its source/rule explanation visible. Move replaceable, optional read and
discovery tools behind one clearly named, keyboard-reachable disclosure. Keep
all existing destinations and provider inspection paths available.

## Constraints

- Preserve `DESIGN.md`, the Plumbline mark, the warm-paper/cool-gray palette,
  square controls, structural rules, and the Navigator | Stream | Inspector
  workbench.
- Preserve routes, feed selection, search, provider composition, account
  actions, OAuth, posting, engagement, profiles, chat, and Spaces behavior.
- Do not add a second provider or policy abstraction.
- Do not hide consequential errors, permission prompts, or primary actions.
- Keep browser links, keyboard focus, target sizes, mobile navigation, and
  reduced-motion behavior intact.

## Success signal

At desktop width, the first viewport has one primary stream, one selected
surface inspector, one global search affordance, and a compact `More context`
control. Feed lists, progress guidance, live-event discovery, and trends appear
only after that control is expanded. The feed surface exposes one concise
authority summary; deeper provider comparison remains available through an
inspection control.
