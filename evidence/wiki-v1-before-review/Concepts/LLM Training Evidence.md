---
title: LLM Training Evidence
aliases: []
type: concept
source_ids: [class-4-assignment-brief]
generated_by: gemma4:e4b
reviewed: false
updated: 2026-09-28
---

# LLM Training Evidence

Understanding the learning process requires tracing specific components like tokens, embeddings, gradients, and weight updates.

## Details

<!-- src:class-4-assignment-brief -->
### In [[Building Custom LLM Assignment]]
- The explanation must trace one word from text to its ID and 64-number vector, and explain one saved gradient and weight update. ([[raw/Class 4 - Assignment Brief#README Requirements|§ README Requirements]])
- The loss plot uses fixed panels of at most 20 training and 20 validation documents, averaging non-padding next-token targets. ([[raw/Class 4 - Assignment Brief#Evaluate the Model Fairly|§ Evaluate the Model Fairly]])
- The model uses PyTorch backpropagation and AdamW, and the context window is 48 tokens. ([[raw/Class 4 - Assignment Brief#Open the Notebook|§ Open the Notebook]])
<!-- /src:class-4-assignment-brief -->

## Related

- [[Building Custom LLM Assignment]] — where this idea is applied
- [[Hyperparameter Selection]] — Learning rate and training steps are key hyperparameters

## Sources

- [[raw/Class 4 - Assignment Brief|Class 4 - Assignment Brief]] — original, `class-4-assignment-brief`
