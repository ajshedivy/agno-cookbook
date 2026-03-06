---
name: agentos-api-sessions
description: |
  Interact with AgentOS Session API endpoints. For standard operations
  (listing, creating, renaming, deleting sessions, viewing runs), use
  the provided CLI script first. Only write custom Python when the script
  cannot handle the use case (e.g., persistent conversations, clearing
  history, bulk deletion, advanced filtering). Trigger when: managing
  sessions remotely, inspecting session history, creating session tests,
  or asking things like "find me all sessions from the researcher agent"
  or "get the latest runs from session X."
license: Apache-2.0
metadata:
  version: "1.1.0"
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

## Default: Use the CLI Script

**Always try the provided script first.** It covers listing sessions, creating
sessions, inspecting session details, viewing runs, renaming, and deleting —
all from the command line with no custom code needed.

The script is at: `scripts/manage_sessions.py`

### List all sessions

```bash
uv run scripts/manage_sessions.py --base-url http://localhost:7777
```

### List sessions for a specific agent

```bash
uv run scripts/manage_sessions.py --base-url http://localhost:7777 \
  --agent-id researcher
```

### List sessions for a specific user

```bash
uv run scripts/manage_sessions.py --base-url http://localhost:7777 \
  --user-id alice@example.com
```

### Inspect a session

```bash
uv run scripts/manage_sessions.py --base-url http://localhost:7777 \
  --session-id abc-123
```

### Show runs inside a session

```bash
uv run scripts/manage_sessions.py --base-url http://localhost:7777 \
  --session-id abc-123 --show-runs
```

### Create a new session

```bash
uv run scripts/manage_sessions.py --base-url http://localhost:7777 \
  --create --agent-id my-agent --user-id alice --name "Research Chat"
```

### Rename a session

```bash
uv run scripts/manage_sessions.py --base-url http://localhost:7777 \
  --session-id abc-123 --rename "New Name"
```

### Delete a session

```bash
uv run scripts/manage_sessions.py --base-url http://localhost:7777 \
  --session-id abc-123 --delete
```

### Full CLI reference

```
uv run scripts/manage_sessions.py --help
```

## When to Write Custom Python

Only write ad-hoc Python when the CLI script cannot handle your use case:

- **Persistent conversations** (running an agent within a session across multiple messages)
- **Clearing session history** while keeping the session intact
- **Bulk deletion** of multiple sessions at once
- **Advanced filtering** (by type, session name, sorting, pagination)
- **Updating session metadata** (PATCH endpoint)
- **Fetching a specific run** by run ID
- **Custom error handling** or retry logic
- **Integration tests** that assert on session or run content

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
| POST | `/sessions/{session_id}/clear` | Clear session history |
| DELETE | `/sessions` | Delete multiple sessions |

## Custom Python Examples

### Use Sessions for Persistent Conversations

```python
import asyncio
from agno.client import AgentOSClient

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

asyncio.run(main())
```

### Clear Session History

Erase all conversation history while keeping the session:

```python
await client.clear_session("session-id-here")
```

### Advanced Filtering

The list endpoint supports filtering beyond what the CLI provides:

```python
async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    sessions = await client.get_sessions(
        type="agent",
        session_name="Research",
        sort_by="created_at",
        sort_order="asc",
        limit=50,
        page=2,
    )
    for sess in sessions.data:
        print(f"  {sess.session_id}: {sess.session_name or 'Unnamed'}")
```

## Anti-Patterns

- **Don't write custom Python for basic operations** — use the CLI script for listing, creating, inspecting, renaming, and deleting sessions
- **Don't forget `db=` on agents** — without storage, sessions don't persist between API calls
- **Don't create sessions for every request** — use the same `session_id` for continuous conversations
- **Don't forget `add_history_to_context=True`** — without it, agents won't recall prior messages
- **Don't ignore pagination** — use `limit` and `page` when listing many sessions

## Further Reading

For advanced session management patterns, read `references/api-patterns.md`.
