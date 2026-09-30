---
title: Server-Side Validation
aliases: [Next-Js Backend Validation Layer]
type: concept
source_ids: [networking-tracker-project]
generated_by: gemma4:e4b
reviewed: true
updated: 2026-09-28
---

# Server-Side Validation

A Next.js Route Handler acts as a secondary validation layer, re-validating payloads received via API calls using a specific Zod schema.

## Details

<!-- src:networking-tracker-project -->
### In [[Networking Tracker App]]
- Every create/edit request must first call `POST /api/contacts/validate`, which re-validates the payload using the same `zod` schema as the automated test. ([[raw/Networking Tracker Project#Architecture|§ Architecture]])
- This server-side validation step is separate from (and in addition to) the database-level `CHECK` constraints. ([[raw/Networking Tracker Project#Architecture|§ Architecture]])
- This layer ensures that requests crafted to skip the UI are still rejected with field-level errors. ([[raw/Networking Tracker Project#Architecture|§ Architecture]])
<!-- /src:networking-tracker-project -->

## Related

- [[Networking Tracker App]] — where this idea is applied

## Sources

- [[raw/Networking Tracker Project|Networking Tracker Project]] — original, `networking-tracker-project`
