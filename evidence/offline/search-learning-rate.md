# wiki search

```text
$ wiki search "learning rate"
search: "learning rate"  (scope=raw, top 3, no answer generated)

[1] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > My three hyperparameters (L23-27)  [ORIGINAL]
    bm25=6.69  cosine=0.425  fused=0.0325
    | | Learning rate | `0.0001` | Used the notebook's suggested reference value. This is a conservative rate for Adam on this size of convolutional network — large enough to learn within 100 episodes, small enough to avoid destabilizing Q-value estimates given the small (5,000-transition) replay buffer. | Evaluation settings were left unchanged as required: the same 5 seeds (`101, 202, 303, 404, 505`), 5% evaluation …

[2] raw/Class 4 - nanoGPT Experiment.md § My Custom LLM Experiment > My evidence > Tokens, embeddings, gradient, and one weight update (L164-186)  [ORIGINAL]
    bm25=6.76  cosine=0.349  fused=0.0315
    | (`-0.99912 × lr`), **not** `-lr * gradient` (which would be `-6.9e-9`, about 1,400× smaller). This is a real, checkable illustration of why the training cell's comment says AdamW "is not simply learning-rate times gradient": on its very first step, Adam's bias-corrected first/second-moment estimates both reduce to the raw gradient itself (`m̂ = g`, `v̂ = g²`), so the update becomes `-lr × g/(|g|+ε) ≈ -lr × …

[3] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > My three hyperparameters (L17-23)  [ORIGINAL]
    bm25=4.04  cosine=0.403  fused=0.0311
    | ## My three hyperparameters | Setting | Value | Why I chose it | |---|---|---| | Exploration | `0.25` | Slightly above the notebook's `0.20` starting point, to see whether a bit more randomness during training helps the agent discover higher-scoring paths (e.g. finding fruit or clearing a section) instead of settling early into a narrow, repeated pattern. My first instinct was "Pac-Man has 4 moves, so 25% …
```
