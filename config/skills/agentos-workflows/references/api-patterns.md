# AgentOS Workflows API Reference

## Complete Workflow Endpoints

### GET /workflows
List all configured workflows.

**Response:** Array of `WorkflowSummaryResponse` objects:
- `id`, `name`, `description`, `db_id`
- `is_component`, `current_version`, `stage`

### GET /workflows/{workflow_id}
Get detailed workflow configuration.

### POST /workflows/{workflow_id}/runs
Create a new workflow run.

**Content-Type:** `application/x-www-form-urlencoded`

**Form Parameters:**
- `message` (string): The input prompt
- `stream` (boolean): Enable streaming (SSE)
- `user_id` (string): User identifier
- `session_id` (string): Session identifier

**Non-Streaming Response:** Run result with `run_id`, `content`.

**Streaming Response (SSE):** Stream of `WorkflowRunOutputEvent` objects.

## Workflow Event Types

| Event | Description |
|-------|-------------|
| `RunContent` | Content chunk from an agent step |
| `WorkflowAgentCompleted` | An agent step completed |

## AgentOSClient Methods

```python
from agno.client import AgentOSClient

client = AgentOSClient(base_url="http://localhost:7777")

# Discovery
config = await client.aget_config()  # config.workflows

# Non-streaming
result = await client.run_workflow(
    workflow_id=workflow_id,
    message="prompt",
)
# result.run_id, result.content

# Streaming — returns WorkflowRunOutputEvent objects
async for event in client.run_workflow_stream(
    workflow_id=workflow_id,
    message="prompt",
):
    if event.event == "RunContent" and hasattr(event, "content"):
        print(event.content, end="")
    elif event.event == "WorkflowAgentCompleted":
        print(f"Step completed: {event.content}")
```

## Important Notes

- Workflow streaming uses `event.event` string checks, not `isinstance()`
- Workflows execute steps sequentially — each step builds on the previous
- Steps can contain agents, teams, or custom function executors
- Workflow errors may occur at individual steps — check for errors per step
