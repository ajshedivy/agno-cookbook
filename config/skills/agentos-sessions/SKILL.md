---
name: agentos-sessions
description: |
  Interact with AgentOS Session API endpoints using the AgentOSClient SDK.
  Covers creating, listing, getting, renaming, and deleting sessions,
  plus retrieving session runs. Trigger this skill when: managing
  sessions via the API, using session_id for persistent conversations,
  creating or deleting sessions, or asking "how do I manage sessions
  through the API?"
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["agentos", "sessions", "api", "client", "agno"]
---

# AgentOS Sessions API

Use `agno.client.AgentOSClient` to create, list, inspect, rename, and delete sessions on a remote AgentOS instance. Sessions maintain conversation history and context across runs.

## Prerequisites

Start an AgentOS server with storage configured:

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.db.sqlite import SqliteDb
from agno.os import AgentOS

db = SqliteDb(db_file="tmp/app.db")
agent = Agent(
    name="Assistant",
    model=Claude(id="claude-sonnet-4-5"),
    db=db,
    add_history_to_context=True,
    num_history_runs=5,
)

agent_os = AgentOS(agents=[agent])
agent_os.serve()
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/sessions` | List sessions (paginated, filterable) |
| GET | `/sessions/{session_id}` | Get session by ID |
| GET | `/sessions/{session_id}/runs` | Get session runs |
| GET | `/sessions/{session_id}/runs/{run_id}` | Get specific run |
| POST | `/sessions` | Create new session |
| PATCH | `/sessions/{session_id}` | Update session |
| POST | `/sessions/{session_id}/rename` | Rename session |
| DELETE | `/sessions/{session_id}` | Delete session |
| DELETE | `/sessions` | Delete multiple sessions |

## Create a Session

```python
import asyncio
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    config = await client.aget_config()
    agent_id = config.agents[0].id

    session = await client.create_session(
        agent_id=agent_id,
        user_id="user-123",
        session_name="My Research Session",
    )

    print(f"Session ID: {session.session_id}")
    print(f"Session Name: {session.session_name}")

asyncio.run(main())
```

## List Sessions

```python
async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    sessions = await client.get_sessions(user_id="user-123")
    print(f"Found {len(sessions.data)} sessions")

    for sess in sessions.data:
        print(f"  {sess.session_id}: {sess.session_name or 'Unnamed'}")
```

The list endpoint supports filtering by:
- `type`: Session type — `agent`, `team`, or `workflow`
- `component_id`: Filter by agent/team/workflow ID
- `user_id`: Filter by user
- `session_name`: Partial name match
- `limit`, `page`: Pagination (default: 20 per page)
- `sort_by`, `sort_order`: Sorting (default: `created_at` desc)

## Get Session Details

```python
async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    details = await client.get_session("session-id-here")
    print(f"Agent: {details.agent_id}")
    print(f"User: {details.user_id}")
    print(f"State: {details.session_state}")
```

## Get Session Runs

```python
async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    runs = await client.get_session_runs(session_id="session-id-here")
    print(f"Found {len(runs)} runs")

    for run in runs:
        preview = (str(run.content)[:50] + "...") if run.content else "N/A"
        print(f"  {run.run_id}: {preview}")
```

## Use Sessions for Persistent Conversations

```python
async def main():
    client = AgentOSClient(base_url="http://localhost:7777")
    config = await client.aget_config()
    agent_id = config.agents[0].id
    session_id = "persistent-session-1"

    # First message
    result1 = await client.run_agent(
        agent_id=agent_id,
        message="My name is Alice.",
        session_id=session_id,
    )

    # Second message — agent remembers
    result2 = await client.run_agent(
        agent_id=agent_id,
        message="What's my name?",
        session_id=session_id,
    )
    print(result2.content)  # Should mention Alice
```

## Rename a Session

```python
renamed = await client.rename_session(
    session_id="session-id-here",
    session_name="New Session Name",
)
print(f"Renamed to: {renamed.session_name}")
```

## Delete a Session

```python
# Delete a single session (permanent — removes all runs)
await client.delete_session("session-id-here")
```

## Anti-Patterns

- **Don't forget `db=` on agents** — without storage, sessions don't persist between API calls
- **Don't create sessions for every request** — use the same `session_id` for continuous conversations
- **Don't forget `add_history_to_context=True`** — without it, agents won't recall prior messages
- **Don't ignore pagination** — use `limit` and `page` when listing many sessions

## Further Reading

For advanced session management patterns, read `references/api-patterns.md`.
