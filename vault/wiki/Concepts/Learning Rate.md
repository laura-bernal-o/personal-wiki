---
title: Learning Rate
aliases: [LLM Training Learning Rate]
type: concept
source_ids: [class-3-ms-pacman-dqn, class-4-nanogpt-experiment]
generated_by: gemma4:e4b
reviewed: true
updated: 2026-09-28
---
# Learning Rate

The step size an optimizer uses to update weights. I chose different values for the Pac-Man DQN (0.0001) and the nanoGPT model (0.001).

## Details

<!-- src:class-3-ms-pacman-dqn -->
### In [[Ms Pac-Man DQN Agent]]
- Learning rate `0.0001`: the notebook's suggested reference value, described as conservative for Adam on this size of convolutional network. ([[raw/Class 3 - Ms Pacman DQN#My three hyperparameters|§ My three hyperparameters]])
- Reason given: large enough to learn within 100 episodes, small enough to avoid destabilizing Q-value estimates with the small 5,000-transition replay buffer. ([[raw/Class 3 - Ms Pacman DQN#My three hyperparameters|§ My three hyperparameters]])
<!-- /src:class-3-ms-pacman-dqn -->

<!-- src:class-4-nanogpt-experiment -->
### In [[nanoGPT Experiment]]
- A learning rate of 0.001 was used, which is a standard conservative AdamW starting point for this model size. ([[raw/Class 4 - nanoGPT Experiment#My choices and prediction|§ My choices and prediction]])
- A much higher rate risks loss oscillation or divergence before warmup finishes, while a much lower rate results in minimal loss movement over 3,000 steps. ([[raw/Class 4 - nanoGPT Experiment#My choices and prediction|§ My choices and prediction]])
<!-- /src:class-4-nanogpt-experiment -->

## Related

- [[Gradients and AdamW]] — the learning rate scales the optimizer's update
- [[Hyperparameter Selection]] — the learning rate was one of the three settings chosen for each experiment
- [[Ms Pac-Man DQN Agent]] — used 0.0001
- [[nanoGPT Experiment]] — used 0.001 with warmup + cosine decay

## Sources

- [[raw/Class 3 - Ms Pacman DQN|Class 3 - Ms Pacman DQN]] — original, `class-3-ms-pacman-dqn`
- [[raw/Class 4 - nanoGPT Experiment|Class 4 - nanoGPT Experiment]] — original, `class-4-nanogpt-experiment`
