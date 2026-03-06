---
name: agentos-api-teams
description: |
  Interact with AgentOS Team API endpoints using the AgentOSClient SDK.
  Use this skill to write ad-hoc Python scripts, tests, and automation
  for listing teams, running teams (streaming and non-streaming), and
  cancelling team runs. Trigger when: importing AgentOSClient to work
  with teams, writing scripts to run teams remotely, creating team tests,
  or asking things like "what teams do I have configured?" or "run a
  task on my research team."
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["agentos", "teams", "api", "client", "agno"]
---

# AgentOS Teams API

Use `agno.client.AgentOSClient` to list, inspect, and run teams on a remote AgentOS instance. Install with `pip install agno`.

## Prerequisites

Start an AgentOS server with teams configured:

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.team.team import Team
from agno.os import AgentOS

assistant = Agent(name="Assistant", model=Claude(id="claude-sonnet-4-5"))
researcher = Agent(name="Researcher", model=Claude(id="claude-sonnet-4-5"))

team = Team(
    name="Research Team",
    model=Claude(id="claude-sonnet-4-5"),
    members=[assistant, researcher],
)

agent_os = AgentOS(agents=[assistant, researcher], teams=[team])
agent_os.serve()
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/teams` | List all teams |
| GET | `/teams/{team_id}` | Get team details |
| POST | `/teams/{team_id}/runs` | Create team run |
| POST | `/teams/{team_id}/cancel_run` | Cancel team run |

## List All Teams

```python
import asyncio
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    config = await client.aget_config()
    for team in config.teams or []:
        print(f"Team: {team.id} — {team.name}")

asyncio.run(main())
```

## Run Team (Non-Streaming)

```python
import asyncio
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    config = await client.aget_config()
    if not config.teams:
        print("No teams available")
        return

    team_id = config.teams[0].id

    result = await client.run_team(
        team_id=team_id,
        message="Research and summarize quantum computing advances.",
        user_id="user-123",
        session_id="team-session-1",
    )

    print(f"Run ID: {result.run_id}")
    print(f"Content: {result.content}")

asyncio.run(main())
```

## Run Team (Streaming)

```python
import asyncio
from agno.client import AgentOSClient
from agno.run.team import RunContentEvent, RunCompletedEvent

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    config = await client.aget_config()
    team_id = config.teams[0].id

    async for event in client.run_team_stream(
        team_id=team_id,
        message="Compare Python and Rust for backend development.",
    ):
        if isinstance(event, RunContentEvent):
            print(event.content, end="", flush=True)
        elif isinstance(event, RunCompletedEvent):
            print(f"\nDone! Run ID: {event.run_id}")

asyncio.run(main())
```

## Cancel Team Run

```python
await client.cancel_team_run(
    team_id=team_id,
    run_id=run_id,
)
```

## Team Run with Session Persistence

```python
session_id = "team-research-session"

# First message
result1 = await client.run_team(
    team_id=team_id,
    message="Analyze Tesla's market position.",
    session_id=session_id,
    user_id="analyst",
)

# Second message — team remembers context
result2 = await client.run_team(
    team_id=team_id,
    message="Now compare that to Rivian.",
    session_id=session_id,
    user_id="analyst",
)
```

## Authentication

```python
result = await client.run_team(
    team_id=team_id,
    message="Research topic",
    headers={"Authorization": "Bearer your-jwt-token"},
)
```

## Anti-Patterns

- **Don't forget `await`** — all client methods are async
- **Don't hardcode team IDs** — discover them from `aget_config()`
- **Don't confuse team and agent imports** — teams use `from agno.run.team import RunContentEvent`
- **Don't skip config check** — verify `config.teams` is not empty before running

## Further Reading

For advanced team API patterns, read `references/api-patterns.md`.
