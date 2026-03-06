---
name: agno-agent
description: |
  Build single Agno agents with tools, structured output, storage, memory,
  knowledge bases, guardrails, and human-in-the-loop confirmation. Trigger
  this skill when: importing agno.agent, creating an Agent instance, adding
  tools to an agent, configuring agent storage/memory, or asking "how do I
  build an agent with Agno?"
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["agent", "agno", "ai", "tools", "structured-output"]
---

# Build Agno Agents

Use `agno.agent.Agent` to create AI agents. Install with `pip install agno`.

## Quick Start

```python
from agno.agent import Agent
from agno.models.anthropic import Claude

agent = Agent(
    name="My Agent",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=["Be concise.", "Use tables for data."],
    markdown=True,
)

agent.print_response("Hello!", stream=True)
```

## Core Agent Parameters

```python
Agent(
    name="Agent Name",
    model=Claude(id="claude-sonnet-4-5"),     # Required: model provider
    instructions="System prompt or list",      # str or list[str]
    tools=[ToolKit(), func],                   # Tools the agent can call
    markdown=True,                             # Format output as markdown
    show_tool_calls=True,                      # Display tool invocations
    add_datetime_to_context=True,              # Inject current datetime
    add_history_to_context=True,               # Include conversation history
    num_history_runs=5,                        # How many prior runs to include
    db=SqliteDb(db_file="agent.db"),           # Persistent storage backend
)
```

## Agent with Tools

Give agents tools to interact with external data and services.

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.yfinance import YFinanceTools

agent = Agent(
    name="Finance Agent",
    model=Claude(id="claude-sonnet-4-5"),
    tools=[YFinanceTools()],
    instructions="You are a data-driven financial analyst.",
    add_datetime_to_context=True,
    markdown=True,
)

agent.print_response("Give me a quick investment brief on NVIDIA", stream=True)
```

## Structured Output

Use `output_schema` with a Pydantic model to get typed responses.

```python
from typing import List, Optional
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.yfinance import YFinanceTools

class StockAnalysis(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")
    current_price: float = Field(..., description="Current price in USD")
    summary: str = Field(..., description="One-line summary")
    key_risks: List[str] = Field(..., description="2-3 key risks")
    recommendation: str = Field(..., description="Buy, Hold, or Sell")

agent = Agent(
    name="Analyst",
    model=Claude(id="claude-sonnet-4-5"),
    tools=[YFinanceTools()],
    output_schema=StockAnalysis,
    markdown=True,
)

response = agent.run("Analyze NVIDIA")
analysis: StockAnalysis = response.content
print(f"Price: ${analysis.current_price:.2f}")
print(f"Recommendation: {analysis.recommendation}")
```

## Typed Input and Output

Use `input_schema` + `output_schema` for end-to-end type safety.

```python
from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.models.anthropic import Claude

class AnalysisRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")
    analysis_type: Literal["quick", "deep"] = Field(default="quick")

class AnalysisResult(BaseModel):
    ticker: str
    summary: str
    recommendation: str

agent = Agent(
    name="Typed Agent",
    model=Claude(id="claude-sonnet-4-5"),
    input_schema=AnalysisRequest,
    output_schema=AnalysisResult,
)

# Pass input as dict or Pydantic model
response = agent.run(input={"ticker": "NVDA", "analysis_type": "deep"})
result: AnalysisResult = response.content
```

## Storage (Persistent Conversations)

Add `db=` to persist conversation history across runs. Use `session_id` to maintain conversation threads.

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.db.sqlite import SqliteDb

agent = Agent(
    name="Persistent Agent",
    model=Claude(id="claude-sonnet-4-5"),
    db=SqliteDb(db_file="tmp/agents.db"),
    add_history_to_context=True,
    num_history_runs=5,
)

# Same session_id = continuous conversation
agent.print_response("Hello!", session_id="my-session", stream=True)
agent.print_response("What did I just say?", session_id="my-session", stream=True)
```

## Memory (User Preferences)

Memory persists user-level facts across all sessions. Different from storage (conversation history).

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager

db = SqliteDb(db_file="tmp/agents.db")

memory_manager = MemoryManager(
    model=Claude(id="claude-sonnet-4-5"),
    db=db,
    additional_instructions="Capture user preferences and goals.",
)

agent = Agent(
    name="Memory Agent",
    model=Claude(id="claude-sonnet-4-5"),
    db=db,
    memory_manager=memory_manager,
    enable_agentic_memory=True,    # Agent decides when to store/recall
    # OR: update_memory_on_run=True  # Always run memory manager (guaranteed but slower)
    add_history_to_context=True,
    num_history_runs=5,
)

agent.print_response("I prefer tech stocks", user_id="user@example.com", stream=True)
memories = agent.get_user_memories(user_id="user@example.com")
```

## State Management

Use `session_state` for structured data the agent actively manages (watchlists, counters, flags).

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.db.sqlite import SqliteDb
from agno.run import RunContext

def add_item(run_context: RunContext, item: str) -> str:
    """Add an item to the list."""
    items = run_context.session_state.get("items", [])
    items.append(item)
    run_context.session_state["items"] = items
    return f"Added {item}. Total: {len(items)}"

agent = Agent(
    name="Stateful Agent",
    model=Claude(id="claude-sonnet-4-5"),
    tools=[add_item],
    session_state={"items": []},
    add_session_state_to_context=True,
    db=SqliteDb(db_file="tmp/agents.db"),
    instructions="Current items: {items}",  # State injected into instructions
)
```

Access state: `agent.get_session_state()` or `response.session_state`.

## Knowledge Base

Give agents searchable document collections using vector databases.

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.db.sqlite import SqliteDb
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.vectordb.chroma import ChromaDb
from agno.vectordb.search import SearchType

db = SqliteDb(db_file="tmp/agents.db")

knowledge = Knowledge(
    name="My Docs",
    vector_db=ChromaDb(
        name="docs",
        collection="docs",
        path="tmp/chromadb",
        persistent_client=True,
        search_type=SearchType.hybrid,
        embedder=GeminiEmbedder(id="gemini-embedding-001"),
    ),
    max_results=5,
    contents_db=db,
)

agent = Agent(
    name="Knowledge Agent",
    model=Claude(id="claude-sonnet-4-5"),
    knowledge=knowledge,
    search_knowledge=True,  # Agent searches knowledge automatically
    db=db,
)

# Load documents
knowledge.insert(name="Docs", url="https://docs.agno.com/introduction.md")
agent.print_response("What is Agno?", stream=True)
```

## Guardrails

Validate input before processing using `pre_hooks`.

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.guardrails import PIIDetectionGuardrail, PromptInjectionGuardrail
from agno.guardrails.base import BaseGuardrail
from agno.exceptions import InputCheckError
from agno.run.agent import RunInput

class SpamGuardrail(BaseGuardrail):
    def check(self, run_input):
        content = run_input.input_content_string()
        if content.count("!") > 5:
            raise InputCheckError("Input appears to be spam")

    async def async_check(self, run_input):
        self.check(run_input)

agent = Agent(
    name="Safe Agent",
    model=Claude(id="claude-sonnet-4-5"),
    pre_hooks=[
        PIIDetectionGuardrail(),
        PromptInjectionGuardrail(),
        SpamGuardrail(),
    ],
)
```

## Human-in-the-Loop

Require user confirmation before executing sensitive tools.

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools import tool

@tool(requires_confirmation=True)
def delete_record(record_id: str) -> str:
    """Delete a record. Requires user confirmation."""
    return f"Deleted record {record_id}"

agent = Agent(
    name="Careful Agent",
    model=Claude(id="claude-sonnet-4-5"),
    tools=[delete_record],
)

response = agent.run("Delete record ABC-123")

# Check for pending confirmations
if response.active_requirements:
    for req in response.active_requirements:
        if req.needs_confirmation:
            req.confirm()  # or req.reject()

    # Resume execution
    response = agent.continue_run(
        run_id=response.run_id,
        requirements=response.requirements,
    )
```

## Model Providers

Swap models by changing the import and model ID:

```python
from agno.models.anthropic import Claude
model = Claude(id="claude-sonnet-4-5")

from agno.models.openai import OpenAIChat
model = OpenAIChat(id="gpt-4o")

from agno.models.google import Gemini
model = Gemini(id="gemini-2.0-flash")

from agno.models.ollama import Ollama
model = Ollama(id="llama3.3")
```

## Anti-Patterns

- **Don't forget `add_history_to_context=True`** if you want conversational agents that remember prior messages
- **Don't skip `db=`** if you want sessions to persist across script restarts
- **Don't hardcode model IDs** without showing how to swap them — use a config pattern
- **Don't use `OpenAIChat`** when you want the newer Responses API — use `OpenAIResponses` instead
- **Don't use blocking calls in async contexts** — use `agent.arun()` and `agent.aprint_response()` for async
- **Don't forget to install extras**: `pip install "agno[anthropic]"` for Claude, `pip install "agno[openai]"` for OpenAI

## Further Reading

For extended API patterns and advanced configuration, read `references/api-patterns.md`.
