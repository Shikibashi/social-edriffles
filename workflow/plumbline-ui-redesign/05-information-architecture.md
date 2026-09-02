# Information architecture: Plumbline Editorial Page Mode

## Product model

Page Mode is the ordinary social reading environment. It should feel like a publication whose documents happen to be interactive and networked. Workbench Mode remains the explicit environment for service, identity, authorization, moderation, migration, and protocol operations.

```text
Plumbline publication
  ├─ Masthead
  │    ├─ wordmark
  │    ├─ descriptor
  │    ├─ motto
  │    └─ publication rule
  ├─ Index / Navigator
  │    ├─ account and identity entry
  │    ├─ sections and editions
  │    ├─ reading collections
  │    ├─ services/identity escape hatches
  │    └─ authoring action
  ├─ Editorial Document Stream
  │    ├─ section/edition header
  │    ├─ feed choice and compact source cue
  │    ├─ composer entry
  │    ├─ continuous post entries
  │    └─ post/thread actions
  └─ Marginal Inspector
       ├─ selected object summary
       ├─ why/why-not or omitted explanation
       ├─ source/provider/rule/status
       ├─ user control
       └─ technical record details
```

## Persistent versus contextual information

| Information | Default location | Why | Disclosure level |
|---|---|---|---|
| Plumbline identity | Full-width masthead | Establishes publication before app chrome | Always visible on wide Page Mode; compact mark on mobile |
| Current section | Stream heading | Keeps reading context stable | Always visible |
| Active edition/feed | Section navigation and compact source line | Lets users know which document stream is active | Visible; details on demand |
| Feed ordering | Section metadata or Inspector | Important to interpret selection, but not a toolbar | Compact label; expanded explanation on demand |
| Provider identity | Source cue and Inspector | Prevents provider from becoming invisible network authority | Cue visible; endpoint/DID technical detail on demand |
| Why a post appears | Inspector for selected post; optional inline cue | Supports algorithmic intelligibility without interrupting every entry | One-click explanation |
| Omitted/alternative content | Inspector where knowable | Prevents users inferring social intent from absence | On demand; only if grounded |
| Moderation assertion/rule/action | Inspector or item warning | Keeps layers distinct | Summary at point of effect; full chain on demand |
| PDS/identity/session state | Identity/Services Workbench | High-consequence configuration | Not default feed chrome |
| Raw AT URI/CID/DID/endpoint | Technical detail/raw record | Expert inspection | Two-step disclosure from relevant object |
| Feed freshness/health | Quiet status cue/Inspector | Peripheral awareness | Escalate only when action is needed |

## Selection and synchronization contract

There is one explicit Page Mode selection state. It may be empty, a feed/edition, a post, a thread, an account, a label assertion, or a provider/service. The Navigator, Stream, and Inspector must derive their visible context from the same selection/route state.

```text
route + selected object
        │
        ├─ Navigator: section/route location and available movement
        ├─ Stream: primary document and active entry
        └─ Inspector: source, explanation, rule, status, control
```

Opening an Inspector detail, closing it, or switching provider must preserve the browser URL, stream scroll position where feasible, keyboard focus intent, and the user's selected object. A stale/unavailable relationship is displayed as stale/unavailable, not replaced silently.

## Inspector state machine

```text
No selection
  ├─ show lightweight current-section context
  └─ collapse margin when no useful context exists

Feed selected
  └─ source / ordering / feed controls

Post selected
  ├─ why shown / source / rule / status
  └─ expand → provider details → record/AT URI

Account selected
  └─ identity source / relationship / verification claims

Label selected
  └─ issuer assertion / label meaning / local action

Service selected
  └─ provider / endpoint / health / permissions / alternatives
```

Each state must identify the subject of the note. `Explanation`, `Evidence or status`, and `Control` are separate fields. A provider's explanation does not become a claim that the content is true, complete, or fair.

## Responsive information model

The model remains stable, but spatial composition changes deliberately:

| Mode | Composition | Transformation |
|---|---|---|
| Wide desktop | Masthead; Index; dominant Stream; contextual Inspector | All three roles can be co-visible; Inspector is reduced when no selection |
| Standard desktop | Masthead; compact Index; dominant Stream; Inspector as margin or drawer | Preserve reading measure; reduce rail width and move deep context behind a toggle |
| Tablet | Masthead; Stream; explicit Index/Context controls | Navigator and Inspector become drawers/sheets; current section and source cue stay in Stream |
| Mobile | Compact masthead; Stream; explicit Navigation and Context actions | Bottom/edge controls retain route orientation; no forced desktop grid; context opens as a labeled sheet |
| Workbench | Existing Workbench layout | Stronger controls, tables, and technical detail remain allowed |

Do not implement mobile as “desktop columns stacked.” Mobile operations are explicit: retain route/section identity, reorder authoring and reading controls, compress routine source cues, collapse advanced provenance, defer services, and replace persistent rails with accessible drawers.

## Content anatomy of a stream entry

```text
continuous plumb/provenance spine
  author / handle / time / relationship
  post text
  integrated media or quote figure, if present
  source cue or selected-state marker, if useful
  compact action row
  printer-like separator
```

The stream entry does not become a card merely because it has a boundary. A nested quote is an authored figure/quotation with a clear source link, not a second dashboard panel. Social actions remain real controls and preserve existing behavior.

## Navigation vocabulary

Use user-facing editorial vocabulary in Page Mode:

- publication/masthead;
- Index;
- sections/editions;
- current issue or current section;
- byline;
- marginal note;
- source/provider;
- rule;
- control;
- details/record.

Use technical vocabulary when it names a real object or helps an expert act: DID, AT URI, CID, endpoint, AppView, PDS, labeler, permission, session, provider ID. Do not use `WORKSPACE` or `DOCUMENT STREAM` as dominant user-facing headings.
