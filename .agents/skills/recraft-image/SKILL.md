---
name: recraft-image
description: |
  Recraft V4 image generation prompting guide for logos, vectors, icons, and text-rendered graphics. Covers style encoding in prompts, color palettes, SVG output, and brand asset workflows. Use before calling recraft_image tool.
metadata:
  openclaw:
    requires:
      env:
        - FAL_KEY
    primaryEnv: FAL_KEY
---

# Recraft V4 — Prompting Guide

Use this skill before generating images with the `recraft_image` tool. Recraft V4 is the best choice for **logos, brand assets, vector graphics, icons, and images with precise text rendering**.

## When to Use Recraft (vs. FLUX or Imagen)

| Need | Recraft V4 | FLUX.2 | Imagen 4 |
|------|-----------|--------|----------|
| Logo design | **Best** | Good | Poor |
| Vector/SVG output | **Only option** | No | No |
| Icon sets | **Best** | OK | Poor |
| Text in images | **Excellent** | Excellent (Flex) | Very good |
| Color palette control | **Exact hex** | Hex in prompt | Describe only |
| Photorealism | Weak | Excellent | Excellent |
| Complex scenes | Limited | Best | Very good |

**Rule:** Recraft for brand/graphic assets, FLUX for creative/photographic, Imagen for photorealistic.

## Model Selection

| Model | Cost | Best for |
|-------|------|----------|
| `v4` | $0.04 | Default — good quality, fast |
| `v4-pro` | $0.25 | Maximum quality logos, hero brand assets |

## Style Encoding in Prompts

**IMPORTANT:** The `style` parameter is currently broken on fal.ai (returns 422). Encode style directly in the prompt text instead.

| Target style | Prompt prefix |
|-------------|---------------|
| Realistic photo | "Realistic photograph of..." |
| Digital illustration | "Digital illustration of..." |
| Vector illustration | "Clean vector illustration of..." |
| Flat icon | "Flat design icon of..." |
| Line icon | "Minimal line icon of..." |
| Logo | "Professional logo design for..." |
| Watercolor | "Watercolor painting of..." |

### Effective Prompt Structure

```
[Style prefix] + [Subject with specifics] + [Color/palette direction] +
[Background instruction] + [Text content if any]
```

## Logo Prompting

### Wordmark

```
Professional wordmark logo for "NEXUS", modern geometric sans-serif typeface,
clean lines, balanced letterforms, on a pure white background.
Minimal and corporate. Colors: navy blue #1B365D.
```

### Icon + Text

```
Professional logo combining a stylized mountain peak icon with the text "SUMMIT"
beneath it. Clean vector style, geometric shapes, on transparent background.
Primary color: deep teal #006D6F, accent: warm gold #C8963E.
```

### Abstract Mark

```
Abstract geometric logo mark using overlapping translucent circles forming
a dynamic pattern. Modern tech startup aesthetic. Colors: electric blue #0066FF
and coral pink #FF6B6B on white background.
```

## Icon Set Prompting

For consistent icon sets, use a template prompt and vary only the subject:

```
Flat design icon of [SUBJECT], minimal style, solid fill, rounded corners,
2px consistent stroke weight, on transparent background.
Color palette: #2563EB primary, #F59E0B accent, #1F2937 dark.
```

Subjects to swap: `a calendar`, `a gear/settings`, `a user profile`, `a notification bell`, etc.

**Consistency tips:**

- Keep the style description identical across all icons
- Use the same color palette
- Specify the same stroke weight and corner style
- Generate in the same aspect ratio (square or square_hd)

## Color Palette Control

Recraft accepts hex color arrays via the `colors` parameter:

```python
{
    "prompt": "A modern tech company logo...",
    "colors": ["#0066FF", "#00CC88", "#FFFFFF"]
}
```

**In prompt text** (more reliable):

```
...using a color palette of electric blue (#0066FF), mint green (#00CC88),
and white (#FFFFFF). No other colors.
```

## Text Rendering

Recraft V4 has excellent text rendering:

- **Quote exact text**: `logo reading "ACME CORP"`
- **Specify font characteristics**: "bold geometric sans-serif", "elegant thin serif"
- **One text element at a time** — multiple text blocks reduce accuracy
- **Short text only** — 1-4 words render perfectly, beyond that quality drops

## SVG Output

Recraft is the only tool that produces vector SVG output. Use when:

- The asset needs to scale infinitely (logos, icons)
- The output will be used in web/print at multiple sizes
- Clean vector lines are required

**Note:** SVG output may need to be enabled at the tool level; check if the tool exposes SVG format options.

## Iteration Workflow

1. **Draft** (v4, 2-3 prompt variations) → pick best concept direction
2. **Refine** (v4, iterate colors/layout) → dial in the design
3. **Final** (v4-pro) → hero asset with maximum quality
4. **Variants** — generate color/layout variations for client choice

## Common Mistakes

- **Using Recraft for photos** — it's not a photorealism model. Use FLUX or Imagen.
- **Overloading the prompt** — Recraft works best with focused, clean descriptions.
- **Forgetting background** — always specify "on white background", "on transparent background", or "on dark background."
- **Using the `style` parameter** — currently broken on fal.ai. Encode in prompt text.
- **Requesting complex multi-element scenes** — Recraft is a graphics tool, not a scene compositor.
