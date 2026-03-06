# AgentOS Sessions API Reference

## Complete Session Endpoints

### GET /sessions
List sessions with pagination, filtering, and sorting.

**Query Parameters:**
- `type` (string): Session type — `agent`, `team`, or `workflow` (default: `agent`)
- `component_id` (string): Filter by agent/team/workflow ID
- `user_id` (string): Filter by user ID
- `session_name` (string): Partial name match
- `limit` (integer, default: 20): Items per page
- `page` (integer, default: 1): Page number
- `sort_by` (string, default: `created_at`): Sort field
- `sort_order` (string, default: `desc`): Sort direction
- `db_id` (string): Database ID
- `table` (string): Database table name

**Response:** `PaginatedResponse[SessionSchema]`
- `data`: Array of sessions (`session_id`, `session_name`, `session_state`, `created_at`, `updated_at`)
- `meta`: Pagination info (`page`, `limit`, `total_pages`, `total_count`, `search_time_ms`)

### GET /sessions/{session_id}
Get session details by ID.

### GET /sessions/{session_id}/runs
Get all runs in a session.

### GET /sessions/{session_id}/runs/{run_id}
Get a specific run by ID within a session.

### POST /sessions
Create a new session.

**Body Parameters:**
- `agent_id` (string): Agent to associate with
- `user_id` (string): User who owns the session
- `session_name` (string): Human-readable name

### PATCH /sessions/{session_id}
Update session properties.

### POST /sessions/{session_id}/rename
Rename a session.

**Body Parameters:**
- `session_name` (string): New name

### DELETE /sessions/{session_id}
Permanently delete a session and all associated runs.

### DELETE /sessions
Delete multiple sessions.

## AgentOSClient Methods

```python
from agno.client import AgentOSClient

client = AgentOSClient(base_url="http://localhost:7777")

# Create
session = await client.create_session(
    agent_id="agent-id",
    user_id="user-id",
    session_name="Session Name",
)
# session.session_id, session.session_name

# List
sessions = await client.get_sessions(user_id="user-id")
# sessions.data — list of SessionSchema

# Get details
details = await client.get_session("session-id")
# details.agent_id, details.user_id, details.session_state

# Get runs
runs = await client.get_session_runs(session_id="session-id")
# list of run objects with run_id, content

# Rename
renamed = await client.rename_session(
    session_id="session-id",
    session_name="New Name",
)

# Delete
await client.delete_session("session-id")
```

## Session Types

Sessions can be associated with agents, teams, or workflows:
- `type=agent` — Agent sessions (default)
- `type=team` — Team sessions
- `type=workflow` — Workflow sessions
