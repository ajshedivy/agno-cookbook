---
name: agentos-api-teams
description: |
  Interact with AgentOS Team API endpoints. For standard operations
  (listing teams, running teams, streaming), use the provided CLI
  script first. Only write custom Python when the script cannot handle
  the use case (e.g., cancellation, chaining multiple calls, custom
  error handling). Trigger when: running teams remotely, listing teams,
  creating team tests, or asking things like "what teams do I have
  configured?" or "run a task on my research team."
license: Apache-2.0
metadata:
  version: "1.1.0"
  author: agno-team
  tags: ["agentos", "teams", "api", "client", "agno"]
---

# AgentOS Teams API

## Prerequisites

Start an AgentOS server with teams configured:

```bash
export ANTHROPIC_API_KEY=sk-...
uv run start_agentos.py  # See agno-agentos skill
```

## Default: Use the CLI Script

**Always try the provided script first.** It covers listing teams, running
teams (streaming and non-streaming), and session persistence — all from the
command line with no custom code needed.

The script is at: `scripts/run_teams.py`

### List all teams

```bash
uv run scripts/run_teams.py --base-url http://localhost:7777
```

### Run a team with a message

```bash
uv run scripts/run_teams.py --base-url http://localhost:7777 \
  --team-id research-team \
  -m "Compare Python and Rust"
```

### Stream a response

```bash
uv run scripts/run_teams.py --base-url http://localhost:7777 \
  --team-id research-team \
  -m "Analyze Tesla stock" --stream
```

### Persistent sessions

```bash
uv run scripts/run_teams.py --base-url http://localhost:7777 \
  --team-id research-team \
  -m "Analyze NVIDIA" --session-id research-1

uv run scripts/run_teams.py --base-url http://localhost:7777 \
  --team-id research-team \
  -m "Now compare to AMD" --session-id research-1
```

### Run against a remote server

```bash
uv run scripts/run_teams.py --base-url http://my-server:8000 \
  -m "Research AI trends"
```

### Full CLI reference

```
uv run scripts/run_teams.py --help
```

## When to Write Custom Python

Only write ad-hoc Python when the CLI script cannot handle your use case:

- **Cancel a team run** mid-execution
- **Chaining multiple team calls** in a single script
- **Custom error handling** or retry logic
- **Programmatic inspection** of team config (members, model, description)
- **Integration tests** that assert on response content
- **Authentication** with custom headers (e.g., JWT tokens)

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/teams` | List all teams |
| GET | `/teams/{team_id}` | Get team details |
| POST | `/teams/{team_id}/runs` | Create team run |
| POST | `/teams/{team_id}/cancel_run` | Cancel team run |

## Custom Python Examples

### Cancel Team Run

```python
await client.cancel_team_run(
    team_id=team_id,
    run_id=run_id,
)
```

### Authentication

When the AgentOS instance has a security key configured:

```python
result = await client.run_team(
    team_id=team_id,
    message="Research topic",
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
- **Don't hardcode team IDs** — discover them from `aget_config()` or the CLI script
- **Don't confuse team and agent imports** — teams use `from agno.run.team import RunContentEvent`
- **Don't skip discovery** — always call `aget_config()` first to verify teams exist
- **Don't forget the server** — start AgentOS before running client code

## Further Reading

For advanced team API patterns, read `references/api-patterns.md`.
