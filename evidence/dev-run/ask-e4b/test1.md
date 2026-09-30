# Evidence card — test1: direct, one source

| field | value |
|---|---|
| run at | 2026-09-28T18:28:31 |
| interaction mode | **ask** (stateless, no chat history, no persona) |
| execution | **local** — Ollama 0.34.3 on 127.0.0.1 |
| network | ONLINE (internet reachable) |
| model | `gemma4:e4b` · 8.0B · Q4_K_M · digest `c6eb396dbd59` |
| embeddings | `embeddinggemma` (local) + BM25, RRF fusion, top 8 raw passages |
| device | Apple M1, 16 GB unified memory, macOS 27.0 |

## Question

> What learning rate did I use for the nanoGPT experiments?

## Expected (written before the run, from `evals/questions.json`)

- **Behavior:** Answer 0.001 (with warmup + cosine decay), citing the Class 4 nanoGPT README.
- **Sources:** raw/Class 4 - nanoGPT Experiment.md
- **Passage:** Learning rate: 0.001, with built-in warmup + cosine decay.

## Retrieved passages (exactly what Gemma saw)

<details><summary><b>[S1]</b> raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > Scope (L229-237) — bm25 6.17, cosine 0.553</summary>

```text
## Scope

- Use the supplied nanoGPT model. Writing the network yourself is optional. PyTorch runs the small model on CPU without an API key or pretrained weights. The vocabulary uses words and punctuation, not characters.

- A working chat interface is required; a terminal or notebook loop is enough. A website, backend service, deployment, GPU purchase, or large-model training is optional. Keep the experiment small enough to inspect.

- [Karpathy's nanoGPT source](https://github.com/karpathy/nanoGPT/blob/3adf61e154c3fe3fca428ad6bc3818b27a3b8291/model.py) is the core reference. The larger [GPT video project](https://github.com/karpathy/ng-video-lecture) is an optional explanation of GPT training. The current lab already uses PyTorch and word tokens.

- Two experiments are required: the starter corpus and your corpus extension for at least two eval categories. More training steps or further experiments are optional. Explain outcomes honestly; improvement is not guaranteed.
```
</details>

<details><summary><b>[S2]</b> raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > Overview (L5-8) — bm25 10.41, cosine 0.496</summary>

```text
## Overview

Use the ready-made notebook to understand the basics of a language model: corpus, tokens, vectors, embeddings, neural networks, and learning. It uses Andrej Karpathy's actual nanoGPT model, using PyTorch and a small word-token transformer. Choose your corpus, training steps, and learning rate, then submit one public GitHub repository URL with your executed notebook and evidence. This miniature model generates short sentences from a narrow corpus, not general chat answers.
```
</details>

<details><summary><b>[S3]</b> raw/Class 4 - nanoGPT Experiment.md § My Custom LLM Experiment (L1-11) — bm25 5.69, cosine 0.578</summary>

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

<details><summary><b>[S4]</b> raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > Open the Notebook (L41-50) — bm25 5.17, cosine 0.540</summary>

```text
## Open the Notebook

- [Custom LLM sample project on GitHub](https://github.com/pepealonso95/custom-llm)

- Local Jupyter or VS Code: install requirements.txt and open custom_llm.ipynb with that Python 3 environment. Colab generally includes PyTorch; notebook setup installs the PDF reader if absent. The pinned nanoGPT model source is provided.

- [Open custom_llm.ipynb in Google Colab. The default CPU runtime is enough.](https://colab.research.google.com/github/pepealonso95/custom-llm/blob/main/custom_llm.ipynb)

- Read [Karpathy's nanoGPT explanation](https://github.com/karpathy/nanoGPT) alongside the notebook. The model uses two blocks, four heads, 64-number embeddings, a 48-token context, PyTorch backpropagation, and AdamW. Whole-word tokenization is a classroom choice, not intrinsic to nanoGPT. Classroom additions make data, evaluation, and learning visible.
```
</details>

<details><summary><b>[S5]</b> raw/Class 4 - nanoGPT Experiment.md § My Custom LLM Experiment > My choices and prediction (L12-36) — bm25 5.28, cosine 0.523</summary>

```text
## My choices and prediction

- **Corpus:** started with the supplied synthetic classroom corpus
  (`CORPUS = "classroom"`), then ran a second experiment with two files added to
  `corpus/`: [`negation.txt`](corpus/negation.txt) and
  [`opposites.txt`](corpus/opposites.txt) — **591 new unique passages**,
  targeting the eval suite's `negation` and `opposites` extension categories.
  Both files are text I generated myself from simple sentence templates (no
  external/copyrighted source, no PDFs), so there are no permission concerns.
  I deliberately used **different names, objects, and adjective pairs** than the
  eval suite's fixtures (the eval uses `hot/cold`, `empty/full`, `noisy/quiet`,
  `ava/tea/milk`, `box/red/blue`, `door/open/closed` — my corpus uses
  `big/small`, `wet/dry`, `sharp/dull`, `maya/leo/...` did-not-buy patterns with
  different objects, etc.) so I teach the *grammatical pattern*, not the
  specific test answers. See [`corpus_manifest.json` (starter run)](llm_runs/20260922T173600_827803Z/corpus_manifest.json)
  and [`corpus_manifest.json` (expanded run)](llm_runs/20260922T173848_430218Z/corpus_manifest.json)
  for exact filenames, hashes, and passage counts.
- **Training steps:** 10 steps first (setup check — confirmed the whole pipeline
  ran end to end), then **3,000 steps** for both real experiments, matching the
  assignment's suggested starting budget. One step updates weights on a batch
  of 32 documents, not the whole corpus, so 3,000 steps means roughly 96,000
  document-draws with repetition against ~4,600–5,200 unique passages.
- **Learning rate: 0.001**, with built-in warmup + cosine decay. This is a
  standard conservative AdamW starting point for a model this size: large
  enough to make real progress in a few thousand steps, small enough (with
```
</details>

<details><summary><b>[S6]</b> raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > My three hyperparameters (L23-27) — bm25 6.13, cosine 0.484</summary>

```text
| Learning rate | `0.0001` | Used the notebook's suggested reference value. This is a conservative rate for Adam on this size of convolutional network — large enough to learn within 100 episodes, small enough to avoid destabilizing Q-value estimates given the small (5,000-transition) replay buffer. |

Evaluation settings were left unchanged as required: the same 5 seeds (`101, 202, 303, 404, 505`),
5% evaluation exploration, and the same step cap, before and after training.
```
</details>

<details><summary><b>[S7]</b> raw/Class 4 - nanoGPT Experiment.md § My Custom LLM Experiment > My choices and prediction (L33-52) — bm25 4.92, cosine 0.494</summary>

```text
document-draws with repetition against ~4,600–5,200 unique passages.
- **Learning rate: 0.001**, with built-in warmup + cosine decay. This is a
  standard conservative AdamW starting point for a model this size: large
  enough to make real progress in a few thousand steps, small enough (with
  warmup) to avoid loss spikes early in training. A much higher rate risks the
  loss oscillating or diverging before warmup finishes; a much lower rate would
  mean 3,000 steps barely moves the loss at all.

**My full written prediction, made before training, is in the notebook itself**
(section 1 of [`custom_llm.py`](custom_llm.py), reproduced in both executed
notebooks): I expected training/validation loss to fall together and level off
well below the untrained baseline (near ln(vocab size)), expected `starter_patterns`
eval cases to improve the most since they're literally the trained sentence
frames, expected `starter_transfer` to improve less, and expected the 24
`extend_corpus` cases to **not** improve from more starter-corpus training,
since that vocabulary simply isn't there. All of that held. What I did *not*
fully predict: that adding negation/opposites *pattern* training with
deliberately different words would still leave the eval's specific `negation`/
`opposites` cases at 0/3 each — see [Fixed language evals](#my-fixed-language-evals) below.
```
</details>

<details><summary><b>[S8]</b> raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > My three hyperparameters (L17-23) — bm25 4.29, cosine 0.489</summary>

```text
## My three hyperparameters

| Setting | Value | Why I chose it |
|---|---|---|
| Exploration | `0.25` | Slightly above the notebook's `0.20` starting point, to see whether a bit more randomness during training helps the agent discover higher-scoring paths (e.g. finding fruit or clearing a section) instead of settling early into a narrow, repeated pattern. My first instinct was "Pac-Man has 4 moves, so 25% exploration ≈ 1-in-4 randomness" — that's not quite right (see the action-space nuance below: the action set actually has 9 entries, and exploration is a per-decision probability, not tied to the action count at all). I kept `0.25` anyway as a deliberate, slightly-higher-than-default value rather than for that original reason. |
| Episodes | `5`, then `100`, then `800` | I first ran `5` episodes as a setup check, then the notebook's starting value of `100` episodes as my main experiment. That 100-episode run's training curve oscillated rather than climbed steadily, so rather than guess whether more training would resolve it, I re-ran at `800` episodes specifically to test that. See "What I expected vs. what I observed" below for what that actually showed. |
| Learning rate | `0.0001` | Used the notebook's suggested reference value. This is a conservative rate for Adam on this size of convolutional network — large enough to learn within 100 episodes, small enough to avoid destabilizing Q-value estimates given the small (5,000-transition) replay buffer. |
```
</details>

## Gemma's answer (verbatim)

```text
The learning rate used for the nanoGPT experiments was 0.001 [S5][S7]. This rate was chosen as a standard conservative AdamW starting point for a model of this size [S5][S7].
```

## Automatic citation check

- [S5] → `raw/Class 4 - nanoGPT Experiment.md § My Custom LLM Experiment > My choices and prediction (L12-36)`
- [S7] → `raw/Class 4 - nanoGPT Experiment.md § My Custom LLM Experiment > My choices and prediction (L33-52)`
- insufficient-evidence response: **no**
- all citations point to retrieved passages: **yes**

## Timing

- wall time 46.66 s (model load 6.23 s) · 2725 prompt tokens · 50 output tokens · 8.6 tok/s
- loaded model memory (ollama ps): {'gemma4:e4b': 3.3}

## Assessment (human review)

_TODO: open each cited passage and verify every claim._
