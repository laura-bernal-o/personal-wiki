---
title: Hyperparameter Selection
aliases: []
type: concept
source_ids: [class-3-ms-pacman-dqn]
generated_by: gemma4:e4b
reviewed: false
updated: 2026-09-28
---

# Hyperparameter Selection

The hyperparameters used for the DQN training included exploration rate, episode count, and learning rate.

## Details

<!-- src:class-3-ms-pacman-dqn -->
### In [[Ms Pac-Man DQN Agent Training]]
- Exploration was set to `0.25` to test if slightly more randomness helps discover higher-scoring paths. ([[raw/Class 3 - Ms Pacman DQN#My three hyperparameters|§ My three hyperparameters]])
- Episodes were tested at 5, 100, and 800 to observe training curve behavior. ([[raw/Class 3 - Ms Pacman DQN#My three hyperparameters|§ My three hyperparameters]])
- The learning rate was set to `0.0001` as a conservative rate for Adam on this network size. ([[raw/Class 3 - Ms Pacman DQN#My three hyperparameters|§ My three hyperparameters]])
<!-- /src:class-3-ms-pacman-dqn -->

## Related

- [[Ms Pac-Man DQN Agent Training]] — These settings were applied during the agent's training

## Sources

- [[raw/Class 3 - Ms Pacman DQN|Class 3 - Ms Pacman DQN]] — original, `class-3-ms-pacman-dqn`
