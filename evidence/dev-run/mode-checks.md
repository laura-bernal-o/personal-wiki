# Mode boundary checks — 2026-09-28 19:02

- model: `gemma4:e4b` · Q4_K_M · digest `c6eb396dbd59` · execution **local** (Ollama 0.34.3)
- network: ONLINE (internet reachable)
- device: Apple M1, 16 GB unified memory, macOS 27.0

## 1. Chat (one continuous conversation with Wren)

### capabilities: “what can you help me with?”

_Expected:_ explain real capabilities; no notes search, no citations, no refusal

**Harness trace:** `· no notes searched · 22.3s`

```text
I'm here to help you with your notes. Think of me as a sounding board for your studying.

I can help you:
*   Brainstorm, outline, draft, or rewrite text for your assignments.
*   Look things up in your personal wiki for course or project details.

If you need to look up something specific from your notes, just tell me what it is, and I can use the `search_notes` tool.

What are you working on right now?
```

### capabilities: “what can we do?”

_Expected:_ same: conversational, no notes search

**Harness trace:** `· no notes searched · 20.1s`

```text
We can work on anything related to your coursework or projects.

For example, we could:
1.  **Review Material:** If you have a confusing concept, we can talk through it.
2.  **Drafting:** If you need to write an essay section or code explanation, I can help you structure it or rewrite it.
3.  **Checking Notes:** If you're unsure about a requirement or a detail from a past assignment, I can check your wiki for what you've already written down.

Just point me in a direction. Do you want to work on the Ms. Pac-Man DQN, the nanoGPT assignment, or something else?
```

### draft: “Draft a 5-step study plan for reviewing my Pac-Man DQN project before a quiz.”

_Expected:_ may search notes; any facts about the project must carry [S#] citations; plan labeled as suggestion

**Harness trace:** `· no notes searched · 41.0s`

```text
A five-step plan sounds manageable. Since this is for review, we should focus on understanding, not just reading.

Here is a draft plan. We can adjust the depth of each step later.

**5-Step Pac-Man DQN Review Plan**

1.  **Concept Mapping (Theory):** Outline the core components of DQN. What is the relationship between the state, action, and Q-value function? (This tests understanding, not just memory.)
2.  **Algorithm Walkthrough (Process):** Trace the entire DQN loop step-by-step. From collecting an experience tuple $\langle s, a, r, s' \rangle$ to updating the target network.
3.  **Code Review (Implementation):** Skim through the key functions in your code. Can you explain *why* you used a specific function (e.g., why use a separate target network)?
4.  **Failure Analysis (Troubleshooting):** Identify 2-3 potential failure points in the project (e.g., instability, high variance). How would you debug or fix them?
5.  **Practice Scenarios (Application):** Work through a hypothetical scenario. "If the rewards were much sparser, what part of the learning process would struggle most?"

How does that look? We can turn this into actionable bullet points, or we can drill down into any of those steps.
```

### follow-up: “make that shorter”

_Expected:_ rewrite the previous plan using conversation context; no new search

**Harness trace:** `· no notes searched · 21.7s`

```text
Okay, let's tighten that up.

**Concise Pac-Man DQN Review Plan**

1.  **The Theory:** Map out the core DQN components (State $\to$ Action $\to$ Q-Value).
2.  **The Flow:** Walk through the full learning cycle (Experience $\to$ Update).
3.  **The Code:** Review 2-3 critical functions and explain their *purpose*.
4.  **The Weak Spots:** Pinpoint 2 potential bugs or limitations and how to solve them.
5.  **The 'Why':** Prepare answers for "Why did you choose X over Y?" questions.

Is that punchier enough?
```

### chat-only claim: “Fun fact: my favorite ghost in the Pac-Man project was Sue.”

_Expected:_ acknowledge; must not treat this as a verified note

**Harness trace:** `· no notes searched · 11.0s`

```text
Got it. I'll keep that in mind if we're discussing the project details.

(Suggestion: We should probably stick to the technical aspects for the quiz, but I'll note it.)

What's next? Should we flesh out Step 1, or do you want to look up any specific requirements from the assignment brief?
```

## 2. Search (retrieval tool only, no model answer)

```text
$ wiki search "exploration rate Pac-Man" --scope raw -k 3
search: "exploration rate Pac-Man"  (scope=raw, top 3, no answer generated)

[1] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > Limitation and next experiment (L172-181)  [ORIGINAL]
    bm25=14.20  cosine=0.517  fused=0.0325
    | I'd change **exploration** next — increase it from 0.25 to something like 0.4 — on the reasoning that the agent needs more varied close-call encounters with ghosts to have anything to learn an evasion policy *from*, and pushing more randomness into training is a more direct way to generate those than simply repeating the same exploration rate for longer. *Note on process: I originally started a 500-episode run to …

[2] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > Training plot (L89-96)  [ORIGINAL]
    bm25=17.77  cosine=0.446  fused=0.0320
    | ## Training plot ![Training dashboard: score, loss, and exploration over 800 episodes](results/training_dashboard.png) Score per episode (top), training loss (middle), and exploration rate (bottom, constant at 25% after the 1,000-decision random warm-up). Full per-episode data: [`results/training.csv`](results/training.csv).

[3] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > My three hyperparameters (L23-27)  [ORIGINAL]
    bm25=11.17  cosine=0.409  fused=0.0306
    | | Learning rate | `0.0001` | Used the notebook's suggested reference value. This is a conservative rate for Adam on this size of convolutional network — large enough to learn within 100 episodes, small enough to avoid destabilizing Q-value estimates given the small (5,000-transition) replay buffer. | Evaluation settings were left unchanged as required: the same 5 seeds (`101, 202, 303, 404, 505`), 5% evaluation …
```

## 3. Ask ignores chat history

The chat above claimed a favorite ghost. Ask mode starts fresh and only sees retrieved raw passages:

```text
$ wiki ask "What was my favorite ghost in the Pac-Man project?"
Retrieved passages:
  [S1] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent (L1-7)
  [S2] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > How the agent works, in plain language (L114-141)
  [S3] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > Limitation and next experiment (L142-174)
  [S4] raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > Run the Provided Language Evals (L93-103)
  [S5] raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > Open the Notebook (L41-50)
  [S6] raw/Class 4 - Assignment Brief.md § Class 4 Assignment: Building a Custom LLM > Scope (L229-237)
  [S7] raw/Networking Tracker Project.md § Networking Tracker > Local setup (L110-152)
  [S8] raw/Networking Tracker Project.md § Networking Tracker > Testing (L246-275)

INSUFFICIENT EVIDENCE: the notes do not say what the user's favorite ghost was in the Pac-Man project. The passages discuss the agent's learning rule, which involves comparing predictions to `reward + discounted value of the next screen` [S2], and note that the agent's evaluation score nearly doubled because it got better at collecting points within a short lifespan [S3].

Sources:
  [S2] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > How the agent works, in plain language (L114-141)
  [S3] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > Limitation and next experiment (L142-174)
  citation check: all citations point to retrieved passages
model: gemma4:e4b (local) · 66.75s · 3473 prompt tok · 82 out tok
```

_Expected:_ INSUFFICIENT EVIDENCE — the claim exists only in chat, not in any source.

## Assessment (human review)

_TODO_
