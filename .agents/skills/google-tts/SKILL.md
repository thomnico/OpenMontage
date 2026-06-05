---
name: google-tts
description: |
  Google Cloud TTS voice selection, SSML optimization, and multilingual production guide. Covers Chirp 3 HD, Neural2, WaveNet, and Studio voice tiers. Use before calling google_tts tool.
metadata:
  openclaw:
    requires:
      env:
        - GOOGLE_API_KEY
    primaryEnv: GOOGLE_API_KEY
---

# Google Cloud TTS — Voice & Prompting Guide

Use this skill before generating speech with the `google_tts` tool. Google TTS offers 700+ voices across 50+ languages — the widest multilingual coverage of any TTS provider in OpenMontage.

## Voice Tier Selection

| Tier | Quality | Cost/1M chars | Best for |
|------|---------|---------------|----------|
| **Chirp 3 HD** | Most natural, expressive | ~$30 | Hero narration, English content |
| **Journey** | Conversational, warm | ~$16 | Podcasts, casual explainers |
| **Neural2** | Clean, professional | ~$16 | Corporate, educational |
| **WaveNet** | Smooth, natural | ~$16 | General purpose |
| **Studio** | Broadcast quality | ~$160 | Premium broadcast, audiobooks |
| **Standard** | Basic, robotic | ~$4 | Drafts, prototyping only |

**Default recommendation:** Chirp 3 HD for English, Neural2 for other languages.

## Recommended Voices

### English (en-US)

| Voice | Gender | Character | Use case |
|-------|--------|-----------|----------|
| `en-US-Chirp3-HD-Orus` | Male | Rich, cinematic | Explainers, documentaries |
| `en-US-Chirp3-HD-Aoede` | Female | Warm, authoritative | Narration, tutorials |
| `en-US-Chirp3-HD-Charon` | Male | Deep, dramatic | Trailers, intros |
| `en-US-Chirp3-HD-Kore` | Female | Bright, energetic | Social media, upbeat |
| `en-US-Neural2-D` | Male | Neutral, professional | Corporate, reports |
| `en-US-Neural2-F` | Female | Clear, professional | Corporate, reports |
| `en-US-Journey-D` | Male | Conversational | Podcasts, casual |
| `en-US-Journey-F` | Female | Conversational | Podcasts, casual |

### French (fr-FR)

| Voice | Gender | Character |
|-------|--------|-----------|
| `fr-FR-Neural2-A` | Female | Clear, natural |
| `fr-FR-Neural2-B` | Male | Professional |
| `fr-FR-Neural2-D` | Male | Warm |
| `fr-FR-Chirp3-HD-*` | Various | Check availability — Chirp 3 HD expanding |

### Other Languages

Use format: `{lang}-{region}-{tier}-{variant}`. Examples:

- `es-ES-Neural2-A` (Spanish female)
- `de-DE-Neural2-B` (German male)
- `ja-JP-Neural2-B` (Japanese male)
- `pt-BR-Neural2-A` (Portuguese female)
- `zh-CN-Neural2-A` (Chinese female)

## Speaking Rate & Pitch Tuning

| Content type | Rate | Pitch | Why |
|-------------|------|-------|-----|
| Documentary narration | 0.9 - 1.0 | 0.0 | Measured, authoritative |
| Tutorial / explainer | 1.0 - 1.05 | 0.0 | Natural teaching pace |
| Energetic / social media | 1.1 - 1.2 | +1.0 to +2.0 | Upbeat, engaging |
| Dramatic / trailer | 0.85 - 0.95 | -2.0 to -1.0 | Weighty, cinematic |
| Rapid recap / highlights | 1.15 - 1.25 | 0.0 | Efficient delivery |

**Rule:** Never go below 0.8 (sounds drunk) or above 1.3 (sounds chipmunk).

## SSML Optimization

Google TTS supports full SSML. Use it for precise control:

### Pauses

```xml
<speak>
  First point about the topic.
  <break time="800ms"/>
  Now, the surprising part.
  <break time="1.2s"/>
  And here is why it matters.
</speak>
```

### Emphasis

```xml
<speak>
  This is <emphasis level="strong">critically important</emphasis> to understand.
</speak>
```

### Prosody (rate, pitch, volume in-line)

```xml
<speak>
  <prosody rate="slow" pitch="-2st">In the beginning, there was silence.</prosody>
  <break time="1s"/>
  <prosody rate="medium" pitch="+1st">Then everything changed.</prosody>
</speak>
```

### Say-as (numbers, dates, units)

```xml
<speak>
  The temperature is <say-as interpret-as="unit">25°C</say-as>.
  Revenue reached <say-as interpret-as="cardinal">1500000</say-as> dollars
  on <say-as interpret-as="date" format="mdy">03/15/2025</say-as>.
</speak>
```

**Note:** SSML support varies by voice tier. Chirp 3 HD and Journey may not support all SSML tags. Test with Neural2/WaveNet if SSML is critical.

## Multilingual Production

Google TTS's main advantage over ElevenLabs: **native support for 50+ languages** with high-quality voices.

### Language Matching Rules

1. **Always set `language_code`** to match the text language
2. **Voice must match language** — `en-US-Neural2-D` cannot speak French
3. **For mixed-language scripts**, generate segments per-language and stitch with audio_mixer

### Localization Workflow

1. Translate script per target language
2. Select the best voice per language (Neural2 minimum, Chirp 3 HD where available)
3. Match speaking rate to language rhythm (French ~0.95, Spanish ~1.05, Japanese ~1.0)
4. Generate and review per-language audio
5. Mix with common music/SFX track

## Comparison with ElevenLabs

| Dimension | Google TTS | ElevenLabs |
|-----------|-----------|------------|
| Languages | 50+ (broadest) | 29 |
| Voice cloning | No | Yes |
| Expressiveness | Good (Chirp 3 HD) | Best (v2, v3) |
| SSML support | Full | Limited (flash/turbo only) |
| Cost | $4-$30/1M chars | ~$30/1M chars |
| Consistency | Very high | High (v2), variable (v3) |

**When to pick Google TTS:**

- Multilingual/localization projects
- SSML precision needed
- Budget-conscious (Neural2 at $16/1M)
- Non-English primary language

**When to pick ElevenLabs:**

- Maximum expressiveness/emotion
- Voice cloning needed
- English-primary content
- Character voices
