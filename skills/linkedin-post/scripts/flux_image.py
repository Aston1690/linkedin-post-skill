#!/usr/bin/env python3
"""
Flux 2 Image Generation Script for LinkedIn Post Skill.

Uses the Flux 2 model via BFL (Black Forest Labs) API or OpenRouter
to generate high-quality images from detailed text prompts.

Usage:
    python flux_image.py --prompt "Your design prompt" --output "./output/post.png"
    python flux_image.py --prompt "..." --output "..." --aspect portrait --width 1080 --height 1350
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

# Aspect ratio presets for LinkedIn
ASPECT_PRESETS = {
    "square": (1080, 1080),
    "portrait": (1080, 1350),
    "landscape": (1350, 1080),
}

# BFL API endpoint for Flux 2
BFL_API_URL = "https://api.bfl.ml/v1"
BFL_FLUX_MODEL = "flux-pro-1.1-ultra"

# OpenRouter endpoint (uses chat completions with image modality)
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_FLUX_MODEL = "black-forest-labs/flux.2-pro"


def get_api_key():
    """Get the Flux API key from environment."""
    key = os.environ.get("FLUX_API_KEY")
    if not key:
        # Try loading from .env file in common locations
        for env_path in [".env", "../.env", "../../.env", os.path.expanduser("~/Desktop/Prompt-OS/.env")]:
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
        print("Error: FLUX_API_KEY not found. Set it as an environment variable or in .env file.", file=sys.stderr)
        sys.exit(1)
    return key


def detect_api_provider(api_key):
    """Detect which API provider to use based on key format."""
    if api_key.startswith("sk-or-v1-"):
        return "openrouter"
    else:
        return "bfl"


def generate_with_bfl(prompt, width, height, api_key):
    """Generate image using BFL (Black Forest Labs) Flux 2 API."""
    # Submit generation request
    payload = json.dumps({
        "prompt": prompt,
        "width": width,
        "height": height,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{BFL_API_URL}/{BFL_FLUX_MODEL}",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-Key": api_key,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            task_id = result.get("id")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Error submitting to BFL API ({e.code}): {body}", file=sys.stderr)
        sys.exit(1)

    if not task_id:
        print("Error: No task ID returned from BFL API.", file=sys.stderr)
        sys.exit(1)

    print(f"Generation submitted (task: {task_id}). Polling for result...")

    # Poll for result
    for attempt in range(120):  # Up to ~4 minutes
        time.sleep(2)
        poll_req = urllib.request.Request(
            f"{BFL_API_URL}/get_result?id={task_id}",
            headers={"X-Key": api_key},
        )
        try:
            with urllib.request.urlopen(poll_req) as resp:
                poll_result = json.loads(resp.read().decode())
        except urllib.error.HTTPError:
            continue

        status = poll_result.get("status")
        if status == "Ready":
            image_url = poll_result.get("result", {}).get("sample")
            if image_url:
                return download_image(image_url)
            else:
                print("Error: Result ready but no image URL found.", file=sys.stderr)
                sys.exit(1)
        elif status == "Failed":
            print(f"Error: Generation failed: {poll_result}", file=sys.stderr)
            sys.exit(1)
        else:
            if attempt % 5 == 0:
                print(f"  Status: {status}...")

    print("Error: Generation timed out after 4 minutes.", file=sys.stderr)
    sys.exit(1)


def generate_with_openrouter(prompt, width, height, api_key):
    """Generate image using OpenRouter API with Flux 2 Pro model (chat completions + image modality)."""
    payload = json.dumps({
        "model": OPENROUTER_FLUX_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "modalities": ["image"],
    }).encode("utf-8")

    req = urllib.request.Request(
        OPENROUTER_API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://linkedin-post-skill.local",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Error from OpenRouter API ({e.code}): {body}", file=sys.stderr)
        sys.exit(1)

    # Extract image from chat completions response
    choices = result.get("choices", [])
    if not choices:
        print(f"Error: No choices in response: {result}", file=sys.stderr)
        sys.exit(1)

    message = choices[0].get("message", {})
    images = message.get("images", [])
    if images:
        image_url = images[0].get("image_url", {}).get("url", "")
        if image_url.startswith("data:"):
            # Base64 data URL — extract and decode
            header, b64data = image_url.split(",", 1)
            return base64.b64decode(b64data)
        elif image_url:
            return download_image(image_url)

    print(f"Error: No image data in response: {result}", file=sys.stderr)
    sys.exit(1)


def download_image(url):
    """Download image from URL and return bytes."""
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def main():
    parser = argparse.ArgumentParser(description="Generate images with Flux 2 model")
    parser.add_argument("--prompt", required=True, help="Detailed image generation prompt")
    parser.add_argument("--output", required=True, help="Output file path (PNG)")
    parser.add_argument("--aspect", choices=["square", "portrait", "landscape"], default="portrait",
                        help="Aspect ratio preset (default: portrait)")
    parser.add_argument("--width", type=int, help="Custom width (overrides aspect preset)")
    parser.add_argument("--height", type=int, help="Custom height (overrides aspect preset)")
    parser.add_argument("--reference", help="Path to reference image (for style guidance, BFL only)")

    args = parser.parse_args()

    # Determine dimensions
    if args.width and args.height:
        width, height = args.width, args.height
    else:
        width, height = ASPECT_PRESETS[args.aspect]

    # Ensure output directory exists
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Get API key and detect provider
    api_key = get_api_key()
    provider = detect_api_provider(api_key)

    print(f"Generating with Flux 2 via {provider.upper()}...")
    print(f"  Dimensions: {width}x{height}")
    print(f"  Output: {args.output}")

    # Generate
    if provider == "bfl":
        image_data = generate_with_bfl(args.prompt, width, height, api_key)
    else:
        image_data = generate_with_openrouter(args.prompt, width, height, api_key)

    # Save
    output_path.write_bytes(image_data)
    print(f"Image saved to: {args.output}")
    print(f"  Size: {len(image_data):,} bytes")


if __name__ == "__main__":
    main()
