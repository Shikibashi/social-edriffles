# Domain dictionary

This is the shared vocabulary for the community directory cleanup flow.

| Term | Meaning |
| --- | --- |
| Community | A Radlib private-space record with `kind = community`, an owner DID, visibility, and optional display metadata. |
| Directory | The viewer-scoped, paginated result of `listCommunities`; it may contain communities the viewer does not own. |
| Owned community | A directory record whose `ownerDid` exactly equals the authenticated viewer DID. |
| Protocol Space | The Standard Spaces authorization resource associated with a non-public community. |
| Metadata cascade | Removal of the Radlib community row and its dependent members, records, invitations, and related private rows through the database foreign-key cascade. |
| Start from scratch | Delete every community owned by the authenticated viewer, leave other owners' communities intact, and leave the create-community path available. |

Ownership is an authorization boundary, not a display preference. Missing or
untrusted ownership data is treated as not owned by the client.
