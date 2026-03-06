# AgentOSClient API Reference

## Client Constructor

```python
from agno.client import AgentOSClient

client = AgentOSClient(
    base_url="http://localhost:7777",  # AgentOS server URL
)
```

## Discovery Methods

```python
# Get full configuration
config = await client.aget_config()
config.agents     # List of agent configs
config.teams      # List of team configs
config.workflows  # List of workflow configs
config.name       # App name
config.os_id      # App ID

# Get specific agent details
agent = await client.aget_agent(agent_id)
agent.name
agent.model
agent.tools
```

## Agent Execution

```python
# Non-streaming
result = await client.run_agent(
    agent_id="agent-id",
    message="Your prompt",
    session_id="optional-session",       # For persistent conversations
    user_id="optional-user",             # For user-specific memory
)

result.run_id       # Unique run identifier
result.content      # Response text
result.metrics      # Token usage (total_tokens, etc.)

# Streaming
async for event in client.run_agent_stream(
    agent_id="agent-id",
    message="Your prompt",
    session_id="optional-session",
):
    if isinstance(event, RunContentEvent):
        print(event.content, end="")
    elif isinstance(event, RunCompletedEvent):
        print(f"Done: {event.run_id}")
```

## Team Execution

```python
# Non-streaming
result = await client.run_team(
    team_id="team-id",
    message="Your prompt",
)

# Streaming
async for event in client.run_team_stream(
    team_id="team-id",
    message="Your prompt",
):
    ...
```

## Workflow Execution

```python
# Non-streaming
result = await client.run_workflow(
    workflow_id="workflow-id",
    message="Your prompt",
)

# Streaming
async for event in client.run_workflow_stream(
    workflow_id="workflow-id",
    message="Your prompt",
):
    ...
```

## Memory Operations

```python
# Create
memory = await client.create_memory(
    memory="User prefers concise responses",
    user_id="user-id",
    topics=["preferences"],
)

# List
memories = await client.list_memories(user_id="user-id")
for mem in memories.data:
    print(mem.memory_id, mem.memory)

# Get specific
memory = await client.get_memory(memory_id, user_id="user-id")

# Update
updated = await client.update_memory(
    memory_id=memory_id,
    memory="Updated memory content",
    user_id="user-id",
    topics=["preferences", "style"],
)

# Delete
await client.delete_memory(memory_id, user_id="user-id")

# Get topics
topics = await client.get_memory_topics()

# Get stats
stats = await client.get_user_memory_stats()
```

## Session Management

```python
# Get sessions for a user
sessions = await client.get_sessions(user_id="user-id")
```

## Authentication

```python
# Pass auth headers to individual calls
headers = {"Authorization": "Bearer your-jwt-token"}

# Headers can be passed to client methods that support them
result = await client.run_agent(
    agent_id="agent-id",
    message="Hello",
    headers=headers,
)
```

## Error Types

```python
from agno.client import RemoteServerUnavailableError

try:
    config = await client.aget_config()
except RemoteServerUnavailableError as e:
    print(f"Server unavailable: {e.message}")
    print(f"URL: {e.base_url}")
```

## Testing Best Practices

1. **Start server in a fixture**: Use `subprocess` or `pytest-docker` to spin up AgentOS
2. **Use unique session IDs**: Prevent test interference with `session_id=f"test-{uuid4()}"`
3. **Assert on content**: Check response content, not just that it's non-empty
4. **Test streaming and non-streaming**: Both paths should work
5. **Clean up memories**: Delete test memories in teardown
6. **Use timeouts**: Prevent hanging tests with `asyncio.wait_for()`
