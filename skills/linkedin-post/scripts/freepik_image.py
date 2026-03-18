#!/usr/bin/env python3
"""
Freepik Mystic Image Generation Script for LinkedIn Post Skill.

Uses Freepik's Mystic API to generate high-quality images from text prompts.
Supports style references, structure references, and brand color palettes.

Usage:
    python freepik_image.py --prompt "Your design prompt" --output "./output/post.png"
    python freepik_image.py --prompt "..." --output "..." --aspect social_post_4_5 --model realism
    python freepik_image.py --prompt "..." --output "..." --style-ref "./reference.png" --colors "#FF6B00,#1A1A2E"
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

# Freepik API endpoints
FREEPIK_MYSTIC_URL = "https://api.freepik.com/v1/ai/mystic"
FREEPIK_CLASSIC_URL = "https://api.freepik.com/v1/ai/text-to-image"
FREEPIK_KONTEXT_PRO_URL = "https://api.freepik.com/v1/ai/text-to-image/flux-kontext-pro"

# Aspect ratio mapping for LinkedIn formats
ASPECT_PRESETS = {
    "square": "square_1_1",
    "portrait": "social_post_4_5",
    "story": "social_story_9_16",
    "landscape": "widescreen_16_9",
    "traditional_portrait": "traditional_3_4",
}

# Model options
MODELS = ["realism", "fluid", "zen", "flexible", "super_real", "editorial_portraits"]


def get_api_key():
    """Get the Freepik API key from environment or .env files."""
    key = os.environ.get("FREEPIK_API_KEY")
    if not key:
        for env_path in [".env", "../.env", "../../.env", os.path.expanduser("~/.env")]:
            if os.path.exists(env_path):
                with open(env_path) as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("FREEPIK_API_KEY="):
                            key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            break
                if key:
                    break
    if not key:
        print("ERROR: FREEPIK_API_KEY not found. Set it as an environment variable.", file=sys.stderr)
        sys.exit(1)
    return key


def encode_image_to_base64(image_path):
    """Read an image file and return base64 encoded string."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def parse_colors(color_string):
    """Parse comma-separated hex colors into Freepik color array."""
    if not color_string:
        return None
    colors = []
    hex_colors = [c.strip() for c in color_string.split(",")]
    weight = round(1.0 / len(hex_colors), 2)
    for c in hex_colors:
        if not c.startswith("#"):
            c = "#" + c
        colors.append({"color": c, "weight": weight})
    return colors


def generate_mystic(api_key, prompt, aspect_ratio="social_post_4_5", model="realism",
                    resolution="2k", style_ref=None, structure_ref=None,
                    colors=None, creative_detailing=50):
    """Generate image using Freepik Mystic API (async)."""

    payload = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "model": model,
        "resolution": resolution,
        "creative_detailing": creative_detailing,
        "filter_nsfw": True,
    }

    if style_ref and os.path.exists(style_ref):
        payload["style_reference"] = encode_image_to_base64(style_ref)
        payload["adherence"] = 60
        payload["hdr"] = 60

    if structure_ref and os.path.exists(structure_ref):
        payload["structure_reference"] = encode_image_to_base64(structure_ref)
        payload["structure_strength"] = 50

    if colors:
        color_array = parse_colors(colors)
        if color_array:
            payload["styling"] = {"colors": color_array}

    headers = {
        "x-freepik-api-key": api_key,
        "Content-Type": "application/json",
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(FREEPIK_MYSTIC_URL, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            task_id = result.get("data", {}).get("task_id")
            if not task_id:
                print(f"ERROR: No task_id returned. Response: {json.dumps(result, indent=2)}", file=sys.stderr)
                sys.exit(1)
            print(f"Task created: {task_id}")
            return task_id
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else "No body"
        print(f"ERROR {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


def poll_mystic_task(api_key, task_id, max_wait=120, interval=5):
    """Poll task status until completed or failed."""
    headers = {
        "x-freepik-api-key": api_key,
    }

    # The GET endpoint to check a specific task
    url = f"{FREEPIK_MYSTIC_URL}/{task_id}"

    elapsed = 0
    while elapsed < max_wait:
        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                data = result.get("data", {})
                status = data.get("status", "UNKNOWN")
                print(f"  Status: {status} ({elapsed}s)")

                if status == "COMPLETED":
                    return data
                elif status == "FAILED":
                    print(f"ERROR: Task failed. Response: {json.dumps(result, indent=2)}", file=sys.stderr)
                    sys.exit(1)
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            print(f"  Poll error {e.code}: {error_body}", file=sys.stderr)

        time.sleep(interval)
        elapsed += interval

    print(f"ERROR: Timed out after {max_wait}s", file=sys.stderr)
    sys.exit(1)


def generate_kontext_pro(api_key, prompt, aspect_ratio="portrait_2_3",
                          input_image=None, guidance=3, steps=50,
                          seed=None, output_format="png"):
    """Generate image using Flux Kontext Pro (async task-based).

    Flux Kontext Pro excels at:
    - Accurate text rendering on images
    - Style-consistent generation from reference images
    - High-quality photorealistic outputs with text overlays
    """
    payload = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "guidance": guidance,
        "steps": steps,
        "output_format": output_format,
    }

    if seed is not None:
        payload["seed"] = seed

    # input_image can be a URL or local file path
    if input_image:
        if input_image.startswith("http"):
            payload["input_image"] = input_image
        elif os.path.exists(input_image):
            # Convert local file to data URI
            b64 = encode_image_to_base64(input_image)
            ext = Path(input_image).suffix.lstrip(".").lower()
            mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp"}.get(ext, "image/png")
            payload["input_image"] = f"data:{mime};base64,{b64}"

    headers = {
        "x-freepik-api-key": api_key,
        "Content-Type": "application/json",
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(FREEPIK_KONTEXT_PRO_URL, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            task_id = result.get("data", {}).get("task_id")
            if not task_id:
                print(f"ERROR: No task_id returned. Response: {json.dumps(result, indent=2)}", file=sys.stderr)
                sys.exit(1)
            print(f"Kontext Pro task created: {task_id}")
            return task_id
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else "No body"
        print(f"ERROR {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


def poll_kontext_task(api_key, task_id, max_wait=180, interval=5):
    """Poll Kontext Pro task status until completed."""
    headers = {"x-freepik-api-key": api_key}
    url = f"{FREEPIK_KONTEXT_PRO_URL}/{task_id}"

    elapsed = 0
    while elapsed < max_wait:
        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                data = result.get("data", {})
                status = data.get("status", "UNKNOWN")
                print(f"  Status: {status} ({elapsed}s)")

                if status == "COMPLETED":
                    return data
                elif status in ("FAILED", "ERROR"):
                    print(f"ERROR: Task failed. Response: {json.dumps(result, indent=2)}", file=sys.stderr)
                    sys.exit(1)
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            print(f"  Poll error {e.code}: {error_body}", file=sys.stderr)

        time.sleep(interval)
        elapsed += interval

    print(f"ERROR: Timed out after {max_wait}s", file=sys.stderr)
    sys.exit(1)


def generate_classic(api_key, prompt, size="square_1_1", num_images=1, guidance_scale=1.5):
    """Generate image using classic text-to-image (synchronous, returns base64)."""
    payload = {
        "prompt": prompt,
        "num_images": num_images,
        "guidance_scale": guidance_scale,
        "image": {"size": size},
        "filter_nsfw": True,
    }

    headers = {
        "x-freepik-api-key": api_key,
        "Content-Type": "application/json",
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(FREEPIK_CLASSIC_URL, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else "No body"
        print(f"ERROR {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)


def save_base64_image(b64_data, output_path):
    """Save base64-encoded image to file."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "wb") as f:
        f.write(base64.b64decode(b64_data))
    print(f"Image saved: {output}")
    return str(output)


def save_url_image(url, output_path):
    """Download image from URL and save to file."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, str(output))
    print(f"Image saved: {output}")
    return str(output)


def main():
    parser = argparse.ArgumentParser(description="Generate LinkedIn post images using Freepik API")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--aspect", default="portrait",
                       choices=list(ASPECT_PRESETS.keys()) + [
                           "square_1_1", "social_post_4_5", "social_story_9_16",
                           "traditional_3_4", "portrait_2_3", "widescreen_16_9"
                       ],
                       help="Aspect ratio (default: portrait = 4:5)")
    parser.add_argument("--model", default="realism", choices=MODELS, help="AI model")
    parser.add_argument("--resolution", default="2k", choices=["1k", "2k", "4k"], help="Resolution")
    parser.add_argument("--style-ref", default=None, help="Style reference image path")
    parser.add_argument("--structure-ref", default=None, help="Structure reference image path")
    parser.add_argument("--colors", default=None, help="Comma-separated hex colors e.g. '#FF6B00,#1A1A2E'")
    parser.add_argument("--creative-detailing", type=int, default=50, help="Detail level 0-100")
    parser.add_argument("--engine", default="mystic", choices=["mystic", "classic", "kontext"], help="API engine")
    parser.add_argument("--input-image", default=None, help="Input/reference image path or URL (for Kontext Pro)")
    parser.add_argument("--guidance", type=float, default=3, help="Guidance scale for Kontext Pro (1-10)")
    parser.add_argument("--steps", type=int, default=50, help="Inference steps for Kontext Pro (1-100)")
    parser.add_argument("--seed", type=int, default=None, help="Seed for reproducible outputs")

    args = parser.parse_args()
    api_key = get_api_key()

    # Resolve aspect ratio
    aspect = ASPECT_PRESETS.get(args.aspect, args.aspect)

    if args.engine == "kontext":
        # Kontext Pro uses slightly different aspect ratio names
        kontext_aspect_map = {
            "square_1_1": "square_1_1",
            "social_post_4_5": "portrait_2_3",  # closest match
            "social_story_9_16": "social_story_9_16",
            "traditional_3_4": "classic_4_3",
            "widescreen_16_9": "widescreen_16_9",
            "portrait_2_3": "portrait_2_3",
        }
        k_aspect = kontext_aspect_map.get(aspect, "portrait_2_3")
        print(f"Generating with Kontext Pro (aspect={k_aspect}, guidance={args.guidance}, steps={args.steps})...")

        task_id = generate_kontext_pro(
            api_key, args.prompt, aspect_ratio=k_aspect,
            input_image=args.input_image or args.style_ref,
            guidance=args.guidance, steps=args.steps,
            seed=args.seed
        )

        print("Polling for result...")
        result = poll_kontext_task(api_key, task_id)

        # Kontext Pro returns images in generated array
        generated = result.get("generated", [])
        if generated:
            img = generated[0]
            if isinstance(img, dict):
                if "url" in img:
                    save_url_image(img["url"], args.output)
                elif "base64" in img:
                    save_base64_image(img["base64"], args.output)
                else:
                    for key in img:
                        if isinstance(img[key], str) and len(img[key]) > 100:
                            save_base64_image(img[key], args.output)
                            break
            elif isinstance(img, str):
                if img.startswith("http"):
                    save_url_image(img, args.output)
                else:
                    save_base64_image(img, args.output)
        else:
            print(f"No images generated. Full result: {json.dumps(result, indent=2)}", file=sys.stderr)
            sys.exit(1)

    elif args.engine == "mystic":
        print(f"Generating with Mystic ({args.model}, {aspect}, {args.resolution})...")
        task_id = generate_mystic(
            api_key, args.prompt, aspect_ratio=aspect, model=args.model,
            resolution=args.resolution, style_ref=args.style_ref,
            structure_ref=args.structure_ref, colors=args.colors,
            creative_detailing=args.creative_detailing
        )

        print("Polling for result...")
        result = poll_mystic_task(api_key, task_id)

        generated = result.get("generated", [])
        if generated:
            # Mystic returns URLs or base64
            img = generated[0]
            if isinstance(img, dict):
                if "url" in img:
                    save_url_image(img["url"], args.output)
                elif "base64" in img:
                    save_base64_image(img["base64"], args.output)
                else:
                    # Try saving the whole thing
                    print(f"Image data keys: {list(img.keys())}")
                    for key in img:
                        if isinstance(img[key], str) and len(img[key]) > 100:
                            save_base64_image(img[key], args.output)
                            break
            elif isinstance(img, str):
                if img.startswith("http"):
                    save_url_image(img, args.output)
                else:
                    save_base64_image(img, args.output)
        else:
            print(f"No images generated. Full result: {json.dumps(result, indent=2)}", file=sys.stderr)
            sys.exit(1)

    else:
        print(f"Generating with Classic ({aspect})...")
        result = generate_classic(api_key, args.prompt, size=aspect)

        images = result.get("data", [])
        if images and images[0].get("base64"):
            save_base64_image(images[0]["base64"], args.output)
        else:
            print(f"No images returned. Response: {json.dumps(result, indent=2)}", file=sys.stderr)
            sys.exit(1)

    print("Done!")


if __name__ == "__main__":
    main()
