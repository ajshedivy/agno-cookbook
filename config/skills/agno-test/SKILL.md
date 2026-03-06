---
name: agno-test
description: |
  Test Agno agents using the AgentOSClient SDK. Covers connecting to
  AgentOS, running agents/teams/workflows, streaming, session management,
  memory operations, and knowledge search. Trigger this skill when:
  importing agno.client, using AgentOSClient, testing agents remotely,
  writing agent tests, or asking "how do I test an Agno agent?"
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["testing", "client", "agno", "agentos"]
---

# Test Agents with AgentOSClient

Use `agno.client.AgentOSClient` to interact with running AgentOS instances programmatically. Only requires `uv` — all dependencies are declared inline via PEP 723.

## Prerequisites

Start an AgentOS server first:

```bash
export ANTHROPIC_API_KEY=sk-...
uv run start_agentos.py  # See agno-agentos skill
```

## Connect and Discover

```python
import asyncio
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    # Discover available agents, teams, and workflows
    config = await client.aget_config()
    print(f"Agents: {[a.id for a in (config.agents or [])]}")
    print(f"Teams: {[t.id for t in (config.teams or [])]}")
    print(f"Workflows: {[w.id for w in (config.workflows or [])]}")

    # Get details about a specific agent
    if config.agents:
        agent = await client.aget_agent(config.agents[0].id)
        print(f"Name: {agent.name}, Tools: {len(agent.tools or [])}")

asyncio.run(main())
```

## Run Agents (Non-Streaming)

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
    )

    print(f"Run ID: {result.run_id}")
    print(f"Content: {result.content}")
    print(f"Tokens: {result.metrics.total_tokens if result.metrics else 'N/A'}")

asyncio.run(main())
```

## Run Agents (Streaming)

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
    ):
        if isinstance(event, RunContentEvent):
            print(event.content, end="", flush=True)
        elif isinstance(event, RunCompletedEvent):
            print(f"\nCompleted! Run ID: {event.run_id}")

asyncio.run(main())
```

## Run Teams

```python
import asyncio
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    config = await client.aget_config()
    team_id = config.teams[0].id

    # Non-streaming
    result = await client.run_team(
        team_id=team_id,
        message="Research and summarize quantum computing advances.",
    )
    print(result.content)

    # Streaming
    from agno.run.agent import RunContentEvent
    async for event in client.run_team_stream(
        team_id=team_id,
        message="Compare Python and Rust.",
    ):
        if isinstance(event, RunContentEvent):
            print(event.content, end="", flush=True)

asyncio.run(main())
```

## Run Workflows

```python
import asyncio
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    config = await client.aget_config()
    workflow_id = config.workflows[0].id

    result = await client.run_workflow(
        workflow_id=workflow_id,
        message="Analyze the latest AI trends.",
    )
    print(result.content)

asyncio.run(main())
```

## Session Management

Use `session_id` for persistent conversations:

```python
async def main():
    client = AgentOSClient(base_url="http://localhost:7777")
    config = await client.aget_config()
    agent_id = config.agents[0].id

    # First message
    result1 = await client.run_agent(
        agent_id=agent_id,
        message="My name is Alice.",
        session_id="session-123",
    )

    # Second message — agent remembers
    result2 = await client.run_agent(
        agent_id=agent_id,
        message="What's my name?",
        session_id="session-123",
    )
    print(result2.content)  # Should mention Alice
```

## Memory Operations

Create, list, update, and delete user memories:

```python
import asyncio
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")
    user_id = "test-user"

    # Create a memory
    memory = await client.create_memory(
        memory="User prefers dark mode",
        user_id=user_id,
        topics=["preferences", "ui"],
    )
    print(f"Created: {memory.memory_id}")

    # List memories
    memories = await client.list_memories(user_id=user_id)
    for mem in memories.data:
        print(f"  {mem.memory_id}: {mem.memory}")

    # Update a memory
    updated = await client.update_memory(
        memory_id=memory.memory_id,
        memory="User strongly prefers dark mode",
        user_id=user_id,
        topics=["preferences", "ui", "accessibility"],
    )

    # Delete a memory
    await client.delete_memory(memory.memory_id, user_id=user_id)

asyncio.run(main())
```

## Error Handling

```python
from agno.client import AgentOSClient

try:
    client = AgentOSClient(base_url="http://localhost:7777")
    config = await client.aget_config()
except Exception as e:
    print(f"Connection failed: {e}")
    # Common: RemoteServerUnavailableError if server isn't running
```

## Writing pytest Tests

```python
import asyncio
import pytest
from agno.client import AgentOSClient

@pytest.fixture
def client():
    return AgentOSClient(base_url="http://localhost:7777")

@pytest.mark.asyncio
async def test_agent_responds(client):
    config = await client.aget_config()
    assert len(config.agents) > 0

    result = await client.run_agent(
        agent_id=config.agents[0].id,
        message="What is 2 + 2?",
    )
    assert result.content is not None
    assert "4" in str(result.content)

@pytest.mark.asyncio
async def test_streaming_works(client):
    from agno.run.agent import RunContentEvent

    config = await client.aget_config()
    agent_id = config.agents[0].id

    chunks = []
    async for event in client.run_agent_stream(
        agent_id=agent_id,
        message="Say hello",
    ):
        if isinstance(event, RunContentEvent):
            chunks.append(event.content)

    full_response = "".join(chunks)
    assert len(full_response) > 0
```

## Event Types

| Event | Description |
|-------|-------------|
| `RunContentEvent` | Streamed content chunk. Access `event.content` |
| `RunCompletedEvent` | Run finished. Access `event.run_id` |

Import from: `from agno.run.agent import RunContentEvent, RunCompletedEvent`

## Anti-Patterns

- **Don't forget `await`** — all client methods are async
- **Don't skip `aget_config()`** — always discover available agents before running
- **Don't hardcode agent IDs** — discover them from config
- **Don't forget the server** — start AgentOS before running client code
- **Don't use blocking calls in async** — use `asyncio.run()` or `await`

## Further Reading

For advanced client patterns and full API reference, read `references/api-patterns.md`.
