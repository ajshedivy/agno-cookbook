# Multimodal API Patterns

## Media Types

```python
from agno.media import Image, Audio, Video
```

## Image Input

```python
# From URL
Image(url="https://example.com/photo.jpg")

# From local file
Image(filepath="path/to/image.png")

# From bytes
Image(content=raw_bytes, media_type="image/png")
```

## Audio Input

```python
# From local file
Audio(filepath="path/to/audio.mp3")

# From URL
Audio(url="https://example.com/audio.wav")
```

## Video Input

```python
# From local file
Video(filepath="path/to/video.mp4")

# From URL
Video(url="https://example.com/video.mp4")
```

## Passing Media to Agents

```python
agent.print_response(
    "Describe this",
    images=[Image(...)],           # 0 or more images
    audio=[Audio(...)],            # 0 or more audio files
    videos=[Video(...)],           # 0 or more videos
    stream=True,
)
```

## Audio Output Configuration

```python
from agno.models.openai import OpenAIChat

model = OpenAIChat(
    id="gpt-4o-audio-preview",
    modalities=["text", "audio"],
    audio={"voice": "alloy", "format": "wav"},
)

agent = Agent(model=model)
response = agent.run("Tell me a story.")

if response.audio:
    with open("output.wav", "wb") as f:
        f.write(response.audio)
```

## Model Capabilities Matrix

| Model | Images | Audio In | Audio Out | Video |
|-------|--------|----------|-----------|-------|
| GPT-4o | Yes | No | No | No |
| GPT-4o-audio-preview | Yes | Yes | Yes | No |
| Claude Sonnet/Opus | Yes | No | No | No |
| Gemini 2.0 Flash | Yes | Yes | No | Yes |
| Gemini 2.0 Pro | Yes | Yes | No | Yes |

## Structured Extraction from Images

```python
from pydantic import BaseModel

class ExtractedData(BaseModel):
    text: str
    objects: list[str]

agent = Agent(
    model="openai:gpt-4o",
    output_schema=ExtractedData,
)

response = agent.run(
    "Extract data from this image.",
    images=[Image(filepath="document.png")],
)
data: ExtractedData = response.content
```

## Multi-Image Comparison

```python
agent.print_response(
    "Compare these images and list the differences.",
    images=[
        Image(filepath="before.png"),
        Image(filepath="after.png"),
    ],
    stream=True,
)
```
