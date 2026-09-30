# Measured memory use and response time

Device: Apple M1 (8-core CPU, 8-core GPU, Metal 4), **16 GB unified memory**, macOS 27.0, on AC power.
Runtime: Ollama 0.34.3 (llama.cpp backend, 100% GPU per `ollama ps`).
While these runs happened, macOS reported ~34% memory free and ~4.7–5 GB swap in use, with normal apps (browser, Claude, WhatsApp) open.

## Memory

| What | How measured | Value |
|---|---|---|
| `gemma4:e4b` (Q4_K_M) loaded, 8k context | `ollama ps` / `/api/ps` | **3.3–3.4 GB** |
| `gemma4:e4b` loaded, 16k context (ingest) | `ollama ps` during ingest | 3.4 GB |
| `gemma4:e2b` loaded, 8k context | `/api/ps` | 1.9 GB |
| `embeddinggemma` (BF16, 308M) | `/api/ps` | 0.67 GB |
| **Total for the default setup** (E4B + embeddings) | sum | **≈ 4.1 GB** |
| Python harness process (`wiki ingest`) | `/usr/bin/time -l` peak memory footprint | ≈ 37 MB |
| Disk: `gemma4:e4b` download | `ollama list` | 9.6 GB (the Ollama build includes the vision/audio encoders; 8.0B total params) |
| Disk: retrieval index (`data/index/`) | `du` | < 1 MB |

The 9.6 GB download is much bigger than the 3.4 GB in memory because Ollama only loads the text-generation weights for these requests.

## Response time: ask mode (the offline run, `evidence/offline/ask/`)

| Test | End-to-end | Prompt tokens | Output tokens |
|---|---|---|---|
| test1 | 47.0 s (includes 6.7 s model load after restart) | 2,824 | 40 |
| test2 | 65.6 s | 2,982 | 201 |
| test3 | 51.4 s | 2,287 | 101 |
| test4 | 45.2 s | 2,457 | 81 |

Most of the time goes to **reading the prompt** (~2.3–3k tokens of evidence at roughly 50–100 tokens/s on this M1). Generating the answer runs at ~6–9 tokens/s. Retrieval itself (BM25 + one embedding call) takes well under 1 s.

## Response time: ingest

| Run | Source size | Gemma call | Total |
|---|---|---|---|
| First ingest, online (4 sources) | 4.2k / 6.3k / 9.7k / 5.5k prompt tokens | 215 s / 279 s / 419 s / 312 s | 1,246 s |
| **Offline ingest of the Class 5 brief** | 2.9k prompt tokens, 1.4k output tokens | 216 s | **236 s** |
| Re-ingest of an unchanged source | (hash match, skipped) | none | 0.0 s |

## E2B vs E4B on the same 4 questions (dev run, after the retrieval fixes)

| | `gemma4:e2b` | `gemma4:e4b` |
|---|---|---|
| Loaded memory | 1.9 GB | 3.4 GB |
| Time per question | 19–26 s | 42–77 s |
| test1 | ✅ | ✅ |
| test2 (paraphrased "why") | ⚠️ said survival stayed flat but **gave none of the three causes** | ✅ all three causes, cited |
| test3 (two sources) | ✅ (terser) | ✅ |
| test4 (unsupported) | ✅ | ✅ |

Cards: [`dev-run/ask-e2b/`](dev-run/ask-e2b/) and [`dev-run/ask-e4b/`](dev-run/ask-e4b/).

**Choice:** E4B is the smallest model that answered all four tests correctly, and it fits in 16 GB (≈4.1 GB including embeddings) with room left for the OS and apps. E2B is 2.5× faster and would suit an 8 GB machine or casual chat, but it missed the one question that needed synthesis.

Note on an earlier measurement: in one "warm" benchmark, E4B answered in 18 s. That was Ollama reusing its cache for an identical repeated prompt, so it's not a fair number; the table above uses fresh questions only.
