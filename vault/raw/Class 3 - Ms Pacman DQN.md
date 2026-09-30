# Training a Ms. Pac-Man DQN Agent

Class 3 assignment: train a Deep Q-Network (DQN) on Ms. Pac-Man (`ALE/MsPacman-v5`), choosing
three hyperparameters, and explain what it actually learned. This repository is a submission
copy of the [starter project](https://github.com/pepealonso95/pacman-dqn), with my executed
notebook and results added.

## Open and run

1. Clone this repository.
2. Open [`pacman_dqn.ipynb`](pacman_dqn.ipynb) in Jupyter, VS Code, or Google Colab (a Python
   3.11–3.13 kernel is required).
3. Section 1 already contains my three chosen values (below). Choose **Run All** to reproduce
   the experiment, or just read the saved cell outputs — they're already executed and visible.
4. The notebook installs its own packages and detects GPU/MPS/CPU automatically.

## My three hyperparameters

| Setting | Value | Why I chose it |
|---|---|---|
| Exploration | `0.25` | Slightly above the notebook's `0.20` starting point, to see whether a bit more randomness during training helps the agent discover higher-scoring paths (e.g. finding fruit or clearing a section) instead of settling early into a narrow, repeated pattern. My first instinct was "Pac-Man has 4 moves, so 25% exploration ≈ 1-in-4 randomness" — that's not quite right (see the action-space nuance below: the action set actually has 9 entries, and exploration is a per-decision probability, not tied to the action count at all). I kept `0.25` anyway as a deliberate, slightly-higher-than-default value rather than for that original reason. |
| Episodes | `5`, then `100`, then `800` | I first ran `5` episodes as a setup check, then the notebook's starting value of `100` episodes as my main experiment. That 100-episode run's training curve oscillated rather than climbed steadily, so rather than guess whether more training would resolve it, I re-ran at `800` episodes specifically to test that. See "What I expected vs. what I observed" below for what that actually showed. |
| Learning rate | `0.0001` | Used the notebook's suggested reference value. This is a conservative rate for Adam on this size of convolutional network — large enough to learn within 100 episodes, small enough to avoid destabilizing Q-value estimates given the small (5,000-transition) replay buffer. |

Evaluation settings were left unchanged as required: the same 5 seeds (`101, 202, 303, 404, 505`),
5% evaluation exploration, and the same step cap, before and after training.

## What I expected vs. what I observed

**Expected:** With only 100 training episodes — a small fraction of what published DQN results
use (the original DeepMind DQN paper trains on tens of millions of decisions) — I expected at
best a small, noisy improvement over the untrained network, not competent play.

**Stage 1 (100 episodes) — observed:** That's roughly what happened. The mean evaluation score
improved modestly (492.0 → 554.0, +12.6%), but individual seeds moved in both directions. The
25-episode rolling average of the *training* scores oscillated rather than climbed steadily
(616 → a peak of 816 around episode 50 → down to 645 → back up to 703 by episode 100), so I
couldn't honestly tell from that run alone whether more training would keep improving things, or
whether the network had hit an instability ceiling from the small replay buffer.

**Stage 2 (800 episodes) — observed:** I re-ran the full experiment from scratch (same
exploration and learning rate, since this notebook always starts from a fresh untrained network —
there's no partial-resume) at 800 episodes specifically to resolve that question. The result was
genuinely informative, in a way I didn't fully expect:

- The **evaluation mean nearly doubled**: 492.0 → 942.0 (+91.5%), clearly stronger than the
  100-episode run. So more training data did help the network's actual decision quality.
- But **survival time barely moved**: average steps per training episode was 593.6 in the *first*
  25 episodes and 573.6 in the *last* 25 — statistically flat across all 800 episodes, at
  roughly 20% of the 3,000-decision cap both times. **Every single episode in both runs (100/100,
  then 800/800) ended the same way: a ghost caught Pac-Man.** None hit the time limit.

Put together: 8x more training made the network noticeably better at *scoring* (likely eating
pellets and vulnerable ghosts more efficiently in the time it has), but did essentially nothing
to help it *survive longer*. That's a specific, useful finding, not just "it got better" — see
the limitation below for why I think that split happened.

## Actual training record

| Metric | 100-episode run | 800-episode run (final) |
|---|---|---|
| Completed episodes | 100 / 100 requested | 800 / 800 requested |
| Total decisions | 59,549 | 473,552 |
| Learning updates | 14,638 | 118,139 |
| Elapsed time | 601 s (~10 min) | 4,493 s (~75 min) |
| Hardware | Apple Silicon (macOS 14, arm64), PyTorch MPS backend | same |
| Interrupted? | No | No |

Source: [`results/training_summary.json`](results/training_summary.json),
[`results/config.json`](results/config.json) (800-episode run). An earlier 500-episode attempt
was intentionally stopped partway and re-run at 800 instead of being resumed, since this notebook
always trains a fresh network per run — see the process note at the end of "Limitation and next
experiment" below.

## Evaluation scores (before / after 800 episodes)

Same 5 seeds, 5% exploration, same step cap, before and after training. Full data:
[`results/comparison.json`](results/comparison.json).

| Seed | Baseline (untrained) | After 800 episodes |
|---|---|---|
| 101 | 350 | 480 |
| 202 | 500 | 1580 |
| 303 | 320 | 1350 |
| 404 | 800 | 620 |
| 505 | 490 | 680 |
| **Mean** | **492.0** | **942.0** |

## Training plot

![Training dashboard: score, loss, and exploration over 800 episodes](results/training_dashboard.png)

Score per episode (top), training loss (middle), and exploration rate (bottom, constant at 25%
after the 1,000-decision random warm-up). Full per-episode data:
[`results/training.csv`](results/training.csv).

## Gameplay evidence

| Stage | GIF |
|---|---|
| Untrained (episode 0) | ![Untrained gameplay](results/untrained.gif) |
| After 200 episodes | ![After 200 episodes](results/intermediate_ep200.gif) |
| After 400 episodes | ![After 400 episodes](results/intermediate_ep400.gif) |
| After 600 episodes | ![After 600 episodes](results/intermediate_ep600.gif) |
| After 800 episodes | ![After 800 episodes](results/intermediate_ep800.gif) |
| Best trained (5-game evaluation, best of 5) | ![Best trained gameplay](results/trained_best.gif) |

Each GIF shows **only the first 20 seconds** of a game that can run up to ~200 seconds — the
on-screen score at the point a GIF cuts off is *not* the game's final score, just wherever
Pac-Man was 20 seconds in. The real final scores are the ones in the table above and in
[`results/demo_scores.json`](results/demo_scores.json) (32 checkpoints, every 25 episodes,
one game each — noisier than the 5-seed table since each is a single game).

## How the agent works, in plain language

- **Observations:** the agent doesn't see game variables (score, position, ghost state) directly.
  It sees the raw game screen — four consecutive grayscale 84x84 frames stacked together, so it
  can infer motion (which way things are moving) from a single snapshot.
- **Actions:** the environment exposes 9 discrete actions — up/down/left/right, four diagonals,
  and no-op — mirroring the 8 physical positions of an Atari joystick plus center. One decision
  covers 4 emulator frames.

  **Nuance on the diagonals:** the classic Pac-Man/Ms. Pac-Man maze is a fixed grid of
  horizontal and vertical corridors — there's no 45° path for a sprite to actually travel. I
  tested this directly rather than assume: I cloned the exact same in-game moment and compared
  where Pac-Man ended up after holding each of the 9 actions from that identical starting point.
  When one component of a diagonal was blocked by a wall, the game simply fell back to the open
  cardinal direction (e.g. `UPLEFT` landed in the exact same spot as `LEFT` alone; `DOWNRIGHT`
  matched `RIGHT` alone). So a "diagonal" action isn't ignored, but it isn't a genuine diagonal
  move either — it behaves like "turn onto whichever of these two directions the corridor
  currently allows." Practically, at any given position in the maze, Pac-Man only ever has
  somewhere between 2–4 *meaningfully different* directions available, even though the raw
  action space the network chooses from has 9 entries.
- **Rewards:** the points the game itself awards — eating a pellet, a power pellet, a scared
  ghost, or a fruit. Training rewards are clipped to [-1, +1] to keep learning stable, but every
  score reported above is the real, unclipped game score.
- **Learning rule:** the network predicts an expected future value for each of the 9 moves. It
  learns by comparing that prediction to `reward + discounted value of the next screen`
  (estimated by a slower-updating target copy of the network), using experience it stores in a
  replay buffer rather than only the most recent move.

## Limitation and next experiment

**Limitation: the agent never learns to survive longer — only to score more efficiently in the
short life it gets.** This is the clearest finding from comparing the 100- and 800-episode runs.
In *both* runs, 100% of episodes ended in a real game-over (a ghost caught Pac-Man) — 100/100 and
then 800/800 — and none came anywhere near the 3,000-decision time limit. Average survival was
~595 decisions (~20% of the cap) after 100 episodes and ~592 decisions (still ~20%) after 800
episodes: statistically unchanged despite 8x more training. So while the evaluation *score*
nearly doubled, that's almost certainly because the network got better at collecting points
*within* roughly the same short lifespan (efficient pellet paths, occasionally eating vulnerable
ghosts after a power pellet for a big bonus), not because it learned to evade ghosts better.

I looked into why survival specifically might be stuck, rather than just guessing:

- **Sticky actions are baked into both training and evaluation and can't be tuned away.** The
  environment uses `repeat_action_probability=0.25` — 25% of the time, the game ignores the
  agent's chosen move and repeats its *previous* move instead. Near a ghost, a blocked "turn
  away" command is often fatal. This adds real, structural death risk that no amount of training
  removes, since it's part of the fixed environment config, not a learnable pattern.
- **Grayscale preprocessing may hide the one color cue evasion depends on.** After a power
  pellet, ghosts turn blue/flashing to signal "safe to approach" — a color-only cue that could
  collapse into similar gray values at 84x84 resolution, making the single highest-value
  evasion/pursuit decision harder to learn from pixels alone.
- **Evasion is a harder credit-assignment problem than pellet collection at this scale.** Pellets
  are static and reward every nearby step; reacting correctly to moving, chasing ghosts requires
  more varied experience than a 5,000-transition replay buffer and infrequent (every 1,000
  decisions) target-network syncing are well-suited to generalize from.

**Next experiment:** since two runs at very different episode counts (100 vs. 800) left survival
time completely flat, episode count doesn't look like the lever that fixes this specific problem.
I'd change **exploration** next — increase it from 0.25 to something like 0.4 — on the reasoning
that the agent needs more varied close-call encounters with ghosts to have anything to learn an
evasion policy *from*, and pushing more randomness into training is a more direct way to generate
those than simply repeating the same exploration rate for longer.

*Note on process: I originally started a 500-episode run to test the 100-episode run's
oscillating training curve, but killed it partway (~200/500 episodes) once I decided to go
straight to 800 instead — this notebook always trains from a fresh network per run, so there was
no way to combine that partial run with a longer one anyway.*

## Files

- Executed notebook (all outputs visible, saved after the final 800-episode run): [`pacman_dqn.ipynb`](pacman_dqn.ipynb)
- Selected evidence for this README: [`results/`](results/)
- The full run folders (`pacman_runs/20260915_162142_648428/` for the 100-episode run,
  `pacman_runs/20260915_221004_958016/` for the final 800-episode run — including all model
  checkpoints and each run's ZIP) are generated by the notebook and excluded from this repository
  by `.gitignore` (checkpoints alone are ~6.7 MB each). They're kept locally; the evidence needed
  to review this submission is committed under `results/` and embedded above.

## Setup notes

Verified locally with Python 3.12.0, PyTorch 2.14.0, Gymnasium 1.3.0, ALE 0.11.2, on macOS 14
(Apple Silicon, MPS backend). See [`results/config.json`](results/config.json) for the full
package/version record captured by the notebook itself.
