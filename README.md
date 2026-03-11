# LinkedIn Post Skill for Claude Code

Create high-performing LinkedIn posts — single images and multi-slide carousels — using Gemini AI image generation, directly from Claude Code.

## What It Does

- Generates production-ready LinkedIn post graphics (single image or carousel)
- Writes LinkedIn-optimized copy when given just a topic
- Supports portrait (1080x1350) and square (1080x1080) formats
- Uses Flash model for quick drafts, Pro model for final output up to 4K
- Includes 12 LinkedIn-specific design principles, carousel templates, and quality checklists

## Prerequisites

1. **Claude Code** installed
2. **Nano Banana Pro plugin** (provides Gemini image generation):
   ```
   /install-plugin buildatscale-tv/claude-code-plugins nano-banana-pro
   ```
3. **`GEMINI_API_KEY`** environment variable set with a valid Google Gemini API key

## Installation

Install this skill in Claude Code:

```
/install-skill Aston1690/linkedin-post-skill
```

## Usage

Just ask Claude Code to create a LinkedIn post:

- "Create a LinkedIn post about AI in recruitment"
- "Make a LinkedIn carousel on 5 tips for remote teams"
- "Design a LinkedIn graphic announcing our new product"

The skill will:
1. Collect your brand info and brief
2. Write copy (if needed) using proven LinkedIn formulas
3. Show you a Design Spec for approval
4. Generate a draft (Flash) → review → final (Pro at 2K)
5. Export to `./output/`

## What You Provide

| Input | Required | Notes |
|-------|----------|-------|
| Brand info | Yes | Colors (hex), fonts, logo, tone |
| Content brief | Yes | Topic at minimum — skill writes copy if needed |
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

## License

MIT
