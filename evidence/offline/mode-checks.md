# Mode boundary checks — 2026-09-29 22:32

- model: `gemma4:e4b` · Q4_K_M · digest `c6eb396dbd59` · execution **local** (Ollama 0.34.3)
- network: OFFLINE (internet unreachable)
- device: Apple M1, 16 GB unified memory, macOS 27.0

## 1. Chat (one continuous conversation with Wren)

### capabilities: “what can you help me with?”

_Expected:_ explain real capabilities; no notes search, no citations, no refusal

**Harness trace:** `· no notes searched · 22.1s`

```text
I'm here to help you with your notes.

I can:
*   **Brainstorm, draft, outline, plan, and rewrite text** with you. We can work on anything you're writing right now.
*   **Search your personal wiki** for anything related to your courses or projects (like Ms. Pac-Man or nanoGPT).
*   **Point you to the right commands** for using the wiki tools if you need to look up something specific.

Basically, I'm a sounding board for your schoolwork. Just let me know what you're stuck on.
```

### capabilities: “what can we do?”

_Expected:_ same: conversational, no notes search

**Harness trace:** `· no notes searched · 23.9s`

```text
We can work on almost anything related to your coursework. Here are a few ideas:

1.  **Reviewing Concepts:** If you're confused about a topic, we can talk it through.
2.  **Drafting:** If you have an essay or report, we can outline it or rewrite sections.
3.  **Project Work:** We can look at your specific projects. If you need to know what you wrote down about the **nanoGPT assignment** or the **Networking Tracker**, I can search your notes for details.
4.  **Organizing:** We can structure messy notes into clear outlines or bullet points.

If you want to check what you've already recorded about a project, just tell me what it is, and I can use the search tool.

What subject or task is on your mind right now?
```

### draft: “Draft a 5-step study plan for reviewing my Pac-Man DQN project before a quiz.”

_Expected:_ may search notes; any facts about the project must carry [S#] citations; plan labeled as suggestion

**Harness trace:** `· no notes searched · 42.2s`

```text
Suggestion: Since I don't know what you've covered in your notes for the Pac-Man DQN project, I'll draft a general, solid framework. We can tweak it once you tell me what specific areas you need to focus on.

Here is a 5-step study plan:

1.  **Review Core Concepts (The "Why"):** Don't just look at code. Spend time understanding *why* DQN was chosen for this problem. Review the theory behind Q-learning, state representation, and the role of the DQN architecture.
2.  **Walk Through the Pipeline (The "How"):** Trace the entire data flow. How does the environment generate a state? How does the network take that state as input? What is the final output used for (action selection)?
3.  **Code Walkthrough (The "What"):** Go through the most complex functions in your own code (e.g., the experience replay mechanism or the target network update). Pretend you are explaining it to someone who hasn't seen it.
4.  **Troubleshoot Edge Cases (The "What If"):** Think about what could go wrong. What happens if the reward signal is noisy? What if the exploration rate ($\epsilon$) decays too fast? Be ready to explain the fixes.
5.  **Practice Simulation:** If possible, run a short, focused simulation or trace a specific, tricky sequence of actions through the system manually.

Does this structure look right, or should we spend more time on the math, the Python implementation, or something else?
```

### follow-up: “make that shorter”

_Expected:_ rewrite the previous plan using conversation context; no new search

**Harness trace:** `· no notes searched · 17.9s`

```text
Here is a much shorter version:

1.  **Theory Check:** Review the core DQN concepts (Q-learning, state/action space).
2.  **Flow Map:** Trace the entire process from environment state $\rightarrow$ network input $\rightarrow$ action output.
3.  **Code Deep Dive:** Manually walk through the hardest functions (e.g., replay buffer updates).
4.  **Failure Points:** Predict and explain what happens if things break (e.g., poor exploration).
5.  **Test Run:** Run a short, targeted simulation to confirm the whole loop works.

How's that? More digestible?
```

### chat-only claim: “Fun fact: my favorite ghost in the Pac-Man project was Sue.”

_Expected:_ acknowledge; must not treat this as a verified note

**Harness trace:** `· no notes searched · 5.5s`

```text
Got it. Sue.

(No action needed on that, unless you want me to search your notes for anything related to "Sue" or specific ghost dynamics!)
```

## 2. Search (retrieval tool only, no model answer)

```text
$ wiki search "exploration rate Pac-Man" --scope raw -k 3
search: "exploration rate Pac-Man"  (scope=raw, top 3, no answer generated)

[1] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > Limitation and next experiment (L172-181)  [ORIGINAL]
    bm25=14.85  cosine=0.517  fused=0.0325
    | I'd change **exploration** next — increase it from 0.25 to something like 0.4 — on the reasoning that the agent needs more varied close-call encounters with ghosts to have anything to learn an evasion policy *from*, and pushing more randomness into training is a more direct way to generate those than simply repeating the same exploration rate for longer. *Note on process: I originally started a 500-episode run to …

[2] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > Training plot (L89-96)  [ORIGINAL]
    bm25=18.74  cosine=0.446  fused=0.0320
    | ## Training plot ![Training dashboard: score, loss, and exploration over 800 episodes](results/training_dashboard.png) Score per episode (top), training loss (middle), and exploration rate (bottom, constant at 25% after the 1,000-decision random warm-up). Full per-episode data: [`results/training.csv`](results/training.csv).

[3] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > My three hyperparameters (L23-27)  [ORIGINAL]
    bm25=11.94  cosine=0.409  fused=0.0306
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
  [S7] raw/Class 5 - Personal Wiki Brief.md § Class 5 Assignment: Personal Wiki with Local Gemma + RAG > Build Your Personal Wiki (L51-56)
  [S8] raw/Class 5 - Personal Wiki Brief.md § Class 5 Assignment: Personal Wiki with Local Gemma + RAG > Submission (L77-79)

INSUFFICIENT EVIDENCE: the notes do not say what the user's favorite ghost was in the Pac-Man project. The passages discuss the agent's learning process, which involves rewards for eating a scared ghost [S2], and the agent's limitation regarding survival time [S3].

Sources:
  [S2] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > How the agent works, in plain language (L114-141)
  [S3] raw/Class 3 - Ms Pacman DQN.md § Training a Ms. Pac-Man DQN Agent > Limitation and next experiment (L142-174)
  citation check: all citations point to retrieved passages
model: gemma4:e4b (local) · 8.93s · 3023 prompt tok · 62 out tok
```

_Expected:_ INSUFFICIENT EVIDENCE — the claim exists only in chat, not in any source.

## Assessment (human review)

| Check | Result |
|---|---|
| "what can you help me with?" / "what can we do?" | ✅ Accurate capabilities (drafting, wiki search, CLI commands), **no notes search**, no citations, no insufficient-evidence refusal |
| Draft a study plan | ⚠️ Partial. The plan is labeled "Suggestion:" and invents no personal facts, but Gemma **did not call `search_notes`** even though the request says "*my* Pac-Man DQN project". It honestly said it didn't know my notes, instead of looking them up, so the plan is generic. It also used LaTeX (`$\epsilon$`). This is the main chat limitation (see README → Reflection). |
| "make that shorter" | ✅ Shortened the previous plan from conversation history; no new search |
| Chat-only claim ("favorite ghost was Sue") | ✅ Acknowledged; not saved or treated as a source |
| `wiki search` | ✅ Original passages with paths, line ranges and scores; no generated answer |
| `wiki ask` after the chat claim | ✅ INSUFFICIENT EVIDENCE, so chat history did not leak into ask mode |
