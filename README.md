# LinkedIn Post Skill for Claude Code

Create high-performing LinkedIn posts — single images and multi-slide carousels — using Puppeteer HTML-to-image rendering and open-source stock photos, directly from Claude Code.

## What It Does

- Generates production-ready LinkedIn post graphics (single image or carousel)
- Renders pixel-perfect designs from HTML/CSS using Puppeteer — no paid AI APIs needed
- Fetches matching stock photos from Unsplash, Pexels, and Pixabay
- **Strictly follows image suggestions** from your content document
- Writes LinkedIn-optimized copy when given just a topic
- Supports portrait (1080x1350) and square (1080x1080) formats
- Includes 6 professional layout templates, 12 design principles, and quality checklists
- Uses reference images as visual guides for layout structure

## Prerequisites

1. **Claude Code** installed
2. **Node.js** v18+ installed
3. **At least one image API key** (for stock photos):
   - `UNSPLASH_ACCESS_KEY` — from [Unsplash Developers](https://unsplash.com/developers)
   - `PEXELS_API_KEY` — from [Pexels API](https://www.pexels.com/api/)
   - `PIXABAY_API_KEY` — from [Pixabay API](https://pixabay.com/api/docs/)

## One-Line Install

```bash
bash <(curl -sL https://raw.githubusercontent.com/Aston1690/linkedin-post-skill/main/install.sh)
```

Then restart Claude Code. Type `/linkedin-post` to use it.

## How It Works

1. **HTML Templates** — 6 professional layout patterns (Header Bar, Split, Testimonial, Stats, Service, CTA)
2. **Puppeteer Rendering** — Converts HTML/CSS to pixel-perfect PNG screenshots at 2x resolution
3. **Open-Source Photos** — Fetches images from Unsplash/Pexels/Pixabay matching your content doc's image suggestions
4. **Reference-Based Design** — Studies reference images for layout structure, then replicates in HTML with your brand

## Usage

Just ask Claude Code to create a LinkedIn post:

- "Create a LinkedIn post about AI in recruitment"
- "Make a LinkedIn carousel on 5 tips for remote teams"
- "Design a LinkedIn graphic announcing our new product"

The skill will:
1. Match your brand to a reference style category
2. Fetch stock photos matching your content doc's image suggestions
3. Collect your brand info and brief
4. Write copy (if needed) using proven LinkedIn formulas
5. Show you a Design Spec for approval
6. Render the design with Puppeteer
7. Export to `./output/`

## What You Provide

| Input | Required | Notes |
|-------|----------|-------|
| Brand info | Yes | Colors (hex), fonts, logo, tone |
| Content brief | Yes | Topic at minimum — include image suggestions for best results |
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

## Layout Templates

| Pattern | Best For | Template |
|---------|----------|----------|
| Header Bar | General posts, announcements | `pattern1_header_bar.html` |
| Split | Feature showcase, team intros | `pattern2_split.html` |
| Testimonial | Client quotes, social proof | `pattern3_testimonial.html` |
| Stats | Data-driven, results | `pattern4_stats.html` |
| Service | Value props, capabilities | `pattern5_service.html` |
| CTA | Closing slides, contact | `pattern6_cta.html` |

## License

MIT
