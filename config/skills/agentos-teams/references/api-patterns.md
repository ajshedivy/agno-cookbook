# AgentOS Teams API Reference

## Complete Team Endpoints

### GET /teams
List all configured teams with members, model, tools, and settings.

**Response:** Array of `TeamResponse` objects with fields:
- `id`, `name`, `description`, `mode`, `role`, `db_id`
- `model`: `ModelResponse` (name, model, provider)
- `members`: Array of nested `AgentResponse` or `TeamResponse`
- `tools`, `knowledge`, `memory`, `reasoning`, `sessions`, `streaming`
- `system_message`, `response_settings`, `metadata`, `input_schema`
- `is_component`, `current_version`, `stage`

### GET /teams/{team_id}
Get detailed team configuration.

### POST /teams/{team_id}/runs
Create a new team run.

**Content-Type:** `application/x-www-form-urlencoded`

**Form Parameters:**
- `message` (string): The input prompt
- `stream` (boolean): Enable streaming (SSE)
- `user_id` (string): User identifier
- `session_id` (string): Session identifier
- `session_state` (JSON string): State to inject
- `dependencies` (JSON string): Runtime parameters
- `metadata` (JSON string): Custom metadata

**Non-Streaming Response:** Run result with `run_id`, `content`.

**Streaming Response (SSE):** Stream of events:
- `RunContentEvent`: Content chunks
- `RunCompletedEvent`: Run finished

### POST /teams/{team_id}/cancel_run
Cancel a running team execution. Attempts graceful stop.

## AgentOSClient Methods

```python
from agno.client import AgentOSClient
from agno.run.team import RunContentEvent, RunCompletedEvent

client = AgentOSClient(base_url="http://localhost:7777")

# Discovery
config = await client.aget_config()  # config.teams

# Non-streaming
result = await client.run_team(
    team_id=team_id,
    message="prompt",
    session_id="optional",
    user_id="optional",
)

# Streaming
async for event in client.run_team_stream(
    team_id=team_id,
    message="prompt",
):
    if isinstance(event, RunContentEvent):
        print(event.content, end="")
    elif isinstance(event, RunCompletedEvent):
        print(f"Done: {event.run_id}")
```

## Important Notes

- Team streaming events import from `agno.run.team`, not `agno.run.agent`
- Teams coordinate multiple agents — each member processes its part
- Session persistence works the same way as agents — use `session_id`
