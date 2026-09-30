---
title: DQN Learning Rule
aliases: []
type: concept
source_ids: [class-3-ms-pacman-dqn]
generated_by: gemma4:e4b
reviewed: false
updated: 2026-09-28
---

# DQN Learning Rule

The network learns by predicting future value and comparing it to a target value derived from the reward and the next state's estimated value.

## Details

<!-- src:class-3-ms-pacman-dqn -->
### In [[Ms Pac-Man DQN Agent Training]]
- The network predicts an expected future value for each of the 9 moves. ([[raw/Class 3 - Ms Pacman DQN#How the agent works, in plain language|§ How the agent works, in plain language]])
- Learning occurs by comparing the prediction to `reward + discounted value of the next screen` using a replay buffer. ([[raw/Class 3 - Ms Pacman DQN#How the agent works, in plain language|§ How the agent works, in plain language]])
<!-- /src:class-3-ms-pacman-dqn -->

## Related

- [[Ms Pac-Man DQN Agent Training]] — This explains the core mechanism of the agent's learning

## Sources

- [[raw/Class 3 - Ms Pacman DQN|Class 3 - Ms Pacman DQN]] — original, `class-3-ms-pacman-dqn`
