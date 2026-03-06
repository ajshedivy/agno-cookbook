# Memory API Patterns

## Full MemoryManager Constructor

```python
MemoryManager(
    model="openai:gpt-4o",                   # Model for memory extraction
    db=SqliteDb(db_file="agents.db"),         # Storage backend
    additional_instructions=[                  # Guide what to capture
        "Capture user preferences.",
        "Remember project context.",
    ],
)
```

## Memory Modes Comparison

| Mode | Parameter | Behavior |
|------|-----------|----------|
| Agentic | `enable_agentic_memory=True` | Agent decides when to store/recall |
| Always-On | `update_memory_on_run=True` | Extract memories every run |

## Memory Operations

```python
# Get all user memories
memories = agent.get_user_memories(user_id="alice")

# Memory object properties
for m in memories:
    m.memory_id   # Unique ID
    m.memory      # Content string
    m.topics      # List of topic tags
    m.user_id     # Associated user
```

## Memory with PostgreSQL (Production)

```python
from agno.db.postgres import PostgresDb

db = PostgresDb(
    db_url="postgresql+psycopg://user:pass@localhost:5432/mydb",
    table_name="agent_memories",
)

memory_manager = MemoryManager(model="openai:gpt-4o", db=db)
```

## Memory Tools

```python
from agno.tools.memory import MemoryTools

# Give agent explicit memory management tools
agent = Agent(
    model="openai:gpt-4o",
    tools=[MemoryTools()],
    memory_manager=memory_manager,
    db=db,
)
```

## Multi-Agent Shared Memory

```python
db = SqliteDb(db_file="shared.db")
memory_mgr = MemoryManager(model="openai:gpt-4o", db=db)

# Both agents share the same memory store
agent_a = Agent(model="openai:gpt-4o", memory_manager=memory_mgr, db=db,
                enable_agentic_memory=True)
agent_b = Agent(model="openai:gpt-4o", memory_manager=memory_mgr, db=db,
                enable_agentic_memory=True)

# Memories stored by agent_a are visible to agent_b for the same user_id
```

## Memory vs Session State

| Feature | Memory | Session State |
|---------|--------|--------------|
| Scope | User-level, cross-session | Single session |
| Managed by | MemoryManager (LLM) | Tools via RunContext |
| Use case | Preferences, goals | Shopping cart, counters |
| Parameter | `memory_manager=` | `session_state=` |
