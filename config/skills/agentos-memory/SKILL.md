---
name: agentos-memory
description: |
  Interact with AgentOS Memory API endpoints using the AgentOSClient SDK.
  Covers creating, listing, getting, updating, and deleting user memories,
  plus retrieving memory topics and stats. Trigger this skill when:
  managing user memories via the API, using create_memory or list_memories,
  or asking "how do I manage memories through the API?"
license: Apache-2.0
metadata:
  version: "1.0.0"
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

## Create a Memory

```python
import asyncio
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    memory = await client.create_memory(
        memory="User prefers dark mode for all applications",
        user_id="user-123",
        topics=["preferences", "ui"],
    )

    print(f"Memory ID: {memory.memory_id}")
    print(f"Content: {memory.memory}")
    print(f"Topics: {memory.topics}")

asyncio.run(main())
```

## List Memories

```python
async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    memories = await client.list_memories(user_id="user-123")
    print(f"Found {len(memories.data)} memories")

    for mem in memories.data:
        print(f"  {mem.memory_id}: {mem.memory}")
```

The list endpoint supports filtering by:
- `user_id`: Filter by user
- `agent_id`: Filter by agent
- `team_id`: Filter by team
- `search_content`: Fuzzy search within memory content
- `topics`: Comma-separated topic filters
- `limit`, `page`: Pagination (default: 20 per page)
- `sort_by`, `sort_order`: Sorting (default: `updated_at` desc)

## Get a Specific Memory

```python
retrieved = await client.get_memory("memory-id-here", user_id="user-123")
print(f"Memory: {retrieved.memory}")
print(f"Topics: {retrieved.topics}")
```

## Update a Memory

```python
updated = await client.update_memory(
    memory_id="memory-id-here",
    memory="User strongly prefers dark mode for all applications and websites",
    user_id="user-123",
    topics=["preferences", "ui", "accessibility"],
)

print(f"Updated: {updated.memory}")
print(f"Topics: {updated.topics}")
```

## Delete a Memory

```python
await client.delete_memory("memory-id-here", user_id="user-123")
```

## Get Memory Topics

Retrieve all unique topics across all memories:

```python
topics = await client.get_memory_topics()
print(f"All topics: {topics}")
```

## Get User Memory Stats

Retrieve aggregated memory statistics:

```python
stats = await client.get_user_memory_stats()
print(f"Stats: {len(stats.data)} entries")
```

## Full Memory Lifecycle

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

- **Don't forget `user_id`** — memories are scoped to users
- **Don't skip topics** — topics enable filtering and categorization
- **Don't store conversation content as memories** — use sessions for that
- **Don't forget `update_memory_on_run=True`** on agents — required for automatic memory creation
- **Don't assume topics/stats endpoints exist** — they're optional and may not be available on all instances

## Further Reading

For advanced memory API patterns, read `references/api-patterns.md`.
