---
name: agentos-api-memory
description: |
  Interact with AgentOS Memory API endpoints. For standard operations
  (listing, creating, updating, deleting memories, searching, topics),
  use the provided CLI script first. Only write custom Python when the
  script cannot handle the use case (e.g., advanced filtering, stats,
  chaining multiple calls, integration tests). Trigger when: managing
  user memories, writing scripts to manage user preferences, creating
  memory tests, or asking things like "what memories does this user
  have?" or "add a preference for dark mode."
license: Apache-2.0
metadata:
  version: "1.1.0"
  author: agno-team
  tags: ["agentos", "memory", "api", "client", "agno"]
---

# AgentOS Memory API

Use `agno.client.AgentOSClient` to create, list, update, and delete user memories on a remote AgentOS instance. Memories persist user preferences and facts across sessions.

## Prerequisites

Start an AgentOS server with memory enabled:

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager
from agno.os import AgentOS

db = SqliteDb(db_file="tmp/app.db")
agent = Agent(
    name="Assistant",
    model=Claude(id="claude-sonnet-4-5"),
    db=db,
    memory_manager=MemoryManager(model=Claude(id="claude-sonnet-4-5"), db=db),
    update_memory_on_run=True,
)

agent_os = AgentOS(agents=[agent])
agent_os.serve()
```

## Default: Use the CLI Script

**Always try the provided script first.** It covers listing, searching,
creating, updating, and deleting memories — plus listing topics — all from
the command line with no custom code needed.

The script is at: `scripts/manage_memories.py`

### List all memories for a user

```bash
uv run scripts/manage_memories.py --user-id alice@example.com
```

### Search memories by content

```bash
uv run scripts/manage_memories.py --user-id alice --search "dark mode"
```

### Create a new memory

```bash
uv run scripts/manage_memories.py --user-id alice \
  --create "User prefers dark mode" --topics preferences,ui
```

### Get a specific memory

```bash
uv run scripts/manage_memories.py --memory-id abc-123 --user-id alice
```

### Update a memory

```bash
uv run scripts/manage_memories.py --memory-id abc-123 --user-id alice \
  --update "User strongly prefers dark mode" --topics preferences,ui,accessibility
```

### Delete a memory

```bash
uv run scripts/manage_memories.py --memory-id abc-123 --user-id alice --delete
```

### List all memory topics

```bash
uv run scripts/manage_memories.py --topics-list
```

### Use a different server

```bash
uv run scripts/manage_memories.py --base-url http://my-server:8000 --user-id alice
```

### Full CLI reference

```
uv run scripts/manage_memories.py --help
```

## When to Write Custom Python

Only write ad-hoc Python when the CLI script cannot handle your use case:

- **Advanced list filtering** (by `agent_id`, `team_id`, topic filters, pagination, sorting)
- **Memory stats** (`get_user_memory_stats`)
- **Chaining multiple memory calls** in a single script
- **Custom error handling** or retry logic
- **Integration tests** that assert on memory content
- **Programmatic lifecycle orchestration** (create-then-update flows)

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/memories` | List memories (paginated, filterable) |
| GET | `/memories/{memory_id}` | Get memory by ID |
| GET | `/memories/topics` | Get all memory topics |
| GET | `/memories/stats` | Get user memory stats |
| POST | `/memories` | Create a memory |
| PATCH | `/memories/{memory_id}` | Update a memory |
| DELETE | `/memories/{memory_id}` | Delete a memory |

## Custom Python Examples

### List Memories with Advanced Filtering

The list endpoint supports filtering beyond what the CLI provides:

```python
import asyncio
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    memories = await client.list_memories(
        user_id="user-123",
        agent_id="my-agent",
        topics="preferences,ui",
        limit=50,
        page=2,
        sort_by="created_at",
        sort_order="asc",
    )
    print(f"Found {len(memories.data)} memories")

    for mem in memories.data:
        print(f"  {mem.memory_id}: {mem.memory}")

asyncio.run(main())
```

### Get User Memory Stats

Retrieve aggregated memory statistics:

```python
stats = await client.get_user_memory_stats()
print(f"Stats: {len(stats.data)} entries")
```

### Full Memory Lifecycle (Programmatic)

Chain multiple calls when you need create-then-verify flows:

```python
import asyncio
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")
    user_id = "demo-user"

    # Create
    memory = await client.create_memory(
        memory="Favorite color is blue",
        user_id=user_id,
        topics=["preferences"],
    )
    print(f"Created: {memory.memory_id}")

    # List
    memories = await client.list_memories(user_id=user_id)
    print(f"Total memories: {len(memories.data)}")

    # Update
    updated = await client.update_memory(
        memory_id=memory.memory_id,
        memory="Favorite color is dark blue",
        user_id=user_id,
        topics=["preferences", "colors"],
    )
    print(f"Updated: {updated.memory}")

    # Delete
    await client.delete_memory(memory.memory_id, user_id=user_id)
    print("Deleted")

asyncio.run(main())
```

## Memory vs Storage

- **Memory**: User preferences and facts ("what do I know about you?") — persists across sessions
- **Storage/Sessions**: Conversation history ("what did we discuss?") — tied to a session

## Anti-Patterns

- **Don't write custom Python for basic operations** — use the CLI script
- **Don't forget `user_id`** — memories are scoped to users
- **Don't skip topics** — topics enable filtering and categorization
- **Don't store conversation content as memories** — use sessions for that
- **Don't forget `update_memory_on_run=True`** on agents — required for automatic memory creation
- **Don't assume topics/stats endpoints exist** — they're optional and may not be available on all instances

## Further Reading

For advanced memory API patterns, read `references/api-patterns.md`.
