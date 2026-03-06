---
name: agno-models
description: |
  Configure model providers for Agno agents. Covers Anthropic, OpenAI,
  Google, Groq, Ollama, AWS Bedrock, Azure, and 40+ other providers.
  Trigger this skill when: switching model providers, configuring model
  parameters, using model strings, or asking "how do I use a different
  model with Agno?"
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["models", "providers", "anthropic", "openai", "ollama", "agno"]
---

# Configure Agno Model Providers

Agno supports 40+ model providers. Swap models with a single line change. Install with `pip install agno`.

## Model Strings (Simplest)

Pass a `provider:model_id` string directly:

```python
from agno.agent import Agent

# OpenAI
agent = Agent(model="openai:gpt-4o")

# Anthropic
agent = Agent(model="anthropic:claude-sonnet-4-5")

# Google
agent = Agent(model="google:gemini-2.0-flash")

# Groq
agent = Agent(model="groq:llama-3.3-70b-versatile")

# Ollama (local)
agent = Agent(model="ollama:llama3.3")

# DeepSeek
agent = Agent(model="deepseek:deepseek-chat")
```

## Model Class Imports

For more control, import model classes directly:

```python
# Anthropic
from agno.models.anthropic import Claude
model = Claude(id="claude-sonnet-4-5")

# OpenAI Chat
from agno.models.openai import OpenAIChat
model = OpenAIChat(id="gpt-4o")

# OpenAI Responses API
from agno.models.openai import OpenAIResponses
model = OpenAIResponses(id="gpt-4o")

# Google Gemini
from agno.models.google import Gemini
model = Gemini(id="gemini-2.0-flash")

# Groq
from agno.models.groq import Groq
model = Groq(id="llama-3.3-70b-versatile")

# Ollama
from agno.models.ollama import Ollama
model = Ollama(id="llama3.3")

# AWS Bedrock
from agno.models.aws import AwsBedrock
model = AwsBedrock(id="anthropic.claude-sonnet-4-5-v1")

# Azure OpenAI
from agno.models.azure import AzureOpenAI
model = AzureOpenAI(
    id="gpt-4o",
    azure_endpoint="https://myendpoint.openai.azure.com/",
    azure_deployment="my-deployment",
)

# Mistral
from agno.models.mistral import MistralChat
model = MistralChat(id="mistral-large-latest")

# xAI
from agno.models.xai import xAI
model = xAI(id="grok-2")

# Cohere
from agno.models.cohere import CohereChat
model = CohereChat(id="command-r-plus")

# Together
from agno.models.together import Together
model = Together(id="meta-llama/Llama-3.3-70B-Instruct-Turbo")

# Fireworks
from agno.models.fireworks import Fireworks
model = Fireworks(id="accounts/fireworks/models/llama-v3p3-70b-instruct")
```

## Model Parameters

Common parameters available on all model classes:

```python
from agno.models.openai import OpenAIChat

model = OpenAIChat(
    id="gpt-4o",
    temperature=0.7,           # Creativity (0.0 = deterministic, 1.0 = creative)
    max_tokens=4096,           # Maximum output tokens
    top_p=0.9,                 # Nucleus sampling
    stop=["END"],              # Stop sequences
)
```

## Environment Variables

Each provider reads its API key from a standard environment variable:

```bash
# Anthropic
export ANTHROPIC_API_KEY=sk-ant-...

# OpenAI
export OPENAI_API_KEY=sk-...

# Google
export GOOGLE_API_KEY=...

# Groq
export GROQ_API_KEY=gsk_...

# Mistral
export MISTRAL_API_KEY=...

# Together
export TOGETHER_API_KEY=...

# Fireworks
export FIREWORKS_API_KEY=...

# xAI
export XAI_API_KEY=...
```

## Provider Extras

Install the provider-specific extra:

```bash
pip install "agno[anthropic]"     # Claude
pip install "agno[openai]"        # GPT-4o
pip install "agno[google]"        # Gemini
pip install "agno[groq]"          # Groq
pip install "agno[ollama]"        # Ollama (local)
pip install "agno[aws-bedrock]"   # AWS Bedrock
pip install "agno[azure]"         # Azure OpenAI
pip install "agno[mistral]"       # Mistral
pip install "agno[cohere]"        # Cohere
pip install "agno[together]"      # Together
pip install "agno[fireworks]"     # Fireworks
```

## Using get_model

Parse model strings programmatically:

```python
from agno.models.utils import get_model

model = get_model("openai:gpt-4o")
model = get_model("anthropic:claude-sonnet-4-5")
model = get_model("ollama:llama3.3")
```

## Configurable Model Pattern

Make models configurable via environment variables:

```python
import os
from agno.agent import Agent

model_string = os.environ.get("AGNO_MODEL", "openai:gpt-4o")

agent = Agent(
    model=model_string,
    markdown=True,
)
```

## Comparing Models

Use the same agent definition with different models:

```python
from agno.agent import Agent

models = [
    "openai:gpt-4o",
    "anthropic:claude-sonnet-4-5",
    "google:gemini-2.0-flash",
]

for model_id in models:
    agent = Agent(model=model_id, markdown=True)
    response = agent.run("What is 2 + 2?")
    print(f"{model_id}: {response.content}")
```

## Anti-Patterns

- **Don't hardcode model IDs** — use environment variables or config for flexibility
- **Don't forget provider extras** — `pip install agno` alone doesn't include any provider
- **Don't use `OpenAIChat` for reasoning models** — use `OpenAIResponses` for o3/o4-mini
- **Don't assume all models support tools** — check provider docs for tool calling support
- **Don't mix model string and class** — use one approach consistently
- **Don't forget API keys** — each provider needs its own environment variable

## Further Reading

For the full provider list and advanced model configuration, read `references/api-patterns.md`.
