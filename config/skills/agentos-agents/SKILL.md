---
name: agentos-agents
description: |
  Interact with AgentOS Agent API endpoints using the AgentOSClient SDK.
  Covers listing agents, getting agent details, running agents (streaming
  and non-streaming), cancelling runs, and continuing runs. Trigger this
  skill when: running agents via the API, using run_agent or
  run_agent_stream, discovering available agents, or asking "how do I
  run an agent through the API?"
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["agentos", "agents", "api", "client", "agno"]
---

# AgentOS Agents API

Use `agno.client.AgentOSClient` to list, inspect, and run agents on a remote AgentOS instance. Install with `pip install agno`.

## Prerequisites

Start an AgentOS server first:

```bash
pip install "agno[os,anthropic]"
export ANTHROPIC_API_KEY=sk-...
python start_agentos.py  # See agno-agentos skill
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/agents` | List all agents |
| GET | `/agents/{agent_id}` | Get agent details |
| POST | `/agents/{agent_id}/runs` | Create agent run |
| POST | `/agents/{agent_id}/cancel_run` | Cancel agent run |
| POST | `/agents/{agent_id}/continue_run` | Continue agent run (resume with tool results) |

## List All Agents

```python
import asyncio
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    config = await client.aget_config()
    for agent in config.agents or []:
        print(f"Agent: {agent.id} — {agent.name}")

asyncio.run(main())
```

## Get Agent Details

```python
async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    agent = await client.aget_agent("my-agent-id")
    print(f"Name: {agent.name}")
    print(f"Model: {agent.model}")
    print(f"Tools: {len(agent.tools or [])}")
    print(f"Knowledge: {agent.knowledge}")
    print(f"Memory: {agent.memory}")
```

## Run Agent (Non-Streaming)

```python
import asyncio
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    config = await client.aget_config()
    agent_id = config.agents[0].id

    result = await client.run_agent(
        agent_id=agent_id,
        message="What is 2 + 2?",
        user_id="user-123",          # Optional: for user-specific memory
        session_id="session-456",    # Optional: for persistent conversations
    )

    print(f"Run ID: {result.run_id}")
    print(f"Content: {result.content}")
    print(f"Tokens: {result.metrics.total_tokens if result.metrics else 'N/A'}")

asyncio.run(main())
```

## Run Agent (Streaming)

```python
import asyncio
from agno.client import AgentOSClient
from agno.run.agent import RunContentEvent, RunCompletedEvent

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    config = await client.aget_config()
    agent_id = config.agents[0].id

    async for event in client.run_agent_stream(
        agent_id=agent_id,
        message="Tell me a short joke.",
        user_id="user-123",
        session_id="session-456",
    ):
        if isinstance(event, RunContentEvent):
            print(event.content, end="", flush=True)
        elif isinstance(event, RunCompletedEvent):
            print(f"\nDone! Run ID: {event.run_id}")

asyncio.run(main())
```

## Run Agent with Dependencies

Pass runtime parameters to agent tools via `dependencies`:

```python
result = await client.run_agent(
    agent_id=agent_id,
    message="What is my name?",
    dependencies={"robot_name": "Anna"},
)
```

## Run Agent with Structured Output

Pass a JSON schema to enforce structured responses:

```python
import json

output_schema = {
    "type": "object",
    "properties": {
        "answer": {"type": "string"},
        "confidence": {"type": "number"},
    },
    "required": ["answer", "confidence"],
}

result = await client.run_agent(
    agent_id=agent_id,
    message="What is the capital of France?",
    output_schema=json.dumps(output_schema),
)
```

## Cancel Agent Run

```python
# Cancel a running agent execution
await client.cancel_agent_run(agent_id=agent_id)
```

## Continue Agent Run

Resume a paused execution (e.g., after human-in-the-loop tool approval):

```python
await client.continue_agent_run(agent_id=agent_id)
```

## Authentication

When the AgentOS instance has a security key configured:

```python
client = AgentOSClient(base_url="http://localhost:7777")

result = await client.run_agent(
    agent_id=agent_id,
    message="Hello",
    headers={"Authorization": "Bearer your-jwt-token"},
)
```

## Error Handling

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

- **Don't forget `await`** — all client methods are async
- **Don't hardcode agent IDs** — discover them from `aget_config()`
- **Don't skip discovery** — always call `aget_config()` first to verify agents exist
- **Don't forget the server** — start AgentOS before running client code
- **Don't ignore streaming events** — always handle both `RunContentEvent` and `RunCompletedEvent`

## Further Reading

For advanced agent API patterns, read `references/api-patterns.md`.
