# Evidence card — test2: paraphrased, one source

| field | value |
|---|---|
| run at | 2026-09-28T17:56:28 |
| interaction mode | **ask** (stateless, no chat history, no persona) |
| execution | **local** — Ollama 0.34.3 on 127.0.0.1 |
| network | ONLINE (internet reachable) |
| model | `gemma4:e2b` · 5.1B · Q4_K_M · digest `7fbdbf8f5e45` |
| embeddings | `embeddinggemma` (local) + BM25, RRF fusion, top 8 raw passages |
| device | Apple M1, 16 GB unified memory, macOS 27.0 |

## Question

> Why didn't my Pac-Man agent get better at staying alive even after much longer training?

## Expected (written before the run, from `evals/questions.json`)

- **Behavior:** Survival stayed ~20% of the cap (every episode ended with a ghost catching Pac-Man); likely causes: sticky actions (repeat_action_probability=0.25), grayscale preprocessing hiding the blue-ghost color cue, and evasion being a harder credit-assignment problem for a 5,000-transition replay buffer. Cite the Class 3 README.
- **Sources:** raw/Class 3 - Ms Pacman DQN.md
- **Passage:** Limitation: the agent never learns to survive longer ... Sticky actions ... Grayscale preprocessing ... Evasion is a harder credit-assignment problem

## Retrieved passages (exactly what Gemma saw)

<details><summary><b>[S1]</b> raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > What I expected vs. what I observed (L43-57) — bm25 22.71, cosine 0.574</summary>

```text
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
```
</details>

<details><summary><b>[S2]</b> raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > Limitation and next experiment (L142-174) — bm25 19.94, cosine 0.605</summary>

```text
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
```
</details>

<details><summary><b>[S3]</b> raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > What I expected vs. what I observed (L28-47) — bm25 13.79, cosine 0.493</summary>

```text
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
```
</details>

<details><summary><b>[S4]</b> raw/Class 4 - nanoGPT Experiment.md § My Custom LLM Experiment (L1-11) — bm25 12.33, cosine 0.249</summary>

```text
# My Custom LLM Experiment

Class 4 assignment — training [Karpathy's nanoGPT](https://github.com/karpathy/nanoGPT)
(word-token classroom build) from scratch, twice, and evaluating it honestly.
Built from the [starter repo](https://github.com/pepealonso95/custom-llm).

Grading uses deliverable quality **4 points**, testing & evaluation **3 points**,
and working result **3 points**. My model's eval percentage is *not* my grade —
what follows is complete, honest evidence for both experiments, including the
parts that didn't work.
```
</details>

<details><summary><b>[S5]</b> raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > Learning Focus (L207-210) — bm25 10.88, cosine 0.262</summary>

```text
## Learning Focus

The central purpose is understanding how data becomes predictions and how a neural network learns. Your explanation, choices, and visible evidence should support one another. A bigger network, longer training run, or more convincing sample does not replace an explanation. Report limitations rather than claiming the model understands language from a few plausible strings. Losses across different corpora are not a class ranking.
```
</details>

<details><summary><b>[S6]</b> raw/Class 4 - nanoGPT Experiment.md § My Custom LLM Experiment > My evidence > Loss and samples (L124-137) — bm25 4.51, cosine 0.285</summary>

```text
| Untrained | `pear professor bond doctor course harvest team physician journey checking buyer delivery traffic report the lecturer item offering and system <UNK> taste recommended mentioned bus question customer at mortgage nurse in instructor` | `ticket cap taste , bike kite` |
| Halfway (1500) | `our school has a question about the new educator and lesson .` | `the report about the pear explains the juice in detail .` |
| Final (3000) | `the report about the nurse explains the health in detail .` / `the consumer compared the offering after checking the price .` | `the report about the consumer explains the service in detail .` / `we learned about the important therapist during a discussion of patient .` |

Full sample files (4 samples per checkpoint, including any empty/garbled ones):
[starter `samples/`](llm_runs/20260922T173600_827803Z/samples/),
[expanded `samples/`](llm_runs/20260922T173848_430218Z/samples/).

**What changed:** the untrained model outputs unstructured word salad (correct
*token types* for the corpus, no structure). By 1,500 steps both models already
produce grammatical, on-template sentences. Training loss and generated-text
quality both plateau by 3,000 steps — more steps on this corpus would likely
not help much further, since the corpus is a small set of repeated templates.
```
</details>

<details><summary><b>[S7]</b> raw/Class 4 - nanoGPT Experiment.md § My Custom LLM Experiment > What I learned (L393-415) — bm25 3.66, cosine 0.298</summary>

```text
that row. The **embedding table** (or "embedding") is the whole matrix —
   every token's vector, all learned together. Meaning lives entirely in the
   numbers, never in the ID.
3. **What makes this a neural network, and how it learns.** Two transformer
   blocks map token+position embeddings through causal self-attention and a
   feed-forward layer to output scores (logits) over the vocabulary. Loss
   (cross-entropy) measures how much probability the model put on the actual
   next token. `loss.backward()` computes the gradient of that loss with
   respect to *every* parameter (I saved one: `customer`'s first embedding
   coordinate had gradient `0.00069`, meaning "increasing this number very
   slightly would have increased the loss slightly, so decrease it"). AdamW
   then updates the parameter using that gradient plus momentum and
   per-parameter adaptive scaling — not just `lr * gradient` — which is why my
   step-0 update (`-0.0000099913`) is close to but not exactly `-1e-5 *
   0.00069`.
4. **Attention and context.** Attention lets each position mix in information
   from *earlier* tokens in the same sequence, weighted by a learned
   compatibility score between queries and keys; a triangular mask forces
   every position to ignore anything after it, which is what makes this a
   valid next-token predictor instead of a model that could "cheat" by
   peeking ahead.
5. **Probabilities, sampling, and temperature.** The final layer produces one
   score per vocabulary word; softmax turns those into a probability
```
</details>

<details><summary><b>[S8]</b> raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > Your Three Choices (L69-82) — bm25 4.12, cosine 0.242</summary>

```text
## Your Three Choices

- Corpus: first run the supplied classroom corpus, then expand it with focused files for at least two extension-eval categories. Explain your sources, the unique passages added, and what patterns they could teach. Folder-only mode remains available for further experiments.

- Training steps: a positive whole number of weight updates. Try 10 for setup, then 3,000 as a starting training budget. A step is not an entire pass through the corpus. Runtime and sample quality depend on your machine, data, and choices.

- Learning rate: the initial size of the optimizer's updates. Start with 0.001. The notebook uses warmup and cosine decay during training. Explain why excessively large or small updates could be a problem.

- Edit those three settings in section 1 and write your prediction before training. You can keep the defaults, provided you explain your choices.

- The 48-token context window keeps this model small enough to inspect. Longer text is split into passages, not silently truncated. Use data you have permission to share, without confidential or personal records.

- Build the vocabulary only from training text and report both training and held-out unknown-token rates. Other settings are optional experiments. Change one at a time and explain it. Complete and understand the baseline notebook first.
```
</details>

## Gemma's answer (verbatim)

```text
The agent did not learn to survive longer, only to score more efficiently in the short life it received [S2]. The average survival time remained statistically flat across the 100-episode and 800-episode runs, with both runs ending in a game-over for Pac-Man [S1][S2]. This is because the network got better at collecting points within the same short lifespan, rather than learning to evade ghosts better [S2].
```

## Automatic citation check

- [S2] → `raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > Limitation and next experiment (L142-174)`
- [S1] → `raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > What I expected vs. what I observed (L43-57)`
- insufficient-evidence response: **no**
- all citations point to retrieved passages: **yes**

## Timing

- wall time 25.73 s (model load 0.0 s) · 3170 prompt tokens · 96 output tokens · 16.2 tok/s
- loaded model memory (ollama ps): {'gemma4:e2b': 1.89, 'embeddinggemma:latest': 0.67}

## Assessment (human review)

_TODO: open each cited passage and verify every claim._
