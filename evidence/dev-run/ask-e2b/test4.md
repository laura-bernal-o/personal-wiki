# Evidence card — test4: unsupported

| field | value |
|---|---|
| run at | 2026-09-28T18:04:49 |
| interaction mode | **ask** (stateless, no chat history, no persona) |
| execution | **local** — Ollama 0.34.3 on 127.0.0.1 |
| network | ONLINE (internet reachable) |
| model | `gemma4:e2b` · 5.1B · Q4_K_M · digest `7fbdbf8f5e45` |
| embeddings | `embeddinggemma` (local) + BM25, RRF fusion, top 8 raw passages |
| device | Apple M1, 16 GB unified memory, macOS 27.0 |

## Question

> What grade did I receive on the Class 3 Pac-Man assignment?

## Expected (written before the run, from `evals/questions.json`)

- **Behavior:** State that the notes do not contain the grade received. Grading criteria (4/3/3 points) exist in the sources but are not a received grade, so they must not be presented as the answer.
- **Sources:** (none — unsupported question)
- **Passage:** —

## Retrieved passages (exactly what Gemma saw)

<details><summary><b>[S1]</b> raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent (L1-7) — bm25 16.20, cosine 0.477</summary>

```text
# Training a Ms. Pac-Man DQN Agent

Class 3 assignment: train a Deep Q-Network (DQN) on Ms. Pac-Man (`ALE/MsPacman-v5`), choosing
three hyperparameters, and explain what it actually learned. This repository is a submission
copy of the [starter project](https://github.com/pepealonso95/pacman-dqn), with my executed
notebook and results added.
```
</details>

<details><summary><b>[S2]</b> raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > How Evals Affect Your Assignment Grade (L25-33) — bm25 9.55, cosine 0.394</summary>

```text
## How Evals Affect Your Assignment Grade

This assignment is graded out of 10 using the course framework: deliverable quality (4 points), testing & evaluation (3 points), and working result (3 points). The 48-case eval percentage is a model measurement, not your assignment grade. The runner does not calculate your grade.

- Deliverable quality (4 points): submit both executed experiments, readable source code, corpus sources and choices, and a clear README. Explain the model's learning process using your actual token, embedding, gradient, and loss evidence. Explain why you chose at least two extension categories and how your new teaching material addresses their gaps.

- Testing & evaluation (3 points): run all 48 unchanged cases before and after training in each experiment. That means four complete result sets: starter untrained, starter trained, expanded-corpus untrained, and expanded-corpus trained. Save every case, the CSV/JSON results, summaries, and separation checks. Compare all-case success, scorable accuracy, vocabulary coverage, group/category scores, and actual free continuations, alongside the existing loss evidence. Explain failures and whether changes reflect vocabulary coverage, learned patterns, or both.

- Working result (3 points): demonstrate your trained nanoGPT, rerunnable evals on your saved model, and a working interface that produces actual replies from that model. Include launch instructions, the model/run identity, and at least 3 real chat interactions with a screenshot or recording. A terminal or notebook interface is sufficient; a polished website is not required.
```
</details>

<details><summary><b>[S3]</b> raw/Class 4 - nanoGPT Experiment.md § My Custom LLM Experiment (L1-11) — bm25 8.14, cosine 0.380</summary>

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

<details><summary><b>[S4]</b> raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > How Evals Affect Your Assignment Grade (L39-40) — bm25 7.63, cosine 0.390</summary>

```text
Before submitting, make the README show a four-row comparison for the two experiments and their untrained/trained stages, link all four result sets, identify the extension categories and added data, discuss at least one concrete failure or limitation, and link your chat evidence.
```
</details>

<details><summary><b>[S5]</b> raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > How Evals Affect Your Assignment Grade (L33-39) — bm25 6.54, cosine 0.401</summary>

```text
- Working result (3 points): demonstrate your trained nanoGPT, rerunnable evals on your saved model, and a working interface that produces actual replies from that model. Include launch instructions, the model/run identity, and at least 3 real chat interactions with a screenshot or recording. A terminal or notebook interface is sufficient; a polished website is not required.

Running and interpreting the evals is required. Missing runs, omitted cases, a missing corpus-extension comparison, or unsupported conclusions reduce testing & evaluation credit. Results produced by training on test prompts or answer keys are not valid evaluation evidence; remove the leakage and rerun. Incomplete notebook/code or a nonworking model/interface also affects the relevant deliverable or working-result category. Partial credit follows the evidence provided; this is not an automatic all-or-nothing checklist.

There is no minimum model pass rate, leaderboard, or required numerical improvement. A low score, unknown-word cases, or an extension experiment that does not improve can still earn full testing & evaluation credit when the required experiments are complete, the method is valid, and the analysis explains what happened. Unknown-word cases count as zero in the model's all-case metric, not as an automatic deduction of the same percentage from your grade. A high score alone cannot replace valid evaluation, understanding, and a working deliverable.

Before submitting, make the README show a four-row comparison for the two experiments and their untrained/trained stages, link all four result sets, identify the extension categories and added data, discuss at least one concrete failure or limitation, and link your chat evidence.
```
</details>

<details><summary><b>[S6]</b> raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > How the agent works, in plain language (L114-132) — bm25 8.02, cosine 0.358</summary>

```text
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
```
</details>

<details><summary><b>[S7]</b> raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > What I expected vs. what I observed (L43-57) — bm25 6.92, cosine 0.348</summary>

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

<details><summary><b>[S8]</b> raw/Class 4 - nanoGPT Experiment.md § My Custom LLM Experiment > My fixed language evals > By category (trained models) (L230-256) — bm25 2.82, cosine 0.188</summary>

```text
### By category (trained models)

| Category | Starter trained | Expanded trained |
|---|---:|---:|
| domain_context (8) | 8/8 | 8/8 |
| domain_place (8) | 8/8 | 8/8 |
| new_wording (8) | 4/8 | **8/8** |
| grammar (3) | 0/3 (unscorable) | 0/3 (unscorable) |
| opposites (3) | 0/3 (unscorable) | 0/3 (unscorable) |
| negation (3) | 0/3 (unscorable) | 0/3 (unscorable) |
| reference (3) | 0/3 (unscorable) | 0/3 (unscorable) |
| sequence (3) | 0/3 (unscorable) | 0/3 (unscorable) |
| spatial_relations (3) | 0/3 (unscorable) | 0/3 (unscorable) |
| everyday_knowledge (3) | 0/3 (unscorable) | 0/3 (unscorable) |
| categories_and_analogies (3) | 0/3 (unscorable) | 0/3 (unscorable) |

**What worked:** every `starter_patterns` case (the exact trained sentence
frames) reached 16/16 in *both* trained runs. `new_wording` (new phrasings of
starter vocabulary) went from 4/8 to a perfect **8/8** in the expanded run —
this is a real, interesting improvement, and my best guess for why is that
adding 591 more passages using the same core grammar (subject/object/negation
sentences) gave the model more exposure to sentence-final punctuation and
clause boundaries generally, which is exactly the kind of pattern
`new_wording` cases probe, even though those specific cases don't use
negation/opposites vocabulary.

**What did not work, and why:** all 6 of my target `negation`/`opposites`
```
</details>

## Gemma's answer (verbatim)

```text
INSUFFICIENT EVIDENCE: the notes do not say what grade was received on the Class 3 Pac-Man assignment.
```

## Automatic citation check

- (no citations)
- insufficient-evidence response: **yes**
- all citations point to retrieved passages: **yes**

## Timing

- wall time 20.72 s (model load 0.0 s) · 2756 prompt tokens · 26 output tokens · 18.0 tok/s
- loaded model memory (ollama ps): {'gemma4:e2b': 1.89, 'embeddinggemma:latest': 0.67}

## Assessment (human review)

_TODO: open each cited passage and verify every claim._
