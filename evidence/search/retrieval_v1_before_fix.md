# Retrieval check v1 (before fixes) — BM25 (no stemming) + embeddinggemma, RRF, top 5, raw only

## test1
```
search: "What learning rate did I use for the nanoGPT experiments?"  (scope=raw, top 5, no answer generated)

[1] raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > Scope (L229-237)  [ORIGINAL]
    bm25=8.40  cosine=0.553  fused=0.0323
    | ## Scope - Use the supplied nanoGPT model. Writing the network yourself is optional. PyTorch runs the small model on CPU without an API key or pretrained weights. The vocabulary uses words and punctuation, not characters. - A working chat interface is required; a terminal or notebook loop is enough. A website, backend service, deployment, GPU purchase, or large-model training is optional. Keep the experiment small …

[2] raw/Class 4 - nanoGPT Experiment.md § My Custom LLM Experiment (L1-11)  [ORIGINAL]
    bm25=6.20  cosine=0.578  fused=0.0318
    | # My Custom LLM Experiment Class 4 assignment — training [Karpathy's nanoGPT](https://github.com/karpathy/nanoGPT) (word-token classroom build) from scratch, twice, and evaluating it honestly. Built from the [starter repo](https://github.com/pepealonso95/custom-llm). Grading uses deliverable quality **4 points**, testing & evaluation **3 points**, and working result **3 points**. My model's eval percentage is *not* …

[3] raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > Overview (L5-8)  [ORIGINAL]
    bm25=9.96  cosine=0.496  fused=0.0313
    | ## Overview Use the ready-made notebook to understand the basics of a language model: corpus, tokens, vectors, embeddings, neural networks, and learning. It uses Andrej Karpathy's actual nanoGPT model, using PyTorch and a small word-token transformer. Choose your corpus, training steps, and learning rate, then submit one public GitHub repository URL with your executed notebook and evidence. This miniature model …

[4] raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > Open the Notebook (L41-50)  [ORIGINAL]
    bm25=5.90  cosine=0.540  fused=0.0310
    | ## Open the Notebook - [Custom LLM sample project on GitHub](https://github.com/pepealonso95/custom-llm) - Local Jupyter or VS Code: install requirements.txt and open custom_llm.ipynb with that Python 3 environment. Colab generally includes PyTorch; notebook setup installs the PDF reader if absent. The pinned nanoGPT model source is provided. - [Open custom_llm.ipynb in Google Colab. The default CPU runtime is …

[5] raw/Class 4 - nanoGPT Experiment.md § My Custom LLM Experiment > My choices and prediction (L12-36)  [ORIGINAL]
    bm25=3.70  cosine=0.523  fused=0.0284
    | ## My choices and prediction - **Corpus:** started with the supplied synthetic classroom corpus (`CORPUS = "classroom"`), then ran a second experiment with two files added to `corpus/`: [`negation.txt`](corpus/negation.txt) and [`opposites.txt`](corpus/opposites.txt) — **591 new unique passages**, targeting the eval suite's `negation` and `opposites` extension categories. Both files are text I generated myself from …
```

## test2
```
search: "Why didn't my Pac-Man agent get better at staying alive even after much longer training?"  (scope=raw, top 5, no answer generated)

[1] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > What I expected vs. what I observed (L43-57)  [ORIGINAL]
    bm25=17.80  cosine=0.574  fused=0.0325
    | there's no partial-resume) at 800 episodes specifically to resolve that question. The result was genuinely informative, in a way I didn't fully expect: - The **evaluation mean nearly doubled**: 492.0 → 942.0 (+91.5%), clearly stronger than the 100-episode run. So more training data did help the network's actual decision quality. - But **survival time barely moved**: average steps per training episode was 593.6 in …

[2] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > Limitation and next experiment (L142-160)  [ORIGINAL]
    bm25=15.89  cosine=0.605  fused=0.0325
    | ## Limitation and next experiment **Limitation: the agent never learns to survive longer — only to score more efficiently in the short life it gets.** This is the clearest finding from comparing the 100- and 800-episode runs. In *both* runs, 100% of episodes ended in a real game-over (a ghost caught Pac-Man) — 100/100 and then 800/800 — and none came anywhere near the 3,000-decision time limit. Average survival was …

[3] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > Limitation and next experiment (L172-181)  [ORIGINAL]
    bm25=11.62  cosine=0.502  fused=0.0312
    | I'd change **exploration** next — increase it from 0.25 to something like 0.4 — on the reasoning that the agent needs more varied close-call encounters with ghosts to have anything to learn an evasion policy *from*, and pushing more randomness into training is a more direct way to generate those than simply repeating the same exploration rate for longer. *Note on process: I originally started a 500-episode run to …

[4] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > What I expected vs. what I observed (L28-47)  [ORIGINAL]
    bm25=10.14  cosine=0.493  fused=0.0305
    | ## What I expected vs. what I observed **Expected:** With only 100 training episodes — a small fraction of what published DQN results use (the original DeepMind DQN paper trains on tens of millions of decisions) — I expected at best a small, noisy improvement over the untrained network, not competent play. **Stage 1 (100 episodes) — observed:** That's roughly what happened. The mean evaluation score improved …

[5] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > How the agent works, in plain language (L114-132)  [ORIGINAL]
    bm25=13.94  cosine=0.402  fused=0.0294
    | ## How the agent works, in plain language - **Observations:** the agent doesn't see game variables (score, position, ghost state) directly. It sees the raw game screen — four consecutive grayscale 84x84 frames stacked together, so it can infer motion (which way things are moving) from a single snapshot. - **Actions:** the environment exposes 9 discrete actions — up/down/left/right, four diagonals, and no-op — …
```

## test3
```
search: "Compare the learning rates I chose for the Pac-Man DQN and the nanoGPT model."  (scope=raw, top 5, no answer generated)

[1] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > My three hyperparameters (L17-23)  [ORIGINAL]
    bm25=9.81  cosine=0.559  fused=0.0325
    | ## My three hyperparameters | Setting | Value | Why I chose it | |---|---|---| | Exploration | `0.25` | Slightly above the notebook's `0.20` starting point, to see whether a bit more randomness during training helps the agent discover higher-scoring paths (e.g. finding fruit or clearing a section) instead of settling early into a narrow, repeated pattern. My first instinct was "Pac-Man has 4 moves, so 25% …

[2] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent (L1-7)  [ORIGINAL]
    bm25=9.84  cosine=0.519  fused=0.0315
    | # Training a Ms. Pac-Man DQN Agent Class 3 assignment: train a Deep Q-Network (DQN) on Ms. Pac-Man (`ALE/MsPacman-v5`), choosing three hyperparameters, and explain what it actually learned. This repository is a submission copy of the [starter project](https://github.com/pepealonso95/pacman-dqn), with my executed notebook and results added.

[3] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > My three hyperparameters (L23-27)  [ORIGINAL]
    bm25=8.20  cosine=0.547  fused=0.0315
    | | Learning rate | `0.0001` | Used the notebook's suggested reference value. This is a conservative rate for Adam on this size of convolutional network — large enough to learn within 100 episodes, small enough to avoid destabilizing Q-value estimates given the small (5,000-transition) replay buffer. | Evaluation settings were left unchanged as required: the same 5 seeds (`101, 202, 303, 404, 505`), 5% evaluation …

[4] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > Training plot (L89-96)  [ORIGINAL]
    bm25=6.76  cosine=0.536  fused=0.0296
    | ## Training plot ![Training dashboard: score, loss, and exploration over 800 episodes](results/training_dashboard.png) Score per episode (top), training loss (middle), and exploration rate (bottom, constant at 25% after the 1,000-decision random warm-up). Full per-episode data: [`results/training.csv`](results/training.csv).

[5] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > What I expected vs. what I observed (L28-47)  [ORIGINAL]
    bm25=6.69  cosine=0.535  fused=0.0291
    | ## What I expected vs. what I observed **Expected:** With only 100 training episodes — a small fraction of what published DQN results use (the original DeepMind DQN paper trains on tens of millions of decisions) — I expected at best a small, noisy improvement over the untrained network, not competent play. **Stage 1 (100 episodes) — observed:** That's roughly what happened. The mean evaluation score improved …
```

## test4
```
search: "What grade did I receive on the Class 3 Pac-Man assignment?"  (scope=raw, top 5, no answer generated)

[1] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent (L1-7)  [ORIGINAL]
    bm25=10.65  cosine=0.477  fused=0.0328
    | # Training a Ms. Pac-Man DQN Agent Class 3 assignment: train a Deep Q-Network (DQN) on Ms. Pac-Man (`ALE/MsPacman-v5`), choosing three hyperparameters, and explain what it actually learned. This repository is a submission copy of the [starter project](https://github.com/pepealonso95/pacman-dqn), with my executed notebook and results added.

[2] raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > How Evals Affect Your Assignment Grade (L25-33)  [ORIGINAL]
    bm25=9.37  cosine=0.394  fused=0.0320
    | ## How Evals Affect Your Assignment Grade This assignment is graded out of 10 using the course framework: deliverable quality (4 points), testing & evaluation (3 points), and working result (3 points). The 48-case eval percentage is a model measurement, not your assignment grade. The runner does not calculate your grade. - Deliverable quality (4 points): submit both executed experiments, readable source code, …

[3] raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > How Evals Affect Your Assignment Grade (L33-39)  [ORIGINAL]
    bm25=7.03  cosine=0.401  fused=0.0315
    | - Working result (3 points): demonstrate your trained nanoGPT, rerunnable evals on your saved model, and a working interface that produces actual replies from that model. Include launch instructions, the model/run identity, and at least 3 real chat interactions with a screenshot or recording. A terminal or notebook interface is sufficient; a polished website is not required. Running and interpreting the evals is …

[4] raw/Class 4 - nanoGPT Experiment.md § My Custom LLM Experiment (L1-11)  [ORIGINAL]
    bm25=8.21  cosine=0.380  fused=0.0313
    | # My Custom LLM Experiment Class 4 assignment — training [Karpathy's nanoGPT](https://github.com/karpathy/nanoGPT) (word-token classroom build) from scratch, twice, and evaluating it honestly. Built from the [starter repo](https://github.com/pepealonso95/custom-llm). Grading uses deliverable quality **4 points**, testing & evaluation **3 points**, and working result **3 points**. My model's eval percentage is *not* …

[5] raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > How Evals Affect Your Assignment Grade (L39-40)  [ORIGINAL]
    bm25=7.26  cosine=0.390  fused=0.0312
    | Before submitting, make the README show a four-row comparison for the two experiments and their untrained/trained stages, link all four result sets, identify the extension categories and added data, discuss at least one concrete failure or limitation, and link your chat evidence.
```
