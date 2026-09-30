---
title: Custom LLM Experiment Training
aliases: []
type: project
source_ids: [class-4-nanogpt-experiment]
generated_by: gemma4:e4b
reviewed: false
updated: 2026-09-28
---

# Custom LLM Experiment Training

This note details the process of training a custom LLM from scratch using nanoGPT, comparing a starter corpus run against an expanded corpus run incorporating negation and opposite pairs.

## Details

<!-- src:class-4-nanogpt-experiment -->
- The experiment involved training a model from scratch using the nanoGPT framework, starting with a synthetic classroom corpus. ([[raw/Class 4 - nanoGPT Experiment#My Custom LLM Experiment|§ My Custom LLM Experiment]])
- The expanded corpus added 591 new unique passages using negation and opposite pairs, deliberately using different words than the evaluation suite fixtures. ([[raw/Class 4 - nanoGPT Experiment#My choices and prediction|§ My choices and prediction]])
- Training utilized 3,000 steps with a learning rate of 0.001, employing built-in warmup and cosine decay. ([[raw/Class 4 - nanoGPT Experiment#My choices and prediction|§ My choices and prediction]])
- The expanded run achieved 100% accuracy on the 'new_wording' category, while the specific negation/opposites eval cases remained unscorable due to vocabulary limitations. ([[raw/Class 4 - nanoGPT Experiment#By category (trained models)|§ By category (trained models)]])
- The model demonstrated a limitation regarding third-person pronouns (`she`/`he`) as they were never present in the training corpus. ([[raw/Class 4 - nanoGPT Experiment#My chat interface|§ My chat interface]])
<!-- /src:class-4-nanogpt-experiment -->

## Related

- [[Agent Action Space]] — Related to general LLM generation concepts
- [[Agent Observation Space]] — Related to general LLM generation concepts
- [[Chat Interface Requirements]] — Describes the implementation of the chat interface

## Sources

- [[raw/Class 4 - nanoGPT Experiment|Class 4 - nanoGPT Experiment]] — original, `class-4-nanogpt-experiment`
