# Evidence card — ask run

| field | value |
|---|---|
| run at | 2026-09-29T22:32:46 |
| interaction mode | **ask** (stateless, no chat history, no persona) |
| execution | **local** — Ollama 0.34.3 on 127.0.0.1 |
| network | OFFLINE (internet unreachable) |
| model | `gemma4:e4b` · 8.0B · Q4_K_M · digest `c6eb396dbd59` |
| embeddings | `embeddinggemma` (local) + BM25, RRF fusion, top 8 raw passages |
| device | Apple M1, 16 GB unified memory, macOS 27.0 |

## Question

> What was my favorite ghost in the Pac-Man project?

## Retrieved passages (exactly what Gemma saw)

<details><summary><b>[S1]</b> raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent (L1-7) — bm25 12.92, cosine 0.332</summary>

```text
# Training a Ms. Pac-Man DQN Agent

Class 3 assignment: train a Deep Q-Network (DQN) on Ms. Pac-Man (`ALE/MsPacman-v5`), choosing
three hyperparameters, and explain what it actually learned. This repository is a submission
copy of the [starter project](https://github.com/pepealonso95/pacman-dqn), with my executed
notebook and results added.
```
</details>

<details><summary><b>[S2]</b> raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > How the agent works, in plain language (L114-141) — bm25 10.74, cosine 0.340</summary>

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
  action space the network chooses from has 9 entries.
- **Rewards:** the points the game itself awards — eating a pellet, a power pellet, a scared
  ghost, or a fruit. Training rewards are clipped to [-1, +1] to keep learning stable, but every
  score reported above is the real, unclipped game score.
- **Learning rule:** the network predicts an expected future value for each of the 9 moves. It
  learns by comparing that prediction to `reward + discounted value of the next screen`
  (estimated by a slower-updating target copy of the network), using experience it stores in a
  replay buffer rather than only the most recent move.
```
</details>

<details><summary><b>[S3]</b> raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > Limitation and next experiment (L142-174) — bm25 10.29, cosine 0.350</summary>

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

<details><summary><b>[S4]</b> raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > Run the Provided Language Evals (L93-103) — bm25 1.71, cosine 0.199</summary>

```text
## Run the Provided Language Evals

An eval is a fixed test: a prompt, a rule for judging the response, and the model's actual result. The corpus is study material; the eval suite is the exam. Training on the exam can make memorization look like learning.

- Use the 48 synthetic language tests already provided in evals/language_evals.json: 16 reserved prompts for starter-corpus patterns, 8 new phrasings using familiar words, and 24 extension challenges. The extension skills are grammar, opposites, negation, references, sequence, spatial relations, everyday knowledge, and categories/analogies. You do not need to invent the eval suite.

- Read [all 48 language eval cases](https://github.com/pepealonso95/custom-llm/blob/main/evals/language_evals.json) and the [runnable eval guide](https://github.com/pepealonso95/custom-llm/blob/main/evals/README.md) in the sample repository. Keep the cases, four answer choices, answer key, and scoring method unchanged across experiments. Each case includes its category and an explanation. The suite is stored in evals/, outside corpus/.

- Keep eval prompts, reference answers, scoring rules, and generated eval outputs out of all training inputs, including PDFs, Markdown, generated classroom sentences, and copied chat logs. Do not use eval text to build the vocabulary or update weights. Ordinary words and underlying subject knowledge may overlap; the test items themselves must stay separate. Keep CORPUS_FOLDER pointed only at corpus/, never at the whole project.

- The notebook removes generated classroom sentences containing reserved test prefixes before splitting data or building the vocabulary. It rejects exact test prefixes in imported files and rejects corpus folders that include evals/ or the project root. Inspect eval_separation.json, the file manifest, and your training text. These checks do not catch all paraphrases or copied answer lists. The existing 90/10 loss panels remain separate measurements.
```
</details>

<details><summary><b>[S5]</b> raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > Open the Notebook (L41-50) — bm25 1.65, cosine 0.190</summary>

```text
## Open the Notebook

- [Custom LLM sample project on GitHub](https://github.com/pepealonso95/custom-llm)

- Local Jupyter or VS Code: install requirements.txt and open custom_llm.ipynb with that Python 3 environment. Colab generally includes PyTorch; notebook setup installs the PDF reader if absent. The pinned nanoGPT model source is provided.

- [Open custom_llm.ipynb in Google Colab. The default CPU runtime is enough.](https://colab.research.google.com/github/pepealonso95/custom-llm/blob/main/custom_llm.ipynb)

- Read [Karpathy's nanoGPT explanation](https://github.com/karpathy/nanoGPT) alongside the notebook. The model uses two blocks, four heads, 64-number embeddings, a 48-token context, PyTorch backpropagation, and AdamW. Whole-word tokenization is a classroom choice, not intrinsic to nanoGPT. Classroom additions make data, evaluation, and learning visible.
```
</details>

<details><summary><b>[S6]</b> raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > Scope (L229-237) — bm25 1.67, cosine 0.186</summary>

```text
## Scope

- Use the supplied nanoGPT model. Writing the network yourself is optional. PyTorch runs the small model on CPU without an API key or pretrained weights. The vocabulary uses words and punctuation, not characters.

- A working chat interface is required; a terminal or notebook loop is enough. A website, backend service, deployment, GPU purchase, or large-model training is optional. Keep the experiment small enough to inspect.

- [Karpathy's nanoGPT source](https://github.com/karpathy/nanoGPT/blob/3adf61e154c3fe3fca428ad6bc3818b27a3b8291/model.py) is the core reference. The larger [GPT video project](https://github.com/karpathy/ng-video-lecture) is an optional explanation of GPT training. The current lab already uses PyTorch and word tokens.

- Two experiments are required: the starter corpus and your corpus extension for at least two eval categories. More training steps or further experiments are optional. Explain outcomes honestly; improvement is not guaranteed.
```
</details>

<details><summary><b>[S7]</b> raw/Class 5 - Personal Wiki Brief.md § Class 5 Assignment: Personal Wiki with Local Gemma + RAG > Build Your Personal Wiki (L51-56) — bm25 1.74, cosine 0.168</summary>

```text
## Build Your Personal Wiki

Choose at least three sources you can inspect, such as course notes, research articles, or personal project notes. Keep original sources unchanged in vault/raw/. Store generated summaries and linked pages separately in vault/wiki/. Have your harness read a source, send its text and instructions to local Gemma, and save a reviewed wiki page with a reference back to the source. Connect related pages with links and update vault/index.md so a reader and your retrieval code can find them.

Split long text into useful passages and retain the source path and page or section when available. Explain how much text your harness passes to Gemma. Review generated summaries against the originals. Correct invented or misleading statements in the wiki rather than changing the evidence.
```
</details>

<details><summary><b>[S8]</b> raw/Class 5 - Personal Wiki Brief.md § Class 5 Assignment: Personal Wiki with Local Gemma + RAG > Submission (L77-79) — bm25 2.61, cosine 0.138</summary>

```text
## Submission

Create your own public GitHub repository containing your CLI and harness code, README, shareable wiki sources and pages, and test evidence. Do not commit model weights or credentials. Submit your own project repository through the course submission portal.
```
</details>

## Gemma's answer (verbatim)

```text
INSUFFICIENT EVIDENCE: the notes do not say what the user's favorite ghost was in the Pac-Man project. The passages discuss the agent's learning process, which involves rewards for eating a scared ghost [S2], and the agent's limitation regarding survival time [S3].
```

## Automatic citation check

- [S2] → `raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > How the agent works, in plain language (L114-141)`
- [S3] → `raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > Limitation and next experiment (L142-174)`
- insufficient-evidence response: **yes**
- all citations point to retrieved passages: **yes**

## Timing

- wall time 48.64 s (model load 0.0 s) · 3023 prompt tokens · 62 output tokens · 8.3 tok/s
- loaded model memory (ollama ps): {'gemma4:e4b': 3.3, 'embeddinggemma:latest': 0.67}

## Assessment (human review)

**Verdict: PASS.** The favorite-ghost claim was only said in chat (see `mode-checks.md`). Ask mode has no chat history, retrieved only raw sources, and answered INSUFFICIENT EVIDENCE. The extra context sentences (S2: rewards for eating a scared ghost; S3: survival limitation) are accurate.
