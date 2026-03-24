#!/usr/bin/env python3
"""
generate-image skill — Gemini image generation CLI
Usage: python generate.py --prompt "..." [options]
Output: JSON to stdout  |  Errors: stderr + exit 1
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

FLASH_MODEL = "gemini-3.1-flash-image-preview"
PRO_MODEL = "gemini-3-pro-image-preview"
ALLOWED_MODELS = {FLASH_MODEL, PRO_MODEL}

ALLOWED_ASPECT_RATIOS = {
    "1:1", "16:9", "9:16", "4:3", "3:4", "2:3", "3:2",
    "21:9", "4:5", "5:4", "1:4", "4:1", "1:8", "8:1",
}

ALLOWED_SIZES = {"512", "1K", "2K", "4K"}


def die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def warn(msg: str) -> None:
    print(f"WARNING: {msg}", file=sys.stderr)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate or edit images via the Gemini API.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--prompt", required=True, help="Generation or editing prompt.")
    p.add_argument(
        "--model",
        default=FLASH_MODEL,
        help=f"Model ID. Default: {FLASH_MODEL}. Allowed: {', '.join(sorted(ALLOWED_MODELS))}",
    )
    p.add_argument(
        "--aspect-ratio",
        dest="aspect_ratio",
        default=None,
        help="Aspect ratio (e.g. 16:9, 9:16, 1:1). Optional.",
    )
    p.add_argument(
        "--size",
        default="1K",
        choices=sorted(ALLOWED_SIZES),
        help="Output image size: 512 | 1K | 2K | 4K. Default: 1K.",
    )
    p.add_argument(
        "--modalities",
        default="IMAGE",
        help="Response modalities: IMAGE (default) or TEXT,IMAGE.",
    )
    p.add_argument(
        "--thinking",
        default="minimal",
        choices=["minimal", "High"],
        help="Thinking level: minimal (default) | High.",
    )
    p.add_argument(
        "--google-search",
        dest="google_search",
        action="store_true",
        help="Enable Google Search grounding.",
    )
    p.add_argument(
        "--image-search",
        dest="image_search",
        action="store_true",
        help="Enable image search grounding (Flash model only).",
    )
    p.add_argument(
        "--input-image",
        dest="input_image",
        default=None,
        help="Path to source image for editing mode.",
    )
    p.add_argument(
        "--output",
        default=None,
        help="Output file path. Default: ./gemini-image-{timestamp}.png",
    )
    p.add_argument(
        "--output-dir",
        dest="output_dir",
        default=None,
        help="Output directory (used when --output is not set).",
    )
    return p.parse_args()


def resolve_output_path(args: argparse.Namespace) -> Path:
    if args.output:
        return Path(args.output).expanduser().resolve()
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"gemini-image-{timestamp}.png"
    if args.output_dir:
        base = Path(args.output_dir).expanduser().resolve()
        base.mkdir(parents=True, exist_ok=True)
        return base / filename
    return Path.cwd() / filename


def build_modalities(modalities_str: str) -> list[str]:
    return [m.strip().upper() for m in modalities_str.split(",")]


def main() -> None:
    args = parse_args()

    # Validate model
    if args.model not in ALLOWED_MODELS:
        die(
            f"Model '{args.model}' is not allowed. "
            f"Use one of: {', '.join(sorted(ALLOWED_MODELS))}. "
            f"Never use gemini-2.5-flash-image or any gemini-2.x / gemini-1.x model."
        )

    # Validate aspect ratio
    if args.aspect_ratio and args.aspect_ratio not in ALLOWED_ASPECT_RATIOS:
        die(
            f"Aspect ratio '{args.aspect_ratio}' is not supported. "
            f"Allowed: {', '.join(sorted(ALLOWED_ASPECT_RATIOS))}"
        )

    # Validate image-search / model compatibility
    if args.image_search and args.model != FLASH_MODEL:
        warn(
            f"--image-search is only supported on {FLASH_MODEL}. "
            f"Ignoring --image-search for model '{args.model}'."
        )
        args.image_search = False

    # Validate input image exists
    if args.input_image:
        input_path = Path(args.input_image).expanduser().resolve()
        if not input_path.exists():
            die(f"--input-image path does not exist: {input_path}")
    else:
        input_path = None

    # Import SDK (late import so argparse errors surface before SDK errors)
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        die(
            "google-genai is not installed. Run: pip install 'google-genai>=1.55.0'"
        )

    try:
        from PIL import Image as PILImage
    except ImportError:
        die("Pillow is not installed. Run: pip install 'Pillow>=10.0.0'")

    # Initialise client (reads GEMINI_API_KEY from env, falls back to Google ADC)
    client = genai.Client()

    # Build image_config
    image_config_kwargs: dict = {"image_size": args.size}
    if args.aspect_ratio:
        image_config_kwargs["aspect_ratio"] = args.aspect_ratio
    image_config = types.ImageConfig(**image_config_kwargs)

    # Build thinking_config
    thinking_config = types.ThinkingConfig(thinking_level=args.thinking)

    # Build tools
    tools: list = []
    if args.image_search:
        tools.append({"google_search": {"search_types": {"web_search": {}, "image_search": {}}}})
    elif args.google_search:
        tools.append({"google_search": {}})

    # Build GenerateContentConfig
    config_kwargs: dict = {
        "response_modalities": build_modalities(args.modalities),
        "thinking_config": thinking_config,
    }
    if image_config:
        config_kwargs["image_config"] = image_config
    if tools:
        config_kwargs["tools"] = tools

    config = types.GenerateContentConfig(**config_kwargs)

    # Build contents
    if input_path:
        source_image = PILImage.open(input_path)
        contents = [args.prompt, source_image]
    else:
        contents = [args.prompt]

    # Call API
    try:
        response = client.models.generate_content(
            model=args.model,
            contents=contents,
            config=config,
        )
    except Exception as exc:
        die(f"Gemini API call failed: {exc}")

    # Process response parts
    output_path = resolve_output_path(args)
    saved_path: str | None = None
    text_parts: list[str] = []

    try:
        for part in response.parts:
            if getattr(part, "thought", False):
                continue  # skip thinking traces
            if part.inline_data is not None:
                img = part.as_image()
                output_path.parent.mkdir(parents=True, exist_ok=True)
                img.save(output_path)
                saved_path = str(output_path)
            elif part.text:
                text_parts.append(part.text)
    except Exception as exc:
        die(f"Failed to process response: {exc}")

    if saved_path is None:
        die(
            "No image was returned in the response. "
            "The model may have refused the prompt or returned text only. "
            f"Text response: {' '.join(text_parts)!r}"
        )

    # Build usage dict
    try:
        meta = response.usage_metadata
        usage = {
            "input_tokens": getattr(meta, "prompt_token_count", None),
            "output_tokens": getattr(meta, "candidates_token_count", None),
        }
    except AttributeError:
        usage = {"input_tokens": None, "output_tokens": None}

    result = {
        "path": saved_path,
        "text": " ".join(text_parts) if text_parts else None,
        "model": args.model,
        "usage": usage,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
