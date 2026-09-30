---
title: nanoGPT Experiment
aliases: [Custom LLM Experiment Training]
type: project
source_ids: [class-4-nanogpt-experiment]
generated_by: gemma4:e4b
reviewed: true
updated: 2026-09-28
---

# nanoGPT Experiment

My Class 4 project: training Karpathy's nanoGPT from scratch on a small classroom corpus, twice (starter and expanded corpus), and evaluating it honestly.

## Details

<!-- src:class-4-nanogpt-experiment -->
- The experiment involved training a model from scratch using the nanoGPT framework, starting with a synthetic classroom corpus. ([[raw/Class 4 - nanoGPT Experiment#My Custom LLM Experiment|§ My Custom LLM Experiment]])
- The expanded corpus added 591 new unique passages using negation and opposite pairs, deliberately using different words than the evaluation suite fixtures. ([[raw/Class 4 - nanoGPT Experiment#My choices and prediction|§ My choices and prediction]])
- Training utilized 3,000 steps with a learning rate of 0.001, employing built-in warmup and cosine decay. ([[raw/Class 4 - nanoGPT Experiment#My choices and prediction|§ My choices and prediction]])
- The expanded run achieved 100% accuracy on the 'new_wording' category, while the specific negation/opposites eval cases remained unscorable due to vocabulary limitations. ([[raw/Class 4 - nanoGPT Experiment#By category (trained models)|§ By category (trained models)]])
- The model demonstrated a limitation regarding third-person pronouns (`she`/`he`) as they were never present in the training corpus. ([[raw/Class 4 - nanoGPT Experiment#My chat interface|§ My chat interface]])
<!-- /src:class-4-nanogpt-experiment -->

## Related

- [[Causal Self-Attention]] — how the model uses earlier tokens
- [[Chat Interface Requirements]] — the chat.py interface built for the assignment
- [[Corpus Expansion Strategy]] — the negation and opposites files added in the second run
- [[Custom LLM Assignment]] — the brief this experiment answers
- [[Gradients and AdamW]] — the traced weight update
- [[Hyperparameter Selection]] — training steps and learning rate choices
- [[Learning Rate]] — 0.001 with warmup + cosine decay
- [[Temperature Sampling]] — how generation settings changed the samples

## Sources

- [[raw/Class 4 - nanoGPT Experiment|Class 4 - nanoGPT Experiment]] — original, `class-4-nanogpt-experiment`
