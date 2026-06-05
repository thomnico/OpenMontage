---
name: google-imagen
description: |
  Google Imagen 4 image generation prompting guide. Covers model selection (standard/fast/ultra), prompt structure, aspect ratios, and photorealistic optimization. Use before calling google_imagen tool.
metadata:
  openclaw:
    requires:
      env:
        - GOOGLE_API_KEY
    primaryEnv: GOOGLE_API_KEY
---

# Google Imagen 4 — Prompting Guide

Use this skill before generating images with the `google_imagen` tool. Imagen 4 excels at photorealism, text rendering, and instruction following.

## Model Selection

| Model | Cost/image | Best for |
|-------|-----------|----------|
| `imagen-4.0-generate-001` | $0.04 | Default — balanced quality and speed |
| `imagen-4.0-fast-generate-001` | $0.02 | Drafts, iteration, previews |
| `imagen-4.0-ultra-generate-001` | $0.06 | Hero shots, final assets, maximum detail |

**Rule:** Use `fast` for exploration (3-4 variants), then `generate` or `ultra` for the final pick.

## Prompt Structure

Imagen 4 responds best to **detailed natural language descriptions** (max 480 tokens).

```
[Subject with specific details] + [Action/pose] + [Environment/setting] +
[Lighting conditions] + [Camera/lens technical details] + [Mood/atmosphere]
```

### What Works Well

- **Specificity over abstraction.** "A 35-year-old woman with auburn hair wearing a navy blazer" beats "a professional woman."
- **Lighting is king.** Always specify: golden hour, rim lighting, softbox, overcast, neon, etc.
- **Camera language.** Imagen responds to: "shot on 85mm f/1.4", "wide-angle lens", "overhead shot", "macro close-up."
- **Material descriptions.** "Brushed aluminum", "matte ceramic", "weathered leather" — surface textures dramatically improve realism.
- **Spatial relationships.** "In the foreground", "reflected in", "casting a shadow on" — be explicit about depth.

### What to Avoid

- **No negative prompts.** Imagen 4 does not support them. Describe what you WANT, not what you don't.
- **No keyword spam.** Don't stack "8K, ultra detailed, masterpiece" — that's Stable Diffusion syntax. Imagen ignores it.
- **No contradictions.** "Realistic photograph of a cartoon character" confuses the model.
- **Vague lighting.** Unspecified lighting = flat, boring results.

## Aspect Ratios

| Ratio | Use case |
|-------|----------|
| `1:1` | Social media posts, thumbnails, profile images |
| `16:9` | YouTube thumbnails, video frames, hero banners |
| `9:16` | Instagram Stories, TikTok, Shorts |
| `4:3` | Blog posts, presentations |
| `3:4` | Pinterest, portraits |

**Tip:** Match the aspect ratio to the final use. Don't generate 1:1 then crop — Imagen composes within the ratio.

## Prompt Patterns by Use Case

### Photorealistic Scene

```
A cozy bookshop interior at dusk, warm tungsten lighting from vintage pendant lamps,
floor-to-ceiling oak bookshelves filled with leather-bound books, a tabby cat sleeping
on a reading chair, steam rising from a ceramic coffee cup on the side table.
Shot on Sony A7IV with 35mm f/1.8 lens, shallow depth of field, natural color grading.
```

### Product Shot

```
A single matte black wireless earbud floating against a pure white background,
soft studio lighting with a gentle gradient shadow beneath, slight reflection on
the glossy surface. Commercial product photography style, clean and minimal.
```

### Video Thumbnail / Scene Frame

```
Close-up of a scientist's hands holding a glowing blue crystal in a dark laboratory,
dramatic side lighting from a single lab lamp casting long shadows, shallow depth of field,
the scientist's face barely visible in the background blur. Cinematic color grading,
teal and orange tones.
```

### Illustration / Graphic

```
A flat-design infographic illustration showing the water cycle, with labeled arrows
for evaporation, condensation, and precipitation. Clean vector style with a soft
blue-to-white gradient background. Text labels reading "Evaporation", "Condensation",
"Precipitation" in clean sans-serif font.
```

## Text Rendering

Imagen 4 has strong text rendering. To get reliable text in images:

- **Quote the exact text** you want: `a sign reading "OPEN 24 HOURS"`
- **Specify the font style**: "bold sans-serif", "elegant serif", "handwritten script"
- **Keep text short** — 1-5 words render best, longer text may degrade
- **Place text explicitly**: "centered at the top", "on the storefront sign", "written on the chalkboard"

## Iteration Workflow

1. **Explore** (fast model, 2-3 prompts) → pick best direction
2. **Refine** (standard model, iterate prompt details) → dial in composition
3. **Finalize** (ultra model, final prompt) → hero asset

## Comparison with FLUX

| Dimension | Imagen 4 | FLUX.2 |
|-----------|----------|--------|
| Photorealism | Excellent (Google's strength) | Excellent |
| Text rendering | Very good | Best (especially Flex) |
| Speed | Fast (esp. fast model) | Varies by model |
| Style control | Natural language only | JSON structured + natural |
| Negative prompts | Not supported | Not supported |
| Color precision | Good (describe colors) | Excellent (hex codes) |
| Cost | $0.02-0.06 | $0.02-0.10 |

**When to pick Imagen over FLUX:**

- Photorealistic scenes with complex lighting
- Google ecosystem integration needed
- Fast iteration at low cost (fast model)
- Product photography style

**When to pick FLUX over Imagen:**

- Typography-heavy designs
- Precise color control (hex codes)
- Structured scene composition (JSON prompting)
- Multi-reference editing
