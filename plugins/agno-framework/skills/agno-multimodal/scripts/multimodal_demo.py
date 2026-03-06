# /// script
# requires-python = ">=3.11"
# dependencies = ["agno[openai]"]
# ///
"""
Multimodal Demo
================
Self-contained demo of multimodal agents — image analysis and structured
extraction from images.

Usage:
    export OPENAI_API_KEY=sk-...
    uv run multimodal_demo.py
    uv run multimodal_demo.py --model "anthropic:claude-sonnet-4-5"
    uv run multimodal_demo.py --image "path/to/image.png"
"""

import argparse
from typing import Optional

from pydantic import BaseModel, Field

from agno.agent import Agent
from agno.media import Image

# ---------------------------------------------------------------------------
# Structured output schema for image analysis
# ---------------------------------------------------------------------------
class ImageAnalysis(BaseModel):
    description: str = Field(..., description="Detailed description of the image")
    objects: list[str] = Field(..., description="List of objects detected")
    dominant_colors: list[str] = Field(..., description="Dominant colors in the image")
    mood: str = Field(..., description="Overall mood or atmosphere")


# ---------------------------------------------------------------------------
# Demo URLs (public domain images)
# ---------------------------------------------------------------------------
DEMO_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Camponotus_flavomarginatus_ant.jpg/1200px-Camponotus_flavomarginatus_ant.jpg",
]


def main():
    parser = argparse.ArgumentParser(description="Multimodal demo")
    parser.add_argument(
        "--model",
        default="openai:gpt-4o",
        help="Model string, e.g. 'openai:gpt-4o' or 'anthropic:claude-sonnet-4-5'",
    )
    parser.add_argument(
        "--image",
        default=None,
        help="Path to a local image file (uses demo URLs if not provided)",
    )
    args = parser.parse_args()

    # --- Demo 1: Basic image description ---
    print("=== Demo 1: Image Description ===\n")

    agent = Agent(
        name="Vision Agent",
        model=args.model,
        instructions=["Describe images in detail. Be specific about what you see."],
        markdown=True,
    )

    if args.image:
        images = [Image(filepath=args.image)]
    else:
        images = [Image(url=DEMO_IMAGES[0])]

    agent.print_response(
        "What do you see in this image?",
        images=images,
        stream=True,
    )

    # --- Demo 2: Structured extraction ---
    print("\n\n=== Demo 2: Structured Extraction ===\n")

    structured_agent = Agent(
        name="Structured Vision Agent",
        model=args.model,
        output_schema=ImageAnalysis,
    )

    if args.image:
        images = [Image(filepath=args.image)]
    else:
        images = [Image(url=DEMO_IMAGES[0])]

    response = structured_agent.run(
        "Analyze this image.",
        images=images,
    )

    analysis: ImageAnalysis = response.content
    print(f"Description: {analysis.description}")
    print(f"Objects: {', '.join(analysis.objects)}")
    print(f"Colors: {', '.join(analysis.dominant_colors)}")
    print(f"Mood: {analysis.mood}")

    # --- Demo 3: Multi-image comparison ---
    if not args.image:
        print("\n\n=== Demo 3: Multi-Image Comparison ===\n")

        agent.print_response(
            "Compare these two images. What are the key differences?",
            images=[Image(url=url) for url in DEMO_IMAGES],
            stream=True,
        )


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
