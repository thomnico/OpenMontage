---
name: elevenlabs-production
description: |
  ElevenLabs production-grade audio prompting for video pipelines. Covers voice casting by video type, narration style presets, music prompting by mood/genre, SFX layering strategy, French voice recommendations, and audio mastering workflow (levels, ducking, fades). Use alongside the base elevenlabs skill for API reference.
metadata:
  openclaw:
    requires:
      env:
        - ELEVENLABS_API_KEY
    primaryEnv: ELEVENLABS_API_KEY
---

# ElevenLabs — Production Audio Guide

Use this skill when producing audio for video pipelines. The base `elevenlabs` skill covers API code; this skill covers **what to generate and how to prompt for cinematic-quality results**.

## Voice Casting Matrix

Choose voice + settings based on video type, not personal preference.

### English Voices

| Video Type | Voice | Voice ID | stability | similarity | style | speed | Why |
|-----------|-------|----------|-----------|------------|-------|-------|-----|
| Explainer / educational | George | `JBFqnCBsd6RMkjVDRZzb` | 0.80 | 0.90 | 0.05 | 1.0 | Warm authority, clear diction |
| Documentary / cinematic | George | `JBFqnCBsd6RMkjVDRZzb` | 0.85 | 0.90 | 0.00 | 0.92 | Slower, gravitas |
| Tutorial / how-to | Rachel | `21m00Tcm4TlvDq8ikWAM` | 0.75 | 0.85 | 0.10 | 1.0 | Approachable clarity |
| Social media / energetic | Rachel | `21m00Tcm4TlvDq8ikWAM` | 0.40 | 0.75 | 0.55 | 1.10 | Punchy, engaging |
| Corporate / SaaS | Adam | `pNInz6obpgDQGcFmaJgB` | 0.85 | 0.90 | 0.00 | 1.0 | Neutral professional |
| Trailer / hype | Adam | `pNInz6obpgDQGcFmaJgB` | 0.70 | 0.85 | 0.30 | 0.88 | Dramatic weight |
| Podcast / conversational | Any | — | 0.45 | 0.80 | 0.40 | 0.95 | Natural cadence |

### French Voices

ElevenLabs has strong French support on `eleven_multilingual_v2`. Recommended approach:

1. **List French voices:** `client.voices.get_all()` → filter by `labels.language == "fr"`
2. **Best native-quality:** Look for voices tagged `french` with high `similarity_boost`
3. **Fallback:** George and Rachel both handle French text on multilingual_v2, but with slight accent

**French voice settings adjustment:**

- Increase `stability` by +0.05 (French prosody benefits from consistency)
- Set `speed` to 0.95 (French narration pacing is naturally slower than English)
- Use `eleven_multilingual_v2` — never use monolingual models for French

### Model Selection for Production

| Scenario | Model | Rationale |
|----------|-------|-----------|
| **Final deliverable** | `eleven_multilingual_v2` | Most consistent, zero SSML surprises |
| **Script iteration / drafts** | `eleven_flash_v2_5` | Fast, cheap, good enough to judge pacing |
| **Precise pause control** | `eleven_flash_v2_5` | Only model with reliable `<break>` SSML |
| **Maximum emotion** | `eleven_v3` | Alpha — generate 3 takes, pick best. Budget 3x cost. |
| **Multilingual / French** | `eleven_multilingual_v2` | Only reliable model for non-English |

## Narration Prompting Patterns

### Section-by-Section Generation

Never generate an entire script in one API call. Break by section for:

- Better pacing control
- Easier retakes (re-generate one section, not the whole thing)
- Audio-driven scene timing (each section's duration drives its scene)

```python
sections = [
    {"id": "hook", "text": "Did you know that..."},
    {"id": "problem", "text": "Most people think..."},
    {"id": "solution", "text": "But here's what actually works..."},
    {"id": "cta", "text": "Try it yourself..."},
]

for section in sections:
    audio = client.text_to_speech.convert(
        text=section["text"],
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(stability=0.80, similarity_boost=0.90, style=0.05, speed=1.0),
    )
    save(audio, f"audio/{section['id']}.mp3")
```

### Pacing by Section Type

| Section | Speed | Stability | Tip |
|---------|-------|-----------|-----|
| Hook (opening) | 1.0-1.05 | 0.60 | Slightly more dynamic to grab attention |
| Exposition | 1.0 | 0.80 | Clear, steady |
| Climax / reveal | 0.90-0.95 | 0.70 | Slower for impact, lower stability for drama |
| Call-to-action | 1.05-1.10 | 0.75 | Energetic close |
| Transition phrases | 1.0 | 0.85 | Neutral bridge |

### Text Preparation

Before sending text to ElevenLabs:

1. **Spell out numbers:** "5 million" → "five million" (prevents weird pronunciation)
2. **Phonetic spelling for jargon:** "nginx" → "engine-x", "kubectl" → "kube-control"
3. **Add commas for natural pauses:** "Now, here's the thing, most people..."
4. **Remove markdown formatting:** Strip `**bold**`, `*italic*`, `#headers`
5. **One sentence per paragraph** for multilingual_v2 (it reads paragraph breaks as pauses)

## Music Prompting for Video

### Genre-to-Video-Type Matrix

| Video Type | Genre prompt | Tempo | Duration tip |
|-----------|-------------|-------|-------------|
| Explainer | "Upbeat electronic, clean synths, positive, modern" | 120-130 BPM | Match total video length |
| Documentary | "Ambient orchestral, slow strings, atmospheric, contemplative" | 70-80 BPM | Can loop; match act length |
| Trailer | "Cinematic epic, building drums, brass swells, tension" | 90-100 BPM | 60-90s with build and drop |
| Tutorial | "Light acoustic, gentle guitar, warm, minimal" | 90-110 BPM | Background-safe, low energy |
| Social media | "Lo-fi hip hop, chill beats, jazzy piano, relaxed" | 80-90 BPM | 30-60s, loopable |
| Corporate | "Modern corporate, subtle piano, ambient pads, optimistic" | 100-110 BPM | Neutral, non-distracting |
| Sports / hype | "Trap beats, aggressive bass, high energy, anthemic" | 140-160 BPM | Short bursts, 15-30s clips |

### Music Prompt Structure

```
[Genre/style] + [Key instruments] + [Mood/energy] + [Context] + [Constraints]
```

**Good examples:**

```
"Ambient electronic, soft synth pads and gentle arpeggios, dreamy and ethereal, 
for a science documentary about space, no vocals, slow build"

"Indie folk, acoustic guitar fingerpicking with light percussion, 
warm and nostalgic, for a travel vlog montage, 90 BPM"

"Dark cinematic, deep cello and distant piano, tension building slowly, 
for a mystery thriller trailer, 70 BPM, no vocals"
```

**Always add:** `force_instrumental=True` for background music. Vocals compete with narration.

### Duration Matching

- Generate music 5-10% longer than the video — easier to trim than to extend
- For looping background: generate 30-60s and loop in audio_mixer
- For builds/drops: match to video structure (e.g., 30s build + 10s drop for reveal moment)

## Sound Effects Prompting

### Layering Strategy for Video

Videos need 3 SFX layers minimum:

| Layer | Purpose | `prompt_influence` | Duration |
|-------|---------|-------------------|----------|
| **Ambient bed** | Continuous atmosphere | 0.3-0.4 | 10-22s, looped |
| **Transition hits** | Scene changes | 0.6-0.8 | 0.5-2s |
| **Accent foley** | Key moments | 0.7-0.9 | 0.5-3s |

### Ambient Bed Prompts

```
"Soft office ambiance, keyboard typing, distant voices, air conditioning hum"
"City street atmosphere, light traffic, pedestrians, birds, distant construction"
"Nature forest, gentle wind through trees, bird song, stream water"
"Dark futuristic laboratory hum, electronic beeps, distant machinery"
```

Set `loop=True` and `duration_seconds=15` for seamless ambient beds.

### Transition Sound Prompts

```
"Digital glitch transition, short electronic swoosh"           → scene change
"Soft whoosh, gentle air movement, 1 second"                   → subtle transition
"Cinematic boom, deep sub bass impact, dramatic"               → dramatic reveal
"Paper page turn, crisp and close, single page"                → chapter change
"Camera shutter click, mechanical, single shot"                → photo reveal
```

### Accent / Foley Prompts

```
"Notification chime, bright and modern, single ping"           → UI element
"Typing on mechanical keyboard, short burst, 3 keystrokes"     → tech scene
"Cash register cha-ching, satisfying metallic ring"            → money/value
"Pen writing on paper, scratchy, quick signature"              → document scene
"Glass clink, champagne toast, celebratory"                    → success moment
```

### Prompt Quality Rules

1. **Specify duration in the prompt** — "1 second" or "short burst" helps the model
2. **Name the material/surface** — "metal on wood" beats "impact sound"
3. **Reference the perspective** — "close-up" vs "distant" changes the spatial quality
4. **One sound per generation** — don't layer in the prompt; generate separately and mix

## Audio Mastering Workflow

After generating all audio assets, mix them for the final video:

### Level Targets

| Track | Target level | Role |
|-------|-------------|------|
| Narration | -14 to -16 LUFS | Primary — always on top |
| Music | -24 to -28 LUFS | Background — never compete with voice |
| SFX ambient | -30 to -35 LUFS | Subliminal atmosphere |
| SFX accents | -18 to -22 LUFS | Brief punches above music |

### Ducking Pattern

Music ducks when narration plays. Use audio_mixer or ffmpeg sidechain:

```bash
# Simple approach: generate two music versions
# 1. Full volume for intro/outro (no narration)
# 2. Reduced -10dB for narrated sections
ffmpeg -i music.mp3 -filter:a "volume=-10dB" music_ducked.mp3
```

### Final Mix Order

1. **Lay narration** — this is the timing master
2. **Add ambient bed** — loop under entire duration
3. **Add music** — full volume intro, duck during narration, full volume outro
4. **Add transition SFX** — at each scene cut point
5. **Add accent foley** — at key visual moments
6. **Normalize** — target -14 LUFS integrated for YouTube/social

## Production Checklist

Before declaring audio complete:

- [ ] All narration sections generated and listened to
- [ ] Pronunciation issues fixed (phonetic spelling or retake)
- [ ] Music genre matches video mood
- [ ] Music is instrumental (no competing vocals)
- [ ] Ambient bed loops cleanly
- [ ] Transition sounds placed at scene boundaries
- [ ] Narration sits above music at all times
- [ ] Total audio length matches video timeline
- [ ] French content uses `eleven_multilingual_v2` model
