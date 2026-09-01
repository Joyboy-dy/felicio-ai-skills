# App Router boundaries

Use a Server Component when the unit primarily composes server data and markup without browser-only interaction. Introduce a Client Component at the narrowest boundary that needs state, effects, event handlers, browser APIs, or client-only libraries.

Check the installed Next.js version before relying on version-sensitive APIs. Keep server-only imports out of client module graphs. Props crossing to client components should be serializable under the framework's current rules.
