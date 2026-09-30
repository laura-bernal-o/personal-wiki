---
title: Local Model Deployment
aliases: []
type: concept
source_ids: [class-5-personal-wiki-brief]
generated_by: gemma4:e4b
reviewed: true
updated: 2026-09-29
---

# Local Model Deployment

Choosing a local model requires considering parameter size (E2B, E4B, 26B MoE) and quantization (Q4_0) relative to available system memory (RAM vs VRAM).

## Details

<!-- src:class-5-personal-wiki-brief -->
### In [[Personal Wiki Assignment]]
- E2B (2B) is suggested for tight memory situations, loading at approximately 2.9 GB at Q4_0. ([[raw/Class 5 - Personal Wiki Brief#Choose Gemma for Your Computer|§ Choose Gemma for Your Computer]])
- E4B (4B) is suggested when more memory is available, loading at approximately 4.5 GB at Q4_0. ([[raw/Class 5 - Personal Wiki Brief#Choose Gemma for Your Computer|§ Choose Gemma for Your Computer]])
- The 26B A4B MoE loads all 26B weights but activates about 4B parameters per token, requiring careful memory planning. ([[raw/Class 5 - Personal Wiki Brief#Choose Gemma for Your Computer|§ Choose Gemma for Your Computer]])
<!-- /src:class-5-personal-wiki-brief -->

## Related

- [[Personal Wiki Assignment]] — The assignment mandates using a local open-weight model

## Sources

- [[raw/Class 5 - Personal Wiki Brief|Class 5 - Personal Wiki Brief]] — original, `class-5-personal-wiki-brief`
