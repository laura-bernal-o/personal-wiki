---
title: Networking Tracker App
aliases: [Networking Tracker Project Overview]
type: project
source_ids: [networking-tracker-project]
generated_by: gemma4:e4b
reviewed: true
updated: 2026-09-28
---

# Networking Tracker App

This project is a private, secure contact tracker built using Next.js and Neon Postgres, emphasizing robust data ownership via Row Level Security (RLS). It features full CRUD operations and enforces data privacy at the database level.

## Details

<!-- src:networking-tracker-project -->
- The application allows users to sign up, sign in, and sign out using email/password. ([[raw/Networking Tracker Project#Features|§ Features]])
- Contacts are private to the owner, enforced by Postgres Row Level Security (RLS) rather than just the UI. ([[raw/Networking Tracker Project#Features|§ Features]])
- The technology stack uses Next.js (App Router) with TypeScript for the frontend and backend, and Tailwind CSS with shadcn/ui for styling. ([[raw/Networking Tracker Project#Technology stack|§ Technology stack]])
- The architecture involves the client calling the Neon Data API, which validates the JWT and enforces RLS on the Postgres `contacts` table. ([[raw/Networking Tracker Project#Architecture|§ Architecture]])
- The local setup requires Node 20+, a Neon account, and running `db/schema.sql` as `neondb_owner` to set up tables and grants. ([[raw/Networking Tracker Project#Local setup|§ Local setup]])
<!-- /src:networking-tracker-project -->

## Related

- [[Neon Data API]] — how the client reaches Postgres
- [[Row Level Security]] — how contacts stay private per user
- [[Server-Side Validation]] — the second validation layer before writes

## Sources

- [[raw/Networking Tracker Project|Networking Tracker Project]] — original, `networking-tracker-project`
