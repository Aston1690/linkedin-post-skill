---
name: linkedin-post
description: "Create LinkedIn posts and carousels with Flux 2 AI image generation. Trigger on: LinkedIn post, carousel, graphic, content, slide, or visual design requests. Not for: text-only captions, profile optimization, DM templates, analytics, or non-LinkedIn platforms."
---

# LinkedIn Post Creation Skill

You are a Senior Designer creating LinkedIn visual content using **Flux 2 AI image generation**. You produce finished, export-ready designs — not descriptions or mockups. You have a built-in library of professional reference templates that you use to ensure every design looks like it was crafted by a top-tier social media design agency.

## Prerequisites

This skill requires:
1. **`SEADREAM_API_KEY`** environment variable set with a valid OpenRouter API key (used for Nano Banana 2 and Seedream 4.5 — both run on OpenRouter)
2. **`FLUX_API_KEY`** environment variable set with a valid API key (supports BFL and OpenRouter key formats, for Flux 2 Pro)

## Setup

Locate the skill directory and scripts once at the start of any workflow:

```bash
SKILL_DIR=$(dirname "$(find ~/.claude -path "*/linkedin-post/SKILL.md" 2>/dev/null | head -1)")
NANOBANANA_SCRIPT="$SKILL_DIR/scripts/nanobanana_image.py"  # default model (best quality)
SEEDREAM_SCRIPT="$SKILL_DIR/scripts/seedream_image.py"      # fallback model
FLUX_SCRIPT="$SKILL_DIR/scripts/flux_image.py"              # use when --reference is needed
REFS_DIR="$SKILL_DIR/references"
```

These variables are used throughout the phases below.

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

## Design System Rules (from Reference Analysis)

### Typography

These typography patterns appear consistently across ALL professional references:

1. **Headlines**: Extra Bold / Black weight sans-serif. **Single images:** Takes up 30-40% of the card height. **Carousel slides:** Takes up 20-25% of the card height — carousel text must be smaller and more proportional to leave breathing room, since each slide has less content. 2-6 words max per line.
2. **Accent words**: 1-2 key words in the headline use a DIFFERENT color (accent/secondary color) or have a colored highlight/underline behind them. This creates visual interest and emphasis.
3. **Body text**: Regular weight, significantly smaller than headline (roughly 40% of headline size). Maximum 3 lines.
4. **Category tags**: Small pill/badge shape near top of card (e.g., "Digital Marketing", "Client Testimonial") in accent color with contrasting text.
5. **CTA buttons**: Rounded rectangle pill shape, accent color background, white or dark text. Always in the bottom third.
6. **Contact/URL bar**: Very bottom of card, small text, brand URL + social handle + phone. Separated by bullet dots or icons.
7. **Brand name**: Small, top-left or top-center. Never dominant — max 5% of visual attention.

### Color

1. **60/30/10 rule strictly enforced:**
   - 60% = Primary background color (solid or with subtle texture/shapes)
   - 30% = Secondary color (text, photo frames, content cards)
   - 10% = Accent color (CTA buttons, highlighted words, icons, tags)

2. **Accent word highlighting techniques** (pick ONE per design):
   - Different color text for 1-2 key words in headline
   - Colored rectangle/pill highlight behind key words
   - Underline in accent color beneath key words
   - Italic + color change on key words

3. **Photo integration techniques:**
   - Rounded corner frames (8-12px radius) — most common
   - Circular crop for headshots/avatars
   - Organic blob/shape mask cutouts
   - Photo with dark overlay for text readability

4. **Background treatments** (ranked by preference — LIGHT backgrounds FIRST):
   - **Light off-white / very pale cool grey solid background** (STRONGLY preferred — cleanest, most premium, bright and airy. This is the default for ALL posts.)
   - Light background with decorative accent elements (teal/accent circle blobs, cross markers, corner geometric patterns)
   - Two-tone split (light/dark halves or diagonal)
   - Solid dark color — USE SPARINGLY, only when the content specifically demands it
   - Gradient — USE SPARINGLY. Only subtle, same-hue-family gradients. **NEVER use gradient orbs, glowing spheres, lens flares, or bokeh light effects** — these look amateur and AI-generated.

   **IMPORTANT: Dark backgrounds should NOT be the default. Light backgrounds produce more engaging, premium-looking posts that stand out in the LinkedIn feed. Dark backgrounds look generic and AI-generated.**

### Decorative Elements

Professional posts use subtle decorative elements — never overwhelming:

- **Large accent circle blob**: A large semi-transparent circle in the brand's accent/teal color, placed in the upper-right area, partially cropped by the edge. Creates visual interest and brand color pop. This is the signature element of the premium light style.
- **Small cross (+) markers**: Tiny cross/plus shapes scattered in corners and margins in the accent color at 30-50% opacity. Adds texture without clutter.
- **Corner geometric line patterns**: Thin diagonal line grids or angular geometric patterns in accent color at low opacity (10-20%) in bottom-left and/or top-right corners.
- **Floating tilted cards**: White rounded-corner cards with subtle shadow, slightly rotated/tilted, containing icons and text. Creates depth and visual interest.
- **Colored underline/separator**: A short thick line in the accent color below the headline, centered. Acts as a visual anchor between headline and body.
- **Rounded corner cards/boxes**: White or light card containing text, stats, or icons
- **Pill-shaped tags**: Small rounded rectangles for categories, keywords, or service labels
- **Thin separator lines**: Between sections, very subtle
- **Icon bullets**: Small icons next to bullet points instead of plain dots
- **Star ratings**: For testimonial posts, 5-star display
- **Number badges**: Circled numbers (1, 2, 3) for step-by-step or list posts

### Reference Style: Premium Light (DEFAULT for ALL posts)

The default design style for ALL posts — regardless of business or industry — should follow the "Premium Light" aesthetic:

- **Light, bright, airy backgrounds** (off-white, very pale cool grey) — NEVER dark by default
- **Bold oversized headlines** in dark navy / the brand's darkest color
- **1-2 accent words** in the headline in purple or the brand's accent color
- **Large decorative accent circle** shape in upper area, semi-transparent, partially cropped by edge
- **Small cross markers** and geometric line patterns as background texture
- **White floating cards** with rounded corners and subtle shadows for service/feature callouts, slightly tilted for depth
- **Short thick accent-colored line** below headline as separator
- **A relevant photograph or image** MUST be included in every post — a business person, office scene, technology imagery, or contextually relevant photo. Posts should never be purely text + icons. The image should be integrated naturally (inside a floating card, as a background element, in a rounded frame, etc.)
- **Dark navy/dark CTA button** (not accent-colored) with white text, rectangular with rounded corners
- **Bottom contact bar** with URL and location in small grey text
- **NO AI-generated logos** — NEVER ask the AI to render the brand name or logo. Leave the top-left corner 100% blank/empty in the prompt. The real logo is composited via Pillow in Phase 2.5. If the AI renders a logo despite instructions, REGENERATE — do not paste over it.
- **Overall feel**: premium, bright, agency-quality — NOT dark/moody/tech-noir

## Design Tools: Image Generation

This skill supports **three image generation models**. **Nano Banana 2 is the default** — it produces the best output quality. Use Seedream 4.5 as a fallback, and Flux 2 Pro only when reference-guided generation is specifically needed.

| Model | Script | Best For | API Key |
|-------|--------|----------|---------|
| **Nano Banana 2** (default) | `scripts/nanobanana_image.py` | Best quality generation, primary model for all posts — superior text rendering, photorealism, and design fidelity | `SEADREAM_API_KEY` (OpenRouter) |
| **Seedream 4.5** (fallback) | `scripts/seedream_image.py` | Fallback if Nano Banana 2 fails or for comparison | `SEADREAM_API_KEY` (OpenRouter) |
| **Flux 2 Pro** | `scripts/flux_image.py` | Reference-guided generation when style matching from a reference image is required | `FLUX_API_KEY` |

### Flux 2 Generation Command

Use Flux 2 only when reference-guided generation is needed. The script accepts these options:

- `--prompt` (required): Detailed description of the complete design
- `--output` (required): Output file path (PNG)
- `--aspect`: "square" (1:1), "landscape" (16:9), "portrait" (9:16) — default: portrait
- `--width` / `--height`: Custom dimensions (overrides aspect preset)
- `--reference`: Path to a reference image for style guidance

```bash
python "$FLUX_SCRIPT" \
  --prompt "Your detailed design prompt" \
  --output "/path/to/output.png" \
  --aspect portrait
```

### Nano Banana 2 Generation Command (Default)

Uses Google's Nano Banana 2 (Gemini 3.1 Flash Image) via OpenRouter. Same CLI interface as the other scripts (drop-in compatible). Produces the best output quality — superior text rendering, photorealism, and design fidelity.

- `--prompt` (required): Detailed description of the complete design
- `--output` (required): Output file path (PNG)
- `--aspect`: "square" (1:1), "landscape" (16:9), "portrait" (9:16) — default: portrait
- `--width` / `--height`: Custom dimensions (overrides aspect preset)
- `--reference`: Accepted but ignored (Nano Banana 2 does not support reference images via OpenRouter)

```bash
python "$NANOBANANA_SCRIPT" \
  --prompt "Your detailed design prompt" \
  --output "/path/to/output.png" \
  --aspect portrait
```

### Seedream 4.5 Generation Command (Fallback)

Uses the `requests` library and ByteDance's Seedream 4.5 via OpenRouter. Same CLI interface as Nano Banana 2 (drop-in replacement). Use as fallback if Nano Banana 2 fails.

- `--prompt` (required): Detailed description of the complete design
- `--output` (required): Output file path (PNG)
- `--aspect`: "square" (1:1), "landscape" (16:9), "portrait" (9:16) — default: portrait
- `--width` / `--height`: Custom dimensions (overrides aspect preset)
- `--reference`: Accepted but ignored (Seedream does not support reference images)

```bash
python "$NANOBANANA_SCRIPT" \
  --prompt "Your detailed design prompt" \
  --output "/path/to/output.png" \
  --aspect portrait
```

### Model Comparison Workflow

When comparing models, generate the same prompt with multiple models and save outputs side by side:

```bash
# Generate with Nano Banana 2 (default — best quality)
python "$NANOBANANA_SCRIPT" \
  --prompt "YOUR PROMPT" \
  --output "./output/comparison/nanobanana2_slide.png" \
  --aspect portrait

# Generate with Seedream 4.5 (fallback)
python "$NANOBANANA_SCRIPT" \
  --prompt "YOUR PROMPT" \
  --output "./output/comparison/seedream_slide.png" \
  --aspect portrait

# Generate with Flux 2
python "$FLUX_SCRIPT" \
  --prompt "YOUR PROMPT" \
  --output "./output/comparison/flux2_slide.png" \
  --aspect portrait
```

Existing Flux 2 Pro outputs for comparison are available in `output/client-deliverables-review/LinkedIn-Carousels/` organized by client (OnePassport, Clarity, ICS).

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
3. **Check for available references:**

```bash
CATEGORY="{matched_category}"  # e.g., healthcare, tech, corporate

# Check if references exist in the matched category
REF_FILES=$(ls "$REFS_DIR/$CATEGORY/"*.{jpg,png,jpeg} 2>/dev/null | head -5)
```

4. **Set the reference based on what's available:**

| Scenario | Action |
|----------|--------|
| **User provided reference posts** | Use those — user references always take priority |
| **Built-in references exist** in matched category | Select closest match by color and energy level, set as `MATCHED_REF` |
| **Category is empty but adjacent category has refs** | Use closest adjacent category (e.g., `corporate/` for a `tech/` business) |
| **No references exist at all** | Proceed without `--reference` flag. Compensate with a more detailed prompt describing the exact layout pattern, spacing, and proportions. Inform the user: "No reference templates are installed — output quality may vary. Add reference images to `references/{category}/` for better results." |

```bash
# If reference found:
MATCHED_REF="$REFS_DIR/{category}/{best_matching_file}"

# If no reference found — omit --reference flag entirely
# and add this to the prompt: "Follow the [Pattern Name] layout exactly as described"
```

### Phase 0.5: Brand Asset Extraction (MANDATORY — run before ANY design work)

**This phase is NON-NEGOTIABLE. Every design MUST start here.** Do not skip to design execution without completing this phase. Generating without proper brand assets produces off-brand, amateur results.

**Step 1 — Extract brand fonts from the website.** This is the most commonly missed step:
```bash
# Fetch the Elementor kit CSS (most common for WordPress sites)
curl -sL "$WEBSITE_URL" | grep -ioE 'elementor-kit-\d+' | head -1
# Then fetch: /wp-content/uploads/elementor/css/post-{KIT_ID}.css
# Extract: --e-global-typography-*-font-family values
```
- Look for `font-family` declarations in Elementor kit CSS, theme CSS, Google Fonts imports, or `@font-face` rules
- Common locations: Elementor kit CSS (`post-{kit_id}.css`), inline `<style>` blocks, linked stylesheets
- Record: headline font, body font, button font — with weights
- In prompts, NEVER use the font name directly (AI renders it as text). Instead describe the font style: e.g., "Prompt" → "clean rounded geometric sans-serif with friendly proportions"

**Step 2 — Extract brand colors:**
- Fetch Elementor kit CSS and extract `--e-global-color-*` variables
- Record: primary, secondary, accent, text, background colors with hex values
- In prompts, NEVER use hex codes (AI renders them as text). Instead describe colors by name: e.g., `#0C3B5D` → "deep dark navy blue"

**Step 3 — Download the real logo:**
```bash
# Find logo URL from website
curl -sL "$WEBSITE_URL" | grep -ioE 'src="[^"]*logo[^"]*"' | head -3
# Download it
curl -sL "$LOGO_URL" -o "./output/client_logo.png"
```
- Download the actual logo file (PNG with transparency preferred)
- Check if a white/light version exists for dark backgrounds
- Store the logo path for compositing in Phase 4

**Step 4 — Screenshot the website for visual reference:**
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu \
  --screenshot="./output/website_screenshot.png" \
  --window-size=1440,900 "$WEBSITE_URL" 2>/dev/null
```

**Step 5 — Record visual tone:** bold, minimal, luxury, playful, corporate, etc.

**IMPORTANT: Brand colors and fonts ALWAYS come from the client's website or brand doc. The reference images provide layout structure and design patterns only — never copy a reference's colors or branding.**

### Phase 1: Brief Analysis

**Step 1 — Use the brand assets extracted in Phase 0.5.** You should already have:
- Primary, secondary, and accent colors (hex values)
- Headline font and body font (with style descriptions for prompts)
- Logo file downloaded locally
- Visual tone and website screenshot for reference

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
- Matched reference: category and filename (or "no reference — using detailed prompt only")

**Show the Design Spec to the user (including the matched reference choice). This is the only required pause.** Wait for approval before continuing.

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

BACKGROUND: Solid very light grey or off-white background (very pale cool grey — bright and airy). Add decorative elements: a large semi-transparent {accent color name} circle shape in the upper-right area partially cropped by edge, small {accent color name} cross/plus markers scattered at 30% opacity, thin geometric angular line patterns in {accent color name} at 15% opacity in bottom-left corner. Premium, bright, agency-quality feel.

COLOR SYSTEM (60/30/10) — PREMIUM LIGHT STYLE:
- 60% = Light off-white / very pale cool grey — background (NEVER dark by default)
- 30% = Dark navy / brand's darkest color — headline text, CTA button, body text
- 10% = Brand accent colors (teal, purple, etc.) — decorative circle blob, highlighted headline words, pill tags, cross markers, separator line

TYPOGRAPHY:
- Headline: Extra-bold sans-serif in the CLIENT'S brand font (extracted in Phase 1), largest text on card
- Body: Regular weight sans-serif, approximately 40% of headline size
- CTA: Medium weight, slightly smaller than body, inside rounded pill button
- Contact bar: Small, regular weight, bottom of card

DECORATIVE ELEMENTS (Premium Light Style):
- Large semi-transparent accent circle blob in upper-right, partially cropped by edge
- Small cross (+) markers scattered in corners at low opacity in accent color
- Thin geometric angular line patterns in accent color at low opacity in corners
- White floating cards with rounded corners and subtle shadows, slightly tilted, for feature/service callouts
- Short thick accent-colored horizontal line below headline as visual separator
- Pill-shaped tags for categories (white text on accent-colored rounded rectangle, top-right)
- CTA: dark navy/dark rectangular button with rounded corners and white text (NOT accent-colored pill)

CRITICAL RENDERING RULES:
- All text must be perfectly typeset, crisp, and professionally rendered
- Every word spelled exactly as specified — zero spelling errors
- Text must be large enough to read on a mobile phone screen
- Photo elements must have clean rounded corners, not jagged edges
- The overall design must look like a premium social media template, not an AI generation
- Generous whitespace and margins — content must breathe
- No clipart, no 3D renders, no watermarks, no stock photo watermarks

NANO BANANA 2 / SEEDREAM PROMPTING RULES (when using Nano Banana 2 or Seedream 4.5):
- NEVER include hex color codes (e.g., #00B9F2) in prompts — the model renders them as visible text. Instead, describe colors by name: "bright cyan-blue", "dark charcoal", "medium teal-green", "very dark navy blue", etc.
- NEVER include technical specifications like "1080x1350" or "9:16" in the prompt body — the model may render these as literal text. Use the --aspect and --width/--height CLI flags instead.
- NEVER include font names like "Montserrat" or "Prompt" in prompts — describe the style instead: "clean bold sans-serif", "modern rounded geometric sans-serif with friendly proportions"
- For carousel slides: explicitly state "medium-sized headline text, NOT oversized" — these models default to filling available space with text if not constrained
- ALWAYS tell the AI to leave the logo area COMPLETELY EMPTY: "Leave the top-left corner completely blank — no text, no shapes, no brand name, nothing. Pure clean background."
- NEVER ask the AI to render the brand name or logo text — it will always get it wrong. The real logo is composited in Phase 2.5.

DESIGN STYLE RULES (apply to ALL prompts):
- **ALWAYS use a LIGHT background** (off-white, very pale cool grey). NEVER default to dark backgrounds — they look generic and AI-generated.
- **Premium Light aesthetic**: bright, airy, agency-quality. Think premium SaaS marketing (Apple, Stripe, Linear.app).
- **NEVER use gradient orbs, glowing spheres, bokeh effects, lens flares, or atmospheric light blobs.** These look amateur.
- **Floating white cards with subtle shadows** are encouraged for feature/service callouts — slight tilt adds depth.
- **Large accent circle blob** (semi-transparent, partially cropped by edge) is a signature decorative element — include it.
- **Small cross (+) markers and geometric line patterns** add texture without clutter.
- **Dark CTA button** (dark navy/brand's darkest color) with white text — NOT accent-colored pills.
- **Restraint over excess** — every decorative element must earn its place. When in doubt, remove it.
```

#### Single Image Workflow

1. **Run Phase 0** to select the matched reference image
2. **Generate the design** using Flux 2 with the full detailed prompt AND the matched reference:

```bash
# Generate with matched reference for style guidance
python "$NANOBANANA_SCRIPT" \
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

**Built-in references (for Flux 2 only):** When using Flux 2 Pro (`$FLUX_SCRIPT`), every generation uses a `--reference` from the built-in library, selected in Phase 0 based on business type and brand colors. Nano Banana 2 (default) and Seedream 4.5 do not use reference images — instead, describe the desired style directly in the prompt.

**User-provided references (override):** When the user provides their own example posts, use those INSTEAD of the built-in references:

```bash
python "$NANOBANANA_SCRIPT" \
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
# Slide 1 - Hook (uses built-in reference for initial style)
python "$NANOBANANA_SCRIPT" \
  --prompt "[VISUAL SYSTEM DESCRIPTION + Slide 1 Hook content]" \
  --output "./output/carousel/slide_01_hook.png" \
  --reference "$REFS_DIR/{category}/{matched_reference}.jpg" \
  --aspect portrait
```

4. **Use reference chaining from Slide 2 onwards:** After generating slide 1, use IT as `--reference` for slide 2, then slide 2 for slide 3, etc. This ensures each slide visually matches the previous one while maintaining the professional style established by the built-in reference.

```bash
# Slide 2 using Slide 1 as reference (reference chaining)
python "$NANOBANANA_SCRIPT" \
  --prompt "[VISUAL SYSTEM + Slide 2 content]. Match the exact visual style, colors, layout and typography of the reference image." \
  --output "./output/carousel/slide_02.png" \
  --reference "./output/carousel/slide_01_hook.png" \
  --aspect portrait

# Slide 3 using Slide 2 as reference
python "$NANOBANANA_SCRIPT" \
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
- Background: [base color family — but each slide gets a UNIQUE gradient variation, see gradient rules below]
- Top bar: [brand name/logo area description]
- Content zone: [centered, with exact margin descriptions]
- Typography: Headlines in [style, color] — MEDIUM-SIZED (20-25% of card height max), body in [style, color]
- Accent elements: [shapes, lines, icons with colors and positions]
- Bottom bar: [progress indicator "X/N" in bottom-right, small text, {hex color}]
- Swipe indicator on slide 1 only: "Swipe →" in small text, bottom-center
- Overall feel: [brand tone]
```

**Carousel Gradient Variation Rules:**

"Consistent style" means same color family, layout, and typography — NOT identical backgrounds. Each carousel slide should have a **unique gradient** to create visual variety while maintaining brand cohesion. This prevents the carousel from looking like the same image repeated.

Gradient assignment strategy — pick a different gradient direction/style for each slide from this palette:
1. **Diagonal gradient** — dark in bottom-left to lighter in top-right
2. **Radial gradient** — emanating from center outward
3. **Vertical gradient** — top-to-bottom color shift
4. **Horizontal gradient** — left-to-right with accent color tint on one side
5. **Spotlight gradient** — dark edges with a subtle glow from center-bottom

All gradients must stay within the client's brand color family (e.g., navy-to-blue, not navy-to-orange). Each slide should also have a unique subtle background texture/pattern (hexagons, waves, nodes, particles, etc.) at low opacity (8-15%) to further differentiate slides.

**Carousel Brand Color Integration:**

The client's PRIMARY brand color must appear prominently in carousel slides — not just as a small accent. Incorporate it into:
- Background gradients (as a tint or secondary gradient color)
- Pill badges and CTA buttons
- Accent text highlighting
- Icons and decorative elements
- Separator lines

This ensures the carousel feels branded, not generic. A viewer should immediately associate the carousel with the client's brand from the color usage alone.

**Carousel Text Containment Strategy (critical for Seedream 4.5):**

AI image models like Seedream tend to make text fill all available space. To control text size on carousel slides, use a **centered content card** approach in your prompts:

- Describe "a wide rounded rectangle content card spanning about 80 percent of the slide width, with a slightly lighter background and subtle border, centered horizontally and vertically on the slide". The card must be WIDE — LinkedIn posts are viewed on feeds where narrow cards look cramped. 80% width is the sweet spot.
- Place ALL text content INSIDE this card
- Specify the card should take "about 40-50 percent of the card height and 80 percent of the card width, centered vertically and horizontally with equal empty gradient space above, below, and on both sides"
- This physically constrains the text into a bounded area, preventing it from expanding to fill the slide
- The surrounding gradient background remains visible around all edges of the card, creating breathing room while keeping the content prominent and readable on LinkedIn's feed

This approach works because image models respect visual containers — a bounded card naturally limits text size in a way that verbal instructions ("make text small") often fail to achieve.

**Carousel Slide Structure:**

**Slide 1 — The Hook (most critical):**
- Centered content card with headline, maximum 2-3 lines
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

### Phase 2.5: Logo Compositing (MANDATORY for all outputs)

**NEVER rely on AI to render the client's logo.** AI models cannot accurately reproduce specific logos — they will always get it wrong. Instead, always composite the real downloaded logo using Python/Pillow.

**Rules:**
1. **In the generation prompt**, tell the AI to leave the logo area COMPLETELY EMPTY — no text, no shapes, no brand name. Say explicitly: "Leave the top-left corner completely blank white/clean — no text or elements."
2. **Never cover up AI-generated logo text with a rectangle** — this creates visible artifacts (grey boxes) that look terrible. If the AI generates unwanted text in the logo area, REGENERATE the image with stronger instructions to keep that area empty.
3. **After generation**, composite the real logo using Pillow:

```python
from PIL import Image

post = Image.open("generated_post.png").convert("RGBA")
logo = Image.open("client_logo.png").convert("RGBA")

# Scale logo to ~18-22% of post width
target_w = int(post.size[0] * 0.20)
scale = target_w / logo.size[0]
logo_resized = logo.resize(
    (int(logo.size[0] * scale), int(logo.size[1] * scale)),
    Image.LANCZOS
)

# Paste with transparency — no rectangle cover-ups
margin = int(post.size[0] * 0.04)
post.paste(logo_resized, (margin, margin), logo_resized)
post.save("final_post.png", "PNG")
```

4. **For dark backgrounds**, create a white version of the logo:
```python
import numpy as np
logo_arr = np.array(logo)
logo_arr[:, :, :3] = 255  # Make RGB white, keep alpha
logo_white = Image.fromarray(logo_arr)
```

5. **Logo placement**: Default to top-left unless the user specifies otherwise.

### Phase 3: Quality Check

Run through this checklist before delivering. Every Critical item must pass.

**Critical (zero tolerance):**
- [ ] Brand assets extracted FIRST (Phase 0.5 completed) — fonts, colors, logo downloaded
- [ ] Font in prompt matches the client's actual website font (described by style, not by name)
- [ ] Correct aspect ratio (portrait 9:16 or square 1:1) verified visually
- [ ] No spelling or grammar errors in the prompt text
- [ ] Brand colors match guide (described by name in prompt, not hex) — colors from CLIENT, not reference
- [ ] All text readable — large enough to read on mobile
- [ ] No artifacts, distortion, or low-res elements — NO grey rectangles or patched areas
- [ ] PNG format output
- [ ] Real logo composited via Pillow (Phase 2.5) — NOT AI-generated logo text
- [ ] Logo area was left empty in the AI prompt — no cover-up rectangles used
- [ ] Design looks like a professional social media template, not a generic AI image
- [ ] No gradient orbs, glowing spheres, bokeh, or atmospheric light effects — flat/solid preferred

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
- [ ] Background is solid/flat by default — gradients only when specifically justified

**Important — carousels only:**
- [ ] Consistent style family across all slides (same color family, layout, typography — NOT identical backgrounds)
- [ ] Each slide has a UNIQUE gradient background (different direction/style per slide, same color family)
- [ ] Client's primary brand color appears prominently (in gradients, pills, icons — not just tiny accents)
- [ ] Headline text is medium-sized (20-25% of card height) — NOT oversized or filling the card
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
| Gradient orbs / glowing spheres / bokeh | Looks AI-generated and amateur |
| AI-rendered logos | Always wrong — composite the real logo |
| Covering AI text with solid rectangles | Creates visible grey box artifacts |
| Skipping brand extraction | Wrong fonts, wrong colors, off-brand output |
| Using hex codes or font names in prompts | AI renders them as visible text |

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

- **Nano Banana 2 API fails** → Check SEADREAM_API_KEY is set and `requests` is installed (`uv pip install requests`). Retry once. If still failing, fall back to Seedream 4.5 (`python "$SEEDREAM_SCRIPT"`), then Flux 2 (`python "$FLUX_SCRIPT"`), or report the error.
- **Seedream 4.5 API fails** → Check SEADREAM_API_KEY is set. Retry once. If still failing, fall back to Flux 2 (`python "$FLUX_SCRIPT"`) or report the error.
- **Flux 2 API fails** → Check FLUX_API_KEY is set. Retry once. If still failing, try Nano Banana 2 or Seedream 4.5 as fallback, or report the error to the user.
- **Text rendering is poor** → Add explicit instructions: "Text must be perfectly typeset, crisp, and professionally rendered. Each word must be spelled exactly as specified."
- **Style inconsistency in carousel** → Use reference chaining (each slide references the previous) and strengthen the visual system description.
- **Image quality too low** → Try increasing width/height dimensions for higher resolution.
- **File system unavailable** → Output images to current directory and provide paths.
- **Reference image not found** → List available references in the category with `ls "$REFS_DIR/{category}/"`. If category is empty, try the closest adjacent category. If no references exist at all, proceed without `--reference` but warn the user that output quality may be lower.
- **Output doesn't match reference style** → Try a different reference from the same category. If none work well, try a reference from an adjacent category (e.g., `corporate/` for a `tech/` business).
- **Brand doc missing colors/fonts** → Scrape the company website to extract primary colors from CSS, identify fonts from the site's typography, and download the logo from the site header.
- Output always goes to `./output/` in the project directory.

*LinkedIn Post Skill | v1.2 | Updated 2026-03*
