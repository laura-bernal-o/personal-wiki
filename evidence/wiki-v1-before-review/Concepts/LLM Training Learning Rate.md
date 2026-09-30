---
title: LLM Training Learning Rate
aliases: []
type: concept
source_ids: [class-4-nanogpt-experiment]
generated_by: gemma4:e4b
reviewed: false
updated: 2026-09-28
---

# LLM Training Learning Rate

The learning rate was set to 0.001 with built-in warmup and cosine decay to ensure progress without early loss spikes.

## Details

<!-- src:class-4-nanogpt-experiment -->
### In [[Custom LLM Experiment Training]]
- A learning rate of 0.001 was used, which is a standard conservative AdamW starting point for this model size. ([[raw/Class 4 - nanoGPT Experiment#My choices and prediction|§ My choices and prediction]])
- A much higher rate risks loss oscillation or divergence before warmup finishes, while a much lower rate results in minimal loss movement over 3,000 steps. ([[raw/Class 4 - nanoGPT Experiment#My choices and prediction|§ My choices and prediction]])
<!-- /src:class-4-nanogpt-experiment -->

## Related

- [[Custom LLM Experiment Training]] — This concept was central to the overall training process

## Sources

- [[raw/Class 4 - nanoGPT Experiment|Class 4 - nanoGPT Experiment]] — original, `class-4-nanogpt-experiment`
