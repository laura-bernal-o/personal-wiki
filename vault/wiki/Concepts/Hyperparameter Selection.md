---
title: Hyperparameter Selection
aliases: []
type: concept
source_ids: [class-3-ms-pacman-dqn, class-4-nanogpt-experiment]
generated_by: gemma4:e4b
reviewed: true
updated: 2026-09-28
---

# Hyperparameter Selection

How I picked the training settings for each experiment and why: exploration, episodes, and learning rate for the DQN; training steps and learning rate for nanoGPT.

## Details

<!-- src:class-3-ms-pacman-dqn -->
### In [[Ms Pac-Man DQN Agent]]
- Exploration was set to `0.25` to test if slightly more randomness helps discover higher-scoring paths. ([[raw/Class 3 - Ms Pacman DQN#My three hyperparameters|§ My three hyperparameters]])
- Episodes were tested at 5, 100, and 800 to observe training curve behavior. ([[raw/Class 3 - Ms Pacman DQN#My three hyperparameters|§ My three hyperparameters]])
- The learning rate was set to `0.0001` as a conservative rate for Adam on this network size. ([[raw/Class 3 - Ms Pacman DQN#My three hyperparameters|§ My three hyperparameters]])
<!-- /src:class-3-ms-pacman-dqn -->

<!-- src:class-4-nanogpt-experiment -->
### In [[nanoGPT Experiment]]
- Training steps: 10 as a setup check, then 3,000 for both real experiments, matching the suggested starting budget. ([[raw/Class 4 - nanoGPT Experiment#My choices and prediction|§ My choices and prediction]])
- Learning rate 0.001 with warmup + cosine decay (see [[Learning Rate]]). ([[raw/Class 4 - nanoGPT Experiment#My choices and prediction|§ My choices and prediction]])
<!-- /src:class-4-nanogpt-experiment -->

## Related

- [[DQN Learning Rule]] — Hyperparameters govern the application of the learning rule
- [[Learning Rate]] — compares the learning rate chosen in both experiments
- [[Ms Pac-Man DQN Agent]] — exploration 0.25, episodes 5→100→800, learning rate 0.0001
- [[nanoGPT Experiment]] — 3,000 steps, learning rate 0.001

## Sources

- [[raw/Class 3 - Ms Pacman DQN|Class 3 - Ms Pacman DQN]] — original, `class-3-ms-pacman-dqn`
- [[raw/Class 4 - nanoGPT Experiment|Class 4 - nanoGPT Experiment]] — original, `class-4-nanogpt-experiment`
