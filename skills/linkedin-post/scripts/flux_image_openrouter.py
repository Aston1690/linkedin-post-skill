#!/usr/bin/env python3
"""
Image Generation Script for LinkedIn Post Skill — OpenRouter chat-completions variant.

Uses openai/gpt-5-image-mini via OpenRouter's chat/completions endpoint which returns
image data in the 'images' field of the message object.

Usage:
    python flux_image_openrouter.py --prompt "Your design prompt" --output "./output/post.png"
    python flux_image_openrouter.py --prompt "..." --output "..." --aspect portrait
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

ASPECT_PRESETS = {
    "square": (1080, 1080),
    "portrait": (1080, 1350),
    "landscape": (1350, 1080),
}

OPENROUTER_CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"
IMAGE_MODEL = "openai/gpt-5-image-mini"


def get_api_key():
    key = os.environ.get("FLUX_API_KEY")
    if not key:
        for env_path in [".env", "../.env", "../../.env",
                         os.path.expanduser("~/Desktop/Prompt-OS/.env")]:
            if os.path.exists(env_path):
                with open(env_path) as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("FLUX_API_KEY="):
                            key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            break
            if key:
                break
    if not key:
        print("Error: FLUX_API_KEY not found.", file=sys.stderr)
        sys.exit(1)
    return key


def generate_image(prompt, width, height, api_key):
    """Generate image via OpenRouter chat completions endpoint."""
    # Embed size hint in the prompt since the endpoint doesn't take size params
    full_prompt = f"{prompt}\n\nIMPORTANT: Generate this as a {width}x{height} pixel image."

    payload = json.dumps({
        "model": IMAGE_MODEL,
        "messages": [
            {
                "role": "user",
                "content": full_prompt
            }
        ],
        "stream": False
    }).encode("utf-8")

    req = urllib.request.Request(
        OPENROUTER_CHAT_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://linkedin-post-skill.local",
            "X-Title": "LinkedIn Post Skill",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Error from OpenRouter API ({e.code}): {body[:500]}", file=sys.stderr)
        sys.exit(1)

    # Extract image from the 'images' field
    choices = result.get("choices", [])
    if not choices:
        print(f"Error: No choices in response: {json.dumps(result)[:500]}", file=sys.stderr)
        sys.exit(1)

    message = choices[0].get("message", {})

    # Check 'images' field (primary location for this model)
    images = message.get("images", [])
    if images:
        img_entry = images[0]
        img_type = img_entry.get("type")
        if img_type == "image_url":
            url_data = img_entry.get("image_url", {}).get("url", "")
            if url_data.startswith("data:"):
                # Base64 data URI
                _, b64 = url_data.split(",", 1)
                return base64.b64decode(b64)
            else:
                # Regular URL
                return download_image(url_data)

    # Fallback: check 'content' field for image parts
    content = message.get("content")
    if isinstance(content, list):
        for item in content:
            if item.get("type") == "image_url":
                url_data = item.get("image_url", {}).get("url", "")
                if url_data.startswith("data:"):
                    _, b64 = url_data.split(",", 1)
                    return base64.b64decode(b64)
                else:
                    return download_image(url_data)

    print(f"Error: No image found in response. Message keys: {list(message.keys())}", file=sys.stderr)
    print(f"Response preview: {json.dumps(result)[:1000]}", file=sys.stderr)
    sys.exit(1)


def download_image(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def main():
    parser = argparse.ArgumentParser(description="Generate LinkedIn images via OpenRouter")
    parser.add_argument("--prompt", required=True, help="Detailed image generation prompt")
    parser.add_argument("--output", required=True, help="Output file path (PNG)")
    parser.add_argument("--aspect", choices=["square", "portrait", "landscape"], default="portrait")
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--reference", help="(ignored for OpenRouter provider)")

    args = parser.parse_args()

    if args.width and args.height:
        width, height = args.width, args.height
    else:
        width, height = ASPECT_PRESETS[args.aspect]

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    api_key = get_api_key()

    print(f"Generating with {IMAGE_MODEL} via OpenRouter...")
    print(f"  Dimensions hint: {width}x{height}")
    print(f"  Output: {args.output}")

    image_data = generate_image(args.prompt, width, height, api_key)

    output_path.write_bytes(image_data)
    print(f"Image saved to: {args.output}")
    print(f"  Size: {len(image_data):,} bytes")


if __name__ == "__main__":
    main()
