---
title: Ms Pac-Man DQN Agent
aliases: [Ms Pac-Man DQN Agent Training]
type: project
source_ids: [class-3-ms-pacman-dqn]
generated_by: gemma4:e4b
reviewed: true
updated: 2026-09-28
---

# Ms Pac-Man DQN Agent

My Class 3 project: training a Deep Q-Network to play Ms. Pac-Man from raw screen pixels, then checking what it actually learned.

## Details

<!-- src:class-3-ms-pacman-dqn -->
- The assignment required training a DQN on Ms. Pac-Man using three chosen hyperparameters and explaining the agent's learned behavior. ([[raw/Class 3 - Ms Pacman DQN#Training a Ms. Pac-Man DQN Agent|§ Training a Ms. Pac-Man DQN Agent]])
- The agent's observations are the raw game screen, consisting of four consecutive grayscale 84x84 frames stacked together. ([[raw/Class 3 - Ms Pacman DQN#How the agent works, in plain language|§ How the agent works, in plain language]])
- The agent's actions are drawn from 9 discrete actions: up/down/left/right, four diagonals, and no-op. ([[raw/Class 3 - Ms Pacman DQN#How the agent works, in plain language|§ How the agent works, in plain language]])
- The agent learns by comparing its prediction to `reward + discounted value of the next screen` using a replay buffer. ([[raw/Class 3 - Ms Pacman DQN#How the agent works, in plain language|§ How the agent works, in plain language]])
- Chosen settings: exploration 0.25, episodes 5 → 100 → 800, learning rate 0.0001. ([[raw/Class 3 - Ms Pacman DQN#My three hyperparameters|§ My three hyperparameters]])
- After 800 episodes the evaluation mean rose from 492.0 to 942.0 (+91.5%) on the same 5 seeds. ([[raw/Class 3 - Ms Pacman DQN#Evaluation scores (before / after 800 episodes)|§ Evaluation scores]])
- Limitation: survival stayed flat at about 20% of the 3,000-decision cap; every episode ended with a ghost catching Pac-Man. Suspected causes: sticky actions (25%), grayscale hiding the blue-ghost cue, and a hard credit-assignment problem for a small replay buffer. ([[raw/Class 3 - Ms Pacman DQN#Limitation and next experiment|§ Limitation and next experiment]])
- Next experiment proposed: raise exploration from 0.25 to about 0.4. ([[raw/Class 3 - Ms Pacman DQN#Limitation and next experiment|§ Limitation and next experiment]])
<!-- /src:class-3-ms-pacman-dqn -->

## Related

- [[Agent Action Space]] — the 9 actions it chooses from
- [[Agent Observation Space]] — what the network sees (4 stacked 84x84 grayscale frames)
- [[DQN Learning Rule]] — how it learns from reward and a target network
- [[Hyperparameter Selection]] — why these settings were chosen
- [[Learning Rate]] — compare with the nanoGPT learning rate

## Sources

- [[raw/Class 3 - Ms Pacman DQN|Class 3 - Ms Pacman DQN]] — original, `class-3-ms-pacman-dqn`
