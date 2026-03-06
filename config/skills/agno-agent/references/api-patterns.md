# Agno Agent API Reference

## Full Agent Constructor Parameters

```python
Agent(
    # Identity
    name="Agent Name",                         # Display name
    agent_id="unique-id",                      # Unique identifier (auto-generated if omitted)
    role="Describe the agent's role",          # Used in team contexts
    description="What this agent does",        # Used for routing decisions

    # Model
    model=Claude(id="claude-sonnet-4-5"),      # Any agno.models.* provider

    # Instructions
    instructions="System prompt",              # str or list[str]
    # instructions=["Rule 1.", "Rule 2."],     # List form

    # Tools
    tools=[ToolKit(), function_tool],          # Toolkit instances or plain functions

    # Output
    markdown=True,                             # Format as markdown
    show_tool_calls=True,                      # Show tool call details
    output_schema=PydanticModel,               # Structured output (Pydantic model)
    input_schema=InputModel,                   # Typed input (Pydantic model)

    # Context
    add_datetime_to_context=True,              # Inject current datetime
    add_history_to_context=True,               # Include conversation history
    num_history_runs=5,                        # Number of prior runs in context

    # Storage
    db=SqliteDb(db_file="agent.db"),           # Storage backend
    enable_session_summaries=True,             # Summarize sessions

    # Memory
    memory_manager=MemoryManager(...),         # Memory extraction manager
    enable_agentic_memory=True,                # Agent-driven memory (efficient)
    update_memory_on_run=True,                 # Always update memory (guaranteed)

    # State
    session_state={"key": "value"},            # Initial session state dict
    add_session_state_to_context=True,         # Inject state into instructions

    # Knowledge
    knowledge=Knowledge(...),                  # Knowledge base
    search_knowledge=True,                     # Auto-search knowledge

    # Guardrails
    pre_hooks=[GuardrailInstance()],            # Input validation hooks

    # Skills
    skills=Skills(loaders=[LocalSkills(...)]), # Agent skills
)
```

## Model Provider Imports

```python
# Anthropic (Claude)
from agno.models.anthropic import Claude
model = Claude(id="claude-sonnet-4-5")
model = Claude(id="claude-sonnet-4-5")
model = Claude(id="claude-haiku-4-5-20251001")

# OpenAI
from agno.models.openai import OpenAIChat
model = OpenAIChat(id="gpt-4o")
model = OpenAIChat(id="gpt-4o-mini")

# OpenAI Responses API (newer)
from agno.models.openai import OpenAIResponses
model = OpenAIResponses(id="gpt-4o")

# Google Gemini
from agno.models.google import Gemini
model = Gemini(id="gemini-2.0-flash")

# Ollama (local)
from agno.models.ollama import Ollama
model = Ollama(id="llama3.3")

# AWS Bedrock
from agno.models.aws import AwsBedrock
model = AwsBedrock(id="anthropic.claude-3-sonnet-20240229-v1:0")

# Azure OpenAI
from agno.models.azure import AzureOpenAI
model = AzureOpenAI(id="gpt-4o", azure_endpoint="...", api_version="...")

# Groq
from agno.models.groq import Groq
model = Groq(id="llama-3.3-70b-versatile")
```

## Storage Backends

```python
# SQLite (development / single-server)
from agno.db.sqlite import SqliteDb
db = SqliteDb(db_file="tmp/agents.db")

# PostgreSQL (production / multi-server)
from agno.db.postgres import PostgresDb
db = PostgresDb(db_url="postgresql+psycopg://user:pass@host:5432/dbname")
```

## Vector Database Options

```python
# ChromaDB (local, easy setup)
from agno.vectordb.chroma import ChromaDb
vector_db = ChromaDb(
    name="my_collection",
    collection="my_collection",
    path="tmp/chromadb",
    persistent_client=True,
    search_type=SearchType.hybrid,
    embedder=GeminiEmbedder(id="gemini-embedding-001"),
)

# PgVector (PostgreSQL, production)
from agno.vectordb.pgvector import PgVector
vector_db = PgVector(
    table_name="embeddings",
    db_url="postgresql+psycopg://user:pass@host:5432/dbname",
    embedder=OpenAIEmbedder(id="text-embedding-3-small"),
)

# LanceDB (serverless, local)
from agno.vectordb.lancedb import LanceDb
vector_db = LanceDb(
    table_name="embeddings",
    uri="tmp/lancedb",
    embedder=OpenAIEmbedder(id="text-embedding-3-small"),
)
```

## Embedder Options

```python
from agno.knowledge.embedder.google import GeminiEmbedder
embedder = GeminiEmbedder(id="gemini-embedding-001")

from agno.knowledge.embedder.openai import OpenAIEmbedder
embedder = OpenAIEmbedder(id="text-embedding-3-small")
```

## Knowledge Loading Methods

```python
from agno.knowledge.knowledge import Knowledge

knowledge = Knowledge(
    name="My Knowledge",
    vector_db=vector_db,
    max_results=5,
    contents_db=db,
)

# Load from URL
knowledge.insert(name="Docs", url="https://example.com/docs.md")

# Load from file
knowledge.insert(name="PDF", path="path/to/document.pdf")

# Load from text
knowledge.insert(name="Notes", text_content="Content here...")
```

## Running Agents

```python
# Sync
agent.print_response("prompt", stream=True)           # Print streamed output
response = agent.run("prompt")                          # Get RunResponse
response = agent.run("prompt", session_id="session-1")  # With session
response = agent.run(input={"key": "value"})            # Typed input

# Async
await agent.aprint_response("prompt", stream=True)
response = await agent.arun("prompt")
```

## RunResponse Object

```python
response = agent.run("prompt")
response.content        # str or Pydantic model (if output_schema set)
response.run_id         # Unique run identifier
response.session_id     # Session identifier
response.metrics        # Token usage metrics
response.session_state  # Current session state dict
response.active_requirements  # Pending confirmations (human-in-the-loop)
```

## Reasoning Tools

Add chain-of-thought reasoning to any agent:

```python
from agno.tools.reasoning import ReasoningTools

agent = Agent(
    model=Claude(id="claude-sonnet-4-5"),
    tools=[ReasoningTools(add_instructions=True)],
)
```
