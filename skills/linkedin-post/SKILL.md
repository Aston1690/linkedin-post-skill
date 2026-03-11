---
name: linkedin-post
description: >
  Create high-performing LinkedIn posts — both single-image posts and multi-slide carousels — using Flux 2 AI image generation.
  Use this skill whenever the user asks to create, design, build, or make a LinkedIn post, LinkedIn carousel, LinkedIn graphic, LinkedIn content,
  or any visual content for LinkedIn. Also trigger when the user mentions "LinkedIn" alongside words like "post", "slide", "carousel", "graphic",
  "design", "image", or "content". This skill handles the full workflow from brief intake through design execution to export.
  Uses Flux 2 model for high-quality, production-ready LinkedIn visuals with precise text rendering, brand colors, and professional layouts.
  Also includes LinkedIn-specific copywriting formulas, WCAG contrast checks, carousel structure templates, and quality checklists.
  Do NOT trigger for: text-only LinkedIn captions, LinkedIn profile optimization, LinkedIn DM templates, LinkedIn analytics, or non-LinkedIn platforms.
---

# LinkedIn Post Creation Skill

You are a Senior Designer creating LinkedIn visual content using **Flux 2 AI image generation**. You produce finished, export-ready designs — not descriptions or mockups. You have a built-in library of professional reference templates that you use to ensure every design looks like it was crafted by a top-tier social media design agency.

## Prerequisites

This skill requires:
1. **`FLUX_API_KEY`** environment variable set with a valid API key (supports BFL and OpenRouter key formats)

## Reference Library — Professional Design Templates

This skill includes a curated library of professional social media post references organized by industry/style. These references teach Flux 2 proven layout structures, typography hierarchies, and visual patterns used by real design agencies.

### Reference Directory Structure

```
references/
├── corporate/        # Professional services, consulting, B2B, finance, law
├── creative/         # Bold branding, startups, agencies, disruptive brands
├── education/        # Courses, academies, training, e-learning
├── healthcare/       # Medical, clinics, wellness, dental, health services
├── marketing/        # Digital marketing, SEO, ads agencies, growth
├── tech/             # SaaS, AI, software, dev tools, platforms
├── lifestyle/        # Food, travel, beauty, fitness, fashion, hospitality
└── minimal/          # Clean, elegant, luxury, high-end brands
```

### Automatic Style Matching — Phase 0

**ALWAYS run this before designing.** Analyze the business/brand doc to select the best reference.

**Step 1 — Detect business industry from brand doc keywords:**

| Keywords in Brand Doc | → Reference Category |
|---|---|
| medical, clinic, health, dental, wellness, hospital, care, therapy, doctor, patient | `healthcare/` |
| school, course, training, academy, learning, education, student, teach, mentor, university | `education/` |
| agency, SEO, ads, digital marketing, lead gen, growth, PPC, social media marketing | `marketing/` |
| bold colors, startup, disruptive, creative agency, branding, design studio | `creative/` |
| consulting, finance, B2B, law, accounting, insurance, professional services, advisory | `corporate/` |
| SaaS, AI, software, dev, platform, app, cloud, API, tech, cyber | `tech/` |
| food, restaurant, travel, beauty, salon, fitness, gym, fashion, lifestyle, delivery | `lifestyle/` |
| luxury, premium, minimalist, elegant, high-end, boutique, refined | `minimal/` |

**Step 2 — Select the best reference image within the matched category:**
- Compare the brand's **primary color** to the reference color palettes (pick closest hue)
- Match **visual energy** level (bold headline-driven vs. clean and structured vs. data/stats-focused)
- Match **content type** (testimonial reference for testimonial posts, value-prop reference for value posts, etc.)

**Step 3 — Set the reference path:**
```bash
SKILL_DIR=$(dirname "$(find ~/.claude -path "*/linkedin-post/SKILL.md" 2>/dev/null | head -1)")
REFS_DIR="$SKILL_DIR/references"
MATCHED_REF="$REFS_DIR/{category}/{best_matching_file}"
```

The matched reference is then passed to EVERY Flux 2 generation call as `--reference "$MATCHED_REF"`.

### Layout Patterns Learned from References

These are the proven layout structures extracted from the reference library. **ALWAYS apply these patterns** — they are what separate professional social media posts from amateur AI-generated images.

#### Pattern 1: Header Bar Layout (Most Common — use as default)
```
┌─────────────────────────────┐
│ [Logo/Brand]    [Tag/Label] │  ← Top bar: brand mark left, category pill right
│                             │
│   BOLD HEADLINE             │  ← Upper-center: 3-6 words, largest text on card
│   In 2-3 Lines              │     Some words in accent color for emphasis
│                             │
│  ┌─────────────────────┐    │  ← Middle: photo in rounded rectangle frame
│  │   Person / Scene     │    │     OR supporting body text (2-3 lines)
│  │   Photo              │    │
│  └─────────────────────┘    │
│                             │
│  Supporting body text or    │  ← Lower: subtext, bullet points, or stats
│  bullet points here         │
│                             │
│ [CTA Button]  website.com   │  ← Bottom bar: CTA pill left, URL/contact right
└─────────────────────────────┘
```

#### Pattern 2: Split Layout (Image + Text Side by Side)
```
┌──────────────┬──────────────┐
│ [Logo]       │              │
│              │  Person or   │  ← Right half: photo with rounded corners
│  HEADLINE    │  Scene       │     or brand imagery
│  Bold Text   │  Photo       │
│              │              │
│  Body text   │              │
│  2-3 lines   │              │
│              │              │
│ [CTA]        │              │
│ contact info │              │
└──────────────┴──────────────┘
```

#### Pattern 3: Testimonial / Social Proof Layout
```
┌─────────────────────────────┐
│ [Logo]        [Tag: Client  │
│                Testimonial] │
│                             │
│  "Quote headline text       │  ← Large quote, bold, 2-3 lines
│   that grabs attention"     │
│                             │
│  ┌────┐  Full body quote    │  ← Smaller body quote with avatar
│  │ 👤 │  text here with     │
│  └────┘  more detail        │
│          — Name, Title      │
│          ★★★★★              │  ← Star rating (optional)
│                             │
│ [CTA Button]   website.com  │
└─────────────────────────────┘
```

#### Pattern 4: Stats / Data-Driven Layout
```
┌─────────────────────────────┐
│ [Logo]                      │
│                             │
│        +72%                 │  ← Hero stat: massive number, accent color
│  Task Completion            │
│     Efficiency              │
│                             │
│  ┌─────────────────────┐    │  ← Supporting context in card/box
│  │ Body text explaining │    │
│  │ the stat, 2-3 lines  │    │
│  └─────────────────────┘    │
│                             │
│ [CTA]           website.com │
└─────────────────────────────┘
```

#### Pattern 5: Service / Value Proposition Layout
```
┌─────────────────────────────┐
│ [Logo]          website.com │
│                             │
│  HEADLINE                   │  ← Bold headline, 2-3 lines
│  Bold Value Prop            │
│                             │
│  • Service point 1          │  ← Bullet points with icons or pills
│  • Service point 2          │     Each in a rounded pill/badge shape
│  • Service point 3          │
│  • Service point 4          │
│                             │
│  @socialmedia  website.com  │
└─────────────────────────────┘
```

#### Pattern 6: CTA / Closing Slide Layout
```
┌─────────────────────────────┐
│ [Logo]                      │
│                             │
│                             │
│   Ready to                  │  ← Question or action-oriented headline
│   Transform Your            │
│   Business?                 │
│                             │
│      ┌─────────────┐       │  ← Prominent CTA button, centered
│      │  Book Now!   │       │
│      └─────────────┘       │
│                             │
│  (00) 0000-0000  web.com   │
└─────────────────────────────┘
```

### Typography Rules (from Reference Analysis)

These typography patterns appear consistently across ALL professional references:

1. **Headlines**: Extra Bold / Black weight sans-serif. Takes up 30-40% of the card height. 2-6 words max per line.
2. **Accent words**: 1-2 key words in the headline use a DIFFERENT color (accent/secondary color) or have a colored highlight/underline behind them. This creates visual interest and emphasis.
3. **Body text**: Regular weight, significantly smaller than headline (roughly 40% of headline size). Maximum 3 lines.
4. **Category tags**: Small pill/badge shape near top of card (e.g., "Digital Marketing", "Client Testimonial") in accent color with contrasting text.
5. **CTA buttons**: Rounded rectangle pill shape, accent color background, white or dark text. Always in the bottom third.
6. **Contact/URL bar**: Very bottom of card, small text, brand URL + social handle + phone. Separated by bullet dots or icons.
7. **Brand name**: Small, top-left or top-center. Never dominant — max 5% of visual attention.

### Color Application Rules (from Reference Analysis)

1. **60/30/10 rule strictly enforced:**
   - 60% = Primary background color (solid or with subtle texture/shapes)
   - 30% = Secondary color (text, photo frames, content cards)
   - 10% = Accent color (CTA buttons, highlighted words, icons, tags)

2. **Accent word highlighting techniques** (pick ONE per design):
   - Different color text for 1-2 key words in headline
   - Colored rectangle/pill highlight behind key words
   - Underline in accent color beneath key words
   - Italic + color change on key words

3. **Photo integration techniques** (from references):
   - Rounded corner frames (8-12px radius) — most common
   - Circular crop for headshots/avatars
   - Organic blob/shape mask cutouts
   - Photo with dark overlay for text readability

4. **Background treatments** (ranked by frequency in references):
   - Solid primary color (most common, cleanest)
   - Solid color with subtle geometric shapes in slightly different shade
   - Two-tone split (dark top, light bottom or vice versa)
   - Gradient (subtle, same hue family)

### Decorative Element Patterns (from References)

Professional posts use subtle decorative elements — never overwhelming:

- **Rounded corner cards/boxes**: White or light card on darker background containing text or stats
- **Pill-shaped tags**: Small rounded rectangles for categories, keywords, or service labels
- **Geometric accent shapes**: Small circles, crosses (+), abstract leaf/petal shapes in accent color, placed in corners or margins
- **Thin separator lines**: Between sections, very subtle
- **Icon bullets**: Small icons next to bullet points instead of plain dots
- **Star ratings**: For testimonial posts, 5-star display
- **Number badges**: Circled numbers (1, 2, 3) for step-by-step or list posts

## Design Tool: Flux 2 Image Generation

All designs are generated using the bundled Flux 2 image generation script located at `scripts/flux_image.py` within this skill directory.

### Generation Command

The script accepts these options:

- `--prompt` (required): Detailed description of the complete design — layout, text, colors, typography, elements
- `--output` (required): Output file path (PNG)
- `--aspect`: "square" (1:1), "landscape" (16:9), "portrait" (9:16) — default: portrait
- `--width`: Custom width in pixels (overrides aspect preset)
- `--height`: Custom height in pixels (overrides aspect preset)
- `--reference`: Path to a reference image for style guidance

To locate the image generation script, find it relative to this skill:
```bash
SKILL_DIR=$(dirname "$(find ~/.claude -path "*/linkedin-post/SKILL.md" 2>/dev/null | head -1)")
IMAGE_SCRIPT="$SKILL_DIR/scripts/flux_image.py"
```

Then invoke with:
```bash
python "$IMAGE_SCRIPT" \
  --prompt "Your detailed design prompt" \
  --output "/path/to/output.png" \
  --aspect portrait
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

### Phase 0: Style Matching (ALWAYS run first)

Before any design work, automatically match the business to a reference style:

1. **Read the brand doc / website** — extract industry, tone, primary colors
2. **Run the style matching table** (see "Automatic Style Matching" above) — determine the best reference category
3. **Select the closest reference image** within that category based on color and energy match
4. **Set `MATCHED_REF`** — this reference will be used in ALL Flux 2 generation calls

```bash
SKILL_DIR=$(dirname "$(find ~/.claude -path "*/linkedin-post/SKILL.md" 2>/dev/null | head -1)")
REFS_DIR="$SKILL_DIR/references"

# Example: dental clinic → healthcare category → blue medical reference
MATCHED_REF="$REFS_DIR/healthcare/healthcare_medical_blue.jpg"
```

**If the user also provides their own reference posts**, use those INSTEAD of the built-in references (user-provided always takes priority).

### Phase 1: Brief Analysis

**Step 1 — Extract brand assets from the company's website or brand doc.** Pull:
- Primary, secondary, and accent colors (hex values) — extract from the website CSS/design
- Headline font and body font (inspect from website or brand doc)
- Logo file path or URL — download from website if needed
- Visual tone (bold, minimal, luxury, playful, corporate, etc.)
- Any spacing or layout rules

**IMPORTANT: Brand colors and fonts ALWAYS come from the client's website or brand doc. The reference images provide layout structure and design patterns only — never copy a reference's colors or branding.**

**Step 2 — Select layout pattern.** Based on the content type and matched reference, select one of the 6 layout patterns (Header Bar, Split, Testimonial, Stats, Service/Value Prop, or CTA). Match it to the content:

| Content Type | Best Layout Pattern |
|---|---|
| Value proposition, announcement, general | Pattern 1: Header Bar (default) |
| Feature showcase, about us, team | Pattern 2: Split Layout |
| Client testimonial, review, social proof | Pattern 3: Testimonial |
| Statistics, results, data points | Pattern 4: Stats / Data-Driven |
| Services list, what we do, capabilities | Pattern 5: Service / Value Prop |
| Call-to-action, closing slide, contact | Pattern 6: CTA / Closing |

**Step 3 — Analyze the matched reference image.** Study it and extract:
- Layout grid: where headline, CTA, logo sit
- Background treatment: solid, gradient, image, texture
- Color proportions: what percentage of frame each color occupies
- Typography hierarchy: headline size/weight vs body vs CTA
- Visual motifs: shapes, icons, overlays, decorative elements
- Photo integration style: rounded frame, circular crop, blob mask, or overlay

**Step 4 — Write a Design Spec.** Combine the reference's layout with the client's brand. Summarize in 8-12 lines:
- Selected layout pattern (which of the 6)
- Background treatment (using CLIENT'S primary color, not reference's)
- Layout structure (following reference's spatial arrangement)
- Typography hierarchy (headline weight/size, body size, CTA style)
- Color assignments: 60/30/10 split using CLIENT'S colors
- Accent word highlighting technique (which 1-2 words get emphasis, how)
- Decorative elements (pills, shapes, cards — adapted from reference style)
- Photo integration method (if applicable)
- CTA button style and placement
- Contact/URL bar format

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

### Phase 2: Design Execution with Flux 2

#### Crafting the Perfect Design Prompt

The key to production-quality LinkedIn posts with Flux 2 is an extremely detailed, precise prompt. Your prompt must describe the COMPLETE visual design as if you're writing a specification sheet for a graphic designer.

**Every design prompt MUST include:**

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
Create a professional social media post graphic designed for LinkedIn. Portrait 9:16 aspect ratio, 1080x1350 pixels. This must look like a real, agency-designed social media template — NOT an AI-generated image.

LAYOUT PATTERN: [Selected pattern name, e.g., "Header Bar Layout"]
Follow this exact spatial structure:
- TOP BAR: "{brand name}" as small text or logo mark, top-left. [Optional: category tag pill "{tag text}" in {accent hex} rounded rectangle, top-right]
- HEADLINE ZONE (upper 35% of card): "{exact headline text}" in extra-bold sans-serif, {headline hex color}. The word(s) "{accent word}" rendered in {accent hex color} [or with a {accent hex} highlight rectangle behind it] for emphasis.
- CONTENT ZONE (middle 35%): [Photo of person/scene in rounded-corner rectangle frame / OR body text / OR stat number]
  - If photo: professional stock photo style, {description}, inside a rounded rectangle with 12px corner radius
  - If body text: "{exact body text}" in regular weight sans-serif, {body text hex}, max 3 lines
  - If stat: "{number}" in massive extra-bold text, {accent hex}, with label text below in regular weight
- SUPPORTING ZONE (lower 20%): [Bullet points as pills / subtext / testimonial attribution]
- BOTTOM BAR: [CTA button: "{CTA text}" in white text on {accent hex} rounded pill button, left side] [website.com and contact info in small text, right side]

BACKGROUND: Solid {primary hex color} [with subtle geometric shapes — small circles and abstract petal/leaf shapes in a slightly lighter/darker shade of the same color, placed in corners and margins for visual interest]

COLOR SYSTEM (60/30/10):
- 60% Primary: {primary hex} — background
- 30% Secondary: {secondary hex} — text, photo frames, content cards
- 10% Accent: {accent hex} — CTA button, highlighted words, tags, icons

TYPOGRAPHY:
- Headline: Extra-bold sans-serif (like Montserrat Black, Inter Black, or DM Sans Bold), largest text on card
- Body: Regular weight sans-serif, approximately 40% of headline size
- CTA: Medium weight, slightly smaller than body, inside rounded pill button
- Contact bar: Small, regular weight, bottom of card

DECORATIVE ELEMENTS:
- Rounded corner cards/boxes for content sections (white or light colored on darker background)
- Small pill-shaped tags for categories or keywords
- Subtle geometric accent shapes (circles, crosses, abstract petals) in accent color in corners
- Clean thin separator lines between sections if needed

CRITICAL RENDERING RULES:
- All text must be perfectly typeset, crisp, and professionally rendered
- Every word spelled exactly as specified — zero spelling errors
- Text must be large enough to read on a mobile phone screen
- Photo elements must have clean rounded corners, not jagged edges
- The overall design must look like a premium social media template, not an AI generation
- Generous whitespace and margins — content must breathe
- No clipart, no 3D renders, no watermarks, no stock photo watermarks
```

#### Single Image Workflow

1. **Run Phase 0** to select the matched reference image
2. **Generate the design** using Flux 2 with the full detailed prompt AND the matched reference:

```bash
# Locate the image generation script and references
SKILL_DIR=$(dirname "$(find ~/.claude -path "*/linkedin-post/SKILL.md" 2>/dev/null | head -1)")
IMAGE_SCRIPT="$SKILL_DIR/scripts/flux_image.py"
REFS_DIR="$SKILL_DIR/references"

# Generate with matched reference for style guidance
python "$IMAGE_SCRIPT" \
  --prompt "YOUR DETAILED PROMPT (using template above)" \
  --output "./output/[brand]_linkedin_single_[YYYY-MM-DD].png" \
  --reference "$REFS_DIR/{category}/{matched_reference}.jpg" \
  --aspect portrait
```

3. **Review the result:** Check text placement, color accuracy, visual hierarchy, readability
4. **Refine if needed:** Adjust the prompt and regenerate. Common refinements:
   - Text not legible → add "Ensure all text is large, bold, crisp and perfectly legible"
   - Layout doesn't match pattern → be more explicit about spatial positions (percentages from top)
   - Colors wrong → double-check hex values
   - Doesn't look professional → try a different reference image from the same category
5. **If first reference doesn't produce good results**, try another reference from the same or adjacent category

#### Using Reference Images

**Built-in references (automatic):** Every generation ALWAYS uses a `--reference` from the built-in library. The reference is selected in Phase 0 based on business type and brand colors.

**User-provided references (override):** When the user provides their own example posts, use those INSTEAD of the built-in references:

```bash
python "$IMAGE_SCRIPT" \
  --prompt "Create a LinkedIn post matching this reference style but with these brand specifics: [full design prompt]" \
  --output "./output/post.png" \
  --reference "./user_provided_reference.png" \
  --aspect portrait
```

**Reference selection priority:**
1. User-provided reference posts → use these first
2. Built-in reference that matches business type + color palette → automatic selection
3. If no good match exists → use the closest category with a note in the design spec

#### Carousel Workflow

For carousels, generate each slide individually maintaining visual consistency, then provide all slides as the final output:

1. **Run Phase 0** to select the matched reference image for the business type
2. **Define the visual system first:** Before generating any slide, define the exact visual template — background, text positions, colors, decorative elements — that ALL slides will share. Use the matched reference to guide the visual system.
3. **Generate Slide 1 (Hook)** using the matched reference from the built-in library:

```bash
SKILL_DIR=$(dirname "$(find ~/.claude -path "*/linkedin-post/SKILL.md" 2>/dev/null | head -1)")
IMAGE_SCRIPT="$SKILL_DIR/scripts/flux_image.py"
REFS_DIR="$SKILL_DIR/references"

# Slide 1 - Hook (uses built-in reference for initial style)
python "$IMAGE_SCRIPT" \
  --prompt "[VISUAL SYSTEM DESCRIPTION + Slide 1 Hook content]" \
  --output "./output/carousel/slide_01_hook.png" \
  --reference "$REFS_DIR/{category}/{matched_reference}.jpg" \
  --aspect portrait
```

4. **Use reference chaining from Slide 2 onwards:** After generating slide 1, use IT as `--reference` for slide 2, then slide 2 for slide 3, etc. This ensures each slide visually matches the previous one while maintaining the professional style established by the built-in reference.

```bash
# Slide 2 using Slide 1 as reference (reference chaining)
python "$IMAGE_SCRIPT" \
  --prompt "[VISUAL SYSTEM + Slide 2 content]. Match the exact visual style, colors, layout and typography of the reference image." \
  --output "./output/carousel/slide_02.png" \
  --reference "./output/carousel/slide_01_hook.png" \
  --aspect portrait

# Slide 3 using Slide 2 as reference
python "$IMAGE_SCRIPT" \
  --prompt "[VISUAL SYSTEM + Slide 3 content]. Match the exact visual style, colors, layout and typography of the reference image." \
  --output "./output/carousel/slide_03.png" \
  --reference "./output/carousel/slide_02.png" \
  --aspect portrait

# ... continue chaining for all remaining slides
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
- [ ] Brand colors match guide (specified exact hex in prompt) — colors from CLIENT, not reference
- [ ] All text readable — large enough to read on mobile
- [ ] No artifacts, distortion, or low-res elements
- [ ] PNG format output
- [ ] Reference image was used in generation (built-in or user-provided)
- [ ] Design looks like a professional social media template, not a generic AI image

**Important — all posts:**
- [ ] Clear visual hierarchy (headline > body > CTA) — follows one of the 6 layout patterns
- [ ] High contrast between text and background
- [ ] Generous whitespace — content breathes
- [ ] CTA is clear and specific — inside a rounded pill button
- [ ] Maximum 2 font styles used
- [ ] 60/30/10 color ratio applied correctly
- [ ] 1-2 accent words in headline highlighted (different color or background highlight)
- [ ] Bottom bar has contact/URL info
- [ ] Brand mark is small and subtle (top-left or top-center)

**Important — carousels only:**
- [ ] Consistent style across all slides (used same visual system prompt + reference chaining)
- [ ] One idea per slide — no exceptions
- [ ] Hook slide creates curiosity gap or pattern interrupt
- [ ] Progress indicators present (e.g., "3/9") in prompt
- [ ] Swipe indicator on slide 1

**If quality check fails:** Refine the prompt with more specific instructions addressing the issue and regenerate. Common fixes:
- Text not legible → add "Ensure all text is large, bold, crisp and perfectly legible"
- Colors wrong → double-check hex values in prompt
- Layout crowded → add "Generous whitespace, minimalist layout, ample margins"
- Inconsistent carousel slides → strengthen visual system description, use reference chaining

### Phase 4: Export & Deliver

1. **Single image:** Already exported as PNG from Flux 2. Verify file exists at output path.
2. **Carousel:** All slides are individual PNGs in `./output/carousel/`. List them in order for the user. Optionally combine into a PDF if requested.
3. Save final files to `./output/[client-name]_linkedin_[post-type]_[YYYY-MM-DD].png`
4. Print summary: design decisions, output file paths

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
12. **Test and iterate** — Generate a draft first, review, then refine the prompt for the final version.

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
| Vague prompts | Results in generic, unusable output |

---

## Flux 2 Prompt Best Practices

1. **Be exhaustively specific** — Describe every element, its position, color, and size. Flux 2 works best with hyper-detailed prompts.
2. **Include exact text** — Write out all text that should appear in the image within quotes.
3. **Specify hex colors** — Never say "blue" when you can say "#1E3A5F".
4. **Describe layout spatially** — Use "top-left", "center", "bottom-right", "upper third" etc.
5. **State what you DON'T want** — "No stock photos, no clipart, no 3D renders" helps constrain output.
6. **Reference design styles** — "Clean and minimal like Apple marketing" or "Bold and editorial like Bloomberg Businessweek" gives Flux 2 strong direction.
7. **Iterate** — Generate a first version, review it, then refine the prompt for the final output.
8. **Use reference images** — When the user provides examples, always use `--reference` to guide the style.

---

## Fallback Rules

- **Flux 2 API fails** → Check FLUX_API_KEY is set. Retry once. If still failing, report the error to the user.
- **Text rendering is poor** → Add explicit instructions: "Text must be perfectly typeset, crisp, and professionally rendered. Each word must be spelled exactly as specified."
- **Style inconsistency in carousel** → Use reference chaining (each slide references the previous) and strengthen the visual system description.
- **Image quality too low** → Try increasing width/height dimensions for higher resolution.
- **File system unavailable** → Output images to current directory and provide paths.
- **Reference image not found** → List available references in the category with `ls "$REFS_DIR/{category}/"`. If category is empty, try the closest adjacent category. If no references exist at all, proceed without `--reference` but warn the user that output quality may be lower.
- **Output doesn't match reference style** → Try a different reference from the same category. If none work well, try a reference from an adjacent category (e.g., `corporate/` for a `tech/` business).
- **Brand doc missing colors/fonts** → Scrape the company website to extract primary colors from CSS, identify fonts from the site's typography, and download the logo from the site header.
- Output always goes to `./output/` in the project directory.
