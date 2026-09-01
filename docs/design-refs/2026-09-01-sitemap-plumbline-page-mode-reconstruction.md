r# Plumbline Page Mode route map

```mermaid
flowchart LR
  Home[Home / Following] --> Profile[Profile]
  Home --> Thread[Post thread]
  Home --> Feed[Custom feed]
  Home --> Discovery[Topic or tag]
  Home --> Community[Community board]
  Home --> Services[Services workbench]
  Services --> Identity[Identity and recovery]
  Services --> Moderation[Moderation and Reach]
  Services --> Diagnostics[Diagnostics]

  subgraph Page_Mode[Editorial Page Mode]
    Home
    Profile
    Thread
    Feed
    Discovery
    Community
  end

  subgraph Workbench_Mode[Capability Workbench Mode]
    Services
    Identity
    Moderation
    Diagnostics
  end
```

## Route role

- Page Mode routes share the full desktop masthead, index-like navigator,
  editorial document stream, and marginal inspector.
- Workbench Mode routes retain explicit tables, controls, service boundaries,
  policy configuration, and diagnostic affordances.
- Messages remain in their existing specialized split-view behavior rather than
  being forced into either layout by this visual correction.
