---
name: perplexity-research
description: |
  Perplexity Sonar API research guide for video pre-production. Covers query structure, source grounding, fact extraction, and research-to-script workflows. Use during idea and script pipeline stages.
metadata:
  openclaw:
    requires:
      env:
        - PERPLEXITY_API_KEY
    primaryEnv: PERPLEXITY_API_KEY
---

# Perplexity Research — Video Pre-Production Guide

Use this skill during the **idea** and **script** stages to gather grounded, web-sourced research for video content. Perplexity's Sonar API returns cited, up-to-date information — critical for factual explainers, news content, and educational videos.

## API Quick Reference

### Endpoint

```
POST https://api.perplexity.ai/chat/completions
```

### Authentication

```
Authorization: Bearer $PERPLEXITY_API_KEY
```

### Models

| Model | Best for | Speed |
|-------|----------|-------|
| `sonar` | General research, quick facts | Fast |
| `sonar-pro` | Deep research, complex topics | Slower, more thorough |
| `sonar-reasoning` | Analysis, comparisons, multi-source synthesis | Slowest, highest quality |

**Default:** `sonar` for initial research, `sonar-pro` for script-backing research.

### Basic Request

```python
import requests
import os

response = requests.post(
    "https://api.perplexity.ai/chat/completions",
    headers={
        "Authorization": f"Bearer {os.environ['PERPLEXITY_API_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "You are a research assistant for video production. Provide factual, cited information."},
            {"role": "user", "content": "What are the latest statistics on ocean plastic pollution in 2025?"}
        ],
    },
)
data = response.json()
answer = data["choices"][0]["message"]["content"]
citations = data.get("citations", [])
```

## Research Query Patterns

### Pattern 1: Fact Gathering (Idea Stage)

For the **idea** stage — gather hooks, stats, and angles on a topic.

```
System: You are a research assistant for a video production team.
        Return facts as bullet points with source attribution.
        Focus on surprising, counterintuitive, or visually compelling facts.

User: Research the topic "[TOPIC]" for a [DURATION]-second [PLATFORM] video.
      I need:
      1. 5 surprising facts or statistics (with dates and sources)
      2. 3 common misconceptions to debunk
      3. 2-3 recent developments (last 12 months)
      4. Visual hooks — what would look compelling on screen
```

### Pattern 2: Deep Dive (Script Stage)

For the **script** stage — verify claims and get supporting detail.

```
System: You are a fact-checker for educational video content.
        Every claim must have a source. Flag any claim that has
        conflicting sources. Distinguish between established facts,
        recent findings, and ongoing debates.

User: I'm writing a script that claims: "[SPECIFIC CLAIM]".
      1. Is this accurate? Cite the primary source.
      2. What nuance am I missing?
      3. What's the most up-to-date data on this?
      4. Any expert quotes I can paraphrase for narration?
```

### Pattern 3: Competitor/Landscape (Idea Stage)

For positioning content within what already exists.

```
System: You are a content strategist analyzing the video landscape.

User: What are the top-performing YouTube videos about "[TOPIC]" in the last year?
      1. What angles do they cover?
      2. What's missing — what angle hasn't been covered well?
      3. What titles and hooks got the most engagement?
      4. What's the typical video length for this topic?
```

### Pattern 4: Visual Reference (Scene Planning)

For finding real-world visual references.

```
System: You are a visual researcher for video production.

User: I need visual reference ideas for a scene about "[CONCEPT]".
      1. What real-world locations or objects best represent this concept?
      2. What visual metaphors are commonly used?
      3. Any famous images, artworks, or films that capture this well?
      4. What colors and moods are associated with this concept?
```

## Research-to-Script Workflow

1. **Topic exploration** (sonar) → 3-5 angle candidates with key facts
2. **Angle selection** → user picks the most compelling angle
3. **Deep fact-check** (sonar-pro) → verify every claim in the script outline
4. **Source compilation** → extract citations for description/credits
5. **Visual cues** → extract visual concepts for scene planning

### Extracting Script-Ready Content

When processing Perplexity responses, extract:

| Element | How to use in script |
|---------|---------------------|
| Statistics with dates | Narration hooks: "In 2025, researchers found that..." |
| Expert quotes | Paraphrased narration or text overlay |
| Counterintuitive facts | Opening hook or twist moment |
| Source URLs | Video description, pinned comment |
| Visual concepts | Scene plan image prompts, B-roll search queries |

## Prompting Best Practices

### Be Specific About Recency

```
BAD:  "Tell me about AI"
GOOD: "What are the most significant AI developments in Q1 2026, specifically in video generation?"
```

### Ask for Structure

```
BAD:  "Research quantum computing"
GOOD: "Explain quantum computing for a general audience in 5 key points, each under 30 words, suitable for narration in a 60-second explainer video."
```

### Request Citations Explicitly

```
Add to any query: "Cite specific sources for every factual claim. Include publication date."
```

### Multi-Turn for Depth

Use follow-up messages in the same conversation for progressive depth:

1. "Overview of [topic]" → get the landscape
2. "Go deeper on point #3 about [specific aspect]" → drill into the best angle
3. "Find the original study behind [claim]" → verify the source

## Cost Management

Perplexity charges per request, not per token. Optimize by:

- Batching related questions into single prompts
- Using `sonar` for exploration, `sonar-pro` only for verification
- Caching research results in the project's `artifacts/` directory as `research_brief.json`

## Integration with Pipeline

| Pipeline stage | Perplexity role |
|---------------|----------------|
| **Idea** | Topic exploration, hook discovery, angle selection |
| **Script** | Fact verification, quote sourcing, nuance checking |
| **Scene plan** | Visual reference ideas, B-roll keyword suggestions |
| **Assets** | Image prompt enrichment (real-world details from research) |
