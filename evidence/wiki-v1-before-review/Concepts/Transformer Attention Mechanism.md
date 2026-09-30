---
title: Transformer Attention Mechanism
aliases: []
type: concept
source_ids: [class-4-nanogpt-experiment]
generated_by: gemma4:e4b
reviewed: false
updated: 2026-09-28
---

# Transformer Attention Mechanism

Attention allows each position to mix information from earlier tokens based on learned compatibility scores between queries and keys, while a triangular mask enforces causality.

## Details

<!-- src:class-4-nanogpt-experiment -->
### In [[Custom LLM Experiment Training]]
- Attention weights are determined by a learned compatibility score between queries and keys. ([[raw/Class 4 - nanoGPT Experiment#What I learned|§ What I learned]])
- A triangular mask forces every position to ignore tokens that appear after it, ensuring valid next-token prediction. ([[raw/Class 4 - nanoGPT Experiment#What I learned|§ What I learned]])
<!-- /src:class-4-nanogpt-experiment -->

## Related

- [[Custom LLM Experiment Training]] — The mechanism is fundamental to how the LLM processes context

## Sources

- [[raw/Class 4 - nanoGPT Experiment|Class 4 - nanoGPT Experiment]] — original, `class-4-nanogpt-experiment`
