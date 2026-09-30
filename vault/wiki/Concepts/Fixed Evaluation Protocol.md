---
title: Fixed Evaluation Protocol
aliases: []
type: concept
source_ids: [class-4-assignment-brief]
generated_by: gemma4:e4b
reviewed: true
updated: 2026-09-28
---

# Fixed Evaluation Protocol

Evaluation requires running the 48-case suite before and after training, ensuring test data never influences model weights.

## Details

<!-- src:class-4-assignment-brief -->
### In [[Custom LLM Assignment]]
- The 48 synthetic language tests must be kept outside the training corpus. ([[raw/Class 4 - Assignment Brief#Run the Provided Language Evals|§ Run the Provided Language Evals]])
- The evaluation must be run before and after training for both the starter and expanded-corpus experiments. ([[raw/Class 4 - Assignment Brief#Run the Provided Language Evals|§ Run the Provided Language Evals]])
- The test items must never enter the model's prompt or its weight updates. ([[raw/Class 4 - Assignment Brief#Example: Corpus vs. Evals|§ Example: Corpus vs. Evals]])
<!-- /src:class-4-assignment-brief -->

## Related

- [[Custom LLM Assignment]] — This protocol is central to the assignment grading

## Sources

- [[raw/Class 4 - Assignment Brief|Class 4 - Assignment Brief]] — original, `class-4-assignment-brief`
