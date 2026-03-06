# AgentOS Memory API Reference

## Complete Memory Endpoints

### GET /memories
List memories with pagination, filtering, and search.

**Query Parameters:**
- `user_id` (string): Filter by user
- `agent_id` (string): Filter by agent
- `team_id` (string): Filter by team
- `search_content` (string): Fuzzy search within memory content
- `topics` (array): Comma-separated topic filters
- `limit` (integer, default: 20): Items per page
- `page` (integer, default: 1): Page number
- `sort_by` (string, default: `updated_at`): Sort field
- `sort_order` (string, default: `desc`): Sort direction
- `db_id` (string): Database ID
- `table` (string): Database table

**Response:** `PaginatedResponse[UserMemorySchema]`
- `data`: Array of memories (`memory_id`, `memory`, `topics`, `agent_id`, `team_id`, `user_id`, `updated_at`)
- `meta`: Pagination info

### GET /memories/{memory_id}
Get a specific memory by ID.

### GET /memories/topics
Get all unique topics across all memories.

### GET /memories/stats
Get aggregated user memory statistics.

### POST /memories
Create a new memory.

**Body Parameters:**
- `memory` (string): Memory content
- `user_id` (string): User who owns the memory
- `topics` (array): Topic tags

### PATCH /memories/{memory_id}
Update an existing memory.

**Body Parameters:**
- `memory` (string): Updated content
- `user_id` (string): User ID
- `topics` (array): Updated topics

### DELETE /memories/{memory_id}
Delete a specific memory.

## AgentOSClient Methods

```python
from agno.client import AgentOSClient

client = AgentOSClient(base_url="http://localhost:7777")

# Create
memory = await client.create_memory(
    memory="User prefers concise responses",
    user_id="user-id",
    topics=["preferences"],
)
# memory.memory_id, memory.memory, memory.topics

# List
memories = await client.list_memories(user_id="user-id")
# memories.data — list of UserMemorySchema

# Get
memory = await client.get_memory("memory-id", user_id="user-id")

# Update
updated = await client.update_memory(
    memory_id="memory-id",
    memory="Updated content",
    user_id="user-id",
    topics=["preferences", "style"],
)

# Delete
await client.delete_memory("memory-id", user_id="user-id")

# Topics (optional endpoint)
topics = await client.get_memory_topics()

# Stats (optional endpoint)
stats = await client.get_user_memory_stats()
```

## Memory Schema

```python
# UserMemorySchema
{
    "memory_id": "uuid-string",
    "memory": "Memory content text",
    "topics": ["topic1", "topic2"],
    "agent_id": "agent-id or null",
    "team_id": "team-id or null",
    "user_id": "user-id",
    "updated_at": "2025-01-01T00:00:00Z"
}
```
