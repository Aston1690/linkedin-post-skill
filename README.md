# LinkedIn Post Skill for Claude Code

Create beautiful, agency-quality LinkedIn posts and carousels with AI image generation — directly from Claude Code.

## What It Does

- Generates production-ready LinkedIn post graphics (single image or carousel)
- Uses **Nano Banana 2** (Gemini 3.1 Flash Image) as the default AI generation model
- Supports **Seedream 4.5** as fallback and **Flux 2 Pro** for reference-guided generation
- **Premium Light aesthetic** — bright, airy designs with light backgrounds, decorative elements, and floating cards
- Extracts brand colors, fonts, and logos from any client website automatically
- Composites the real client logo via Pillow — never relies on AI to render logos
- Always includes relevant photographs in every post
- Writes LinkedIn-optimized copy when given just a topic
- Supports portrait (1080x1350) and square (1080x1080) formats
- Includes 6 professional layout patterns, 12 design principles, and quality checklists

## One-Line Install

```bash
bash <(curl -sL https://raw.githubusercontent.com/Aston1690/linkedin-post-skill/main/install.sh)
```

Then restart Claude Code. Type `/linkedin-post` to use it.

## Prerequisites

1. **Claude Code** installed
2. **Python 3** with `requests` and `Pillow` packages
3. **At least one API key** (set as environment variable):
   - `SEADREAM_API_KEY` — OpenRouter API key (used for Nano Banana 2 and Seedream 4.5)
   - `FLUX_API_KEY` — BFL or OpenRouter key (for Flux 2 Pro reference-guided generation)

## Image Generation Models

| Model | Script | Best For | API Key |
|-------|--------|----------|---------|
| **Nano Banana 2** (default) | `nanobanana_image.py` | Best quality — superior text rendering and design fidelity | `SEADREAM_API_KEY` |
| **Seedream 4.5** (fallback) | `seedream_image.py` | Fallback if Nano Banana 2 fails | `SEADREAM_API_KEY` |
| **Flux 2 Pro** | `flux_image.py` | Reference-guided generation with style matching | `FLUX_API_KEY` |

## Usage

Just ask Claude Code to create a LinkedIn post:

- "Create a LinkedIn post about AI in recruitment"
- "Make a LinkedIn carousel on 5 tips for remote teams"
- "Design a LinkedIn graphic announcing our new product"

The skill will:
1. Extract brand assets from the client's website (colors, fonts, logo)
2. Match the business to a reference style category
3. Write copy (if needed) using proven LinkedIn formulas
4. Show you a Design Spec for approval
5. Generate the design with AI (Nano Banana 2 by default)
6. Composite the real logo via Pillow
7. Export to `./output/`

## Design Style: Premium Light

Every post follows the **Premium Light** aesthetic by default:

- Light off-white / pale grey backgrounds (never dark)
- Bold oversized headlines in dark navy with accent words in purple
- Large semi-transparent accent circle blob in upper-right
- Small cross (+) markers and geometric line patterns as texture
- White floating cards with rounded corners and subtle shadows
- Relevant photographs integrated into every design
- Dark navy CTA button with white text
- Real logo composited cleanly (never AI-rendered)

## What You Provide

| Input | Required | Notes |
|-------|----------|-------|
| Brand info | Yes | Website URL, or colors (hex) + fonts + logo |
| Content brief | Yes | Topic at minimum — ideally key message + audience |
| Post type | Yes | Single image or carousel (skill recommends if unclear) |
| CTA | Yes | Default: "Follow for more" |
| Reference posts | Optional | 2-3 examples you like |

## Formats

| Format | Dimensions | Best For |
|--------|-----------|----------|
| Single portrait | 1080 x 1350 px | Maximum feed engagement (+23% vs square) |
| Single square | 1080 x 1080 px | Universal safe option |
| Carousel portrait | 1080 x 1350 px/slide | Educational, lists, stories |
| Carousel square | 1080 x 1080 px/slide | Alternative carousel |

## Layout Patterns

| Pattern | Best For |
|---------|----------|
| Header Bar | General posts, announcements |
| Split | Feature showcase, team intros |
| Testimonial | Client quotes, social proof |
| Stats | Data-driven, results |
| Service | Value props, capabilities |
| CTA | Closing slides, contact |

## License

MIT
