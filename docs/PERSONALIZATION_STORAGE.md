# Personalization Storage and Multi-device Policy

| Surface | Mechanism | At-rest property | Clearing/eviction |
|---|---|---|---|
| Web | AsyncStorage web backend, account-DID key | Browser storage isolation; not a secure vault | Browser clear/site eviction can remove state; backups are outside app control |
| iOS | AsyncStorage native backend | OS-managed app storage; no secure-deletion claim | App deletion/storage pressure/backups may remove or retain copies |
| Android | AsyncStorage native backend | OS-managed app storage; no secure-deletion claim | App deletion/storage pressure/backups may remove or retain copies |
| Linux/web deployment | Same web backend as web | Browser profile boundary only | User/browser policy controls eviction |

Portable export/import is the guaranteed v1 portability mechanism. Automatic synchronization is intentionally not implemented. Devices diverge independently; importing a profile replaces only personalization state after strict validation. Explicit settings are never overwritten by inferred profile state. Conflicting explicit settings are resolved by the user's latest explicit import, not by provider or learned signals.
