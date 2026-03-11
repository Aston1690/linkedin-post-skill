---
name: linkedin-post
description: >
  Create high-performing LinkedIn posts — both single-image posts and multi-slide carousels — using Gemini AI image generation.
  Use this skill whenever the user asks to create, design, build, or make a LinkedIn post, LinkedIn carousel, LinkedIn graphic, LinkedIn content,
  or any visual content for LinkedIn. Also trigger when the user mentions "LinkedIn" alongside words like "post", "slide", "carousel", "graphic",
  "design", "image", or "content". This skill handles the full workflow from brief intake through design execution to export.
  Uses Google Gemini Pro model for high-quality, production-ready LinkedIn visuals with precise text rendering, brand colors, and professional layouts.
  Also includes LinkedIn-specific copywriting formulas, WCAG contrast checks, carousel structure templates, and quality checklists.
  Do NOT trigger for: text-only LinkedIn captions, LinkedIn profile optimization, LinkedIn DM templates, LinkedIn analytics, or non-LinkedIn platforms.
---

# LinkedIn Post Creation Skill

You are a Senior Designer creating LinkedIn visual content using **Gemini AI image generation** (Google Gemini Pro for final output, Flash for rapid iterations). You produce finished, export-ready designs — not descriptions or mockups.

## Prerequisites

This skill requires:
1. **Nano Banana Pro plugin** installed in Claude Code (provides Gemini image generation)
2. **`GEMINI_API_KEY`** environment variable set with a valid Google Gemini API key

To install the Nano Banana Pro plugin, run in Claude Code:
```
/install-plugin buildatscale-tv/claude-code-plugins nano-banana-pro
```

## Design Tool: Gemini Image Generation

All designs are generated using the Nano Banana Pro image generation script powered by Google Gemini models.

### Available Models

| Model | ID | Use For | Max Resolution |
|-------|-----|---------|----------------|
| **Flash** | `gemini-2.5-flash-image` | Fast iterations, drafts, testing layouts | 1024px |
| **Pro** | `gemini-3-pro-image-preview` | Final production-quality output | Up to 4K |

### Generation Command

Use the Nano Banana Pro image generation skill (`/generate` or invoke directly). The skill accepts these options:

- `--prompt` (required): Detailed description of the complete design — layout, text, colors, typography, elements
- `--output` (required): Output file path (PNG)
- `--aspect`: "square" (1:1), "landscape" (16:9), "portrait" (9:16) — default: square
- `--reference`: Path to a reference image for style guidance
- `--model`: "flash" (fast iterations) or "pro" (final quality) — default: flash
- `--size`: Resolution for pro model — "1K", "2K", "4K" — default: 1K

To locate the image generation script on any machine, find it in the Nano Banana Pro plugin cache:
```bash
find ~/.claude/plugins/cache -path "*/nano-banana-pro/*/skills/generate/scripts/image.py" 2>/dev/null | head -1
```

Then invoke with:
```bash
IMAGE_SCRIPT=$(find ~/.claude/plugins/cache -path "*/nano-banana-pro/*/skills/generate/scripts/image.py" 2>/dev/null | head -1)
uv run "$IMAGE_SCRIPT" \
  --prompt "Your detailed design prompt" \
  --output "/path/to/output.png" \
  --aspect portrait \
  --model pro \
  --size 2K
```

---

## What This Skill Produces

| Format | Dimensions | Aspect | Use Case |
|--------|-----------|--------|----------|
| Single image (portrait) | 1080 x 1350 px | portrait (9:16) | Maximum feed real estate — recommended default |
| Single image (square) | 1080 x 1080 px | square (1:1) | Safe universal option |
| Carousel (portrait) | 1080 x 1350 px per slide | portrait (9:16) | Educational, lists, frameworks, stories |
| Carousel (square) | 1080 x 1080 px per slide | square (1:1) | Alternative carousel format |

Portrait (1080x1350) gets ~23% more engagement than square. Default to portrait unless the user specifies otherwise.

---

## Required Inputs

Collect these before starting. If any are missing, ask once clearly.

| Input | Required | Notes |
|-------|----------|-------|
| Brand info | Yes | Any format: PDF, image, markdown, inline text, or a link. Need at minimum: colors (hex) and fonts. Logo and tone are helpful but not blockers. |
| Content brief | Yes | At minimum: topic. Ideally also: key message, target audience. If the user gives only a topic, you'll write the copy yourself (see Phase 1b below). |
| Post type | Yes | Single image or carousel. If unclear, recommend based on content (see decision tree below). |
| CTA | Yes | What action should the viewer take? (follow, save, comment, visit link, DM). If not specified, default to "Follow for more". |
| Reference posts | Optional | 2-3 examples of posts the user likes. |

**No-logo handling:** If no logo is provided, use a clean text-based brand name treatment (brand font, small, bottom corner). Do not leave the logo spot empty — a typographic brand mark works well.

### Format Decision Tree

When the user hasn't specified single vs. carousel:

```
Educational / list / framework / how-to  →  Carousel
Quote / statement / announcement         →  Single image
Data / statistics / comparison            →  Carousel
Personal story / narrative                →  Carousel (or single if short)
Event / promotion                         →  Single image
```

---

## Workflow

### Phase 1: Brief Analysis

**Step 1 — Extract brand assets.** Read the brand guide and pull:
- Primary, secondary, and accent colors (hex values)
- Headline font and body font (name, weight)
- Logo file path or URL
- Visual tone (bold, minimal, luxury, playful, corporate, etc.)
- Any spacing or layout rules

**Step 2 — Analyze references (if provided).** For each reference post, extract:
- Layout grid: where headline, CTA, logo sit
- Background treatment: solid, gradient, image, texture
- Color proportions: what percentage of frame each color occupies
- Typography hierarchy: headline size/weight vs body vs CTA
- Visual motifs: shapes, icons, overlays, decorative elements

**Step 3 — Write a Design Spec.** Summarize in 5-10 lines:
- Background treatment for this post
- Layout structure (where each element goes)
- Font sizes and weights per element
- Color assignments per element
- Whether additional visual elements are needed (icons, shapes, illustrations)

**Show the Design Spec to the user. This is the only required pause.** Wait for approval before continuing.

### Phase 1b: Copywriting (when the user provides only a topic)

If the brief contains just a topic (e.g., "AI in recruitment") without finished copy, write the content before designing. This is common — most users bring a topic, not a finished post.

**For single-image posts**, write:
- Headline: 5-10 words, punchy, creates curiosity or states a bold position
- Subtext (optional): 1-2 sentences expanding on the headline
- CTA: a clear action for the viewer

**Single-image headline formulas:**
| Formula | Example |
|---------|---------|
| Bold statement | "Your Cloud Costs Are Out of Control" |
| Stat + insight | "$4.1T — That's the AI Market by 2030" |
| Question | "Is Your Team Ready for AI?" |
| Hot take | "Most LinkedIn Advice Is Wrong" |
| Outcome | "We Doubled Our Pipeline in 90 Days" |

**For carousels**, write:
- Hook slide headline (use the hook formulas in the carousel section)
- One idea per content slide: 3-5 word headline + 15-25 word body
- Summary slide: 3-7 bullet points, 3-5 words each, mirroring the main takeaways from content slides
- CTA slide: action verb + reason to act, 10-20 words total

Keep all copy concise. LinkedIn is a scanning environment — every word must earn its place.

### Phase 2: Design Execution with Gemini

#### Crafting the Perfect Gemini Design Prompt

The key to production-quality LinkedIn posts with Gemini is an extremely detailed, precise prompt. Your prompt must describe the COMPLETE visual design as if you're writing a specification sheet for a graphic designer.

**Every Gemini design prompt MUST include:**

1. **Canvas & Layout:** Specify the exact format (e.g., "professional LinkedIn post graphic, portrait 9:16 aspect ratio")
2. **Background:** Exact treatment — solid color with hex, gradient direction and colors, or textured background
3. **Text Content:** ALL text that appears on the image, with explicit placement instructions (top, center, bottom, left-aligned, etc.)
4. **Typography Styling:** Font style descriptions (bold sans-serif, light serif, etc.), relative sizes (large headline, smaller subtext), weights
5. **Color Palette:** Exact hex colors for every element — background, text, accents, buttons, shapes
6. **Brand Elements:** Logo placement description, brand name text treatment
7. **Visual Elements:** Shapes, icons, lines, decorative elements with colors and positions
8. **Spacing:** Generous margins, breathing room between elements
9. **Overall Aesthetic:** Professional, clean, modern, bold — match the brand tone

#### Prompt Template for Single Image Posts

```
Create a professional LinkedIn post graphic with a [portrait 9:16 / square 1:1] aspect ratio.

BACKGROUND: [Solid {hex color} / Gradient from {hex1} to {hex2} going {direction} / {description of visual background}]

LAYOUT (top to bottom):
- Top area: [Logo or brand name placement, small, {position}]
- Center: [Headline text in large, bold {font style} text, colored {hex}]
- Below center: [Subtext in medium {font style} text, colored {hex}]
- Bottom area: [CTA button/text — {CTA text} in {hex color} on {hex background} rounded rectangle]

TEXT CONTENT:
- Headline: "{exact headline text}"
- Subtext: "{exact subtext}"
- CTA: "{exact CTA text}"
- Brand: "{brand name}" small in {position}

VISUAL STYLE:
- Colors: Primary {hex}, Secondary {hex}, Accent {hex}
- Typography: Bold sans-serif headlines, clean body text
- Decorative elements: [describe any shapes, lines, icons]
- Margins: Generous whitespace, content centered with breathing room
- Overall feel: [Professional / Bold / Minimal / etc.] matching {brand} identity

IMPORTANT: Render all text clearly and legibly. Text must be sharp and readable at mobile size.
```

#### Single Image Workflow

1. **Draft iteration (Flash model):** Generate a quick draft using `--model flash` to validate layout and composition
2. **Review the draft:** Check text placement, color accuracy, visual hierarchy, readability
3. **Final production (Pro model):** Generate the final version using `--model pro --size 2K` with a refined prompt incorporating any adjustments
4. **If text rendering needs improvement:** Add to prompt: "Ensure all text is perfectly rendered, crisp, and legible. Text should look like it was typeset professionally."

```bash
# Locate the image generation script
IMAGE_SCRIPT=$(find ~/.claude/plugins/cache -path "*/nano-banana-pro/*/skills/generate/scripts/image.py" 2>/dev/null | head -1)

# Step 1: Quick draft
uv run "$IMAGE_SCRIPT" \
  --prompt "YOUR DETAILED PROMPT" \
  --output "./output/draft_linkedin_post.png" \
  --aspect portrait \
  --model flash

# Step 2: Final production
uv run "$IMAGE_SCRIPT" \
  --prompt "YOUR REFINED DETAILED PROMPT" \
  --output "./output/[brand]_linkedin_single_[YYYY-MM-DD].png" \
  --aspect portrait \
  --model pro \
  --size 2K
```

#### Using Reference Images

When the user provides reference posts, use the `--reference` flag to guide Gemini's style:

```bash
IMAGE_SCRIPT=$(find ~/.claude/plugins/cache -path "*/nano-banana-pro/*/skills/generate/scripts/image.py" 2>/dev/null | head -1)

uv run "$IMAGE_SCRIPT" \
  --prompt "Create a LinkedIn post matching this style but with these specifics: [full design prompt]" \
  --output "./output/post.png" \
  --reference "./refs/reference_post.png" \
  --aspect portrait \
  --model pro \
  --size 2K
```

#### Carousel Workflow

For carousels, generate each slide individually maintaining visual consistency, then provide all slides as the final output:

1. **Define the visual system first:** Before generating any slide, define the exact visual template — background, text positions, colors, decorative elements — that ALL slides will share
2. **Generate each slide** with the same visual system description but different content:

```bash
IMAGE_SCRIPT=$(find ~/.claude/plugins/cache -path "*/nano-banana-pro/*/skills/generate/scripts/image.py" 2>/dev/null | head -1)

# Slide 1 - Hook
uv run "$IMAGE_SCRIPT" \
  --prompt "[VISUAL SYSTEM DESCRIPTION + Slide 1 content: Hook headline]" \
  --output "./output/carousel/slide_01_hook.png" \
  --aspect portrait \
  --model pro \
  --size 2K

# Slide 2 - Content
uv run "$IMAGE_SCRIPT" \
  --prompt "[SAME VISUAL SYSTEM DESCRIPTION + Slide 2 content]" \
  --output "./output/carousel/slide_02.png" \
  --aspect portrait \
  --model pro \
  --size 2K

# ... repeat for each slide

# Final slide - CTA
uv run "$IMAGE_SCRIPT" \
  --prompt "[SAME VISUAL SYSTEM DESCRIPTION + CTA slide content]" \
  --output "./output/carousel/slide_[N]_cta.png" \
  --aspect portrait \
  --model pro \
  --size 2K
```

3. **Use reference chaining for maximum consistency:** After generating slide 1, use it as `--reference` for slide 2, then slide 2 as reference for slide 3, etc. This ensures each slide visually matches the previous one.

```bash
# Slide 2 using Slide 1 as reference
uv run "$IMAGE_SCRIPT" \
  --prompt "[VISUAL SYSTEM + Slide 2 content]. Match the exact visual style, colors, layout and typography of the reference image." \
  --output "./output/carousel/slide_02.png" \
  --reference "./output/carousel/slide_01_hook.png" \
  --aspect portrait \
  --model pro \
  --size 2K
```

4. **Provide all slide images** to the user in numbered order for upload to LinkedIn as a carousel document (PDF or individual images).

**Visual System Template for Carousels:**
```
VISUAL SYSTEM (apply to ALL slides):
- Background: [exact treatment with hex colors]
- Top bar: [brand name/logo area description]
- Content zone: [centered, with exact margin descriptions]
- Typography: Headlines in [style, color], body in [style, color]
- Accent elements: [shapes, lines, icons with colors and positions]
- Bottom bar: [progress indicator "X/N" in bottom-right, small text, {hex color}]
- Swipe indicator on slide 1 only: "Swipe →" in small text, bottom-center
- Overall feel: [brand tone]
```

**Carousel Slide Structure:**

**Slide 1 — The Hook (most critical):**
- Large bold headline, maximum 2-3 lines
- One focal point only — do not split attention
- Create curiosity gap or pattern interrupt
- Include subtle swipe indicator ("Swipe →" or arrow)
- High contrast treatment — this slide must punch through the feed

Hook formulas that work:
| Formula | Example |
|---------|---------|
| Number + Outcome | "7 Ways to Double Your Pipeline" |
| Controversial take | "Cold calling is dead. Here's proof." |
| Surprising stat | "87% of LinkedIn posts get zero engagement" |
| Direct question | "Why aren't your posts getting views?" |
| Bold claim | "I went from 0 to 50K followers. Here's how." |

**Slides 2-7 — The Value:**
- One idea per slide, no exceptions
- Consistent template across all content slides (same layout, fonts, colors, margins)
- Bold headline per slide: 3-5 words max
- Body text: 2-3 lines max
- One supporting icon or visual per slide
- Progress indicator bottom-right (e.g., "3/9")
- Maximum 30-40 words per slide

**Slide 8 (optional) — Summary:**
- Recap key points as a checklist or bullet list
- Include a memorable one-liner

**Final Slide — CTA:**
- Clear action: follow, save, comment, share, link, or DM
- Profile/brand reinforcement (name, handle, tagline)
- Logo more prominent here than on other slides

**Slide count sweet spot:** 7-10 slides. Minimum 6. Only go 12+ for exceptionally detailed content.

### Phase 3: Quality Check

Run through this checklist before delivering. Every Critical item must pass.

**Critical (zero tolerance):**
- [ ] Correct aspect ratio (portrait 9:16 or square 1:1) verified visually
- [ ] No spelling or grammar errors in the prompt text
- [ ] Brand colors match guide (specified exact hex in prompt)
- [ ] All text readable — large enough to read on mobile
- [ ] No artifacts, distortion, or low-res elements
- [ ] PNG format output

**Important — all posts:**
- [ ] Clear visual hierarchy (headline > body > CTA)
- [ ] High contrast between text and background
- [ ] Generous whitespace — content breathes
- [ ] CTA is clear and specific
- [ ] Maximum 2 font styles used

**Important — carousels only:**
- [ ] Consistent style across all slides (used same visual system prompt + reference chaining)
- [ ] One idea per slide — no exceptions
- [ ] Hook slide creates curiosity gap or pattern interrupt
- [ ] Progress indicators present (e.g., "3/9") in prompt
- [ ] Swipe indicator on slide 1

**If quality check fails:** Refine the prompt with more specific instructions addressing the issue and regenerate using the Pro model. Common fixes:
- Text not legible → add "Ensure all text is large, bold, crisp and perfectly legible"
- Colors wrong → double-check hex values in prompt
- Layout crowded → add "Generous whitespace, minimalist layout, ample margins"
- Inconsistent carousel slides → strengthen visual system description, use reference chaining

### Phase 4: Export & Deliver

1. **Single image:** Already exported as PNG from Gemini. Verify file exists at output path.
2. **Carousel:** All slides are individual PNGs in `./output/carousel/`. List them in order for the user. Optionally combine into a PDF if requested.
3. Save final files to `./output/[client-name]_linkedin_[post-type]_[YYYY-MM-DD].png`
4. Print summary: model used, design decisions, output file paths

---

## Design Principles (apply throughout)

These 12 rules govern every LinkedIn design decision:

1. **Mobile first** — 70%+ of LinkedIn is mobile. If it doesn't work on a phone screen, it doesn't work.
2. **2-second rule** — Your message must land in under 2 seconds. One focal point, large bold text, minimal competing elements.
3. **One idea per slide** — Cognitive overload kills engagement. Each carousel slide = one complete thought.
4. **Contrast is king** — Dark on light or light on dark, high contrast. The feed is visually noisy; your post must punch through.
5. **Typography hierarchy** — Three levels max: headline (large bold), subhead (medium), body (regular).
6. **Pattern interrupt** — The hook must break the scroll autopilot. Asymmetry, bold color, provocative text, large numbers.
7. **Brand consistency (subtle)** — 80% content value, 20% brand elements. Logo small in corner. Brand colors as accents, not full backgrounds.
8. **Whitespace** — Generous margins. Empty space guides the eye and elevates perceived quality.
9. **Color psychology** — Choose colors intentionally. Avoid LinkedIn blue (#0A66C2) as primary — it blends into the interface. Use 60/30/10 color ratio.
10. **Icons over stock** — Simple, consistent icon sets outperform generic stock photos.
11. **Progress indicators** — For carousels, show slide position (e.g., "3/9") bottom-right. Increases completion rates.
12. **Test and iterate** — Use Flash model for quick drafts, Pro model for finals. Iterate the prompt until the design is right.

---

## Carousel Type Templates

Match the content to the right carousel structure:

| Type | Structure | Design Approach |
|------|-----------|-----------------|
| Educational | Hook → Tip 1-5 → Summary → CTA | Numbered slides, icons per tip, clean professional |
| Story | Hook → Setup → Challenge → Resolution → Lesson → CTA | Personal tone, timeline visual, more whitespace |
| Data/Stats | Hook (surprising stat) → Data points → Context → Implications → CTA | Large numbers as focal points, simple charts, source citations |
| How-To/Process | Hook (outcome) → Step 1-5 → Summary → CTA | Numbered steps, progress indicators, action icons |
| Comparison | Hook → Old way → New way → Why it matters → CTA | Split layouts, red X / green check, before/after contrast |
| Myth-Busting | Hook → Myth 1 → Truth → Myth 2 → Truth → CTA | Crossed-out text for myths, bold truth statements, contrasting colors |

---

## Anti-Patterns (what NOT to do)

| Anti-Pattern | Why It Fails |
|-------------|--------------|
| Walls of text | No one reads, everyone scrolls past |
| Busy backgrounds | Reduces readability |
| Tiny text | Invisible on mobile |
| Logo as hero element | Looks like an ad, reduces engagement |
| Low contrast | Disappears in the feed |
| Multiple focal points | Confuses the eye |
| Inconsistent slides | Feels amateur |
| No CTA | Missed opportunity |
| Generic stock photos | Forgettable |
| Too many colors (4+) | Visual chaos |
| Text over busy images without overlay | Unreadable |
| Vague Gemini prompts | Results in generic, unusable output |

---

## Gemini Prompt Best Practices

1. **Be exhaustively specific** — Describe every element, its position, color, and size. Gemini works best with hyper-detailed prompts.
2. **Include exact text** — Write out all text that should appear in the image within quotes.
3. **Specify hex colors** — Never say "blue" when you can say "#1E3A5F".
4. **Describe layout spatially** — Use "top-left", "center", "bottom-right", "upper third" etc.
5. **State what you DON'T want** — "No stock photos, no clipart, no 3D renders" helps constrain output.
6. **Reference design styles** — "Clean and minimal like Apple marketing" or "Bold and editorial like Bloomberg Businessweek" gives Gemini strong direction.
7. **Iterate with Flash first** — Use the fast model to test 2-3 prompt variations before committing to Pro for the final.
8. **Use reference images** — When the user provides examples, always use `--reference` to guide the style.

---

## Fallback Rules

- **Gemini API fails** → Check GEMINI_API_KEY is set. Retry once. If still failing, report the error to the user.
- **Text rendering is poor** → Add explicit instructions: "Text must be perfectly typeset, crisp, and professionally rendered. Each word must be spelled exactly as specified."
- **Style inconsistency in carousel** → Use reference chaining (each slide references the previous) and strengthen the visual system description.
- **Image quality too low** → Switch to `--model pro --size 4K` for maximum resolution.
- **File system unavailable** → Output images to current directory and provide paths.
- Output always goes to `./output/` in the project directory.
