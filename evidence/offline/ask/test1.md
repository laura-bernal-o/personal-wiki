# Evidence card — test1: direct, one source

| field | value |
|---|---|
| run at | 2026-09-29T22:29:13 |
| interaction mode | **ask** (stateless, no chat history, no persona) |
| execution | **local** — Ollama 0.34.3 on 127.0.0.1 |
| network | OFFLINE (internet unreachable) |
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

<details><summary><b>[S1]</b> raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > Overview (L5-8) — bm25 11.00, cosine 0.496</summary>

```text
## Overview

Use the ready-made notebook to understand the basics of a language model: corpus, tokens, vectors, embeddings, neural networks, and learning. It uses Andrej Karpathy's actual nanoGPT model, using PyTorch and a small word-token transformer. Choose your corpus, training steps, and learning rate, then submit one public GitHub repository URL with your executed notebook and evidence. This miniature model generates short sentences from a narrow corpus, not general chat answers.
```
</details>

<details><summary><b>[S2]</b> raw/Class 4 - nanoGPT Experiment.md § My Custom LLM Experiment (L1-11) — bm25 6.12, cosine 0.578</summary>

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

<details><summary><b>[S3]</b> raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > Scope (L229-237) — bm25 6.51, cosine 0.553</summary>

```text
## Scope

- Use the supplied nanoGPT model. Writing the network yourself is optional. PyTorch runs the small model on CPU without an API key or pretrained weights. The vocabulary uses words and punctuation, not characters.

- A working chat interface is required; a terminal or notebook loop is enough. A website, backend service, deployment, GPU purchase, or large-model training is optional. Keep the experiment small enough to inspect.

- [Karpathy's nanoGPT source](https://github.com/karpathy/nanoGPT/blob/3adf61e154c3fe3fca428ad6bc3818b27a3b8291/model.py) is the core reference. The larger [GPT video project](https://github.com/karpathy/ng-video-lecture) is an optional explanation of GPT training. The current lab already uses PyTorch and word tokens.

- Two experiments are required: the starter corpus and your corpus extension for at least two eval categories. More training steps or further experiments are optional. Explain outcomes honestly; improvement is not guaranteed.
```
</details>

<details><summary><b>[S4]</b> raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > Open the Notebook (L41-50) — bm25 5.45, cosine 0.540</summary>

```text
## Open the Notebook

- [Custom LLM sample project on GitHub](https://github.com/pepealonso95/custom-llm)

- Local Jupyter or VS Code: install requirements.txt and open custom_llm.ipynb with that Python 3 environment. Colab generally includes PyTorch; notebook setup installs the PDF reader if absent. The pinned nanoGPT model source is provided.

- [Open custom_llm.ipynb in Google Colab. The default CPU runtime is enough.](https://colab.research.google.com/github/pepealonso95/custom-llm/blob/main/custom_llm.ipynb)

- Read [Karpathy's nanoGPT explanation](https://github.com/karpathy/nanoGPT) alongside the notebook. The model uses two blocks, four heads, 64-number embeddings, a 48-token context, PyTorch backpropagation, and AdamW. Whole-word tokenization is a classroom choice, not intrinsic to nanoGPT. Classroom additions make data, evaluation, and learning visible.
```
</details>

<details><summary><b>[S5]</b> raw/Class 4 - nanoGPT Experiment.md § My Custom LLM Experiment > My choices and prediction (L12-36) — bm25 5.55, cosine 0.523</summary>

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

<details><summary><b>[S6]</b> raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > My three hyperparameters (L23-27) — bm25 6.69, cosine 0.484</summary>

```text
| Learning rate | `0.0001` | Used the notebook's suggested reference value. This is a conservative rate for Adam on this size of convolutional network — large enough to learn within 100 episodes, small enough to avoid destabilizing Q-value estimates given the small (5,000-transition) replay buffer. |

Evaluation settings were left unchanged as required: the same 5 seeds (`101, 202, 303, 404, 505`),
5% evaluation exploration, and the same step cap, before and after training.
```
</details>

<details><summary><b>[S7]</b> raw/Class 4 - nanoGPT Experiment.md § My Custom LLM Experiment > My evidence > Tokens, embeddings, gradient, and one weight update (L164-186) — bm25 7.39, cosine 0.466</summary>

```text
(`-0.99912 × lr`), **not** `-lr * gradient` (which would be `-6.9e-9`, about
1,400× smaller). This is a real, checkable illustration of why the training
cell's comment says AdamW "is not simply learning-rate times gradient": on
its very first step, Adam's bias-corrected first/second-moment estimates both
reduce to the raw gradient itself (`m̂ = g`, `v̂ = g²`), so the update becomes
`-lr × g/(|g|+ε) ≈ -lr × sign(gradient)` — the optimizer moves the parameter
by (approximately) one learning-rate step in the direction that reduces loss,
regardless of how large or small the gradient itself was. Later steps, once
the running averages have accumulated history from many gradients, behave
differently. Warmup also kept this very first step's learning rate tiny —
`1e-05`, not the full `0.001`.

**Next-token probability comparison** for the prefix `"the customer"` (starter run):

| | Before training (top 5) | After training (top 5) |
|---|---|---|
| Predictions | `customer` 1.6%, `bus` 1.1%, `educator` 1.0%, `us` 1.0%, `application` 1.0% | `reviewed` 17.8%, `recommended` 17.1%, `ordered` 16.9%, `selected` 16.3%, `compared` 16.0% |

Before training the distribution is nearly flat (all candidates within a point
of each other — essentially noise from random initialization). After training
the model heavily favors the verbs that actually follow "the customer" in the
training frames (`the customer ordered/reviewed/compared/returned/recommended/
selected the product ...`) — a direct, inspectable readout of what the network
```
</details>

<details><summary><b>[S8]</b> raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > My three hyperparameters (L17-23) — bm25 4.67, cosine 0.489</summary>

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
For the nanoGPT experiments, the learning rate used was 0.001 [S5]. This learning rate was used with built-in warmup + cosine decay [S5].
```

## Automatic citation check

- [S5] → `raw/Class 4 - nanoGPT Experiment.md § My Custom LLM Experiment > My choices and prediction (L12-36)`
- insufficient-evidence response: **no**
- all citations point to retrieved passages: **yes**

## Timing

- wall time 46.99 s (model load 6.65 s) · 2824 prompt tokens · 40 output tokens · 8.8 tok/s
- loaded model memory (ollama ps): {'gemma4:e4b': 3.3}

## Assessment (human review)

**Verdict: PASS (retrieval ✅, answer ✅, citations ✅)**

- Retrieval: the expected passage (`My choices and prediction`, which contains "Learning rate: 0.001, with built-in warmup + cosine decay") was retrieved as [S5]. Retrieval also surfaced the Class 4 *brief*, which recommends starting at 0.001; that would have been the wrong source for "what did **I** use".
- Answer: "0.001 … with built-in warmup + cosine decay". I opened `raw/Class 4 - nanoGPT Experiment.md` lines 34–35: the claim is stated there verbatim.
- Citations: both sentences cite [S5] (my own README, not the brief), so they're correct.
