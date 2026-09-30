# Personal Wiki

Course and project notes, generated from the originals in `raw/` by local Gemma and reviewed by hand.
Start with a project, follow **Related** links to concepts, and use **Sources** at the bottom of any note to open the original evidence.

- [[Sources]] — catalog of the 5 original documents and which notes they produced

## Courses

_Assignment briefs and what each class asked for._

- [[Custom LLM Assignment]] — The Class 4 brief: train a tiny nanoGPT from a notebook, expand its corpus, evaluate it before and after training, and explain how it learns.
- [[Personal Wiki Assignment]] — This assignment requires building a personal wiki using a local Gemma model and Retrieval Augmented Generation (RAG) to power three distinct CLI modes: chat, ask, and search.

## Projects

_Things I built or ran, with results._

- [[Ms Pac-Man DQN Agent]] — My Class 3 project: training a Deep Q-Network to play Ms. Pac-Man from raw screen pixels, then checking what it actually learned.
- [[Networking Tracker App]] — This project is a private, secure contact tracker built using Next.js and Neon Postgres, emphasizing robust data ownership via Row Level Security (RLS).
- [[nanoGPT Experiment]] — My Class 4 project: training Karpathy's nanoGPT from scratch on a small classroom corpus, twice (starter and expanded corpus), and evaluating it honestly.

## Concepts

_Reusable ideas that show up across projects._

- [[Agent Action Space]] — The environment provides 9 discrete actions, though the physical maze structure limits meaningful movement to fewer directions.
- [[Agent Observation Space]] — The agent processes the raw game screen as its observation, which is four stacked grayscale frames.
- [[Causal Self-Attention]] — Attention allows each position to mix information from earlier tokens based on learned compatibility scores between queries and keys, while a triangular mask enforces causality.
- [[Chat Interface Requirements]] — The chat interface must be functional, using the trained model to generate responses without retraining or modifying the corpus.
- [[Corpus Expansion Strategy]] — Corpus expansion involves adding focused files to teach specific patterns, requiring the selection of at least two extension categories.
- [[DQN Learning Rule]] — The network learns by predicting future value and comparing it to a target value derived from the reward and the next state's estimated value.
- [[Explaining Model Learning]] — Understanding the learning process requires tracing specific components like tokens, embeddings, gradients, and weight updates.
- [[Fixed Evaluation Protocol]] — Evaluation requires running the 48-case suite before and after training, ensuring test data never influences model weights.
- [[Gradients and AdamW]] — Optimization involves calculating the gradient of the loss with respect to every parameter, which is then used by the optimizer (like AdamW) to update weights.
- [[Hyperparameter Selection]] — How I picked the training settings for each experiment and why: exploration, episodes, and learning rate for the DQN; training steps and learning rate for nanoGPT.
- [[Learning Rate]] — The step size an optimizer uses to update weights. I chose different values for the Pac-Man DQN (0.0001) and the nanoGPT model (0.001).
- [[Local Model Deployment]] — Choosing a local model requires considering parameter size (E2B, E4B, 26B MoE) and quantization (Q4_0) relative to available system memory (RAM vs VRAM).
- [[Neon Data API]] — The client interacts with the database exclusively through the Neon Data API, which automatically attaches the user's JWT and enforces RLS.
- [[Obsidian Wiki Structure]] — For Obsidian readability, notes should use short, natural filenames (2–6 words) and maintain a clear separation between raw, reviewed, and generated content.
- [[Retrieval Augmented Generation]] — RAG involves retrieving relevant passages from a local index and including them in a prompt to guide the model's answer generation.
- [[Row Level Security]] — RLS is implemented on the `contacts` table using four specific policies to ensure users can only interact with their own data.
- [[Server-Side Validation]] — A Next.js Route Handler acts as a secondary validation layer, re-validating payloads received via API calls using a specific Zod schema.
- [[Temperature Sampling]] — Temperature controls the sampling process by dividing the logits before softmax; lower values sharpen the distribution, while higher values flatten it.
- [[Three Required Modes]] — The system must implement three distinct interaction modes—Chat, Ask, and Search—each with specific functional requirements.
