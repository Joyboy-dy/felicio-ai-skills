# Next.js implementation patterns

## Reads

Keep privileged credentials and authorization on the server. Choose static/cached/request-specific behavior from data freshness and security requirements, then use APIs supported by the installed Next.js version.

## Writes

Validate and authorize mutations at the server boundary. On success, update/revalidate affected UI using the project's established mechanism. Treat optimistic UI as an experience layer, not proof of persistence.

## Shared logic

Move reusable business/domain logic out of route components/handlers when multiple routes need it or it deserves independent tests. Do not create layers solely to satisfy a fixed folder diagram.
