---
title: Gradients and AdamW
aliases: [Gradient Descent Optimization]
type: concept
source_ids: [class-4-nanogpt-experiment]
generated_by: gemma4:e4b
reviewed: true
updated: 2026-09-28
---

# Gradients and AdamW

Optimization involves calculating the gradient of the loss with respect to every parameter, which is then used by the optimizer (like AdamW) to update weights.

## Details

<!-- src:class-4-nanogpt-experiment -->
### In [[nanoGPT Experiment]]
- Loss.backward() computes the gradient of the loss with respect to every parameter, which is saved as the gradient. ([[raw/Class 4 - nanoGPT Experiment#What I learned|§ What I learned]])
- AdamW updates parameters using the gradient plus momentum and per-parameter adaptive scaling, not simply `lr * gradient`. ([[raw/Class 4 - nanoGPT Experiment#What I learned|§ What I learned]])
<!-- /src:class-4-nanogpt-experiment -->

## Related

- [[nanoGPT Experiment]] — The entire training process relies on this optimization method

## Sources

- [[raw/Class 4 - nanoGPT Experiment|Class 4 - nanoGPT Experiment]] — original, `class-4-nanogpt-experiment`
