# Staging

Staging is a separate HTTPS origin and deployment identity built with `EXPO_PUBLIC_ENV=staging`. It must not reuse production deployment credentials or redirect origins. Fixture integrations are allowed only when labeled; production capability labels remain truthful.

# Rollback

Promote the previous immutable static deployment when a smoke check fails. Rollback changes client code only; it does not revert identity, PDS, associations, personalization, or remote service state. Re-run root validation and record the restored artifact checksum and deployment ID.
