---
title: Agent Action Space
aliases: []
type: concept
source_ids: [class-3-ms-pacman-dqn]
generated_by: gemma4:e4b
reviewed: false
updated: 2026-09-28
---

# Agent Action Space

The environment provides 9 discrete actions, though the physical maze structure limits meaningful movement to fewer directions.

## Details

<!-- src:class-3-ms-pacman-dqn -->
### In [[Ms Pac-Man DQN Agent Training]]
- The environment exposes 9 discrete actions: up/down/left/right, four diagonals, and no-op. ([[raw/Class 3 - Ms Pacman DQN#How the agent works, in plain language|§ How the agent works, in plain language]])
- Diagonal actions often behave like the cardinal direction that the corridor allows, rather than a true diagonal move. ([[raw/Class 3 - Ms Pacman DQN#How the agent works, in plain language|§ How the agent works, in plain language]])
<!-- /src:class-3-ms-pacman-dqn -->

## Related

- [[Ms Pac-Man DQN Agent Training]] — This details the output space the agent selects from

## Sources

- [[raw/Class 3 - Ms Pacman DQN|Class 3 - Ms Pacman DQN]] — original, `class-3-ms-pacman-dqn`
