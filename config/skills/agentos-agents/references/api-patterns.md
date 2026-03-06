# AgentOS Agents API Reference

## Complete Agent Endpoints

### GET /agents
List all configured agents with metadata, model, tools, and settings.

**Response:** Array of `AgentResponse` objects.

### GET /agents/{agent_id}
Get detailed agent configuration and capabilities.

**Path Parameters:**
- `agent_id` (string, required): Agent identifier

**Response:** `AgentResponse` with fields:
- `id`, `name`, `db_id`, `description`, `role`
- `model`: `ModelResponse` (name, model, provider)
- `tools`, `sessions`, `knowledge`, `memory`, `reasoning`
- `default_tools`, `system_message`, `extra_messages`
- `response_settings`, `introduction`, `streaming`, `metadata`
- `input_schema`, `is_component`, `current_version`, `stage`

### POST /agents/{agent_id}/runs
Create a new agent run.

**Content-Type:** `application/x-www-form-urlencoded`

**Form Parameters:**
- `message` (string): The input prompt
- `stream` (boolean): Enable streaming (SSE)
- `user_id` (string): User identifier
- `session_id` (string): Session identifier for persistence
- `session_state` (JSON string): State to inject into the session
- `dependencies` (JSON string): Runtime parameters for tools
- `metadata` (JSON string): Custom metadata
- `output_schema` (JSON string): JSON schema for structured output
- `use_json_schema` (boolean): Preserve JSON formatting

**Non-Streaming Response:** Run result with `run_id`, `content`, `metrics`.

**Streaming Response (SSE):** Stream of events:
- `RunContentEvent`: Content chunks (`event.content`)
- `RunCompletedEvent`: Run finished (`event.run_id`)

### POST /agents/{agent_id}/runs/{run_id}/cancel
Cancel a running agent execution. Attempts graceful stop.

### POST /agents/{agent_id}/runs/continue
Continue a previously paused agent run.

## AgentOSClient Methods

```python
from agno.client import AgentOSClient

client = AgentOSClient(base_url="http://localhost:7777")

# Discovery
config = await client.aget_config()          # Returns config with agents list
agent = await client.aget_agent(agent_id)    # Returns AgentResponse

# Non-streaming execution
result = await client.run_agent(
    agent_id=agent_id,
    message="prompt",
    session_id="optional",
    user_id="optional",
    headers={"Authorization": "Bearer token"},
)
# result.run_id, result.content, result.metrics

# Streaming execution
async for event in client.run_agent_stream(
    agent_id=agent_id,
    message="prompt",
    session_id="optional",
    user_id="optional",
):
    if isinstance(event, RunContentEvent):
        print(event.content, end="")
    elif isinstance(event, RunCompletedEvent):
        print(f"Done: {event.run_id}")
```

## Authentication

All endpoints support optional `Authorization: Bearer <token>` header when security is configured.

## Error Responses

| Code | Description |
|------|-------------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Agent not found |
| 422 | Validation Error |
| 500 | Internal Server Error |

```python
from agno.client import RemoteServerUnavailableError

try:
    result = await client.run_agent(agent_id=agent_id, message="hello")
except RemoteServerUnavailableError as e:
    print(f"Server down: {e.message} at {e.base_url}")
```
