#!/usr/bin/env python3
"""
Nano Banana 2 (Gemini 3.1 Flash Image) Generation Script for LinkedIn Post Skill.

Uses Google's Nano Banana 2 model via OpenRouter's chat/completions endpoint
to generate high-quality images from detailed text prompts.

Usage:
    python nanobanana_image.py --prompt "Your design prompt" --output "./output/post.png"
    python nanobanana_image.py --prompt "..." --output "..." --aspect portrait
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: 'requests' package is required. Install with: uv pip install requests", file=sys.stderr)
    sys.exit(1)

ASPECT_PRESETS = {
    "square": (1080, 1080),
    "portrait": (1080, 1350),
    "landscape": (1350, 1080),
}

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
NANOBANANA_MODEL = "google/gemini-3.1-flash-image-preview"


def get_api_key():
    """Get the API key from environment (reuses SEADREAM_API_KEY since both use OpenRouter)."""
    key = os.environ.get("SEADREAM_API_KEY")
    if not key:
        key = os.environ.get("NANOBANANA_API_KEY")
    if not key:
        for env_path in [".env", "../.env", "../../.env",
                         os.path.expanduser("~/Desktop/Prompt-OS/.env")]:
            if os.path.exists(env_path):
                with open(env_path) as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("SEADREAM_API_KEY=") or line.startswith("NANOBANANA_API_KEY="):
                            key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            break
                if key:
                    break
    if not key:
        print("Error: SEADREAM_API_KEY (or NANOBANANA_API_KEY) not found. Set it as an environment variable or in .env file.",
              file=sys.stderr)
        sys.exit(1)
    return key


def generate_image(prompt, width, height, api_key):
    """Generate image via OpenRouter chat completions with Nano Banana 2."""
    full_prompt = f"{prompt}\n\nIMPORTANT: Generate this as a {width}x{height} pixel image."

    response = requests.post(
        url=OPENROUTER_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://linkedin-post-skill.local",
            "X-Title": "LinkedIn Post Skill",
        },
        data=json.dumps({
            "model": NANOBANANA_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            "modalities": ["image"]
        }),
        timeout=180,
    )

    if response.status_code != 200:
        print(f"Error from OpenRouter API ({response.status_code}): {response.text[:500]}", file=sys.stderr)
        sys.exit(1)

    result = response.json()

    # Extract image from the response
    choices = result.get("choices", [])
    if not choices:
        print(f"Error: No choices in response: {json.dumps(result)[:500]}", file=sys.stderr)
        sys.exit(1)

    message = choices[0].get("message", {})

    # Check 'images' field (primary location for image models)
    images = message.get("images", [])
    if images:
        for image in images:
            if isinstance(image, dict):
                url_data = image.get("image_url", {}).get("url", "") if "image_url" in image else image.get("url", "")
                if url_data.startswith("data:"):
                    _, b64 = url_data.split(",", 1)
                    return base64.b64decode(b64)
                elif url_data:
                    return requests.get(url_data, timeout=60).content

    # Fallback: check 'content' field for image parts
    content = message.get("content")
    if isinstance(content, list):
        for item in content:
            if item.get("type") == "image_url":
                url_data = item.get("image_url", {}).get("url", "")
                if url_data.startswith("data:"):
                    _, b64 = url_data.split(",", 1)
                    return base64.b64decode(b64)
                elif url_data:
                    return requests.get(url_data, timeout=60).content

    print(f"Error: No image found in response. Message keys: {list(message.keys())}", file=sys.stderr)
    print(f"Response preview: {json.dumps(result)[:1000]}", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Generate LinkedIn images with Nano Banana 2 via OpenRouter")
    parser.add_argument("--prompt", required=True, help="Detailed image generation prompt")
    parser.add_argument("--output", required=True, help="Output file path (PNG)")
    parser.add_argument("--aspect", choices=["square", "portrait", "landscape"], default="portrait")
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--reference", help="(ignored — Nano Banana 2 does not support reference images via OpenRouter)")

    args = parser.parse_args()

    if args.width and args.height:
        width, height = args.width, args.height
    else:
        width, height = ASPECT_PRESETS[args.aspect]

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    api_key = get_api_key()

    print(f"Generating with Nano Banana 2 (Gemini 3.1 Flash Image) via OpenRouter...")
    print(f"  Dimensions hint: {width}x{height}")
    print(f"  Output: {args.output}")

    image_data = generate_image(prompt=args.prompt, width=width, height=height, api_key=api_key)

    output_path.write_bytes(image_data)
    print(f"Image saved to: {args.output}")
    print(f"  Size: {len(image_data):,} bytes")


if __name__ == "__main__":
    main()
