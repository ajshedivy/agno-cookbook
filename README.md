# Agno Cookbook

Cookbook examples for [Agno](https://github.com/agno-agi/agno) with configurable model selection. Switch models via `.env` instead of editing code.

## Quick Start

```bash
# Clone and setup
git clone <repo-url> && cd agno-cookbook
cp .env.example .env

# Install dependencies + your provider SDK
uv sync --extra quickstart --extra anthropic

# Run an example
uv run python cookbook/00_quickstart/agent_with_tools.py
```

Edit `.env` with your API key and preferred model:

```bash
AGNO_MODEL=anthropic:claude-sonnet-4-20250514
ANTHROPIC_API_KEY=sk-ant-...
```

## Model Configuration

Set `AGNO_MODEL` in `.env` using the format `provider:model_id`. Agno supports 40+ providers.

**You must install the provider's SDK** via `uv sync --extra <provider>`:

| `AGNO_MODEL` | Install command | API key env var |
|---|---|---|
| `openai:gpt-4o` | `uv sync --extra openai` | `OPENAI_API_KEY` |
| `anthropic:claude-sonnet-4-20250514` | `uv sync --extra anthropic` | `ANTHROPIC_API_KEY` |
| `google:gemini-3-flash-preview` | `uv sync --extra google` | `GOOGLE_API_KEY` |
| `groq:llama-3.3-70b-versatile` | `uv sync --extra groq` | `GROQ_API_KEY` |
| `mistral:mistral-large-latest` | `uv sync --extra mistral` | `MISTRAL_API_KEY` |
| `cohere:command-r-plus` | `uv sync --extra cohere` | `COHERE_API_KEY` |
| `ollama:llama3.2` | `uv sync --extra ollama` | *(none — runs locally)* |

You can combine multiple extras:

```bash
uv sync --extra quickstart --extra anthropic   # Quickstart tools + Anthropic
uv sync --extra all-models                     # All major provider SDKs
```

## AgentOS

The `agentos-serve` package lets you spin up AgentOS from any Python file containing Agno agents, teams, or workflows.

### Install (editable mode, for development)

```bash
uv pip install -e agentos-serve
```

Or install it via the `serve` extra (non-editable, from PyPI):

```bash
uv sync --extra serve
```

### Usage

```bash
# Serve a single file
agentos-serve cookbook/02_agents/01_quickstart/basic_agent.py

# Serve all agents in a directory
agentos-serve cookbook/02_agents/01_quickstart/

# The cookbook also provides an `agentos` alias
uv run agentos cookbook/02_agents/01_quickstart/
```

See [`agentos-serve/README.md`](agentos-serve/README.md) for full CLI options and extras.

## Directory Structure

```
cookbook/
  00_quickstart/     # Start here
  01_demo/           # Full demo app
  02_agents/         # Agent patterns
  03_teams/          # Multi-agent teams
  04_workflows/      # Workflow orchestration
  05_agent_os/       # Agent OS examples
  06_storage/        # Persistence
  07_knowledge/      # Knowledge bases & embedders
  08_learning/       # Self-learning agents
  09_evals/          # Evaluation patterns
  10_reasoning/      # Reasoning strategies
  11_memory/         # Memory management
  90_models/         # Provider-specific demos (hardcoded models)
  91_tools/          # Tool integrations
  92_integrations/   # Third-party integrations
  93_components/     # UI components
```

> **Note:** `cookbook/90_models/` contains provider-specific examples with hardcoded model classes. These are intentionally not configurable — they demonstrate provider-specific features.
