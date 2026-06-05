---
name: fal-video-prompting
description: |
  fal.ai video generation prompting guide. Provider-specific techniques for Kling v3, MiniMax/Hailuo, and Veo 3.1 via the fal.ai gateway. Covers prompt structure per provider, camera direction syntax, image-to-video strategies, provider selection decision matrix, cost optimization, and multi-clip production workflows.
metadata:
  openclaw:
    requires:
      env:
        - FAL_KEY
    primaryEnv: FAL_KEY
---

# fal.ai Video Generation — Prompting Guide

Use this skill before generating video clips via the fal.ai gateway. Each provider (Kling, MiniMax, Veo) has different prompt strengths. This skill teaches you to exploit each one.

## Provider Selection Matrix

| Need | Best Provider | Model | Cost | Why |
|------|-------------|-------|------|-----|
| **Highest visual fidelity** | Kling | v3/standard | ~$0.40 | Best detail, skin textures, lighting |
| **Best camera control** | MiniMax | hailuo-02/pro | ~$0.25 | Follows framing/motion directions precisely |
| **Built-in audio + dialogue** | Veo | veo3.1 | ~$0.50 | Only provider with native audio generation |
| **Fast iteration / drafts** | MiniMax | hailuo-2.3-fast/standard | ~$0.08 | Cheapest, fast, good enough for layout |
| **Image-to-video** | Kling | v3/standard | ~$0.40 | Best at preserving reference image identity |
| **Nature / landscapes** | Veo | veo3.1 | ~$0.50 | Exceptional natural environments |
| **Character close-ups** | Kling | v3/standard | ~$0.40 | Most consistent faces and expressions |
| **Abstract / motion graphics** | MiniMax | hailuo-02/standard | ~$0.15 | Follows compositional prompts well |
| **Product shots** | Kling | v2.1/master | ~$0.30 | Clean, commercial-quality objects |

### Decision Flow

```
Need audio in the clip?
  YES → Veo 3.1
  NO → Need best visual quality?
    YES → Is it character/face focused?
      YES → Kling v3
      NO  → Kling v3 or Veo 3.1
    NO → Need fast/cheap?
      YES → MiniMax hailuo-2.3-fast
      NO  → MiniMax hailuo-02/pro
```

## Prompt Structure — Universal Rules

All fal.ai video providers respond to this structure:

```
[Shot type + camera movement] + [Subject with specifics] + [Action/motion] +
[Environment + lighting] + [Mood/style] + [Technical details]
```

### Always Include

1. **Camera direction** — pan, tilt, dolly, static, handheld, drone, tracking
2. **Subject motion** — what moves, how, how fast
3. **Lighting** — golden hour, neon, overcast, studio, rim lighting
4. **Duration awareness** — 5s clips need simple motion; 10s clips need progression

### Always Avoid

- **Multiple scene changes** in one clip — each clip = one continuous shot
- **Complex multi-character interactions** — keep to 1-2 subjects
- **Text/UI elements** — video models can't render readable text
- **Abrupt changes** — describe smooth, continuous motion

## Kling v3 — Cinematic Fidelity

Kling excels at photorealistic quality and character consistency.

### Prompt Techniques

**Character shots:**

```
Close-up of a woman in her 30s with dark curly hair and warm brown eyes,
wearing a denim jacket, looking directly at camera with a slight smile.
Soft studio lighting from the left, shallow depth of field, warm color grading.
Static camera, slight natural head movement. 5 seconds.
```

**Action sequences:**

```
Tracking shot following a runner sprinting through a rainy city street at night,
neon signs reflecting on wet pavement, camera matching their pace from the side.
Shallow depth of field, anamorphic lens flare, cinematic color grading with
teal and orange tones. 10 seconds.
```

**Product shots:**

```
Slow 360-degree orbit around a matte black wireless headphone on a marble surface,
soft studio lighting with gradient background transitioning from dark to light.
Clean commercial photography style, shallow depth of field. 10 seconds.
```

### Kling-Specific Tips

- **v3/standard** is the default — use it unless budget is tight
- **v2.1/master** is cheaper and still excellent for products and environments
- **Duration 5s** for single-motion shots, **10s** for camera movements with progression
- **Image-to-video**: provide a clean, high-resolution reference. Kling preserves identity well.
- Kling generates **native audio** — ambient sounds are often included automatically

### Camera Direction Syntax (Kling)

```
"Slow dolly in..."          — forward camera push
"Tracking shot..."          — camera follows subject laterally
"Crane shot rising..."      — vertical camera lift
"Handheld, slightly shaky." — documentary feel
"Static tripod shot."       — locked-off frame
"Slow zoom on..."           — lens zoom (no camera movement)
"Aerial drone, descending..." — birds-eye approaching
```

## MiniMax/Hailuo — Prompt-Following Champion

MiniMax is the most obedient to camera directions and compositional instructions.

### Prompt Techniques

**Camera-driven B-roll:**

```
Smooth dolly shot pushing through a modern co-working space, passing desks
with open laptops and coffee cups, morning sunlight streaming through floor-
to-ceiling windows creating long shadows. Soft, warm color palette. 5 seconds.
```

**Graphic/abstract motion:**

```
Abstract geometric shapes made of translucent glass, slowly rotating and
intersecting against a deep navy background. Soft caustic reflections and
prismatic light refractions. Minimal, clean, modern design aesthetic.
Static camera, slow motion. 5 seconds.
```

**Atmospheric environments:**

```
Wide establishing shot of a misty mountain valley at dawn, camera slowly
panning right revealing a small village with smoking chimneys. Volumetric
fog in the valley, warm golden light breaking through clouds. Cinematic
widescreen framing. 10 seconds.
```

### MiniMax-Specific Tips

- **hailuo-02/pro** for final assets — best balance of quality and cost
- **hailuo-2.3-fast/standard** for drafts — fastest generation, cheapest
- MiniMax excels at **following compositional instructions** — describe exact framing
- Strong at **camera movement descriptions** — uses them more literally than other providers
- Less strong at **face detail** — prefer Kling for character close-ups
- Describe the **entire motion arc** for 10s clips: "starts with... then reveals... ending on..."

### Camera Direction Syntax (MiniMax)

MiniMax responds particularly well to film terminology:

```
"Steadicam walk-and-talk..."   — smooth tracking
"Dutch angle, slowly tilting..." — stylistic tilt
"Rack focus from foreground to..." — depth-of-field shift
"Push-in on..."                — dramatic approach
"Pull-out revealing..."        — context expansion
"Whip pan to..."               — fast directional cut
```

## Veo 3.1 — Audio-Integrated Video

Veo is the only provider that generates **synchronized audio** (dialogue, ambient, music).

### Prompt Techniques

**Dialogue scene:**

```
A barista behind a coffee counter says "Here's your usual, enjoy!" while
handing over a steaming cup. The customer replies "Thanks, smells amazing."
Warm cafe ambiance, espresso machine hissing in the background, soft
indie music playing. Medium shot, slight handheld movement. 8 seconds.
```

**Ambient audio scene:**

```
Aerial drone shot slowly descending over a tropical beach at sunset.
Waves crashing on shore, seagulls calling, gentle wind. Camera starts
high, descends to waist height approaching the water. Golden hour
lighting, vibrant colors. 10 seconds.
```

**Nature with soundscape:**

```
Close-up of a campfire crackling at night, sparks floating up into a
star-filled sky. Fire popping and hissing sounds, distant crickets.
Camera slowly tilts up from the flames to the Milky Way. 10 seconds.
```

### Veo-Specific Tips

- **veo3.1** for maximum quality — **veo3.1/fast** for 2x speed at slight quality loss
- **Always describe the audio** in the prompt — Veo generates what you describe
- **Dialogue works** — describe who speaks, what they say, in what tone
- **Ambient sound follows the scene** — describe specific sounds for best results
- **Native audio is baked in** — can't separate tracks afterward. Generate SFX separately if you need mixing control.
- Best for **establishing shots** and **atmospheric sequences** where audio matters
- Duration: supports 5-10s clips

### Audio Prompting for Veo

Include audio cues in the visual prompt:

```
Good: "...birds singing, leaves rustling, distant stream"
Good: "...mechanical hum, keyboard typing, office chatter"
Good: "A narrator says 'Welcome to the future' in a deep voice"
Bad:  "...with background music" (too vague — describe the music)
Bad:  (no audio description at all — you'll get random audio)
```

## Image-to-Video Strategies

All three providers support image-to-video. Choose wisely:

| Strategy | Provider | Tip |
|----------|---------|-----|
| **Animate a hero image** | Kling v3 | Describe only the motion, not the scene (it's in the image) |
| **Product animation** | Kling v2.1/master | "Slow orbit around the product, studio lighting" |
| **Landscape pan** | Veo 3.1 | "Camera slowly pans across the scene, birds chirping" |
| **Abstract motion** | MiniMax | "Shapes begin to float and rotate, soft transitions" |

### Image-to-Video Prompt Rules

1. **Don't re-describe the image** — the model sees it. Describe only what should change/move.
2. **Specify the camera, not the content** — "slow zoom in on the subject's face" not "a person with brown hair..."
3. **Keep motion simple** — subtle movement > dramatic action for image-to-video
4. **High-res input** — provide at least 1024px on the longest side

## Multi-Clip Production Workflow

When generating multiple clips for a video:

### 1. Plan the Shot List

Map each scene to a provider:

```
Scene 1 (hook/intro):     Kling v3     — character close-up, dramatic
Scene 2 (problem):        MiniMax pro  — B-roll montage, camera-driven
Scene 3 (solution):       MiniMax pro  — product demo, tracking shot
Scene 4 (proof):          Veo 3.1      — testimonial with dialogue
Scene 5 (CTA):            Kling v3     — character direct-to-camera
```

### 2. Visual Consistency

- Use the **same aspect ratio** across all clips (16:9 or 9:16)
- Include **consistent lighting direction** in all prompts ("lighting from the left")
- Specify **consistent color grading** ("warm teal-and-orange color grading")
- For character consistency: use **image-to-video** with the same reference image

### 3. Generate in Parallel

fal.ai supports concurrent requests. Generate all clips simultaneously:

- Run Kling, MiniMax, and Veo calls in parallel (different endpoints)
- Same-provider clips queue on fal.ai's side — no rate limit concern for normal volume

### 4. Review and Iterate

- Watch each clip for: motion coherence, visual quality, prompt adherence
- Regenerate weak clips only — don't redo the entire batch
- Use MiniMax fast for quick replacement iterations, upgrade to pro/Kling for finals

## Cost Optimization

| Strategy | Savings | How |
|----------|---------|-----|
| **Draft with MiniMax fast** | 5-8x cheaper | Use hailuo-2.3-fast/standard for layout, upgrade for finals |
| **5s over 10s** | 2x cheaper | Use 5s clips where motion is simple |
| **Batch similar shots** | Time savings | Group by provider, run in parallel |
| **Skip audio generation** | Use Veo only when audio needed | Generate SFX separately with ElevenLabs for mixing control |
| **Image-to-video for consistency** | Fewer retakes | Reference images reduce style drift |
