---
name: agentos-api-workflows
description: |
  Interact with AgentOS Workflow API endpoints. For standard operations
  (listing workflows, running workflows, streaming), use the provided CLI
  script first. Only write custom Python when the script cannot handle
  the use case (e.g., custom event handling, chaining multiple workflow
  calls, error handling with retries). Trigger when: running workflows
  remotely, listing workflows, creating workflow tests, or asking things
  like "what workflows do I have?" or "run my content pipeline workflow."
license: Apache-2.0
metadata:
  version: "1.1.0"
  author: agno-team
  tags: ["agentos", "workflows", "api", "client", "agno"]
---

# AgentOS Workflows API

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

## Default: Use the CLI Script

**Always try the provided script first.** It covers listing workflows, running
workflows (streaming and non-streaming), and auto-selecting the first workflow —
all from the command line with no custom code needed.

The script is at: `scripts/run_workflows.py`

### List all workflows

```bash
uv run scripts/run_workflows.py --base-url http://localhost:7777
```

### Run a specific workflow

```bash
uv run scripts/run_workflows.py --base-url http://localhost:7777 \
  --workflow-id qa-workflow \
  -m "Explain machine learning"
```

### Stream a workflow response

```bash
uv run scripts/run_workflows.py --base-url http://localhost:7777 \
  -m "Analyze AI trends" --stream
```

### Run against a remote server

```bash
uv run scripts/run_workflows.py --base-url http://my-server:8000 \
  -m "Process this request"
```

### Full CLI reference

```
uv run scripts/run_workflows.py --help
```

## When to Write Custom Python

Only write ad-hoc Python when the CLI script cannot handle your use case:

- **Custom event handling** beyond printing content (e.g., aggregating step results)
- **Chaining multiple workflow calls** in a single script
- **Custom error handling** or retry logic
- **Authentication** with custom headers
- **Programmatic inspection** of workflow config (steps, agents)
- **Integration tests** that assert on response content

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/workflows` | List all workflows |
| GET | `/workflows/{workflow_id}` | Get workflow details |
| POST | `/workflows/{workflow_id}/runs` | Create workflow run |

## Workflow Event Types

| Event | Description |
|-------|-------------|
| `RunContent` | Streamed content chunk from an agent step |
| `WorkflowAgentCompleted` | An agent step within the workflow completed |

## Custom Python Examples

### Error Handling

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

### Authentication

When the AgentOS instance has a security key configured:

```python
result = await client.run_workflow(
    workflow_id=workflow_id,
    message="Run workflow",
    headers={"Authorization": "Bearer your-jwt-token"},
)
```

## Anti-Patterns

- **Don't write custom Python for basic operations** — use the CLI script
- **Don't forget `await`** — all client methods are async
- **Don't hardcode workflow IDs** — discover them from `aget_config()` or the CLI script
- **Don't confuse event types** — workflow streaming uses `event.event` string checks, not `isinstance()`
- **Don't ignore error responses** — workflows can fail at individual steps; check for errors

## Further Reading

For advanced workflow API patterns, read `references/api-patterns.md`.
