---
title: Temperature Sampling
aliases: [Temperature Sampling Decoding]
type: concept
source_ids: [class-4-nanogpt-experiment]
generated_by: gemma4:e4b
reviewed: true
updated: 2026-09-28
---

# Temperature Sampling

Temperature controls the sampling process by dividing the logits before softmax; lower values sharpen the distribution, while higher values flatten it.

## Details

<!-- src:class-4-nanogpt-experiment -->
### In [[nanoGPT Experiment]]
- Temperature divides the logits before softmax, which is a decoding-time choice, not a training one. ([[raw/Class 4 - nanoGPT Experiment#Temperature comparison|§ Temperature comparison]])
- A low temperature (e.g., 0.3) results in nearly identical, safe, high-probability continuations, whereas a high temperature (e.g., 1.2) increases variety. ([[raw/Class 4 - nanoGPT Experiment#Temperature comparison|§ Temperature comparison]])
<!-- /src:class-4-nanogpt-experiment -->

## Related

- [[nanoGPT Experiment]] — This concept was demonstrated when comparing different sampling temperatures

## Sources

- [[raw/Class 4 - nanoGPT Experiment|Class 4 - nanoGPT Experiment]] — original, `class-4-nanogpt-experiment`
