---
name: agentos-workflows
description: |
  Interact with AgentOS Workflow API endpoints using the AgentOSClient SDK.
  Covers listing workflows, running workflows (streaming and non-streaming),
  and handling workflow events. Trigger this skill when: running workflows
  via the API, using run_workflow or run_workflow_stream, discovering
  available workflows, or asking "how do I run a workflow through the API?"
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["agentos", "workflows", "api", "client", "agno"]
---

# AgentOS Workflows API

Use `agno.client.AgentOSClient` to list and run workflows on a remote AgentOS instance. Install with `pip install agno`.

## Prerequisites

Start an AgentOS server with workflows configured:

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.db.sqlite import SqliteDb
from agno.workflow.step import Step
from agno.workflow.workflow import Workflow
from agno.os import AgentOS

db = SqliteDb(db_file="tmp/app.db")
assistant = Agent(name="Assistant", model=Claude(id="claude-sonnet-4-5"), db=db)

workflow = Workflow(
    name="QA Workflow",
    description="Simple Q&A workflow",
    db=db,
    steps=[Step(name="Answer", agent=assistant)],
)

agent_os = AgentOS(agents=[assistant], workflows=[workflow])
agent_os.serve()
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/workflows` | List all workflows |
| GET | `/workflows/{workflow_id}` | Get workflow details |
| POST | `/workflows/{workflow_id}/runs` | Create workflow run |

## List All Workflows

```python
import asyncio
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    config = await client.aget_config()
    for wf in config.workflows or []:
        print(f"Workflow: {wf.id} — {wf.name}")

asyncio.run(main())
```

## Run Workflow (Non-Streaming)

```python
import asyncio
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    config = await client.aget_config()
    if not config.workflows:
        print("No workflows available")
        return

    workflow_id = config.workflows[0].id

    result = await client.run_workflow(
        workflow_id=workflow_id,
        message="What are the benefits of using Python for data science?",
    )

    print(f"Run ID: {result.run_id}")
    print(f"Content: {result.content}")

asyncio.run(main())
```

## Run Workflow (Streaming)

Workflow streaming returns `WorkflowRunOutputEvent` objects with different event types:

```python
import asyncio
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    config = await client.aget_config()
    workflow_id = config.workflows[0].id

    async for event in client.run_workflow_stream(
        workflow_id=workflow_id,
        message="Explain machine learning in simple terms.",
    ):
        # Handle content from agent events
        if event.event == "RunContent" and hasattr(event, "content"):
            print(event.content, end="", flush=True)
        # Handle workflow step completion
        elif event.event == "WorkflowAgentCompleted" and hasattr(event, "content") and event.content:
            print(event.content, end="", flush=True)

    print()

asyncio.run(main())
```

## Workflow Event Types

| Event | Description |
|-------|-------------|
| `RunContent` | Streamed content chunk from an agent step |
| `WorkflowAgentCompleted` | An agent step within the workflow completed |

## Error Handling

```python
try:
    result = await client.run_workflow(
        workflow_id=workflow_id,
        message="Process this request.",
    )
    print(result.content)
except Exception as e:
    print(f"Error: {e}")
    if hasattr(e, "response"):
        print(f"Response: {e.response.text}")
```

## Authentication

```python
result = await client.run_workflow(
    workflow_id=workflow_id,
    message="Run workflow",
    headers={"Authorization": "Bearer your-jwt-token"},
)
```

## Anti-Patterns

- **Don't forget `await`** — all client methods are async
- **Don't hardcode workflow IDs** — discover them from `aget_config()`
- **Don't confuse event types** — workflow streaming uses `event.event` string checks, not `isinstance()`
- **Don't ignore error responses** — workflows can fail at individual steps; check for errors

## Further Reading

For advanced workflow API patterns, read `references/api-patterns.md`.
