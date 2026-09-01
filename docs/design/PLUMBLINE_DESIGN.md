# Plumbline Design

**Status:** Canonical product-specific design language
**Product:** Plumbline
**Canonical domain:** `plumblines.uk`
**Base design system:** Edriffles Computer Web (ECW)
**Product design branch:** **Plumbline Editorial ECW — Seamful Hypertext Workbench**

---

# 1. Purpose

Plumbline is an ATProto social client built on Edriffles Computer Web.

ECW remains the underlying family-level design system. It defines the computer-native interaction model, browser behavior, accessibility expectations, information density, control grammar, typography roles, responsive behavior, and general visual vocabulary.

Plumbline adds a product-specific layer.

The central design proposition is:

> **A radical individualist periodical evolved continuously into an open-web social client and serious desktop information tool.**

Its historical and conceptual ancestry is approximately:

```text
Benjamin Tucker's Liberty
        ↓
serious radical periodical
        ↓
document-centric old web
        ↓
desktop information software
        ↓
Edriffles Computer Web
        ↓
ATProto
        ↓
Plumbline
```

Do not recreate any historical stage literally.

The desired result is contemporary software belonging to that continuous lineage.

---

# 2. Source Precedence

When design requirements conflict, use this precedence:

1. Correct product behavior and existing constitutional contracts
2. Accessibility, security, browser correctness, and platform behavior
3. `PLUMBLINE_DESIGN.md`
4. Current ECW design documentation
5. Existing Plumbline/ECW implementation
6. Historical references and inspiration

Plumbline may specialize ECW.

It must not silently change behavioral contracts merely to achieve a visual result.

---

# 3. What Plumbline Adds to ECW

ECW already provides:

* explicitness;
* operator agency;
* progressive simultaneity;
* organized information density;
* direct manipulation;
* visible application state;
* learnable complexity;
* multiple command paths;
* browser-native behavior;
* hypertext and addressability;
* strong but configurable defaults;
* recoverability;
* Page Mode;
* Workbench Mode;
* Georgia-like display typography;
* Verdana-like UI/content typography;
* Courier-like metadata typography;
* visible borders and rules;
* square or nearly square geometry;
* explicit controls;
* modern accessibility;
* platform respect.

Plumbline adds:

* editorial composition;
* seamful ATProto infrastructure;
* institutional provenance;
* contestable authority;
* provider legibility;
* ordinary exit and substitution;
* attention sovereignty;
* plumb-line iconography;
* a warmer editorial palette;
* document-stream social presentation.

The distinction is:

> **ECW explains the computer. Plumbline explains the institutions acting through the computer.**

---

# 4. Governing Product Principle

Plumbline behaves as an agent of the individual using it.

It should not present any provider, algorithm, moderation system, authority, or default as more universal than it actually is.

Every consequential surface should make the following progressively answerable:

1. **What is happening?**
2. **Who or what is responsible?**
3. **According to whose rules?**
4. **What can I change?**
5. **What can I use instead?**

This is the **Plumbline Test**.

Not every answer belongs on the default screen.

The user must be able to reach the answer without needing external debugging tools when the underlying system makes it knowable.

---

# 5. Political Expression Through Software

Plumbline's radical liberalism is expressed primarily through institutional design rather than political decoration.

Translate the principles into mechanisms.

## Individual sovereignty

The account holder is the primary unit of agency.

Identity, permissions, providers, feeds, moderation configuration, associations, and migration should be understandable from the user's perspective.

## Freedom of association

Users can choose, create, join, leave, mute, filter, subscribe, unsubscribe, and participate in associations within the capabilities of the underlying system.

Associations remain distinguishable from network-wide authority.

## Freedom of exit

Export, backup, provider replacement, authorization revocation, and migration are normal operations.

Do not make ordinary exit mechanisms resemble catastrophic destructive actions.

## Pluralism

Do not visually equate one AppView, feed generator, labeler, resolver, or provider with ATProto itself.

## Equal treatment

Use consistent interaction and provenance rules regardless of whether the responsible actor is Plumbline, Bluesky, a third-party service, a community, or the user.

## Competition and substitution

Where providers are substitutable, expose useful operations such as:

```text
Inspect…
Configure…
Change…
Compare…
Test…
Remove…
```

## Contestability

Defaults may be strong.

Defaults must not become invisible authority.

---

# 6. Seamful ATProto

ATProto is a composition of different services and authorities.

Plumbline should not flatten them into a fictional single platform.

Relevant concepts include:

```text
Identity
PDS
AppView
Feed Generator
Labeler
Resolver
Verification source
Community authority
Client rule
```

The canonical model is **progressive seamfulness**:

```text
ordinary interface
        ↓
simple

context inspector
        ↓
explanatory

service workbench
        ↓
powerful

raw protocol / diagnostics
        ↓
expert
```

Do not expose protocol internals merely because they exist.

Expose a seam when understanding it gives the user meaningful information, diagnosis, choice, or control.

---

# 7. Editorial Direction

Plumbline is the editorial branch of ECW.

The interface should resemble a serious publication that became interactive software rather than software wearing a newspaper theme.

Take from serious periodical design:

* strong masthead identity;
* typographic hierarchy;
* rules;
* columns;
* compact metadata;
* marginal information;
* deliberate alignment;
* limited decorative dead space;
* continuous reading rhythm;
* seriousness of presentation.

Do not take:

* fake parchment;
* distressed paper;
* blackletter;
* ornate Victorian borders;
* literal newspaper columns where inappropriate;
* fake printing defects;
* antique-interface cosplay.

The editorial influence is structural.

---

# 8. Tucker Influence

Benjamin Tucker's *Liberty* is a conceptual and editorial ancestor, not a skin.

Use the influence through:

* individual sovereignty;
* equal treatment;
* skepticism toward hidden authority;
* consistency;
* editorial seriousness;
* explicit disagreement and provenance;
* the plumb-line metaphor.

Political quotations should not become generic UI decoration.

The optional motto:

> *Liberty, the mother of order.*

may appear in restrained branding contexts such as a masthead, About surface, or project documentation.

It should not appear everywhere.

---

# 9. The Plumb Line

The physical plumb line is the canonical Plumbline symbol.

Its basic geometry is:

```text
vertical line
      ↓
suspended weight
      ↓
precise point
```

It represents:

* reference;
* consistency;
* alignment;
* provenance;
* ancestry;
* inspection.

## Primary mark

A thin vertical line terminating in a compact geometric plumb bob.

At small sizes, use a highly simplified monochrome form.

At larger sizes, the bob may become dimensional aged brass.

## Interface derivatives

Use plumb-line geometry abstractly for:

* active navigation;
* thread ancestry;
* provenance chains;
* quotation rules;
* selected providers;
* timeline position;
* unread boundaries;
* pane divisions;
* inspector relationships;
* reference points.

Do not scatter literal plumb-bob illustrations throughout the product.

The geometry should become the visual grammar.

---

# 10. Product Identity

The product name is:

**Plumbline**

The canonical domain is:

**plumblines.uk**

Do not use:

* Social;
* social.edriffles.us;
* Asterism;
* generic Bluesky branding

as the primary public product identity.

The application should have:

* Plumbline application name;
* Plumbline page metadata;
* Plumbline favicon;
* Plumbline app/PWA icon;
* Plumbline social metadata;
* Plumbline domain defaults where appropriate.

Do not blindly replace technical references to Bluesky where the software is actually describing Bluesky infrastructure or compatibility.

Branding changes must preserve technical truth.

---

# 11. Masthead

Desktop Page Mode may use a restrained Plumbline editorial masthead.

Conceptually:

```text
[plumb] PLUMBLINE
        SOCIAL CLIENT FOR THE OPEN WEB

             Liberty, the mother of order.

────────────────────────────────────────────
```

The masthead should establish identity without consuming excessive vertical space.

It is not a fake browser or fake operating-system title bar.

---

# 12. Typography

Preserve ECW's three typographic voices but assign them more sharply.

## Display / editorial

Georgia or the current ECW display-serif stack.

Use for:

* Plumbline wordmark;
* major screen titles;
* feed titles;
* inspector titles;
* important editorial headings;
* appropriate long-form surfaces.

## Interface

Verdana or the current ECW UI stack.

Use for:

* post content;
* navigation;
* buttons;
* menus;
* controls;
* explanatory prose;
* ordinary settings.

## Infrastructure

Courier New or the current ECW system/metadata stack.

Use for:

* DIDs;
* AT URIs;
* endpoints;
* service identifiers;
* timestamps;
* provider IDs;
* versions;
* algorithm IDs;
* protocol state;
* diagnostics.

Do not make all Workbench headings monospace.

Technical information should look technical.

Important product hierarchy should look editorial.

---

# 13. Color

Retain ECW semantic color roles while creating a Plumbline editorial palette.

The characteristic light appearance should use approximately these roles:

```text
Paper             warm ivory / warm off-white
Paper recessed    slightly darker neutral
Ink               near-black navy
Secondary ink     charcoal / muted navy
Rule              warm neutral gray
Rule strong       darker neutral
Link              conventional dark blue
Visited           restrained purple
Plumb brass       aged muted brass
Success           green
Warning           amber/yellow semantic color
Error             red/pink semantic color
```

Introduce product-specific semantic tokens such as:

```text
--pl-paper
--pl-paper-recessed
--pl-ink
--pl-ink-secondary
--pl-rule
--pl-rule-strong
--pl-brass
--pl-brass-muted
--pl-provenance-line
--pl-reference-point
```

Brass is an identity color.

It must not replace semantic warning, success, error, or focus colors.

Dark and dim appearances should translate the same hierarchy rather than merely invert the page.

---

# 14. Remove the Generic Grid from Normal Page Mode

The current ECW web implementation may use a visible background grid.

Plumbline Editorial Page Mode should generally not.

The editorial hierarchy should come from:

* baseline rhythm;
* columns;
* alignment;
* vertical rules;
* horizontal rules;
* typography;
* provenance lines;
* margins.

A visible grid may remain appropriate in:

* diagnostics;
* raw protocol tools;
* development surfaces;
* specialized technical Workbench views.

Do not let a decorative grid dominate the social reading experience.

---

# 15. Page Mode

Plumbline specializes ECW Page Mode.

The canonical desktop social layout is:

```text
Navigator | Document Stream | Inspector
```

This is not three equal generic panels.

Each region has a different role.

---

# 16. Navigator

The Navigator should resemble an interactive publication contents column.

Example:

```text
HOME
Notifications
Messages
Search

FEEDS
│ Following
  Custom Feeds
  Discover

LISTS
  …

SERVICES
  …

IDENTITY
  …

BACKUPS
  …
```

Prefer:

* compact headings;
* rules;
* indentation;
* explicit links;
* small symbolic icons;
* a vertical Plumbline selection marker.

Avoid:

* giant sidebar buttons;
* rounded navigation pills;
* excessive containers;
* mobile-tab styling stretched across desktop.

---

# 17. Document Stream

The main feed is a continuous document stream.

Do not present ordinary posts as isolated floating cards.

Conceptually:

```text
◆
│ Alice Morrison  @alice.example · 12m
│
│ Post content appears here.
│
│ Reply 12   Repost 8   Like 42   …
│
────────────────────────────────────────
◆
│ Next post
│ …
```

Use:

* thin rules;
* thread/provenance lines;
* compact author metadata;
* explicit links;
* clear indentation;
* typographic hierarchy;
* normal media embedded in the stream.

Large media can occupy meaningful width without turning the whole post into a floating card.

Density should come from organization, not tiny type.

---

# 18. Inspector

The Inspector is a first-class Plumbline surface.

It is not primarily a recommendation or engagement rail.

It explains the currently selected object.

## Post inspector

May expose:

```text
WHY THIS POST?

Feed
Reason
Ordering
Feed provider
AppView
Moderation sources

POST DETAILS

AT URI
Author DID
Indexed time
Labels
Record source
Record CID
```

## Feed inspector

May expose:

* generator;
* provider;
* feed URI;
* objective;
* algorithm;
* version;
* ordering;
* health;
* moderation sources;
* available alternatives.

## Account inspector

May expose:

* handle;
* DID;
* PDS;
* resolver provenance;
* verification sources;
* relationship state;
* relevant moderation state.

Use:

* definition lists;
* tables;
* marginal-note structures;
* rules;
* expandable detail.

Avoid turning every field group into a card.

---

# 19. Provenance

Consequential externally supplied state should have inspectable provenance.

Examples include:

* feed results;
* ranking explanations;
* labels;
* verification;
* identity resolution;
* service state;
* moderation actions;
* community authority.

Do not fabricate explanations.

If a provider does not expose a reason, say so.

Prefer:

```text
Provider supplied no public ranking explanation
```

over inventing a plausible local explanation.

---

# 20. Why This Post?

Where sufficient information exists, Plumbline should provide a truthful explanation.

Example:

```text
WHY THIS POST?

Feed          Following
Reason        You follow @alice.example
Ordering      Reverse chronological

Feed provider plumblines.uk
AppView       api.bsky.app
Moderation    2 sources

[Inspect details →]
```

For externally ranked feeds, distinguish:

* provider-declared reason;
* client-local explanation;
* information that is unavailable.

Never collapse these into one generic explanation.

---

# 21. Services Workbench

Services belongs in ECW Workbench Mode.

Possible navigator:

```text
SERVICES
├─ Identity
├─ Personal Data Server
├─ AppView
├─ Feed Providers
├─ Moderation Services
├─ Verification
├─ Search
├─ Authorization
├─ Backups
└─ Diagnostics
```

Prefer structured comparison surfaces:

```text
SERVICE    PROVIDER         STATE     ACTIONS
AppView    example.app      Active    Inspect…
Feed       plumblines.uk    Active    Change…
Labeler    example.org      Active    Configure…
PDS        example.host     Active    Inspect…
```

Use a table when the information is tabular.

Do not convert this information into a grid of cards.

---

# 22. Moderation & Reach

Moderation should remain decomposable.

Canonical model:

```text
Source
  ↓
Assertion / Label
  ↓
Rule
  ↓
Client Action
```

The interface should distinguish where technically possible:

* hosting/PDS action;
* AppView behavior;
* labeler assertion;
* community-local moderation;
* direct user relationship;
* local Plumbline display rule.

Do not visually represent every moderation outcome as the same kind of platform judgment.

---

# 23. Identity and Exit

Identity surfaces should make these relationships legible:

```text
Handle
DID
PDS
Resolver
Recovery
Sessions
Authorizations
Backups
Migration
```

Migration should look like ordinary account administration.

Examples:

```text
Export Repository…
Create Backup…
Move to Another PDS…
Revoke Session…
```

Permanent destructive actions remain clearly destructive.

Ordinary portability does not belong in a theatrical "Danger Zone."

---

# 24. Permissions as Delegated Authority

An authorization grants software authority.

Treat permissions accordingly.

The interface should make understandable:

* which authority has been granted;
* to whom;
* why;
* for what scope;
* whether it is currently active;
* how to revoke it.

Prefer progressive permission requests where supported.

Do not request broad authority merely because the application may eventually use it.

---

# 25. Attention Sovereignty

Feeds and ranking systems are tools.

They are not sovereign editors.

Where supported, users should be able to:

* identify the feed;
* identify its provider;
* understand its claimed ordering model;
* inspect available ranking explanations;
* choose another feed;
* choose another provider;
* change local ranking;
* configure local filtering;
* disable unwanted attention mechanisms.

Do not obscure a ranking objective behind the phrase "the algorithm."

---

# 26. Association

Private accounts, protected access, spaces, communities, and related association mechanisms should distinguish:

* individual relationships;
* community-local rules;
* community authority;
* network-wide behavior.

A community ban is not automatically a network ban.

A local membership rule is not automatically an AppView policy.

The interface should preserve those distinctions.

---

# 27. Hypertext

Plumbline remains a web application.

Preserve:

* real links;
* visible link affordances;
* visited-link state where appropriate;
* browser Back and Forward;
* open in new tab/window;
* selectable text;
* copyable URLs;
* page zoom;
* platform keyboard conventions;
* addressable resources.

Advanced surfaces may expose:

```text
Copy AT URI
Copy DID
Inspect Record…
View Raw Data…
```

Expert inspection should not be required for ordinary use.

---

# 28. Controls

Retain ECW structural signification.

A button should look actionable.

An input should look editable.

A selected control should look selected.

Keyboard focus must remain obvious.

For Plumbline Editorial ECW:

* use quieter beveling than classic ECW;
* use fewer enclosing boxes;
* use thinner rules;
* rely more on typography and alignment;
* preserve explicit signifiers;
* avoid flat-interface ambiguity.

The target is:

> **editorial ECW**

not:

> **newspaper skin over ECW controls**

---

# 29. Responsive Behavior

Desktop is the fullest expression of Plumbline.

As width decreases:

1. preserve the Document Stream;
2. demote or overlay the Inspector;
3. collapse the Navigator;
4. preserve explicit access to both;
5. retain provenance and service commands;
6. retain the editorial hierarchy.

Do not simply stack every desktop pane vertically.

Mobile may simplify spatial composition without becoming a different visual system.

---

# 30. Accessibility

Plumbline inherits ECW accessibility requirements.

At minimum preserve:

* keyboard operation;
* visible focus;
* two-tone focus where appropriate;
* forced-colors survival;
* reduced-motion behavior;
* adequate target sizes;
* semantic roles;
* no color-only state;
* screen-reader labels;
* robust text scaling;
* localization;
* RTL compatibility;
* clear loading/error/offline/stale states.

Editorial styling never overrides usability.

---

# 31. Iconography

Use the existing ECW size hierarchy.

## Small UI symbols

16–22px.

Primarily monochrome.

Use for:

* navigation;
* actions;
* menu items;
* compact controls.

## Larger object/application icons

32px and above.

May become dimensional.

The Plumbline application icon should use a geometric plumb bob, preferably aged brass on a restrained field.

Do not put a `P` inside the icon unless later evidence shows the symbol is insufficient.

Do not replace ordinary universal icons with forced plumb-line metaphors.

Home should still look like Home.

Search should still look like Search.

Reserve Plumbline-specific geometry for distinctive concepts such as:

* provenance;
* service source;
* migration;
* inspection;
* rule chain;
* current reference.

---

# 32. Things Plumbline Must Not Become

Do not create:

* fake Windows 98/2000;
* fake desktop chrome;
* generic Y2K nostalgia;
* generic neobrutalism;
* a Web3 dashboard;
* an anarchist zine;
* black/red activist branding;
* circle-A imagery;
* fists;
* flags;
* politician portraits;
* Victorian-newspaper cosplay;
* fake parchment;
* excessive ornamental brass;
* luxury-magazine minimalism;
* mobile-first SaaS stretched across desktop;
* giant floating card stacks;
* pill-heavy navigation;
* excessive glass/transparency;
* a protocol debugger as the default user experience.

The politics should be inferable from what the application lets the user inspect, choose, change, contest, and leave.

---

# 33. Existing Product Behavior Is an Asset

The fork already contains important Plumbline-aligned mechanisms including:

* explicit AppView provider selection;
* no silent AppView substitution;
* feed provenance;
* provider and feed-provider identification;
* provider-supplied ranking explanations;
* local ranking choice;
* "Change provider" and "Change ranking" affordances;
* service boundaries;
* identity-resolution provenance;
* migration machinery;
* protected-account access;
* permissioned/private associations;
* existing constitutional contracts.

The redesign should elevate these mechanisms into a coherent information architecture.

Do not replace working mechanisms with decorative mock equivalents.

---

# 34. Repository Boundary

Use `social-edriffles` as the cross-stack source of truth for product and constitutional documentation.

Use `social-app` for client implementation.

Use `atproto` for protocol/PDS-side implementation where required.

The visual redesign should primarily affect `social-app`.

Do not introduce protocol changes merely to satisfy a visual requirement unless the existing product behavior genuinely lacks data needed by the interface and the change is justified separately.

---

# 35. Acceptance Criteria

A major surface is not complete merely because its colors match.

## Home / feed

A user can determine:

* which feed is active;
* what ordering model is active when knowable;
* who supplies the feed;
* which AppView is involved when relevant;
* how to inspect or change those choices.

The timeline reads as a continuous document rather than generic cards.

## Post

A user can inspect:

* why it appears when knowable;
* relevant provenance;
* applicable moderation sources;
* underlying address/record information at expert depth.

## Services

A user can distinguish:

* PDS;
* AppView;
* feed provider;
* labeler;
* other configurable services.

Changing one must not visually imply changing all others.

## Moderation

A user can distinguish relevant source, assertion, rule, and resulting action.

## Identity

A user can understand:

* handle;
* DID;
* host;
* resolver/provenance where useful;
* backup/export;
* migration.

## Association

A user can distinguish personal, community-local, and network/provider authority.

## Branding

The product presents itself as:

**Plumbline**

at:

**plumblines.uk**

without erasing technically accurate references to Bluesky or other providers.

## Visual identity

The result feels like:

**serious editorial publication + open hypertext + computer-native ECW + seamful ATProto**

rather than:

**Bluesky with a retro stylesheet.**

---

# 36. Final Test

For every major surface ask:

> **What is happening, who is responsible, according to whose rules, what can I change, and what can I use instead?**

Then ask:

> **Does this look like a serious publication that evolved into interactive software rather than a social app wearing a newspaper theme?**

A Plumbline implementation should pass both tests.
