---
name: agentos-api-agents
description: |
  Interact with AgentOS Agent API endpoints. For standard operations
  (listing agents, running agents, streaming), use the provided CLI
  script first. Only write custom Python when the script cannot handle
  the use case (e.g., structured output, dependencies, cancellation,
  chaining multiple calls). Trigger when: running agents remotely,
  listing agents, creating agent tests, or asking things like "kick off
  a run in my test agent" or "what agents do I have configured?"
license: Apache-2.0
metadata:
  version: "1.1.1"
  author: agno-team
  tags: ["agentos", "agents", "api", "client", "agno"]
---

# AgentOS Agents API

## Prerequisites

Start an AgentOS server first:

```bash
export ANTHROPIC_API_KEY=sk-...
uv run start_agentos.py  # See agno-agentos skill
```

## Default: Use the CLI Script

**Always try the provided script first.** It covers listing agents, running
agents (streaming and non-streaming), session persistence, and dependencies —
all from the command line with no custom code needed.

The script is at: `scripts/run_agents.py`

### List all agents

```bash
uv run scripts/run_agents.py --base-url http://localhost:8000
```

### Show full AgentOS config

```bash
uv run scripts/run_agents.py --base-url http://localhost:8000 --config
```

### Show agent-specific config (tools, model, knowledge, memory)

```bash
uv run scripts/run_agents.py --base-url http://localhost:8000 --config --agent-id my-agent
```

### Run an agent with a message

```bash
uv run scripts/run_agents.py --base-url http://localhost:8000 \
  --agent-id my-agent \
  -m "What is 2 + 2?"
```

### Stream a response

```bash
uv run scripts/run_agents.py --base-url http://localhost:8000 \
  --agent-id my-agent \
  -m "Tell me a joke" --stream
```

### Persistent sessions

```bash
uv run scripts/run_agents.py --base-url http://localhost:8000 \
  --agent-id my-agent \
  -m "My name is Alice" --session-id chat-1 --user-id alice

uv run scripts/run_agents.py --base-url http://localhost:8000 \
  --agent-id my-agent \
  -m "What is my name?" --session-id chat-1 --user-id alice
```

### Pass dependencies to agent tools

```bash
uv run scripts/run_agents.py --base-url http://localhost:8000 \
  --agent-id my-agent \
  -m "Greet me" --dependencies '{"robot_name": "Anna"}'
```

### Full CLI reference

```
uv run scripts/run_agents.py --help
```

## When to Write Custom Python

Only write ad-hoc Python when the CLI script cannot handle your use case:

- **Structured output** (passing a JSON schema)
- **Cancel or continue** a running agent
- **Chaining multiple agent calls** in a single script
- **Custom error handling** or retry logic
- **Programmatic inspection** of agent config beyond what `--config` shows
- **Integration tests** that assert on response content

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/agents` | List all agents |
| GET | `/agents/{agent_id}` | Get agent details |
| POST | `/agents/{agent_id}/runs` | Create agent run |
| POST | `/agents/{agent_id}/cancel_run` | Cancel agent run |
| POST | `/agents/{agent_id}/continue_run` | Continue agent run (resume with tool results) |

## Custom Python Examples

### Get Agent Details

```python
import asyncio
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    agent = await client.aget_agent("my-agent-id")
    print(f"Name: {agent.name}")
    print(f"Model: {agent.model}")
    print(f"Tools: {len(agent.tools or [])}")
    print(f"Knowledge: {agent.knowledge}")
    print(f"Memory: {agent.memory}")

asyncio.run(main())
```

### Run Agent with Structured Output

```python
import asyncio, json
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    output_schema = {
        "type": "object",
        "properties": {
            "answer": {"type": "string"},
            "confidence": {"type": "number"},
        },
        "required": ["answer", "confidence"],
    }

    result = await client.run_agent(
        agent_id="my-agent",
        message="What is the capital of France?",
        output_schema=json.dumps(output_schema),
    )
    print(result.content)

asyncio.run(main())
```

### Cancel Agent Run

```python
await client.cancel_agent_run(agent_id=agent_id)
```

### Continue Agent Run

Resume a paused execution (e.g., after human-in-the-loop tool approval):

```python
await client.continue_agent_run(agent_id=agent_id)
```

### Authentication

When the AgentOS instance has a security key configured:

```python
result = await client.run_agent(
    agent_id=agent_id,
    message="Hello",
    headers={"Authorization": "Bearer your-jwt-token"},
)
```

### Error Handling

```python
from agno.client import AgentOSClient, RemoteServerUnavailableError

try:
    client = AgentOSClient(base_url="http://localhost:7777")
    config = await client.aget_config()
except RemoteServerUnavailableError as e:
    print(f"Server unavailable: {e.message}")
    print(f"URL: {e.base_url}")
```

## Anti-Patterns

- **Don't write custom Python for basic list/run operations** — use the CLI script
- **Don't forget `await`** — all client methods are async
- **Don't hardcode agent IDs** — discover them from `aget_config()` or the CLI script
- **Don't skip discovery** — always call `aget_config()` first to verify agents exist
- **Don't forget the server** — start AgentOS before running client code
- **Don't ignore streaming events** — always handle both `RunContentEvent` and `RunCompletedEvent`

## Further Reading

For advanced agent API patterns, read `references/api-patterns.md`.
