---
name: stock-media-search
description: |
  Search optimization for Pexels, Pixabay, and Unsplash stock media APIs. Covers keyword strategies, filter usage, multi-provider search, and B-roll selection for video production. Use before calling pexels_image, pexels_video, pixabay_image, pixabay_video, clip_search, or direct_clip_search tools.
metadata:
  openclaw:
    requires:
      env_any:
        - PEXELS_API_KEY
        - PIXABAY_API_KEY
        - UNSPLASH_ACCESS_KEY
---

# Stock Media Search — Optimization Guide

Use this skill before searching for stock images or video clips with Pexels, Pixabay, Unsplash, or the unified clip_search/direct_clip_search tools.

## Provider Strengths

| Provider | Images | Video | Strengths | License |
|----------|--------|-------|-----------|---------|
| **Pexels** | Excellent | Excellent | Curated, professional, good people/lifestyle | Free, no attribution required |
| **Pixabay** | Good | Good | Large volume, diverse categories, music too | Free, no attribution required |
| **Unsplash** | Excellent | No | Premium photography, artistic, high-res | Free, attribution appreciated |

### When to Use Which

- **Hero shots / key visuals** → Unsplash (highest artistic quality) or Pexels
- **B-roll footage** → Pexels (best curated video) then Pixabay (more variety)
- **Volume search** (many clips needed) → Pixabay (largest catalog) + Pexels
- **People / lifestyle** → Pexels (strongest category)
- **Nature / landscapes** → All three are strong; Unsplash for stills, Pexels for video
- **Tech / business** → Pexels first, Pixabay fallback
- **Abstract / textures** → Pixabay (most variety in abstract categories)

## Search Keyword Strategy

Stock search APIs are keyword-based, not natural-language. Optimize your queries:

### Rule 1: Use English Keywords

All three APIs index content in English. Even for French-language productions, search in English.

### Rule 2: Simple, Concrete Nouns

```
BAD:  "beautiful sunset over the ocean with warm colors"
GOOD: "ocean sunset golden hour"

BAD:  "a professional woman working at her desk in a modern office"
GOOD: "woman office laptop"

BAD:  "futuristic technology concept with data visualization"
GOOD: "data visualization dashboard"
```

### Rule 3: 2-4 Keywords Maximum

APIs rank by keyword match, not semantic understanding. More keywords = fewer results.

```
Optimal: "mountain hiking trail"     (3 keywords)
OK:      "mountain trail fog"        (3 keywords, more specific)
Too many: "person hiking mountain trail sunrise fog backpack" (7 keywords)
```

### Rule 4: Synonym Expansion

If the first search returns weak results, try synonyms:

| Concept | Try these keywords |
|---------|-------------------|
| Business | office, corporate, meeting, workspace, professional |
| Technology | tech, digital, code, computer, software, AI |
| Nature | landscape, forest, ocean, mountain, wildlife |
| People | person, team, group, crowd, portrait |
| Movement | motion, running, walking, speed, action |
| Calm/peaceful | serene, minimal, quiet, zen, meditation |

### Rule 5: Category-Specific Tricks

**For video B-roll:**

- Add movement descriptors: "aerial city", "timelapse clouds", "slow motion water"
- Specify shot types: "drone forest", "closeup hands", "wide angle street"

**For backgrounds:**

- Add "background" or "texture": "dark gradient background", "marble texture"
- Add "abstract": "abstract blue waves", "abstract geometric"

**For lifestyle:**

- Avoid overly specific descriptions
- "coffee shop work" > "freelancer drinking latte in artisanal coffee shop"

## Filter Usage

### Orientation

| Filter | When to use |
|--------|-------------|
| `landscape` | 16:9 video frames, YouTube thumbnails, hero banners |
| `portrait` | 9:16 Stories/Reels/Shorts, mobile-first content |
| `square` | Social media posts, thumbnails |

**Always set orientation** when you know the target format — it dramatically improves result relevance.

### Size (Pexels/Pixabay)

- `large` or `medium` for final production
- `small` for previews/drafts

### Color (Pexels)

Filter by dominant color when matching a color palette. Available: red, orange, yellow, green, turquoise, blue, violet, pink, brown, black, gray, white.

## Multi-Provider Search Strategy

For best coverage, search across providers in this order:

### For Video Clips

1. **Pexels** (curated, high quality) → take best matches
2. **Pixabay** (volume) → fill gaps
3. Use `direct_clip_search` or `clip_search` to search all at once

### For Still Images

1. **Unsplash** (artistic quality) → hero shots
2. **Pexels** (professional) → supporting visuals
3. **Pixabay** (volume) → fill remaining gaps

### Deduplication

Stock providers share some content. When searching multiple providers:

- Compare by visual similarity, not filename
- Prefer the highest resolution version
- Prefer the source with the best metadata (title, tags)

## B-Roll Selection for Video Production

When searching for B-roll to support a narration script:

1. **Extract key visual concepts** from each script section
2. **Search one concept per query** — don't combine unrelated concepts
3. **Match shot energy to narration tone:**
   - Calm narration → slow panning shots, static scenes
   - Energetic narration → fast cuts, action shots, aerial footage
   - Technical narration → close-ups, screen recordings, diagrams
4. **Plan visual variety:**
   - Mix wide, medium, close-up shots
   - Alternate between people, places, and objects
   - Include at least one transition-friendly shot (abstract, motion blur)

## Common Mistakes

- **Searching in French** — APIs index in English. Translate first.
- **Too many keywords** — 2-4 is optimal. More = worse results.
- **Not setting orientation** — returns mixed landscape/portrait, most unusable.
- **Single provider only** — always search 2+ providers for best coverage.
- **Ignoring video duration** — check clip length matches your scene timing.
- **Generic queries** — "business" returns 10,000 results. "team meeting whiteboard" returns 50 relevant ones.
