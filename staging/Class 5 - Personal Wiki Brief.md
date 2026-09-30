# Class 5 Assignment: Personal Wiki with Local Gemma + RAG

Build your own CLI and harness to talk to your own data, using a local open-weight model that fits your computer and works offline.

## Overview

Build a personal wiki from your own notes and documents. Use local Gemma to organize linked pages and power three distinct CLI modes: chat as a personal assistant, ask for grounded factual answers, and search for original passages. Build your own harness to connect the interface, conversation, retrieval, prompts, model, citations, and saved outputs. This is a standalone, one-and-done Assignment 4, separate from the capstone. No sample GitHub repository is provided.

## Model, Retrieval, RAG, and Harness

Model: local Gemma generates text from the instructions and context your program supplies. It does not automatically read your files, remember every conversation, or operate your tools.

Retrieval tool: code that searches your local index and returns relevant original passages with source paths. Its job is to find evidence. Search mode exposes this tool's results directly, without generating an answer.

RAG workflow: retrieve relevant passages, include them in a prompt, and have the model answer using that evidence. Ask mode uses this workflow. RAG supplies context at answer time; it does not train the model.

Harness: the surrounding application code you build. It manages modes, instructions and personality, conversation context, tool calls, prompt assembly, local model calls, citation checks, errors, and saved outputs. Retrieval is one tool the harness can use; the harness decides when it is needed.

CLI: the terminal interface through which a user controls the harness. You can reuse inference and search libraries, but you must understand and assemble the connecting code. Explain one path from a user's command to the displayed result.

## Three Required Modes: Chat, Ask, Search

Chat = personal assistant. Give it a recognizable voice and a clear description of what it can actually do. It should help brainstorm, draft, plan, and work through ideas, using recent conversation for follow-ups. Retrieve notes when the request needs them, not for every message. Cite claims based on retrieved notes; label proposals as suggestions and never invent personal facts.

Chat example: "what can you help me with?" should explain the assistant's real capabilities and suggest a useful starting point. It should not return "insufficient evidence" or pull in unrelated course passages. After a draft or plan, "make that shorter" should use the conversation.

Ask = factual personal research. Treat each question independently of chat history. Retrieve relevant evidence, answer directly in a neutral voice, and show citations. If the sources do not support the answer, say so. Personality, brainstorming, and guesses must not replace evidence.

Search = inspect the sources. Return matching original passages and source locations. Do not generate a synthesized answer. This lets you check whether retrieval found the right material before evaluating the model.

The harness enforces these differences through separate instructions, context, and tool use. Chat history is conversation context, not automatically verified source material. If you add a save-memory feature, make saving an explicit user action and keep generated drafts separate from original evidence.

Chat, ask, and search describe interaction modes. Local and online describe where the model runs. All three interaction modes are required locally; an online option is an extension and never replaces offline operation.

## Choose Gemma for Your Computer

B means billion parameters. Google's E2B and E4B names describe effective parameter counts; their extra embedding tables also use memory. Quantization stores weights with fewer bits to reduce memory use, with possible quality tradeoffs.

E2B (often called 2B): approximately 2.9 GB to load at Q4_0. Start here when memory is tight.

E4B (often called 4B): approximately 4.5 GB to load at Q4_0. Try it when your device has room for a larger model.

26B A4B MoE: approximately 14.4 GB to load at Q4_0. It activates about 4B parameters per token, but fast inference still loads all 26B weights. It does not have a 4B memory footprint.

These official Gemma loading estimates are not total application requirements. Q4_0 is a 4-bit format. Leave additional memory for context, the runtime, retrieval, the operating system, and other apps. Check the exact model file and runtime you choose.

RAM is system memory; dedicated VRAM belongs to a discrete GPU. On Apple Silicon, CPU and GPU share unified memory. Disk space stores downloads; it is not working memory. CPU or partial GPU offloading can be slower than keeping the model in GPU memory.

Practical starting points, not guaranteed minimums: on an 8 GB Apple Silicon Mac, start with quantized E2B and short context; on a 16 GB Mac, consider E2B or E4B. On a PC with 6–8 GB dedicated VRAM, start with E2B and try E4B only if the runtime and context fit. With 32 GB or more unified memory, or 24 GB or more dedicated VRAM, 26B MoE is a candidate, not a requirement.

## Build Your Personal Wiki

Choose at least three sources you can inspect, such as course notes, research articles, or personal project notes. Keep original sources unchanged in vault/raw/. Store generated summaries and linked pages separately in vault/wiki/. Have your harness read a source, send its text and instructions to local Gemma, and save a reviewed wiki page with a reference back to the source. Connect related pages with links and update vault/index.md so a reader and your retrieval code can find them.

Split long text into useful passages and retain the source path and page or section when available. Explain how much text your harness passes to Gemma. Review generated summaries against the originals. Correct invented or misleading statements in the wiki rather than changing the evidence.

## Make the Wiki Readable in Obsidian

Name notes for their subject. Use short, natural filenames, usually 2–6 words, such as GPU Parallel Training.md, Course Project Ideas.md, or Retrieval Augmented Generation.md. Match the note's first heading to its filename. Do not use exported task titles, full sentences, timestamps, UUIDs, hashes, or chunk numbers as generated note names. Keep machine IDs and original filenames in properties or a source catalog.

Open vault/ itself as the Obsidian vault, not the entire code repository or course folder. Keep unchanged originals in raw/, reviewed notes in wiki/, and embedded images in attachments/ when needed. Keep code, logs, retrieval chunks, embeddings, test answers, and other generated machine files outside the vault. Keep index.md as a human landing page, grouped by topic with short descriptions and links.

Make the graph useful for exploration. Show the curated wiki notes, for example with the graph filter path:wiki/, and turn off Attachments so images and PDFs do not overwhelm the view.

## Your Three Choices

Data: what is this wiki for, which sources belong in it, and what questions should it answer? Model: which Gemma size and quantization fit your own device? Retrieval: start with a local index and keyword search, or use local embeddings. A hosted embedding API would break the offline requirement. The model has a limited context window. Select relevant passages and keep their source labels instead of sending the entire wiki for every question.

## Run Your Four Question Tests

An eval is a fixed question, an expected behavior, and the system's actual result. Test 1: a direct question answered by one source. Test 2: another answerable question, ideally phrased differently from the source. Test 3: a third question with known supporting evidence; it can connect two sources. Test 4: a plausible question whose answer is missing from the wiki; the expected behavior is an explicit statement that the evidence is insufficient. Keep your test expectations outside the searchable wiki. Run all four tests offline.

## How Your Assignment Is Graded

This assignment uses the course framework: deliverable quality (4 points), testing & evaluation (3 points), and working result (3 points), for 10 points total.

## Submission

Create your own public GitHub repository containing your CLI and harness code, README, shareable wiki sources and pages, and test evidence. Do not commit model weights or credentials. Submit your own project repository through the course submission portal.
