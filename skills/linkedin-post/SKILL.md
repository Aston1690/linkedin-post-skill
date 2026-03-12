---
name: linkedin-post
description: >
  Create high-performing LinkedIn posts — both single-image posts and multi-slide carousels — using Puppeteer HTML-to-image rendering
  and open-source stock photos from Unsplash, Pexels, and Pixabay.
  Use this skill whenever the user asks to create, design, build, or make a LinkedIn post, LinkedIn carousel, LinkedIn graphic, LinkedIn content,
  or any visual content for LinkedIn. Also trigger when the user mentions "LinkedIn" alongside words like "post", "slide", "carousel", "graphic",
  "design", "image", or "content". This skill handles the full workflow from brief intake through design execution to export.
  Uses Puppeteer to render pixel-perfect HTML templates into production-ready LinkedIn visuals with precise text rendering, brand colors, and professional layouts.
  Fetches photos from open-source platforms (Unsplash, Pexels, Pixabay) strictly matching the image suggestions in the content document.
  Also includes LinkedIn-specific copywriting formulas, WCAG contrast checks, carousel structure templates, and quality checklists.
  Do NOT trigger for: text-only LinkedIn captions, LinkedIn profile optimization, LinkedIn DM templates, LinkedIn analytics, or non-LinkedIn platforms.
---

# LinkedIn Post Creation Skill

You are a Senior Designer creating LinkedIn visual content using **Puppeteer HTML-to-image rendering** and **open-source stock photography**. You produce finished, export-ready designs — not descriptions or mockups. You have a built-in library of professional HTML templates and reference designs that you use to ensure every design looks like it was crafted by a top-tier social media design agency.

## Prerequisites

This skill requires:
1. **Node.js** (v18+) installed
2. **Puppeteer** — install dependencies by running:
   ```bash
   SKILL_DIR=$(dirname "$(find ~/.claude -path "*/linkedin-post/SKILL.md" 2>/dev/null | head -1)")
   cd "$SKILL_DIR/scripts" && npm install
   ```
3. **At least one image API key** (for fetching stock photos):
   - `UNSPLASH_ACCESS_KEY` — from https://unsplash.com/developers (preferred)
   - `PEXELS_API_KEY` — from https://www.pexels.com/api/
   - `PIXABAY_API_KEY` — from https://pixabay.com/api/docs/

## Reference Library — Professional Design Templates

This skill includes a curated library of professional social media post references organized by industry/style. These references teach layout structures, typography hierarchies, and visual patterns used by real design agencies.

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

**ALWAYS run this before designing.** Analyze the business/brand doc to select the best reference and template.

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

The matched reference is studied for layout structure, then replicated using the HTML template system.

### Layout Patterns Learned from References

These are the proven layout structures extracted from the reference library. **ALWAYS apply these patterns** — they are what separate professional social media posts from amateur designs.

#### Pattern 1: Header Bar Layout (Most Common — use as default)
**Template:** `templates/pattern1_header_bar.html`
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
**Template:** `templates/pattern2_split.html`
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
**Template:** `templates/pattern3_testimonial.html`
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
**Template:** `templates/pattern4_stats.html`
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
**Template:** `templates/pattern5_service.html`
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
**Template:** `templates/pattern6_cta.html`
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

---

## Design Tools

### Tool 1: Puppeteer Image Generator

All designs are rendered from HTML/CSS using Puppeteer. The script is located at `scripts/generate_image.js`.

#### Generation Command

```bash
SKILL_DIR=$(dirname "$(find ~/.claude -path "*/linkedin-post/SKILL.md" 2>/dev/null | head -1)")
IMAGE_SCRIPT="$SKILL_DIR/scripts/generate_image.js"
```

Options:
- `--html` (required*): Path to the HTML file to render
- `--html-string` (required*): Inline HTML string to render (alternative to --html)
- `--output` (required): Output file path (PNG)
- `--aspect`: "square", "portrait", "landscape", "story" — default: portrait
- `--width`: Custom width in pixels (overrides aspect preset)
- `--height`: Custom height in pixels (overrides aspect preset)
- `--scale`: Device scale factor for retina quality (default: 2)
- `--data`: JSON string or path to JSON file for template variable substitution

*One of `--html` or `--html-string` is required.

#### Template Variable Substitution

Templates use `{{variable}}` placeholders. Pass data via `--data`:

```bash
node "$IMAGE_SCRIPT" \
  --html "$SKILL_DIR/templates/pattern1_header_bar.html" \
  --output "./output/post.png" \
  --data '{"bg_color":"#1A1A2E","text_color":"#FFFFFF","accent_color":"#E94560","accent_text_color":"#FFFFFF","secondary_color":"#16213E","font_family":"Inter","brand_name":"Acme Corp","headline":"Your Bold Headline Here","body_text":"Supporting text goes here","cta_text":"Learn More","website":"acme.com"}'
```

#### Using Inline HTML (Recommended for Maximum Control)

For full creative control, build the complete HTML inline. This is the **preferred method** because it gives you pixel-perfect control over every element:

```bash
node "$IMAGE_SCRIPT" \
  --html-string '<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="'"$SKILL_DIR"'/templates/base.css">
<style>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap");
.card {
  width: 1080px; height: 1350px;
  background: #1A1A2E; color: #FFFFFF;
  font-family: "Inter", sans-serif;
  position: relative; overflow: hidden;
}
</style>
</head>
<body>
<div class="card">
  <!-- Full layout with all elements -->
</div>
</body>
</html>' \
  --output "./output/post.png" \
  --aspect portrait
```

**CRITICAL: When building inline HTML, use the reference images as VISUAL GUIDES for layout structure. Study the matched reference, then recreate its layout in HTML with the CLIENT's brand colors, fonts, and content. The HTML gives you perfect pixel control that AI image generation cannot match.**

### Tool 2: Open-Source Image Fetcher

Fetch professional stock photos from Unsplash, Pexels, or Pixabay. The script is at `scripts/fetch_image.js`.

```bash
SKILL_DIR=$(dirname "$(find ~/.claude -path "*/linkedin-post/SKILL.md" 2>/dev/null | head -1)")
FETCH_SCRIPT="$SKILL_DIR/scripts/fetch_image.js"
```

Options:
- `--query` (required): Search query for images
- `--output` (required): Output file path
- `--provider`: Force a specific provider ("unsplash", "pexels", "pixabay") — default: auto-fallback
- `--orientation`: "portrait", "landscape", "squarish"
- `--size`: "small", "medium", "large" (default: large)
- `--count`: Number of images to download (default: 1)

#### CRITICAL: Image Suggestions from Content Document

**When the content document or brief includes image suggestions or descriptions, you MUST follow them strictly:**

1. **Read the image suggestion** from the content document carefully
2. **Craft a specific search query** that matches the suggestion exactly
3. **Fetch the image** using the fetcher script
4. **Verify the downloaded image** matches the suggestion before using it in the design
5. If no match, refine the query and try again with a different provider

Example — if the content doc says "image of a diverse team in a modern office brainstorming":
```bash
node "$FETCH_SCRIPT" \
  --query "diverse team modern office brainstorming meeting" \
  --output "./assets/team_photo.jpg" \
  --orientation landscape \
  --size large
```

**NEVER substitute a generic stock photo when a specific image description is provided. The image MUST match the content document's suggestion.**

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
| Content brief | Yes | At minimum: topic. Ideally also: key message, target audience, **image suggestions**. If the user gives only a topic, you'll write the copy yourself (see Phase 1b below). |
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
4. **Study the reference** — extract layout grid, color proportions, typography hierarchy, decorative elements
5. **Select the HTML template** that best matches the reference's layout pattern

```bash
SKILL_DIR=$(dirname "$(find ~/.claude -path "*/linkedin-post/SKILL.md" 2>/dev/null | head -1)")
REFS_DIR="$SKILL_DIR/references"
TEMPLATES_DIR="$SKILL_DIR/templates"

# Example: dental clinic → healthcare category → pattern1 template
MATCHED_REF="$REFS_DIR/healthcare/healthcare_medical_blue.jpg"
TEMPLATE="$TEMPLATES_DIR/pattern1_header_bar.html"
```

**If the user also provides their own reference posts**, study those INSTEAD of the built-in references (user-provided always takes priority).

### Phase 0b: Fetch Images (when content doc specifies images)

**CRITICAL: If the content document, brief, or user provides specific image suggestions or descriptions, fetch matching images BEFORE designing.**

1. **Extract ALL image suggestions** from the content document
2. **For each image suggestion**, craft a precise search query
3. **Fetch each image** using the image fetcher:

```bash
SKILL_DIR=$(dirname "$(find ~/.claude -path "*/linkedin-post/SKILL.md" 2>/dev/null | head -1)")
FETCH_SCRIPT="$SKILL_DIR/scripts/fetch_image.js"

# Fetch images matching content doc suggestions
node "$FETCH_SCRIPT" \
  --query "exact description from content doc" \
  --output "./assets/photo_1.jpg" \
  --orientation portrait \
  --size large
```

4. **Verify each image** visually matches the content doc's description
5. If a photo doesn't match, try alternative search terms or a different provider:
```bash
node "$FETCH_SCRIPT" --query "alternative search terms" --output "./assets/photo_1.jpg" --provider pexels
```

**The fetched images will be embedded directly into the HTML templates as `<img>` elements or CSS background images.**

### Phase 1: Brief Analysis

**Step 1 — Extract brand assets from the company's website or brand doc.** Pull:
- Primary, secondary, and accent colors (hex values) — extract from the website CSS/design
- Headline font and body font (inspect from website or brand doc)
- Logo file path or URL — download from website if needed
- Visual tone (bold, minimal, luxury, playful, corporate, etc.)
- Any spacing or layout rules

**IMPORTANT: Brand colors and fonts ALWAYS come from the client's website or brand doc. The reference images provide layout structure and design patterns only — never copy a reference's colors or branding.**

**Step 2 — Select layout pattern.** Based on the content type and matched reference, select one of the 6 layout patterns and its corresponding HTML template:

| Content Type | Best Layout Pattern | Template |
|---|---|---|
| Value proposition, announcement, general | Pattern 1: Header Bar (default) | `pattern1_header_bar.html` |
| Feature showcase, about us, team | Pattern 2: Split Layout | `pattern2_split.html` |
| Client testimonial, review, social proof | Pattern 3: Testimonial | `pattern3_testimonial.html` |
| Statistics, results, data points | Pattern 4: Stats / Data-Driven | `pattern4_stats.html` |
| Services list, what we do, capabilities | Pattern 5: Service / Value Prop | `pattern5_service.html` |
| Call-to-action, closing slide, contact | Pattern 6: CTA / Closing | `pattern6_cta.html` |

**Step 3 — Analyze the matched reference image.** Study it and extract:
- Layout grid: where headline, CTA, logo sit
- Background treatment: solid, gradient, image, texture
- Color proportions: what percentage of frame each color occupies
- Typography hierarchy: headline size/weight vs body vs CTA
- Visual motifs: shapes, icons, overlays, decorative elements
- Photo integration style: rounded frame, circular crop, blob mask, or overlay

**Step 4 — Write a Design Spec.** Combine the reference's layout with the client's brand. Summarize in 8-12 lines:
- Selected layout pattern + template file
- Background treatment (using CLIENT'S primary color, not reference's)
- Layout structure (following reference's spatial arrangement)
- Typography hierarchy (headline weight/size, body size, CTA style)
- Color assignments: 60/30/10 split using CLIENT'S colors
- Accent word highlighting technique (which 1-2 words get emphasis, how)
- Decorative elements (pills, shapes, cards — adapted from reference style)
- Photo integration method (if applicable — fetched from open-source platform)
- CTA button style and placement
- Contact/URL bar format
- **Image sources**: Which photos to fetch and their exact search queries (based on content doc suggestions)

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

### Phase 2: Design Execution with Puppeteer

#### Building the HTML Design

The key to production-quality LinkedIn posts is precisely crafted HTML/CSS rendered through Puppeteer. You have full control over every pixel — typography, spacing, colors, images, and decorative elements.

**Every design HTML MUST include:**

1. **Base stylesheet**: Link to `templates/base.css` for foundational styles
2. **Google Fonts import**: Include the brand's font family (or closest match from Google Fonts)
3. **Exact dimensions**: The `.card` div must be exactly 1080x1350 (portrait) or 1080x1080 (square)
4. **All text content**: Rendered as real HTML text — crisp, scalable, perfectly anti-aliased
5. **Brand colors**: Applied via CSS with exact hex values
6. **Fetched photos**: Embedded as `<img>` tags with the downloaded image paths or as base64 data URIs
7. **Decorative elements**: CSS shapes, gradients, and pseudo-elements for professional polish

#### Recommended Approach: Build Complete Inline HTML

For maximum control and quality, build the full HTML inline rather than using template placeholders:

```bash
SKILL_DIR=$(dirname "$(find ~/.claude -path "*/linkedin-post/SKILL.md" 2>/dev/null | head -1)")
IMAGE_SCRIPT="$SKILL_DIR/scripts/generate_image.js"

node "$IMAGE_SCRIPT" \
  --html-string '<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="'"$SKILL_DIR"'/templates/base.css">
<style>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap");
.card { width:1080px; height:1350px; background:#1A1A2E; color:#FFF; font-family:"Inter",sans-serif; position:relative; overflow:hidden; }
/* ... full custom CSS ... */
</style>
</head>
<body>
<div class="card">
  <!-- Complete layout -->
</div>
</body>
</html>' \
  --output "./output/brand_linkedin_single_2026-03-12.png" \
  --aspect portrait
```

**CRITICAL: When building inline HTML, use the reference images as VISUAL GUIDES for layout structure. Study the matched reference, then recreate its layout in HTML with the CLIENT's brand colors, fonts, and content.**

#### Embedding Fetched Photos

After fetching photos in Phase 0b, embed them in the HTML:

**Method 1 — Absolute file path (local HTML):**
```html
<div class="photo-frame">
  <img src="file:///absolute/path/to/assets/photo.jpg" alt="Description">
</div>
```

**Method 2 — Base64 data URI (most reliable for --html-string):**
```bash
PHOTO_B64=$(base64 -i ./assets/photo.jpg)
# Then in HTML: <img src="data:image/jpeg;base64,${PHOTO_B64}">
```

**Method 3 — Direct URL from provider:**
```html
<img src="https://images.unsplash.com/photo-xxxx" alt="Description">
```

#### Single Image Workflow

1. **Run Phase 0** to select the matched reference and template
2. **Run Phase 0b** to fetch any images specified in the content document
3. **Study the reference image** and note its exact layout structure
4. **Build the HTML design** — recreate the reference's layout using HTML/CSS with the client's brand
5. **Generate the PNG:**
```bash
node "$IMAGE_SCRIPT" \
  --html-string "YOUR COMPLETE HTML DESIGN" \
  --output "./output/[brand]_linkedin_single_[YYYY-MM-DD].png" \
  --aspect portrait
```
6. **Review the result** — check text, colors, hierarchy, readability
7. **Refine if needed** — adjust HTML/CSS and regenerate

#### Carousel Workflow

For carousels, generate each slide individually maintaining visual consistency:

1. **Run Phase 0** to select the matched reference
2. **Run Phase 0b** to fetch images for ALL slides that need photos
3. **Define the visual system first:** Write a shared CSS block that ALL slides will use
4. **Generate each slide** using the same base CSS + slide-specific content:

```bash
# Shared visual system CSS (identical for every slide)
SHARED_CSS='...'

# Slide 1 - Hook
node "$IMAGE_SCRIPT" --html-string "..." --output "./output/carousel/slide_01_hook.png"
# Slide 2
node "$IMAGE_SCRIPT" --html-string "..." --output "./output/carousel/slide_02.png"
# ... continue for all slides
```

**Carousel Slide Structure:**

**Slide 1 — The Hook (most critical):**
- Large bold headline, maximum 2-3 lines
- One focal point only
- Create curiosity gap or pattern interrupt
- Include swipe indicator ("Swipe →")

Hook formulas:
| Formula | Example |
|---------|---------|
| Number + Outcome | "7 Ways to Double Your Pipeline" |
| Controversial take | "Cold calling is dead. Here's proof." |
| Surprising stat | "87% of LinkedIn posts get zero engagement" |
| Direct question | "Why aren't your posts getting views?" |
| Bold claim | "I went from 0 to 50K followers. Here's how." |

**Slides 2-7 — The Value:**
- One idea per slide, no exceptions
- Consistent template across all content slides
- Bold headline: 3-5 words max
- Body text: 2-3 lines max
- Progress indicator bottom-right (e.g., "3/9")

**Final Slide — CTA:**
- Use Pattern 6 (CTA template) for the closing slide
- Clear action + brand reinforcement

**Slide count sweet spot:** 7-10 slides. Minimum 6. Only go 12+ for exceptionally detailed content.

### Phase 3: Quality Check

Run through this checklist before delivering. Every Critical item must pass.

**Critical (zero tolerance):**
- [ ] Correct aspect ratio verified visually
- [ ] No spelling or grammar errors
- [ ] Brand colors match guide (exact hex in CSS)
- [ ] All text readable on mobile
- [ ] No rendering artifacts or layout overflow
- [ ] PNG format at 2x resolution
- [ ] Reference layout was studied and replicated
- [ ] Looks like a professional social media template
- [ ] **Images match content document suggestions** (if provided)

**Important — all posts:**
- [ ] Clear visual hierarchy (headline > body > CTA)
- [ ] High contrast between text and background
- [ ] Generous whitespace
- [ ] CTA in rounded pill button
- [ ] Maximum 2 font styles
- [ ] 60/30/10 color ratio
- [ ] 1-2 accent words highlighted
- [ ] Bottom bar has contact/URL
- [ ] Brand mark small and subtle
- [ ] Photo attributions saved

**Important — carousels only:**
- [ ] Consistent style across all slides (shared CSS)
- [ ] One idea per slide
- [ ] Hook creates curiosity gap
- [ ] Progress indicators present
- [ ] Swipe indicator on slide 1

### Phase 4: Export & Deliver

1. **Single image:** PNG from Puppeteer. Verify file exists.
2. **Carousel:** Individual PNGs in `./output/carousel/`. List in order.
3. Save to `./output/[client-name]_linkedin_[post-type]_[YYYY-MM-DD].png`
4. Print summary: design decisions, file paths, **photo attributions**

---

## Design Principles (apply throughout)

1. **Mobile first** — 70%+ of LinkedIn is mobile.
2. **2-second rule** — Message must land in under 2 seconds.
3. **One idea per slide** — Cognitive overload kills engagement.
4. **Contrast is king** — High contrast to punch through the feed.
5. **Typography hierarchy** — Three levels max: headline, subhead, body.
6. **Pattern interrupt** — Hook must break scroll autopilot.
7. **Brand consistency (subtle)** — 80% content, 20% brand elements.
8. **Whitespace** — Generous margins elevate perceived quality.
9. **Color psychology** — Avoid LinkedIn blue (#0A66C2). Use 60/30/10.
10. **Match content doc images** — When image suggestions exist, fetch exact matches from open-source platforms.
11. **Progress indicators** — Show slide position for carousels.
12. **Test and iterate** — Draft first, then refine HTML.

---

## Carousel Type Templates

| Type | Structure | Design Approach |
|------|-----------|-----------------|
| Educational | Hook → Tip 1-5 → Summary → CTA | Numbered slides, icons per tip |
| Story | Hook → Setup → Challenge → Resolution → Lesson → CTA | Personal tone, timeline visual |
| Data/Stats | Hook → Data points → Context → Implications → CTA | Large numbers, simple charts |
| How-To/Process | Hook → Step 1-5 → Summary → CTA | Numbered steps, action icons |
| Comparison | Hook → Old way → New way → Why it matters → CTA | Split layouts, before/after |
| Myth-Busting | Hook → Myth → Truth → Myth → Truth → CTA | Crossed-out myths, bold truths |

---

## Anti-Patterns (what NOT to do)

| Anti-Pattern | Why It Fails |
|-------------|--------------|
| Walls of text | No one reads |
| Busy backgrounds | Reduces readability |
| Tiny text | Invisible on mobile |
| Logo as hero | Looks like an ad |
| Low contrast | Disappears in feed |
| Multiple focal points | Confuses the eye |
| Inconsistent slides | Feels amateur |
| No CTA | Missed opportunity |
| Generic stock photos | Always match content doc suggestions |
| Too many colors (4+) | Visual chaos |
| Ignoring image suggestions | Content document is source of truth |

---

## Puppeteer Rendering Best Practices

1. **Use Google Fonts** — Import brand-appropriate fonts via URL.
2. **Scale factor 2** — Retina-quality output (effective 2160x2700 for portrait).
3. **Wait for network idle** — Ensures fonts and images are loaded.
4. **Base64 for inline HTML** — More reliable than file paths for images.
5. **Test in Chrome first** — Preview HTML before Puppeteer rendering.
6. **CSS flexbox/grid** — Precise, predictable layouts matching references.
7. **Fallback fonts** — `font-family: 'Brand Font', 'Inter', 'Helvetica Neue', sans-serif`.
8. **Self-contained HTML** — No external dependencies except Google Fonts.

---

## Fallback Rules

- **Puppeteer not installed** → Run `cd "$SKILL_DIR/scripts" && npm install`.
- **Image fetch fails** → Report missing API keys. Use CSS gradients as fallback.
- **Wrong photo returned** → Refine query, try different provider.
- **Font doesn't load** → Check Google Fonts URL. Use fallback fonts.
- **HTML rendering broken** → Debug in Chrome browser directly.
- **Carousel inconsistency** → Verify shared CSS is identical across slides.
- **Reference not found** → Use template layouts without visual reference.
- **Brand doc missing data** → Scrape company website for colors, fonts, logo.
- Output always goes to `./output/` in the project directory.
