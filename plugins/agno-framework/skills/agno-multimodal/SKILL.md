---
name: agno-multimodal
description: |
  Build multimodal Agno agents that handle images, audio, and video.
  Covers image analysis, audio input/output, video captions, and file
  processing. Trigger this skill when: processing images with agents,
  handling audio or video, using vision capabilities, or asking "how
  do I build a multimodal agent?"
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["multimodal", "images", "audio", "video", "vision", "agno"]
---

# Build Multimodal Agno Agents

Agno agents can process images, audio, and video using model vision and multimodal capabilities. Install with `pip install agno`.

## Image Analysis

### From URLs

```python
from agno.agent import Agent
from agno.media import Image

agent = Agent(
    model="openai:gpt-4o",
    markdown=True,
)

agent.print_response(
    "What's in this image?",
    images=[Image(url="https://example.com/photo.jpg")],
    stream=True,
)
```

### From Local Files

```python
from agno.agent import Agent
from agno.media import Image

agent = Agent(
    model="openai:gpt-4o",
    markdown=True,
)

agent.print_response(
    "Describe this image in detail.",
    images=[Image(filepath="path/to/image.png")],
    stream=True,
)
```

### Multiple Images

```python
agent.print_response(
    "Compare these two images.",
    images=[
        Image(url="https://example.com/before.jpg"),
        Image(url="https://example.com/after.jpg"),
    ],
    stream=True,
)
```

## Audio Input

```python
from agno.agent import Agent
from agno.media import Audio

agent = Agent(
    model="openai:gpt-4o-audio-preview",
    markdown=True,
)

agent.print_response(
    "Transcribe and summarize this audio.",
    audio=[Audio(filepath="path/to/recording.mp3")],
    stream=True,
)
```

## Audio Output

Generate spoken responses:

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(
    model=OpenAIChat(
        id="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"},
    ),
)

response = agent.run("Tell me a short story about a robot.")

# Save audio output
if response.audio:
    with open("output.wav", "wb") as f:
        f.write(response.audio)
```

## Video Analysis

```python
from agno.agent import Agent
from agno.media import Video

agent = Agent(
    model="google:gemini-2.0-flash",
    markdown=True,
)

agent.print_response(
    "Describe what happens in this video.",
    videos=[Video(filepath="path/to/video.mp4")],
    stream=True,
)
```

## Image with Tools

Combine vision with tools for richer analysis:

```python
from agno.agent import Agent
from agno.media import Image
from agno.tools.websearch import WebSearchTools

agent = Agent(
    model="openai:gpt-4o",
    tools=[WebSearchTools()],
    instructions=["Identify objects in images and search for more info."],
    markdown=True,
)

agent.print_response(
    "What landmark is this? Give me historical facts.",
    images=[Image(filepath="landmark.jpg")],
    stream=True,
)
```

## Multimodal Agent with Structured Output

Extract structured data from images:

```python
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.media import Image

class ReceiptData(BaseModel):
    store_name: str = Field(..., description="Name of the store")
    total: float = Field(..., description="Total amount")
    items: list[str] = Field(..., description="List of items purchased")

agent = Agent(
    model="openai:gpt-4o",
    output_schema=ReceiptData,
)

response = agent.run(
    "Extract the receipt data.",
    images=[Image(filepath="receipt.jpg")],
)

receipt: ReceiptData = response.content
print(f"Store: {receipt.store_name}, Total: ${receipt.total:.2f}")
```

## Model Support for Multimodal

| Capability | Models |
|------------|--------|
| Image input | GPT-4o, Claude Sonnet/Opus, Gemini |
| Audio input | GPT-4o-audio-preview |
| Audio output | GPT-4o-audio-preview |
| Video input | Gemini 2.0 Flash |

## Anti-Patterns

- **Don't send huge images** — resize before sending to save tokens and latency
- **Don't use vision models for text-only tasks** — they cost more per token
- **Don't forget model compatibility** — not all models support all modalities
- **Don't mix audio and vision in one call** unless the model supports it
- **Don't skip `filepath=` for local files** — use `url=` only for remote resources

## Further Reading

For advanced multimodal patterns and provider-specific options, read `references/api-patterns.md`.
