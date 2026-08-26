# Layout blueprint: Communities forum surface

## Page anatomy

1. **Global route header** — existing Bluesky `Communities` title and back
   affordance.
2. **Community switcher** — compact list of communities visible to the current
   identity; selected item has a structural border and text state.
3. **Community identity block** — name, description, visibility/access copy,
   computed topic count, and the `New topic` action.
4. **Local tab strip** — `Threads`, `Latest`, `Members`, `About`; real tab
   controls with a selected state.
5. **Forum content** — topic rows with derived title, excerpt, author DID,
   latest time, and computed reply count; Latest uses the same records but
   surfaces recent activity.
6. **Topic detail** — root record, replies grouped by the authorized root URI,
   `Back to topics`, and contextual reply composer.
7. **Access and recovery** — membership controls, invite field, partial-read
   notice, errors, refresh, and owner-only management affordances.

## Grid and density

- Existing Bluesky center column is the outer constraint.
- Use one forum column, 16px page gutter, 12px section gaps, 48px minimum
  interaction rows, and 1px structural borders.
- Topic rows use a two-line content block plus a compact metadata line. On wide
  desktop widths the primary text can grow; no rigid three-column card grid is
  introduced.
- The header action aligns to the upper-right where space permits and wraps
  below the description on narrow widths.

## Topic row anatomy

```text
topic title                                      >
short body excerpt
from did:...  ·  0 replies  ·  2026-08-26 12:34
```

The arrow is a text affordance only; the entire row is keyboard/touch
activatable. If a reply relationship is not present in the read result, the
row remains a top-level topic and shows `0 replies` rather than guessing.

## Detail anatomy

```text
Back to topics
TOPIC
title
from did:... · timestamp
body
----------------
REPLIES (n)
reply body / author / timestamp
----------------
Reply in this topic
textarea + Post reply
```

## Mobile reordering

- Keep `Communities` and selected community identity at the top.
- Put `New topic` immediately after the community access summary.
- Keep tabs reachable before the first topic row.
- Replace topic detail in place and provide `Back to topics` above the title.
- Keep technical Space/DID details after the human-readable About content.
