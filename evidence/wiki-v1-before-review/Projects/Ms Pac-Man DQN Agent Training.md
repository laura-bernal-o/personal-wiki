---
title: Ms Pac-Man DQN Agent Training
aliases: []
type: project
source_ids: [class-3-ms-pacman-dqn]
generated_by: gemma4:e4b
reviewed: false
updated: 2026-09-28
---

# Ms Pac-Man DQN Agent Training

This project details training a Deep Q-Network (DQN) agent on Ms. Pac-Man using specific hyperparameters and analyzing the results across different episode counts.

## Details

<!-- src:class-3-ms-pacman-dqn -->
- The assignment required training a DQN on Ms. Pac-Man using three chosen hyperparameters and explaining the agent's learned behavior. ([[raw/Class 3 - Ms Pacman DQN#Training a Ms. Pac-Man DQN Agent|§ Training a Ms. Pac-Man DQN Agent]])
- The agent's observations are the raw game screen, consisting of four consecutive grayscale 84x84 frames stacked together. ([[raw/Class 3 - Ms Pacman DQN#How the agent works, in plain language|§ How the agent works, in plain language]])
- The agent's actions are drawn from 9 discrete actions: up/down/left/right, four diagonals, and no-op. ([[raw/Class 3 - Ms Pacman DQN#How the agent works, in plain language|§ How the agent works, in plain language]])
- The agent learns by comparing its prediction to `reward + discounted value of the next screen` using a replay buffer. ([[raw/Class 3 - Ms Pacman DQN#How the agent works, in plain language|§ How the agent works, in plain language]])
<!-- /src:class-3-ms-pacman-dqn -->

## Related

- [[Agent Action Space]] — The action space details how the agent interacts with the environment
- [[Hyperparameter Selection]] — The hyperparameters were central to the training process

## Sources

- [[raw/Class 3 - Ms Pacman DQN|Class 3 - Ms Pacman DQN]] — original, `class-3-ms-pacman-dqn`
