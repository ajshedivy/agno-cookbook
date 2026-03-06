---
name: agno-memory
description: |
  Add persistent memory to Agno agents. Covers MemoryManager, agentic
  memory, shared memory between agents, multi-user sessions, and memory
  tools. Trigger this skill when: importing agno.memory, configuring
  MemoryManager, enabling agentic memory, or asking "how do I add memory
  to an agent?"
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["memory", "persistence", "agno", "user-preferences"]
---

# Add Memory to Agno Agents

Memory lets agents remember user-level facts (preferences, goals, context) across all sessions. Different from storage (conversation history).

## Quick Start

```python
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager

db = SqliteDb(db_file="tmp/agents.db")

memory_manager = MemoryManager(
    model="openai:gpt-4o",
    db=db,
)

agent = Agent(
    name="Memory Agent",
    model="openai:gpt-4o",
    db=db,
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_history_to_context=True,
    num_history_runs=5,
)

agent.print_response(
    "I prefer Python over JavaScript",
    user_id="user@example.com",
    stream=True,
)

# Retrieve stored memories
memories = agent.get_user_memories(user_id="user@example.com")
for m in memories:
    print(f"- {m.memory}")
```

## Memory vs Storage

| Feature | Memory | Storage |
|---------|--------|---------|
| Scope | User-level facts | Conversation history |
| Persistence | Across all sessions | Per session |
| Content | Preferences, goals, context | Chat messages |
| Parameter | `memory_manager=` | `db=` |

## MemoryManager Configuration

```python
from agno.memory import MemoryManager

memory_manager = MemoryManager(
    model="openai:gpt-4o",         # Model for memory extraction
    db=db,                          # Database to store memories
    additional_instructions="Capture user preferences and technical context.",
)
```

## Memory Modes

### Agentic Memory (Recommended)

The agent decides when to store/recall memories. More natural, fewer unnecessary writes:

```python
agent = Agent(
    model="openai:gpt-4o",
    memory_manager=memory_manager,
    enable_agentic_memory=True,     # Agent chooses when to use memory
    db=db,
)
```

### Always-On Memory

Run memory manager on every interaction. Guaranteed capture but slower:

```python
agent = Agent(
    model="openai:gpt-4o",
    memory_manager=memory_manager,
    update_memory_on_run=True,      # Always extract memories
    db=db,
)
```

## Memory with Custom Instructions

Guide what the memory manager captures:

```python
memory_manager = MemoryManager(
    model="openai:gpt-4o",
    db=db,
    additional_instructions=[
        "Capture the user's programming language preferences.",
        "Remember project names and tech stacks.",
        "Track dietary restrictions and food preferences.",
        "Ignore small talk and greetings.",
    ],
)
```

## Shared Memory Between Agents

Multiple agents can share the same memory store via the same `db` and `user_id`:

```python
db = SqliteDb(db_file="tmp/shared.db")

memory_manager = MemoryManager(model="openai:gpt-4o", db=db)

assistant = Agent(
    name="Assistant",
    model="openai:gpt-4o",
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    db=db,
)

researcher = Agent(
    name="Researcher",
    model="openai:gpt-4o",
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    db=db,
)

# Both agents access the same user memories
assistant.print_response("I work on the Acme project", user_id="alice", stream=True)
researcher.print_response("What project does the user work on?", user_id="alice", stream=True)
```

## Multi-User Sessions

Use `user_id` to isolate memories per user:

```python
agent.print_response("I like dark mode", user_id="alice", stream=True)
agent.print_response("I like light mode", user_id="bob", stream=True)

alice_memories = agent.get_user_memories(user_id="alice")
bob_memories = agent.get_user_memories(user_id="bob")
```

## Memory Tools

Give agents explicit tools to manage memories:

```python
from agno.tools.memory import MemoryTools

agent = Agent(
    model="openai:gpt-4o",
    tools=[MemoryTools()],
    db=db,
    memory_manager=memory_manager,
)
```

## Retrieving and Managing Memories

```python
# Get all memories for a user
memories = agent.get_user_memories(user_id="alice")

# Memories have structure
for m in memories:
    print(f"ID: {m.memory_id}")
    print(f"Content: {m.memory}")
    print(f"Topics: {m.topics}")
```

## Anti-Patterns

- **Don't confuse memory with storage** — memory is user-level facts, storage is chat history
- **Don't forget `user_id`** — without it, memories can't be isolated per user
- **Don't use `update_memory_on_run=True` with `enable_agentic_memory=True`** — pick one mode
- **Don't skip `db=`** — memories need a database backend to persist
- **Don't store sensitive data** — memories are plain text; avoid PII or secrets

## Further Reading

For custom memory managers and advanced patterns, read `references/api-patterns.md`.
