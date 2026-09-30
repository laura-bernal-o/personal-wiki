---
title: Neon Data API Usage
aliases: []
type: concept
source_ids: [networking-tracker-project]
generated_by: gemma4:e4b
reviewed: false
updated: 2026-09-28
---

# Neon Data API Usage

The client interacts with the database exclusively through the Neon Data API, which automatically attaches the user's JWT and enforces RLS.

## Details

<!-- src:networking-tracker-project -->
### In [[Networking Tracker Project Overview]]
- The `@neondatabase/neon-js` client attaches the signed-in user's JWT to every Data API request automatically. ([[raw/Networking Tracker Project#Architecture|§ Architecture]])
- The Data API acts as a REST layer over Postgres, enforcing RLS on every request, regardless of the client's intent. ([[raw/Networking Tracker Project#Architecture|§ Architecture]])
- The client-side code uses the public environment variables `NEXT_PUBLIC_NEON_AUTH_URL` and `NEXT_PUBLIC_NEON_DATA_API_URL`. ([[raw/Networking Tracker Project#Environment variables|§ Environment variables]])
<!-- /src:networking-tracker-project -->

## Related

- [[Networking Tracker Project Overview]] — where this idea is applied
- [[Row Level Security Implementation]] — The Data API is the mechanism that triggers the RLS policies

## Sources

- [[raw/Networking Tracker Project|Networking Tracker Project]] — original, `networking-tracker-project`
