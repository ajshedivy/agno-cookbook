# Models API Patterns

## Model String Format

```
provider:model_id
```

Examples: `openai:gpt-4o`, `anthropic:claude-sonnet-4-5`, `ollama:llama3.3`

## Full Provider List

| Provider | String Prefix | Class Import | Extras |
|----------|--------------|--------------|--------|
| OpenAI | `openai:` | `agno.models.openai.OpenAIChat` | `agno[openai]` |
| OpenAI Responses | `openai_responses:` | `agno.models.openai.OpenAIResponses` | `agno[openai]` |
| Anthropic | `anthropic:` | `agno.models.anthropic.Claude` | `agno[anthropic]` |
| Google | `google:` | `agno.models.google.Gemini` | `agno[google]` |
| Groq | `groq:` | `agno.models.groq.Groq` | `agno[groq]` |
| Ollama | `ollama:` | `agno.models.ollama.Ollama` | `agno[ollama]` |
| AWS Bedrock | `aws:` | `agno.models.aws.AwsBedrock` | `agno[aws-bedrock]` |
| Azure | `azure:` | `agno.models.azure.AzureOpenAI` | `agno[azure]` |
| Mistral | `mistral:` | `agno.models.mistral.MistralChat` | `agno[mistral]` |
| Cohere | `cohere:` | `agno.models.cohere.CohereChat` | `agno[cohere]` |
| xAI | `xai:` | `agno.models.xai.xAI` | `agno[xai]` |
| DeepSeek | `deepseek:` | `agno.models.deepseek.DeepSeek` | `agno[deepseek]` |
| Together | `together:` | `agno.models.together.Together` | `agno[together]` |
| Fireworks | `fireworks:` | `agno.models.fireworks.Fireworks` | `agno[fireworks]` |
| Cerebras | `cerebras:` | `agno.models.cerebras.Cerebras` | `agno[cerebras]` |
| LiteLLM | `litellm:` | `agno.models.litellm.LiteLLM` | `agno[litellm]` |

## Common Model Parameters

```python
from agno.models.openai import OpenAIChat

model = OpenAIChat(
    id="gpt-4o",
    temperature=0.7,        # 0.0-2.0, creativity
    max_tokens=4096,         # Max output tokens
    top_p=0.9,               # Nucleus sampling
    stop=["END"],            # Stop sequences
    seed=42,                 # Reproducibility
)
```

## get_model Utility

```python
from agno.models.utils import get_model

# Parse model strings programmatically
model = get_model("openai:gpt-4o")
model = get_model("anthropic:claude-sonnet-4-5")

# Pass existing model objects through
from agno.models.openai import OpenAIChat
model = get_model(OpenAIChat(id="gpt-4o"))  # Returns as-is

# None returns None
model = get_model(None)  # Returns None
```

## Environment Variables

| Provider | Variable |
|----------|----------|
| OpenAI | `OPENAI_API_KEY` |
| Anthropic | `ANTHROPIC_API_KEY` |
| Google | `GOOGLE_API_KEY` |
| Groq | `GROQ_API_KEY` |
| Mistral | `MISTRAL_API_KEY` |
| Cohere | `COHERE_API_KEY` |
| xAI | `XAI_API_KEY` |
| Together | `TOGETHER_API_KEY` |
| Fireworks | `FIREWORKS_API_KEY` |

## Configurable Model Pattern

```python
import os
from agno.agent import Agent

# Read from environment, default to OpenAI
model = os.environ.get("AGNO_MODEL", "openai:gpt-4o")
agent = Agent(model=model)
```

## Azure OpenAI Configuration

```python
from agno.models.azure import AzureOpenAI

model = AzureOpenAI(
    id="gpt-4o",
    azure_endpoint="https://myendpoint.openai.azure.com/",
    azure_deployment="my-deployment",
    api_version="2024-02-15-preview",
)
```

## AWS Bedrock Configuration

```python
from agno.models.aws import AwsBedrock

model = AwsBedrock(
    id="anthropic.claude-sonnet-4-5-v1",
    region="us-east-1",
)
```
