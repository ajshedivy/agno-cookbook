---
name: agno-storage
description: |
  Configure persistent storage backends for Agno agents and teams. Covers
  SQLite, PostgreSQL, Redis, MongoDB, and other backends for conversation
  history, session persistence, and state management. Trigger this skill
  when: importing agno.db, configuring agent storage, adding session
  persistence, or asking "how do I persist agent conversations?"
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["storage", "persistence", "database", "sessions", "agno"]
---

# Configure Agno Storage

Use `db=` on agents and teams to persist conversation history across runs. Install with `pip install agno`.

## Quick Start

```python
from agno.agent import Agent
from agno.db.sqlite import SqliteDb

db = SqliteDb(db_file="tmp/agents.db")

agent = Agent(
    name="Persistent Agent",
    model="openai:gpt-4o",
    db=db,
    add_history_to_context=True,
    num_history_runs=5,
)

# Same session_id = continuous conversation
agent.print_response("My name is Alice", session_id="session-1", stream=True)
agent.print_response("What's my name?", session_id="session-1", stream=True)
```

## Storage Backends

### SQLite (Development)

No server needed. Great for local development and prototyping:

```python
from agno.db.sqlite import SqliteDb

db = SqliteDb(db_file="tmp/agents.db")
```

### PostgreSQL (Production)

Full-featured relational storage for production deployments:

```python
from agno.db.postgres import PostgresDb

db = PostgresDb(
    db_url="postgresql+psycopg://user:pass@localhost:5432/mydb",
    table_name="agent_sessions",
)
```

### Redis

Fast in-memory storage for high-throughput scenarios:

```python
from agno.db.redis import RedisDb

db = RedisDb(
    prefix="agno:",
    host="localhost",
    port=6379,
    db=0,
)
```

### MongoDB

Document-oriented storage:

```python
from agno.db.mongo import MongoDb

db = MongoDb(
    db_url="mongodb://localhost:27017",
    db_name="agno",
    collection_name="sessions",
)
```

### MySQL

```python
from agno.db.mysql import MySQLDb

db = MySQLDb(
    db_url="mysql+pymysql://user:pass@localhost:3306/mydb",
    table_name="agent_sessions",
)
```

## Core Storage Parameters

```python
agent = Agent(
    model="openai:gpt-4o",
    db=db,                          # Storage backend
    add_history_to_context=True,    # Include past messages in context
    num_history_runs=5,             # Number of prior runs to include
)
```

## Session Management

Use `session_id` to maintain conversation threads:

```python
# Start a conversation
agent.print_response("Hello!", session_id="thread-42", stream=True)

# Continue the same conversation
agent.print_response("What did I just say?", session_id="thread-42", stream=True)

# Start a separate conversation
agent.print_response("Hello!", session_id="thread-99", stream=True)
```

## Session State

Store structured data that the agent can read and update:

```python
from agno.run import RunContext

def add_item(run_context: RunContext, item: str) -> str:
    """Add an item to the shopping list."""
    items = run_context.session_state.get("items", [])
    items.append(item)
    run_context.session_state["items"] = items
    return f"Added {item}"

agent = Agent(
    model="openai:gpt-4o",
    tools=[add_item],
    session_state={"items": []},
    add_session_state_to_context=True,
    db=db,
)
```

## Session Summaries

Summarize long conversations to save context window space:

```python
agent = Agent(
    model="openai:gpt-4o",
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
    enable_session_summaries=True,      # Summarize older messages
    session_summary_num_runs=5,         # Summarize after 5 runs
)
```

## Shared Storage for Teams

All team members can share one database:

```python
from agno.team.team import Team

db = SqliteDb(db_file="tmp/team.db")

agent1 = Agent(name="Agent 1", model="openai:gpt-4o", db=db)
agent2 = Agent(name="Agent 2", model="openai:gpt-4o", db=db)

team = Team(
    name="My Team",
    model="openai:gpt-4o",
    members=[agent1, agent2],
    db=db,
    add_history_to_context=True,
)
```

## Anti-Patterns

- **Don't forget `add_history_to_context=True`** — without it, the agent won't see past messages
- **Don't use SQLite in production** — use PostgreSQL or another production database
- **Don't skip `session_id`** — without it, each run is isolated
- **Don't set `num_history_runs` too high** — large histories waste context window tokens
- **Don't store secrets in session state** — it's persisted as plain text

## Further Reading

For advanced storage patterns and migration guides, read `references/api-patterns.md`.
